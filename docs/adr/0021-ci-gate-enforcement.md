---
template_id: "ADR"
version: "1.0"
lane_eligible:
  - "STRUCTUREE"
  - "AUDIT"
related:
  - "docs/adr/README.md"
  - "docs/CONVENTIONS.md#pr3--gate-before-action"
---

# ADR — 0021-ci-gate-enforcement

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-15  
**Liée à POC**: vide  
**Liée à ADR amont**: 0009, 0012, 0020 (linter, codegen, graph — tous outillés en Run 10+)

## Contexte

La discipline multi-service est désormais outillée (ADR-0009 linter, ADR-0020 graph) et la cohérence canon est vérifiable (ADR-0012 codegen avec `--check`). Mais aucun mécanisme ne **garantit** que ces outils sont exécutés avant chaque merge.

Conséquence : un contributeur peut merger un PR qui casse la discipline multi-service sans aucun signal. Les outils existent mais ne sont pas dans le pipeline CI. La discipline n'est pas enforceable.

## Décision

**Créer un script bash canonique `scripts/vbb-ci-local.sh` qui exécute en séquence les vérifications canoniques, et le brancher sur les hooks CI (GitHub Actions, GitLab CI, etc.) via un snippet copy-paste.**

### Le script canonique

```bash
#!/usr/bin/env bash
# vbb-ci-local.sh — VBB canonical CI gate
# Reference: ADR-0021 (Gap-15 — Gate enforcement)
# Usage: bash scripts/vbb-ci-local.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== VBB CI gate ==="

echo "[1/4] vbb-contract-lint..."
python tools/vbb-contract-lint.py

echo "[2/4] vbb-multiservice-lint (--strict)..."
python tools/vbb-multiservice-lint.py --strict || {
    echo "❌ multiservice-lint failed"
    exit 1
}

echo "[3/4] vbb-multiservice-graph (--check-cycle)..."
python tools/vbb-multiservice-graph.py --check-cycle || {
    echo "❌ cycle detected in service graph"
    exit 1
}

echo "[4/4] vbb-architecture agents --check..."
python tools/vbb-architecture.py agents --check || {
    echo "❌ AGENTS.md / CLAUDE.md drift detected"
    exit 1
}

echo "✅ All gates passed"
```

### Branchement CI

Le snippet copy-paste pour GitHub Actions :

```yaml
# .github/workflows/vbb-ci.yml
name: VBB CI
on: [push, pull_request]
jobs:
  vbb-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: bash scripts/vbb-ci-local.sh
```

Pour GitLab CI, `.gitlab-ci.yml` équivalent.

### Comportement

- Exit 0 : toutes les vérifications passent. Merge autorisé.
- Exit 1 : au moins une vérification échoue. Merge bloqué.
- Logs détaillés pour debug.

### Local vs CI

Le script est **idempotent** entre local et CI : un contributeur peut exécuter `bash scripts/vbb-ci-local.sh` localement avant de push, et obtenir le même résultat qu'en CI. Pas de surprise en CI.

## Conséquences

### Positives
- La discipline multi-service est **enforceable** en CI.
- Les contributeurs ont un feedback rapide (local = CI).
- Les ADR-0009/0012/0020 sont consommés dans le pipeline.

### Négatives / coûts
- Le script est obligatoire pour adopter la discipline multi-service (sinon PR bloqué en CI).
- Si un outil casse (bug dans `vbb-multiservice-lint`), tout le pipeline casse. Outillage mature requis.

### Neutres
- Le script est **dans le repo** (`scripts/vbb-ci-local.sh`), donc versionnable.
- Chaque projet peut adapter le snippet CI à sa plateforme.

## Alternatives rejetées (≥ 2)

### Alternative A — Hook pre-commit (local uniquement)
- **Description** : un hook pre-commit qui exécute les vérifications avant commit.
- **Pourquoi rejetée** : local uniquement, ne couvre pas le push direct via UI GitHub. CI est plus robuste.

### Alternative B — Pas de gate, faire confiance aux reviewers
- **Description** : statu quo, discipline humaine uniquement.
- **Pourquoi rejetée** : ne survit pas au passage à l'échelle. Les régressions passent.

### Alternative C — Un outil unique « vbb-ci » qui orchestre
- **Description** : un binaire `vbb-ci` qui encapsule toute la logique.
- **Pourquoi rejetée** : ajoute une dépendance externe. Un script bash est portable et auditable.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Le script casse sur un environnement exotique (Windows sans bash) | moyenne | faible | Snippet CI pour Linux/Mac uniquement ; Windows = WSL ou Docker |
| Les outils évoluent et le script doit être mis à jour | forte | faible | Le script référence les outils par nom ; mise à jour triviale |
| Les contributeurs contournent le gate (push --force) | faible | moyen | Branch protection rules dans GitHub/GitLab protègent |

## Hypothèses

- Bash est disponible dans tous les environnements CI modernes (Linux, macOS).
- Python 3.10+ est disponible (cohérent avec les autres outils vbb).
- Les 3 outils (`vbb-multiservice-lint`, `vbb-multiservice-graph`, `vbb-architecture`) sont implémentés (Run 13+).

## Références

- ADR amont : [`0009-multiservice-lint-discipline.md`](0009-multiservice-lint-discipline.md) (linter)
- ADR amont : [`0020-multiservice-graph.md`](0020-multiservice-graph.md) (graph avec `--check-cycle`)
- ADR amont : [`0012-codegen-agents-claudemd.md`](0012-codegen-agents-claudemd.md) (codegen avec `--check`)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-15
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: PROCESS
reversible: true
depends_on:
  - "0009-multiservice-lint-discipline.md"
  - "0020-multiservice-graph.md"
  - "0012-codegen-agents-claudemd.md"
blocks:
  - "scripts/vbb-ci-local.sh (implémentation, Run 13+)"
  - "CI enforcement (snippet copy-paste par projet)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```