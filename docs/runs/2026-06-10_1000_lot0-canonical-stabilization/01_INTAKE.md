# 01_INTAKE — RUN 01 · Lot 0 : Stabilisation canonique du repo

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE  
**Objectif** : Établir la vérité canonique du repo avant tout nouveau chantier fonctionnel.

## 1. Objectif du run

Stabiliser les chiffres, index et labels documentaires de vibebackbone :
- Nombre réel de skills → chiffre unique partagé par tous les fichiers
- Nombre réel de prompts → chiffre unique partagé par tous les fichiers
- Cohérence entre README, AGENTS, SYSTEM, GUIDE, CONTEXT, INDEX, AUDIT_STATUS
- Classement des skills méta/orphelins
- Retrait ou reformulation des labels de maturité non prouvés

Aucune nouvelle feature. Aucun nouveau skill. Aucun nouveau contrat.

## 2. Scope

### Fichiers autorisés (modification)

- `README.md`
- `AGENTS.md`
- `SYSTEM.md`
- `GUIDE.md`
- `docs/CONTEXT.md`
- `docs/AUDIT_STATUS.md`
- `docs/SESSION.md`
- `docs/INDEX.md`
- `skills/INDEX.yaml` (si existant)
- Tout index global existant lié aux skills/prompts

### Fichiers à créer

- `docs/runs/2026-06-10_1000_lot0-canonical-stabilization/01_INTAKE.md`
- `docs/runs/2026-06-10_1000_lot0-canonical-stabilization/02_DISCOVERY.md`
- `docs/runs/2026-06-10_1000_lot0-canonical-stabilization/04_PLAN.md`
- `docs/runs/2026-06-10_1000_lot0-canonical-stabilization/05_PATCH_SUMMARY_RUN_01.md`
- `docs/runs/2026-06-10_1000_lot0-canonical-stabilization/06_REVIEW_NOTES.md`
- `docs/runs/2026-06-10_1000_lot0-canonical-stabilization/07_CLOSEOUT.md`

### Interdictions

- Ne pas ajouter de CONTRACT.yaml
- Ne pas modifier les scripts Python (sauf nécessité absolue)
- Ne pas modifier setup.sh
- Ne pas modifier les hooks
- Ne pas renommer des skills
- Ne pas supprimer des skills
- Ne pas traduire en anglais
- Ne pas créer de dashboard
- Ne pas créer de compactor
- Ne pas changer la philosophie des 4 voies

## 3. Risques

| ID | Risque | Mitigation |
|----|--------|------------|
| R-I01 | Chiffre contradictoire découvert tardivement → réouvrir le plan | Discovery exhaustive avant toute modification |
| R-I02 | Modification accidentelle d'un SKILL.md | Ne toucher que les fichiers listés en scope |
| R-I03 | Label de maturité interprété comme rétrogradation | Formuler prudemment : « partiellement vérifié » pas « instable » |
| R-I04 | Oubli d'un fichier référençant les chiffres | Recherche `grep` exhaustive avant patch |

## 4. Critères de succès

- [ ] Un seul chiffre canonique pour les skills, partagé par tous les fichiers de gouvernance
- [ ] Un seul chiffre canonique pour les prompts, partagé par tous les fichiers de gouvernance
- [ ] Aucun label de maturité non prouvé (ex: « production-ready » sur le projet global)
- [ ] Tous les skills méta/orphelins classés explicitement
- [ ] CONTEXT.md reste court et routeur
- [ ] Aucun fichier hors scope modifié
- [ ] Aucun contrat nouveau ajouté