# Enzo Health — Scribe Product Context
**For internal AI agent use. Last updated: April 3, 2026.**

This document gives the Enzo Health Paperclip agent team accurate, detailed context about the Scribe product so that all agent outputs — QAPI reports, clinical QA reviews, regulatory analyses, outcomes dashboards — reflect what the platform actually does rather than generic assumptions.

---

## What Scribe Is

Scribe is Enzo Health's mobile application built for home health and hospice clinicians working in the field with patients. Its core function is **ambient listening**: the app listens to clinical visits and post-visit interactions and uses that audio to automatically complete patient documentation. The result is that clinicians can focus entirely on the patient during a visit instead of typing notes, and still walk away with documentation that accurately reflects the encounter.

Scribe currently supports **four disciplines**:
- Skilled Nursing (SN)
- Physical Therapy (PT)
- Occupational Therapy (OT)
- Speech Therapy (ST/SLP)

It covers **all OASIS visit types** (Start of Care, Resumption of Care, Follow-Up, Discharge, Transfer) and all **subsequent (non-OASIS) visits** within an episode.

---

## The Two Transcript Components

Every Scribe session generates documentation from two distinct audio captures:

### 1. In-Visit Component
The app listens to the full interaction between the clinician and the patient (and any caregiver present) inside the patient's home. This captures:
- The clinical assessment conversation
- Patient-reported symptoms, status changes, and concerns
- Education delivered by the clinician
- Caregiver training and instructions
- Responses to OASIS and Planicare items

The ambient capture means the clinician does not need to narrate into the phone or pause the visit to take notes. Everything said during the clinical encounter becomes input for documentation.

### 2. Post-Visit Survey
This is a structured interview the clinician completes **after leaving the patient's home** — outside in their car or another private setting. It serves two purposes:

**a) Clarification and completeness:** The AI uses this to ask follow-up questions about anything ambiguous from the in-visit transcript, fill in details that weren't explicitly stated during the visit, and confirm answers to specific OASIS items.

**b) Sensitive information capture:** This is the designated space for information the clinician cannot or should not say in front of the patient or caregiver. This includes:
- Pest infestation in the home
- Hoarding situations
- Adult Protective Services (APS) concerns
- Safety risks observed in the home environment
- Abuse, neglect, or exploitation indicators
- Other private clinical judgments

This design is intentional and clinically important — it protects patient dignity while ensuring that sensitive but medically relevant observations are not lost.

---

## Documentation Output

Once both transcripts are complete, Scribe automatically generates responses to all required documentation fields. This includes:

- **OASIS items** — all applicable items for the visit type (SOC, ROC, FU, DC, Transfer)
- **Planicare sections** — discipline-specific care plan documentation
- **Clinical narrative / visit note** — the free-text clinical note reflecting the encounter
- **Patient education documentation** — what was taught, patient/caregiver response
- **Skilled need justification** — clinical rationale for skilled services (critical for ADR/audit defense)
- **Goal progress** — documentation of progress toward established care plan goals

### Agent Implication (Clinical Documentation QA):
Scribe is the source of all visit notes that the Clinical Documentation QA agent reviews. When reviewing notes, the agent should understand that these notes are AI-generated from ambient transcripts — common failure modes include vague skilled justification (the AI didn't hear explicit clinical reasoning), missing patient response (education was given but response wasn't captured in audio), and OASIS inconsistency (in-visit audio conflicted with post-visit survey answers).

---

## Interactive Sections (Manual Input + AI Assist)

Beyond ambient listening, Scribe has four structured interactive sections that clinicians use for specific documentation needs:

### 1. Vital Signs
Clinicians enter vital signs directly into the app during or after the visit. Captured vitals:
- Blood pressure (sitting, standing if applicable)
- Heart rate / pulse
- Respiratory rate
- Temperature
- O2 saturation
- Pain scale (0–10)
- Weight (when applicable)
- Blood glucose (when applicable)

**Why it matters:** Vital signs entered here are stored in a structured, easily accessible format. Clinicians can pull them for:
- Handoff reports to physicians
- Assisted living facility documentation
- Physician communication notes
- OASIS M items that require vital sign documentation (e.g., M1240 Pain, M1060 Height/Weight)

This avoids the common problem of clinicians needing to scroll through a long narrative transcript to find a specific number.

### 2. Wound Care Documentation
This section allows clinicians to fully document wound assessment findings, including:
- Wound measurements (length × width × depth in cm)
- Wound characteristics (stage, tunneling, undermining, exudate type and amount, tissue type, periwound condition)
- **Photo capture** — photos are taken in-app and directly associated with the specific wound record
- Wound care goal linkage — each wound is connected to its care plan goal
- Wound care intervention documentation — supplies used, technique, patient/caregiver instructions

**Note on supplies:** Scribe supports documentation of wound care supply usage in compliance with physician order language (e.g., generic alternative authorization).

**Why it matters for agents:** Wound care documentation quality is one of the highest-risk areas for ADR and probe review. The Clinical Documentation QA agent should flag any wound notes where measurements are absent, photos are undocumented, or wound care interventions don't align with the physician order.

### 3. Medication Management
Clinicians can capture the patient's medication list in two ways:
- **Photo of pill bottles** — the clinician photographs individual medication bottles
- **Photo of medication list** — photographs a printed or handwritten med list
- **Combination** — both sources simultaneously

Scribe's AI automatically extracts:
- Medication name (brand and generic)
- Dosage and strength
- Route of administration
- Frequency / schedule
- Prescribing physician (when visible on label)
- Refill information (when visible)

The extracted information populates a structured medication list within the visit documentation.

**Why it matters:** Accurate medication reconciliation is required at every OASIS assessment visit and is a common survey deficiency. This section directly supports M2000–M2020 (drug regimen review) and is foundational for the medication management outcome measure tracked by the Outcomes Analyst agent.

### 4. Visit Outline / Road Map
This is a guided checklist that functions as a real-time clinical compass during the visit. Before or during a visit, the clinician sees a structured outline of:
- Every OASIS item applicable to this visit type and discipline
- Every Planicare section they need to address
- Questions they need to ask or assess to ensure thorough documentation

The road map adapts to visit type (SOC vs. subsequent vs. discharge), discipline, and patient-specific care plan. Its purpose is to close documentation gaps before they happen — if a clinician follows the road map, the AI write-back will be more complete and accurate.

**Agent implication (Clinical Documentation QA):** When reviewing a note and the clinician followed the road map, gaps in documentation are more likely to reflect a genuine clinical finding (e.g., the patient refused assessment) rather than a missed item. Notes without road map completion may have more systematic gaps.

---

## Supported Visit Types and Disciplines Matrix

| Visit Type | SN | PT | OT | ST/SLP |
|---|---|---|---|---|
| Start of Care (SOC) | ✅ | ✅ | ✅ | ✅ |
| Resumption of Care (ROC) | ✅ | ✅ | ✅ | ✅ |
| Follow-Up (Subsequent) | ✅ | ✅ | ✅ | ✅ |
| Discharge | ✅ | ✅ | ✅ | ✅ |
| Transfer to Inpatient | ✅ | ✅ | ✅ | ✅ |

---

## How Scribe Connects to the Agent Team

| Agent | Scribe Connection |
|---|---|
| **Founding Engineer** | Scribe API is integration priority #1. FE should build the connector that pulls completed visit notes from Scribe into `/clinical-qa/notes/` for automated QA review. |
| **Clinical Documentation QA** | Scribe is the source of every note reviewed. QA reviews should account for AI-generated documentation patterns (ambient capture artifacts, vague justification, transcript-to-OASIS inconsistencies). |
| **QAPI Specialist** | Scribe documentation quality directly affects OASIS data accuracy, which flows into QAPI outcome calculations. Documentation errors = outcome measure errors = QAPI distortion. |
| **Outcomes Analyst** | OASIS-based quality measures (improvement in ambulation, bathing, dyspnea, etc.) all depend on accurate OASIS capture at SOC and DC — which Scribe generates. Medication management outcome (M2020) is directly tied to Scribe's medication section. |
| **Survey Readiness** | Survey deficiencies most commonly cite visit notes for missing skilled justification, unsigned/undated entries, and incomplete OASIS. All are Scribe outputs. Mock surveys should evaluate Scribe-generated notes directly. |
| **Regulatory Intelligence** | OASIS-E changes, LCD/NCD updates for specific diagnoses, and documentation standard changes (e.g., CMS CoP revisions) directly affect what Scribe must capture. New regulations should be flagged with a "Scribe Impact" section. |
| **CEO** | Scribe is the primary data entry point for the entire platform. Documentation quality from Scribe cascades into every downstream product (scheduling, QAPI, outcomes, billing readiness). |

---

## Known Gaps / Areas Without Integration (as of April 2026)

- **No live API connection yet** — Scribe notes are not yet flowing automatically into the Paperclip workspace. FE-1 task is to build this connector.
- **Physician orders not in Scribe** — Scribe does not currently capture or store physician orders (485 Plan of Care). Order alignment must be verified externally.
- **No billing/coding integration** — Scribe generates clinical documentation but does not code visits for billing. ICD-10 codes used in notes are for clinical documentation, not claims.
- **Hospice not yet live** — Scribe currently covers home health disciplines only. Hospice documentation is a future roadmap item.

---

## Demo Environment
A Scribe demo environment is available. If agents need to reference specific field labels, UI flow, or feature behavior not documented here, request the demo link from Danielle (PM).

---

*This document should be updated whenever Scribe adds new features, visit types, or disciplines. Notify the Regulatory Intelligence agent of any changes that affect OASIS item coverage.*
