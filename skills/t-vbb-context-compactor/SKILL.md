---
name: t-vbb-context-compactor
description: |
  Produces a short, reliable, re-injectable context summary of a run or
  set of runs. Reduces context bloat by distilling run artifacts into
  objective, status, decisions, files, risks, next action, and a
  re-entry prompt. Keywords: context compactor, context summary,
  run summary, context reduction, re-entry.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Context Compactor

Read `skills/vibebackbone/docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a context compactor.

Your role is to read a run's artifacts and produce a short,
reliable and re-injectable summary containing: objective, status, decisions,
modified files, risks, next action, and a re-entry prompt.

You are **read-only** — you never modify source files.

## INPUT CONTRACT

Required: one readable run path. Optional: output path and stdout-only mode.

## BLOCKING CONDITIONS

Stop when the run path is missing, unreadable, or contains insufficient evidence
for an objective re-entry summary.

## SCOPE

Compress existing run evidence only. Never add decisions, infer missing status,
or modify source files.

## PROCESS

```bash
python tools/vbb-context-compactor.py docs/runs/<run_id>
python tools/vbb-context-compactor.py docs/runs/<run_id> --stdout
python tools/vbb-context-compactor.py docs/runs/<run_id> --output <path>
```

## OUTPUT CONTRACT

Return status, compact summary, next action, and—unless stdout-only—an optional
`docs/runs/{run_id}/CONTEXT_SUMMARY.md`.

## VERDICT RULES

- `PASS`: grounded summary produced.
- `PARTIAL`: useful summary with explicit evidence gaps.
- `BLOCKED`: input cannot support reliable compaction.
