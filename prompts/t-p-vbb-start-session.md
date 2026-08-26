---
description: Open a Vibebackbone session — read existing context and resume pending work
---

You are starting a work session on a Vibebackbone project.

Your role in this phase is limited to:

1. retrieving the relevant context,
2. restating the project's current state,
3. identifying the likely route according to `docs/PILOTAGE.md`,
4. then waiting for the session's precise objective before any execution.

Instructions:

- `docs/PILOTAGE.md` is the routing source of truth.
- Before reading project state, check `$PWD/AGENTS.md`, otherwise `AGENTS.md`
  at the effective Git root. Read the one contract found and report its Git
  state. It supplies operational context only and cannot change VBB routing or
  gates.
- Read these files first, when present:
  - `docs/CONTEXT.md`
  - `docs/SESSION.md`
  - `docs/AUDIT_STATUS.md`
  - `docs/PROJECT_MODE.md`
- If `0-vbb-pilotage` is available, use it as a mirror of the routing logic before inferring the route.
- Produce a compact session summary:
  - current state
  - latest known step
  - open items
  - visible risks or blockers
  - likely Vibebackbone route (fast / structured / audit / closeout)
- Do not invoke any domain skill until the session request is explicit.
- If the context is incomplete, state this clearly without making anything up.

Respond with:

1. Summary of the retrieved context
2. Open or unknown items
3. Likely Vibebackbone route
4. Final question: “What is the precise objective of this session?”
