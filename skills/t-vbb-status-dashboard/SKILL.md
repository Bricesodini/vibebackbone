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

## TOOL

```bash
python tools/vbb-status-dashboard.py
python tools/vbb-status-dashboard.py --json
python tools/vbb-status-dashboard.py --full
python tools/vbb-status-dashboard.py --repo <path>
```