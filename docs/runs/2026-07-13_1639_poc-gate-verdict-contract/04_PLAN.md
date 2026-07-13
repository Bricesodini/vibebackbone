---
run_id: "2026-07-13_1639_poc-gate-verdict-contract"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-13T16:48:00+02:00"
ended_at: "2026-07-13T16:52:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "CANON_CHANGE_PROPOSAL.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — POC gate verdict contract

## Wave 1 — Tests first

- Add a table-driven test around `check_poc()`.
- Cover canonical bold GO, legacy plain GO, NO-GO, PIVOT, absent verdict and missing POC.

## Wave 2 — Minimal implementation

- Make GO parsing tolerate canonical Markdown emphasis.
- Remove PIVOT from the positive matcher.
- Return `POC_VERDICT_PIVOT` before the absent-verdict fallback.

## Wave 3 — Coherence

- Verify templates/GUIDE express GO-only.
- Record Core → Hermes/Cody decision without rewriting existing user changes.

## Wave 4 — Validation

- Focused tests, full P.R2, distribution smoke and independent review.

## Acceptance

- GO bold/plain PASS.
- NO-GO/PIVOT/absent/missing BLOCK with distinct reasons.
- CLI/JSON keys and exit codes unchanged.
