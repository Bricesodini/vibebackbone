# LONG-RUN OUTPUT CONTRACT

> **Canonical source:** `~/02_Dev/vibebackbone/skills/vibebackbone/docs/PILOTAGE.md`
> This document is an **index card only** — for searchability via `vbb-index.py`.

## Keywords

`LONG-RUN OUTPUT CONTRACT`, `FINAL_STATUS`, `PROGRESS`, `COMPLETE_DURABLE`, `PARTIAL_DURABLE`, `EXTENSION_REQUEST`, `TIMEOUT_CLOSEOUT`, `PARTIAL_CONTROL`, `FAILED_SILENT_TIMEOUT`, `BLOCKED`, `verdict`, `budget`, `threshold`, `elapsed`, `worker`, `artifact`, `durable`

## Purpose

Defines how VBB workers report their execution status for **long-running tasks** that may exceed the initial time budget.

- PROGRESS checkpoint signals at 50% of budget
- FINAL_STATUS always required at end
- Durable artifact must contain FINAL_STATUS block

## Route Budgets

| Route | Initial | Extension1 | Extension 2 | Hard max | PROGRESS threshold |
|-------|---------|-------------|-------------|----------|-------------------|
| FAST | 60s | +120s | — | 5 min | 30s |
| STRUCTURED | 180s | +300s | +600s | 20 min | 90s |
| AUDIT | 180s | +300s | — | 15 min | 90s |
| CLOSEOUT | 90s | +180s | — | 5 min | 45s |

## Block Formats

### PROGRESS

```
[PROGRESS] elapsed_seconds: <N> | next_step: <description> | risks: <list>
```

Emit when `elapsed >= PROGRESS threshold` — at threshold, not at task end.

### FINAL_STATUS

```yaml
FINAL_STATUS:
  elapsed_seconds: <actual>
  budget_initial: <route_initial>
  progress_emitted: true|false
  progress_count: <N>
  extension_requested: true|false
  timeout_closeout_emitted: true|false
  verdict: COMPLETE|EXTENDED|PARTIAL_CONTROL|FAILED_SILENT_TIMEOUT|BLOCKED
  files_touched: []
  tests_run: []
  tests_missing: []
  risks: []
  open_points: []
```

### EXTENSION_REQUEST

```
[EXTENSION_REQUEST] reason: <why> | next_step: <bounded_action> | estimated_time: <N>s
```

Send before current budget expires. The controlling agent or human grants or denies.

### TIMEOUT_CLOSEOUT

```
[TIMEOUT_CLOSEOUT] reason: hard_timeout|controlled_stop | files_touched: []
```

## Durability Classification

| Condition | Durability |
|-----------|-----------|
| FINAL_STATUS in durable artifact (07_CLOSEOUT.md, audit report) | `COMPLETE_DURABLE` |
| FINAL_STATUS only in delegate summary | `PARTIAL_DURABLE` |
| TIMEOUT_CLOSEOUT in durable artifact | `COMPLETE_DURABLE` |
| No FINAL_STATUS and no TIMEOUT_CLOSEOUT | `FAILED_SILENT_TIMEOUT` |

## Verdict Mapping

| Condition | Verdict |
|-----------|---------|
| FINAL_STATUS + correct blocks + in durable artifact | `LONG_RUN_CONTROL_VALIDATED` + `COMPLETE_DURABLE` |
| FINAL_STATUS + correct blocks + summary only | `LONG_RUN_CONTROL_VALIDATED` + `PARTIAL_DURABLE` |
| FINAL_STATUS + no PROGRESS (elapsed > threshold) | `PARTIAL_CONTROL` + `PARTIAL_DURABLE` |
| TIMEOUT_CLOSEOUT present | `PARTIAL_CONTROL` |
| No FINAL_STATUS and no TIMEOUT_CLOSEOUT | `FAILED_SILENT_TIMEOUT` |
| Cannot determine next step | `BLOCKED` |

## Scenarios

**Scenario A — Within threshold:** `FINAL_STATUS` (verdict: COMPLETE), no PROGRESS required.

**Scenario B — Over threshold:** `FINAL_STATUS` (verdict: COMPLETE/EXTENDED) + at least 1 PROGRESS block emitted at threshold.

**Scenario C — Hard timeout:** `TIMEOUT_CLOSEOUT` (verdict: PARTIAL_CONTROL or FAILED_SILENT_TIMEOUT).

**Scenario D — Silent failure:** No FINAL_STATUS, no TIMEOUT_CLOSEOUT → `FAILED_SILENT_TIMEOUT`.

## Parallel Worker Safety

Parallel workers MUST NOT write to shared mutable artifacts (`ACTIVITY_LOG.md`, `SESSION.md`, `AUDIT_STATUS.md`, `CONTEXT.md`).

Each parallel worker writes to its own isolated artifact:
```
docs/runs/<YYYYMMDD_HHMM>_<worker>_<task>/07_CLOSEOUT.md
```

Only the designated closeout role may write to shared artifacts — serially,
after all workers complete.

## References

- Canonical spec: `docs/PILOTAGE.md` (`LONG-RUN RULE` section)
- Skill companion: `skills/vibebackbone/docs/PILOTAGE.md`
