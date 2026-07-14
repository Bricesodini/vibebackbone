---
run_id: "2026-07-14_1440_ruff-format"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:39:00+02:00"
ended_at: "2026-07-14T14:40:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Ruff format baseline

## Objectif

Passer la baseline formatter de 29 fichiers à zéro sans changement sémantique.

## Pré-conditions

- ADR 0035 ACCEPTED et Ruff check déjà à zéro.
- Diff formatter read-only inventorié : 29 fichiers, 4 déjà conformes.
- Integration Gate PASS avant formatage.

## Étapes ordonnées

1. Capturer les AST normalisés des 29 fichiers.
2. Exécuter `ruff format tools tests` une seule fois.
3. Comparer les AST et inspecter le stat/diff.
4. Exécuter Ruff check/format check, pytest et P.R2.
5. Mettre à jour QOA-007 vers mypy 20 + gate restant.

## Critères d'acceptation

- 33/33 fichiers conformes après formatage.
- AST avant/après identique pour chaque fichier.
- Ruff check zéro, 180 tests + CI locale verts.
- Aucun renommage, suppression ou ajout logique.

## Plan de rollback global

Revenir au commit `513eb2e`; le formatage ne porte aucune migration de donnée.

## Risques identifiés

- Diff volumineux masquant un changement non mécanique.
- Outil/version différents entre configuration et exécution.

## Analyse d'impact

Formatage de Contract Tooling Core et tests. Les quatre distributions héritent
du code identique ; aucun adapter, contrat, output ou gate ne change.

## Integration Gate

- ADR: `docs/adr/0035-supported-python-static-toolchain.md`
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
