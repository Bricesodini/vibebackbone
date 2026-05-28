---
audit_type: global_implementation_readiness
date: 2026-05-28
auditor: codex
route: AUDIT
scope: vibebackbone distribution repo, with focus on reuse for another implementation
verdict: PARTIAL
temporal_provenance: docs/TEMPORAL_PROVENANCE.md
---

# Global Implementation Readiness Audit

**Date**: 2026-05-28  
**Route**: AUDIT  
**Goal**: assess whether this repository is ready to serve as the basis for another implementation.

## Executive summary

Vibebackbone is auditable and mature as a governance/reference distribution: the repository has clear system boundaries, complete skill and contract coverage, active governance files, green local tests, working install smoke tests, and a usable status dashboard.

Verdict for another implementation: **PARTIAL**.

The repository is safe to reuse as:

- a canonical governance model;
- a skills/prompts catalog;
- a source of implementation requirements for a future runtime.

It should not yet be treated as:

- a fully executable Formal Skill runtime;
- a perfectly aligned release package;
- a clean implementation seed without stabilization.

Before another implementation, run a short stabilization pass on adapter/package coherence, tracked generated files, CI parity, and the formal executor boundary.

## Evidence reviewed

Governance:

- `docs/CONTEXT.md`
- `docs/PILOTAGE.md`
- `docs/PROJECT_MODE.md`
- `docs/SESSION.md`
- `docs/AUDIT_STATUS.md`
- `docs/TEMPORAL_PROVENANCE.md`

Distribution and implementation surface:

- `README.md`
- `GUIDE.md`
- `docs/DEPLOYMENT.md`
- `docs/RUNBOOK.md`
- `setup.sh`
- `package.json`
- `.github/workflows/smoke.yml`
- `.github/workflows/vbb-contracts.yml`
- `skills/INDEX.yaml`
- `tools/*.py`
- `tests/*.py`
- `tests/*.sh`

Checks run:

```bash
python tools/vbb-contract-lint.py
python tools/vbb-contract-runtime.py --all --dry-run
python -m pytest
bash scripts/vbb-ci-local.sh
bash tests/smoke-install.sh
python tools/vbb-status-dashboard.py
```

Observed results:

- Contract lint: `0 error(s)`.
- Contract runtime dry-run: `44 PASS`, `17 PARTIAL`, `2 BLOCKED`.
- Pytest: `71 passed`.
- Local CI: `7 passed`, `0 failed`, `0 warnings`.
- Smoke install: pass, including install, idempotent reinstall, force governance, uninstall.
- Inventory: `63` skill directories, `63` `SKILL.md`, `63` contracts, `33` prompts total.

## Audit readiness

| Domain | Verdict | Evidence |
|--------|---------|----------|
| Functional stability | READY | Mode is `DISTRIBUTION`; scope and next action are declared in `docs/CONTEXT.md`. |
| Structural readability | READY | Clear `skills/`, `prompts/`, `docs/`, `tools/`, `tests/` layout. |
| Minimal documentation | READY | README, GUIDE, DEPLOYMENT, RUNBOOK, governance docs and audits exist. |
| Boundary clarity | READY | Inputs/outputs are skills, prompts, setup adapters, governance docs and local tools. |
| Critical invariants | PARTIAL | Contract coverage and route rules are visible, but runtime enforcement remains declarative. |
| Environment clarity | PARTIAL | Python/PyYAML dependency exists, local CI works, but GitHub/local parity is not exact. |

Readiness verdict: **READY for audit**, **PARTIAL for direct reimplementation**.

## Findings

### IMPL-001 — Adapter packaging counts diverge from canonical inventory

**Severity**: P1  
**Confidence**: high

**Finding**: `setup.sh` reports and deploys a prompt/skill adapter view that does not match the canonical repository inventory.

**Evidence**:

- Canonical inventory: `63` skill directories, `63` `SKILL.md`, `63` contracts, `33` prompts total.
- `README.md`, `GUIDE.md`, `CHANGELOG.md`, `docs/CONTEXT.md`, and `docs/AUDIT_STATUS.md` advertise `63 skills` and `33 prompts`.
- `bash tests/smoke-install.sh` passed, but setup output reported `64 skills · 26 prompts installed`.
- `setup.sh` counts skills with `ls "$SKILLS_SRC"`, which includes `INDEX.yaml`.
- Prompt adapters iterate only over `prompts/*.md`, so the 7 canonical prompts under `prompts/canonical/` are not deployed as provider command files.

**Impact**:

Another implementation could copy the wrong packaging semantics: canonical prompts exist but are not adapter-deployed, and the setup success line overstates skill count. This is a release trust problem, not a core governance failure.

**Recommended action**:

Make adapter inventory explicit:

1. Count skill directories, not all entries in `skills/`.
2. Decide whether canonical prompts must be provider commands.
3. If yes, deploy `prompts/canonical/*.md`; if no, document "33 total, 26 adapter commands".
4. Add a smoke assertion for the displayed setup counts.

### IMPL-002 — Formal runtime boundary is still declarative

**Severity**: P1  
**Confidence**: high

**Finding**: Contracts are complete and linted, but the system still relies on agents interpreting Markdown and YAML rather than an executor enforcing gates, state, and transitions.

**Evidence**:

- `docs/audits/global-evaluation-20260613.md` states "No runtime executor" and "contracts are declarative-only".
- Current runtime check is a dry-run: `44 PASS`, `17 PARTIAL`, `2 BLOCKED`.
- `setup.sh` installs governance and prompt/skill files, not a runtime that enforces route transitions or gate outcomes.

**Impact**:

For another implementation, the repo is a strong specification source but not yet a runtime foundation. A new implementation that assumes executable semantics will inherit hidden human/agent interpretation costs.

**Recommended action**:

Before building another implementation, define a small executor boundary:

- contract discovery;
- route selection;
- gate evaluation;
- artifact output validation;
- status propagation into `AUDIT_STATUS.md`;
- non-goals for v1 runtime.

Use the existing contracts as fixtures, not as already-enforced behavior.

### IMPL-003 — Release documentation has stale distribution counts

**Severity**: P2  
**Confidence**: high

**Finding**: `docs/DEPLOYMENT.md` still says `62 skills`, while active docs and measured inventory say `63`.

**Evidence**:

- `docs/DEPLOYMENT.md` says "Installer les 62 skills" and "Les 62 skills".
- `README.md`, `GUIDE.md`, `CHANGELOG.md`, `docs/CONTEXT.md`, and measured inventory say `63`.

**Impact**:

This creates low-grade release ambiguity for adopters and for a future implementation team using DEPLOYMENT as operational truth.

**Recommended action**:

Align `docs/DEPLOYMENT.md` with the current inventory and add it to the counter-check set.

### IMPL-004 — Git tracks generated Python bytecode

**Severity**: P2  
**Confidence**: high

**Finding**: Python bytecode files under `tests/__pycache__/` and `tools/__pycache__/` are tracked.

**Evidence**:

`git ls-files '*__pycache__*'` lists Python 3.11 `.pyc` files for tests and tools.

**Impact**:

Another implementation could inherit environment-specific artifacts, noisy diffs, and Python-version residue. This also makes routine local validation more error-prone: Python 3.13 test runs created additional untracked bytecode.

**Recommended action**:

Remove tracked `__pycache__` files from git and ensure `.gitignore` covers `__pycache__/` and `*.py[cod]`.

### IMPL-005 — GitHub CI and local CI are close but not identical

**Severity**: P2  
**Confidence**: medium

**Finding**: `scripts/vbb-ci-local.sh` runs the full pytest suite, while `.github/workflows/vbb-contracts.yml` runs selected test files directly and does not mirror the local `pytest tests/ -q` step.

**Evidence**:

- Local CI passed with `pytest tests/`.
- GitHub workflow runs contract lint, runtime dry-run, loop closure tests, portability tests, and project init tests.
- Tests for status dashboard, index, context compactor, and full pytest collection are covered locally but not directly by the workflow.

**Impact**:

Local confidence can exceed GitHub enforcement. A future implementation may repeat this split and miss regressions in tools not included in GitHub Actions.

**Recommended action**:

Make GitHub CI call `bash scripts/vbb-ci-local.sh`, or make both local and GitHub share one test list.

### IMPL-006 — Temporal provenance is documented but still costly for downstream reuse

**Severity**: P2  
**Confidence**: high

**Finding**: Future-dated historical artifacts are explicitly documented, but they remain a cognitive and automation hazard for a new implementation.

**Evidence**:

- Current workspace date for this audit: `2026-05-28`.
- `docs/TEMPORAL_PROVENANCE.md` documents imported future-dated runs from `2026-06-10` through `2026-06-13`.
- `python tools/vbb-status-dashboard.py` reports temporal provenance notes and `35` run directories dated after local date.

**Impact**:

This is acceptable in the current repo because provenance is explicit. A new implementation should not inherit this state as live project memory, or it will blur "historical evidence" and "current status".

**Recommended action**:

For another implementation, start with fresh generated governance files through `t-vbb-project-context-init` / `tools/vbb-project-init.py`, then import only selected reference audits as documentation, not active project status.

## Implementation guidance for the next build

Recommended stance: **reuse as reference, not as runtime seed**.

Immediate stabilization before another implementation:

1. Fix setup inventory and prompt adapter semantics (`IMPL-001`).
2. Align deployment docs and counter checks (`IMPL-003`).
3. Remove tracked bytecode (`IMPL-004`).
4. Make GitHub CI mirror local CI (`IMPL-005`).
5. Write the executor boundary ADR before implementing runtime behavior (`IMPL-002`).
6. Initialize the new implementation with fresh governance state, not this repo's audit history (`IMPL-006`).

## Final verdict

**PARTIAL — suitable as a canonical specification and governance source; not yet suitable as a direct executable implementation base without a short stabilization pass.**

No P0 was found. The open P1 risks are bounded and actionable.
