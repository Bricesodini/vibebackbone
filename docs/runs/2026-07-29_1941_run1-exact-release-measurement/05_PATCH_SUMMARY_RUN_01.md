---
run_id: "2026-07-29_1941_run1-exact-release-measurement"
phase: "05_PATCH_SUMMARY"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-29T20:10:00+02:00"
ended_at: "2026-07-29T20:12:00+02:00"
next_phase: "06_REVIEW"
artifacts_consumed:
  - "05_EXECUTION.md"
artifacts_produced:
  - "05_PATCH_SUMMARY_RUN_01.md"
---

# 05_PATCH_SUMMARY_RUN_01

## Functional change set

- exact run/path normalization and expected-SHA binding;
- explicit release-gate interfaces;
- removal of implicit latest-run authority from local/remote CI evidence;
- exact canonical active-risk extraction;
- negative and non-regression tests;
- bounded Core/distribution decision record.

## Files modified

### Core implementation

- `tools/vbb_run_resolution.py`
- `tools/vbb-adversarial-gate.py`
- `tools/vbb-loop-closure-check.py`
- `tools/vbb-status-dashboard.py`

### Gate carriers and documentation

- `scripts/vbb-ci-local.sh`
- `.github/workflows/vbb-contracts.yml`
- `docs/REFERENCE/pre-merge-gate.md`
- `docs/DISTRIBUTIONS.md`

### Tests

- `tests/test_run_resolution.py`
- `tests/test_adversarial_gate_yaml_unwrap.py`
- `tests/test_loop_closure.py`
- `tests/test_status_dashboard.py`
- `tests/test_pre_merge_gate_5b.py`

### Run artifacts

- `01_INTAKE.md`
- `02_AUDIT.md`
- `POC.md`
- `INTEGRATION_GATE.md`
- `04_PLAN.md`
- `05_EXECUTION.md`
- `05_PATCH_SUMMARY_RUN_01.md`

## Unresolved point

Distinct A2 falsification and final closeout are pending. No commit is
authorized before they pass.
