---
context_role: project-mode
phase: transverse
status: active
updated: 2026-05-23
---

# PROJECT_MODE — vibebackbone

## Mode

**`DISTRIBUTION`**

## Définition

vibebackbone n'est pas une application opérée en production. C'est un framework
de skills, prompts et gouvernance distribué à Pi, OpenCode, Codex et Claude Code
via `setup.sh`. Le « mode » signale l'angle d'évaluation à appliquer aux skills
qui sont `mode_sensitive`.

## Implications

| Aspect | Comportement en mode DISTRIBUTION |
|--------|------------------------------------|
| Sécurité | Pas de surface d'attaque applicative ; les audits ciblent les fichiers et le script d'installation |
| Données | Aucune donnée utilisateur traitée ; règles RGPD non applicables |
| Production | Pas de production runtime ; un « release » est un tag git + publication |
| Verdicts mode-sensitive | Cascade `verdict × env` (`PILOTAGE.md`) interprétée comme `DEV` par défaut |
| Mises à jour | Via `git pull` ; les symlinks de `setup.sh` suivent automatiquement |

## Transitions de mode

Le mode `DISTRIBUTION` n'est pas transitoire vers `PROD` au sens classique.
Une transition vers un autre mode (`SERVICE`, `LIBRARY` consommée par un autre
outil, etc.) imposerait :

1. La mise à jour explicite de ce fichier.
2. Le passage par `t-vbb-mode-transition-gate` qui produit un artefact d'audit.
3. La mise à jour de `docs/AUDIT_STATUS.md` § Mode-transition.

## Référence

Ce fichier est lu en début de session par les skills `mode_sensitive` listés
dans `skills/INDEX.yaml`. Sa modification doit suivre la voie STRUCTUREE et
produire un closeout dans `docs/runs/`.
