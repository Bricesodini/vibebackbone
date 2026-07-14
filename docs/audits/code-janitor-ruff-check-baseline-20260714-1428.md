# Code Janitor — Ruff check baseline

## Context

**Date**: 2026-07-14 14:28 Europe/Paris
**Scope**: `ruff-check-baseline` — `tools/**/*.py`, `tests/**/*.py`
**Mode**: DISTRIBUTION interpreted as DEV
**Source**: ADR 0035 and `ruff check tools tests --output-format concise`

This read-only pass applies the scoped-audit protocol. It evaluates only the 37
Ruff findings selected by the canonical `E4/E7/E9/F` rules. Formatting and type
errors are outside this pass.

## Verdict

`PARTIAL` — all 37 findings are bounded and removable without redesign, but the
baseline is not READY until the four cleanup classes pass targeted review and
the global test suite. No structural signal was found.

## Findings (prioritized)

### JAN-01 — Unused imports and assignments

- **scope**: `ruff-check-baseline`
- **Severity**: P1
- **Type**: `dead-code`
- **Evidence**: 6 `F401` imports and 8 `F841` assignments across tools/tests.
- **Risk**: false dependencies and review noise; test setup assignments require
  manual preservation of their side-effecting calls.
- **Effort**: S
- **Recommended action**: remove imports; replace unused test variables with
  direct calls rather than deleting fixture creation.

### JAN-02 — Placeholder-free f-strings

- **scope**: `ruff-check-baseline`
- **Severity**: P2
- **Type**: `debug-leftovers`
- **Evidence**: 19 `F541` findings in runtime output construction.
- **Risk**: style noise only; changing string contents would be behavioral.
- **Effort**: S
- **Recommended action**: remove only the `f` prefix and assert tests preserve
  output contracts.

### JAN-03 — Ambiguous local name `l`

- **scope**: `ruff-check-baseline`
- **Severity**: P2
- **Type**: `naming`
- **Evidence**: 3 `E741` findings in review-tier comprehensions.
- **Risk**: poor readability; careless renaming could mismatch tuple meaning.
- **Effort**: S
- **Recommended action**: rename to `label` consistently inside the bounded
  comprehensions and run review-tier/dashboard tests.

### JAN-04 — Dynamic loader import placement

- **scope**: `ruff-check-baseline`
- **Severity**: P2
- **Type**: `structure`
- **Evidence**: one `E402` on the deliberately delayed `importlib.util` import
  in `vbb-loop-closure-check.py`; surrounding imports are already top-level.
- **Risk**: leaving the exception undocumented creates permanent lint debt;
  moving this standard-library import has no intended initialization effect.
- **Effort**: S
- **Recommended action**: move `importlib.util` into the standard-library import
  group and preserve the dynamic module-loading sequence unchanged.

## Quick wins (≤ 60 minutes total)

1. Apply Ruff safe fixes for unused imports and f-string prefixes, then review.
2. Convert unused fixture assignments to direct calls.
3. Rename the three ambiguous locals manually.
4. Move the standard-library import and run focused plus global tests.

## Consolidation plan (max 7 steps)

1. Capture the 37-finding baseline.
2. Pass ADR 0035 POC/Integration Gate for the cleanup run.
3. Apply safe Ruff fixes without unsafe fixes.
4. Review every deletion and string diff.
5. Correct the 12 remaining assignments/names/import placement manually.
6. Run focused tests, Ruff zero, P.R2 and local CI.
7. Keep QOA-007 MITIGATING until format, mypy and CI promotion also pass.

## Structural gaps detected

None in scope. The findings are local, mechanical and already governed by ADR
0035; `1-vbb-tech-debt` is not required.

## Unknowns / needs confirmation

- No external consumer inventory can prove that private textual diagnostics are
  parsed; existing tests and full P.R2 are the available compatibility evidence.
- Ruff reports 25 safe autofixes and 8 optional unsafe fixes; unsafe fixes are
  explicitly excluded from the remediation.

## After this skill runs

Proceed to a separate STRUCTURED remediation run linked to ADR 0035. The report
itself performs no code modification.

```yaml
FINAL_STATUS:
  elapsed_seconds: 75
  budget_initial: 180
  progress_emitted: false
  progress_count: 0
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/audits/code-janitor-ruff-check-baseline-20260714-1428.md
    - docs/AUDIT_STATUS.md
  tests_run:
    - ruff check tools tests --output-format concise
  tests_missing:
    - remediation verification
  risks:
    - QOA-007
  open_points:
    - 37 Ruff findings remain until the remediation run
```
