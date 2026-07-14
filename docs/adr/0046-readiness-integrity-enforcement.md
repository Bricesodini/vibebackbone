# ADR 0046 — Enforce readiness integrity at runtime boundaries

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit `go`), Codex
**Related POC**: `docs/runs/2026-07-14_2124_readiness-integrity/POC.md`

## Context

A legacy `~/.codex/AGENTS.md` symlink can point to the tracked Core
`AGENTS.md`. The Codex compiler and uninstaller follow that link and mutate the
source. The dashboard then continues to expose the documentary READY token,
and strict loop closure does not validate the declared long-run timing fields.

## Decision

1. Provider runtime writers never follow a destination symlink into a Core
   source. The known legacy Codex link is migrated to a regular compiled file;
   unrelated links require explicit force and are replaced without mutating
   their targets.
2. Canonical governance sources containing generated runtime markers are
   rejected before compilation.
3. The dashboard exposes documentary and measured verdicts separately while
   keeping `verdict` as the effective, conservative result.
4. Strict loop closure rejects internally inconsistent long-run summaries.

## Consequences

### Positive

- Core governance cannot be recursively compiled through a legacy runtime link.
- READY cannot remain green when repository invariants visibly fail.
- Existing long-run declarations become machine-checkable.

### Negative / costs

- Dashboard consumers that interpreted `verdict` as documentary-only truth
  must use the new `documented_verdict` field.
- Legacy symlink migration adds provider-specific installer branches.

## Rejected alternatives

- Preserve the Codex symlink: rejected because compiled runtime content and
  canonical source content have different ownership.
- Only repair the current machine: rejected because it leaves every existing
  installation exposed.
- Continue parsing READY without measurements: rejected because it recreates
  the false-green state.

## Rollback

Revert the implementation commit and restore the previous dashboard schema.
Do not recreate the unsafe Codex-to-Core symlink.
