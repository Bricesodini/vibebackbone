# ADR 0043 — Domain verdict and runtime status orthogonality

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit approval), Codex
**Related to**: ADR 0042
**Related POC**: `docs/runs/2026-07-14_2115_verdict-status-boundary/POC.md`

## Context

All contracts expose runtime statuses, while six contracts also carry a root
`verdict_mapping` that no linter, runtime or executor consumes. The mappings
conflate a skill's successful execution with its conclusion about the audited
subject and one mapping emits `NOT_APPLICABLE`, which is not a runtime status.

## Decision

Domain verdicts and runtime statuses are orthogonal. Runtime status reports
contract execution (`PASS`, `PARTIAL`, `FAIL`, `BLOCKED`); domain verdicts
report the conclusion about the subject using the vocabulary owned by the
skill. Core does not infer one dimension from the other and rejects root
`verdict_mapping` metadata.

## Consequences

### Positive

- A successful audit may report a negative domain conclusion without becoming
  a technical failure.
- Six dead mappings and their invalid extension disappear.
- The boundary is enforceable without copying boilerplate to 64 contracts.

### Negative / costs

- Consumers that need policy coupling must declare it explicitly rather than
  relying on an implicit conversion.

### Neutral

- Current runtime behavior is unchanged because it never consumed the field.

## Rejected alternatives

### Alternative A — Copy a canonical mapping to every contract

Rejected because it creates boilerplate and preserves semantic conflation.

### Alternative B — Introduce contract schema v0.4 now

Rejected because no current consumer requires a structured domain-verdict
field; the migration would be speculative.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Hidden consumer reads the unversioned root field | Low | Medium | Repository-wide search plus four-distribution impact review |
| Future consumer needs structured domain verdicts | Medium | Low | Open a schema ADR from demonstrated consumption evidence |

## Assumptions

- Repository search accurately represents Core and active distribution code.
- Runtime status remains the sole gate comparison dimension today.

## References

- Audit: `docs/runs/2026-07-14_1745_skill-catalog-optimization-audit/02_AUDIT_REPORT.md`
- Impact: `docs/audits/impact-analysis-verdict-status-boundary-20260714-2115.md`
- POC: `docs/runs/2026-07-14_2115_verdict-status-boundary/POC.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - "PATT-05"
blocks:
  - "docs/runs/2026-07-14_2115_verdict-status-boundary"
supersedes: []
verified_at: "2026-07-14T21:15:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-approval + repository-evidence"
```
