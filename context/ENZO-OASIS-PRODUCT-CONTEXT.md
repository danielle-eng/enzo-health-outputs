# Enzo Health — OASIS Management Product Context
**For internal AI agent use. Last updated: April 3, 2026. Compiled from live demo environment at demoagency.enzo.health.**

---

## What OASIS Management Is

OASIS Management is Enzo Health's dedicated module for tracking, reviewing, and submitting OASIS assessments across all active patient episodes. OASIS (Outcome and Assessment Information Set) is the federally mandated assessment instrument for home health — every episode requires OASIS completion at Start of Care, Resumption of Care, Follow-Up (when clinically indicated), Recertification, Discharge, and Transfer to Inpatient.

The OASIS Management module serves two user groups:

- **Clinical Reviewers / QA Staff** — who complete structured QA review of each OASIS prior to CMS submission
- **Clinical Managers** — who oversee the submission pipeline and manage timeliness compliance

OASIS submission timeliness is a direct Conditions of Participation requirement (§484.55) and one of the most commonly cited survey deficiencies. This module exists specifically to ensure no OASIS falls through the cracks.

---

## Interface Structure

The OASIS Management module has two primary views:

1. **List View** — the default view; shows all active OASIS records with status, reviewer, and due date
2. **Individual Review Screen** — opens when a specific OASIS record is selected; the split-screen QA workspace

---

## List View

### Status Dashboard (Top)

Six status categories shown as filter tabs with counts:

| Status | Meaning |
|---|---|
| **Pending Review** | OASIS submitted by the clinician via Scribe, awaiting reviewer assignment or review start |
| **Due This Week** | OASIS with a submission deadline within the next 7 days — timeliness risk |
| **In QA Review** | Assigned to a reviewer; review actively in progress |
| **Returned for Changes** | Reviewer has identified issues and sent the OASIS back to the clinician for corrections |
| **Awaiting Submission** | QA review complete and approved; pending CMS iQIES/state submission |
| **Submitted** | Successfully submitted to CMS |

**Demo counts (April 3, 2026):**
- Pending Review: 4
- Due This Week: 2
- In QA Review: 1
- Returned for Changes: 1
- Awaiting Submission: 1
- Total active records visible in demo list: 6 patients

### Patient List Columns

Each row in the list represents one OASIS assessment:

| Column | Description |
|---|---|
| **Patient Name** | Patient full name (links to individual review screen) |
| **Episode** | Episode number for this certification period |
| **OASIS Type** | Assessment type: SOC, Recert, ROC, DC, Transfer |
| **Status** | Current pipeline status (color-coded badge) |
| **Reviewer** | Assigned QA reviewer name, or "Unassigned" |
| **Due Date** | Date by which OASIS must be submitted to CMS |

**Demo patient list:**

| Patient | Episode | OASIS Type | Status | Reviewer | Due Date |
|---|---|---|---|---|---|
| Margaret Chen | #3 | SOC | In QA Review | Sarah Johnson | 11/15/2025 |
| Robert Davis | #1 | Recert | Pending Review | Unassigned | — |
| Susan Thompson | #2 | SOC | Due This Week | Unassigned | — |
| James Wilson | #1 | ROC | Pending Review | Unassigned | — |
| Linda Martinez | #4 | DC | Awaiting Submission | Sarah Johnson | — |
| Dorothy Taylor | #2 | Recert | Returned for Changes | M. Patel | — |

---

## Individual OASIS Review Screen

Accessed by clicking any patient row in the list. This is the QA reviewer's primary workspace — a split-screen interface designed for side-by-side clinical document review and OASIS item completion.

### Demo Record: Margaret Chen

- **Patient:** Margaret Chen
- **Age:** 78 years old
- **DOB:** 03/15/1946
- **MRN:** MRN-78432
- **Episode:** #3
- **Payer:** Medicare Part A
- **Primary Diagnosis:** Heart Failure (ICD-10: I50.9)
- **OASIS Type:** SOC (Start of Care)
- **OASIS SOC Date:** 09/30/2025
- **Review Status:** In Review
- **Reviewer:** Sarah Johnson
- **Lock Deadline:** 11/15/2025 (Day 5 of the 5-day SOC window)

### Header Bar

The review screen header shows:
- Patient name and demographic summary
- Reviewer name (assigned)
- Lock deadline with countdown (e.g., "Day 5" indicating the assessment must be locked by this date)
- "Back to OASIS" navigation link to return to the list

### Risk Flags

Two clinical risk flags are displayed prominently below the header, giving the reviewer immediate clinical context before beginning the review:

| Risk Flag | Demo Value |
|---|---|
| **Hospitalization Risk** | Moderate |
| **Functional Improvement** | High |

These flags are computed from the combination of clinical data already in the record and provide the reviewer with a predictive lens. A Moderate hospitalization risk means this patient's episode warrants clinical attention — the care plan and visit frequency should reflect this.

---

### Left Panel — OASIS Item Review

The left panel displays all OASIS items organized by clinical section. Each item shows:
- The OASIS item code (e.g., GG0130A1)
- The item description
- The current response value (code and label)
- An **AI suggestion indicator** (sparkle/robot icon) when the AI has a suggested response or flagged a potential inconsistency

**Demo items visible (GG-series — Functional Status and Functional Abilities):**

#### Functional Status (GG0130 series)

| Item Code | Description | Current Value | AI Flag |
|---|---|---|---|
| GG0130A1 | Eating | 06 — Independent | No |
| GG0130B1 | Oral Hygiene | 04 — Supervision | Yes — 1 AI suggestion |
| GG0130C1 | Toileting Hygiene | 04 — Supervision | No |

#### Functional Abilities (GG0170 series)

| Item Code | Description | Current Value | AI Flag |
|---|---|---|---|
| GG0170A1 | Roll Left and Right | 03 — Partial/Moderate Assistance | Yes — 1 AI suggestion |
| GG0170B1 | Sit to Lying | 04 — Supervision | No |
| GG0170C1 | Lying to Sitting on Side of Bed | 03 — Partial/Moderate Assistance | No |

**GG Response Scale (standard OASIS-E coding):**
- 06 = Independent — Patient completes activity with no assistance
- 05 = Setup or Clean-Up Assistance — Helper sets up or tidies up; patient does activity
- 04 = Supervision or Touching Assistance — Helper provides verbal cues or occasional physical touch
- 03 = Partial/Moderate Assistance — Helper provides 25–49% of assistance
- 02 = Substantial/Maximal Assistance — Helper provides 50–75% of assistance
- 01 = Dependent — Helper provides more than 75% of assistance

### AI Suggestion Feature

Items flagged with the AI suggestion indicator open an expandable section labeled "1 AI suggestions" (with sparkle/robot icon). Reviewers can view the AI's suggested response and the reasoning behind it before accepting, modifying, or rejecting the suggestion.

This feature addresses one of the most common OASIS quality problems: response inconsistency across items that should logically agree (e.g., a patient coded as Independent in eating but Dependent in transferring when the clinical narrative suggests otherwise).

**Agent implication (Clinical Documentation QA):**
AI suggestion flags on OASIS items are the system's native inconsistency detector. When an item carries an AI flag that was ignored (suggestion rejected), the QA agent should treat this as a higher-scrutiny item.

---

### Right Panel — Clinical Document Viewer

The right panel displays the source clinical documents the reviewer references while completing the OASIS review. Interface controls include:

- **Pagination** — navigate between pages of the uploaded document
- **Zoom control** — zoom percentage adjustable (70% shown in demo)
- **Download button** — download the source document
- **Open in new window** — opens document in a separate browser tab for side-by-side comparison

The document viewer allows the reviewer to visually cross-reference what the clinician documented in Scribe (or the uploaded referral packet) against what is coded in each OASIS item — this is the core QA workflow.

---

## OASIS Submission Pipeline

From the Scheduling module's and Scribe's perspective, the OASIS lifecycle looks like this:

```
Clinician completes visit in Scribe (SOC, ROC, Recert, DC, Transfer)
    ↓
Scribe generates OASIS responses from ambient transcript + post-visit survey
    ↓
Documentation status → "Submitting to EHR" → "Ready for Review in EHR"
    ↓
OASIS record appears in OASIS Management list as "Pending Review"
    ↓
Reviewer assigned → Status: In QA Review
    ↓
Reviewer completes review:
    • Issues found → Returned for Changes (back to clinician)
    • Clean review → Awaiting Submission
    ↓
CMS submission → Submitted
```

---

## OASIS Timeliness Requirements

OASIS Management is built specifically to enforce these CMS timeliness requirements:

| Assessment Type | Timeliness Requirement | Survey Citation |
|---|---|---|
| **SOC OASIS** | Must be completed within 5 calendar days of the SOC date | §484.55 |
| **Recertification OASIS** | Must be completed within the last 5 days of the current certification period or the first 5 days of the new period | §484.55 |
| **Discharge OASIS** | Must be completed on the last skilled visit day or within 2 calendar days of discharge | §484.55 |
| **Transfer OASIS** | Must be completed when patient transfers to an inpatient facility | §484.55 |

The "Lock Deadline: Day 5" shown in the Margaret Chen record is the system enforcing the SOC 5-day window. Items approaching this deadline surface as "Due This Week" in the list view.

---

## OASIS Types and Clinical Context

| OASIS Type | Trigger | Clinical Significance |
|---|---|---|
| **SOC** | First billable skilled visit | Establishes the episode baseline — all improvement outcome measures are anchored to this assessment |
| **ROC** | Patient returns from inpatient stay | Captures patient status after hospitalization; important for rehospitalization outcome tracking |
| **Recert** | End/beginning of each 60-day certification period | Reauthorizes the episode; recert OASIS drives PDGM payment for the next period |
| **DC** | Last skilled visit of the episode | Compared to SOC to calculate outcome measures (ambulation, bathing, dyspnea, etc.) |
| **Transfer** | Patient admitted to inpatient facility | Documents patient status at time of transfer; triggers hospitalization tracking |

---

## Agent Integration Map

| Agent | OASIS Management Connection |
|---|---|
| **QAPI Specialist** | OASIS submission timeliness is a direct QAPI measure. The "Pending Review: 4 / Due This Week: 2" counts in the demo are QAPI data points. High returned-for-changes rates indicate systemic documentation quality issues that belong in QAPI analysis. |
| **Clinical Documentation QA** | Returned OASIS records ("Returned for Changes" status) are the highest-priority QA items. The QA agent should treat these equivalently to critical documentation errors. AI suggestion flags on OASIS items indicate areas where the AI detected inconsistency — these are starting points for clinical review. |
| **Outcomes Analyst** | Every quality outcome measure (improvement in ambulation, bathing, dyspnea, pain, etc.) is calculated from paired SOC and DC OASIS assessments. OASIS accuracy is foundational to all outcomes work — a single miscoded GG item affects the agency's public quality scores. |
| **Survey Readiness** | OASIS timeliness (within 5-day SOC window, recert window, 2-day DC window) is tracked under §484.55 and is among the most commonly cited home health survey deficiencies. The "Due This Week" alert in OASIS Management is a direct survey risk indicator. |
| **Regulatory Intelligence** | OASIS item changes (e.g., OASIS-E updates, new GG-series items, removal or modification of M-series items) directly affect what the platform captures and what reviewers must evaluate. New OASIS item guidance should be flagged with a "OASIS Impact" section in the weekly digest. |
| **CEO Agent** | OASIS submission pipeline depth (how many records are pending, overdue, or returned) is a leading indicator of clinical operations health. An agency with chronic OASIS backlogs has downstream quality data problems that affect STAR ratings and HHVBP payments. |
| **Founding Engineer** | OASIS Management is not yet API-connected to the Paperclip workspace. When integrated, visit completion status from Scheduling should be the trigger for OASIS record creation in this module. The "Submitting to EHR → Ready for Review" transition is the integration handoff point. |

---

## Known Gaps / Placeholder Areas

- **Recertification review screen** — only the SOC (Margaret Chen) record was explored in detail; Recert and DC review screens may have additional or different item sets
- **Returned for Changes workflow** — the feedback mechanism (how the reviewer communicates specific changes needed back to the clinician) not explored
- **CMS submission process** — the actual iQIES submission flow and confirmation from CMS not explored
- **Reviewer assignment workflow** — how reviewers are assigned to records (manual vs. auto-assigned, workload distribution) not confirmed
- **OASIS-E complete item list** — only GG0130 and GG0170 items were visible in the demo review screen; full item list for SOC includes all M-series and GG-series items across multiple sections
- **Branch-level filtering** — whether OASIS Management supports multi-branch filtering (like Scheduling does) not confirmed

*These sections will be updated when the Enzo PM provides additional product documentation.*
