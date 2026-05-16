# PROJECT_MODE.md — vibebackbone

**Version :** 1.0 | **Date :** 2026-05-16

## Identité du repo

Ce dépôt est le **catalogue de distribution du système vibebackbone**.
Il contient les skills, prompts, et fichiers de gouvernance destinés à être injectés
dans des projets cibles. Il n'est pas lui-même un projet consommateur.

## Mode

- **État :** DISTRIBUTION
- **Usage :** Source amont pour les agents Pi, Claude Code, Cursor, Codex, etc.
- **Gouvernance :** AGENTS.md (canonique), SYSTEM.md (runtime)
- **Skills :** 57 skills standards dans `skills/`
- **Prompts :** 24 prompts de pilotage dans `prompts/`

## Consignes

- Les fichiers `docs/SESSION.md` et `docs/AUDIT_STATUS.md` sont locaux (gitignorés).
- `docs/PROJECT_MODE.md` est versionné — il décrit la nature du repo.
- Ne pas modifier les SKILL.md sans passer par la phase d'audit appropriée.
- Le README.md sert de point d'entrée marketing et d'installation.
