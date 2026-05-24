# 02_DISCOVERY — RUN 05 : Résultats bruts des 3 audits

**Date** : 2026-06-10  
**Voie** : AUDIT → CLÔTURE

---

## Audit 04A — Sécurité (2-vbb-security)

| ID | Sév | Statut | Résumé |
|----|-----|--------|--------|
| SEC-001 | P2 | OPEN | os.popen() pour horodatage backup |
| SEC-002 | P3 | OPEN | eval() pour variable dynamique |
| SEC-003 | P2 | OPEN | Symlinks absolus → dangling si repo déplacé |
| SEC-004 | P3 | OPEN | TOCTOU race condition sur symlinks |
| SEC-005 | P2 | OPEN | PyYAML non épinglé (supply chain) |
| SEC-006 | P3 | ACCEPTED_RISK | exec_module pour phase-router |
| SEC-007 | P2 | OPEN | setup.sh écrit dans $HOME sans sandbox |
| SEC-008 | P2 | ACCEPTED_RISK | Pas de vérification d'intégrité des skills |
| SEC-009 | P2 | OPEN | GitHub Actions sans permissions minimales |
| SEC-010 | N/A | FALSE_POSITIVE | Pas de secret exposé (confirmation) |

## Audit 04B — Dette technique (1-vbb-tech-debt)

| ID | Sév | Statut | Résumé |
|----|-----|--------|--------|
| TD-001 | P2 | OPEN | setup.sh monolithe 652 lignes, 8 blocs Python |
| TD-002 | P2 | OPEN | Duplication install/uninstall dans setup.sh |
| TD-003 | P2 | OPEN | 36/58 skills sans CONTRACT.yaml (62 %) |
| TD-004 | P3 | OPEN | 5 artefacts migration en racine |
| TD-005 | P3 | OPEN | 4 skills phase/préfixe incohérents |
| TD-006 | P2 | OPEN | Pas de test pour contract linter |
| TD-007 | P3 | OPEN | 1 fichier .bak non nettoyé |
| TD-008 | P3 | ACCEPTED_RISK | deploy.sh template 1303 lignes |
| TD-009 | P3 | OPEN | 1 skill en version 0.1 |
| TD-010 | P3 | OPEN | Pas de test pour phase router |

## Audit 04C — CI (2-vbb-ci)

| ID | Sév | Statut | Résumé |
|----|-----|--------|--------|
| CI-001 | P2 | OPEN | Workflows sans permissions block |
| CI-002 | P2 | OPEN | PyYAML non épinglé dans workflows |
| CI-003 | P3 | OPEN | Pas de cache pip |
| CI-004 | P2 | OPEN | Incohérence CI locale vs GitHub |
| CI-005 | P3 | OPEN | Pas de filtre de branche |
| CI-006 | P2 | OPEN | smoke.yml macOS only |
| CI-007 | P3 | OPEN | Matrice Python limitée |
| CI-008 | P2 | OPEN | Pas de tests négatifs pour lint/router |

---

## Total brut : 27 findings

- Sécurité : 9 (5 P2 + 3 P3 + 1 FALSE_POSITIVE)
- Dette technique : 10 (4 P2 + 6 P3)
- CI : 8 (5 P2 + 3 P3)

---

## Doublons identifiés

| Doublon | Sources | Constat commun |
|---------|---------|----------------|
| CI-001 = SEC-009 | Sécurité + CI | Workflows sans permissions |
| CI-002 = SEC-005 | Sécurité + CI | PyYAML non épinglé |
| CI-008 = TD-006 + TD-010 | Dette technique + CI | Pas de tests pour lint + router |
| TD-001 ∩ SEC-007 | Dette + Sécurité | setup.sh concentration de risques |
| TD-002 ∩ SEC-007 | Dette + Sécurité | setup.sh duplication install/uninstall → $HOME |

5 doublons → réduction de 27 → ~22 findings uniques.