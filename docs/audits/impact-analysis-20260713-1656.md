---
kind: "audit_report"
audit_type: "impact-analysis"
run_id: "2026-07-13_1656_retire-hermes"
status: "READY"
date: "2026-07-13"
agent: "codex / t-vbb-impact-analyzer"
---

# Impact analysis — Hermes retirement

## Change analyzed

Official support is narrowed to Pi, OpenCode, Codex and Claude Code; all live
Hermes/Cody distribution code and active documentation are removed.

## Direct impact

- Breaking removal of `distributions/hermes/` and `--provider hermes`.
- Removal or neutralization of Hermes-specific tests, hooks and messages.
- Canonical architecture and distribution catalog change.

## Indirect impact

- Generated `docs/RELATIONS.md` changes with the distribution block.
- README, GUIDE, DEPLOYMENT, RUNBOOK, Core sentinel and changelog must agree.
- Historical artifacts continue to contain Hermes references by design.

## External impact

- Four supported provider adapters are independent of Hermes; selective dry-run
  for all four exited 0 before implementation.
- Runtime state below `~/.hermes/` is external and will not be touched.
- Direct external imports of the removed proxy are UNKNOWN.

## Contracts / APIs / schemas

- Breaking CLI surface: `--provider hermes` rejected after cutover.
- No skill contract, data schema, API or database change.
- Core credential rule remains; the Hermes-only bypass implementation is retired.

## Classification

**BREAKING**, intentionally accepted via ADR 0025 and the user's explicit request.

## UNKNOWN

- Whether an untracked consumer relies on the repository proxy modules.

## FINAL_STATUS

```yaml
FINAL_STATUS:
  verdict: COMPLETE
  files_touched:
    - docs/runs/2026-07-13_1656_retire-hermes/02_AUDIT.md
    - docs/audits/impact-analysis-20260713-1656.md
  tests_run:
    - four-provider selective setup dry-run
    - provider dependency scan
  tests_missing:
    - external consumer inventory
  risks:
    - intentional provider CLI break
  open_points: []
```
