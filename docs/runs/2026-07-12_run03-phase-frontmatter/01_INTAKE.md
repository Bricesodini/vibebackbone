---
run_id: "2026-07-12_run03-phase-frontmatter"
phase: "01_INTAKE"
voie: "FAST-STANDARD"
status: "READY"
kind: "INTAKE"
agent: "pi"
started_at: "2026-07-12T16:00:00Z"
---

# 01_INTAKE — Run 03 Phase frontmatter

## Type de intake

**Kind** : `INTAKE` (FAST-STANDARD)
**Source spec** : [`docs/strategy/vbb-improvements-roadmap/runs/run-03-phase-frontmatter.md`](../../strategy/vbb-improvements-roadmap/runs/run-03-phase-frontmatter.md)
**Source audit** : [`docs/audits/audit-B-loop-discipline-20260712-1230.md`](../../audits/audit-B-loop-discipline-20260712-1230.md) §AUDIT-B-004

## Goal (reformulé depuis spec)

Remplacer `phase: 1` (valeur numérique ambiguë) par `phase: 02_AUDIT` (valeur explicite alignée sur le protocole 7 phases) dans les 5 skills `1-vbb-*`, et créer `docs/PHASE_TO_SKILLS.md` comme cartographie canonique phase↔skill (single source of truth).

## Périmètre

**Inclus** :
- QW-3.1 : Création `docs/PHASE_TO_SKILLS.md` (cartographie canonique)
- QW-3.2 : Frontmatter `phase: 02_AUDIT` sur 5 skills `1-vbb-*` :
  - `skills/1-vbb-code-janitor/SKILL.md`
  - `skills/1-vbb-tech-debt/SKILL.md`
  - `skills/1-vbb-monolith-detector/SKILL.md`
  - `skills/1-vbb-conventions/SKILL.md`
  - `skills/1-vbb-formatter/SKILL.md`

**Excluded** (cf. spec §5) :
- ❌ Modification des autres skills `2-vbb-*` (Run 6+)
- ❌ Modification des skills `t-vbb-*` (déjà transverse)
- ❌ Modification du canon `CONVENTIONS.md` ou `PILOTAGE.md`
- ❌ Création d'outils, d'ADR, ou de nouveau prompt

## Risque canon

**Semi** (nouveau fichier `docs/PHASE_TO_SKILLS.md` créé comme référence de cartographie, mais `CONVENTIONS.md` / `PILOTAGE.md` intacts).

## Pre-merge gate

**SKIP** (route FAST-STANDARD, autorisé par `docs/REFERENCE/pre-merge-gate.md`).

## Fichiers à modifier

6 fichiers :
- 5 skills `1-vbb-*` (QW-3.2)
- 1 nouveau `docs/PHASE_TO_SKILLS.md` (QW-3.1)

## Acceptance criteria (depuis spec §8)

- ✅ `docs/PHASE_TO_SKILLS.md` créé
- ✅ 5 skills `1-vbb-*` ont `phase: 02_AUDIT`
- ✅ `git diff` canon = vide
- ✅ Aucun outil canonique cassé par le changement de format
- ✅ `05_PATCH_SUMMARY.md` existe
- ✅ `07_CLOSEOUT.md` existe avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` contient la ligne
- ✅ git commit effectué

## Statut

**READY** — intake validé, exécution autorisée sur GO utilisateur.