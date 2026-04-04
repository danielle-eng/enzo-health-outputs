# Enzo Health Paperclip — Wave 4 Launch Tasks

Wave 4 activates the four new agents built in pre-Wave 4 prep and integrates them with the existing 8 agents into a fully coordinated 12-agent system. The goal is end-to-end patient journey coverage — from first referral call through final discharge — with all agents handing off to each other automatically.

---

## 🏗️ Founding Engineer — Issue FE-4
**Title:** Extend workspace for new agents + build end-to-end patient journey orchestration

**Tasks:**

1. Create new workspace directories for the four new agents:
   ```
   /workspaces/enzo-health/
   ├── intake/                     ← Intake & Referral Agent outputs
   ├── clinical-qa/oasis/          ← OASIS QA Agent outputs
   ├── billing/                    ← PDGM/Billing Agent outputs
   └── scheduling/                 ← Scheduling/Visit Frequency Agent outputs
   ```

2. Update `run_agent_workflow.sh` to include all four new agent scripts in the correct pipeline order:
   ```
   Intake → OASIS QA → PDGM/Billing → Scheduling → Recert/Discharge → Clinical QA → QAPI → Outcomes → CEO
   ```

3. Build an end-to-end patient journey orchestration script at `/data/scripts/patient_journey_pipeline.py`:
   - Accepts a patient ID and agency ID
   - Runs intake screening → OASIS QA → PDGM billing review → scheduling check → recert/discharge evaluation in sequence
   - Produces a single unified patient summary report tying all agent outputs together
   - Saves to `/reports/patient-journey/YYYY-MM-DD-[patient-id]-full-journey.md`

4. Write a `WAVE-4-COMPLETION-SUMMARY.md` documenting what was built in Wave 4.

**Save all files to the workspace. Push to GitHub.**

---

## 🔬 OASIS QA Agent — Issue OASIS-1
**Title:** First full OASIS accuracy audit across the mock agency census

**Tasks:**

1. Run `oasis_qa_checker.py` for all 3 sample patients (PT001, PT002, PT003) in batch:
   - Review each patient's OASIS for internal consistency errors
   - Flag any Tier 1 payment-critical items with issues
   - Generate per-patient OASIS QA review reports

2. Produce a monthly OASIS Accuracy Report summarizing:
   - Total assessments reviewed
   - Error rate by OASIS item tier (Tier 1 / Tier 2 / Tier 3)
   - Top 3 most common OASIS scoring errors found
   - Items flagged for correction before billing submission
   - Estimated PDGM payment impact of identified errors

   Save as: `/clinical-qa/oasis/2026-04-oasis-accuracy-report.md`

3. For any Tier 1 item errors found: create a correction memo flagging those patients to the PDGM Billing Agent.

   Save as: `/clinical-qa/oasis/2026-04-oasis-correction-flags.md`

**Push all outputs to GitHub.**

---

## 💰 PDGM / Billing & Coding Agent — Issue PDGM-1
**Title:** First full agency billing review — revenue optimization and LUPA risk scan

**Tasks:**

1. Run `pdgm_billing_checker.py` for all 3 sample episodes (EP001/PT001, EP002/PT002, EP003/PT003):
   - Calculate HIPPS codes and 30-day payment amounts for each
   - Identify comorbidity adjustment opportunities
   - Check ICD-10 code accuracy and PDGM grouping
   - Generate per-episode billing review reports

2. Produce an Agency Revenue Optimization Report summarizing:
   - Total estimated 30-day revenue across reviewed episodes
   - Revenue at risk from coding errors or missed comorbidity adjustments
   - LUPA risk patients and estimated payment impact if LUPA triggered
   - Top 3 revenue leakage patterns identified
   - Specific action items: which patients need recoding, which need comorbidity documentation

   Save as: `/billing/2026-04-revenue-optimization-report.md`

3. Calculate the potential annual revenue impact if the identified optimizations were applied across a 50-patient agency census (extrapolate from the sample).

   Include in the report above.

**Push all outputs to GitHub.**

---

## 📥 Intake & Referral Agent — Issue INTAKE-1
**Title:** First intake pipeline report — referral velocity, acceptance rates, rejection analysis

**Tasks:**

1. Run `intake_screening_processor.py` against the 3 sample referrals (REF-20260404-001, -002, -003):
   - Produce screening reports for each referral
   - Document accept/conditional accept/decline decisions with rationale

2. Produce an Intake Pipeline Report for April 2026:
   - Referral volume summary (total received, accepted, conditional, declined)
   - Average time-to-screening (target: < 2 hours)
   - Top rejection reasons and their frequency
   - Missing documentation patterns (what's most commonly missing from referrals)
   - Estimated revenue impact of declined referrals (if the issue had been addressed)
   - Recommendations for referral source education (what to send with a referral)

   Save as: `/intake/2026-04-intake-pipeline-report.md`

3. Create a one-page Referral Source Education Sheet — a simple checklist of what referring physicians/hospitals need to include with a home health referral to maximize acceptance speed.

   Save as: `/intake/referral-source-checklist.md`

**Push all outputs to GitHub.**

---

## 📅 Scheduling & Visit Frequency Agent — Issue SCHED-1
**Title:** First scheduling compliance report — LUPA risk identification and visit gap analysis

**Tasks:**

1. Run `scheduling_compliance_checker.py` against the sample agency census:
   - Calculate compliance rates for all active patients by discipline
   - Identify patients at LUPA risk
   - Flag clinicians with productivity concerns

2. Produce a Weekly Scheduling Compliance Report for the week of April 4, 2026:
   - Overall agency compliance score
   - Patients at LUPA risk with days remaining and visits needed
   - Visit frequency gap analysis by discipline
   - Clinician productivity dashboard (schedule fill rate, no-show rate)
   - Action items: who needs visits scheduled this week to avoid LUPA

   Save as: `/scheduling/2026-04-04-scheduling-compliance.md`
   (Update the existing file if it already exists)

3. Write a LUPA Prevention Protocol — a 1-page workflow for scheduling coordinators to follow when a patient is flagged as LUPA risk:
   - When to escalate
   - How to prioritize scheduling
   - What to document when visits cannot be completed

   Save as: `/scheduling/lupa-prevention-protocol.md`

**Push all outputs to GitHub.**

---

## 🎯 CEO Agent — Issue CEO-4
**Title:** Wave 4 executive summary + updated HTML dashboard + customer demo package

**Tasks:**

1. Review all Wave 4 outputs from each agent:
   - OASIS-1: OASIS accuracy report and correction flags
   - PDGM-1: Revenue optimization report with financial impact
   - INTAKE-1: Intake pipeline report and referral source checklist
   - SCHED-1: Scheduling compliance report and LUPA prevention protocol
   - FE-4: End-to-end orchestration and workspace updates

2. Update the HTML dashboard at `/reports/enzo-dashboard.html` to add four new sections:
   - **Intake Pipeline Panel**: referral volume, acceptance rate, avg time-to-screen, top rejection reasons
   - **PDGM Revenue Panel**: total estimated revenue, revenue at risk, LUPA exposure, top comorbidity adjustments
   - **OASIS Accuracy Panel**: assessment accuracy rate, Tier 1 error count, correction items pending
   - **Scheduling Compliance Panel**: agency compliance score, patients at LUPA risk, clinician RED FLAG count

   Use Chart.js (already included). Add the new panels after the existing KPI cards. Keep the existing panels intact.
   Use the same dark theme and card style as the existing dashboard.

3. Write a Wave 4 Executive Summary for Danielle covering:
   - What the 12-agent system now covers end-to-end
   - The revenue story: PDGM optimization + LUPA prevention + intake conversion = quantified annual value
   - What a home health agency gets on Day 1 vs. Day 30 vs. Day 90
   - Recommended Wave 5 priorities

   Save as: `/reports/2026-04-04-wave4-executive-summary.md`

4. Update the customer-facing one-pager (`/reports/customer-one-pager.md`) to reflect the full 12-agent suite.

**Push all outputs to GitHub.**

---

## Launch Order

```
Parallel (no dependencies):
  OASIS-1    ← run oasis_qa_checker.py + monthly accuracy report
  INTAKE-1   ← run intake_screening_processor.py + pipeline report
  SCHED-1    ← run scheduling_compliance_checker.py + LUPA protocol

After OASIS-1 completes:
  PDGM-1     ← depends on OASIS correction flags to inform coding review

After all above complete:
  FE-4       ← update orchestration to include all new agents
  CEO-4      ← synthesize all Wave 4 outputs + update dashboard
```

---

## Wave 5 Preview (after Wave 4 is complete)

- **Live Scribe Integration**: Connect all agents to real Enzo Scribe API with ENZO_API_KEY
- **Customer Onboarding Automation**: End-to-end agency onboarding workflow (intake → first QAPI → first dashboard)
- **Predictive Risk Model**: ML-based hospitalization prediction using OASIS + visit note features
- **Payer Contracting Intelligence**: Analyze payer mix, flag Medicare Advantage plans with unfavorable terms
- **Staff Productivity Analytics**: Deep clinician performance analysis with coaching recommendations
