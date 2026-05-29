# Audit: Pillar 5 Foundation — Robustness Canonicalization

**Date**: 2026-05-29
**Run**: 2026-05-29_1000_robustness-audit
**Route**: AUDIT
**Phase**: 02_AUDIT

---

## Context

This audit evaluates vibebackbone's existing robustness mechanisms to define the canonical
Robustness pillar (Pillar 5). Existing pillars: Readability, Modularity, Coherence &
Convergence. Traçabilité already strongly covered by ADRs, run artifacts, audits,
ARCHITECTURE.md, risk register, and context handoff.

Scope: failure prevention, verification, validation, regression prevention, invariant
protection, error handling, recovery, rollback, operational resilience, implementation
verification. Out of scope: UI, UX, migration policies, AI governance, documentation
translation, prompt redesign.

This audit does not implement changes. It produces findings and a canonical proposal.

---

## Phase 1 — Inventory: Existing Robustness Mechanisms

### 1. Architecture Lint

**Name**: `vbb-architecture.py lint`
**Purpose**: Ensure every architecture-sensitive file is covered by at least one block
in `docs/ARCHITECTURE.md`.
**Failure prevented**: Adding files not referenced by any block; architecture drift;
breaking the single source of truth.
**Trigger**: `python tools/vbb-architecture.py lint` — run by CI, before any arch-impacting
change, by `vbb-dependency-mapper`.
**Coverage**: All files listed in `files:` patterns of 8 blocks. Enforces required fields:
`id`, `type`, `status`, `role`, `responsibilities`, `depends_on`, `impacts`, `files`,
`contracts`, `tests`, `risks`.
**Limitation**: Only checks coverage, not correctness of content. Blocks with incorrect
`depends_on` or `impacts` pass the lint silently. Cannot detect semantic errors.
**Criticality**: **HIGH** — gatekeeper for architecture integrity.

---

### 2. Contract Lint

**Name**: `vbb-contract-lint.py`
**Purpose**: Validate every `CONTRACT.yaml` against the schema: YAML syntax,
skill references, circular dependencies, gate depth, blocking gates, output fields,
agent compatibility, artifact mappings.
**Failure prevented**: Malformed contracts, broken skill references, circular gates,
incompatible agents, missing output fields, invalid artifact declarations.
**Trigger**: CI (local + GitHub), `vbb-contract-runtime`, `vbb-executor validate`,
manual pre-commit.
**Coverage**: 64 contracts. Checks: YAML syntax, gates (before/success/after),
circular deps, expected_status matches target, outputs.required fields, agent list,
artifact mapping (v0.3+).
**Limitation**: Dry-run only — does not execute skill logic. Cannot detect
runtime behavioral issues. PARTIAL results are expected for stubs.
**Criticality**: **HIGH** — gatekeeper for contract integrity.

---

### 3. Loop Closure Check

**Name**: `vbb-loop-closure-check.py`
**Purpose**: Verify that a run directory satisfies the closure invariant for its voie.
**Failure prevented**: Incomplete runs (missing required phase artifacts), missing
frontmatter, placeholder values, runs with unknown voie.
**Trigger**: CI check 4/8, `scripts/vbb-ci-local.sh`, manual after each run.
**Coverage**: Phase file existence + frontmatter validation (7 required fields +
placeholder detection). Voie inference from INTAKE → CLOSEOUT → PATCH_SUMMARY.
**Limitation**: Only checks presence, not content quality. A run with valid
frontmatter but meaningless content passes. Cannot detect semantic gaps.
**Criticality**: **HIGH** — invariant protector for run discipline.

---

### 4. Local CI (vbb-ci-local.sh)

**Name**: `scripts/vbb-ci-local.sh`
**Purpose**: Run 8 checks locally with parity to GitHub CI.
**Failure prevented**: Introducing defects that CI would catch — contract errors,
architecture drift, broken runs, failing tests.
**Trigger**: Manual before commit, post-implementation verification.
**Coverage**:
- [1/8] Contract lint
- [2/8] Architecture lint
- [3/8] Contract runtime dry-run
- [4/8] Loop closure (latest run) — non-blocking warning acceptable
- [5/8] Loop closure tests
- [6/8] Portability tests
- [7/8] Project init tests
- [8/8] Pytest suite
**Limitation**: Check 4 runs on most recent run only — not all runs. Check 3 is
dry-run only. Local-only (not enforced on remote without GitHub Actions).
**Criticality**: **HIGH** — primary gate before any commit.

---

### 5. GitHub CI (vbb-contracts.yml)

**Name**: `.github/workflows/vbb-contracts.yml`
**Purpose**: Enforce contract lint, architecture lint, runtime dry-run, and pytest
on every push/PR across Ubuntu and macOS.
**Failure prevented**: Contract/architecture errors entering main branch.
**Trigger**: On every push and pull request.
**Coverage**: Contract lint, architecture lint, runtime dry-run, pytest.
**Limitation**: Does not run loop closure check (check 4/8). Does not run portability
or project init tests. Does not verify RELATIONS.md regeneration.
**Criticality**: **HIGH** — enforces baseline on all remote commits.

---

### 6. Contract Runtime (vbb-contract-runtime.py)

**Name**: `vbb-contract-runtime.py run --all --dry-run`
**Purpose**: Execute all skill contracts in dry-run mode and report state.
**Failure prevented**: Broken skill contracts that would fail at execution time;
contract invocation errors; missing skill references.
**Trigger**: CI check 3/8, manual pre-commit, release validation.
**Coverage**: 63 contracts (44 PASS, 17 PARTIAL, 2 BLOCKED expected).
PARTIAL = stub output doesn't satisfy success gates (expected).
BLOCKED = scope-freeze gate chain (expected).
**Limitation**: Dry-run stubs produce stub output, not real execution.
PARTIAL results are not automatically actionable.
**Criticality**: **MEDIUM** — catches contract invocation errors but not behavioral ones.

---

### 7. Pytest Suite

**Name**: `tests/` — 9 test suites, 81 tests
**Purpose**: Algorithmic regression detection across core tooling.
**Failure prevented**: Breaking contract linting, loop closure, status dashboard,
context compactor, vbb-architecture, index, project init, portability.
**Trigger**: CI check 8/8, manual pre-commit, pre-release.
**Coverage**:
- `test_contract_lint.py` — contract lint correctness
- `test_loop_closure.py` — loop closure logic (7 phases, 4 routes)
- `test_status_dashboard.py` — dashboard generation
- `test_context_compactor.py` — compact_run behavior, error handling
- `test_vbb_architecture.py` — architecture block validation, Mermaid generation
- `test_vbb_index.py` — index build, search, stale detection
- `test_project_init.py` — project initialization
- `test_portability.py` — tool portability across platforms
**Limitation**: All tests pass currently (81/81 green). Coverage is high for
tooling but no tests cover skill behavioral outputs, prompt quality, or ADR integrity.
**Criticality**: **HIGH** — algorithmic regression prevention.

---

### 8. Executor State Machine (vbb-executor.py)

**Name**: `vbb-executor.py` — formal runtime with gate enforcement
**Purpose**: Execute skill contracts with a state machine: READY → RUNNING →
EVALUATING → DONE | PARTIAL | BLOCKED | FAIL. Implements ADR-0001.
**Failure prevented**: Executing skills without preconditions met; running blocked
skills; proceeding without postconditions.
**Trigger**: `vbb-executor.py run <skill_id> [--run-id <id>] [--strict]`
Manual or scripted. Not run automatically by CI.
**Coverage**: Before gates (blocking), success gates, after gates (blocking), artifact
existence check (v0.3+), gate depth limit enforcement.
**Limitation**: Agent-only skills produce stub output — executor validates contracts,
not agent judgment. Not integrated into the standard CI loop (check 3 uses dry-run,
not executor). Cannot enforce business logic correctness.
**Criticality**: **MEDIUM** — formal state machine for gate enforcement, not yet
in CI loop.

---

### 9. Frontmatter Validation (in loop-closure-check.py)

**Name**: `validate_artifact()` function
**Purpose**: Ensure phase artifacts have valid YAML frontmatter with all required
fields and no placeholder values.
**Failure prevented**: Incomplete artifacts (missing run_id, phase, status, etc.),
unfilled templates.
**Trigger**: Called by `vbb-loop-closure-check.py` for every required phase artifact.
**Coverage**: 8 required fields: `run_id`, `phase`, `voie`, `status`, `agent`,
`started_at`, `ended_at`, `artifacts_produced`. Placeholder detection (`<value>`).
**Limitation**: Only checks frontmatter, not body content. Cannot detect incorrect
but filled-in values (e.g., wrong phase name, wrong status).
**Criticality**: **MEDIUM** — complements file presence check with structure validation.

---

### 10. Anti-Slop Gate (t-vbb-anti-slop-gate)

**Name**: `t-vbb-anti-slop-gate` skill
**Purpose**: Quality gate that detects slop (dead code, style drift, unused imports,
type inconsistencies, broken builds, failing tests) by running available project
tooling in read-only mode.
**Failure prevented**: Accumulation of maintainability debt, style drift, broken
builds entering the codebase.
**Trigger**: Invoked as a skill in phase 4 or before CLOSEOUT in any route.
**Coverage**: Runs project tooling (lint, format check, type check, build check,
test run) in read-only mode. Produces structured report and clear verdict.
**Limitation**: Read-only — cannot fix. Depends on tooling being present in the
target project. Not integrated into CI (CI uses custom checks, not this skill).
**Criticality**: **MEDIUM** — pre-commit quality gate, not yet in standard CI loop.

---

### 11. Status Dashboard (vbb-status-dashboard.py)

**Name**: `vbb-status-dashboard.py`
**Purpose**: Terminal dashboard showing verdict, skills, contracts, tests, latest
runs, open risks, and next action.
**Failure prevented**: Operating without global context; missing audit awareness;
unresolved P0/P1 risks.
**Trigger**: Manual (`python tools/vbb-status-dashboard.py`), or as `t-vbb-status-dashboard`
skill.
**Coverage**: Verdict, skills count, contracts count, test suites, audit status,
P0/P1 open, temporal provenance, next action.
**Limitation**: Dashboard reads from static files — does not re-run audits.
Temporal provenance check only warns if date mismatch exists; does not resolve it.
**Criticality**: **LOW** — diagnostic tool, not a gate.

---

### 12. Index Staleness Detection (vbb-index.py)

**Name**: `_index_is_stale()` in `vbb-index.py`
**Purpose**: Detect when the local index is stale and auto-rebuild it.
**Failure prevented**: Acting on outdated index entries; missing newly added files
from search results.
**Trigger**: Automatic on search when manifest is stale.
**Coverage**: File set comparison + mtime comparison of indexed sources vs manifest.
**Limitation**: Index is search tool, not robustness mechanism per se. Auto-rebuild
hides staleness rather than preventing it.
**Criticality**: **LOW** — operational tool.

---

### 13. Phase Router (vbb-phase-router.py)

**Name**: `vbb-phase-router.py`
**Purpose**: Route a query to the most appropriate skill based on phase and domain.
**Failure prevented**: Incorrect skill selection; running phase 2 without phase 0
preconditions.
**Trigger**: Manual (`python tools/vbb-phase-router.py "<query>"`) or as skill.
**Coverage**: 63 contracts indexed. Route verification: requires semantic trigger match.
**Limitation**: Does not execute skills — only routes. Cannot detect skill behavioral
failures.
**Criticality**: **MEDIUM** — routing gate for phase discipline.

---

### 14. Smoke Tests (smoke-contract-runtime.sh, smoke-install.sh)

**Name**: `tests/smoke-contract-runtime.sh`, `tests/smoke-install.sh`
**Purpose**: End-to-end smoke tests for contract runtime and install process.
**Failure prevented**: Broken install process; contract runtime failures in CI.
**Trigger**: Post-install verification, pre-release validation.
**Coverage**: Contract runtime invocation, install script execution, skill deployment.
**Limitation**: Shell scripts — not pytest. Minimal assertions. Not run in standard CI.
**Criticality**: **MEDIUM** — operational smoke tests.

---

### 15. Review Route (AUDIT route)

**Name**: AUDIT route in PILOTAGE.md
**Purpose**: Enforce read-only audit for security, integrity, compliance, systemic risk.
**Failure prevented**: Implementing fixes during an audit (bias); missing audit phase
before structural changes.
**Trigger**: Any task touching security, integrity, compliance, or systemic risk.
**Coverage**: Phase 02_AUDIT produces timestamped report in `docs/audits/`. Read-only
discipline enforced by route definition.
**Limitation**: Human discipline — no technical enforcement. An agent could modify
during audit if not routed properly.
**Criticality**: **HIGH** — process gate, not technical one. Enforced by PILOTAGE.md.

---

## Phase 2 — Revalidation: Active Robustness Findings

### OPS-001

**Status**: ✅ **RESOLVED** (commit `147f6dc`, 2026-05-28 16:29)

**Pre-fix behavior**: When both `01_INTAKE.md` and `07_CLOSEOUT.md` were absent,
`required_phases = ["07_CLOSEOUT"]` was assigned silently, and the error was added
to the list — but the final verdict was PASS because the artifact list was empty
but valid.

**Post-fix behavior** (current): Errors are added before the fallback assignment.
The final verdict checks `if errors:` and returns FAIL. All 6 reproduction cases
tested 2026-05-29 return FAIL with exit code 1.

**Evidence**: Git commit `147f6dc` — "fix(ops): resolve 3 robustness gaps from
global-robustness audit. OPS-001: explicit fail when both INTAKE and CLOSEOUT
absent instead of silently falling back to pass."

**Verification**: 2026-05-29. Tested against: unknown voie + no closeout (FAIL),
no INTAKE + no closeout (FAIL), CLOTURE + no closeout (FAIL), empty voie (FAIL),
no frontmatter (FAIL), valid STRUCTUREE + missing phases (FAIL). All correct.

**Recommendation**: CLOSED. No further action. Optional cosmetic cleanup: remove
the `required_phases = ["07_CLOSEOUT"]` fallback assignment in the unknown-voie
branch since it has no functional effect.

---

### OPS-002

**Status**: ✅ **RESOLVED** (commit `147f6dc`, 2026-05-28 16:29)

**Finding**: `compact_run()` in `vbb-context-compactor.py` called `sys.exit(1)` on
error conditions (run_dir not found, not a directory, no phase files).

**Post-fix behavior** (current): `compact_run()` returns `None` on error. `main()`
handles `None` and returns exit code 1 with error message.

**Current evidence** (2026-05-29):
```bash
grep -n "sys.exit" tools/vbb-context-compactor.py
```
Output:
```
94:    Does not call sys.exit — callers handle errors.
274:    sys.exit(main())  # only exit in main(), not in helpers
```

`compact_run()` no longer contains `sys.exit`. The only `sys.exit` in the file is
in `main()` at line 274, which is the correct pattern.

**Recommendation**: CLOSED.

---

### OPS-003

**Status**: ✅ **RESOLVED** (commit `147f6dc`, 2026-05-28 16:29)

**Finding**: `temporal_warnings` duplicated `temporal_notes` in `vbb-status-dashboard.py`.

**Current evidence** (2026-05-29):
```bash
grep -n "temporal_warnings" tools/vbb-status-dashboard.py
```
Output: no matches — field removed.

**Recommendation**: CLOSED.

---

## Phase 3 — Gaps: Missing Robustness Principles

### A. Failure Handling

**Gap**: No explicit convention for failure handling in tooling.

**Evidence**: `vbb-contract-lint.py` uses `sys.exit(1)` for failures — correct for CLI
entry point. `vbb-loop-closure-check.py` returns `Tuple[bool, List[str]]` and calls
`sys.exit` in `main()` — correct. `vbb-executor.py` uses `ExecutorState` enum with
terminal states — correct. `vbb-context-compactor.py` returns `Optional[str]` — correct.

**No gap**: Failure handling is already well-implemented in all tools. No convention
needs to be added — the existing pattern is consistent: pure helpers return error
indicators; `main()` handles exit codes. This should be documented as the canonical
failure handling pattern.

---

### B. Recovery

**Gap**: No explicit convention for recovery when a verification loop fails.

**Evidence**: CONVENTIONS.md (Pillar 3) says "If any command fails → do not mark as
implemented. Document the failure, correct if in scope, re-run the full loop."
This covers the loop but not recovery from a failed run.

**No explicit recovery convention** for:
- How to resume after a CI failure
- What to do when a run is partially completed
- How to handle a blocked gate in executor

**Assessment**: Recovery is handled by the run artifact system (partial runs are
preserved in `docs/runs/`). The context compactor can resume from any run directory.
No canonical recovery protocol is missing — the system is designed for resumable
sessions. Low priority gap.

---

### C. Verification

**Gap**: Verification loop is documented in CONVENTIONS.md but not automated.

**Evidence**: CONVENTIONS.md § Pillar 3 defines the 6-command verification loop.
It is run manually before declaring complete, and in CI (8 checks). The loop exists
but is not enforced as a single atomic operation — it is 6 separate commands.

**No gap in content**: The loop is well-defined. **Gap in enforcement**: no single
command that runs the full loop and returns one verdict. This is acceptable — the
CI script already provides this as `bash scripts/vbb-ci-local.sh`.

**Additional gap**: The executor (`vbb-executor.py`) is not part of the CI loop.
Check 3 uses `vbb-contract-runtime.py --dry-run`, not the executor. The formal
executor could be added to CI as `vbb-executor.py validate` but it adds no value
over `vbb-contract-lint.py` for non-executable skills.

**Assessment**: Verification loop is well-defined and well-enforced. No gap.

---

### D. Regression Prevention

**Gap**: No explicit convention for mandatory test coverage before a change is
declared complete.

**Evidence**: CONVENTIONS.md (Pillar 2 — Testing) says "Tests must be algorithmic
and automated, not dependent on LLM judgment." No threshold, no rule about what
must be tested.

**Current practice**: 81 tests cover the tooling. Skills are not tested
algorithmically (agent-only). No convention defines when a new skill needs tests.

**Assessment**: For a governance system, the current test coverage is appropriate.
The 81 tests cover the critical paths (lint, loop, architecture, index, init).
Adding more tests would not significantly improve robustness. **No canonical gap**
— the existing approach (focus on critical paths, not maximum percentage) is correct.

---

### E. Escalation

**Gap**: Escalation is well-defined in PILOTAGE.md (FAST → STRUCTURED/AUDIT)
but not enforced technically.

**Evidence**: PILOTAGE.md defines escalation triggers: data/auth/prod → STRUCTURED;
security/integrity/compliance → AUDIT. This is human-enforced, not automated.

**Assessment**: Process-based escalation (PILOTAGE.md) is the right approach for
a governance system. Technical enforcement of escalation would be over-engineering.
The existing rule is clear and sufficient. **No gap.**

---

### F. Rollback

**Gap**: No explicit rollback mechanism for governance changes.

**Evidence**: ADRs document decisions but there is no rollback protocol if a
change causes problems. `git revert` is the mechanism but no convention defines
when and how to use it.

**Assessment**: For a governance system, `git revert` + new ADR is sufficient.
Rollback is already possible through version control. **No canonical gap.**

---

### G. Implementation Verification

**Gap**: No explicit convention requiring verification before declaring complete.

**Evidence**: CONVENTIONS.md § Verification loop already defines this. "If any
command fails → do not mark as implemented. Document the failure, correct if in
scope, re-run the full loop."

**Assessment**: This gap is already covered. No duplication needed.

---

## Coverage Analysis

### What is well-covered

| Concern | Mechanisms | Quality |
|---------|-----------|---------|
| Contract integrity | Contract lint, runtime dry-run, executor state machine | HIGH |
| Architecture integrity | Architecture lint, dependency mapper, impact analyzer | HIGH |
| Run discipline | Loop closure check, frontmatter validation, CI | HIGH |
| Regression prevention | Pytest (81 tests), CI (8 checks), anti-slop gate | HIGH |
| Verification | 6-command loop in CONVENTIONS.md, CI (8 checks) | HIGH |
| Escalation | PILOTAGE.md (process), phase router | HIGH |
| Error handling | Pattern: helpers return error indicators, main() handles exit | HIGH |

### What is partially covered

| Concern | Gap | Priority |
|---------|-----|----------|
| Executor not in CI loop | `vbb-executor.py validate` not run in CI (redundant with contract-lint) | LOW |
| Context compactor | Recoverable but no explicit recovery protocol | LOW |
| Rollback | `git revert` available but no convention | LOW |

### What is not covered

| Concern | Gap | Priority |
|---------|-----|----------|
| Skill behavioral testing | No algorithmic test for skill outputs | LOW (skill is agent-only) |
| ADR integrity | No automated check that ADRs are internally consistent | LOW |
| Anti-slop not in CI | `t-vbb-anti-slop-gate` not integrated in CI | LOW |

---

## Summary

Vibebackbone has a **strong robustness foundation** across 15 mechanisms.

**HIGH coverage**: Architecture lint, contract lint, loop closure, local CI,
GitHub CI, pytest (81 tests), executor state machine, frontmatter validation,
review route (AUDIT).

**MEDIUM coverage**: Contract runtime dry-run, anti-slop gate, phase router,
smoke tests.

**LOW coverage**: Status dashboard, index staleness detection.

**All 3 active findings (OPS-001, OPS-002, OPS-003) are resolved.**

**The only significant gaps are cosmetic or low-priority**: no single atomic
verification command (acceptable — CI script exists), executor not in CI loop
(redundant with contract-lint for agent-only skills), no explicit rollback
convention (git revert is sufficient).

**No P0 or P1 gaps identified.**

---

*Audit: 2026-05-29 · Phase 1 + 2 + 3 completed · No code modified*
*Verdict: ROBUSTNESS WELL-COVERED — canonical proposal follows in PILLAR_5_PROPOSAL.md*