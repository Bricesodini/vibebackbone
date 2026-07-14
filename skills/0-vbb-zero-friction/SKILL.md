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

## INPUT CONTRACT

Required: a concrete micro-task. Optional: the expected file list and existing
`docs/ACTIVITY_LOG.md`.

## BLOCKING CONDITIONS

If any FAST-ZERO condition fails, do not continue on that route; apply the
escalation rule below.

## SCOPE

Only safe, local, reversible micro-tasks affecting no more than three files and
no runtime, security, data, migration, architecture, contract, or CI behavior.

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

## PROCESS

Read the full prompt, validate every FAST-ZERO condition, apply the bounded
change, run proportionate verification, and record the required artifact.

## OUTPUT CONTRACT

- FAST-ZERO: update `docs/ACTIVITY_LOG.md` only.
- FAST-MINIMAL: update the Activity Log and write `05_PATCH_SUMMARY.md`.

## VERDICT RULES

- `PASS`: bounded change and required record complete.
- `PARTIAL`: safe work completed but verification or record is incomplete.
- `BLOCKED`: the task cannot remain on a zero-friction route.
