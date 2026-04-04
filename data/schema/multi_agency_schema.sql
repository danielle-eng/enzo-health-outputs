-- ========================================================================
-- ENZO HEALTH: Multi-Agency Database Schema
-- ========================================================================
-- This schema supports a multi-tenant SaaS platform for home health agencies
-- Each agency operates in a fully isolated data environment with shared
-- regulatory and benchmarking resources.
--
-- Design Principles:
-- 1. Agency-Level Isolation: agency_id foreign keys enforce data boundaries
-- 2. Row-Level Security (RLS): PostgreSQL policies restrict access by agency
-- 3. Shared Resources: Regulatory items and quality benchmarks are cross-agency
-- 4. Audit Trail: Created/updated timestamps on all clinical tables
-- ========================================================================

-- ========================================================================
-- AGENCY REGISTRY
-- ========================================================================
-- Central registry of all customer agencies and their onboarding status
CREATE TABLE agencies (
    agency_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    cms_certification_number VARCHAR(10) UNIQUE, -- CMS CCN for Medicare/Medicaid
    state VARCHAR(2) NOT NULL, -- US state abbreviation
    phone VARCHAR(20),
    email VARCHAR(255),
    primary_contact_name VARCHAR(255),
    onboarded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    go_live_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) NOT NULL DEFAULT 'onboarding', -- onboarding, active, suspended, churned
    subscription_tier VARCHAR(50) NOT NULL DEFAULT 'standard', -- standard, premium, enterprise
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    archived_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_agencies_status ON agencies(status);
CREATE INDEX idx_agencies_state ON agencies(state);
CREATE INDEX idx_agencies_cms_number ON agencies(cms_certification_number);

COMMENT ON TABLE agencies IS 'Master registry of all agencies in the platform. Each agency is fully isolated.';
COMMENT ON COLUMN agencies.cms_certification_number IS 'CMS Certification Number (CCN) for regulatory reporting';
COMMENT ON COLUMN agencies.status IS 'Current operational status: onboarding, active, suspended, or churned';

-- ========================================================================
-- PATIENT EPISODES
-- ========================================================================
-- Core clinical data: one row per home health episode per patient
-- An episode is the continuous period of care from admission to discharge
CREATE TABLE patient_episodes (
    episode_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(agency_id) ON DELETE CASCADE,
    patient_id VARCHAR(50) NOT NULL, -- Client's internal patient ID (not PII)
    admission_date DATE NOT NULL,
    discharge_date DATE,
    expected_discharge_date DATE,
    payer VARCHAR(100), -- Medicare, Medicaid, Commercial, Self-Pay
    primary_diagnosis_icd10 VARCHAR(10), -- Primary diagnosis code (e.g., J45.901)
    primary_diagnosis_description VARCHAR(500),
    secondary_diagnoses_icd10 TEXT, -- JSON array of secondary diagnoses
    functional_limitation_score INTEGER, -- OASIS functional limitation (0-6)
    cognitive_status VARCHAR(50), -- OASIS cognitive status
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Multi-column unique constraint: one active episode per patient per agency
CREATE UNIQUE INDEX idx_patient_episodes_active ON patient_episodes(agency_id, patient_id) WHERE discharge_date IS NULL;

-- Performance indexes for common queries
CREATE INDEX idx_patient_episodes_agency_id ON patient_episodes(agency_id);
CREATE INDEX idx_patient_episodes_admission_date ON patient_episodes(admission_date);
CREATE INDEX idx_patient_episodes_discharge_date ON patient_episodes(discharge_date);
CREATE INDEX idx_patient_episodes_payer ON patient_episodes(payer);

COMMENT ON TABLE patient_episodes IS 'Clinical episodes representing continuous home health care from admission to discharge';
COMMENT ON COLUMN patient_episodes.patient_id IS 'Agency-specific patient identifier (not shared across agencies)';
COMMENT ON COLUMN patient_episodes.payer IS 'Insurance category: Medicare, Medicaid, Commercial, or Self-Pay';

-- ========================================================================
-- QUALITY INDICATOR SNAPSHOTS
-- ========================================================================
-- Calculated quality metrics for each agency, tracked over time
-- One row per metric per period (monthly/quarterly)
CREATE TABLE quality_snapshots (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(agency_id) ON DELETE CASCADE,
    indicator_code VARCHAR(50) NOT NULL, -- e.g., 'ADL_IMPROVEMENT', 'HOSPITALIZATION_RATE'
    indicator_name VARCHAR(255) NOT NULL,
    period_type VARCHAR(20) NOT NULL, -- 'monthly' or 'quarterly'
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    numerator INTEGER, -- Count of patients with outcome
    denominator INTEGER, -- Total eligible patients
    rate DECIMAL(5, 3), -- Calculated rate (0.000 to 1.000)
    benchmark_rate DECIMAL(5, 3), -- National or regional benchmark
    status VARCHAR(50), -- 'above_benchmark', 'at_benchmark', 'below_benchmark'
    trend_vs_last_period VARCHAR(50), -- 'improving', 'stable', 'declining'
    notes TEXT,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_quality_snapshots_agency_id ON quality_snapshots(agency_id);
CREATE INDEX idx_quality_snapshots_indicator ON quality_snapshots(indicator_code);
CREATE INDEX idx_quality_snapshots_period_date ON quality_snapshots(period_start_date);
CREATE INDEX idx_quality_snapshots_status ON quality_snapshots(status);

COMMENT ON TABLE quality_snapshots IS 'Quality metric snapshots for each agency per reporting period';
COMMENT ON COLUMN quality_snapshots.indicator_code IS 'Standardized quality indicator code used for benchmarking';
COMMENT ON COLUMN quality_snapshots.rate IS 'Calculated percentage (0.000 to 1.000)';
COMMENT ON COLUMN quality_snapshots.benchmark_rate IS 'National or regional benchmark for comparison';

-- ========================================================================
-- CLINICAL NOTE REVIEWS
-- ========================================================================
-- Track quality and compliance reviews of clinical documentation
CREATE TABLE note_reviews (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(agency_id) ON DELETE CASCADE,
    episode_id UUID REFERENCES patient_episodes(episode_id) ON DELETE SET NULL,
    patient_id VARCHAR(50) NOT NULL,
    visit_date DATE NOT NULL,
    discipline VARCHAR(100), -- PT, OT, RN, HHA, SW, etc.
    note_type VARCHAR(100), -- 'initial_assessment', 'progress_note', 'discharge_summary'
    reviewer_name VARCHAR(255),
    score INTEGER CHECK (score >= 0 AND score <= 10), -- 0-10 quality score
    domains JSONB, -- Structured review domains: {"documentation": 8, "assessment": 7, "plan": 6}
    adr_ready BOOLEAN, -- Is note ADR (Alternative Drug Regimen) ready
    deficiency_codes TEXT, -- JSON array of CMS CoP deficiency codes if found
    corrected_at TIMESTAMP WITH TIME ZONE,
    reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_note_reviews_agency_id ON note_reviews(agency_id);
CREATE INDEX idx_note_reviews_episode_id ON note_reviews(episode_id);
CREATE INDEX idx_note_reviews_visit_date ON note_reviews(visit_date);
CREATE INDEX idx_note_reviews_discipline ON note_reviews(discipline);
CREATE INDEX idx_note_reviews_score ON note_reviews(score);

COMMENT ON TABLE note_reviews IS 'Quality assurance reviews of clinical documentation for compliance and completeness';
COMMENT ON COLUMN note_reviews.score IS 'Numerical quality assessment (0-10)';
COMMENT ON COLUMN note_reviews.domains IS 'JSON object with domain-specific scores';
COMMENT ON COLUMN note_reviews.adr_ready IS 'Whether note meets Alternative Drug Regimen readiness standards';

-- ========================================================================
-- SURVEY FINDINGS
-- ========================================================================
-- Track CMS survey findings and agency responses
CREATE TABLE survey_findings (
    finding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(agency_id) ON DELETE CASCADE,
    survey_date DATE NOT NULL,
    survey_type VARCHAR(100), -- 'standard', 'complaint', 'revisit'
    cfr_citation VARCHAR(20), -- e.g., '42 CFR 484.50' for patient rights
    severity VARCHAR(50), -- 'deficiency', 'substantial_compliance', 'non-compliance'
    finding_text TEXT NOT NULL,
    related_episode_id UUID REFERENCES patient_episodes(episode_id) ON DELETE SET NULL,
    corrected_at TIMESTAMP WITH TIME ZONE,
    correction_description TEXT,
    surveyor_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_survey_findings_agency_id ON survey_findings(agency_id);
CREATE INDEX idx_survey_findings_survey_date ON survey_findings(survey_date);
CREATE INDEX idx_survey_findings_cfr_citation ON survey_findings(cfr_citation);
CREATE INDEX idx_survey_findings_severity ON survey_findings(severity);
CREATE INDEX idx_survey_findings_corrected_at ON survey_findings(corrected_at);

COMMENT ON TABLE survey_findings IS 'CMS survey findings and deficiency tracking with correction status';
COMMENT ON COLUMN survey_findings.cfr_citation IS 'Code of Federal Regulations citation (42 CFR)';
COMMENT ON COLUMN survey_findings.severity IS 'Finding severity level per CMS classification';

-- ========================================================================
-- PERFORMANCE IMPROVEMENT PLANS (PIPs)
-- ========================================================================
-- Track PIP status and progress for quality improvement initiatives
CREATE TABLE pips (
    pip_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(agency_id) ON DELETE CASCADE,
    indicator_targeted VARCHAR(255) NOT NULL, -- e.g., 'Readmission Rate', 'Documentation Completeness'
    baseline_rate DECIMAL(5, 3), -- Starting performance rate
    target_rate DECIMAL(5, 3), -- Desired performance rate
    start_date DATE NOT NULL,
    target_date DATE NOT NULL,
    current_rate DECIMAL(5, 3),
    last_measured_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'active', -- active, completed, suspended
    completion_reason VARCHAR(255), -- e.g., 'target_achieved', 'timeframe_extended', 'deprioritized'
    interim_milestones JSONB, -- Array of milestone objects with dates and rates
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_pips_agency_id ON pips(agency_id);
CREATE INDEX idx_pips_status ON pips(status);
CREATE INDEX idx_pips_target_date ON pips(target_date);
CREATE INDEX idx_pips_indicator ON pips(indicator_targeted);

COMMENT ON TABLE pips IS 'Performance Improvement Plan tracking for quality metric improvement';
COMMENT ON COLUMN pips.baseline_rate IS 'Starting performance rate before PIP intervention';
COMMENT ON COLUMN pips.interim_milestones IS 'JSON array of milestone objects with expected progress';

-- ========================================================================
-- REGULATORY DIGEST ITEMS (SHARED ACROSS ALL AGENCIES)
-- ========================================================================
-- Weekly digest of regulatory changes, CMS updates, and policy alerts
-- Shared resource: agencies read this table to stay current on regulations
CREATE TABLE regulatory_items (
    item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    week_of DATE NOT NULL, -- Start date of the week (Monday)
    urgency_level VARCHAR(50) NOT NULL, -- 'critical', 'high', 'medium', 'informational'
    title VARCHAR(500) NOT NULL,
    source VARCHAR(255), -- e.g., 'CMS.gov', 'Federal Register', 'OIG', 'State Board'
    source_url TEXT,
    summary TEXT NOT NULL,
    affected_areas TEXT, -- JSON array of affected areas: ["assessment", "billing", "quality"]
    product_implications TEXT, -- How this affects Enzo features
    action_deadline DATE,
    action_required VARCHAR(255), -- What agencies need to do
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_regulatory_items_week_of ON regulatory_items(week_of);
CREATE INDEX idx_regulatory_items_urgency ON regulatory_items(urgency_level);
CREATE INDEX idx_regulatory_items_action_deadline ON regulatory_items(action_deadline);

COMMENT ON TABLE regulatory_items IS 'Shared regulatory digest accessible to all agencies (cross-tenant)';
COMMENT ON COLUMN regulatory_items.week_of IS 'Monday of the week this digest covers';
COMMENT ON COLUMN regulatory_items.urgency_level IS 'Alert priority: critical, high, medium, or informational';
COMMENT ON COLUMN regulatory_items.product_implications IS 'How this regulatory change affects Enzo platform features';

-- ========================================================================
-- ROW-LEVEL SECURITY (RLS) POLICIES
-- ========================================================================
-- These policies enforce tenant isolation: agencies can only see their own data

-- Enable RLS on agency-specific tables
ALTER TABLE patient_episodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE quality_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE note_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE survey_findings ENABLE ROW LEVEL SECURITY;
ALTER TABLE pips ENABLE ROW LEVEL SECURITY;

-- Policy template (requires auth context like current_user_agency_id):
-- CREATE POLICY agency_isolation ON patient_episodes
-- USING (agency_id = current_setting('app.current_agency_id')::uuid);

COMMENT ON POLICY agency_isolation IS 'Enforces row-level security: users only see data for their agency';

-- ========================================================================
-- SAMPLE QUERIES
-- ========================================================================

-- Query 1: Get all agencies currently below benchmark on hospitalization rate
-- SELECT
--     a.name,
--     qs.period_start_date,
--     qs.rate,
--     qs.benchmark_rate,
--     (qs.benchmark_rate - qs.rate) AS gap
-- FROM agencies a
-- JOIN quality_snapshots qs ON a.agency_id = qs.agency_id
-- WHERE qs.indicator_code = 'HOSPITALIZATION_RATE'
--   AND qs.rate > qs.benchmark_rate -- Below benchmark (higher hospitalization is worse)
--   AND qs.period_end_date >= CURRENT_DATE - INTERVAL '90 days'
-- ORDER BY gap DESC;

-- Query 2: Get all open PIPs by agency with progress
-- SELECT
--     a.name,
--     p.indicator_targeted,
--     p.baseline_rate,
--     p.target_rate,
--     p.current_rate,
--     ROUND((p.current_rate - p.baseline_rate)::numeric / (p.target_rate - p.baseline_rate), 2) AS pct_progress,
--     p.target_date,
--     CASE WHEN p.target_date < CURRENT_DATE THEN 'OVERDUE' ELSE 'ON TRACK' END AS status
-- FROM agencies a
-- JOIN pips p ON a.agency_id = p.agency_id
-- WHERE p.status = 'active'
--   AND p.current_rate IS NOT NULL
-- ORDER BY a.name, p.target_date;

-- Query 3: Get clinical notes with below-target scores from last 30 days
-- SELECT
--     a.name,
--     nr.discipline,
--     nr.visit_date,
--     nr.score,
--     nr.domains,
--     nr.reviewer_name
-- FROM agencies a
-- JOIN note_reviews nr ON a.agency_id = nr.agency_id
-- WHERE nr.score < 7 -- Below target score of 7/10
--   AND nr.reviewed_at >= CURRENT_DATE - INTERVAL '30 days'
-- ORDER BY a.name, nr.score;

-- Query 4: Cross-agency aggregated quality performance (anonymized benchmarking)
-- SELECT
--     qs.indicator_code,
--     qs.period_start_date,
--     ROUND(AVG(qs.rate)::numeric, 3) AS avg_rate_all_agencies,
--     ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY qs.rate)::numeric, 3) AS q1_rate,
--     ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY qs.rate)::numeric, 3) AS median_rate,
--     ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY qs.rate)::numeric, 3) AS q3_rate
-- FROM quality_snapshots qs
-- WHERE qs.period_end_date >= CURRENT_DATE - INTERVAL '180 days'
-- GROUP BY qs.indicator_code, qs.period_start_date
-- ORDER BY qs.indicator_code, qs.period_start_date DESC;

-- ========================================================================
-- SAMPLE REFERENCE DATA
-- ========================================================================

-- Insert sample quality indicators (shared across all agencies)
-- INSERT INTO quality_snapshots (agency_id, indicator_code, indicator_name, period_type, period_start_date, period_end_date, numerator, denominator, rate, benchmark_rate, status)
-- VALUES (agency_id_here, 'ADL_IMPROVEMENT', 'ADL Improvement Score', 'monthly', '2026-03-01', '2026-03-31', 45, 62, 0.726, 0.750, 'below_benchmark');

-- ========================================================================
-- VERSION HISTORY
-- ========================================================================
-- v1.0 (2026-04-04): Initial multi-agency schema with 6 core tables
--   - agencies: Master registry
--   - patient_episodes: Clinical episodes
--   - quality_snapshots: Quality metrics
--   - note_reviews: Documentation QA
--   - survey_findings: CMS survey tracking
--   - pips: Performance improvement plans
--   - regulatory_items: Cross-tenant regulatory digest
--
-- Design assumptions:
-- - PostgreSQL database (UUID, JSONB support, RLS capabilities)
-- - agency_id is the primary isolation key for all tenant data
-- - Timestamps are stored in UTC (TIMESTAMP WITH TIME ZONE)
-- - Quality rates are stored as decimals (0.000 to 1.000) for precision
-- - JSONB columns allow flexible metadata storage
-- ========================================================================
