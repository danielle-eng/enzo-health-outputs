"""
G-Tag Deficiency Tracker
Manages open survey deficiencies and generates Plan of Correction drafts in CMS-2567 format
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum


class DeficiencyStatus(Enum):
    """Deficiency lifecycle states"""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CORRECTED = "CORRECTED"
    VERIFIED = "VERIFIED"


class SeverityLevel(Enum):
    """CMS deficiency severity levels"""
    STANDARD = "Standard"
    CONDITION_LEVEL = "Condition-Level"
    IJ = "Immediate Jeopardy"


@dataclass
class Deficiency:
    """Represents a single survey deficiency"""
    g_tag: str
    cop_section: str
    deficiency_description: str
    survey_date: datetime
    severity: SeverityLevel
    patients_cited: List[str]
    status: DeficiencyStatus = DeficiencyStatus.OPEN
    poc_due_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    poc_draft: Optional[str] = None

    def __post_init__(self):
        """Calculate POC due date (10 days from survey)"""
        if self.poc_due_date is None:
            self.poc_due_date = self.survey_date + timedelta(days=10)


class DeficiencyTracker:
    """
    Tracks survey deficiencies and manages POC drafts
    """

    # Complete G-tag to CoP section mapping
    GTAG_MAPPING = {
        # §484.50 Patient Rights (G412-G490)
        "G0412": "§484.50",
        "G0414": "§484.50",
        "G0416": "§484.50",
        "G0418": "§484.50",
        "G0420": "§484.50",
        "G0422": "§484.50",
        "G0424": "§484.50",
        "G0426": "§484.50",
        "G0428": "§484.50",
        "G0430": "§484.50",
        "G0432": "§484.50",
        "G0434": "§484.50",
        "G0436": "§484.50",
        "G0438": "§484.50",
        "G0440": "§484.50",

        # §484.55 Assessment (G514-G546)
        "G0514": "§484.55",
        "G0516": "§484.55",
        "G0518": "§484.55",
        "G0520": "§484.55",
        "G0522": "§484.55",
        "G0524": "§484.55",
        "G0526": "§484.55",
        "G0528": "§484.55",
        "G0530": "§484.55",
        "G0532": "§484.55",
        "G0534": "§484.55",
        "G0536": "§484.55",
        "G0538": "§484.55",
        "G0540": "§484.55",
        "G0542": "§484.55",
        "G0544": "§484.55",
        "G0546": "§484.55",

        # §484.60 Care Planning (G572-G622)
        "G0572": "§484.60",
        "G0574": "§484.60",  # CARE PLAN GOALS - MOST COMMON
        "G0576": "§484.60",
        "G0578": "§484.60",
        "G0580": "§484.60",
        "G0582": "§484.60",
        "G0584": "§484.60",
        "G0586": "§484.60",
        "G0588": "§484.60",
        "G0590": "§484.60",
        "G0592": "§484.60",
        "G0594": "§484.60",
        "G0596": "§484.60",
        "G0598": "§484.60",
        "G0600": "§484.60",
        "G0602": "§484.60",
        "G0604": "§484.60",
        "G0606": "§484.60",
        "G0608": "§484.60",
        "G0610": "§484.60",
        "G0612": "§484.60",
        "G0614": "§484.60",
        "G0616": "§484.60",
        "G0618": "§484.60",
        "G0620": "§484.60",
        "G0622": "§484.60",

        # §484.70 Skilled Services (G704-G730)
        "G0704": "§484.70",
        "G0706": "§484.70",
        "G0708": "§484.70",
        "G0710": "§484.70",
        "G0712": "§484.70",
        "G0714": "§484.70",
        "G0716": "§484.70",
        "G0718": "§484.70",
        "G0720": "§484.70",
        "G0722": "§484.70",
        "G0724": "§484.70",
        "G0726": "§484.70",
        "G0728": "§484.70",
        "G0730": "§484.70",

        # §484.75 Infection Control (G682, G686)
        "G0682": "§484.75",
        "G0686": "§484.75",

        # §484.80 Aide Services (G768-G818)
        "G0768": "§484.80",
        "G0770": "§484.80",
        "G0772": "§484.80",
        "G0774": "§484.80",
        "G0776": "§484.80",
        "G0778": "§484.80",
        "G0780": "§484.80",
        "G0782": "§484.80",
        "G0784": "§484.80",
        "G0786": "§484.80",
        "G0788": "§484.80",
        "G0790": "§484.80",
        "G0792": "§484.80",
        "G0794": "§484.80",
        "G0796": "§484.80",
        "G0798": "§484.80",
        "G0800": "§484.80",
        "G0802": "§484.80",
        "G0804": "§484.80",
        "G0806": "§484.80",
        "G0808": "§484.80",
        "G0810": "§484.80",
        "G0812": "§484.80",
        "G0814": "§484.80",
        "G0816": "§484.80",
        "G0818": "§484.80",
    }

    def __init__(self):
        self.deficiencies: List[Deficiency] = []
        self.organization_name = "Enzo Health Agency"
        self.administrator_name = "Sarah Johnson, Administrator"
        self.don_name = "Michael Torres, DON"

    def add_deficiency(self, deficiency: Deficiency):
        """Add a deficiency to the tracker"""
        self.deficiencies.append(deficiency)
        # Auto-generate POC draft
        deficiency.poc_draft = self._generate_poc_draft(deficiency)

    def get_deficiency_by_gtag(self, g_tag: str) -> Optional[Deficiency]:
        """Retrieve deficiency by G-tag"""
        return next((d for d in self.deficiencies if d.g_tag == g_tag), None)

    def get_open_deficiencies(self) -> List[Deficiency]:
        """Get all OPEN deficiencies"""
        return [d for d in self.deficiencies if d.status == DeficiencyStatus.OPEN]

    def get_in_progress_deficiencies(self) -> List[Deficiency]:
        """Get all IN_PROGRESS deficiencies"""
        return [d for d in self.deficiencies if d.status == DeficiencyStatus.IN_PROGRESS]

    def get_overdue_deficiencies(self) -> List[Deficiency]:
        """Get deficiencies past their POC due date"""
        now = datetime.now()
        return [d for d in self.deficiencies
                if d.poc_due_date and d.poc_due_date < now and d.status != DeficiencyStatus.VERIFIED]

    def update_status(self, g_tag: str, new_status: DeficiencyStatus):
        """Update deficiency status"""
        deficiency = self.get_deficiency_by_gtag(g_tag)
        if deficiency:
            deficiency.status = new_status
            if new_status == DeficiencyStatus.CORRECTED:
                deficiency.completion_date = datetime.now()

    def days_until_poc_due(self, g_tag: str) -> Optional[int]:
        """Calculate days until POC due date"""
        deficiency = self.get_deficiency_by_gtag(g_tag)
        if deficiency and deficiency.poc_due_date:
            days = (deficiency.poc_due_date - datetime.now()).days
            return days
        return None

    def days_overdue(self, g_tag: str) -> Optional[int]:
        """Calculate days overdue for POC submission"""
        deficiency = self.get_deficiency_by_gtag(g_tag)
        if deficiency and deficiency.poc_due_date:
            days = (datetime.now() - deficiency.poc_due_date).days
            if days > 0:
                return days
        return None

    def _generate_poc_draft(self, deficiency: Deficiency) -> str:
        """Generate POC draft in CMS-2567 format"""
        if deficiency.g_tag == "G0574":
            return self._generate_g0574_poc(deficiency)
        elif deficiency.g_tag == "G0514":
            return self._generate_g0514_poc(deficiency)
        elif deficiency.g_tag == "G0682":
            return self._generate_g0682_poc(deficiency)
        else:
            return self._generate_generic_poc(deficiency)

    def _generate_g0574_poc(self, deficiency: Deficiency) -> str:
        """Generate POC for G0574 (Care Plan Goals)"""
        num_cited = len(deficiency.patients_cited)
        survey_date_str = deficiency.survey_date.strftime("%m/%d/%Y")
        completion_date = (deficiency.survey_date + timedelta(days=3)).strftime("%m/%d/%Y")
        system_review_date = (deficiency.survey_date + timedelta(days=7)).strftime("%m/%d/%Y")
        education_date = (deficiency.survey_date + timedelta(days=10)).strftime("%m/%d/%Y")
        poc_due_str = deficiency.poc_due_date.strftime("%m/%d/%Y")

        poc = f"""
CMS-2567 PLAN OF CORRECTION
G-TAG: G0574 - CARE PLAN GOALS
SURVEY DATE: {survey_date_str}
POC DUE DATE: {poc_due_str}
ORGANIZATION: {self.organization_name}

DEFICIENCY:
{deficiency.deficiency_description}

PATIENTS CITED: {', '.join(deficiency.patients_cited)}

================================================================================
PLAN OF CORRECTION
================================================================================

1. IMMEDIATE CORRECTION (Completion Date: {completion_date})
   ─────────────────────────────────────────────────────────────────────────

   The {self.administrator_name} reviewed the {num_cited} records cited in this
   deficiency. Updated plans of care were completed for all cited patients to
   include specific, measurable goals tied to each pertinent diagnosis, including
   the following parameters:

   • For diabetic patients: Blood sugar ranges (e.g., "maintain fasting glucose
     80-130 mg/dL" rather than "blood sugars will be controlled")
   • For wound care patients: Healing timeline with wound measurements
     (e.g., "reduce wound dimensions from 5cm x 3cm to 3cm x 2cm by [date]")
   • For COPD patients: Oxygen saturation targets
     (e.g., "maintain SpO2 >88% during ambulation")
   • For cardiac patients: Weight gain thresholds
     (e.g., "alert HHA if daily weight gain exceeds 2 lbs")

   All updated plans of care were signed by the attending physician. All goals
   are now diagnosis-specific and include measurable outcomes with defined timelines.

   COMPLETION STATUS: ✓ Completed {completion_date}


2. SYSTEM-WIDE IDENTIFICATION (Completion Date: {system_review_date})
   ─────────────────────────────────────────────────────────────────────────

   The DON/Administrator conducted a comprehensive review of all active patient
   records (N={len(deficiency.patients_cited)} at time of survey) to identify
   any additional plans of care that lacked specific, measurable goals.

   REVIEW PROCESS:
   • All active patient POCs were reviewed for goal specificity and measurability
   • Goals were assessed for diagnosis-specific parameters
   • High-risk diagnoses (diabetes, wounds, COPD, cardiac) were flagged for
     enhanced goal documentation review

   FINDINGS: During this system-wide review, [N] additional records were
   identified that required goal revision. Updated plans of care were completed
   for all identified patients and signed by attending physicians.

   COMPLETION STATUS: ✓ Completed {system_review_date}


3. STAFF EDUCATION (Completion Date: {education_date})
   ─────────────────────────────────────────────────────────────────────────

   All clinical staff responsible for completing plans of care received formal
   in-service education on the following topics:

   a) CMS Requirements for Specific, Measurable Goals
      • Goals must be tied to each pertinent diagnosis
      • Goals must include measurable parameters and defined timelines
      • Broad statements (e.g., "patient will improve") are NOT acceptable
      • Reference: 42 CFR 484.60(c)(5)

   b) Goal-Writing Parameters for High-Risk Diagnoses
      • DIABETES: Include target blood sugar ranges, checking frequency,
        recognition of hypo/hyperglycemia symptoms
      • WOUNDS: Include healing timeline, wound measurement parameters
        (length x width x depth), dressing change frequency
      • COPD: Include oxygen saturation targets, activity tolerance parameters,
        exacerbation trigger recognition
      • CARDIAC/CHF: Include weight monitoring thresholds, sodium restrictions,
        signs of decompensation

   c) Documentation of Hospitalization/ED Risk
      • Assessment of patient's explicit risk for ED visits and hospitalization
      • Related to diagnoses, comorbidities, functional status, living situation
      • Required component of §484.60 plan of care

   EDUCATION PROVIDED BY: {self.don_name}
   FORMAT: In-service training, interactive case review

   All clinical staff signed attendance roster documenting participation.

   COMPLETION STATUS: ✓ Completed {education_date}


4. ONGOING MONITORING & COMPLIANCE ASSURANCE
   ─────────────────────────────────────────────────────────────────────────

   The DON will conduct ongoing audits of patient records per the schedule below:

   MONTH 1-3 (Following Survey):
   • Monthly audit of 10% of active patient records (minimum 5 charts)
   • Focus: Verification of goal specificity and measurability
   • Random selection methodology to ensure representativeness

   QUARTER 2 AND FORWARD:
   • Quarterly audit of 10% of active patient records
   • Continued monitoring for compliance and goal quality

   AUDIT REPORT DISTRIBUTION:
   • Audit findings reported to Quality Assurance and Performance Improvement (QAPI)
     committee monthly
   • Executive summary provided to Governing Body quarterly
   • Deficiencies identified during audit trigger immediate corrective action

   STAFF ACCOUNTABILITY:
   • Staff failing to meet POC documentation standards will be subject to:
     - First violation: Documented verbal coaching with re-education
     - Second violation: Written corrective action plan with progress monitoring
     - Third violation: Disciplinary action per HHA personnel policy

   RESPONSIBLE PARTY: {self.administrator_name}
   ONGOING VERIFICATION: Monthly during months 1-3, then quarterly


5. RESPONSIBLE PARTY FOR PLAN OF CORRECTION
   ─────────────────────────────────────────────────────────────────────────

   {self.administrator_name}
   Title: Administrator
   Agency: {self.organization_name}
   Telephone: [Contact Information]


ESTIMATED COMPLETION DATE FOR FULL COMPLIANCE: {poc_due_str}

================================================================================
CERTIFICATION

I certify that this Plan of Correction was prepared by authorized personnel at
{self.organization_name} and that the corrective actions described above
will be implemented to achieve full compliance with 42 CFR 484.60(c)(5)
regarding specific, measurable goals in plans of care.

Signature: ______________________________    Date: ______________
Name: {self.administrator_name}

"""
        return poc

    def _generate_g0514_poc(self, deficiency: Deficiency) -> str:
        """Generate POC for G0514 (OASIS Assessment)"""
        num_cited = len(deficiency.patients_cited)
        survey_date_str = deficiency.survey_date.strftime("%m/%d/%Y")
        completion_date = (deficiency.survey_date + timedelta(days=5)).strftime("%m/%d/%Y")
        poc_due_str = deficiency.poc_due_date.strftime("%m/%d/%Y")

        poc = f"""
CMS-2567 PLAN OF CORRECTION
G-TAG: G0514 - OASIS ASSESSMENT TIMEFRAME
SURVEY DATE: {survey_date_str}
POC DUE DATE: {poc_due_str}
ORGANIZATION: {self.organization_name}

DEFICIENCY:
{deficiency.deficiency_description}

PATIENTS CITED: {', '.join(deficiency.patients_cited)}

================================================================================
PLAN OF CORRECTION
================================================================================

1. IMMEDIATE CORRECTION (Completion Date: {completion_date})
   ─────────────────────────────────────────────────────────────────────────

   The {self.administrator_name} reviewed the {num_cited} records cited in this
   deficiency. Verification of timely OASIS completion was documented for all
   cited patients:

   • SOC/ROC OASIS completed within required timeframe
   • Follow-up OASIS (if applicable) completed per CMS requirements
   • All assessment data entered into billing system within 5 business days

   COMPLETION STATUS: ✓ Completed {completion_date}


2. SYSTEM-WIDE IDENTIFICATION
   ─────────────────────────────────────────────────────────────────────────

   Comprehensive review of all active patient records to ensure OASIS
   assessments are completed within required timeframes. Administrative and
   clinical workflows were reviewed to identify any systemic barriers to timely
   OASIS completion.


3. STAFF EDUCATION
   ─────────────────────────────────────────────────────────────────────────

   All RNs and clinical staff participated in education regarding:
   • CMS timeline requirements for OASIS completion
   • Importance of accurate, timely assessment data
   • Impact on billing, reimbursement, and regulatory compliance


4. ONGOING MONITORING
   ─────────────────────────────────────────────────────────────────────────

   Monthly audits will verify timely OASIS completion. Responsible party: DON.
   Reports to QAPI committee and Governing Body.


5. RESPONSIBLE PARTY
   ─────────────────────────────────────────────────────────────────────────
   {self.administrator_name}, Administrator

ESTIMATED COMPLETION DATE: {poc_due_str}

================================================================================
"""
        return poc

    def _generate_g0682_poc(self, deficiency: Deficiency) -> str:
        """Generate POC for G0682 (Infection Control Program)"""
        survey_date_str = deficiency.survey_date.strftime("%m/%d/%Y")
        completion_date = (deficiency.survey_date + timedelta(days=10)).strftime("%m/%d/%Y")
        poc_due_str = deficiency.poc_due_date.strftime("%m/%d/%Y")

        poc = f"""
CMS-2567 PLAN OF CORRECTION
G-TAG: G0682 - INFECTION PREVENTION AND CONTROL PROGRAM
SURVEY DATE: {survey_date_str}
POC DUE DATE: {poc_due_str}
ORGANIZATION: {self.organization_name}
SEVERITY: {deficiency.severity.value}

DEFICIENCY:
{deficiency.deficiency_description}

================================================================================
PLAN OF CORRECTION
================================================================================

1. IMMEDIATE CORRECTION (Completion Date: {completion_date})
   ─────────────────────────────────────────────────────────────────────────

   The {self.administrator_name} has ensured that a comprehensive Infection
   Prevention and Control Program is in place and being implemented:

   • Written infection prevention and control program established
   • Infection control measures documented for all staff
   • Personal protective equipment (PPE) supply chain verified
   • Standard and transmission-based precautions training provided
   • Surveillance mechanisms for infection identification implemented


2. SYSTEM-WIDE REVIEW AND CORRECTIVE ACTION
   ─────────────────────────────────────────────────────────────────────────

   All clinical practices and protocols have been reviewed for compliance with
   infection control standards. Corrective actions have been implemented:

   • Staff compliance with hand hygiene protocols verified
   • Proper use of PPE confirmed through observation
   • Equipment handling and decontamination procedures reviewed
   • Environmental infection control measures assessed


3. STAFF EDUCATION AND TRAINING
   ─────────────────────────────────────────────────────────────────────────

   All staff received comprehensive training on infection prevention and control:
   • Standard precautions and transmission-based precautions
   • Hand hygiene techniques
   • Proper donning and doffing of PPE
   • Equipment and supply handling
   • Reporting procedures for suspected infections


4. ONGOING MONITORING AND COMPLIANCE VERIFICATION
   ─────────────────────────────────────────────────────────────────────────

   Monthly audits will verify compliance with infection control standards:
   • Observation of staff adherence to protocols
   • Review of infection surveillance data
   • Assessment of PPE availability and use
   • Documentation of education and training


5. RESPONSIBLE PARTY
   ─────────────────────────────────────────────────────────────────────────
   {self.administrator_name}, Administrator
   {self.don_name}, DON


ESTIMATED COMPLETION DATE: {poc_due_str}

NOTE: This is a Condition-Level deficiency. Full correction and verification
is required within the specified timeframe.

================================================================================
"""
        return poc

    def _generate_generic_poc(self, deficiency: Deficiency) -> str:
        """Generate generic POC template for other G-tags"""
        survey_date_str = deficiency.survey_date.strftime("%m/%d/%Y")
        poc_due_str = deficiency.poc_due_date.strftime("%m/%d/%Y")

        poc = f"""
CMS-2567 PLAN OF CORRECTION
G-TAG: {deficiency.g_tag}
COP SECTION: {deficiency.cop_section}
SURVEY DATE: {survey_date_str}
POC DUE DATE: {poc_due_str}
ORGANIZATION: {self.organization_name}
SEVERITY: {deficiency.severity.value}

DEFICIENCY:
{deficiency.deficiency_description}

PATIENTS CITED: {', '.join(deficiency.patients_cited) if deficiency.patients_cited else 'Agency-wide'}

================================================================================
PLAN OF CORRECTION
================================================================================

1. IMMEDIATE CORRECTION
   ─────────────────────────────────────────────────────────────────────────
   [Specific corrective actions for cited records]


2. SYSTEM-WIDE IDENTIFICATION
   ─────────────────────────────────────────────────────────────────────────
   [Review of all patient records to identify similar deficiencies]


3. STAFF EDUCATION
   ─────────────────────────────────────────────────────────────────────────
   [Training provided to all affected staff]


4. ONGOING MONITORING
   ─────────────────────────────────────────────────────────────────────────
   [Quarterly audits and verification procedures]


5. RESPONSIBLE PARTY
   ─────────────────────────────────────────────────────────────────────────
   {self.administrator_name}, Administrator


ESTIMATED COMPLETION DATE: {poc_due_str}

================================================================================
"""
        return poc

    def get_executive_summary(self) -> str:
        """Generate executive summary of all deficiencies by CoP"""
        summary = "\n" + "="*80 + "\n"
        summary += "DEFICIENCY EXECUTIVE SUMMARY - BY COP SECTION\n"
        summary += "="*80 + "\n\n"

        # Group by COP section
        by_section = {}
        for deficiency in self.deficiencies:
            section = deficiency.cop_section
            if section not in by_section:
                by_section[section] = []
            by_section[section].append(deficiency)

        # Sort sections
        sorted_sections = sorted(by_section.keys())

        for section in sorted_sections:
            section_deficiencies = by_section[section]
            summary += f"\n{section} - {len(section_deficiencies)} Deficiency/ies\n"
            summary += "-" * 80 + "\n"

            for deficiency in section_deficiencies:
                status_indicator = {
                    DeficiencyStatus.OPEN: "●",
                    DeficiencyStatus.IN_PROGRESS: "◐",
                    DeficiencyStatus.CORRECTED: "◑",
                    DeficiencyStatus.VERIFIED: "✓"
                }
                indicator = status_indicator.get(deficiency.status, "?")

                days_due = self.days_until_poc_due(deficiency.g_tag)
                days_over = self.days_overdue(deficiency.g_tag)

                summary += f"\n  {indicator} G-TAG: {deficiency.g_tag}\n"
                summary += f"    Status: {deficiency.status.value}\n"
                summary += f"    Severity: {deficiency.severity.value}\n"
                summary += f"    Survey Date: {deficiency.survey_date.strftime('%m/%d/%Y')}\n"
                summary += f"    POC Due: {deficiency.poc_due_date.strftime('%m/%d/%Y')}\n"

                if days_due is not None and days_due >= 0:
                    summary += f"    Days Until Due: {days_due}\n"
                elif days_over is not None and days_over > 0:
                    summary += f"    ⚠ OVERDUE: {days_over} days\n"

                if len(deficiency.patients_cited) > 0:
                    summary += f"    Patients Cited: {', '.join(deficiency.patients_cited)}\n"

        summary += "\n" + "="*80 + "\n"
        summary += f"TOTAL DEFICIENCIES: {len(self.deficiencies)}\n"
        summary += f"  OPEN: {len(self.get_open_deficiencies())}\n"
        summary += f"  IN PROGRESS: {len(self.get_in_progress_deficiencies())}\n"
        summary += f"  OVERDUE: {len(self.get_overdue_deficiencies())}\n"
        summary += "="*80 + "\n"

        return summary


# Sample Deficiencies
SAMPLE_DEFICIENCIES = [
    Deficiency(
        g_tag="G0574",
        cop_section="§484.60",
        deficiency_description=(
            "Agency failed to ensure specific and measurable goals in plans of care. "
            "Review of 10 records revealed 3 records with goals that lacked specific, measurable "
            "parameters tied to patient diagnoses. Goals included broad statements such as "
            "'patient will improve' and 'blood sugars will be controlled' without specific targets "
            "or timelines. High-risk diagnoses (diabetes, CHF, wounds) lacked diagnosis-specific "
            "parameters (blood sugar ranges, weight thresholds, wound measurements)."
        ),
        survey_date=datetime(2026, 3, 15),
        severity=SeverityLevel.STANDARD,
        patients_cited=["PT-001", "PT-003", "PT-004"],
        status=DeficiencyStatus.IN_PROGRESS
    ),
    Deficiency(
        g_tag="G0514",
        cop_section="§484.55",
        deficiency_description=(
            "Agency failed to complete OASIS assessments within required timeframes. "
            "Review of 10 records revealed 2 records where Start of Care (SOC) OASIS was not "
            "completed within 5 calendar days of opening."
        ),
        survey_date=datetime(2026, 3, 15),
        severity=SeverityLevel.STANDARD,
        patients_cited=["PT-002", "PT-005"],
        status=DeficiencyStatus.OPEN
    ),
    Deficiency(
        g_tag="G0682",
        cop_section="§484.75",
        deficiency_description=(
            "Agency failed to maintain a comprehensive infection prevention and control program. "
            "Survey revealed that the agency lacked written policies and procedures for "
            "prevention and control of infections, and staff demonstrated inconsistent use of "
            "personal protective equipment. This deficiency is cited at the Condition-Level severity."
        ),
        survey_date=datetime(2026, 3, 15),
        severity=SeverityLevel.CONDITION_LEVEL,
        patients_cited=[],
        status=DeficiencyStatus.CORRECTED,
        completion_date=datetime(2026, 3, 25)
    )
]


def print_poc_draft(deficiency: Deficiency):
    """Print a deficiency's POC draft"""
    if deficiency.poc_draft:
        print(deficiency.poc_draft)


if __name__ == "__main__":
    # Initialize tracker
    tracker = DeficiencyTracker()

    # Add sample deficiencies
    for deficiency in SAMPLE_DEFICIENCIES:
        tracker.add_deficiency(deficiency)

    # Print executive summary
    print(tracker.get_executive_summary())

    # Print detailed POC drafts
    print("\n\n" + "="*80)
    print("SAMPLE POC DRAFT - G0574 (MOST CRITICAL)")
    print("="*80)
    g0574_deficiency = tracker.get_deficiency_by_gtag("G0574")
    if g0574_deficiency:
        print_poc_draft(g0574_deficiency)

    # Print G0514 POC
    print("\n\n" + "="*80)
    print("SAMPLE POC DRAFT - G0514 (OASIS)")
    print("="*80)
    g0514_deficiency = tracker.get_deficiency_by_gtag("G0514")
    if g0514_deficiency:
        print_poc_draft(g0514_deficiency)

    # Print G0682 POC
    print("\n\n" + "="*80)
    print("SAMPLE POC DRAFT - G0682 (INFECTION CONTROL - CONDITION-LEVEL)")
    print("="*80)
    g0682_deficiency = tracker.get_deficiency_by_gtag("G0682")
    if g0682_deficiency:
        print_poc_draft(g0682_deficiency)

    # Print timing analysis
    print("\n\n" + "="*80)
    print("POC TIMELINE ANALYSIS")
    print("="*80 + "\n")
    for deficiency in tracker.deficiencies:
        days_due = tracker.days_until_poc_due(deficiency.g_tag)
        days_over = tracker.days_overdue(deficiency.g_tag)
        print(f"G-TAG: {deficiency.g_tag}")
        print(f"  POC Due Date: {deficiency.poc_due_date.strftime('%m/%d/%Y')}")
        if days_due is not None and days_due >= 0:
            print(f"  Days Until Due: {days_due}")
        elif days_over is not None and days_over > 0:
            print(f"  STATUS: {days_over} days OVERDUE ⚠")
        print()

    print("\n" + "="*80)
    print("RECOMMENDATIONS FOR AGENCY LEADERSHIP")
    print("="*80)
    print("""
1. G0574 (CARE PLAN GOALS) - IN PROGRESS:
   - CRITICAL PRIORITY: Complete POC draft within next 3 days
   - Ensure all 3 cited patient POCs are updated with specific, measurable goals
   - Conduct staff in-service on goal-writing requirements
   - Expected completion: by March 25, 2026

2. G0514 (OASIS) - OPEN:
   - Submit POC draft by March 25, 2026 (10 days from survey)
   - Review all active patient records for timely OASIS completion
   - Identify and correct any late assessments
   - Implement monitoring system to prevent future delays

3. G0682 (INFECTION CONTROL) - CORRECTED:
   - Program is documented as corrected as of March 25, 2026
   - Awaiting surveyor verification
   - Continue monthly staff education and compliance audits
   - Expected verification: April-May 2026

OVERALL AGENCY STATUS:
   - 1 Condition-Level deficiency (G0682) - requires verification
   - 2 Standard-Level deficiencies - require timely POC and correction
   - All POCs must be submitted by March 25, 2026
   - Recommend monthly compliance audits for remainder of calendar year
""")

    print("="*80 + "\n")
