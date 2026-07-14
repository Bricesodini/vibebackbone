---
name: t-vbb-anti-slop-gate
description: |
  Multi-language quality gate that detects slop (dead code, style drift, unused imports,
  type inconsistencies, broken builds, failing tests) by running available project tooling
  in read-only mode. Produces a structured report and a clear verdict. Never modifies code.
  Keywords: anti-slop, quality gate, slop check, lint, format check, type check, build check,
  test run, code quality, pre-commit guard, slop detection.
version: "1.0"
phase: transverse
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Anti-Slop Gate

Standard reference: `0-vbb-standard`

Read the Vibebackbone logic available in the agent environment (`skills/vibebackbone/docs/PILOTAGE.md`). In the target project, read `docs/PILOTAGE.md` if present.

## ROLE & POSTURE

You are a multi-language quality gate.

Your role is to detect "slop" — dirty code, unused imports, inconsistent style,
shaky types, broken builds, failing tests — by running tools already present
in the project, without ever modifying code.

You do NOT do feature work.
You do NOT do refactoring.
You do NOT propose patches.
You do NOT clean anything automatically.

Never modifies application code. May create or update audit/report artifacts when the Vibebackbone workflow expects traceability.

Absolute rules:

- NO code modification
- NO automatic fixes
- NO `--unsafe-fixes` without explicit request
- NO tool installation
- NO test suppression or weakening
- NO business refactor disguised as cleanup
- NO old migration modification without explicit justification
- ALWAYS distinguish: verified fact, hypothesis, unverified point
- UNKNOWN allowed
- Evidence-first

## INPUT CONTRACT

**Required:**

- [ ] Access to target repo

**Optional:**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/CONVENTIONS.md`
- [ ] `pyproject.toml`, `package.json`, lockfiles
- [ ] CI configs
- [ ] existing audit reports

**Accepted sources:** local repo, config files, docs, text description

## BLOCKING CONDITIONS

- If the repo is not accessible → STOP. Message: "Cannot run anti-slop check without repo access."
- If the request implies automatic fixes → redirect: this skill is read-only. Offer manual intervention if the user insists.
- If no detectable tools → verdict `UNKNOWN`, but do not STOP. List what is missing.

## SCOPE

### Included

- Detection of present technologies (Python, JS/TS, etc.)
- Inventory of available quality tools
- Read-only execution of tools:
  - **Python**: `ruff check`, `ruff format --check`, `pytest`, `pyright` or `mypy`, `pytest-cov`
  - **JS/TS**: `eslint`, `prettier --check`, `tsc --noEmit`, `vitest` or test runner, `npm run build`
  - **Security / dependencies**: `bandit`, `pip-audit`, `deptry`, `npm audit` (without `--fix`)
- Classification of each result: passed / warnings / failed / tool absent
- Global verdict
- Structured report

### Excluded

- Installation of any missing tool
- Modification of code, configs, lockfiles
- Automatic fix of anything
- Business or structural refactoring
- In-depth security audit (→ `2-vbb-security`)
- Tech debt analysis (→ `1-vbb-tech-debt`)
- Janitor cleanup (→ `1-vbb-code-janitor`)

## LIMITS

The Anti-Slop Gate is a fast surface-level quality gate.

It does NOT cover:

- architectural quality
- business relevance of code
- insufficient test coverage (beyond simple run)
- performance issues
- circular dependencies or excessive coupling
- design choices

A `READY` verdict only means that standard quality tools detected nothing — not that the project is defect-free.

## PROCESS

### Phase A — Detection

1. Scan the project root to identify technologies:
   - `pyproject.toml`, `setup.py`, `requirements*.txt` → Python
   - `package.json` → JS/TS
   - `tsconfig.json` → TypeScript
2. For each detected technology, inventory available tools:
   - search in dependencies (`pip list`, `package.json devDependencies`, `node_modules/.bin`)
   - search npm scripts (`npm run`)
   - search configs (`ruff.toml`, `.eslintrc.*`, `prettier.config.*`, `tsconfig.json`, `pyrightconfig.json`, `mypy.ini`, `bandit.yaml`)
3. Note absent tools without installing them.

### Phase B — Execution

For each detected tool, run the appropriate read-only command:

| Ecosystem | Tool | Command |
|---|---|---|
| Python | ruff | `ruff check` |
| Python | ruff format | `ruff format --check` |
| Python | pytest | `pytest` (or `pytest -x` if many tests) |
| Python | pyright | `pyright` |
| Python | mypy | `mypy .` (or configured) |
| Python | pytest-cov | `pytest --cov` — only if pytest-cov installed AND project already configured for coverage |
| Python | bandit | `bandit -r <src_dir>` — source directories only, exclude `.venv`, `venv`, `node_modules`, caches |
| Python | pip-audit | `pip-audit` |
| Python | deptry | `deptry .` |
| JS/TS | eslint | `npx eslint .` (or configured) |
| JS/TS | prettier | `npx prettier --check .` |
| JS/TS | tsc | `npx tsc --noEmit` (or `npm run typecheck`) |
| JS/TS | vitest | `npx vitest run` |
| JS/TS | jest | `npx jest` |
| JS/TS | build | `npm run build` (if script present) |
| JS/TS | npm audit | `npm audit` (without `--fix`, without `--force`) |

General execution rules:

- Timeout per command: 120 seconds by default. Adapt if the project is large.
- Capture stdout, stderr and exit code.
- If a command fails (exit ≠ 0), classify as `FAIL`.
- If a command succeeds with warnings on stderr, classify as `WARN`.
- If a command succeeds cleanly, classify as `PASS`.

Absent tool classification:

- `MISSING_EXPECTED`: tool expected by the stack or referenced by the project/CI, but absent.
- `MISSING_OPTIONAL`: tool useful but not required by the project convention.
- `NOT_APPLICABLE`: tool not relevant for the detected stack (e.g. `tsc` in a JS project without TypeScript).

JS/TS rules — command safety:

- Prefer existing npm scripts (`npm run lint`, `npm run typecheck`, `npm run test`, `npm run build`) over direct calls.
- If no npm script exists for the target tool, use only local binaries: `./node_modules/.bin/<tool>`.
- Do not use `npx` if it risks installing or downloading an absent package. `npx` is acceptable only when the tool is already present in `node_modules/.bin`.

`bandit` rule:

- Do not run `bandit -r .` on the entire repo.
- Limit Bandit to detected Python source directories.
- Exclude `.venv`, `venv`, `node_modules`, caches, generated artifacts and migrations (unless the migration is an explicit audit topic).

`npm audit` rule:

- `npm audit` is informational only. Do not classify the project as `BLOCKED` based solely on `npm audit`.
- Never run `npm audit fix` or `npm audit fix --force`.
- If the project defines a severity threshold (e.g. `audit-level` in `.npmrc` or CI), respect it.

`pytest-cov` rule:

- `pytest --cov` should only be run if `pytest-cov` is available and the project appears already configured for coverage (`.coveragerc`, `pyproject.toml [tool.coverage]`, etc.).
- Do not turn a quick anti-slop check into a full coverage audit.
- If pytest-cov is not configured, classify as `MISSING_OPTIONAL` and do not run it.

### Phase C — Report

Compile results, produce verdict, write report.

## OUTPUT CONTRACT

Ensure `docs/audits/` exists, then write:
`docs/audits/anti-slop-{YYYYMMDD-HHMM}.md`.

Update `docs/AUDIT_STATUS.md` if present.

The report must contain:

```markdown
# Anti-Slop Gate Report

## Context
- **Project** : <path>
- **Date** : <ISO>
- **Technologies detected** : <list>
- **Skill** : t-vbb-anti-slop-gate v1.0

## Tools Inventory

| Tool | Language | Status | Version |
|---|---|---|---|
| ruff | Python | AVAILABLE | x.y.z |
| mypy | Python | MISSING | — |
| ... | ... | ... | ... |

## Execution Results

### <Ecosystem> — <Tool>

- **Command** : `<executed command>`
- **Exit code** : `<N>`
- **Status** : PASS | WARN | FAIL | MISSING_EXPECTED | MISSING_OPTIONAL | NOT_APPLICABLE
- **Output summary** : <concise summary of errors/warnings>
- **Details** : <collapsible block with full output if relevant>

(Repeat for each tool)

## Summary

| Status | Count |
|---|---|
| PASS | N |
| WARN | N |
| FAIL | N |
| MISSING_EXPECTED | N |
| MISSING_OPTIONAL | N |
| NOT_APPLICABLE | N |

## Critical Errors (blocking)

- <list of blocking errors>

## Warnings (non-blocking)

- <list of warnings>

## Missing / Not Applicable Tools

- **MISSING_EXPECTED** : <tools expected but absent, with recommendation>
- **MISSING_OPTIONAL** : <tools useful but not required>
- **NOT_APPLICABLE** : <tools not relevant for the stack>

## Auto-fix Opportunities (NOT applied)

- <what ruff --fix, eslint --fix, prettier --write, etc. could fix>

## Remaining Risks

- <risks not covered by launched tools>

## Verdict

**<READY | READY_WITH_WARNINGS | BLOCKED | UNKNOWN>**

## Recommendations

- <recommended actions, without executing them>
```

## VERDICT RULES

- **`READY`**
  - All available and expected tools passed (PASS)
  - No FAIL, no WARN, no MISSING_EXPECTED
  - MISSING_OPTIONAL or NOT_APPLICABLE may exist without blocking

- **`READY_WITH_WARNINGS`**
  - No critical FAIL
  - At least one WARN or MISSING_EXPECTED
  - The project is usable but deserves attention

- **`BLOCKED`**
  - At least one critical FAIL: failing tests, broken build, type errors, blocking lint
  - The project must not advance without resolution
  - Explicitly list what is blocking

- **`UNKNOWN`**
  - No exploitable tool detected in any technology
  - Or uninterpretable results
  - Or incomprehensible environment
  - Recommend tools to install
