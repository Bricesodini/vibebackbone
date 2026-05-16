# CLAUDE.md — vibebackbone

Tu operationnes sous la gouvernance **vibebackbone**.

**vibebackbone = 57 skills · 24 prompts · 4 voies (rapide, structurée, audit, clôture)**

## Fichiers de gouvernance

- `AGENTS.md` — Grammaire opérationnelle canonique (à la racine vibebackbone)
- `SYSTEM.md` — Comportement runtime Pi
- `skills/vibebackbone/docs/PILOTAGE.md` — Pilotage opérationnel v2.0

## Raccourcis (chemins relatifs au repo vibebackbone)

- Skills : `skills/` (57 dossiers, chacun contient un SKILL.md)
- Prompts : `prompts/` (24 templates)
- Catalogue complet : `skills/0-vbb-guide/SKILL.md`

## Règle fondamentale

Avant toute action, classer la tâche dans une voie :

1. **RAPIDE** — risque faible, action directe
2. **STRUCTURÉE** — plan avant modification (contrats, multi-fichiers)
3. **AUDIT** — séquence d'audit (sécurité, intégrité)
4. **CLÔTURE** — handoff de session

En cas de doute, lire `AGENTS.md` section 3 (Triage opérationnel).

## Utilisation typique

```bash
# Lister les skills disponibles
ls skills/

# Lire le guide
cat skills/0-vbb-guide/SKILL.md

# Choisir et appliquer un skill
# Ex: cat skills/2-vbb-security/SKILL.md puis suivre les étapes
```
