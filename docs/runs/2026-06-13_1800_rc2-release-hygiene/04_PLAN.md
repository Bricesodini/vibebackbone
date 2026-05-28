---
phase: "04_PLAN"
run_id: "2026-06-13_1800_rc2-release-hygiene"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-06-13T18:05:00Z"
ended_at: "2026-06-13T18:15:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "docs/runs/2026-06-13_1800_rc2-release-hygiene/01_INTAKE.md"
artifacts_produced:
  - "docs/runs/2026-06-13_1800_rc2-release-hygiene/04_PLAN.md"
---

# 04_PLAN — RUN 21: RC2 Release Hygiene Fixes

## Plan

1. Fix F-01 by adding pytest to `requirements.txt`, adding an explicit local CI dependency preflight, and documenting `python3 -m pip install -r requirements.txt`.
2. Fix F-02 by replacing obsolete 57/58 skill references in public docs with 62 skills / 62 contracts where relevant.
3. Fix F-03 by updating `RELEASE_CHECKLIST.md` for RC2, clean-checkout dependency bootstrap, and reproduced checks.
4. Fix F-04 by documenting that the stale local `v1.0.0` tag must be deleted/recreated before stable, without pushing any stable tag.
5. Fix F-05 by untracking bytecode files and ignoring `__pycache__/` plus `*.py[cod]`.
6. Add GitHub CI parity by running `pytest tests/ -q` in the workflow.
7. Update `docs/CONTEXT.md`, `docs/AUDIT_STATUS.md`, and RUN 21 artifacts.
8. Run the required verification command sequence and report RC2 readiness.

## Exit criteria

- Required verification commands pass after dependency bootstrap.
- `git ls-files '*__pycache__*' '*.pyc'` returns no tracked files.
- Stable `v1.0.0` is not tagged or pushed by this run.
- `v1.0.0-rc.2` is ready to tag and push for external review.
