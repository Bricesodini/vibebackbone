---
run_id: "2026-05-27_2159_mvp-start-implementation"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-05-27T20:05:00Z"
ended_at: "2026-05-27T20:10:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/runs/2026-05-27_2154_mvp-start-implementation-plan/04_PLAN.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — MVP Start Implementation

## Objectif

Appliquer les Runs 0-7 du plan de maniere sequentielle, sans activer le run optionnel de prompt dedie.

## Etapes ordonnees

| # | Action | Fichiers cibles | Validation | Rollback |
|---|--------|-----------------|------------|----------|
| 0 | Baseline compteurs/router | aucun | lint + router absent | aucun |
| 1 | Creer protocole MVP Start | `docs/MVP_START_PROTOCOL.md`, `docs/INDEX.md` | recherche sections | retirer document + index |
| 2 | Creer skill RICO | `skills/0-vbb-rico-readiness/`, `skills/INDEX.yaml` | lint + router match | supprimer skill + index |
| 3 | Integrer gouvernance | `docs/PILOTAGE.md`, `docs/AGENTIC_RUN_PROTOCOL.md`, `AGENTS.md`, `SYSTEM.md` | recherche regles | revert paragraphes |
| 4 | Integrer prompts/router | `prompts/`, `docs/router/ROUTER_MATRIX.md` | router + recherche | revert prompts |
| 5 | Router leger/status | `docs/CONTEXT.md`, `docs/AUDIT_STATUS.md` | fichier court + recherche | retirer lignes |
| 6 | Harmoniser compteurs | README/GUIDE/release/provider docs | `rg` compteurs stale | revert docs |
| 7 | Valider et closeout | run artifacts | CI + closure | corriger ou documenter |

## Critères d'acceptation

- `0-vbb-rico-readiness` route pour RICO/MVP/readiness.
- 63 skills et 63 contrats mesures.
- 33 prompts mesures.
- Aucune reference active aux anciens compteurs 62/32 dans les docs vivantes controlees.
- CI locale PASS.
