# 03_SYNTHESIS — RUN 05 : Registre consolidé des risques

**Date** : 2026-06-10  
**Voie** : AUDIT → CLÔTURE

---

## Registre consolidé (22 risques uniques après déduplication)

### SYNERGY-001 — Workflows GitHub Actions sans permissions

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-001 |
| **Sources** | SEC-009 + CI-001 |
| **Sévérité** | P2 |
| **Catégorie** | SECURITY / CI |
| **Statut** | OPEN |
| **Impact** | Workflow compromis peut modifier le repo |
| **Effort** | 2 lignes |
| **Quick win** | ✅ Oui |
| **Recommandation** | Ajouter `permissions: contents: read` aux 2 workflows |

### SYNERGY-002 — PyYAML non épinglé

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-002 |
| **Sources** | SEC-005 + CI-002 |
| **Sévérité** | P2 |
| **Catégorie** | SECURITY / CI |
| **Statut** | OPEN |
| **Impact** | Build non déterministe, risque supply chain |
| **Effort** | 2 lignes |
| **Quick win** | ✅ Oui |
| **Recommandation** | `pyyaml>=6.0,<7.0` dans requirements.txt + `pip install -r requirements.txt` dans workflows |

### SYNERGY-003 — Pas de tests pour lint et router

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-003 |
| **Sources** | TD-006 + TD-010 + CI-008 |
| **Sévérité** | P2 |
| **Catégorie** | TESTS |
| **Statut** | OPEN |
| **Impact** | Faux PASS possibles. Régressions non détectées par CI. |
| **Effort** | Moyen (2 fichiers de test à créer) |
| **Quick win** | Non |
| **Recommandation** | Créer `tests/test_contract_lint.py` + `tests/test_phase_router.py` |

### SYNERGY-004 — setup.sh monolithe (652 lignes, 8 blocs Python)

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-004 |
| **Sources** | TD-001 + SEC-007 |
| **Sévérité** | P2 |
| **Catégorie** | TECH_DEBT / SECURITY |
| **Statut** | OPEN |
| **Impact** | Difficile à tester, risqué à modifier, concentre les risques |
| **Effort** | Moyen |
| **Quick win** | Non |
| **Recommandation** | Extraire blocs Python en `tools/vbb-setup-*.py` |

### SYNERGY-005 — setup.sh duplication install/uninstall

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-005 |
| **Sources** | TD-002 + SEC-007 |
| **Sévérité** | P2 |
| **Catégorie** | TECH_DEBT |
| **Statut** | OPEN |
| **Impact** | Divergence install/uninstall, résidus après uninstall |
| **Effort** | Moyen |
| **Quick win** | Non |
| **Recommandation** | Centraliser les cibles dans un tableau, itérer pour install/uninstall |

### SYNERGY-006 — os.popen() pour horodatage backup

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-006 |
| **Sources** | SEC-001 |
| **Sévérité** | P2 |
| **Catégorie** | SECURITY |
| **Statut** | OPEN |
| **Impact** | RCE théorique via contrôle PATH |
| **Effort** | 1 ligne |
| **Quick win** | ✅ Oui |
| **Recommandation** | Remplacer par `datetime.now().strftime()` |

### SYNERGY-007 — Symlinks absolus → dangling si repo déplacé

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-007 |
| **Sources** | SEC-003 |
| **Sévérité** | P2 |
| **Catégorie** | SECURITY / PORTABILITY |
| **Statut** | OPEN |
| **Impact** | Skills compromis si chemin d'origine recréé |
| **Effort** | Moyen |
| **Quick win** | Non |
| **Recommandation** | Symlinks relatifs ou vérification d'intégrité au démarrage |

### SYNERGY-008 — 36/58 skills sans contrat (62 %)

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-008 |
| **Sources** | TD-003 |
| **Sévérité** | P2 |
| **Catégorie** | CONTRACTS |
| **Statut** | OPEN |
| **Impact** | Aucune vérification mécanique pour 62 % des skills |
| **Effort** | Élevé (36 contrats à créer) |
| **Quick win** | Non |
| **Recommandation** | Contractualiser Phase 1 (16) puis Phase 4 (10) par lots |

### SYNERGY-009 — Incohérence CI locale vs GitHub Actions

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-009 |
| **Sources** | CI-004 |
| **Sévérité** | P2 |
| **Catégorie** | CI |
| **Statut** | OPEN |
| **Impact** | Faux sentiment de confiance local vs remote |
| **Effort** | Moyen |
| **Quick win** | Non |
| **Recommandation** | Fusionner workflows, ajouter smoke-install en local, closure en CI |

### SYNERGY-010 — smoke.yml macOS only

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-010 |
| **Sources** | CI-006 |
| **Sévérité** | P2 |
| **Catégorie** | CI / PORTABILITY |
| **Statut** | OPEN |
| **Impact** | Régression Linux non détectée pour setup.sh |
| **Effort** | 5 lignes |
| **Quick win** | ✅ Oui |
| **Recommandation** | Ajouter matrice OS + Python |

### SYNERGY-011 — eval() pour variable dynamique

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-011 |
| **Sources** | SEC-002 |
| **Sévérité** | P3 |
| **Catégorie** | SECURITY |
| **Statut** | OPEN |
| **Impact** | Injection théorique (faible) |
| **Effort** | Faible |
| **Quick win** | Oui (refactor pattern) |
| **Recommandation** | Remplacer eval par retours stdout |

### SYNERGY-012 — TOCTOU race condition sur symlinks

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-012 |
| **Sources** | SEC-004 |
| **Sévérité** | P3 |
| **Catégorie** | SECURITY |
| **Statut** | OPEN |
| **Impact** | Symlink malveillant pendant fenêtre |
| **Effort** | 2 lignes |
| **Quick win** | ✅ Oui |
| **Recommandation** | Remplacer `rm && ln -s` par `ln -sf` |

### SYNERGY-013 — 5 artefacts migration en racine

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-013 |
| **Sources** | TD-004 |
| **Sévérité** | P3 |
| **Catégorie** | DOCS |
| **Statut** | OPEN |
| **Impact** | Bruit dans la racine |
| **Effort** | 5 mv |
| **Quick win** | ✅ Oui |
| **Recommandation** | Déplacer dans `docs/archive/` |

### SYNERGY-014 — 4 skills phase/préfixe incohérents

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-014 |
| **Sources** | TD-005 |
| **Sévérité** | P3 |
| **Catégorie** | TECH_DEBT |
| **Statut** | OPEN |
| **Impact** | Routage ambigu |
| **Effort** | 1 ligne |
| **Quick win** | ✅ Oui |
| **Recommandation** | Corriger t-vbb-status-report phase→transverse |

### SYNERGY-015 — 1 fichier .bak non nettoyé

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-015 |
| **Sources** | TD-007 |
| **Sévérité** | P3 |
| **Catégorie** | DOCS |
| **Statut** | OPEN |
| **Impact** | Pollution |
| **Effort** | 1 commande |
| **Quick win** | ✅ Oui |
| **Recommandation** | `git rm skills/vibebackbone/docs/PILOTAGE.md.bak` |

### SYNERGY-016 — 1 skill en version 0.1

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-016 |
| **Sources** | TD-009 |
| **Sévérité** | P3 |
| **Catégorie** | TECH_DEBT |
| **Statut** | OPEN |
| **Impact** | Signal de maturité incohérent |
| **Effort** | 1 ligne |
| **Quick win** | ✅ Oui |
| **Recommandation** | Bump t-vbb-status-report v0.1→1.0 |

### SYNERGY-017 — Pas de cache pip

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-017 |
| **Sources** | CI-003 |
| **Sévérité** | P3 |
| **Catégorie** | CI |
| **Statut** | OPEN |
| **Impact** | Gaspillage minutes CI |
| **Effort** | 1 ligne |
| **Quick win** | ✅ Oui |
| **Recommandation** | Ajouter `cache: pip` dans setup-python |

### SYNERGY-018 — Pas de filtre de branche

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-018 |
| **Sources** | CI-005 |
| **Sévérité** | P3 |
| **Catégorie** | CI |
| **Statut** | OPEN |
| **Impact** | Runs CI inutiles |
| **Effort** | 3 lignes |
| **Quick win** | ✅ Oui |
| **Recommandation** | Ajouter `branches: [main]` |

### SYNERGY-019 — Matrice Python limitée (3.11 only)

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-019 |
| **Sources** | CI-007 |
| **Sévérité** | P3 |
| **Catégorie** | CI |
| **Statut** | OPEN |
| **Impact** | Régression Python 3.12 non détectée |
| **Effort** | 1 ligne |
| **Quick win** | ✅ Oui |
| **Recommandation** | Étendre à `["3.11", "3.12"]` |

### SYNERGY-020 — exec_module pour phase-router

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-020 |
| **Sources** | SEC-006 |
| **Sévérité** | P3 |
| **Catégorie** | SECURITY |
| **Statut** | ACCEPTED_RISK |
| **Impact** | RCE si tools/ est compromis |
| **Effort** | N/A |
| **Quick win** | N/A |
| **Recommandation** | Accepté — mode DISTRIBUTION, pas de surface réseau |

### SYNERGY-021 — Pas de vérification d'intégrité des skills

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-021 |
| **Sources** | SEC-008 |
| **Sévérité** | P2 |
| **Catégorie** | SECURITY |
| **Statut** | ACCEPTED_RISK |
| **Impact** | Instructions compromises si skill modifié |
| **Effort** | Élevé |
| **Quick win** | Non |
| **Recommandation** | Accepté — contrôle d'accès git + revue PR |

### SYNERGY-022 — deploy.sh template 1303 lignes

| Champ | Valeur |
|-------|--------|
| **ID** | SYNERGY-022 |
| **Sources** | TD-008 |
| **Sévérité** | P3 |
| **Catégorie** | TECH_DEBT |
| **Statut** | ACCEPTED_RISK |
| **Impact** | Template distribué, pas du code VBB |
| **Effort** | N/A |
| **Quick win** | N/A |
| **Recommandation** | Accepté — template à usage client |

---

## Synthèse

| Catégorie | Count |
|----------|-------|
| SECURITY | 6 (3 P2 + 2 P3 + 1 ACCEPTED) |
| CI | 7 (2 P2 + 3 P3 + 2 croisés) |
| TECH_DEBT | 5 (1 P2 + 3 P3 + 1 ACCEPTED) |
| CONTRACTS | 1 (1 P2) |
| DOCS | 2 (2 P3) |
| TESTS | 1 (1 P2) |
| PORTABILITY | 1 (1 P2, croisé SECURITY) |

**Total** : 22 risques uniques (9 P2 + 10 P3 + 3 ACCEPTED_RISK)