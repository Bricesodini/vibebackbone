---
run_id: "2026-07-14_2124_readiness-integrity"
phase: "02_AUDIT"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
---

# POC — legacy Codex symlink corruption

**Status**: CONCLUDED
**Date**: 2026-07-14
**Linked ADR**: `docs/adr/0046-readiness-integrity-enforcement.md`
**Linked run**: `docs/runs/2026-07-14_2124_readiness-integrity/`

## Hypothesis

The current forced Codex deployment follows a legacy destination symlink and
recursively grows the tracked Core source.

## Test

Run two forced Codex installs in a disposable archived copy of the repository,
with `$HOME/.codex/AGENTS.md` linked to that copy's root `AGENTS.md`.

## Success criterion

The defect is verified if the source byte count increases and the number of
generated start markers grows after the second deployment.

## Observed result

- Source before: `5904` bytes.
- After first forced deployment: `10606` bytes, `1` generated start marker.
- After second forced deployment: `15309` bytes, `2` generated start markers.
- Current real worktree independently contains `104` accidental added lines in
  `AGENTS.md` and the runtime path resolves to that source.

## Decision

Verdict: GO

The defect is deterministic and the implementation must add a no-follow
migration plus source-integrity guard before any real deployment is retried.

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0046-readiness-integrity-enforcement.md
hypothesis_validated: true
metric_observed: "5904 -> 10606 -> 15309 bytes; 0 -> 1 -> 2 markers"
metric_threshold: "source unchanged; exactly one runtime marker pair"
reproducible: true
verified_at: "2026-07-14T21:00:33+02:00"
verified_by: "codex"
```
