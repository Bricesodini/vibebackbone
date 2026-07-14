---
run_id: "2026-07-14_1410_executor-cleanup"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:12:00+02:00"
ended_at: "2026-07-14T14:14:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Executor cleanup

## Objectif

Réduire la dette de maintenance et de type sans modifier les sorties ni la
machine d'état de l'executor.

## Pré-conditions

- ADR 0001 ACCEPTED.
- Huit tests directs existants passent.
- Baseline mypy observée : 34 erreurs dans ce module.

## Étapes ordonnées

1. Prouver que les deux surfaces nettoyées sont caractérisables.
2. Passer l'Integration Gate.
3. Ajouter tests loader et writer closeout.
4. Annoter `result` et les signatures, retirer la seconde `_yaml_load`.
5. Renommer `write_closEOUT` et son unique appel interne.
6. Rejouer mypy, tests ciblés, P.R2.
7. Fermer GMA-003 et consigner Core↔distributions.

## Critères d'acceptation

- Mypy executor 0 erreur.
- Deux définitions `_yaml_load` deviennent une.
- Ancien symbole mal casé absent.
- CLI/JSON et états inchangés selon tests.

## Plan de rollback global

Revenir au commit Wave 0 ; aucun format persistant n'est migré.

## Risques identifiés

- Annotation masquant un type réellement incohérent.
- Renommage oublié dans un appel interne.

## Analyse d'impact

- Bloc Contract Tooling Core ; quatre distributions héritent.
- Aucun adapter, contrat YAML ou API externe modifié.

## Integration Gate

- ADR: `docs/adr/0001-formal-executor-boundary.md`
- POC: `POC.md`
- CAN_CODE_START: YES — voir `INTEGRATION_GATE.md`.
