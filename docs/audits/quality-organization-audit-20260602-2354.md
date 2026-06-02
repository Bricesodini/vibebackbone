---
kind: audit_report
route: AUDIT
status: PARTIAL
agent: codex
created_at: "2026-06-02T23:54:09+02:00"
run_id: "2026-06-02_2354_quality-organization-audit"
---

# Quality Organization Audit — 2026-06-02 23:54

## Executive Summary

Verdict: **PARTIAL**.

The core Vibebackbone quality loop is strong: architecture lint, contract lint,
contract dry-run, pytest, and local CI all run successfully. The measured
inventory is coherent for the main catalog: **64 skills, 64 contracts, 33
prompts**.

The main risks are not in the skill catalog itself. They are in the
post-reorganization edges: Core vs Distribution truth, status/risk dashboards,
run ordering, and distribution code that moved but still references old
`tools/proxy` paths.

## Scope

- Repository root: `/Users/bot/02_dev/vibebackbone`
- Governance read: `docs/CONTEXT.md`, `docs/PILOTAGE.md`,
  `docs/PROJECT_MODE.md`, `docs/SESSION.md`, `docs/AUDIT_STATUS.md`,
  `docs/CONVENTIONS.md`, `docs/DISTRIBUTIONS.md`
- Code and artifacts inspected: `tools/`, `tests/`, `skills/`, `prompts/`,
  `docs/`, `.github/`, `scripts/`, `distributions/`
- Out of scope: implementation fixes, canonical rule changes, release actions

## Readiness And Scope Gates

- **Audit readiness**: READY. The repo has readable structure, governance files,
  run artifacts, tests, CI, and explicit invariants.
- **Scope freeze**: READY_WITH_CAVEATS. The distribution/core split is written,
  but the current tree contradicts part of that written scope.
- **ADR/POC gate**: PASS after `POC.md`; the POC confirmed read-only checks
  produce usable audit evidence.

## Verification Results

| Command | Result | Evidence |
|---|---:|---|
| `python tools/vbb-gate-check.py docs/runs/2026-06-02_2354_quality-organization-audit --json` | PASS | `can_code_start=true`, no blockers |
| `python tools/vbb-architecture.py lint` | PASS | 0 errors, 0 warnings |
| `python tools/vbb-architecture.py graph --write` | PASS | regenerated `docs/RELATIONS.md` with no diff |
| `python tools/vbb-contract-lint.py` | PASS | 0 errors |
| `python tools/vbb-contract-runtime.py run --all --dry-run` | PARTIAL_EXPECTED | 43 PASS, 19 PARTIAL, 2 BLOCKED/FAIL |
| `pytest tests/ -q` | PASS | 95 passed, 2 skipped |
| `bash scripts/vbb-ci-local.sh` | PASS | 8 passed, 0 failed |
| `ruff check .` | FAIL | 51 findings |
| `ruff format --check .` | FAIL | 42 files would be reformatted |
| `mypy tools tests` | FAIL | 63 errors |
| `pyright tools tests` | FAIL | 27 errors |
| `python -m pytest distributions/hermes/proxy/tests distributions/hermes/bypass-lint/tests -q` | FAIL | `ModuleNotFoundError: No module named 'tools.proxy'` |

## Findings

### QOA-001 — P1 — Core/Distribution boundary is contradicted by the repo tree

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `docs/DISTRIBUTIONS.md` says distributions are isolated outside the repo
    and "do not live in the VBB Core tree".
  - `distributions/README.md` says this folder hosts operational declinations.
  - The repo contains 55 tracked files under `distributions/`, including
    `distributions/hermes/proxy/*.py`, proxy ADRs, tests, config examples, and
    bypass-lint tooling.
  - `docs/ARCHITECTURE.md` does not reference `distributions/**`; sampled
    distribution paths are not covered by architecture source.
- **Why it matters**: the biggest reorganization introduced a competing truth:
  either distributions are out-of-repo runtime glue, or they are in-repo
  governed artifacts. Today they are both, which weakens impact analysis and
  ownership.
- **Recommended action**: decide one model and encode it everywhere. If
  `distributions/` stays in repo, add architecture blocks, CI coverage, and a
  distribution quality boundary. If not, move runtime code out and keep only
  catalog/docs pointers.

### QOA-002 — P1 — Hermes proxy migration is incomplete and tests are broken

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `python -m pytest distributions/hermes/proxy/tests
    distributions/hermes/bypass-lint/tests -q` fails during collection with
    `ModuleNotFoundError: No module named 'tools.proxy'`.
  - `distributions/hermes/proxy/tests/conftest.py` imports
    `from tools.proxy.crypto import generate_key, select_backend`.
  - `distributions/hermes/proxy/README.md` still instructs users to copy and
    run `tools/proxy/...` paths.
  - `rg "tools/proxy|tools.proxy" distributions/hermes` returns many stale
    references across docs, tests, config, and bypass-lint messages.
- **Why it matters**: a distribution subtree now looks first-class but cannot be
  tested from its current location. Security/proxy code is especially sensitive
  to broken tests and stale usage docs.
- **Recommended action**: run a dedicated STRUCTURED remediation for Hermes
  migration paths. Update imports, README/POC paths, config defaults, and CI
  inclusion together.

### QOA-003 — P1 — Default loop closure can validate the wrong run

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `tools/vbb-loop-closure-check.py` auto-detects most recent run by reverse
    lexicographic directory sort.
  - `tools/vbb-status-dashboard.py` uses the same name-based ordering for
    latest runs.
  - The current run
    `2026-06-02_2354_quality-organization-audit` was incomplete during the
    audit, and explicit loop closure correctly failed for missing
    `02_AUDIT.md`, `03_DECISION.md`, and `07_CLOSEOUT.md`.
  - The default loop closure command still resolved to
    `20260602_0817_pr-operational-principles` because mixed run-id formats make
    `20260602_...` sort after `2026-06-...`.
- **Why it matters**: the canonical verification loop can report PASS while not
  checking the current or chronologically latest run.
- **Recommended action**: require explicit `--run-id` in CI/closeout gates, or
  normalize run-id parsing to date/time semantics and reject mixed legacy
  formats from auto-resolution.

### QOA-004 — P1 — Status dashboard hides active open risks

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `python tools/vbb-status-dashboard.py --json` returned `"risks": []`.
  - `docs/AUDIT_STATUS.md` contains active open rows: `DOC-001`, `DOC-002`,
    `LLM-LOAD-002`, `LLM-LOAD-003`, `QA-002`, `QA-003`, `QA-004`, `QA-005`,
    `QA-006`, `QA-007`.
  - `tools/vbb-status-dashboard.py` only extracts rows from the first
    `## Risks identified` section, not later audit-note risk tables.
- **Why it matters**: the status command can tell an operator there are no open
  risks while the canonical audit status file contains many. That is a direct
  traceability failure.
- **Recommended action**: make risk extraction section-agnostic or introduce one
  normalized active risk table that all audit notes feed.

### QOA-005 — P2 — `AUDIT_STATUS.md` contains contradictory quality-adoption state

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - The quality adoption narrative says QA-002 was added, QA-003 count verified,
    and QA-006 harmonized.
  - The table immediately below keeps QA-002, QA-003, and QA-006 as Open.
  - Current measured prompt count is 33, so the QA-003 row "actual 27 files" is
    stale against live inventory.
- **Why it matters**: `AUDIT_STATUS.md` is the audit dashboard. Contradictory
  statuses force humans and agents to choose which sentence is canonical.
- **Recommended action**: normalize each QA row to one state and move historical
  stale wording to an archive note.

### QOA-006 — P2 — Run artifact hygiene has loose, unchecked files

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `docs/runs/README.md` defines a run as a timestamped folder with phase
    artifacts.
  - `docs/runs/routing-fix-verification.md` is a loose root-level run artifact,
    marked `Status: PENDING`, and is not covered by loop closure.
  - `docs/runs/README.md` is also a root-level Markdown file, but it is an index
    and should be explicitly distinguished from run artifacts.
- **Why it matters**: loose operational files in `docs/runs/` evade the closure
  invariant and can remain pending indefinitely.
- **Recommended action**: add a hygiene check that allows only `README.md` and
  timestamped run directories at `docs/runs/` root; move the routing verification
  file into a proper run or archive.

### QOA-007 — P2 — Optional quality tools expose unmanaged style/type debt

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `ruff check .`: 51 findings.
  - `ruff format --check .`: 42 files would be reformatted.
  - `mypy tools tests`: 63 errors.
  - `pyright tools tests`: 27 errors.
  - CI currently runs contract lint, architecture lint, runtime dry-run and
    pytest, but not style/type gates.
- **Why it matters**: after a large reorganization, lack of enforced style/type
  gates lets moved code rot silently. This is especially visible in
  `distributions/hermes`.
- **Recommended action**: decide whether these tools are canonical. If yes, add
  configs and staged remediation. If no, document them as non-gating so agents
  stop treating their failure ambiguously.

### QOA-008 — P2 — Distribution code is outside architecture and CI coverage

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `docs/ARCHITECTURE.md` references setup/docs/workflow files but no
    `distributions/**` source paths.
  - `scripts/vbb-ci-local.sh` and GitHub CI run `pytest tests/ -q` only.
  - Direct distribution pytest fails before test execution because imports still
    point to old `tools.proxy` paths.
- **Why it matters**: architecture lint can pass while a large, security-related
  distribution subtree is absent from the architecture source and CI signal.
- **Recommended action**: add a `distribution-runtime` architecture block and a
  separate CI job for distribution tests, or explicitly exclude distributions
  from VBB Core quality claims.

### QOA-009 — P3 — Status counters drift from measured state

- **Evidence level**: VERIFIED_FINDING
- **Evidence**:
  - `docs/CONTEXT.md` and `docs/SESSION.md` still mention `82/82` tests.
  - Current `pytest tests/ -q` returns `95 passed, 2 skipped`.
  - Contract runtime dry-run measured `43 PASS | 19 PARTIAL | 2 BLOCKED/FAIL`,
    while `docs/AUDIT_STATUS.md` still records `44 PASS · 17 PARTIAL · 2
    BLOCKED`.
- **Why it matters**: static counters are easy to trust and hard to keep true.
- **Recommended action**: replace static counts with generated command
  references or update them during closeout only from machine output.

## Roadmap

### Immediate

1. Fix the Core/Distribution decision: in-repo governed distributions vs
   out-of-repo runtime glue.
2. Repair Hermes proxy path migration (`tools/proxy` → current package path)
   and add a distribution test target.
3. Fix run auto-resolution: explicit `--run-id` or semantic timestamp parsing.
4. Fix status dashboard risk extraction so active risks are visible.

### Next

1. Reconcile `AUDIT_STATUS.md` QA rows and stale counters.
2. Move or archive loose `docs/runs/routing-fix-verification.md`.
3. Decide whether `ruff`, `ruff format`, `mypy`, and `pyright` are canonical
   gates; then remediate or document as non-gating.

### Later

1. Reduce large skill/prompt load surfaces already identified by prior audits.
2. Exercise the canon-change proposal template once as an operational test.

## Residual Risks And Unknowns

- I did not inspect external Hermes profiles under `~/.hermes/profiles/`; this
  audit is limited to the repository tree.
- I did not fix any code or documentation contradictions in this run.
- Distribution tests may require package-path decisions before they can be made
  meaningful.

## FINAL_STATUS

```yaml
FINAL_STATUS:
  elapsed_seconds: 900
  budget_initial: 900
  progress_emitted: true
  progress_count: 6
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/audits/quality-organization-audit-20260602-2354.md
    - docs/runs/2026-06-02_2354_quality-organization-audit/
    - docs/AUDIT_STATUS.md
    - docs/CONTEXT.md
    - docs/SESSION.md
  tests_run:
    - python tools/vbb-gate-check.py docs/runs/2026-06-02_2354_quality-organization-audit --json
    - python tools/vbb-architecture.py lint
    - python tools/vbb-architecture.py graph --write
    - python tools/vbb-contract-lint.py
    - python tools/vbb-contract-runtime.py run --all --dry-run
    - pytest tests/ -q
    - bash scripts/vbb-ci-local.sh
    - ruff check .
    - ruff format --check .
    - mypy tools tests
    - pyright tools tests
    - python -m pytest distributions/hermes/proxy/tests distributions/hermes/bypass-lint/tests -q
  tests_missing: []
  risks:
    - QOA-001
    - QOA-002
    - QOA-003
    - QOA-004
    - QOA-005
    - QOA-006
    - QOA-007
    - QOA-008
    - QOA-009
  open_points:
    - Decide Core vs Distribution placement model.
    - Repair Hermes proxy migration before treating distribution code as release-ready.
```
