---
run_id: "2026-07-14_1845_routing-trigger-precedence"
phase: "02_AUDIT"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T18:47:00+02:00"
ended_at: "2026-07-14T18:51:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "../../audits/impact-analysis-routing-trigger-precedence-20260714-1845.md"
---

# 02_AUDIT — Routing trigger precedence

## Evidence

The 64 contracts contain exactly six case-insensitive duplicate triggers:

| Trigger | Current contracts | Generic owner | Qualified alternative |
|---|---|---|---|
| `api contract` | designer / auditor | designer | `audit api contract` |
| `dead code` | janitor / anti-slop | janitor | `dead code quality gate` |
| `unused imports` | janitor / anti-slop | janitor | `unused import quality gate` |
| `monolith` | detector / tech debt | detector | `monolith debt` |
| `pilotage` | orchestrator / reference | orchestrator | `pilotage reference` |
| `status` | dashboard / report | dashboard | `status report` |

The router sums substring matches and strict mode rejects top candidates less
than 0.5 apart. Exact shared triggers therefore create avoidable ambiguity.

## Finding

`PATT-04` is confirmed P1. No contract-level or linter invariant currently
prevents recurrence.

```yaml
FINAL_STATUS:
  verdict: PARTIAL
  tests_run:
    - "casefolded 64-contract trigger inventory"
  tests_missing: []
  risks:
    - "six exact trigger collisions"
  open_points:
    - "assign unique generic owners and enforce uniqueness"
```
