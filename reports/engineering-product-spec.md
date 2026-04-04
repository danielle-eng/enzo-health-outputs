# Enzo Health — Engineering Product Specification
## SaaS Platform for Home Health Compliance & Revenue Operations

**Document Version:** 1.0
**Last Updated:** April 4, 2026
**Audience:** Engineering Team
**Status:** In Development — Ready for Production Build

---

## 1. Product Vision

Enzo Health is building the **daily operating system for home health compliance and revenue** — not a quarterly reporting tool. The core insight is that home health agencies need to know, *every morning*, where they stand on compliance and revenue health.

**Mission:** Enable Director of Nursing (DON) and Agency Administrator leaders to make informed operational decisions daily, powered by overnight AI agent analysis.

**Success Metric:** Agencies log in daily (not quarterly) to view their action list, understand priority deficiencies, and track progress toward survey readiness.

### Why "Daily" Matters
- Surveys are unannounced; agencies must be perpetually survey-ready
- Compliance issues compound; early detection prevents deficiency stacks
- Revenue leakage (missed billing, PDGM miscodings) is measured in real dollars per day
- The product is a habit → log in, see what changed overnight, act, move on

---

## 2. User Personas & Dashboard Requirements

### Persona 1: Director of Nursing (DON)
**Role:** Clinical and compliance ownership; survey defensibility.
**Time Commitment:** 15 minutes daily.
**Key Questions:**
- Are we survey-ready right now?
- What clinical documentation is deficient?
- Which visits are out of compliance?
- What's trending positively/negatively?

**Dashboard Structure:**
- Hero Metric: **Survey Readiness Score** (0–100)
- Today's Action List (Critical → Important → FYI)
- 7-day Survey Readiness trend sparkline
- Rolling 30/60/90-day quality indicator cards (selectable period)
- Deficiency status summary with deadline alerts

### Persona 2: Agency Administrator / Operations Director
**Role:** Financial and operational ownership; revenue optimization.
**Time Commitment:** 20 minutes daily.
**Key Questions:**
- What's our billing health?
- Are we capturing all revenue?
- Which claims are at risk of denial?
- What PDGM coding issues exist?

**Dashboard Structure:**
- Hero Metric: **Revenue Health Score** (0–100, composite of billing accuracy, PDGM coding quality, claim denial rate)
- Today's Action List (Critical → Important → FYI)
- 30/60/90-day billing quality trend with period selector
- QAPI continuous monitoring status
- Upcoming regulatory deadlines

### Role-Based Views (Database & API)
| Role | Features | Data Access |
|------|----------|-------------|
| DON | Survey Readiness, Clinical QA, Visit Compliance, Deficiency Tracker | All clinical data, read-only deficiency view, can assign/acknowledge tasks |
| Admin | Revenue Health, Billing QA, PDGM issues, QAPI monitoring | All operational data, can modify billing corrections, track claims |
| Owner | All DON + Admin features, plus agency config, user management, billing | Full read/write on all modules |
| Enzo Staff (read-only) | Dashboard view-only, no action capability | Per-agency audit access for support |

---

## 3. Survey Readiness Score (Build First — Core Feature)

### Formula & Components
The Survey Readiness Score (0–100) is the primary metric for DON daily engagement. It represents the agency's probability of passing an unannounced Medicare survey *today*.

**Score Composition:**
- **Documentation Quality** (30 points): OASIS timing, completeness, clinical accuracy
- **Visit Compliance** (20 points): HIS compliance, frequency compliance, homebound status validation
- **OASIS Accuracy** (20 points): Item accuracy vs. clinical record, prior assessments, discharge validation
- **Care Planning** (15 points): POC completeness, discipline coordination, skilled nursing justification
- **Open Deficiencies** (15 points): Any unresolved prior survey deficiencies or immediate risk items

**Score Bands:**
```
90–100   = Survey Ready (green)
70–89    = Moderate Risk (yellow)
50–69    = Elevated Risk (orange)
0–49     = High Risk (red)
```

### Database Schema
```sql
-- Survey Readiness Score History (time-series)
CREATE TABLE survey_readiness_scores (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  score_date DATE NOT NULL,  -- date of calculation
  overall_score INT NOT NULL CHECK (overall_score >= 0 AND overall_score <= 100),
  documentation_quality INT NOT NULL,
  visit_compliance INT NOT NULL,
  oasis_accuracy INT NOT NULL,
  care_planning INT NOT NULL,
  open_deficiencies INT NOT NULL,
  calculated_at TIMESTAMP DEFAULT NOW(),
  created_by UUID REFERENCES users(id),  -- which agent calculated this

  UNIQUE(agency_id, score_date),
  CONSTRAINT agency_isolation CHECK (agency_id IS NOT NULL)
);

-- Score component details (drilldown)
CREATE TABLE survey_readiness_components (
  id BIGSERIAL PRIMARY KEY,
  score_id BIGINT NOT NULL REFERENCES survey_readiness_scores(id) ON DELETE CASCADE,
  component_type VARCHAR(50) NOT NULL,  -- 'documentation_quality', 'visit_compliance', etc.
  finding_count INT NOT NULL,  -- number of issues in this component
  finding_examples JSONB,  -- array of specific issues: [{type, record_id, description}, ...]
  remediation_task_ids UUID[],  -- links to action_items table

  INDEX ON score_id
);
```

### Daily Calculation & Overnight Agent Run
- **Trigger:** 11:00 PM UTC (customizable per agency)
- **Agent:** Uses OASIS QA, Clinical Documentation QA, Visit Compliance agents to gather metrics
- **Calculation:** Weighted algorithm sums components, normalizes to 0–100
- **Persistence:** New row in `survey_readiness_scores` for each date (enables trend calculation)
- **Retention:** Keep full history (no archival)

### Dashboard Display
```
Survey Readiness Score
┌─────────────────────────────────────┐
│  82 / 100    Survey Ready  ✓        │  ← Hero metric, large font
│  ↑ +3 from yesterday                │  ← Delta indicator
│                                     │
│  7-day trend: 78→79→80→79→81→82    │  ← Sparkline chart
│  30 days: +5 points trending up     │
│                                     │
│  [View Drilldown] [View Deficiencies] │
└─────────────────────────────────────┘
```

### Drilldown Feature (Click Any Component)
When DON clicks "Documentation Quality," page shows:
- All issues contributing to this score (missing timelines, incomplete fields, clinical inconsistencies)
- Specific visit/record affected
- Recommended remediation
- Button to create action item

---

## 4. QAPI Continuous Monitoring (vs. Quarterly Report)

### What It Is
Instead of running QA once per quarter and writing a report, QAPI continuously measures quality across a rolling 30/60/90-day window and feeds into the daily dashboard.

### Core Components
**Rolling Quality Indicators Table:**
```sql
CREATE TABLE quality_indicators (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  indicator_date DATE NOT NULL,  -- date of measurement
  indicator_type VARCHAR(100) NOT NULL,  -- 'hchb_visit_frequency', 'oasis_accuracy_pct', 'care_plan_completeness', ...
  value DECIMAL(5,2) NOT NULL,  -- 0–100, or actual count
  measurement_period_days INT NOT NULL,  -- 30, 60, or 90
  national_benchmark DECIMAL(5,2),  -- from live CMS data
  agency_benchmark DECIMAL(5,2),  -- agency-specific target
  variance_from_benchmark DECIMAL(6,2),  -- negative = worse than benchmark

  UNIQUE(agency_id, indicator_date, indicator_type, measurement_period_days),
  INDEX (agency_id, indicator_date)
);

-- PIP (Plan of Improvement) Tracker
CREATE TABLE pips (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  quality_indicator_id BIGINT REFERENCES quality_indicators(id),
  pip_description TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'active',  -- 'active', 'on_track', 'at_risk', 'completed'
  start_date DATE NOT NULL,
  target_completion_date DATE NOT NULL,
  current_value DECIMAL(5,2),
  target_value DECIMAL(5,2),
  progress_pct INT,
  interventions JSONB,  -- [{intervention, owner, deadline, completion_status}, ...]
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### CMS CASPER Integration
**Requirement:** Fetch live national/state benchmarks from CMS CASPER API (quarterly update minimum).
- Endpoint: `https://data.cms.gov/api/timeseries?domain=home_health_quality`
- Data needed: Top 10 quality indicators by state
- Caching strategy: Pull monthly; invalidate on demand via admin dashboard
- Storage: Cache in `agency_benchmarks` table with refresh_at timestamp

### Governing Body Package Auto-Generation
- **Trigger:** Quarterly (Jan 1, Apr 1, Jul 1, Oct 1) or on-demand
- **Contents:** Executive summary of QAPI findings, PIP status, benchmark comparison, recommendations
- **Output:** PDF document auto-generated from `quality_indicators` + `pips` tables
- **Engineering:** Template engine (Jinja2) + WeasyPrint for PDF generation; store PDF in S3 with audit log

### Dashboard Display
```
QAPI Monitoring — Last 90 Days
┌────────────────────────────────────────┐
│ HIS Compliance         87% ↑2%          │
│ vs. CMS National Avg   85%  ✓ ahead     │
│                                        │
│ OASIS Accuracy         82% ↓1%          │
│ vs. CMS National Avg   88%  ! behind    │
│                                        │
│ PIPs: 2 Active, 1 At Risk               │
│ │ Missing Physician Orders (due 5/1)    │
│ │ → 65% complete, on track             │
│                                        │
│ [View Full Quality Report]              │
└────────────────────────────────────────┘
```

---

## 5. Survey Readiness Deficiency Tracker

### Why This Exists
When an agency receives a survey deficiency, they must:
1. Document exactly what was cited
2. Plan how to fix it (Plan of Correction)
3. Track submission and CMS verification
4. Prevent repeat deficiencies

This module provides persistent, trackable workflow for all of the above.

### Database Schema
```sql
CREATE TABLE survey_deficiencies (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  survey_date DATE NOT NULL,
  deficiency_status VARCHAR(50) DEFAULT 'open',  -- 'open', 'poc_in_review', 'submitted', 'verified_closed', 'unresolved'
  cms_citation VARCHAR(20),  -- e.g., '42 CFR 484.12(c)(2)'
  description TEXT NOT NULL,
  severity VARCHAR(50),  -- 'scope_severity', 'pattern', 'isolated'
  due_date_poc DATE NOT NULL,  -- CMS deadline for POC submission

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (agency_id, deficiency_status)
);

CREATE TABLE plan_of_correction (
  id BIGSERIAL PRIMARY KEY,
  deficiency_id BIGINT NOT NULL REFERENCES survey_deficiencies(id) ON DELETE CASCADE,
  status VARCHAR(50) DEFAULT 'draft',  -- 'draft', 'in_review', 'submitted_to_cms', 'verified_closed'
  description TEXT NOT NULL,
  root_cause TEXT,
  interventions TEXT[],  -- array of corrective actions
  responsible_person_id UUID REFERENCES users(id),
  implementation_start DATE,
  implementation_end DATE,
  metrics_for_verification TEXT[],  -- how CMS will verify compliance
  evidence_documents JSONB,  -- [{doc_type, uploaded_file_id, upload_date}, ...]

  submitted_to_cms_at TIMESTAMP,
  cms_verification_received_at TIMESTAMP,
  cms_verification_result VARCHAR(50),  -- 'accepted', 'rejected', 'pending'

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (deficiency_id)
);

-- Track repeat deficiencies
CREATE TABLE deficiency_patterns (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  cms_citation VARCHAR(20) NOT NULL,
  citation_type VARCHAR(100),  -- full citation description
  occurrence_count INT DEFAULT 1,
  first_cited_date DATE,
  most_recent_date DATE,

  UNIQUE(agency_id, cms_citation),
  INDEX (agency_id, occurrence_count DESC)
);
```

### Deficiency Tracker Dashboard
```
Survey Deficiencies — Current Status
┌──────────────────────────────────────┐
│ Open: 3  In Review: 1  Submitted: 0  │
│                                      │
│ 1. 42 CFR 484.12(c)(2)               │
│    Documentation Timeliness          │
│    Due: May 1, 2026 (27 days)        │
│    Severity: Scope & Severity        │
│    Status: Draft POC                 │
│    [Edit POC] [Submit to CMS]        │
│                                      │
│ 2. 42 CFR 484.48(a)(1)               │
│    Care Plan Documentation           │
│    Due: April 15, 2026 (11 days)   │ ← Red: urgent
│    Severity: Isolated                │
│    Status: In Review                 │
│    Assigned to: Jane Smith           │
│    [View Details]                    │
└──────────────────────────────────────┘
```

### Alerts & Notifications
- **7-day alert:** "Deficiency due in 7 days — POC must be submitted by [date]"
- **3-day alert:** "URGENT: Deficiency due in 3 days"
- **On submission:** Email to DON confirming CMS receipt
- **On CMS verification:** Dashboard badge indicating closure

---

## 6. Action Tracking & Audit Trail

### Core Concept
Every agent recommendation and manual task becomes an action item that can be:
- Assigned to a user with a due date
- Tracked through status workflow
- Audited for survey defensibility

### Database Schema
```sql
CREATE TABLE action_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,

  -- Origin & Classification
  source VARCHAR(50),  -- 'agent_recommendation', 'manual_task', 'deficiency_remediation', 'survey_preparation'
  agent_type VARCHAR(50),  -- 'clinical_documentation_qa', 'visit_compliance', 'billing_qa', etc.

  -- Status & Assignment
  status VARCHAR(50) DEFAULT 'new',  -- 'new', 'acknowledged', 'in_progress', 'resolved', 'closed'
  assigned_to_id UUID REFERENCES users(id),
  due_date DATE,
  completed_at TIMESTAMP,
  closed_at TIMESTAMP,

  -- Evidence & Notes
  supporting_data JSONB,  -- {visit_id, record_id, metric_name, affected_patients, ...}
  resolution_notes TEXT,
  resolution_evidence_file_ids UUID[],

  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT agency_isolation CHECK (agency_id IS NOT NULL),
  INDEX (agency_id, status),
  INDEX (agency_id, due_date),
  INDEX (assigned_to_id)
);

-- Audit trail for every state change
CREATE TABLE action_item_audit_log (
  id BIGSERIAL PRIMARY KEY,
  action_item_id UUID NOT NULL REFERENCES action_items(id) ON DELETE CASCADE,
  previous_status VARCHAR(50),
  new_status VARCHAR(50) NOT NULL,
  changed_by_id UUID NOT NULL REFERENCES users(id),
  change_timestamp TIMESTAMP DEFAULT NOW(),
  change_reason TEXT,  -- why the status changed

  INDEX (action_item_id, change_timestamp DESC)
);
```

### Action List Tiers
**Critical (Red):**
- Deficiency due within 3 days
- Survey risk identified (e.g., homebound status issue affecting 5+ patients)
- Billing issue affecting >$10K revenue
- CMS compliance violation

**Important (Yellow):**
- Deficiency due within 30 days
- Survey risk identified (affects 1–2 patients)
- Process improvement recommendations
- Quality metric below target

**FYI (Gray):**
- Informational updates
- Trend notifications
- Benchmark comparisons
- Weekly summary items

---

## 7. Notification System

### Architecture
Multi-channel notification system with agency-level configuration and user-level preferences.

### Channels
1. **In-App Badge:** Unread notification count; clicking opens notification center
2. **Daily Email Digest:** 7:00 AM local time; all overnight agent findings + new action items
3. **Slack/Teams Real-Time:** Critical alerts only (when user has integrated Slack)
4. **Weekly Summary Email:** Friday 5:00 PM; FYI items + trend summary

### Database Schema
```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  recipient_user_id UUID REFERENCES users(id),

  title VARCHAR(255) NOT NULL,
  message TEXT,
  notification_type VARCHAR(50),  -- 'deficiency_alert', 'quality_metric', 'task_assigned', 'survey_risk', 'billing_issue'
  urgency VARCHAR(50) DEFAULT 'normal',  -- 'critical', 'important', 'fyi'

  action_item_id UUID REFERENCES action_items(id),
  deficiency_id BIGINT REFERENCES survey_deficiencies(id),
  quality_indicator_id BIGINT REFERENCES quality_indicators(id),

  created_at TIMESTAMP DEFAULT NOW(),
  read_at TIMESTAMP,
  read_via VARCHAR(50),  -- 'web', 'email', 'slack'

  CONSTRAINT agency_isolation CHECK (agency_id IS NOT NULL),
  INDEX (agency_id, created_at DESC),
  INDEX (recipient_user_id, read_at)
);

CREATE TABLE notification_deliveries (
  id BIGSERIAL PRIMARY KEY,
  notification_id UUID NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
  channel VARCHAR(50) NOT NULL,  -- 'email', 'slack', 'teams', 'sms'
  delivery_status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'sent', 'failed', 'bounced'
  sent_at TIMESTAMP,
  delivery_id VARCHAR(255),  -- external service ID (SendGrid, Slack, etc.)
  error_message TEXT,

  INDEX (notification_id, channel)
);

-- Agency notification preferences
CREATE TABLE agency_notification_preferences (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL UNIQUE REFERENCES agencies(id) ON DELETE CASCADE,

  -- Channel enablement
  email_digest_enabled BOOLEAN DEFAULT TRUE,
  email_digest_time TIME DEFAULT '07:00:00',  -- 7:00 AM
  slack_enabled BOOLEAN DEFAULT FALSE,
  slack_webhook_url TEXT ENCRYPTED,  -- use pgcrypto
  teams_enabled BOOLEAN DEFAULT FALSE,
  teams_webhook_url TEXT ENCRYPTED,

  -- Routing rules by urgency
  critical_to_email BOOLEAN DEFAULT TRUE,
  critical_to_slack BOOLEAN DEFAULT TRUE,
  important_to_email BOOLEAN DEFAULT TRUE,
  important_to_slack BOOLEAN DEFAULT FALSE,
  fyi_to_email BOOLEAN DEFAULT FALSE,

  -- Event routing
  deficiency_alerts_enabled BOOLEAN DEFAULT TRUE,
  billing_alerts_enabled BOOLEAN DEFAULT TRUE,
  survey_prep_alerts_enabled BOOLEAN DEFAULT TRUE,
  quality_metric_alerts_enabled BOOLEAN DEFAULT TRUE,

  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Notification Service Implementation
**Tech:** FastAPI background task queue (Celery + Redis)

**Flow:**
1. Agent or user action triggers notification event
2. Event written to notification table
3. Celery task `dispatch_notification` reads preferences
4. Route to appropriate channels (email via SendGrid, Slack via API, in-app badge)
5. Log delivery status in `notification_deliveries`

**Email Template Example:**
```
Subject: Enzo Daily Digest — 3 new action items

Hi [First Name],

Here's your agency update for [Date]:

CRITICAL (Needs Today)
• Deficiency due April 15 — POC review pending
  [Review Now →]

IMPORTANT (This Week)
• Visit Compliance: 2 cases missing physician order within 48h
  [See Details →]

FYI (Informational)
• Survey Readiness Score up to 82 (+2 from yesterday)
• Quality benchmark: HIS compliance 87% (↑2%)

[View Full Dashboard →]
```

---

## 8. Multi-Tenant Architecture Requirements

### Agency Isolation
Every data query must include `agency_id` filter. Use Row-Level Security (RLS) in PostgreSQL to enforce.

```sql
-- Enable RLS on all multi-tenant tables
ALTER TABLE survey_readiness_scores ENABLE ROW LEVEL SECURITY;

CREATE POLICY agency_isolation_policy ON survey_readiness_scores
  USING (agency_id = current_setting('app.current_agency_id')::UUID);

-- Apply to all multi-tenant tables:
-- agencies, users, action_items, notifications, survey_deficiencies, quality_indicators, pips, etc.
```

### Role-Based Access Control (RBAC)
```sql
CREATE TABLE user_roles (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  role VARCHAR(50) NOT NULL,  -- 'don', 'admin', 'owner', 'enzo_staff'

  UNIQUE(user_id, agency_id),
  INDEX (agency_id, role)
);

-- Permissions table (if needed for fine-grained control)
CREATE TABLE role_permissions (
  role VARCHAR(50) NOT NULL,
  permission VARCHAR(100) NOT NULL,  -- 'view_survey_readiness', 'create_action_item', 'assign_task', etc.

  UNIQUE(role, permission)
);
```

**Role Permission Matrix:**

| Feature | DON | Admin | Owner | Enzo Staff |
|---------|-----|-------|-------|-----------|
| View Survey Readiness | RW | R | RW | R |
| View Revenue Health | R | RW | RW | R |
| Create Action Item | C | C | C | - |
| Assign Task | R | R | RW | - |
| Access Deficiency Tracker | RW | R | RW | R |
| Submit POC to CMS | RW | - | RW | - |
| View Audit Log | R | R | RW | R |
| Configure Notifications | R | R | RW | - |
| Manage Users | - | - | RW | - |
| View Billing Data | R | RW | RW | R |

### Per-Agency Configuration
```sql
CREATE TABLE agency_configs (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL UNIQUE REFERENCES agencies(id) ON DELETE CASCADE,

  -- Care settings
  care_setting VARCHAR(50),  -- 'home_health', 'hospice', 'mixed'

  -- Benchmarks & targets
  survey_readiness_target INT DEFAULT 85,
  his_compliance_target DECIMAL(5,2) DEFAULT 95.0,
  oasis_accuracy_target DECIMAL(5,2) DEFAULT 90.0,

  -- EMR Integration
  emr_system VARCHAR(50),  -- 'hchb', 'wellsky', 'matrixcare', 'axxess', 'manual'
  emr_api_key TEXT ENCRYPTED,
  emr_client_id TEXT ENCRYPTED,
  emr_last_sync_at TIMESTAMP,

  -- Scheduling
  agent_run_time TIME DEFAULT '23:00:00',  -- 11 PM UTC
  agent_run_timezone VARCHAR(50) DEFAULT 'America/New_York',

  -- CMS settings
  provider_id VARCHAR(10),  -- CMS provider number
  clia_number VARCHAR(10),
  state_license_number VARCHAR(50),

  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 9. EMR Connector Roadmap

### Priority Order (Build Sequence)
1. **Homecare Homebase (HCHB)** — ~35% market share; most frequently requested
2. **WellSky (formerly Kinnser)** — ~25% market share; strong mid-market presence
3. **MatrixCare** — ~15% market share; significant hospice penetration
4. **Axxess** — ~10% market share; growing mid-market segment
5. **Manual CSV Upload** — fallback for unsupported agencies; daily file drop into SFTP

### Connector Framework
```python
# Abstract base class all connectors inherit from
class EMRConnector:
    def authenticate(self) -> bool:
        """Test API credentials; return True/False"""
        pass

    def fetch_patients(self, date_range: tuple) -> List[Patient]:
        """Fetch patient roster with demographics"""
        pass

    def fetch_visits(self, date_range: tuple) -> List[Visit]:
        """Fetch visit logs with admission, note times, disciplines"""
        pass

    def fetch_clinical_notes(self, visit_id: str) -> str:
        """Fetch visit note text for clinical QA agents"""
        pass

    def fetch_oasis_data(self, patient_id: str) -> Dict:
        """Fetch latest OASIS assessment"""
        pass

    def fetch_care_plan(self, patient_id: str) -> Dict:
        """Fetch plan of care"""
        pass

    def log_sync_event(self, status: str, record_count: int):
        """Record sync success/failure for monitoring"""
        pass

# Example: HCHB Connector
class HCHBConnector(EMRConnector):
    def __init__(self, client_id: str, api_key: str):
        self.base_url = "https://api.homecarehomebase.com/v2"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def fetch_visits(self, date_range):
        # Implement HCHB API pagination
        # GET /patients/{id}/visits?start_date=&end_date=
        pass
```

### Webhook Support
EMR systems that support webhooks should push data updates in real-time:
- **Trigger:** Patient admission, visit logged, OASIS submitted
- **Endpoint:** `POST /api/v1/webhooks/emr/{connector_type}`
- **Payload:** Event type, patient ID, visit ID, timestamp
- **Response:** 200 OK with retry count for failures

### Database Schema
```sql
CREATE TABLE emr_syncs (
  id BIGSERIAL PRIMARY KEY,
  agency_id UUID NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
  connector_type VARCHAR(50) NOT NULL,  -- 'hchb', 'wellsky', 'matrixcare', 'axxess', 'manual'

  sync_status VARCHAR(50),  -- 'pending', 'in_progress', 'success', 'partial_failure', 'failed'
  records_synced INT,
  records_failed INT,
  error_message TEXT,

  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,

  INDEX (agency_id, completed_at DESC)
);
```

---

## 10. What's Already Built — Agent Layer

### 12 Agents Deployed
1. **Intake/Referral Agent** — Validates new patient referrals; flags missing required data
2. **OASIS QA Agent** — Checks OASIS assessment completeness and clinical logic
3. **PDGM/Billing Agent** — Validates PDGM coding; identifies billing errors
4. **Scheduling Agent** — Checks visit frequency compliance (60-day window, frequency rules)
5. **Clinical Documentation QA Agent** — Analyzes visit notes for completeness, timeliness, clinical justification
6. **Survey Readiness Agent** — Aggregates findings from all other agents; calculates daily score
7. **QAPI Agent** — Calculates rolling quality indicators; tracks PIPs
8. **Outcomes/HHVBP Agent** — Tracks HHVBP outcome measures and benchmarks
9. **Regulatory Intelligence Agent** — Scans CMS updates; alerts on new regulations
10. **Recertification/Discharge Agent** — Validates discharge planning and recert windows
11. **Founding Engineer** — Real-time code debugging and architecture validation
12. **CEO Agent** — Executive summary generation; market opportunity tracking

**Each agent:**
- Is a standalone Python script (location: `/agents/{agent_name}/agent.py`)
- Has input spec (what data it consumes) and output spec (what it produces)
- Has an AGENTS.md documenting assumptions, known limitations, and sample data usage
- Currently runs on sample data (JSON fixtures); needs live EMR connector wiring

### Agent Execution Pipeline
```
[Nightly Trigger @ 11 PM]
  ↓
[Enzo Scribe Connector] → fetch clinical notes, OASIS, care plan
  ↓
[Parallel Agent Execution]
  ├─→ OASIS QA Agent
  ├─→ Clinical Documentation QA Agent
  ├─→ Visit Compliance Agent
  ├─→ PDGM Billing Agent
  └─→ Care Planning Agent
  ↓
[Survey Readiness Agent] → aggregates findings → calculates score
  ↓
[QAPI Agent] → calculates quality indicators
  ↓
[Output] → Write to database (scores, metrics, action items)
  ↓
[Notification Service] → Dispatch morning digest
```

**Current State:**
- All agent logic is functional
- Agent code is testable and works on sample data
- Integration points defined but not wired to live EMR
- No persistent storage (agents currently output JSON; not saved)

---

## 11. Gap Summary — Priority Build Order

### Phase 1: Foundation (Weeks 1–4)
**Blocker for everything else:**

1. **Authentication & User Management**
   - Implement Clerk or Auth0 integration
   - SSO for enterprise customers
   - Role provisioning on login
   - User role/permission enforcement in FastAPI middleware
   - Estimated effort: 2 weeks

2. **Database Persistence Layer**
   - PostgreSQL multi-tenant schema (RLS)
   - `survey_readiness_scores`, `quality_indicators`, `pips`, `action_items` tables
   - `agency_configs` for per-agency settings
   - Connection pooling and migration tools
   - Estimated effort: 1.5 weeks

3. **Scheduled Agent Runner**
   - Move from Railway manual triggers to Celery Beat (or Railway cron)
   - Daily 11 PM UTC agent orchestration
   - Error handling and retry logic
   - Agent output → database insertion
   - Estimated effort: 1 week

### Phase 2: Core Daily Experience (Weeks 5–10)
4. **Survey Readiness Score Module**
   - Dashboard display with trend sparkline
   - Drilldown pages for each component
   - Database persistence and daily calculation
   - Estimated effort: 2 weeks

5. **Notification Service**
   - Multi-channel routing (email, Slack, in-app badge)
   - Agency-level configuration UI
   - Daily digest generation and SendGrid integration
   - Estimated effort: 2 weeks

6. **QAPI Continuous Monitoring**
   - Quality indicator calculation and storage
   - CMS benchmark fetching (CASPER API)
   - PIP tracker UI
   - Estimated effort: 1.5 weeks

7. **Action Tracking & Audit Trail**
   - Action item creation, assignment, status workflow
   - Audit log for every state change
   - Assignment to user → due date → completion tracking
   - Estimated effort: 1.5 weeks

### Phase 3: Compliance Workflows (Weeks 11–14)
8. **Deficiency Tracker & POC Workflow**
   - Deficiency logging with CMS citation
   - Plan of Correction drafting and review
   - CMS submission tracking
   - Deadline alerts and repeat deficiency detection
   - Estimated effort: 2 weeks

9. **Dashboard Build-Out**
   - DON role dashboard (Survey Readiness hero metric, clinical view)
   - Admin role dashboard (Revenue Health hero metric, billing view)
   - Role-based access enforcement
   - Estimated effort: 2 weeks

### Phase 4: EMR Integration & Scale (Weeks 15–24)
10. **EMR Connector Framework**
    - Abstract connector base class
    - HCHB connector implementation + testing
    - Authentication, pagination, error handling
    - Sync monitoring and retry logic
    - Estimated effort: 4 weeks

11. **WellSky Connector**
    - Estimated effort: 2 weeks (reuse framework)

12. **MatrixCare & Axxess Connectors**
    - Estimated effort: 2 weeks each

13. **Policy & Procedure Management** (Stretch)
    - CMS policy library integration
    - Agency procedure documentation
    - Compliance mapping
    - Estimated effort: 2 weeks

14. **Multi-Branch/Multi-Agency Support** (Stretch)
    - Consolidate agencies under single owner account
    - Roll-up reporting and cross-agency insights
    - Estimated effort: 1 week

---

## 12. Tech Stack Recommendation

### Backend
- **Language:** Python (already used for all agents)
- **Framework:** FastAPI (async, built-in dependency injection, auto-generated docs)
- **Database:** PostgreSQL 14+ (RLS for multi-tenancy, JSONB, full-text search)
- **Job Scheduler:** Celery + Redis (for agent orchestration) *or* Railway Cron (if staying simple)
- **Connection Pool:** SQLAlchemy + psycopg2 (synchronous) or asyncpg (async)

### Frontend
- **Framework:** React 18+
- **Styling:** Tailwind CSS (matches design system expectations)
- **State Management:** TanStack Query (data fetching + caching)
- **Charts:** Recharts or Victory (sparklines, quality indicator trends)
- **UI Components:** shadcn/ui (Tailwind-based, accessible components)
- **Deployment:** Vercel or Netlify (CI/CD, edge functions)

### Authentication
- **Provider:** Clerk or Auth0 (both support SSO, webhooks, RBAC)
- **Flow:** OAuth 2.0; zero handling of passwords
- **Integration:** FastAPI middleware for token validation and role injection

### Notifications
- **Email:** SendGrid (transactional + bulk digest)
- **Slack:** Slack API (webhook for real-time; app for advanced features)
- **Teams:** Microsoft Teams Connector API
- **In-App:** WebSockets + Redis Pub/Sub (for real-time badge updates)

### Data Connectors
- **EMR APIs:** HTTP clients (httpx, aiohttp) with retry logic
- **CMS Data:** requests library for CASPER API polling
- **Enzo Scribe:** Already built; integrate via webhook

### Infrastructure
- **Hosting:** Railway (already deployed; supports Python, PostgreSQL, Redis)
- **Storage:** AWS S3 or Cloudflare R2 (for uploaded POC evidence files, PDF reports)
- **Monitoring:** DataDog or New Relic (APM, error tracking, dashboards)
- **Logging:** Structured logging (python-json-logger) → CloudWatch or DataDog
- **CI/CD:** GitHub Actions (already set up)

### Development Tools
- **Package Manager:** Poetry (Python dependency management)
- **Testing:** pytest + pytest-cov (unit + integration tests)
- **Linting:** ruff (Python linter; faster than flake8)
- **Type Checking:** mypy (static type checking)
- **API Docs:** FastAPI auto-generates OpenAPI 3.0 + Swagger UI
- **Database Migrations:** Alembic (SQL version control)

### Security
- **Encryption:** pgcrypto (in-database encryption for API keys, webhook secrets)
- **Secrets Management:** Railway secrets or AWS Secrets Manager
- **HTTPS:** Let's Encrypt (auto-renewal via Railway)
- **CORS:** FastAPI middleware configured per environment
- **Rate Limiting:** FastAPI + slowapi (to prevent abuse)

---

## 13. Detailed Build Specification — Phase 1 (Week 1)

### Task 1.1: PostgreSQL Schema Setup
**Deliverable:** `/database/schema.sql`

**Create tables:**
- `agencies` (id, name, provider_id, state, created_at)
- `users` (id, email, first_name, last_name, auth_provider_id, created_at)
- `user_roles` (user_id, agency_id, role, created_at)
- `survey_readiness_scores` (with full time-series structure from Section 3)
- `action_items` (with audit trail from Section 6)
- `notifications` (with delivery log from Section 7)
- `agency_configs` (from Section 8)

**Add constraints:**
- RLS policies on all multi-tenant tables
- Foreign key cascades
- Unique constraints on (agency_id, date) pairs for time-series

**Status:** Ready to implement

### Task 1.2: FastAPI Project Scaffold
**Deliverable:** `/backend/` directory structure

```
backend/
├── main.py                 # FastAPI app initialization
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── config.py              # Settings management
├── database.py            # SQLAlchemy session + engine
├── middleware/
│   ├── auth.py            # Clerk/Auth0 token validation
│   ├── error_handler.py    # Global error handling
│   └── logging.py         # Structured logging
├── models/                # SQLAlchemy ORM models
│   ├── agency.py
│   ├── user.py
│   ├── survey_readiness.py
│   ├── action_item.py
│   └── notification.py
├── schemas/               # Pydantic request/response schemas
│   ├── agency.py
│   ├── action_item.py
│   └── notification.py
├── routes/                # API endpoints
│   ├── auth.py            # Login, logout, profile
│   ├── dashboard.py       # GET /dashboard (hero metrics, action list)
│   ├── action_items.py    # CRUD for action_items
│   ├── notifications.py   # GET /notifications, mark-read
│   └── admin.py           # Agency config endpoints
├── agents/                # Symlink to /agents for imports
└── tests/
    ├── test_auth.py
    ├── test_dashboard.py
    └── test_action_items.py
```

**Dependencies to install:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9  # or psycopg[binary]
alembic==1.13.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0  # for token validation
httpx==0.25.1
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
```

**Status:** Ready to implement

### Task 1.3: Clerk Integration
**Deliverable:** Auth middleware + user provisioning

**Steps:**
1. Create Clerk app in Clerk Dashboard
2. Add `/api/auth/callback` endpoint to receive user data on login
3. Implement middleware to validate JWT from Clerk
4. On first login, create `users` record and assign default role
5. Inject user context into request (`request.state.user`, `request.state.agency_id`)

**Code outline (FastAPI middleware):**
```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
import httpx

async def verify_clerk_token(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    # Verify token with Clerk's JWKS endpoint
    # (Clerk provides a library; use clerk-sdk-python)

    user_id = decode_token(token)
    db_user = session.query(User).filter(User.auth_provider_id == user_id).first()
    request.state.user = db_user
    request.state.agency_id = db_user.user_roles[0].agency_id
```

**Status:** Ready to implement

---

## 14. Success Metrics & Launch Criteria

### Product Success Metrics
- **Daily Active Users:** Target >70% of agency users logging in 5+ days/week
- **Time to Action:** Average time from alert → action item creation <2 minutes
- **Survey Readiness Trend:** Agencies using platform for >60 days show +15% avg score improvement
- **Deficiency Resolution:** 95% of logged deficiencies result in completed POC (not pending)

### Technical Success Metrics
- **API Uptime:** 99.5% target
- **Dashboard Load Time:** <2 seconds (p95)
- **Notification Delivery:** 99% within 5 minutes of trigger
- **Database Query Performance:** <500ms (p95) on all dashboard queries
- **Agent Reliability:** >95% success rate on nightly runs

### Launch Readiness Checklist
- [ ] PostgreSQL schema migrated and tested
- [ ] FastAPI scaffold deployed to staging
- [ ] Clerk authentication tested end-to-end
- [ ] Survey Readiness Score calculation logic implemented
- [ ] Daily agent orchestration running consistently
- [ ] Email digest template and SendGrid integration working
- [ ] Dashboard UI displaying hero metric and action list
- [ ] Role-based access control enforced
- [ ] At least one EMR connector (HCHB) operational with sample data
- [ ] Notification system routing to all channels
- [ ] Deficiency tracker CRUD operations working
- [ ] Load testing: 10 concurrent users, 50 requests/sec peak
- [ ] Security: OWASP top 10 checklist completed
- [ ] Documentation: API docs auto-generated; deployment runbook written

---

## 15. Appendix: File Locations & References

**Agent Scripts:**
- `/agents/intake_referral/agent.py`
- `/agents/oasis_qa/agent.py`
- `/agents/pdgm_billing/agent.py`
- `/agents/scheduling/agent.py`
- `/agents/clinical_documentation_qa/agent.py`
- `/agents/survey_readiness/agent.py`
- `/agents/qapi/agent.py`
- `/agents/outcomes_hhvbp/agent.py`
- `/agents/regulatory_intelligence/agent.py`
- `/agents/recert_discharge/agent.py`
- `/agents/founding_engineer/agent.py`
- `/agents/ceo/agent.py`

**Documentation:**
- `/docs/AGENTS.md` — Overview of all 12 agents
- `/docs/API.md` — FastAPI endpoint reference
- `/docs/DATABASE.md` — Schema and query examples
- `/docs/DEPLOYMENT.md` — Railway setup and CI/CD pipeline

**Frontend:**
- `/frontend/` — React app (to be created)

**Configuration:**
- `/.env.example` — Template for local dev

---

**End of Specification**
