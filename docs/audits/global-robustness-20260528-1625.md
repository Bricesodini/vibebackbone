---
run_id: 2026-05-28_1625_global-robustness-audit
phase: 02_AUDIT
route: AUDIT
status: PARTIAL
agent: local
started_at: 2026-05-28T14:25:00Z
ended_at: 2026-05-28T14:50:00Z
next_phase: 03_DECISION
artifacts_consumed:
  - docs/ARCHITECTURE.md
  - docs/RELATIONS.md
  - docs/AUDIT_STATUS.md
  - tools/*.py
  - tests/*.py
  - skills/INDEX.yaml
  - .github/workflows/vbb-contracts.yml
  - scripts/vbb-ci-local.sh
artifacts_produced:
  - docs/audits/global-robustness-20260528-1625.md
---

# Audit: Global Robustness — vibebackbone

**Verdict: `PARTIAL`**

Comprehensive read-only audit of vibebackbone's tooling, CI, error handling,
operational readiness, and audit memory. No code modifications.

---

## Context

This audit evaluates the robustness of the vibebackbone repository as a
governance/tooling system — not a web application. Scope is adapted accordingly:
Python tools, CI scripts, contract tooling, audit memory, and error handling
consistency.

Evidence gathered from: tools/*.py, tests/*.py, CI files, docs/ARCHITECTURE.md,
docs/AUDIT_STATUS.md, skills/INDEX.yaml, docs/runs/.

---

## Verdict: PARTIAL

Vibebackbone is operationally healthy. 81 tests pass, CI is clean (local + GitHub),
contracts are valid (63/63), index is complete (63/63). The architecture-source
layer integration is solid (ARCHITECTURE.md canonique, RELATIONS.md généré,
vbb-architecture.py fonctionnel). Skills are aligned.

However, 3 robustness gaps exist beyond what the previous architecture audit
identified. They are bounded and actionable.

---

## Findings (P0 → P1 → P2)

### OPS-001 | P1 | HIGH | vbb-loop-closure-check.py — unknown voie on fallback silently passes

**File:** `tools/vbb-loop-closure-check.py` — `check_run()` function

**Finding:** When `01_INTAKE.md` is absent and the voie cannot be inferred, the
function falls back to `required_phases = ["07_CLOSEOUT"]` instead of failing.
This means a run with an unknown or missing voie and no closeout would pass
silently.

```python
# Current code (line ~180):
else:
    # Unknown voie — fall back to universal minimum
    required_phases = ["07_CLOSEOUT"]
```

If a run directory has no closeout and no intake, `check_run` returns PASS
with an empty artifact list.

**Impact:** A malformed run (e.g., a session that crashed before producing
any artifact) would be reported as closed, bypassing the invariant entirely.

**Recommendation:** Fail explicitly when both intake and closeout are absent.
Add: `if not closeout_path.exists(): errors.append("07_CLOSEOUT.md: missing
(required fallback invariant)")`

---

### OPS-002 | P2 | MEDIUM | vbb-context-compactor.py — sys.exit(1) inside helper function

**File:** `tools/vbb-context-compactor.py` — `compact_run()` function

**Finding:** `compact_run()` calls `sys.exit(1)` on two error conditions:

```python
# Inside compact_run(), called by main():
if not run_dir.exists():
    print(f"Error: ...", file=sys.stderr)
    sys.exit(1)   # ← process exit inside a helper function

if not run_dir.is_dir():
    sys.exit(1)   # ← same

if not phase_files:
    sys.exit(1)   # ← same
```

`compact_run()` is a pure content transformer — it should return an error
indicator or raise, not call `sys.exit`. The caller (`main()`) cannot
recover, cannot format the error, and cannot distinguish between different
failure modes.

**Impact:** Operational clarity. Tests cannot call `compact_run()` with a
missing directory without triggering a process exit.

**Recommendation:** Replace `sys.exit(1)` with:
- `return None` and handle `None` in `main()`;
- or raise `ValueError("run directory not found: {run_dir}")` (callable).

---

### OPS-003 | P2 | MEDIUM | vbb-status-dashboard.py — temporal_warnings duplicates temporal_notes

**File:** `tools/vbb-status-dashboard.py` — `gather_status()`

**Finding:** `temporal_notes` is populated when temporal provenance is absent.
`temporal_warnings` is set to `[]` when provenance is present, and otherwise
equals `temporal_notes`. This means the dashboard displays the same information
in two different fields, and the "warnings" field does not add value beyond
what "notes" already provides.

```python
# gather_status() returns:
"temporal_notes": get_temporal_notes(repo),
"temporal_warnings": [] if temporal_provenance_present(repo) else get_temporal_notes(repo),
```

**Impact:** Minor cognitive noise. The dashboard shows duplicate temporal
provenance information under two different labels.

**Recommendation:** Remove `temporal_warnings` field entirely and always use
`temporal_notes` (with an appropriate label in the dashboard output).
Or rename `temporal_warnings` to `temporal_flags` and only populate it
when there is an actionable operational concern.

---

## Passed Checks

| Check | Result |
|-------|--------|
| Contract lint | 0 errors, 63/63 valid |
| Architecture lint | 0 errors, 7 blocks valid |
| Pytest suite | 81/81 passed |
| Local CI | 8/8 checks passed |
| GitHub CI | architecture lint + pytest covered |
| Contract runtime --all --dry-run | 44 PASS · 17 PARTIAL · 2 BLOCKED (expected) |
| Loop closure (latest run) | PASS (STRUCTUREE, 4 phases verified) |
| Phase router | 63 contracts indexed, routing clean |
| Status dashboard | verdict=PARTIAL, 63 skills, 63 contracts, 8 test suites |
| vbb-index | 338 entries, 340k tokens est., auto-rebuild on stale |
| AUDIT_STATUS.md | active, up-to-date with full risk register |

---

## Known Accepted Risks (unchanged)

| ID | Status | Note |
|----|--------|------|
| IMPL-002 | Mitigating | Formal runtime executor not yet implemented |
| SYNERGY-004 | Mitigating | setup.sh monolith (hardened, still long) |
| SYNERGY-005 | Mitigating | Governance duplication across files |
| LANG-001 | Accepted | 10 SKILL.md still have FR body content |
| LANG-002 | Accepted | Prompts contain FR narrative (human-facing by design) |

---

## Unknowns / Open Questions

- No audit of the contract runtime's actual executor path (dry-run stubs used).
  Full execution path needs a live run to validate.
- No audit of backup/restore for audit memory (`docs/audits/`, `docs/runs/`).
  These are versioned but not backed up separately.
- No audit of actual pre-commit hook behavior (only the installer is tested).

---

## Summary

Vibebackbone is robust at its current scope. The 3 findings above are bounded
operational concerns, not structural defects. No P0 found. No systemic risk
identified.

The two P2 findings (OPS-002, OPS-003) are quality-of-implementation improvements.
OPS-001 is the only actionable gap that could produce a false-positive closure
in production conditions.

---

*Audit: 2026-05-28 · 16:25 UTC · local agent · no code modified*