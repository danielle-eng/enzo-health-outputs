#!/usr/bin/env python3
"""
Recertification / Discharge Processor for Enzo Health

Pulls recent visit notes from the Scribe API for patients approaching their
60-day Medicare certification end date, evaluates continued skilled need
across four clinical domains, and drafts a narrative case conference note
supporting either recertification or discharge from the agency.

Usage:
    python recert_discharge_processor.py --agency-id SUNRISE
    python recert_discharge_processor.py --agency-id SUNRISE --window-days 14
    python recert_discharge_processor.py --agency-id SUNRISE --dry-run
    python recert_discharge_processor.py --agency-id SUNRISE --patient-id PT001
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import time


# ============================================================================
# Configuration
# ============================================================================

SCRIBE_BASE_URL = os.environ.get('ENZO_SCRIBE_BASE_URL', '').rstrip('/')
API_KEY = os.environ.get('ENZO_API_KEY', '')

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = WORKSPACE_ROOT / 'clinical-qa' / 'recert'
LOGS_DIR = Path(__file__).parent / 'logs'

# Default look-ahead window for recert: flag patients whose cert ends within N days
DEFAULT_WINDOW_DAYS = 14

# Medicare home health certification period
CERT_PERIOD_DAYS = 60

# Minimum number of recent notes to pull for review
MIN_NOTES_FOR_REVIEW = 3

# ============================================================================
# Skilled Need Criteria
# ============================================================================

MEDICARE_HOMEBOUND_INDICATORS = [
    "homebound", "unable to leave home", "taxing effort", "considerable effort",
    "requires assistance to leave", "walker", "wheelchair", "bedbound",
    "shortness of breath", "legally blind", "psychiatric condition",
    "cannot ambulate", "fall risk", "unsafe to leave", "medical contraindication"
]

SKILLED_NURSING_INDICATORS = [
    "wound care", "wound assessment", "dressing change", "iv therapy", "iv infusion",
    "injection", "insulin", "foley catheter", "ostomy", "tracheostomy",
    "complex medication management", "medication teaching", "skilled observation",
    "assessment of unstable condition", "parenteral nutrition", "tube feeding",
    "picc line", "port", "diabetic management", "pain management",
    "cardiac monitoring", "blood pressure management", "oxygen titration",
    "edema management", "skin integrity", "pressure ulcer", "surgical wound",
    "staples", "sutures", "drain", "colostomy", "urostomy"
]

THERAPY_INDICATORS = [
    "physical therapy", "occupational therapy", "speech therapy", "speech-language",
    "pt visit", "ot visit", "slp visit", "therapeutic exercise", "gait training",
    "balance training", "transfer training", "strengthening", "range of motion",
    "activities of daily living", "adl training", "cognitive rehabilitation",
    "dysphagia", "swallowing", "communication", "home exercise program",
    "adaptive equipment", "functional goal", "restoration", "maintenance therapy",
    "fall prevention", "ambulation training", "stair training", "energy conservation"
]

SAFETY_CAREGIVER_INDICATORS = [
    "fall risk", "fall precautions", "high fall risk", "cognitively impaired",
    "confusion", "dementia", "alzheimer", "caregiver", "caregiver education",
    "lives alone", "unsafe alone", "elopement", "wandering", "medication errors",
    "non-compliant", "poor safety awareness", "environmental hazard",
    "caregiver burden", "caregiver fatigue", "inadequate support",
    "social isolation", "behavioral concerns", "impaired judgment",
    "poor insight", "safety concern", "home hazard"
]

DISCHARGE_READINESS_INDICATORS = [
    "goals met", "goals achieved", "independent", "no longer requires skilled",
    "stable condition", "no active wound", "self-managing", "caregiver independent",
    "patient independent", "returning to prior level", "plateau",
    "no further skilled need", "discharge appropriate", "community resources",
    "outpatient follow-up", "physician follow-up", "well-controlled",
    "consistent compliance", "no new concerns", "maintenance only"
]

# ============================================================================
# Logging
# ============================================================================

def setup_logging() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f'recert_discharge_{datetime.now().strftime("%Y%m%d")}.log'

    logger = logging.getLogger('recert_discharge')
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
# Scribe API Interface
# ============================================================================

def fetch_patients_approaching_recert(agency_id: str, window_days: int, logger: logging.Logger) -> List[Dict]:
    """
    Fetch patients whose certification end date falls within `window_days` from today.
    Returns list of patient dicts with id, name, soc_date, cert_end_date, disciplines.

    In production this calls the Scribe API. The endpoint is expected to be:
      GET /api/v1/patients?agency_id=<id>&cert_end_before=<date>&status=active
    """
    if not SCRIBE_BASE_URL or not API_KEY:
        logger.warning("ENZO_SCRIBE_BASE_URL or ENZO_API_KEY not set — using sample data")
        return _sample_patient_list(agency_id, window_days)

    try:
        import requests
        cutoff_date = (date.today() + timedelta(days=window_days)).isoformat()
        today_str = date.today().isoformat()

        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        params = {
            "agency_id": agency_id,
            "status": "active",
            "cert_end_before": cutoff_date,
            "cert_end_after": today_str,
        }

        resp = requests.get(f"{SCRIBE_BASE_URL}/api/v1/patients", headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        patients = resp.json().get("patients", [])
        logger.info(f"Fetched {len(patients)} patients approaching recert for {agency_id}")
        return patients

    except Exception as e:
        logger.error(f"Error fetching patients from Scribe API: {e}")
        logger.info("Falling back to sample data for demonstration")
        return _sample_patient_list(agency_id, window_days)


def fetch_recent_notes(patient_id: str, agency_id: str, days_back: int = 21, logger: Optional[logging.Logger] = None) -> List[Dict]:
    """
    Fetch recent visit notes for a patient from Scribe.
    Returns list of note dicts with date, discipline, clinician, and note_text.
    """
    if not SCRIBE_BASE_URL or not API_KEY:
        return _sample_notes_for_patient(patient_id)

    try:
        import requests
        since_date = (date.today() - timedelta(days=days_back)).isoformat()
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        params = {
            "agency_id": agency_id,
            "patient_id": patient_id,
            "since": since_date,
            "sort": "date_desc",
            "limit": 20,
        }

        resp = requests.get(f"{SCRIBE_BASE_URL}/api/v1/notes", headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        notes = resp.json().get("notes", [])
        if logger:
            logger.info(f"Fetched {len(notes)} recent notes for patient {patient_id}")
        return notes

    except Exception as e:
        if logger:
            logger.error(f"Error fetching notes for {patient_id}: {e}")
        return _sample_notes_for_patient(patient_id)


# ============================================================================
# Clinical Evaluation Engine
# ============================================================================

def evaluate_homebound_status(notes: List[Dict]) -> Dict:
    """Check if notes support continued Medicare homebound status."""
    all_text = " ".join(n.get("note_text", "").lower() for n in notes)
    matched = [ind for ind in MEDICARE_HOMEBOUND_INDICATORS if ind in all_text]

    if len(matched) >= 3:
        strength = "Strong"
        supported = True
    elif len(matched) >= 1:
        strength = "Present but limited"
        supported = True
    else:
        strength = "Not documented"
        supported = False

    return {
        "supported": supported,
        "strength": strength,
        "indicators_found": matched[:5],
        "note": "Homebound status is documented in recent visit notes." if supported
                else "Homebound status documentation is absent or insufficient in recent notes — this is a compliance risk."
    }


def evaluate_skilled_nursing_need(notes: List[Dict]) -> Dict:
    """Identify ongoing skilled nursing needs from recent notes."""
    sn_notes = [n for n in notes if n.get("discipline", "").upper() in ("SN", "RN", "LPN", "NURSING")]
    all_text = " ".join(n.get("note_text", "").lower() for n in sn_notes) if sn_notes else \
               " ".join(n.get("note_text", "").lower() for n in notes)

    matched = [ind for ind in SKILLED_NURSING_INDICATORS if ind in all_text]
    discharge_signals = [ind for ind in DISCHARGE_READINESS_INDICATORS if ind in all_text]

    if len(matched) >= 4:
        level = "High"
        ongoing = True
    elif len(matched) >= 1:
        level = "Moderate"
        ongoing = True
    elif len(discharge_signals) >= 2:
        level = "None identified — discharge signals present"
        ongoing = False
    else:
        level = "Low / unclear"
        ongoing = False

    return {
        "ongoing": ongoing,
        "level": level,
        "skilled_needs_identified": matched[:6],
        "discharge_signals": discharge_signals[:3],
    }


def evaluate_therapy_need(notes: List[Dict]) -> Dict:
    """Identify ongoing therapy needs (PT/OT/SLP) from recent notes."""
    therapy_notes = [n for n in notes if n.get("discipline", "").upper() in ("PT", "OT", "SLP", "ST")]
    all_text = " ".join(n.get("note_text", "").lower() for n in therapy_notes) if therapy_notes else \
               " ".join(n.get("note_text", "").lower() for n in notes)

    matched = [ind for ind in THERAPY_INDICATORS if ind in all_text]
    disciplines_active = list({n.get("discipline", "Unknown").upper() for n in therapy_notes})

    goals_mentioned = any(kw in all_text for kw in ["goal", "functional goal", "rehab goal", "objective"])
    goals_met = any(kw in all_text for kw in ["goals met", "goals achieved", "goal achieved", "met goal"])

    if len(matched) >= 3 and not goals_met:
        ongoing = True
        level = "Active therapy with measurable goals"
    elif len(matched) >= 1 and goals_met:
        ongoing = False
        level = "Goals met — therapy may be appropriate for discharge"
    elif len(matched) >= 1:
        ongoing = True
        level = "Some therapy need identified"
    else:
        ongoing = False
        level = "No therapy need documented"

    return {
        "ongoing": ongoing,
        "level": level,
        "therapy_needs_identified": matched[:5],
        "active_disciplines": disciplines_active,
        "goals_documented": goals_mentioned,
        "goals_met_signal": goals_met,
    }


def evaluate_safety_caregiver(notes: List[Dict]) -> Dict:
    """Assess safety concerns and caregiver support factors."""
    all_text = " ".join(n.get("note_text", "").lower() for n in notes)
    matched = [ind for ind in SAFETY_CAREGIVER_INDICATORS if ind in all_text]

    high_concern_terms = ["lives alone", "cognitively impaired", "dementia", "high fall risk",
                          "unsafe alone", "caregiver burden", "elopement", "behavioral concerns"]
    high_concerns = [t for t in high_concern_terms if t in all_text]

    if len(high_concerns) >= 2:
        level = "High — significant safety/caregiver concerns"
        warrants_continued_care = True
    elif len(matched) >= 2:
        level = "Moderate — safety concerns noted"
        warrants_continued_care = True
    elif len(matched) >= 1:
        level = "Low — minor concerns documented"
        warrants_continued_care = False
    else:
        level = "No safety concerns documented"
        warrants_continued_care = False

    return {
        "warrants_continued_care": warrants_continued_care,
        "level": level,
        "concerns_identified": matched[:6],
        "high_concern_flags": high_concerns,
    }


def make_recommendation(homebound: Dict, skilled_nursing: Dict, therapy: Dict, safety: Dict) -> Tuple[str, str, int]:
    """
    Synthesize domain evaluations into a RECERTIFY or DISCHARGE recommendation.
    Returns: (recommendation, rationale, confidence_score_0_to_100)
    """
    recert_score = 0
    discharge_score = 0

    # Homebound
    if homebound["supported"] and homebound["strength"] == "Strong":
        recert_score += 25
    elif homebound["supported"]:
        recert_score += 15
    else:
        discharge_score += 20

    # Skilled nursing
    if skilled_nursing["ongoing"] and skilled_nursing["level"] == "High":
        recert_score += 30
    elif skilled_nursing["ongoing"]:
        recert_score += 20
    else:
        discharge_score += 25

    # Therapy
    if therapy["ongoing"] and not therapy["goals_met_signal"]:
        recert_score += 25
    elif therapy["goals_met_signal"]:
        discharge_score += 20
    elif not therapy["ongoing"] and not therapy["active_disciplines"]:
        discharge_score += 10

    # Safety/caregiver
    if safety["warrants_continued_care"] and safety["level"].startswith("High"):
        recert_score += 20
    elif safety["warrants_continued_care"]:
        recert_score += 10
    else:
        discharge_score += 5

    total = recert_score + discharge_score
    if total == 0:
        confidence = 50
    else:
        confidence = int((max(recert_score, discharge_score) / total) * 100)

    if recert_score >= discharge_score:
        recommendation = "RECERTIFY"
        rationale = _build_recert_rationale(homebound, skilled_nursing, therapy, safety)
    else:
        recommendation = "DISCHARGE"
        rationale = _build_discharge_rationale(homebound, skilled_nursing, therapy, safety)

    return recommendation, rationale, confidence


def _build_recert_rationale(homebound, skilled_nursing, therapy, safety) -> str:
    parts = []
    if homebound["supported"]:
        parts.append(f"patient continues to meet Medicare homebound criteria ({', '.join(homebound['indicators_found'][:2]) if homebound['indicators_found'] else 'per documentation'})")
    if skilled_nursing["ongoing"]:
        needs = skilled_nursing["skilled_needs_identified"][:3]
        parts.append(f"ongoing skilled nursing needs include {', '.join(needs)}" if needs else "continued skilled nursing observation and assessment is required")
    if therapy["ongoing"]:
        discs = therapy["active_disciplines"]
        parts.append(f"{'/ '.join(discs) if discs else 'therapy'} services are ongoing with active functional goals that have not yet been achieved")
    if safety["warrants_continued_care"]:
        concerns = safety["concerns_identified"][:2]
        parts.append(f"safety and caregiver concerns ({', '.join(concerns) if concerns else 'as documented'}) warrant continued skilled oversight")
    return "; ".join(parts) if parts else "multiple domains indicate continued skilled need"


def _build_discharge_rationale(homebound, skilled_nursing, therapy, safety) -> str:
    parts = []
    if not homebound["supported"]:
        parts.append("documentation does not support continued homebound status")
    if not skilled_nursing["ongoing"]:
        if skilled_nursing["discharge_signals"]:
            parts.append(f"skilled nursing goals appear to have been met ({', '.join(skilled_nursing['discharge_signals'][:2])})")
        else:
            parts.append("no ongoing skilled nursing need is identified in recent documentation")
    if therapy["goals_met_signal"]:
        parts.append("therapy goals have been achieved and the patient appears to be at a stable functional level")
    elif not therapy["ongoing"] and not therapy["active_disciplines"]:
        parts.append("no active therapy services or therapy goals are documented")
    if not safety["warrants_continued_care"]:
        parts.append("no significant safety or caregiver concerns are identified that would require skilled oversight")
    return "; ".join(parts) if parts else "clinical documentation indicates the patient is appropriate for discharge at this time"


# ============================================================================
# Case Conference Note Generator
# ============================================================================

def draft_case_conference_note(
    patient: Dict,
    notes: List[Dict],
    homebound: Dict,
    skilled_nursing: Dict,
    therapy: Dict,
    safety: Dict,
    recommendation: str,
    rationale: str,
    confidence: int
) -> str:
    """
    Generate a narrative case conference note suitable for inclusion in the
    patient's clinical record, IDT documentation, or EMR.
    """
    today = date.today().strftime("%B %d, %Y")
    patient_name = patient.get("name", "Patient")
    patient_id = patient.get("id", "Unknown")
    cert_end = patient.get("cert_end_date", "upcoming")
    soc_date = patient.get("soc_date", "N/A")
    primary_dx = patient.get("primary_diagnosis", "as documented on plan of care")
    disciplines = patient.get("disciplines", [])
    note_count = len(notes)

    disc_str = ", ".join(disciplines) if disciplines else "the interdisciplinary team"

    # Build the note sections
    header = f"""CASE CONFERENCE NOTE — {'RECERTIFICATION RECOMMENDATION' if recommendation == 'RECERTIFY' else 'DISCHARGE RECOMMENDATION'}
Date: {today}
Patient ID: {patient_id}
Patient Name: {patient_name}
Start of Care: {soc_date}
Current Certification End Date: {cert_end}
Primary Diagnosis: {primary_dx}
Disciplines Participating: {disc_str}
Recommendation: {recommendation}
Confidence: {confidence}%
"""

    # Clinical status paragraph
    recent_date_range = ""
    if notes:
        sorted_notes = sorted(notes, key=lambda n: n.get("date", ""), reverse=True)
        most_recent = sorted_notes[0].get("date", "recently")
        oldest = sorted_notes[-1].get("date", "")
        if oldest and oldest != most_recent:
            recent_date_range = f"between {oldest} and {most_recent}"
        else:
            recent_date_range = f"as of {most_recent}"

    clinical_status = f"""CLINICAL STATUS REVIEW:
A review of {note_count} visit note{"s" if note_count != 1 else ""} {recent_date_range} was conducted in preparation for this case conference. """

    # Homebound paragraph
    if homebound["supported"]:
        clinical_status += f"The patient continues to demonstrate homebound status, with documentation reflecting {', '.join(homebound['indicators_found'][:3]) if homebound['indicators_found'] else 'functional limitations'} that make leaving the home {'a considerable effort' if homebound['strength'] == 'Strong' else 'challenging'}. "
    else:
        clinical_status += "Recent documentation does not clearly establish homebound status, which is a compliance concern that must be addressed before recertification is pursued. "

    # Skilled nursing paragraph
    if skilled_nursing["ongoing"]:
        sn_needs = skilled_nursing["skilled_needs_identified"][:4]
        clinical_status += f"Skilled nursing services remain medically necessary. Active skilled needs identified include: {', '.join(sn_needs) if sn_needs else 'ongoing skilled observation and assessment of unstable condition'}. "
    else:
        if skilled_nursing["discharge_signals"]:
            clinical_status += f"The patient's condition has stabilized and skilled nursing needs appear to have been resolved, with documentation noting {', '.join(skilled_nursing['discharge_signals'][:2])}. "
        else:
            clinical_status += "Current documentation does not support an ongoing skilled nursing need at this time. "

    # Therapy paragraph
    if therapy["ongoing"] and therapy["active_disciplines"]:
        discs = therapy["active_disciplines"]
        goals_str = "Functional goals remain active and have not yet been achieved" if not therapy["goals_met_signal"] else "The patient is progressing toward goals"
        clinical_status += f"{'/'.join(discs)} services are ongoing. {goals_str}, supporting continued episodic care. "
    elif therapy["goals_met_signal"]:
        clinical_status += "Therapy goals have been met and the patient has demonstrated the ability to maintain functional gains independently or with caregiver support. Therapy discharge is appropriate at this juncture. "
    elif not therapy["active_disciplines"]:
        clinical_status += "No active therapy services are currently on the plan of care. "

    # Safety paragraph
    if safety["warrants_continued_care"]:
        concerns = safety["concerns_identified"][:3]
        high_flags = safety["high_concern_flags"]
        if high_flags:
            clinical_status += f"Safety and caregiver considerations remain clinically significant. The patient presents with {', '.join(high_flags[:2])}, which requires skilled oversight to ensure patient safety and appropriate caregiver guidance. "
        else:
            clinical_status += f"Safety factors noted include {', '.join(concerns[:2]) if concerns else 'risks requiring ongoing skilled monitoring'}. These factors support continued interdisciplinary involvement. "
    else:
        clinical_status += "No significant safety concerns or caregiver deficits have been identified that would independently necessitate continued skilled services. "

    # Recommendation and plan paragraph
    if recommendation == "RECERTIFY":
        plan = f"""RECOMMENDATION AND PLAN:
Based on the foregoing review, the interdisciplinary team recommends RECERTIFICATION for an additional 60-day episode of care. This recommendation is supported by the following: {rationale}.

The plan of care will be reviewed and updated to reflect the patient's current status and goals. Orders will be submitted to the attending physician for signature prior to the certification end date of {cert_end}. Goals for the upcoming certification period will focus on {_generate_recert_goals(skilled_nursing, therapy, safety)}. The patient and caregiver have been educated regarding the plan of care and are in agreement.

The case will be reviewed again at the midpoint of the new certification period or sooner if the patient's condition changes."""
    else:
        plan = f"""RECOMMENDATION AND PLAN:
Based on the foregoing review, the interdisciplinary team recommends DISCHARGE from home health services. This recommendation is supported by the following: {rationale}.

Prior to discharge, the following steps will be completed: (1) final visit(s) will be conducted by each active discipline to confirm the patient's readiness and ensure all goals have been addressed; (2) the patient and caregiver will receive comprehensive discharge instructions including medication management, follow-up appointments, and signs/symptoms requiring emergency evaluation; (3) community resources and outpatient services will be arranged as appropriate; and (4) the attending physician will be notified of the discharge plan and any outstanding clinical concerns.

The discharge OASIS will be completed within the required timeframe. The patient and caregiver have been advised of the discharge plan and verbalize understanding."""

    # Footer
    footer = f"""
Documentation prepared by: Enzo Health Recertification/Discharge Agent
Review date: {today}
This case conference note is generated to support clinical decision-making. Final recertification or discharge decisions require physician authorization and clinician sign-off per agency policy."""

    return f"{header}\n{clinical_status}\n{plan}{footer}"


def _generate_recert_goals(skilled_nursing, therapy, safety) -> str:
    goals = []
    if skilled_nursing["ongoing"]:
        sn = skilled_nursing["skilled_needs_identified"]
        if sn:
            goals.append(f"resolution or stabilization of {sn[0]}")
    if therapy["ongoing"]:
        goals.append("achievement of functional therapy goals and maximization of independence in ADLs")
    if safety["warrants_continued_care"]:
        goals.append("caregiver education and reinforcement of safe home management strategies")
    if not goals:
        goals.append("continued skilled monitoring and management of the patient's primary diagnosis")
    return ", ".join(goals)


# ============================================================================
# Batch Runner
# ============================================================================

def run_batch(agency_id: str, window_days: int, dry_run: bool, patient_id: Optional[str],
              logger: logging.Logger) -> Dict:
    """Run the recert/discharge evaluation for all eligible patients or a single patient."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().strftime("%Y-%m-%d")
    results = []

    # Fetch patients
    if patient_id:
        logger.info(f"Single-patient mode: evaluating {patient_id}")
        patients = [{"id": patient_id, "name": f"Patient {patient_id}",
                     "cert_end_date": (date.today() + timedelta(days=7)).isoformat(),
                     "soc_date": (date.today() - timedelta(days=53)).isoformat(),
                     "disciplines": ["SN", "PT"],
                     "primary_diagnosis": "As documented on plan of care"}]
    else:
        logger.info(f"Batch mode: fetching patients with cert ending within {window_days} days")
        patients = fetch_patients_approaching_recert(agency_id, window_days, logger)

    if not patients:
        logger.warning("No patients found approaching recertification window")
        return {"agency_id": agency_id, "date": today_str, "patients_evaluated": 0, "results": []}

    logger.info(f"Evaluating {len(patients)} patient(s)")

    for patient in patients:
        pid = patient.get("id", "Unknown")
        logger.info(f"  Processing patient {pid}...")

        # Fetch notes
        notes = fetch_recent_notes(pid, agency_id, days_back=21, logger=logger)

        # Evaluate each domain
        homebound = evaluate_homebound_status(notes)
        skilled_nursing = evaluate_skilled_nursing_need(notes)
        therapy = evaluate_therapy_need(notes)
        safety = evaluate_safety_caregiver(notes)

        # Make recommendation
        recommendation, rationale, confidence = make_recommendation(homebound, skilled_nursing, therapy, safety)

        # Draft case conference note
        note_text = draft_case_conference_note(
            patient, notes, homebound, skilled_nursing, therapy, safety,
            recommendation, rationale, confidence
        )

        result = {
            "patient_id": pid,
            "patient_name": patient.get("name", pid),
            "cert_end_date": patient.get("cert_end_date", ""),
            "recommendation": recommendation,
            "confidence": confidence,
            "domains": {
                "homebound_status": homebound,
                "skilled_nursing": skilled_nursing,
                "therapy": therapy,
                "safety_caregiver": safety,
            },
            "rationale": rationale,
            "case_conference_note": note_text,
        }
        results.append(result)

        # Save individual case conference note
        if not dry_run:
            note_path = OUTPUT_DIR / f"{today_str}-{pid}-case-conference.md"
            note_path.write_text(note_text, encoding="utf-8")
            logger.info(f"  Saved case conference note: {note_path}")

    # Build batch summary report
    recert_count = sum(1 for r in results if r["recommendation"] == "RECERTIFY")
    discharge_count = sum(1 for r in results if r["recommendation"] == "DISCHARGE")

    summary = _build_batch_summary(agency_id, today_str, results, recert_count, discharge_count)

    if not dry_run:
        summary_path = OUTPUT_DIR / f"{today_str}-recert-discharge-batch.md"
        summary_path.write_text(summary, encoding="utf-8")
        logger.info(f"Batch summary saved: {summary_path}")

        # Also save machine-readable JSON
        json_path = OUTPUT_DIR / f"{today_str}-recert-discharge-batch.json"
        json_out = {
            "agency_id": agency_id,
            "date": today_str,
            "window_days": window_days,
            "patients_evaluated": len(results),
            "recertify_count": recert_count,
            "discharge_count": discharge_count,
            "results": [
                {k: v for k, v in r.items() if k != "case_conference_note"}
                for r in results
            ]
        }
        json_path.write_text(json.dumps(json_out, indent=2), encoding="utf-8")
        logger.info(f"JSON results saved: {json_path}")
    else:
        logger.info("[DRY RUN] Would have saved batch summary and JSON results")
        print("\n" + "="*60)
        print(summary)
        print("="*60)

    return {
        "agency_id": agency_id,
        "date": today_str,
        "patients_evaluated": len(results),
        "recertify_count": recert_count,
        "discharge_count": discharge_count,
        "results": results,
    }


def _build_batch_summary(agency_id, today_str, results, recert_count, discharge_count) -> str:
    lines = [
        f"# Recertification / Discharge Batch Report",
        f"**Agency:** {agency_id}",
        f"**Date:** {today_str}",
        f"**Patients Evaluated:** {len(results)}",
        f"**Recommended for Recertification:** {recert_count}",
        f"**Recommended for Discharge:** {discharge_count}",
        f"",
        f"---",
        f"",
        f"## Patient Summary",
        f"",
        f"| Patient ID | Name | Cert End | Recommendation | Confidence |",
        f"|---|---|---|---|---|",
    ]

    for r in sorted(results, key=lambda x: x.get("cert_end_date", "")):
        pid = r["patient_id"]
        name = r.get("patient_name", pid)
        cert_end = r.get("cert_end_date", "—")
        rec = r["recommendation"]
        conf = r["confidence"]
        icon = "🔄" if rec == "RECERTIFY" else "✅"
        lines.append(f"| {pid} | {name} | {cert_end} | {icon} {rec} | {conf}% |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## Individual Case Conference Notes",
        f"",
        f"Individual notes are saved to `/clinical-qa/recert/` for each patient.",
        f"File naming: `{today_str}-[patient-id]-case-conference.md`",
        f"",
        f"---",
        f"",
        f"## Action Items",
        f"",
    ])

    if recert_count > 0:
        lines.append(f"**Recertifications ({recert_count} patients):**")
        for r in results:
            if r["recommendation"] == "RECERTIFY":
                lines.append(f"- [ ] {r['patient_id']} ({r.get('patient_name', '')}) — cert ends {r.get('cert_end_date', 'soon')} — obtain physician recertification order")
        lines.append("")

    if discharge_count > 0:
        lines.append(f"**Discharges ({discharge_count} patients):**")
        for r in results:
            if r["recommendation"] == "DISCHARGE":
                lines.append(f"- [ ] {r['patient_id']} ({r.get('patient_name', '')}) — schedule final visits and complete discharge OASIS")
        lines.append("")

    lines.extend([
        f"---",
        f"",
        f"*Generated by Enzo Health Recertification/Discharge Agent — {today_str}*",
    ])

    return "\n".join(lines)


# ============================================================================
# Sample Data (for use when Scribe API is not configured)
# ============================================================================

def _sample_patient_list(agency_id: str, window_days: int) -> List[Dict]:
    today = date.today()
    return [
        {
            "id": "PT-2001",
            "name": "Margaret Chen",
            "soc_date": (today - timedelta(days=52)).isoformat(),
            "cert_end_date": (today + timedelta(days=8)).isoformat(),
            "disciplines": ["SN", "PT"],
            "primary_diagnosis": "Hip fracture s/p ORIF (S72.001A), Type 2 Diabetes (E11.9)",
        },
        {
            "id": "PT-2002",
            "name": "Robert Williams",
            "soc_date": (today - timedelta(days=55)).isoformat(),
            "cert_end_date": (today + timedelta(days=5)).isoformat(),
            "disciplines": ["SN", "OT"],
            "primary_diagnosis": "CHF exacerbation (I50.9), HTN (I10)",
        },
        {
            "id": "PT-2003",
            "name": "Dorothy Alvarez",
            "soc_date": (today - timedelta(days=58)).isoformat(),
            "cert_end_date": (today + timedelta(days=2)).isoformat(),
            "disciplines": ["SN"],
            "primary_diagnosis": "Wound care post-colorectal surgery (K57.30), IDDM (E10.65)",
        },
    ]


def _sample_notes_for_patient(patient_id: str) -> List[Dict]:
    today = date.today()
    sample_data = {
        "PT-2001": [
            {
                "date": (today - timedelta(days=3)).isoformat(),
                "discipline": "PT",
                "clinician": "James Okonkwo, PT",
                "note_text": "Patient is a 74-year-old female s/p right hip ORIF presenting for physical therapy visit. Patient demonstrates homebound status due to considerable effort required to ambulate secondary to post-surgical weight-bearing restrictions and significant pain with movement. She requires maximum assistance to ambulate 20 feet with walker. Gait training performed focusing on weight-bearing as tolerated technique. Balance training exercises completed in standing with bilateral upper extremity support. Therapeutic exercise program including hip abductor strengthening and range of motion performed. Patient tolerated 45 minutes of therapy with rest breaks. Functional goal of ambulating 150 feet with supervision remains active and not yet achieved. Patient and daughter educated on home exercise program. Fall risk remains high secondary to gait instability, post-surgical status, and pain. Patient is progressing toward goals at slower than expected pace. Continued PT services are medically necessary to achieve safe functional mobility and reduce fall risk. Patient verbalized understanding of home exercise program."
            },
            {
                "date": (today - timedelta(days=5)).isoformat(),
                "discipline": "SN",
                "clinician": "Maria Santos, RN",
                "note_text": "Patient is a 74-year-old female s/p right hip ORIF with Type 2 Diabetes. Patient is homebound due to inability to ambulate safely without maximum assistance secondary to post-surgical status and pain. Skilled nursing visit performed for wound assessment, medication management, and diabetic monitoring. Surgical incision is healing — staples intact, no signs of infection, minimal serous drainage. Blood glucose checked: 187 mg/dL. Patient reports inconsistent insulin administration secondary to confusion regarding sliding scale. Complex medication management and insulin education provided. Patient reviewed insulin administration technique with return demonstration — requires reinforcement. Patient also takes Coumadin; INR drawn and sent to lab per physician order. Patient educated on anticoagulation precautions and fall prevention. Caregiver (daughter) present and educated on glucose monitoring and medication administration. Home environment assessed — scatter rugs removed per prior recommendation. Skilled observation of post-surgical status and diabetic management medically necessary."
            },
            {
                "date": (today - timedelta(days=10)).isoformat(),
                "discipline": "SN",
                "clinician": "Maria Santos, RN",
                "note_text": "Follow-up skilled nursing visit. Patient continues homebound status — requires assistance to leave home, taxing effort required. Wound site reassessed. Staples intact, area well-approximated. Blood glucose 210 mg/dL — elevated. Medication teaching reinforced regarding insulin management. Patient expresses confusion about sliding scale insulin dosing. Additional education provided with written materials. Physician notified of continued elevated blood glucose. Plan to monitor closely. Fall risk remains high — patient uses walker and requires supervision. Caregiver verbalized understanding of fall precautions."
            },
        ],
        "PT-2002": [
            {
                "date": (today - timedelta(days=4)).isoformat(),
                "discipline": "OT",
                "clinician": "Priya Nair, OT",
                "note_text": "Patient is an 82-year-old male with CHF exacerbation and HTN presenting for OT evaluation and treatment. Patient is homebound due to significant shortness of breath with minimal exertion — unable to climb stairs, requires rest after ambulating 10 feet on level surface. OT skilled services provided for ADL retraining and energy conservation. Patient demonstrates decreased endurance and requires moderate assistance for bathing and dressing. Energy conservation techniques taught and practiced. Adaptive equipment discussed (long-handled sponge, shower chair). Patient verbalized understanding and will attempt with supervised practice next visit. Activities of daily living goals remain active. Caregiver (wife) present and educated on safe assistance techniques. Goal of patient performing bathing with setup assistance remains unmet. Continued OT medically necessary."
            },
            {
                "date": (today - timedelta(days=6)).isoformat(),
                "discipline": "SN",
                "clinician": "David Park, RN",
                "note_text": "Skilled nursing visit for CHF management. Patient reports 2-pillow orthopnea and ankle edema. Weight up 3 lbs since last visit. Shortness of breath present at rest — oxygen saturation 93% on room air. Patient is homebound — shortness of breath with minimal exertion prevents safe community ambulation without significant medical risk. Lung assessment reveals bibasilar crackles. Physician notified of weight gain and worsening edema. Lasix dose adjustment ordered. Skilled nursing observation and assessment of unstable CHF status medically necessary. Patient educated on daily weights, sodium restriction, and signs and symptoms requiring emergency evaluation. Patient and wife verbalized understanding but wife expresses caregiver burden and fatigue in managing patient's complex medical needs at home. Social work referral placed. Cardiac monitoring ongoing."
            },
            {
                "date": (today - timedelta(days=12)).isoformat(),
                "discipline": "SN",
                "clinician": "David Park, RN",
                "note_text": "Skilled nursing visit. Patient with CHF — condition remains unstable. Weight stable this visit. Patient reports improved sleeping. Edema in bilateral ankles 1+ pitting. Lungs clear. Medication management reinforced — patient on multiple cardiac medications. Medication reconciliation completed. Patient on Lasix, Lisinopril, Carvedilol, Digoxin, Aldactone. Medication compliance reviewed and reinforced. Patient educated on each medication and purpose. Caregiver fatigue noted — wife states she feels overwhelmed managing all medications and monitoring. Social work referral confirmed active."
            },
        ],
        "PT-2003": [
            {
                "date": (today - timedelta(days=2)).isoformat(),
                "discipline": "SN",
                "clinician": "Angela Torres, RN",
                "note_text": "Skilled nursing visit for post-surgical wound care. Patient is a 67-year-old female s/p colorectal surgery with colostomy. Patient is homebound due to wound care requirements and post-surgical activity restrictions. Wound care performed — colostomy site assessed, output appropriate, peristomal skin intact. Colostomy pouch changed per protocol. Patient is progressing well in ostomy management — able to perform pouch change independently with verbal cueing only. Goals met related to ostomy independence — patient verbalized confidence in self-care. IDDM management reviewed — blood glucose 132 mg/dL, within acceptable range. Insulin administration technique observed — patient self-administering correctly. No signs of infection. Patient reports feeling well. Patient is stable and self-managing ostomy care. She lives alone but has daily family support. Discharge from home health services may be appropriate at the conclusion of this certification period as patient goals have largely been met."
            },
            {
                "date": (today - timedelta(days=7)).isoformat(),
                "discipline": "SN",
                "clinician": "Angela Torres, RN",
                "note_text": "Skilled nursing wound care visit. Post-surgical wound healing well. Colostomy functioning appropriately. Ongoing ostomy education provided — patient demonstrating improved independence with pouch management. Patient performing all aspects of ostomy care with setup assistance only. Blood glucose management stable — patient is consistent compliance with insulin regimen. Educated on continued dietary management and activity progression. Patient expressed readiness for discharge, states she feels comfortable managing her care. Goals are nearly achieved. Patient has consistent family support and will follow up with surgeon and endocrinologist post-discharge."
            },
            {
                "date": (today - timedelta(days=14)).isoformat(),
                "discipline": "SN",
                "clinician": "Angela Torres, RN",
                "note_text": "Skilled nursing visit for wound care and ostomy teaching. Post-op week 6. Wound healing well — no signs of infection. Ostomy pouch change performed with patient return demonstration. Patient is learning ostomy care — required moderate assistance this visit. Blood glucose monitoring reviewed. Patient managing insulin with some coaching. Goals include patient independence in ostomy care and self-management of diabetes. Continue skilled nursing services for wound management and patient education."
            },
        ],
    }
    return sample_data.get(patient_id, [])


# ============================================================================
# Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Enzo Health Recertification/Discharge Processor"
    )
    parser.add_argument("--agency-id", required=True, help="Agency identifier (e.g. SUNRISE)")
    parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS,
                        help=f"Days before cert end to flag patients (default: {DEFAULT_WINDOW_DAYS})")
    parser.add_argument("--patient-id", help="Evaluate a single patient by ID")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print output without saving files")
    args = parser.parse_args()

    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Enzo Health Recertification/Discharge Processor")
    logger.info(f"Agency: {args.agency_id} | Window: {args.window_days} days | Dry run: {args.dry_run}")
    logger.info("=" * 60)

    results = run_batch(
        agency_id=args.agency_id,
        window_days=args.window_days,
        dry_run=args.dry_run,
        patient_id=args.patient_id,
        logger=logger,
    )

    logger.info(f"Complete. Evaluated {results['patients_evaluated']} patient(s): "
                f"{results.get('recertify_count', 0)} RECERTIFY, "
                f"{results.get('discharge_count', 0)} DISCHARGE")


if __name__ == "__main__":
    main()
