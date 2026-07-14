# ADR 0038 — Unique generic routing-trigger ownership

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit Go), Codex
**Related to**: ADR 0032
**Related POC**: `docs/runs/2026-07-14_1845_routing-trigger-precedence/POC.md`

## Context

Six case-insensitive trigger strings are shared by two contracts. The router
scores substring matches and cannot infer whether a generic phrase names a
reference, an audit, a cleanup, a gate, a detector or a report.

## Decision

Every case-insensitive exact routing trigger has one contract owner. Generic
phrases belong to the broad entrypoint responsible for that intent; adjacent
skills remain discoverable through qualified action/stage phrases. Contract
lint blocks duplicate exact triggers catalog-wide.

## Consequences

### Positive

- Strict routing is deterministic for the six known generic intents.
- Ownership is readable directly from contract metadata.
- Future exact collisions fail before merge.

### Negative / costs

- Secondary intents require a more explicit query.
- Trigger changes require responsibility-corpus maintenance.

### Neutral

- Router scoring, skill IDs and phase scopes do not change.

## Rejected alternatives

### Alternative A — Static numeric contract priority

Rejected because a global bias hides intent ownership and can distort unrelated
queries.

### Alternative B — Keep ambiguity and rely on strict-mode errors

Rejected because all six collisions have a clear generic owner and a useful
qualified secondary phrase.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Qualified phrase still overlaps via substring | Medium | Medium | Strict responsibility tests |
| Legitimate future shared trigger | Low | Low | Use a qualified phrase; revise ADR if evidence requires sharing |

## Assumptions

- Exact generic trigger sharing is not a supported multiplexing mechanism.
- More specific queries are acceptable for secondary responsibilities.

## References

- Audit: `docs/audits/impact-analysis-routing-trigger-precedence-20260714-1845.md`
- POC: `docs/runs/2026-07-14_1845_routing-trigger-precedence/POC.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - "ADR 0032"
blocks:
  - "docs/runs/2026-07-14_1845_routing-trigger-precedence"
supersedes: []
verified_at: "2026-07-14T18:51:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-go + catalog-inventory + router-characterization"
```
