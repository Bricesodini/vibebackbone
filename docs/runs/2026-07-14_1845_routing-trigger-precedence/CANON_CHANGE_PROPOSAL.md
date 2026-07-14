---
run_id: "2026-07-14_1845_routing-trigger-precedence"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-14T18:51:00+02:00"
human_validated_by: "Brice — explicit Go"
---

# Canon Change Proposal — Unique generic trigger ownership

## Current canon

Routing triggers are precise descriptions but exact uniqueness is not enforced.

## Problem

Six shared exact triggers produce ambiguous ownership in the current substring
scorer.

## Proposed canon

Each case-insensitive exact trigger has one owner. Adjacent responsibilities use
qualified action/stage phrases. Contract lint blocks duplicates.

## Benefits

1. Deterministic generic routing.
2. Readable responsibility ownership.
3. Automated drift prevention.

## Risks

1. Secondary queries become more explicit.
2. Qualified phrases require regression coverage.

## Impact analysis

Five contract pairs, Core contract lint and router responsibility tests change.
All four distributions inherit the rule without adapter changes.

## Migration plan

Replace secondary duplicates atomically, add lint, then verify twelve queries.

## Backward compatibility

- [x] Fully backward compatible for generic intents; explicit secondary intent
  phrasing is required where routing was previously ambiguous.

## Human decision

- [x] **Approved** — explicit `Go` from Brice for this authorized run sequence.

**Validator signature**: Brice **Date**: 2026-07-14
