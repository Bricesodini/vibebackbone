---
run_id: "2026-07-29_1941_run1-exact-release-measurement"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-29T19:59:00+02:00"
ended_at: "2026-07-29T20:12:00+02:00"
next_phase: "06_REVIEW"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "POC.md"
  - "INTEGRATION_GATE.md"
  - "04_PLAN.md"
artifacts_produced:
  - "05_EXECUTION.md"
  - "05_PATCH_SUMMARY_RUN_01.md"
---

# 05_EXECUTION — Run 1 exact release measurement

## Authorization used

Implementation started only after:

- POC verdict `GO`, 4/4;
- ADR 0027 observed `ACCEPTED`;
- Integration Gate `PASS`;
- `can_code_start=true`;
- explicit `implementation_authorization.status=AUTHORIZED`.

## Changes implemented

1. `tools/vbb_run_resolution.py` now resolves a bare run ID and its exact path
   to one canonical child of `docs/runs`, rejecting outside or ambiguous
   fallback paths.
2. The same module verifies the existing
   `adversarial.certification.bound_to.{run_id,commit}` contract against an
   expected full Git SHA.
3. The adversarial and loop-closure gates accept `--expected-commit`, require an
   explicit run in that mode and fail on missing/mismatched binding.
4. Loop closure normalizes ID/path forms before checking, which includes only
   the necessary part of F9.
5. The dashboard recognizes the exact canonical
   `Description and reopen trigger` active-risk header.
6. Local CI no longer uses implicit latest-run authority. Exact local release
   evidence requires `VBB_RUN_ID` and `VBB_EXPECTED_COMMIT` together.
7. Remote CI validates changed run closeouts explicitly instead of selecting a
   future or unrelated latest run.
8. The canonical pre-merge reference documents the exact run/SHA invocation.
9. Core-to-distribution placement and unchanged adapters are recorded in
   `docs/DISTRIBUTIONS.md`.

No product/framework version, changelog, release checklist, tag, historical
run or release candidate was modified. Three scoped regression cases were
added to the adversarial corpus only after the A2 attack task confirmed the
corresponding bypasses, as required by the corpus contract.

## Fails-before evidence

Before implementation, the focused suite produced 10 expected failures:

- three missing shared-resolution/binding functions;
- canonical active-risk table parsed as empty;
- adversarial expected-commit CLI absent;
- loop-closure path/ID divergence;
- loop-closure expected-commit CLI absent.

POC literal evidence is in `POC.md`.

## Passes-after evidence

```text
Focused Run 1 suite: 107 passed
Adversarial corpus and corpus contract: 18 passed
Explicit negative-proof selection: 14 passed
Full pytest: 444 passed, 1 skipped
Ruff check: PASS
Ruff format: PASS
Mypy: PASS, 18 source files
Architecture lint: PASS, 0 errors, 0 warnings, 11 blocks
Architecture graph: generated, no tracked diff
Contract lint: PASS, 0 errors, 1 pre-existing non-blocking F12 warning
Local CI: PASS, 14 passed, 0 failed, 0 warnings
Setup structural smoke: PASS=32, FAIL=0, WARN=0
Four-provider install smoke: PASS
Distribution propagation tests: 6 passed
```

The local CI count is 14 because the two run gates correctly report `SKIP`
when no exact run/SHA pair is declared. Their positive and negative exact-mode
behavior is covered by focused tests. A release claim must run with both
variables and cannot treat this generic CI invocation as release evidence.

## Negative-proof results

| Proof | Result | Evidence |
|---|---|---|
| future `--latest` cannot be exact release evidence | PASS | expected-commit rejects implicit latest; CI contains no `--latest` |
| wrong SHA | PASS | both gates return non-zero |
| missing binding | PASS | shared binding verifier fails closed |
| wrong bound run ID | PASS | shared binding verifier fails closed |
| bare ID/path divergence | PASS | both normalize to one run |
| outside or ambiguous fallback path | PASS | shared resolver returns no subject |
| canonical active P0 | PASS | parsed; measured `BLOCKED` |
| canonical active P1 | PASS | parsed; measured `PARTIAL` |
| canonical active P2 | PASS | parsed; measured `PARTIAL` |
| prose `READY` overrides risk | PASS | effective verdict remains measured result |
| half-declared local subject | PASS | local CI exits 1 |
| workflow subject selection | PASS | only changed explicit closeouts are gated |
| qualified Description header variants | PASS | open P0 remains parsed and blocks READY |
| invented but well-formed full SHA | PASS | rejected because the Git commit object does not exist |
| external directory with matching run name | PASS | rejected outside the declared canonical runs directory |

## Scope control

- `RR-BK-02`: implemented and mechanically covered.
- `RR-BK-03`: implemented and mechanically covered.
- `F9`: only exact-child ID/path normalization was implemented.
- no other finding was opened or remediated.

## Remaining execution condition

The technical counter-proofs pass, but the available review actor disclosed
the same Codex/GPT-5/OpenAI identity as the implementer. The required distinct
A2 witness is therefore unavailable and the implementation is not
commit-ready.
