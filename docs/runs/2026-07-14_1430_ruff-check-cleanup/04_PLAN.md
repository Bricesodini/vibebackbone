---
run_id: "2026-07-14_1430_ruff-check-cleanup"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:29:00+02:00"
ended_at: "2026-07-14T14:30:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Ruff check cleanup

## Objectif

Fermer les 37 findings Ruff sans modifier les contrats ni le comportement.

## Pré-conditions

- ADR 0035 ACCEPTED.
- Janitor scopé PARTIAL avec quatre classes bornées.
- POC diff safe-fix revu et Integration Gate PASS avant mutation.

## Étapes ordonnées

1. Appliquer uniquement `ruff check --fix` (safe fixes).
2. Revoir le diff des 25 corrections automatiques.
3. Corriger manuellement F841, E741 et E402 restants.
4. Lancer les tests ciblés des fichiers touchés, Ruff puis P.R2.
5. Mettre à jour QOA-007 sans le fermer avant format/mypy/CI.

## Critères d'acceptation

- `ruff check tools tests` = 0.
- Aucun `noqa`, ignore ou exclusion ajouté.
- Tests dashboard, executor, runtime et loop closure verts.
- Suite globale et CI locale vertes.

## Plan de rollback global

Revenir au commit Wave 2 `4ebfbc4`; aucun format persistant n'est migré.

## Risques identifiés

- Suppression accidentelle d'un appel de fixture à effet de bord.
- Renommage incohérent d'un élément de tuple.
- Modification involontaire d'une chaîne de sortie.

## Analyse d'impact

Contract Tooling Core et tests uniquement. Les quatre distributions héritent ;
aucun adapter, contrat ou configuration de gate ne change.

## Integration Gate

- ADR: `docs/adr/0035-supported-python-static-toolchain.md`
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
