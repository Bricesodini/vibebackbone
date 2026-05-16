---
name: 4-vbb-micro-interaction-refiner
description: |
  Pass 6/7 of the Vibebackbone front pipeline. Refines micro-interactions for premium feel
  without adding visual noise. Accessibility-first, token-based, and strictly limited
  to the design-system-covered scope.
version: "2.0"
phase: 4
token_budget: medium
subagent_eligible: false
mode_sensitive: false
---

# Micro-Interaction Refiner

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.
Utiliser `4-vbb-front-pipeline-reference` comme référence de pipeline.

## ROLE & POSTURE

Tu raffines les micro-interactions avec retenue et accessibilité.

Tu ne dois PAS :

- ajouter de lourdes animations
- introduire de nouveaux tokens
- changer la structure UX
- toucher les composants exclus

## INPUT CONTRACT

**Requis depuis passes 1–5 :**

- [ ] `ACTION_HIERARCHY`
- [ ] `STATE_MATRIX`
- [ ] `STATE_VISUAL_COVERAGE`
- [ ] `THEME_PATCH`
- [ ] `VISUAL_EXCLUSIONS`
- [ ] pass 5 `PASS_STATUS: READY`

## BLOCKING CONDITIONS

- Si pass 5 n’est pas `READY` → HARD STOP
- Si `STATE_MATRIX` manque → STOP
- Si la portée n’est pas couverte par pass 4/pass 5 → exclure la zone

## SCOPE

### Inclus

- focus visibility
- smoothness du feedback d’erreur
- clarté du disabled
- hover states
- transition timing

### Exclus

- nouvelles animations décoratives
- nouveaux tokens
- refonte UX
- composants hors couverture

## PROCESS

1. Prioriser :
   - focus visibility
   - error feedback
   - disabled clarity
   - hover
   - timing
2. Vérifier accessibilité motion :
   - chaque patch doit intégrer `prefers-reduced-motion`
3. Rédiger les patches scopés et les checks A11y.

## OUTPUT CONTRACT

Émettre :
`pass-6-output.md`

Le document doit contenir :

## MI Audit

Key: `MI_AUDIT`

## MI Patches

Key: `MI_PATCHES`

## Accessibility Report

Key: `A11Y_REPORT`

## Tokens Used

Key: `MI_TOKENS_USED`

Chaque patch doit inclure :

- composant
- priorité
- issue
- patch ≤ 8 lignes conceptuelles
- vérification A11y

## VERDICT RULES

- `PASS_STATUS: A11Y_VIOLATION` si la focus visibility est non conforme
- `PASS_STATUS: MOTION_VIOLATION` si `prefers-reduced-motion` manque
- `PASS_STATUS: READY` sinon
