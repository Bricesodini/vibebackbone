---
audit_id: "impact-analysis-routing-trigger-precedence-20260714-1845"
skill: "t-vbb-impact-analyzer"
status: "READY"
classification: "NON_BREAKING"
date: "2026-07-14"
---

# Impact analysis — Routing trigger precedence

## Change surface

- Ten existing contracts participate in five skill pairs and six duplicate
  triggers; only the secondary owners require trigger replacement.
- `tools/vbb-contract-lint.py` gains a catalog-wide uniqueness invariant.
- `tests/test_contract_lint.py` gains controlled duplicate rejection and
  responsibility-routing cases.

## Propagation

| Surface | Impact | Required action |
|---|---|---|
| Skill contracts | Behavioral metadata | Replace six secondary-owner duplicates with qualified phrases |
| Router | Compatible | No scoring algorithm change |
| Contract lint | Blocking additive rule | Reject case-insensitive exact duplicates |
| Tests | Expanded | Prove zero duplicates and intended owners in strict mode |
| Four distributions | Inherited Core behavior | No adapter change |

## Classification

**NON_BREAKING.** Generic intents gain deterministic ownership. Previously
ambiguous secondary behavior remains reachable through explicit action/stage
phrases, and contract IDs and phase scopes remain stable.

```yaml
FINAL_STATUS:
  verdict: READY
  tests_run:
    - "64-contract duplicate trigger inventory"
    - "router scoring inspection"
  tests_missing: []
  risks:
    - "over-broad qualified phrases could still overlap by substring"
  open_points: []
```
