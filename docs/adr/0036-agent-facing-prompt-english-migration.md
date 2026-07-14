# ADR — 0036-agent-facing-prompt-english-migration

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit request), Codex (formalization)
**Related to**: GMA-005, FL-01, FL-02, READY-GOV-001, READY-GIT-002
**Related POC**: `docs/runs/2026-07-14_1700_prompt-english-migration/POC.md`

## Context

The English-only prompt convention is already canonical, but 18 of 33 active
prompts still contain French instructions. These files are shared Core assets
installed by the Pi, OpenCode, Codex and Claude Code distributions.

## Decision

Translate the 18 affected prompts to English in place. Preserve filenames,
phase/route/verdict enums, command names, artifact paths, links, thresholds and
responsibility boundaries. Human-readable template labels and generic
placeholders are translated; executable tokens are not. Add a conservative
regression test for unambiguous French instructional markers. Do not translate
historical runs or governance documents under this decision.

## Consequences

### Positive

- One agent-facing language across all supported prompt entrypoints.
- The existing convention becomes testable rather than aspirational.
- All four distributions inherit the same Core correction.

### Negative / cost

- Large textual diff requiring structural equivalence review.
- Nuance can drift if machine tokens or decision thresholds are paraphrased.

### Neutral

- No prompt file moves, aliases, adapters, setup paths or provider state change.
- `SESSION.md` truth reconciliation is included as a prerequisite remediation,
  not as part of the prompt language policy.

## Rejected alternatives

### A — Keep French as a permanent exception

Rejected because it preserves a known conflict with the active convention and
the user explicitly requested English.

### B — Translate every Markdown document

Rejected because governance documents may retain their existing language and
historical evidence must not be rewritten.

### C — Rename routes and verdict enums during translation

Rejected because machine-facing tokens are contracts, not prose.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| behavioral drift | preserve tokens/links/thresholds and review diffs |
| inconsistent batches | non-overlapping ownership plus controller integration |
| future regression | conservative pytest language guard |

## References

- `docs/CONVENTIONS.md`
- `PROMPTS_ARCHITECTURE.md`
- `docs/audits/format-lint-prompt-language-20260714-1645.md`

```yaml
FINAL_STATUS: ACCEPTED
decision_class: AGENT_LANGUAGE
reversible: true
depends_on:
  - docs/CONVENTIONS.md
blocks:
  - prompt English migration
supersedes: []
verified_by: "Brice + Codex"
verified_method: "explicit-human-request + bounded-inventory"
```
