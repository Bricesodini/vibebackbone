# 02_DISCOVERY — RUN 04C · Lot 1C : Inventaire CI

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `2-vbb-ci`

---

## CI existante

### Provider : GitHub Actions

### Workflows

| Workflow | Fichier | Triggers | OS | Python | Steps |
|----------|--------|---------|-----|--------|-------|
| `vbb-contracts` | `.github/workflows/vbb-contracts.yml` | push, PR | ubuntu-latest + macos-latest | 3.11 | 5 (lint, runtime, 3 test suites) |
| `smoke` | `.github/workflows/smoke.yml` | push, PR | macos-latest only | default | 1 (install test) |

### Script local

| Script | Checks | Portabilité |
|--------|--------|-------------|
| `scripts/vbb-ci-local.sh` | 6 (lint, runtime, closure, 3 test suites) | macOS + Linux |

---

## Triggers

- push (toute branche) → déclenche les 2 workflows
- pull_request → déclenche les 2 workflows
- Pas de filtre de branche → runs inutiles sur les branches de dev

---

## Matrice

| Workflow | OS | Python |
|----------|-----|--------|
| vbb-contracts | ubuntu + macos | 3.11 seul |
| smoke | macos only | default |

Manquant : Python 3.10, 3.12 (mentionnés dans la consigne initiale mais non implémentés).

---

## Permissions

| Workflow | Block `permissions` | Niveau |
|----------|--------------------|----|
| vbb-contracts | ❌ absent | défaut GITHUB_TOKEN (write) |
| smoke | ❌ absent | défaut GITHUB_TOKEN (write) |

---

## Dépendances

| Workflow | Dépendance | Pin version |
|----------|-----------|------------|
| vbb-contracts | PyYAML via `pip install pyyaml` | ❌ Non épinglé |
| smoke | Aucune | N/A |
| Local | PyYAML (pré-requis local) | ❌ Non épinglé |

---

## Cache

Aucun cache pip configuré → réinstallation PyYAML à chaque run.

---

## Couverture des tests

| Test suite | Local | GitHub |
|-----------|-------|--------|
| test_loop_closure.py | ✅ | ✅ |
| test_portability.py | ✅ | ✅ |
| test_project_init.py | ✅ | ✅ |
| smoke-contract-runtime.sh | ❌ | ❌ |
| smoke-install.sh | ❌ | ✅ (smoke.yml) |
| test_contract_lint.py | ❌ | ❌ |
| test_phase_router.py | ❌ | ❌ |
| Loop closure check | ✅ (WARN) | ❌ |

---

## Cohérence locale vs GitHub

| Check | Local | GitHub | Cohérent |
|-------|-------|--------|----------|
| Contract lint | ✅ | ✅ | ✅ |
| Runtime dry-run | ✅ | ✅ | ✅ |
| Loop closure check | ✅ (WARN) | ❌ | ❌ |
| test_loop_closure | ✅ | ✅ | ✅ |
| test_portability | ✅ | ✅ | ✅ |
| test_project_init | ✅ | ✅ | ✅ |
| smoke-install | ❌ | ✅ | ❌ |