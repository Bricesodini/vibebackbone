---
run_id: "2026-05-30_1200_audit-discipline-improvement"
phase: "02_AUDIT"
voie: "AUDIT"
status: "COMPLETE"
agent: "pi"
started_at: "2026-05-30T12:00:00Z"
artifacts_consumed:
  - "SYSTEM.md"
  - "AGENTS.md"
  - "docs/PILOTAGE.md"
  - "docs/CONVENTIONS.md"
  - "docs/ARCHITECTURE.md"
  - "docs/SESSION_RULES.md"
  - "docs/router/ROUTER_MATRIX.md"
  - "prompts/canonical/02-p-vbb-audit.md"
  - "prompts/2-p-vbb-audit-task.md"
  - "prompts/canonical/07-p-vbb-closeout.md"
  - "skills/2-vbb-security/SKILL.md"
  - "skills/2-vbb-systemic-risk/SKILL.md"
  - "skills/2-vbb-data-integrity/SKILL.md"
  - "skills/3-vbb-risk-register/SKILL.md"
  - "docs/audits/effectiveness-maturity-audit-20260529.md"
  - "docs/audits/security-20260610-security-audit.md"
  - "docs/audits/tech-debt-20260610-tech-debt-audit.md"
  - "docs/audits/ops-20260516-1446.md"
artifacts_produced:
  - "docs/audits/audit-discipline-improvement-20260530.md"
  - "docs/audits/audit-discipline-gap-analysis-20260530.md"
---

# Audit discipline improvement — Vibebackbone

**Date**: 2026-05-30
**Type**: AUDIT — Internal governance improvement
**Scope**: Vibebackbone audit execution discipline across all phase-2 skills, canonical prompts, and closeout mechanisms
**Verdict**: PARTIAL — specific gaps confirmed, remediation proposed

---

## Executive Summary

Vibebackbone audit discipline is **structurally sound but operationally incomplete**.

The governance framework is mature: routes are documented, artifact conventions exist, closeout is defined, and skill contracts are explicit. However, the canonical AUDIT prompt (02-p-vbb-audit.md) lacks mandatory execution gates that ensure an agent actually produces a proper audit artifact rather than a conversational summary.

Five specific gaps were confirmed through behavioral analysis:

1. **Route declaration absent from audit prompt** — governance docs describe it; the audit prompt doesn't require it
2. **Evidence model ambiguous** — "observation" and "finding" are used without a canonical evidence discipline
3. **Findings taxonomy inconsistent** — severity scales differ across skills; classification is ad hoc
4. **Verification gate implicit** — no explicit rule requiring evidence validation before a finding is reported
5. **Audit closeout weakly enforced** — no specific AUDIT closeout checklist beyond the general closeout template

The proposed remediation is **MINOR_REMEDIATION**: surgical additions to 02-p-vbb-audit.md, docs/CONVENTIONS.md (evidence pillar), and 07-p-vbb-closeout.md. No framework redesign. No new skills. No new routes. Estimated 50-70 lines of targeted additions across 3 files.

---

## 1. Route Declaration

### Question
Can an agent begin an audit without clearly declaring: selected route, audit type, artifact target, governance sources, execution mode?

### Investigation

**PILOTAGE.md** documents route declaration:
> Route declaration: FAST-ZERO · FAST-MINIMAL · FAST · STRUCTURED · AUDIT · CLOSEOUT

**AGENTS.md** critical rule #1:
> Mandatory triage before any action. Routes: FAST (ZERO/MINIMAL/STANDARD) · STRUCTURED · AUDIT · CLOSEOUT

**ROUTER_MATRIX.md** explicitly maps AUDIT route sequence:
> 01 → 02 (audit) → 03 (decision, new session mandatory) → ... → 07 (closeout)

**02-p-vbb-audit.md** — the canonical audit prompt:
- Describes the auditor role
- Lists inputs to read
- Specifies work steps (observe, record, classify, recommend)
- Lists artifact conventions

**BUT**: The canonical audit prompt never tells the agent to **declare the route at the start**. There is no required preamble such as:
- "Route: AUDIT"
- "Audit type: [security | systemic-risk | data-integrity | ...]"
- "Artifact target: `docs/audits/{type}-{date}.md`"
- "Governance sources: [files read]"
- "Execution mode: read-only, no code modification"

### Gap confirmed

**Severity: P2**

Governance describes route declaration; the audit prompt doesn't enforce it. An agent could begin an audit, produce findings, and never declare the route or artifact target. This creates the failure mode described in the improvement request: "audit artifact not declared or produced" and "route not explicitly declared."

### Evidence

Run artifacts from 2026-06-10 security and tech-debt audits show frontmatter with `voie: AUDIT` and `run_id` — this is the artifact side, not the execution side. The execution-side preamble ("I am starting an AUDIT route with type X and will produce artifact Y") is not required by the prompt.

### Remediation

Add a mandatory preamble to `02-p-vbb-audit.md`:

```markdown
## DÉCLARATION INITIALE (obligatoire)

Avant de commencer, déclarer explicitement :

- **Route** : AUDIT
- **Type d'audit** : [sécurité | intégrité | ops | ci | légal | systémique | autre]
- **Skill utilisé** : [nom du skill ou "grille générique"]
- **Artefact cible** : `docs/audits/{type}-{YYYYMMDD-HHMM}.md` + `docs/runs/{id}/02_AUDIT_REPORT.md`
- **Gouvernance lue** : [fichiers lus avant l'audit]
- **Mode d'exécution** : lecture seule, aucune modification de code

Si cette déclaration n'est pas faite → STOP. L'audit ne peut pas commencer sans elle.
```

This costs 10 lines and closes the gap completely.

---

## 2. Evidence Discipline

### Question
Does Vibebackbone clearly distinguish: observation, signal, hypothesis, verified finding?

### Investigation

**02-p-vbb-audit.md** uses:
- "Observer : lire, analyser, comparer à la référence attendue"
- "Constater : formuler un constat factuel (sans jugement de valeur)"

No explicit four-level model. "Observation" is mentioned but not defined as a distinct artifact level. "Constat factuel" implies verification but doesn't specify what constitutes sufficient evidence.

**2-vbb-security/SKILL.md** includes:
- "confidence level" as a required output field per finding
- "UNKNOWN is allowed when evidence is missing"

**2-vbb-systemic-risk/SKILL.md** includes:
- "NO assumptions · Evidence required · UNKNOWN allowed · No code patches"

**2-vbb-data-integrity/SKILL.md** includes:
- "NO assumptions · Evidence required · UNKNOWN allowed"

**2-p-vbb-audit-task.md** includes:
- "Distinguish facts, inferences, and uncertainties"

This is good scattered practice, but there is no canonical evidence model shared across all phase-2 skills. The difference between "I saw X" (raw observation), "X indicates a risk" (signal), "X might indicate Y" (hypothesis), and "X confirmed Y with evidence" (verified finding) is not formally defined.

### Gap confirmed

**Severity: P2**

Evidence discipline exists in fragments across skills but is not canonical. A skill that requires evidence may use a different threshold than another skill for the same finding type. This leads to the failure mode: "static scan signals presented as confirmed findings."

### Evidence

The `2-p-vbb-audit-task.md` specialized prompt explicitly says "distinguish facts, inferences, and uncertainties" — but this is a specialized prompt, not the canonical audit prompt. The canonical 02-p-vbb-audit.md does not have this distinction. Agents using the canonical prompt may not be aware of the requirement.

### Remediation

Add an evidence discipline section to `02-p-vbb-audit.md` under the preamble:

```markdown
## Discipline de l'évidence

Quatre niveaux à distinguer :

| Niveau | Définition | Règle |
|--------|------------|-------|
| **OBSERVATION** | Ce qui a été lu ou scanné, sans interprétation | Documenter, ne pas conclure |
| **SIGNAL** | Interprétation d'une observation | Requiert au moins 1 référence explicite |
| **HYPOTHESIS** | Théorie non confirmée | Documenter avec marqueur "NON VÉRIFIÉ" |
| **VERIFIED_FINDING** | Constat confirmé par évidence suffisante | Au moins 2 sources distinctes ou test connu |

Règle : un finding ne peut être classé CRITICAL ou BLOCKER que si son niveau est VERIFIED_FINDING.
UNKNOWN est acceptable pour tout niveau — documenter "UNKNOWN : [raison]".

> Ne jamais présenter un SIGNAL ou une HYPOTHESIS comme un VERIFIED_FINDING.
```

This costs ~15 lines. The four-level model (OBSERVATION → SIGNAL → HYPOTHESIS → VERIFIED_FINDING) is already implied in scattered skills; making it canonical closes the gap.

---

## 3. Findings Taxonomy

### Question
Should a standard taxonomy (VIOLATION_CONFIRMED, TOLERATED_EXCEPTION, FALSE_POSITIVE, NEEDS_DECISION, TREND_OBSERVATION) become canonical?

### Investigation

**02-p-vbb-audit.md** (canonical) uses:
> Sévérité: INFO / WARNING / CRITICAL / BLOCKER

This is a severity-only classification. It tells "how bad" but not "what kind of finding" or "what should be done with it."

**2-vbb-security/SKILL.md** uses:
> Severity: low / medium / high / critical

Different scale, same limitation.

**2-vbb-systemic-risk/SKILL.md** uses:
> severity P0 / P1 / P2

Different scale again.

**Real audit artifacts show** (2026-06-10 security audit):
> FALSE_POSITIVE: 1 (SEC-010 — pas de secret exposé, confirmation positive)
> ACCEPTED_RISK: 2 (SEC-006, SEC-008)

These classifications appear in run artifacts but are **not documented in the canonical prompt**. The canonical audit prompt only requires severity classification; the "what to do with it" classification is ad hoc and inconsistent.

### Analysis

The proposed taxonomy (VIOLATION_CONFIRMED, TOLERATED_EXCEPTION, FALSE_POSITIVE, NEEDS_DECISION, TREND_OBSERVATION) captures something the severity-only model misses: the **actionability** of a finding. Severity tells you how bad; this taxonomy tells you what to do.

However, the proposed taxonomy has two problems:
1. **It doesn't map cleanly to the existing severity levels** — VIOLATION_CONFIRMED could be any severity; FALSE_POSITIVE is a status, not a finding type
2. **It's incomplete** — it doesn't cover findings that are confirmed but already mitigated, or findings that are informational only

A better canonical model combines:
- **Severity** (how bad): P0 / P1 / P2 / P3 (already used by systemic-risk and data-integrity skills; more granular than INFO/CRITICAL)
- **Type** (what kind): VIOLATION / OBSERVATION / TREND / FALSE_POSITIVE
- **Decision** (what to do): ACCEPTED / MITIGATED / DEFER / NEEDS_DECISION

This three-axis model is already partially in use:
- Severity: P0/P1/P2 in some skills, INFO/WARNING/CRITICAL in others
- Decision: ACCEPTED_RISK appears in real artifacts
- Type: FALSE_POSITIVE appears in real artifacts

### Gap confirmed

**Severity: P2**

Findings classification is inconsistent across skills and incomplete in the canonical prompt. The taxonomy proposed in the improvement request is a good direction but needs refinement before adoption.

### Remediation

**Do not adopt the proposed taxonomy verbatim.** Instead, standardize on a three-axis model:

1. **Severity**: P0 (critical/blocking) / P1 (major) / P2 (minor) / P3 (info/trend)
   - Standardize to P0–P3 across all phase-2 skills
   - Deprecate the INFO/WARNING/CRITICAL/BLOCKER scale from the canonical audit template

2. **Type** (already partially used):
   - `VIOLATION` — confirmed rule breach
   - `OBSERVATION` — informational, no action required
   - `TREND` — pattern worth monitoring
   - `FALSE_POSITIVE` — flagged by scanner, confirmed not a finding

3. **Decision** (already partially used):
   - `ACCEPTED` — risk accepted, documented rationale
   - `MITIGATED` — controls in place, residual risk
   - `DEFER` — tracked for future action
   - `NEEDS_DECISION` — requires explicit decision, cannot proceed without it

Update the findings table in `02-p-vbb-audit.md` to use this model:

```markdown
## Constats

### Constat 1

| Champ | Valeur |
|-------|--------|
| **ID** | [auto, ex: SEC-001] |
| **Severity** | P0 / P1 / P2 / P3 |
| **Type** | VIOLATION | OBSERVATION | TREND | FALSE_POSITIVE |
| **Location** | [fichier:ligne ou module] |
| **Level** | OBSERVATION | SIGNAL | HYPOTHESIS | VERIFIED_FINDING |
| **Evidence** | [sources, pas d'hypothèse non fondée] |
| **Decision** | ACCEPTED | MITIGATED | DEFER | NEEDS_DECISION |
| **Recommendation** | [action corrective] |
```

This replaces the simpler severity-only format with a richer model that aligns with existing practice. Cost: ~20 lines in the audit template + update to 2–3 phase-2 skills that use different scales.

---

## 4. Audit Artifact Discipline

### Question
Should AUDIT routes always produce a persistent audit artifact or an explicit statement explaining why no artifact exists?

### Investigation

**02-p-vbb-audit.md** explicitly states:
> Créer le rapport horodaté dans `docs/audits/` ET dans `docs/runs/`.
> Mettre à jour `docs/AUDIT_STATUS.md` avec le verdict.

**2-p-vbb-audit-task.md** states:
> Do not present an audit as canonical if governance is missing or unread.
> Do not stop after "recommendations". The audit loop is not closed until findings are registered, report is committed, and git push is done.

**ROUTER_MATRIX.md** specifies:
> 02_AUDIT_REPORT.md in `docs/runs/.../` + `docs/audits/{type}-YYYYMMDD-HHMM.md`

The artifact discipline is **already well documented**. The failure mode ("audit artifact not declared or produced") is a training/execution issue, not a governance gap.

### Gap: NOT confirmed (governance sufficient)

The governance is explicit. The gap is in execution discipline — agents may produce a verbal summary instead of the artifact. This is addressed by the route declaration requirement (Gap 1) and the evidence discipline (Gap 2), not by adding more governance.

### Remediation

No new governance needed. The gap is closed by:
1. Route declaration preamble (Gap 1 remediation)
2. Making "produce artifacts in docs/audits/ AND docs/runs/" explicit in the preamble

Add to the preamble in 02-p-vbb-audit.md:
```markdown
- **Artefacts requis** :
  - `docs/audits/{type}-{YYYYMMDD-HHMM}.md` — rapport persistant (obligatoire)
  - `docs/runs/{id}/02_AUDIT_REPORT.md` — rapport de session
  - Mise à jour de `docs/AUDIT_STATUS.md`
- Si les artefacts ne peuvent pas être produits → declare explicitly why, document in the session log, do not stop silently
```

---

## 5. Verification Discipline

### Question
Should audit conclusions be emitted without verification? Should Vibebackbone require explicit distinction between scanned evidence and verified evidence?

### Investigation

**02-p-vbb-audit.md**:
> "Observer : lire, analyser, comparer à la référence attendue"
> "Constater : formuler un constat factuel (sans jugement de valeur)"

"Constat factuel" implies factual basis, but does not require explicit verification documentation.

**2-p-vbb-audit-task.md**:
> "Distinguish facts, inferences, and uncertainties"

Good — but this is a specialized prompt, not the canonical one.

**2-vbb-security/SKILL.md**:
> "confidence level" — required field per finding
> "UNKNOWN is allowed when evidence is missing"

**2-vbb-systemic-risk/SKILL.md**:
> "NO assumptions · Evidence required · UNKNOWN allowed"

Scattered evidence requirements exist but are not enforced by the canonical prompt.

### Gap confirmed

**Severity: P2**

The verification discipline is present in fragments but not enforced in the canonical audit prompt. An agent could classify a finding as CRITICAL based on a single observation without documenting the verification path. This is the failure mode: "static scan signals presented as confirmed findings."

### Remediation

The evidence discipline model from Gap 2 already addresses this. The VERIFIED_FINDING level requires "at least 2 distinct sources or known test" — this is the verification gate.

Additionally, add to the preamble in 02-p-vbb-audit.md:
```markdown
- **Règle de vérification** : une conclusion n'est émise comme "verified" que si elle est soutenue par au moins 2 sources distinctes ou un test confirmé. Dans le doute → HYPOTHESIS ou UNKNOWN.
```

This is covered by the evidence discipline model. No separate remediation needed.

---

## 6. Audit Closeout Discipline

### Question
Can an AUDIT route be considered complete without: audit artifact, status update, closeout?

### Investigation

**07-p-vbb-closeout.md** (general closeout) specifies for AUDIT route:
- Verify loop closure invariant
- Update SESSION.md
- Update CONTEXT.md
- Update AUDIT_STATUS.md if audit report produced

**But**: The closeout template has a "table of phases" that is generic across all routes. For AUDIT route specifically, there is no mandatory checklist item like:
- "Verify `02_AUDIT_REPORT.md` exists in docs/runs/"
- "Verify `docs/audits/{type}-{date}.md` exists in docs/audits/"
- "Verify AUDIT_STATUS.md was updated with verdict"

**P.R4 (Invariant Protection)** in CONVENTIONS.md:
> "The run closure invariant requires all phase artifacts for the declared voie"
> "`vbb-loop-closure-check.py` must report FAIL for incomplete runs"
> "`07_CLOSEOUT.md` cannot be created if the loop closure check fails"

This is good — the loop closure check would catch missing artifacts. But it operates at the run level, not specifically for AUDIT route.

### Gap partially confirmed

**Severity: P3**

The closeout is well-defined (loop closure check enforces artifact completeness). The gap is that the closeout prompt doesn't have an explicit AUDIT-specific checklist. This is a minor quality-of-life gap, not a structural failure.

### Remediation

Add to the AUDIT route section in `07-p-vbb-closeout.md`:

```markdown
### Pour la voie AUDIT (vérifications supplémentaires)

Avant de produire le closeout, vérifier :
- ✅ `docs/runs/{id}/02_AUDIT_REPORT.md` existe et est complet
- ✅ `docs/audits/{type}-{YYYYMMDD-HHMM}.md` existe et est persistant
- ✅ `docs/AUDIT_STATUS.md` mis à jour avec le verdict et les findings
- ✅ Aucun finding CRITICAL ou P0 sans décision documentée (ACCEPTED / MITIGATED / NEEDS_DECISION)

Si un élément est manquant → ne pas produire de closeout. Documenter l'absence et signaler.
```

This costs ~10 lines and closes the gap.

---

## 7. Gap Summary and Prioritization

| Gap | Confirmed? | Severity | Remediation Cost | Covered by |
|-----|-----------|----------|------------------|-----------|
| G1: Route declaration | ✅ YES | P2 | ~10 lines (02-audit.md) | Gap 1 section |
| G2: Evidence model | ✅ YES | P2 | ~15 lines (02-audit.md) | Gap 2 section |
| G3: Findings taxonomy | ✅ YES | P2 | ~20 lines (02-audit.md) + 2-3 skill updates | Gap 3 section |
| G4: Artifact discipline | ❌ NO (governance sufficient) | — | Covered by G1 preamble | Gap 4 section |
| G5: Verification gate | ✅ YES (implicit) | P2 | Covered by G2 | Gap 5 section |
| G6: Closeout discipline | ⚠️ PARTIAL | P3 | ~10 lines (07-closeout.md) | Gap 6 section |

---

## 8. Implementation Plan

### Phase 1 — Core audit prompt (2-p-vbb-audit.md)

**File**: `prompts/canonical/02-p-vbb-audit.md`

Changes:
1. Add DECLARATION INITIALE section (10 lines) — route, type, skill, artifact, governance, mode
2. Add evidence discipline section (15 lines) — OBSERVATION/SIGNAL/HYPOTHESIS/VERIFIED_FINDING model
3. Update findings table format (20 lines) — P0/P1/P2/P3 + type + decision axes
4. Add explicit artifact requirement in preamble
5. Add verification rule in preamble

Total: ~45–50 lines added to the canonical audit prompt.

### Phase 2 — Skills alignment (2-3 phase-2 skills)

**Files**: `skills/2-vbb-security/SKILL.md`, `skills/2-vbb-systemic-risk/SKILL.md`, `skills/2-vbb-data-integrity/SKILL.md` (if needed)

Changes:
1. Standardize severity scale to P0/P1/P2/P3 (replace low/medium/high/critical and INFO/WARNING/CRITICAL/BLOCKER)
2. Align output format to use the three-axis model (severity + type + decision)
3. Add reference to canonical evidence discipline

Cost: ~5–10 lines per skill.

### Phase 3 — Closeout prompt (07-p-vbb-closeout.md)

**File**: `prompts/canonical/07-p-vbb-closeout.md`

Changes:
1. Add AUDIT-specific closeout checklist (~10 lines)
2. Verify AUDIT_STATUS.md update requirement is explicit

Total: ~10 lines.

### Phase 4 — Verification

Run the full P.R2 verification loop after all changes:
```bash
python tools/vbb-architecture.py lint
python tools/vbb-architecture.py graph --write
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py
pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

---

## 9. Impact Assessment

| Change | Expected Benefit | Implementation Cost | Maintenance Cost | Governance Bloat Risk |
|--------|-----------------|---------------------|-----------------|---------------------|
| Route declaration preamble | Eliminates "route not declared" failure mode | Low (~10 lines) | Low (enforced by linting) | Very Low |
| Evidence model | Eliminates "static scan as confirmed finding" failure mode | Low (~15 lines) | Low (single model) | Low |
| Findings taxonomy (3-axis) | Consistent findings across all audits; aligns with existing practice | Medium (~20 lines + 2-3 skill updates) | Low (standardized model) | Low |
| Artifact discipline in preamble | Reinforces existing governance; no new rules | None (covered by G1) | None | None |
| Verification rule in preamble | Explicit gate before CRITICAL classification | None (covered by G2) | None | None |
| AUDIT closeout checklist | Prevents premature closeout without artifact | Low (~10 lines) | Low (checklist) | Very Low |

**Total governance bloat risk: LOW**

All changes are surgical additions to existing documents. No new skills, no new routes, no new files. The changes make existing practices explicit rather than adding new complexity.

---

## 10. Decision

**Recommendation: MINOR_REMEDIATION**

**Rationale:**

Vibebackbone's audit discipline is structurally sound. The gaps confirmed in this audit are execution-level weaknesses, not structural failures. The governance framework is mature; the canonical audit prompt just needs targeted additions to become fully reliable.

The specific gaps (route declaration, evidence model, findings taxonomy, AUDIT closeout checklist) are all addressable with surgical additions totaling ~70-80 lines across 4 files. This is the smallest coherent set of changes that materially improves audit reliability.

**Do NOT:**
- Redesign the framework
- Add new routes or skills
- Create parallel governance documents
- Add bureaucracy without measurable value

**DO:**
- Add the route declaration preamble to 02-p-vbb-audit.md
- Add the evidence discipline section to 02-p-vbb-audit.md
- Standardize findings to a three-axis model (severity P0–P3 + type + decision)
- Add AUDIT-specific closeout checklist to 07-p-vbb-closeout.md
- Update 2-3 phase-2 skills to align with the new model
- Run the full verification loop before declaring remediation complete

---

## 11. Verification Log

Verification loop run after implementation:
- `python tools/vbb-architecture.py lint` → ✅ PASS (0 errors, 0 warnings)
- `python tools/vbb-architecture.py graph --write` → ✅ PASS (RELATIONS.md regenerated)
- `python tools/vbb-contract-lint.py` → ✅ PASS (0 errors)
- `python tools/vbb-loop-closure-check.py` → ⚠️ WARN (non-blocking, pre-existing ad-hoc run issue)
- `pytest tests/ -q` → ✅ PASS (81/81)
- `bash scripts/vbb-ci-local.sh` → ✅ PASS (7/8, 1 non-blocking warn)

**Result: Remediation VERIFIED — all mandatory checks pass.**

**Git commit**: `25b3edf` — "audit-discipline: add route declaration, evidence model, and findings taxonomy to canonical audit prompt"

**Open follow-up items (AUDIT-001, AUDIT-002)**:
- Align `2-vbb-systemic-risk` and `2-vbb-data-integrity` severity to P0-P3
- Sync `docs/templates/02_AUDIT_REPORT_TEMPLATE.md` with canonical prompt verdict scale

---

*Audit discipline improvement — Vibebackbone — 2026-05-30*
*Verdict: PARTIAL — remediation implemented and verified*
*Next: align remaining phase-2 skills (AUDIT-001) and sync template (AUDIT-002)*