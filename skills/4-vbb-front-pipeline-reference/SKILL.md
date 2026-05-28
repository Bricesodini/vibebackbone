---
name: 4-vbb-front-pipeline-reference
description: |
  Canonical reference for the 7-pass Vibebackbone front pipeline. Defines execution modes,
  subsystem boundaries (ENGINE vs VISUAL), gate conditions, scope locks, and rollback protocol.
  This is a decision and protocol reference, not an execution pass.
version: "2.1"
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

## VALIDITY CRITERIA

A pass output is INVALID if it contains only:
  - token lists without SURFACE_CARTOGRAPHY
  - primitive component proposals without surface context
  - migration plans without CENTRALIZATION_ROADMAP

A pass output is VALID only if:
  - Pass 1: SURFACE_CARTOGRAPHY (named surfaces) + STATE_MATRIX (7 states mapped)
  - Pass 4: TOKEN_DEFINITION_MAP + PRIMITIVE_REGISTRY_CHECK + CENTRALIZATION_GAPS + CENTRALIZATION_ROADMAP
  - All passes: No direct primitive proposals before surface mapping complete

## SEPARATION OF RESPONSIBILITIES

| Pass | Required Keys | Optional Seeds |
|------|---------------|---------------|
| Pass 1 (UX Engine) | SURFACE_CARTOGRAPHY, STATE_MATRIX | TOKEN_DEFINITION_MAP seeds, PRIMITIVE_REGISTRY_CHECK seeds |
| Pass 4 (Design System) | TOKEN_DEFINITION_MAP, PRIMITIVE_REGISTRY_CHECK, CENTRALIZATION_GAPS, CENTRALIZATION_ROADMAP | — |

## GENERIC_OUTPUT_DETECTION

If output contains phrases like:
  - "commençons par les tokens"
  - "créons Button/Badge/Tooltip"
  - "migration vers un design system"
WITHOUT prior SURFACE_CARTOGRAPHY → REJECT and return to pass 1.

## GATE ENFORCEMENT

| Gate | Requirement |
|------|-------------|
| pass 1 → 2 | SURFACE_CARTOGRAPHY must exist |
| pass 2 → 3 | CANONICAL_PATTERNS must reference SURFACE_CARTOGRAPHY |
| pass 3 → 4 | SURFACE_CARTOGRAPHY + STATE_MATRIX must be frozen |
| pass 4 → 5 | All 6 required keys must be populated (2 from Pass 1, 4 from Pass 4) |

**Pass 4 → 5 gate detail (6 keys required):**

| Key | Source | Requirement |
|-----|--------|-------------|
| SURFACE_CARTOGRAPHY | Pass 1 | Must exist, Level 1–2 named |
| STATE_MATRIX | Pass 1 | Must map 7 states to surfaces |
| TOKEN_DEFINITION_MAP | Pass 4 | Must show definition → usage traceability |
| PRIMITIVE_REGISTRY_CHECK | Pass 4 | Must identify central vs local primitives |
| CENTRALIZATION_GAPS | Pass 4 | Must list non-centralized values with impact |
| CENTRALIZATION_ROADMAP | Pass 4 | Must order remediation by surface level |

If any key is missing or empty → HARD BLOCK, return to appropriate pass.

## VERDICT RULES

Cette ressource n'émet pas READY / PARTIAL / BLOCKED par défaut.

Sortie attendue :

- clarification de protocole
- rappel de gate
- rappel de mode
- detection de generic_output si applicable
