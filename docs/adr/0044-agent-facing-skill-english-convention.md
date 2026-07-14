# ADR 0044 — Agent-facing skill English convention

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit approval), Codex
**Related to**: ADR 0036
**Related POC**: `docs/runs/2026-07-14_2145_skill-english-migration/POC.md`

## Context

ADR 0036 migrated active prompts to English. A conservative scan now finds
French instructional prose in five active `SKILL.md` files, creating a mixed
agent-facing catalog despite otherwise shared Core behavior.

## Decision

All active agent-facing prose in `skills/*/SKILL.md` is English. Closed
machine-facing route, risk, verdict and status enums may remain allowlisted;
historical evidence is not rewritten. A conservative regression test enforces
both instructional markers and unapproved accented tokens.

## Consequences

### Positive

- One operational language across prompts and skills.
- Future prose drift is detected without treating every technical token as text.
- Commands, paths, IDs and contract enums remain stable.

### Negative / costs

- French-language trigger examples become English; routing contracts remain
  responsible for multilingual support when evidence demonstrates a need.

### Neutral

- User-facing conversation language remains unrestricted.

## Rejected alternatives

### Alternative A — Translate only the large Janitor block

Rejected because four small mixed-language residues would keep the convention
ambiguous.

### Alternative B — Reject every accented character globally

Rejected because machine enums and historical evidence require explicit,
reviewable exceptions.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Translation changes a behavioral condition | Low | Medium | Preserve structure, commands, paths, verdicts and IDs; scoped diff review |
| Detector produces false positives | Low | Low | Conservative vocabulary and closed token allowlist |

## References

- ADR 0036
- Impact: `docs/audits/impact-analysis-skill-english-migration-20260714-2145.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - "ADR 0036"
blocks:
  - "docs/runs/2026-07-14_2145_skill-english-migration"
supersedes: []
verified_at: "2026-07-14T21:45:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-approval + classified-inventory"
```
