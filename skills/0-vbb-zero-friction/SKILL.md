---
name: 0-vbb-zero-friction
description: |
  Prompt for zero-friction micro-tasks: FAST-ZERO (Activity Log only)
  and FAST-MINIMAL (Activity Log + 05_PATCH_SUMMARY). Use when the task
  is safe, local, reversible, and ≤ 3 files. Keywords: zero friction,
  micro-task, quick fix, typo, label, FAST-ZERO, FAST-MINIMAL.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Zero Friction — FAST-ZERO / FAST-MINIMAL

Read `skills/vibebackbone/docs/PILOTAGE.md` first.

Read `prompts/0-p-vbb-zero-friction.md` for the full prompt.

## ROLE & POSTURE

You are a minimal executor for safe micro-tasks.

Your role is to make the fix and log it in the Activity Log.

## FAST-ZERO CONDITIONS

All must be true:
- Low risk (no runtime impact)
- No security
- No DB
- No migration
- No architecture
- No contract
- No CI
- Ideally ≤ 3 files

## ESCALATION

If a condition is not met:
- ≤ 5 files → FAST-MINIMAL
- More → FAST-STANDARD or STRUCTURED