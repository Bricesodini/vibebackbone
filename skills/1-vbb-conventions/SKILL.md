---
name: 1-vbb-conventions
description: |
  Establishes and maintains repo-wide conventions for naming, structure, imports,
  configuration, tests, and documentation in order to reduce convention drift and
  make the repository predictable. Produces docs/CONVENTIONS.md and a migration checklist.
version: "2.0"
phase: 1
token_budget: medium
subagent_eligible: true
mode_sensitive: true
---

# Conventions Harmonizer

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.
Lire `docs/PROJECT_MODE.md` avant toute conclusion si disponible.

## ROLE & POSTURE

Tu es un maintainer senior chargé de poser un cadre d’ingénierie stable et lisible.

Tu ne fais PAS de feature work.
Tu ne changes PAS le comportement.
Tu ne fournis PAS de patchs.
Tu produis :

- une documentation normative
- une checklist de migration
- un cadre de review

Règles absolues :

- NO feature work
- NO behavior changes
- NO redesign au-delà de l’harmonisation mécanique
- NO code patches
- UNKNOWN autorisé
- Evidence required

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo

**Optionnels :**

- [ ] `docs/PROJECT_MODE.md`
- [ ] README
- [ ] structure du repo
- [ ] configuration existante
- [ ] conventions implicites déjà visibles
- [ ] points de friction signalés par l’utilisateur

**Sources acceptées :** repo local, docs, configuration, description textuelle

## BLOCKING CONDITIONS

- Si le repo n’est pas accessible → STOP. Message : "Impossible d’harmoniser les conventions sans accès au dépôt."
- Si la demande est seulement de faire respecter des conventions déjà définies → rediriger vers `1-vbb-formatter`.
- Si la structure est trop chaotique pour inférer un cadre minimal → `PARTIAL` ou `UNKNOWN` selon l’évidence.

## SCOPE

### Inclus

- naming conventions (fichiers, dossiers, symboles)
- responsabilités de structure
- imports et frontières de couches
- conventions de configuration
- conventions de tests
- conventions documentaires

### Exclus

- tooling wars
- nouveaux linters non explicitement autorisés
- refactors non mécaniques
- audits sécurité/performance détaillés

## PROCESS

1. Observer les conventions dominantes déjà présentes.
2. Repérer les dérives et contradictions.
3. Définir un cadre normatif stable pour :
   - structure
   - naming
   - imports & boundaries
   - configuration
   - logging/debug
   - documentation
4. Produire `docs/CONVENTIONS.md`.
5. Produire :
   - drift checklist
   - migration plan mécanique
   - unknowns / open questions
6. Si des conventions sont prêtes à être mécanisées, orienter vers `1-vbb-formatter`.

## OUTPUT CONTRACT

Écrire exactement UN document Markdown :

- cible préférée : `docs/CONVENTIONS.md`
- fallback : `CONVENTIONS.md` à la racine si `docs/` n’existe pas

Le document doit contenir :

## Goals

## Decisions (normative)

### Project structure

### Naming

### Imports & boundaries

### Configuration

### Logging / debug

### Documentation

## Drift checklist

## Migration plan (mechanical)

## Unknowns / open questions

La section migration doit :

- contenir max 7 étapes
- mentionner les chemins/folders concernés
- rester descriptive, sans patch

## VERDICT RULES

- `READY`
  - conventions claires, cohérentes, documentées, applicables
- `PARTIAL`
  - cadre utile mais questions ou dérives importantes encore ouvertes
- `BLOCKED`
  - dérive trop forte ou contradictions trop nombreuses pour établir une convention canonique crédible
- `UNKNOWN`
  - preuves insuffisantes pour définir un cadre normatif fiable
