#!/usr/bin/env python3
"""
Scheduling & Visit Frequency Compliance Checker for Enzo Health

Monitors whether patients are receiving ordered visit frequencies per the Plan of Care.
Identifies LUPA (Low Utilization Payment Adjustment) risk, calculates compliance rates,
and flags clinician workload issues.

Usage:
    python scheduling_compliance_checker.py --agency-id SUNRISE
    python scheduling_compliance_checker.py --agency-id SUNRISE --week-of 2026-04-04
    python scheduling_compliance_checker.py --agency-id SUNRISE --dry-run
    python scheduling_compliance_checker.py --agency-id SUNRISE --sample-run
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from collections import defaultdict
import random


# ============================================================================
# Configuration
# ============================================================================

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = WORKSPACE_ROOT / 'scheduling'
LOGS_DIR = Path(__file__).parent / 'logs'

# LUPA Thresholds (minimum visits per 30-day period by PDGM clinical group)
LUPA_THRESHOLDS = {
    'MMTA-Cardiac/Circulatory': 3,
    'MMTA-Endocrine': 3,
    'MMTA-GI/GU': 3,
    'MMTA-Infectious Disease': 3,
    'MMTA-Neuro': 3,
    'MMTA-Respiratory': 3,
    'MMTA-Other': 3,
    'Behavioral Health': 3,
    'Complex Nursing Interventions': 4,
    'MS Rehab': 3,
    'Neuro Rehab': 3,
    'Ortho Rehab': 3,
}

# ============================================================================
# Logging
# ============================================================================

def setup_logging() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f'scheduling_compliance_{datetime.now().strftime("%Y%m%d")}.log'

    logger = logging.getLogger('scheduling_compliance')
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
# Sample Census Data
# ============================================================================

def _sample_census() -> List[Dict]:
    """Return 10 sample patients with ordered frequencies and actual visit data."""
    return [
        {
            'patient_id': 'PT001',
            'patient_name': 'John Smith',
            'admission_date': '2026-03-05',
            'pdgm_group': 'MMTA-Cardiac/Circulatory',
            'ordered_frequencies': {
                'SN': 3,  # 3 visits per week = 12 per 30 days
                'PT': 2,  # 2 visits per week = 8 per 30 days
            },
            'visits_this_week': {
                'SN': 3,  # On track
                'PT': 2,  # On track
            },
            'visits_cumulative_period': {
                'SN': 11,  # 11 visits in ~27 days (1 below expected, but period not over)
                'PT': 7,   # 7 visits in ~27 days
            },
            'days_in_period': 27,
            'period_boundary': 30,  # Last day of 1st 30-day period is day 30
        },
        {
            'patient_id': 'PT002',
            'patient_name': 'Mary Williams',
            'admission_date': '2026-03-01',
            'pdgm_group': 'MMTA-Endocrine',
            'ordered_frequencies': {
                'SN': 2,  # 2 visits per week = 8 per 30 days
            },
            'visits_this_week': {
                'SN': 1,  # One visit this week
            },
            'visits_cumulative_period': {
                'SN': 6,  # Only 6 visits in 34 days (below LUPA minimum of 3)
            },
            'days_in_period': 34,
            'period_boundary': 30,
            'issue': 'LUPA risk — only 6 visits by day 34, well below minimum',
        },
        {
            'patient_id': 'PT003',
            'patient_name': 'Robert Davis',
            'admission_date': '2026-03-10',
            'pdgm_group': 'Complex Nursing Interventions',
            'ordered_frequencies': {
                'SN': 4,  # 4 visits per week = 16 per 30 days
                'PT': 1,  # 1 visit per week = 4 per 30 days
            },
            'visits_this_week': {
                'SN': 4,
                'PT': 1,
            },
            'visits_cumulative_period': {
                'SN': 15,  # 15 visits in 24 days (on track for >16)
                'PT': 3,   # 3 visits in 24 days
            },
            'days_in_period': 24,
            'period_boundary': 30,
        },
        {
            'patient_id': 'PT004',
            'patient_name': 'Patricia Johnson',
            'admission_date': '2026-03-08',
            'pdgm_group': 'MS Rehab',
            'ordered_frequencies': {
                'PT': 3,  # 3 visits per week = 12 per 30 days
                'OT': 2,  # 2 visits per week = 8 per 30 days
            },
            'visits_this_week': {
                'PT': 1,  # Only 1 PT visit this week (should be 3)
                'OT': 2,
            },
            'visits_cumulative_period': {
                'PT': 8,   # 8 visits in 26 days (below expected ~10)
                'OT': 6,   # 6 visits in 26 days (on track)
            },
            'days_in_period': 26,
            'period_boundary': 30,
            'issue': 'PT clinician coverage gap — only 1 visit this week',
        },
        {
            'patient_id': 'PT005',
            'patient_name': 'Michael Brown',
            'admission_date': '2026-02-20',
            'pdgm_group': 'Neuro Rehab',
            'ordered_frequencies': {
                'PT': 2,  # 2 visits per week
                'SLP': 2,  # 2 visits per week (dysphagia management)
            },
            'visits_this_week': {
                'PT': 0,  # No PT this week — patient hospitalized
                'SLP': 1,
            },
            'visits_cumulative_period': {
                'PT': 9,   # 9 visits in 44 days (1st period complete, 2nd in progress)
                'SLP': 8,  # 8 visits in 44 days
            },
            'days_in_period': 44,
            'period_boundary': 60,
            'current_period': 2,  # In 2nd 30-day period
            'issue': 'Hospitalization — missed PT visit; flagged for discharge assessment',
        },
        {
            'patient_id': 'PT006',
            'patient_name': 'Susan Taylor',
            'admission_date': '2026-03-12',
            'pdgm_group': 'MMTA-Respiratory',
            'ordered_frequencies': {
                'SN': 3,  # 3 visits per week
            },
            'visits_this_week': {
                'SN': 3,
            },
            'visits_cumulative_period': {
                'SN': 12,  # 12 visits in 22 days (excellent compliance)
            },
            'days_in_period': 22,
            'period_boundary': 30,
        },
        {
            'patient_id': 'PT007',
            'patient_name': 'Thomas Anderson',
            'admission_date': '2026-03-15',
            'pdgm_group': 'MMTA-GI/GU',
            'ordered_frequencies': {
                'SN': 2,  # 2 visits per week
            },
            'visits_this_week': {
                'SN': 0,  # Patient refused visits this week
            },
            'visits_cumulative_period': {
                'SN': 3,  # 3 visits in 19 days (below expected ~5)
            },
            'days_in_period': 19,
            'period_boundary': 30,
            'issue': 'Low compliance — patient refusing visits',
        },
        {
            'patient_id': 'PT008',
            'patient_name': 'Nancy Lee',
            'admission_date': '2026-03-11',
            'pdgm_group': 'Behavioral Health',
            'ordered_frequencies': {
                'SN': 2,  # 2 visits per week (medication management, psychiatric assessment)
            },
            'visits_this_week': {
                'SN': 2,
            },
            'visits_cumulative_period': {
                'SN': 7,  # 7 visits in 23 days (above minimum)
            },
            'days_in_period': 23,
            'period_boundary': 30,
        },
        {
            'patient_id': 'PT009',
            'patient_name': 'Charles Martinez',
            'admission_date': '2026-03-18',
            'pdgm_group': 'Ortho Rehab',
            'ordered_frequencies': {
                'PT': 3,  # 3 visits per week (post-op knee replacement)
                'OT': 1,  # 1 visit per week
            },
            'visits_this_week': {
                'PT': 3,
                'OT': 1,
            },
            'visits_cumulative_period': {
                'PT': 9,  # 9 visits in 16 days (excellent)
                'OT': 3,  # 3 visits in 16 days
            },
            'days_in_period': 16,
            'period_boundary': 30,
        },
        {
            'patient_id': 'PT010',
            'patient_name': 'Margaret Fernandez',
            'admission_date': '2026-03-06',
            'pdgm_group': 'MMTA-Neuropathy',
            'ordered_frequencies': {
                'SN': 2,  # 2 visits per week (wound care, diabetic education)
                'PT': 1,  # 1 visit per week
            },
            'visits_this_week': {
                'SN': 2,
                'PT': 0,  # No PT this week — clinician off, coverage gap
            },
            'visits_cumulative_period': {
                'SN': 9,   # 9 visits in 25 days (on track)
                'PT': 2,   # 2 visits in 25 days (1 below expected ~3)
            },
            'days_in_period': 25,
            'period_boundary': 30,
            'issue': 'PT clinician coverage gap',
        }
    ]


def _sample_clinician_productivity() -> List[Dict]:
    """Return sample clinician productivity data."""
    return [
        {
            'clinician_id': 'CLIN001',
            'clinician_name': 'Lisa Anderson',
            'discipline': 'SN',
            'caseload_size': 8,
            'visits_this_week': 12,
            'schedule_fill_rate': 85,
            'no_show_rate': 3,
            'reschedule_rate': 5,
        },
        {
            'clinician_id': 'CLIN002',
            'clinician_name': 'David Rodriguez',
            'discipline': 'PT',
            'caseload_size': 6,
            'visits_this_week': 14,
            'schedule_fill_rate': 78,
            'no_show_rate': 8,
            'reschedule_rate': 12,
            'issue': 'Schedule fill rate yellow flag (78%)',
        },
        {
            'clinician_id': 'CLIN003',
            'clinician_name': 'Jennifer Kim',
            'discipline': 'OT',
            'caseload_size': 5,
            'visits_this_week': 9,
            'schedule_fill_rate': 88,
            'no_show_rate': 2,
            'reschedule_rate': 4,
        },
        {
            'clinician_id': 'CLIN004',
            'clinician_name': 'Marcus Johnson',
            'discipline': 'SLP',
            'caseload_size': 4,
            'visits_this_week': 8,
            'schedule_fill_rate': 90,
            'no_show_rate': 1,
            'reschedule_rate': 3,
        },
        {
            'clinician_id': 'CLIN005',
            'clinician_name': 'Angela Torres',
            'discipline': 'PT',
            'caseload_size': 3,
            'visits_this_week': 4,
            'schedule_fill_rate': 45,
            'no_show_rate': 15,
            'reschedule_rate': 20,
            'issue': 'RED FLAG: Schedule fill rate 45%, no-show rate 15%',
        },
    ]


# ============================================================================
# Compliance Scoring Engine
# ============================================================================

def calculate_compliance_rate(visits_ordered: int, visits_actual: int, days_in_period: int, period_days: int = 30) -> float:
    """
    Calculate compliance rate, pro-rated for partial period.
    Example: 11 visits ordered for month, 9 actual in 27 days of 30-day period
    = (9 / (11 * 27/30)) * 100 = (9 / 9.9) * 100 = 90.9%
    """
    if days_in_period == 0 or visits_ordered == 0:
        return 0.0

    expected_visits = visits_ordered * (days_in_period / period_days)
    compliance_rate = (visits_actual / expected_visits) * 100 if expected_visits > 0 else 0.0
    return min(compliance_rate, 100.0)  # Cap at 100%


def calculate_lupa_risk_score(
    visits_actual: int,
    lupa_minimum: int,
    days_remaining: int,
    compliance_rate: float
) -> Tuple[float, str]:
    """
    Calculate LUPA risk score (0-100).
    Components:
    - 60%: Progress toward LUPA minimum (visits_actual / lupa_minimum)
    - 20%: Time remaining in period (days_remaining / 30)
    - 20%: Compliance rate (compliance_rate / 100)
    """
    visits_component = (visits_actual / lupa_minimum) * 60 if lupa_minimum > 0 else 0
    time_component = (days_remaining / 30) * 20
    compliance_component = (min(compliance_rate, 100) / 100) * 20

    score = visits_component + time_component + compliance_component

    if score >= 80:
        risk_level = 'LOW RISK'
    elif score >= 70:
        risk_level = 'MODERATE RISK'
    elif score >= 60:
        risk_level = 'HIGH RISK'
    else:
        risk_level = 'CRITICAL RISK'

    return score, risk_level


def assess_clinician_status(
    schedule_fill_rate: float,
    no_show_rate: float,
    reschedule_rate: float
) -> str:
    """Determine clinician status based on productivity metrics."""
    if schedule_fill_rate < 60 or no_show_rate > 10 or reschedule_rate > 15:
        return 'RED FLAG'
    elif schedule_fill_rate < 75 or no_show_rate > 5 or reschedule_rate > 10:
        return 'YELLOW FLAG'
    else:
        return 'ON TARGET'


# ============================================================================
# Analysis Engine
# ============================================================================

def analyze_patient_compliance(patient: Dict, week_of: date) -> Dict[str, Any]:
    """Analyze a single patient's compliance."""
    result = {
        'patient_id': patient['patient_id'],
        'patient_name': patient['patient_name'],
        'pdgm_group': patient['pdgm_group'],
        'days_in_period': patient['days_in_period'],
        'period_boundary': patient['period_boundary'],
        'disciplines': {},
        'escalations': [],
    }

    lupa_minimum = LUPA_THRESHOLDS.get(patient['pdgm_group'], 3)
    days_remaining = patient['period_boundary'] - patient['days_in_period']

    # Analyze each discipline
    for discipline, ordered_freq in patient['ordered_frequencies'].items():
        visits_actual = patient['visits_cumulative_period'].get(discipline, 0)
        visits_per_week = ordered_freq

        # Calculate expected visits for period
        expected_visits = visits_per_week * (patient['period_boundary'] / 7)

        # Calculate compliance
        compliance_rate = calculate_compliance_rate(
            int(expected_visits),
            visits_actual,
            patient['days_in_period'],
            patient['period_boundary']
        )

        # Calculate LUPA risk (for primary discipline only; simplified model)
        lupa_risk_score, lupa_risk_level = calculate_lupa_risk_score(
            visits_actual,
            lupa_minimum,
            days_remaining,
            compliance_rate
        )

        result['disciplines'][discipline] = {
            'ordered_per_week': visits_per_week,
            'expected_total': int(expected_visits),
            'visits_actual': visits_actual,
            'compliance_rate': round(compliance_rate, 1),
            'lupa_risk_score': round(lupa_risk_score, 1),
            'lupa_risk_level': lupa_risk_level,
            'visits_this_week': patient['visits_this_week'].get(discipline, 0),
        }

        # Flag LUPA risk
        if lupa_risk_level in ('HIGH RISK', 'CRITICAL RISK'):
            result['escalations'].append({
                'type': 'LUPA_RISK',
                'discipline': discipline,
                'message': f'{discipline}: {visits_actual} visits, {lupa_minimum} required, {days_remaining} days remaining',
                'action': 'Schedule urgent visit(s) or contact physician for frequency adjustment'
            })

        # Flag low compliance
        if compliance_rate < 80 and days_remaining > 7:
            result['escalations'].append({
                'type': 'LOW_COMPLIANCE',
                'discipline': discipline,
                'message': f'{discipline}: {compliance_rate:.1f}% compliance ({visits_actual}/{int(expected_visits)} visits)',
                'action': 'Investigate barriers and schedule make-up visits'
            })

        # Flag scheduling gap (no visits this week)
        if patient['visits_this_week'].get(discipline, 0) == 0 and days_remaining > 7:
            result['escalations'].append({
                'type': 'SCHEDULING_GAP',
                'discipline': discipline,
                'message': f'{discipline}: No visits this week',
                'action': 'Contact clinician supervisor to schedule make-up visit'
            })

    # Add patient-level issue if provided in sample data
    if 'issue' in patient:
        result['patient_issue'] = patient['issue']

    result['overall_compliance_rate'] = round(
        sum(d['compliance_rate'] for d in result['disciplines'].values()) / len(result['disciplines']),
        1
    ) if result['disciplines'] else 0

    return result


def analyze_clinician_productivity(clinician: Dict) -> Dict[str, Any]:
    """Analyze a single clinician's productivity."""
    result = {
        'clinician_id': clinician['clinician_id'],
        'clinician_name': clinician['clinician_name'],
        'discipline': clinician['discipline'],
        'caseload_size': clinician['caseload_size'],
        'visits_this_week': clinician['visits_this_week'],
        'schedule_fill_rate': clinician['schedule_fill_rate'],
        'no_show_rate': clinician['no_show_rate'],
        'reschedule_rate': clinician['reschedule_rate'],
        'status': assess_clinician_status(
            clinician['schedule_fill_rate'],
            clinician['no_show_rate'],
            clinician['reschedule_rate']
        ),
    }

    if 'issue' in clinician:
        result['issue'] = clinician['issue']

    return result


# ============================================================================
# Reporting
# ============================================================================

def generate_compliance_report(
    agency_id: str,
    week_of: date,
    patient_analyses: List[Dict],
    clinician_analyses: List[Dict]
) -> str:
    """Generate comprehensive compliance report."""
    report = f"""# Scheduling & Visit Frequency Compliance Report

**Agency:** {agency_id}
**Week of:** {week_of.strftime('%Y-%m-%d')}
**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## EXECUTIVE SUMMARY

| Metric | Value |
|---|---|
| Total Active Patients | {len(patient_analyses)} |
| Patients at LUPA Risk | {sum(1 for p in patient_analyses if any(e['type'] == 'LUPA_RISK' for e in p['escalations']))} |
| Patients with Low Compliance (<80%) | {sum(1 for p in patient_analyses if any(e['type'] == 'LOW_COMPLIANCE' for e in p['escalations']))} |
| Patients with Scheduling Gaps | {sum(1 for p in patient_analyses if any(e['type'] == 'SCHEDULING_GAP' for e in p['escalations']))} |
| Average Compliance Rate (All Patients) | {round(sum(p['overall_compliance_rate'] for p in patient_analyses) / len(patient_analyses), 1)}% |
| Clinicians ON TARGET | {sum(1 for c in clinician_analyses if c['status'] == 'ON TARGET')} |
| Clinicians YELLOW FLAG | {sum(1 for c in clinician_analyses if c['status'] == 'YELLOW FLAG')} |
| Clinicians RED FLAG | {sum(1 for c in clinician_analyses if c['status'] == 'RED FLAG')} |

---

## DETAILED PATIENT ANALYSIS

"""

    # Group patients by risk level
    critical_patients = [p for p in patient_analyses if any(e['type'] == 'LUPA_RISK' and 'CRITICAL' in str(e.get('message', '')) for e in p['escalations'])]
    high_risk_patients = [p for p in patient_analyses if any(e['type'] == 'LUPA_RISK' for e in p['escalations']) and p not in critical_patients]
    moderate_risk_patients = [p for p in patient_analyses if any(e['type'] == 'LOW_COMPLIANCE' for e in p['escalations']) and p not in critical_patients and p not in high_risk_patients]
    on_track_patients = [p for p in patient_analyses if p not in critical_patients and p not in high_risk_patients and p not in moderate_risk_patients]

    if critical_patients:
        report += "### CRITICAL RISK — Immediate Action Required\n\n"
        for patient in critical_patients:
            report += f"**{patient['patient_name']}** (ID: {patient['patient_id']})\n"
            report += f"- PDGM Group: {patient['pdgm_group']}\n"
            report += f"- Days in Period: {patient['days_in_period']} / {patient['period_boundary']}\n"
            report += f"- Overall Compliance: {patient['overall_compliance_rate']}%\n"
            for disc, data in patient['disciplines'].items():
                report += f"- {disc}: {data['visits_actual']}/{data['expected_total']} visits ({data['compliance_rate']}%) | LUPA Risk: {data['lupa_risk_level']}\n"
            for escalation in patient['escalations']:
                report += f"  - **{escalation['type']}:** {escalation['message']}\n"
                report += f"    Action: {escalation['action']}\n"
            if 'patient_issue' in patient:
                report += f"  - Note: {patient['patient_issue']}\n"
            report += "\n"

    if high_risk_patients:
        report += "### HIGH RISK — Schedule Make-Up Visits\n\n"
        for patient in high_risk_patients:
            report += f"**{patient['patient_name']}** (ID: {patient['patient_id']})\n"
            report += f"- PDGM Group: {patient['pdgm_group']}\n"
            report += f"- Overall Compliance: {patient['overall_compliance_rate']}%\n"
            for escalation in patient['escalations']:
                report += f"  - {escalation['message']} → {escalation['action']}\n"
            report += "\n"

    if moderate_risk_patients:
        report += "### MODERATE RISK — Monitor Closely\n\n"
        for patient in moderate_risk_patients[:5]:  # Show first 5
            report += f"**{patient['patient_name']}** (ID: {patient['patient_id']}): {patient['overall_compliance_rate']}% compliance\n"

    if on_track_patients:
        report += f"### ON TRACK — {len(on_track_patients)} patients\n\n"
        report += "All other patients are meeting or exceeding ordered visit frequencies.\n\n"

    # Clinician Productivity
    report += "---\n\n## CLINICIAN PRODUCTIVITY\n\n"

    red_flag_clinicians = [c for c in clinician_analyses if c['status'] == 'RED FLAG']
    yellow_flag_clinicians = [c for c in clinician_analyses if c['status'] == 'YELLOW FLAG']
    on_target_clinicians = [c for c in clinician_analyses if c['status'] == 'ON TARGET']

    if red_flag_clinicians:
        report += "### RED FLAG — Immediate Manager Review\n\n"
        for clinician in red_flag_clinicians:
            report += f"**{clinician['clinician_name']}** ({clinician['discipline']})\n"
            report += f"- Caseload: {clinician['caseload_size']} patients\n"
            report += f"- Visits This Week: {clinician['visits_this_week']}\n"
            report += f"- Schedule Fill Rate: {clinician['schedule_fill_rate']}%\n"
            report += f"- No-Show Rate: {clinician['no_show_rate']}%\n"
            report += f"- Reschedule Rate: {clinician['reschedule_rate']}%\n"
            if 'issue' in clinician:
                report += f"- Issue: {clinician['issue']}\n"
            report += "\n"

    if yellow_flag_clinicians:
        report += "### YELLOW FLAG — Monitor\n\n"
        for clinician in yellow_flag_clinicians:
            report += f"- {clinician['clinician_name']} ({clinician['discipline']}): {clinician['schedule_fill_rate']}% fill rate\n"

    report += f"\n### ON TARGET — {len(on_target_clinicians)} clinicians\n\n"

    # Escalations Summary
    report += "---\n\n## ESCALATION SUMMARY\n\n"

    lupa_escalations = [p for p in patient_analyses for e in p['escalations'] if e['type'] == 'LUPA_RISK']
    if lupa_escalations:
        report += "**Escalate to PDGM Billing Agent:**\n"
        for patient in patient_analyses:
            for escalation in patient['escalations']:
                if escalation['type'] == 'LUPA_RISK':
                    report += f"- {patient['patient_name']} ({patient['patient_id']}): {escalation['message']}\n"

    compliance_escalations = [p for p in patient_analyses for e in p['escalations'] if e['type'] == 'LOW_COMPLIANCE']
    if compliance_escalations:
        report += "\n**Escalate to Clinical QA Agent:**\n"
        for patient in patient_analyses:
            for escalation in patient['escalations']:
                if escalation['type'] == 'LOW_COMPLIANCE':
                    report += f"- {patient['patient_name']} ({patient['patient_id']}): {escalation['message']}\n"

    gap_escalations = [p for p in patient_analyses for e in p['escalations'] if e['type'] == 'SCHEDULING_GAP']
    if gap_escalations:
        report += "\n**Escalate to Scheduling Supervisor:**\n"
        for patient in patient_analyses:
            for escalation in patient['escalations']:
                if escalation['type'] == 'SCHEDULING_GAP':
                    report += f"- {patient['patient_name']} ({patient['patient_id']}): {escalation['message']}\n"

    if red_flag_clinicians:
        report += "\n**Escalate to Clinician Manager:**\n"
        for clinician in red_flag_clinicians:
            report += f"- {clinician['clinician_name']} ({clinician['discipline']}): Review performance and schedule fill rate\n"

    report += f"\n*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    return report


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Scheduling & Visit Frequency Compliance Checker for Enzo Health'
    )
    parser.add_argument('--agency-id', required=True, help='Agency ID (e.g., SUNRISE)')
    parser.add_argument('--week-of', help='Date for week of report (YYYY-MM-DD), defaults to current week')
    parser.add_argument('--sample-run', action='store_true', help='Run with sample census data')
    parser.add_argument('--dry-run', action='store_true', help='Display results without writing to disk')

    args = parser.parse_args()

    logger = setup_logging()
    logger.info(f"Starting scheduling compliance check for agency {args.agency_id}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Determine week of
    if args.week_of:
        week_of = datetime.strptime(args.week_of, '%Y-%m-%d').date()
    else:
        week_of = date.today()

    # Get census data
    if args.sample_run:
        census = _sample_census()
        clinicians = _sample_clinician_productivity()
        logger.info(f"Running with {len(census)} sample patients and {len(clinicians)} clinicians")
    else:
        logger.error("Only --sample-run is currently implemented")
        sys.exit(1)

    # Analyze patients
    patient_analyses = []
    for patient in census:
        analysis = analyze_patient_compliance(patient, week_of)
        patient_analyses.append(analysis)
        logger.info(f"Patient {patient['patient_id']}: {analysis['overall_compliance_rate']}% compliance")

    # Analyze clinicians
    clinician_analyses = []
    for clinician in clinicians:
        analysis = analyze_clinician_productivity(clinician)
        clinician_analyses.append(analysis)
        logger.info(f"Clinician {clinician['clinician_id']}: {analysis['status']}")

    # Generate report
    report = generate_compliance_report(args.agency_id, week_of, patient_analyses, clinician_analyses)

    if not args.dry_run:
        output_file = OUTPUT_DIR / f"{week_of.isoformat()}-scheduling-compliance.md"
        output_file.write_text(report)
        logger.info(f"Compliance report saved to {output_file}")
    else:
        print(report)

    logger.info("Scheduling compliance checking complete")


if __name__ == '__main__':
    main()
