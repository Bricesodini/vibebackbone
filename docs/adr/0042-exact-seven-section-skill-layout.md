# ADR 0042 — Exact seven-section skill layout

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit Go), Codex
**Related to**: `0-vbb-standard`
**Related POC**: `docs/runs/2026-07-14_2045_skill-section-normalization/POC.md`

## Context

Twelve skills diverge from the standard: five combine equivalent sections and
seven compact wrappers omit headings even though their behavior is usable.

## Decision

Every catalog SKILL.md contains the exact seven mandatory level-two headings.
Additional sections remain allowed. Equivalent combined headings are split
without semantic change. Compact wrappers use concise one-to-three-line sections
and are not expanded with duplicated guidance.

## Consequences

### Positive

- Predictable parsing and review across 64 skills.
- Compact skills remain compact.
- Future drift is blocked by catalog lint.

### Negative / costs

- Tool wrappers carry a small amount of explicit structural prose.

### Neutral

- Skill responsibilities, commands and routing remain unchanged.

## Rejected alternatives

### Alternative A — Accept semantic heading aliases

Rejected because alias sets create another mapping surface and combined sections
obscure blocking/scope boundaries.

### Alternative B — Expand wrappers to full standard examples

Rejected because it would increase cognitive load without behavioral value.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Added prose changes behavior | Low | Medium | Minimal factual wrappers; responsibility regression review |
| Exact lint rejects useful extra sections | Low | Low | Require presence only; allow additional headings |

## References

- `docs/audits/impact-analysis-skill-section-normalization-20260714-2045.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on: []
blocks:
  - "docs/runs/2026-07-14_2045_skill-section-normalization"
supersedes: []
verified_at: "2026-07-14T20:52:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-go + exact-catalog-inventory"
```
