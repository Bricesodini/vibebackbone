# 02_DISCOVERY — RUN 04B · Lot 1C : Zone d'analyse dette technique

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `1-vbb-tech-debt`

---

## Repository inventory

| Dimension | Valeur |
|-----------|--------|
| Skills | 58 (5+16+12+1+10+13+1) |
| Prompts | 32 (7+25) |
| Contracts | 22/58 (38 %) |
| Scripts | setup.sh (652 lignes), 2 scripts scripts/ |
| Outils Python | 4 scripts (1521 lignes total) |
| Tests | 3 suites Python (28 tests), 2 smoke bash |
| Workflows CI | 2 (smoke.yml, vbb-contracts.yml) |
| Docs root .md | 13 fichiers (7 governance, 5 artefacts migration, 1 CHANGELOG) |

---

## Canonical vs legacy mapping

| Catégorie | Canonique | Legacy/Résidu |
|----------|-----------|--------------|
| Installation | `setup.sh` | Aucun héritage — canonical |
| Contrats | `skills/*/CONTRACT.yaml` + `INDEX.yaml` | 36 skills sans contrat |
| Gouvernance | `AGENTS.md`, `SYSTEM.md`, `docs/CONTEXT.md` | 5 fichiers .md migration racine |
| CI | `.github/workflows/` | `smoke.yml` limité |
| Tests | `tests/test_*.py` | Aucun test pour lint, router |
| Templates | `docs/templates/` | Aucun — canonical |

---

## Zones identifiées pour audit

1. **setup.sh** : 652 lignes, 8 blocs Python embarqués, logique install/uninstall dupliquée
2. **Contrats** : 36/58 skills sans contrat (62%)
3. **Fichiers legacy racine** : 5 artefacts de migration non archivés
4. **Phase/naming inconsistencies** : 4 skills avec préfixe ≠ phase frontmatter
5. **Couverture tests** : Pas de test pour lint ni router
6. **Fichiers .bak** : 1 fichier backup non nettoyé
7. **Version skill outlier** : 1 skill en v0.1 (status-report)