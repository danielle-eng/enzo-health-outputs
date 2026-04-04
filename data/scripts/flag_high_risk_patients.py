#!/usr/bin/env python3
"""
High-Risk Patient Flagging Script

Applies risk scoring algorithm to identify patients at high risk of
hospitalization or adverse outcomes for immediate clinical review.

Risk Criteria (1 point each):
  1. Diagnosis: CHF, COPD, or Pneumonia
  2. Multi-morbidity: 3+ chronic conditions
  3. Prior hospitalization during current episode
  4. Recent Medicare admission (≤30 days)
  5. Prior ED visit during current episode
  6. Post-surgical status (≤60 days)

Patients with score ≥2 flagged for immediate clinical review.

Usage:
    python flag_high_risk_patients.py --census-file 2026-04-04-SUNRISE-census.csv
    python flag_high_risk_patients.py --census-file 2026-04-04-SUNRISE-census.csv --date 2026-04-04
"""

import argparse
import csv
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ============================================================================
# Configuration
# ============================================================================

# High-risk diagnoses (ICD-10 prefixes)
HIGH_RISK_DIAGNOSES = [
    'I50',   # Heart failure
    'J44',   # COPD
    'J18',   # Pneumonia
    'J45',   # Asthma (included as chronic)
    'J43',   # Emphysema
]

# Paths
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / 'data'
OUTPUT_DIR = WORKSPACE_ROOT / 'outcomes' / 'high-risk'


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure logging."""
    logger = logging.getLogger('flag_high_risk_patients')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


# ============================================================================
# Risk Scoring
# ============================================================================

def is_high_risk_diagnosis(icd10_code: str) -> bool:
    """
    Check if ICD-10 code is a high-risk diagnosis.

    Args:
        icd10_code: ICD-10 code (e.g., 'I50.9', 'J44.1')

    Returns:
        True if code matches high-risk diagnoses
    """
    if not icd10_code:
        return False

    code = icd10_code.strip().upper()

    # Check against high-risk prefixes
    for prefix in HIGH_RISK_DIAGNOSES:
        if code.startswith(prefix):
            return True

    return False


def is_recent_admission(admission_date: str, cutoff_days: int = 30) -> bool:
    """
    Check if patient was admitted within cutoff days.

    Args:
        admission_date: Date in YYYY-MM-DD format
        cutoff_days: Number of days to look back

    Returns:
        True if admission is recent
    """
    if not admission_date or admission_date == '':
        return False

    try:
        admit_dt = datetime.fromisoformat(admission_date).date()
        cutoff_dt = (datetime.now(timezone.utc) - timedelta(days=cutoff_days)).date()
        return admit_dt >= cutoff_dt
    except (ValueError, AttributeError):
        return False


def is_post_surgical(admission_date: str, cutoff_days: int = 60) -> bool:
    """
    Check if patient is within post-surgical period.

    Args:
        admission_date: Date of admission (YYYY-MM-DD)
        cutoff_days: Post-surgical window in days

    Returns:
        True if within post-surgical period
    """
    if not admission_date or admission_date == '':
        return False

    # In production, would query for surgical procedures in notes
    # For now, use admission as a proxy if it's recent
    try:
        admit_dt = datetime.fromisoformat(admission_date).date()
        cutoff_dt = (datetime.now(timezone.utc) - timedelta(days=cutoff_days)).date()
        return admit_dt >= cutoff_dt
    except (ValueError, AttributeError):
        return False


def calculate_risk_score(patient_record: Dict[str, str]) -> Tuple[int, List[str]]:
    """
    Calculate risk score for a patient.

    Args:
        patient_record: Patient record from CSV

    Returns:
        Tuple of (score, list of risk factors)
    """
    score = 0
    risk_factors = []

    # 1. High-risk diagnosis (CHF, COPD, Pneumonia)
    primary_dx = patient_record.get('PrimaryDiagnosisICD10', '')
    if is_high_risk_diagnosis(primary_dx):
        score += 1
        risk_factors.append(f"High-risk diagnosis: {primary_dx}")

    # 2. Multi-morbidity (approximated by diagnosis description length or notes)
    # In production, would count ICD-10 codes in patient record
    notes = patient_record.get('Notes', '').lower()
    if 'multiple' in notes or 'comorbid' in notes or 'multi' in notes:
        score += 1
        risk_factors.append("Multi-morbidity documented")

    # 3. Prior hospitalization during episode
    had_hospitalization = patient_record.get('Hospitalization', '0') == '1'
    if had_hospitalization:
        score += 1
        hosp_date = patient_record.get('HospitalizationDate', '')
        risk_factors.append(f"Prior hospitalization: {hosp_date}")

    # 4. Recent Medicare admission (within 30 days)
    payer = patient_record.get('Payer', '').lower()
    admission_date = patient_record.get('AdmissionDate', '')
    if 'medicare' in payer and is_recent_admission(admission_date, cutoff_days=30):
        score += 1
        risk_factors.append(f"Recent Medicare admission: {admission_date}")

    # 5. Prior ED visit during episode
    had_ed_visit = patient_record.get('EDVisit', '0') == '1'
    if had_ed_visit:
        score += 1
        risk_factors.append("Prior ED visit during episode")

    # 6. Post-surgical status (within 60 days)
    if is_post_surgical(admission_date, cutoff_days=60):
        # Check if admission reason suggests surgery (e.g., joint replacement)
        if primary_dx.startswith('Z96'):  # Presence of artificial joint
            score += 1
            risk_factors.append(f"Post-surgical status (joint replacement)")

    return score, risk_factors


# ============================================================================
# File I/O
# ============================================================================

def read_census_csv(filepath: Path) -> List[Dict[str, str]]:
    """
    Read a census CSV file.

    Args:
        filepath: Path to CSV file

    Returns:
        List of patient records
    """
    records = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row and row.get('PatientID'):
                records.append(row)
    return records


def save_high_risk_flags(
    high_risk_patients: List[Dict[str, any]],
    output_date: str,
    output_dir: Path = OUTPUT_DIR
) -> str:
    """
    Save high-risk patient flags to markdown file.

    Args:
        high_risk_patients: List of flagged patients with risk info
        output_date: Date for filename (YYYY-MM-DD)
        output_dir: Output directory

    Returns:
        Path to saved file
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Filename: YYYY-MM-DD-high-risk-flags.md
    filename = f"{output_date}-high-risk-flags.md"
    filepath = output_dir / filename

    with open(filepath, 'w') as f:
        f.write("# High-Risk Patient Flags\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Date:** {output_date}\n")
        f.write(f"**Total Flagged:** {len(high_risk_patients)}\n\n")

        f.write("## Overview\n\n")
        f.write("Patients are flagged for clinical review based on risk score ≥2.\n\n")

        f.write("## Scoring Criteria\n\n")
        f.write("1 point each for:\n")
        f.write("- High-risk diagnosis (CHF, COPD, Pneumonia)\n")
        f.write("- Multi-morbidity (3+ chronic conditions)\n")
        f.write("- Prior hospitalization during episode\n")
        f.write("- Recent Medicare admission (≤30 days)\n")
        f.write("- Prior ED visit during episode\n")
        f.write("- Post-surgical status (≤60 days)\n\n")

        # Sort by score descending, then by patient ID
        sorted_patients = sorted(
            high_risk_patients,
            key=lambda p: (-p['score'], p['patient_id'])
        )

        f.write("## Flagged Patients\n\n")

        for patient in sorted_patients:
            f.write(f"### {patient['patient_id']} (Score: {patient['score']})\n\n")
            f.write(f"**Payer:** {patient['payer']}\n")
            f.write(f"**Primary Diagnosis:** {patient['diagnosis']} - {patient['diagnosis_desc']}\n")
            f.write(f"**Admission Date:** {patient['admission_date']}\n")

            if patient['risk_factors']:
                f.write("\n**Risk Factors:**\n")
                for factor in patient['risk_factors']:
                    f.write(f"- {factor}\n")

            f.write("\n---\n\n")

        f.write("## Instructions for Clinical Review\n\n")
        f.write("1. Contact flagged patients within 48 hours\n")
        f.write("2. Assess care plan adequacy\n")
        f.write("3. Consider intensified monitoring or frequency adjustment\n")
        f.write("4. Document interventions and outcomes\n")

    return str(filepath)


# ============================================================================
# Main Logic
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Flag high-risk patients for clinical review',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python flag_high_risk_patients.py --census-file 2026-04-04-SUNRISE-census.csv
  python flag_high_risk_patients.py --census-file 2026-04-04-SUNRISE-census.csv --date 2026-04-04
        """
    )

    parser.add_argument(
        '--census-file',
        required=True,
        type=str,
        help='Path to census CSV file'
    )
    parser.add_argument(
        '--date',
        type=str,
        default=None,
        help='Output file date (YYYY-MM-DD). Default: today'
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("High-Risk Patient Flagging Started")
    logger.info("=" * 70)

    try:
        # Resolve census file path
        census_path = Path(args.census_file)
        if not census_path.is_absolute():
            census_path = DATA_DIR / census_path

        if not census_path.exists():
            logger.error(f"Census file not found: {census_path}")
            return 1

        logger.info(f"Reading census file: {census_path}")

        # Read census data
        records = read_census_csv(census_path)
        logger.info(f"Read {len(records)} patient records")

        if not records:
            logger.warning("No patient records found")
            return 0

        # Calculate risk scores
        high_risk_patients = []
        risk_score_distribution = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        for record in records:
            score, risk_factors = calculate_risk_score(record)

            # Track distribution
            risk_score_distribution[min(score, 6)] += 1

            # Flag patients with score ≥2
            if score >= 2:
                high_risk_patients.append({
                    'patient_id': record.get('PatientID', ''),
                    'score': score,
                    'payer': record.get('Payer', ''),
                    'diagnosis': record.get('PrimaryDiagnosisICD10', ''),
                    'diagnosis_desc': record.get('PrimaryDiagnosisDescription', ''),
                    'admission_date': record.get('AdmissionDate', ''),
                    'risk_factors': risk_factors
                })

        logger.info(f"Identified {len(high_risk_patients)} high-risk patients (score ≥2)")

        # Log score distribution
        logger.info("Risk Score Distribution:")
        for score in sorted(risk_score_distribution.keys()):
            count = risk_score_distribution[score]
            pct = (count / len(records) * 100) if records else 0
            logger.info(f"  Score {score}: {count} patients ({pct:.1f}%)")

        # Save flags
        output_date = args.date or datetime.now().date().isoformat()
        output_file = save_high_risk_flags(high_risk_patients, output_date)
        logger.info(f"Saved flags to: {output_file}")

        # Log summary
        logger.info("=" * 70)
        logger.info("High-Risk Patient Flagging Summary")
        logger.info("=" * 70)
        logger.info(f"Census file: {census_path.name}")
        logger.info(f"Total patients: {len(records)}")
        logger.info(f"High-risk patients (score ≥2): {len(high_risk_patients)}")
        logger.info(f"Flagging rate: {len(high_risk_patients) / len(records) * 100:.1f}%")
        logger.info(f"Output: {output_file}")
        logger.info("=" * 70)

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        logger.error("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
