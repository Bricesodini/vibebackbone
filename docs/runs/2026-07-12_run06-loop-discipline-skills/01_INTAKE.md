---
run_id: "2026-07-12_run06-loop-discipline-skills"
phase: "01_INTAKE"
voie: "FAST-STANDARD"
status: "READY"
kind: "INTAKE"
agent: "pi"
started_at: "2026-07-12T23:50:00Z"
---

# 01_INTAKE — Run 06 Loop discipline skills

## Type de intake

**Kind** : `INTAKE` (FAST-STANDARD)
**Source spec** : [`docs/strategy/vbb-improvements-roadmap/runs/run-06-loop-discipline-skills.md`](../../strategy/vbb-improvements-roadmap/runs/run-06-loop-discipline-skills.md)
**Source audit** : [`docs/audits/audit-B-loop-discipline-20260712-1230.md`](../../audits/audit-B-loop-discipline-20260712-1230.md) §AUDIT-B-003 (P2)

## Goal (reformulé depuis spec)

Ajouter une section `## After this skill runs` dans les 5 skills `1-vbb-*` identifiés par AUDIT-B-003, qui :
1. Référence canoniquement `docs/REFERENCE/pre-merge-gate.md` pour P.R2
2. Auto-positionne la skill dans la boucle canonique (`02_AUDIT`)
3. Documente la transition attendue vers `03_DECISION` puis `04_PLAN` (si findings P0/P1)

## Périmètre

**Inclus** : 5 SKILL.md (ajout section `## After this skill runs` uniquement) :
- `skills/1-vbb-code-janitor/SKILL.md`
- `skills/1-vbb-tech-debt/SKILL.md`
- `skills/1-vbb-monolith-detector/SKILL.md`
- `skills/1-vbb-conventions/SKILL.md`
- `skills/1-vbb-formatter/SKILL.md`

**Excluded** :
- ❌ Modification des autres skills `2-vbb-*` (Run ultérieur)
- ❌ Modification des skills `t-vbb-*` (déjà transverse)
- ❌ Canon `CONVENTIONS.md` (P.R2 déjà canon, Pillar 5)
- ❌ `docs/REFERENCE/pre-merge-gate.md` (canon référencé, non touché)
- ❌ Création d'ADR, d'outil, ou de nouveau prompt
- ❌ Remplacement de `phase: 02_AUDIT` (déjà fait par Run 3)
- ❌ Section « Before this skill runs » (non demandée par l'audit)

## Risque canon

**Faible** — modifie uniquement le corps markdown des SKILL.md, pas le canon, pas les outils, pas le frontmatter.

## Pre-merge gate

**SKIP** (route FAST-STANDARD).

## Acceptance criteria (depuis spec §8)

- ✅ 5 SKILL.md ont une section `## After this skill runs`
- ✅ Chaque section référence canoniquement `docs/REFERENCE/pre-merge-gate.md`
- ✅ Chaque section auto-positionne la skill dans la boucle
- ✅ `vbb-contract-lint.py` reste à 0 erreur / 0 warning
- ✅ Aucun canon non lié touché
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

## Statut

**READY** — intake validé, exécution autorisée sur GO utilisateur.