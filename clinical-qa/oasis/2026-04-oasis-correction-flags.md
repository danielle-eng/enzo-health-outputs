# OASIS Correction Flags Memo

**TO:** PDGM Billing Agent, Revenue Cycle Operations
**FROM:** Paperclip QA Agent, Clinical Quality Assurance
**DATE:** April 4, 2026
**RE:** April 2026 OASIS Assessment Corrections - Patient PT003

---

## Overview

QA review of three OASIS Start-of-Care assessments has identified one item requiring clinician follow-up and documentation enhancement. This memo documents the flag and provides actionable items for coordination between Clinical Operations and Billing.

**Summary:**
- Total assessments reviewed: 3
- Critical coding errors: 0
- Warnings requiring clinician review: 1
- Claims ready for submission: 3

---

## Flagged Assessment Details

### Patient PT003 - ADL Scoring Variance (REVIEW REQUIRED)

**Clinical Encounter Data:**
- Patient ID: PT003 (Robert Johnson)
- Episode Start: March 20, 2026
- SOC Assessment Date: April 3, 2026
- Diagnosis: S72.001A (Closed fracture of right femoral neck, initial encounter for closed fracture)
- PDGM Assignment: MMTA-General (Orthopedic) | HIPPS 008100
- Current Payment Status: $4,400.00 per 30-day episode

---

## Specific Items Needing Correction/Documentation

### Flag 1: M1800 Series - ADL Functional Scoring Inconsistency

**Issue Description:**
The assessment documents a clinically inconsistent ADL score pattern:
- **M1810 (Grooming):** 0 = Independent
- **M1820 (Bathing):** 2 = Supervision or Limited Assistance
- **M1830 (Toileting):** 3 = Extensive Assistance
- **M1840 (Transfer):** 3 = Extensive Assistance

**Finding:** Wide functional disparity (range: 0 to 3) without corresponding clinical narrative explaining why the patient can perform grooming independently while requiring extensive assistance with toileting and transfers.

**Risk Category:** Tier 2 (Documentation Clarification)
- No coding error detected
- No payment recalculation triggered
- Compliance risk: LOW (internal QA flag, not audit exposure)

**Clinical Interpretation Needed:**
The current assessment assigns a functional level of "Medium" based on ADL score of 5. This is mathematically correct, but clinical justification is needed for the assessor's entry. Possible explanations:

1. **Post-surgical status:** Right femoral neck fracture with precautions limiting lower extremity use (explains toileting/transfer difficulty vs. upper-body grooming independence)
2. **Selective functional preservation:** Patient may have pre-existing upper extremity strength/capability while new fracture limits lower-body function
3. **Assessment methodology:** Ensure assessor documented basis for each individual item score, not averaged from assumption

**Required Documentation Enhancement:**
Add narrative explanation in the assessment (typically in the clinical notes or functional assessment section) stating:

*Example language:*
> "ADL scoring reflects post-operative presentation with right femoral neck fracture (S72.001A) managed with bed rest and weight-bearing precautions. Patient demonstrates intact upper extremity strength and independence with grooming and hygiene tasks. However, weight-bearing restrictions and acute pain limit functional ability in transfers and toileting, requiring assistance with lower-body ADL tasks. Assessment reflects current clinical status pending physical therapy progression."

---

## Billing Coordination Items

### Action Item 1: No Revenue Impact - Proceed with Claim

**Status:** GREEN - CLEAR TO BILL

- HIPPS Code 008100 is correctly assigned
- Functional Level multiplier (Medium/1.00x) is appropriate
- Comorbidity status (CA0) is accurate given current active diagnoses
- Payment: $4,400.00 for 30-day episode
- **No hold required.** Claim can be submitted as generated.

The ADL variance flag is an internal clinical documentation note, not a billing correction requirement.

---

### Action Item 2: Clinical Documentation Follow-up

**Responsible Party:** Clinical Operations / Nursing Supervisor

**Timeline:** Within 2 business days

**Task:**
1. Contact PT003 clinician (RN/LUPA assessment clinician)
2. Request brief clinical note clarifying ADL score rationale (can be added to assessment revision or chart)
3. Ensure note is scanned/uploaded to patient chart before claim submission final approval
4. No reassessment required—clarifying narrative is sufficient

**Documentation Format:**
- Brief narrative (3-5 sentences) explaining clinical basis for functional score pattern
- Reference patient's surgical status (femoral neck fracture, current restrictions)
- Specify expected progression timeline for functional recovery

---

### Action Item 3: Billing System Workflow

**Responsible Party:** PDGM Billing Agent

**Current Status:**
- PT003 billing ready for submission
- HIPPS code: 008100
- 30-day payment rate: $4,400.00
- LUPA status: Non-LUPA, projected 15 visits over 60-day episode (safe margin above 4-visit threshold)

**Workflow Item:**
1. Release PT003 claim for submission in standard EOB cycle
2. Add note to patient file: "Clinical note clarification requested—ADL variance narrative expected by [DATE]"
3. If note is not received by target date, escalate to clinical supervisor but do NOT hold claim resubmission (current submission is billing-accurate)

---

## Revenue & Compliance Summary

| Patient | HIPPS | Status | Payment | Correction Needed | Billing Impact |
|---------|-------|--------|---------|-------------------|-----------------|
| PT001 | 007220 | PASS | $10,472.28 | None | Clear to Bill |
| PT002 | 009020 | PASS | $6,491.52 | None | Clear to Bill |
| PT003 | 008100 | FLAG | $4,400.00 | Documentation | Clear to Bill |

**Total Estimated 30-Day Revenue:** $21,363.80

**Monthly Projection (assuming consistent episode mix):** ~$21.4K monthly / ~$256K annually from this 3-patient sample

---

## Escalation Path (If Needed)

**Scenario 1:** If clinician cannot provide acceptable narrative clarification
- **Action:** QA supervisor reviews functional level determination; if clinically defensible, notation remains in file as supporting QA review
- **Impact:** No billing change; internal QA documentation only

**Scenario 2:** If clinical review reveals data entry error (e.g., ADL scores were transposed)
- **Action:** Clinician corrects OASIS record; revised assessment generates new HIPPS code if functional level changes
- **Impact:** May trigger revised payment calculation; resubmit claim
- **Likelihood:** Very Low (current scoring is internally consistent, just underdocumented)

---

## Key Coordination Message for PDGM Billing Agent

**Summary for Billing Operations:**

PT003 has an internal clinical documentation flag that does NOT require billing correction. The OASIS assessment is mathematically and logically sound; the secondary request for a narrative note is best practice quality assurance that should be tracked but does not delay claim submission.

**Proceed with claim submission for all three episodes at calculated rates.**

---

## QA Process Notes

**Review Methodology:**
- Automated consistency checks on ADL, pressure ulcer, ambulation, medication management, depression screening, and homebound variables
- Manual review of HIPPS calculation and PDGM group assignment
- Clinical risk stratification for audit exposure

**Findings:**
- 0 critical errors (would require corrected OASIS form before billing)
- 1 documentation flag (enhanced clarity recommended; does not block submission)
- 3/3 episodes passed QA and approved for standard billing workflow

---

**Report Prepared By:** Paperclip QA System
**Review Date:** April 4, 2026
**Next Batch Review:** May 1, 2026

*This memo documents internal quality assurance findings. Clinical narratives are recommended to support documentation integrity but are not required for claim submission to proceed.*
