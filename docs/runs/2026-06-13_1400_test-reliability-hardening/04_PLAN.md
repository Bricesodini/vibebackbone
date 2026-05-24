---
phase: "04_PLAN"
run_id: "2026-06-13_1400_test-reliability-hardening"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-06-13T14:05:00Z"
ended_at: "2026-06-13T14:10:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "docs/runs/2026-06-13_1400_test-reliability-hardening/01_INTAKE.md"
artifacts_produced:
  - "docs/runs/2026-06-13_1400_test-reliability-hardening/04_PLAN.md"
---

# 04_PLAN — RUN 20A: Test Reliability Hardening

## RUN 01 (only run)

### Scope
- Fix 7 test files for pytest compatibility
- Fix loop closure frontmatter on global-evaluation-audit run
- Fix dashboard `extract_next_action` to support EN field names
- Update CI script with step numbering and documented WARN behavior

### Steps
1. Rewrite test runner pattern: remove `test(name, fn)` custom runner, rename `_test_*` → `test_*` functions
2. Fix frontmatter on `2026-06-13_1200_global-evaluation-audit` run (add voie, required fields, add 02_AUDIT + 03_DECISION artifacts)
3. Update `vbb-status-dashboard.py` `extract_next_action` to match both FR and EN field names
4. Add pytest step to CI script, update numbering, document WARN behavior
5. Add `if __name__ == "__main__"` block with pytest import + manual fallback for direct execution
6. Verify: `pytest tests/ -q` = all green, `python3 tests/test_X.py` = all green, `scripts/vbb-ci-local.sh` = PASS

### Tests
- `pytest tests/ -q` → 69 passed, 0 failed
- `python3 tests/test_loop_closure.py` → 14 passed
- `python3 tests/test_portability.py` → 6 passed
- `python3 tests/test_project_init.py` → 10 passed
- `python3 tests/test_contract_lint.py` → 15 passed
- `python3 tests/test_context_compactor.py` → 9 passed
- `python3 tests/test_status_dashboard.py` → 8 passed
- `python3 tests/test_vbb_index.py` → 7 passed
- `scripts/vbb-ci-local.sh` → PASS (6 passed, 0 failed, 1 WARN on in-progress run)