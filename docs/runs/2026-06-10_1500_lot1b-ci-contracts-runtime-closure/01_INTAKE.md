# 01_INTAKE — RUN 03 · Lot 1B : Étendre la CI contrats/runtime/closure

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

## Objectif

Étendre la CI (GitHub Actions + script local) pour vérifier mécaniquement les contrats, le runtime dry-run, la fermeture des runs, et les tests.

## Scope autorisé

- `.github/workflows/**`
- `scripts/vbb-ci-local.sh`
- `tools/vbb-contract-lint.py` (adaptation mineure)
- `tools/vbb-contract-runtime.py` (adaptation mineure)
- `tools/vbb-loop-closure-check.py` (adaptation mineure)
- `tests/**`
- `docs/AUDIT_STATUS.md`
- `docs/CONTEXT.md`
- `docs/runs/2026-06-10_1500_lot1b-ci-contracts-runtime-closure/`

## Interdictions

- Pas de nouveaux CONTRACT.yaml
- Pas de modification de SKILL.md
- Pas de modification de setup.sh
- Pas de modification des hooks git
- Pas de dashboard/compactor
- Pas de changement de philosophie des voies

## Risques

| ID | Risque | Mitigation |
|----|--------|------------|
| R-III-01 | GitHub Actions matrix trop coûteuse | Commencer par ubuntu-latest + macos-latest, Python 3.11 seul |
| R-III-02 | Loop closure check PARTIAL/BLOCKED sur runs en cours | Tolerer PARTIAL sur le closure check (exit 0 si ≤ 1 BLOCKED connu) |
| R-III-03 | Tests smoke-contract-runtime.sh écrit des traces |dry-run uniquement dans CI |
| R-III-04 | Compatibilité macos vs ubuntu (python3 path) | Utiliser `python3` partout, pas de chemin absolu |

## Critères de succès

- [ ] Workflow GitHub Actions créé ou mis à jour
- [ ] Script local `scripts/vbb-ci-local.sh` créé
- [ ] Checks contrats/runtime/closure/tests exécutables
- [ ] CI locale PASS
- [ ] Aucun changement hors scope
- [ ] docs/CONTEXT.md et docs/AUDIT_STATUS.md mis à jour