# Enzo Health Paperclip — Wave 1 Launch Tasks

These are the first issues to assign each agent the moment the Paperclip instance is live and configured. Complete them in order: Founding Engineer first (it scaffolds the workspace everything else depends on), then all other agents in parallel.

---

## 🏗️ Founding Engineer — Issue FE-1
**Title:** Bootstrap workspace and verify all MCP tool connectivity

**Description:**
This is the first deployment. Your job is to stand up the infrastructure every other agent depends on before they run their first task.

**Tasks (in order):**

1. Create the full workspace directory structure at `/workspaces/enzo-health/`:
   ```
   /workspaces/enzo-health/
   ├── qapi/data/
   ├── qapi/reports/
   ├── qapi/pips/
   ├── qapi/governing-body/
   ├── clinical-qa/notes/
   ├── clinical-qa/weekly-audit/
   ├── clinical-qa/reports/
   ├── survey-readiness/mock-surveys/
   ├── survey-readiness/gap-lists/
   ├── survey-readiness/poc/
   ├── regulatory/digests/
   ├── regulatory/impact-analyses/
   ├── outcomes/dashboards/
   ├── outcomes/rca/
   ├── outcomes/high-risk/
   ├── reports/
   ├── templates/
   └── data/
   ```

2. Verify connectivity for all available MCP tools:
   - Run a test ICD-10 lookup (search for "I50.9" — heart failure)
   - Run a test NPI search (search for any active home health agency NPI)
   - Run a test CMS coverage search (search LCD for "home health" or "skilled nursing")
   - Document results: which tools responded, any errors, response times

3. Create all 8 document templates in `/workspaces/enzo-health/templates/`:
   - `qapi-quarterly-report-template.md`
   - `pip-template.md`
   - `governing-body-package-template.md`
   - `note-qa-review-template.md`
   - `mock-survey-template.md`
   - `rca-template.md`
   - `regulatory-digest-template.md`
   - `outcomes-dashboard-template.md`

   Each template should be populated with the structure defined in the relevant agent's AGENTS.md file — not blank files, but ready-to-fill frameworks.

4. Create a QAPI data input template at `/workspaces/enzo-health/data/qapi-manual-input-template.csv` — a structured CSV that an agency can fill in manually before API integrations are live. Include columns for:
   - Patient ID, Admission Date, Discharge Date, Payer (Medicare/Medicaid/Private), Primary Diagnosis (ICD-10), Hospitalization (Y/N), Hospitalization Date, ED Visit (Y/N), Discharge Disposition, OASIS SOC Date, OASIS DC Date

5. Write a `README.md` at `/workspaces/enzo-health/README.md` documenting:
   - The full directory structure and what each folder is for
   - Which agent owns each folder
   - How to name files (date-prefix convention)
   - MCP tool connectivity status from step 2

**Acceptance Criteria:**
- All directories exist
- All 8 templates are populated (not blank)
- README.md is complete
- MCP connectivity report is documented in README

---

## 📋 QAPI Specialist — Issue QAPI-1
**Title:** Produce a sample Q1 QAPI report using mock agency data

**Description:**
FE-1 must be complete before starting this task (workspace and templates must exist).

Build the first end-to-end QAPI workflow output using realistic mock data so we can validate the format and quality before connecting to live agency data.

**Tasks:**

1. Using the QAPI manual input template created by the Founding Engineer, create a sample dataset representing one quarter of activity for a fictional 50-patient home health agency. Use realistic values:
   - ~50 patient episodes over 13 weeks (Q1: Jan–Mar)
   - Medicare as primary payer for 70% of patients
   - CHF, COPD, diabetes, orthopedic post-op as top diagnoses
   - Hospitalization rate around 24% (slightly above national average to give the QAPI program something to work on)
   - Mix of discharge dispositions

   Save as: `/workspaces/enzo-health/data/2026-Q1-mock-agency-sample-data.csv`

2. Using the quarterly QAPI report template, produce a complete Q1 QAPI report for this mock agency. Include:
   - All key quality indicator calculations (outcome rates, hospitalization rate, ED rate)
   - Benchmark comparison (use CMS national averages from your training data or look up current benchmarks)
   - At minimum 2 indicators that are below benchmark (to trigger PIPs)
   - Narrative analysis of each flagged indicator

   Save as: `/workspaces/enzo-health/qapi/reports/2026-Q1-mock-agency-qapi-report.md`

3. Write one complete PIP for the highest-priority indicator identified in the Q1 report. Use the full PIP template format including problem statement, root cause analysis, goal, interventions, timeline, and measurement plan.

   Save as: `/workspaces/enzo-health/qapi/pips/2026-Q1-hospitalization-reduction-pip.md`

4. Produce a governing body package summary — the executive-level summary of Q1 findings suitable for presenting to an agency's board or governing body.

   Save as: `/workspaces/enzo-health/qapi/governing-body/2026-Q1-governing-body-package.md`

**Acceptance Criteria:**
- Sample data CSV exists and is realistic
- Q1 report is complete with all sections filled
- At least 1 PIP is fully written
- Governing body package is board-ready

---

## 🩺 Clinical Documentation QA Agent — Issue CDQA-1
**Title:** Build and test the note review framework with sample visit notes

**Description:**
Create 3 sample visit notes (ranging from excellent to poor quality) and run each through the full QA review process. This validates the review framework and creates a reference library of what good and bad documentation looks like.

**Tasks:**

1. Write 3 sample home health skilled nursing visit notes representing different quality levels:
   - **Note A (Score 5/5):** A CHF patient, skilled medication management visit, excellent documentation — explicit skilled need, clear patient response, OASIS-consistent, homebound status documented, goal progress addressed
   - **Note B (Score 3/5):** A COPD patient, wound care visit, moderate quality — skilled need implied but not explicit, some vague language ("tolerated well"), missing patient response to education
   - **Note C (Score 1–2/5):** A post-hip-replacement patient, PT visit, poor quality — generic language, no skilled justification, no OASIS reference, would not survive ADR review

   Save notes to `/workspaces/enzo-health/clinical-qa/notes/` as:
   - `2026-04-03-PT001-sample-note-A.md`
   - `2026-04-03-PT002-sample-note-B.md`
   - `2026-04-03-PT003-sample-note-C.md`

2. Run each note through the full per-note QA review process. Produce a structured feedback report for each using the Note Feedback Format from your AGENTS.md.

   Save reviews as:
   - `2026-04-03-PT001-review.md`
   - `2026-04-03-PT002-review.md`
   - `2026-04-03-PT003-review.md`

3. Write a brief clinician education memo (1 page) summarizing the top 3 documentation errors found across the sample notes and how to fix them. This becomes a reference resource for new agency customers.

   Save as: `/workspaces/enzo-health/clinical-qa/reports/2026-04-documentation-coaching-memo.md`

**Acceptance Criteria:**
- 3 sample notes exist covering the quality spectrum
- 3 QA review reports are complete with scores and specific feedback
- Coaching memo is written and ready to share with agency clinicians

---

## 🔍 Survey Readiness Agent — Issue SR-1
**Title:** Produce the first mock survey against the sample patient records

**Description:**
Using the sample patient records created by the Clinical Documentation QA Agent (CDQA-1 must be complete or running concurrently), conduct a mock survey review against the most commonly cited Conditions of Participation.

**Tasks:**

1. Review the 3 sample notes from CDQA-1 as if you were a CMS surveyor conducting an unannounced survey. For each note, evaluate against:
   - § 484.55 — Comprehensive Assessment (OASIS timeliness, completeness)
   - § 484.60 — Care Planning (plan of care reflected in notes, physician orders)
   - § 484.110 — Clinical Records (signed, dated, complete)
   - § 484.75 — Skilled Professional Services (skilled care documented)

2. Produce a mock survey report documenting findings in CMS Statement of Deficiencies (SOD) format. For each deficiency found, cite the specific CFR section, describe the finding, reference the evidence, and provide the recommendation.

   Save as: `/workspaces/enzo-health/survey-readiness/mock-surveys/2026-04-mock-survey.md`

3. Produce the Priority Gap List from the mock survey findings — categorize each gap as Critical (red), Moderate (yellow), or Minor (green) with specific corrective actions.

   Save as: `/workspaces/enzo-health/survey-readiness/gap-lists/2026-04-gap-list.md`

4. For any finding that rises to Moderate or Critical level, draft a Plan of Correction using the POC template.

   Save as: `/workspaces/enzo-health/survey-readiness/poc/2026-04-sample-poc.md`

**Acceptance Criteria:**
- Mock survey report exists in SOD format with specific CoP citations
- Gap list is prioritized with color coding and corrective actions
- POC drafted for any Moderate/Critical findings

---

## 📡 Regulatory Intelligence Agent — Issue REG-1
**Title:** Produce the first weekly regulatory digest for the week of April 3, 2026

**Description:**
Stand up the weekly digest workflow. Research current regulatory environment for home health and hospice and produce the first digest. This will become a recurring weekly output.

**Tasks:**

1. Research the current regulatory environment for home health. Look for:
   - Any recent CMS QSO memos affecting home health or hospice (issued in the last 30–60 days)
   - Status of the 2026 Home Health PPS Final Rule (effective January 1, 2026) — what changed in payment rates, OASIS, or quality measures?
   - Any active proposed rules or comment periods relevant to home health
   - Any recent OIG work plan updates or audit findings in home health
   - Any LCD/NCD changes affecting common home health diagnoses (CHF, COPD, diabetes, wound care)

   Use available web search and CMS coverage MCP tools.

2. Produce the weekly regulatory digest for the week of March 30 – April 3, 2026 using the full digest format (🔴 Urgent / 🟡 Watch / 🟢 Informational + Product Implications).

   Save as: `/workspaces/enzo-health/regulatory/digests/2026-04-03-digest.md`

3. If the 2026 HH PPS Final Rule represents a significant change (payment rate change, OASIS item changes, new quality measures), produce a full Impact Analysis document.

   Save as: `/workspaces/enzo-health/regulatory/impact-analyses/2026-01-01-hh-pps-final-rule.md`

**Acceptance Criteria:**
- Weekly digest is complete with all sections filled and at least 3 items across urgency categories
- Product Implications section specifically addresses Scribe, Intake, Scheduling, and QAPI module
- Impact analysis written if 2026 Final Rule contains material changes

---

## 📊 Outcomes Analyst — Issue OA-1
**Title:** Produce the first monthly outcomes dashboard and validate HHVBP model

**Description:**
Using the mock agency data from QAPI-1, produce the April 2026 outcomes dashboard and model the HHVBP payment impact.

**Tasks:**

1. Using the Q1 mock agency data from the QAPI Specialist (QAPI-1 must be complete or data available), calculate the following outcome rates:
   - Improvement in Ambulation, Bathing, Dyspnea, Pain, Medication Management
   - Discharge to Community rate
   - Acute Care Hospitalization rate
   - ED Use without hospitalization rate
   - 30-day Rehospitalization rate
   - Timely Initiation of Care rate

   Compare each to CMS national benchmarks (use your training data for 2024–2025 benchmarks as a baseline).

2. Produce the monthly outcomes dashboard for April 2026 using the full dashboard format including STAR rating estimates, key outcome measures with benchmark comparison, hospitalization counts, HHVBP projection, and top 3 improvement opportunities with quantified impact.

   Save as: `/workspaces/enzo-health/outcomes/dashboards/2026-04-dashboard.md`

3. Using the mock data's hospitalization cases (from QAPI-1 — the patients who were hospitalized during Q1), produce 2 complete Hospitalization Root Cause Analyses. Create realistic clinical scenarios explaining why the hospitalization may have occurred and what could have prevented it.

   Save as:
   - `/workspaces/enzo-health/outcomes/rca/2026-03-15-PT010-rca.md`
   - `/workspaces/enzo-health/outcomes/rca/2026-02-28-PT023-rca.md`

4. Apply the High-Risk Patient Flagging criteria to the mock agency's current census. Identify 3–5 "patients" from the mock data who meet 2+ risk criteria and produce the weekly high-risk flag report.

   Save as: `/workspaces/enzo-health/outcomes/high-risk/2026-04-03-high-risk-flags.md`

**Acceptance Criteria:**
- Dashboard is complete with all sections, benchmark comparisons, and HHVBP projection
- At least 2 RCAs are fully written
- High-risk flag report identifies patients with specific risk factors listed

---

## 🎯 CEO Agent — Issue CEO-1
**Title:** Produce the first executive summary report and establish coordination protocols

**Description:**
Once all other Wave 1 tasks are complete (or substantially in progress), synthesize the outputs into a CEO-level summary and establish how agents will coordinate going forward.

**Tasks:**

1. Review the outputs from all Wave 1 tasks:
   - FE-1: Workspace status, template library, MCP connectivity
   - QAPI-1: Q1 report, PIPs, governing body package
   - CDQA-1: Sample reviews, coaching memo
   - SR-1: Mock survey findings, gap list, POC
   - REG-1: Weekly digest, impact analysis
   - OA-1: Outcomes dashboard, RCAs, high-risk flags

2. Write a 1–2 page executive summary suitable for Danielle (Enzo Health PM) covering:
   - What the agent org has built in Wave 1
   - What a home health agency customer would receive if they activated this suite today
   - The 3 highest-value outputs (which deliverables would have the most immediate impact for an agency)
   - Recommended Wave 2 priorities (what to build next)
   - Any gaps identified — things agents couldn't complete due to missing data, missing integrations, or tool limitations

   Save as: `/workspaces/enzo-health/reports/2026-04-03-wave1-executive-summary.md`

3. Write a coordination protocol document — how agents will work together going forward on a recurring basis. Include:
   - Weekly rhythm (what each agent produces weekly, in what order, and who receives outputs)
   - Monthly rhythm (what triggers monthly outputs, cross-agent dependencies)
   - Quarterly rhythm (full QAPI cycle, governing body package, STAR rating review)
   - Escalation rules (what gets flagged to CEO agent vs. handled autonomously)

   Save as: `/workspaces/enzo-health/reports/agent-coordination-protocol.md`

**Acceptance Criteria:**
- Executive summary is written and board-ready (clear, non-technical language)
- Wave 2 priorities are specific and actionable
- Coordination protocol covers all three rhythms (weekly / monthly / quarterly)

---

## Launch Order

```
Day 1:  FE-1       ← must go first, everything depends on workspace scaffold
Day 1:  QAPI-1     ← start immediately after FE-1 completes
        CDQA-1     ← can run in parallel with QAPI-1
        REG-1      ← can run in parallel (no dependency on other agents)

Day 2:  SR-1       ← depends on CDQA-1 sample notes
        OA-1       ← depends on QAPI-1 mock data

Day 3:  CEO-1      ← synthesizes all Wave 1 outputs
```

---

## Wave 2 Preview (after Wave 1 is complete)

- **FE-2:** Build the Scribe API connector — pull real visit notes into `/clinical-qa/` for live QA review
- **QAPI-2:** Connect to real agency data and run first live quarterly analysis
- **REG-2:** Set up recurring weekly digest schedule (automated trigger every Monday)
- **OA-2:** Build the HHVBP financial model with agency-specific baseline data
- **SR-2:** Conduct full mock survey against 10 real patient records
- **CEO-2:** Produce first customer-facing demo package showing what the platform delivers
