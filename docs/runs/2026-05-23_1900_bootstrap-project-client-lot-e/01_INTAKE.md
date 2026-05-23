---
run_id: "2026-05-23_1900_bootstrap-project-client-lot-e"
phase: "01_INTAKE"
voie: "RAPIDE"
status: "READY"
agent: "claude-code"
started_at: "2026-05-23T19:00:00Z"
ended_at: "2026-05-23T19:05:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "docs/runs/2026-05-23_1800_artifact-verify-lot-c/07_CLOSEOUT.md"
  - "docs/templates/07_CLOSEOUT.md.template"
  - "skills/INDEX.yaml"
artifacts_produced:
  - "docs/runs/2026-05-23_1900_bootstrap-project-client-lot-e/01_INTAKE.md"
---

# 01_INTAKE — bootstrap-project-client-lot-e

## Contexte

Suite de PR #3 (Lot C). L'invariant de clôture est mécaniquement vérifié.
Prochain besoin identifié : un projet vierge ne peut pas recevoir VBB sans
manipulation manuelle — il faut un skill de bootstrap.

## Objectif

Créer `t-vbb-project-context-init` (Lot E) :

1. `tools/vbb-project-init.py` — outil Python idempotent.
2. `skills/t-vbb-project-context-init/SKILL.md + CONTRACT.yaml`.
3. `skills/INDEX.yaml` mis à jour.
4. Tests positifs et négatifs.

## Voie

**RAPIDE** — périmètre clair, zéro contrat de données, zéro impact prod.

## Scope

- `tools/` : 1 nouveau fichier (`vbb-project-init.py`)
- `skills/t-vbb-project-context-init/` : SKILL.md + CONTRACT.yaml (nouveau)
- `skills/INDEX.yaml` : ajout du skill
- `tests/` : test_project_init.py
- `docs/runs/2026-05-23_1900_bootstrap-project-client-lot-e/` : run courant

## Hors scope

- R-006 (correction des anciens runs PR #1/#2) — hors scope, résolu séparément
- Bootstrap projet client avec VBB pré-installé — couvert par ce Lot
- Extension aux skills phase 2 — PR #5
</content>
</invoke>