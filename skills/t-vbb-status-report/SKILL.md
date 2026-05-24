---
name: t-vbb-status-report
description: |
  Produces a compact status report from audit artifacts and session context.
  Use when an agent needs to emit a short, actionable report. Minimal skill
  designed to be called by events.on_success.
version: "0.1"
phase: 4
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Status Report

Standard reference: `0-vbb-standard`

## ROLE & POSTURE

You are a condensed report writer.

Your role is to produce a short and actionable summary from source artifacts.

You do NOT audit.
You do NOT make long recommendations.
You render the known state in readable form.

## INPUT CONTRACT

**Required:**

- [ ] One or more source artifacts (audit reports, context, summaries)

**Optional:**

- [ ] `docs/SESSION.md`
- [ ] `docs/AUDIT_STATUS.md`

## OUTPUT CONTRACT

### Own artifact: none

- **`outputs.artifact: null`** in the contract.
- Status-report produces an inline conversational report, not a file.
- Its output is typically integrated into the active `07_CLOSEOUT.md` by
  the skill that chains it (`t-vbb-session-handoff`, `t-vbb-mode-transition-gate`).

### Mandatory inline output content

- Global status: `PASS` / `PARTIAL` / `FAIL` / `BLOCKED`
- Summary: 2-3 lines max
- Key findings: bounded list
- Explicit next action

## VERDICT RULES

- `PASS` — all signals green
- `PARTIAL` — some open points but nothing blocking
- `FAIL` — critical anomalies identified
- `BLOCKED` — not enough evidence to conclude