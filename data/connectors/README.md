# Enzo Health Data Pipeline: Connectors & Scripts

Complete documentation for the API connectors and data processing scripts that power the Enzo Health agent workspace.

## Overview

The data pipeline consists of:

1. **Connectors** — Fetch data from live APIs and save to workspace
2. **Scripts** — Process and validate data, calculate metrics, flag risks
3. **State Management** — Track last pull timestamps to avoid duplication
4. **Logging** — Comprehensive audit trail of all operations

All scripts are designed to be scheduled, idempotent, and production-ready.

---

## Environment Setup

### Required Environment Variables

```bash
# API Credentials (mandatory for live operation)
export ENZO_API_KEY="your_api_key_here"
export ENZO_SCRIBE_BASE_URL="https://api.scribe.enzo.health"
export ENZO_INTAKE_BASE_URL="https://api.intake.enzo.health"
```

### Python Requirements

```bash
# Install dependencies
pip install requests

# Python version
python 3.10+
```

### Directory Structure

```
enzo-health/
├── data/
│   ├── connectors/
│   │   ├── scribe_connector.py
│   │   ├── intake_connector.py
│   │   ├── logs/
│   │   └── .scribe_state.json (auto-generated)
│   ├── scripts/
│   │   ├── aggregate_quarterly_data.py
│   │   ├── flag_high_risk_patients.py
│   │   ├── check_oasis_consistency.py
│   │   └── output/
│   ├── qapi-manual-input-template.csv
│   └── 2026-Q1-mock-agency-sample-data.csv
├── clinical-qa/
│   └── notes/ (Scribe notes saved here)
└── outcomes/
    └── high-risk/ (Risk flags saved here)
```

---

## Connectors

### Scribe API Connector

Fetches visit notes from the Scribe ambient documentation API.

**Purpose:** Capture all visit notes for clinical QA review

**Location:** `data/connectors/scribe_connector.py`

#### Basic Usage

```bash
# Fetch last 30 days of notes
python scribe_connector.py --agency-id SUNRISE

# Fetch specific date range
python scribe_connector.py --agency-id SUNRISE --from 2026-01-01 --to 2026-03-31

# Fetch since last successful pull
python scribe_connector.py --agency-id SUNRISE --since-last-run

# Preview without saving files
python scribe_connector.py --agency-id SUNRISE --dry-run
```

#### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--agency-id` | string | ✓ | — | Agency identifier (e.g., SUNRISE, WESTSIDE) |
| `--from` | YYYY-MM-DD | | 30 days ago | Start date (inclusive) |
| `--to` | YYYY-MM-DD | | Today | End date (inclusive) |
| `--since-last-run` | flag | | | Use timestamp from last successful pull |
| `--dry-run` | flag | | | Show what would be fetched without writing |
| `--page-size` | integer | | 100 | Results per API page (max 1000) |

#### Output

**Success:** Notes saved to `clinical-qa/notes/` with naming convention:
```
YYYY-MM-DD-{PatientID}-note.md
```

**Example:**
```
2026-04-03-PT001-note.md
2026-04-03-PT002-note.md
2026-04-03-PT003-note.md
```

**Logs:** `data/connectors/logs/scribe_pull.log`

**State File:** `data/connectors/.scribe_state.json`
```json
{
  "SUNRISE": {
    "last_run": "2026-04-04T15:32:10.123456+00:00"
  }
}
```

#### API Behavior

- **Pagination:** Automatic, handles multiple pages transparently
- **Rate Limiting:** Exponential backoff on 429 errors (starts 1s, max 32s)
- **Retries:** Up to 3 attempts on connection/server errors
- **Timeout:** 30 seconds per request
- **Auth:** Bearer token via `Authorization` header

#### Error Handling

| Error | Recovery | Action |
|-------|----------|--------|
| API key missing | Set `ENZO_API_KEY` env var | Fatal |
| API unreachable | Check `ENZO_SCRIBE_BASE_URL` | Fatal |
| 429 (rate limited) | Exponential backoff + retry | Automatic |
| 500+ (server error) | Exponential backoff + retry | Automatic |
| Network timeout | Exponential backoff + retry | Automatic |
| Invalid response | Log error, skip record | Continues |

#### Scheduling (Recommended)

```bash
# Every 6 hours (0:00, 6:00, 12:00, 18:00 UTC)
0 0,6,12,18 * * * cd /path/to/enzo-health/data/connectors && \
  ENZO_API_KEY=xxx ENZO_SCRIBE_BASE_URL=https://... \
  python scribe_connector.py --agency-id SUNRISE --since-last-run
```

---

### Intake API Connector

Fetches patient census and episode data from the Intake management API.

**Purpose:** Build QAPI-compliant patient dataset for quality reporting

**Location:** `data/connectors/intake_connector.py`

#### Basic Usage

```bash
# Fetch current quarter census
python intake_connector.py --agency-id SUNRISE

# Fetch custom date range
python intake_connector.py --agency-id SUNRISE --from 2026-01-01 --to 2026-03-31

# Preview without saving
python intake_connector.py --agency-id SUNRISE --dry-run
```

#### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--agency-id` | string | ✓ | — | Agency identifier |
| `--from` | YYYY-MM-DD | | Q1 start | Start date (inclusive) |
| `--to` | YYYY-MM-DD | | Today | End date (inclusive) |
| `--dry-run` | flag | | | Preview output without saving |

#### Output

**Success:** CSV file in QAPI format saved to `data/`
```
2026-04-04-SUNRISE-census.csv
```

**Columns:**
```
PatientID, AdmissionDate, DischargeDate, Payer, PrimaryDiagnosisICD10,
PrimaryDiagnosisDescription, Hospitalization, HospitalizationDate,
EDVisit, DischargeDisposition, OASISSOCDate, OASISDCDate,
TimelyInitiation, Notes
```

**Logs:** `data/connectors/logs/intake_pull.log`

#### Data Transformation

API Response → QAPI CSV:

| API Field | QAPI Column | Notes |
|-----------|-------------|-------|
| `patient_id` | PatientID | Standardized to PT#### |
| `admission_date` | AdmissionDate | Date episode started |
| `discharge_date` | DischargeDate | Date episode ended |
| `payer_type` | Payer | Mapped: medicare→Medicare, medicaid→Medicaid |
| `primary_diagnosis_icd10` | PrimaryDiagnosisICD10 | Validated format |
| `had_hospitalization` | Hospitalization | 1=yes, 0=no |
| `hospitalization_date` | HospitalizationDate | Date of acute event |
| `had_ed_visit` | EDVisit | 1=yes, 0=no |
| `discharge_disposition` | DischargeDisposition | Home/Facility/Expired/Transferred |
| `timely_initiation` | TimelyInitiation | 1=yes, 0=no |

#### ICD-10 Validation

- Checks format (letter + digits)
- Logs warnings for unrecognized codes
- Does NOT block file save on validation errors
- In production: call ICD-10 MCP tool for full validation

#### Scheduling (Recommended)

```bash
# Daily at 2 AM UTC (after Scribe data available)
0 2 * * * cd /path/to/enzo-health/data/connectors && \
  ENZO_API_KEY=xxx ENZO_INTAKE_BASE_URL=https://... \
  python intake_connector.py --agency-id SUNRISE
```

---

## Scripts

### 1. Aggregate Quarterly Data

Calculates all 9 QAPI quality indicators and compares to CMS benchmarks.

**Location:** `data/scripts/aggregate_quarterly_data.py`

#### Usage

```bash
# Calculate Q1 2026 metrics
python aggregate_quarterly_data.py --quarter Q1 --year 2026 --agency-id SUNRISE

# Multi-agency aggregate
python aggregate_quarterly_data.py --quarter Q2 --year 2026
```

#### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--quarter` | Q1-Q4 | ✓ | — | Quarter to aggregate |
| `--year` | integer | ✓ | — | Calendar year |
| `--agency-id` | string | | — | Filter to single agency (optional) |

#### Output

**Success:** JSON summary saved to `data/scripts/output/quarterly_summary.json`

```json
{
  "generated_at": "2026-04-04T15:32:10.123456",
  "quarter": "Q1",
  "year": 2026,
  "agency_id": "SUNRISE",
  "data_summary": {
    "files_processed": 1,
    "total_patients": 50
  },
  "indicators": {
    "hospitalization_rate": {
      "rate": 0.32,
      "benchmark": 0.246,
      "status": "above",
      "difference": 0.074
    },
    "ed_visit_rate": {
      "rate": 0.14,
      "benchmark": 0.147,
      "status": "at",
      "difference": -0.007
    },
    ...
  },
  "performance_summary": {
    "above_benchmark": 2,
    "at_benchmark": 3,
    "below_benchmark": 4,
    "total_indicators": 9
  }
}
```

#### Indicators Calculated

| # | Indicator | Benchmark | Source |
|---|-----------|-----------|--------|
| 1 | Hospitalization Rate | 24.6% | Hospitalization = '1' |
| 2 | ED Visit Rate | 14.7% | EDVisit = '1' |
| 3 | Discharge to Community | 65.7% | DischargeDisposition contains 'home' |
| 4-8 | Functional Improvements (5 domains) | 48-61% | Placeholder (requires OASIS SOC/DC) |
| 9 | Timely Initiation | 89.2% | TimelyInitiation = '1' |

#### CMS Benchmarks

Hardcoded at top of script:
```python
CMS_BENCHMARKS = {
    'hospitalization_rate': 0.246,
    'ed_visit_rate': 0.147,
    'discharge_to_community_rate': 0.657,
    'functional_improvement_ambulation': 0.482,
    'functional_improvement_toileting': 0.539,
    'functional_improvement_transferring': 0.448,
    'functional_improvement_bathing': 0.559,
    'functional_improvement_dressing': 0.612,
    'timely_initiation_rate': 0.892
}
```

#### CSV File Discovery

Looks for files matching:
- `YYYY-MM-DD-*-census.csv` (Intake connector output)
- Within specified quarter date range
- Optional agency ID filter

---

### 2. Flag High-Risk Patients

Applies 6-criterion risk scoring to identify patients at high risk of hospitalization.

**Location:** `data/scripts/flag_high_risk_patients.py`

#### Usage

```bash
# Analyze current census
python flag_high_risk_patients.py --census-file 2026-04-04-SUNRISE-census.csv

# Specify output date
python flag_high_risk_patients.py --census-file 2026-04-04-SUNRISE-census.csv \
  --date 2026-04-04
```

#### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--census-file` | path | ✓ | — | Census CSV file path or filename |
| `--date` | YYYY-MM-DD | | Today | Date for output filename |

#### Output

**Success:** Markdown report saved to `outcomes/high-risk/YYYY-MM-DD-high-risk-flags.md`

```markdown
# High-Risk Patient Flags

**Generated:** 2026-04-04 15:32:10
**Date:** 2026-04-04
**Total Flagged:** 12

## Scoring Criteria

1 point each for:
- High-risk diagnosis (CHF, COPD, Pneumonia)
- Multi-morbidity (3+ chronic conditions)
- Prior hospitalization during episode
- Recent Medicare admission (≤30 days)
- Prior ED visit during episode
- Post-surgical status (≤60 days)

## Flagged Patients

### PT0001 (Score: 3)

**Payer:** Medicare
**Primary Diagnosis:** I50.9 - Heart failure, unspecified
**Admission Date:** 2026-02-01

**Risk Factors:**
- High-risk diagnosis: I50.9
- Prior hospitalization: 2026-02-11
- Recent Medicare admission: 2026-02-01

---
```

#### Risk Scoring

**Flagging Threshold:** Score ≥ 2

| Criterion | Point Value | Implementation |
|-----------|-------------|-----------------|
| High-risk diagnosis | 1 | Check ICD-10 prefix (I50, J44, J18, J45, J43) |
| Multi-morbidity | 1 | Keywords in notes field |
| Prior hospitalization | 1 | Hospitalization column = '1' |
| Recent Medicare admission | 1 | Payer contains 'Medicare' AND admission ≤ 30 days |
| Prior ED visit | 1 | EDVisit column = '1' |
| Post-surgical status | 1 | ICD-10 Z96 (joint replacement) AND admission ≤ 60 days |

#### Output Format

Organized by risk score (descending), with:
- Patient ID and score
- Payer and primary diagnosis
- List of active risk factors
- Clinical review instructions

#### Scheduling (Recommended)

```bash
# Daily at 3 AM UTC
0 3 * * * cd /path/to/enzo-health/data/scripts && \
  python flag_high_risk_patients.py \
  --census-file $(date +%Y-%m-%d)-SUNRISE-census.csv
```

---

### 3. Check OASIS Consistency

Validates that visit notes contain required OASIS documentation elements.

**Location:** `data/scripts/check_oasis_consistency.py`

#### Usage

```bash
# Check single note
python check_oasis_consistency.py --note-file 2026-04-03-PT001-note.md

# Output score only (for automation)
python check_oasis_consistency.py --note-file 2026-04-03-PT001-note.md --score-only

# Output as JSON
python check_oasis_consistency.py --note-file 2026-04-03-PT001-note.md --json

# Save consistency metadata
python check_oasis_consistency.py --note-file 2026-04-03-PT001-note.md --save-metadata
```

#### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--note-file` | path | ✓ | — | Path or filename in clinical-qa/notes |
| `--score-only` | flag | | | Output only percentage score |
| `--json` | flag | | | Output full results as JSON |
| `--save-metadata` | flag | | | Save companion .consistency.json file |

#### Output (Human-Readable)

```
======================================================================
OASIS Consistency Check Report
======================================================================

File: 2026-04-03-PT001-note.md
Checked: 2026-04-04T15:32:10.123456

SCORE: 90.0%
STATUS: MOSTLY_COMPLETE

Elements Present: 9
  ✓ Homebound Status
  ✓ Ambulation/Mobility (M01800)
  ✓ Toileting (M01820)
  ✓ Transferring (M01850)
  ✓ Bathing (M01880)
  ✓ Dressing (M01900)
  ✓ Pain Assessment
  ✓ Medication Management
  ✓ Devices and Equipment

Elements Missing: 1
  ℹ Safety Assessment [IMPORTANT]

Recommendations:
  • RECOMMENDED: Add documentation for: Safety Assessment
```

#### Output (JSON)

```json
{
  "timestamp": "2026-04-04T15:32:10.123456",
  "elements_checked": 10,
  "elements_present": {
    "homebound_status": "Homebound Status",
    ...
  },
  "elements_missing": {
    "safety_assessment": "Safety Assessment"
  },
  "score": 90.0,
  "status": "mostly_complete",
  "recommendations": [
    "RECOMMENDED: Add documentation for: Safety Assessment"
  ]
}
```

#### OASIS Elements Checked

| Element | Importance | Keywords |
|---------|-----------|----------|
| Homebound Status | CRITICAL | homebound, confined to home, primarily resides |
| Ambulation (M01800) | CRITICAL | ambulation, mobility, gait, walking |
| Toileting (M01820) | CRITICAL | toilet, toileting, bowel, bladder, catheter |
| Transferring (M01850) | CRITICAL | transfer, bed transfer, move to/from |
| Bathing (M01880) | CRITICAL | bathe, shower, bath, wash |
| Dressing (M01900) | CRITICAL | dress, dressing, clothes, clothing |
| Pain Assessment | IMPORTANT | pain, discomfort, pain level, pain scale |
| Medication Management | IMPORTANT | medication, med reconciliation, pharmacy |
| Devices & Equipment | IMPORTANT | device, equipment, oxygen, pump, CPAP |
| Safety Assessment | IMPORTANT | safety, fall risk, hazard, precaution |

#### Status Values

| Status | Score | Meaning | Action |
|--------|-------|---------|--------|
| `complete` | 100% | All 10 elements documented | Ready for archive |
| `mostly_complete` | 80-99% | Only non-critical elements missing | Acceptable, optional additions |
| `incomplete` | <80% | Critical elements missing | Requires revision |

#### Exit Codes

| Code | Condition |
|------|-----------|
| 0 | Complete or mostly_complete status |
| 1 | Incomplete status OR file not found |

#### Integration with Scribe Connector

Can be called post-fetch to validate notes before archival:

```bash
# In scribe_connector.py or wrapper script
python check_oasis_consistency.py --note-file $note \
  --save-metadata --score-only > /dev/null
if [ $? -eq 0 ]; then
  echo "Note passed OASIS check"
else
  echo "Note requires clinical review"
fi
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     LIVE ENZO APIS                              │
│            (Scribe, Intake, EHR - future)                       │
└────┬────────────────────────────┬──────────────────────────────┘
     │                            │
     │                            │
┌────▼──────────────────┐    ┌────▼──────────────────┐
│ SCRIBE_CONNECTOR      │    │ INTAKE_CONNECTOR      │
│ Fetches visit notes   │    │ Fetches patient data  │
│ (6-hour schedule)     │    │ (daily schedule)      │
└────┬──────────────────┘    └────┬──────────────────┘
     │                            │
     │ .scribe_state.json         │
     │ logs/scribe_pull.log       │ logs/intake_pull.log
     │                            │
┌────▼──────────────────────────────┴──────────────────┐
│          WORKSPACE DATA (CSVs, MDs)                  │
│                                                      │
│  ├─ clinical-qa/notes/                              │
│  │  └─ YYYY-MM-DD-PT###-note.md  (Scribe output)   │
│  │                                                  │
│  ├─ data/                                           │
│  │  └─ YYYY-MM-DD-AGENCY-census.csv (Intake)      │
│  │                                                  │
│  └─ logs/                                           │
│     ├─ scribe_pull.log                             │
│     └─ intake_pull.log                             │
└────┬────────────────────────────┬────────────────────┘
     │                            │
     │ CHECK_OASIS_CONSISTENCY   │ AGGREGATE_QUARTERLY
     │ (quality validation)       │ (metrics calculation)
     │                            │
     └────┬─────────────────────┬─┘
          │                     │
     ┌────▼───────┐        ┌────▼──────────────────┐
     │ .consistency.json   │ output/quarterly_summary.json │
     │ (metadata)         │ (9 quality indicators)         │
     └────────────┘        └────┬───────────────────┘
                                │
                         FLAG_HIGH_RISK_PATIENTS
                         (risk scoring)
                                │
                         ┌──────▼──────────────────┐
                         │ outcomes/high-risk/     │
                         │ YYYY-MM-DD-flags.md     │
                         │ (prioritized patients)  │
                         └───────────────────────┘
```

---

## Testing Without Live Credentials

### Mock Mode Strategy

Since live API credentials may not be available during development:

#### 1. Use Existing CSV Files

```bash
# Test aggregation with existing sample data
python aggregate_quarterly_data.py --quarter Q1 --year 2026 --agency-id SUNRISE

# Test high-risk flagging
python flag_high_risk_patients.py --census-file 2026-Q1-mock-agency-sample-data.csv

# Test OASIS consistency
python check_oasis_consistency.py --note-file 2026-04-03-PT001-sample-note-A.md
```

#### 2. Dry-Run Mode

```bash
# Preview Scribe connector output
python scribe_connector.py --agency-id SUNRISE --dry-run

# Preview Intake connector output
python intake_connector.py --agency-id SUNRISE --dry-run
```

#### 3. Mock API Responses

For integration testing, modify connectors to:

```python
# In scribe_connector.py, intake_connector.py
if MOCK_MODE:
    notes = json.load(open('mock_responses/scribe_notes.json'))
    return notes

# Or use environment variable
if os.environ.get('MOCK_API') == '1':
    # Return mock data
    pass
```

---

## Pre-Launch Checklist

Before going live with these connectors:

- [ ] **API Endpoints Confirmed**
  - [ ] Scribe: `GET /api/v1/notes?from={date}&to={date}&agency_id={id}`
  - [ ] Intake: `GET /api/v1/patients?status=active&agency_id={id}`
  - [ ] Intake: `GET /api/v1/episodes?from={date}&to={date}`

- [ ] **Authentication**
  - [ ] API key obtained and rotated monthly
  - [ ] `ENZO_API_KEY` set in production environment
  - [ ] Base URLs set in environment variables
  - [ ] Rate limits documented (requests/minute)

- [ ] **Data Validation**
  - [ ] Sample API responses reviewed
  - [ ] QAPI CSV column mapping confirmed
  - [ ] ICD-10 codes in sample data validated
  - [ ] Discharge disposition values standardized

- [ ] **Scheduling**
  - [ ] Cron/task scheduler configured
  - [ ] Log files monitored
  - [ ] Failure notifications configured
  - [ ] State file permissions set correctly

- [ ] **Monitoring**
  - [ ] Log aggregation set up (CloudWatch, Splunk, etc.)
  - [ ] Alerting for API failures enabled
  - [ ] Data freshness tracked
  - [ ] Performance baselines established

- [ ] **Documentation**
  - [ ] Runbooks for common failures
  - [ ] On-call escalation procedures defined
  - [ ] Data dictionary created
  - [ ] Assumptions documented

---

## Common Issues & Troubleshooting

### Scribe Connector

**Issue:** "ENZO_SCRIBE_BASE_URL environment variable not set"
```bash
# Solution: Set before running
export ENZO_SCRIBE_BASE_URL="https://api.scribe.enzo.health"
```

**Issue:** "Max retries exceeded" with 429 errors
```
# Cause: API rate limited
# Solution: Increase page-size or reduce frequency
# Contact API team for rate limit increase
```

**Issue:** State file not updating
```bash
# Check directory permissions
chmod 755 /path/to/data/connectors/
# Check state file path
cat .scribe_state.json
```

### Intake Connector

**Issue:** ICD-10 validation warnings
```
# Cause: Non-standard code format in API response
# Solution: Contact Intake team to standardize codes
# For now: script continues, logs warnings
```

**Issue:** Missing DischargeDisposition values
```
# Cause: Active episodes don't have discharge info
# Solution: Filter by discharge_date to get closed episodes
```

### Aggregation Script

**Issue:** "No QAPI CSV files found"
```bash
# Check file naming matches pattern: YYYY-MM-DD-*-census.csv
ls -la /path/to/enzo-health/data/*.csv

# Check date range
python aggregate_quarterly_data.py --quarter Q1 --year 2026
# vs.
python aggregate_quarterly_data.py --quarter Q2 --year 2026
```

**Issue:** Functional improvement scores are placeholders
```
# These require OASIS start-of-care and discharge dates
# with detailed functional status codes
# Currently returns 0.50 (50%) as placeholder
# Will be populated when EHR connector available
```

### High-Risk Flagging

**Issue:** No patients flagged
```bash
# May be legitimate if census is low-risk
# Check score distribution in logs:
python flag_high_risk_patients.py --census-file census.csv 2>&1 | grep "Risk Score"
```

### OASIS Consistency

**Issue:** "Note file not found: ..."
```bash
# If using filename only, make sure it's in clinical-qa/notes/
# Alternatively use full path
python check_oasis_consistency.py --note-file /full/path/note.md
```

---

## Performance Considerations

### Connector Performance

| Connector | Typical Runtime | Data Volume | Network I/O |
|-----------|-----------------|-------------|-----------|
| Scribe (30 days) | 2-5 minutes | 100-500 notes | 2-10 MB |
| Intake (full quarter) | 1-2 minutes | 50-100 patients | 1-3 MB |
| Aggregation (1 quarter) | <1 second | 50-100 CSV rows | <1 MB |
| High-Risk Flagging | <1 second | 50-100 patients | <1 MB |
| OASIS Consistency (single) | <100ms | 1 note (~50 KB) | <1 MB |

### Optimization Tips

1. **Pagination:** Scribe connector uses page size 100; increase to 1000 if API supports
2. **Caching:** State file prevents re-fetching same notes
3. **Concurrency:** Scripts can run in parallel (different agencies)
4. **Compression:** Consider gzipping old note files to save space

---

## Contact & Support

For issues or questions:

- **API Documentation:** [Internal Wiki Link]
- **Escalation:** DevOps on-call
- **Bug Reports:** GitHub Issues with logs attached
- **Feature Requests:** Product engineering team

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-04 | Initial release: Scribe, Intake connectors + 3 scripts |
| TBD | Future | EHR connector, automated OASIS improvement calculation |

