#!/usr/bin/env python3
"""
Scribe API Connector for Enzo Health

Fetches visit notes from the Scribe API and saves them to the clinical-qa workspace.
Handles authentication, pagination, rate limiting, and state management.

Usage:
    python scribe_connector.py --agency-id SUNRISE
    python scribe_connector.py --agency-id SUNRISE --since-last-run
    python scribe_connector.py --agency-id SUNRISE --dry-run
    python scribe_connector.py --agency-id SUNRISE --from 2026-01-01 --to 2026-03-31
"""

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List
import time

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError


# ============================================================================
# Configuration
# ============================================================================

# Base URL and API key from environment
SCRIBE_BASE_URL = os.environ.get('ENZO_SCRIBE_BASE_URL', '').rstrip('/')
API_KEY = os.environ.get('ENZO_API_KEY', '')

# Paths relative to workspace
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
NOTES_DIR = WORKSPACE_ROOT / 'clinical-qa' / 'notes'
LOGS_DIR = Path(__file__).parent / 'logs'
STATE_FILE = Path(__file__).parent / '.scribe_state.json'

# Rate limiting and retry configuration
MAX_RETRIES = 3
INITIAL_BACKOFF = 1  # seconds
MAX_BACKOFF = 32  # seconds
REQUEST_TIMEOUT = 30  # seconds
RATE_LIMIT_RETRY_AFTER = 60  # seconds

# Pagination
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(log_file: Optional[Path] = None) -> logging.Logger:
    """Configure logging to file and console."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    if log_file is None:
        log_file = LOGS_DIR / 'scribe_pull.log'

    logger = logging.getLogger('scribe_connector')
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
# State Management
# ============================================================================

def read_state() -> Dict[str, Any]:
    """Read the last run state from file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Failed to read state file: {e}")
    return {}


def write_state(state: Dict[str, Any]) -> None:
    """Write state to file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to write state file: {e}")


def get_last_run_timestamp(agency_id: str) -> Optional[datetime]:
    """Get the timestamp of the last successful pull for an agency."""
    state = read_state()
    agency_state = state.get(agency_id, {})
    last_run_str = agency_state.get('last_run')

    if last_run_str:
        try:
            return datetime.fromisoformat(last_run_str)
        except ValueError:
            return None
    return None


def update_last_run(agency_id: str, timestamp: datetime) -> None:
    """Update the last run timestamp for an agency."""
    state = read_state()
    if agency_id not in state:
        state[agency_id] = {}
    state[agency_id]['last_run'] = timestamp.isoformat()
    write_state(state)


# ============================================================================
# API Client
# ============================================================================

class ScribeAPIClient:
    """Client for the Scribe API with auth, pagination, and retry logic."""

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
            base_url: Base URL for the API (e.g., https://api.enzo.health)
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
            'User-Agent': 'Enzo-Scribe-Connector/1.0'
        })

    def _should_retry(self, status_code: int) -> bool:
        """Determine if a request should be retried based on status code."""
        # Retry on server errors and rate limiting
        return status_code in [429, 500, 502, 503, 504]

    def _calculate_backoff(self, attempt: int) -> int:
        """Calculate exponential backoff time."""
        backoff = min(INITIAL_BACKOFF * (2 ** attempt), MAX_BACKOFF)
        # Add jitter
        jitter = backoff * 0.1 * (hash(str(time.time())) % 100) / 100
        return int(backoff + jitter)

    def get_notes(
        self,
        agency_id: str,
        from_date: datetime,
        to_date: datetime,
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> List[Dict[str, Any]]:
        """
        Fetch visit notes from the API with pagination.

        Args:
            agency_id: Agency ID to filter by
            from_date: Start date (inclusive)
            to_date: End date (inclusive)
            page_size: Results per page

        Returns:
            List of note documents

        Raises:
            RequestException: If API request fails after retries
        """
        all_notes = []
        offset = 0

        from_str = from_date.strftime('%Y-%m-%d')
        to_str = to_date.strftime('%Y-%m-%d')

        self.logger.info(
            f"Fetching notes for agency {agency_id} from {from_str} to {to_str}"
        )

        while True:
            attempt = 0
            while attempt <= self.max_retries:
                try:
                    url = f"{self.base_url}/api/v1/notes"
                    params = {
                        'from': from_str,
                        'to': to_str,
                        'agency_id': agency_id,
                        'offset': offset,
                        'limit': page_size
                    }

                    self.logger.debug(
                        f"Request: GET {url} | offset={offset}, limit={page_size}"
                    )

                    resp = self.session.get(
                        url,
                        params=params,
                        timeout=self.timeout
                    )

                    if resp.status_code == 200:
                        data = resp.json()
                        notes = data.get('notes', [])
                        total = data.get('total', 0)

                        if not notes:
                            self.logger.info(f"Fetched {len(all_notes)} total notes")
                            return all_notes

                        all_notes.extend(notes)
                        self.logger.debug(
                            f"Page {offset // page_size + 1}: {len(notes)} notes "
                            f"(total so far: {len(all_notes)}/{total})"
                        )

                        offset += page_size
                        break

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

            if attempt > self.max_retries:
                raise RequestException(
                    f"Max retries exceeded fetching notes at offset {offset}"
                )

    def close(self) -> None:
        """Close the session."""
        self.session.close()


# ============================================================================
# File Operations
# ============================================================================

def save_note(note: Dict[str, Any], notes_dir: Path) -> str:
    """
    Save a note to a file with standardized naming.

    Args:
        note: Note document from API
        notes_dir: Directory to save to

    Returns:
        Path to saved file
    """
    # Extract key fields
    patient_id = note.get('patient_id', 'UNKNOWN')
    note_date = note.get('visit_date', datetime.now().date()).split('T')[0]

    # Standardize patient ID format
    patient_id = str(patient_id).replace(' ', '').upper()
    if not patient_id.startswith('PT'):
        patient_id = f'PT{patient_id}'

    # Create filename: YYYY-MM-DD-{patient_id}-note.md
    filename = f"{note_date}-{patient_id}-note.md"
    filepath = notes_dir / filename

    notes_dir.mkdir(parents=True, exist_ok=True)

    # Save as markdown
    with open(filepath, 'w') as f:
        f.write("# Visit Note\n\n")
        f.write(f"**Patient ID:** {note.get('patient_id', 'N/A')}\n")
        f.write(f"**Visit Date:** {note.get('visit_date', 'N/A')}\n")
        f.write(f"**Clinician:** {note.get('clinician_name', 'N/A')}\n")
        f.write(f"**Agency:** {note.get('agency_id', 'N/A')}\n\n")

        f.write("## Clinical Documentation\n\n")
        f.write(note.get('transcribed_note', 'No content available.'))
        f.write("\n\n---\n\n")
        f.write(f"*Captured: {note.get('created_at', 'N/A')}*\n")

    return str(filepath)


# ============================================================================
# Main Logic
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fetch visit notes from Scribe API and save to workspace',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scribe_connector.py --agency-id SUNRISE
  python scribe_connector.py --agency-id SUNRISE --since-last-run
  python scribe_connector.py --agency-id SUNRISE --dry-run
  python scribe_connector.py --agency-id SUNRISE --from 2026-01-01 --to 2026-03-31
        """
    )

    parser.add_argument(
        '--agency-id',
        required=True,
        help='Agency ID to fetch notes for'
    )
    parser.add_argument(
        '--from',
        dest='from_date',
        type=str,
        help='Start date (YYYY-MM-DD). Default: 30 days ago'
    )
    parser.add_argument(
        '--to',
        dest='to_date',
        type=str,
        help='End date (YYYY-MM-DD). Default: today'
    )
    parser.add_argument(
        '--since-last-run',
        action='store_true',
        help='Fetch only notes since last successful pull'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fetched without writing files'
    )
    parser.add_argument(
        '--page-size',
        type=int,
        default=DEFAULT_PAGE_SIZE,
        help=f'Results per page (default: {DEFAULT_PAGE_SIZE})'
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("Scribe API Connector Started")
    logger.info("=" * 70)

    # Validate API credentials
    if not SCRIBE_BASE_URL:
        logger.error("ENZO_SCRIBE_BASE_URL environment variable not set")
        return 1
    if not API_KEY:
        logger.error("ENZO_API_KEY environment variable not set")
        return 1

    # Determine date range
    if args.since_last_run:
        last_run = get_last_run_timestamp(args.agency_id)
        if last_run:
            from_date = last_run
            logger.info(f"Using last run timestamp: {from_date.isoformat()}")
        else:
            from_date = datetime.now(timezone.utc) - timedelta(days=30)
            logger.info(f"No previous run found. Using 30-day default: {from_date.date()}")
    elif args.from_date:
        from_date = datetime.fromisoformat(args.from_date).replace(tzinfo=timezone.utc)
    else:
        from_date = datetime.now(timezone.utc) - timedelta(days=30)

    if args.to_date:
        to_date = datetime.fromisoformat(args.to_date).replace(tzinfo=timezone.utc)
    else:
        to_date = datetime.now(timezone.utc)

    logger.info(f"Date range: {from_date.date()} to {to_date.date()}")
    logger.info(f"Agency ID: {args.agency_id}")
    logger.info(f"Dry run: {args.dry_run}")

    try:
        # Create API client
        client = ScribeAPIClient(SCRIBE_BASE_URL, API_KEY, logger)

        # Fetch notes
        notes = client.get_notes(
            args.agency_id,
            from_date,
            to_date,
            page_size=args.page_size
        )
        client.close()

        logger.info(f"Fetched {len(notes)} notes")

        if not notes:
            logger.info("No notes to process")
            return 0

        # Process notes
        saved_count = 0
        if args.dry_run:
            logger.info("[DRY RUN] Would save the following notes:")
            for i, note in enumerate(notes, 1):
                patient_id = note.get('patient_id', 'UNKNOWN')
                visit_date = note.get('visit_date', 'N/A')
                logger.info(f"  {i}. {patient_id} ({visit_date})")
        else:
            for note in notes:
                try:
                    filepath = save_note(note, NOTES_DIR)
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Failed to save note: {e}")

        # Log summary
        logger.info("=" * 70)
        logger.info("Scribe API Pull Summary")
        logger.info("=" * 70)
        logger.info(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
        logger.info(f"Agency: {args.agency_id}")
        logger.info(f"Notes fetched: {len(notes)}")
        logger.info(f"Notes saved: {saved_count}")
        logger.info(f"Date range: {from_date.date()} to {to_date.date()}")

        # Update state if not a dry run
        if not args.dry_run and notes:
            update_last_run(args.agency_id, datetime.now(timezone.utc))
            logger.info("State file updated with latest run timestamp")

        logger.info("=" * 70)

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        logger.error("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
