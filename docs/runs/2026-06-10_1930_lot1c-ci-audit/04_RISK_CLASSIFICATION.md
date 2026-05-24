# 04_RISK_CLASSIFICATION — RUN 04C · Lot 1C : Classification risques CI

**Date** : 2026-06-10  
**Voie** : AUDIT

---

## Priorisation

### Haute (bloquant avant v1.0)

| ID | Action | Effort |
|----|--------|--------|
| CI-001 | Ajouter `permissions: contents: read` aux 2 workflows | 2 lignes |
| CI-002 | Épingler PyYAML dans workflows et requirements.txt | 2 lignes |
| CI-004 | Fusionner workflows + aligner local/GitHub | Moyen |
| CI-006 | smoke.yml matrice OS | 5 lignes |
| CI-008 | Créer tests négatifs lint/router (cf. TD-006/TD-010) | Moyen |

### Basse (cosmétique / optimisation)

| ID | Action | Effort |
|----|--------|--------|
| CI-003 | Ajouter cache pip | 1 ligne |
| CI-005 | Ajouter filtre de branche | 3 lignes |
| CI-007 | Étendre matrice Python | 1 ligne |

---

## Workflow cible proposé (texte)

```yaml
name: vbb-ci
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  checks:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements.txt
      - run: python3 tools/vbb-contract-lint.py
      - run: python3 tools/vbb-contract-runtime.py run --all --dry-run
      - run: python3 tests/test_loop_closure.py
      - run: python3 tests/test_portability.py
      - run: python3 tests/test_project_init.py
      - run: python3 tests/test_contract_lint.py    # À créer
      - run: python3 tests/test_phase_router.py     # À créer
      - run: bash tests/smoke-install.sh
```

---

## Verdict prévu

**PARTIAL** — CI existante et fonctionnelle mais invariants importants manquants (permissions, version pinning, cohérence local/remote, couverture tests).