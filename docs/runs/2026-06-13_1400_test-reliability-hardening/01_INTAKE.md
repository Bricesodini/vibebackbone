---
phase: "01_INTAKE"
run_id: "2026-06-13_1400_test-reliability-hardening"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-06-13T14:00:00Z"
ended_at: null
next_phase: "04_PLAN"
artifacts_consumed: []
artifacts_produced:
  - "docs/runs/2026-06-13_1400_test-reliability-hardening/01_INTAKE.md"
---

# 01_INTAKE — RUN 20A: Test Reliability Hardening

## Objective

Make `pytest tests/ -q` fully green and `scripts/vbb-ci-local.sh` return unambiguous PASS.

## Problem diagnosis

### Pytest fixture errors (7/7 test files)

All 7 test files define a local `test(name: str, fn)` function as a lightweight
test runner. Pytest discovers this function signature and interprets `name` as a
fixture request → 7/7 `ERROR at setup of test — fixture 'name' not found`.

The tests work when run directly (`python3 tests/test_X.py`) but fail under pytest.

### CI loop closure WARN

The CI script's step 3 (`loop-closure-check`) runs without a run_id, auto-picks
the most recent run dir. The most recent run (`2026-06-13_1200_global-evaluation-audit`)
was produced by an AUDIT route session that used `route` instead of `voie` in
frontmatter, and was missing several required frontmatter fields. This causes
a WARN (non-blocking) in CI, which is ambiguous.

## Plan

### Fix 1: Convert test files to pytest-compatible format

Each test file currently uses a custom `test(name, fn)` runner called from `main()`.
Strategy: rewrite each so that individual test functions are discovered by pytest
directly. Keep backward compatibility with `python3 tests/test_X.py` via `if __name__ == "__main__"`.

Approach per file:
- Remove the global `test(name, fn)` function (conflicts with pytest collection)
- Rename `_test_*` helper functions to `test_*` so pytest discovers them
- Add `if __name__ == "__main__"` block that runs `pytest.main([__file__])`
  or calls each test directly for backward compatibility
- Keep all test logic identical — only structural changes

### Fix 2: Fix CI script loop closure ambiguity

Two options:
a. Pass explicit `--run-id` to loop-closure-check in CI (pick a known-good run)
b. Make loop-closure-check skip runs that aren't from STRUCTURED/FAST workflows

Best approach: (a) — use a known-good run ID. The CI should check the latest
run that was produced by a normal workflow, not by ad-hoc sessions. We'll add
a `--skip-unknown-voie` flag or simply pass a stable reference run.

Actually simpler: just fix the recent run's frontmatter so the WARN disappears.
But the broader fix is to make CI not WARN on unknown-voie runs. Let me look at
what runs exist with valid frontmatter.

Simpler approach: modify CI to pass `--run-id` pointing to the most recent run
that has proper frontmatter, or add a filter that skips UNKNOWN voie runs.

Best: add `--accept-unknown-voie` or simply make the CI script pass a hardcoded
reference run that is known-good. Even better: make the CI not do loop-closure
at all on the latest run (since it's ad-hoc) and instead run the loop-closure
test suite which already validates the tool.

Wait — the CI already runs `test_loop_closure.py` in step 4. The step 3 check
against the live repo is a dogfood check. The issue is that the latest run
doesn't have valid frontmatter. The cleanest fix is to ensure new runs have
proper frontmatter (which we're already doing in this run) and update the
CI to handle the UNKNOWN voie case gracefully.

Decision: Modify `vbb-loop-closure-check.py` to accept `--allow-unknown-voie`
which makes it skip the voie-requirement check and only verify that 07_CLOSEOUT
exists with valid frontmatter. Then update CI to use this flag.

Actually, even simpler: The CI loop-closure step uses `run_check_warn` (non-blocking).
The WARN is acceptable as documented. The task says "ensure CI returns clean PASS,
not ambiguous PASS/WARN unless documented." So we need to either:
1. Make the WARN documented and expected, OR
2. Fix the root cause (the run's frontmatter)

I'll do both: fix the recent run frontmatter (it's our own audit run, we can
update it) and add a comment in the CI script documenting when WARN is expected.

## Scope

- `tests/test_context_compactor.py`
- `tests/test_contract_lint.py`
- `tests/test_loop_closure.py`
- `tests/test_portability.py`
- `tests/test_project_init.py`
- `tests/test_status_dashboard.py`
- `tests/test_vbb_index.py`
- `scripts/vbb-ci-local.sh` (if needed)
- `tools/vbb-loop-closure-check.py` (if needed)
- `docs/runs/2026-06-13_1200_global-evaluation-audit/01_INTAKE.md` (frontmatter fix)
- `docs/runs/2026-06-13_1200_global-evaluation-audit/07_CLOSEOUT.md` (frontmatter fix)

## Out of scope

- Tools source logic (only test structure changes)
- Contract files
- SKILL.md files
- Governance docs (except frontmatter fixes)

## Handoff

→ 04_PLAN: execute fixes