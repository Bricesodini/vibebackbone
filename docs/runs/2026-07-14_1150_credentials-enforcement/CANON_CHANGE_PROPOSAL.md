---
run_id: "2026-07-14_1150_credentials-enforcement"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-14T12:12:00+02:00"
human_validated_by: "Brice — explicit Go approving SEC-01 Option A"
---

# Canon Change Proposal — activate credentials enforcement truth

## Current Canon

AGENTS.md Critical Rule #13 prohibits credentials but states that the
enforcement linter is deferred and the hook only logs a notice.

## Problem

ADR 0033 and SEC-02 activate a blocking Core tool in the hook and CI. Keeping
the deferred wording would create parallel truth between governance and code.

## Proposed Canon

Keep the prohibition unchanged, replace the deferred-status sentence with the
active enforcement surfaces, and preserve mandatory manual review as defense in
depth because pattern detection is intentionally not exhaustive.

## Benefits

1. Canon describes the executable state.
2. Agents know both automated and manual obligations.
3. P0-5-D can close without overstating detection guarantees.

## Risks

1. Consumers with copied old hooks may incorrectly assume they are protected.
2. Pattern coverage can be mistaken for proof of absence.
3. The exception marker requires review against bypass abuse.

## Impact Analysis

### Files

| File | Change type | Description |
|---|---|---|
| `AGENTS.md` | canon status update | deferred → active hook + CI, manual review retained |
| `tools/vbb-credentials-gate.py` | enforcement | shared differential scanner |
| `docs/DISTRIBUTIONS.md` | propagation log | four adapters inherit Core rule |

### Modules / Architecture Blocks

| Block | Impact | Action |
|---|---|---|
| governance-core | active rule wording | update one critical rule |
| contract-tooling | new security responsibility | add tool/hook/test evidence |
| distribution-setup | inherited Core governance | no adapter patch |

### Skills

| Skill | Change needed | Priority |
|---|---|---|
| none | existing security/remediation contracts remain valid | N/A |

### Prompts

| Prompt | Change needed | Priority |
|---|---|---|
| none | prompts consume AGENTS.md governance | N/A |

### Tests

| Test | Must pass | Currently passing |
|---|---|---|
| `tests/test_credentials_gate.py` | yes | 16/16 |
| `tests/test_framework_gate_hook.sh` | yes | 10/10 |
| full pytest | yes | 168 passed, 1 skipped before closeout |

## Migration Plan

### Phase 1 — Communication

- [x] Decision recorded in ADR 0033 and DISTRIBUTIONS.md.
- [x] Active risk and remediation report linked.

### Phase 2 — Parallel state

- [x] Not required; installed hooks delegate to the versioned script.

### Phase 3 — Cutover

- [x] Old log-only behavior removed.
- [x] New scanner called locally and in CI.
- [x] Canon wording updated in the same change set.
- [x] Tests updated.

### Phase 4 — Verification

- [x] Architecture lint passed after final docs.
- [x] Contract lint passed after final docs.
- [x] Local CI passed without warning after closeout.
- [x] Relevant pytest suite passed after final docs.
- [x] No competing active canon remains undocumented.

## Backward Compatibility

- [x] Fully backward compatible for delegating hooks; clean changes need no
  consumer action.
- [ ] Grace period required.
- [ ] Breaking consumer migration required.

## Human Decision

- [x] **Approved** — Brice approved Option A with `Go` after SEC-01 presented
  the exact hook + CI architecture.
- [ ] **Rejected**
- [ ] **Needs revision**

**Validator signature**: Brice (conversation record) **Date**: 2026-07-14

## Verification Loop

- [x] Canonical P.R2 complete after implementation and closeout.
- [x] Documentation links and closeout complete.

## Closeout Notes

P.R2 PASS: 170 tests passed, 1 skipped; local CI 9/9, 0 warning.

**Final status**: CLOSED **Closed by**: Codex **Date**: 2026-07-14
