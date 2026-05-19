---
name: t-vbb-project-context-init
description: |
  Initializes or verifies the canonical Vibebackbone documentation scaffold for a project.
  Creates or updates the minimal docs/ frame required for shared operation across agents,
  including PROJECT_MODE, PILOTAGE, CONTEXT, SESSION, AUDIT_STATUS, and docs/audits/.
  Never changes application code. Prefer create-or-update over destructive replacement.
version: "2.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Project Context Init

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord si le fichier existe déjà.

## ROLE & POSTURE

Tu initialises le cadre documentaire canonique qui permet aux agents Vibebackbone de travailler avec les mêmes règles.

Tu ne modifies PAS le code applicatif.
Tu ne remplaces PAS destructivement des documents existants.
Tu préfères :

- create-or-update
- placeholders explicites
- compatibilité avec le cadre Vibebackbone existant

Règles absolues :

- NO application code changes
- NO destructive overwrites
- Prefer create-or-update over replace
- Keep compatibility with `docs/PILOTAGE.md`
- UNKNOWN autorisé si certaines informations projet manquent

## INPUT CONTRACT

**Requis :**

- [ ] Accès au répertoire racine du projet

**Optionnels :**

- [ ] Nom du projet
- [ ] Mode initial DEV ou PROD
- [ ] Stack principale
- [ ] Finalité / description courte du projet
- [ ] Docs existantes à conserver ou fusionner

**Sources acceptées :** repo local, docs existantes, description textuelle, README

## BLOCKING CONDITIONS

- Si le repo root n’est pas accessible → STOP. Message : "Impossible d’initialiser le cadre Vibebackbone sans accès au dépôt."
- Si des docs existantes contiennent déjà la vérité projet → ne pas les écraser ; les mettre à jour ou les préserver.
- Si mode, stack ou finalité sont inconnus → créer le scaffold avec placeholders explicites et le signaler dans la sortie.

## SCOPE

Créer ou vérifier le scaffold canonique suivant :

- `docs/CONTEXT.md`
- `docs/PROJECT_MODE.md`
- `docs/PILOTAGE.md`
- `docs/SESSION.md`
- `docs/AUDIT_STATUS.md`
- `docs/audits/`

Créer aussi si nécessaire, ou au moins proposer, selon le projet :

- `docs/ARCHITECTURE.md`
- `docs/RELATIONS.md`

### Inclus

- création du dossier `docs/`
- création du dossier `docs/audits/`
- vérification de la présence des docs canoniques
- création de placeholders explicites si les informations manquent
- compatibilité avec le pilotage Vibebackbone

### Exclus

- modification du code source
- refactor repo
- création de features
- remplissage spéculatif de la vérité projet

## PROCESS

1. Déterminer l’identité minimale du projet :
   - nom
   - mode initial
   - stack
   - finalité courte
2. Créer `docs/` si absent.
3. Créer `docs/audits/` si absent.
4. Vérifier les docs canoniques :
   - créer si absentes
   - mettre à jour si présentes mais incomplètes
5. Si `docs/PILOTAGE.md` est absent, le créer à partir du contenu canonique.
6. Si le projet a déjà une vérité documentaire, préserver et intégrer au lieu d’écraser.
7. Signaler les placeholders restant à compléter.

## OUTPUT CONTRACT

La sortie doit contenir :

- ce qui a été créé
- ce qui a été mis à jour
- ce qui a été laissé intact
- les informations projet encore manquantes
- les placeholders restant à compléter

Si des fichiers ont été créés ou proposés, la sortie doit mentionner explicitement :

- `docs/CONTEXT.md`
- `docs/PROJECT_MODE.md`
- `docs/PILOTAGE.md`
- `docs/SESSION.md`
- `docs/AUDIT_STATUS.md`
- `docs/audits/`

## VERDICT RULES

- `READY`
  - scaffold canonique présent ou correctement initialisé
- `PARTIAL`
  - scaffold présent mais plusieurs placeholders restent à compléter
- `BLOCKED`
  - initialisation impossible sans accès repo ou sans préserver une vérité existante conflictuelle
- `UNKNOWN`
  - utilisé seulement si l’état documentaire visible est trop incomplet pour conclure proprement
