#!/usr/bin/env python3
"""
OASIS QA Consistency Checker for Enzo Health

Validates OASIS assessment data for internal consistency across all three tiers
of items, checks PDGM clinical grouping, identifies scoring errors, and generates
a structured QA review report.

Usage:
    python oasis_qa_checker.py --patient-id PT001 --agency-id SUNRISE
    python oasis_qa_checker.py --patient-id PT001 --agency-id SUNRISE --dry-run
    python oasis_qa_checker.py --agency-id SUNRISE [--window-days 14]
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import copy


# ============================================================================
# Configuration
# ============================================================================

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = WORKSPACE_ROOT / 'clinical-qa' / 'oasis'
LOGS_DIR = Path(__file__).parent / 'logs'

# Ensure output directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(log_file=None):
    """Configure logging for the script."""
    if log_file is None:
        log_file = LOGS_DIR / f"oasis_qa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# PDGM Clinical Grouping Reference
# ============================================================================

PDGM_DIAGNOSIS_MAPPING = {
    # MMTA-Cardiac (Group 1)
    'I10': 'MMTA-Cardiac', 'I11': 'MMTA-Cardiac', 'I12': 'MMTA-Cardiac',
    'I13': 'MMTA-Cardiac', 'I14': 'MMTA-Cardiac', 'I15': 'MMTA-Cardiac',
    'I20': 'MMTA-Cardiac', 'I21': 'MMTA-Cardiac', 'I22': 'MMTA-Cardiac',
    'I23': 'MMTA-Cardiac', 'I24': 'MMTA-Cardiac', 'I25': 'MMTA-Cardiac',
    'I26': 'MMTA-Cardiac', 'I27': 'MMTA-Cardiac', 'I28': 'MMTA-Cardiac',
    'I30': 'MMTA-Cardiac', 'I31': 'MMTA-Cardiac', 'I32': 'MMTA-Cardiac',
    'I33': 'MMTA-Cardiac', 'I34': 'MMTA-Cardiac', 'I35': 'MMTA-Cardiac',
    'I36': 'MMTA-Cardiac', 'I37': 'MMTA-Cardiac', 'I38': 'MMTA-Cardiac',
    'I39': 'MMTA-Cardiac', 'I40': 'MMTA-Cardiac', 'I41': 'MMTA-Cardiac',
    'I42': 'MMTA-Cardiac', 'I43': 'MMTA-Cardiac', 'I44': 'MMTA-Cardiac',
    'I45': 'MMTA-Cardiac', 'I46': 'MMTA-Cardiac', 'I47': 'MMTA-Cardiac',
    'I48': 'MMTA-Cardiac', 'I49': 'MMTA-Cardiac', 'I50': 'MMTA-Cardiac',
    'I51': 'MMTA-Cardiac', 'I52': 'MMTA-Cardiac',
    'R00': 'MMTA-Cardiac', 'R01': 'MMTA-Cardiac', 'R02': 'MMTA-Cardiac',
    'R03': 'MMTA-Cardiac', 'R04': 'MMTA-Cardiac', 'R05': 'MMTA-Cardiac',
    'R06': 'MMTA-Cardiac', 'R07': 'MMTA-Cardiac', 'R09': 'MMTA-Cardiac',

    # MMTA-Neuro (Group 2)
    'G89': 'MMTA-Neuro', 'G20': 'MMTA-Neuro', 'G21': 'MMTA-Neuro',
    'G22': 'MMTA-Neuro', 'G23': 'MMTA-Neuro', 'G24': 'MMTA-Neuro',
    'G25': 'MMTA-Neuro', 'G26': 'MMTA-Neuro', 'G30': 'MMTA-Neuro',
    'G31': 'MMTA-Neuro', 'G32': 'MMTA-Neuro', 'G35': 'MMTA-Neuro',
    'G36': 'MMTA-Neuro', 'G37': 'MMTA-Neuro', 'G40': 'MMTA-Neuro',
    'G41': 'MMTA-Neuro', 'G47': 'MMTA-Neuro',
    'I63': 'MMTA-Neuro', 'I64': 'MMTA-Neuro', 'I65': 'MMTA-Neuro',
    'I66': 'MMTA-Neuro', 'I67': 'MMTA-Neuro',
    'R25': 'MMTA-Neuro', 'R26': 'MMTA-Neuro', 'R27': 'MMTA-Neuro',

    # MMTA-Pulmonary (Group 3)
    'J40': 'MMTA-Pulmonary', 'J41': 'MMTA-Pulmonary', 'J42': 'MMTA-Pulmonary',
    'J43': 'MMTA-Pulmonary', 'J44': 'MMTA-Pulmonary', 'J45': 'MMTA-Pulmonary',
    'J46': 'MMTA-Pulmonary', 'J47': 'MMTA-Pulmonary',
    'J80': 'MMTA-Pulmonary', 'J81': 'MMTA-Pulmonary', 'J82': 'MMTA-Pulmonary',
    'J84': 'MMTA-Pulmonary', 'J94': 'MMTA-Pulmonary', 'J95': 'MMTA-Pulmonary',

    # MMTA-Diabetes (Group 5)
    'E10': 'MMTA-Diabetes', 'E11': 'MMTA-Diabetes', 'E12': 'MMTA-Diabetes',
    'E13': 'MMTA-Diabetes', 'E00': 'MMTA-Diabetes', 'E01': 'MMTA-Diabetes',
    'E02': 'MMTA-Diabetes', 'E03': 'MMTA-Diabetes', 'E04': 'MMTA-Diabetes',
    'E05': 'MMTA-Diabetes', 'E06': 'MMTA-Diabetes', 'E07': 'MMTA-Diabetes',
    'E20': 'MMTA-Diabetes', 'E21': 'MMTA-Diabetes', 'E22': 'MMTA-Diabetes',
    'E23': 'MMTA-Diabetes', 'E24': 'MMTA-Diabetes', 'E25': 'MMTA-Diabetes',
    'E26': 'MMTA-Diabetes', 'E27': 'MMTA-Diabetes', 'E29': 'MMTA-Diabetes',
    'E30': 'MMTA-Diabetes', 'E31': 'MMTA-Diabetes', 'E34': 'MMTA-Diabetes',
    'E35': 'MMTA-Diabetes',

    # Wounds (Group 7)
    'L89': 'Wounds', 'L97': 'Wounds', 'L98': 'Wounds',

    # Orthopedic (Group 8)
    'M00': 'Orthopedic', 'M01': 'Orthopedic', 'M02': 'Orthopedic',
    'M05': 'Orthopedic', 'M06': 'Orthopedic', 'M07': 'Orthopedic',
    'M08': 'Orthopedic', 'M09': 'Orthopedic', 'M10': 'Orthopedic',
    'M11': 'Orthopedic', 'M12': 'Orthopedic', 'M13': 'Orthopedic',
    'M14': 'Orthopedic', 'M15': 'Orthopedic', 'M16': 'Orthopedic',
    'M17': 'Orthopedic', 'M18': 'Orthopedic', 'M19': 'Orthopedic',
    'M20': 'Orthopedic', 'M21': 'Orthopedic', 'M22': 'Orthopedic',
    'M23': 'Orthopedic', 'M24': 'Orthopedic', 'M25': 'Orthopedic',
    'M45': 'Orthopedic', 'M46': 'Orthopedic', 'M47': 'Orthopedic',
    'M48': 'Orthopedic', 'M50': 'Orthopedic', 'M51': 'Orthopedic',
    'M53': 'Orthopedic', 'M54': 'Orthopedic',
    'M70': 'Orthopedic', 'M71': 'Orthopedic', 'M72': 'Orthopedic',
    'M73': 'Orthopedic', 'M75': 'Orthopedic', 'M76': 'Orthopedic',
    'M77': 'Orthopedic', 'M79': 'Orthopedic',

    # Psychiatric (Group 12)
    'F01': 'Psychiatric', 'F02': 'Psychiatric', 'F03': 'Psychiatric',
    'F04': 'Psychiatric', 'F05': 'Psychiatric', 'F06': 'Psychiatric',
    'F07': 'Psychiatric', 'F09': 'Psychiatric', 'F10': 'Psychiatric',
    'F11': 'Psychiatric', 'F12': 'Psychiatric', 'F13': 'Psychiatric',
    'F14': 'Psychiatric', 'F15': 'Psychiatric', 'F16': 'Psychiatric',
    'F17': 'Psychiatric', 'F18': 'Psychiatric', 'F19': 'Psychiatric',
    'F20': 'Psychiatric', 'F21': 'Psychiatric', 'F22': 'Psychiatric',
    'F23': 'Psychiatric', 'F24': 'Psychiatric', 'F25': 'Psychiatric',
    'F28': 'Psychiatric', 'F29': 'Psychiatric', 'F30': 'Psychiatric',
    'F31': 'Psychiatric', 'F32': 'Psychiatric', 'F33': 'Psychiatric',
    'F34': 'Psychiatric', 'F39': 'Psychiatric', 'F40': 'Psychiatric',
    'F41': 'Psychiatric', 'F42': 'Psychiatric', 'F43': 'Psychiatric',
    'F44': 'Psychiatric', 'F45': 'Psychiatric', 'F48': 'Psychiatric',
    'F50': 'Psychiatric', 'F51': 'Psychiatric', 'F52': 'Psychiatric',
    'F53': 'Psychiatric', 'F54': 'Psychiatric', 'F55': 'Psychiatric',
    'F59': 'Psychiatric', 'F60': 'Psychiatric', 'F61': 'Psychiatric',
    'F62': 'Psychiatric', 'F63': 'Psychiatric', 'F64': 'Psychiatric',
    'F65': 'Psychiatric', 'F66': 'Psychiatric', 'F68': 'Psychiatric',
    'F69': 'Psychiatric', 'F70': 'Psychiatric', 'F71': 'Psychiatric',
    'F72': 'Psychiatric', 'F73': 'Psychiatric', 'F78': 'Psychiatric',
    'F79': 'Psychiatric', 'F80': 'Psychiatric', 'F81': 'Psychiatric',
    'F82': 'Psychiatric', 'F84': 'Psychiatric', 'F88': 'Psychiatric',
    'F89': 'Psychiatric', 'F90': 'Psychiatric', 'F91': 'Psychiatric',
    'F92': 'Psychiatric', 'F93': 'Psychiatric', 'F94': 'Psychiatric',
    'F95': 'Psychiatric', 'F98': 'Psychiatric', 'F99': 'Psychiatric',
}

LUPA_THRESHOLDS = {
    'MMTA-Cardiac': 6, 'MMTA-Neuro': 6, 'MMTA-Pulmonary': 6,
    'MMTA-Orthopedic': 5, 'MMTA-Diabetes': 6, 'MMTA-General': 6,
    'Wounds': 4, 'Orthopedic': 4, 'Cardiac': 6,
    'Neurological': 6, 'Medication Management': 4, 'Psychiatric': 4,
}

# ============================================================================
# Sample OASIS Data for Testing
# ============================================================================

SAMPLE_PATIENTS = {
    'PT001': {
        'patient_id': 'PT001',
        'patient_name': 'John Doe',
        'assessment_type': 'SOC',
        'assessment_date': '2026-04-01',
        'agency_id': 'SUNRISE',
        'primary_diagnosis': 'L89.91',  # Pressure ulcer, unspecified, unhealed
        'secondary_diagnoses': ['E11.9', 'I10'],  # Diabetes, Hypertension
        'oasis_items': {
            'M1021': 'L89.91',
            'M1023': ['E11.9', 'I10'],
            'M1033': 0,  # Low risk of hospitalization
            'M1800': 3,  # Bathing - extensive assist
            'M1810': 3,  # Toilet transferring - extensive assist
            'M1820': 3,  # Transferring - extensive assist
            'M1830': 2,  # Walking - limited assist
            'M1840': 1,  # Unable to leave home
            'M1850': 2,  # Cannot attend medical appointments
            'M1860': 2,  # Chairbound
            'M1242': 2,  # Moderate pain
            'M1306': 1,  # Has pressure ulcer
            'M1307': 'Right heel',  # Location
            'M1308': 2,  # Stage 2
            'M1910': 1,  # At risk for falls
            'M2020': 2,  # Medication management - limited assist
            'M2030': 1,  # Medication complexity - 5+ medications
            'M2401': 0,  # No depression screening needed
            'GG0130': 3,  # Admission function - minimal assist
            'GG0170': 'NA',  # Discharge not yet applicable
        }
    },
    'PT002': {
        'patient_id': 'PT002',
        'patient_name': 'Jane Smith',
        'assessment_type': 'SOC',
        'assessment_date': '2026-04-02',
        'agency_id': 'SUNRISE',
        'primary_diagnosis': 'I50.9',  # Heart failure, unspecified
        'secondary_diagnoses': ['E11.21', 'N18.3'],  # Diabetes with renal, CKD stage 3
        'oasis_items': {
            'M1021': 'I50.9',
            'M1023': ['E11.21', 'N18.3'],
            'M1033': 1,  # High risk of hospitalization
            'M1800': 0,  # Bathing - independent
            'M1810': 0,  # Toilet transferring - independent
            'M1820': 0,  # Transferring - independent
            'M1830': 1,  # Walking - supervision
            'M1840': 0,  # Able to leave home
            'M1850': 0,  # Able to attend medical appointments
            'M1860': 0,  # Not bedbound/chairbound
            'M1242': 1,  # Mild pain
            'M1306': 0,  # No pressure ulcer
            'M1307': 'NA',
            'M1308': 'NA',
            'M1910': 0,  # Not at risk for falls
            'M2020': 1,  # Medication management - supervision
            'M2030': 1,  # Medication complexity - 5+ medications
            'M2401': 1,  # Depression screening indicated
            'M2400': 'PHQ-2 score: 2',  # Positive screening result
            'GG0130': 6,  # Admission function - independent
            'GG0170': 'NA',
        }
    },
    'PT003': {
        'patient_id': 'PT003',
        'patient_name': 'Robert Johnson',
        'assessment_type': 'SOC',
        'assessment_date': '2026-04-03',
        'agency_id': 'SUNRISE',
        'primary_diagnosis': 'S72.001A',  # Fracture of right femur, initial encounter
        'secondary_diagnoses': ['M17.11'],  # Primary osteoarthritis, right knee
        'oasis_items': {
            'M1021': 'S72.001A',
            'M1023': ['M17.11'],
            'M1033': 0,
            'M1800': 0,  # Bathing - independent
            'M1810': 2,  # Toilet transferring - limited assist
            'M1820': 3,  # Transferring - extensive assist (post-fracture)
            'M1830': 3,  # Walking - extensive assist (post-fracture)
            'M1840': 1,  # Unable to leave home (post-fracture)
            'M1850': 1,  # Unable to attend appointments (post-fracture)
            'M1860': 1,  # Supervision required (partial weight bearing)
            'M1242': 2,  # Moderate pain (post-fracture)
            'M1306': 0,
            'M1307': 'NA',
            'M1308': 'NA',
            'M1910': 1,  # At risk for falls (post-fracture, mobility limited)
            'M2020': 0,  # Medication management - independent
            'M2030': 0,  # Medication complexity - 1-4 medications
            'M2401': 0,
            'GG0130': 4,  # Admission function - supervision (post-fracture)
            'GG0170': 'NA',
        },
        'note': 'ERROR: M1800 (bathing) = independent, but M1820/M1830 require extensive assist. Inconsistent.'
    }
}

# ============================================================================
# OASIS Consistency Checker
# ============================================================================

class OASISQAChecker:
    """Validates OASIS assessment for consistency and accuracy."""

    def __init__(self, patient_data: Dict[str, Any], dry_run: bool = False):
        self.patient_data = patient_data
        self.dry_run = dry_run
        self.errors = []
        self.warnings = []
        self.successes = []

    def check_all(self) -> Dict[str, Any]:
        """Run all consistency checks."""
        logger.info(f"Starting OASIS QA check for patient {self.patient_data['patient_id']}")

        self.check_adl_consistency()
        self.check_pressure_ulcer_logic()
        self.check_ambulation_consistency()
        self.check_medication_management()
        self.check_depression_screening()
        self.check_homebound_status()
        self.check_primary_diagnosis()

        return self.generate_report()

    def check_adl_consistency(self):
        """Check ADL item consistency."""
        items = self.patient_data['oasis_items']

        # If bedbound/chairbound, ADL items should not be fully independent
        if items.get('M1860') in [3, 4]:  # Chairbound or bedbound
            if items.get('M1800') in [0, 1]:  # Independent/supervision in bathing
                self.errors.append(
                    f"ADL Inconsistency: M1860 (chairbound/bedbound) = {items['M1860']} "
                    f"but M1800 (bathing) = {items['M1800']} (independent/supervision). "
                    f"Recommend M1800 >= 2 or explanation in notes."
                )

        # Check if multiple ADLs show independence while one shows full assist
        adl_items = [items.get(f'M18{x}0', None) for x in [0, 1, 2, 3]]
        if None not in adl_items:
            if max(adl_items) >= 3 and min(adl_items) in [0, 1]:
                self.warnings.append(
                    f"ADL Variance: Some ADL items show independence (0-1) while others "
                    f"show extensive/total assist (3-4). Verify clinical consistency: {adl_items}"
                )

        self.successes.append("ADL consistency check completed")

    def check_pressure_ulcer_logic(self):
        """Check pressure ulcer item logic."""
        items = self.patient_data['oasis_items']

        if items.get('M1306') == 0:  # No pressure ulcer
            if items.get('M1307') not in [None, 'NA']:
                self.errors.append(
                    f"Pressure Ulcer Logic: M1306 = 0 (no ulcer) "
                    f"but M1307 (location) = '{items['M1307']}'. "
                    f"If no ulcer, M1307 and M1308 must be NA."
                )
            if items.get('M1308') not in [None, 'NA']:
                self.errors.append(
                    f"Pressure Ulcer Logic: M1306 = 0 (no ulcer) "
                    f"but M1308 (stage) = {items['M1308']}. "
                    f"If no ulcer, M1307 and M1308 must be NA."
                )
        elif items.get('M1306') == 1:  # Has pressure ulcer
            if items.get('M1307') in [None, 'NA']:
                self.errors.append(
                    f"Pressure Ulcer Logic: M1306 = 1 (has ulcer) "
                    f"but M1307 (location) = '{items['M1307']}'. "
                    f"Must specify location."
                )
            if items.get('M1308') in [None, 'NA']:
                self.errors.append(
                    f"Pressure Ulcer Logic: M1306 = 1 (has ulcer) "
                    f"but M1308 (stage) = {items['M1308']}. "
                    f"Must specify stage."
                )

        self.successes.append("Pressure ulcer logic check completed")

    def check_ambulation_consistency(self):
        """Check ambulation and locomotion consistency."""
        items = self.patient_data['oasis_items']

        m1860 = items.get('M1860')
        m1850 = items.get('M1850')
        m1830 = items.get('M1830')

        # If bedbound, shouldn't be independent in ambulation
        if m1860 == 4:  # Bedbound
            if m1830 in [0, 1]:
                self.errors.append(
                    f"Ambulation Inconsistency: M1860 (bedbound) = 4 "
                    f"but M1830 (walking) = {m1830} (independent/supervision). "
                    f"Recommend M1830 >= 3."
                )

        # Chairbound should have limited mobility
        if m1860 == 3:  # Chairbound
            if m1830 in [0]:
                self.warnings.append(
                    f"Ambulation Inconsistency: M1860 (chairbound) = 3 "
                    f"but M1830 (walking) = {m1830} (independent). "
                    f"Verify that patient can walk independently despite being chairbound."
                )

        self.successes.append("Ambulation consistency check completed")

    def check_medication_management(self):
        """Check medication management consistency."""
        items = self.patient_data['oasis_items']

        m2020 = items.get('M2020')
        m2030 = items.get('M2030')

        # If low medication complexity, shouldn't require extensive assist
        if m2030 == 0:  # Low complexity (1-4 meds)
            if m2020 in [3, 4]:  # Extensive/total assist
                self.warnings.append(
                    f"Medication Management: M2030 = 0 (low complexity) "
                    f"but M2020 = {m2020} (extensive/total assist). "
                    f"Verify clinical justification."
                )

        self.successes.append("Medication management consistency check completed")

    def check_depression_screening(self):
        """Check depression screening conditional logic."""
        items = self.patient_data['oasis_items']

        m2401 = items.get('M2401')
        m2400 = items.get('M2400')

        if m2401 == 1:  # Screening indicated / positive
            if m2400 in [None, 'NA']:
                self.errors.append(
                    f"Depression Screening: M2401 = 1 (positive screening) "
                    f"but M2400 (PHQ-2 result) = '{m2400}'. "
                    f"Must document screening result or PHQ-2 score."
                )
        elif m2401 == 0:  # No screening indicated
            if m2400 not in [None, 'NA']:
                self.warnings.append(
                    f"Depression Screening: M2401 = 0 (no screening) "
                    f"but M2400 (result) = '{m2400}'. "
                    f"Should be NA if screening not indicated."
                )

        self.successes.append("Depression screening check completed")

    def check_homebound_status(self):
        """Check homebound status consistency."""
        items = self.patient_data['oasis_items']

        m1840 = items.get('M1840')  # Ability to leave home
        m1850 = items.get('M1850')  # Attend appointments
        m1860 = items.get('M1860')  # Bedbound/chairbound

        # If able to leave home, shouldn't be bedbound
        if m1840 == 0:  # Able to leave home
            if m1860 in [3, 4]:  # Chairbound or bedbound
                self.warnings.append(
                    f"Homebound Status: M1840 = 0 (able to leave home) "
                    f"but M1860 = {m1860} (chairbound/bedbound). "
                    f"Verify that patient can actually leave home."
                )

        # If unable to leave home, at least one mobility indicator should support it
        if m1840 == 1:  # Unable to leave home
            if m1850 == 0 and m1860 == 0:  # Can attend appointments AND not bedbound
                self.warnings.append(
                    f"Homebound Status: M1840 = 1 (unable to leave) "
                    f"but M1850 = 0 (able to attend appointments) and M1860 = 0 (not bedbound). "
                    f"Verify clinical rationale for homebound status."
                )

        self.successes.append("Homebound status check completed")

    def check_primary_diagnosis(self):
        """Check primary diagnosis for PDGM grouping."""
        m1021 = self.patient_data['oasis_items'].get('M1021')

        if m1021:
            # Extract first 3 characters (category code)
            category = m1021[:3]

            pdgm_group = PDGM_DIAGNOSIS_MAPPING.get(category, 'MMTA-General')

            self.successes.append(
                f"Primary Diagnosis: {m1021} → PDGM Group: {pdgm_group}"
            )

            # Check if diagnosis appears to be a symptom code (R code)
            if m1021.startswith('R') and self.patient_data.get('note'):
                self.warnings.append(
                    f"Diagnosis Specificity: M1021 = {m1021} is a symptom code. "
                    f"If etiology is documented in notes, consider coding to etiology instead."
                )

    def generate_report(self) -> Dict[str, Any]:
        """Generate structured QA review report."""
        patient_id = self.patient_data['patient_id']
        assessment_type = self.patient_data.get('assessment_type', 'Unknown')
        assessment_date = self.patient_data.get('assessment_date', str(date.today()))

        report = {
            'patient_id': patient_id,
            'assessment_type': assessment_type,
            'assessment_date': assessment_date,
            'review_date': str(date.today()),
            'audit_risk': 'High' if self.errors else 'Low',
            'corrections_required': len(self.errors) > 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'successes': self.successes,
        }

        return report

# ============================================================================
# Report Generation
# ============================================================================

def write_report(report: Dict[str, Any], dry_run: bool = False) -> Path:
    """Write QA review report to file."""
    patient_id = report['patient_id']
    timestamp = date.today().isoformat()
    filename = f"{timestamp}-{patient_id}-oasis-review.md"
    filepath = OUTPUT_DIR / filename

    content = f"""# OASIS Accuracy Review

**Patient ID:** {report['patient_id']}
**Assessment Type:** {report['assessment_type']}
**Assessment Date:** {report['assessment_date']}
**Reviewed:** {report['review_date']}

## Summary

**Audit Risk Level:** {report['audit_risk']}
**Corrections Required:** {'Yes' if report['corrections_required'] else 'No'}

## Findings

### Errors (Critical - Require Correction)
"""

    if report['errors']:
        for error in report['errors']:
            content += f"- **{error}**\n"
    else:
        content += "- No critical errors found\n"

    content += "\n### Warnings (Review Recommended)\n"

    if report['warnings']:
        for warning in report['warnings']:
            content += f"- {warning}\n"
    else:
        content += "- No warnings\n"

    content += "\n### Passed Checks\n"

    for success in report['successes']:
        content += f"- {success}\n"

    content += "\n## Recommendation\n"

    if report['corrections_required']:
        content += "**Action Required:** Review and correct flagged items before claim submission.\n"
    else:
        content += "**Action:** Assessment passes QA review. Ready for submission.\n"

    if not dry_run:
        with open(filepath, 'w') as f:
            f.write(content)
        logger.info(f"Report written to {filepath}")
    else:
        logger.info(f"[DRY RUN] Report would be written to {filepath}")

    return filepath

# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='OASIS QA Consistency Checker for Enzo Health'
    )
    parser.add_argument('--patient-id', type=str, help='Patient ID to check')
    parser.add_argument('--agency-id', type=str, required=True, help='Agency ID')
    parser.add_argument('--dry-run', action='store_true', help='Run without writing files')
    parser.add_argument('--test-all', action='store_true', help='Run checks on all sample patients')

    args = parser.parse_args()

    # If no patient specified and test-all, run on samples
    if args.test_all or (not args.patient_id and args.agency_id):
        logger.info("Running on sample patient data")
        for patient_id, patient_data in SAMPLE_PATIENTS.items():
            patient_data['agency_id'] = args.agency_id
            checker = OASISQAChecker(patient_data, dry_run=args.dry_run)
            report = checker.check_all()

            print(f"\n{'='*80}")
            print(f"Patient: {patient_id} ({patient_data.get('patient_name', 'Unknown')})")
            print(f"Audit Risk: {report['audit_risk']}")
            print(f"Corrections Required: {report['corrections_required']}")
            print(f"\nErrors: {len(report['errors'])}")
            for error in report['errors']:
                print(f"  - {error}")
            print(f"\nWarnings: {len(report['warnings'])}")
            for warning in report['warnings']:
                print(f"  - {warning}")

            write_report(report, dry_run=args.dry_run)
    elif args.patient_id:
        logger.info(f"Checking patient {args.patient_id}")
        if args.patient_id in SAMPLE_PATIENTS:
            patient_data = SAMPLE_PATIENTS[args.patient_id].copy()
            patient_data['agency_id'] = args.agency_id
            checker = OASISQAChecker(patient_data, dry_run=args.dry_run)
            report = checker.check_all()

            print(f"\n{'='*80}")
            print(f"Patient: {args.patient_id}")
            print(f"Audit Risk: {report['audit_risk']}")
            print(f"Corrections Required: {report['corrections_required']}")
            print(f"\nErrors ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"  - {error}")
            print(f"\nWarnings ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"  - {warning}")

            write_report(report, dry_run=args.dry_run)
        else:
            logger.error(f"Patient {args.patient_id} not found in sample data")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
