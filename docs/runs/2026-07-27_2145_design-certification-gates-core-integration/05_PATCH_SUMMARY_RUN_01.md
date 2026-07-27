# 05_PATCH_SUMMARY_RUN_01 — Design/Certification assurance v1

## Objective delivered

The canonical Core now distinguishes `DESIGN` and `CERTIFICATION` gate
families while retaining local `PASS/FAIL`. Subject assurance is stored in the
sibling `ASSURANCE_STATUS`; implementation authorization is explicit and
fail-closed.

## Modified surfaces

- Core authorities: `AGENTS.md`, `docs/PILOTAGE.md`,
  `docs/AGENTIC_RUN_PROTOCOL.md`, `docs/GATE_ASSURANCE_GOVERNANCE.md`.
- Decision and architecture: ADR 0050, `docs/ARCHITECTURE.md`,
  generated `docs/RELATIONS.md`, `docs/DISTRIBUTIONS.md`.
- Navigation: `README.md`, `GUIDE.md`, `docs/INDEX.md`,
  `docs/runs/README.md`.
- Templates: intake, plan, review and closeout canonical and legacy variants.
- Prompts: canonical plan, review and closeout.
- Enforcement: `tools/vbb-loop-closure-check.py`.
- Tests: `tests/test_loop_closure.py`.
- Evidence: run artifacts and two timestamped audits.

## Compatibility

- No field removed or renamed.
- Historical runs remain valid without `ASSURANCE_STATUS`.
- New formal runs are validated from cutoff `2026-07-27_2145`.
- No distribution-specific rule or setup change.
- No consumer project modification.

## Tests

- `pytest -q tests/test_loop_closure.py` → 35 passed.
- `pytest -q` → 250 passed, 1 skipped.
- setup smoke → 32 PASS, 0 FAIL.
- architecture and contract lint → PASS.

## Unresolved points

- Independent review is required before closeout and before any commit/push.
- P.R2 must be rerun after review/remediation and final closeout.
