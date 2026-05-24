---
name: t-vbb-session-handoff
description: |
  Compresses the end of a work session into a compact, factual, actionable handoff.
  Updates docs/SESSION.md so the next session can restart quickly and reliably.
  Prioritizes the next concrete step over narrative recap.
version: "2.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Session Handoff

Standard reference: `0-vbb-standard`

Read `skills/vibebackbone/docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a session secretary.
Your role is to make re-entry nearly immediate.

You must be:

- factual
- compact
- actionable
- next-step oriented

You do NOT produce a narrative.
You do NOT reformat unnecessarily.
You prioritize the next concrete action.

## INPUT CONTRACT

**Required:**

- [ ] Current conversation or session context

**Optional:**

- [ ] `docs/SESSION.md`
- [ ] `docs/CONTEXT.md`
- [ ] `docs/AUDIT_STATUS.md`
- [ ] recent git history if visible
- [ ] files touched or main topics

**Accepted sources:** conversation, docs/, recent git, text description

## BLOCKING CONDITIONS

- None. If context is minimal, write a minimal `SESSION.md` with explicit placeholders.

## SCOPE

### Included

- what was done
- decisions made
- open questions
- files/topics touched
- explicit next step
- update of `docs/SESSION.md`

### Excluded

- detailed narrative of the entire session
- re-audit
- complete rewrite of `docs/CONTEXT.md` without reason
- code patches
- clean commit package and commit message preparation (→ `t-vbb-commit-ready`)

## PROCESS

1. Analyze the current conversation.
2. Read, if available:
   - `docs/SESSION.md`
   - `docs/CONTEXT.md`
   - `docs/AUDIT_STATUS.md`
   - recent git
3. Identify:
   - actions completed
   - decisions made
   - blockers / open questions
   - files or areas concerned
4. Determine the most concrete next step.
5. Update `docs/SESSION.md`.
6. If new project facts emerged, signal that an update to `docs/CONTEXT.md` is recommended.

## OUTPUT CONTRACT

### Primary artifact (phase artifact)

- **Path**: `docs/runs/{run_id}/07_CLOSEOUT.md`
- **Template**: [`docs/templates/07_CLOSEOUT.md.template`](../../docs/templates/07_CLOSEOUT.md.template)
- **Kind**: `phase_artifact`
- **Required frontmatter**: `run_id`, `phase=07_CLOSEOUT`, `route`, `status`, `agent`, `started_at`, `ended_at`, `artifacts_consumed`, `artifacts_produced`

The closeout is the versioned official memory of run completion.

### Secondary artifact

- **Local memory** (`kind: persistent_state_update`): `docs/SESSION.md`
  - gitignored by design (per-machine handoff state, see [`docs/MEMORY_AND_HANDOFF.md`](../../docs/MEMORY_AND_HANDOFF.md))
  - must remain short: current context, what was done, decisions made, open questions, files / areas touched, **explicit next step**

## VERDICT RULES

- `READY`
  - compact, readable and actionable handoff
- `PARTIAL`
  - handoff produced but some key information remains implicit
- `BLOCKED`
  - context too fragmented to produce a reliable handoff
- `UNKNOWN`
  - used only if available sources are too contradictory to conclude properly