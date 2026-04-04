# Enzo Health OA-2 Deliverables Index
**HHVBP Financial Model with Agency-Specific Baseline Inputs**

**Generated:** April 4, 2026  
**Agency:** Sunrise Home Health  
**Analysis Period:** Q1 2026 Actual + Q2 2026 Projection

---

## Quick Navigation

### Executive Summary
Start here for high-level findings and key metrics:
**→ [OA-2-COMPLETION-SUMMARY.md](./OA-2-COMPLETION-SUMMARY.md)**
- Baseline metrics (TPS 10.8, -6.27% adjustment, -$31,373/year)
- Highest-ROI opportunity (ED use reduction: +$1,746/year)
- Q2 projection (if hospitalization PIP on track: -5.91% adjustment, +$1,808 recovery)
- Next steps and monitoring plan

---

## Analysis Reports

### 1. HHVBP Sensitivity Analysis
**File:** [2026-Q1-hhvbp-sensitivity-analysis.md](./2026-Q1-hhvbp-sensitivity-analysis.md)

**Contains:**
- Baseline vs. national benchmarks (all 10 measures)
- Individual measure improvements (5-point scenarios, ranked by ROI)
- 5 named scenarios:
  - Hospitalization PIP goal (24% → 16%)
  - Timely initiation PIP goal (92% → 98%)
  - Functional outcome improvement (Ambulation, Bathing, Dyspnea)
  - Best case (all at benchmark)
  - Worst case (all 10 pts below benchmark)
- Breakeven analysis
- Top 3 high-ROI opportunities with detailed business cases
- Combined implementation strategy
- Quarterly monitoring scorecard

**Use This For:** Detailed financial modeling, scenario planning, board presentations

---

### 2. Q1 Actual + Q2 Projection Dashboard
**File:** [2026-Q1-Q2-projection-dashboard.md](./2026-Q1-Q2-projection-dashboard.md)

**Contains:**
- Q1 2026 actual performance (50-patient census analysis)
- Q1 clinical deep-dive:
  - Hospitalization root cause analysis (diagnosis breakdown)
  - ED utilization findings
  - Functional outcome gaps
  - Assessment timeliness issues
- Q2 projected performance (3 financial scenarios)
- Projection methodology with confidence levels
- Q1-Q2 financial projection (conservative vs. optimistic)
- Trend indicators (leading and lagging metrics)
- Weekly/monthly monitoring plan (April-June)
- Risk assessment and mitigation strategies
- Detailed milestone tracker
- Clinical quality improvement summary

**Use This For:** Operational monitoring, staff communication, quarterly reviews, board updates

---

## Python Models (Production-Ready)

### 1. HHVBP Financial Model
**File:** [/data/scripts/hhvbp_model.py](../../../data/scripts/hhvbp_model.py)

**Capabilities:**
- 10 HHVBP measures (achievement + benchmark scoring)
- Total Performance Score (TPS) calculation (0-100 scale)
- Payment adjustment mapping (-8% to +8%)
- Sensitivity analysis (measure improvements)
- Scenario analysis (best case, worst case, etc.)
- JSON and markdown report outputs

**Default Data:** Sunrise Home Health Q1 2026

**Usage:**
```bash
# Default (Sunrise data)
python3 hhvbp_model.py

# Custom agency
python3 hhvbp_model.py --revenue 750000 --hospitalization 18.0 --ambulation 52.0

# Export to JSON
python3 hhvbp_model.py --json-output results.json

# See all options
python3 hhvbp_model.py --help
```

**Use This For:** Custom agency analysis, model replication, financial projections

---

### 2. Star Rating Estimator
**File:** [/data/scripts/star_rating_estimator.py](../../../data/scripts/star_rating_estimator.py)

**Capabilities:**
- 7 OASIS-based star rating measures
- Linear mean percentile methodology (CMS approach)
- 1-5 star mapping with composite quality score
- Measure impact analysis (which metrics lifting vs. dragging)
- "What-if" improvement scenarios
- JSON and markdown outputs

**Default Data:** Sunrise Home Health Q1 2026 (estimated)

**Usage:**
```bash
# Default (Sunrise data)
python3 star_rating_estimator.py

# Custom agency
python3 star_rating_estimator.py --agency "New Agency" --hospitalization 16.0

# Export to JSON
python3 star_rating_estimator.py --json-output results.json
```

**Use This For:** Star rating estimation, quality benchmarking, provider profiling

---

## JSON Outputs (Machine-Readable)

### 1. HHVBP Model Output
**File:** [hhvbp-model-output.json](./hhvbp-model-output.json)

**Contains:**
- Metadata (generation timestamp, revenue)
- Summary metrics (TPS, adjustment %, dollar impact)
- Performance data (all 10 measures)
- Benchmarks and thresholds
- Detailed measure scores

**Use This For:** Data integration, downstream analysis, API consumption

---

### 2. Star Rating Output
**File:** [star-rating-output.json](./star-rating-output.json)

**Contains:**
- Metadata (agency name, timestamp)
- Results (composite score, star rating)
- Measure-level data (agency performance, benchmark, percentile)

**Use This For:** Quality dashboards, provider comparison tools, external reporting

---

## Key Findings Summary

### Sunrise Home Health Baseline (Q1 2026)

| Metric | Value | Status |
|--------|-------|--------|
| **TPS** | 10.8 / 100 | SEVERE UNDERPERFORMANCE |
| **Payment Adjustment** | -6.27% | -$31,373/year penalty |
| **Star Rating** | 1 / 5 | Bottom 10% nationally |
| **Composite Quality Score** | 36.0 / 100 | Below minimum acceptable |

### Measures Performance vs. Benchmark
- 9 of 10 measures below benchmark
- Only strength: Medication Management (+2.9 pts better)
- Biggest gaps: Hospitalization (+9.3 pts worse), Discharge (-9.8 pts worse)
- Functional outcomes avg 5-7 points below benchmark

### Highest-ROI Opportunity
**ED Use Without Hospitalization (10% → 5%)**
- Annual recovery: +$1,746/year
- Implementation cost: $4,000
- Timeline: 8-12 weeks
- ROI: Positive in Year 2+

### Q2 Projection (If PIP On Track)
- Hospitalization reduction: 24% → 16%
- Projected TPS: 13.0 (vs. 10.8 baseline)
- Projected adjustment: -5.91% (vs. -6.27%)
- Annual recovery: +$1,808

---

## How to Use This Folder

### For Finance/Leadership
1. Read: [OA-2-COMPLETION-SUMMARY.md](./OA-2-COMPLETION-SUMMARY.md) — 10 min overview
2. Review: [2026-Q1-hhvbp-sensitivity-analysis.md](./2026-Q1-hhvbp-sensitivity-analysis.md) — scenarios & strategy
3. Share: JSON files for dashboards and reporting

### For Clinical Operations
1. Read: [2026-Q1-Q2-projection-dashboard.md](./2026-Q1-Q2-projection-dashboard.md) — clinical context
2. Reference: Milestone tracker and monitoring plan (April-June)
3. Use: Key metrics for staff communication

### For Data/Analytics
1. Review: Python model documentation (inline comments)
2. Test: Run models with different inputs
3. Export: JSON outputs for downstream integration
4. Extend: Adapt models for other agencies

### For Board Presentations
1. Use: Summary metrics from [OA-2-COMPLETION-SUMMARY.md](./OA-2-COMPLETION-SUMMARY.md)
2. Show: Financial scenarios from sensitivity analysis
3. Present: Q2 projection and recovery opportunity

---

## Technical Specifications

### HHVBP Model
- **Language:** Python 3
- **Dependencies:** Standard library only (json, argparse, datetime, typing)
- **Lines of Code:** 650+
- **Documentation:** Full inline comments
- **Extensibility:** Any agency, any year

### Star Rating Estimator
- **Language:** Python 3
- **Dependencies:** Standard library only
- **Lines of Code:** 500+
- **Documentation:** Full inline comments
- **Extensibility:** Any agency, any year

### Accuracy & Validation
- CY 2026 HHVBP specifications implemented
- CMS benchmark values used
- Mathematical accuracy verified against test cases
- Star rating methodology validated against published guidelines

---

## Contact & Support

**For Technical Questions:**
Review inline code documentation in Python files.

**For Methodological Questions:**
Refer to CMS published HHVBP documentation:
https://www.cms.gov/Medicare/Quality-Reporting-Systems/HHVBP

**For Agency-Specific Analysis:**
Use Python models with your agency's performance data.

---

## File Manifest

```
/sessions/nice-brave-brahmagupta/workspaces/enzo-health/
├── data/scripts/
│   ├── hhvbp_model.py                 (650+ lines, fully documented)
│   └── star_rating_estimator.py       (500+ lines, fully documented)
└── outcomes/dashboards/
    ├── INDEX.md                       (This file)
    ├── OA-2-COMPLETION-SUMMARY.md     (Executive summary)
    ├── 2026-Q1-hhvbp-sensitivity-analysis.md       (Detailed scenarios)
    ├── 2026-Q1-Q2-projection-dashboard.md          (Actual + projection)
    ├── hhvbp-model-output.json        (Machine-readable)
    └── star-rating-output.json        (Machine-readable)
```

---

## Next Steps

### Immediate (April 2026)
- Activate hospitalization PIP (daily monitoring protocols)
- Deploy SOC scheduling automation
- Begin weekend nursing on-call (ED reduction)
- Launch communication coaching

### Mid-Quarter (May)
- Review interim Q2 metrics (May 1-5)
- PT/OT protocol rollout
- Monthly clinical huddles
- Staff training completion

### End-of-Quarter (June)
- Q2 comprehensive analysis
- HHVBP adjustment revision
- Star rating re-estimation
- H1 2026 board review

---

**Generated by:** Enzo Health Outcomes Analyst Agent  
**Date:** April 4, 2026  
**Status:** Complete and validated
