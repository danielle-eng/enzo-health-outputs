# Enzo Health — Scheduling Product Context
**For internal AI agent use. Last updated: April 3, 2026. Compiled from live demo environment at demoagency.enzo.health.**

---

## What Scheduling Is

Scheduling is Enzo Health's visit management and clinician capacity module. It handles the assignment of patient visits to field clinicians across all disciplines, tracks visit completion status, and gives agency administrators real-time visibility into workforce utilization. It connects directly to the patient's plan of care (what visits are ordered) and feeds into clinical documentation (when visits are completed, Scribe is triggered).

The primary user is the **Scheduler** (Stephanie role in demo), though Clinical Managers have full visibility and field clinicians see their own schedules in the Scribe mobile app.

---

## Supported Disciplines

Scheduling covers all disciplines the agency employs:

| Code | Discipline | Typical Visit Type |
|---|---|---|
| RN | Registered Nurse | Skilled nursing — OASIS, wound care, medication management, teaching |
| LPN/LVN | Licensed Practical/Vocational Nurse | Skilled nursing — subsequent visits under RN supervision |
| PT | Physical Therapist | Therapy evaluation and treatment |
| PTA | Physical Therapy Assistant | PT follow-up visits under PT supervision |
| OT | Occupational Therapist | OT evaluation and treatment |
| OTA | Occupational Therapy Assistant | OT follow-up visits under OT supervision |
| ST/SLP | Speech-Language Pathologist | Speech therapy evaluation and treatment |
| HHA | Home Health Aide | Personal care visits — bathing, grooming, ADL assistance |
| MSW | Medical Social Worker | Social work evaluation and follow-up |

---

## Interface Views

Scheduling has four main views accessible via tabs at the top of the module:

### 1. Overview (Default)
The agency-wide dashboard showing capacity status, daily alerts, and productivity metrics. This is the Scheduler's command center for the day.

### 2. By Patient (22 in demo)
All scheduled visits organized by patient. Shows every patient with upcoming visits, visit type, assigned clinician, and status. Number in tab header reflects total active patients with scheduled visits.

### 3. By Clinician
All scheduled visits organized by individual clinician. Shows each clinician's full schedule — useful for managing workload, identifying gaps, and reassigning visits when a clinician calls out.

### 4. Pending Visits
Visits that exist (they've been ordered and are in the system) but have not yet been assigned to a clinician. This is the scheduler's to-do queue for making assignments.

---

## Overview Dashboard

### Alert Cards (Top Row)
Three alert types surface automatically based on visit status:

**Missed Visits**
- Visits that were scheduled but not completed by the clinician
- Require two actions: (1) clinical review to ensure patient safety, and (2) provider notification per CoP requirements
- A missed skilled nursing visit on a high-acuity patient is a potential patient safety event and survey deficiency

**Returned Visits**
- Visits that a clinician started but returned to the scheduler — typically because the patient was unavailable, refused the visit, or a clinical issue arose that requires a different clinician or visit type
- Awaiting scheduler action: reassign to another clinician, contact patient, or document refusal

**Pending Visits**
- Visits awaiting clinician confirmation or response
- The clinician has been offered the visit but has not yet accepted or responded
- High pending visit counts indicate a staffing capacity or communication issue

### Agency Productivity Panel
Shows discipline-by-discipline workforce capacity in real time:

| Field | Description |
|---|---|
| Discipline badge | Color-coded discipline abbreviation (RN, PT, OT, etc.) |
| Staff count | Number of active clinicians in that discipline |
| Total | Total visits assigned today across all clinicians in that discipline |
| Avg | Average visits per clinician in that discipline today |
| Status | Capacity assessment: At capacity / Over capacity / Underutilized |

**Demo snapshot (April 3, 2026):**

| Discipline | Staff | Total Visits | Avg | Status |
|---|---|---|---|---|
| RN | 4 | 18 | 4.5 | At capacity |
| LPN/LVN | 3 | 15 | 5.0 | At capacity |
| PT | 2 | 12 | 6.0 | **Over capacity** |
| PTA | 2 | 9 | 4.5 | At capacity |
| OT | 1 | 3 | 3.0 | Underutilized |
| OTA | 1 | 3 | 3.0 | Underutilized |
| HHA | 3 | 15 | 5.0 | At capacity |
| MSW | 1 | 2 | 2.0 | Underutilized |

Capacity thresholds appear to be: Underutilized < ~4 avg, At capacity ~4–5.5 avg, Over capacity > 5.5–6 avg. Exact thresholds may vary by agency configuration.

### Today's Summary (Right Panel)
A real-time count of the day's visit activity:

| Metric | Demo Value | What It Means |
|---|---|---|
| **Assigned** | 55 | Total visits assigned to clinicians today |
| **Unassigned** | 7 | Visits that need to be assigned (scheduler action required) |
| **SOC** | 9 | Start of Care visits today (highest priority — first visit with a new patient) |
| **ROC** | 0 | Resumption of Care visits today (patient returning from hospital) |

SOC and ROC counts matter because these visits require OASIS assessment completion — they are higher-complexity, longer-duration visits and have strict timeliness requirements under the CoPs.

### Quick Actions
Two quick actions available directly from the Overview:
- **Schedule Unassigned Visits** — opens the Pending Visits view to begin making assignments
- **View Clinician Schedules** — opens the By Clinician view to review individual workloads

---

## Visit Lifecycle (Scheduling Perspective)

From the scheduling module's point of view, a visit moves through these states:

```
Ordered (from Plan of Care)
    ↓
Pending (in Scheduling queue, awaiting assignment)
    ↓
Assigned (clinician confirmed, appears on their mobile schedule)
    ↓
In Progress (clinician has started the visit in Scribe)
    ↓
Submitting to EHR (Scribe transcription complete, documentation submitting)
    ↓
Ready for Review in EHR (documentation complete, awaiting clinical QA)
    ↓
Completed
```

The mobile app (Scribe) reflects exactly this workflow — in the demo, the clinician schedule view shows visit statuses including "In Progress", "Submitting to EHR", "RN SOC", "RN ROC", "SN SUB" (subsequent), and "Ready for Review in EHR".

**Missed** and **Returned** are exception states that break this flow and require scheduler intervention.

---

## Multi-Branch / Multi-Organization Support

The scheduling module supports agencies with multiple branches. In the demo, the organization "Healthcare Providers" has four branches:
- Healthcare Providers - Salt Lake City
- Healthcare Providers - Lehi
- Healthcare Providers - St. George/Washington
- Healthcare Providers - Med-recon

The "All Teams" filter at the top of Scheduling allows the scheduler to view all branches combined or filter to a single branch. Clinicians are assigned to branches, and visits are typically assigned within branch boundaries (geographic optimization).

---

## Scheduling and OASIS Timeliness

A critical function of Scheduling is protecting OASIS timeliness compliance:

**SOC OASIS window:** Skilled nursing Start of Care assessment must be completed within 5 calendar days of the SOC date (the first billable visit). If the SOC visit is not scheduled and completed within this window, the agency is out of compliance with §484.55.

**Recertification window:** Recertification OASIS must be completed within the last 5 days of the current certification period or the first 5 days of the new period. Scheduling must ensure the recertification visit is assigned and completed within this window.

**Discharge OASIS:** Discharge assessment must be completed on the last skilled visit or within 2 calendar days of discharge.

The OASIS module's "Due This Week" alert is directly upstream of scheduling — if an OASIS is due and the visit isn't scheduled, the scheduler is the person who needs to act first.

---

## HHA Supervisory Visit Scheduling

A specific scheduling compliance requirement: Home Health Aide supervisory visits.

Under §484.80, the supervising RN must conduct an in-person supervisory visit with HHA patients at least every 14 days. This visit must be:
- Conducted by an RN (or in some cases another skilled clinician)
- Completed in the patient's home at a time when the HHA is present or providing care
- Documented in the clinical record

The scheduling team is responsible for ensuring these supervisory visits are inserted into the RN schedule on the correct cadence. Missed supervisory visits are a common survey deficiency.

---

## Key Metrics and Reports

**Operational reports tied to Scheduling:**
- Missed Visits report — missed visits by date range with reasons and coverage impact
- Clinical: LUPA & Outlier Analysis — episodes trending toward LUPA (Low Utilization Payment Adjustment), which occurs when fewer than the threshold visits are completed in an episode
- Clinical: Hospital Holds — patients currently inpatient (visits on hold while patient is hospitalized)

**LUPA Risk from a Scheduling Perspective:**
LUPA occurs when an episode has fewer than the threshold number of visits (varies by HHRG/PDGM payment group). Scheduling is the first line of defense — if visit frequency is falling below the plan of care, the scheduler and clinical manager need to intervene early. The LUPA & Outlier Analysis report flags these episodes.

---

## Connection to Scribe (Mobile App)

Scheduling and Scribe are tightly coupled:

1. When a visit is **assigned** in Scheduling, it appears on the clinician's schedule in the Scribe mobile app
2. The clinician sees: patient name, phone number, visit type (SOC, ROC, SUB, DC), and any intake notes shared with clinical staff
3. When the clinician taps the visit in Scribe, the **ambient listening session begins** — the in-visit recording starts
4. After the visit, the clinician completes the **post-visit survey** in Scribe
5. When Scribe finishes transcription and documentation, the visit status in the EHR changes to "Submitting to EHR" → "Ready for Review in EHR"
6. This status change is visible to the Clinical Manager and QA team in the back office

---

## Agent Integration Map

| Agent | Scheduling Connection |
|---|---|
| **Founding Engineer** | Scheduling API is integration priority #3. Visit completion status is the trigger for Scribe note submission and OASIS timing tracking. Build an automated monitor that flags visits approaching timeliness thresholds. |
| **QAPI Agent** | Missed visit rates, returned visit rates, and visit frequency variance (planned vs. actual) are QAPI outcome indicators. High missed-visit or returned-visit rates in a specific discipline or branch are a performance improvement opportunity. |
| **Clinical Documentation QA** | Visit type from Scheduling (SOC vs. SUB vs. DC) determines what documentation is required. A note submitted under a "SUB" visit type that contains OASIS-level documentation is a potential billing and compliance flag. |
| **Outcomes Analyst** | Scheduling data is essential for LUPA risk management and for validating that visit frequency matches the plan of care. Visits per episode by discipline directly affect HHVBP payment calculations. The SOC and ROC counts in Today's Summary reflect new episodes starting — a leading indicator of monthly census trends. |
| **Survey Readiness** | HHA supervisory visit scheduling (every 14 days, RN in home while HHA present) is a §484.80 requirement and frequent survey deficiency. Mock surveys should verify supervisory visit cadence. Missed visit documentation and patient notification are also survey issues. |
| **Regulatory Intelligence** | Changes to PDGM visit thresholds, LUPA thresholds by HHRG, or HHA supervisory visit frequency requirements directly affect scheduling protocols. New rules should be flagged with "Scheduling Impact." |
| **CEO Agent** | Scheduling capacity metrics (over-capacity disciplines, unassigned visit counts, SOC/ROC volumes) are leading operational health indicators. A PT discipline running at 6 visits/clinician over multiple days is a staffing risk that needs executive visibility. |

---

## Known Gaps / Placeholder Areas

- **By Patient view detail** — individual visit details, visit history per patient, rescheduling workflow not explored
- **By Clinician view detail** — individual clinician schedule layout, drive time optimization, geographic clustering not explored
- **Pending Visits workflow** — exact process for matching unassigned visits to available clinicians not explored
- **Visit assignment logic** — whether the system has any auto-matching/optimization (e.g., geographic proximity, clinician-patient relationship continuity) not confirmed from demo
- **Patient notification** — whether Scheduling sends automated reminders to patients/families not confirmed

*These sections will be updated when the Enzo PM provides additional product documentation.*
