#!/usr/bin/env python3
"""
Intake & Referral Screening Processor for Enzo Health

Processes new patient referrals for Medicare home health eligibility screening.
Validates ICD-10 codes, homebound status, physician NPI, and generates an
intake screening recommendation: Accept, Conditional Accept, or Decline.

Usage:
    python intake_screening_processor.py --agency-id SUNRISE --referral-id REF001
    python intake_screening_processor.py --agency-id SUNRISE --referral-id REF001 --dry-run
    python intake_screening_processor.py --agency-id SUNRISE --sample-run
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import re


# ============================================================================
# Configuration
# ============================================================================

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = WORKSPACE_ROOT / 'intake'
LOGS_DIR = Path(__file__).parent / 'logs'

# ============================================================================
# ICD-10 Code Validation Database
# ============================================================================

PDGM_EXCLUDED_Z_CODES = {
    'Z59': 'Problems associated with housing and economic circumstances',
    'Z60': 'Problems related to social environment',
    'Z62': 'Problems related to upbringing',
    'Z63': 'Problems related to primary support group, including family circumstances',
    'Z64': 'Problems related to certain psychosocial circumstances',
    'Z65': 'Problems related to other psychosocial circumstances',
}

PDGM_EXCLUDED_R_CODES = {
    'R01': 'Abnormal heart beat',
    'R02': 'Gangrene, not elsewhere classified',
    'R03': 'Abnormal blood-pressure reading, without diagnosis',
    'R04': 'Hemorrhage from respiratory passages',
    'R05': 'Fever',
    'R06': 'Abnormalities of breathing',
    'R07': 'Chest pain',
    'R09': 'Other symptoms and signs involving the circulatory and respiratory systems',
    'R10': 'Abdominal and pelvic pain',
    'R11': 'Nausea and vomiting',
    'R12': 'Heartburn',
    'R13': 'Dysphagia',
    'R14': 'Flatulence and related conditions',
    'R15': 'Fecal incontinence',
    'R19': 'Other symptoms and signs involving the digestive system and abdomen',
    'R20': 'Disturbances of skin sensation',
    'R21': 'Rash and other nonspecific skin eruption',
    'R23': 'Other skin changes',
    'R25': 'Abnormal involuntary movements',
    'R26': 'Abnormalities of gait and mobility',
    'R27': 'Other lack of coordination',
    'R29': 'Other symptoms and signs involving the nervous and musculoskeletal systems',
    'R30': 'Dysuria',
    'R31': 'Hematuria',
    'R33': 'Retention of urine',
    'R35': 'Polyuria',
    'R37': 'Sexual dysfunction, unspecified',
    'R39': 'Other and unspecified symptoms and signs involving the genitourinary system',
    'R41': 'Other symptoms and signs involving cognitive functions and awareness',
    'R45': 'Symptoms and signs involving emotional state',
    'R46': 'Symptoms and signs involving appearance and behaviour',
    'R47': 'Speech disturbances, not elsewhere classified',
    'R48': 'Dyslexia and other symbolic dysfunctions, not elsewhere classified',
    'R49': 'Voice and resonance disorders',
    'R50': 'Fever of unspecified origin',
    'R51': 'Headache',
    'R52': 'Pain, unspecified',
    'R53': 'Malaise and fatigue',
    'R54': 'Age-related physical debility',
    'R55': 'Syncope and collapse',
    'R56': 'Convulsions, not elsewhere classified',
    'R57': 'Shock, not elsewhere classified',
    'R58': 'Hemorrhage, not elsewhere classified',
    'R59': 'Enlarged lymph nodes',
    'R60': 'Edema, unspecified',
    'R61': 'Hyperhidrosis',
    'R62': 'Lack of expected normal physiological development',
    'R63': 'Symptoms and signs concerning food and fluid intake',
    'R64': 'Cachexia',
    'R65': 'Symptoms and signs generally characteristic of systemic viral infections',
    'R68': 'Other general symptoms and signs',
    'R69': 'Illness, unspecified',
}

PDGM_EXCLUDED_AFTERCARE_CODES = {
    'Z42': 'Encounter for plastic and reconstructive surgery',
    'Z43': 'Encounter for attention to artificial openings',
    'Z44': 'Encounter for fitting and adjustment of external prosthetic device',
    'Z45': 'Encounter for adjustment and management of implanted device',
    'Z46': 'Encounter for fitting and adjustment of other devices',
    'Z47': 'Orthopedic aftercare',
    'Z48': 'Encounter for change of dressing and removal of wound dressing',
    'Z49': 'Encounter for care involving renal dialysis',
    'Z50': 'Encounter for care involving use of rehabilitation procedures',
    'Z51': 'Encounter for other aftercare and medical care',
}

HOME_HEALTH_RELEVANT_DIAGNOSES = {
    'I50': 'Heart failure',
    'E11': 'Type 2 diabetes mellitus',
    'I10': 'Essential hypertension',
    'J45': 'Asthma',
    'J44': 'Chronic obstructive pulmonary disease (COPD)',
    'L89': 'Pressure ulcer',
    'I86': 'Varicose veins',
    'R40': 'Altered mental status',
    'R41': 'Altered mental status / amnesia',
    'G89': 'Pain, not elsewhere classified',
    'M79': 'Other and unspecified soft tissue disorders',
    'M96': 'Intraoperative and postprocedural complications',
    'T81': 'Complications of care',
    'S72': 'Fracture of femur',
    'S82': 'Fracture of lower leg',
    'M17': 'Bilateral primary osteoarthritis of knee',
    'M19': 'Primary osteoarthritis',
    'M25': 'Other joint disorder',
    'G82': 'Paraplegia and tetraplegia',
    'G83': 'Other paralytic syndromes',
    'I63': 'Cerebral infarction',
    'I61': 'Intracerebral hemorrhage',
    'G04': 'Encephalitis, myelitis, encephalomyelitis',
    'R13': 'Dysphagia',
    'R47': 'Speech disturbances',
}

# ============================================================================
# Homebound Status Indicators
# ============================================================================

PHYSICAL_HOMEBOUND_INDICATORS = [
    'walker', 'wheelchair', 'cane', 'bedbound', 'chairbound', 'o2 dependent',
    'shortness of breath', 'dyspnea', 'severe dyspnea', 'severe sob', 'limited endurance',
    'post-surgical restriction', 'post-op restriction', 'terminal illness', 'severe pain',
    'taxing effort', 'considerable effort', 'unable to leave home', 'requires assistance to leave',
    'severe cardiac', 'severe pulmonary', 'severe respiratory', 'immobilized',
    'amputation', 'paralysis', 'severe weakness', 'legally blind', 'blindness'
]

MEDICAL_HOMEBOUND_INDICATORS = [
    'wound care', 'open wound', 'drainage', 'wound restriction', 'sterile dressing',
    'immunocompromised', 'immune suppressed', 'infectious disease', 'isolation',
    'transmission precaution', 'medically contraindicated', 'medically inadvisable',
    'recent hospitalization', 'acute illness', 'active infection'
]

SAFETY_HOMEBOUND_INDICATORS = [
    'dementia', 'cognitive impairment', 'altered mental status', 'confusion',
    'fall risk', 'high fall risk', 'unsafe alone', 'psychiatric condition',
    'behavioral concerns', 'elopement', 'wandering', 'impaired judgment',
    'lives alone', 'no caregiver', 'safety concern', 'environmental hazard',
    'unable to access community safely'
]

SKILLED_NURSING_INDICATORS = [
    'wound care', 'dressing change', 'wound assessment', 'iv therapy', 'iv infusion',
    'injection', 'insulin', 'foley catheter', 'ostomy', 'tracheostomy',
    'complex medication', 'medication management', 'medication teaching',
    'skilled observation', 'unstable condition', 'parenteral nutrition', 'tube feeding',
    'picc line', 'port', 'diabetic management', 'pain management',
    'cardiac monitoring', 'oxygen titration', 'edema management', 'skin integrity',
    'pressure ulcer', 'surgical wound'
]

THERAPY_INDICATORS = [
    'physical therapy', 'occupational therapy', 'speech therapy', 'speech-language pathology',
    'pt visit', 'ot visit', 'slp visit', 'therapeutic exercise', 'gait training',
    'balance training', 'transfer training', 'strengthening', 'range of motion',
    'adl training', 'functional goal', 'dysphagia', 'swallowing', 'communication',
    'adaptive equipment', 'ambulation training'
]

# ============================================================================
# Logging
# ============================================================================

def setup_logging() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f'intake_screening_{datetime.now().strftime("%Y%m%d")}.log'

    logger = logging.getLogger('intake_screening')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fmt = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# ============================================================================
# Sample Referral Data
# ============================================================================

def _sample_referrals() -> List[Dict]:
    """Return 3 sample referrals for testing: straightforward, problem, and MA case."""
    return [
        {
            'referral_id': 'REF-20260404-001',
            'patient_name': 'John Smith',
            'patient_dob': '1944-06-15',
            'admission_address': '123 Main St, Columbus, OH 43085',
            'referring_physician': 'Dr. Sarah Johnson',
            'physician_npi': '1234567893',
            'primary_diagnosis_code': 'I50.9',
            'primary_diagnosis_description': 'Unspecified heart failure',
            'secondary_diagnoses': ['E11.9 - Type 2 diabetes', 'I10 - Essential hypertension'],
            'referral_narrative': 'Patient hospitalized for acute decompensated heart failure. Discharged on diuretics and ACE inhibitor. Homebound due to severe dyspnea on exertion. Lives with wife. Requires skilled nursing assessment of medication response, edema management, and weight monitoring. Patient is bedbound most of the day.',
            'homebound_status': 'Documented - bedbound, dyspnea, post-hospitalization',
            'insurance': 'Medicare Part A',
            'physician_certification_status': 'Plan of Care signed and dated',
            'facetoface_status': 'Physician visit documented 2 days before admission',
            'equipment_needs': 'None',
        },
        {
            'referral_id': 'REF-20260404-002',
            'patient_name': 'Mary Williams',
            'patient_dob': '1948-03-22',
            'admission_address': '456 Oak Ave, Columbus, OH 43085',
            'referring_physician': 'Dr. Michael Chen',
            'physician_npi': '9876543210',
            'primary_diagnosis_code': 'R52.9',
            'primary_diagnosis_description': 'Unspecified pain',
            'secondary_diagnoses': ['M19.9 - Primary osteoarthritis, unspecified'],
            'referral_narrative': 'Patient with chronic pain and osteoarthritis. Needs help with ADLs. Referred for physical therapy. Lives with son.',
            'homebound_status': 'Vague - "elderly" and "limited mobility"',
            'insurance': 'Medicare Advantage (plan unknown)',
            'physician_certification_status': 'No Plan of Care received - verbal order only',
            'facetoface_status': 'No face-to-face documented',
            'equipment_needs': 'None',
            'issues': ['Primary diagnosis is R-code (symptom) instead of underlying osteoarthritis code',
                       'No Plan of Care signature',
                       'No face-to-face encounter scheduled or documented',
                       'MA prior authorization not obtained',
                       'Homebound status not clearly documented']
        },
        {
            'referral_id': 'REF-20260404-003',
            'patient_name': 'Robert Davis',
            'patient_dob': '1940-11-08',
            'admission_address': '789 Elm Dr, Columbus, OH 43085',
            'referring_physician': 'Dr. Jennifer Lopez',
            'physician_npi': '5555555555',
            'primary_diagnosis_code': 'L89.91',
            'primary_diagnosis_description': 'Pressure ulcer of unspecified site, stage 3',
            'secondary_diagnoses': ['E11.22 - Type 2 diabetes with diabetic chronic kidney disease',
                                   'N18.3 - Chronic kidney disease, stage 3b'],
            'referral_narrative': 'Patient with stage 3 sacral pressure wound and diabetic kidney disease. Post-hospitalization for acute kidney injury. Referred from hospital discharge planning. Homebound due to wound care restrictions and severe deconditioning. Requires sterile dressing changes every 48 hours, skilled wound assessment, and monitoring for infection. Physician wants wound care and nursing management prior to discharge planning.',
            'homebound_status': 'Documented - wound restriction, post-op, severe deconditioning',
            'insurance': 'Medicare Advantage - Aetna',
            'physician_certification_status': 'Plan of Care signed but prior authorization not yet received',
            'facetoface_status': 'NP visit documented 1 day before admission - qualifies',
            'equipment_needs': 'Advanced wound care supplies, specialty dressings',
            'ma_prior_auth_status': 'Pending (submitted, awaiting approval)',
        }
    ]


# ============================================================================
# ICD-10 Validation
# ============================================================================

def validate_icd10_code(code: str) -> Dict[str, Any]:
    """Validate an ICD-10 code for home health appropriateness."""
    code_upper = code.upper().strip()

    # Check format (basic validation)
    if not re.match(r'^[A-Z]\d{2}(\.\d{1,2})?$', code_upper):
        return {
            'valid': False,
            'error': 'Invalid ICD-10 format. Expected format: A12 or A12.34',
            'code': code_upper,
            'is_excluded': False,
            'is_appropriate': False,
        }

    # Extract prefix
    prefix = code_upper[:3]

    # Check if it's a PDGM-excluded Z-code
    if prefix.startswith('Z'):
        if prefix in PDGM_EXCLUDED_Z_CODES:
            return {
                'valid': True,
                'code': code_upper,
                'is_excluded': True,
                'exclusion_type': 'Z-code (social determinant)',
                'description': PDGM_EXCLUDED_Z_CODES[prefix],
                'is_appropriate': False,
                'note': 'Z-codes are generally not appropriate as primary diagnosis for home health. Requires underlying disease code.',
            }

    # Check if it's a PDGM-excluded R-code
    if prefix.startswith('R'):
        if prefix in PDGM_EXCLUDED_R_CODES:
            return {
                'valid': True,
                'code': code_upper,
                'is_excluded': True,
                'exclusion_type': 'R-code (symptom)',
                'description': PDGM_EXCLUDED_R_CODES[prefix],
                'is_appropriate': False,
                'note': 'R-codes (symptoms) should not be primary diagnosis when etiology is known. Use underlying disease code instead.',
            }

    # Check if it's a PDGM-excluded aftercare code
    if prefix in PDGM_EXCLUDED_AFTERCARE_CODES:
        return {
            'valid': True,
            'code': code_upper,
            'is_excluded': True,
            'exclusion_type': 'Aftercare code (Z42-Z51)',
            'description': PDGM_EXCLUDED_AFTERCARE_CODES[prefix],
            'is_appropriate': False,
            'note': 'Aftercare codes are not appropriate as primary diagnosis unless in acute post-op period with active skilled need.',
        }

    # Check if it's a home health-relevant diagnosis
    if prefix in HOME_HEALTH_RELEVANT_DIAGNOSES:
        return {
            'valid': True,
            'code': code_upper,
            'is_excluded': False,
            'is_appropriate': True,
            'description': HOME_HEALTH_RELEVANT_DIAGNOSES[prefix],
            'note': 'This is a legitimate home health diagnosis.',
        }

    # If we reach here, code is valid format but not explicitly in our database
    return {
        'valid': True,
        'code': code_upper,
        'is_excluded': False,
        'is_appropriate': None,  # Unknown — human review required
        'note': 'Code format is valid. Manual review recommended to confirm home health appropriateness.',
    }


# ============================================================================
# Homebound Status Screening
# ============================================================================

def screen_homebound_status(referral_narrative: str) -> Dict[str, Any]:
    """Assess homebound status indicators from referral narrative."""
    narrative_lower = referral_narrative.lower()

    physical_matches = [ind for ind in PHYSICAL_HOMEBOUND_INDICATORS if ind in narrative_lower]
    medical_matches = [ind for ind in MEDICAL_HOMEBOUND_INDICATORS if ind in narrative_lower]
    safety_matches = [ind for ind in SAFETY_HOMEBOUND_INDICATORS if ind in narrative_lower]

    total_matches = len(physical_matches) + len(medical_matches) + len(safety_matches)

    if total_matches >= 3:
        status = 'Strong'
        homebound = True
    elif total_matches >= 1:
        status = 'Present but limited'
        homebound = True
    else:
        status = 'Not documented'
        homebound = False

    return {
        'homebound': homebound,
        'status': status,
        'physical_indicators': physical_matches[:3],
        'medical_indicators': medical_matches[:3],
        'safety_indicators': safety_matches[:3],
        'total_indicators': total_matches,
        'assessment': f'Homebound status is {status}. Patient has {total_matches} documented indicator(s).'
    }


# ============================================================================
# NPI Validation (Stub)
# ============================================================================

def validate_npi(npi: str) -> Dict[str, Any]:
    """
    Validate NPI format and structure.
    In production, this would call the CMS NPPES lookup tool.
    """
    npi_clean = npi.strip()

    # Check length
    if len(npi_clean) != 10 or not npi_clean.isdigit():
        return {
            'valid': False,
            'npi': npi_clean,
            'error': 'NPI must be exactly 10 digits',
            'format_check': 'Failed',
            'nppes_lookup': 'Not performed',
        }

    # Luhn check (basic implementation)
    def luhn_check(num_str):
        digits = [int(d) for d in num_str]
        total = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        return total % 10 == 0

    if not luhn_check(npi_clean):
        return {
            'valid': False,
            'npi': npi_clean,
            'error': 'NPI failed Luhn check digit validation',
            'format_check': 'Failed',
            'nppes_lookup': 'Not performed',
        }

    # Format is valid; in production, would call NPPES lookup here
    return {
        'valid': True,
        'npi': npi_clean,
        'format_check': 'Passed',
        'nppes_lookup': 'Not performed (stub)',
        'note': 'NPI format is valid. In production, would verify enrollment status and credentials with CMS NPPES.',
    }


# ============================================================================
# Screening Engine
# ============================================================================

def screen_referral(referral: Dict) -> Dict[str, Any]:
    """Execute full screening on a referral."""
    results = {
        'referral_id': referral.get('referral_id'),
        'patient_name': referral.get('patient_name'),
        'screening_date': datetime.now().isoformat(),
        'categories': {}
    }

    # Category 1: Clinical Eligibility
    icd10_validation = validate_icd10_code(referral.get('primary_diagnosis_code', ''))
    homebound_assessment = screen_homebound_status(referral.get('referral_narrative', ''))

    clinical_findings = []
    clinical_severity = 'Acceptable'

    if icd10_validation['is_excluded']:
        clinical_findings.append(f"PRIMARY DIAGNOSIS IS EXCLUDED: {icd10_validation['exclusion_type']} - {icd10_validation['note']}")
        clinical_severity = 'Critical Failure'
    elif icd10_validation['is_appropriate'] is False:
        clinical_findings.append(f"PRIMARY DIAGNOSIS QUESTIONABLE: {icd10_validation['note']}")
        clinical_severity = 'Major Concern' if clinical_severity == 'Acceptable' else clinical_severity
    elif icd10_validation['is_appropriate'] is None:
        clinical_findings.append(f"PRIMARY DIAGNOSIS REQUIRES REVIEW: {icd10_validation['note']}")

    if not homebound_assessment['homebound']:
        clinical_findings.append("HOMEBOUND STATUS NOT DOCUMENTED")
        clinical_severity = 'Critical Failure'
    elif homebound_assessment['status'] == 'Present but limited':
        clinical_findings.append(f"HOMEBOUND STATUS VAGUE: Only {homebound_assessment['total_indicators']} indicator(s) documented")
        if clinical_severity != 'Critical Failure':
            clinical_severity = 'Major Concern'

    skilled_need = any(ind in referral.get('referral_narrative', '').lower() for ind in SKILLED_NURSING_INDICATORS + THERAPY_INDICATORS)
    if not skilled_need:
        clinical_findings.append("SKILLED NEED NOT DOCUMENTED")
        clinical_severity = 'Critical Failure'

    if referral.get('facetoface_status', '').lower().startswith('no'):
        clinical_findings.append("NO FACE-TO-FACE ENCOUNTER DOCUMENTED OR SCHEDULED")
        clinical_severity = 'Critical Failure' if clinical_severity != 'Critical Failure' else clinical_severity

    results['categories']['clinical_eligibility'] = {
        'icd10_validation': icd10_validation,
        'homebound_assessment': homebound_assessment,
        'skilled_need_present': skilled_need,
        'facetoface_documented': not referral.get('facetoface_status', '').lower().startswith('no'),
        'findings': clinical_findings if clinical_findings else ['All clinical criteria appear met'],
        'severity': clinical_severity,
    }

    # Category 2: Physician Requirements
    npi_validation = validate_npi(referral.get('physician_npi', ''))
    physician_findings = []
    physician_severity = 'Acceptable'

    if not npi_validation['valid']:
        physician_findings.append(f"INVALID NPI: {npi_validation.get('error')}")
        physician_severity = 'Critical Failure'
    else:
        physician_findings.append(f"NPI FORMAT VALID: {npi_validation['npi']}")

    if 'no plan' in referral.get('physician_certification_status', '').lower() or 'verbal' in referral.get('physician_certification_status', '').lower():
        physician_findings.append("PLAN OF CARE NOT SIGNED BY PHYSICIAN")
        physician_severity = 'Critical Failure'
    else:
        physician_findings.append(f"PLAN OF CARE STATUS: {referral.get('physician_certification_status', 'Unknown')}")

    results['categories']['physician_requirements'] = {
        'npi_validation': npi_validation,
        'physician_certification': referral.get('physician_certification_status', 'Unknown'),
        'findings': physician_findings,
        'severity': physician_severity,
    }

    # Category 3: Insurance & Authorization
    insurance_findings = []
    insurance_severity = 'Acceptable'

    insurance = referral.get('insurance', 'Unknown')
    insurance_findings.append(f"COVERAGE: {insurance}")

    if 'advantage' in insurance.lower():
        ma_status = referral.get('ma_prior_auth_status', 'Unknown')
        if 'pending' in ma_status.lower():
            insurance_findings.append(f"MA PRIOR AUTH PENDING - cannot bill until received")
            if insurance_severity == 'Acceptable':
                insurance_severity = 'Major Concern'
        elif 'received' not in ma_status.lower() and 'approved' not in ma_status.lower():
            insurance_findings.append(f"MA PRIOR AUTH NOT OBTAINED")
            insurance_severity = 'Critical Failure'

    results['categories']['insurance_authorization'] = {
        'coverage_type': insurance,
        'findings': insurance_findings,
        'severity': insurance_severity,
    }

    # Category 4: Operational Readiness
    operational_findings = []
    operational_severity = 'Acceptable'

    address = referral.get('admission_address', 'Unknown')
    if 'columbus, oh' in address.lower():
        operational_findings.append(f"GEOGRAPHY: Within service area (Columbus, OH)")
    else:
        operational_findings.append(f"GEOGRAPHY: {address} - OUT OF AREA")
        operational_severity = 'Critical Failure'

    equipment = referral.get('equipment_needs', 'None')
    operational_findings.append(f"EQUIPMENT NEEDS: {equipment}")

    results['categories']['operational_readiness'] = {
        'address': address,
        'equipment_needs': equipment,
        'findings': operational_findings,
        'severity': operational_severity,
    }

    # Overall Recommendation
    severities = [
        results['categories']['clinical_eligibility']['severity'],
        results['categories']['physician_requirements']['severity'],
        results['categories']['insurance_authorization']['severity'],
        results['categories']['operational_readiness']['severity'],
    ]

    if any(s == 'Critical Failure' for s in severities):
        recommendation = 'DECLINE'
        confidence = 90
    elif any(s == 'Major Concern' for s in severities):
        recommendation = 'CONDITIONAL ACCEPT'
        confidence = 70
    else:
        recommendation = 'ACCEPT'
        confidence = 95

    results['recommendation'] = recommendation
    results['confidence_score'] = confidence

    return results


# ============================================================================
# Reporting
# ============================================================================

def generate_screening_report(screening_result: Dict) -> str:
    """Generate a markdown screening report."""
    report = f"""# Intake Referral Screening Report

**Referral ID:** {screening_result['referral_id']}
**Patient:** {screening_result['patient_name']}
**Screening Date:** {screening_result['screening_date']}

## RECOMMENDATION

**Decision:** {screening_result['recommendation']}
**Confidence:** {screening_result['confidence_score']}%

---

## Clinical Eligibility

**Severity:** {screening_result['categories']['clinical_eligibility']['severity']}

**ICD-10 Primary Diagnosis:**
- Code: {screening_result['categories']['clinical_eligibility']['icd10_validation']['code']}
- Valid: {screening_result['categories']['clinical_eligibility']['icd10_validation']['valid']}
- Excluded: {screening_result['categories']['clinical_eligibility']['icd10_validation']['is_excluded']}
- Appropriate: {screening_result['categories']['clinical_eligibility']['icd10_validation']['is_appropriate']}

**Homebound Status:**
- Status: {screening_result['categories']['clinical_eligibility']['homebound_assessment']['status']}
- Total Indicators: {screening_result['categories']['clinical_eligibility']['homebound_assessment']['total_indicators']}
- Physical: {', '.join(screening_result['categories']['clinical_eligibility']['homebound_assessment']['physical_indicators']) or 'None'}
- Medical: {', '.join(screening_result['categories']['clinical_eligibility']['homebound_assessment']['medical_indicators']) or 'None'}
- Safety: {', '.join(screening_result['categories']['clinical_eligibility']['homebound_assessment']['safety_indicators']) or 'None'}

**Skilled Need Present:** {screening_result['categories']['clinical_eligibility']['skilled_need_present']}

**Face-to-Face Documented:** {screening_result['categories']['clinical_eligibility']['facetoface_documented']}

**Findings:**
"""
    for finding in screening_result['categories']['clinical_eligibility']['findings']:
        report += f"- {finding}\n"

    report += f"""
---

## Physician Requirements

**Severity:** {screening_result['categories']['physician_requirements']['severity']}

**NPI Validation:**
- Valid: {screening_result['categories']['physician_requirements']['npi_validation']['valid']}
- NPI: {screening_result['categories']['physician_requirements']['npi_validation']['npi']}

**Plan of Care:** {screening_result['categories']['physician_requirements']['physician_certification']}

**Findings:**
"""
    for finding in screening_result['categories']['physician_requirements']['findings']:
        report += f"- {finding}\n"

    report += f"""
---

## Insurance & Authorization

**Severity:** {screening_result['categories']['insurance_authorization']['severity']}

**Coverage:** {screening_result['categories']['insurance_authorization']['coverage_type']}

**Findings:**
"""
    for finding in screening_result['categories']['insurance_authorization']['findings']:
        report += f"- {finding}\n"

    report += f"""
---

## Operational Readiness

**Severity:** {screening_result['categories']['operational_readiness']['severity']}

**Address:** {screening_result['categories']['operational_readiness']['address']}
**Equipment Needs:** {screening_result['categories']['operational_readiness']['equipment_needs']}

**Findings:**
"""
    for finding in screening_result['categories']['operational_readiness']['findings']:
        report += f"- {finding}\n"

    report += f"""
---

## Next Steps

"""
    if screening_result['recommendation'] == 'ACCEPT':
        report += "- Route to Admissions Coordinator\n- Begin onboarding process\n- Schedule first visit\n"
    elif screening_result['recommendation'] == 'CONDITIONAL ACCEPT':
        report += "- Identify outstanding conditions that must be resolved\n- Set deadline for resolution\n- Flag for follow-up within 24 hours\n"
    else:  # DECLINE
        report += "- Document decline reason with specific regulation citation\n- Route decline letter to referring practice\n- Offer to reconsider if additional documentation provided\n"

    report += f"\n*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    return report


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Intake & Referral Screening Processor for Enzo Health'
    )
    parser.add_argument('--agency-id', required=True, help='Agency ID (e.g., SUNRISE)')
    parser.add_argument('--referral-id', help='Specific referral ID to screen')
    parser.add_argument('--sample-run', action='store_true', help='Run with sample referrals')
    parser.add_argument('--dry-run', action='store_true', help='Display results without writing to disk')

    args = parser.parse_args()

    logger = setup_logging()
    logger.info(f"Starting intake screening for agency {args.agency_id}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get referrals to process
    if args.sample_run:
        referrals = _sample_referrals()
        logger.info(f"Running with {len(referrals)} sample referrals")
    else:
        logger.error("Only --sample-run is currently implemented")
        sys.exit(1)

    # Process each referral
    for referral in referrals:
        logger.info(f"Screening referral {referral['referral_id']} for patient {referral['patient_name']}")

        screening_result = screen_referral(referral)
        report = generate_screening_report(screening_result)

        if not args.dry_run:
            output_file = OUTPUT_DIR / f"{datetime.now().strftime('%Y-%m-%d')}-{referral['referral_id']}-screening.md"
            output_file.write_text(report)
            logger.info(f"Screening report saved to {output_file}")
        else:
            print(report)

        # Log recommendation
        logger.info(f"Referral {referral['referral_id']}: {screening_result['recommendation']} (confidence: {screening_result['confidence_score']}%)")

    logger.info("Intake screening processing complete")


if __name__ == '__main__':
    main()
