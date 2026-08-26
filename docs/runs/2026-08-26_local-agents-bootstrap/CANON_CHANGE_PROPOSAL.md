---
run_id: "2026-08-26_local-agents-bootstrap"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-08-26T00:00:00+02:00"
human_validated_by: "Brice — explicit implementation authorization in this session"
---

# Canon Change Proposal — repository-local operational contracts

## Current Canon

VBB Core starts from its own invariants and project-state hierarchy. It had no
declared, deterministic handoff for an external repository's `AGENTS.md`.

## Problem

Repository-specific operating constraints could be present but not demonstrably
loaded before `SESSION.md` and classification.

## Proposed Canon

Add one bounded local operational-contract discovery before project state. The
contract complements VBB and cannot change its governance logic.

## Benefits

1. Repository context is visible before decisions are made.
2. Untracked contracts remain visible rather than silently ignored.
3. No recursive parent discovery or consumer-specific knowledge is introduced.

## Risks

1. A provider may not invoke the Core bootstrap; entrypoint documentation and
   propagation evidence make that limitation visible.
2. Local prose may attempt governance; it is explicitly non-applicable.

## Impact Analysis

| Surface | Change |
|---|---|
| Governance Core | Bootstrap sequence, contract documentation and discovery tool |
| Prompt library | Two session/build entrypoints load before `SESSION.md` |
| Pi, Codex, Claude, OpenCode | Inherit unchanged Core source through existing adapters |
| Studio / consumers | No change |

## Human Decision

- [x] **Approved** — user authorized implementation in this session.

## Verification Loop

- [ ] Architecture, contract and full local-CI checks are recorded at closeout.
- [x] Targeted bootstrap tests added.
