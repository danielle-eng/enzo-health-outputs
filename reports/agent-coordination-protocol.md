# Agent Coordination Protocol
## Enzo Health Multi-Agent Operating System

**Prepared by:** CEO Agent
**Effective Date:** April 4, 2026
**Version:** 1.0
**Scope:** All seven Wave 1 agents operating on behalf of home health agencies

---

## Overview

Seven specialized agents work together to produce comprehensive compliance, quality, and outcomes intelligence for home health agencies. This protocol defines how they coordinate to avoid duplication, maintain data integrity, and escalate issues appropriately.

### Agent Roster

1. **QAPI Specialist** — Quality measurement, PIPs, governing body reporting
2. **Clinical Documentation QA Agent** — Visit note scoring and compliance coaching
3. **Survey Readiness Agent** — Mock surveys, gap lists, compliance readiness
4. **Regulatory Intelligence Agent** — CMS updates, LCD/NCD changes, regulatory tracking
5. **Outcomes Analyst** — Quality measures, STAR ratings, HHVBP projections, high-risk patients
6. **Founding Engineer** — System architecture, templates, data schemas
7. **CEO Agent** (Coordination) — Cross-agent dependencies, escalation, reporting

---

## Operating Rhythms

### WEEKLY RHYTHM

#### Monday 8:00 AM — Data Intake & Validation
**Who:** Outcomes Analyst, QAPI Specialist
**What:**
- Outcomes Analyst pulls new patient episode data from prior week (admissions, discharges, OASIS completions)
- Validates data completeness (all required fields present, dates logical, diagnoses valid)
- Flags any missing data to Founding Engineer for escalation
- QAPI Specialist receives validated dataset

**Deliverable:** Clean dataset ready for analysis

**Duration:** 1 hour

---

#### Monday 2:00 PM — Clinical Documentation QA Review
**Who:** Clinical Documentation QA Agent
**What:**
- Reviews all clinical notes submitted in prior 7 days (SNV, SOC, ROC, discharge notes)
- Scores each note on 5 domains: skilled care justification, assessment completeness, goal documentation, patient understanding, compliance readiness
- Identifies notes scoring <7/10 (needs revision) and flags to agency clinical director
- Identifies common errors across notes and queues them for Coaching Memo update
- Compiles weekly QA summary: total notes reviewed, % passing, top 3 deficiency types

**Deliverable:** Weekly QA report + flagged notes for rework

**Duration:** 2-3 hours (scales with note volume)

**Escalation:** Notes scoring <4/10 flagged to CEO Agent for urgent follow-up (audit risk)

---

#### Tuesday 9:00 AM — High-Risk Patient Review
**Who:** Outcomes Analyst, Clinical Risk Manager
**What:**
- Reviews all patients from current census against high-risk criteria (CHF/COPD/pneumonia diagnosis, prior hospitalization this episode, recent ED visit, post-surgical status within 60 days)
- Flags patients meeting 2+ criteria as high-risk
- For each flagged patient: documents current status, identifies care gaps, recommends intervention protocol
- Compiles weekly high-risk report with specific clinical recommendations

**Deliverable:** High-risk patient list + intervention protocols

**Duration:** 1-2 hours

**Handoff:** Report delivered to agency clinical director by Tuesday 2 PM for care team huddle scheduling

---

#### Wednesday 10:00 AM — Regulatory Digest Preparation
**Who:** Regulatory Intelligence Agent
**What:**
- Reviews all CMS publications, LCD updates, OIG audit reports, and regulatory changes from prior week
- Categorizes findings: 🔴 Urgent (action required immediately), 🟡 Monitor (track closely, may require action), 🟢 Informational (awareness only)
- Assesses impact on each Enzo product (Scribe, Intake, Scheduling, QAPI)
- Identifies any changes requiring documentation template updates or system modifications
- Compiles weekly regulatory digest

**Deliverable:** Weekly regulatory digest + product impact assessment

**Duration:** 1.5-2 hours

**Escalation:** Any urgent changes (effective within 30 days) flagged to CEO Agent for priority product roadmap discussion

---

#### Thursday 2:00 PM — PIP Progress Review (If PIPs Active)
**Who:** QAPI Specialist, Clinical Leadership
**What:**
- Reviews progress on all active PIPs against measurement plans
- Collects updated implementation data: interventions launched? Compliance rates? Any obstacles?
- Remeasures key metrics (hospitalization rate, ED utilization, assessment timeliness, etc.) if measurement window permits
- Identifies PIPs ahead/on-track vs. behind schedule
- Escalates obstacles to CEO Agent

**Deliverable:** PIP progress update memo

**Duration:** 1-2 hours

**Escalation:** PIPs falling behind target → CEO Agent coordinates with Clinical Director for course correction

---

#### Friday 3:00 PM — Weekly Agent Sync Call
**Who:** CEO Agent facilitates; all other agents report status
**Duration:** 30 minutes
**Agenda:**
1. QA Agent: documentation quality trends (are deficiencies improving or worsening?)
2. Outcomes Agent: high-risk patient updates (any new flags? Any resolved?)
3. Regulatory Agent: regulatory changes requiring product updates
4. QAPI Specialist: PIP progress
5. Survey Readiness Agent: any new compliance gaps identified?
6. CEO Agent: prioritizes next week, flags escalations to Danielle if needed

**Output:** Weekly sync summary (1-page) documenting key trends, escalations, and next week's priorities

---

### MONTHLY RHYTHM

#### By 5th of Month — Monthly Outcomes Dashboard Refresh
**Who:** Outcomes Analyst
**What:**
- Compiles all Q1/Q2/Q3 data (depending on current month) into full outcomes dashboard
- Calculates STAR rating estimate
- Updates HHVBP payment projection with current performance
- Identifies top 3 improvement opportunities (ranked by financial impact)
- Highlights any new high-risk patients admitted this month
- Compares month-over-month metrics (is hospitalization rate improving? ED utilization? Functional outcomes?)

**Deliverable:** Monthly outcomes dashboard (2-3 pages, executive summary + detailed tables)

**Distribution:** Sent to Danielle + agency CFO/Executive Director

**Timeline:** Due by end of first week of each month

---

#### By 10th of Month — Clinical Documentation Coaching Memo Update
**Who:** Clinical Documentation QA Agent
**What:**
- If new deficiency patterns identified (QA reviews across 4 weeks identify new common error):
  - Creates before/after example from actual notes
  - Writes coaching guidance (what's wrong, why it matters, how to fix)
  - Adds to master Coaching Memo
- If existing errors are improving (documented by QA scores trending upward):
  - Celebrates success in memo update (reinforces what's working)

**Deliverable:** Updated Clinical Documentation Coaching Memo

**Distribution:** Sent to all clinical staff (email + printed copies on staff board)

**Frequency:** Updated monthly (or more often if new critical deficiency identified)

---

#### By 15th of Month — Regulatory Impact Summary
**Who:** Regulatory Intelligence Agent, QAPI Specialist
**What:**
- Synthesizes all weekly regulatory digests from past month into single impact summary
- Identifies which changes have specific implications for this agency (vs. general awareness)
- Provides QAPI Specialist with any changes affecting quality measures, documentation templates, or compliance requirements
- Flags any regulatory changes requiring documentation template updates (hand-off to Founding Engineer)

**Deliverable:** Monthly regulatory impact summary + product update requirements

**Timeline:** Due by mid-month

---

#### By 20th of Month — PIP Progress Report (If PIPs Active)
**Who:** QAPI Specialist
**What:**
- Comprehensive PIP progress update covering all active PIPs
- For each PIP:
  - Milestone completion status (on time? behind? ahead?)
  - Intervention adherence (% of clinical staff trained, % of high-risk patients on structured monitoring, etc.)
  - Measurement results (if measurement window complete): are we trending toward goal?
  - Obstacles identified and mitigation strategies
- Identifies any PIPs requiring course correction (escalate to CEO Agent)

**Deliverable:** Comprehensive PIP status report

**Distribution:** Danielle + agency Executive Director

**Timeline:** Due by 20th of each month

---

#### By 25th of Month — Survey Readiness Gap Assessment Update
**Who:** Survey Readiness Agent
**What:**
- Reviews all corrective actions from prior gaps (are they complete? Did they actually fix the problem?)
- Conducts spot-check audits (review 5-10 random patient records) for any new gaps emerging
- Updates priority gap list:
  - Mark closed gaps as resolved (with evidence of correction)
  - Identify any new gaps
  - Re-prioritize based on survey risk level
- Provides revised gap list with updated target completion dates

**Deliverable:** Updated Gap List with remediation status

**Timeline:** Due by 25th of each month

---

### QUARTERLY RHYTHM

#### Month 1 of Quarter (Jan/Apr/Jul/Oct) — Full QAPI Cycle

**Week 1: Data Preparation**
- Outcomes Analyst compiles complete patient census for quarter (all patients admitted/discharged during 90-day period)
- QAPI Specialist receives clean dataset

**Week 2: Quality Measurement**
- QAPI Specialist calculates all quality indicators against national benchmarks
- Identifies which indicators are RED (≥3 points below benchmark), YELLOW (1-3 points below), GREEN (at/above benchmark)
- Conducts root cause analysis for any RED indicators

**Week 3: PIP Development (If New PIPs Needed)**
- QAPI Specialist develops formal Performance Improvement Projects for any new RED indicators
- Includes: problem statement, root cause analysis, goal (SMART), 7+ interventions with owners and due dates, measurement plan
- Circulates draft PIP to Clinical Director for feedback

**Week 4: Governance Package**
- QAPI Specialist prepares Board Quality Package:
  - Quality performance at a glance (table comparing to benchmarks)
  - Key wins this quarter (patient safety events, functional improvements, etc.)
  - Areas of concern (RED indicators with root causes + PIPs)
  - Regulatory/compliance updates from Regulatory Agent
  - Recommended board actions (motions to approve PIPs, resource allocations, etc.)

**Deliverable:** Complete quarterly QAPI report + governance package

**Timeline:** All products due by end of Month 1 (e.g., by April 30 for Q1)

**Distribution:** Danielle + Board Chair + Agency Executive Director

---

#### Month 2 of Quarter (Feb/May/Aug/Nov) — Mid-Quarter PIP Check-In

- QAPI Specialist reviews progress on active PIPs (are interventions on track?)
- Outcomes Analyst does early trend analysis (any improvement signs yet?)
- If PIPs significantly behind schedule → CEO Agent flags for course correction

---

#### Month 3 of Quarter (Mar/Jun/Sep/Dec) — Quarter-End Measurement + Next Quarter Planning

- QAPI Specialist completes full measurement of all quality indicators at quarter-end
- Outcomes Analyst produces preliminary STAR rating and HHVBP payment estimate
- Regulatory Agent scans for any CY 2027/2028 changes that should inform planning
- Leadership team reviews results, prepares for next quarter's QAPI cycle

---

## Data Flow Diagram

```
New Patient Episode Admitted
          ↓
[Intake System Captures Data]
          ↓
Weekly: Clinical notes submitted → QA Agent scores → Flagged for rework if <7/10
             ↓
             Outcomes Agent pulls OASIS → Calculates measures → Flags high-risk
             ↓
             QAPI Specialist reviews weekly summary
             ↓
Monthly: Dashboard updated → Coaching memo revised → Gaps re-assessed
             ↓
Quarterly: Full QAPI report + PIP development/update + Governance package
             ↓
[All reports to Danielle + Agency Leadership]
```

---

## Escalation Rules

### Escalate to CEO Agent Immediately (Same Day)
- Clinical QA identifies note scoring <4/10 (audit-critical deficiency)
- Outcomes Analyst flags imminent patient safety risk (e.g., patient with sepsis not on antibiotic therapy despite documented diagnosis)
- Regulatory Agent identifies change effective within 30 days (API deadline)
- QAPI Specialist determines PIP is significantly behind schedule (won't hit interim target)
- Survey Readiness Agent identifies new D/E/F-level deficiency (potential harm risk)

**Escalation Path:** Agent → CEO Agent → Danielle (with context)

**Response Time:** Danielle receives summary within 2 hours; recommended action within 4 hours

---

### Escalate to Danielle Weekly (Friday Sync)
- Weekly QA summary (% notes passing, top deficiencies, clinicians needing coaching)
- Regulatory changes requiring product roadmap updates
- PIP progress (on track vs. behind schedule)
- High-risk patient trends (any worsening? Any patterns?)
- Any obstacles requiring external intervention

**Escalation Path:** CEO Agent → Danielle (via weekly summary email + Friday call)

**Response Time:** Danielle reviews Friday; responds with direction by Monday AM

---

### Handle Autonomously (No Escalation Needed)
- Weekly QA flagging individual notes for revision (clinical director can manage)
- Regulatory awareness-only updates (no action required)
- Routine PIP progress within expected timeline
- New high-risk patient flags (clinical care team implements protocol)
- Monthly dashboard/report production (routine reporting)

---

## Handoff Standards

### File Naming Convention
All agents follow ISO-8601 date prefix + lowercase-with-hyphens format:

```
YYYY-MM-DD-[agent-type]-[report-type]-[optional-identifier].md
```

Examples:
- `2026-04-04-qapi-quarterly-report.md`
- `2026-04-03-qa-clinical-review-PT001.md`
- `2026-04-03-regulatory-digest.md`
- `2026-04-03-high-risk-flags.md`
- `2026-04-03-survey-gaps-priority-list.md`
- `2026-04-04-pip-hospitalization-reduction.md`

### Cross-Agent References
When agent A references agent B's work, use internal markdown links:

```
Based on findings in [Clinical QA Weekly Report](../../clinical-qa/reports/2026-04-weekly-audit.md),
we identified documentation gaps in wound assessment affecting [Gap #4].
```

### Metadata Headers
Every report includes:

```
**Prepared by:** [Agent Name]
**Report Period:** [Date Range]
**Agency:** [Sunrise Home Health]
**Date Generated:** [YYYY-MM-DD]
```

This ensures chain of custody and makes it clear which agent produced which output.

---

## Data Governance

### What Counts as "Clean Data"
- All required OASIS fields completed
- Patient dates logical (admission before discharge; assessment within 90 days of admission)
- ICD-10 diagnoses valid (verified against ICD-10 code list)
- No duplicate episodes (each patient-admission pair unique)
- Payer information populated

### Who Validates
Founding Engineer maintains data validation rules. Outcomes Analyst runs validation before handing data to QAPI Specialist. Any validation failures escalated to CEO Agent (cannot proceed with analysis).

### What Happens to Invalid Data
- If <5% of records are invalid: Founding Engineer corrects and re-runs analysis
- If 5-10% invalid: Escalate to agency (possible data entry errors) + proceed with valid subset
- If >10% invalid: Stop analysis, escalate to CEO Agent (systemic data quality issue)

---

## Template Management

All agents reference standardized templates stored in `/templates/` folder:

| Template | Owner | Update Frequency |
|----------|-------|-------------------|
| qapi-quarterly-report-template.md | QAPI Specialist | Quarterly (on regulatory changes) |
| pip-template.md | QAPI Specialist | As needed (new PIPs) |
| governing-body-package-template.md | QAPI Specialist | Quarterly |
| note-qa-review-template.md | Clinical QA Agent | Monthly (new deficiency patterns) |
| mock-survey-template.md | Survey Readiness Agent | Quarterly (per CoP changes) |
| rca-template.md | Outcomes Analyst | As needed (new hospitalizations) |
| regulatory-digest-template.md | Regulatory Agent | Weekly |
| outcomes-dashboard-template.md | Outcomes Analyst | Monthly |

**Update Protocol:** When regulatory or operational changes require template updates:
1. Agent identifies need (e.g., "OASIS-E2 changes require updates to note-qa-review-template")
2. Agent updates template with new data elements/fields
3. Agent notifies Founding Engineer (template change logged)
4. Agent uses updated template for all future reports
5. Founding Engineer documents change in template version notes

---

## Conflict Resolution

### Scenario 1: Outcomes Agent's High-Risk Flag vs. Clinical Director's Assessment
**Situation:** Outcomes Agent flags PT0045 as high-risk (CHF + recent admission + facility discharge). Clinical Director says patient is stable and doesn't need intensive monitoring.

**Resolution:**
1. Outcomes Agent provides clinical rationale for flag (e.g., "CHF patients have 18-24% 30-day rehospitalization risk; facility discharge indicates frailty")
2. Clinical Director reviews and either: (a) accepts flag and implements protocol, or (b) documents override with clinical rationale
3. If override, Outcomes Agent removes flag but flags the decision in monthly report to Danielle (for pattern analysis)
4. If overrides become frequent, escalates to CEO Agent to clarify criteria or recalibrate model

---

### Scenario 2: Regulatory Agent Identifies New Requirement vs. Product Roadmap Conflict
**Situation:** Regulatory Agent flags OASIS-E2 implementation (April 1 deadline). Product team is in middle of other priority (HHVBP dashboard). Who wins?

**Resolution:**
1. Regulatory Agent escalates to CEO Agent immediately (regulatory deadline is external, hard stop)
2. CEO Agent escalates to Danielle with options:
   - Option A: Push back HHVBP dashboard, prioritize OASIS-E2 (meets regulatory deadline)
   - Option B: Partial OASIS-E2 implementation by April 1, full implementation by May 15
   - Option C: OASIS-E2 via workaround (manual template update) until product update ready
3. Danielle decides; CEO Agent communicates decision to all agents

---

### Scenario 3: Multiple Agents Producing Conflicting Recommendations
**Situation:** Clinical QA Agent recommends aggressive coaching for clinician (score 4/10 on notes). Survey Readiness Agent recommends remedial documentation for the same clinician (to fix gap compliance). Which protocol applies?

**Resolution:**
1. Both are correct; they address different needs:
   - QA Agent's coaching prevents future claim denials (ongoing quality)
   - Survey Readiness Agent's remediation fixes past gap (compliance preparation)
2. Both protocols apply simultaneously (clinician gets both coaching + remediation plan)
3. CEO Agent clarifies ownership: QA Agent owns ongoing coaching; Survey Readiness Agent owns gap-specific remediation
4. Clinician is flagged for "intensive support" (weekly coaching + weekly gap remediation check-in) until both metrics improve

---

## Success Metrics

### For Each Agent

**QAPI Specialist:**
- All quarterly reports delivered on schedule
- Active PIPs achieve ≥50% of interim targets (e.g., hospitalization reduction PIP should achieve 2-point improvement by Q2)
- Board package completed by deadline

**Clinical Documentation QA Agent:**
- 100% of notes reviewed within 48 hours of submission
- Documentation quality scores trending upward month-over-month
- <5% of notes flagged for revision (target: 85%+ pass rate)

**Survey Readiness Agent:**
- All identified gaps have documented corrective actions within 2 weeks
- Target: 0 new gaps identified in follow-up survey; all prior gaps resolved

**Regulatory Intelligence Agent:**
- 100% of regulatory digests delivered on schedule
- Zero missed regulatory deadlines (all changes identified ≥30 days before effective date)
- Product team receives ≥2 weeks notice before new documentation/system changes required

**Outcomes Analyst:**
- Monthly dashboard delivered by 5th of month
- HHVBP payment projection accuracy within ±2% (measured against CMS published scores)
- High-risk flags result in 25%+ reduction in hospitalization rate for flagged patients

**Founding Engineer:**
- System uptime 99.5%+
- Data validation catches 95%+ of data quality issues
- New templates deployed within 48 hours of request

**CEO Agent:**
- All escalations resolved within SLA (immediate = 2 hours; weekly = 24 hours)
- Weekly sync summary delivered every Friday
- Danielle receives no surprises (all significant findings flagged proactively)

---

## Transition from Wave 1 to Production

### Phase 1: Mock Data → Live Data (Week 1-4 of Wave 2)
- Agents continue running on mock data set (Sunrise Home Health)
- Simultaneously, integrate live data from pilot agency (TBD)
- Run side-by-side comparison: does system produce same insights on real data?
- Refine data validation rules, measurement algorithms

### Phase 2: Pilot Agency (Week 5-12)
- Go live with one real home health agency (not-for-profit preferred; lower downside risk)
- Agents produce all standard reports (weekly, monthly, quarterly)
- Clinical team implements recommendations from agents
- Measure: do interventions improve quality metrics?

### Phase 3: Onboarding SOP (Week 13+)
- Document: what does successful onboarding look like?
- Define: what's the minimum data needed to get agents running?
- Create: onboarding checklist for new agencies (data export template, admin setup, staff training)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-04 | Initial Wave 1 protocol |

---

*Agent Coordination Protocol v1.0 | Enzo Health | April 4, 2026*
