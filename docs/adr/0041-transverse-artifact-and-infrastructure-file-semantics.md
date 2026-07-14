# ADR 0041 — Transverse artifact and infrastructure-file semantics

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit Go), Codex
**Related to**: ADR 0039, ADR 0040
**Related POC**: `docs/runs/2026-07-14_2015_transverse-artifact-contracts/POC.md`

## Context

Five transverse writers declare null artifacts. Docker generation also produces
a deterministic infrastructure bundle for which the closed taxonomy has no
truthful kind. Anti-slop has two mutually exclusive report destinations.

## Decision

Add `infrastructure_file` to the closed taxonomy. Docker generation declares its
mandatory report and deterministic infrastructure bundle. Anti-slop always
ensures `docs/audits/` and writes its report there. Git-sync declares its report
with `must_exist_after_run: false`. Transverse normative writer patterns may not
be paired with `artifact: null`.

## Consequences

### Positive

- PATT-03 closes across all nineteen cases.
- Docker outputs become formally observable.
- Audit reports converge on one directory.

### Negative / costs

- Anti-slop consumers relying on the root fallback must use `docs/audits/`.
- Docker contract metadata becomes larger because the bundle is explicit.

### Neutral

- Generation behavior and filenames do not change.

## Rejected alternatives

### Alternative A — Keep anti-slop destination alternatives

Rejected because the current schema/runtime cannot enforce exactly-one paths and
the canonical directory is safe to create.

### Alternative B — Represent Docker files only in `generated_files`

Rejected because deterministic documented files should be formally verifiable.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Optional Docker topology file absent | Medium | Medium | Mark topology-dependent paths optional |
| Git-sync optional report falsely required | Low | Medium | Primary must-exist false |

## References

- `docs/audits/impact-analysis-transverse-artifact-contracts-20260714-2015.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - "ADR 0039"
  - "ADR 0040"
blocks:
  - "docs/runs/2026-07-14_2015_transverse-artifact-contracts"
supersedes: []
verified_at: "2026-07-14T20:22:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-go + output-inventory + impact-analysis"
```
