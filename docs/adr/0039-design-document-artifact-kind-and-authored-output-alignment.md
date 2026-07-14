# ADR 0039 — Design-document artifact kind and authored-output alignment

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit Go), Codex
**Related to**: ADR 0004
**Related POC**: `docs/runs/2026-07-14_1915_phase1-artifact-contracts/POC.md`

## Context

Eight Phase-1 skills explicitly instruct the agent to write a report or design
document, but their v0.3 contracts declare `artifact: null`. Seven outputs are
audits; the API contract designer's output is a design document and does not fit
the existing closed kind set without semantic distortion.

## Decision

Add `design_document` to the closed artifact taxonomy. Map the eight normative
outputs to their exact paths, including `AUDIT_STATUS.md` only where the skill
requires it. Contract lint rejects `artifact: null` for a `1-vbb-*` skill whose
SKILL.md contains a line-start normative instruction to write a report or
document.

## Consequences

### Positive

- Contracts describe the files the skills already require.
- API design is not mislabeled as an audit or generic phase artifact.
- Future Phase-1 prose/contract null drift fails before merge.

### Negative / costs

- The linter recognizes one narrow normative prose pattern.
- New authored-output wording must remain compatible or move to structured
  metadata in a future schema.

### Neutral

- Runtime/executor artifact path verification is already kind-agnostic.

## Rejected alternatives

### Alternative A — Label the API design as `audit_report`

Rejected because the skill explicitly performs pre-implementation design and
forbids audit verdicts.

### Alternative B — Use `phase_artifact` with empty frontmatter

Rejected because the file is a domain design document outside the run phase
artifact hierarchy and has no canonical phase template.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Prose detector false positive | Low | Medium | Restrict to `1-vbb-*`, line-start `Write`, and `report/document` |
| Dynamic supplemental docs remain unmodeled | Medium | Low | Keep `files_created` output; model only deterministic primary/persistent paths |

## Assumptions

- The normative output lines remain authoritative until artifact declarations
  move into a single structured source.
- Conditional supplemental documentation is represented in structured runtime
  outputs, not as a deterministic artifact path.

## References

- Audit: `docs/audits/impact-analysis-phase1-artifact-contracts-20260714-1915.md`
- POC: `docs/runs/2026-07-14_1915_phase1-artifact-contracts/POC.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - "ADR 0004"
blocks:
  - "docs/runs/2026-07-14_1915_phase1-artifact-contracts"
supersedes: []
verified_at: "2026-07-14T19:22:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-go + artifact-inventory + runtime-inspection"
```
