---
run_id: "2026-07-29_1941_run1-exact-release-measurement"
phase: "POC"
voie: "STRUCTUREE"
status: "CONCLUDED"
agent: "codex"
started_at: "2026-07-29T19:50:00+02:00"
ended_at: "2026-07-29T19:57:00+02:00"
artifacts_produced:
  - "POC.md"
---

# POC — Exact and honest release measurement

**Status**: CONCLUDED
**Date**: 2026-07-29
**Liée à ADR**: `docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md`
**Liée à RUN**: `docs/runs/2026-07-29_1941_run1-exact-release-measurement/`

## Hypothesis

We assume `RR-BK-02` and `RR-BK-03` can be closed without a new governance
concept by extending the accepted shared-resolution contract to an explicit
run argument plus the existing `certification.bound_to.commit`, and by matching
the canonical qualified description header in the active-risk table.

## Test (concrete and executable)

The POC used only temporary directories and the unmodified baseline:

```bash
python - <<'PY'
# 1. Create target and future closed runs.
# 2. Observe latest_closed_run selecting the future run.
# 3. Prototype exact-child resolution for bare ID and absolute path.
# 4. Require certification.bound_to.run_id and commit to equal the declared
#    run and expected SHA.
# 5. Create clean synchronized Git fixtures containing the exact canonical
#    active-risk table for P0, P1 and P2.
# 6. Compare get_open_risks() with measure_repository_health() after the same
#    risk is made visible.
PY

python tools/vbb-loop-closure-check.py \
  2026-07-29_0840_audit-remediation --strict

python tools/vbb-loop-closure-check.py \
  docs/runs/2026-07-29_0840_audit-remediation --strict

python tools/vbb-adversarial-gate.py \
  2026-07-29_0840_audit-remediation \
  --expected-commit 6b0daf4785d652b23931b80aafba57979e69d9b4 \
  --strict
```

The full executed script is preserved in the session command transcript; it
created no repository file.

## Success criterion

`GO` if all four statements are observed:

1. implicit latest selection can choose the wrong future run;
2. one canonical explicit resolver makes bare ID and exact path identify the
   same run and rejects a wrong SHA;
3. the current parser misses the exact canonical risk header;
4. the existing health logic already prevents `READY` once P0/P1/P2 risks are
   visible.

## Observed result

- **Execution date**: 2026-07-29 19:57 +02:00
- **Literal key output**:

```text
CURRENT_LATEST_SELECTED=2026-07-30_0700_future
PROTOTYPE_EXPLICIT raw=2026-07-29_1200_target sha=a*40 ok=True subject=2026-07-29_1200_target
PROTOTYPE_EXPLICIT raw=<absolute-target-path> sha=a*40 ok=True subject=2026-07-29_1200_target
PROTOTYPE_EXPLICIT raw=2026-07-29_1200_target sha=b*40 ok=False subject=2026-07-29_1200_target
CURRENT_RISK_PARSE severity=P0 count=0
PROTOTYPE_MEASURE severity=P0 verdict=BLOCKED
CURRENT_RISK_PARSE severity=P1 count=0
PROTOTYPE_MEASURE severity=P1 verdict=PARTIAL
CURRENT_RISK_PARSE severity=P2 count=0
PROTOTYPE_MEASURE severity=P2 verdict=PARTIAL
CURRENT_LOOP_ID_RC=0
CURRENT_LOOP_PATH_RC=2
CURRENT_ADVERSARIAL_EXPECTED_COMMIT_RC=2
vbb-adversarial-gate: error: unrecognized arguments: --expected-commit
```

- **Measured metric**: 4/4 statements observed (threshold: 4/4).

## Necessary implementation demonstrated by the POC

1. Add one exact-child resolver to `tools/vbb_run_resolution.py`; use it in
   loop-closure and the adversarial gate. `F9` is therefore necessary only for
   this normalization, because ID and path currently produce different
   subjects/results.
2. Add an optional explicit expected-commit assertion to both release-relevant
   gates. It must require an explicit run, reject `--latest`, and compare
   against the existing canonical `certification.bound_to` record.
3. Remove implicit latest-run authority from CI gate evidence. Validate explicit
   changed runs in remote CI, and require explicit run/SHA inputs for
   release-bound local verification.
4. Recognize a description header whose canonical name starts with
   `Description`, while still requiring ID, severity and status columns.
5. Add negative tests before implementation for future selection, wrong SHA,
   missing binding, outside path, canonical P0/P1/P2 tables and prose
   `READY` override.

No version, release document, tag, historical run or deferred item is needed.

## Decision

- **Verdict**: GO
- **Justification**: the prototype satisfies 4/4 measurable statements and
  bounds the patch to the existing ADR 0027, ADR 0046 and ADR 0051 contracts.

## Bilan

The hypothesis is validated. Implementation may proceed only after the
Integration Gate explicitly returns `can_code_start=true`.

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: GO
adr_link: "docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md"
hypothesis_validated: true
metric_observed: "4/4"
metric_threshold: "4/4"
reproducible: true
verified_at: "2026-07-29T17:57:00Z"
verified_by: "codex"
```

## A2 remediation POC

The three counter-review bypasses were converted into executable locks and
replayed against the functional checkpoint before changing implementation:

```text
RUN1-A2-CR-01 FAIL-BEFORE: GitHub workflow omits --expected-commit "$VBB_HEAD_SHA"
RUN1-A2-CR-02 FAIL-BEFORE: verify_certification_subject is absent while historical binding accepts the old valid commit
RUN1-A2-CR-03 FAIL-BEFORE: P0 REOPENED is absent from active risks and cannot block READY
```

Command:

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_pre_merge_gate_5b.py::test_remote_release_binding_carries_checked_out_sha_to_both_gates \
  tests/test_run_resolution.py::test_certification_rejects_historical_commit_when_head_differs \
  tests/test_status_dashboard.py::test_reopened_p0_is_active_and_forces_blocked
```

Observed: `3 failed`. Verdict: `GO`; each finding has a direct negative oracle
and no implementation outside the existing release-measurement surface is
required.
