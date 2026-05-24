---
context_role: session-rules
phase: transverse
status: active
updated: 2026-06-12
---

# SESSION_RULES — When to stay, when to switch

> 1 session = 1 role = 1 intent = 1 usable output

## Stay in the same session

All criteria true: same role · same route · scope unchanged or reduced · risk unchanged or lowered · context <75% · reasonable duration (FAST-ZERO <5 min, FAST-MINIMAL <15 min, FAST <30 min, others <2 h)

## Switch to a new session

Mandatory if at least one: role changes · risk increases · scope widens · context >75% · closeout produced · duration exceeded · provider changes

## Escalation → new session

FAST task that reveals data/auth/security/compliance/prod impact: **immediate stop** → partial `07_CLOSEOUT.md` → new session STRUCTURED or AUDIT. Detail: [PILOTAGE.md § Escalation rule](PILOTAGE.md#escalation-rule)

## Session handoff

Continuity is carried by versioned artifacts, not conversation. Full read/write cycle in [MEMORY_AND_HANDOFF.md](MEMORY_AND_HANDOFF.md).

## Anti-patterns

- Continuing FAST after detecting elevated risk
- `05_EXECUTION` without frozen `04_PLAN` in STRUCTURED route
- Two runs in the same `docs/runs/{slug}/` folder
- Resuming without reading previous run's `07_CLOSEOUT.md`

Memory anti-patterns: [MEMORY_AND_HANDOFF.md § Anti-patterns](MEMORY_AND_HANDOFF.md#anti-patterns)

## Links

- [PILOTAGE.md](PILOTAGE.md) — triage, routes, escalation
- [MEMORY_AND_HANDOFF.md](MEMORY_AND_HANDOFF.md) — memory, handoff, read/write cycle
- [AGENTIC_RUN_PROTOCOL.md](AGENTIC_RUN_PROTOCOL.md) — the 7 phases