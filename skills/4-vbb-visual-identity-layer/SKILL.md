---
name: 4-vbb-visual-identity-layer
description: |
  Pass 5/7 of the Vibebackbone front pipeline. Applies validated visual identity after
  UX stabilization, under strict moodboard and human validation requirements.
  Runs in two phases: visual freeze first, implementation second.
version: "2.1"
phase: 4
token_budget: high
subagent_eligible: false
mode_sensitive: false
---

# Visual Identity Layer

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Use `4-vbb-front-pipeline-reference` as pipeline reference.

## ROLE & POSTURE

You apply visual identity only after structural and human validation.

You must NOT:

- modify flow or action hierarchy
- touch excluded components
- change token structure
- introduce unvalidated visual decisions

## INPUT CONTRACT

**Required from passes 1–4:**

- [ ] `ACTION_HIERARCHY`
- [ ] `STATE_MATRIX`
- [ ] `CANONICAL_PATTERNS`
- [ ] `TOKEN_COVERAGE`
- [ ] `DS_SCORE`
- [ ] `DS_EXCEPTIONS`

**Mandatory moodboard:**

- [ ] visual description
- [ ] ≥ 2 web references
- [ ] palette
- [ ] typographic direction
- [ ] intensity level
- [ ] explicit restrictions

## BLOCKING CONDITIONS

- If pass 4 is `BLOCKED` → HARD STOP
- If pass 4 is `CONDITIONAL` without human validation → STOP
- If a moodboard element is missing → STOP, max 1 clarification round
- If still incomplete → `PASS_BLOCKED: moodboard_incomplete`

## SCOPE

### Phase A — Visual Freeze

- moodboard analysis
- visual intent synthesis
- await human validation

### Phase B — Implementation

- only within `TOKEN_COVERAGE` coverage
- never on `DS_EXCEPTIONS`
- token-based application only

## PROCESS

### Phase A

1. Extract visual principles.
2. Write `VISUAL_INTENT`.
3. Await explicit human validation.

### Phase B

1. Reapply confirmed `VISUAL_INTENT`.
2. Produce `THEME_PATCH`.
3. Verify `STATE_VISUAL_COVERAGE`.
4. Document justifications and exclusions.

## OUTPUT CONTRACT

Emit:
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

- `PASS_STATUS: AWAITING_VALIDATION` if Phase A not validated
- `PASS_STATUS: READY` once Phase B is produced

`VISUAL_INTENT` + `THEME_PATCH` become the rollback snapshot for pass 7.