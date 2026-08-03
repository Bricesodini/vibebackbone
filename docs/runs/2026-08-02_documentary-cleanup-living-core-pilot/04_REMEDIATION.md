---
run_id: "2026-08-02_documentary-cleanup-living-core-pilot"
phase: "04_REMEDIATION"
voie: "AUDIT"
status: "completed"
agent: "codex"
started_at: "2026-08-02T00:00:00Z"
ended_at: "2026-08-02T00:00:00Z"
artifacts_consumed:
  - "02_AUDIT.md"
  - "03_DECISION.md"
artifacts_produced:
  - "04_REMEDIATION.md"
---

# 04_REMEDIATION — Authorized living-core corrections

## Human authorization

Only LDC-001, LDC-002, LDC-003 and LDC-006 received `OUI`. LDC-004, LDC-005,
LDC-007 and LDC-008 remain `PLUS TARD` and were not remediated.

## Executed procedures

| Finding | Procedure | Scope | Result |
|---|---|---|---|
| LDC-003 | Documentary correction | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` frontmatter and provenance note | ADR 0053 is the explicit v1.2 alignment; ADR 0051 remains historical and unchanged. |
| LDC-002 | Documentary correction | `distributions/pi/SYSTEM.md` (source of root `SYSTEM.md`) | Runtime guidance now names the current v1.2 contract and preserves v1.1 only as historical semantics. |
| LDC-001 | Bootstrap correction | `AGENTS.md` | Critical Rule 16 is present with the approved OUI/NON/PLUS TARD behavior. |
| LDC-006 | Navigation correction | `docs/CONTEXT.md` | Router reflects the current bounded pilot, observable local/published state, applicable contract and runtime limitation. |

## Provenance and projection checks

- `SYSTEM.md` remains the symlink to `distributions/pi/SYSTEM.md`; no second
  source was created.
- No other distribution consumes a tracked `SYSTEM.md` representation in this
  repository.
- ADR 0051 was not edited.
- No document was deleted, moved, archived, tagged, or classified in the
  repository.
- No runtime was redeployed and no deployed runtime was certified.

## Deferred debts

- **LDC-004 / LDC-005 / LDC-007:** provenance references, DTS scope and prompt
  contract remain deferred; unresolved observations stay `UNKNOWN`.
- **LDC-008:** deployed Pi identity and provenance remain `UNKNOWN`. A later
  run must identify the deployed source, compare repository/distribution/
  runtime state, decide on redeployment or rollback, and validate from
  scratch.

## Validation results

| Check | Result | Observation |
|---|---|---|
| `python tools/vbb-architecture.py lint` | PASS | 0 errors, 0 warnings. |
| `python tools/vbb-contract-lint.py` | PASS | 0 errors; one pre-existing non-blocking description-length warning. |
| `python tools/vbb-document-convention-lint.py .` | PASS | `VBB-DOC-V1: PASS`. |
| `python -m pytest tests/test_documentary_skills_dtp_alignment.py -q` | PASS | 8 tests passed. |
| `python -m pytest -q` | FAIL | 517 passed, 1 skipped, 1 failed in pre-existing `test_status_dashboard.py::test_next_action`; no dashboard change was authorized. |
| `python tools/vbb-adversarial-gate.py <run> --strict` | BLOCKED | The run has no closeout artifact yet; this is not a governance verdict on the corrected documents. |
| `git diff --check` | PASS | No whitespace errors. |

The status dashboard executed and reported `PARTIAL` because the worktree is
not clean, HEAD is detached, no upstream is configured, and repository risks
remain open. Its existing `next_action` assertion failure remains outside this
run. This artifact records the authorized corrections; it is not a
certification of the deployed runtime.
