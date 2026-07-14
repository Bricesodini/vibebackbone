---
run_id: "2026-07-14_2124_readiness-integrity"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T21:27:00+02:00"
ended_at: "2026-07-14T21:29:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed: ["01_INTAKE.md", "POC.md", "INTEGRATION_GATE.md"]
artifacts_produced: ["04_FIX_PLAN.md"]
---

# 04_FIX_PLAN — readiness integrity

## Ordered work

| # | Change | Validation | Rollback |
|---|---|---|---|
| 1 | Add Codex no-follow install/uninstall migration and source guard | disposable legacy-link smoke test; source SHA stable | revert provider and root setup changes |
| 2 | Restore the canonical root `AGENTS.md` and migrate the real runtime file | Git diff clean for source; runtime is a regular file with one marker pair | retain backup and restore link only for diagnosis, never normal operation |
| 3 | Add measured dashboard posture and effective verdict | clean/dirty/divergent/corrupt temp-repo tests | preserve documented parser and revert effective aggregation |
| 4 | Validate long-run summaries in strict loop closure | controlled valid/invalid fixtures | disable new strict validator |
| 5 | Update architecture, distribution log, active truth and closeout | complete P.R2 and exact-SHA checks | keep status PARTIAL and document blocker |

## Definition of done

- Core source is unchanged by repeated Codex install and uninstall.
- Dashboard cannot report effective READY on the reproduced state.
- The 840/180/no-extension pattern is rejected in strict closure.
- Full P.R2, local CI, disposable HOME install, and exact-SHA remote CI pass.

## Impact analysis

- **Performed**: YES, using the approved repository-grounded plan.
- **Classification**: CONDITIONAL.
- **Core impact**: dashboard and closure semantics affect all four distributions.
- **Distribution impact**: install/uninstall migration is Codex-specific glue.
- **Data/auth/security impact**: none; filesystem integrity only.

## Integration Gate

- **ADR**: `docs/adr/0046-readiness-integrity-enforcement.md` — PASS.
- **POC**: `docs/runs/2026-07-14_2124_readiness-integrity/POC.md` — PASS.
- **CAN_CODE_START**: YES, subject to automated gate confirmation.
