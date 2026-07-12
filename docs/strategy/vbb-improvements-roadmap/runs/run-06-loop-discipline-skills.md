---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run06-loop-discipline-skills
route: FAST-STANDARD
updated: 2026-07-12
---

# Run 06 — Loop discipline skills (P.R2 explicite dans 5 skills `1-vbb-*`)

> **Route** : FAST-STANDARD
> **Effort** : S (~15 min)
> **Risque canon** : faible (modifie uniquement le corps des SKILL.md, pas le canon)
> **Pre-merge gate** : SKIP (route FAST-STANDARD)
> **Statut** : `READY — prêt à exécuter sur GO`

---

## 1. Goal

Ajouter une section **`## After this skill runs`** dans les 5 skills `1-vbb-*` identifiés par AUDIT-B-003, qui :
1. **Référence canoniquement** [`docs/REFERENCE/pre-merge-gate.md`](../../../REFERENCE/pre-merge-gate.md) pour P.R2 (sans dupliquer le contenu — rule "no parallel truth").
2. **Auto-positionne** la skill dans la boucle canonique : « you are a `02_AUDIT` skill, your output feeds `04_PLAN` si findings P0/P1 ».
3. **Documente la transition attendue** : `04_PLAN` si findings P0/P1, sinon `07_CLOSEOUT` (skip plan).

**Cible canon (déjà posée)** : `docs/CONVENTIONS.md` Pillar 5 → P.R2 (`docs/REFERENCE/pre-merge-gate.md`).

---

## 2. Findings source

| ID | Finding | Fichier | Sévérité |
|----|---------|---------|----------|
| **AUDIT-B-003** | 5 skills `1-vbb-*` (code-janitor, tech-debt, monolith-detector, conventions, formatter) — aucune référence à P.R2, pre-merge-gate, ou phases 01-07 | `docs/audits/audit-B-loop-discipline-20260712-1230.md` | P2 |

**Source audit** : [`docs/audits/audit-B-loop-discipline-20260712-1230.md`](../../../audits/audit-B-loop-discipline-20260712-1230.md)

**Note** : R-B-1 (audit prompt), R-B-2 (decision prompt), R-B-3 (execution prompt), R-B-4 (frontmatter phase) sont déjà adressés par Run 2 et Run 3. Run 6 cible **R-B-5** (section explicite de transition dans chaque skill `1-vbb-*`).

---

## 3. Modifications (5 SKILL.md)

Pour chaque skill, ajouter une section `## After this skill runs` à la fin du fichier (avant `## VERDICT RULES` ou en queue de document, après les output contracts).

### 3.1 — `skills/1-vbb-code-janitor/SKILL.md`

**Insertion** : après `## OUTPUT CONTRACT` (ligne 222), avant `## Context` (ligne 222 — peut nécessiter un ajustement).

**Section à ajouter** :

```markdown
## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md`
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` if findings include P0/P1
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).
```

### 3.2 — `skills/1-vbb-tech-debt/SKILL.md`

**Section à ajouter** :

```markdown
## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state (incl. janitor findings if `1-vbb-code-janitor` was run first)
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md`
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` if findings include P0/P1
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).
```

### 3.3 — `skills/1-vbb-monolith-detector/SKILL.md`

**Section à ajouter** :

```markdown
## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md`
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` if findings include P0/P1 (likely, since monolith patterns usually require refactor)
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).
```

### 3.4 — `skills/1-vbb-conventions/SKILL.md`

**Section à ajouter** :

```markdown
## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md`
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` if findings include P0/P1
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).
```

### 3.5 — `skills/1-vbb-formatter/SKILL.md`

**Section à ajouter** :

```markdown
## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md` (this skill proposes a plan only, no execution)
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` (always, since this skill's output is itself a plan)
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).
```

---

## 4. Justification du contenu

| Élément | Pourquoi |
|---------|----------|
| **« This is a `02_AUDIT` skill »** | Auto-positionnement explicite dans la boucle 01-07 (résout partiellement AUDIT-B-004 sur ces 5 skills). |
| **Référence à `pre-merge-gate.md`** | Respect de la règle « no parallel truth » — P.R2 canon est dans ce fichier, on ne duplique pas les 5 vérifications. |
| **« 04_PLAN if findings P0/P1 »** | Distinction comportementale : un audit sans finding P0/P1 peut closer directement (skip plan). Un audit avec finding P0/P1 doit passer par 04_PLAN puis 05_EXECUTION. Cohérent avec R-B-1 (Run 2). |
| **Référence à `03-p-vbb-decision.md`** | Cohérence avec R-B-2 (Run 2) : la transition depuis AUDIT est toujours via DECISION. |
| **Différence pour `1-vbb-formatter`** | Ce skill produit un plan d'enforcement, donc 04_PLAN est toujours nécessaire (logique propre à ce skill). |

---

## 5. Excluded

- ❌ Modification des autres skills `2-vbb-*` (Run ultérieur, hors scope Run 6)
- ❌ Modification des skills `t-vbb-*` (déjà transverse)
- ❌ Modification du canon `CONVENTIONS.md` (P.R2 déjà canon, voir Pillar 5)
- ❌ Modification de `docs/REFERENCE/pre-merge-gate.md` (canon, non touché)
- ❌ Création d'ADR, d'outil, ou de nouveau prompt
- ❌ Remplacement de `phase: 02_AUDIT` (déjà fait par Run 3)
- ❌ Section « Before this skill runs » — non demandée par l'audit ; pourrait être ajoutée dans un futur run

---

## 6. Process

1. Ajouter la section `## After this skill runs` dans chacun des 5 SKILL.md (position : fin du fichier, après les output contracts, avant le verdict rules — à ajuster selon la structure existante)
2. Vérifier `vbb-contract-lint.py` reste à 0 erreur / 0 warning (modifications purement markdown)
3. Vérifier qu'aucun canon non lié n'est touché
4. Produire `01_INTAKE.md`, `05_PATCH_SUMMARY.md`, `07_CLOSEOUT.md`
5. Mettre à jour `docs/ACTIVITY_LOG.md`
6. Git commit

---

## 7. Verification

```bash
# 1. vbb-contract-lint.py (ne doit pas changer)
python tools/vbb-contract-lint.py
# Attendu : "0 error(s), 0 warning(s) found"

# 2. Section "After this skill runs" présente dans les 5 skills
for f in 1-vbb-code-janitor 1-vbb-tech-debt 1-vbb-monolith-detector 1-vbb-conventions 1-vbb-formatter; do
  grep -c "After this skill runs" skills/$f/SKILL.md
done
# Attendu : 1 hit chacun

# 3. Référence canonique pre-merge-gate présente
for f in 1-vbb-code-janitor 1-vbb-tech-debt 1-vbb-monolith-detector 1-vbb-conventions 1-vbb-formatter; do
  grep -c "pre-merge-gate.md" skills/$f/SKILL.md
done
# Attendu : >= 1 hit chacun

# 4. Aucun canon non lié touché
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/REFERENCE/pre-merge-gate.md tools/vbb-contract-lint.py
# Attendu : vide
```

---

## 8. Acceptance criteria

Run 6 est **COMPLET** si :

- ✅ 5 SKILL.md ont une section `## After this skill runs`
- ✅ Chaque section référence canoniquement `docs/REFERENCE/pre-merge-gate.md`
- ✅ Chaque section auto-positionne la skill dans la boucle (`02_AUDIT`, transition vers `03_DECISION` puis `04_PLAN`)
- ✅ `vbb-contract-lint.py` reste à 0 erreur / 0 warning
- ✅ Aucun canon non lié touché (CONVENTIONS.md, PILOTAGE.md, AGENTIC_RUN_PROTOCOL.md, pre-merge-gate.md, vbb-contract-lint.py)
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

---

## 9. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/audits/audit-B-loop-discipline-20260712-1230.md`](../../../audits/audit-B-loop-discipline-20260712-1230.md) — source AUDIT-B-003
- [`../../../docs/REFERENCE/pre-merge-gate.md`](../../../REFERENCE/pre-merge-gate.md) — canon P.R2 référencé
- [`../../../docs/CONVENTIONS.md`](../../../CONVENTIONS.md) — Pillar 5 / P.R2 (canon)
- [`../../../prompts/canonical/02-p-vbb-audit.md`](../../../prompts/canonical/02-p-vbb-audit.md) — boucle AUDIT (R-B-1, Run 2)
- [`../../../prompts/canonical/03-p-vbb-decision.md`](../../../prompts/canonical/03-p-vbb-decision.md) — boucle DECISION (R-B-2, Run 2)
- [`../../../prompts/canonical/05-p-vbb-execution.md`](../../../prompts/canonical/05-p-vbb-execution.md) — P.R2 (R-B-3, Run 2)