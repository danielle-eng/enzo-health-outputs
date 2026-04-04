#!/usr/bin/env python3
"""
Daily Action List Aggregator for Enzo Health

Collects urgent items from all agent outputs and produces a prioritized
"Today's Actions" list with three priority tiers:
- CRITICAL (must address today)
- IMPORTANT (address this week)
- FYI (informational, no immediate action)

Generates role-specific views (DON vs Admin) with different emphasis.
"""

import argparse
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Priority(Enum):
    """Action priority tiers."""
    CRITICAL = ('CRITICAL', 'red', '🔴')
    IMPORTANT = ('IMPORTANT', 'yellow', '🟡')
    FYI = ('FYI', 'green', '🟢')

    @property
    def label(self):
        return self.value[0]

    @property
    def color(self):
        return self.value[1]

    @property
    def emoji(self):
        return self.value[2]


class ActionItem:
    """Represents a single action item."""

    def __init__(
        self,
        title: str,
        priority: Priority,
        source: str,
        estimated_time: str,
        details: Dict = None,
        deadline_date: str = None,
    ):
        self.title = title
        self.priority = priority
        self.source = source
        self.estimated_time = estimated_time
        self.details = details or {}
        self.deadline_date = deadline_date
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'priority': self.priority.label,
            'source': self.source,
            'estimated_time': self.estimated_time,
            'details': self.details,
            'deadline_date': self.deadline_date,
            'created_at': self.created_at,
        }


class DailyActionListGenerator:
    """Generates daily action list from multiple sources."""

    def __init__(self, agency_id: str, role: str = 'both', date_str: str = None):
        """Initialize generator with agency, role, and date."""
        if role not in ('don', 'admin', 'both'):
            raise ValueError("Role must be 'don', 'admin', or 'both'")

        self.agency_id = agency_id
        self.role = role
        self.date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.now()
        self.date_str = self.date.strftime('%Y-%m-%d')

        # Workspace paths
        base_path = Path(__file__).parent.parent
        self.scheduling_path = base_path / 'scheduling'
        self.clinical_qa_path = base_path / 'clinical-qa'
        self.recert_path = base_path / 'recert-discharge'
        self.intake_path = base_path / 'intake'
        self.regulatory_path = base_path / 'regulatory'
        self.outcomes_path = base_path / 'outcomes'
        self.output_path = base_path / 'reports' / 'daily-actions'
        self.output_path.mkdir(parents=True, exist_ok=True)

    def generate_actions(self) -> Tuple[List[ActionItem], Dict[str, int]]:
        """Generate action items from all sources."""
        actions = []

        # CRITICAL items
        actions.extend(self._generate_critical_items())

        # IMPORTANT items
        actions.extend(self._generate_important_items())

        # FYI items
        actions.extend(self._generate_fyi_items())

        # Filter by role if needed
        if self.role != 'both':
            actions = self._filter_by_role(actions, self.role)

        # Count by priority
        counts = {
            'CRITICAL': len([a for a in actions if a.priority == Priority.CRITICAL]),
            'IMPORTANT': len([a for a in actions if a.priority == Priority.IMPORTANT]),
            'FYI': len([a for a in actions if a.priority == Priority.FYI]),
            'TOTAL': len(actions),
        }

        return actions, counts

    def _generate_critical_items(self) -> List[ActionItem]:
        """Generate CRITICAL priority items."""
        items = []

        # From scheduling: LUPA risk <5 days, <80% visits
        lupa_data = self._load_sample_scheduling_data()
        for patient in lupa_data.get('patients_lupa_critical', []):
            items.append(ActionItem(
                title=f"Schedule {patient['visits_needed']} visits for {patient['patient_name']} before {patient['deadline']} to avoid LUPA payment reduction",
                priority=Priority.CRITICAL,
                source='Scheduling',
                estimated_time='~30 min',
                details={
                    'patient_id': patient['patient_id'],
                    'visits_needed': patient['visits_needed'],
                    'visit_completion': patient['visit_completion'],
                },
                deadline_date=patient['deadline'],
            ))

        # From recert/discharge: cert expiring <3 days, no physician order
        recert_data = self._load_sample_recert_data()
        for patient in recert_data.get('certs_expiring_critical', []):
            items.append(ActionItem(
                title=f"Obtain recertification order for {patient['patient_name']} — cert ends {patient['cert_end_date']}",
                priority=Priority.CRITICAL,
                source='Recertification',
                estimated_time='~45 min',
                details={
                    'patient_id': patient['patient_id'],
                    'cert_end_date': patient['cert_end_date'],
                },
                deadline_date=patient['cert_end_date'],
            ))

        # From clinical-qa: notes scoring 1-2/5 (high audit risk)
        qa_data = self._load_sample_qa_data()
        for note in qa_data.get('high_risk_notes', []):
            items.append(ActionItem(
                title=f"High audit risk note: {note['patient_name']} visit {note['visit_date']} — {note['clinician']} — review and correct before month end",
                priority=Priority.CRITICAL,
                source='Clinical QA',
                estimated_time='~20 min',
                details={
                    'patient_id': note['patient_id'],
                    'risk_score': note['risk_score'],
                    'visit_date': note['visit_date'],
                },
                deadline_date=(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
            ))

        # From survey deficiency tracker: open deficiencies due <3 days
        deficiency_data = self._load_sample_deficiency_data()
        for deficiency in deficiency_data.get('deficiencies_due_critical', []):
            items.append(ActionItem(
                title=f"Submit Plan of Correction for {deficiency['title']} — due {deficiency['due_date']}",
                priority=Priority.CRITICAL,
                source='Survey Compliance',
                estimated_time='~1.5 hrs',
                details={
                    'deficiency_id': deficiency['deficiency_id'],
                    'category': deficiency['category'],
                },
                deadline_date=deficiency['due_date'],
            ))

        return items

    def _generate_important_items(self) -> List[ActionItem]:
        """Generate IMPORTANT priority items."""
        items = []

        # From scheduling: LUPA risk 5-10 days remaining
        lupa_data = self._load_sample_scheduling_data()
        for patient in lupa_data.get('patients_lupa_important', []):
            items.append(ActionItem(
                title=f"Monitor visit scheduling for {patient['patient_name']} — {patient['visits_needed']} visits needed by {patient['deadline']}",
                priority=Priority.IMPORTANT,
                source='Scheduling',
                estimated_time='~10 min',
                details={
                    'patient_id': patient['patient_id'],
                    'visits_needed': patient['visits_needed'],
                    'days_remaining': patient['days_remaining'],
                },
                deadline_date=patient['deadline'],
            ))

        # From intake: conditional referrals >48 hrs without resolution
        intake_data = self._load_sample_intake_data()
        for referral in intake_data.get('conditional_referrals_pending', []):
            items.append(ActionItem(
                title=f"Follow up on conditional referral {referral['referral_id']} — {referral['issue']}",
                priority=Priority.IMPORTANT,
                source='Intake',
                estimated_time='~20 min',
                details={
                    'referral_id': referral['referral_id'],
                    'submitted_date': referral['submitted_date'],
                    'hours_pending': referral['hours_pending'],
                },
                deadline_date=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            ))

        # From recert/discharge: cert expiring 4-10 days
        recert_data = self._load_sample_recert_data()
        for patient in recert_data.get('certs_expiring_important', []):
            items.append(ActionItem(
                title=f"Schedule case conference for {patient['patient_name']} — cert ends {patient['cert_end_date']}",
                priority=Priority.IMPORTANT,
                source='Recertification',
                estimated_time='~30 min',
                details={
                    'patient_id': patient['patient_id'],
                    'cert_end_date': patient['cert_end_date'],
                    'days_remaining': patient['days_remaining'],
                },
                deadline_date=patient['cert_end_date'],
            ))

        # From OASIS: pending corrections
        qa_data = self._load_sample_qa_data()
        for correction in qa_data.get('pending_oasis_corrections', []):
            items.append(ActionItem(
                title=f"Correct OASIS item {correction['item_code']} for {correction['patient_name']} before next billing cycle",
                priority=Priority.IMPORTANT,
                source='OASIS',
                estimated_time='~15 min',
                details={
                    'patient_id': correction['patient_id'],
                    'item_code': correction['item_code'],
                    'issue': correction['issue'],
                },
                deadline_date=(datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
            ))

        return items

    def _generate_fyi_items(self) -> List[ActionItem]:
        """Generate FYI priority items."""
        items = []

        # From regulatory: new digest available
        regulatory_data = self._load_sample_regulatory_data()
        for digest in regulatory_data.get('new_digests', []):
            items.append(ActionItem(
                title=f"New regulatory digest available: {digest['headline']}",
                priority=Priority.FYI,
                source='Regulatory',
                estimated_time='~10 min',
                details={
                    'digest_id': digest['digest_id'],
                    'published_date': digest['published_date'],
                },
            ))

        # From outcomes: quality indicator changes >2%
        outcomes_data = self._load_sample_outcomes_data()
        for measure in outcomes_data.get('trending_measures', []):
            direction = 'up' if measure['change_pct'] > 0 else 'down'
            items.append(ActionItem(
                title=f"{measure['measure_name']} trending {direction}: {measure['current_rate']}% vs. {measure['prior_rate']}% last period",
                priority=Priority.FYI,
                source='Outcomes',
                estimated_time='~5 min',
                details={
                    'measure_code': measure['measure_code'],
                    'change_pct': measure['change_pct'],
                    'period': measure['period'],
                },
            ))

        # From scheduling: clinician productivity flags
        scheduling_data = self._load_sample_scheduling_data()
        for clinician in scheduling_data.get('clinician_productivity_flags', []):
            items.append(ActionItem(
                title=f"{clinician['name']} schedule fill rate at {clinician['fill_rate']}% — manager review recommended",
                priority=Priority.FYI,
                source='Scheduling',
                estimated_time='~15 min',
                details={
                    'clinician_id': clinician['clinician_id'],
                    'fill_rate': clinician['fill_rate'],
                    'open_slots': clinician['open_slots'],
                },
            ))

        return items

    def _filter_by_role(self, actions: List[ActionItem], role: str) -> List[ActionItem]:
        """Filter actions by role (DON vs Admin)."""
        if role == 'don':
            # DON prioritizes: documentation, survey, clinical items
            relevant_sources = {
                'Clinical QA', 'Survey Compliance', 'Recertification',
                'Outcomes', 'Regulatory',
            }
        elif role == 'admin':
            # Admin prioritizes: revenue, billing, scheduling, operational
            relevant_sources = {
                'Scheduling', 'Intake', 'OASIS', 'Survey Compliance',
                'Regulatory',
            }
        else:
            return actions

        return [a for a in actions if a.source in relevant_sources]

    def save_json_report(self, actions: List[ActionItem], counts: Dict[str, int]) -> str:
        """Save JSON report."""
        report_data = {
            'agency_id': self.agency_id,
            'date': self.date_str,
            'role': self.role,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_items': counts['TOTAL'],
                'critical_count': counts['CRITICAL'],
                'important_count': counts['IMPORTANT'],
                'fyi_count': counts['FYI'],
            },
            'actions': [a.to_dict() for a in actions],
        }

        role_suffix = f"-{self.role}" if self.role != 'both' else ""
        output_file = self.output_path / f"{self.date_str}-{self.agency_id}{role_suffix}-actions.json"

        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"Saved JSON report to {output_file}")
        return str(output_file)

    def save_markdown_report(self, actions: List[ActionItem], counts: Dict[str, int]) -> str:
        """Save human-readable markdown report."""
        role_label = "DON" if self.role == 'don' else ("Admin" if self.role == 'admin' else "All Roles")

        md = f"""# Daily Action List
**Agency:** {self.agency_id}
**Role View:** {role_label}
**Date:** {self.date_str}
**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

| Priority | Count |
|----------|-------|
| 🔴 CRITICAL | {counts['CRITICAL']} |
| 🟡 IMPORTANT | {counts['IMPORTANT']} |
| 🟢 FYI | {counts['FYI']} |
| **TOTAL** | **{counts['TOTAL']}** |

---

## Actions by Priority

"""

        # Critical actions
        critical_actions = [a for a in actions if a.priority == Priority.CRITICAL]
        if critical_actions:
            md += "### 🔴 CRITICAL (Must Address Today)\n\n"
            for i, action in enumerate(critical_actions, 1):
                md += f"{i}. **{action.title}**\n"
                md += f"   - **Source:** {action.source}\n"
                md += f"   - **Time Estimate:** {action.estimated_time}\n"
                if action.deadline_date:
                    md += f"   - **Deadline:** {action.deadline_date}\n"
                md += "\n"

        # Important actions
        important_actions = [a for a in actions if a.priority == Priority.IMPORTANT]
        if important_actions:
            md += "### 🟡 IMPORTANT (Address This Week)\n\n"
            for i, action in enumerate(important_actions, 1):
                md += f"{i}. **{action.title}**\n"
                md += f"   - **Source:** {action.source}\n"
                md += f"   - **Time Estimate:** {action.estimated_time}\n"
                if action.deadline_date:
                    md += f"   - **Deadline:** {action.deadline_date}\n"
                md += "\n"

        # FYI actions
        fyi_actions = [a for a in actions if a.priority == Priority.FYI]
        if fyi_actions:
            md += "### 🟢 FYI (Informational)\n\n"
            for i, action in enumerate(fyi_actions, 1):
                md += f"{i}. **{action.title}**\n"
                md += f"   - **Source:** {action.source}\n"
                md += f"   - **Time Estimate:** {action.estimated_time}\n"
                md += "\n"

        md += "\n---\n*Report generated by Enzo Health Daily Action List Dashboard*\n"

        role_suffix = f"-{self.role}" if self.role != 'both' else ""
        output_file = self.output_path / f"{self.date_str}-{self.agency_id}{role_suffix}-actions.md"

        with open(output_file, 'w') as f:
            f.write(md)

        logger.info(f"Saved markdown report to {output_file}")
        return str(output_file)

    def _load_sample_scheduling_data(self) -> Dict:
        """Return sample scheduling data."""
        return {
            'patients_lupa_critical': [
                {
                    'patient_id': 'P010',
                    'patient_name': 'Margaret Johnson',
                    'visits_needed': 3,
                    'visit_completion': 65,
                    'deadline': (self.date + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'days_remaining': 3,
                }
            ],
            'patients_lupa_important': [
                {
                    'patient_id': 'P011',
                    'patient_name': 'Robert Chen',
                    'visits_needed': 2,
                    'days_remaining': 7,
                    'deadline': (self.date + timedelta(days=7)).strftime('%Y-%m-%d'),
                }
            ],
            'clinician_productivity_flags': [
                {
                    'clinician_id': 'C001',
                    'name': 'Sarah Martinez',
                    'fill_rate': 72,
                    'open_slots': 8,
                },
                {
                    'clinician_id': 'C002',
                    'name': 'David Park',
                    'fill_rate': 68,
                    'open_slots': 12,
                }
            ]
        }

    def _load_sample_recert_data(self) -> Dict:
        """Return sample recertification data."""
        return {
            'certs_expiring_critical': [
                {
                    'patient_id': 'P020',
                    'patient_name': 'Helen Rodriguez',
                    'cert_end_date': (self.date + timedelta(days=2)).strftime('%Y-%m-%d'),
                    'days_remaining': 2,
                }
            ],
            'certs_expiring_important': [
                {
                    'patient_id': 'P021',
                    'patient_name': 'James Thompson',
                    'cert_end_date': (self.date + timedelta(days=7)).strftime('%Y-%m-%d'),
                    'days_remaining': 7,
                }
            ]
        }

    def _load_sample_qa_data(self) -> Dict:
        """Return sample QA data."""
        return {
            'high_risk_notes': [
                {
                    'patient_id': 'P030',
                    'patient_name': 'Carol Anderson',
                    'visit_date': '2026-04-02',
                    'clinician': 'RN Susan Lee',
                    'risk_score': 2,
                }
            ],
            'pending_oasis_corrections': [
                {
                    'patient_id': 'P031',
                    'patient_name': 'Edward Walsh',
                    'item_code': 'M1040',
                    'issue': 'Ambulatory status missing clinical basis',
                }
            ]
        }

    def _load_sample_intake_data(self) -> Dict:
        """Return sample intake data."""
        return {
            'conditional_referrals_pending': [
                {
                    'referral_id': 'REF-2026-0847',
                    'issue': 'Physical therapy not approved by insurance',
                    'submitted_date': (self.date - timedelta(hours=60)).isoformat(),
                    'hours_pending': 60,
                }
            ]
        }

    def _load_sample_deficiency_data(self) -> Dict:
        """Return sample deficiency data."""
        return {
            'deficiencies_due_critical': [
                {
                    'deficiency_id': 'DEF-2026-001',
                    'title': 'Inadequate clinical documentation in initial assessments',
                    'category': 'Documentation',
                    'due_date': (self.date + timedelta(days=2)).strftime('%Y-%m-%d'),
                }
            ]
        }

    def _load_sample_regulatory_data(self) -> Dict:
        """Return sample regulatory data."""
        return {
            'new_digests': [
                {
                    'digest_id': 'REG-2026-0412',
                    'headline': 'CMS Updates LUPA Thresholds for Q2 2026',
                    'published_date': self.date_str,
                }
            ]
        }

    def _load_sample_outcomes_data(self) -> Dict:
        """Return sample outcomes data."""
        return {
            'trending_measures': [
                {
                    'measure_code': 'OUTCOME-HH-001',
                    'measure_name': 'Improvement in ambulation/locomotion',
                    'current_rate': 68.5,
                    'prior_rate': 65.2,
                    'change_pct': 3.3,
                    'period': 'March 2026',
                }
            ]
        }


def main():
    parser = argparse.ArgumentParser(
        description='Generate daily action list for home health agency'
    )
    parser.add_argument(
        '--agency-id',
        required=True,
        help='Agency identifier (e.g., SUNRISE)'
    )
    parser.add_argument(
        '--role',
        default='both',
        choices=['don', 'admin', 'both'],
        help='Role view for action list (default: both)'
    )
    parser.add_argument(
        '--date',
        default=datetime.now().strftime('%Y-%m-%d'),
        help='Action list date in YYYY-MM-DD format (default: today)'
    )

    args = parser.parse_args()

    try:
        generator = DailyActionListGenerator(args.agency_id, args.role, args.date)
        actions, counts = generator.generate_actions()

        # Save reports
        json_file = generator.save_json_report(actions, counts)
        md_file = generator.save_markdown_report(actions, counts)

        # Print summary to stdout
        role_label = "DON" if args.role == 'don' else ("Admin" if args.role == 'admin' else "All Roles")
        print(f"\n{'='*70}")
        print(f"DAILY ACTION LIST - {args.agency_id} ({role_label})")
        print(f"{'='*70}")
        print(f"Date: {generator.date_str}")
        print(f"\nPriority Summary:")
        print(f"  🔴 CRITICAL:  {counts['CRITICAL']:2d} items")
        print(f"  🟡 IMPORTANT: {counts['IMPORTANT']:2d} items")
        print(f"  🟢 FYI:       {counts['FYI']:2d} items")
        print(f"  {'─'*40}")
        print(f"  TOTAL:       {counts['TOTAL']:2d} items")
        print(f"\nReports saved:")
        print(f"  JSON: {json_file}")
        print(f"  Markdown: {md_file}")
        print(f"{'='*70}\n")

        return 0

    except Exception as e:
        logger.error(f"Error generating daily action list: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
