---
run_id: "2026-05-23_1800_artifact-verify-lot-c"
phase: "01_INTAKE"
voie: "RAPIDE"
status: "READY"
agent: "claude-code"
started_at: "2026-05-23T18:00:00Z"
ended_at: "2026-05-23T18:05:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "docs/runs/2026-05-23_1700_contracts-artifact-schema-lot-b-d/07_CLOSEOUT.md"
  - "tools/vbb-contract-runtime.py"
  - "docs/runs/README.md"
artifacts_produced:
  - "docs/runs/2026-05-23_1800_artifact-verify-lot-c/01_INTAKE.md"
---

# 01_INTAKE — artifact-verify-lot-c

## Contexte

Suite directe de PR #2 (Lot B+D). Les contrats déclarent leurs artefacts
(`outputs.artifact` v0.3), mais le runtime ne les vérifie pas encore et
aucune porte ne bloque le commit si un artefact est manquant.

## Objectif

Activer la vérification mécanique des artefacts (Lot C) :

1. Étendre `tools/vbb-contract-runtime.py` — warning + PARTIAL si artefact absent.
2. Créer `tools/vbb-loop-closure-check.py` — vérifie l'invariant de clôture d'un run.
3. Intégrer dans `t-vbb-commit-ready` — BLOCKED si invariant violé.
4. Tests positifs et négatifs.

## Voie

**RAPIDE** — périmètre clair, impact limité à l'outillage, zéro contrat de données.

## Scope

- `tools/` : 2 fichiers (runtime étendu + nouveau loop-closure-check)
- `skills/t-vbb-commit-ready/` : SKILL.md + CONTRACT.yaml
- `tests/` : test_loop_closure.py
- `scripts/` : install-vbb-pre-commit.sh
- `docs/runs/2026-05-23_1800_artifact-verify-lot-c/` : run courant (01+05+07)

## Hors scope

- Bootstrap projet client (`t-vbb-project-context-init`) — PR #4
- Extension aux skills phase 2 — PR #5
- Corrections gouvernance (PILOTAGE, compteurs) — PR #6
