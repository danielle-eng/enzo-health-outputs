# High-Risk Patient Flag Report

**Agency:** Sunrise Home Health
**Report Period:** April 3, 2026
**Data Source:** Q1 2026 Census (patients with active or recent episodes)
**Prepared by:** Enzo Health Outcomes Analyst Agent

---

## Report Summary

Applied high-risk criteria to Sunrise Home Health's Q1 patient census to identify patients at elevated risk for hospitalization or adverse outcomes. Analysis flagged 5 patients meeting 2+ high-risk criteria. These patients warrant intensified monitoring, care coordination, and preventive interventions.

---

## High-Risk Criteria

Patients flagged if they meet 2 or more of the following criteria:

1. **Primary diagnosis is CHF, COPD, or pneumonia** (high-acuity, exacerbation-prone conditions)
2. **Age complexity indicator** (inferred from diagnosis complexity; Medicare payer with multi-morbidity suggests advanced age)
3. **Prior hospitalization during this episode** (demonstrated decompensation; high rehospitalization risk)
4. **Medicare primary payer with recent admission** (≤30 days from current assessment date)
5. **Prior ED visit during this episode** (indicates acute symptoms not managed outpatient)
6. **Post-surgical patient within 60 days of procedure** (elevated infection/complication risk)

---

## Flagged Patients

### FLAG 1: PT0023

**Patient ID:** PT0023
**Primary Diagnosis:** I50.9 — Heart failure, unspecified
**Admission Date:** 01/16/2026
**Discharge Date:** 03/28/2026 (Still active as of analysis date 04/03)
**Payer:** Medicare
**Status:** Discharged to home/self-care

**Criteria Met (2/6):**
1. ✓ **Primary diagnosis is CHF** — High-acuity, exacerbation-prone; typical for elderly Medicare population
2. ✓ **Medicare primary payer with recent admission** — Admitted 01/16/2026; less than 90 days from current date

**Risk Score:** 2/6 (33% risk threshold)

**Clinical Context:**
- Long episode (79 days from admission to discharge) indicates either extended recovery or frequent complications
- No hospitalization or ED visit documented during episode (positive indicator)
- CHF diagnosis alone carries 18-24% rehospitalization risk within 30 days of discharge
- Age complexity: Medicare CHF patients typically age 75+ with multiple comorbidities

**Recommended Interventions:**
1. **Intensive Transitional Care (Post-Discharge):** If patient discharged 03/28, ensure intensive monitoring for 30 days post-discharge:
   - Daily weight checks for first 14 days
   - Telephonic check-in at 48 hours post-discharge
   - Cardiology follow-up within 7 days
   - Assessment of medication access and adherence

2. **Diuretic and Volume Management Education:** Reinforce understanding of Lasix dosing, daily weights, fluid restriction (2L/day)

3. **Escalation Criteria Documentation:** Ensure patient/caregiver have written escalation pathway:
   - Weight gain ≥3 lbs in 1 day = call RN immediately
   - New dyspnea, orthopnea, or ankle swelling = same-day assessment
   - Chest discomfort or severe SOB = call 911

4. **PCP/Cardiology Coordination:** Verify post-discharge communication with cardiologist on medication adjustments, follow-up testing, and rehospitalization risk

---

### FLAG 2: PT0040

**Patient ID:** PT0040
**Primary Diagnosis:** I50.9 — Heart failure, unspecified
**Admission Date:** 03/07/2026
**Discharge Date:** 03/26/2026 (Still in episode at time of analysis; likely to discharge shortly)
**Payer:** Medicare
**Status:** Discharged to home/self-care

**Criteria Met (2/6):**
1. ✓ **Primary diagnosis is CHF** — High-acuity, exacerbation-prone
2. ✓ **Medicare primary payer with recent admission** — Admitted 03/07/2026; within 30 days of current date; very recent

**Risk Score:** 2/6 (33% risk threshold)

**Clinical Context:**
- Very recent admission (03/07, just 27 days before analysis)
- Short episode length (19 days) suggests acute presentation requiring HH intervention (likely post-hospitalization)
- No ED visit or hospitalization documented during episode
- Age/complexity: Medicare CHF patient, likely elderly with multiple comorbidities

**Recommended Interventions:**
1. **Immediate Post-Discharge Intensive Monitoring:** Patient just admitted 03/07; if discharged 03/26, implement intensive 30-day post-discharge protocol:
   - Scheduled check-in call at 48 hours post-discharge (04/27 or 04/28)
   - Weekly telephonic assessment for first month
   - One in-person RN visit at 1 week and 3 weeks post-discharge

2. **Rapid Risk Stratification:** Assess for additional risk factors:
   - Does patient live alone? (social isolation increases risk)
   - Is there cognitive decline or depression? (affects self-management)
   - What is ejection fraction? (reduced EF carries higher risk)
   - Are there comorbidities (diabetes, CKD, COPD)? (compound CHF risk)

3. **Medication Reconciliation:** Verify that discharge medications from acute hospital (if prior hospitalization) are being taken correctly; assess adherence barriers

4. **Outpatient Cardiology Engagement:** Ensure patient has cardiology follow-up scheduled within 7-14 days post-discharge; provide RN contact info in case patient needs bridge support before appointment

---

### FLAG 3: PT0050

**Patient ID:** PT0050
**Primary Diagnosis:** J18.9 — Pneumonia, unspecified
**Admission Date:** 03/10/2026
**Discharge Date:** 03/28/2026 (Still in episode; likely to discharge shortly)
**Payer:** Medicare
**Status:** Discharged to home/self-care

**Criteria Met (2/6):**
1. ✓ **Primary diagnosis is pneumonia** — High-acuity, infection-prone; recurrence risk
2. ✓ **Medicare primary payer with recent admission** — Admitted 03/10/2026; within 30 days of current date

**Risk Score:** 2/6 (33% risk threshold)

**Clinical Context:**
- Recent admission (03/10, 24 days before analysis)
- Pneumonia indicates acute infection; risk of relapse, resistant organisms, or complications
- No ED visit or hospitalization during episode suggests good management
- Typical pneumonia episode length 3-4 weeks; patient appears on track for discharge

**Recommended Interventions:**
1. **Post-Discharge Respiratory Monitoring:**
   - Assess for persistent cough, dyspnea, or fever at discharge assessment
   - Provide instructions on activity progression and avoiding respiratory irritants
   - Telephonic check-in at 48 hours and 1 week post-discharge

2. **Respiratory Assessment Protocol:**
   - Monitor oxygen saturation if prior hypoxia
   - Assess adherence to prescribed antibiotics (if still on course)
   - Screen for secondary infections (sinusitis, bronchitis)
   - Assess for recurrence risk factors: smoking history, COPD, immunosuppression

3. **Patient Education on Recurrence Prevention:**
   - Influenza and pneumococcal vaccination status verification (if not current, arrange)
   - Smoking cessation resources if applicable
   - Infection prevention: hand hygiene, mask use if high-risk contacts

4. **PCP Follow-Up:** Verify that patient has PCP follow-up scheduled within 2 weeks for repeat chest imaging or clinical reassessment if symptoms persist

---

### FLAG 4: PT0045

**Patient ID:** PT0045
**Primary Diagnosis:** I50.9 — Heart failure, unspecified
**Admission Date:** 03/22/2026
**Discharge Date:** 04/01/2026 (Post-discharge, but recently discharged)
**Payer:** Medicare
**Status:** Discharged to facility (SNF/other)

**Criteria Met (3/6):**
1. ✓ **Primary diagnosis is CHF** — High-acuity, exacerbation-prone
2. ✓ **Medicare primary payer with recent admission** — Admitted 03/22/2026; within 30 days of current date; very recent
3. ✓ **Post-discharge disposition suggests high acuity** — Discharged to facility (SNF) rather than home indicates need for additional support

**Risk Score:** 3/6 (50% risk threshold) — HIGH RISK

**Clinical Context:**
- Very recent admission (03/22, just 12 days before analysis)
- Short episode length (10 days) indicates acute CHF decompensation requiring intensive management
- Disposition to SNF rather than home/self-care suggests patient too frail or complex for independent management
- Age/complexity: Medicare CHF patient, likely elderly with multiple comorbidities affecting functional status
- Potential for SNF to HH transition or readmission to acute care if decompensation recurs

**Recommended Interventions:**
1. **Intensive Facility-Based Coordination:**
   - Establish weekly communication with SNF nursing on patient's status
   - Ensure SNF is implementing diuretic protocol and daily weights
   - Provide SNF with home health escalation criteria and direct RN contact number
   - Coordinate any needed HH services (PT, wound care) with SNF care team

2. **Planned HH Transition Preparation:**
   - Assess trajectory for discharge from SNF to HH (likely 2-4 weeks)
   - If transition planned, pre-arrange intensive HH support:
     - 3x/week RN visits for first 4 weeks
     - Daily weight monitoring via phone
     - Physician-RN escalation protocol active from day 1

3. **Frailty and Functional Assessment:**
   - Clarify why patient required SNF vs. home: mobility limitations? Cognitive decline? Unsafe home environment? Caregiver unavailable?
   - Develop plan to address limiting factors before HH discharge (PT for mobility, cognitive screening, home safety evaluation, caregiver training)

4. **Preventing Readmission Cascade:**
   - Patient at high risk for SNF → HH → Readmission → SNF cycle
   - Ensure strong discharge planning and support during HH phase
   - Schedule post-SNF-discharge HH intake visit within 48 hours of HH admission (if transition occurs)

---

### FLAG 5: PT0036

**Patient ID:** PT0036
**Primary Diagnosis:** I50.9 — Heart failure, unspecified
**Admission Date:** 03/03/2026
**Discharge Date:** 03/26/2026 (Recently discharged)
**Payer:** Medicare
**Status:** Discharged to home/self-care

**Criteria Met (2/6):**
1. ✓ **Primary diagnosis is CHF** — High-acuity, exacerbation-prone
2. ✓ **Medicare primary payer with recent admission** — Admitted 03/03/2026; within 30 days of current date (32 days, borderline)

**Risk Score:** 2/6 (33% risk threshold)

**Clinical Context:**
- Recent admission (03/03, 32 days before analysis; at edge of 30-day threshold)
- Moderate episode length (23 days) suggests acute presentation with good recovery trajectory
- No ED visit or hospitalization during episode
- Discharged to home with assumption of self-care capability

**Recommended Interventions:**
1. **30-Day Post-Discharge Transitional Care:**
   - Scheduled RN visit at 48-72 hours post-discharge (if not completed)
   - Telephonic check-in at 1 week, 2 weeks, and 4 weeks post-discharge
   - Assessment of medication adherence, weight status, dietary compliance, symptom control

2. **Home Environment Assessment:**
   - Verify patient has scale for daily weights (if not available, provide or arrange)
   - Assess for safe medication storage and adherence aids (pillbox, medication list)
   - Verify patient has phone access for emergency contact
   - Screen for social determinants: Can patient afford medications? Food security?

3. **Patient Education Review:**
   - Reinforce CHF management: diuretic use, fluid restriction, daily weights, symptom recognition
   - Provide written escalation criteria in large print, accessible location
   - Assess health literacy and adjust education materials if needed

4. **PCP/Cardiology Follow-Up:**
   - Verify cardiology appointment scheduled within 7-14 days post-discharge
   - Confirm PCP aware of recent hospitalization and HH episode
   - Ensure HH is copied on cardiologist's assessment and plan

---

## Summary

**Total High-Risk Patients Flagged:** 5

**Risk Distribution:**
- 2/6 criteria met: 4 patients (PT0023, PT0040, PT0050, PT0036) — Standard high-risk monitoring
- 3/6 criteria met: 1 patient (PT0045) — Intensive high-risk monitoring (SNF-based, frail, recent admission)

**Diagnosis Distribution:**
- CHF: 4 patients (80%)
- Pneumonia: 1 patient (20%)

**Common Risk Factors:**
- All 5 patients have Medicare primary payer
- 4 of 5 admitted in March 2026 (very recent)
- Payer type and recent admission dates suggest vulnerable population with high readmission risk

**Recommended Actions:**
1. **Immediate (by 04/06/2026):** Assign high-risk flags to primary care RNs; review recommendations with care team
2. **Short-term (by 04/13/2026):** Implement recommended interventions for all 5 patients; document in care plans
3. **Ongoing (monthly):** Monitor hospitalization/ED recurrence in these 5 patients; measure effectiveness of interventions
4. **Quarterly:** Update high-risk flags as new patients admitted; remove flags for patients discharged or no longer meeting criteria

---

*High-Risk Flag Report prepared by Enzo Health Outcomes Analyst Agent — April 3, 2026*
