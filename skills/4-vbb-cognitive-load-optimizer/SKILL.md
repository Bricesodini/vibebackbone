---
name: 4-vbb-cognitive-load-optimizer
description: |
  Pass 3/7 of the Vibebackbone front pipeline. Reduces cognitive load by optimizing
  information hierarchy, grouping, density, and terminology clarity without conflicting
  with passes 1 and 2.
version: "2.1"
phase: 4
token_budget: high
subagent_eligible: false
mode_sensitive: false
---

# Cognitive Load Optimizer

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Use `4-vbb-front-pipeline-reference` as pipeline reference.

## ROLE & POSTURE

You reduce mental friction and improve readability/scanability.

You must NOT:

- change aesthetics
- add decorative elements
- modify task flow defined in pass 1
- break canonical patterns defined in pass 2
- restructure action hierarchy
- produce code patches

## INPUT CONTRACT

**Required from passes 1–2:**

- [ ] `SIMPLIFIED_FLOW`
- [ ] `CANONICAL_PATTERNS`
- [ ] `ACTION_HIERARCHY`

## BLOCKING CONDITIONS

- If `SIMPLIFIED_FLOW` is missing → STOP. Message: "Cannot optimize cognitive load without validated flow."
- If `PASS_STATUS: STRUCTURAL_CONFLICT` from pass 2 → limit scope to non-conflicting zones and document exclusions.
- If an optimization contradicts `ACTION_HIERARCHY` or `CANONICAL_PATTERNS` → optimization forbidden.

## SCOPE

### Included

- visual density
- information hierarchy
- logical grouping
- label clarity/length
- scanning efficiency
- compatible structural simplifications

### Excluded

- aesthetics
- new UX patterns
- flow changes
- inversion of pass 1–2 decisions

## PROCESS

1. Calculate a cognitive score on 5 weighted dimensions:
   - visual density
   - information hierarchy clarity
   - logical grouping
   - label clarity & length
   - scanning efficiency
2. Identify friction zones.
3. Document optimizations forbidden by upstream conflict.
4. Propose only changes that can be approved without contradiction.
5. If score < 6, produce a mandatory text structural patch.

## OUTPUT CONTRACT

Emit:
`pass-3-output.md`

Document must contain:

## 1. Cognitive Load Score

Key: `CL_SCORE`

## 2. Excluded Zones

## 3. Key Friction Points

## 4. Conflict Log

Key: `CONFLICT_LOG`

## 5. Structural Improvement Proposals

Key: `APPROVED_CHANGES`

## 6. Structural Patch

mandatory if score < 6, pseudocode/description only

## VERDICT RULES

- `PASS_STATUS: BLOCKED` if `CL_SCORE < 4`
- `PASS_STATUS: PATCH_REQUIRED` if `4 ≤ CL_SCORE < 6`
- `PASS_STATUS: READY` if `CL_SCORE ≥ 6`

`APPROVED_CHANGES` is frozen for passes 4–7.