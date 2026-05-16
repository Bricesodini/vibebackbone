---
name: 4-vbb-visual-identity-layer
description: |
  Pass 5/7 of the Vibebackbone front pipeline. Applies validated visual identity after
  UX stabilization, under strict moodboard and human validation requirements.
  Runs in two phases: visual freeze first, implementation second.
version: "2.0"
phase: 4
token_budget: high
subagent_eligible: false
mode_sensitive: false
---

# Visual Identity Layer

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.
Utiliser `4-vbb-front-pipeline-reference` comme référence de pipeline.

## ROLE & POSTURE

Tu appliques l’identité visuelle seulement après validation structurelle et humaine.

Tu ne dois PAS :

- modifier le flow ou l’action hierarchy
- toucher aux composants exclus
- changer la structure des tokens
- introduire des décisions visuelles non validées

## INPUT CONTRACT

**Requis depuis passes 1–4 :**

- [ ] `ACTION_HIERARCHY`
- [ ] `STATE_MATRIX`
- [ ] `CANONICAL_PATTERNS`
- [ ] `TOKEN_COVERAGE`
- [ ] `DS_SCORE`
- [ ] `DS_EXCEPTIONS`

**Moodboard obligatoire :**

- [ ] description visuelle
- [ ] ≥ 2 références web
- [ ] palette
- [ ] direction typographique
- [ ] niveau d’intensité
- [ ] restrictions explicites

## BLOCKING CONDITIONS

- Si pass 4 est `BLOCKED` → HARD STOP
- Si pass 4 est `CONDITIONAL` sans validation humaine → STOP
- Si un élément moodboard manque → STOP, max 1 clarification round
- Si toujours incomplet → `PASS_BLOCKED: moodboard_incomplete`

## SCOPE

### Phase A — Visual Freeze

- analyse du moodboard
- synthèse d’intention visuelle
- attente de validation humaine

### Phase B — Implementation

- seulement dans la couverture `TOKEN_COVERAGE`
- jamais sur `DS_EXCEPTIONS`
- application token-based uniquement

## PROCESS

### Phase A

1. Extraire principes visuels.
2. Rédiger `VISUAL_INTENT`.
3. Attendre validation humaine explicite.

### Phase B

1. Réappliquer `VISUAL_INTENT` confirmé.
2. Produire `THEME_PATCH`.
3. Vérifier `STATE_VISUAL_COVERAGE`.
4. Documenter justifications et exclusions.

## OUTPUT CONTRACT

Émettre :
`pass-5-output.md`

### Phase A

## Visual Intent Summary

Key: `VISUAL_INTENT`
`[AWAITING HUMAN VALIDATION]`

### Phase B

## 1. Visual Intent Summary (confirmed)

## 2. Theme Patch

Key: `THEME_PATCH`

## 3. State Visual Coverage

Key: `STATE_VISUAL_COVERAGE`

## 4. Justification Log

## 5. Exclusion Log

Key: `VISUAL_EXCLUSIONS`

## VERDICT RULES

- `PASS_STATUS: AWAITING_VALIDATION` si Phase A non validée
- `PASS_STATUS: READY` une fois la Phase B produite

`VISUAL_INTENT` + `THEME_PATCH` deviennent le snapshot de rollback pour pass 7.
