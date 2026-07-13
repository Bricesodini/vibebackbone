---
run_id: "2026-07-13_1656_retire-hermes"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-13T17:03:00+02:00"
human_validated_by: "Brice — explicit request, 2026-07-13"
---

# Canon Change Proposal — Supported runtimes

## Current Canon

Five active distributions including Hermes/Cody; some Core texts assume Cody as
the orchestrator enforcing otherwise generic VBB rules.

## Problem

Hermes did not satisfy the operator and creates disproportionate code,
security, test and documentation surface.

## Proposed Canon

Official support is limited to Pi, OpenCode, Codex and Claude Code. Core rules
use runtime-neutral language. Hermes-specific code is removed, not promoted.

## Benefits

1. Clear product boundary.
2. Smaller maintenance and security surface.
3. Consistent installer and documentation.

## Risks

1. Intentional break for Hermes users.
2. External proxy consumers are unknown.
3. Historical references may be mistaken for active support.

## Backward Compatibility

- [x] Breaking change — recorded in ADR 0025 and CHANGELOG.

## Human Decision

- [x] **Approved** — explicit request from Brice.

## Verification Loop

- [x] Architecture lint and graph (0 error, 0 warning; `docs/RELATIONS.md` regenerated).
- [x] Contract lint (0 error, 0 warning).
- [x] Loop closure strict, claims, plan and test-audit validation.
- [x] Full pytest and local CI (`133 passed, 1 skipped`; CI 7 PASS, 1 WARN non-blocking).
- [x] Four-provider dry-run and active-reference scan.
