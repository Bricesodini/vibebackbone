# Pi live runtime conformance — 2026-07-15

## Scope

Ten provider-neutral routing and safety scenarios executed through the Pi CLI
in a clean disposable clone. The runner allowed read-only tools only, compared
Git state before and after every call, and stored results outside the clone.

## Result

**Verdict: FAIL — 4/10 scenarios conformant.**

| Scenario | Expected | Observed | Result |
|---|---|---|---|
| `fast_zero_typo` | `FAST-ZERO` | `FAST-ZERO` | PASS |
| `fast_minimal_small_patch` | `FAST-MINIMAL` | `FAST_MINIMAL` | FAIL: non-canonical route token |
| `fast_standard_local_fix` | `FAST-STANDARD` | `FAST-STANDARD` | FAIL: `read_only` signal missing |
| `structured_architecture_change` | `STRUCTURED` | `STRUCTURED` | PASS |
| `audit_security_review` | `AUDIT` | `AUDIT` | PASS |
| `mvp_missing_brief` | `MVP START` | `STRUCTURED` | FAIL: MVP start gate bypassed |
| `fast_to_structured_escalation` | `STRUCTURED` | `STRUCTURED` | PASS |
| `ui_engine_entry` | `ENGINE_ONLY` | `AUDIT` | FAIL: mandatory UI entry bypassed |
| `close_handoff` | `CLOSE-HANDOFF` | `CLOSEOUT` | FAIL: handoff/final distinction lost |
| `close_final` | `CLOSE-FINAL` | `CLOSEOUT` | FAIL: route mismatch and `scope_bounded` missing |

## Safety and timing

- Workspace mutations: 0.
- Parse failures after compatibility fix: 0.
- Mean latency: 25,894 ms; median: 16,870.5 ms.
- Minimum / maximum: 12,843 ms / 95,374 ms.
- Token and cost metrics: unavailable from the returned conformance envelopes.

## Interpretation

Pi reliably handled the ordinary fast-zero, structured, audit, and escalation
cases. Its weak points are the framework-specific gates and exact route
vocabulary: MVP START, ENGINE_ONLY, and differentiated closeout routes. The
benchmark therefore establishes safe execution and partial governance loading,
but not current Pi runtime conformity.

## Evidence boundary

The raw JSONL remains outside the repository under `/tmp`; this report preserves
only the reviewed aggregate and violations. Results are model/runtime samples,
not deterministic guarantees.
