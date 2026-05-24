# 01_INTAKE — RUN 02 · Lot 1A : Contractualiser les 6 skills critiques Phase 2/3

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

## Objectif

Améliorer la vérifiabilité mécanique du système en alignant les CONTRACT.yaml des 6 skills critiques Phase 2/3 avec leurs SKILL.md respectifs.

**Note** : Les 6 CONTRACT.yaml existent déjà depuis un lot précédent. Ce run consiste à les **améliorer** — pas à les créer de zéro — en corrigeant les écarts entre SKILL.md et CONTRACT.yaml.

## Scope autorisé

### Fichiers modifiables

- `skills/2-vbb-security/CONTRACT.yaml`
- `skills/2-vbb-db-robustness/CONTRACT.yaml`
- `skills/2-vbb-data-integrity/CONTRACT.yaml`
- `skills/2-vbb-systemic-risk/CONTRACT.yaml`
- `skills/2-vbb-api-auditor/CONTRACT.yaml`
- `skills/3-vbb-risk-register/CONTRACT.yaml`
- `skills/INDEX.yaml` (si nécessaire)
- `docs/AUDIT_STATUS.md`
- `docs/CONTEXT.md`
- `docs/runs/2026-06-10_1200_lot1a-critical-contracts/`

### Interdictions

- Ne pas modifier les SKILL.md (sauf correction minimale nécessaire)
- Ne pas créer de nouveaux skills
- Ne pas modifier les scripts Python
- Ne pas modifier setup.sh
- Ne pas modifier les hooks
- Ne pas traduire
- Ne pas créer de dashboard ou compactor
- Ne pas toucher aux autres skills

## Risques

| ID | Risque | Mitigation |
|----|--------|------------|
| R-II-01 | Sur-spécification des contrats (trop rigides pour le runtime) | Garder les statuts alignés sur le linter existant |
| R-II-02 | Incohérence terminologique SKILL.md ↔ CONTRACT.yaml | Aligner READY/PARTIAL/BLOCKED/NOT_APPLICABLE |
| R-II-03 | Casser le linter ou le runtime existant | Valider par `vbb-contract-lint.py` et `vbb-contract-runtime.py --dry-run` |
| R-II-04 | Ajouter des champs non supportés par le runtime | Se limiter au schéma existant |

## Critères de succès

- [ ] 6 contrats améliorés et alignés avec leurs SKILL.md
- [ ] Lint PASS sur les 6 contrats
- [ ] Runtime dry-run PASS ou PARTIAL documenté
- [ ] Aucun fichier hors scope modifié
- [ ] Statuts SKILL.md ↔ CONTRACT.yaml alignés (READY/PARTIAL/BLOCKED/NOT_APPLICABLE et PASS/FAIL)
- [ ] Entrées spécifiques reflétées dans les contrats
- [ ] Blocking conditions reflétées dans les gates
- [ ] Couverture contrats : 22 → 28 validé (les 6 existent déjà, mais maintenant alignés)