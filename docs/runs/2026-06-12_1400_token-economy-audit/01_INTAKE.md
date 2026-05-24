# 01_INTAKE — RUN 13 : Token Economy Audit

**Date** : 2026-06-12  
**Voie** : AUDIT  
**Phase** : 01_INTAKE

---

## Objectif

Auditer tous les fichiers chargés ou susceptibles d'être chargés par les agents afin de réduire le coût contextuel sans perdre l'efficacité opérationnelle.

## Scope lecture

- AGENTS.md, SYSTEM.md, CLAUDE.md, GUIDE.md, PILOTAGE.md
- docs/CONTEXT.md, AUDIT_STATUS.md, ACTIVITY_LOG.md
- prompts/**, skills/**/SKILL.md, skills/**/CONTRACT.yaml
- docs/runs/README.md

## Interdictions

- Audit uniquement — ne pas réécrire les fichiers dans ce run
- Ne pas modifier le code source

## Classification cible

| Couche | Rôle | Chargé quand |
|--------|------|---------------|
| L0 | Boot context | Chaque session |
| L1 | Router context | Pour choisir voie/phase/skill |
| L2 | Contract context | Pour vérifier/exécuter un skill |
| L3 | Full skill/reference | Seulement si nécessaire |
| L4 | Archive/history | Jamais par défaut |

## Résultat attendu

- Rapport `docs/audits/token-economy-20260612.md`
- Plan de réduction pour RUN 14