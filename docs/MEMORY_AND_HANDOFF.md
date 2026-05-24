---
context_role: memory-rules
phase: transverse
status: active
updated: 2026-06-12
---

# MEMORY_AND_HANDOFF — Official memory and transitions

> vibebackbone memory is not in the conversation. It lives in stable artifacts, versioned or explicitly local.

## Three memory levels

| Level | Duration | Examples | Authority |
|-------|----------|---------|-----------|
| Conversational | Ephemeral | LLM context window | Never authoritative |
| Local persistent | Gitignored | `docs/SESSION.md`, `.vbb/` | Survives session, not machine |
| Official versioned | Persistent | `docs/CONTEXT.md`, `docs/AUDIT_STATUS.md`, `docs/runs/`, `docs/audits/` | **Source of truth** |

On divergence: **official always wins**. Conversation alone is never authoritative.

## Handoff — What must cross

| Information | Medium |
|-------------|--------|
| Major decision | `07_CLOSEOUT.md` + `docs/CONTEXT.md` |
| Remaining action | `07_CLOSEOUT.md` |
| Unresolved risk | `docs/AUDIT_STATUS.md` |
| Operating mode | `docs/PROJECT_MODE.md` |
| Immediate re-entry | `docs/SESSION.md` (local) |

**Does not cross**: intermediate reasoning, abandoned explorations, verbose output, conversation history.

## Read/write cycles

**Write** (end of session): conversation → filter → `07_CLOSEOUT.md` → synthesize → `CONTEXT.md` / `AUDIT_STATUS.md`

**Read** (start of session):
1. `docs/CONTEXT.md` (always)
2. `docs/PROJECT_MODE.md` (always)
3. `docs/SESSION.md` (if present)
4. `docs/AUDIT_STATUS.md` (if AUDIT route)
5. Latest `07_CLOSEOUT.md`

Do not load all of `docs/runs/` — target the current run.

## Anti-patterns

- Citing conversational fact without writing it in an artifact
- Resuming without reading `07_CLOSEOUT.md`
- Updating `CONTEXT.md` without going through a closeout
- Treating `SESSION.md` as authoritative (it is local)
- Compacting context before persisting decisions

## Links

- [SESSION_RULES.md](SESSION_RULES.md) — when to switch sessions
- [PILOTAGE.md](PILOTAGE.md) — triage and routes
- [AGENTIC_RUN_PROTOCOL.md](AGENTIC_RUN_PROTOCOL.md) — the 7 phases