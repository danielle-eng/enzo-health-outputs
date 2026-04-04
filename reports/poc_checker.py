"""
Plan of Care (POC) Compliance Checker
Validates home health patient care plans against the 16 required CMS components under §484.60
Identifies G0574 risk (missing/deficient measurable goals)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import re


@dataclass
class ComplianceComponent:
    """Represents a single POC component compliance check"""
    component_num: int
    component_name: str
    is_present: bool
    is_complete: bool
    is_compliant: bool
    notes: str = ""


@dataclass
class GoalAnalysis:
    """Represents analysis of a single care goal"""
    goal_text: str
    is_measurable: bool
    is_diagnosis_specific: bool
    has_parameters: bool
    has_timeline: bool
    linked_diagnosis: Optional[str] = None
    issues: List[str] = field(default_factory=list)


class PlanOfCareChecker:
    """
    Validates patient POCs against 16 required CMS components
    """

    # The 16 Required POC Components per §484.60
    REQUIRED_COMPONENTS = {
        1: "All pertinent diagnoses",
        2: "Mental/psychosocial/cognitive status",
        3: "Types of services, supplies, and equipment (discipline-specific)",
        4: "Frequency and duration of home health visits (per service)",
        5: "Prognosis and rehabilitation potential",
        6: "Functional limitations",
        7: "Activities permitted",
        8: "Nutritional requirements",
        9: "All medications (including OTC, topicals, supplements)",
        10: "All allergies",
        11: "Safety measures to protect against injury",
        12: "Patient's risk for ED visits and hospitalization (explicit)",
        13: "Patient/caregiver education plan (what, when, by whom)",
        14: "Goals (measurable, specific to each diagnosis)",
        15: "Physician orders (specific and measurable)",
        16: "Discharge/transfer plan"
    }

    # High-risk diagnoses requiring specific goal documentation
    HIGH_RISK_DIAGNOSES = {
        "diabetes": ["blood sugar range", "monitoring frequency", "hypoglycemia signs"],
        "CHF": ["weight gain threshold", "signs of decompensation", "activity tolerance"],
        "wound": ["healing timeline", "wound measurements", "dressing changes"],
        "COPD": ["exacerbation triggers", "oxygen saturation target", "activity tolerance"],
        "post-stroke": ["rehabilitation timeline", "functional milestones", "therapy frequency"],
        "post-op": ["weight bearing progression", "activity restrictions", "healing timeline"],
    }

    def __init__(self, patient_id: str, patient_name: str, diagnoses: List[str], poc_data: Dict):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.diagnoses = [d.lower() for d in diagnoses]
        self.poc_data = poc_data
        self.compliance_results: List[ComplianceComponent] = []
        self.goal_analyses: List[GoalAnalysis] = []
        self.g0574_risk = "LOW"
        self.overall_score = 0.0

    def analyze(self) -> Dict:
        """Run full compliance analysis"""
        self._check_all_components()
        self._analyze_goals()
        self._assess_g0574_risk()
        return self._generate_report()

    def _check_all_components(self):
        """Check presence and completeness of all 16 components"""
        for comp_num, comp_name in self.REQUIRED_COMPONENTS.items():
            is_present = self._is_component_present(comp_num)
            is_complete = self._is_component_complete(comp_num) if is_present else False
            is_compliant = is_present and is_complete

            notes = self._get_component_notes(comp_num)

            self.compliance_results.append(ComplianceComponent(
                component_num=comp_num,
                component_name=comp_name,
                is_present=is_present,
                is_complete=is_complete,
                is_compliant=is_compliant,
                notes=notes
            ))

    def _is_component_present(self, component_num: int) -> bool:
        """Check if component data exists in POC"""
        component_key = f"component_{component_num}"
        data = self.poc_data.get(component_key)

        if data is None or data == "":
            return False
        if isinstance(data, list) and len(data) == 0:
            return False
        if isinstance(data, dict) and len(data) == 0:
            return False
        return True

    def _is_component_complete(self, component_num: int) -> bool:
        """Check if component is complete (not just present)"""
        component_key = f"component_{component_num}"
        data = self.poc_data.get(component_key)

        # Component-specific completeness checks
        if component_num == 1:  # Diagnoses
            return isinstance(data, list) and len(data) > 0
        elif component_num == 9:  # Medications
            return isinstance(data, list) and len(data) > 0
        elif component_num == 10:  # Allergies
            return isinstance(data, list) and len(data) > 0
        elif component_num == 14:  # Goals - checked separately in _analyze_goals
            return isinstance(data, list) and len(data) > 0
        else:
            # For other components, just check if content is substantial
            if isinstance(data, str):
                return len(data.strip()) > 10
            return True

    def _get_component_notes(self, component_num: int) -> str:
        """Get detailed notes about component status"""
        component_key = f"component_{component_num}"
        data = self.poc_data.get(component_key)

        if not data:
            return "MISSING"

        if component_num == 1 and isinstance(data, list):
            return f"Documented: {', '.join(data)}"
        elif component_num == 9 and isinstance(data, list):
            return f"{len(data)} medications documented"
        elif component_num == 10 and isinstance(data, list):
            if len(data) == 0 or (len(data) == 1 and data[0] == "NKDA"):
                return "No documented allergies (or NKDA)"
            return f"Documented: {', '.join(data)}"
        elif component_num == 14:
            if isinstance(data, list):
                return f"{len(data)} goals documented - see goal analysis"
            return str(data)[:50] + "..."
        else:
            return "Present"

    def _analyze_goals(self):
        """Analyze goal measurability and diagnosis-specificity"""
        goals = self.poc_data.get("component_14", [])

        if not goals or not isinstance(goals, list):
            goals = []

        for goal_text in goals:
            analysis = self._analyze_single_goal(goal_text)
            self.goal_analyses.append(analysis)

    def _analyze_single_goal(self, goal_text: str) -> GoalAnalysis:
        """Analyze a single goal for measurability and specificity"""
        goal_lower = goal_text.lower()
        issues = []

        # Check for measurability indicators
        has_numbers = bool(re.search(r'\d+', goal_text))
        has_timeline = any(phrase in goal_lower for phrase in [
            'week', 'month', 'day', 'by end of', 'within', 'by date',
            'during', 'after', 'prior to'
        ])
        has_parameters = any(phrase in goal_lower for phrase in [
            'range', 'percent', '%', 'times', 'times per', 'frequency',
            'level', 'threshold', 'mg', 'lb', 'lbs', 'inches', 'cm'
        ])

        is_measurable = has_numbers or (has_timeline and has_parameters)

        # Check for diagnosis-specificity
        linked_diagnosis = self._find_linked_diagnosis(goal_text)
        is_diagnosis_specific = linked_diagnosis is not None

        # Flag broad statements
        broad_phrases = [
            "will improve", "will receive safe", "will be safe",
            "will get better", "will maintain", "will be stable"
        ]

        if any(phrase in goal_lower for phrase in broad_phrases):
            if not has_numbers and not has_parameters:
                issues.append("Goal is too broad - lacks specific parameters")
                is_measurable = False

        # Check for diagnosis-specific requirements
        if is_diagnosis_specific:
            diagnosis = linked_diagnosis.lower()
            if "diabet" in diagnosis and "range" not in goal_lower and "glucose" not in goal_lower:
                issues.append(f"Diabetes goal missing blood sugar range")
            elif "wound" in diagnosis and "timeline" not in goal_lower and "week" not in goal_lower:
                issues.append(f"Wound goal missing healing timeline")
            elif "copd" in diagnosis and "oxygen" not in goal_lower and "saturation" not in goal_lower:
                issues.append(f"COPD goal missing oxygen saturation target")
        else:
            if not is_broad_phrase(goal_lower):
                issues.append("Goal not linked to specific diagnosis")

        return GoalAnalysis(
            goal_text=goal_text,
            is_measurable=is_measurable,
            is_diagnosis_specific=is_diagnosis_specific,
            has_parameters=has_parameters,
            has_timeline=has_timeline,
            linked_diagnosis=linked_diagnosis,
            issues=issues
        )

    def _find_linked_diagnosis(self, goal_text: str) -> Optional[str]:
        """Try to link goal to a specific patient diagnosis"""
        goal_lower = goal_text.lower()

        for diagnosis in self.diagnoses:
            if diagnosis in goal_lower:
                return diagnosis

        # Check for implied diagnoses
        if any(word in goal_lower for word in ["blood sugar", "glucose", "diabetes", "diabetic"]):
            if any("diabet" in d for d in self.diagnoses):
                return "diabetes"
        if any(word in goal_lower for word in ["heart", "chf", "cardiac", "edema", "weight gain"]):
            if any("chf" in d or "heart" in d for d in self.diagnoses):
                return "CHF"
        if any(word in goal_lower for word in ["wound", "healing", "ulcer", "pressure"]):
            if any("wound" in d or "ulcer" in d for d in self.diagnoses):
                return "wound"
        if any(word in goal_lower for word in ["copd", "breathing", "oxygen", "lung"]):
            if any("copd" in d or "lung" in d for d in self.diagnoses):
                return "COPD"

        return None

    def _assess_g0574_risk(self):
        """Assess risk level for G0574 deficiency"""
        # Check component 14 (goals)
        goals_component = next((c for c in self.compliance_results if c.component_num == 14), None)

        high_risk_count = 0
        medium_risk_count = 0

        # If goals missing entirely
        if not goals_component or not goals_component.is_present:
            self.g0574_risk = "HIGH"
            high_risk_count += 1
        else:
            # Check goal quality
            non_measurable_goals = sum(1 for g in self.goal_analyses if not g.is_measurable)
            non_specific_goals = sum(1 for g in self.goal_analyses if not g.is_diagnosis_specific)

            if non_measurable_goals > 0 or non_specific_goals > 0:
                high_risk_count += 1

        # Check for other critical missing components
        critical_components = [1, 9, 10, 12]  # diagnoses, meds, allergies, ED/hosp risk
        missing_critical = sum(1 for c in self.compliance_results
                              if c.component_num in critical_components and not c.is_present)

        if missing_critical > 1:
            high_risk_count += 1
        elif missing_critical == 1:
            medium_risk_count += 1

        # Determine overall G0574 risk
        if high_risk_count >= 2:
            self.g0574_risk = "HIGH"
        elif high_risk_count == 1 or medium_risk_count >= 2:
            self.g0574_risk = "MEDIUM"
        else:
            self.g0574_risk = "LOW"

    def _generate_report(self) -> Dict:
        """Generate compliance report"""
        # Calculate compliance score
        compliant_count = sum(1 for c in self.compliance_results if c.is_compliant)
        self.overall_score = (compliant_count / len(self.REQUIRED_COMPONENTS)) * 100

        # Identify missing components
        missing_components = [
            f"{c.component_num}: {c.component_name}"
            for c in self.compliance_results if not c.is_present
        ]

        # Identify deficient goals
        deficient_goals = [
            {
                "goal": g.goal_text,
                "issues": g.issues,
                "linked_diagnosis": g.linked_diagnosis
            }
            for g in self.goal_analyses if not g.is_measurable or not g.is_diagnosis_specific
        ]

        # Generate recommendations
        recommendations = self._generate_recommendations()

        return {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "compliance_score": f"{self.overall_score:.1f}%",
            "g0574_risk": self.g0574_risk,
            "compliant_components": compliant_count,
            "total_components": len(self.REQUIRED_COMPONENTS),
            "missing_components": missing_components,
            "deficient_goals": deficient_goals,
            "recommendations": recommendations,
            "cms_citations": self._generate_cms_citations()
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate specific recommendations for gaps"""
        recommendations = []

        for component in self.compliance_results:
            if not component.is_present:
                if component.component_num == 14:
                    recommendations.append(
                        f"URGENT: Add measurable, diagnosis-specific goals to POC. "
                        f"Goals must include parameters, timelines, and be tied to {', '.join(self.diagnoses[:2])}"
                    )
                elif component.component_num == 12:
                    recommendations.append(
                        f"Document explicit assessment of patient's risk for ED visits and hospitalization. "
                        f"Consider diagnoses: {', '.join(self.diagnoses)}"
                    )
                else:
                    recommendations.append(f"Add missing component: {component.component_name}")

        # Goal-specific recommendations
        for goal_analysis in self.goal_analyses:
            if goal_analysis.issues:
                for issue in goal_analysis.issues:
                    recommendations.append(f"Goal issue: {issue}")

        return recommendations[:5]  # Return top 5 recommendations

    def _generate_cms_citations(self) -> str:
        """Generate CMS citation language for deficiencies"""
        citation = ""

        if self.g0574_risk in ["HIGH", "MEDIUM"]:
            citation = (
                "42 CFR 484.60(c) - The plan of care must contain ... "
                "(5) A statement of the specific measurable goals derived from the patient's diagnoses and the "
                "patient's rehabilitation potential ... Goals must be individualized, specific to each diagnosis, "
                "and include measurable parameters. For high-risk diagnoses (diabetes, wounds, COPD, cardiac), "
                "goals must include diagnosis-specific parameters (e.g., blood sugar ranges, wound measurements, "
                "oxygen saturation targets, weight thresholds)."
            )

        return citation


class POCBatchProcessor:
    """Process multiple patient POCs"""

    def __init__(self, patients: List[Dict]):
        self.patients = patients
        self.results = []

    def process_all(self) -> List[Dict]:
        """Process all patient POCs"""
        for patient in self.patients:
            checker = PlanOfCareChecker(
                patient_id=patient["patient_id"],
                patient_name=patient["patient_name"],
                diagnoses=patient["diagnoses"],
                poc_data=patient["poc_data"]
            )
            self.results.append(checker.analyze())
        return self.results

    def print_summary(self):
        """Print executive summary"""
        print("\n" + "="*80)
        print("PLAN OF CARE COMPLIANCE SUMMARY REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        high_risk = sum(1 for r in self.results if r["g0574_risk"] == "HIGH")
        medium_risk = sum(1 for r in self.results if r["g0574_risk"] == "MEDIUM")
        low_risk = sum(1 for r in self.results if r["g0574_risk"] == "LOW")
        avg_score = sum(float(r["compliance_score"].rstrip("%")) for r in self.results) / len(self.results)

        print(f"\nPatients Analyzed: {len(self.results)}")
        print(f"  - HIGH G0574 Risk: {high_risk}")
        print(f"  - MEDIUM G0574 Risk: {medium_risk}")
        print(f"  - LOW G0574 Risk: {low_risk}")
        print(f"Average Compliance Score: {avg_score:.1f}%")
        print("\nDetailed Results:\n")

    def print_detailed_reports(self):
        """Print detailed report for each patient"""
        for report in self.results:
            print("\n" + "-"*80)
            print(f"PATIENT: {report['patient_name']} (ID: {report['patient_id']})")
            print("-"*80)
            print(f"Compliance Score: {report['compliance_score']}")
            print(f"G0574 Risk Level: {report['g0574_risk']}")
            print(f"Components Compliant: {report['compliant_components']}/{report['total_components']}")

            if report['missing_components']:
                print(f"\nMISSING COMPONENTS ({len(report['missing_components'])}):")
                for comp in report['missing_components']:
                    print(f"  - {comp}")

            if report['deficient_goals']:
                print(f"\nDEFICIENT GOALS ({len(report['deficient_goals'])}):")
                for goal in report['deficient_goals']:
                    print(f"  Goal: \"{goal['goal']}\"")
                    if goal['linked_diagnosis']:
                        print(f"    Linked Diagnosis: {goal['linked_diagnosis']}")
                    for issue in goal['issues']:
                        print(f"    Issue: {issue}")

            if report['recommendations']:
                print(f"\nRECOMMENDATIONS:")
                for i, rec in enumerate(report['recommendations'], 1):
                    print(f"  {i}. {rec}")

            if report['cms_citations']:
                print(f"\nCMS CITATION LANGUAGE:")
                print(f"  {report['cms_citations']}")


def is_broad_phrase(text: str) -> bool:
    """Check if text is a generic broad phrase"""
    return any(phrase in text for phrase in [
        "will improve", "will receive", "will be", "will get",
        "will maintain", "will be stable", "will receive safe care"
    ])


# Sample Patient Data
SAMPLE_PATIENTS = [
    {
        "patient_id": "PT-001",
        "patient_name": "Maria Santos",
        "diagnoses": ["CHF", "Diabetes Type 2", "Hypertension"],
        "poc_data": {
            "component_1": ["CHF", "Diabetes Type 2", "Hypertension"],
            "component_2": "Alert and oriented x3",
            "component_3": {"RN": "wound care", "PT": "mobility training"},
            "component_4": "RN 3x/week, PT 2x/week",
            "component_5": "Good prognosis with compliance",
            "component_6": "Limited ambulation, SOB with exertion",
            "component_7": "Bedrest with bathroom privileges",
            "component_8": "Low sodium, diabetic diet",
            "component_9": ["Lisinopril 10mg daily", "Metformin 500mg BID"],
            "component_10": [],  # MISSING
            "component_11": "Fall risk awareness, non-skid socks",
            "component_12": None,  # MISSING - ED/hosp risk not documented
            "component_13": "Education on diet compliance and signs of decompensation",
            "component_14": [
                "Patient will improve heart function",  # TOO BROAD
                "Blood sugars will be controlled",  # NO RANGE
                "Patient will receive safe care"  # TOO BROAD
            ],
            "component_15": "Monitor daily weights, BP monitoring",
            "component_16": "Discharge to self-care when stable"
        }
    },
    {
        "patient_id": "PT-002",
        "patient_name": "James Wilson",
        "diagnoses": ["Post-hip replacement", "History of GERD"],
        "poc_data": {
            "component_1": ["Post-hip replacement (POD 5)", "History of GERD"],
            "component_2": "Alert and oriented x3, motivated",
            "component_3": {"PT": "ambulation and strengthening", "RN": "post-op wound monitoring"},
            "component_4": "PT 3x/week for 4 weeks, RN 2x/week",
            "component_5": "Excellent prognosis, full weight bearing in 4 weeks",
            "component_6": "Right leg strength limited, pain with motion",
            "component_7": "Weight bearing as tolerated with walker",
            "component_8": "Regular diet, avoid GERD triggers",
            "component_9": ["Oxycodone 5mg Q4H PRN", "Pantoprazole 40mg daily"],
            "component_10": ["NKDA"],
            "component_11": "Non-skid footwear, clear pathways, walker at all times",
            "component_12": "Low risk for ED/hospitalization; post-op pain managed; compliance good",
            "component_13": "PT/HHA education on weight bearing restrictions, wound care, pain management by RN and PT",
            "component_14": [
                "Patient will ambulate 50 feet with walker independently by end of week 4",
                "Patient will demonstrate safe transfer technique (bed to chair) by end of week 2",
                "Surgical wound will heal without complications per standard post-op timeline"
            ],
            "component_15": "Weight bearing as tolerated, avoid hip flexion >90 degrees",
            "component_16": "Discharge to home when ambulating 200+ feet with walker, independent ADLs"
        }
    },
    {
        "patient_id": "PT-003",
        "patient_name": "Dorothy Alvarez",
        "diagnoses": ["Wound care", "COPD"],
        "poc_data": {
            "component_1": ["Pressure ulcer stage 3", "COPD with recent exacerbation"],
            "component_2": "Mild cognitive impairment, lives with daughter",
            "component_3": {"RN": "wound care", "HHA": "ADL assistance"},
            "component_4": "RN 2x/week, HHA 3x/week",
            "component_5": "Fair prognosis, wound healing expected",
            "component_6": "Limited mobility, limited lung capacity, pain with activity",
            "component_7": "Bedrest with bathroom privileges",
            "component_8": "Adequate protein intake for healing",
            "component_9": ["Albuterol inhaler", "Metoprolol"],  # INCOMPLETE - missing OTC items
            "component_10": ["Penicillin"],
            "component_11": "Turn/position Q2H, use air mattress",
            "component_12": None,  # MISSING - COPD exacerbation history = high hosp risk
            "component_13": "Daughter educated on wound care and medication administration",
            "component_14": [
                "Wound will heal this episode",  # NO TIMELINE
                "Patient will breathe better"  # NOT MEASURABLE
            ],
            "component_15": "Weekly wound assessments, measure length/width/depth",
            "component_16": None  # MISSING
        }
    },
    {
        "patient_id": "PT-004",
        "patient_name": "Robert Chen",
        "diagnoses": ["Post-stroke", "Hypertension"],
        "poc_data": {
            "component_1": ["CVA (ischemic) 2 weeks ago", "Hypertension"],
            "component_2": "Alert, mild expressive aphasia, motivated",
            "component_3": {"PT": "mobility/strengthening", "SLP": "speech therapy", "OT": "ADL retraining"},
            "component_4": "PT 3x/week, SLP 2x/week, OT 1x/week for 8 weeks",
            "component_5": "Good rehabilitation potential, age 74",  # VAGUE
            "component_6": "Right-sided weakness (3/5), speech difficulty, mild dysphagia",
            "component_7": "Weight bearing with supervision, avoid aspiration",
            "component_8": "Regular diet with swallow precautions",
            "component_9": ["Lisinopril 20mg daily", "Aspirin 81mg daily"],
            "component_10": ["NKDA"],
            "component_11": "Fall precautions, non-skid shoes, supervision during therapy",
            "component_12": "Moderate risk for ED due to new stroke; close BP monitoring",
            "component_13": "Family education on stroke precautions and swallow safety",
            "component_14": [
                "Patient will ambulate 100 feet with supervision by week 4",  # SOMEWHAT MEASURABLE
                "Patient will regain functional speech ability",  # VAGUE TIMELINE
                "Right arm strength will improve"  # NO PARAMETERS
            ],
            "component_15": "BP monitoring BID, swallow precautions",
            "component_16": None  # MISSING
        }
    }
]


if __name__ == "__main__":
    processor = POCBatchProcessor(SAMPLE_PATIENTS)
    processor.process_all()
    processor.print_summary()
    processor.print_detailed_reports()

    print("\n" + "="*80)
    print("END OF COMPLIANCE REPORT")
    print("="*80)
