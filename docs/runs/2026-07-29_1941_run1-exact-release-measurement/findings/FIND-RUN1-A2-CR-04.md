---
finding_id: "RUN1-A2-CR-04"
severity: "S0"
state: "REMEDIATED"
scope: "RR-BK-02/RR-BK-03"
---

# RUN1-A2-CR-04 — empty expected commit disabled loop certification

## Observation

`vbb-loop-closure-check.py` previously guarded certification with a truthiness
test. Passing `--expected-commit ""` therefore skipped subject verification and
could return `exit_intent: PASS` with code 0.

## Required invariant

- `expected_commit is None`: option absent; historical/non-certifying behavior
  remains available under the existing contract.
- `expected_commit == ""` (or whitespace): explicitly supplied invalid input;
  fail closed with `invalid_or_empty_expected_commit`.
- a non-empty value: validate full SHA format, Git object existence, bound
  metadata, and (in certification mode) equality with `HEAD`.

## Remediation

The shared run-resolution authority now validates explicitly supplied SHAs.
Both `vbb-loop-closure-check.py` and `vbb-adversarial-gate.py` invoke that
validation before selecting or certifying a run. The exact empty-string attack
and close variants are covered by regression tests.

## Status

Technical remediation is complete on the new checkpoint. Certification remains
`PENDING_A2`; the previous checkpoint `7ccbb6202219b2ec151b77ac57f3d68134d2cadd`
is `REJECTED_BY_A2` and is not retargeted or deleted.
