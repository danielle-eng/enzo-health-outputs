# Enzo Health — Intake Product Context
**For internal AI agent use. Last updated: April 3, 2026. Compiled from live demo environment at demoagency.enzo.health.**

---

## What Intake Is

Intake is Enzo Health's referral-to-admission management module. It handles everything from the moment a referral is received from a hospital, physician, or referring facility through the clinical acceptance decision, insurance verification, and handoff to the scheduling team for the first visit. It is the operational front door of the home health agency.

The primary user of Intake is the **Intake Coordinator** (Taylor role in demo), though Clinical Managers have full access and Billing Specialists access the financial components.

---

## The Intake Workflow

Intake uses a **Kanban board** as its primary interface. Every patient referral is a card that moves left to right through the pipeline as the intake team works it.

### Pipeline Stages (8 total)

| Stage | Description | Who Acts |
|---|---|---|
| **New** | Referral just received; no action taken yet | Intake Coordinator |
| **In Progress** | Coordinator actively working — verifying insurance, reviewing clinical docs, building the record | Intake Coordinator |
| **On Hold** | Awaiting something external — missing documents, waiting on patient/family decision, pending physician callback | Intake Coordinator |
| **Accept/Decline** | Clinical review complete; waiting on agency's formal accept or decline decision | Clinical Manager |
| **Waiting for Scheduling** | Accepted; SOC visit needs to be scheduled | Scheduler |
| **Admitted** | First visit scheduled and episode active | System / Clinical |
| **Declined** | Agency formally declined the referral | Intake Coordinator / Clinical Manager |
| **Canceled** | Referral withdrawn by the referring source, or patient no longer needs services | Intake Coordinator |

Total pipeline: 20 patients visible in demo across all stages.

### Referral Card Information (Kanban view)
Each card on the board shows:
- Patient name and date of birth
- Referral source (where the referral came from)
- Referring facility
- Insurance/payer
- Priority level (color-coded badge)
- Checklist progress indicator (e.g., "3/5" — 3 of 5 intake tasks complete)
- Date received

---

## Referral Sources

The system accepts referrals from multiple channels, automatically or manually routed:

| Source | Description |
|---|---|
| **Epic** | Direct EHR integration — referrals flow in from hospital Epic systems |
| **Allscripts** | EHR integration with Allscripts-based facilities |
| **Ensocare** | Referral management platform used by many SNFs and hospitals |
| **Strata** | Referral management platform |
| **E-Fax** | Electronic fax — common for physician offices |
| **Email** | Emailed referral packets |
| **Upload** | Manual upload — coordinator scans and uploads paper referral packet |

The AI-generated referral summary (see below) works across all source types once a document is in the system.

---

## Priority Levels

Every referral card is assigned a priority level, visible as a color-coded badge:

| Priority | Use Case |
|---|---|
| **STAT** | Immediate — patient being discharged today, SOC required within hours |
| **Urgent** | Same-day or next-day SOC required |
| **ASAP** | High priority, SOC within 2–3 days |
| **Routine** | Standard timeline, SOC within the ordered window |
| **No Priority** | Canceled or declined referrals; no active prioritization needed |

---

## The Patient Intake Record

Each referral card opens into a full patient record with tabbed sections. The record is built progressively as the intake coordinator works through the checklist.

### Overview Tab

The Overview tab is the intake coordinator's primary workspace. It contains four sections:

#### 1. AI-Generated Referral Summary
Automatically extracted and generated from uploaded referral documents (discharge summaries, physician orders, referral packets). The summary appears at the top of the Overview with a "Generated from referral documents" badge.

The AI summary covers:
- Patient demographics and age
- Referring facility and discharge date
- Primary diagnosis and reason for referral
- Medicare/payer verification status
- SOC window (first and last acceptable date)
- Disciplines ordered
- Face-to-face encounter status
- Signing provider confirmation status

**Example from demo:**
> "Margaret Chen is a 76-year-old female referred from Riverside Medical Center on 01/18/2025 following hospitalization for a chronic venous stasis ulcer of the right lower extremity. Patient was discharged 01/18/2025. Medicare Part A is active and verified. SOC window is 01/20 -- 01/22/2025. Skilled nursing and therapy services have been ordered. Face-to-face encounter is documented. Signing provider confirmed."

This summary gives clinical staff a quick read on the patient before opening the full record.

#### 2. Intake Note
A free-text field visible only to clinical staff assigned to the patient (not visible to all staff). Used for operational coordination details the clinical team needs before the SOC visit:
- Family contact preferences (e.g., "call ahead, patient is hard of hearing")
- Access instructions (door codes, parking)
- Supply needs that must be confirmed before the visit
- Family engagement notes (who will be present, caregiver dynamics)
- Safety or sensitivity flags (not for formal clinical documentation — that goes in the post-visit survey in Scribe)

Character limit: 279 characters (as of demo).

#### 3. Referral Order
Structured capture of the physician's order details:

- **Referral Date** — when the referral was received
- **SOC Date** — scheduled or ordered Start of Care date; labeled "Physician-Ordered" if specified on the 485 or discharge order
- **Disciplines Ordered** — each discipline with its ordered start date; checked if ordered, grayed out if not:
  - SN (Skilled Nursing)
  - PT (Physical Therapy)
  - OT (Occupational Therapy)
  - ST (Speech Therapy)
  - HHA (Home Health Aide)
  - MSW (Medical Social Work)
- **Ordering Provider** — the physician ordering home health services (name and credentials)
- **Referral Source** — the sending facility or organization
- **Contact** — referral coordinator contact at the sending facility (name, title, email, phone)

#### 4. Eligibility & Authorization
Insurance verification and authorization tracking — one of the most operationally critical sections of Intake.

**Eligibility section:**
- Payer name (e.g., Medicare Part A, Medicare Advantage - UnitedHealthcare)
- Member ID
- In Network: Yes/No
- Auth Required: Yes/No
- Patient Responsibility (copay amount — often $0 for Medicare Part A)
- Eligibility Status: Verified / Pending / Not Verified
- Verification date

**Authorization Tracking by Discipline:**
A table showing authorized visits for each discipline:

| Discipline | Date Span | Used / Total |
|---|---|---|
| SN | 01/15/2025 – 03/31/2025 | 6/15 |
| PT | 01/23/2025 – 03/31/2025 | 4/12 |
| OT | 01/24/2025 – 03/31/2025 | 2/8 |
| ST | 01/24/2025 – 03/31/2025 | 0/6 |
| HHA | 01/26/2025 – 03/31/2025 | 3/10 |

This table is the real-time authorization utilization tracker. As visits are completed, the "Used" count increments. Coordinators can see at a glance which disciplines are approaching their authorization limit.

#### 5. F2F & Signing Provider
Face-to-face encounter documentation — required under §424.22 for Medicare home health coverage:

- F2F Present: Yes/No
- F2F Date
- Provider who performed the F2F (facility and specialty)
- Reason/documentation type (e.g., Physician Progress Note, Hospital Discharge Summary)
- Within 90-day window: Yes/No (auto-calculated — F2F must be within 90 days before or 30 days after SOC)
- Link to view the F2F document
- Signing Provider — the physician who will certify the Plan of Care:
  - Name and NPI
  - Confirmation method (e.g., "Confirmed via phone | Spoke with: Maria (front desk) | 01/18/2025")

---

### Patient Info Tab

Sub-tabs within Patient Info:

**Demographics:**
- Full legal name (including middle name/hyphenated names)
- Date of birth and calculated age
- Gender
- MRN (agency-assigned Medical Record Number)
- Medicare/Medicaid ID
- Home address
- Phone (home and cell)
- Email
- Preferred contact method (e.g., "Phone call to daughter Lisa")
- Primary language and whether language is spoken at home vs. written preference
- Interpreter needed: Yes/No

**Caregivers section (within Demographics):**
- List of all caregivers with:
  - Name and relationship
  - Phone and email
  - Two flags: **Teachable** (can receive clinical education) and **Emergency** (emergency contact)

**Episode Info** — episode-level details for the current certification period

**Care Team** — assigned clinicians by discipline

**Providers** — referring physician, attending physician, PCP, specialists

**Face-to-Face** — detailed F2F documentation (mirrors and expands on Overview F2F section)

---

### Clinical Tab

Sub-tabs within Clinical — all data is AI-extracted from the referral packet, with page number citations showing where in the document each item was found:

**Diagnosis:**
- Primary diagnosis (e.g., CHF Exacerbation)
- Secondary diagnoses (e.g., COPD, Type 2 Diabetes)
- Each with ICD-10 code and page reference from source document
- Ability to add diagnoses manually or mark a different one as primary

**Medications** — medication list extracted from referral documents

**Allergies** — documented allergies from referral packet

**Vitals** — baseline vitals captured from discharge documentation

**Labs** — relevant lab results from the referral packet

**Wounds & Procedures** — wound documentation extracted from clinical records (wound type, location, current treatment)

**Goals & Interventions** — care goals and planned interventions from the physician order or care plan

**Supplies & DME** — ordered medical supplies and durable medical equipment

---

### Other Tabs

**Tasks** — intake checklist items assigned to team members with due dates and completion status. The checklist progress indicator on the kanban card (e.g., "3/5") reflects how many Tasks are complete.

**Communication** — message log for communications with the referring facility, patient, family, and internal team. All communication related to the referral is documented here.

**Orders** — physician orders associated with this intake

**Notes** — clinical notes attached to the patient record during intake

**Financial** — billing and financial clearance details; managed by Billing Specialist role

**Documents** — uploaded referral packet documents, F2F documentation, signed orders, and other attachments. "View Documents" button in the header opens a document viewer with zoom/download/print capability.

---

## Payer Mix Observed in Demo

The demo agency works with a wide range of payers, reflecting a typical home health agency census:
- Medicare Part A (traditional, episodic payment — primary payer for home health)
- Medicare Part B (therapy-only episodes)
- Medicare Advantage plans (UnitedHealthcare, Humana Gold Plus)
- Medicaid
- Blue Cross Blue Shield (PPO and HMO)
- Aetna Commercial
- Cigna PPO
- UnitedHealthcare Commercial
- Veterans Affairs (VA)
- Workers Compensation
- Kaiser Permanente
- Tricare

---

## Key Metrics Tracked in Intake

The Operational Reports section includes intake-specific metrics:
- **Decline Reasons** — why referrals are declined, by category and payer; reveals payer-specific patterns
- **Non-Admit Reasons** — why accepted referrals didn't convert to admissions
- **Time in Status** — average time spent in each kanban stage; reveals bottlenecks in the intake workflow
- **Time to Accept** — time from referral receipt to the accept/decline decision; benchmark for intake efficiency

---

## Agent Integration Map

| Agent | Intake Connection |
|---|---|
| **Founding Engineer** | Intake API is integration priority #2. Connect the referral order, eligibility/authorization data, and AI referral summary to agent workspace for patient context on every episode. |
| **QAPI Agent** | Non-admit rates, decline reasons, and payer mix from Intake feed into operational quality metrics. High decline rates by payer or diagnosis are a QAPI indicator. |
| **Clinical Documentation QA** | AI-extracted diagnoses and clinical data in Intake (Clinical tab) should be consistent with what the SOC OASIS documents. Discrepancies between intake diagnoses and OASIS assessment responses are a flag for review. |
| **Outcomes Analyst** | Authorization tracking in Intake (used/total visits by discipline) is the first indicator of LUPA risk. If a patient is on a path to fewer visits than planned, it should trigger early intervention. |
| **Survey Readiness** | F2F documentation completeness and timing (within 90-day window, confirmed signing provider) is a direct CoP requirement under §424.22 and one of the most commonly cited Medicare deficiencies. The F2F section of Intake is the compliance checkpoint. |
| **Regulatory Intelligence** | LCD/NCD changes that affect admissibility (e.g., diagnosis-specific coverage requirements) directly affect the Accept/Decline stage. New regulatory guidance should be flagged with "Intake Impact" for the intake team. |
| **CEO Agent** | Intake funnel metrics (referrals received → admitted → declined → canceled) are agency growth indicators. Referral source distribution reflects the agency's referral relationship strategy. |

---

## Known Gaps / Placeholder Areas

- **Episode Info sub-tab** — not explored in detail; likely contains certification period dates, episode number, branch assignment
- **Care Team sub-tab** — not explored; likely shows assigned clinicians by discipline for the episode
- **Financial tab** — managed by Billing Specialist; contains billing clearance, payer-specific financial information
- **Intake checklist specifics** — the exact list of tasks that make up the progress indicator (e.g., 0/4, 3/5) varies by payer and patient type; full checklist detail TBD from PM

*These sections will be updated when the Enzo PM provides additional product documentation.*
