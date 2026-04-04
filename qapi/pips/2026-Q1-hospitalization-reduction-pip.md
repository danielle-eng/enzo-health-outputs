# Performance Improvement Project (PIP)

**PIP Title:** Acute Care Hospitalization Reduction Initiative
**Agency:** Sunrise Home Health
**Indicator Targeted:** Acute Care Hospitalization Rate
**PIP Owner:** QAPI Specialist / Clinical Director
**Start Date:** April 4, 2026
**Target Completion:** September 30, 2026
**Status:** Active

---

## Problem Statement

Sunrise Home Health experienced an acute care hospitalization rate of 24.0% in Q1 2026 (12 of 50 patients hospitalized), significantly exceeding the CMS national benchmark of 14.7%. This represents a 9.3 percentage point gap above benchmark—a clinically and economically significant problem.

**Current State Metrics:**
- **Baseline rate:** 24.0% (12/50 patients)
- **Benchmark:** 14.7%
- **Gap:** 9.3 percentage points
- **Estimated excess hospitalizations:** 5-6 preventable episodes per quarter
- **Cost impact:** Estimated $50,000-$75,000 in excess acute care costs (at ~$10K per hospitalization)

Hospitalizations during home health episodes indicate suboptimal outpatient management, delayed intervention on clinical deterioration, or gaps in care coordination. While patient acuity and comorbidities influence hospitalization rates, the significant gap versus benchmark suggests process and system opportunities for improvement.

**Patient Population Context:**
- 72% Medicare beneficiaries (age typically 75+)
- Top diagnoses: CHF (28%), COPD (20%), Diabetes (14%), post-surgical status (14%)
- These high-risk diagnoses require proactive monitoring and early intervention to prevent acute decompensation

---

## Root Cause Analysis

### Fishbone Categories

**People (Clinical and Support Staff):**
- Limited staff training on early warning signs specific to CHF/COPD/post-op complications
- Inconsistent protocols for communication with physicians when vital signs change
- Lack of standardized escalation training (when to call MD, when to recommend ED/hospitalization vs. schedule urgent visit)
- Nurse-to-patient ratios may limit frequency of assessment for high-risk patients
- Potential gaps in caregiver education delivery during initial visits

**Process (Workflows and Protocols):**
- No formalized "early warning sign" protocol with defined thresholds for intervention
- Reactive rather than proactive assessment model (assess when patient calls, rather than scheduled high-risk monitoring)
- Delayed physician communication or unclear communication when concerns arise (no standardized templates or escalation procedures)
- Initial care plans may not include specific monitoring frequency/parameters for high-risk diagnoses
- Limited after-hours clinical access: patients/caregivers may resort to ED when unable to reach home health
- Discharge planning does not adequately prepare patients/caregivers for symptom recognition and response

**Systems/Technology (EHR, Documentation, Communication Tools):**
- EHR lacks automated alerts for high-risk diagnosis flags (CHF, COPD, post-op status)
- No dashboard or alert system for vital sign trending (daily weights for CHF, oxygen saturation for COPD)
- Communication between home health nurses and primary care physicians is primarily phone-based with inconsistent documentation in physician's chart
- Limited use of telehealth or remote monitoring (pulse oximetry, weight scales, BP cuffs) for high-risk patients
- No SMS/patient portal system to provide bedside guidance when patients first notice concerning symptoms

**Environment (Patient Acuity, Geography, Payer/Policy):**
- High proportion of vulnerable elderly population (>75) with multiple comorbidities and limited health literacy
- Some geographic service areas have ED utilization culture (patients may default to ED rather than home health call)
- Caregiver availability varies; some patients live alone with limited support system
- Medicare rules require skilled nursing but may not incentivize proactive frequent visits
- Seasonal variation: winter months may increase respiratory/cardiac exacerbations

**Data/Measurement (Reporting and Data Accuracy):**
- Hospitalization data relies on patient/caregiver report or readmission notifications from hospitals—potential lag in identification
- Current data does not distinguish between "preventable" vs. "non-preventable" hospitalizations
- Limited analysis of timing between last nursing visit and hospitalization (gap analysis)
- No root cause coding for individual hospitalizations (why admitted? when did deterioration begin?)

---

## Primary Root Causes (Prioritized)

**1. Insufficient Early Warning Sign Recognition and Response (People + Process)**
- Staff and caregivers do not have standardized protocols for recognizing early decompensation
- When concerning symptoms/signs occur, there is no clear protocol for when/how to escalate
- Reactive model: nurses assess when patients call, not on predictable schedule for high-risk diagnoses

**2. Limited Proactive Monitoring and Telehealth Capability (Systems/Technology)**
- High-risk patients (CHF, COPD) lack structured remote monitoring (daily weights, O2 sat, vitals trending)
- No automated alerts for concerning trends
- Staff unable to intervene between scheduled visits

**3. Inadequate Care Coordination with Primary Care Physicians (Process)**
- Delayed or unclear communication when patients deteriorate
- No standardized escalation protocol or template for urgent/emergent physician communication
- Uncertainty about physician preferences and protocols for patient contact/instruction

**4. Insufficient Patient and Caregiver Education (People + Process)**
- Patients/caregivers lack clear guidance on symptom recognition
- No written materials or standardized education on "when to call home health vs. 911"
- Limited education on medication compliance, diet (for CHF), activity tolerance, etc.

---

## Goal

**SMART Goal:** 

By September 30, 2026, reduce the acute care hospitalization rate from 24.0% to ≤16.0%, as measured by quarterly hospitalization rate analysis of all home health episodes completed in Q2, Q3 2026, achieving 67% reduction in the current-benchmark gap and approaching the 14.7% national benchmark. Success is defined as:
- **Interim target (Q2 2026 end):** ≤20% hospitalization rate
- **Final target (Q3 2026 end):** ≤16% hospitalization rate

This represents reduction of approximately 4 hospitalizations per quarter and annualized savings of ~$40,000-$60,000 in avoidable acute care costs.

---

## Interventions

| # | Intervention | Owner | Due Date | Status | Measurement |
|---|-------------|-------|----------|--------|-------------|
| 1 | **Develop and deploy standardized "Early Warning Sign" protocol and quick-reference guide** for top 3 diagnoses (CHF, COPD, post-op) with specific thresholds (e.g., CHF: weight gain >2-3 lbs/day, new orthopnea; COPD: increased sputum, O2 sat <88% on home O2). Distribute to all clinical staff and make available to patients/caregivers. | Clinical Director + Nursing Supervisor | 04/25/2026 | Pending | All nursing staff trained and attestation documentation; patient education materials distributed in 100% of CHF/COPD admissions |
| 2 | **Establish 24/7 clinical triage line** for patients/caregivers to call with concerns (staffed by RN or on-call RN). Create escalation protocol: triage call → assess by phone → recommend nursing visit same/next-day vs. ED evaluation. Document all triage calls in EHR. | Operations Director + Chief Nurse | 05/15/2026 | Pending | Triage line operational; call logs maintained; monthly report of call volume and disposition (visit scheduled vs. ED recommendation) |
| 3 | **Implement structured monitoring plan for high-risk diagnoses:** CHF patients = daily weight monitoring (patient or nurse call-in) + weekly nurse visit; COPD patients = oxygen sat/peak flow monitoring + weekly visits. Deploy to all CHF/COPD patients admitted Q2 onward. Consider remote monitoring devices (scales, pulse oximeters) for select patients. | Nursing Supervisor + IT Director | 05/31/2026 | Pending | 100% of CHF/COPD patients on structured monitoring; weekly monitoring logs reviewed; ≥75% compliance with daily/weekly assessments |
| 4 | **Develop and implement physician communication protocol:** Standardized template for urgent/emergent updates to primary care MD (email + phone). Clarify expectations on response time and escalation. Include physician contact preferences and patient-specific protocols in care plans. Schedule Q2 communication with all referring physicians to review protocol. | QAPI Specialist + Coding/Billing | 05/10/2026 | Pending | Protocol approved by Medical Director; 100% of referring physician practices contacted; feedback survey completed; template use tracked in EHR |
| 5 | **Enhance discharge planning and patient/caregiver education:** Develop one-page educational handout for each diagnosis (CHF, COPD, diabetes, post-op) covering: symptom warning signs, when to call home health vs. 911, medication adherence, diet/activity guidelines. Include illustration of symptom escalation timeline. Deliver at initial assessment and reinforce at discharge. | Education Coordinator + Nursing Supervisor | 05/20/2026 | Pending | Educational materials finalized and pilot-tested; 100% of patients receive materials; post-visit surveys assess understanding; integration into discharge documentation |
| 6 | **Implement preventive care measures and monitoring:** For CHF patients: daily weights + dietary sodium education + diuretic monitoring. For COPD: respiratory assessment tools + smoking cessation support + medication technique review. For post-op: wound checks, mobility progression, pain management. Include frequency/parameters in individualized care plans. | Clinical Director + Discipline Leaders (PT/OT) | 05/31/2026 | Pending | Care plans include specific preventive parameters; weekly clinical huddles review high-risk patient status; early warning sign documentation in 100% of high-risk records |
| 7 | **Establish data monitoring and escalation process:** Weekly review of all high-risk patients (CHF, COPD, recent post-op) in clinical huddle; flag any patient approaching concerning metrics. Monthly analysis of admissions in prior month: identify any hospitalizations, timing of last visit vs. admission, and documented early warning signs. Create dashboard of early warning sign trends. | QAPI Specialist + Nursing Supervisor | 05/10/2026 | Pending | Weekly huddle minutes document; monthly dashboard produced; root cause analysis completed for each hospitalization |

---

## Measurement Plan

### Baseline
- **Current rate:** 24.0% (12/50 patients hospitalized in Q1 2026)
- **Measurement period:** Q1 2026 (January 1 – March 31, 2026)
- **Data source:** Home health episode data, claim/billing records, hospital notifications

### Remeasurement Dates and Methodology

**Monthly Check-ins (Ongoing):**
- Week 1 of each month: Clinical huddle reviews all high-risk patients (CHF, COPD, post-op) and notes any new hospitalizations, ED visits, or concerning trends
- Week 2: QAPI specialist produces hospitalization tracking report (count, timing, root cause preliminary assessment)
- Week 3: Interventions reviewed for adherence and effectiveness; course corrections made as needed

**Quarterly Formal Measurement (Formal Rate Calculation):**
- **Q2 2026 (by 07/15/2026):** Calculate hospitalization rate for patients with discharge dates in Q2 (April 1 – June 30)
  - **Interim target:** ≤20% (improvement of 4 percentage points)
  - If met: continue interventions with optimization
  - If not met: escalate root cause analysis and consider additional interventions (e.g., increased monitoring frequency, more home visits)

- **Q3 2026 (by 10/15/2026):** Calculate hospitalization rate for Q3 patients (July 1 – September 30)
  - **Final target:** ≤16% (improvement of 8 percentage points toward benchmark)
  - If met: PIP complete; transition to sustainability phase with continued monitoring
  - If not met: extend PIP into Q4 with refined interventions

### Data Sources
1. **Home health EHR:** Hospitalization flag, hospital admission dates, discharge summaries
2. **Billing/claims data:** Claims for same-patient acute care admissions during home health episode
3. **Hospital notifications:** Readmission/transfer notifications received from acute care facilities
4. **Nursing documentation:** Visit notes documenting vital signs, weight trends, symptom assessments
5. **Patient/caregiver reports:** Collected at nursing visits and during triage line calls

### Success Threshold
- **Q2 success:** ≤20% hospitalization rate (minimum 4 percentage point improvement)
- **Q3 success:** ≤16% hospitalization rate (minimum 8 percentage point improvement)
- **Secondary success measures:**
  - 100% of high-risk patients on structured monitoring protocol by end Q2
  - 75% compliance with daily/weekly assessment data collection by end Q2
  - 24/7 triage line operational with documented call logs
  - Zero gaps in early warning sign protocol training among clinical staff

### Sustainability and Ongoing Monitoring
- If PIP achieves target by Q3 2026: transition to quarterly monitoring with continued data collection and annual review
- Continue physician communication protocol and patient education as standard practice
- Annual staff re-training on early warning sign recognition
- Maintain remote monitoring for high-risk diagnoses as feasible

---

## Progress Notes

**04/04/2026 — PIP Initiated**
- Baseline data confirmed: 24.0% hospitalization rate in Q1 2026 (12/50 patients)
- Root cause analysis completed; 7 interventions defined
- Roles and responsibilities assigned
- Kickoff meeting scheduled for 04/10/2026

**[To be updated quarterly with implementation progress, remeasurement results, and intervention adjustments]**

---

## Appendix: Intervention Timeline

```
April 2026:
  04/10 — PIP Kickoff meeting with all stakeholders
  04/25 — Early Warning Sign protocol finalized & staff training begins
  05/10 — Physician communication protocol finalized; MD outreach begins

May 2026:
  05/10 — Monitoring/escalation process established; weekly huddles begin
  05/15 — 24/7 triage line operational
  05/20 — Patient/caregiver educational materials finalized
  05/31 — Structured monitoring plan deployed to all CHF/COPD patients; preventive care protocols implemented

June 2026:
  06/30 — Q2 patients completed; data collection for Q2 rate calculation

July 2026:
  07/15 — Q2 hospitalization rate calculated and reported
  07/31 — Q2 results reviewed; course corrections if needed

August 2026:
  08/31 — Q3 patients midway through discharge; monitoring ongoing

September 2026:
  09/30 — Q3 patients completed

October 2026:
  10/15 — Q3 hospitalization rate calculated; final PIP assessment
```

---

*This PIP was generated by the Enzo Health QAPI Agent. It is based on Q1 2026 baseline data (24.0% hospitalization rate, 50-patient sample) and targets CMS benchmark of 14.7%. All dates and targets are projections; actual implementation may vary based on organizational resources and patient population changes.*
