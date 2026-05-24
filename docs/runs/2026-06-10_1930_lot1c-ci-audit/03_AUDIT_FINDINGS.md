# 03_AUDIT_FINDINGS — RUN 04C · Lot 1C : Audit CI

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `2-vbb-ci`

---

## CI-001 — Workflows sans permissions block (réédition SEC-009)

| Champ | Valeur |
|-------|--------|
| **ID** | CI-001 |
| **Sévérité** | P2 |
| **Zone** | .github/workflows/ |
| **Fichier** | `.github/workflows/vbb-contracts.yml`, `.github/workflows/smoke.yml` |
| **Constat** | Aucun workflow ne déclare de `permissions` block. Par défaut, `GITHUB_TOKEN` a `contents: write`, `packages: write`, etc. Pour un workflow qui ne fait que lire et tester, seul `contents: read` est nécessaire. |
| **Impact** | Workflow compromis peut pousser du code ou modifier des releases |
| **Preuve** | Aucun `permissions:` dans les 2 workflows |
| **Recommandation** | Ajouter `permissions: contents: read` au niveau workflow |
| **Statut** | OPEN |

---

## CI-002 — PyYAML non épinglé dans le workflow (réédition SEC-005)

| Champ | Valeur |
|-------|--------|
| **ID** | CI-002 |
| **Sévérité** | P2 |
| **Zone** | .github/workflows/vbb-contracts.yml |
| **Fichier** | `.github/workflows/vbb-contracts.yml` ligne `pip install pyyaml` |
| **Constat** | La dépendance PyYAML est installée sans version épinglée. `pip install pyyaml` installe la dernière version disponible, qui peut changer entre deux runs, cassant la reproductibilité. |
| **Impact** | Build non déterministe. Risque supply chain. Un run peut réussir aujourd'hui et échouer demain si PyYAML 7.0 sort avec des breaking changes. |
| **Preuve** | `run: pip install pyyaml` — pas de version. `requirements.txt: pyyaml` — pas de version non plus. |
| **Recommandation** | `pip install pyyaml>=6.0,<7.0` ou `pip install -r requirements.txt` avec `pyyaml>=6.0,<7.0` |
| **Statut** | OPEN |

---

## CI-003 — Pas de cache pip

| Champ | Valeur |
|-------|--------|
| **ID** | CI-003 |
| **Sévérité** | P3 |
| **Zone** | .github/workflows/vbb-contracts.yml |
| **Fichier** | `.github/workflows/vbb-contracts.yml` |
| **Constat** | Aucun cache n'est configuré pour les dépendances pip. PyYAML est réinstallé à chaque run (~5-10s). |
| **Impact** | Gaspillage de temps CI mineur. Coût marginale. |
| **Preuve** | Pas de `actions/cache` ni `cache-dependency-path` |
| **Recommandation** | Ajouter cache pip : `cache: 'pip'` dans `actions/setup-python@v5` (support natif) |
| **Statut** | OPEN |

---

## CI-004 — Incohérence CI locale vs GitHub Actions

| Champ | Valeur |
|-------|--------|
| **ID** | CI-004 |
| **Sévérité** | P2 |
| **Zone** | scripts/ vs .github/workflows/ |
| **Fichier** | `scripts/vbb-ci-local.sh` vs `.github/workflows/` |
| **Constat** | 3 divergences entre CI locale et GitHub : (1) loop closure check présent en local, absent de GitHub ; (2) smoke-install.sh présent sur GitHub, absent en local ; (3) le script local a un mode WARN pour le closure check, mais GitHub n'a pas d'équivalent. Un développeur peut avoir un PASS local mais un FAIL sur GitHub ou inversement. |
| **Impact** | Faux sentiment de confiance. Tests locaux ≠ CI remote. |
| **Preuve** | Local : 6 checks. GitHub vbb-contracts : 5 checks. Smoke workflow : 1 check distinct. |
| **Recommandation** | 1. Fusionner vbb-contracts.yml et smoke.yml en un seul workflow. 2. Ajouter le closure check en GitHub (sur un run complété connu). 3. Ajouter smoke-install.sh en local. |
| **Statut** | OPEN |

---

## CI-005 — Pas de filtre de branche sur les triggers

| Champ | Valeur |
|-------|--------|
| **ID** | CI-005 |
| **Sévérité** | P3 |
| **Zone** | .github/workflows/ |
| **Fichier** | Les 2 workflows |
| **Constat** | Les workflows se déclenchent sur tout push et toute PR, sans filtre de branche. Des pushes sur des branches de dev ou temporaires déclenchent la CI inutilement. |
| **Impact** | Gasillage de minutes CI. Bruit dans les résultats. |
| **Preuve** | `on: push:` sans `branches:` filter |
| **Recommandation** | Ajouter `branches: [main]` et éventuellement `branches-ignore: [deps/**]` |
| **Statut** | OPEN |

---

## CI-006 — smoke.yml : macOS seulement, pas de matrice Python

| Champ | Valeur |
|-------|--------|
| **ID** | CI-006 |
| **Sévérité** | P2 |
| **Zone** | .github/workflows/smoke.yml |
| **Fichier** | `.github/workflows/smoke.yml` |
| **Constat** | Le workflow smoke ne tourne que sur macos-latest, sans matrice Python. setup.sh est critique et tourne sur tous les OS — il devrait être testé sur les deux OS et plusieurs versions de Python. |
| **Impact** | Régression macOS→Linux non détectée. setup.sh écrit dans $HOME différemment selon l'OS. |
| **Preuve** | `runs-on: macos-latest` — pas de matrix |
| **Recommandation** | Étendre la matrice à `[ubuntu-latest, macos-latest]` × Python `[3.11, 3.12]` |
| **Statut** | OPEN |

---

## CI-007 — Matrice Python limitée à 3.11

| Champ | Valeur |
|-------|--------|
| **ID** | CI-007 |
| **Sévérité** | P3 |
| **Zone** | .github/workflows/vbb-contracts.yml |
| **Fichier** | `.github/workflows/vbb-contracts.yml` |
| **Constat** | Python 3.11 uniquement. Pas de test sur 3.10 (min) ni 3.12 (current). |
| **Impact** | Régression sur d'autres versions Python non détectée par CI. |
| **Preuve** | `python-version: ["3.11"]` |
| **Recommandation** | Étendre à `["3.10", "3.11", "3.12"]` si le coût est acceptable, sinon `["3.11", "3.12"]` |
| **Statut** | OPEN |

---

## CI-008 — Pas de test pour contract lint ni phase router (croisement TD-006/TD-010)

| Champ | Valeur |
|-------|--------|
| **ID** | CI-008 |
| **Sévérité** | P2 |
| **Zone** | tests/ + .github/workflows/ |
| **Fichier** | N/A (fichiers manquants) |
| **Constat** | La CI exécute le lint et le runtime, mais aucune suite de tests ne valide leurs comportements en conditions négatives. Si le linter ou le runtime casse, la CI ne détectera que le crash, pas les faux PASS. |
| **Impact** | Faux PASS possibles. Le lint peut passer avec 0 erreurs mais manquer des validations. |
| **Preuve** | `find tests -name "*lint*" -o -name "*router*"` → 0 résultats |
| **Recommandation** | Créer `tests/test_contract_lint.py` et `tests/test_phase_router.py` (cf. TD-006, TD-010) |
| **Statut** | OPEN |

---

## Résumé des findings

| ID | Sévérité | Statut | Résumé |
|----|----------|--------|--------|
| CI-001 | P2 | OPEN | Pas de permissions block (SEC-009 réédité) |
| CI-002 | P2 | OPEN | PyYAML non épinglé (SEC-005 réédité) |
| CI-003 | P3 | OPEN | Pas de cache pip |
| CI-004 | P2 | OPEN | Incohérence CI locale vs GitHub |
| CI-005 | P3 | OPEN | Pas de filtre de branche |
| CI-006 | P2 | OPEN | smoke.yml macOS only |
| CI-007 | P3 | OPEN | Matrice Python limitée |
| CI-008 | P2 | OPEN | Pas de tests négatifs pour lint/router |

**Distribution** :
- P0 : 0
- P1 : 0
- P2 : 5 (CI-001, CI-002, CI-004, CI-006, CI-008)
- P3 : 3 (CI-003, CI-005, CI-007)

**Croisement sécurité** : CI-001 et CI-002 sont des rééditions des findings SEC-009 et SEC-005 de l'audit sécurité — confirmés ici avec un focus CI.