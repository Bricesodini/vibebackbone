---
name: t-vbb-status-dashboard
description: |
  Read-only terminal dashboard for Vibebackbone repo health.
  Shows verdict, skills, contracts, tests, latest runs, open risks,
  and next action. Keywords: status, dashboard, health check,
  repo status, terminal dashboard.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Status Dashboard

Read `skills/vibebackbone/docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a status reader.

Your role is to display the current state of the Vibebackbone repo.

You are **read-only** — you never modify files.

## INPUT CONTRACT

Required: repository access. Optional: JSON, full, or alternate-repository mode.

## BLOCKING CONDITIONS

Stop when the target repository is inaccessible or not sufficiently initialized
to locate its governance state.

## SCOPE

Read and display current repository health. Do not synthesize durable reports,
change state, or remediate findings.

## PROCESS

```bash
python tools/vbb-status-dashboard.py
python tools/vbb-status-dashboard.py --json
python tools/vbb-status-dashboard.py --full
python tools/vbb-status-dashboard.py --repo <path>
```

## OUTPUT CONTRACT

Return the measured verdict, compact health summary and explicit next action;
emit JSON only when requested.

## VERDICT RULES

- `PASS`: dashboard measurements completed without active blocker.
- `PARTIAL`: measurements completed with open risks or incomplete optional data.
- `BLOCKED`: required repository state cannot be read.
