# Enzo Health — Quality Management Product Context
**For internal AI agent use. Last updated: April 3, 2026. Compiled from live demo environment at demoagency.enzo.health.**

---

## What Quality Management Is

Quality Management is Enzo Health's central quality command center — the most directly relevant existing product to the Paperclip QAPI, Survey Readiness, and Clinical Documentation QA agents. It consolidates risk identification, chart auditing, incident tracking, and survey readiness into a single dashboard. Unlike the reporting module (which provides historical data exports), Quality Management is a real-time, action-oriented workspace. It surfaces what needs attention today and gives managers tools to assign work, create action plans, and track resolution.

The primary user is the **Clinical Manager** (Zach role in demo). The module is accessible from the main navigation and opens to the Overview tab by default.

---

## Interface Structure

Quality Management has four tabs:

| Tab | Purpose |
|---|---|
| **Overview** | Executive dashboard — risk summary, work queue, quick-access cards |
| **Chart Audits** | Chart review queue — pending and returned audits assigned to QA staff |
| **Incidents & Logs** | Incident reporting — falls, medication errors, infections, near-misses |
| **Survey Readiness** | Compliance tracking against Conditions of Participation |

---

## Overview Tab

The Overview tab is the Quality Management command center. It has four main components:

### Dashboard Metrics (Top Row)
Five metric cards spanning the top of the Overview:

| Metric | Demo Value | What It Means |
|---|---|---|
| **High Risk Patients** | 5 | Patients flagged as high-acuity based on OASIS, visit patterns, or clinical conditions |
| **Open Tasks** | 24 | Quality-related tasks not yet resolved across all work queue items |
| **Charts Flagged** | 31 | Clinical charts flagged for QA review or containing documentation issues |
| **Active Incidents** | 3 | Open incident reports (falls, medication errors, infections, etc.) |
| **Survey Status** | Yellow | Overall survey readiness state (Red / Yellow / Green) |
| **CMS Quality STAR** | 4.5 (+0.5 vs last year) | The agency's public CMS Overall Quality of Patient Care STAR rating with year-over-year trend |

The CMS STAR rating is the most public-facing metric in the platform — a 4.5 star agency is in the top tier nationally. The +0.5 vs. last year trend indicates meaningful improvement and should be called out in CEO/governing body reporting.

---

### Top Risks Driving Quality (Center Panel)

The core intelligence feature of Quality Management. This panel uses AI to surface and prioritize the agency's current quality risks. Each risk item includes:

- **Severity label** — High / Moderate / Low (color-coded)
- **Risk description** — plain-language description of the quality problem
- **Impact areas** — which STAR measures, HHCAHPS composites, and/or CMS CoP citation are affected
- **Quantified impact** — specific numerical estimate of the risk's effect (e.g., "-0.3 potential stars", "+18% hospitalization risk", "-7% on benchmark measure")
- **"Create action plan" button** — opens the Action Plan modal directly from the risk item (see below)

**Demo snapshot (April 3, 2026) — Top Risks:**

| Severity | Risk | Impact Areas | Quantified Impact |
|---|---|---|---|
| 🔴 High | Late OASIS submissions in SN discipline | Star Ratings, ACH benchmark, §484.55 | -0.3 potential stars |
| 🔴 High | Inconsistent wound orders vs. documentation | Survey readiness, §484.60, Infection control | +18% hospitalization risk |
| 🟡 Moderate | Medication education not documented at SOC | Med Education benchmark, Star Ratings | -7% on benchmark measure |
| 🟡 Moderate | Delayed SOC visits after referral | Timely Initiation measure, Star Ratings, §484.55 | -0.2 potential stars |
| 🟢 Low | Supervisory visit documentation incomplete | §484.80, Aide oversight compliance | Potential survey finding |

This list is the real-time equivalent of a QAPI indicator dashboard. The Paperclip QAPI agent should treat this panel as the native system's prioritized finding list and ensure its own quarterly outputs are consistent with (and deeper than) what appears here.

---

### Action Plan Modal

When a user clicks "Create action plan" on any Top Risk item, a modal opens with the following structure:

- **Description** — the full risk description from the panel (pre-populated)
- **Estimated Impact** — quantified impact carried over from the risk card
- **AI Insight** — a computed projection showing the STAR rating improvement achievable if this issue is corrected (e.g., "Resolving this issue could improve your STAR rating by 0.3 points over the next 2 quarters")
- **Create action plan button** — clicking this generates a PIP/action plan and adds it to the work queue

This modal is the bridge between risk identification and intervention. The AI Insight feature means the platform already estimates improvement potential — agent PIPs should align with or contextualize these projections.

---

### Priority Work Queue (Right Panel)

An ordered, actionable task list displaying the most urgent quality items. Each row includes:

| Field | Description |
|---|---|
| Severity badge | High / Moderate / Low color dot |
| Task description | What needs to be done and which charts or patients are involved |
| Due date | "Overdue", "Due today", "Within 3 days", or a specific date |
| Owner | Name and role of the assigned staff member |

**Demo snapshot — Priority Work Queue (April 3, 2026):**

| Severity | Task | Due | Owner |
|---|---|---|---|
| 🔴 High | Late OASIS submissions — 7 charts | Overdue | QA M. Patel |
| 🔴 High | Catheter-associated UTI follow-up | Due today | QA Nurse R. Sullivan |
| 🟡 Moderate | Infection control gaps — 2 charts | Within 3 days | IC Nurse L. Thomas |
| 🟡 Moderate | Chart audit returned — Ana Rodriguez | Due today | QA K. Johnson |
| 🟡 Moderate | POC not updated at recert — 3 charts | Within 3 days | CM D. Harris |
| 🟡 Moderate | Fall investigation pending — Margaret Chen | Within 3 days | CM D. Harris |
| 🟡 Moderate | Missed visit documentation — 5 visits | Within 3 days | Branch Mgr R. Green |
| 🟢 Low | Pending audit — Margaret Chen | 12/05 | Coding L. Ramirez |

The work queue is the operational to-do list for the QA and clinical management team. Items here should cascade into agent outputs — if the QAPI agent produces a PIP for hospitalization reduction, a corresponding task should appear (or be recommended to appear) in this queue.

---

### Quick-Access Cards (Bottom Row)

Three summary cards that give instant counts on the three sub-module areas:

**Chart Audits:**
- 8 pending chart audits
- 3 returned (sent back to clinician for corrections)
- Opens the Chart Audits tab

**Incidents & Logs:**
- 3 open incidents
- 1 high-severity incident
- Opens the Incidents & Logs tab

**Survey Readiness:**
- 17 total compliance issues
- 4 high-priority issues
- Opens the Survey Readiness tab

---

## Chart Audits Tab

Manages the chart review lifecycle. Clinical QA staff are assigned charts for audit review, and this tab tracks the status of each review.

**Key statuses:**
- **Pending** — chart has been flagged and assigned to a reviewer, review not yet started
- **Returned** — reviewer has completed review and sent the chart back to the clinician for corrections

The 8 pending / 3 returned counts visible from the Overview card represent the current queue depth.

### Agent Implication (Clinical Documentation QA):
The Chart Audits tab is where the Clinical Documentation QA agent's review outputs belong. When the API is live, agent review reports should populate this queue directly — each note review the agent completes should appear as an audit item in this tab with findings attached.

---

## Incidents & Logs Tab

Tracks adverse events and near-misses occurring during the home health episode. Categories include:

- Falls (most common)
- Medication errors
- Infections
- Near-misses
- Other incidents

Each incident has a severity classification and open/closed status. The 3 open incidents (1 high) shown in the demo are the current unresolved events requiring follow-up.

### Agent Implication (QAPI Specialist):
Incident counts feed into QAPI outcome measures. Fall rate and medication error rate are QAPI indicators. The QAPI agent's quarterly analysis should reference incident log totals from this tab to calculate event rates.

### Agent Implication (Survey Readiness):
Incident documentation, investigation completion, and corrective action timelines are survey-reviewed items. The Margaret Chen fall investigation (visible in the Priority Work Queue) is an example of an incident that crosses both the Incidents & Logs and the work queue.

---

## Survey Readiness Tab

Compliance tracking against the Conditions of Participation (42 CFR Part 484). This tab functions as the agency's internal compliance checklist — it tracks where the agency has confirmed compliance and where gaps exist.

The 17 total issues / 4 high-priority issues shown in the demo represent the current survey readiness posture. A Yellow survey status (visible in the Overview dashboard metrics) means the agency has some issues that need remediation but is not at high risk.

**Survey status definitions:**
- 🟢 **Green** — No significant survey risk; agency is in strong compliance posture
- 🟡 **Yellow** — Some compliance gaps; targeted remediation needed before a survey
- 🔴 **Red** — Significant compliance risk; immediate intervention required

### Agent Implication (Survey Readiness Agent):
The Survey Readiness tab is the agent's primary data source when API-connected. Mock survey outputs and gap lists produced by the agent should mirror and extend the findings already captured here. The agent's value-add is depth — taking a gap identified in this tab and producing a full SOD-format finding with corrective action.

---

## Connection to Other Modules

Quality Management integrates with every other Enzo product:

| Source Module | What It Feeds into Quality Management |
|---|---|
| **OASIS Management** | Late OASIS submissions → Top Risks, Work Queue overdue items |
| **Scheduling** | Missed visits, returned visits → Incidents, QAPI indicators |
| **Intake** | Declined referral rates → QAPI operational metrics |
| **Scribe** | Visit note content → Chart Audits (when note has QA flag) |
| **Reports & Analytics** | STAR ratings, HHCAHPS scores, rehospitalization → Overview dashboard metrics |

---

## Agent Integration Map

| Agent | Quality Management Connection |
|---|---|
| **QAPI Specialist** | This is the native QAPI module. The Top Risks panel is the real-time QAPI indicator list. Agent quarterly reports should be consistent with and deeper than what appears here. PIPs generated by the agent should correspond to action plans created in this system. |
| **Clinical Documentation QA** | Chart Audits tab is the native home for note review results. Agent review outputs should be structured to populate this tab. Returned chart counts are a quality metric in themselves. |
| **Survey Readiness** | Survey Readiness tab is the primary data source for mock survey work. The 17 open issues in demo are the starting point for gap prioritization. Mock surveys should produce outputs in the same format as findings here. |
| **Outcomes Analyst** | The 4.5 STAR rating is the agency's public quality score. All outcomes analysis should be oriented around moving this number. STAR rating year-over-year trend (+0.5) is a performance validation data point. |
| **CEO Agent** | Quality Management Overview is the executive dashboard. CEO synthesis reports should match the format and framing of this view. The High Risk / Open Tasks / Charts Flagged / Survey Status summary is the executive quality scorecard. |
| **Founding Engineer** | Quality Management API (not yet connected) should eventually push Top Risks and Work Queue items into agent context automatically. Until then, agents work from manually provided snapshots. |

---

## Known Gaps / Placeholder Areas

- **Chart Audits tab detail** — individual audit record format, clinician feedback structure, reviewer assignment workflow not fully explored in demo
- **Incidents & Logs tab detail** — individual incident form fields, investigation workflow, notification requirements not explored
- **Survey Readiness tab detail** — specific CoP line items tracked, compliance evidence fields, how gaps are marked as resolved not explored
- **Action plan lifecycle** — how a created action plan moves from modal → work queue → completion not confirmed from demo
- **QAPI report generation** — whether Quality Management generates the formal QAPI quarterly report natively or whether that is an agent function (likely the latter)

*These sections will be updated when the Enzo PM provides additional product documentation.*
