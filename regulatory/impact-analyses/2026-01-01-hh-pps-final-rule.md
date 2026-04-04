# CY 2026 Home Health Prospective Payment System (HH PPS) Final Rule
## Impact Analysis for Home Health Agencies and Software Vendors

**Rule Reference:** CMS-1828-F
**Publication Date:** December 2, 2025 (Federal Register)
**Effective Date:** January 1, 2026
**Analysis Date:** April 4, 2026
**Prepared By:** Enzo Health Regulatory Intelligence

---

## Executive Summary

The CY 2026 Home Health Prospective Payment System Final Rule, published by CMS on November 28, 2025, represents a significant update to Medicare home health payment policies and quality measurement requirements. The most consequential change is a **net 1.3% aggregate payment reduction** to home health agencies ($220 million annually), which is substantially less than the 6.4% reduction originally proposed in June 2025.

This analysis covers:
1. Payment rate changes (net reduction of 1.3%)
2. OASIS item additions, deletions, and modifications
3. New and modified quality measures
4. HHVBP model updates
5. Required agency compliance actions
6. Enzo product roadmap implications

---

## I. PAYMENT RATE CHANGES — EFFECTIVE JANUARY 1, 2026

### A. Aggregate Payment Adjustment

**Net Change: -1.3% (approximately $220 million reduction annually)**

This represents a significant reduction from the 6.4% ($1.135 billion) payment cut originally proposed in June 2025. The substantial decrease in the final reduction was driven by CMS's reconsideration of its permanent adjustment methodology following extensive industry comments.

### B. Components of the Final Rate Adjustment

The net 1.3% reduction is composed of:

| Component | Amount | Percentage |
|-----------|--------|-----------|
| CY 2026 HH Payment Update Factor | +$405 million | +2.4% |
| Permanent Adjustment (PDGM recalibration) | -$150 million | -0.9% |
| Temporary Adjustment (mitigation) | -$460 million | -2.7% |
| Fixed-Dollar Loss Ratio Update | -$15 million | -0.1% |
| **Net Payment Change** | **-$220 million** | **-1.3%** |

### C. Per-Episode Impact

On average, the net reduction translates to approximately **$19 per 30-day home health episode**, though the actual impact varies significantly based on:
- Patient case-mix group (PDGM classification)
- Geographic location (wage index)
- Agency-specific LUPA (Low Utilization Payment Adjustment) thresholds
- Outlier payment qualification

### D. Permanent vs. Temporary Adjustments

**Permanent Adjustment: -1.023%**
- CMS finalized a permanent prospective payment adjustment to account for the impact of Patient-Driven Groupings Model (PDGM) implementation for CYs 2020-2022
- This adjustment reflects actual utilization patterns versus CMS's original assumptions
- This adjustment carries forward into future years unless CMS modifies methodology

**Temporary Adjustment: -3.0%**
- CMS finalized a temporary adjustment for CY 2026 only to mitigate financial instability and potential access to care impacts
- This is designed to reduce the burden of the permanent adjustment in a single year
- Sunset scheduled for 2027 unless extended by CMS

### E. Why the Final Rule is Less Severe Than Proposed

The original June 2025 proposed rule included a 6.4% payment reduction. CMS substantially reduced this cut in response to:
1. **Industry Advocacy:** Over 950,000 public comments expressing concerns about agency viability
2. **Access to Care Issues:** Potential provider exits and service reductions
3. **Methodological Reconsideration:** CMS reconsidered how to calculate the permanent adjustment based on actual PDGM performance data
4. **Policy Objectives:** CMS sought to balance payment accuracy with beneficiary access and agency sustainability

---

## II. OASIS-E2 DATA COLLECTION CHANGES — EFFECTIVE APRIL 1, 2026

### A. Overview

The OASIS-E2 data set represents an "off-cycle" release of the OASIS instruments, effective April 1, 2026. All assessments with a completion date on or after April 1, 2026, must use the E2 version. This is a mandatory transition with no grace period.

### B. Items Removed from OASIS

**COVID-19 Vaccination Item (O0350) - REMOVED**
- Item: "Patient's COVID-19 Vaccination is Up to Date"
- Removal Effective: April 1, 2026
- Reason: No longer required for quality reporting; burden reduction
- Clinical Impact: One fewer assessment item to document at discharge/transfer/SOC

**Four Assessment Items Removed from Standard Patient Assessment:**
1. **One Living Situation Item** – Specific OASIS item to be confirmed in E2 guidance
2. **Two Food Items** – Removes redundant nutritional status assessment elements
3. **One Utilities Item** – Reduces environmental assessment documentation burden

**Total Items Removed: 5**

**Rationale:** CMS determined these items were either redundant, burdensome, or no longer clinically useful for quality measurement or care planning.

### C. Items Modified or Replaced

**M0069 (Gender) → A0810 (Sex)**
- Change: Terminology shift from "Gender" to "Sex"
- Response Options: Updated to align with current standards
- Effective: April 1, 2026
- Clinical Impact: Minimal; primarily a terminology update

**A1250 (Transportation) — Updated Response Options**
- Previous Item: M0160 (Transportation)
- New Item: A1250 (Transportation for medical services)
- Change: Slight variation in available response options
- Effective: April 1, 2026
- Clinical Impact: Clinicians must select from updated response set

### D. Items Added to OASIS-E2

**Sensory Assessment Items (added at Resumption of Care timepoint):**
1. **Hearing Assessment Item** – New OASIS item to assess hearing status at ROC
2. **Vision Assessment Item** – New OASIS item to assess vision status at ROC
3. **Language Assessment Item** – New OASIS item to assess ability to communicate/understand

**Functional Assessment Items (new measures effective with quality reporting):**
1. **Improvement in Bathing** – OASIS item supporting new quality measure
2. **Improvement in Upper Body Dressing** – OASIS item supporting new quality measure
3. **Improvement in Lower Body Dressing** – OASIS item supporting new quality measure

**Total Items Added: 6 new data elements**

### E. All-Payer OASIS Collection Requirement

**Effective: July 1, 2025 (already in effect)**
- OASIS data collection is now mandatory for **ALL home health patients**, not just Medicare beneficiaries
- Applies to patients receiving skilled nursing or therapy services, regardless of payer source
- Medicaid, private pay, and other insurance patients now trigger OASIS documentation requirements
- Significantly expands documentation burden for agencies

---

## III. NEW AND MODIFIED QUALITY MEASURES

### A. Removal of COVID-19 Vaccine Measure

**Measure:** "Percentage of Patients Who Are Up to Date with COVID-19 Vaccination"
- Removal Effective: CY 2026 HH Quality Reporting Program (QRP)
- Associated OASIS Item: O0350 (removed as noted above)
- Impact: Reduces required quality measure documentation and reporting burden
- Clinical Documentation: Agencies no longer need to assess or document COVID-19 vaccination status for quality reporting

### B. Removal of HHCAHPS-Related Measures (HHVBP Only)

Three of five HHCAHPS-related measures are being removed from the HHVBP model:
- Removal of three HHCAHPS measures
- Only two HHCAHPS-related measures remain
- Reason: Broader updates to the HHCAHPS survey instrument
- Impact: 18% reduction in Total Performance Score allocation (HHVBP)

### C. Addition of New Quality Measures

**Three OASIS-Based Outcome Measures:**
1. **Improvement in Bathing** (M1810 equivalent)
   - Measure: Percentage of home health episodes with improvement in bathing function
   - Data Source: OASIS assessment at start of care vs. discharge/transfer
   - Quality Reporting: Included in CY 2026 HH QRP

2. **Improvement in Upper Body Dressing** (M1820 equivalent)
   - Measure: Percentage of home health episodes with improvement in upper body dressing
   - Data Source: OASIS assessment at start of care vs. discharge/transfer
   - Quality Reporting: Included in CY 2026 HH QRP

3. **Improvement in Lower Body Dressing** (M1830 equivalent)
   - Measure: Percentage of home health episodes with improvement in lower body dressing
   - Data Source: OASIS assessment at start of care vs. discharge/transfer
   - Quality Reporting: Included in CY 2026 HH QRP

**One Claims-Based Outcome Measure:**
1. **Medicare Spending Per Beneficiary for Post-Acute Care (MSPB-PAC)**
   - Measure: Total Medicare spending per beneficiary for post-acute episodes
   - Data Source: CMS claims data (not agency-reported)
   - Quality Reporting: Included in CY 2026 HH QRP
   - Clinical Impact: Minimal direct documentation requirement; calculated by CMS

### D. Quality Measure Summary

| Measure | Type | Change | Effective |
|---------|------|--------|-----------|
| COVID-19 Vaccination | OASIS-based | REMOVED | CY 2026 |
| Bathing Improvement | OASIS-based | ADDED | CY 2026 |
| Upper Body Dressing | OASIS-based | ADDED | CY 2026 |
| Lower Body Dressing | OASIS-based | ADDED | CY 2026 |
| MSPB-PAC | Claims-based | ADDED | CY 2026 |
| Three HHCAHPS Measures | HHCAHPS | REMOVED (HHVBP only) | CY 2026 |

---

## IV. PATIENT-DRIVEN GROUPINGS MODEL (PDGM) AND CASE-MIX UPDATES

### A. Case-Mix Weight Recalibration

CMS recalibrated case-mix weights using updated 2024 PDGM behavior data to:
- Adjust weights based on actual utilization patterns (vs. predictions)
- Account for provider behavior changes over the past 4 years of PDGM implementation
- Align payment more accurately with resource consumption

**Impact:** Payment for specific PDGM groups may increase or decrease based on recalibrated weights. Agencies with high-utilization case-mix will experience different payment impacts than low-utilization agencies.

### B. Functional Impairment Level (FIL) Updates

CMS updated the functional impairment levels within PDGM groupings:
- Reflects actual functional status distributions across home health population
- May affect assignment of patients to specific PDGM groups
- Impacts episode payment amounts

### C. Comorbidity Subgroup Updates

CMS recalibrated comorbidity subgroups to reflect:
- Current prevalence of comorbidities in home health population
- Updated payment accuracy based on 2024 data
- Changes in clinical complexity distribution

### D. Low-Utilization Payment Adjustment (LUPA) Thresholds

CMS updated LUPA thresholds for CY 2026:
- LUPA thresholds determine when episodes receive fixed rates vs. PDGM rates
- Updated thresholds reflect current utilization patterns
- Impact varies by PDGM group and service type

**Impact:** Some episodes that were previously LUPA in 2025 may no longer qualify, or vice versa, affecting payment methodology.

---

## V. HOME HEALTH VALUE-BASED PURCHASING (HHVBP) UPDATES

### A. Overview

CY 2026 is the fourth performance year of the expanded HHVBP Model. Performance in CY 2026 determines payment adjustments for CY 2028 claims.

### B. Measure Set Changes

**Removal of HHCAHPS Measures:**
- Three of five HHCAHPS measures eliminated
- Two HHCAHPS measures remain
- Reason: Broader HHCAHPS survey updates from CMS
- Impact: 18% reduction in Total Performance Score allocation

**Addition of New Measures:**
- Four new measures added (three OASIS-based + one claims-based)
- Recalibration of all component weights required
- New weights reflect 40% OASIS, reduced HHCAHPS percentage

### C. Total Performance Score Recalculation

**Impact of Measure Changes:**
- Removal of 18% of scoring (three HHCAHPS measures)
- Addition of new bathing/dressing measures increases OASIS weighting to 40%
- All other component weights adjusted proportionally
- Agencies must ensure accurate documentation of new functional measures

### D. Performance Year Timing

- **CY 2026 = Performance Year (PY) 4**
- Agencies' CY 2026 performance data → Analyzed and scored in 2027
- Performance assessment → Applies to CY 2028 claims
- 2-year lag between performance and payment adjustment

---

## VI. FACE-TO-FACE ENCOUNTER REQUIREMENTS

### A. Expanded Practitioner Authority

The final rule clarifies and potentially expands who can document the required face-to-face encounter:
- Physician (MD, DO) — certifying or non-certifying
- Nurse practitioner (NP)
- Physician assistant (PA)
- Clinical nurse specialist (CNS)

**Impact:** Agencies have more flexibility in who can perform/document the required face-to-face encounter for homebound status documentation.

### B. Documentation Requirements

- Face-to-face encounter must support home-bound determination
- Must be documented in patient record
- Required within specified timeframe prior to claim submission
- Applies to Medicare and Medicare Advantage claims

---

## VII. WHAT HOME HEALTH AGENCIES MUST DO

### A. Immediate Actions (By April 1, 2026)

1. **Implement OASIS-E2 Data Collection**
   - Update all assessment forms and templates
   - Train all clinical staff on new/modified items
   - Remove COVID-19 vaccination assessment
   - Remove four deprecated assessment items
   - Add new sensory and functional assessment items
   - Verify system/software updates support E2

2. **Update Documentation Workflows**
   - Ensure electronic or paper assessment forms use OASIS-E2
   - Implement new item requirements in clinical practice
   - Establish quality review processes for OASIS-E2 compliance

3. **Staff Training**
   - Conduct comprehensive training on OASIS-E2 changes
   - Provide specific guidance on new sensory assessment items
   - Update assessment protocols in job aids/checklists

### B. Short-Term Actions (By June 30, 2026)

1. **Quality Measure Implementation**
   - Establish data capture process for new bathing/dressing outcome measures
   - Update quality reporting systems to calculate new measures
   - Monitor compliance with measure documentation requirements

2. **Financial Analysis**
   - Analyze impact of 1.3% payment reduction by PDGM group
   - Identify high-risk case-mix groups with largest payment decreases
   - Model financial projections under updated case-mix weights

3. **Compliance Review**
   - Audit OASIS-E2 documentation accuracy
   - Review assessment completion rates for new items
   - Identify and remediate documentation gaps

### C. Long-Term Actions (Ongoing)

1. **HHVBP Performance Optimization**
   - Establish baseline performance on new bathing/dressing measures
   - Implement care protocols to maximize functional improvement
   - Monitor MSPB-PAC spending trajectory
   - Prepare for CY 2028 payment adjustments based on CY 2026 performance

2. **Budget Management**
   - Implement cost control measures to offset 1.3% payment reduction
   - Optimize PDGM assignments to maximize payment
   - Monitor LUPA threshold changes and manage utilization accordingly

3. **Regulatory Monitoring**
   - Remain alert for any CMS guidance updates on OASIS-E2 implementation
   - Monitor for proposed changes to CY 2027 HH PPS rule
   - Track OIG audit focus areas related to home health

---

## VIII. ENZO PRODUCT ROADMAP IMPLICATIONS

### A. Scribe (Ambient Clinical Documentation)

**Priority: CRITICAL - Immediate Implementation Required**

**OASIS-E2 Updates:**
- [ ] Remove COVID-19 vaccination assessment item from all templates
- [ ] Remove deprecated items: Living Situation, Food (2 items), Utilities
- [ ] Add sensory assessment items: Hearing, Vision, Language (for ROC)
- [ ] Replace M0069 (Gender) with A0810 (Sex)
- [ ] Update A1250 (Transportation) response options
- [ ] Validate all OASIS-E2 item mappings in documentation templates
- [ ] Update voice/dictation prompts to reflect E2 terminology

**Quality Measure Support:**
- [ ] Ensure bathing functional status capture (M1810 equivalent)
- [ ] Ensure upper body dressing documentation (M1820 equivalent)
- [ ] Ensure lower body dressing documentation (M1830 equivalent)
- [ ] Implement logic to ensure functional assessment at both SOC and discharge

**Documentation Optimization:**
- [ ] Review Scribe prompts for alignment with new assessment items
- [ ] Optimize language to support clinician burden reduction
- [ ] Implement quality checks to ensure all required items documented
- [ ] Create Scribe templates for new sensory assessment items

**Testing & Deployment:**
- [ ] Complete E2 regression testing
- [ ] Beta test with pilot agencies
- [ ] Deploy by March 20, 2026 (11 days before April 1 deadline)
- [ ] Provide training resources to customers

### B. Intake (Initial Assessment / Care Planning)

**Priority: HIGH - Implementation by April 1, 2026**

**Assessment Form Updates:**
- [ ] Update initial assessment forms to reflect OASIS-E2 changes
- [ ] Remove deprecated items from data capture workflows
- [ ] Add new sensory and functional assessment fields
- [ ] Implement data validation for required E2 items
- [ ] Ensure all required fields are marked and cannot be skipped

**PDGM Grouping Impact:**
- [ ] Verify PDGM grouping logic reflects updated case-mix methodology
- [ ] Review comorbidity subgroup mapping
- [ ] Test LUPA threshold determination with new parameters
- [ ] Monitor for any changes to grouping algorithm

**Care Plan Alignment:**
- [ ] Ensure care plans address new functional outcome measures (bathing, dressing)
- [ ] Implement protocols to support functional improvement
- [ ] Align initial goals with OASIS data capture

**Testing & Deployment:**
- [ ] Test OASIS-E2 data capture end-to-end
- [ ] Validate PDGM assignment with new weights
- [ ] Deploy by March 20, 2026
- [ ] Train customer support team on E2 form updates

### C. Scheduling

**Priority: MEDIUM - Monitoring & Coordination**

**Assessment Scheduling:**
- [ ] Ensure comprehensive assessments capture new bathing/dressing measures at both SOC and discharge
- [ ] Monitor for assessment scheduling gaps that might impact functional measure capture
- [ ] Coordinate with Scribe/Intake to ensure proper timepoint documentation

**Utilization Management:**
- [ ] Monitor episode-level utilization relative to updated LUPA thresholds
- [ ] Identify any scheduling patterns that might trigger adverse payment impacts
- [ ] Alert agencies to potential PDGM group changes based on case-mix updates

**Compliance Monitoring:**
- [ ] Track assessment completion rates post-April 1 to monitor E2 adoption
- [ ] Flag any episodes missing required OASIS-E2 items
- [ ] Coordinate with QAPI on documentation compliance

### D. QAPI (Quality Assurance / Performance Improvement)

**Priority: CRITICAL - Comprehensive Monitoring Required**

**Quality Measure Updates:**
- [ ] Remove COVID-19 vaccination measure from all quality dashboards
- [ ] Add new bathing improvement measure calculation
- [ ] Add new upper body dressing improvement measure calculation
- [ ] Add new lower body dressing improvement measure calculation
- [ ] Add MSPB-PAC spending per beneficiary tracking
- [ ] Recalibrate all benchmarks for new measure set

**HHVBP Performance Tracking (CY 2026 → CY 2028 Payment Impact):**
- [ ] Establish baseline performance on new functional measures
- [ ] Update Total Performance Score calculation to reflect removed HHCAHPS measures
- [ ] Recalibrate component weights based on new measure allocation
- [ ] Monitor functional improvement outcomes (bathing, dressing)
- [ ] Track spending per beneficiary trajectory

**Documentation Compliance Audits:**
- [ ] Implement audit protocols for OASIS-E2 compliance
- [ ] Establish performance metrics for new item completion rates
- [ ] Monitor sensory assessment documentation accuracy
- [ ] Audit functional status assessment at SOC vs. discharge for measure validity

**Financial Impact Analysis:**
- [ ] Calculate agency-level impact of 1.3% payment reduction
- [ ] Analyze by PDGM group and case-mix composition
- [ ] Model financial projections for 2026
- [ ] Identify high-risk patient populations with largest payment impact

**OIG Audit Preparedness:**
- [ ] Develop proactive audit readiness protocols
- [ ] Establish documentation accuracy monitoring
- [ ] Review medical necessity determination processes
- [ ] Implement compliance tracking for face-to-face requirements
- [ ] Create audit trail for OASIS-E2 assessment completion

---

## IX. TIMELINE & CRITICAL DATES

| Date | Event | Impact |
|------|-------|--------|
| 1/1/2026 | CY 2026 HH PPS rates effective | -1.3% payment reduction in effect |
| 3/20/2026 | RECOMMENDED: Software updates deployed | Agencies can test before deadline |
| 4/1/2026 | OASIS-E2 mandatory implementation | All assessments after 4/1 must use E2 |
| 4/1/2026 | New quality measures effective | New bathing/dressing measures in effect |
| 7/1/2026 | All-payer OASIS collection in effect | Already in effect since 7/1/2025 |
| 12/31/2026 | CY 2026 performance year ends | Marks end of data collection for 2026 |
| 2027 | Performance scoring & analysis | CY 2026 data analyzed for HHVBP |
| 2028 | HHVBP payment adjustments apply | CY 2026 performance → CY 2028 payment |

---

## X. SUMMARY OF CHANGES BY PRODUCT

### Scribe
- **OASIS-E2 integration** (remove 5 items, add 6 items, modify terminology)
- **New functional assessment support** (bathing, dressing)
- **Documentation optimization** for new measures

### Intake
- **Assessment form updates** (OASIS-E2 items)
- **Data validation** for new required items
- **PDGM grouping logic verification** (new case-mix weights)

### Scheduling
- **Monitoring & coordination** for OASIS-E2 compliance
- **Utilization tracking** relative to updated LUPA thresholds
- **Assessment scheduling** for new measures

### QAPI
- **Quality measure recalculation** (new measures, removed measures)
- **HHVBP performance tracking** (recalibrated weights, new measures)
- **Documentation compliance monitoring** (OASIS-E2 accuracy)
- **Financial impact analysis** (1.3% reduction by PDGM group)

---

## Conclusion

The CY 2026 Home Health Prospective Payment System Final Rule represents a moderate financial reduction (1.3% vs. proposed 6.4%) paired with significant operational and data collection changes. The most time-sensitive requirement is OASIS-E2 implementation by April 1, 2026, which requires immediate action from all home health agencies and their software vendors.

The new quality measures and HHVBP recalibration create opportunities for agencies to demonstrate value through functional outcome improvements, but require accurate documentation and robust QAPI processes to track performance over the 2-year lag to payment adjustment.

Enzo Health products must be updated to support these changes comprehensively, with Scribe, Intake, and QAPI requiring most significant modifications to maintain compliance and functionality.

---

**Sources:**
- [CMS CY 2026 Home Health Prospective Payment System Final Rule](https://www.cms.gov/newsroom/fact-sheets/calendar-year-cy-2026-home-health-prospective-payment-system-final-rule-cms-1828-f)
- [Federal Register - CY 2026 HH PPS Final Rule](https://www.federalregister.gov/documents/2025/12/02/2025-21767/medicare-and-medicaid-programs-calendar-year-2026-home-health-prospective-payment-system-hh-pps-rate)
- [CMS OASIS Data Sets](https://www.cms.gov/medicare/quality/home-health/oasis-data-sets)
- [CMS Expanded HHVBP Model](https://www.cms.gov/priorities/innovation/innovation-models/expanded-home-health-value-based-purchasing-model)
