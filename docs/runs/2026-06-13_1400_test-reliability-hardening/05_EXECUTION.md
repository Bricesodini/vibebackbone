---
phase: "05_EXECUTION"
run_id: "2026-06-13_1400_test-reliability-hardening"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-06-13T14:10:00Z"
ended_at: "2026-06-13T14:45:00Z"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "docs/runs/2026-06-13_1400_test-reliability-hardening/04_PLAN.md"
artifacts_produced:
  - "tests/test_context_compactor.py"
  - "tests/test_contract_lint.py"
  - "tests/test_loop_closure.py"
  - "tests/test_portability.py"
  - "tests/test_project_init.py"
  - "tests/test_status_dashboard.py"
  - "tests/test_vbb_index.py"
  - "tools/vbb-status-dashboard.py"
  - "scripts/vbb-ci-local.sh"
  - "docs/runs/2026-06-13_1200_global-evaluation-audit/01_INTAKE.md"
  - "docs/runs/2026-06-13_1200_global-evaluation-audit/07_CLOSEOUT.md"
  - "docs/runs/2026-06-13_1200_global-evaluation-audit/02_AUDIT.md"
  - "docs/runs/2026-06-13_1200_global-evaluation-audit/03_DECISION.md"
---

# 05_PATCH_SUMMARY — RUN 20A: Test Reliability Hardening

## Files changed

| File | Change |
|------|--------|
| `tests/test_context_compactor.py` | Rewritten: custom `test(name,fn)` → pytest `test_*` functions + `__main__` fallback |
| `tests/test_contract_lint.py` | Rewritten: same pattern |
| `tests/test_loop_closure.py` | Rewritten: same pattern |
| `tests/test_portability.py` | Rewritten: same pattern |
| `tests/test_project_init.py` | Rewritten: same pattern |
| `tests/test_status_dashboard.py` | Rewritten: same pattern |
| `tests/test_vbb_index.py` | Rewritten: same pattern |
| `tools/vbb-status-dashboard.py` | `extract_next_action()`: added EN match (`- **Next action**`) alongside FR (`- **prochaine action**`) |
| `scripts/vbb-ci-local.sh` | Added pytest step (7/7), renumbered 4–6 to 4/7–6/7, documented WARN on step 3 |
| `docs/runs/.../01_INTAKE.md` | Fixed frontmatter: added voie, required fields per loop-closure spec |
| `docs/runs/.../07_CLOSEOUT.md` | Fixed frontmatter: added voie, agent, started_at, ended_at, artifacts_produced |
| `docs/runs/.../02_AUDIT.md` | Added (required for AUDIT voie) |
| `docs/runs/.../03_DECISION.md` | Added (required for AUDIT voie) |

## Diff summary

### Root cause: pytest fixture collision

All 7 test files defined a local `test(name: str, fn)` function as a lightweight
test runner. Pytest collects this function by name and interprets `name` as a
fixture request → 7/7 `ERROR at setup of test — fixture 'name' not found`.

### Fix: rename and restructure

- Removed the `test(name, fn)` wrapper function
- Renamed all `_test_*` helper functions to `test_*` for pytest auto-discovery
- Added `if __name__ == "__main__"` block with: `import pytest` → `pytest.main([__file__, "-q"])` 
  plus a manual fallback loop for environments without pytest
- Test logic identical — only structural changes

### Secondary fixes

- Dashboard `extract_next_action` now matches both FR and EN field names (post language harmonization)
- Global evaluation audit run frontmatter fixed to pass loop-closure check
- Added 02_AUDIT.md and 03_DECISION.md to satisfy AUDIT voie requirements

## Verification

```
pytest tests/ -q           → 69 passed, 0 failed
python3 tests/test_*.py    → all pass (69/69 total)
scripts/vbb-ci-local.sh    → PASS (6 passed, 0 failed, 1 WARN on in-progress run)
```