# Test coverage — runtime conformance benchmark

## Scope

`tools/vbb_runtime_conformance.py`, the shared scenario/schema/adapter manifests,
and their deterministic CI integration.

## Critical paths and visible coverage

| Critical path | Coverage |
|---|---|
| Canonical four-provider and ten-scenario manifest | Covered by manifest validation and 40-result matrix test |
| Route, signal, mutation, and FINAL_STATUS enforcement | Covered by parameterized negative tests |
| Missing and duplicate results | Covered |
| JSON wrapper and JSONL extraction | Covered |
| Safe provider command defaults | Covered for all four adapters |
| Accidental live workspace mutation | Covered with a real temporary Git repository |
| Live execution consent | Covered; `--confirm-live` is mandatory |
| CI parity | Covered by static assertions for local and GitHub workflows |
| Token, latency, and cost aggregation | Covered by the deterministic matrix contract; unavailable metrics remain null |

## Priority gaps

1. Record one real read-only result per provider to characterize current CLI
   event wrappers and authentication behavior.
2. Repeat one scenario three times per provider to measure model variance.
3. Add a promoted golden baseline only after human review of live outputs.

These gaps concern optional live evidence, not deterministic evaluator safety.

## Verdict

`PARTIAL` — deterministic critical paths are covered and release-safe; actual
provider/model behavior remains intentionally unexecuted because live calls
consume credentials or credits and were not authorized as part of CI.

## Unknowns

- Whether every provider exposes token and cost metrics in its current event schema.
- Whether OpenCode creates provider session state inside a disposable workspace.
- Cross-model variance until repeated live samples exist.
