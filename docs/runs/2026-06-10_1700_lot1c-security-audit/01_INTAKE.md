# 01_INTAKE — RUN 04A · Lot 1C : Auto-audit sécurité

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `2-vbb-security`

## Objectif

Exécuter un audit sécurité réel du repo vibebackbone avec son propre skill `2-vbb-security`. Produire un rapport classifié, mettre à jour AUDIT_STATUS.md. **Ne corriger aucun code.**

## Règle absolue

Audit = **lecture seule**. Aucune modification de :
- setup.sh
- scripts/**
- tools/**
- .github/**
- skills/**
- prompts/**
- code source quelconque

Seules exceptions :
- artefacts d'audit dans `docs/audits/`
- `docs/AUDIT_STATUS.md`
- `docs/CONTEXT.md`
- `docs/runs/2026-06-10_1700_lot1c-security-audit/`

## Scope d'analyse

Priorité haute :
- `setup.sh`
- `scripts/install-vbb-pre-commit.sh`
- `scripts/vbb-ci-local.sh`
- `tools/vbb-*.py`
- `.github/workflows/vbb-contracts.yml`
- `.github/workflows/smoke.yml`
- `requirements.txt`
- `tests/smoke-*.sh`

Focus sécurité :
- Exécution shell dangereuse (eval, exec, $() non quoté)
- Permissions excessives (chmod 777, sudo)
- Symlinks vers cibles incontrôlées
- Écriture dans `$HOME` sans validation
- Injection de commandes
- Chemins non quotés
- Dépendances Python (supply chain)
- Secrets exposés dans le repo
- Fichiers modifiés hors repo (side effects)
- Risques hooks git
- Risques agents LLM (prompt injection, exfiltration contexte)

## Critères de succès

- [ ] Audit produit et classifié
- [ ] Findings avec ID, sévérité, zone, constat, preuve, recommandation
- [ ] AUDIT_STATUS.md mis à jour
- [ ] Aucun code modifié
- [ ] Prochaines actions proposées

## Risques

| ID | Risque | Mitigation |
|----|--------|------------|
| R-04A-01 | Modification accidentelle de code | Mode lecture seule strict, pas de write sur les fichiers analysés |
| R-04A-02 | Faux positifs | Classer FALSE_POSITIVE si applicable |
| R-04A-03 | Couverture incomplète | Classer zones non analysées comme UNKNOWN |