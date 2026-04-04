# Enzo Health Workspace

**Founded:** April 4, 2026
**Founding Engineer:** Enzo Health FE-1
**Workspace Root:** `/sessions/nice-brave-brahmagupta/workspaces/enzo-health/`

---

## Directory Structure and Purpose

### Top-Level Directories

#### `/qapi/` — Quality Assurance and Performance Improvement
Central hub for all quality measurement and improvement activities.

- **`qapi/data/`** — Raw quality data feeds and manual input templates
  - CSV uploads, data imports, measurement extracts
  - Agent: QAPI Data Analyst
  - File naming: `YYYY-MM-DD-[description].csv`

- **`qapi/reports/`** — Quarterly QAPI reports, executive summaries
  - Agent: QAPI Specialist
  - File naming: `YYYY-MM-DD-[agency]-qapi-report.md`

- **`qapi/pips/`** — Performance Improvement Projects (active and archived)
  - PIP documentation, root cause analyses, intervention tracking
  - Agent: QAPI Specialist, Clinical Leadership
  - File naming: `[PIP-ID]-[title].md` or `PIP-[YYYY-MM-DD].md`

- **`qapi/governing-body/`** — Board presentation packages, governance materials
  - Quality summaries for board review
  - Agent: QAPI Specialist
  - File naming: `YYYY-MM-DD-board-package.md`

---

#### `/clinical-qa/` — Clinical Documentation Quality Assurance
Reviews and audits of clinician documentation for compliance and quality.

- **`clinical-qa/notes/`** — Individual clinical note reviews
  - Scored QA reviews of SOC, ROC, routine, and discharge notes
  - Agent: Clinical Documentation QA Agent
  - File naming: `YYYY-MM-DD-PT-[ID]-visit-qa.md`

- **`clinical-qa/weekly-audit/`** — Weekly audit summaries
  - Aggregated weekly QA results, trends, patterns
  - Agent: Clinical Documentation QA Agent
  - File naming: `YYYY-MM-DD-weekly-audit.md`

- **`clinical-qa/reports/`** — Monthly/quarterly documentation quality reports
  - Summary reports by clinician role, visit type, payer
  - Agent: Clinical Documentation QA Agent
  - File naming: `YYYY-MM-DD-[month]-qa-report.md`

---

#### `/survey-readiness/` — Medicare Survey Preparation
Mock surveys, compliance gap identification, and readiness tracking.

- **`survey-readiness/mock-surveys/`** — Mock survey reports
  - Statement of Deficiencies format internal surveys
  - Agent: Survey Readiness Agent
  - File naming: `YYYY-MM-DD-[agency]-mock-survey.md`

- **`survey-readiness/gap-lists/`** — Compliance gap tracking
  - Items to address before actual CMS survey
  - Agent: Survey Readiness Agent
  - File naming: `YYYY-MM-DD-survey-gaps.md`

- **`survey-readiness/poc/`** — Proof-of-correction documentation
  - Evidence that deficiencies have been corrected
  - Agent: Compliance Officer
  - File naming: `YYYY-MM-DD-POC-[tag-number].md`

---

#### `/regulatory/` — Regulatory Intelligence and Compliance
Tracking regulatory changes, coverage policies, and compliance requirements.

- **`regulatory/digests/`** — Weekly regulatory intelligence digests
  - CMS updates, NCD/LCD changes, regulatory changes
  - Agent: Regulatory Intelligence Agent
  - File naming: `YYYY-MM-DD-regulatory-digest.md`

- **`regulatory/impact-analyses/`** — Impact analyses of regulatory changes
  - How new policies affect operations, billing, documentation
  - Agent: Regulatory Analyst
  - File naming: `YYYY-MM-DD-[regulation]-impact-analysis.md`

---

#### `/outcomes/` — Quality Outcomes and Patient Safety
Outcome measurement, hospitalization analysis, high-risk patient tracking.

- **`outcomes/dashboards/`** — Monthly outcomes dashboards
  - STAR ratings, quality measures, payment projections
  - Agent: Outcomes Analyst Agent
  - File naming: `YYYY-MM-[month]-outcomes-dashboard.md`

- **`outcomes/rca/`** — Root Cause Analyses of hospitalizations
  - Individual patient hospitalizations and preventability assessment
  - Agent: Outcomes Analyst Agent
  - File naming: `YYYY-MM-DD-RCA-[PT-ID].md`

- **`outcomes/high-risk/`** — High-risk patient tracking
  - Patients at high risk of hospitalization or readmission
  - Agent: Clinical Risk Manager
  - File naming: `YYYY-MM-DD-high-risk-list.md`

---

#### `/reports/` — Executive and Stakeholder Reports
Cross-functional reports for internal and external stakeholders.

- File naming: `YYYY-MM-DD-[stakeholder]-[report-type].md`
- Agent: Executive Reporting Agent

---

#### `/templates/` — Document Templates
Standardized templates for all report types. Use these as starting points for new documents.

**Available templates:**
1. `qapi-quarterly-report-template.md` — Full QAPI quarterly report structure
2. `pip-template.md` — Performance Improvement Project documentation
3. `governing-body-package-template.md` — Board quality package
4. `note-qa-review-template.md` — Clinical note QA review scoring
5. `mock-survey-template.md` — Mock survey statement of deficiencies
6. `rca-template.md` — Hospitalization root cause analysis
7. `regulatory-digest-template.md` — Weekly regulatory intelligence digest
8. `outcomes-dashboard-template.md` — Monthly outcomes dashboard

All templates are structured with placeholders `[LIKE THIS]` for easy customization.

---

#### `/data/` — Data Files and Inputs
Raw data, data imports, measurement extracts, and reference files.

- `qapi-manual-input-template.csv` — Template for manual data entry of patient episodes
  - Columns: PatientID, AdmissionDate, DischargeDate, Payer, PrimaryDiagnosisICD10, Hospitalization, etc.
  - File naming for imports: `YYYY-MM-DD-[agency]-patient-data.csv`

---

## File Naming Conventions

All files use ISO 8601 date prefixes and lowercase-with-hyphens naming:

```
YYYY-MM-DD-[description]-[optional-identifier].md
```

Examples:
- `2026-04-04-memorial-hospital-qapi-q1-report.md`
- `2026-03-15-PT-001-hospitalization-rca.md`
- `2026-04-04-regulatory-digest.md`
- `2026-03-20-survey-gaps.md`

---

## Agent Ownership and Responsibilities

| Directory | Primary Agent | Secondary Agents |
|-----------|---------------|------------------|
| `qapi/data` | QAPI Data Analyst | — |
| `qapi/reports` | QAPI Specialist | Clinical Leadership |
| `qapi/pips` | QAPI Specialist | Clinical Leadership, Care Coordination |
| `qapi/governing-body` | QAPI Specialist | Executive Director |
| `clinical-qa/notes` | Clinical Documentation QA Agent | — |
| `clinical-qa/weekly-audit` | Clinical Documentation QA Agent | Clinician Manager |
| `clinical-qa/reports` | Clinical Documentation QA Agent | QAPI Specialist |
| `survey-readiness/mock-surveys` | Survey Readiness Agent | Compliance Officer |
| `survey-readiness/gap-lists` | Survey Readiness Agent | Clinical Leadership |
| `survey-readiness/poc` | Compliance Officer | — |
| `regulatory/digests` | Regulatory Intelligence Agent | — |
| `regulatory/impact-analyses` | Regulatory Analyst | QAPI Specialist |
| `outcomes/dashboards` | Outcomes Analyst Agent | QAPI Specialist |
| `outcomes/rca` | Outcomes Analyst Agent | Clinical Leadership |
| `outcomes/high-risk` | Clinical Risk Manager | Care Coordination |
| `reports` | Executive Reporting Agent | QAPI Specialist |

---

## MCP Tool Connectivity Status

All MCP tools have been tested and verified functional as of April 4, 2026.

### ICD-10 Code Lookup
**Tool:** `lookup_code` (ICD-10-CM diagnosis)
**Test Query:** Code I50.9 (Heart failure, unspecified)

**Result:**
```
Code: I50.9
Short Description: Heart failure, unspecified
Long Description: Heart failure, unspecified
Valid for HIPAA Transactions: Yes
Chapter: I
Category: I50
```
**Status:** ✅ OPERATIONAL

---

### NPI Search (Home Health Agencies)
**Tool:** `npi_search` (National Provider Identifier)
**Test Query:** Taxonomy "Home Health" in California

**Results (2 records returned):**

1. **1 & 1 HOME HEALTH, INC.**
   - NPI: 1962743146
   - Type: Organization (NPI-2)
   - Primary Address: 1075 YORBA PL, PLACENTIA, CA 92870
   - Phone: 800-940-7659
   - Taxonomy: Home Health (251E00000X)

2. **1 ACT HEALTHCARE CORP**
   - NPI: 1669047619
   - Type: Organization (NPI-2)
   - Primary Address: 15480 ARROW HWY STE 205, BALDWIN PARK, CA 91706
   - Phone: 626-364-7079
   - Taxonomy: Home Health (251E00000X)

**Status:** ✅ OPERATIONAL

---

### CMS Local Coverage Determination (LCD) Search
**Tool:** `search_local_coverage` (Medicare coverage policies)
**Test Query:** Keyword "home health", limit 2 results

**Results (2 LCDs returned):**

1. **Physical Therapy - Home Health**
   - Document ID: L33942 (Version 49)
   - Contractor: CGS Administrators, LLC (HHH MAC)
   - Effective Date: 08/07/2025
   - Last Updated: 07/29/2025
   - URL: https://www.cms.gov/medicare-coverage-database/view/lcd.aspx?lcdid=33942&ver=49

2. **Home Health Skilled Nursing Care-Teaching and Training: Alzheimer's Disease and Behavioral Disturbances**
   - Document ID: L34562 (Version 45)
   - Contractor: Palmetto GBA (HHH MAC)
   - Effective Date: 08/07/2025
   - Last Updated: 07/28/2025
   - URL: https://www.cms.gov/medicare-coverage-database/view/lcd.aspx?lcdid=34562&ver=45

**Status:** ✅ OPERATIONAL

---

## Getting Started

### To Create a New Report
1. Choose the appropriate template from `/templates/`
2. Copy it to the relevant folder in the workspace (e.g., `/qapi/reports/` for a quarterly report)
3. Rename following the convention: `YYYY-MM-DD-[description].md`
4. Fill in placeholders `[LIKE THIS]` with actual data
5. Update internal links if referencing other documents

### To Import Manual Data
1. Use the template in `/data/qapi-manual-input-template.csv`
2. Fill in patient episodes (one row per patient episode)
3. Save as: `YYYY-MM-DD-[agency-name]-patient-data.csv`
4. Move to `/data/` folder for processing

### To Track Quality Performance
1. Check `/qapi/reports/` for latest quarterly QAPI report
2. Review active PIPs in `/qapi/pips/`
3. Check `/outcomes/dashboards/` for STAR rating and payment estimates
4. Track high-risk patients in `/outcomes/high-risk/`

---

## Integration Notes

- **Data Flow:** Manual data → `/data/` → Processing → `/qapi/reports/`, `/outcomes/dashboards/`, `/qapi/pips/`
- **Regulatory Intelligence:** `/regulatory/digests/` → Impact analyses → PIP triggers in `/qapi/pips/`
- **Survey Prep:** Gaps in `/survey-readiness/gap-lists/` → PIPs → POC in `/survey-readiness/poc/`
- **Patient Safety:** Hospitalizations → `/outcomes/rca/` → High-risk flagging in `/outcomes/high-risk/`

---

**Last Updated:** April 4, 2026
**Verified By:** Enzo Health Founding Engineer (FE-1)
**Next Review:** Q2 2026
