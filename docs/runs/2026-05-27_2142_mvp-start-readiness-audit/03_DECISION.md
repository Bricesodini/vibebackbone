---
run_id: "2026-05-27_2142_mvp-start-readiness-audit"
phase: "03_DECISION"
voie: "AUDIT"
status: "PARTIAL"
agent: "codex"
started_at: "2026-05-27T20:10:00Z"
ended_at: "2026-05-27T20:15:00Z"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "docs/audits/mvp-start-readiness-20260527-2142.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — MVP Start Readiness Audit

## Decision

Proceed to implementation only after treating the MVP Start integration as a systemic governance change, not as a documentation-only patch.

## Rationale

The audit found that the requested behavior spans canonical governance, routing, prompt entrypoints, skill contracts, index coverage and public counters. A partial patch would create parallel truth: Markdown could say "no code before readiness" while the executable router and prompt matrix still permit normal structured execution.

## Accepted implementation baseline

- Add `docs/MVP_START_PROTOCOL.md`.
- Add `skills/0-vbb-rico-readiness/SKILL.md` and `CONTRACT.yaml`.
- Add the new skill to `skills/INDEX.yaml`.
- Update routing documentation and the prompt router.
- Update `docs/CONTEXT.md` as a compact pointer only.
- Update `docs/PILOTAGE.md` and `docs/AGENTIC_RUN_PROTOCOL.md` with blocking readiness rules.
- Harmonize counters and release/status wording after the new inventory is known.

## Decisions still open

1. Count MVP START as a fifth public route or document it as a mandatory pre-route gate before STRUCTURED EXECUTION.
2. Create a dedicated prompt `0-p-vbb-mvp-start.md` or update `0-p-vbb-before-building.md` to invoke RICO readiness first.
3. Correct rc.1 release-count drift in place or add an `Unreleased` section that records the correction.

## Next action

Start a STRUCTURED implementation run once the three open decisions are resolved or explicitly scoped by the executor.
