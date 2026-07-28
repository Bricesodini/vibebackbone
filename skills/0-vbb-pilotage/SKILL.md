---
name: 0-vbb-pilotage
description: |
  Reference for Vibebackbone execution paths and triage rules.
  Use when selecting workflow, clarifying execution level, or checking how a task
  should be routed across FAST, STRUCTURED, AUDIT, or HANDOFF paths.
  Post-cutoff (2026-07-28_1400) tasks also require declaring an adversarial
  level (A0/A1/A2) per the criticality matrix; this skill surfaces that
  requirement during triage.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
adr: "0051"
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
- (post-cutoff) the adversarial level declaration

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
- (post-cutoff) adversarial level declaration rules

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
6. (Post-cutoff) **Declare the adversarial level** per the criticality
   matrix in `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.2. Apply
   the 7 fail-closed rules of §4.3 (escalation always toward more
   prudent). If the declared level is contested, the effective level
   is `A1` until resolution.

## ADVERSARIAL LEVEL TRIAGE (post-cutoff)

Per ADR 0051, every post-cutoff run must declare its adversarial level:

- **A0** — pure documentation with no agent-steering effect, no
  contract, no behavior, no data path. Never for governance canon
  per `§1.1` (governance canon = minimum A1).
- **A1** — observable behavior change on a single internal surface;
  bounded exploration.
- **A2** — auth, secrets, data integrity, money, published contract,
  concurrency, deployment, governance canon, `S0/S1` history in
  last 10 runs. Requires distinct actor + human decision or
  `A2_DISTINCT_AGENT_PROXY`.

**Fail-closed rules:**

| Situation | Effective level |
|---|---|
| Undeclared level | A1 |
| Level declared A0 but A1/A2 trigger matches | trigger level |
| Contested level (written objection in 01_INTAKE.md) | A1 |
| Conflict between declarer and classifier | A1 |

## OUTPUT CONTRACT

Output must contain:

- selected path
- (post-cutoff) declared adversarial level + reason
- brief explanation
- reminder of escalation rule if relevant
- corresponding Vibebackbone skill family
- explicit note when `docs/PILOTAGE.md` and this skill diverge, with document precedence stated

## VERDICT RULES

Default output = path clarification.

Do NOT emit READY / PARTIAL / BLOCKED / UNKNOWN unless explicitly requested.
