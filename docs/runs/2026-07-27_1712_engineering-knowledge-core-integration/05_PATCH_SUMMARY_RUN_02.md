# 05_PATCH_SUMMARY_RUN_02 — Enforcement and regression

**Date**: 2026-07-27
**Run**: 02 / 02
**Based on**: `04_PLAN.md`

## Run objective

Enforce the Knowledge Harvest contract for governance-v1 runs while preserving
all historical runs, then verify Core propagation.

## Modified files

| File | Action | Change |
|---|---|---|
| `tools/vbb-loop-closure-check.py` | MODIFIED | Version-aware harvest validation |
| `tests/test_loop_closure.py` | MODIFIED | Historical, valid, missing and invalid harvest fixtures |
| `tests/test_engineering_knowledge_governance.py` | CREATED | Cross-surface governance invariants |
| `docs/templates/07_CLOSEOUT.md.template` | MODIFIED | Version and disposition contract |
| `docs/RELATIONS.md` | GENERATED | Projection of the 10 architecture blocks |

## Enforcement behavior

- Runs without `knowledge_governance_version` remain valid.
- Version `1.0` requires the same version in intake and closeout.
- `knowledge_harvest` accepts only `NONE`, `OBSERVATION_RECORDED` or
  `EVIDENCE_LINKED`.
- Missing, invalid or unsupported values fail loop closure.
- Automation validates structure; it does not promote knowledge.

## Tests

| Test | Result | Notes |
|---|---|---|
| Targeted knowledge + loop tests | PASSED | 29 passed |
| Full pytest | PASSED | 240 passed, 1 skipped |
| Architecture graph generation | PASSED | `docs/RELATIONS.md` regenerated |
| Architecture lint | PASSED | 10 blocks |
| Contract lint | PASSED | 0 errors |
| Distribution setup smoke | PASSED | Pi, OpenCode, Codex, Claude routed |
| Full install/uninstall smoke | PASSED | all four distributions |
| Ruff format | PASSED after mechanical format | 2 files normalized |

## Initial validation failure and correction

The first targeted run exposed that closeout-only and minimal historical routes
were treated as missing intake files. The validator was corrected to treat
absent intake as legacy unless a governance version is declared. One prompt
assertion was clarified. The targeted suite then passed 29/29.

The first local CI run failed only Ruff format on the two new Python files and
warned that the active run lacked its final phase artifacts. Ruff was applied;
phase artifacts were normalized to `04_PLAN.md` and `05_EXECUTION.md`.

## Divergences from the plan

No semantic divergence. The version marker replaced a date-based cutover,
providing a more explicit and portable compatibility boundary.

## Unresolved points

| Point | Blocking? | Description |
|---|---|---|
| Independent integration review | Yes | Must occur in a distinct session |
| Final local CI after closeout artifact | Yes | Re-run once harvest is present |

## Handoff

**Next phase**: independent `06_REVIEW_RUN_01`.
**Points requiring attention**: opt-in compatibility boundary, route coverage,
single authority, no phase 08 and distribution inheritance.
