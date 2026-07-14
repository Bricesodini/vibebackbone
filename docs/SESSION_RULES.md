---
context_role: session-rules
phase: transverse
status: active
updated: 2026-07-13
---

# SESSION_RULES — When to stay, when to switch

> 1 session = 1 role = 1 intent = 1 usable output

## Stay in the same session

All criteria true: same role · same route · scope unchanged or reduced · risk unchanged or lowered · context <75% · reasonable duration (FAST-ZERO <5 min, FAST-MINIMAL <15 min, FAST <30 min, others <2 h)

## Switch to a new session

Mandatory if at least one: role changes · risk increases · scope widens · context >75% · closeout produced · duration exceeded · provider changes

## Escalation → new session

FAST task that reveals data/auth/security/compliance/prod impact: **immediate stop** → partial `07_CLOSEOUT.md` → new session STRUCTURED or AUDIT. Detail: [PILOTAGE.md § Escalation rule](PILOTAGE.md#escalation-rule)

## Context compaction (40% / 75%) — ADR-0029

- **~40% of context window consumed** — indicative threshold: run
  `python tools/vbb-context-compactor.py docs/runs/<id>` and write a
  mini-handoff (recommended, not blocking). Between two scoped-audit passes,
  this is the default checkpoint (cf. `REFERENCE/scoped-audit-protocol.md`).
- **75%** — hard limit: compaction **or** new session is mandatory **before any
  new action**. This is the prescriptive side of the existing "context <75%"
  stay criterion above: crossing it without compacting is an anti-pattern.

## Session handoff

Continuity is carried by versioned artifacts, not conversation. Full read/write cycle in [MEMORY_AND_HANDOFF.md](MEMORY_AND_HANDOFF.md).

## Anti-patterns

- Continuing FAST after detecting elevated risk
- `05_EXECUTION` without frozen `04_PLAN` in STRUCTURED route
- Two runs in the same `docs/runs/{slug}/` folder
- Resuming without reading previous run's `07_CLOSEOUT.md`
- Crossing 75% context without compaction or session switch (see § Context compaction)

Memory anti-patterns: [MEMORY_AND_HANDOFF.md § Anti-patterns](MEMORY_AND_HANDOFF.md#anti-patterns)

## Handoff vs Closeout

The `07_CLOSEOUT.md` artefact carries an explicit `kind:` field in its frontmatter, distinguishing two semantics:

- **`HANDOFF`** : travail non terminé, reprise attendue. `docs/SESSION.md` (local, gitignored) contains non-trivial `Actions en cours`. The next session should resume from this state.
- **`CLOSEOUT`** : fin claire du processus. `docs/SESSION.md` is emptied (or replaced by a pointer to this closeout) before the run is declared complete.

**Rule of thumb:**

- If the run produced value AND nothing meaningful is left for the next session → `CLOSEOUT`.
- If the run produced partial value AND the next session must resume work → `HANDOFF`.

**Session history archive:** every handoff is mirrored to `docs/SESSION.history/{YYYY-MM-DD}.md` (local, gitignored) before `SESSION.md` is updated for the next session. This preserves continuity across machine reinstalls without leaking session content into the versioned repo.

Canonical reference: [`docs/templates/07_CLOSEOUT.md.template`](templates/07_CLOSEOUT.md.template) (frontmatter `kind:` field).
Auto-computation: [`prompts/canonical/07-p-vbb-closeout.md` § Étape 1](../prompts/canonical/07-p-vbb-closeout.md).

## Links

- [PILOTAGE.md](PILOTAGE.md) — triage, routes, escalation
- [MEMORY_AND_HANDOFF.md](MEMORY_AND_HANDOFF.md) — memory, handoff, read/write cycle
- [AGENTIC_RUN_PROTOCOL.md](AGENTIC_RUN_PROTOCOL.md) — the 7 phases
