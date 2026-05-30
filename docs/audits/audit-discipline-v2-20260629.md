---
audit_type: audit_discipline_v2
date: 2026-06-29
auditor: self-audit (AUDIT route)
scope: audit_discipline_evidence_chain
verdict: ACCEPTED_WITH_MODIFICATIONS — 2 proposals accepted (modified), 1 accepted as-is, 1 rejected
---

# Audit Discipline V2 — Evidence Chain Strengthening

**Date**: 2026-06-29
**Type**: AUDIT — Internal governance improvement (remediation round 2)
**Scope**: Vibebackbone audit discipline: evidence chain rigor, finding classification, read-only contract, confidence levels
**Skill used**: Grille générique (audit governance)
**Artifact**: `docs/audits/audit-discipline-v2-20260629.md`
**Governance read**: PILOTAGE.md, CONVENTIONS.md, 02-p-vbb-audit.md, 07-p-vbb-closeout.md, 2-vbb-audit-task.md, 2-vbb-security/SKILL.md, 2-vbb-systemic-risk/SKILL.md, 3-vbb-risk-register/SKILL.md
**Mode**: Lecture seule, aucune modification de code source

---

## Verdict global

**Verdict**: READY — with accepted modifications

The prior remediation (2026-05-30) established the foundation (route declaration, evidence model, three-axis findings taxonomy, audit closeout checklist). This second audit confirms the foundation is structurally sound. The remaining failure mode — signals elevated to findings too quickly — requires surgical strengthening, not structural redesign.

**Two proposals accepted with modification, one accepted as-is, one rejected.**

---

## 1. Prior Remediation Status

| Gap (Round 1) | Status | Location |
|----------------|--------|----------|
| Route declaration preamble | ✅ Implemented | 02-p-vbb-audit.md §DÉCLARATION INITIALE |
| Evidence model (4-level) | ✅ Implemented | 02-p-vbb-audit.md §Discipline de l'évidence |
| Three-axis findings taxonomy | ✅ Implemented | 02-p-vbb-audit.md §Étape 3 — Classer |
| Verification rule | ✅ Implemented | 02-p-vbb-audit.md §DÉCLARATION INITIALE |
| Audit closeout checklist | ✅ Implemented | 07-p-vbb-closeout.md §Étape 6 |

**All five gaps from round 1 are closed.** The current prompt contains:
- Mandatory initial declaration (route, type, skill, artifact, governance, mode)
- Evidence discipline table (OBSERVATION / SIGNAL / HYPOTHESIS / VERIFIED_FINDING)
- Findings table with Severity × Type × Decision × Evidence Level
- Verification rule ("2 sources distinctes ou test confirmé")
- Explicit closeout checklist for AUDIT routes

---

## 2. Current Failure Mode Analysis

**Observed pattern** (per the remediation request):

```
Observation → Signal → Conclusion
```

**Desired pattern**:

```
Observation → Signal → Hypothesis → Verification → Finding → Decision
```

**Root cause**: The current evidence model defines **what each level IS** but does not require the agent to **show the trace** from one level to the next. An agent can:
1. Read code (observation)
2. Interpret it (signal)
3. Immediately classify it as a finding

Without documenting:
- What hypothesis they formed
- How they verified it
- What evidence path they followed

This is not a model gap (the levels exist) — it's an **enforcement gap** (the path through the levels is not mandatory).

---

## 3. Proposal Analysis

### Proposal A — Mandatory Evidence Ladder

**Original request**: Introduce a mandatory evidence chain for every finding.

**Current state**: Four-level model exists (OBSERVATION / SIGNAL / HYPOTHESIS / VERIFIED_FINDING) with verification rule.

**Gap**: The model defines levels but does not require a traceable path through them.

**Verdict**: ✅ **ACCEPT with MODIFICATION**

**Modification rationale**:
- Do NOT create a new 6-step model — the existing 4-level model is sufficient
- Do add a mandatory **evidence trace requirement**: each VERIFIED_FINDING must document its path through the levels
- The trace is a 2–3 line field per finding, not a new governance layer
- This prevents the observed failure mode (signal → conclusion) without adding structural complexity

**Implementation**: Add an evidence trace requirement to the findings table in 02-p-vbb-audit.md. Each finding classified as VERIFIED_FINDING must include an explicit trace:

```
Evidence trace: OBSERVATION [what was read] → SIGNAL [interpretation] → VERIFICATION [how confirmed] → FINDING
```

This is 1 additional field in the findings table, not a new model.

---

### Proposal B — Mandatory Finding Classification

**Original request**: Introduce explicit classification taxonomy (VIOLATION_CONFIRMED, TOLERATED_EXCEPTION, FALSE_POSITIVE, NEEDS_DECISION, TREND_OBSERVATION).

**Current state**: Three-axis model already in place (Severity P0–P3 × Type VIOLATION/OBSERVATION/TREND/FALSE_POSITIVE × Decision ACCEPTED/MITIGATED/DEFER/NEEDS_DECISION).

**Analysis**:
- The proposed single-axis taxonomy is a **collapse** of the current three-axis model
- VIOLATION_CONFIRMED → Type:VIOLATION + Decision: confirmed (default for VIOLATION)
- TOLERATED_EXCEPTION → Type:VIOLATION + Decision:ACCEPTED (or Type:OBSERVATION + Decision:ACCEPTED)
- FALSE_POSITIVE → Type:FALSE_POSITIVE (already exists)
- NEEDS_DECISION → Decision:NEEDS_DECISION (already exists)
- TREND_OBSERVATION → Type:TREND (already exists)

The proposed taxonomy is **less expressive** than what's already in place. Every proposed classification can be expressed with the current model, and the current model can express things the proposed taxonomy cannot (e.g., a VIOLATION that is MITIGATED, or a TREND that NEEDS_DECISION).

**The example given** (localhost fallback as TOLERATED_EXCEPTION instead of VIOLATION_CONFIRMED) is correctly handled by the current model:
- Type: VIOLATION (it IS a best-practice violation)
- Decision: ACCEPTED (it's tolerated in development)
- This combination precisely expresses "tolerated exception"

The real issue isn't the taxonomy — it's **agent judgment** in classifying findings. An agent might default to VIOLATION/NEEDS_DECISION when the correct classification is VIOLATION/ACCEPTED. This is a **guidance gap**, not a taxonomy gap.

**Verdict**: ❌ **REJECT the proposed taxonomy**

The proposed single-axis taxonomy removes information already captured by the three-axis model. Instead:
- Keep the existing three-axis model
- Add **classification guidance** to help agents distinguish common misclassification patterns (see implementation)

---

### Proposal C — Read-Only Audit Contract

**Original request**: Explicit behavior contract when user requests "without modifying code."

**Current state**: 
- DÉCLARATION INITIALE states: "Mode d'exécution : lecture seule, aucune modification de code"
- Interdictions section states: "❌ Modifier du code ou des fichiers pendant l'audit"
- Closeout explicitly updates AUDIT_STATUS.md, SESSION.md, CONTEXT.md

**Gap**: The current statement forbids "modification de code ou des fichiers" but the audit process itself creates new files (reports) and updates status files. The boundary between "audit artifact production" (allowed) and "governance/status modification" (contextual) is implicit.

**Verdict**: ✅ **ACCEPT as proposed**

The proposal correctly identifies that the allow/forbid boundary needs to be explicit. The current "lecture seule" declaration is too broad — it prohibits "modifying files" but audits must create new files and update status files. A sharper allow/forbid list will eliminate ambiguity.

**Implementation**: Replace the current "Mode d'exécution" line with an explicit contract section in 02-p-vbb-audit.md, listing what is allowed and forbidden during an audit phase.

---

### Proposal D — Audit Confidence Levels

**Original request**: Introduce confidence scoring (A/B/C/D).

**Current state**: Evidence levels already classify claim strength (OBSERVATION < SIGNAL < HYPOTHESIS < VERIFIED_FINDING).

**Analysis**:
- Proposal's Level A ≈ current VERIFIED_FINDING (2+ sources)
- Proposal's Level B ≈ current SIGNAL (1 verified source)
- Proposal's Level C ≈ current SIGNAL (weak signal)
- Proposal's Level D ≈ current HYPOTHESIS (intuition)

The confidence levels map to the current evidence model but add a **second classification axis** that overlaps conceptually. An agent must ask: "Is this a VERIFIED_FINDING with confidence B, or a SIGNAL with confidence A?" — the distinction is unclear and adds cognitive load without proportional benefit.

The stated goal ("prevent weak observations from appearing equivalent to strongly verified findings") is already addressed by the evidence model IF properly enforced. The enforcement gap (Proposal A's trace requirement) directly solves this.

**Verdict**: ❌ **REJECT**

Adding a confidence axis creates conceptual overlap with the existing evidence model, increases classification complexity from 3 axes to 4, and the goal is better served by enforcing the existing evidence chain (Proposal A modification). No additional axis is needed.

---

## 4. Decision Summary

| Proposal | Verdict | Rationale |
|----------|---------|-----------|
| A — Evidence Ladder | **ACCEPT with MODIFICATION** | Enforce trace through existing levels, not new levels |
| B — Finding Classification | **REJECT** | Current 3-axis model is more expressive; add guidance instead |
| C — Read-Only Contract | **ACCEPT as proposed** | Sharpen allow/forbid boundary |
| D — Confidence Levels | **REJECT** | Overlaps evidence model; enforcement of existing model is sufficient |

---

## 5. Implementation Plan

### Change 1: Evidence trace requirement (Proposal A)

**File**: `prompts/canonical/02-p-vbb-audit.md`
**What**: Add mandatory evidence trace field to the findings table structure
**Lines**: ~8 lines added to the findings table template
**Migration impact**: Agents must produce the trace field for VERIFIED_FINDING entries. No structural change to governance.

### Change 2: Read-only audit contract (Proposal C)

**File**: `prompts/canonical/02-p-vbb-audit.md`
**What**: Replace the single "Mode d'exécution" line with an explicit AUDIT CONTRACT section
**Lines**: ~12 lines replacing ~1 line
**Migration impact**: Clearer behavioral contract; no structural change.

### Change 3: Classification guidance (Proposal B mitigation)

**File**: `prompts/canonical/02-p-vbb-audit.md`
**What**: Add a brief note on common misclassification patterns under the classification step
**Lines**: ~10 lines
**Migration impact**: Guidance only; no structural change.

### Change 4: Template alignment

**File**: `docs/templates/02_AUDIT_REPORT_TEMPLATE.md`
**What**: Update template to match the new findings table format (evidence trace, consistent severity scale)
**Lines**: ~15 lines changed
**Migration impact**: Template consistency.

### Change 5: Skill alignment (minor)

**File**: `skills/2-vbb-security/SKILL.md`
**What**: Add reference to canonical evidence discipline
**Lines**: ~3 lines

**File**: `skills/2-vbb-systemic-risk/SKILL.md`
**What**: Add reference to canonical evidence discipline
**Lines**: ~3 lines

### No changes to:
- `07-p-vbb-closeout.md` — already updated in round 1
- `docs/CONVENTIONS.md` — no pillar changes needed
- No new routes, skills, or governance layers

---

## 6. Verification Requirements

After implementation:

1. Read `prompts/canonical/02-p-vbb-audit.md` — verify evidence trace requirement is present and findings table includes the new field
2. Read `prompts/canonical/02-p-vbb-audit.md` — verify AUDIT CONTRACT section is present with explicit allow/forbid lists
3. Read `docs/templates/02_AUDIT_REPORT_TEMPLATE.md` — verify template aligns with canonical prompt
4. Read `skills/2-vbb-security/SKILL.md` and `skills/2-vbb-systemic-risk/SKILL.md` — verify evidence discipline reference
5. Run governance consistency check: `python tools/vbb-contract-lint.py`
6. Run architecture lint: `python tools/vbb-architecture.py lint`
7. Confirm no new files, routes, skills, or governance pillars were introduced

---

## 7. Risques

| Risk | Severity | Mitigation |
|------|----------|------------|
| Evidence trace adds per-finding overhead | P3 | Trace is 2-3 lines per finding; minimal |
| AUDIT CONTRACT may be too rigid for edge cases | P3 | "unless explicitly requested" escape clause |
| Classification guidance may be ignored by agents | P2 | Enforced by evidence trace requirement |
| Template misalignment with canonical prompt | P2 | Template updated in this remediation |

---

## Ce qui est hors scope

- No confidence level axis (Proposal D — rejected)
- No single-axis classification taxonomy (Proposal B — rejected)
- No new route families, skills, or governance pillars
- No changes to ROUTER_MATRIX, PILOTAGE, or SESSION_RULES
- No changes to verification tooling (vbb-loop-closure-check)
- No migration of existing audit reports

---

*Audit discipline v2 — Vibebackbone — 2026-06-29*
*Verdict: READY — 2 proposals accepted (modified), 1 accepted as-is, 1 rejected*
*Next: implement surgical changes to 02-p-vbb-audit.md, template, and skill references*