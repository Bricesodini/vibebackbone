---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run03-phase-frontmatter
route: FAST-STANDARD
updated: 2026-07-12
phase_phase_label: "Run 3 — Phase frontmatter explicite + cartographie canonique"
---

# Run 03 — Phase frontmatter explicite + cartographie canonique (FAST-STANDARD)

> **Route** : FAST-STANDARD
> **Effort** : S (~25 min)
> **Risque canon** : semi (introduit `docs/PHASE_TO_SKILLS.md` comme référence de cartographie phase↔skill, mais ne touche pas le canon CONVENTIONS.md / PILOTAGE.md)
> **Pre-merge gate** : SKIP (route FAST-STANDARD, cf. `docs/REFERENCE/pre-merge-gate.md`)
> **Statut** : `READY — prêt à exécuter sur GO`

---

## 1. Goal

Remplacer la valeur générique `phase: 1` dans les 5 skills `1-vbb-*` par une valeur explicite `phase: 02_AUDIT`, et créer `docs/PHASE_TO_SKILLS.md` comme cartographie canonique phase↔skill (single source of truth pour la cartographie).

---

## 2. Findings source

| ID | Finding | Fichier |
|----|---------|---------|
| **AUDIT-B-004** | Le frontmatter `phase:` des skills est ambigu (valeur numérique `1`) et il n'existe aucune cartographie canonique phase↔skill | 5 skills `skills/1-vbb-*/SKILL.md` |

**Source audit** : `docs/audits/audit-B-loop-discipline-20260712-1230.md`

---

## 3. Modifications

### QW-3.1 — Création de `docs/PHASE_TO_SKILLS.md` (cartographie canonique)

**Nouveau fichier** : `docs/PHASE_TO_SKILLS.md`

**Contenu** : cartographie explicite des phases agentiques (01-07) vers les skills, avec règle de mise à jour et exemple.

### QW-3.2 — Frontmatter `phase: 02_AUDIT` sur 5 skills `1-vbb-*`

Remplacement de `phase: 1` par `phase: 02_AUDIT` dans le frontmatter de :

| Fichier | Modif |
|---------|-------|
| `skills/1-vbb-code-janitor/SKILL.md` | `phase: 1` → `phase: 02_AUDIT` |
| `skills/1-vbb-tech-debt/SKILL.md` | `phase: 1` → `phase: 02_AUDIT` |
| `skills/1-vbb-monolith-detector/SKILL.md` | `phase: 1` → `phase: 02_AUDIT` |
| `skills/1-vbb-conventions/SKILL.md` | `phase: 1` → `phase: 02_AUDIT` |
| `skills/1-vbb-formatter/SKILL.md` | `phase: 1` → `phase: 02_AUDIT` |

**Justification** : la valeur `1` était ambiguë (la "phase 1" du modèle agentique 01-07 inclut en réalité INTAKE, AUDIT, DECISION, PLAN, EXECUTION, REVIEW, CLOSEOUT). La valeur `02_AUDIT` est explicite : ces skills sont des **audits structurels** qui produisent un rapport. Ils correspondent à la phase 02 du modèle agentique canonique (cf. `prompts/canonical/02-p-vbb-audit.md`).

**Note importante** : cette modification est **non-rétrocompatible** pour les consommateurs qui parsent le frontmatter et s'attendent à un entier. Cependant :
- Aucun outil canonique (`tools/vbb-*.py`) ne parse `phase:` à ce jour.
- La cartographie dans `docs/PHASE_TO_SKILLS.md` documente la convention.

---

## 4. Contenu de `docs/PHASE_TO_SKILLS.md`

```markdown
---
context_role: phase-mapping
phase: transverse
status: canonical
updated: 2026-07-12
---

# PHASE_TO_SKILLS — Cartographie canonique phase ↔ skill

> **Statut** : canonique pour la cartographie phase↔skill. Single source of truth.
> **Référence agentique** : [prompts/canonical/02-p-vbb-audit.md](../../prompts/canonical/02-p-vbb-audit.md) et 7 phases canoniques.

## Convention `phase:` dans le frontmatter SKILL.md

| Valeur `phase:` | Phase agentique | Description |
|-----------------|------------------|-------------|
| `0` | Readiness & cadrage | Gate, scope freeze, audit readiness, RICO readiness |
| `01_INTAKE` | INTAKE | Réception et cadrage initial |
| `02_AUDIT` | AUDIT | Production de rapports d'audit (read-only) |
| `03_DECISION` | DECISION | Prise de décision documentée |
| `04_PLAN` | PLAN | Planification détaillée |
| `05_EXECUTION` | EXECUTION_RUN_N | Implémentation d'un run |
| `06_REVIEW` | REVIEW | Review d'un patch |
| `07_CLOSEOUT` | CLOSEOUT | Clôture d'un run |
| `1` | _deprecated_ | Valeur ambiguë, à remplacer par `02_AUDIT` |
| `2` | _deprecated_ | Valeur ambiguë, à remplacer par `02_AUDIT` (audits de fond) |
| `3` | _deprecated_ | Valeur ambiguë |
| `4` | _deprecated_ | Valeur ambiguë |
| `t` | transverse | Skills transverses (Docker, Git, CI, deployment, etc.) |
| `transverse` | transverse | Idem `t` (alias explicite) |

## Cartographie actuelle (par phase canonique)

### Phase 02_AUDIT (audits structurels phase 1)

| Skill | Description courte |
|-------|---------------------|
| `1-vbb-code-janitor` | Stabilisation non-créative (entropie) |
| `1-vbb-tech-debt` | Diagnostic dette technique |
| `1-vbb-monolith-detector` | Détection patterns monolithiques |
| `1-vbb-conventions` | Harmonisation conventions repo |
| `1-vbb-formatter` | Plan enforcement formatter/linter |

### Phase 02_AUDIT (audits de fond phase 2)

| Skill | Description courte |
|-------|---------------------|
| `2-vbb-api-auditor` | Audit API vs contrats |
| `2-vbb-data-integrity` | Audit invariants métier |
| `2-vbb-db-robustness` | Audit robustesse DB |
| `2-vbb-security` | Audit sécurité |
| ... (10 autres) | ... |

### Phase transverse

| Skill | Description courte |
|-------|---------------------|
| `t-vbb-commit-ready` | Package commit + message conventionnel |
| `t-vbb-session-handoff` | Compression handoff de session |
| ... (15 autres) | ... |

## Règle de mise à jour

Toute nouvelle skill DOIT avoir son `phase:` aligné sur la convention ci-dessus.
Toute modification de `phase:` doit être tracée dans ce fichier (pas de drift silencieux).

## Liens

- [skills/0-vbb-standard/SKILL.md](../../skills/0-vbb-standard/SKILL.md) — frontmatter standard
- [prompts/canonical/02-p-vbb-audit.md](../../prompts/canonical/02-p-vbb-audit.md) — phase 02 AUDIT
- [docs/PILOTAGE.md](PILOTAGE.md) — routes et familles
- [docs/AGENTIC_RUN_PROTOCOL.md](AGENTIC_RUN_PROTOCOL.md) — protocole 7 phases
```

---

## 5. Excluded

- ❌ Modification des autres skills `2-vbb-*` (phase 2 audits de fond — Run 6+)
- ❌ Modification des skills `t-vbb-*` (déjà transverse — non concernés par ce run)
- ❌ Modification du canon `CONVENTIONS.md` ou `PILOTAGE.md`
- ❌ Création d'outils, d'ADR, ou de nouveau prompt

---

## 6. Process

1. Créer `docs/PHASE_TO_SKILLS.md` avec le contenu ci-dessus
2. Modifier le frontmatter des 5 skills `1-vbb-*` (`phase: 1` → `phase: 02_AUDIT`)
3. Vérifier `git diff` ne montre aucun canon modifié
4. Vérifier qu'aucun outil `tools/vbb-*.py` ne parse `phase:` (sanity check)
5. Produire `05_PATCH_SUMMARY.md` et `07_CLOSEOUT.md`
6. Mettre à jour `docs/ACTIVITY_LOG.md`
7. Git commit

---

## 7. Verification

```bash
# 1. Aucun canon modifié
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md
# Attendu : vide

# 2. Aucun outil ne parse `phase:`
grep -rn '"phase"' tools/ | grep -v 'phase_router\|phase-router'
# Attendu : vide ou seulement les usages documentés

# 3. Tous les 5 skills ont phase: 02_AUDIT
for f in 1-vbb-code-janitor 1-vbb-tech-debt 1-vbb-monolith-detector 1-vbb-conventions 1-vbb-formatter; do
  grep "phase:" skills/$f/SKILL.md
done
# Attendu : phase: 02_AUDIT pour les 5

# 4. PHASE_TO_SKILLS.md existe
test -f docs/PHASE_TO_SKILLS.md && echo "OK"
```

---

## 8. Acceptance criteria

Run 3 est **COMPLET** si :

- ✅ `docs/PHASE_TO_SKILLS.md` créé
- ✅ 5 skills `1-vbb-*` ont `phase: 02_AUDIT` (au lieu de `phase: 1`)
- ✅ `git diff` canon = vide
- ✅ Aucun outil canonique cassé par le changement de format
- ✅ `05_PATCH_SUMMARY.md` existe
- ✅ `07_CLOSEOUT.md` existe avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` contient la ligne
- ✅ git commit effectué

---

## 9. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/audits/audit-B-loop-discipline-20260712-1230.md`](../../../docs/audits/audit-B-loop-discipline-20260712-1230.md) — AUDIT-B-004
- [`../../../prompts/canonical/02-p-vbb-audit.md`](../../../prompts/canonical/02-p-vbb-audit.md) — phase 02 AUDIT canonique
- [`../../../docs/AGENTIC_RUN_PROTOCOL.md`](../../../docs/AGENTIC_RUN_PROTOCOL.md) — protocole 7 phases
