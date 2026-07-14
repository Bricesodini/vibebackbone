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
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — readiness integrity

## Objectif

Prevent runtime-to-Core writes, false READY output, and internally inconsistent
long-run closure declarations.

## Pré-conditions

- ADR 0046 accepted by explicit user approval.
- Reproducible legacy-link POC is GO.
- Automated integration gate returns `can_code_start=true`.

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|---|---|---|---|
| 1 | Protect Codex install/uninstall and migrate the legacy runtime link | `distributions/codex/setup.sh`, `setup.sh` | disposable smoke test; stable Core bytes | revert installer changes, never recreate unsafe link |
| 2 | Split documentary and measured dashboard truth | dashboard tool and tests | clean/dirty/divergent/corrupt repositories | revert effective aggregation |
| 3 | Enforce declared long-run invariants | loop-closure tool and tests | strict valid/invalid fixtures | disable new strict validation |
| 4 | Propagate architecture and governance truth | architecture/status/distribution docs | architecture lint and generated graph | keep PARTIAL and report blocker |

## Critères d'acceptation (Definition of Done)

- [x] Repeated Codex installation leaves the canonical source byte-identical.
- [x] Current runtime is a regular compiled file with one marker pair.
- [x] Dashboard effective verdict cannot remain READY on dirty/corrupt state.
- [x] Strict closure rejects 840/180 seconds without an extension.
- [x] P.R2 complete; commit, push and remote CI remain closeout actions.

## Plan de rollback global

Revert the implementation commit, retain runtime backups, and keep the global
posture PARTIAL until a safe alternative is implemented.

## Risques identifiés

- JSON semantic change: retain every existing field and add explicit measured
  fields; document `verdict` as conservative effective output.
- Legacy symlink ownership: never follow writes and preserve unrelated targets.

## Analyse d'impact

- **Effectuée ?**: OUI, via `t-vbb-impact-analyzer` planning.
- **Périmètre d'impact**: Contract Tooling Core and Codex distribution setup.
- **Risques d'effet de bord**: bounded by disposable HOME and temporary Git
  repository tests.

## Handoff vers `05_EXECUTION`

- **Première action concrète**: implement the Codex no-follow boundary.
- **Points de vigilance**: do not invoke the real installer before the smoke
  migration test passes.

## Integration Gate

- **ADR**: `docs/adr/0046-readiness-integrity-enforcement.md` — PASS.
- **POC**: `docs/runs/2026-07-14_2124_readiness-integrity/POC.md` — PASS.
- **CAN_CODE_START**: YES.
