# Technical debt — mypy baseline

## Repository inventory

**Date**: 2026-07-14 14:55 Europe/Paris
**Scope**: `mypy-baseline` — nine tools reported by `mypy tools`
**Mode**: DISTRIBUTION interpreted as DEV
**Verdict**: `READY`

The canonical checker reports 20 errors: 10 missing container annotations, two
credential-loop shadowing errors, one dashboard return annotation mismatch, one
index generator inference error, two contract-runtime output-shape errors and
four optional dynamic-import dereferences.

## Canonical vs legacy mapping

ADR 0035 and `pyproject.toml` are canonical. No legacy mypy config, secondary
checker or parallel type surface exists. The errors arise from implicit Python
container inference, not from competing implementations.

## Legacy assessment

No legacy type layer was found. `Dict`/`List` aliases remain the repository's
current annotation style and should be used consistently in this bounded run;
migrating the whole repository to built-in generics is out of scope.

## Technical debt assessment

### TD-201 — Heterogeneous dictionaries inferred too narrowly

- **scope**: `mypy-baseline`
- **Severity**: P1
- **Confidence**: high
- **Evidence**: contract runtime and index report incompatible `None`, dict and
  generator item types after initial literal inference.
- **Why this matters**: later valid mutations are treated as contradictions,
  obscuring the actual runtime shape.
- **Recommended action**: annotate boundary dictionaries/lists as
  `Dict[str, Any]` or `List[Dict[str, Any]]` where the contract is deliberately
  heterogeneous; do not add ignores.

### TD-202 — Dynamic import specification is dereferenced while optional

- **scope**: `mypy-baseline`
- **Severity**: P1
- **Confidence**: high
- **Evidence**: four errors at contract-runtime router loading because
  `spec_from_file_location` and `loader` are optional by API contract.
- **Why this matters**: a missing/broken local module would currently fail with
  an indirect attribute error.
- **Recommended action**: assert or explicitly reject missing spec/loader before
  module construction, matching the executor and loop-closure pattern.

### TD-203 — Empty containers lack declared element types

- **scope**: `mypy-baseline`
- **Severity**: P2
- **Confidence**: high
- **Evidence**: ten `var-annotated` errors in lint, compactor, architecture,
  multiservice lint, index and runtime.
- **Why this matters**: container contracts depend on later mutation order.
- **Recommended action**: add the narrowest evidence-backed list/set/dict type.

### TD-204 — Credential report loops reuse one variable for two dataclasses

- **scope**: `mypy-baseline`
- **Severity**: P2
- **Confidence**: high
- **Evidence**: `item` iterates `AllowedExample` then `Finding`, causing two
  assignment/attribute errors.
- **Why this matters**: human readers and type inference lose the distinction
  between allow evidence and blocking findings.
- **Recommended action**: use `example` and `finding`; preserve output exactly.

### TD-205 — Contract coverage percentage annotation is stale

- **scope**: `mypy-baseline`
- **Severity**: P2
- **Confidence**: high
- **Evidence**: `count_contracts` declares three integers but returns a rounded
  float ratio for non-empty repositories.
- **Why this matters**: the public helper contract contradicts runtime truth.
- **Recommended action**: correct the return annotation to `Tuple[int, int,
  float]`; do not alter the calculated value.

## Architecture assessment

The findings remain inside the existing Contract Tooling block. No boundary,
dependency direction or distribution adapter changes. TD-202 improves explicit
failure at an existing dynamic-loader boundary without redesign.

## Database assessment

Not applicable: no database, schema, migration or persisted-data surface exists
in this scope.

## Test & operations assessment

Direct suites cover contract lint/runtime, credentials, compactor,
architecture, dashboard and index. Multiservice lint has less direct coverage,
but its change is an empty-list annotation only. P.R2 and all-contract dry-run
remain mandatory. No operational service or production state is involved.

## Priority roadmap

### Immediate

1. Type dynamic import and heterogeneous contract-runtime structures.
2. Type/rename credentials and remaining containers.
3. Run mypy zero plus focused tests.

### Next

Promote Ruff check/format/mypy to local and GitHub CI in a separate run after
this baseline reaches zero.

### Later

Consider TypedDict/dataclasses only if these internal dictionaries become a
published or repeatedly changing interface; do not abstract prematurely.

## After this skill runs

Proceed to a separate STRUCTURED remediation run linked to ADR 0035. This audit
is read-only and does not modify Python.

```yaml
FINAL_STATUS:
  elapsed_seconds: 80
  budget_initial: 180
  progress_emitted: false
  progress_count: 0
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/audits/tech-debt-mypy-baseline-20260714-1455.md
    - docs/AUDIT_STATUS.md
  tests_run:
    - mypy tools --no-error-summary
  tests_missing:
    - remediation verification
  risks:
    - QOA-007
  open_points:
    - 20 mypy errors remain until remediation
```
