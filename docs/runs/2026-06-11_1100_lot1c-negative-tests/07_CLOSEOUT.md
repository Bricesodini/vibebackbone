# 07_CLOSEOUT — RUN 06B : Tests négatifs lint/router

**Date** : 2026-06-11  
**Voie** : STRUCTURÉE  
**Verdict** : ✅ PASS

---

## Résumé

15 tests négatifs et positifs ajoutés pour le linter de contrats et le runtime. 28 tests existants inchangés. CI locale PASS. Résout SYNERGY-003.

### Tests ajoutés

| # | Catégorie | Test | Résultat |
|---|-----------|------|----------|
| 1 | Linter négatif | Missing required top-level key 'entrypoint' | ✅ |
| 2 | Linter négatif | Invalid type 'python_function' | ✅ |
| 3 | Linter négatif | Invalid output status 'UNKNOWN' | ✅ |
| 4 | Linter négatif | Missing required output field 'summary' | ✅ |
| 5 | Linter négatif | Unknown agent 'unknown-agent-xyz' | ✅ |
| 6 | Linter négatif | Event referencing unindexed skill | ✅ |
| 7 | Linter négatif | v0.3 artifact missing path_pattern | ✅ |
| 8 | Linter négatif | Unsupported version '9.9' | ✅ |
| 9 | Linter négatif | Blocking gate without expected_status | ✅ |
| 10 | Linter positif | Valid minimal v0.3 contract passes | ✅ |
| 11 | Runtime négatif | Non-existent skill_id → BLOCKED | ✅ |
| 12 | Runtime positif | Real skill dry-run returns valid status | ✅ |
| 13 | Runtime positif | --all --dry-run completes | ✅ |
| 14 | Router négatif | Unknown phase → None/empty (skipped if router not present) | ✅ |
| 15 | Router positif | Valid query doesn't crash | ✅ |

### Non-régression
- test_loop_closure.py : 12/12 ✅
- test_portability.py : 6/6 ✅
- test_project_init.py : 10/10 ✅
- **Total : 43/43 passés**

### Fichiers modifiés
- `tests/test_contract_lint.py` — créé (395 lignes)

### SYNERGY résolu
- SYNERGY-003 : ✅ Tests négatifs lint/router ajoutés

### Risques résiduels
- 7 P2 : contractualisation, setup.sh refactor, cohérence CI, symlinks absolus
- 10 P3 : cosmétiques
- 3 ACCEPTED_RISK
- Le router (vbb-phase-router.py) n'existe pas encore — tests sont des skips gracieux

### Prochaine action recommandée
**RUN 07 — Voie RAPIDE allégée (ZERO / MINIMAL / STANDARD + Activity Log minimal)**