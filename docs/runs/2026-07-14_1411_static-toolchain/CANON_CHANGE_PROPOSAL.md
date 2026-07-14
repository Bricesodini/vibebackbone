---
run_id: "2026-07-14_1411_static-toolchain"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-14T14:11:00+02:00"
human_validated_by: "Brice — Go"
---

# Canon Change Proposal — Supported Python static toolchain

## Current Canon

`docs/CONVENTIONS.md` définit la lisibilité, la cohérence et P.R2, mais ne
désigne aucun formatter, linter ou type checker Python supporté.

## Problem

Les outils locaux ne sont ni versionnés ni configurés, leurs résultats ne sont
pas reproductibles et Pyright apparaît dans la dette sans contrat réel.

## Proposed Canon

Ruff 0.13.1 assure check + format, mypy 2.1.0 assure le typage de `tools/`, avec
Python 3.11. Pyright est hors contrat. La CI n'est activée qu'après zéro.

## Benefits

1. Une seule vérité de configuration.
2. Résultats reproductibles localement et en CI future.
3. Aucune gate structurellement rouge pendant la migration.

## Risks

1. La phase non-gating pourrait durer ; QOA-007 reste actif.
2. Les versions devront être mises à jour explicitement.
3. Le formatage produira un diff mécanique séparé.

## Impact Analysis

| File | Change type | Description |
|---|---|---|
| `docs/CONVENTIONS.md` | canon | toolchain et cycle de promotion |
| `pyproject.toml` | config | paramètres partagés |
| `requirements-dev.txt` | dependency | versions exactes |
| `docs/ARCHITECTURE.md` | trace | surface quality tooling |

Le bloc Contract Tooling et les quatre distributions héritent de la convention.
Aucun skill, prompt, adapter ou runtime provider ne change.

## Migration Plan

1. Configurer et mesurer sans gate.
2. Nettoyer Ruff, format puis mypy dans Wave 3.
3. Promouvoir local + GitHub CI seulement à zéro.

## Backward Compatibility

- [x] Fully backward compatible — no action required from consumers

## Human Decision

- [x] **Approved** — Brice, `Go`, 2026-07-14

## Verification Loop

P.R2 complète avant closeout ; checks statiques attendus rouges et non-gating
jusqu'à Wave 3.

## Closeout Notes

Configuration appliquée sans exclusion et baseline reproduite. P.R2 consignée
dans le closeout du run.

**Final status**: CLOSED **Closed by**: Codex **Date**: 2026-07-14
