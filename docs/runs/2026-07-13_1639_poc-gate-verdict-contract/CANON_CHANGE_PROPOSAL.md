---
run_id: "2026-07-13_1639_poc-gate-verdict-contract"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-13T16:48:00+02:00"
human_validated_by: "Brice Sodini — GO on READY plan, 2026-07-13"
---

# Canon Change Proposal — Align POC verdict enforcement

## Current Canon

The documented contract says only a POC verdict `GO` may unlock implementation.
`NO-GO` and `PIVOT` are distinct outcomes.

## Problem

The parser rejects the bold verdict syntax emitted by the canonical template and
accepts PIVOT as GO. Documentation and enforcement therefore diverge.

## Proposed Canon

- Preserve the existing GO-only rule.
- Parse both the canonical Markdown form and the legacy plain form.
- Return a dedicated blocker for PIVOT.
- Keep CLI, JSON keys and exit codes unchanged.

## Benefits

1. Template output passes without workaround.
2. PIVOT cannot authorize the rejected initial proposal.
3. Regression behavior is deterministic and test-covered.

## Risks

1. Hidden consumers relying on PIVOT pass-through will now block.
2. Regex parsing remains less robust than a future structured field.

## Impact Analysis

### Files

| File | Change type | Description |
|---|---|---|
| `tools/vbb-gate-check.py` | MODIFY | verdict parsing and blocker |
| `tests/test_gate_check_poc_verdicts.py` | CREATE | verdict matrix |
| Core documentation/templates | VERIFY/MODIFY | remove divergences only |
| `docs/DISTRIBUTIONS.md` | MODIFY | record Core propagation decision |

### Modules / Architecture Blocks

| Block | Impact | Action |
|---|---|---|
| governance-core | CONDITIONAL | align enforcement with documented contract |
| distribution-setup | NON_BREAKING | run smoke verification |

### Tests

| Test | Must pass | Currently passing |
|---|---|---|
| POC verdict matrix | yes | not yet created |
| full pytest | yes | baseline green after R0 |
| local CI | yes | baseline green after R0 |

## Migration Plan

1. Add failing regression tests.
2. Apply the minimal parser change.
3. Verify Core documentation and distribution references.
4. Run P.R2 and independent review.

## Backward Compatibility

- [x] GO consumers remain compatible.
- [x] PIVOT behavior intentionally tightens to the documented contract.

## Human Decision

- [x] **Approved** — user GO validates the READY plan.

## Verification Loop

- [ ] Architecture lint
- [ ] RELATIONS regeneration
- [ ] Contract lint
- [ ] Loop closure
- [ ] Full pytest and local CI
