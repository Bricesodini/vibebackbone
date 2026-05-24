# 04_PLAN — RUN 03 · Lot 1B : Plan CI

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

---

## 1. Workflow GitHub Actions cible

Créer `.github/workflows/vbb-contracts.yml` :

```yaml
name: vbb-contracts
on:
  push:
  pull_request:

jobs:
  contracts:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ["3.11"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install pyyaml
      - run: python3 tools/vbb-contract-lint.py
      - run: python3 tools/vbb-contract-runtime.py run --all --dry-run
      - run: python3 tests/test_loop_closure.py
      - run: python3 tests/test_portability.py
      - run: python3 tests/test_project_init.py
```

Note : `vbb-loop-closure-check.py` n'est pas lancé directement en CI car il requiert un `run_id` et vérifie des artefacts de session. Les tests `test_loop_closure.py` le couvrent déjà via des tests unitaires avec des données de test isolées.

---

## 2. Script CI local cible

Créer `scripts/vbb-ci-local.sh` :

- `set -euo pipefail`
- Détection portable de `REPO_ROOT`
- Étapes :
  1. Contract lint
  2. Contract runtime dry-run
  3. Loop closure check (sur le run le plus récent)
  4. Tests Python (3 suites)
- Résumé final coloré
- Exit 0 si tous passent, exit 1 sinon
- Tolérance : loop closure PARTIAL/BLOCKED sur un run en cours = avertissement, pas bloquant

---

## 3. Fichier requirements.txt

Créer `requirements.txt` minimal :

```
pyyaml
```

---

## 4. Stratégie pour PARTIAL/BLOCKED

Le runtime dry-run peut retourner PARTIAL ou BLOCKED pour certains skills (scope-freeze PARTIAL, audit-readiness BLOCKED, etc.). C'est le comportement attendu d'un repo qui n'a pas encore auto-audité.

**Décision** : Le runtime dry-run ne doit PAS faire échouer la CI. On vérifie que :
- le lint est clean (0 erreurs)
- le runtime s'exécute sans crash
- les tests unitaires passent

On ne vérifie PAS que tous les skills retournent PASS en dry-run (irréaliste à ce stade).

---

## 5. Fichiers à créer/modifier

| Fichier | Action |
|---------|--------|
| `.github/workflows/vbb-contracts.yml` | Créer |
| `scripts/vbb-ci-local.sh` | Créer |
| `requirements.txt` | Créer |
| `docs/AUDIT_STATUS.md` | Mettre à jour (R-004 statut si applicable) |
| `docs/CONTEXT.md` | Mettre à jour contexte actif |

---

## 6. Checklist de validation

- [ ] `vbb-contracts.yml` exécute lint + runtime dry-run + 3 test suites
- [ ] Matrice OS : ubuntu-latest + macos-latest
- [ ] `vbb-ci-local.sh` exécutable et portable
- [ ] `requirements.txt` minimal
- [ ] Aucun fichier hors scope modifié