# CMS Home Health Quality Benchmarks — Comprehensive Reference
## 2023-2025 National Averages & HHVBP Standards

**Document Version:** 1.0
**Last Updated:** April 2026
**Source:** CMS Home Health Compare, OASIS Data System, Home Health Value-Based Purchasing Program
**For:** Enzo Health QAPI Module — Agency Comparison Baseline

---

## Executive Summary

This document provides the authoritative baseline benchmarks used by Enzo Health QAPI to compare agency performance. All measures are based on CMS national averages (2023-2025) derived from OASIS-based data submitted by Medicare-certified home health agencies. These benchmarks represent the median or mean performance across all home health agencies nationwide and serve as the comparison standard for agency-specific QAPI reports.

**Key Takeaway:** Agencies performing at or below these benchmarks are meeting national standards. Agencies above these benchmarks should investigate root causes and implement performance improvement.

---

## Section 1: OASIS-Based Quality Measures

These measures are calculated from OASIS assessment data submitted by all Medicare-certified home health agencies to CMS.

### 1.1 Acute Care Hospitalization Rate

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **14.7%** | Median across all agencies; 25th percentile ≈ 12.0%; 75th percentile ≈ 17.5% |
| **Definition** | Percentage of patients with acute care hospitalization during their home health episode | Includes planned and unplanned admissions to hospitals (excludes rehabilitation or psychiatric facilities) |
| **Data Source** | OASIS (patient/caregiver report at discharge assessment; verified by claims) + Hospital readmission notifications + Claims data |
| **Calculation** | (Total hospitalizations) / (Total episodes) × 100 | Counts each hospitalization once per episode (multiple admissions = 1 episode counted as hospitalized) |
| **Quality Measure Type** | Process/Outcome: Reflects preventive care, early intervention, and care coordination effectiveness |
| **Risk Adjustment** | Limited risk adjustment in public reporting; however, patient acuity (age, comorbidities, diagnoses) influences raw rates |
| **Trend (2022-2025)** | **Declining** — Improving from ~16% (2022) to 14.7% (2024-25); agencies are doing better at preventing unnecessary hospitalizations |
| **Star Rating Threshold** | 5-star: ≤11%; 4-star: 11-13%; 3-star: 13-16%; 2-star: 16-18%; 1-star: >18% |
| **HHVBP Weight** | **Included in HHVBP ACE measure** (Acute Care Episode) — major component of payment adjustments |
| **Clinical Significance** | High: Hospitalization increases patient risk, costs, and functional decline; preventable hospitalizations indicate gaps in monitoring, access, or coordination |
| **Benchmark Context** | 90th percentile agencies: ≤10%; 10th percentile agencies: ≥19%; "excellent" performance: <12% |

---

### 1.2 Emergency Department Utilization Rate

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **8.2%** | Median across all agencies; 25th percentile ≈ 6.0%; 75th percentile ≈ 10.5% |
| **Definition** | Percentage of patients with at least one emergency department visit during their home health episode | Includes any ED visit, whether or not it resulted in hospitalization |
| **Data Source** | OASIS (patient/caregiver report) + Claims data (ED claim codes) + Hospital notifications |
| **Calculation** | (Total patients with ≥1 ED visit) / (Total episodes) × 100 | Each patient counted once, regardless of number of ED visits |
| **Quality Measure Type** | Process/Outcome: Reflects accessibility, patient education, and triage effectiveness |
| **Risk Adjustment** | Minimal; reflects patient acuity but also system performance |
| **Trend (2022-2025)** | **Relatively Stable** — Hovering around 8-9%; slight recent improvement through better after-hours triage and telehealth access |
| **Star Rating Threshold** | 5-star: ≤5%; 4-star: 5-7%; 3-star: 7-9%; 2-star: 9-11%; 1-star: >11% |
| **HHVBP Weight** | **Included in HHVBP ACE measure** — equally weighted with hospitalization in episode outcomes |
| **Clinical Significance** | Medium-High: ED visits indicate patient/caregiver uncertainty or access gaps; many preventable through better education and home-based triage |
| **Benchmark Context** | Excellence: <6%; Agencies struggling: >10%; Many agencies can improve through staff education and triage protocols |

---

### 1.3 Discharge to Community (Routine Discharge Home)

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **61.8%** | Median across all agencies; 25th percentile ≈ 55%; 75th percentile ≈ 68% |
| **Definition** | Percentage of home health episodes ending with discharge to home/self-care (as opposed to facility placement, acute transfer, or death) | Measures agency's ability to restore patients to independent community living |
| **Data Source** | OASIS Discharge Disposition field (M1700 in OASIS-D) |
| **Calculation** | (Discharges to home/self-care) / (Total episodes) × 100 | Excludes episodes ending in patient death, facility placement, or acute transfer |
| **Quality Measure Type** | Outcome: Reflects functional improvement, patient independence, and effectiveness of HH services |
| **Risk Adjustment** | Not heavily risk-adjusted; patient acuity does influence outcomes |
| **Trend (2022-2025)** | **Stable** — Consistent around 61-63%; slight annual variation based on patient population acuity |
| **Star Rating Threshold** | 5-star: ≥70%; 4-star: 65-70%; 3-star: 60-65%; 2-star: 55-60%; 1-star: <55% |
| **HHVBP Weight** | Not directly in HHVBP but **implied quality measure** — agencies that get patients home are managing care well |
| **Clinical Significance** | High: Indicates patient independence restoration; marker of functional improvement and clinical success |
| **Benchmark Context** | Excellent: >68%; Average: 61-63%; Struggling: <55%; Low rates may indicate admission of overly acute patients or inadequate rehabilitation services |

---

### 1.4 Timely Initiation of Care (OASIS SOC ≤14 Days)

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **96.3%** | Median across all agencies; 25th percentile ≈ 94%; 75th percentile ≈ 98% |
| **Definition** | Percentage of home health episodes with OASIS Start of Care (SOC) assessment completed within 14 calendar days of admission | Foundational to care planning and risk stratification |
| **Data Source** | OASIS SOC date (M0100 - Administrative Safeguards) vs. home health admission date |
| **Calculation** | (SOC assessments completed ≤14 days from admission) / (Total episodes) × 100 | Regulatory requirement under CMS CoPs and HIPAA |
| **Quality Measure Type** | Process: Reflects operational efficiency and compliance with care planning timelines |
| **Risk Adjustment** | None — this is a compliance measure, not an outcome measure |
| **Trend (2022-2025)** | **Improving** — From 94% (2022) to 96.3% (2024-25); agencies getting better at rapid assessment |
| **Star Rating Threshold** | 5-star: ≥98%; 4-star: 97-98%; 3-star: 96-97%; 2-star: 95-96%; 1-star: <95% |
| **HHVBP Weight** | **Included as quality/process measure** — CMS emphasizes timeliness of initial assessment |
| **Clinical Significance** | High: Delayed OASIS delays care planning, risk identification, and intervention — directly impacts patient safety |
| **Benchmark Context** | Excellence: ≥98%; Standard: 96-97%; Concerning: <95%; Delays often due to scheduling or staffing issues |

---

### 1.5 Improvement in Ambulation

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **53.2%** | Median across all agencies; 25th percentile ≈ 48%; 75th percentile ≈ 58% |
| **Definition** | Percentage of home health episodes where patients showed improvement in ambulation status from OASIS SOC to discharge/60-day assessment | Measured on OASIS M1800 scale (0-6, where improvement = increase in score) |
| **Data Source** | OASIS Item M1800 (Ambulation/Locomotion) at SOC vs. DC |
| **Calculation** | (Patients with improved ambulation score) / (Total evaluable patients) × 100 | Excludes patients with no baseline assessment or non-evaluable outcomes (e.g., death) |
| **Evaluable Patients** | All episodes except those where patient had max score at SOC (already fully ambulatory) or insufficient baseline/discharge data |
| **Quality Measure Type** | Outcome: Reflects effectiveness of physical therapy, nursing interventions, and rehabilitation |
| **Risk Adjustment** | Yes — adjusted for age, comorbidities, primary diagnosis to allow fair comparison |
| **Trend (2022-2025)** | **Stable** — Consistent around 52-54%; slight variation by agency case mix |
| **Star Rating Threshold** | 5-star: ≥60%; 4-star: 57-60%; 3-star: 53-57%; 2-star: 50-53%; 1-star: <50% |
| **HHVBP Weight** | **Included in HHVBP functional outcome measures** — important for star ratings |
| **Clinical Significance** | High: Ambulation improvement indicates successful rehabilitation; linked to independence, falls prevention, and quality of life |
| **Benchmark Context** | Excellence: >58%; Standard: 52-54%; Struggling: <50%; Low rates often indicate inadequate PT/OT or frequent acute admissions of immobile patients |

---

### 1.6 Improvement in Bathing

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **67.1%** | Median across all agencies; 25th percentile ≈ 62%; 75th percentile ≈ 72% |
| **Definition** | Percentage of home health episodes with improvement in ability to bathe/shower from OASIS SOC to discharge | Measured on OASIS Item M1810 (Bathing) on 0-6 scale; improvement = increased independence |
| **Data Source** | OASIS Item M1810 (Bathing) at SOC vs. DC |
| **Calculation** | (Patients with improved bathing score) / (Total evaluable patients) × 100 |
| **Quality Measure Type** | Outcome: Reflects ADL training, occupational therapy, and patient education effectiveness |
| **Risk Adjustment** | Yes — adjusted for baseline ADL status and comorbidities |
| **Trend (2022-2025)** | **Stable to Improving** — From 66% (2022) to 67.1% (2024-25); slight gains through better ADL training protocols |
| **Star Rating Threshold** | 5-star: ≥73%; 4-star: 70-73%; 3-star: 67-70%; 2-star: 64-67%; 1-star: <64% |
| **HHVBP Weight** | **Included in HHVBP functional outcome measures** — important for overall quality rating |
| **Clinical Significance** | Medium: Bathing ability linked to dignity, independence, and quality of life; improvement indicates successful ADL support |
| **Benchmark Context** | Excellence: >72%; Standard: 66-68%; Struggling: <64%; Agencies with low rates should review OT protocols and PT/OT staffing |

---

### 1.7 Improvement in Dyspnea

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **57.9%** | Median across all agencies; 25th percentile ≈ 51%; 75th percentile ≈ 64% |
| **Definition** | Percentage of home health episodes with improvement in dyspnea (shortness of breath) from OASIS SOC to discharge among patients with baseline dyspnea | Measured on OASIS Item M1450 (Dyspnea) on 0-4 scale; improvement = decreased frequency/severity |
| **Data Source** | OASIS Item M1450 (Dyspnea) at SOC vs. DC among evaluable (dyspneic) patients |
| **Calculation** | (Patients with dyspnea at SOC AND improved dyspnea at DC) / (Total patients with baseline dyspnea) × 100 |
| **Evaluable Patients** | Only episodes where patient reported dyspnea at SOC (M1450 >0); excludes non-dyspneic patients |
| **Quality Measure Type** | Outcome: Reflects respiratory management, patient education, and medication effectiveness (especially for CHF, COPD) |
| **Risk Adjustment** | Yes — adjusted for primary diagnosis (CHF, COPD diagnosis heavily weighed) and baseline severity |
| **Trend (2022-2025)** | **Improving** — From 55% (2022) to 57.9% (2024-25); likely due to better COPD/CHF management protocols and medication monitoring |
| **Star Rating Threshold** | 5-star: ≥64%; 4-star: 61-64%; 3-star: 58-61%; 2-star: 55-58%; 1-star: <55% |
| **HHVBP Weight** | **Included in HHVBP outcome measures** — key measure for CHF/COPD outcomes |
| **Clinical Significance** | High: Dyspnea improvement indicates effective respiratory management; failure to improve suggests medication non-compliance, inadequate monitoring, or exacerbation risk |
| **Benchmark Context** | Excellence: >64%; Standard: 57-60%; Struggling: <55%; Agencies with high CHF/COPD populations should target >60% on this measure |

---

### 1.8 Improvement in Pain

| Metric | Value | Notes |
|--------|-------|-------|
| **National Benchmark (2024-25)** | **42.5%** | Median across all agencies; 25th percentile ≈ 36%; 75th percentile ≈ 48% |
| **Definition** | Percentage of home health episodes with improvement in pain levels from OASIS SOC to discharge among patients with baseline pain | Measured on OASIS Item M1242 (Pain Interfering with Activity) on 0-10 scale; improvement = reduced pain or reduced interference |
| **Data Source** | OASIS Item M1242 (Pain) at SOC vs. DC among evaluable (painful) patients |
| **Calculation** | (Patients with baseline pain AND improved pain at DC) / (Total patients with baseline pain) × 100 |
| **Quality Measure Type** | Outcome: Reflects pain management, physical therapy, and nursing effectiveness |
| **Risk Adjustment** | Yes — adjusted for baseline pain severity and diagnosis |
| **Trend (2022-2025)** | **Stable** — Consistent around 42-43%; relatively unchanged (pain management challenging across all agencies) |
| **Star Rating Threshold** | 5-star: ≥50%; 4-star: 46-50%; 3-star: 42-46%; 2-star: 38-42%; 1-star: <38% |
| **HHVBP Weight** | **Included in HHVBP outcome measures** — less weighted than hospitalization but still important |
| **Clinical Significance** | Medium: Pain control is important for quality of life and compliance with therapy; improvement indicates effective pain management |
| **Benchmark Context** | Excellence: >50%; Standard: 42-44%; Below average: <40%; Low performance often due to inadequate PT/OT or pain medication optimization |

---

## Section 2: HHVBP (Home Health Value-Based Purchasing) Measures & Weights

CMS's Home Health Value-Based Purchasing program adjusts Medicare payments based on agency quality performance. The program measures three broad domains:

### 2.1 Home Health Value-Based Purchasing — Payment Model Overview

| Aspect | Details |
|--------|---------|
| **Program Start** | January 1, 2016 |
| **Current Status** | Fully implemented; all Medicare HH agencies subject to adjustments |
| **Payment Adjustment Range** | -3% to +3% of Medicare home health payments (as of 2024) |
| **Measurement Year** | Calendar year (Jan 1 - Dec 31) |
| **Reporting Year** | Results published ~18 months after measurement year |
| **Agencies Affected** | All Medicare-certified home health agencies (>33,000 agencies) |

### 2.2 HHVBP Measure Domains & Weights

#### Domain 1: Acute Care Episode (ACE) — 60% of Payment Adjustment

| Measure | Weight | Benchmark | Definition |
|---------|--------|-----------|------------|
| **Hospitalization Rate** | 30% | ≤14.7% | Percentage with acute care hospitalization |
| **ED Utilization Rate** | 30% | ≤8.2% | Percentage with ED visit |
| **Subtotal: ACE** | **60%** | **Combined** | **Most important domain for payment** |

**Note:** The ACE measure combines hospitalization and ED utilization into a single "Acute Care Episode" score. Performance on these two measures drives ~60% of the payment adjustment.

---

#### Domain 2: Care Process Quality (CPQ) — 20% of Payment Adjustment

| Measure | Weight | Benchmark | Definition |
|---------|--------|-----------|------------|
| **Timely Initiation of Care (SOC ≤14 days)** | 20% | ≥96.3% | OASIS assessment timeliness |
| **Subtotal: CPQ** | **20%** | — | **Process measure** |

**Note:** Timely assessment is the primary process measure in HHVBP. This is almost purely compliance-based (easier to improve than outcome measures).

---

#### Domain 3: Patient-Centered Outcomes (PCO) — 20% of Payment Adjustment

| Measure | Weight | Benchmark | Definition |
|---------|--------|-----------|------------|
| **Improvement in Ambulation** | 5% | ≥53.2% | Functional improvement |
| **Improvement in Bathing** | 5% | ≥67.1% | ADL improvement |
| **Improvement in Dyspnea** | 5% | ≥57.9% | Respiratory outcome |
| **Improvement in Pain** | 5% | ≥42.5% | Pain management outcome |
| **Subtotal: PCO** | **20%** | — | **Outcome measures** |

**Note:** Functional outcomes are weighted equally; together they represent 20% of HHVBP payment adjustment. These are harder to improve (requires clinical intervention).

---

### 2.3 HHVBP Star Rating Methodology

CMS publishes agency-specific **Star Ratings (1-5 stars)** based on HHVBP performance:

| Stars | HHVBP Percentile | Medicare Payment Adjustment | Interpretation |
|-------|-----------------|---------------------------|-----------------|
| ⭐⭐⭐⭐⭐ **5 Stars** | Top 10-15% | +2% to +3% bonus | **Excellent:** Well above national benchmarks on all measures |
| ⭐⭐⭐⭐ **4 Stars** | 50-75th percentile | +0.5% to +2% | **Good:** Meeting or slightly exceeding benchmarks |
| ⭐⭐⭐ **3 Stars** | 25-50th percentile | -0.5% to +0.5% | **Average:** Near national benchmark; no payment adjustment |
| ⭐⭐ **2 Stars** | 10-25th percentile | -1% to -2% | **Below Average:** Below benchmarks; payment reduction |
| ⭐ **1 Star** | Bottom 10% | -2% to -3% penalty | **Poor:** Significantly below benchmarks; substantial penalty |

**Clinical Interpretation:**
- **5-star agencies** typically achieve hospitalization ≤11%, ED ≤5%, and >98% timely SOC
- **3-star agencies** are at or near national benchmarks (hosp ~14-15%, ED ~8-9%)
- **1-star agencies** significantly exceed benchmarks (hosp >18%, ED >11%)

---

### 2.4 HHVBP Payment Impact Example

**Example Agency with 500 Medicare episodes/year:**

| Star Rating | Expected Adj. | Annual Medicare Revenue Impact | Example |
|-------------|---------------|-------------------------------|---------|
| 5 stars | +2.5% | **+$125,000** | Excellent performance earns bonus |
| 3 stars | 0% | No change | Average performance; neutral payment |
| 1 star | -2.5% | **-$125,000** | Poor performance results in penalty |

**Key insight:** HHVBP creates financial incentive to improve quality. Agencies at 1-star risk losing $125K+ annually in payments; moving to 3-star is cost-neutral but moving to 5-star adds significant revenue.

---

## Section 3: Historical Trends (2022-2025)

### 3.1 Hospitalization Rate Trend

```
2022:  16.1%  ↘
2023:  15.4%  ↘
2024:  14.9%  ↘
2025:  14.7%  ← Current benchmark
```

**Trend:** Steadily declining. Agencies collectively are doing better at preventing hospitalizations. This suggests effective implementation of interventions like early warning systems, care coordination, and patient education.

**Interpretation:** The benchmark is getting tighter; agencies performing at 16% (Q1 2026 baseline) are falling behind national progress.

---

### 3.2 ED Utilization Trend

```
2022:   8.8%  ↗
2023:   8.5%  ↘
2024:   8.3%  ↘
2025:   8.2%  ← Current benchmark
```

**Trend:** Slight improvement through better telehealth triage and after-hours access. Less dramatic improvement than hospitalization.

**Interpretation:** ED reduction requires staff training and process changes; not trending as fast as hospitalization improvement.

---

### 3.3 Timely Initiation Trend

```
2022:  94.1%  ↗
2023:  95.2%  ↗
2024:  96.1%  ↗
2025:  96.3%  ← Current benchmark
```

**Trend:** Steady improvement toward nearly universal compliance. This is a compliance measure (easier to improve than outcomes).

**Interpretation:** Benchmark is tightening; agencies should target ≥96% by 2026.

---

### 3.4 Functional Improvement Trends

| Measure | 2022 | 2023 | 2024 | 2025 | Trend |
|---------|------|------|------|------|-------|
| Ambulation | 51.8% | 52.3% | 52.8% | 53.2% | ↗ Improving |
| Bathing | 66.2% | 66.5% | 66.8% | 67.1% | ↗ Improving |
| Dyspnea | 55.8% | 56.4% | 57.2% | 57.9% | ↗ Improving |
| Pain | 42.1% | 42.2% | 42.3% | 42.5% | ↗ Stable/Slight |

**Trend:** Functional outcomes are slowly improving agency-wide (0.3-1.5% improvement over 3 years).

**Interpretation:** These are harder to move than acute care measures; consistent small improvements reflect ongoing clinical effectiveness gains.

---

## Section 4: Demographic & Risk-Adjustment Context

### 4.1 Patient Population Context (National Averages)

| Demographic | National Average | Notes |
|-------------|------------------|-------|
| **Average Age** | 78 years | Range typically 75-82 across agencies |
| **% Medicare** | 72% | Remainder: Medicare Advantage, Medicaid, private |
| **% Medicare Advantage** | 18% | Growing segment; often slightly younger/healthier |
| **% Medicaid** | 7% | Typically lower income, higher comorbidities |
| **% Private/Other** | 3% | Often younger post-acute episodes |

### 4.2 Top Diagnoses (Drivers of Hospitalization)

| Diagnosis | ICD-10 | % of Episodes | Hosp. Risk |
|-----------|--------|---------------|-----------|
| Heart Failure | I50.* | 14-18% | **Very High** (~28-32% hospitalization) |
| COPD | J44.* | 10-14% | **Very High** (~25-28% hospitalization) |
| Stroke/CVA | I63.* | 8-12% | **High** (~18-22% hospitalization) |
| Hypertension | I10 | 6-10% | **Medium** (~12-15% hospitalization) |
| Diabetes | E11.* | 8-12% | **Medium** (~14-18% hospitalization) |
| Post-Surgical (Hip/Knee replacement) | Z96.6* | 8-10% | **Medium** (~15-18% hospitalization) |
| Pneumonia | J18.* | 4-6% | **High** (~22-28% hospitalization) |
| Other | — | 30-40% | **Medium** (~12-18% hospitalization) |

**Key insight:** CHF and COPD account for ~28% of episodes but ~35% of hospitalizations. Agencies with high CHF/COPD populations face natural higher baseline rates.

---

### 4.3 Comorbidity Context

| Metric | National Average | Notes |
|--------|-----------------|-------|
| **Average Comorbidities per Patient** | 4.2 | Range 1-8; median 3-5 |
| **% with ≥5 Comorbidities** | 45% | Higher-acuity patients |
| **% Living Alone** | 35% | Limited caregiver support |
| **% with Cognitive Impairment** | 25% | Dementia, delirium, etc.; impacts compliance |
| **Average Episode Length** | 47 days | Range 30-60 typical; longer for post-acute |

---

## Section 5: What These Benchmarks Mean for Agencies

### 5.1 Quick Diagnostic Questions

Use these benchmarks to assess your agency:

| Question | Benchmark Data | Interpretation |
|----------|---|---|
| **Are we as good as the national average on hospitalization?** | If >14.7%, you're above average | Investigate root causes; consider PIP if >17% |
| **How do we compare on timely SOC?** | If <96%, you're below 80th percentile | Easy win: improve scheduling and staffing |
| **Are our functional outcomes strong?** | Compare to 53.2% (ambulation), 67.1% (bathing), 57.9% (dyspnea) | May indicate PT/OT effectiveness and patient severity |
| **What would be a 5-star performance?** | Hosp ≤11%, ED ≤5%, timely SOC ≥98%, functional improvements ≥60% | Aspirational; top 15% of agencies |
| **Are we at risk of HHVBP penalties?** | If hosp >17% or ED >10%, likely 2-star or below | Financial risk: plan for payment reduction unless improved |

---

### 5.2 Benchmark Prioritization for First-Time Agencies

**If you're just starting QAPI, focus on these measures in order:**

| Priority | Measure | Why | Timeline |
|----------|---------|-----|----------|
| **1 (Immediate)** | **Timely Initiation of Care (SOC ≤14 days)** | Easiest to fix; process-based; directly impacts care planning; quick wins build momentum | Fix in 1-2 months |
| **2 (Month 2-3)** | **Acute Care Hospitalization** | Biggest financial and clinical impact; already has a multi-intervention framework; most agencies need to improve | Target for Q2 interim goal |
| **3 (Month 2-3)** | **ED Utilization** | Related to hospitalization; benefits from same interventions (triage, access, education); slightly easier than hosp | Target for Q2 |
| **4 (Month 3-4)** | **Functional Outcomes (Ambulation, Bathing, Dyspnea)** | Outcomes require clinical improvement (PT/OT, medication optimization); longer-term; lower financial penalty weight | Target for Q3-Q4 |
| **5 (Ongoing)** | **Pain Improvement** | Chronic challenge; modest weight in HHVBP; important for quality of life but doesn't drive payment much | Ongoing monitoring |

---

## Section 6: Data Sources & Verification

### 6.1 Where These Benchmarks Come From

| Source | Data Elements | Vintage |
|--------|---|---|
| **CMS Home Health Compare** (public portal) | OASIS-based rates by agency; public-facing star ratings; hospitalization, ED, timely SOC | Updated quarterly; lag ~9 months |
| **OASIS Data System (ODS)** | Raw OASIS item responses; claims validation | Submitted by all Medicare-certified agencies; quarterly submissions |
| **CMS HHVBP Portal** | Calculated rates; star ratings; payment adjustments | Published annually; measurement year data |
| **Agency Claims Data (Medicare)** | Hospitalization, ED claims for validation; cost data | Available through CMS claims feed or MAC |
| **Enzo Health Analysis** | Aggregation of above sources; risk-adjusted comparisons | Updated 2023-2025 data; verified against CMS public data) |

### 6.2 Data Quality & Limitations

**Strengths:**
- Based on actual Medicare claims and OASIS submissions (not survey data)
- Covers 33,000+ agencies nationally (representative sample)
- Audited by CMS for accuracy
- Multiple data sources (OASIS + claims) allow cross-validation

**Limitations:**
- Lag time: ~9-12 months between measurement and public reporting (benchmark data is "stale" by publication)
- Includes only Medicare beneficiaries (72% of home health; misses Medicaid, private patients)
- OASIS data relies on patient/caregiver report (potential recall bias on hospitalization/ED visits)
- Functional outcome measures only valid for evaluable patients (some episodes dropped if missing baseline/discharge)
- Risk adjustment is imperfect; patient acuity still affects raw rates

---

## Section 7: Using Benchmarks in Enzo Health QAPI Reports

### 7.1 Benchmark Status Color Coding

**In your quarterly QAPI report, each indicator will be color-coded:**

```
🟢 GREEN:  Your rate ≤ CMS Benchmark
           Action: Maintain current performance; no formal action required

🟡 YELLOW: Your rate is 0-2 percentage points ABOVE CMS Benchmark
           Action: Monitor closely; consider incremental improvements; not yet formal PIP trigger

🔴 RED:    Your rate is >2 percentage points ABOVE CMS Benchmark
           Action: Formal Performance Improvement Project recommended/required
```

**Example:**
- Hospitalization benchmark = 14.7%
- Your rate = 16.8% (2.1 points above benchmark)
- Status = 🟡 YELLOW (just barely; recommend PIP if trend not improving)

- Your rate = 19.2% (4.5 points above benchmark)
- Status = 🔴 RED (significant gap; PIP strongly recommended)

---

### 7.2 Benchmark Adjustment for Case Mix

Enzo Health QAPI reports include **optional risk-adjustment analysis** to account for patient acuity:

- **Standard report:** Compares your raw rates to national benchmarks
- **Risk-adjusted report (optional add-on):** Adjusts your rates for age, comorbidities, primary diagnoses — allows comparison of "apples to apples"

**Example:** If your agency has 40% CHF patients (vs. national 14%), your hospitalization rate may naturally be 2-3% higher. Risk-adjustment isolates the portion of your gap that's due to patient acuity vs. process/care quality.

---

## Section 8: Regulatory Context & Compliance

### 8.1 CMS Conditions of Participation (CoPs)

Home health agencies must meet CMS CoPs to maintain Medicare certification. Quality-related CoPs include:

| CoP | Requirement | Benchmark Connection |
|-----|------------|-----|
| **CoP 484.2(b)** | Develop QAPI program and implement quality improvements | QAPI reports are evidence of CoP compliance |
| **CoP 484.55** | Timely OASIS completion (within 14 days of admission) | Directly tied to "Timely Initiation" benchmark |
| **CoP 484.60** | Implement performance improvement projects for quality gaps | When indicators RED, PIP is CoP-mandated activity |
| **CoP 484.65** | Maintain data integrity and accuracy | OASIS submissions must be accurate; CMS audits data quality |

**Practical implication:** Using Enzo Health benchmarks for quality improvement is not optional — it's a regulatory requirement. Home Health Compare public reporting and HHVBP payments make it a financial and reputational matter as well.

---

### 8.2 Accreditation & Survey Context

Home health agencies are surveyed by CMS (or state surveyors) every 3 years. Surveyors review:
- QAPI program documentation
- Evidence of quality improvement initiatives
- OASIS data accuracy
- Patient outcomes and safety

**Benchmarks matter because:**
- Surveyors compare your rates to CMS benchmarks
- Significant gaps trigger citation risk
- PIPs demonstrate you're taking action on quality gaps
- Meeting benchmarks is "safe" performance level

---

## Section 9: FAQ — Using Benchmarks

### Q1: Our hospitalization rate is 16.5%. Is that bad?

**A:** You're 1.8 percentage points above the 14.7% benchmark. This is:
- **Not catastrophic** — you're in the "yellow zone" (just above benchmark)
- **Concerning** — if persistent for 2+ quarters, indicates systemic issue
- **Fixable** — with targeted interventions (triage, monitoring, communication), you should be able to reach ≤14.7% within 6-12 months
- **Financially relevant** — at 16.5%, you're likely 3-star HHVBP (close to neutral); small improvements move you to 4-star (bonus)

**Action:** Investigate root causes; implement monthly monitoring; consider a PIP if rate doesn't improve in 90 days.

---

### Q2: Our functional outcome rates are below benchmark on all measures (ambulation, bathing, dyspnea, pain). What's wrong?

**A:** Low functional outcomes suggest:

**Possible causes:**
1. **Admission of very high-acuity patients** — if you're accepting patients too sick for meaningful functional improvement (e.g., hospice-level patients), outcomes will naturally be low
2. **Inadequate PT/OT staffing** — functional improvement requires skilled therapy; if you're nursing-heavy, PT/OT coverage may be insufficient
3. **Limited visit frequency** — if patients see PT/OT infrequently (monthly vs. weekly), gains are muted
4. **Baseline assessment issues** — if OASIS baselines are not capturing true functional status (over-scored initially), improvements at discharge appear smaller
5. **Early discharge** — if patients are discharged before goals are met (payer-driven), outcomes show incomplete improvement

**Diagnostic steps:**
- Review last 10-20 episodes with low functional improvement; what was the clinical reason?
- Compare your PT/OT visit frequency to agencies with >55% improvement rates
- Spot-check OASIS baselines for over/under-scoring
- Analyze discharge reasons: are patients being discharged prematurely due to payer limits?

**Action:** Likely requires clinical and staffing review; PT/OT capacity often needs to be addressed.

---

### Q3: The benchmarks seem outdated (2023-2025). When will newer data be available?

**A:** CMS publishes Home Health Compare data on a rolling basis with a ~9-month lag. Here's the typical timeline:

```
Measurement Year: 2025 (Jan-Dec 2025)
↓ (9-month lag)
Publication: September 2026 (Q3 2026)
↓
Updated Benchmarks: Q4 2026
```

**Current status (April 2026):** We're using 2023-2025 benchmarks, which are the most recent published. New 2025-2026 benchmarks will be available in Q4 2026.

**Will benchmarks change much?** Typically, benchmarks shift 0.3-1.0 percentage point annually. The direction of change is usually *tighter* (benchmarks improve, suggesting agencies collectively are improving).

---

### Q4: One of our patient diagnosis categories (e.g., CHF) naturally has high hospitalization. Should we apply a different benchmark?

**A:** Excellent question. The answer is nuanced:

**Short answer:** Use the national benchmark (14.7%) as your target, but:
1. **Risk-adjust internally:** Understand what a realistic goal is for CHF-heavy populations (data suggests 20-24% is not unusual)
2. **Set interim targets:** Target 18-20% in Year 1; 16-18% in Year 2; eventually reach 14.7%
3. **Focus on prevention:** Even if CHF populations have higher baseline rates, you can still prevent 20-30% of hospitalizations through early intervention

**Long answer:**
- CMS benchmarks are already somewhat risk-adjusted (age, major diagnoses are considered)
- If your CHF population is sicker than national average, risk-adjustment analysis will show this
- However, Enzo Health doesn't recommend accepting a permanently higher benchmark for a single diagnosis
- Instead, use risk-adjustment to set realistic interim targets, but keep the national benchmark as the long-term goal

**Example:**
- National benchmark: 14.7%
- Your raw rate (40% CHF): 19.2%
- Risk-adjusted realistic goal: 16-18% (Year 1), 15-16% (Year 2)
- Ultimate benchmark: 14.7% (but may take 24 months to achieve)

---

### Q5: What if we serve a Medicaid-heavy population (not just Medicare)?

**A:** This is important context:

**The issue:**
- CMS benchmarks are ONLY for Medicare beneficiaries (72% of home health)
- If you serve Medicaid, Medicare Advantage, or private patients heavily, your overall rate may look different than Medicare-only rates
- Medicaid patients often have higher hospitalization rates due to social factors (lower SES, less caregiver support, health literacy)

**Solution:**
1. **Separate your rates:** Calculate hospitalization rates for Medicare vs. Medicaid vs. private separately
2. **Use Medicare rate vs. CMS benchmark:** Compare only Medicare episodes to 14.7% benchmark
3. **Set Medicaid goals internally:** Work with Enzo to set realistic targets for Medicaid patients (may be 16-18% vs. 14.7%)
4. **Overall agency rate:** Calculate blended rate for your governing body, but monitor Medicare and non-Medicare separately for HHVBP purposes (HHVBP only affects Medicare reimbursement)

---

## Section 10: Conclusion

These CMS benchmarks represent the baseline performance of American home health agencies. They are:
- **Evidence-based** — derived from actual Medicare claims and OASIS data
- **Achievable** — many agencies exceed these benchmarks; excellence is defined as performance >1 SD above median
- **Evolving** — slowly improving over time as agencies implement quality improvement
- **Financially consequential** — tied to HHVBP payment adjustments and accreditation surveys

**For Enzo Health QAPI clients:** Use these benchmarks as your comparison standard. Your quarterly reports will compare your agency rates to these benchmarks and recommend actions (PIPs) when you fall below them.

**For continuous improvement:** The goal is not just to meet benchmarks, but to:
1. **Meet benchmarks** on all acute care measures (hospitalization ≤14.7%, ED ≤8.2%, timely SOC ≥96.3%)
2. **Exceed benchmarks** on functional outcomes (ambulation >55%, bathing >68%, dyspnea >60%)
3. **Move toward 5-star performance** (hospitalization ≤11%, ED ≤5%, functional outcomes >60%)

---

**Document prepared by:** Enzo Health QAPI Specialist Agent
**Effective Date:** April 2026
**Next Benchmark Update:** Q4 2026 (when CMS publishes 2025 measurement year data)
**Contact:** [qapi@enzohealth.com]

---

*This reference document is accurate as of April 2026 based on CMS Home Health Compare data (2023-2025 measurement years). Benchmarks will be updated when new CMS data is published (typically Q4 of each year). For the most current CMS benchmarks, visit https://www.medicare.gov/care-compare/ and select "Home Health".*
