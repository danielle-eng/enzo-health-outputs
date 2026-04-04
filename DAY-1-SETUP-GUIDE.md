# Enzo Health Paperclip — Day 1 Setup Guide
**For: Danielle (Enzo Health PM)**
**Last updated: April 3, 2026**

This guide walks you through standing up the Enzo Health Paperclip instance from scratch — from first login through assigning Wave 1 issues. It assumes Paperclip has already been deployed (via Railway or another host) and you have the admin URL and credentials.

Estimated time: 30–45 minutes.

---

## Before You Start

Make sure you have the following ready:

- [ ] Paperclip instance URL (e.g., `https://enzo-health.paperclip.ai` or your Railway URL)
- [ ] Admin login credentials
- [ ] This folder open on your computer: `Enzo Health Paperclip/`
  - `agents/` — contains all 7 AGENTS.md files
  - `context/` — contains all 6 product context docs
  - `WAVE-1-TASKS.md` — the Wave 1 issue list

---

## Step 1: Log In and Create the Organization

1. Navigate to your Paperclip instance URL
2. Log in with your admin credentials
3. On first login, you'll be prompted to **create an organization**
4. Set the organization name: **Enzo Health**
5. (Optional) Upload the Enzo Health logo
6. Click **Create Organization**

You now have an empty Enzo Health workspace. Next you'll add the agents.

---

## Step 2: Add the 7 Agents

You'll create each agent one at a time. For each agent, the process is:

> **New Agent → Paste name → Paste AGENTS.md contents → Save**

In Paperclip, navigate to **Agents** in the left sidebar and click **+ New Agent**.

---

### Agent 1: Founding Engineer

**Name:** `Founding Engineer`

**AGENTS.md file:** `agents/Founding-Engineer-AGENTS.md`

Open the file, copy the entire contents, and paste into the agent's instruction field.

**Role summary:** Infrastructure and tooling. This agent runs first — it builds the workspace everything else depends on.

---

### Agent 2: QAPI Specialist

**Name:** `QAPI Specialist`

**AGENTS.md file:** `agents/QAPI-Specialist-AGENTS.md`

Open the file, copy the entire contents, and paste into the agent's instruction field.

**Role summary:** Quarterly quality analysis, QAPI reports, PIPs, governing body packages.

---

### Agent 3: Clinical Documentation QA

**Name:** `Clinical Documentation QA`

**AGENTS.md file:** `agents/Clinical-Documentation-QA-AGENTS.md`

Open the file, copy the entire contents, and paste into the agent's instruction field.

**Role summary:** Per-note clinical documentation review, scoring, clinician coaching.

---

### Agent 4: Survey Readiness

**Name:** `Survey Readiness`

**AGENTS.md file:** `agents/Survey-Readiness-AGENTS.md`

Open the file, copy the entire contents, and paste into the agent's instruction field.

**Role summary:** Mock surveys, CMS Statement of Deficiencies format, gap lists, plans of correction.

---

### Agent 5: Regulatory Intelligence

**Name:** `Regulatory Intelligence`

**AGENTS.md file:** `agents/Regulatory-Intelligence-AGENTS.md`

Open the file, copy the entire contents, and paste into the agent's instruction field.

**Role summary:** Weekly regulatory digest, impact analyses, CMS rule tracking.

---

### Agent 6: Outcomes Analyst

**Name:** `Outcomes Analyst`

**AGENTS.md file:** `agents/Outcomes-Analyst-AGENTS.md`

Open the file, copy the entire contents, and paste into the agent's instruction field.

**Role summary:** Monthly outcomes dashboard, HHVBP modeling, hospitalization RCAs, high-risk patient flags.

---

### Agent 7: CEO

**Name:** `CEO`

**AGENTS.md file:** `agents/CEO-AGENTS.md`

Open the file, copy the entire contents, and paste into the agent's instruction field.

**Role summary:** Executive synthesis, cross-agent coordination, Wave reporting, agent orchestration.

---

## Step 3: Add the Product Context Documents

Each agent needs access to the Enzo product context so outputs are grounded in the actual platform, not generic assumptions. These are shared context documents — attach them to the workspace or individual agents depending on how your Paperclip instance handles shared knowledge.

**The 6 context files to add:**

| File | What It Covers |
|---|---|
| `ENZO-PLATFORM-CONTEXT.md` | Full platform overview — all 7 products, roles, payer mix, multi-branch support |
| `ENZO-SCRIBE-PRODUCT-CONTEXT.md` | Scribe mobile app — ambient listening, visit types, documentation output |
| `ENZO-INTAKE-PRODUCT-CONTEXT.md` | Intake module — kanban workflow, referral sources, patient record structure |
| `ENZO-SCHEDULING-PRODUCT-CONTEXT.md` | Scheduling module — capacity management, visit lifecycle, discipline structure |
| `ENZO-QUALITY-MANAGEMENT-PRODUCT-CONTEXT.md` | Quality Management — top risks, work queue, chart audits, survey readiness |
| `ENZO-OASIS-PRODUCT-CONTEXT.md` | OASIS Management — review pipeline, individual review screen, timeliness requirements |

**Recommended approach:** If Paperclip supports a workspace-level knowledge base, upload all 6 files there. If context is agent-level, add all 6 to the Founding Engineer (since it runs first) and at minimum the 2–3 most relevant files to each other agent.

**Most critical context file per agent:**

| Agent | Must-Have Context File |
|---|---|
| Founding Engineer | ENZO-PLATFORM-CONTEXT.md |
| QAPI Specialist | ENZO-QUALITY-MANAGEMENT-PRODUCT-CONTEXT.md |
| Clinical Documentation QA | ENZO-SCRIBE-PRODUCT-CONTEXT.md |
| Survey Readiness | ENZO-QUALITY-MANAGEMENT-PRODUCT-CONTEXT.md |
| Regulatory Intelligence | ENZO-OASIS-PRODUCT-CONTEXT.md |
| Outcomes Analyst | ENZO-OASIS-PRODUCT-CONTEXT.md |
| CEO | ENZO-PLATFORM-CONTEXT.md |

---

## Step 4: Verify MCP Tool Connectivity

Before assigning Wave 1 issues, confirm the three MCP tools are connected and working. Founding Engineer will test these formally in FE-1, but you can do a quick sanity check now.

**Three MCP tools expected:**

| Tool | What It Does | Quick Test |
|---|---|---|
| **ICD-10 Lookup** | Search and validate diagnosis codes | Look up "I50.9" — should return "Heart failure, unspecified" |
| **NPI Search** | Search the NPPES registry for clinicians and agencies | Search "home health" in Utah — should return agency results |
| **CMS Coverage (LCD/NCD)** | Search Local and National Coverage Determinations | Search "home health" — should return coverage policies |

If any tool returns an error, check the MCP configuration in Paperclip settings before proceeding. Founding Engineer will document the connectivity status in its README output.

---

## Step 5: Assign Wave 1 Issues

With all agents created and context loaded, it's time to assign the first wave of work. Open `WAVE-1-TASKS.md` for the full issue descriptions — below is the assignment order and quick reference.

**⚠️ Important: Launch order matters. FE-1 must complete before other agents start.**

---

### Day 1 — Assign These Now

**Issue FE-1 → Founding Engineer** *(Assign first. Others wait for this.)*

> Bootstrap workspace at `/workspaces/enzo-health/`, verify MCP connectivity, create all 8 document templates, create QAPI CSV input template, write README.

Copy the full FE-1 description from `WAVE-1-TASKS.md` into the issue.

---

**Once FE-1 is complete (or nearly complete), assign these three in parallel:**

**Issue QAPI-1 → QAPI Specialist**

> Create Q1 mock agency sample data (50-patient CSV), produce complete Q1 QAPI report, write one PIP, produce governing body package.

**Issue CDQA-1 → Clinical Documentation QA**

> Write 3 sample visit notes (excellent / moderate / poor quality), run full QA review on each, write clinician coaching memo.

**Issue REG-1 → Regulatory Intelligence**

> Research current regulatory environment, produce first weekly digest (week of March 30 – April 3, 2026), write 2026 HH PPS Final Rule impact analysis.

---

### Day 2 — Assign After Day 1 Completes

**Issue SR-1 → Survey Readiness** *(Depends on CDQA-1 sample notes)*

> Review sample notes as a CMS surveyor, produce SOD-format mock survey report, gap list, plan of correction.

**Issue OA-1 → Outcomes Analyst** *(Depends on QAPI-1 mock data)*

> Calculate outcome rates from mock data, produce monthly outcomes dashboard, write 2 hospitalization RCAs, produce high-risk flag report.

---

### Day 3 — Assign After All Others

**Issue CEO-1 → CEO** *(Synthesizes all Wave 1 outputs)*

> Review all Wave 1 outputs, write executive summary for Danielle, write agent coordination protocol (weekly/monthly/quarterly rhythms).

---

## Step 6: Confirm Output Locations

When agents complete Wave 1, their outputs should land in this workspace directory structure:

```
/workspaces/enzo-health/
├── qapi/
│   ├── data/                    ← QAPI-1: mock agency sample data CSV
│   ├── reports/                 ← QAPI-1: Q1 QAPI report
│   ├── pips/                    ← QAPI-1: hospitalization reduction PIP
│   └── governing-body/          ← QAPI-1: governing body package
├── clinical-qa/
│   ├── notes/                   ← CDQA-1: 3 sample visit notes
│   ├── weekly-audit/
│   └── reports/                 ← CDQA-1: 3 QA reviews + coaching memo
├── survey-readiness/
│   ├── mock-surveys/            ← SR-1: mock survey SOD report
│   ├── gap-lists/               ← SR-1: prioritized gap list
│   └── poc/                     ← SR-1: plan of correction
├── regulatory/
│   ├── digests/                 ← REG-1: weekly digest
│   └── impact-analyses/         ← REG-1: HH PPS Final Rule analysis
├── outcomes/
│   ├── dashboards/              ← OA-1: monthly dashboard
│   ├── rca/                     ← OA-1: 2 hospitalization RCAs
│   └── high-risk/               ← OA-1: high-risk flag report
├── reports/                     ← CEO-1: executive summary + coordination protocol
├── templates/                   ← FE-1: all 8 document templates
└── data/                        ← FE-1: QAPI CSV input template
```

The Founding Engineer creates this structure in FE-1. All other agents save to the folders it creates.

---

## What to Watch For

**After FE-1:**
- Confirm the `/workspaces/enzo-health/` directory exists with all subfolders
- Check the README for MCP connectivity status — if a tool failed, address it before Wave 1 agents need it
- Verify all 8 templates exist in `/templates/` and are populated (not blank)

**After QAPI-1:**
- Open the Q1 report — check that hospitalizations, ED visits, and outcome rates are calculated (not just described)
- Open the PIP — check that it has a root cause analysis, SMART goal, specific interventions, and a measurement plan
- The governing body package should be 1–2 pages, readable by a board member with no clinical background

**After CDQA-1:**
- The three sample notes should span a real quality spectrum — Note A should be obviously better than Note C
- QA reviews should have specific line-level feedback, not generic comments
- Coaching memo should be usable immediately with a real agency

**After REG-1:**
- Weekly digest should have at least 3 items across urgency categories (🔴/🟡/🟢)
- Each item should include a "Product Implications" note specific to Enzo modules
- Impact analysis should address payment rates, OASIS changes, and quality measure changes separately

**After OA-1:**
- Dashboard should show actual calculated rates vs. CMS benchmarks (not estimates)
- HHVBP projection should estimate the payment adjustment percentage
- RCAs should read like real clinical narratives, not templates

**After CEO-1:**
- Executive summary should be readable by Danielle or an agency owner with no prior context
- Coordination protocol should be specific enough to run the agent org with no additional instructions

---

## Troubleshooting

**Agent isn't starting:** Check that the AGENTS.md content was pasted correctly and saved. Some agents require context files to be attached before they can complete their tasks.

**MCP tool errors:** Verify the tool is configured in Paperclip Settings → Integrations. If the ICD-10 or NPI tool isn't responding, the Founding Engineer will note this in its README and subsequent agents will work around it.

**Output files missing:** If an agent completes but files aren't in the expected location, check whether the workspace directory was created by FE-1. Other agents cannot create the scaffold — FE-1 must go first.

**Agent produces generic output:** This usually means it didn't receive the product context files. Re-attach the relevant ENZO-*-PRODUCT-CONTEXT.md files and re-run the issue.

**Wave 1 issue quality is low:** Start with CEO-1 after everything else completes — the CEO agent's synthesis will identify which Wave 1 outputs need revision and flag gaps explicitly.

---

## After Wave 1: What's Next

Wave 2 priorities (from `WAVE-1-TASKS.md`):

1. **FE-2:** Build the Scribe API connector — pull real visit notes into `/clinical-qa/` for live QA review
2. **QAPI-2:** Connect to real agency data and run first live quarterly analysis
3. **REG-2:** Set up recurring weekly digest (automated trigger every Monday)
4. **OA-2:** Build the HHVBP financial model with agency-specific baseline data
5. **SR-2:** Full mock survey against 10 real patient records
6. **CEO-2:** First customer-facing demo package

Wave 2 doesn't start until Wave 1 is complete and CEO-1's executive summary has been reviewed. The CEO agent's Wave 2 recommendations should guide prioritization.

---

*Questions? Contact Danielle at danielle@enzo.health.*
