# Deep Framework Audit — Vibebackbone — 2026-06-02 12:08

**Route**: AUDIT  
**Scope**: Vibebackbone framework repository (`/Users/bot/02_dev/vibebackbone`)  
**Skill used**: `vibebackbone`, `0-vbb-audit-readiness`, generic audit grid  
**Run artifact**: `docs/runs/2026-06-02_1208_deep-framework-audit/02_AUDIT.md`  
**Verdict**: `PARTIAL`

## Executive Summary

Vibebackbone is auditable and its core is structurally solid: 64 skill dirs,
64 `SKILL.md`, 64 `CONTRACT.yaml`, 64 indexed contracts, contract lint PASS,
architecture lint PASS, runtime dry-run stable, and `pytest tests/ -q` passes
81 tests.

The main weaknesses are not product-code defects; they are governance-runtime
trust gaps:

1. Local CI is not reproducible in this workspace because the script pins
   `python3`, while the passing test environment uses conda `python`.
2. The latest run fails the canonical closure invariant.
3. `SKILL.md` and `CONTRACT.yaml` versions diverge across all 64 skills.
4. Navigation/status docs still contain stale counters and future-dated state.
5. Prompt entrypoint names advertised by governance do not resolve at the
   advertised deployed prompt path in this environment.

## Global Verdict

**PARTIAL** — usable as a governance/reference distribution, but not clean enough
to claim full operational trust in local verification and session closure.

## Findings

| ID | Severity | Type | Evidence Level | Summary |
|----|----------|------|----------------|---------|
| VBB-DEEP-001 | P1 | VIOLATION | VERIFIED_FINDING | Local CI fails before checks because `/usr/bin/python3` lacks pytest, while conda `python` passes pytest. |
| VBB-DEEP-002 | P1 | VIOLATION | VERIFIED_FINDING | Latest run `20260602_0817_pr-operational-principles` fails closure invariant. |
| VBB-DEEP-003 | P1 | VIOLATION | VERIFIED_FINDING | 64/64 `SKILL.md` frontmatter versions differ from `CONTRACT.yaml.version`. |
| VBB-DEEP-004 | P2 | VIOLATION | VERIFIED_FINDING | `docs/INDEX.md` says 63 skills while active inventory is 64. |
| VBB-DEEP-005 | P2 | TREND | VERIFIED_FINDING | Future-dated governance state remains operationally visible. |
| VBB-DEEP-006 | P2 | VIOLATION | VERIFIED_FINDING | Tracked `.bak` file exists inside canonical skill docs. |
| VBB-DEEP-007 | P3 | OBSERVATION | VERIFIED_FINDING | `CONVENTIONS.md` traceability counters are stale. |
| VBB-DEEP-008 | P2 | VIOLATION | VERIFIED_FINDING | Short prompt names in AGENTS do not resolve to deployed prompt files at `/Users/bot/.agents/prompts/vibebackbone/`. |

Detailed evidence, traces, commands, and recommendations are in
`docs/runs/2026-06-02_1208_deep-framework-audit/02_AUDIT.md`.

## Verification

| Command | Result |
|---------|--------|
| `python tools/vbb-contract-lint.py` | PASS — 0 errors |
| `python tools/vbb-architecture.py lint` | PASS — 0 errors |
| `python tools/vbb-contract-runtime.py run --all --dry-run` | PASS/PARTIAL baseline — 43 PASS, 19 PARTIAL, 2 BLOCKED |
| `python tools/vbb-loop-closure-check.py` | FAIL — latest run closure invalid |
| `pytest tests/ -q` | PASS — 81 passed |
| `bash scripts/vbb-ci-local.sh` | FAIL — `python3` dependency mismatch (`pytest` missing) |

## Recommended Remediation Order

1. Fix VBB-DEEP-001 and VBB-DEEP-002 first: verification and closure are the
   backbone of the framework's trust model.
2. Clarify VBB-DEEP-003: decide if contract versions are schema versions or
   skill versions, then encode that decision.
3. Clean VBB-DEEP-004, VBB-DEEP-006, VBB-DEEP-007 via a small documentation
   hygiene pass.
4. Resolve VBB-DEEP-008 by installing prompts or reconciling AGENTS short names
   with actual prompt filenames.

## Out of Scope

- No remediation applied.
- No code mutation.
- No exhaustive audit of Hermes profiles outside the repository.

FINAL_STATUS:
  elapsed_seconds: 660
  budget_initial: 180
  progress_emitted: true
  progress_count: 1
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/runs/2026-06-02_1208_deep-framework-audit/01_INTAKE.md
    - docs/runs/2026-06-02_1208_deep-framework-audit/02_AUDIT.md
    - docs/runs/2026-06-02_1208_deep-framework-audit/03_DECISION.md
    - docs/runs/2026-06-02_1208_deep-framework-audit/07_CLOSEOUT.md
    - docs/audits/deep-framework-audit-20260602-1208.md
    - docs/AUDIT_STATUS.md
  tests_run:
    - "python tools/vbb-contract-lint.py"
    - "python tools/vbb-architecture.py lint"
    - "python tools/vbb-contract-runtime.py run --all --dry-run"
    - "python tools/vbb-loop-closure-check.py"
    - "pytest tests/ -q"
    - "bash scripts/vbb-ci-local.sh"
  tests_missing:
    - "Remediation verification loop; no remediation applied."
  risks:
    - "P1 CI local reproducibility gap."
    - "P1 latest run closure invariant gap."
  open_points:
    - "Open remediation session required."
