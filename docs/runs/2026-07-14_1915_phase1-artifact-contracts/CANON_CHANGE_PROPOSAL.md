---
run_id: "2026-07-14_1915_phase1-artifact-contracts"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-14T19:22:00+02:00"
human_validated_by: "Brice — explicit Go"
---

# Canon Change Proposal — Authored artifact alignment

## Current canon

Artifact kinds are closed and `artifact: null` is valid for v0.3 contracts.

## Problem

Eight Phase-1 skills normatively write files but formally declare no artifact;
the API design output has no truthful existing kind.

## Proposed canon

Add `design_document`; map the eight exact paths; reject Phase-1 normative
report/document writer instructions paired with `artifact: null`.

## Benefits

1. Truthful output contracts.
2. Runtime-observable required files.
3. Automated drift prevention.

## Risks

1. Narrow dependency on normative wording.
2. Conditional supplemental files remain represented only in runtime output.

## Impact analysis

Eight contracts, the Core linter and tests change. Runtime path checking already
supports the new kind. Four distributions inherit without adapter changes.

## Migration plan

Add kind and linter rule atomically with all eight mappings and tests.

## Backward compatibility

- [x] Fully backward compatible — existing skill behavior and paths are unchanged.

## Human decision

- [x] **Approved** — explicit `Go` from Brice for this authorized run sequence.

**Validator signature**: Brice **Date**: 2026-07-14
