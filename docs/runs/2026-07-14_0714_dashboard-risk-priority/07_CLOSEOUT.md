---
run_id: "2026-07-14_0714_dashboard-risk-priority"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
kind: "CLOSEOUT"
agent: "codex"
started_at: "2026-07-14T07:19:00+02:00"
ended_at: "2026-07-14T07:19:00+02:00"
next_phase: null
artifacts_consumed:
  - "01_INTAKE.md"
  - "04_PLAN.md"
  - "05_EXECUTION.md"
artifacts_produced:
  - "07_CLOSEOUT.md"
---

# 07_CLOSEOUT — Dashboard risk priority

## Type de closeout

**Kind**: `CLOSEOUT` — the bounded dashboard correction is complete.

## Résultat

QOA-004 is resolved on current evidence. The five-line terminal view now shows
the four active P1 rows before QOA-005 (P2), and JSON retains the same shape.

## Décisions prises

- Recognize risk tables by required headers instead of one fixed section.
- Normalize display markup, retain literal underscores, deduplicate IDs, and
  apply stable severity order.

## Artefacts livrés

| Phase | Fichier | Statut |
|---|---|---|
| 01_INTAKE | `01_INTAKE.md` | `READY` |
| 04_PLAN | `04_PLAN.md` | `READY` |
| 05_EXECUTION | `05_EXECUTION.md` | `READY` |
| 07_CLOSEOUT | `07_CLOSEOUT.md` | `READY` |

## Passe qualité scopée (ADR-0029)

- **Décision**: `SKIPPED (risque faible)`.
- **Déclencheur évalué**: one local read-only tool, no data/auth/security/
  compliance/production state, and no four-file product change.

## Change Set

- Parser: one existing function plus one standard-library import.
- Evidence: one direct regression test.
- Coherence: status, context, and four-distribution impact record.

## Commit Readiness

**READY** after the final P.R2 loop and credential scan.

## Coherence Check

- Gate: PASS; no ADR or POC required.
- JSON fields unchanged; real terminal output prioritizes P1.
- No new module, dependency, skill, or provider adapter.

## Remaining Risks

- The dashboard reports current declared state; stale declarations still require
  correction in `docs/AUDIT_STATUS.md`.
- TER-001 remains the next substantive P1 decision.

## Suggested Commit Message

`fix(dashboard): prioritize active risks`

## Next Action

Run or defer the bounded consumer-refresh POC for TER-001.

## Distribution impact

Generic Core tool correction inherited by Pi, OpenCode, Codex, and Claude Code.
No adapter or runtime-state change; decision recorded in `docs/DISTRIBUTIONS.md`.

```yaml
FINAL_STATUS:
  elapsed_seconds: 300
  budget_initial: 180
  progress_emitted: true
  progress_count: 1
  extension_requested: true
  timeout_closeout_emitted: false
  verdict: EXTENDED
  files_touched:
    - tools/vbb-status-dashboard.py
    - tests/test_status_dashboard.py
    - active status/context and run artifacts
  tests_run:
    - dashboard direct suite
    - real JSON ordering check
    - full pytest and local CI
  tests_missing: []
  risks:
    - declared status can itself be stale
  open_points:
    - TER-001 consumer refresh POC
```
