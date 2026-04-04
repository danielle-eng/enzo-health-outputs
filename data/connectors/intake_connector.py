#!/usr/bin/env python3
"""
Intake API Connector for Enzo Health

Fetches patient census and episode data from the Intake API and transforms it
into QAPI CSV format.

Usage:
    python intake_connector.py --agency-id SUNRISE
    python intake_connector.py --agency-id SUNRISE --from 2026-01-01 --to 2026-03-31
    python intake_connector.py --agency-id SUNRISE --dry-run
"""

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import time

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError


# ============================================================================
# Configuration
# ============================================================================

# Base URLs and API key from environment
INTAKE_BASE_URL = os.environ.get('ENZO_INTAKE_BASE_URL', '').rstrip('/')
API_KEY = os.environ.get('ENZO_API_KEY', '')

# Paths relative to workspace
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / 'data'
LOGS_DIR = Path(__file__).parent / 'logs'

# Rate limiting and retry configuration
MAX_RETRIES = 3
INITIAL_BACKOFF = 1  # seconds
MAX_BACKOFF = 32  # seconds
REQUEST_TIMEOUT = 30  # seconds

# Pagination
DEFAULT_PAGE_SIZE = 100


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(log_file: Optional[Path] = None) -> logging.Logger:
    """Configure logging to file and console."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    if log_file is None:
        log_file = LOGS_DIR / 'intake_pull.log'

    logger = logging.getLogger('intake_connector')
    logger.setLevel(logging.DEBUG)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# ============================================================================
# API Client
# ============================================================================

class IntakeAPIClient:
    """Client for the Intake API with auth, pagination, and retry logic."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        logger: logging.Logger,
        timeout: int = REQUEST_TIMEOUT,
        max_retries: int = MAX_RETRIES
    ):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
            logger: Logger instance
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.logger = logger
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        """Configure session with default headers and auth."""
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Enzo-Intake-Connector/1.0'
        })

    def _should_retry(self, status_code: int) -> bool:
        """Determine if a request should be retried."""
        return status_code in [429, 500, 502, 503, 504]

    def _calculate_backoff(self, attempt: int) -> int:
        """Calculate exponential backoff time."""
        backoff = min(INITIAL_BACKOFF * (2 ** attempt), MAX_BACKOFF)
        jitter = backoff * 0.1 * (hash(str(time.time())) % 100) / 100
        return int(backoff + jitter)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            RequestException: If request fails after retries
        """
        url = f"{self.base_url}{endpoint}"
        attempt = 0

        while attempt <= self.max_retries:
            try:
                self.logger.debug(f"Request: {method} {url} | params={params}")

                if method == 'GET':
                    resp = self.session.get(url, params=params, timeout=self.timeout)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                if resp.status_code == 200:
                    return resp.json()

                elif self._should_retry(resp.status_code):
                    backoff = self._calculate_backoff(attempt)
                    self.logger.warning(
                        f"Got {resp.status_code}. Retrying in {backoff}s "
                        f"(attempt {attempt + 1}/{self.max_retries + 1})"
                    )
                    time.sleep(backoff)
                    attempt += 1

                else:
                    self.logger.error(
                        f"API error {resp.status_code}: {resp.text[:200]}"
                    )
                    resp.raise_for_status()

            except (ConnectionError, Timeout) as e:
                backoff = self._calculate_backoff(attempt)
                self.logger.warning(
                    f"Connection error: {e}. Retrying in {backoff}s "
                    f"(attempt {attempt + 1}/{self.max_retries + 1})"
                )
                time.sleep(backoff)
                attempt += 1

            except RequestException as e:
                self.logger.error(f"Request failed: {e}")
                raise

        raise RequestException(f"Max retries exceeded for {url}")

    def get_patients(
        self,
        agency_id: str,
        status: str = 'active',
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> List[Dict[str, Any]]:
        """
        Fetch active patients (census).

        Args:
            agency_id: Agency ID to filter by
            status: Patient status (active, discharged, all)
            page_size: Results per page

        Returns:
            List of patient documents
        """
        all_patients = []
        offset = 0

        self.logger.info(f"Fetching patients (status={status}) for agency {agency_id}")

        while True:
            params = {
                'agency_id': agency_id,
                'status': status,
                'offset': offset,
                'limit': page_size
            }

            resp = self._make_request('GET', '/api/v1/patients', params)
            patients = resp.get('patients', [])
            total = resp.get('total', 0)

            if not patients:
                self.logger.info(f"Fetched {len(all_patients)} total patients")
                return all_patients

            all_patients.extend(patients)
            self.logger.debug(
                f"Page {offset // page_size + 1}: {len(patients)} patients "
                f"(total so far: {len(all_patients)}/{total})"
            )

            offset += page_size

    def get_episodes(
        self,
        agency_id: str,
        from_date: datetime,
        to_date: datetime,
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> List[Dict[str, Any]]:
        """
        Fetch episode data (admissions and discharges).

        Args:
            agency_id: Agency ID to filter by
            from_date: Start date (inclusive)
            to_date: End date (inclusive)
            page_size: Results per page

        Returns:
            List of episode documents
        """
        all_episodes = []
        offset = 0

        from_str = from_date.strftime('%Y-%m-%d')
        to_str = to_date.strftime('%Y-%m-%d')

        self.logger.info(
            f"Fetching episodes for agency {agency_id} from {from_str} to {to_str}"
        )

        while True:
            params = {
                'agency_id': agency_id,
                'from': from_str,
                'to': to_str,
                'offset': offset,
                'limit': page_size
            }

            resp = self._make_request('GET', '/api/v1/episodes', params)
            episodes = resp.get('episodes', [])
            total = resp.get('total', 0)

            if not episodes:
                self.logger.info(f"Fetched {len(all_episodes)} total episodes")
                return all_episodes

            all_episodes.extend(episodes)
            self.logger.debug(
                f"Page {offset // page_size + 1}: {len(episodes)} episodes "
                f"(total so far: {len(all_episodes)}/{total})"
            )

            offset += page_size

    def close(self) -> None:
        """Close the session."""
        self.session.close()


# ============================================================================
# Data Transformation
# ============================================================================

def validate_icd10_code(code: str, logger: logging.Logger) -> Tuple[bool, str]:
    """
    Validate an ICD-10 code using the available MCP tool.

    For now, returns a basic format check. In production, this would call
    the ICD-10 validation service.

    Args:
        code: ICD-10 code to validate
        logger: Logger instance

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not code or code.upper() in ('', 'N/A', 'UNKNOWN'):
        return True, ""

    # Basic format check: ICD-10-CM format is letter followed by 2 digits
    # then optional decimals (e.g., E11.65)
    code = code.strip().upper()
    if len(code) < 3:
        return False, f"Code too short: {code}"

    # TODO: Call ICD-10 validation MCP tool when available
    # For now, just check basic format
    if not code[0].isalpha():
        return False, f"Code must start with letter: {code}"

    return True, ""


def transform_to_qapi_csv(
    patients: List[Dict[str, Any]],
    episodes: List[Dict[str, Any]],
    logger: logging.Logger
) -> List[Dict[str, str]]:
    """
    Transform API data into QAPI CSV format.

    Maps Intake API responses to QAPI columns:
    PatientID, AdmissionDate, DischargeDate, Payer, PrimaryDiagnosisICD10,
    PrimaryDiagnosisDescription, Hospitalization, HospitalizationDate,
    EDVisit, DischargeDisposition, OASISSOCDate, OASISDCDate,
    TimelyInitiation, Notes

    Args:
        patients: List of patient documents
        episodes: List of episode documents
        logger: Logger instance

    Returns:
        List of dictionaries ready for CSV output
    """
    rows = []
    icd10_warnings = []

    # Create a map of patient ID -> episodes for faster lookup
    episodes_by_patient = {}
    for episode in episodes:
        patient_id = episode.get('patient_id')
        if patient_id not in episodes_by_patient:
            episodes_by_patient[patient_id] = []
        episodes_by_patient[patient_id].append(episode)

    for patient in patients:
        patient_id = patient.get('patient_id', '')
        primary_dx = patient.get('primary_diagnosis_icd10', '')
        primary_dx_desc = patient.get('primary_diagnosis_description', '')

        # Validate ICD-10 code
        is_valid, error_msg = validate_icd10_code(primary_dx, logger)
        if not is_valid:
            warning = f"Patient {patient_id}: {error_msg}"
            icd10_warnings.append(warning)
            logger.warning(f"ICD-10 validation: {warning}")

        # Map patient payer type
        payer = patient.get('payer_type', 'Other')
        payer_map = {
            'medicare': 'Medicare',
            'medicaid': 'Medicaid',
            'private': 'Private',
            'other': 'Other'
        }
        payer = payer_map.get(payer.lower(), 'Other')

        # Get episodes for this patient (latest episode)
        patient_episodes = episodes_by_patient.get(patient_id, [])
        if patient_episodes:
            # Sort by admission date descending and take most recent
            episode = sorted(
                patient_episodes,
                key=lambda e: e.get('admission_date', ''),
                reverse=True
            )[0]
        else:
            episode = {}

        # Build QAPI row
        row = {
            'PatientID': patient_id,
            'AdmissionDate': episode.get('admission_date', ''),
            'DischargeDate': episode.get('discharge_date', ''),
            'Payer': payer,
            'PrimaryDiagnosisICD10': primary_dx,
            'PrimaryDiagnosisDescription': primary_dx_desc,
            'Hospitalization': '1' if episode.get('had_hospitalization', False) else '0',
            'HospitalizationDate': episode.get('hospitalization_date', ''),
            'EDVisit': '1' if episode.get('had_ed_visit', False) else '0',
            'DischargeDisposition': episode.get('discharge_disposition', ''),
            'OASISSOCDate': episode.get('oasis_soc_date', ''),
            'OASISDCDate': episode.get('oasis_dc_date', ''),
            'TimelyInitiation': '1' if episode.get('timely_initiation', False) else '0',
            'Notes': patient.get('notes', '')
        }

        rows.append(row)

    if icd10_warnings:
        logger.warning(f"Found {len(icd10_warnings)} ICD-10 code warnings")

    return rows


def save_qapi_csv(
    rows: List[Dict[str, str]],
    agency_id: str,
    output_dir: Path = DATA_DIR
) -> str:
    """
    Save transformed data to QAPI CSV file.

    Args:
        rows: List of row dictionaries
        agency_id: Agency ID for filename
        output_dir: Directory to save to

    Returns:
        Path to saved file
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Filename: YYYY-MM-DD-{agency_id}-census.csv
    today = datetime.now().date()
    filename = f"{today.isoformat()}-{agency_id}-census.csv"
    filepath = output_dir / filename

    # QAPI column order
    fieldnames = [
        'PatientID',
        'AdmissionDate',
        'DischargeDate',
        'Payer',
        'PrimaryDiagnosisICD10',
        'PrimaryDiagnosisDescription',
        'Hospitalization',
        'HospitalizationDate',
        'EDVisit',
        'DischargeDisposition',
        'OASISSOCDate',
        'OASISDCDate',
        'TimelyInitiation',
        'Notes'
    ]

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return str(filepath)


# ============================================================================
# Main Logic
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fetch patient data from Intake API and save as QAPI CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python intake_connector.py --agency-id SUNRISE
  python intake_connector.py --agency-id SUNRISE --from 2026-01-01 --to 2026-03-31
  python intake_connector.py --agency-id SUNRISE --dry-run
        """
    )

    parser.add_argument(
        '--agency-id',
        required=True,
        help='Agency ID to fetch data for'
    )
    parser.add_argument(
        '--from',
        dest='from_date',
        type=str,
        help='Start date (YYYY-MM-DD). Default: start of current quarter'
    )
    parser.add_argument(
        '--to',
        dest='to_date',
        type=str,
        help='End date (YYYY-MM-DD). Default: today'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fetched without writing files'
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("Intake API Connector Started")
    logger.info("=" * 70)

    # Validate API credentials
    if not INTAKE_BASE_URL:
        logger.error("ENZO_INTAKE_BASE_URL environment variable not set")
        return 1
    if not API_KEY:
        logger.error("ENZO_API_KEY environment variable not set")
        return 1

    # Determine date range
    today = datetime.now(timezone.utc)
    if args.from_date:
        from_date = datetime.fromisoformat(args.from_date).replace(tzinfo=timezone.utc)
    else:
        # Start of current quarter
        if today.month <= 3:
            from_date = datetime(today.year, 1, 1, tzinfo=timezone.utc)
        elif today.month <= 6:
            from_date = datetime(today.year, 4, 1, tzinfo=timezone.utc)
        elif today.month <= 9:
            from_date = datetime(today.year, 7, 1, tzinfo=timezone.utc)
        else:
            from_date = datetime(today.year, 10, 1, tzinfo=timezone.utc)

    if args.to_date:
        to_date = datetime.fromisoformat(args.to_date).replace(tzinfo=timezone.utc)
    else:
        to_date = today

    logger.info(f"Date range: {from_date.date()} to {to_date.date()}")
    logger.info(f"Agency ID: {args.agency_id}")
    logger.info(f"Dry run: {args.dry_run}")

    try:
        # Create API client
        client = IntakeAPIClient(INTAKE_BASE_URL, API_KEY, logger)

        # Fetch data
        patients = client.get_patients(args.agency_id)
        logger.info(f"Fetched {len(patients)} patients")

        episodes = client.get_episodes(args.agency_id, from_date, to_date)
        logger.info(f"Fetched {len(episodes)} episodes")

        client.close()

        if not patients:
            logger.info("No patients to process")
            return 0

        # Transform data
        rows = transform_to_qapi_csv(patients, episodes, logger)

        # Log summary
        logger.info("=" * 70)
        logger.info("Intake Data Processing Summary")
        logger.info("=" * 70)
        logger.info(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
        logger.info(f"Agency: {args.agency_id}")
        logger.info(f"Patients: {len(patients)}")
        logger.info(f"Episodes: {len(episodes)}")
        logger.info(f"QAPI rows: {len(rows)}")

        # Save or show output
        if args.dry_run:
            logger.info("[DRY RUN] Would save the following rows:")
            for i, row in enumerate(rows[:5], 1):
                logger.info(f"  {i}. {row['PatientID']} ({row['Payer']})")
            if len(rows) > 5:
                logger.info(f"  ... and {len(rows) - 5} more rows")
        else:
            filepath = save_qapi_csv(rows, args.agency_id)
            logger.info(f"Saved to: {filepath}")

        logger.info("=" * 70)

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        logger.error("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
