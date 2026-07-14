# ADR 0040 — Front-pass and release artifact semantics

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE / ENGINE_ONLY context
**Decision makers**: Brice (explicit Go), Codex
**Related to**: ADR 0039
**Related POC**: `docs/runs/2026-07-14_1945_front-artifact-contracts/POC.md`

## Context

Five front passes explicitly emit stable `pass-N-output.md` files and the
product changelog writes `CHANGELOG.md`, but all six contracts declare no
artifact. The changelog does not fit the existing closed taxonomy truthfully.

## Decision

Front pass outputs use `phase_artifact` with required existence and an explicit
empty frontmatter requirement because their canonical format is key-based, not
run-frontmatter based. Product changelogs use the new closed kind
`release_document`; `CHANGELOG.md` is primary and the versioned release note is
optional secondary. Front-family normative emit/update instructions may not be
paired with `artifact: null`.

## Consequences

### Positive

- Every explicit front pass file becomes runtime-observable.
- Changelog semantics remain truthful.
- Pipeline behavior and ordering remain untouched.

### Negative / costs

- One artifact kind and two bounded prose patterns are added to lint.

### Neutral

- No UI/UX pass is executed and no visual state is changed.

## Rejected alternatives

### Alternative A — Treat CHANGELOG.md as a design document

Rejected because it is release communication, not product design.

### Alternative B — Treat pass files as optional

Rejected because each output contract says `Emit:` and names exactly one file.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Front detector catches descriptive prose | Low | Medium | Restrict to `4-vbb-*` line-start `Emit:` or `Update (or create)` |
| Optional release note treated as mandatory | Low | Medium | Secondary `must_exist_after_run: false` |

## References

- `skills/4-vbb-front-pipeline-reference/SKILL.md`
- `docs/audits/impact-analysis-front-artifact-contracts-20260714-1945.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - "ADR 0039"
blocks:
  - "docs/runs/2026-07-14_1945_front-artifact-contracts"
supersedes: []
verified_at: "2026-07-14T19:51:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-go + orchestrator-routing + output-inventory"
```
