# 05_PATCH_SUMMARY_RUN_03 — Non-omissible cutover remediation

**Date**: 2026-07-27
**Run**: 03 / 03
**Based on**: `06_REVIEW_RUN_01.md`

## Run objective

Remove the opt-in bypass identified by independent review while preserving
historical runs and existing FAST-MINIMAL semantics.

## Modified files

| File | Change |
|---|---|
| `tools/vbb-loop-closure-check.py` | Objective cutover derived from run identity or `started_at` |
| `tests/test_loop_closure.py` | Cutover omission, dispositions and version regression cases |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | Non-retroactive compatibility contract made explicit |
| `04_PLAN.md` | Corrected self-reference |
| `INTEGRATION_GATE.md` | Corrected plan reference |

## Enforcement behavior

- The v1 contract applies to runs at or after `2026-07-27_1712`, or started at
  or after `2026-07-27T15:12:21Z`, when they use intake or closeout artifacts.
- Omitting both the protocol version and harvest disposition no longer bypasses
  the gate.
- Earlier runs remain valid without retroactive edits.
- FAST-MINIMAL remains governed by its activity-log and patch-summary contract.
- Declared versions must be supported and consistent between intake and
  closeout.

## Regression evidence

The targeted suite passes 34 tests, including:

- a post-cutover run omitting governance fields fails;
- `OBSERVATION_RECORDED` passes;
- `EVIDENCE_LINKED` passes;
- intake/closeout mismatch fails;
- an unsupported version fails;
- historical pre-cutover runs remain valid.

## Remaining gate

Independent Review Run 02 must confirm this remediation before closeout.
