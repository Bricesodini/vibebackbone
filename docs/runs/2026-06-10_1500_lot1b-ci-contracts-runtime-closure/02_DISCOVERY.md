# 02_DISCOVERY — RUN 03 · Lot 1B : Inventaire CI existante

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

---

## 1. Workflows GitHub Actions existants

| Workflow | Fichier | Contenu | Statut |
|----------|---------|---------|--------|
| `smoke` | `.github/workflows/smoke.yml` | Install test (macos-latest only) | Existent mais limité |

Le workflow `smoke.yml` ne teste que `tests/smoke-install.sh` sur macos-latest. Aucun check contrats, runtime, closure ou tests Python.

Il n'existe **pas** de `vbb-contracts.yml`.

---

## 2. Scripts CI locaux existants

| Script | Chemin | Statut |
|--------|--------|--------|
| `vbb-ci-local.sh` | `scripts/vbb-ci-local.sh` | **N'existe pas** |
| `install-vbb-pre-commit.sh` | `scripts/install-vbb-pre-commit.sh` | Existant (pré-commit hook, pas CI) |

---

## 3. Outils disponibles

| Outil | Chemin | Portabilité | Dépendances |
|-------|--------|-------------|-------------|
| `vbb-contract-lint.py` | `tools/` | ✅ Python3, PyYAML | PyYAML |
| `vbb-contract-runtime.py` | `tools/` | ✅ Python3, PyYAML | PyYAML |
| `vbb-loop-closure-check.py` | `tools/` | ✅ Python3, PyYAML | PyYAML |
| `vbb-phase-router.py` | `tools/` | ✅ Python3, PyYAML | PyYAML |
| `vbb-project-init.py` | `tools/` | ✅ Python3, PyYAML | PyYAML |

---

## 4. Tests existants

| Test | Type | Statut |
|------|------|--------|
| `tests/test_loop_closure.py` | Python3 (subprocess) | ✅ 12/12 PASS |
| `tests/test_portability.py` | Python3 (subprocess) | ✅ 6/6 PASS |
| `tests/test_project_init.py` | Python3 (subprocess) | ✅ 10/10 PASS |
| `tests/smoke-contract-runtime.sh` | Bash | ⚠️ Écrit des traces dans `docs/audits/vbb-runtime/` |
| `tests/smoke-install.sh` | Bash | ✅ Install/idempotent/uninstall |

Total : 28 tests PASS (3 Python suites), 1 bash smoke, 1 install smoke.

---

## 5. Dépendances Python

- **PyYAML** : seule dépendance externe
- **pytest** : disponible localement (8.3.4) mais tests n'utilisent pas pytest framework — ils ont leur propre runner
- **Pas de requirements.txt** : à créer ou intégrer dans le workflow

---

## 6. Compatibilité OS

| Aspect | macOS | Linux/Ubuntu | Notes |
|--------|-------|-------------|-------|
| `python3` | ✅ Disponible | ✅ Disponible | Pas de path absolu |
| PyYAML | ✅ | ⚠️ À installer | `pip install pyyaml` |
| Bash | ✅ | ✅ | |
| `mktemp -d` | ✅ | ✅ | |
| Symlinks | ✅ | ✅ | |

---

## 7. Problème R-004 : smoke-contract-runtime.sh

Le fichier `tests/smoke-contract-runtime.sh` utilise `REPO_ROOT` calculé dynamiquement — il est portable. Le problème R-004 mentionne un hardcoding dans un *autre* fichier ou une version antérieure. Le script actuel semble correct.

Il écrit des traces dans `docs/audits/vbb-runtime/` → en CI dry-run uniquement pour ce test, ou tolérer l'écriture.

---

## 8. Lacunes identifiées

| Lacune | Impact | Action |
|--------|--------|--------|
| Pas de CI contrats/runtime/closure | Aucune vérification automatisée post-push | Créer `vbb-contracts.yml` |
| Pas de script CI local | Pas de vérification rapide avant push | Créer `scripts/vbb-ci-local.sh` |
| Pas de `requirements.txt` | Installation PyYAML non documentée pour CI | Créer `requirements.txt` minimal |
| `smoke.yml` ne couvre que l'install | Les checks contrats ne sont jamais lancés par CI | Étendre ou créer workflow séparé |
| Tests Python pas lancés par CI | Seulement lancés manuellement | Intégrer dans workflow |