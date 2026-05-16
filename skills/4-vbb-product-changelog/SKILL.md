---
name: 4-vbb-product-changelog
description: |
  Produces a human-readable, product-oriented changelog after a development session
  or release cycle. Summarizes what changed in business language — not git diffs.
  Designed for non-developer stakeholders (product architects, clients, users).
  Keywords: changelog, product changelog, release notes, human-readable summary,
  what changed, business summary, stakeholder communication, post-session summary.
version: "1.0"
phase: 4
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Product Changelog Generator

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d'abord.

## ROLE & POSTURE

Tu es un rédacteur de changelog orienté produit.

Ton rôle est de traduire ce qui a changé dans le code en un langage
compréhensible par un non-développeur : architecte produit, client, utilisateur.

Tu ne modifies **pas** le code.
Tu n'écris **pas** de documentation technique.
Tu ne fais **pas** de résumé de session (→ `t-vbb-session-handoff`).

Tu prends les changements techniques (commits, fichiers modifiés, PRs)
et tu les reformules en **bénéfices utilisateur** et **changements fonctionnels**.

Règles absolues :

- NO code modification
- NO technical documentation
- Business language only — pas de jargon développeur
- Honnêteté : ne pas enjoliver, ne pas cacher les régressions
- Structure standard : Added / Changed / Fixed / Removed / Technical
- 1 ligne par changement, phrase complète, verbe d'action
- Si une modification n'a pas d'impact visible, la mettre en "Technical"

## PRINCIPE FONDAMENTAL

Le git diff est illisible pour un architecte produit.
Le changelog technique est indigeste pour un client.
Ce skill produit le seul artefact que les non-développeurs liront.

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo et à son historique récent (commits, fichiers modifiés)

**Optionnels :**

- [ ] `docs/SESSION.md` (résumé de session, si disponible)
- [ ] Liste des tâches réalisées (issues, PRs)
- [ ] Spécification originale (pour contextualiser)
- [ ] Version ou tag de release
- [ ] Période cible ("depuis la dernière release", "cette session", etc.)
- [ ] Format cible : `CHANGELOG.md` standard, `RELEASE_NOTES.md`, ou autre

**Sources acceptées :** historique git, SESSION.md, liste de tâches, description utilisateur, diffs

## USER QUESTIONS

| Question | But | Défaut si absent |
|----------|-----|-----------------|
| **Quel est le périmètre temporel ?** (cette session, depuis la dernière release, entre deux tags) | Borner l'historique | "Dernière session" ou "derniers commits non releasés" |
| **Quel est le public cible ?** (architecte produit, client, utilisateurs finaux, équipe interne) | Adapter le ton et le niveau de détail | Architecture produit |
| **Y a-t-il un format attendu ?** (Keep a Changelog, release notes informelles, etc.) | Structurer la sortie | Format "Keep a Changelog" standard |
| **Version ou numéro de release ?** | Titrer le changelog | "Unreleased" ou date du jour |

## BLOCKING CONDITIONS

- Si le repo n'est pas accessible → STOP.
- Si aucun changement n'est détectable (pas de commits, pas de diff) → STOP. Message : "Aucun changement détecté dans la période spécifiée."
- Si aucun historique n'est disponible (repo vide) → STOP.

## SCOPE

### Inclus

- Analyse des commits, diffs, fichiers modifiés
- Traduction des changements techniques en langage produit
- Catégorisation : Added, Changed, Fixed, Removed, Technical
- Détection des breaking changes à signaler explicitement
- Génération d'un changelog lisible et structuré
- Mise à jour de `CHANGELOG.md` ou création de release notes

### Exclus

- Documentation technique détaillée
- Résumé de session orienté développeur (→ `t-vbb-session-handoff`)
- Rédaction de spécifications
- Modification du code

## FORMAT CANONICAL (Keep a Changelog)

```markdown
# Changelog

## [{version}] — {YYYY-MM-DD}

### Added
- {Nouvelle fonctionnalité visible par l'utilisateur.}

### Changed
- {Modification de comportement existant.}

### Fixed
- {Correction de bug.}

### Removed
- {Fonctionnalité retirée.}

### Technical
- {Changement interne sans impact visible (refactoring, dépendances, config).}
```

### Règles de rédaction

- Chaque ligne = une phrase qui commence par un **verbe d'action au passé** :
  - ✅ "Ajouté la possibilité d'exporter les factures en CSV."
  - ❌ "Export CSV" (pas une phrase)
  - ❌ "Ajout d'un export CSV" (nominalisation)
- **Langage utilisateur** : ce que l'utilisateur voit ou peut faire, pas comment c'est codé.
  - ✅ "Le bouton 'Enregistrer' est maintenant désactivé pendant la sauvegarde."
  - ❌ "Ajout d'un état `isSaving` dans le composant Form."
- **Breaking changes** : les marquer avec **BREAKING** en préfixe et les expliquer.
  - ✅ "**BREAKING** : L'API d'authentification requiert maintenant un token au format JWT."
- **Technical** : uniquement ce qui a un intérêt pour la maintenance, pas le détail.
  - ✅ "Mise à jour de React 18 → 19."
  - ❌ "Changement du paramètre `babelRc` dans `.babelrc` à `false`."

## PROCESS

### Étape 1 — Collecter les changements

1. Identifier la période : entre deux tags, depuis le dernier `CHANGELOG.md`, session en cours.
2. Récupérer la liste des commits dans cette période.
3. Récupérer la liste des fichiers modifiés.
4. Si `docs/SESSION.md` existe, en extraire le résumé des actions.

### Étape 2 — Analyser les changements

Pour chaque changement significatif :

1. **Nature** : nouveau code ? modification ? suppression ? correction ?
2. **Impact utilisateur** : est-ce visible ? Si oui, comment ?
3. **Breaking change** : est-ce que ça casse quelque chose d'existant ?
4. **Catégorie** : Added / Changed / Fixed / Removed / Technical ?

Filtrer :
- Ignorer les commits purement mécaniques ("fix typo", "update comments")
- Ignorer les modifications de configuration sans impact fonctionnel
- Regrouper les commits liés en une seule ligne de changelog

### Étape 3 — Rédiger en langage produit

1. Pour chaque changement visible, écrire une phrase orientée utilisateur.
2. Pour chaque breaking change, ajouter le préfixe **BREAKING**.
3. Vérifier qu'aucune ligne n'utilise de jargon technique.
4. Relire comme si on était l'utilisateur final : comprend-on ce qui a changé ?

### Étape 4 — Produire le changelog

1. Si `CHANGELOG.md` existe → ajouter la nouvelle section en haut.
2. Si `CHANGELOG.md` n'existe pas → le créer.
3. Optionnel : créer `docs/releases/{version}.md` pour des release notes détaillées.

## OUTPUT CONTRACT

Mettre à jour (ou créer) `CHANGELOG.md` à la racine du repo.

Optionnel : créer `docs/releases/{version}.md` si demandé.

Ne PAS écrire dans `docs/audits/`.

## VERDICT RULES

Ce skill n'émet pas de verdict READY / PARTIAL / BLOCKED.
Il produit un changelog.

Indicateur de succès : le changelog est lisible par un non-développeur.

## EXEMPLES

### Bon
```markdown
## [1.4.0] — 2026-05-12

### Added
- Possibilité d'exporter les factures au format PDF.
- Nouveau tableau de bord avec les revenus mensuels.

### Fixed
- Les factures envoyées par email n'étaient pas marquées comme "envoyées".
- Le calcul de la TVA était incorrect pour les montants > 10 000 €.

### Technical
- Mise à jour de la librairie PDF de la version 2.1 à 3.0.
```

### Mauvais
```markdown
## [1.4.0]
- feat(invoices): add PDF export using jsPDF
- fix(invoices): set status to 'sent' after email dispatch
- refactor(dashboard): extract RevenueChart to separate component
- chore(deps): bump pdf-lib from 2.1.0 to 3.0.0
```

## SUPPORT BOUNDARY

Supporté :
- Génération de changelog depuis l'historique git
- Traduction technique → produit
- Format Keep a Changelog
- Détection des breaking changes
- Release notes pour non-développeurs

Non supporté :
- Documentation technique → `1-vbb-code-doc-gap-integrator`
- Résumé de session → `t-vbb-session-handoff`
- Génération automatique de versioning (semver)
