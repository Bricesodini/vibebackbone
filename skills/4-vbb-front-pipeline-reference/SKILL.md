---
name: 4-vbb-front-pipeline-reference
description: |
  Canonical reference for the 7-pass Vibebackbone front pipeline. Defines execution modes,
  subsystem boundaries (ENGINE vs VISUAL), gate conditions, scope locks, and rollback protocol.
  This is a decision and protocol reference, not an execution pass.
version: "2.0"
phase: 4
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Front Pipeline Reference

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d'abord.

## ROLE & POSTURE

Tu es une référence de pipeline.
Tu ne dois PAS exécuter le pipeline à la place des passes.
Tu définis :

- les modes d'exécution
- les sous-systèmes
- les gates
- les scope locks
- le rollback protocol

**Règle de déclenchement ENGINE_ONLY** :
Toute demande UI/UX, d'architecture visuelle, de cohérence graphique
ou de centralisation design doit entrer en `ENGINE_ONLY`.
Le mode VISUAL_ONLY ou FULL_RELEASE n'est autorisé qu'après validation
de `SURFACE_CARTOGRAPHY` via pass 1.

## INPUT CONTRACT

**Requis :**

- [ ] Une demande liée au pipeline front Vibebackbone

**Optionnels :**

- [ ] état courant des passes
- [ ] artefacts déjà produits
- [ ] besoin de clarification ENGINE / VISUAL / FULL_RELEASE

## BLOCKING CONDITIONS

- Si la demande ne concerne pas le pipeline front → STOP. Message : "Cette ressource documente uniquement le pipeline front Vibebackbone."
- Si aucun mode d'exécution n'est fourni lors d'un démarrage de pipeline → STOP et demander explicitement le mode.

## SCOPE

### Sous-systèmes

- ENGINE : passes 1-4
- VISUAL : passes 5-7

### Modes

- `ENGINE_ONLY`
- `VISUAL_ONLY`
- `FULL_RELEASE`

### Gates

- pass 1 → 2
- pass 2 → 3
- pass 3 → 4
- pass 4 → 5
- pass 5 → 6
- pass 6 → 7
- pass 7 → delivery

### Scope locks

- pass 1 locks task flow + action hierarchy
- pass 2 locks canonical patterns
- pass 3 locks approved structural changes
- pass 4 locks token coverage
- pass 5 locks visual snapshot

### Rollback

- triggered by pass 7 verdict `ROLLBACK`

## PROCESS

1. **Detect entry intent.** Si la demande est UI/UX / visuelle / design,
   forcer `ENGINE_ONLY` (pas d'entrée directe en pass 4+).
2. Déterminer le mode :
   - `ENGINE_ONLY` → passes 1–4 uniquement
   - `VISUAL_ONLY` → **interdit** sans `SURFACE_CARTOGRAPHY` valide
   - `FULL_RELEASE` → passes 1–7 après ENGINE_ONLY
3. Demander le mode d'exécution si absent et non déductible.
4. Confirmer le mode.
5. Déclarer le pass de départ.
6. Vérifier les préconditions amont.
7. Rappeler les subsystem boundaries.
8. Appliquer les gates et scope locks.
9. **Pour ENGINE_ONLY only**: valider que pass 1 produira
   `SURFACE_CARTOGRAPHY` avant toute progression.

## OUTPUT CONTRACT

La sortie doit contenir :

- mode d'exécution
- sous-système concerné
- pass de départ
- préconditions
- gates amont pertinents
- scope locks actifs
- protocole de rollback si demandé

## VERDICT RULES

Cette ressource n'émet pas READY / PARTIAL / BLOCKED par défaut.

Sortie attendue :

- clarification de protocole
- rappel de gate
- rappel de mode
