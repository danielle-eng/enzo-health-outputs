# Enzo Health — Full Platform Context
**For internal AI agent use. Last updated: April 3, 2026. Compiled from live demo environment at demoagency.enzo.health.**

This document gives the full agent team accurate context on every Enzo Health product so outputs are grounded in the actual platform, not generic assumptions.

---

## Platform Overview

Enzo Health is a healthcare software company building an end-to-end EHR platform specifically for **home health and hospice agencies**. The platform currently covers the full agency workflow from referral receipt through clinical documentation, OASIS management, scheduling, quality oversight, and reporting. It is a web-based back-office EHR paired with a mobile application (Scribe) for field clinicians.

**Current live products:**
1. Intake
2. Scheduling
3. OASIS Management
4. Orders & Supplies
5. Quality Management
6. Reports & Analytics
7. Scribe (mobile — see separate ENZO-SCRIBE-PRODUCT-CONTEXT.md)

**In active development:**
- Full EHR (complete patient record management)
- Billing module (live in demo, production readiness TBD)
- Hospice-specific workflows (Scribe currently home health only)

**Multi-org support:** A single agency can operate multiple branches under one account (e.g., Healthcare Providers - Salt Lake City, Lehi, St. George/Washington, Med-recon). Scheduling and reporting can be filtered by branch/team.

**Role-based access:** The platform has distinct role views:
- Clinical Manager (Zach) — full back-office access
- Scheduler (Stephanie) — scheduling-focused
- Field Clinician (Danielle) — mobile/Scribe view + limited back-office
- Clinical Support Staff (Mariah) — clinical support workflows
- Intake Coordinator (Taylor) — intake-focused
- Billing Specialist (Katie) — billing-focused
- Sales Demo views (Back Office + Mobile App)

---

## 1. Intake

### What It Is
The Intake module manages the full referral-to-admission workflow. It is the entry point for every new patient episode.

### Interface
A **Kanban board** with 8 pipeline stages:

| Stage | Meaning |
|---|---|
| New | Referral received, intake not yet started |
| In Progress | Intake coordinator actively working the referral |
| On Hold | Awaiting information or patient/family response |
| Accept/Decline | Clinical decision pending |
| Waiting for Scheduling | Accepted, SOC visit not yet scheduled |
| Admitted | Patient admitted, episode active |
| Declined | Agency declined the referral |
| Canceled | Referral withdrawn or patient no longer needs services |

Each card shows: patient name, DOB, referral source, referring facility, insurance, priority level, checklist progress (e.g., 3/5 steps complete), and date.

### Referral Sources
The system accepts referrals from: Epic (direct EHR integration), Allscripts (EHR integration), Ensocare (referral management platform), Strata (referral management), E-Fax, Email, and manual Upload (document scan/PDF).

### Priority Levels
STAT → Urgent → ASAP → Routine → No Priority

### Patient Record Structure (tabs)

**Overview tab** contains:
- **AI-Generated Referral Summary** — automatically extracted from uploaded referral documents; summarizes diagnosis, discharge status, Medicare verification, SOC window, disciplines ordered, F2F status
- **Intake Note** — free-text note visible only to clinical staff assigned to the patient; used for coordination details (family contact preferences, supply needs, access notes)
- **Referral Order** — referral date, SOC date (physician-ordered or agency-set), disciplines ordered (SN, PT, OT, ST, HHA, MSW) each with ordered start date
- **Eligibility & Authorization** — payer, member ID, in-network status, auth required (Y/N), patient responsibility/copay, eligibility verification status and date, **authorization tracking by discipline** (date span, visits used vs. total authorized)
- **F2F & Signing Provider** — face-to-face encounter date, provider, reason for encounter, within-90-day-window verification, signing provider name and NPI, confirmation method and contact

**Patient Info tab** (sub-tabs):
- Demographics: full name, DOB/age, gender, MRN, Medicare ID, home address, phone (home/cell), email, preferred contact, language, interpreter needed, caregivers (with relationship, contact info, teachable/emergency flags)
- Episode Info
- Care Team
- Providers
- Face-to-Face

**Clinical tab** (sub-tabs — AI-extracted from referral packet with page citations):
- Diagnosis (primary + secondary diagnoses, extracted from referral document)
- Medications
- Allergies
- Vitals
- Labs
- Wounds & Procedures
- Goals & Interventions
- Supplies & DME

**Other tabs:** Tasks, Communication, Orders, Notes, Financial, Documents

### Key Integration Points for Agents
- **QAPI Agent:** Intake data (referral source, payer mix, admit/decline rates) feeds into operational quality metrics. Non-admit rate by reason is a reportable metric (Decline Reasons and Non-Admit Reasons reports exist).
- **Clinical Documentation QA:** Intake clinical tab (diagnoses, wounds, medications extracted from packet) should align with what the SOC note documents — discrepancies between intake diagnosis and OASIS assessment are a QA flag.
- **Outcomes Analyst:** Intake authorization tracking (used/total by discipline) is where LUPA risk first becomes visible. Patients trending toward LUPA should be flagged early.
- **Survey Readiness:** F2F documentation (within 90-day window, confirmed signing provider) is a direct CoP requirement under §484.55 and a common survey deficiency.
- **Founding Engineer:** Intake API is integration priority #2. The referral summary, diagnoses, and authorization data available in Intake should flow into agent workspace for context on each patient episode.

---

## 2. Scheduling

### What It Is
Scheduling manages the assignment of clinician visits to patients across all disciplines and branches. It is both a **capacity management** tool and a **visit assignment** tool.

### Interface
Four views:
- **Overview** — agency-wide dashboard (default)
- **By Patient** — all visits grouped by patient
- **By Clinician** — all visits grouped by clinician (individual workload view)
- **Pending Visits** — visits not yet assigned

Can be filtered by Team/Branch.

### Overview Dashboard
**Alert summary (top):**
- Missed Visits — visits not completed; require review and provider notification
- Returned Visits — visits returned by clinician (unable to complete); awaiting scheduler action
- Pending Visits — unassigned visits awaiting clinician response

**Agency Productivity panel:**
Shows capacity status for every discipline with number of staff, total visits assigned, and average visits per clinician:
- RN, LPN/LVN, PT, PTA, OT, OTA, HHA, MSW
- Status labels: At capacity, Over capacity, Underutilized

**Today's Summary:**
- Assigned visits total
- Unassigned visits
- SOC visits today
- ROC visits today

**Quick Actions:**
- Schedule Unassigned Visits
- View Clinician Schedules

### Key Integration Points for Agents
- **QAPI Agent:** Missed visits, returned visits, and visit frequency patterns are direct inputs to QAPI outcome measures. High missed-visit rates correlate with poor outcomes and are a survey risk.
- **Outcomes Analyst:** Scheduling data shows whether visit frequency matches the plan of care — LUPA risk is a scheduling and outcomes issue simultaneously.
- **Survey Readiness:** Supervisory visit scheduling (HHA oversight visits) is a CoP requirement under §484.80. The scheduling module tracks HHA visits and aids supervisor visit compliance.
- **Founding Engineer:** Scheduling API is integration priority #3. Visit completion status (assigned → completed → submitted to EHR) is the trigger that feeds Scribe note submission and OASIS timing tracking.

---

## 3. OASIS Management

### What It Is
A dedicated module for tracking OASIS assessment completion, QA review, and CMS submission across all active patient episodes.

### Interface
List view with status dashboard at top and patient-level tracking below.

**Status categories (dashboard):**
| Status | Meaning |
|---|---|
| Pending Review | OASIS submitted by clinician, awaiting QA reviewer assignment or review start |
| Due This Week | OASIS due within 7 days — timely submission risk |
| In QA Review | Assigned to a reviewer, actively being reviewed |
| Returned for Changes | Reviewer sent back to clinician with corrections needed |
| Awaiting Submission | QA complete, awaiting CMS iQIES/state submission |
| Submitted | Successfully submitted |

**Patient list columns:**
- Patient name
- Episode number
- OASIS Type: SOC, Recert (Recertification), ROC, DC (Discharge), Transfer
- Status (color-coded)
- Reviewer (assigned staff or Unassigned)
- Due Date

### Key Integration Points for Agents
- **QAPI Agent:** OASIS submission timeliness directly impacts the Timely Initiation of Care measure and is a common QAPI finding. Late OASIS = late data = inaccurate outcome reporting.
- **Clinical Documentation QA:** Returned OASIS records are the highest-priority QA items. The QA agent should treat "Returned for Changes" OASIS as equivalent to a critical clinical documentation error.
- **Outcomes Analyst:** Every outcome measure (improvement in ambulation, bathing, dyspnea, etc.) is derived from OASIS SOC and DC data. OASIS accuracy is foundational to all outcomes work.
- **Survey Readiness:** OASIS timeliness (SOC within 5 calendar days, final within 30 days) is tracked under §484.55. The "Due This Week" alert is a direct survey risk indicator.

---

## 4. Quality Management

### What It Is
The central quality command center — the most directly relevant existing product to the Paperclip QAPI agent's work. It consolidates risk identification, chart auditing, incident tracking, and survey readiness into one dashboard.

### Interface Tabs

**Overview tab:**
- **Dashboard metrics:** High risk patient count, Open tasks, Charts flagged, Active incidents, Survey status (Yellow/Green/Red), CMS Quality STAR rating with year-over-year trend
- **Top Risks Driving Quality** — AI-prioritized list of agency quality risks, each with:
  - Severity label (High / Moderate / Low)
  - Risk description
  - Impact areas (which STAR measures, which HHCAHPS composites, which CMS CoP citation)
  - Quantified impact (e.g., "-0.3 potential stars", "+18% hospitalization risk", "-7% on benchmark measure")
  - "Create action plan" button — directly generates a PIP/action plan from the finding
- **Priority Work Queue** — ordered task list with severity, item description, due date, and owner
- **Quick-access cards:** Chart Audits (pending/returned counts), Incidents & Logs (open/high counts), Survey Readiness

**Chart Audits tab:**
- Tracks chart reviews in progress
- Status: pending, returned
- Assigns chart audit tasks to QA staff

**Incidents & Logs tab:**
- Tracks falls, medication errors, infections, near-misses, and other incidents
- Severity classification
- Open/closed status

**Survey Readiness tab:**
- Compliance tracking against CoPs
- Mock survey findings and action items

### Sample Top Risks Observed in Demo (April 3, 2026):
1. **High** — Late OASIS submissions in SN discipline → impacts Star Ratings, ACH benchmark, §484.55 → -0.3 potential stars
2. **High** — Inconsistent wound orders vs. documentation → impacts Survey readiness, §484.60, infection control → +18% hospitalization risk
3. **Moderate** — Medication education not documented at SOC → impacts Med Education benchmark, Star Ratings → -7% on benchmark
4. **Moderate** — Delayed SOC visits after referral → impacts Timely Initiation measure, Star Ratings, §484.55 → -0.2 potential stars
5. **Low** — Supervisory visit documentation incomplete → impacts §484.80, aide oversight compliance → Potential survey finding

### Key Integration Points for Agents
- **QAPI Agent:** Quality Management is the native QAPI module. Agent outputs (quarterly reports, PIPs) should reference and be consistent with what's in this module. The "Top Risks" panel is effectively the agency's real-time QAPI indicator list.
- **Survey Readiness Agent:** The Survey Readiness tab and the mock deficiency findings here are the agent's primary data source when connected via API. Mock survey outputs should mirror the format of findings already in this system.
- **Clinical Documentation QA Agent:** Chart Audits tab is where QA review tasks live. Agent review outputs should be structured to populate this system directly.
- **Outcomes Analyst:** The STAR rating shown here (4.5 in demo, Yellow survey) is the agency's public-facing quality score. All agent analyses should orient around moving this number.
- **CEO Agent:** Quality Management overview is the executive dashboard. CEO synthesis reports should match the format and framing of this view.

---

## 5. Reports & Analytics

### What It Is
A structured reporting library organized by domain. Reports are pre-built but filterable by date range, branch, team, clinician, and payer.

### Report Categories

**Operational (4 live, 8 coming soon):**
- Decline Reasons — referral decline analysis by category and payer
- Non-Admit Reasons — why accepted referrals didn't convert to admissions
- Time in Status — average time spent in each intake workflow stage
- Time to Accept — time from referral receipt to acceptance decision
- Coming soon: Admissions, Admissions (Non-duplicated), Patient Census, and more

**Clinical (9 reports):**
- High Risk Patients — elevated risk based on OASIS, visit patterns, conditions
- Missed Visits — missed visits with reasons and coverage impact
- Hospital Holds — patients pending admission while inpatient
- Emergency Preparedness — acuity/disaster status by branch/county/zone
- LUPA & Outlier Analysis — episodes trending toward LUPA/outlier with visit variance
- Potentially Avoidable Events — CMS-defined PAE counts and rates by event type
- Patient Outcomes Summary — outcomes and goal achievement rates
- Rehospitalization Report — readmissions by diagnosis, branch, and clinician
- Wound Healing Progress — wound measurement trends and healing rates

**Financial (5 reports):** (not fully explored; billing module active in demo)

**Quality / QAPI (6 reports):**
- QAPI Dashboard — quality improvement metrics and trend lines
- Survey Readiness — compliance checklist aligned with /admin/quality
- Incident Trending — falls/incidents/near-misses by location, clinician, shift
- Order Tracking — all orders with status, provider, timing
- Star Ratings Preview — Overall Quality of Patient Care star rating and components
- HHCAHPS Scores & Benchmarks — patient experience survey results vs. national/state benchmarks

**AI Analytics (3 reports):**
- AI Usage & Adoption — how often AI suggestions (OASIS, coding, orders, documentation) are accepted vs. overridden, by user and discipline
- AI Impact on Reimbursement — revenue and case-mix weight comparison for AI-assisted vs. non-AI charts
- AI Impact on Quality — changes in QA findings, coding revisions, survey/benchmark metrics when AI is used

**Scribe (1 report):**
- Scribe Metrics Dashboard — average visit length and time-to-submit documentation after visit completion

### Key Integration Points for Agents
- **QAPI Agent:** The Quality/QAPI reports (especially QAPI Dashboard, HHCAHPS Scores, Star Ratings Preview) are the data sources for quarterly QAPI reports. When integrated, agents should pull from these rather than manual input.
- **Outcomes Analyst:** Clinical reports (Rehospitalization, Patient Outcomes Summary, High Risk Patients, Wound Healing) are the raw data the agent analyzes and synthesizes. LUPA & Outlier Analysis feeds directly into HHVBP payment modeling.
- **Regulatory Intelligence:** AI Analytics reports (especially AI Impact on Quality) are relevant for tracking whether regulatory changes affect AI acceptance/override patterns — this is a novel quality metric unique to AI-powered EHRs.
- **Founding Engineer:** Reports API is integration priority #4. The QAPI Dashboard and Clinical reports should eventually feed automatically into agent workspaces instead of requiring manual data export.

---

## 6. Orders & Supplies

### What It Is
Order management for physician orders (Plan of Care / 485) and supply tracking across patient episodes.

### Key Integration Points for Agents
- **Clinical Documentation QA:** Visit note interventions must align with the active physician orders. Orders module is the source of truth for what the clinician is authorized to do — inconsistencies between orders and documentation are a critical QA flag and survey deficiency.
- **Survey Readiness:** Physician order management (§484.60) and supply authorization are direct CoP requirements. Order tracking report (in Quality/QAPI reports) flags orders with timing or provider issues.

---

## 7. Billing

### What It Is
A billing module visible in the demo (accessible to Billing Specialist role). Manages claims, remittance, and payer-specific billing workflows.

*Note: Billing module status in production is TBD as of April 2026. The Enzo platform is tracking toward a complete EHR including billing.*

### Key Integration Points for Agents
- **QAPI Agent:** Payer mix data (Medicare Part A/B, Medicare Advantage, Medicaid, commercial, VA, workers comp) affects QAPI benchmarking. MA plans have different quality requirements than traditional Medicare.
- **Outcomes Analyst:** HHVBP payment adjustment (±5%) is tied to billing. Medicare Part A episode counts determine HHVBP eligibility and weight.

---

## Platform-Wide Notes for All Agents

**What exists natively that agents should not duplicate:**
- The Quality Management module already surfaces AI-prioritized quality risks with CFR citations and star-rating impact. Agent QAPI work should complement and deepen this, not recreate it.
- The OASIS module already tracks submission status and reviewer assignment. Agent clinical QA work should focus on content quality, not submission logistics.
- Reports already exist for HHCAHPS, Star Ratings, Rehospitalization, and LUPA. Agent work should analyze and synthesize these, not recreate the underlying data pull.

**Current data gaps (as of April 2026):**
- No live API connection between Enzo products and the Paperclip agent workspace yet. All agent work in Wave 1 uses manually provided or mock data.
- Hospice workflows not yet in platform.
- Financial/billing integration not yet production-ready.

**Disciplines supported across the platform:**
SN (Skilled Nursing), LPN/LVN, PT (Physical Therapy), PTA, OT (Occupational Therapy), OTA, ST/SLP (Speech Therapy), HHA (Home Health Aide), MSW (Medical Social Work)

**Insurance/payer types seen in demo:**
Medicare Part A, Medicare Part B, Medicare Advantage (UnitedHealthcare, Humana Gold Plus), Medicaid, Blue Cross Blue Shield (PPO and HMO), Aetna Commercial, Cigna PPO, UnitedHealthcare Commercial, Veterans Affairs (VA), Workers Compensation, Kaiser Permanente, Tricare

---

*For Scribe (mobile app) product detail, see ENZO-SCRIBE-PRODUCT-CONTEXT.md in this same folder.*

*This document should be updated as new products launch or existing products add major features. Notify the Regulatory Intelligence agent of any changes that affect OASIS, billing, or quality reporting capabilities.*
