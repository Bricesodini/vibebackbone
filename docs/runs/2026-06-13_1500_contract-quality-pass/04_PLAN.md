---
phase: "04_PLAN"
run_id: "2026-06-13_1500_contract-quality-pass"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-06-13T15:05:00Z"
ended_at: "2026-06-13T15:10:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "docs/runs/2026-06-13_1500_contract-quality-pass/01_INTAKE.md"
artifacts_produced:
  - "docs/runs/2026-06-13_1500_contract-quality-pass/04_PLAN.md"
---

# 04_PLAN — RUN 20B: Contract Quality Pass

## RUN 01 (only run)

### Steps

1. **Inventory FR in machine-facing fields**: scan all 62 contracts for
   accented chars, FR words in events/gates/blocking_conditions
2. **Translate FR→EN**: batch-translate all event.reason, gate.reason,
   blocking_conditions.message fields
3. **Fix events: {} normalization**: decide whether empty events should be
   `{}` or `[]`; verify linter compatibility
4. **Analyze runtime results**: document PARTIAL/BLOCKED causes
5. **Verify**: lint, runtime, pytest, CI all pass

### Quality checks

- 0 lint errors (maintained)
- All machine-facing fields EN-only
- No SKILL.md modified
- No tools/tests/CI modified

### Decisions

- `events: {}` kept as dict (linter expects `.items()`)
- FR in `description` (frontmatter) allowed — human-facing
- FR in `triggers` allowed — keyword matching is language-agnostic