---
run_id: "2026-07-14_1411_static-toolchain"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:12:00+02:00"
ended_at: "2026-07-14T14:13:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "02_AUDIT.md"
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Static toolchain configuration

## Objectif

Rendre Ruff+mypy reproductibles sans modifier le code Python ni les gates.

## Pré-conditions

- ADR 0035 ACCEPTED et CCP approuvé par Brice.
- Audit formatter/linter READY.
- POC reproductible et Integration Gate PASS avant configuration.

## Étapes ordonnées

1. Passer le POC et l'Integration Gate liés à ADR 0035.
2. Ajouter les versions dev exactes et la configuration sans exclusions.
3. Documenter commandes, périmètres et condition de promotion.
4. Rejouer la baseline, P.R2 et consigner l'impact distributions.

## Critères d'acceptation

- Ruff cible Python 3.11, `tools/` + `tests/`, règles `E4/E7/E9/F`.
- Mypy cible Python 3.11 et `tools/`, avec imports externes manquants ignorés.
- Comptes identiques à la baseline (37, 29, 20), prouvant absence de masque.
- P.R2 verte et aucune modification Python/CI.

## Rollback global

Retirer `pyproject.toml`, `requirements-dev.txt` et la convention ajoutée.

## Risques et impact

Le principal risque est de cacher la dette par configuration ; les exclusions
et ignores globaux sont interdits. Changement Core hérité par quatre
distributions, sans adapter.

## Integration Gate

- ADR: `docs/adr/0035-supported-python-static-toolchain.md`
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
