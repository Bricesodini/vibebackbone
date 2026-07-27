---
load_policy: always
context_role: piloting-router
phase: transverse
status: active
---

# Operational Piloting — vibebackbone

**Version** : 2.2 | **Date** : 2026-06-12 | **Status** : Canonical piloting entry point

`load_policy: always` — this file is part of the canonical boot set, sourced
by every supported agent. Triage and escalation rules here are the canonical
source; other governance docs reference this file rather than duplicating.

---

## Role

Canonical operational entry point for any agent or human piloting vibebackbone. Minimal decision grid: classify, escalate, switch routes.

---

## The 5 route families

### MVP START gate

Any project started from zero, MVP build request, initial RICO/brief review, or
request to code before the base specification is complete enters **MVP START**
before implementation.

- **Entry**: new product/MVP, incomplete RICO, missing brief, unclear MVP scope,
  or coding requested before readiness.
- **Minimum action**: apply [`MVP_START_PROTOCOL.md`](MVP_START_PROTOCOL.md) via
  `0-vbb-rico-readiness`.
- **Exit to STRUCTURED**: readiness `READY` with base brief, non-goals, initial
  data model if needed, architecture boundaries, deployment constraints, and
  acceptance criteria.
- **Blocked exit**: readiness `BLOCKED` or `UNKNOWN` -> prioritized blocking
  questions only; no application code, migration, endpoint, model, UI component,
  Docker structure, persistence logic, or business logic.

MVP START is a mandatory pre-route gate, not a replacement for STRUCTURED
execution.

| Route | When | Minimum action | Escalate if |
|-------|------|----------------|-------------|
| **FAST-ZERO** | Safe micro-task, ≤ 3 files | `docs/ACTIVITY_LOG.md` only | Risk detected → STRUCTURED |
| **FAST-MINIMAL** | Small non-trivial task | `05_PATCH_SUMMARY` | Risk detected → STRUCTURED |
| **FAST** (STANDARD) | Simple task, low risk | Act directly | Data/auth/security impact → AUDIT |
| **STRUCTURED** | Architecture, contracts, multi-file | Read mode+session+audit → expose plan | Security → AUDIT |
| **AUDIT** | Security, integrity, compliance, systemic risk | Timestamped report in `docs/audits/`, read-only | — |
| **CLOSE-HANDOFF** | Pause, travail non terminé, reprise attendue | `t-vbb-commit-ready` → git commit → git push → archive `SESSION.md` to `docs/SESSION.history/` → update `SESSION.md` for next session | — |
| **CLOSE-FINAL** | Fin de session, run terminé | `t-vbb-commit-ready` → git commit → git push → empty `SESSION.md` → update `CONTEXT.md` | — |

Full details (sequences, alternatives, artifact conventions): [ROUTER_MATRIX.md](router/ROUTER_MATRIX.md)

---

## Triage rule

```
0. New MVP/from-zero or incomplete RICO ? → MVP START gate
1. Promotes or changes reusable engineering knowledge ? → AUDIT minimum
2. Touches data/auth/prod ? → STRUCTURED minimum
3. Touches security/integrity/compliance ? → AUDIT
4. Neither ? → FAST
5. End of session ? → CLOSE-HANDOFF (paused, reprise attendue) or CLOSE-FINAL (terminated): t-vbb-commit-ready → git commit → git push → update SESSION.md (archive if HANDOFF, empty if FINAL) → update CONTEXT.md
```

### Engineering knowledge gate

Every formal closeout performs the Knowledge Harvest defined in
[`ENGINEERING_KNOWLEDGE_GOVERNANCE.md`](ENGINEERING_KNOWLEDGE_GOVERNANCE.md).

- Recording an observation or linking evidence does not change the delivery
  verdict.
- Qualifying or promoting a candidate enters `AUDIT` minimum.
- Promotion requires a knowledge audit, a distinct independent review and an
  explicit human decision.
- Canonical integration then uses a separately gated `STRUCTURED` run.
- No FAST route may promote, edit or supersede canonical knowledge.

### Pre-execution gate

Before any worker touches the repo on a STRUCTURED or AUDIT route, the run
directory must pass the VBB gate:

```bash
python tools/vbb-gate-check.py <run_dir>
```

The gate is clause-aware (ADR + POC + Integration) and refuses to start a run
that does not conform. Pi, OpenCode, Codex and Claude Code invoke the same Core
tool directly. Exit 0 = proceed, non-zero = STOP and report the failure.

---

## Escalation rule

FAST task that reveals impact on data, auth, security, compliance, production, or systemic behavior → **escalate immediately** to STRUCTURED or AUDIT. Never finish in FAST if the risk has changed.

Full procedure (stop, partial closeout, new session): [SESSION_RULES.md § Escalation](SESSION_RULES.md#escalation--new-session)

---

## LONG-RUN RULE

A timeout is a **checkpoint, not a failure**. No worker may disappear silently.

### Required formats

Workers must emit these blocks at appropriate boundaries:

**PROGRESS** (mid-run heartbeat — see thresholds below):
```yaml
PROGRESS:
  phase: planning|editing|testing|closeout
  done: ""
  next: ""
  files_touched: []
  risks: []
  estimated_remaining: ""
  needs_extension: true|false
```

**EXTENSION_REQUEST** (before timeout — mandatory before any extension is granted):
```yaml
EXTENSION_REQUEST:
  reason: ""
  additional_time_seconds: 300
  scope_unchanged: true|false
  next_bounded_step: ""
  risk_changed: true|false
```

**TIMEOUT_CLOSEOUT** (mandatory on hard timeout or controlled stop):
```yaml
TIMEOUT_CLOSEOUT:
  completed: ""
  incomplete: ""
  files_touched: []
  tests_run: []
  tests_missing: []
  risks: []
  resume_from: ""
  recommended_next_prompt: ""
```

**FINAL_STATUS** (mandatory for every worker — always at end of output):
```yaml
FINAL_STATUS:
  elapsed_seconds: 120
  budget_initial: 180
  progress_emitted: true|false
  progress_count: 0
  extension_requested: true|false
  timeout_closeout_emitted: true|false
  verdict: COMPLETE|EXTENDED|PARTIAL_CONTROL|FAILED_SILENT_TIMEOUT|BLOCKED
  files_touched: []
  tests_run: []
  tests_missing: []
  risks: []
  open_points: []
```

### Budgets by route

| Route | Initial | Extension 1 | Extension 2 | Hard max | PROGRESS threshold (50%) |
|-------|---------|-------------|-------------|----------|-------------------------|
| **FAST** | 60s | +120s | — | 5 min | **30s** |
| **STRUCTURED** | 180s | +300s | +600s | 20 min | **90s** |
| **AUDIT** | 180s | +300s | — | 15 min | **90s** |
| **CLOSEOUT** | 90s | +180s | — | 5 min | **45s** |

### OUTPUT CONTRACT rules

These rules are **mandatory** for all workers.

**Rule 1 — FINAL_STATUS always required (in both summary AND durable artifact).**
Every worker output MUST end with a `FINAL_STATUS` block. Additionally, if the worker produces a durable artifact (`07_CLOSEOUT.md`, audit report, or similar), the `FINAL_STATUS` block MUST be included in that file on disk. The delegate summary alone is NOT a durable record.

**Rule 2 — PROGRESS required when elapsed > threshold.**
If `elapsed_seconds > PROGRESS threshold`, at least one `PROGRESS` block is REQUIRED before `FINAL_STATUS`.

**Rule 3 — EXTENSION_REQUEST required before extension.**
If an agent needs more time, it MUST emit `EXTENSION_REQUEST` before the current budget expires. The controlling agent or human grants or denies.

**Rule 4 — TIMEOUT_CLOSEOUT required on hard timeout or controlled stop.**
If `hard_max` is reached or the run is intentionally stopped, the worker MUST produce `TIMEOUT_CLOSEOUT` instead of `FINAL_STATUS`.

### Scenarios

**Scenario A — Completed within PROGRESS threshold:**
- `FINAL_STATUS` (verdict: COMPLETE)
- `PROGRESS`: not required
- Durable artifact? → write FINAL_STATUS into it if it exists

**Scenario B — Completed after PROGRESS threshold:**
- `FINAL_STATUS` (verdict: COMPLETE or EXTENDED)
- `PROGRESS`: at least 1 block REQUIRED
- `EXTENSION_REQUEST`: if extension was needed and granted
- Durable artifact? → write FINAL_STATUS into it if it exists

**Scenario C — Hard timeout or controlled stop:**
- `TIMEOUT_CLOSEOUT` (verdict: PARTIAL_CONTROL or FAILED_SILENT_TIMEOUT)
- `PROGRESS`: if emitted before the stop
- Durable artifact? → write TIMEOUT_CLOSEOUT into it if it exists

**Scenario D — Worker disappeared silently:**
- No `FINAL_STATUS` and no `TIMEOUT_CLOSEOUT` in output
- Controller verdict: `FAILED_SILENT_TIMEOUT`

### Durability classification

When evaluating FINAL_STATUS and verdict, the controlling agent classifies durability:

| Condition | Durability |
|----------|------------|
| FINAL_STATUS in durable artifact (07_CLOSEOUT.md, audit report, etc.) | `COMPLETE_DURABLE` |
| FINAL_STATUS only in delegate summary, no durable artifact | `PARTIAL_DURABLE` |
| TIMEOUT_CLOSEOUT in durable artifact | `COMPLETE_DURABLE` |
| TIMEOUT_CLOSEOUT only in summary | `PARTIAL_DURABLE` |
| No FINAL_STATUS and no TIMEOUT_CLOSEOUT | `FAILED_SILENT_TIMEOUT` |

`PARTIAL_DURABLE` is not a failure, but it means the record depends on the session summary. Prefer writing blocks into durable artifacts.

### Extension conditions

The controlling agent or human may grant an extension only if:
- phase is clear
- files touched are known
- next step is bounded
- `risk_changed: false`
- `scope_unchanged: true` or explicitly approved

### Verdict vocabulary

- `COMPLETE` — task finished, all required blocks present
- `EXTENDED` — task finished after granted extension
- `LONG_RUN_CONTROL_VALIDATED` — system handled the long run correctly (complete or extended)
- `PARTIAL_CONTROL` — timeout reached but TIMEOUT_CLOSEOUT produced, resume point clear
- `FAILED_SILENT_TIMEOUT` — worker disappeared without TIMEOUT_CLOSEOUT
- `BLOCKED` — cannot determine next step from available state

MVP START escalation:

- critical ambiguity -> blocking questions
- architecture not defined -> no code
- data not modeled -> no persistence
- readiness `PARTIAL` -> framing only
- readiness `BLOCKED` or `UNKNOWN` -> stop before implementation

---

## Verdict cascade × environment

| Verdict | Dev | Staging | Prod |
|---------|-----|---------|------|
| **READY** | Continue | Continue | Continue |
| **PARTIAL** | Continue (warning) | Continue if user confirms | **BLOCK** |
| **BLOCKED** | Stop immediately | Stop immediately | Stop immediately |
| **UNKNOWN** | Continue if user confirms | **Stop** | **Stop** |

Principle: "Fail open = fail dangerous."

---

## Document hierarchy

0. `docs/CONTEXT.md` → MOC, first file to read
1. **This document** → canonical piloting
2. `docs/PROJECT_MODE.md` → mode signal
3. `docs/SESSION.md` → local, gitignored
4. `docs/AUDIT_STATUS.md` → audit dashboard
5. `docs/audits/` · `docs/runs/` → on demand
6. `docs/CONVENTIONS.md` → quality conventions (5 pillars: Readability, Modularity, Coherence, Traçabilité, Robustness P.R1-P.R8)
7. `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` → reusable-learning maturity,
   evidence, review, promotion and supersession

## Quality standards

Quality conventions are canonical in `docs/CONVENTIONS.md`.
Agents must follow them by default.
Any canon change requires a documented proposal and human validation
(`docs/templates/CANON_CHANGE_PROPOSAL.md.template`).

The operational robustness rules P.R1-P.R8 are part of Pillar 5, not a separate
parallel canon. In practice:

- P.R1/P.R2: declare invariants and run the verification loop before completion.
- P.R3/P.R4: expose ambiguity and preserve traceability through durable artifacts.
- P.R5/P.R6: protect rollback paths and avoid silent failure.
- P.R7/P.R8: prevent regression and prefer independent review, or disclose self-review.

---

## For more details

- **Route sequences, artifact conventions**: [ROUTER_MATRIX.md](router/ROUTER_MATRIX.md)
- **Session rules**: [SESSION_RULES.md](SESSION_RULES.md)
- **Memory and handoff**: [MEMORY_AND_HANDOFF.md](MEMORY_AND_HANDOFF.md)
- **Repository index**: [docs/INDEX.md](INDEX.md)

---

_vibebackbone Piloting v2.2 — 2026-06-12 · Canonical root entry point_
