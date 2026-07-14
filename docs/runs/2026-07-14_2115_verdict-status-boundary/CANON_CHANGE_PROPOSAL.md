---
run_id: "2026-07-14_2115_verdict-status-boundary"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-14T21:18:00+02:00"
human_validated_by: "Brice — explicit approval for all proposed runs"
---

# Canon Change Proposal — Verdict/status orthogonality

## Current canon

Runtime status and domain verdict coexist without an explicit boundary; six
contracts carry unused mappings.

## Proposed canon

Treat the dimensions as independent and reject root mapping metadata.

## Benefits

Clear semantics, no dead boilerplate, enforceable boundary.

## Risks

An unpublished external consumer may have read an unvalidated field.

## Human decision

- [x] **Approved** — Brice approved the complete proposed sequence.

**Validator signature**: Brice **Date**: 2026-07-14
