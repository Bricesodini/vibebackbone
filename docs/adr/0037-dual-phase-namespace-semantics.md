# ADR — 0037-dual-phase-namespace-semantics

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (`Go`), Codex (formalization)
**Related to**: PATT-02
**Related POC**: `docs/runs/2026-07-14_1815_phase-semantics/POC.md`

## Context

The repository uses two phase-shaped fields. `SKILL.md phase:` identifies the
canonical seven-phase agentic lifecycle, where Phase-1 audit skills use
`02_AUDIT`. Contract `routing.phase_scope` is a router filter based on catalog
tiers such as `phase_1`. Five skills had completed the frontmatter migration,
eleven had not, while all sixteen contracts consistently use `phase_1`.

## Decision

Keep the namespaces distinct and explicit:

- `SKILL.md phase:` uses canonical lifecycle labels; every `1-vbb-*` skill uses
  `02_AUDIT`;
- `CONTRACT.yaml routing.phase_scope` keeps `phase_1` for backward-compatible
  phase-router filtering;
- contract lint validates both sides for every `1-vbb-*` pair.

## Consequences

### Positive

- Removes deprecated frontmatter without breaking router consumers.
- Turns the intended mapping into a tested invariant.
- Makes future drift fail explicitly.

### Negative / cost

- Two namespaces remain and require clear naming/documentation.
- The linter contains one explicit prefix-to-phase mapping.

### Neutral

- No routing score, trigger, output contract or provider adapter changes.

## Rejected alternatives

### A — Revert five skills to `phase: 1`

Rejected because `PHASE_TO_SKILLS.md` explicitly deprecates numeric Phase 1.

### B — Change all contracts to `02_AUDIT`

Rejected because `vbb-phase-router.py` and its callers use `phase_1` as the
catalog routing scope; that would be a breaking API migration.

### C — Leave the distinction undocumented

Rejected because the independent audit already demonstrated recurring ambiguity.

## References

- `docs/PHASE_TO_SKILLS.md`
- `docs/audits/impact-analysis-phase-semantics-20260714-1815.md`

```yaml
FINAL_STATUS: ACCEPTED
decision_class: CONTRACT_SEMANTICS
reversible: true
depends_on:
  - docs/PHASE_TO_SKILLS.md
blocks:
  - PATT-02 remediation
supersedes: []
verified_by: "Brice + Codex"
verified_method: "explicit-go + impact-analysis + router-characterization"
```
