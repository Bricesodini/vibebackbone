---
context_role: test-coverage-audit
phase: transverse
status: active
run_id: "2026-07-27_1712_engineering-knowledge-core-integration"
updated: 2026-07-27
---

# Test coverage — Engineering knowledge governance

## Scope and mode

- **Mode**: DISTRIBUTION
- **Scope**: the Core engineering-knowledge contract, its agent-facing
  propagation and the loop-closure enforcement added by ADR 0049
- **Evidence**:
  `tests/test_engineering_knowledge_governance.py`,
  `tests/test_loop_closure.py`, independent Review Run 02 and the canonical
  P.R2 result

## Critical paths

| Critical path | Visible coverage | Status |
|---|---|---|
| Required maturity lifecycle and supersession principle | Canonical-content regression assertions | COVERED |
| Unique-authority boundary for records, runs, reviews, closeouts and playbooks | Table-row authority assertions | COVERED |
| Mandatory independent review and human promotion decision | Agent-surface assertions plus independent review | COVERED |
| Post-cutover omission of version and harvest | Negative executable fixture | COVERED |
| Valid `OBSERVATION_RECORDED` and `EVIDENCE_LINKED` dispositions | Positive executable fixtures | COVERED |
| Unsupported or mismatched protocol versions | Negative executable fixtures | COVERED |
| Historical-run compatibility | Unit fixture and two real strict-run probes | COVERED |
| FAST-MINIMAL compatibility | Post-cutover executable probe in independent review | COVERED |
| Four-distribution inheritance | Setup and full install/uninstall smoke | COVERED |
| Absence of automated promotion | Closed disposition vocabulary and reviewer inspection | COVERED |

## Priority gaps

No critical safety path is untested. Three bounded edge cases remain useful for
future hardening:

1. Exercise the timestamp cutover independently of the run-name cutover.
2. Exercise the exact cutover boundary, one instant before and at the boundary.
3. Exercise a post-cutover closeout-only `CLOTURE` route without intake.

These gaps do not permit the demonstrated omission bypass and do not block the
current release.

## Recommended tests

1. A pre-cutover run name with post-cutover `started_at` must require v1 fields.
2. Boundary table: `15:12:20Z` remains historical; `15:12:21Z` requires v1.
3. A post-cutover `CLOTURE` artifact accepts v1 plus a valid harvest and rejects
   missing version or harvest.

## Unknowns and evidence limits

- No real multi-month knowledge-record corpus exists yet; usability and
  lifecycle-friction claims remain unmeasured.
- The audit assesses contract safety, not the future quality of human
  promotion decisions.
- File modification time is used only for P0-3 report freshness, not for the
  knowledge-governance cutover.

## Verdict

`READY`

The major failure modes are covered by executable tests, repository probes,
distribution smoke and independent review. Remaining tests are bounded edge
hardening, not missing critical-path safety.
