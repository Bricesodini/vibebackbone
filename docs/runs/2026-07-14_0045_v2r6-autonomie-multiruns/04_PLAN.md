---
run_id: "2026-07-14_0045_v2r6-autonomie-multiruns"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T23:20:00Z"
ended_at: "2026-07-13T23:24:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/adr/0031-autonomous-multirun-protocol.md (ACCEPTED)"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — v2r6-autonomie-multiruns

## Objectif

Section « Runs autonomes » canonique dans AGENTIC_RUN_PROTOCOL.md (bornes,
gate inter-runs, clôture, stop conditions — ADR-0031) ; LONG_RUN_RULE.md → stub.

## Pré-conditions

- Gate `can_code_start=true` (ADR-0031 liaison stricte, POC non requise).
- V2-R1 (gate fiable) et V2-R4 (40/75 + 4bis) livrés.

## Étapes ordonnées

| # | Action | Fichiers |
|---|--------|----------|
| 1 | Section « Runs autonomes (ADR-0031) » : séquence déclarée, 3 runs max, loop-closure --strict inter-runs, CLOSE-FINAL auto / CLOSE-HANDOFF interruption, 5 stop conditions, hygiène intra-run inchangée | `docs/AGENTIC_RUN_PROTOCOL.md` |
| 2 | LONG_RUN_RULE.md → stub de redirection (liens entrants préservés ; budgets restent dans PILOTAGE) | `docs/LONG_RUN_RULE.md` |
| 3 | Rule 12 : entrée Decisions log | `docs/DISTRIBUTIONS.md` |
| 4 | P.R2 + closeout CLOSE-FINAL + SESSION/ACTIVITY + commit/push | docs du run |

## Critères d'acceptation

- La section canonique énonce les 6 points de l'ADR-0031, sans dupliquer
  PILOTAGE (budgets) ni SESSION_RULES (40/75 — cités par chemin).
- LONG_RUN_RULE.md ≤ 15 lignes, redirection explicite.
- P.R2 5/5 PASS.

## Risques identifiés

- N=3 non validé terrain (assumé, ADR-0031, révisable par CCP).
- Liens entrants vers LONG_RUN_RULE : préservés par le stub (vérif grep faite).

## Rollback

`git revert` du commit du run (docs uniquement).
