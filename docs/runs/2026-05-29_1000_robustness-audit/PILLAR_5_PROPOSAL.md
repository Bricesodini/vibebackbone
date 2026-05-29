# Pillar 5 Proposal — Robustness

**Date**: 2026-05-29
**Run**: 2026-05-29_1000_robustness-audit
**Route**: AUDIT → 03_DECISION
**Type**: Canon Change Proposal

---

## Objective

Define the canonical Robustness pillar (Pillar 5) for Vibebackbone.
This pillar complements existing pillars: Readability, Modularity, Coherence
& Convergence, Traçabilité.

Robustness in Vibebackbone means: the system must detect failure, prevent
regression, protect invariants, and enforce verification before any
implementation is declared complete.

---

## Core Principles

### P.R1 — Fail Explicitly

A tool, gate, or check must fail with an explicit error message.
Silent failures are prohibited.

**Rationale**: Silent failures bypass verification and produce false confidence.
OPS-001 (now resolved) demonstrated this risk.

**Pattern**: Pure helper functions return error indicators (`None`, `False`,
error list). `main()` handles exit codes. Never call `sys.exit()` inside a
pure helper function.

**Applies to**: All tools in `tools/`, all linters, all check functions.

---

### P.R2 — One Verification Loop, All Gates

Before any implementation is declared complete, the full verification loop
must pass:

```bash
python tools/vbb-architecture.py lint
python tools/vbb-architecture.py graph --write
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py
pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

If any command fails → **do not mark as implemented**.
Document the failure, correct if in scope, re-run the full loop.

**Rationale**: Partial verification produces partial confidence.
The loop must be treated as an atomic operation.

**Applies to**: All implementation runs (phase 05) in STRUCTURED, AUDIT,
and FAST-STANDARD routes.

---

### P.R3 — Gate Before Action

A blocking gate must be evaluated before the action it protects.
A skill with unmet preconditions must not proceed.

**Rationale**: Executor state machine (READY → RUNNING → EVALUATING → terminal)
enforces this. Blocking before-gates stop execution; blocking after-gates are
recorded as warnings.

**Pattern**: `vbb-executor.py run <skill_id>` evaluates all before/success/after
gates. For agent-driven work, the phase router enforces phase prerequisites
(phase 0 before phase 2, etc.).

**Applies to**: Skill contracts, phase routing, CI checks.

---

### P.R4 — Invariant Protection

The run closure invariant must never be bypassed.

**Rule**: Every run must produce its required phase artifacts for its voie.
The loop closure check must report FAIL for incomplete runs.
A PASS verdict is only valid when all required artifacts exist and are valid.

**Rationale**: Run artifacts are the memory of the system. Incomplete runs
break traceability, audit integrity, and session resumption.

**Applies to**: All runs (any route), `vbb-loop-closure-check.py`.

---

### P.R5 — Regression Prevention First

No change is merged without algorithmic regression protection.

**Rule**: Every tool change must pass the full pytest suite.
Every contract change must pass `vbb-contract-lint.py`.
Every architecture change must pass `vbb-architecture.py lint`.
These checks are enforced by CI on every push.

**Rationale**: Manual review cannot catch all regressions.
Algorithmic checks (81 tests, 0 lint errors) are the safety net.

**Applies to**: All changes touching `tools/`, `skills/`, `docs/ARCHITECTURE.md`,
`tests/`.

---

### P.R6 — Error Handling by Layer

Errors are handled at the appropriate layer:

| Layer | Error handling |
|-------|---------------|
| Pure function | Return error indicator (`None`, `False`, error list) |
| Stateful function | Raise `ValueError` with context, or return error indicator |
| CLI entry point (`main()`) | Call `sys.exit()` with appropriate code (0 = pass, 1 = fail) |

**Rationale**: Separation of concerns. Helpers remain callable without side
effects. Entry points own process control.

**Applies to**: All Python files in `tools/`, `tests/`.

---

### P.R7 — Escalate on Risk Class Change

A task started in FAST that reveals a risk class change (data, auth, security,
compliance, prod) must escalate immediately.

**Rule**: Stop action, document the escalation in the current artifact,
reclassify the route, resume in the appropriate route.

**Rationale**: Starting in FAST does not grant permission to continue in FAST
when the actual risk class is higher.

**Applies to**: All FAST route executions.

---

### P.R8 — Review Independence

Executor and reviewer should be **independent whenever possible**.

If independence is impossible (small project, quick run, time constraint),
the review must explicitly state that it is self-review, including:
- The reviewer acknowledges the conflict of interest
- The specific artifacts reviewed
- Any compensating controls (e.g., manual check by human)

**Rationale**: Self-review produces cognitive bias and false confidence.
But in fast or small contexts, imposing two sessions can be
counter-productive. The rule is: prioritize independence, document
the compromise when it is not possible.

**Applies to**: STRUCTURED and AUDIT routes (where possible).
FAST routes may use self-review with explicit acknowledgment.

---

## Mandatory Validation Loop

### Standard Loop (all routes)

Before declaring any implementation complete:

```bash
python tools/vbb-architecture.py lint   # must pass — blocks if arch-sensitive file not covered
python tools/vbb-architecture.py graph --write  # must run — regenerates RELATIONS.md
python tools/vbb-contract-lint.py       # must pass — 0 errors
python tools/vbb-loop-closure-check.py # must pass — closure invariant satisfied
pytest tests/ -q                        # must pass — 81 tests green
bash scripts/vbb-ci-local.sh           # must pass — 8/8 checks
```

**Minimum passing criteria**: 0 lint errors, 0 test failures, loop closure PASS.

**Loop execution**: Before every `07_CLOSEOUT.md` in STRUCTURED and AUDIT routes.
Before every commit in FAST-STANDARD route.

### Fast Loop (FAST-ZERO, FAST-MINIMAL)

FAST-ZERO: No verification loop required. `docs/ACTIVITY_LOG.md` entry only.
FAST-MINIMAL: `vbb-loop-closure-check.py` on the run directory.

**Rationale**: Fast routes have lower risk. Loop overhead must be proportionate.

### Pre-commit Loop (advanced)

```bash
bash scripts/vbb-ci-local.sh && git commit
```

Enforces the full CI before any commit. GitHub CI runs a subset (contract lint,
architecture lint, dry-run, pytest) on every push/PR.

---

## Failure Handling Rules

### F.R1 — Lint Failure Blocks

A lint failure (`vbb-architecture.py lint` or `vbb-contract-lint.py`) is a
**hard block**. Implementation must not continue until the lint passes.

### F.R2 — Test Failure Blocks

A pytest failure is a **hard block**. No regression is acceptable.

### F.R3 — Loop Closure Failure Blocks

A loop closure FAIL is a **hard block**. The run is incomplete.
Produce missing artifacts or document the blocker before proceeding.

### F.R4 — CI Failure Blocks

A CI failure is a **hard block**. Do not push until CI passes.

### F.R5 — Document Before Correcting

When a failure is found:
1. Document the failure in the current phase artifact
2. Correct if within scope
3. Re-run the full verification loop
4. Only then declare the run complete

---

## Recovery Rules

### REC.R1 — Failed Run

When a run fails verification:
- Preserve the run directory (do not delete)
- Document the failure and the correction in the phase artifact
- Re-run the verification loop
- If the same check fails twice, escalate to STRUCTURED

### REC.R2 — Crashed Session

When a session crashes mid-run:
- The run directory is preserved (artifacts already written)
- Next session reads the run directory and resumes from the last valid artifact
- `t-vbb-context-compactor.py` can produce a summary for re-entry

### REC.R3 — Blocked Gate

When a skill execution is BLOCKED (preconditions not met):
- Document the blocking gate in the phase artifact
- Specify what preconditions must be satisfied
- Do not proceed until the blocking gate is resolved

---

## Regression Prevention Rules

### REG.R1 — Tools

Every change to `tools/*.py` must pass:
- `pytest tests/ -q`
- `python tools/vbb-contract-lint.py`
- `python tools/vbb-architecture.py lint`

### REG.R2 — Contracts

Every change to `skills/*/CONTRACT.yaml` must pass:
- `python tools/vbb-contract-lint.py`
- `python tools/vbb-contract-runtime.py run --all --dry-run` (PARTIAL acceptable)

### REG.R3 — Architecture

Every change to `docs/ARCHITECTURE.md` must pass:
- `python tools/vbb-architecture.py lint`
- `python tools/vbb-architecture.py graph --write`
- `docs/RELATIONS.md` must be regenerated (never edited manually)

### REG.R4 — Skills

Every new skill must have:
- `SKILL.md` in English
- `CONTRACT.yaml` validated by `vbb-contract-lint.py`
- Indexed in `skills/INDEX.yaml`
- At least one reference in `docs/ARCHITECTURE.md` block `files:`

---

## Escalation Rules

| Trigger | Action |
|---------|--------|
| FAST task reveals data/auth/prod impact | Escalate to STRUCTURED |
| FAST task reveals security/integrity/compliance | Escalate to AUDIT |
| FAST task reveals systemic behavior | Escalate to AUDIT |
| Verification loop failure after 2 attempts | Escalate to STRUCTURED |
| Blocking gate cannot be resolved | Stop, document, ask for human decision |
| Executor state = FAIL | Stop, document, re-run from last PASS artifact |
| CI failure on push | Block push, fix, re-run CI |

**Escalation protocol**: Stop → document in current artifact → reclassify route → resume.

---

## Verification Requirements

| Change type | Required verification |
|-------------|----------------------|
| Tool change | `pytest tests/ -q` + lint |
| Contract change | `vbb-contract-lint.py` + dry-run |
| Architecture change | `vbb-architecture.py lint` + `graph --write` |
| Run completion | Loop closure check on run directory |
| Phase completion | Phase artifact with valid frontmatter |
| Skill addition | Contract lint + index update + ARCHITECTURE.md coverage |
| Prompt addition | Manual review + CI pass |
| Governance change | AUDIT route + ADR + verification loop |

---

## Exit Criteria

A run can be closed (07_CLOSEOUT) when:

1. **All required phase artifacts exist** with valid frontmatter
2. **Loop closure check reports PASS** for the run directory
3. **All verification commands pass** (6-command loop)
4. **No blocking gates** remain unresolved
5. **Changes are committed** (git commit done)

---

## Integration with Existing Pillars

### Readability (Pillar 1)
- Function size ≤ ~20 lines supports testability and debuggability
- Error messages must be clear and actionable (supports failure handling)
- Short functions reduce the likelihood of silent failure paths

### Modularity (Pillar 2)
- Single-responsibility blocks support targeted regression tests
- Interface stability ensures that changing internal implementation
  does not break regression coverage
- Layer separation (UI must not carry business logic) supports
  failure isolation

### Coherence & Convergence (Pillar 3)
- The verification loop is the mechanism that enforces the "no parallel
  truth" principle — if the loop passes, the canon is coherent
- Human validation is required for canon changes, which includes
  robustness changes
- The CANON_CHANGE_PROPOSAL template applies to any change to Pillar 5

### Traçabilité
- Run artifacts (phase files) are the primary evidence of robustness
- Loop closure check verifies that all required artifacts exist
- The audit memory block (`docs/audits/`, `docs/runs/`) preserves
  all robustness evidence

### CONVENTIONS.md
- Pillar 5 extends Pillar 3's verification loop with specific failure
  handling rules, recovery rules, and escalation rules
- No contradiction with existing conventions
- P.R2 (verification loop) is already in CONVENTIONS.md § Pillar 3 —
  Pillar 5 formalizes it as a mandatory rule with specific commands

---

## Summary

Pillar 5 — Robustness is **already substantially implemented** by existing
mechanisms. The purpose of this proposal is to:

1. **Codify** existing practice as explicit rules
2. **Fill** the 3 cosmetic/low-priority gaps identified
3. **Clarify** failure handling pattern (helpers return error indicators)
4. **Formalize** the verification loop as a non-negotiable rule

**No new mechanisms needed.** The 15 existing mechanisms are sufficient.
The proposal adds only documentation and a small set of explicit rules
that align with current practice.

---

*Proposal: 2026-05-29 · Ready for human validation*
*See also: ROBUSTNESS_AUDIT.md (inventory + findings)*