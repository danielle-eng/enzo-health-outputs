# Enzo Health QAPI Module — Agency Onboarding Checklist
## Day 1 Welcome Package

**Welcome to Enzo Health's QAPI Quality Improvement Program!**

This checklist outlines everything you need to know to get started with our comprehensive quality reporting and performance improvement system. We'll guide you through data setup, what to expect in your first 30 days, and how to use your quarterly QAPI reports to drive real improvement.

---

## Phase 1: Pre-Launch Setup (Before Day 1)

- [ ] **Schedule kickoff call** with your Enzo Health QAPI Specialist (15 min intro + 45 min data requirements review)
- [ ] **Designate agency QAPI Coordinator** — single point of contact for data submission, weekly updates, and question escalation
- [ ] **Grant data access** — ensure QAPI Coordinator has read-only access to your home health EHR and claims/billing system
- [ ] **Confirm budget timeline** — understand Enzo Health QAPI module pricing and invoice cadence (typically monthly or quarterly)

---

## Phase 2: Data Collection & Preparation (Days 1-7)

### 2.1 — What Data You Need to Provide

Enzo Health QAPI requires the following data elements to generate your baseline analysis. Data should be provided as **CSV or Excel export** from your EHR/claims system.

#### Minimum Required Fields (Core Dataset)

| Data Element | Format | Source | Frequency | Example |
|---|---|---|---|---|
| **Patient ID** | Unique identifier | EHR | Every admission | PT0001, PT0002 |
| **Admission Date** | YYYY-MM-DD | EHR | Every admission | 2026-01-15 |
| **Discharge Date** | YYYY-MM-DD (if applicable) | EHR | Upon discharge | 2026-03-15 |
| **Primary Diagnosis (ICD-10)** | ICD-10 code | Claims/EHR | Every admission | I50.9 (Heart Failure) |
| **Diagnosis Description** | Text | EHR | Every admission | "Heart failure, unspecified" |
| **Payer Type** | Medicare / Medicare Advantage / Medicaid / Private / Other | Claims | Every admission | Medicare |
| **Hospitalization Flag** | 1 = Yes, 0 = No | Claims/EHR | Upon occurrence | 1 |
| **Hospitalization Date** | YYYY-MM-DD | Hospital notification/Claims | If applicable | 2026-02-10 |
| **ED Visit Flag** | 1 = Yes, 0 = No | Claims/EHR | Upon occurrence | 0 |
| **Discharge Disposition** | Discharged to home/self-care, Transferred to facility, Transferred to acute hospital, Patient expired, Other | EHR | Upon discharge | Discharged to home |
| **OASIS SOC Date** | YYYY-MM-DD | OASIS database | Within 14 days of admission | 2026-01-20 |
| **OASIS DC Date** | YYYY-MM-DD | OASIS database | At discharge or 60 days | 2026-03-14 |
| **Timely Initiation Flag** | 1 = SOC within 14 days, 0 = SOC after 14 days | Calculated | Upon SOC completion | 1 |

#### Additional OASIS Functional Outcomes (For More Detailed Analysis)

If available in your OASIS database, provide:
- **Ambulation Score at SOC and at DC/60-day** (0-6 scale) — for improvement rate calculation
- **Bathing Score at SOC and at DC/60-day** — for improvement rate calculation
- **Dyspnea Score at SOC and at DC/60-day** — for improvement rate calculation
- **Pain Score at SOC and at DC/60-day** — for improvement rate calculation

**Data Format:**
- CSV or Excel workbook
- One row per patient episode (admission-to-discharge)
- Include a Notes column for any data quality flags or explanations
- De-identified (no names, addresses, or full SSNs — patient ID only)

**Where to Find This Data:**
- **EHR:** Most home health EMRs (Amedisys, Qliance, Carepath, Epic HHA, MatrixCare) can export this standardized report
- **OASIS:** Direct export from your OASIS submission system (CMS OASIS database or your state registry)
- **Claims/Billing:** Available from your billing software or through your Medicare Administrative Contractor (MAC)

**Timeline:** Provide baseline data (prior quarter) by **Day 3 of onboarding**. Ongoing weekly updates begin in Week 2.

---

### 2.2 — Data Quality Checklist

Before submitting, verify your data:

- [ ] All admission dates have corresponding discharge dates (or are still active)
- [ ] OASIS SOC dates are between admission and discharge (or within 14 days of admission)
- [ ] Hospitalization dates fall within the home health episode window
- [ ] Payer types are standardized (no variations like "HMO" vs. "Medicare Advantage")
- [ ] ICD-10 codes are valid (check against current CMS ICD-10 code set)
- [ ] No missing values in required fields (use "Unknown" if data is unavailable)
- [ ] Patient IDs are consistent (same ID does not appear with different admission dates unless re-admission)
- [ ] No duplicate rows

**Questions about data quality?** Contact your Enzo Health QAPI Specialist before submission.

---

## Phase 3: First 30 Days — What to Expect

### Week 1 (Days 1-7): Onboarding & Data Intake

| Day(s) | Action | Responsibility | Deliverable |
|--------|--------|---|---|
| Day 1 | Initial QAPI kickoff call | Enzo + Agency QAPI Coord | Agenda + data requirements confirmed |
| Day 2-3 | Agency prepares and exports baseline data | Agency QAPI Coord | CSV/Excel data file |
| Day 3 | Data submission & quality review | Enzo QAPI Agent | Data validation report + feedback |
| Day 5 | Enzo completes initial data validation | Enzo QAPI Agent | Data quality checklist; flags any issues |
| Day 7 | Enzo begins preliminary analysis | Enzo QAPI Agent | [No deliverable; internal work] |

**Agency Action:** Appoint QAPI Coordinator, provide baseline data by Day 3, answer any data quality questions by Day 5.

---

### Week 2 (Days 8-14): Analysis & Preliminary Reporting

| Day(s) | Action | Responsibility | Deliverable |
|--------|--------|---|---|
| Days 8-10 | Enzo completes benchmark comparison and indicator analysis | Enzo QAPI Agent | [Internal analysis] |
| Day 12 | Enzo meets with agency leadership to review preliminary findings | Enzo + Clinical Director | Preliminary findings presentation (verbal or written brief) |
| Day 14 | Agency begins weekly tracker setup and training | Enzo + Agency QAPI Coord | Weekly tracker template + tutorial |

**Agency Action:** Attend preliminary findings meeting; assign someone to manage weekly tracker going forward.

---

### Week 3-4 (Days 15-30): Live System Activation & Training

| Day(s) | Action | Responsibility | Deliverable |
|--------|--------|---|---|
| Days 15-21 | Weekly tracker goes live; agency submits first weekly update | Agency QAPI Coord | First weekly submission (data through end of Week 3) |
| Day 21 | Enzo reviews first weekly submission for completeness | Enzo QAPI Agent | Feedback on submission quality |
| Days 22-28 | Agency completes QAPI training modules (optional) | Enzo + Agency staff | Certificates of completion (if applicable) |
| Day 28 | Enzo delivers **Month 1 Preliminary Report** (informal) | Enzo QAPI Agent | Written summary of Month 1 trends and any RED flags |
| Day 30 | Kickoff planning for quarterly cycle | Enzo + Agency leadership | Agenda for Q1 full report and PIP planning (if needed) |

**Agency Action:** Start weekly tracker submissions by Day 21; plan to implement quarterly report recommendations.

---

## Phase 4: Understanding Your Quarterly QAPI Report

By end of Month 1 (after 30 days), Enzo will deliver your **first formal Quarterly QAPI Report**. Here's what to expect and how to use it.

### 4.1 — Report Structure

Your Quarterly QAPI Report will include:

**Section 1: Executive Summary**
- Your agency's overall performance vs. national CMS benchmarks
- Key findings: which quality indicators are strong, which need attention
- Whether any Performance Improvement Projects (PIPs) are triggered

**Section 2: Quality Indicator Dashboard**
- A table showing each quality measure (e.g., hospitalization rate, ED utilization, functional improvements)
- Your rate | CMS benchmark | Status (GREEN = on target, YELLOW = slightly above, RED = significantly above)
- Trend (if prior quarter data available)

**Section 3: Detailed Indicator Analysis**
- For each indicator, especially those marked YELLOW or RED:
  - Your rate vs. benchmark and the gap size
  - Root cause hypotheses (based on data analysis and clinical judgment)
  - Specific recommendations for improvement

**Section 4: Performance Improvement Projects (PIPs)**
- If 1+ indicators triggered a PIP, this section outlines:
  - Problem statement (why the indicator is off)
  - Root cause analysis (fishbone diagram / 5 Whys)
  - SMART goal (e.g., "reduce hospitalization rate to 16% by Q3")
  - 7 specific interventions with owners and due dates
  - Measurement plan and success metrics
  - Timeline

**Section 5: Patient Safety Events Summary**
- Count of falls, infections, medication errors, adverse events
- Severity assessment
- Any trends or patterns

**Section 6: Governing Body Summary**
- Brief overview for your board/leadership
- Key metrics and status
- Recommended action items

---

### 4.2 — How to Interpret the Status Indicators

| Status | Meaning | Action |
|--------|---------|--------|
| 🟢 **GREEN** | You're meeting or exceeding the CMS national benchmark | Continue current practices; maintain this level of performance; no formal PIP needed |
| 🟡 **YELLOW** | You're slightly above (within 2 percentage points of) the CMS benchmark | Close monitoring recommended; consider incremental process improvements; not yet a formal PIP trigger |
| 🔴 **RED** | You're significantly above (>2 percentage points) the CMS benchmark | **ESCALATE:** A Performance Improvement Project is recommended or required. Requires corrective action plan. |

---

### 4.3 — How to Read & Act on a PIP

If your report includes a Performance Improvement Project (PIP), here's how to implement it:

**Step 1: Understand the Problem** (5-10 min read)
- Read the "Problem Statement" section
- Understand the baseline rate, benchmark, and the gap
- Note the estimated cost impact or patient risk

**Step 2: Review Root Causes** (15 min read)
- Review the "Root Cause Analysis" section
- Discuss with your clinical team: do these root causes match what you see operationally?
- Identify any additional root causes specific to your agency

**Step 3: Commit to the Goal** (Team meeting, 30 min)
- Discuss the SMART goal with your clinical leadership and board
- Confirm resources/budget available to execute the interventions
- Document leadership commitment and approval

**Step 4: Assign Owners & Set Timeline** (30-60 min)
- Enzo will suggest an owner for each intervention
- Confirm that owner has capacity and authority to execute
- Adjust timeline if needed (communicate changes back to Enzo)
- Build a Gantt chart or project plan to track progress

**Step 5: Execute Interventions** (Ongoing)
- Implement interventions according to timeline
- Track monthly progress (using the weekly tracker + monthly huddles)
- Document what's working, what's not, and any obstacles

**Step 6: Measure & Remeasure** (Monthly then Quarterly)
- Monthly snapshot: review hospitalization/ED trends using weekly tracker
- Quarterly formal rate: when new quarter closes, Enzo calculates formal rate (e.g., Q2 hospitalization rate by July 15)
- Compare to interim target (e.g., ≤20% by end Q2) and final target (e.g., ≤16% by end Q3)

**Step 7: Adjust & Scale** (Monthly review)
- If on track: maintain current plan
- If slipping: escalate to Enzo; brainstorm additional interventions
- If exceeding target early: document what's working and maintain

**Step 8: Close the PIP** (Upon goal achievement)
- Once you hit the final target (e.g., ≤16% hospitalization rate), PIP moves to "Sustainability"
- Continue monitoring quarterly; re-train staff annually on key interventions
- Plan to measure that indicator in future quarters to ensure gains persist

---

### 4.4 — PIP Submission for QAPI Committee Review

If you want to submit a PIP (either one recommended by Enzo or one you develop internally) for review by your QAPI committee, **Enzo provides a standardized PIP template and submission process.**

**To submit a PIP:**

1. **Complete the PIP template** (provided by Enzo):
   - Problem statement & root cause analysis
   - SMART goal
   - 5-7 specific interventions with owners/dates
   - Measurement plan

2. **Internal review:**
   - Present PIP to your QAPI committee or clinical leadership for feedback
   - Incorporate feedback; finalize version 1.0

3. **Submit to Enzo:**
   - Email completed PIP to your Enzo QAPI Specialist
   - Enzo reviews for completeness and feasibility (1-week turnaround)
   - Enzo provides written feedback and recommendations

4. **Final approval:**
   - Agency approves recommended adjustments (if any)
   - Clinical Director signs off on final PIP
   - PIP becomes active; monitoring begins

**Timeline:** PIP submission to approval typically takes 2-3 weeks. Start early if you have a Q2 PIP and want it approved by late April.

---

## Phase 5: Quarterly Cycle & Ongoing Engagement

### Calendar of Annual QAPI Activities

| Quarter | Key Dates | Activities |
|---------|-----------|-----------|
| **Q1** | By 04/15 | Q1 QAPI report delivered; any PIPs initiated |
| | Ongoing | Weekly tracker updates; monthly progress monitoring |
| | By 06/30 | Q1 PIP Month 3 assessment (on track for Q2 target?) |
| **Q2** | By 07/15 | Q2 QAPI report delivered; new or continued PIPs reviewed |
| | Ongoing | Weekly tracker updates; monthly progress monitoring |
| | By 09/30 | Q2 PIP Month 3 assessment (on track for Q3 target?) |
| **Q3** | By 10/15 | Q3 QAPI report delivered; PIPs assessed for closure or extension |
| | Ongoing | Weekly tracker updates; monthly progress monitoring |
| | By 12/31 | Q3 PIP Month 3 assessment; plan for Year 2 PIPs |
| **Q4** | By 01/15 (next year) | Q4 QAPI report delivered; Year 1 summary and Year 2 planning |

### Monthly Standing Activities (Every Agency)

- **Week 1 of month:** Submit weekly tracker updates to Enzo (data through prior Friday)
- **Week 2 of month:** Enzo feedback on submission quality
- **Week 3 of month:** Agency clinical huddle review (internal) of hospitalization/ED trends
- **Week 4 of month:** PIP intervention checks (if applicable); adjust timelines if slipping

### Quarterly Activities (Every Agency)

- **Week 1 of new quarter:** Enzo QAPI report generated and submitted
- **Week 2:** Agency leadership meeting to review findings and any new PIP recommendations
- **Week 3:** If PIP is triggered, agency begins root cause analysis and intervention planning
- **Ongoing through quarter:** Weekly tracker + monthly huddles

---

## Phase 6: Frequently Asked Questions (FAQ)

### 1. **What if I don't have all the data fields you're asking for?**

**Answer:** Don't worry — start with what you have. Most home health agencies have:
- Admission/discharge dates
- ICD-10 diagnoses
- Payer type
- Hospitalization flags (from claims or hospital notification)

If you're missing OASIS functional outcomes (ambulation, bathing, etc.), you can still generate reports on acute care indicators (hospitalization, ED, timely SOC). We recommend getting a full OASIS data feed eventually, but it's not required to start.

**What to do:**
- Provide the data you have by Day 3
- Work with Enzo to identify gaps
- Create a 30-day plan to backfill missing data (usually fixable through claims export or OASIS database query)

---

### 2. **I see we have a RED indicator and a recommended PIP. Do we have to do it?**

**Answer:** Technically, PIPs are recommendations, not mandates. However:

- **CMS expectation:** Home health agencies are expected to address quality gaps >2 percentage points above benchmark through formal Quality Improvement methodology
- **Your board will ask:** Board members will see the report and ask why you're not improving a known gap
- **Patient impact:** High hospitalization or ED rates indicate care gaps that likely affect patient outcomes and costs
- **Accreditation:** Many accrediting bodies (AAAHC, CARF, etc.) require documented PIPs for significant quality gaps

**Our recommendation:** Commit to a PIP if an indicator is RED. You can adjust scope or timeline based on your resources, but some improvement plan should be in place.

**To decline a PIP:** Document in your QAPI minutes why you're not pursuing improvement on that indicator (e.g., "Patient population acuity is primary driver; medical necessity for admissions; focus on other initiatives this year"). Be prepared to defend this to your board and surveyors.

---

### 3. **How much time do our staff need to dedicate to QAPI tracking?**

**Answer:** Estimated time commitment:

| Role | Activity | Time/Week |
|------|----------|-----------|
| **QAPI Coordinator** | Weekly tracker updates, data validation, Enzo communication | 3-5 hours |
| **Nursing Supervisor** | Monthly clinical huddle review, PIP intervention oversight | 2-3 hours |
| **Clinical Director** | Quarterly report review, board reporting, PIP approval | 2-3 hours |
| **Front-line staff** | Early warning sign documentation, care coordination (if PIP) | Embedded in existing workflow |

**Total agency burden:** 7-11 hours/week (primarily QAPI Coordinator)

For a 50-patient-per-month agency, this is approximately **10-15 minutes per patient episode** for quality data capture and reporting.

**Tip:** If you use an EHR that exports QAPI metrics directly, you can cut QAPI Coordinator time in half. Contact Enzo about EHR integration options.

---

### 4. **Our numbers look bad compared to the benchmark. Is it because our patients are sicker?**

**Answer:** Maybe — but probably not the whole story. Here's how to assess:

**Patient acuity factors that legitimately increase hospitalization rates:**
- High % of Medicare patients >80 years old
- Heavy concentration of CHF, COPD, cancer diagnoses
- Multi-morbidity (average >4 comorbidities per patient)
- Limited caregiver support (many living alone)
- Low health literacy

**However:**
- CMS benchmarks are already risk-adjusted for age and diagnosis
- Even high-acuity agencies should hit 16-18% hospitalization rate
- If you're at 24%, a 6-8 percentage point gap is "unexplained" by acuity alone
- Root causes usually include process gaps (monitoring, communication, access)

**What to do:**
1. Ask Enzo to do a **risk-stratification analysis** of your patient population vs. national norms
2. If acuity is truly higher, adjust PIP targets slightly (e.g., ≤18% instead of ≤16%), but still pursue improvement
3. Focus PIP interventions on the modifiable root causes (access, communication, monitoring) that don't depend on acuity

---

### 5. **How do we balance QAPI improvement with staff burnout? We're already stretched thin.**

**Answer:** Valid concern. Quality improvement shouldn't add burden; it should uncover and fix inefficiencies.

**Principles:**
- **PIPs are designed to reduce workload, not add it.** If a 24/7 triage line prevents 3-4 unnecessary hospitalizations/month, that's LESS total work downstream
- **Target the right interventions.** Choosing the right fix matters; doing 5 ineffective interventions burns staff faster than doing 1 high-impact intervention
- **Build in staff support.** If a PIP requires new training (e.g., early warning signs), allocate time for training and allow practice time
- **Measure staff perception.** Include in monthly huddles: "Is this intervention helping you do your job better, or creating friction?"

**Enzo's role:**
- We prioritize interventions that have high clinical impact AND manageable implementation burden
- We help you sequence interventions to spread out workload over the quarter
- We track intervention compliance and adjust if adoption is low due to workload

**Agency action:**
- Be transparent with Enzo if a recommended intervention feels unmanageable
- Suggest alternatives that achieve the same goal with less staff impact
- Consider temporary staffing increase or outsourced support (e.g., external case management) to support PIP implementation

---

### 6. **Can we get Enzo's help interpreting our findings or developing our PIP?**

**Answer:** Absolutely. That's what we're here for.

**Enzo support includes:**
- **Interpretation calls:** 30-60 min call with your clinical leadership to review findings and discuss root causes (included in most QAPI packages)
- **PIP development:** Enzo drafts a recommended PIP based on your data and clinical context; your team refines it (included)
- **Implementation coaching:** Monthly check-ins to assess PIP progress, troubleshoot obstacles, adjust interventions (included in some packages; paid add-on in others)
- **Staff training:** Enzo can deliver webinars on specific topics (e.g., early warning sign recognition, medication reconciliation) to support PIP implementation (paid add-on)

**Cost:** QAPI reports are typically bundled; coaching and training are often à la carte. Discuss options with your Enzo account manager during onboarding.

---

## Onboarding Checklist — Master Checklist

### Pre-Launch (Before Day 1)
- [ ] Appoint agency QAPI Coordinator
- [ ] Schedule kickoff call with Enzo
- [ ] Grant EHR/claims data access to QAPI Coordinator
- [ ] Confirm budget and contracting finalized

### Week 1 (Days 1-7)
- [ ] Attend kickoff meeting with Enzo QAPI Specialist
- [ ] Coordinator exports and submits baseline data (CSV/Excel)
- [ ] Enzo completes initial data quality review
- [ ] Agency responds to any data quality questions

### Week 2 (Days 8-14)
- [ ] Enzo completes preliminary analysis
- [ ] Agency leadership attends preliminary findings meeting
- [ ] Weekly tracker template received and reviewed
- [ ] Agency QAPI Coordinator begins setup of weekly tracker

### Week 3-4 (Days 15-30)
- [ ] First weekly tracker submission completed and sent to Enzo
- [ ] Enzo reviews first submission for quality
- [ ] Agency completes any QAPI training modules (optional)
- [ ] Enzo delivers Month 1 Preliminary Report
- [ ] Agency & Enzo plan Q1 quarterly cycle

### Month 2 & Beyond (Ongoing)
- [ ] Weekly tracker submissions every Friday (data through Thursday)
- [ ] Monthly clinical huddle reviews (internal to agency)
- [ ] Quarterly QAPI report review with Enzo
- [ ] Any triggered PIPs moved to implementation phase
- [ ] Quarterly reporting to board/leadership

---

## Next Steps

1. **Confirm your QAPI Coordinator** — Email name and contact info to Enzo by EOD today
2. **Schedule your kickoff call** — Enzo will send a calendar invite for a 1-hour call within 24 hours
3. **Prepare baseline data** — Start exporting Q1 (or prior quarter) data from your EHR by Day 1
4. **Read the Weekly Tracker Template** — Familiarize yourself with what you'll be updating each Friday

---

## Contact & Support

**Your Enzo Health QAPI Specialist:**
- Name: [To be assigned during onboarding]
- Email: [qapi@enzohealth.com]
- Phone: [XXX-XXX-XXXX]
- Response time: 24 hours for questions, 48 hours for data requests

**Quick Reference Links:**
- Weekly Tracker Template: [Link]
- CMS Benchmark Reference: [Link]
- OASIS Data Dictionary: [Link to external resource]
- PIP Template: [Link]

**Questions before you start?** Schedule a pre-kickoff call with Enzo at [scheduling link].

---

**Welcome aboard! We're excited to partner with you on quality improvement. Let's get started.**

*Enzo Health QAPI Module | Prepared April 2026 | Version 1.0*
