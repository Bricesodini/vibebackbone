---
run_id: "2026-07-14_1500_mypy-cleanup"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:57:00+02:00"
ended_at: "2026-07-14T14:59:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Mypy cleanup

## Objectif

Passer mypy de 20 erreurs à zéro en rendant explicites les structures runtime
existantes, sans modifier leurs valeurs ni leurs sorties.

## Pré-conditions

- ADR 0035 ACCEPTED.
- Audit Tech Debt READY avec cinq classes bornées.
- POC et Integration Gate PASS avant code.

## Étapes ordonnées

1. Annoter les conteneurs vides avec leurs types observés.
2. Distinguer variables `example`/`finding` dans credentials.
3. Corriger l'annotation de ratio dashboard sans changer le calcul.
4. Typer les structures hétérogènes runtime/index.
5. Ajouter un guard explicite autour du dynamic import router.
6. Exécuter mypy, Ruff, tests ciblés, dry-run puis P.R2.

## Critères d'acceptation

- Mypy 20→0 sur `tools/`.
- Aucun ignore/suppression/configuration modifiée.
- Sorties credentials/runtime/dashboard inchangées sous tests.
- Suite globale et CI locale vertes.

## Plan de rollback global

Revenir au commit `e20cd91`; aucune donnée ou interface persistante ne migre.

## Risques identifiés

- Annotation trop large masquant un contrat plus précis.
- Guard dynamic-import changeant le type d'échec observé.
- Structure outputs runtime inférée différemment des usages réels.

## Analyse d'impact

Contract Tooling Core uniquement, sans topologie nouvelle. Les quatre
distributions héritent ; aucun adapter ou gate CI ne change.

## Integration Gate

- ADR: `docs/adr/0035-supported-python-static-toolchain.md`
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
