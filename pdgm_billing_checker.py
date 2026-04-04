#!/usr/bin/env python3
"""
PDGM Billing & Coding Checker for Enzo Health

Reviews OASIS data, ICD-10 codes, and visit counts to validate accurate PDGM
classification, HIPPS code calculation, comorbidity adjustments, and LUPA status.
Identifies revenue leakage and calculates potential payment impacts.

Usage:
    python pdgm_billing_checker.py --patient-id PT001 --agency-id SUNRISE
    python pdgm_billing_checker.py --patient-id PT001 --agency-id SUNRISE --dry-run
    python pdgm_billing_checker.py --agency-id SUNRISE --test-all
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
OUTPUT_DIR = WORKSPACE_ROOT / 'billing'
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
        log_file = LOGS_DIR / f"pdgm_billing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
# PDGM Clinical Group Mapping (ICD-10 to Group)
# ============================================================================

PDGM_DIAGNOSIS_MAPPING = {
    # MMTA-Cardiac (Group 1)
    'I10': ('MMTA-Cardiac', 1), 'I11': ('MMTA-Cardiac', 1), 'I12': ('MMTA-Cardiac', 1),
    'I13': ('MMTA-Cardiac', 1), 'I14': ('MMTA-Cardiac', 1), 'I15': ('MMTA-Cardiac', 1),
    'I20': ('MMTA-Cardiac', 1), 'I21': ('MMTA-Cardiac', 1), 'I22': ('MMTA-Cardiac', 1),
    'I23': ('MMTA-Cardiac', 1), 'I24': ('MMTA-Cardiac', 1), 'I25': ('MMTA-Cardiac', 1),
    'I26': ('MMTA-Cardiac', 1), 'I27': ('MMTA-Cardiac', 1), 'I28': ('MMTA-Cardiac', 1),
    'I30': ('MMTA-Cardiac', 1), 'I31': ('MMTA-Cardiac', 1), 'I32': ('MMTA-Cardiac', 1),
    'I33': ('MMTA-Cardiac', 1), 'I34': ('MMTA-Cardiac', 1), 'I35': ('MMTA-Cardiac', 1),
    'I36': ('MMTA-Cardiac', 1), 'I37': ('MMTA-Cardiac', 1), 'I38': ('MMTA-Cardiac', 1),
    'I39': ('MMTA-Cardiac', 1), 'I40': ('MMTA-Cardiac', 1), 'I41': ('MMTA-Cardiac', 1),
    'I42': ('MMTA-Cardiac', 1), 'I43': ('MMTA-Cardiac', 1), 'I44': ('MMTA-Cardiac', 1),
    'I45': ('MMTA-Cardiac', 1), 'I46': ('MMTA-Cardiac', 1), 'I47': ('MMTA-Cardiac', 1),
    'I48': ('MMTA-Cardiac', 1), 'I49': ('MMTA-Cardiac', 1), 'I50': ('MMTA-Cardiac', 1),
    'I51': ('MMTA-Cardiac', 1), 'I52': ('MMTA-Cardiac', 1),

    # MMTA-Neuro (Group 2)
    'G89': ('MMTA-Neuro', 2), 'G20': ('MMTA-Neuro', 2), 'G21': ('MMTA-Neuro', 2),
    'I63': ('MMTA-Neuro', 2), 'I64': ('MMTA-Neuro', 2), 'I65': ('MMTA-Neuro', 2),

    # MMTA-Pulmonary (Group 3)
    'J40': ('MMTA-Pulmonary', 3), 'J41': ('MMTA-Pulmonary', 3), 'J44': ('MMTA-Pulmonary', 3),
    'J45': ('MMTA-Pulmonary', 3), 'J80': ('MMTA-Pulmonary', 3), 'J84': ('MMTA-Pulmonary', 3),

    # MMTA-Diabetes (Group 5)
    'E10': ('MMTA-Diabetes', 5), 'E11': ('MMTA-Diabetes', 5), 'E12': ('MMTA-Diabetes', 5),
    'E13': ('MMTA-Diabetes', 5),

    # Wounds (Group 7)
    'L89': ('Wounds', 7), 'L97': ('Wounds', 7), 'L98': ('Wounds', 7),

    # Orthopedic (Group 8)
    'M00': ('Orthopedic', 8), 'M17': ('Orthopedic', 8), 'M19': ('Orthopedic', 8),
    'S72': ('Orthopedic', 8),

    # Cardiac / Non-Surgical (Group 9)
    'I50': ('Cardiac', 9),

    # Psychiatric (Group 12)
    'F32': ('Psychiatric', 12), 'F33': ('Psychiatric', 12), 'F39': ('Psychiatric', 12),
}

# LUPA Thresholds by group
LUPA_THRESHOLDS = {
    'MMTA-Cardiac': 6, 'MMTA-Neuro': 6, 'MMTA-Pulmonary': 6,
    'MMTA-Orthopedic': 5, 'MMTA-Diabetes': 6, 'MMTA-General': 6,
    'Wounds': 4, 'Orthopedic': 4, 'Cardiac': 6,
    'Neurological': 6, 'Medication Management': 4, 'Psychiatric': 4,
}

# Base payment rates by clinical group (simplified for demo)
BASE_RATES = {
    'MMTA-Cardiac': 4500, 'MMTA-Neuro': 4700, 'MMTA-Pulmonary': 4600,
    'MMTA-Orthopedic': 4300, 'MMTA-Diabetes': 4200, 'MMTA-General': 4100,
    'Wounds': 5200, 'Orthopedic': 4400, 'Cardiac': 4800,
    'Neurological': 4900, 'Medication Management': 4000, 'Psychiatric': 3800,
}

# Comorbidity adjustment multipliers
COMORBIDITY_ADJUSTMENTS = {
    'CA0': 1.0,  # No adjustment
    'CA1': 1.25,  # Single comorbidity
    'CA2': 1.47,  # Multiple comorbidities or interaction pairs
}

# Functional level adjustments
FUNCTIONAL_ADJUSTMENTS = {
    'Low': 0.92,
    'Medium': 1.0,
    'High': 1.37,
}

# Qualifying secondary diagnoses for comorbidity
QUALIFYING_SECONDARY_DIAGNOSES = {
    'E10', 'E11', 'E12', 'E13',  # Diabetes
    'I10', 'I11', 'I12', 'I13', 'I14', 'I15',  # Hypertension
    'I50',  # Heart failure
    'J44', 'J45',  # COPD, Asthma
    'N18',  # Chronic kidney disease
    'F32', 'F33', 'F39',  # Depression
    'I63', 'I64', 'I65', 'I66', 'I67',  # Stroke/TIA
}

# CA2 interaction pairs (automatic CA2 if both present)
CA2_INTERACTION_PAIRS = [
    ('E11', 'N18'),  # Diabetes + CKD
    ('E10', 'N18'),  # Diabetes + CKD
    ('E11', 'I70'),  # Diabetes + PVD
    ('J44', 'I50'),  # COPD + Heart failure
    ('J44', 'E11'),  # COPD + Diabetes
    ('I50', 'E11'),  # Heart failure + Diabetes
]

# ============================================================================
# Sample Episode Data
# ============================================================================

SAMPLE_EPISODES = {
    'EP001': {
        'patient_id': 'PT001',
        'patient_name': 'John Doe',
        'episode_start': '2026-04-01',
        'episode_type': 'SOC',
        'agency_id': 'SUNRISE',
        'primary_diagnosis': 'L89.91',  # Pressure ulcer
        'secondary_diagnoses': ['E11.9', 'I10'],
        'visits_to_date': 4,
        'visit_history': ['SN', 'PT', 'SN', 'OT'],
        'current_date': '2026-04-15',
        'oasis_items': {
            'M1800': 3, 'M1810': 3, 'M1820': 3, 'M1830': 2, 'M1840': 1,
            'M1860': 2, 'M2020': 2, 'M2030': 1,
            'GG0130': 3, 'GG0170': 'NA',
        },
        'discharge_status': 'NA',
    },
    'EP002': {
        'patient_id': 'PT002',
        'patient_name': 'Jane Smith',
        'episode_start': '2026-04-02',
        'episode_type': 'SOC',
        'agency_id': 'SUNRISE',
        'primary_diagnosis': 'I50.9',  # Heart failure
        'secondary_diagnoses': ['E11.21', 'N18.3'],  # Diabetes + CKD (CA2 pair)
        'visits_to_date': 8,
        'visit_history': ['SN', 'SN', 'PT', 'SN', 'PT', 'SN', 'PT', 'SN'],
        'current_date': '2026-04-16',
        'oasis_items': {
            'M1800': 0, 'M1810': 0, 'M1820': 0, 'M1830': 1, 'M1840': 0,
            'M1860': 0, 'M2020': 1, 'M2030': 1,
            'GG0130': 6, 'GG0170': 'NA',
        },
        'discharge_status': 'NA',
    },
    'EP003': {
        'patient_id': 'PT003',
        'patient_name': 'Robert Johnson',
        'episode_start': '2026-03-20',
        'episode_type': 'SOC',
        'agency_id': 'SUNRISE',
        'primary_diagnosis': 'S72.001A',  # Femur fracture (Orthopedic)
        'secondary_diagnoses': ['M17.11'],
        'visits_to_date': 2,
        'visit_history': ['PT', 'PT'],
        'current_date': '2026-03-24',
        'oasis_items': {
            'M1800': 0, 'M1810': 2, 'M1820': 3, 'M1830': 3, 'M1840': 1,
            'M1860': 1, 'M2020': 0, 'M2030': 0,
            'GG0130': 4, 'GG0170': 'NA',
        },
        'discharge_status': 'NA',
        'note': 'LUPA Risk: Only 2 visits with 26 days remaining. Orthopedic threshold is 4 visits.',
    },
}

# ============================================================================
# PDGM Billing Checker
# ============================================================================

class PDGMBillingChecker:
    """Validates PDGM episode billing and coding."""

    def __init__(self, episode_data: Dict[str, Any], dry_run: bool = False):
        self.episode_data = episode_data
        self.dry_run = dry_run
        self.warnings = []
        self.optimizations = []

    def check_all(self) -> Dict[str, Any]:
        """Run all PDGM billing checks."""
        logger.info(f"Starting PDGM billing check for episode {self.episode_data['patient_id']}")

        clinical_group = self.get_clinical_group()
        functional_level = self.calculate_functional_level()
        comorbidity_tier = self.calculate_comorbidity_tier()
        hipps_code = self.calculate_hipps_code(clinical_group, functional_level, comorbidity_tier)
        lupa_status = self.check_lupa_status(clinical_group)
        base_payment = self.calculate_base_payment(clinical_group, functional_level, comorbidity_tier)

        return {
            'patient_id': self.episode_data['patient_id'],
            'episode_start': self.episode_data['episode_start'],
            'clinical_group': clinical_group,
            'functional_level': functional_level,
            'comorbidity_tier': comorbidity_tier,
            'hipps_code': hipps_code,
            'lupa_status': lupa_status,
            'base_payment': base_payment,
            'warnings': self.warnings,
            'optimizations': self.optimizations,
        }

    def get_clinical_group(self) -> Tuple[str, int]:
        """Determine PDGM clinical group from primary diagnosis."""
        primary_dx = self.episode_data['primary_diagnosis']
        category = primary_dx[:3]

        if category in PDGM_DIAGNOSIS_MAPPING:
            group_name, group_num = PDGM_DIAGNOSIS_MAPPING[category]
        else:
            # Default to MMTA-General for unknown codes
            group_name, group_num = ('MMTA-General', 6)
            self.warnings.append(
                f"Diagnosis Code: {primary_dx} not found in PDGM mapping. "
                f"Defaulting to {group_name}. Verify correct ICD-10 code."
            )

        return group_name

    def calculate_functional_level(self) -> str:
        """Calculate functional impairment level from M/GG items."""
        items = self.episode_data['oasis_items']

        # Count ADL dependencies (simplified algorithm)
        adl_score = 0
        for item_key in ['M1800', 'M1810', 'M1820', 'M1830']:
            score = items.get(item_key, 0)
            if score in [0, 1]:
                adl_score += 0
            elif score == 2:
                adl_score += 1
            elif score in [3, 4]:
                adl_score += 2

        # Add bedbound/chairbound penalty
        m1860 = items.get('M1860', 0)
        if m1860 in [3, 4]:
            adl_score += 2

        # Assess GG items
        gg0130 = items.get('GG0130', 0)
        if gg0130 in [0, 1, 2]:
            gg_level = 'High'
        elif gg0130 in [3, 4]:
            gg_level = 'Medium'
        else:
            gg_level = 'Low'

        # Assign level based on total ADL score
        if adl_score <= 3 and gg_level in ['Low', 'Medium']:
            functional_level = 'Low'
        elif adl_score >= 7 or gg_level == 'High':
            functional_level = 'High'
        else:
            functional_level = 'Medium'

        logger.info(f"Functional Level: {functional_level} (ADL score: {adl_score}, GG level: {gg_level})")
        return functional_level

    def calculate_comorbidity_tier(self) -> str:
        """Calculate comorbidity adjustment tier from secondary diagnoses."""
        secondary_dx = self.episode_data.get('secondary_diagnoses', [])

        # Count qualifying secondary diagnoses
        qualifying_count = 0
        for dx in secondary_dx:
            dx_category = dx[:3]
            if dx_category in QUALIFYING_SECONDARY_DIAGNOSES:
                qualifying_count += 1

        # Check for CA2 interaction pairs
        has_ca2_pair = False
        if qualifying_count >= 2:
            for pair in CA2_INTERACTION_PAIRS:
                if any(dx.startswith(pair[0]) for dx in secondary_dx) and \
                   any(dx.startswith(pair[1]) for dx in secondary_dx):
                    has_ca2_pair = True
                    break

        # Assign tier
        if has_ca2_pair:
            comorbidity_tier = 'CA2'
            self.optimizations.append(
                f"Comorbidity Adjustment: CA2 interaction pair detected. "
                f"Secondary diagnoses: {secondary_dx}. Payment includes CA2 multiplier (1.47x)."
            )
        elif qualifying_count >= 2:
            comorbidity_tier = 'CA2'
            self.optimizations.append(
                f"Comorbidity Adjustment: Two qualifying secondary diagnoses. "
                f"Payment includes CA2 multiplier (1.47x)."
            )
        elif qualifying_count == 1:
            comorbidity_tier = 'CA1'
            self.optimizations.append(
                f"Comorbidity Adjustment: One qualifying secondary diagnosis. "
                f"Payment includes CA1 multiplier (1.25x)."
            )
        else:
            comorbidity_tier = 'CA0'
            if secondary_dx:
                self.warnings.append(
                    f"Comorbidity Opportunity: Secondary diagnoses present ({secondary_dx}) "
                    f"but do not qualify for adjustment. Verify each is active and documented."
                )

        return comorbidity_tier

    def calculate_hipps_code(self, clinical_group: str, functional_level: str, comorbidity_tier: str) -> str:
        """Generate 5-character HIPPS code."""
        # Simplified HIPPS code generation
        # Real algorithm is more complex; this is for demonstration

        group_num = PDGM_DIAGNOSIS_MAPPING.get(self.episode_data['primary_diagnosis'][:3], ('MMTA-General', 6))[1]

        # HIPPS format (simplified): [Timing][Clinical Group][Functional][Comorbidity][LUPA]
        timing = '0'  # 0=Early, 1=Late (assuming Early for now)
        clin_code = str(group_num).zfill(2)
        func_code = {'Low': '0', 'Medium': '1', 'High': '2'}.get(functional_level, '1')
        com_code = {'CA0': '0', 'CA1': '1', 'CA2': '2'}.get(comorbidity_tier, '0')
        lupa_code = '0'  # 0=Non-LUPA, 1=LUPA (determined later)

        hipps = f"{timing}{clin_code}{func_code}{com_code}{lupa_code}"
        return hipps

    def check_lupa_status(self, clinical_group: str) -> Dict[str, Any]:
        """Check LUPA status and risk."""
        lupa_threshold = LUPA_THRESHOLDS.get(clinical_group, 6)
        visits_to_date = self.episode_data.get('visits_to_date', 0)

        # Calculate days in episode
        start_date = datetime.strptime(self.episode_data['episode_start'], '%Y-%m-%d')
        current_date = datetime.strptime(self.episode_data['current_date'], '%Y-%m-%d')
        days_elapsed = (current_date - start_date).days
        days_remaining = 30 - days_elapsed

        # Project final visit count
        if days_elapsed > 0:
            daily_visit_rate = visits_to_date / days_elapsed
            projected_visits = visits_to_date + (daily_visit_rate * days_remaining)
        else:
            projected_visits = visits_to_date

        # Determine LUPA status
        if projected_visits < lupa_threshold:
            lupa_status = 'LUPA (At Risk)'
            risk_level = 'HIGH'
            self.warnings.append(
                f"LUPA Risk Alert: {clinical_group} threshold is {lupa_threshold} visits. "
                f"Currently {visits_to_date} visits with {days_remaining} days remaining. "
                f"Projected: {projected_visits:.1f} visits. LUPA status likely."
            )
        elif projected_visits < (lupa_threshold + 1):
            lupa_status = 'Near LUPA Threshold'
            risk_level = 'MEDIUM'
            self.warnings.append(
                f"LUPA Caution: {clinical_group} threshold is {lupa_threshold} visits. "
                f"Currently {visits_to_date} visits. Projected: {projected_visits:.1f}. "
                f"Monitor closely to ensure adequate visits."
            )
        else:
            lupa_status = 'Non-LUPA'
            risk_level = 'LOW'

        return {
            'status': lupa_status,
            'threshold': lupa_threshold,
            'visits_to_date': visits_to_date,
            'projected_visits': round(projected_visits, 1),
            'days_remaining': days_remaining,
            'risk_level': risk_level,
        }

    def calculate_base_payment(self, clinical_group: str, functional_level: str, comorbidity_tier: str) -> Dict[str, float]:
        """Calculate 30-day episode payment."""
        base_rate = BASE_RATES.get(clinical_group, 4300)
        func_multiplier = FUNCTIONAL_ADJUSTMENTS.get(functional_level, 1.0)
        com_multiplier = COMORBIDITY_ADJUSTMENTS.get(comorbidity_tier, 1.0)

        episode_payment = base_rate * func_multiplier * com_multiplier

        return {
            'base_rate': base_rate,
            'functional_multiplier': func_multiplier,
            'comorbidity_multiplier': com_multiplier,
            'total_30_day_payment': round(episode_payment, 2),
        }

# ============================================================================
# Report Generation
# ============================================================================

def write_report(check_result: Dict[str, Any], dry_run: bool = False) -> Path:
    """Write PDGM billing review report to file."""
    patient_id = check_result['patient_id']
    timestamp = date.today().isoformat()
    filename = f"{timestamp}-{patient_id}-pdgm-review.md"
    filepath = OUTPUT_DIR / filename

    lupa = check_result.get('lupa_status', {})
    payment = check_result.get('base_payment', {})

    content = f"""# PDGM Billing & Coding Review

**Patient ID:** {check_result['patient_id']}
**Episode Start:** {check_result['episode_start']}
**Review Date:** {timestamp}

## PDGM Classification

**Clinical Group:** {check_result['clinical_group']}
**Functional Impairment Level:** {check_result['functional_level']}
**Comorbidity Adjustment:** {check_result['comorbidity_tier']}
**HIPPS Code:** {check_result['hipps_code']}

## Payment Calculation

**Base Rate:** ${payment.get('base_rate', 0):,.2f}
**Functional Level Multiplier:** {payment.get('functional_multiplier', 1.0):.2f}x
**Comorbidity Multiplier:** {payment.get('comorbidity_multiplier', 1.0):.2f}x
**Total 30-Day Payment:** ${payment.get('total_30_day_payment', 0):,.2f}

## LUPA Status

**Status:** {lupa.get('status', 'Unknown')}
**Threshold:** {lupa.get('threshold', 0)} visits
**Visits to Date:** {lupa.get('visits_to_date', 0)}
**Projected Total:** {lupa.get('projected_visits', 0)}
**Days Remaining:** {lupa.get('days_remaining', 0)}
**Risk Level:** {lupa.get('risk_level', 'Unknown')}

## Billing Alerts

### Warnings
"""

    if check_result['warnings']:
        for warning in check_result['warnings']:
            content += f"- {warning}\n"
    else:
        content += "- No warnings\n"

    content += "\n### Optimization Opportunities\n"

    if check_result['optimizations']:
        for opt in check_result['optimizations']:
            content += f"- {opt}\n"
    else:
        content += "- No additional optimizations identified\n"

    content += "\n## Recommendation\n"

    if lupa.get('risk_level') == 'HIGH':
        content += "**Action Required:** Episode at LUPA risk. Review care plan and consider visits to justify non-LUPA status.\n"
    elif lupa.get('risk_level') == 'MEDIUM':
        content += "**Action:** Monitor visit count closely. Ensure clinical documentation supports all visits.\n"
    else:
        content += "**Action:** Episode billing appears accurate. Proceed with claim submission.\n"

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
        description='PDGM Billing & Coding Checker for Enzo Health'
    )
    parser.add_argument('--patient-id', type=str, help='Patient ID to check')
    parser.add_argument('--agency-id', type=str, required=True, help='Agency ID')
    parser.add_argument('--dry-run', action='store_true', help='Run without writing files')
    parser.add_argument('--test-all', action='store_true', help='Run checks on all sample episodes')

    args = parser.parse_args()

    # If test-all, run on samples
    if args.test_all or (not args.patient_id and args.agency_id):
        logger.info("Running on sample episode data")
        for ep_id, ep_data in SAMPLE_EPISODES.items():
            ep_data['agency_id'] = args.agency_id
            checker = PDGMBillingChecker(ep_data, dry_run=args.dry_run)
            result = checker.check_all()

            print(f"\n{'='*80}")
            print(f"Episode: {ep_id} | Patient: {ep_data['patient_id']} ({ep_data.get('patient_name', 'Unknown')})")
            print(f"Clinical Group: {result['clinical_group']}")
            print(f"Functional Level: {result['functional_level']}")
            print(f"Comorbidity Tier: {result['comorbidity_tier']}")
            print(f"HIPPS Code: {result['hipps_code']}")
            print(f"30-Day Payment: ${result['base_payment']['total_30_day_payment']:,.2f}")
            print(f"LUPA Status: {result['lupa_status']['status']} (Risk: {result['lupa_status']['risk_level']})")

            if result['warnings']:
                print(f"\nWarnings ({len(result['warnings'])}):")
                for warning in result['warnings']:
                    print(f"  - {warning}")

            if result['optimizations']:
                print(f"\nOptimizations ({len(result['optimizations'])}):")
                for opt in result['optimizations']:
                    print(f"  - {opt}")

            write_report(result, dry_run=args.dry_run)

    elif args.patient_id:
        # Find episode for patient
        ep_id = None
        ep_data = None
        for k, v in SAMPLE_EPISODES.items():
            if v['patient_id'] == args.patient_id:
                ep_id = k
                ep_data = v.copy()
                break

        if ep_data:
            ep_data['agency_id'] = args.agency_id
            checker = PDGMBillingChecker(ep_data, dry_run=args.dry_run)
            result = checker.check_all()

            print(f"\n{'='*80}")
            print(f"Patient: {args.patient_id}")
            print(f"Clinical Group: {result['clinical_group']}")
            print(f"Functional Level: {result['functional_level']}")
            print(f"Comorbidity Tier: {result['comorbidity_tier']}")
            print(f"HIPPS Code: {result['hipps_code']}")
            print(f"30-Day Payment: ${result['base_payment']['total_30_day_payment']:,.2f}")
            print(f"LUPA Status: {result['lupa_status']['status']}")

            if result['warnings']:
                print(f"\nWarnings ({len(result['warnings'])}):")
                for warning in result['warnings']:
                    print(f"  - {warning}")

            if result['optimizations']:
                print(f"\nOptimizations ({len(result['optimizations'])}):")
                for opt in result['optimizations']:
                    print(f"  - {opt}")

            write_report(result, dry_run=args.dry_run)
        else:
            logger.error(f"Patient {args.patient_id} not found in sample data")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
