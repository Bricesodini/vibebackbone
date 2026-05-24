# 01_INTAKE — RUN 04B · Lot 1C : Auto-audit dette technique

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `1-vbb-tech-debt`

## Objectif

Exécuter un audit de dette technique du repo vibebackbone avec son propre skill `1-vbb-tech-debt`. Identifier dette réelle, distinguer bloquante/acceptable/cosmétique. Ne corriger aucun code.

## Règle absolue

Audit = **lecture seule**. Seuls modifiables : artefacts d'audit, AUDIT_STATUS.md, CONTEXT.md, run docs.

## Scope d'analyse

- tools/** — duplication, complexité, portabilité
- scripts/** — portabilité, conventions
- setup.sh — longueur, complexité, duplication
- .github/workflows/** — cohérence
- tests/** — couverture, qualité
- skills/**/CONTRACT.yaml — dette contractuelle
- docs/CONTEXT.md, AUDIT_STATUS.md — cohérence
- README.md, GUIDE.md — dette documentaire

## Risques

| ID | Risque | Mitigation |
|----|--------|------------|
| R-04B-01 | Modification accidentelle | Lecture seule stricte |
| R-04B-02 | Conflit avec findings sécurité | Scope séparé — dette structurelle, pas sécurité |