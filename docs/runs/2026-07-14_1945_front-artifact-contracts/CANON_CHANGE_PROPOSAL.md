---
run_id: "2026-07-14_1945_front-artifact-contracts"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-14T19:51:00+02:00"
human_validated_by: "Brice — explicit Go"
---

# Canon Change Proposal — Front and release artifacts

## Current canon

Artifact kinds are closed; front authored-output null drift is not blocked.

## Problem

Six normative front/release outputs are null and changelog semantics lack a
truthful kind.

## Proposed canon

Add `release_document`, map exact outputs, and block null artifacts for bounded
front-family `Emit:` / `Update (or create)` instructions.

## Benefits

1. Truthful contracts.
2. Runtime-observable pass files.
3. Optional release notes remain optional.

## Risks

1. Bounded prose-pattern dependency.
2. One additional closed artifact kind.

## Impact analysis

Six contracts, Core lint and tests change. Four distributions inherit without
adapter changes; pipeline behavior is unchanged.

## Human decision

- [x] **Approved** — explicit `Go` from Brice.

**Validator signature**: Brice **Date**: 2026-07-14
