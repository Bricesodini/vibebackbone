---
run_id: "2026-07-14_0010_executor-correctness"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T00:11:00+02:00"
ended_at: "2026-07-14T00:11:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/audits/intent-decomp-20260714-0007.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Executor correctness

## Objectif

Faire respecter les statuts contractuels imbriqués, la progression de profondeur
et l'interdiction des cycles dans `vbb-executor.py`.

## Pré-conditions

- Gate ADR-0001 : PASS (`can_code_start=true`).
- Défauts reproduits par tests avant correction.
- Worktree initial borné aux artefacts audit/plan produits dans cette session.

## Steps

1. Ajouter des tests qui reproduisent le faux `BLOCKED` et le `RecursionError`.
2. Faire circuler profondeur et chemin de visite dans les gates before/after.
3. Lire le statut contractuel depuis `outputs.status`, avec fallback terminal
   explicite.
4. Vérifier gates statiques, after gates, contrat absent et profondeur maximale.
5. Exécuter la boucle complète et réconcilier uniquement les statuts concernés.

## Files

- `tests/test_executor.py` — créer.
- `tools/vbb-executor.py` — modifier minimalement.
- `docs/ARCHITECTURE.md`, `docs/AUDIT_STATUS.md`, `docs/TECH_DEBT.md` — mise à
  jour factuelle après tests verts.

## Critères d'acceptation

- Cycle : `BLOCKED` avec erreur explicite, jamais `RecursionError`.
- Gate valide : PASS/DONE, jamais faux `BLOCKED`.
- Suite complète et P.R2 vertes.
- Aucun skill, outil supplémentaire ou dépendance.

## Plan de rollback global

Revenir uniquement sur `tools/vbb-executor.py` et `tests/test_executor.py`, puis
rétablir les statuts SYS-POST-001/GMA-003 si un test de régression ou la boucle
P.R2 échoue. Aucun état externe ou migration n'est impliqué.

## Risques identifiés

- Changer la sémantique des gates statiques — couvert par test direct.
- Masquer un cycle sous un `GATE_FAILED` générique — l'erreur circulaire reste
  explicite dans l'exécution imbriquée et testée séparément.
- Élargir en refactor de l'executor — interdit par le budget +30 lignes nettes.

## ADR

- **Liée à ADR** : `docs/adr/0001-formal-executor-boundary.md`
