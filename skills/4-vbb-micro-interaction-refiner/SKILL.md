---
name: 4-vbb-micro-interaction-refiner
description: |
  Pass 6/7 of the Vibebackbone front pipeline. Refines micro-interactions for premium feel
  without adding visual noise. Accessibility-first, token-based, and strictly limited
  to the design-system-covered scope.
version: "2.1"
phase: 4
token_budget: medium
subagent_eligible: false
mode_sensitive: false
---

# Micro-Interaction Refiner

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Use `4-vbb-front-pipeline-reference` as pipeline reference.

## ROLE & POSTURE

You refine micro-interactions with restraint and accessibility.

You must NOT:

- add heavy animations
- introduce new tokens
- change UX structure
- touch excluded components

## INPUT CONTRACT

**Required from passes 1–5:**

- [ ] `ACTION_HIERARCHY`
- [ ] `STATE_MATRIX`
- [ ] `STATE_VISUAL_COVERAGE`
- [ ] `THEME_PATCH`
- [ ] `VISUAL_EXCLUSIONS`
- [ ] pass 5 `PASS_STATUS: READY`

## BLOCKING CONDITIONS

- If pass 5 is not `READY` → HARD STOP
- If `STATE_MATRIX` is missing → STOP
- If scope is not covered by pass 4/pass 5 → exclude zone

## SCOPE

### Included

- focus visibility
- error feedback smoothness
- disabled clarity
- hover states
- transition timing

### Excluded

- new decorative animations
- new tokens
- UX refactor
- out-of-coverage components

## PROCESS

1. Prioritize:
   - focus visibility
   - error feedback
   - disabled clarity
   - hover
   - timing
2. Check motion accessibility:
   - each patch must integrate `prefers-reduced-motion`
3. Write scoped patches and A11y checks.

## OUTPUT CONTRACT

Emit:
`pass-6-output.md`

Document must contain:

## MI Audit

Key: `MI_AUDIT`

## MI Patches

Key: `MI_PATCHES`

## Accessibility Report

Key: `A11Y_REPORT`

## Tokens Used

Key: `MI_TOKENS_USED`

Each patch must include:

- component
- priority
- issue
- patch ≤ 8 conceptual lines
- A11y verification

## VERDICT RULES

- `PASS_STATUS: A11Y_VIOLATION` if focus visibility is non-compliant
- `PASS_STATUS: MOTION_VIOLATION` if `prefers-reduced-motion` is missing
- `PASS_STATUS: READY` otherwise