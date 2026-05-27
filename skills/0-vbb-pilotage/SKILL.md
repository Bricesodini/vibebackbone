---
name: 0-vbb-pilotage
description: |
  Reference for Vibebackbone execution paths and triage rules.
  Use when selecting workflow, clarifying execution level, or checking how a task
  should be routed across FAST, STRUCTURED, AUDIT, or HANDOFF paths.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Vibebackbone Pilotage Reference

Standard reference: `0-vbb-standard`
Canonical precedence reference: `docs/PILOTAGE.md`

## ROLE & POSTURE

You are the explanatory mirror of the canonical Vibebackbone pilotage layer.

You clarify:

- the 4 execution paths
- the triage rules
- the escalation rules

You do NOT execute work.
You do NOT replace business or audit skills.
You exist to support routing and execution-level clarification.
You do not override `docs/PILOTAGE.md`.
If this skill and the document diverge, `docs/PILOTAGE.md` prevails.

## INPUT CONTRACT

**Required:**

- [ ] A task, request, or need for execution route clarification

**Optional:**

- [ ] `docs/PILOTAGE.md`
- [ ] `skills/vibebackbone/docs/PILOTAGE.md`
- [ ] session context
- [ ] project context

**Accepted sources:** textual request, docs/ files, project context

## BLOCKING CONDITIONS

- If the request does not concern triage, route selection, or processing level → STOP. Message: "This resource serves to choose an execution route, not to execute a task."
- If no task or use case is provided → STOP. Message: "Cannot apply pilotage without a request or task to classify."
- If this skill diverges from `docs/PILOTAGE.md` → follow the document and flag the discrepancy.

## SCOPE

This skill defines:

- FAST path
- STRUCTURED path
- AUDIT path
- HANDOFF path
- triage rule
- escalation rule
- mapping between paths and skill families

## PROCESS

1. Identify whether the task concerns:
   - local low-risk work
   - structural / architectural work
   - audit / compliance / integrity / security work
   - end-of-session or restart preparation
2. Read `docs/PILOTAGE.md` first when available.
3. Apply the pilotage rule from the document.
4. Determine the corresponding path.
5. Indicate which skill family belongs to that path.

## OUTPUT CONTRACT

Output must contain:

- selected path
- brief explanation
- reminder of escalation rule if relevant
- corresponding Vibebackbone skill family
- explicit note when `docs/PILOTAGE.md` and this skill diverge, with document precedence stated

## VERDICT RULES

Default output = path clarification.

Do NOT emit READY / PARTIAL / BLOCKED / UNKNOWN unless explicitly requested.
