# ADR 0045 — Section-aware dashboard verdict parsing

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit execution approval), Codex
**Related to**: independent READY revalidation
**Related POC**: `docs/runs/2026-07-14_2245_dashboard-ready-parser/POC.md`

## Context

`AUDIT_STATUS.md` canonically places its closed global verdict on the first
content line after `## Global verdict`. The dashboard only looks for backticks
on the heading itself, then scans a fallback list that omits `READY`. A valid
READY document therefore becomes generated `UNKNOWN`.

## Decision

The dashboard parses the `Global verdict`/`Verdict global` section first and
returns the first closed status token (`READY`, `PARTIAL`, `PASS`, `FAIL`,
`BLOCKED`, `UNKNOWN`) from the heading or its first bounded content lines. A
word-bounded top-of-file fallback preserves legacy documents.

## Consequences

### Positive

- Canonical READY truth is represented accurately.
- Section-local parsing avoids unrelated status words elsewhere in the file.
- Legacy same-line and top-of-file forms remain supported.

### Negative / costs

- The parser owns a small closed status vocabulary that must evolve with canon.

### Neutral

- Dashboard JSON shape and CLI remain unchanged.

## Rejected alternatives

### Alternative A — Change `AUDIT_STATUS.md` to emit `PASS`

Rejected because it hides the parser defect and changes the campaign verdict.

### Alternative B — Add only `READY` to the old fallback

Rejected because the primary section parser would remain structurally broken.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Parser selects prose rather than verdict | Low | Medium | Section-local bounded scan and word boundaries |
| Legacy format regresses | Low | Low | Controlled same-line and fallback tests |

## References

- Impact: `docs/audits/impact-analysis-dashboard-ready-parser-20260714-2245.md`
- POC: `docs/runs/2026-07-14_2245_dashboard-ready-parser/POC.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on: []
blocks:
  - "docs/runs/2026-07-14_2245_dashboard-ready-parser"
supersedes: []
verified_at: "2026-07-14T22:45:00+02:00"
verified_by: "Brice + Codex"
verified_method: "reproduction + explicit-approval"
```
