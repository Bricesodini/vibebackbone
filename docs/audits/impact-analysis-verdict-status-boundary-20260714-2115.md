---
audit_id: "impact-analysis-verdict-status-boundary-20260714-2115"
skill: "t-vbb-impact-analyzer"
status: "READY"
classification: "NON_BREAKING"
date: "2026-07-14"
---

# Impact analysis — Verdict/status boundary

## Change analyzed

Remove six unused root `verdict_mapping` blocks, define domain verdict and
runtime status as independent dimensions, and reject mapping reintroduction.

## Direct impact

Six contracts, the skill standard, contract lint and controlled tests.

## Indirect impact

Contract authors must expose execution status independently from their domain
conclusion. Gate comparisons continue to use runtime status only.

## External impact

Pi, OpenCode, Codex and Claude Code inherit the same Core boundary. Repository
search finds no distribution adapter or tool consumer of `verdict_mapping`.

## Final classification

**NON_BREAKING.** The removed field is not consumed by Core runtime, executor,
linter, tests or active distribution code.

## UNKNOWN areas

External unpublished consumers are not observable. The field was never part of
a validated schema contract.

```yaml
FINAL_STATUS:
  verdict: READY
  tests_run:
    - "repository-wide verdict_mapping consumer search"
  tests_missing: []
  risks: []
  open_points: []
```
