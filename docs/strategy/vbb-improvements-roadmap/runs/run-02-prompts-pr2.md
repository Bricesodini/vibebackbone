---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run02-prompts-pr2
route: FAST-MINIMAL
updated: 2026-07-12
phase_phase_label: "Run 2 — Prompts canoniques adoptent P.R2"
---

# Run 02 — Prompts canoniques adoptent P.R2 (FAST-MINIMAL)

> **Route** : FAST-MINIMAL
> **Effort** : S (~15 min)
> **Risque canon** : aucun (les prompts canoniques sont des guides, pas du canon)
> **Pre-merge gate** : SKIP (route FAST-MINIMAL, cf. `docs/REFERENCE/pre-merge-gate.md`)
> **Statut** : `READY — GO reçu`

---

## 1. Goal

Aligner 3 prompts canoniques sur les nouvelles conventions de loop discipline introduites par Run 1+ : ajouter la mention explicite de la phase suivante (pour 02-audit et 03-decision) et la référence canonique à `@pre-merge-gate.md` (pour 05-execution).

---

## 2. Findings source

| ID | Finding | Fichier |
|----|---------|---------|
| **AUDIT-B-001 (1/2)** | Le prompt `02-p-vbb-audit.md` ne mentionne pas explicitement la transition vers `03_DECISION` (loop discipline) | `prompts/canonical/02-p-vbb-audit.md` |
| **AUDIT-B-001 (2/2)** | Le prompt `03-p-vbb-decision.md` ne mentionne pas explicitement la transition vers `04_PLAN` | `prompts/canonical/03-p-vbb-decision.md` |
| **AUDIT-B-002** | Le prompt `05-p-vbb-execution.md` ne référence pas `@pre-merge-gate.md` ni les 5 vérifications P.R2 canoniques | `prompts/canonical/05-p-vbb-execution.md` |

**Source audit** : `docs/audits/audit-B-loop-discipline-20260712-1230.md`

---

## 3. Modifications

### QW-2.1 — `02-p-vbb-audit.md` : ajouter section "Next Phase"

**Action** : ajouter en bas du fichier (avant le footer éventuel) une section explicite :

```markdown
## Next phase

After `02_AUDIT` completes, transition explicitly to `03_DECISION` via
[`03-p-vbb-decision.md`](03-p-vbb-decision.md). The decision phase consumes
the audit report (typically `02_AUDIT_REPORT.md` or inline in `01_INTAKE.md`)
and produces a verdict (`READY` / `PARTIAL` / `BLOCKED` / `UNKNOWN`) plus a
chosen route family (`RAPIDE` / `STRUCTUREE` / `AUDIT` / `CLOTURE`).
```

### QW-2.2 — `03-p-vbb-decision.md` : ajouter section "Next Phase"

**Action** : ajouter une section analogue pointant vers `04_PLAN` :

```markdown
## Next phase

After `03_DECISION` completes, transition explicitly to `04_PLAN` via
[`04-p-vbb-plan.md`](04-p-vbb-plan.md). The plan phase consumes the
decision verdict and produces a structured implementation plan
(typically `04_PLAN.md`) with chunked, testable units, dependencies,
and risks flagged before code.
```

### QW-2.3 — `05-p-vbb-execution.md` : référencer `@pre-merge-gate.md`

**Action** : ajouter dans la section de pré-conditions (input contract ou process) une référence canonique :

```markdown
## Pre-merge gate (P.R2)

Before declaring the implementation complete, the executor MUST pass the
**5 canonical P.R2 verifications** defined in
[`docs/REFERENCE/pre-merge-gate.md`](../../../docs/REFERENCE/pre-merge-gate.md):

1. (canonical verification 1)
2. (canonical verification 2)
3. (canonical verification 3)
4. (canonical verification 4)
5. (canonical verification 5)

If any verification fails, the implementation is **NOT** complete and the
executor must either fix and re-verify or escalate via `02-p-vbb-audit.md`.
```

(Les 5 vérifications sont détaillées dans `pre-merge-gate.md` — ne pas les dupliquer ici.)

---

## 4. Excluded

- ❌ Modification des 5 fichiers `01-p-vbb-intake.md`, `04-p-vbb-plan.md`, `06-p-vbb-review.md`, `07-p-vbb-closeout.md` (hors scope de ce run)
- ❌ Modification du canon (`docs/CONVENTIONS.md`, `docs/PILOTAGE.md`, `docs/AGENTIC_RUN_PROTOCOL.md`)
- ❌ Création d'outils, d'ADR, ou de nouveau prompt

---

## 5. Process

1. Lire les 3 fichiers cibles pour repérer les zones d'insertion
2. Appliquer les 3 modifications
3. Vérifier `git diff` ne montre aucun canon modifié
4. Vérifier que les références inter-prompt pointent vers des fichiers existants
5. Produire `05_PATCH_SUMMARY.md` et `07_CLOSEOUT.md`
6. Mettre à jour `docs/ACTIVITY_LOG.md`
7. Git commit

---

## 6. Output contract

| Fichier | Kind | Modif |
|---------|------|-------|
| `prompts/canonical/02-p-vbb-audit.md` | source_modified | QW-2.1 |
| `prompts/canonical/03-p-vbb-decision.md` | source_modified | QW-2.2 |
| `prompts/canonical/05-p-vbb-execution.md` | source_modified | QW-2.3 |
| `docs/runs/2026-07-12_run02-prompts-pr2/01_INTAKE.md` | phase_artifact | Copie de cette spec |
| `docs/runs/2026-07-12_run02-prompts-pr2/05_PATCH_SUMMARY.md` | phase_artifact | Résumé des modifs |
| `docs/runs/2026-07-12_run02-prompts-pr2/07_CLOSEOUT.md` | phase_artifact | Closeout formel |

---

## 7. Verification

```bash
# 1. Aucun canon modifié
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md
# Attendu : vide

# 2. Liens inter-prompt valides
ls prompts/canonical/03-p-vbb-decision.md  # doit exister
ls prompts/canonical/04-p-vbb-plan.md      # doit exister
ls docs/REFERENCE/pre-merge-gate.md        # doit exister
# Attendu : tous présents

# 3. ACTIVITY_LOG contient la ligne
grep "Run 02" docs/ACTIVITY_LOG.md
# Attendu : 1 ligne
```

### Pre-merge gate

**SKIP** — route FAST-MINIMAL, voir `docs/REFERENCE/pre-merge-gate.md`.

---

## 8. Acceptance criteria

Run 2 est **COMPLET** si :

- ✅ Les 3 fichiers prompts sont modifiés
- ✅ `git diff` canon = vide
- ✅ Liens inter-prompt valides (`03-p-vbb-decision.md`, `04-p-vbb-plan.md`, `docs/REFERENCE/pre-merge-gate.md` existent)
- ✅ `05_PATCH_SUMMARY.md` existe
- ✅ `07_CLOSEOUT.md` existe avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` contient la ligne
- ✅ git commit effectué

---

## 9. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/audits/audit-B-loop-discipline-20260712-1230.md`](../../../docs/audits/audit-B-loop-discipline-20260712-1230.md) — AUDIT-B
- [`../../../docs/REFERENCE/pre-merge-gate.md`](../../../docs/REFERENCE/pre-merge-gate.md) — canon P.R2
- [`../../../prompts/canonical/02-p-vbb-audit.md`](../../../prompts/canonical/02-p-vbb-audit.md) — fichier modifié QW-2.1
- [`../../../prompts/canonical/03-p-vbb-decision.md`](../../../prompts/canonical/03-p-vbb-decision.md) — fichier modifié QW-2.2
- [`../../../prompts/canonical/05-p-vbb-execution.md`](../../../prompts/canonical/05-p-vbb-execution.md) — fichier modifié QW-2.3