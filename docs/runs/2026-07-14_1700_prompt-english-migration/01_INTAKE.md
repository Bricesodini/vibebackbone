---
run_id: "2026-07-14_1700_prompt-english-migration"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T17:00:00+02:00"
ended_at: "2026-07-14T17:02:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "docs/audits/format-lint-prompt-language-20260714-1645.md"
  - "docs/runs/2026-07-14_1630_ready-independent-review/02_AUDIT_REPORT.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Agent-facing prompt English migration

## Objective

Reconcile stale SESSION truth, then translate the 18 French prompt surfaces to
English while preserving the existing language-independent contracts.

## Scope

- local `docs/SESSION.md` correction for READY-GOV-001;
- 18 affected files under `prompts/`;
- conservative prompt-language regression test;
- ADR/index, distribution impact and readiness truth updates.

Historical evidence, governance prose, skill bodies, prompt filenames, aliases,
phase/route/verdict enums and provider adapters are out of scope.

## Risk classification

**STRUCTURED** — shared agent language and prompt behavior affect all four
supported runtimes. ADR 0036 and POC evidence are required before execution.
