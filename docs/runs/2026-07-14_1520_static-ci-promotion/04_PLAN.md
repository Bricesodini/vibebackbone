---
run_id: "2026-07-14_1520_static-ci-promotion"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T15:17:00+02:00"
ended_at: "2026-07-14T15:19:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Static CI promotion

## Objectif

Transformer les trois invariants statiques propres en gates bloquantes avec
parité locale/distante et preuve de détection.

## Pré-conditions

- ADR 0021 et ADR 0035 ACCEPTED.
- Ruff check/format et mypy passent sur main propre.
- Audit CI PARTIAL avec correctif borné.
- POC et Integration Gate PASS avant mutation.

## Étapes ordonnées

1. Ajouter un test de wiring local/remote et des versions dev.
2. Installer `requirements-dev.txt` dans GitHub Actions.
3. Ajouter Ruff check, Ruff format et mypy aux deux CI.
4. Mettre à jour le préflight local et les compteurs de checks.
5. Prouver l'échec de chaque commande sur une fixture temporaire contrôlée.
6. Restaurer, passer les trois gates, tests, P.R2 et workflow distant.
7. Fermer QOA-007 seulement après matrice distante verte.

## Critères d'acceptation

- Local CI 12/12 et workflow distant Ubuntu/macOS verts.
- Chaque commande retourne non-zéro sur sa violation dédiée puis zéro restaurée.
- Test de wiring empêche le retrait silencieux d'un check ou du manifest dev.
- Permissions et triggers GitHub inchangés.

## Plan de rollback global

Revenir au commit `a708165`; aucun état externe hors workflow du push.

## Risques identifiés

- Parité textuelle sans parité d'environnement.
- Échec de module absent si manifest incorrect.
- Workflow durablement rouge après promotion.

## Analyse d'impact

Bloc CI/CD et Contract Tooling Core. Les quatre distributions héritent de la
gate de repository ; aucun adapter/runtime provider ne change.

## Integration Gate

- ADR: `docs/adr/0035-supported-python-static-toolchain.md`
- ADR liée: `docs/adr/0021-ci-gate-enforcement.md`
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
