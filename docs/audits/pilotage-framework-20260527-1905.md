---
audit_type: pilotage_framework
date: 2026-05-27
auditor: codex
route: AUDIT
scope: vibebackbone governance, routing, contract runtime, status artifacts
verdict: PARTIAL
---

# Pilotage Framework Audit — Vibebackbone

## Executive Summary

Verdict: PARTIAL.

The Vibebackbone piloting frame is strong as a documented operating grammar: routes are visible, session discipline is explicit, audit artifacts exist, and the repo has a substantial contract/tooling layer. The main weakness is no longer lack of governance; it is divergence between declared governance and executable enforcement.

The most critical issues are:

1. `skills/INDEX.yaml` indexes only 43 contracts while 62 `CONTRACT.yaml` files exist, so router/runtime coverage is lower than the 100% status claimed by dashboard documents.
2. The phase router produces false positives for unknown or unindexed work because agent and neutral phase scores are enough to create candidates without trigger matches.
3. Two pilotage sources both claim canonical authority: `docs/PILOTAGE.md` v2.2 and `skills/vibebackbone/docs/PILOTAGE.md` v2.1.
4. The live workspace date is 2026-05-27, but central status and run artifacts are dated 2026-06-10 to 2026-06-13, weakening temporal trust.
5. The recommended search workflow is currently broken because `.vbb/index/manifest.json` is absent.
6. Persistent debt/status files are stale against current repo facts.

## Scope And Evidence

Files and tools inspected:

- `docs/CONTEXT.md`
- `docs/PILOTAGE.md`
- `skills/vibebackbone/docs/PILOTAGE.md`
- `docs/AUDIT_STATUS.md`
- `docs/TECH_DEBT.md`
- `docs/ACTIVITY_LOG.md`
- `skills/INDEX.yaml`
- `tools/vbb-phase-router.py`
- `tools/vbb-contract-runtime.py`
- `tools/vbb-contract-lint.py`
- `tools/vbb-status-dashboard.py`
- `docs/router/ROUTER_MATRIX.md`
- `README.md`
- `tests/`

Validation commands:

```bash
date '+%Y-%m-%d %H:%M:%S %Z'
python tools/vbb-status-dashboard.py --json
python tools/vbb-contract-lint.py
python tools/vbb-contract-runtime.py run --all --dry-run
pytest -q
python tools/vbb-phase-router.py "nonexistent query xyz 123" --phase phase_99 --agent claude-code --strict
python tools/vbb-index.py search "pilotage canonical source truth"
python tools/vbb-loop-closure-check.py 2026-06-13_1700_release-candidate-prep
```

Observed results:

- Local date: `2026-05-27 19:01:51 CEST`.
- Status dashboard: `skills=62`, `contracts=62`, `contract_coverage=1.0`.
- Contract linter: `0 error(s) found`.
- Contract runtime all: `25 PASS | 16 PARTIAL | 2 BLOCKED/FAIL`, across 43 indexed contracts.
- Pytest: `68 passed, 1 failed`.
- Index search: `Error: index not found. Run 'python tools/vbb-index.py build' first.`
- Loop closure check on latest listed run: PASS when called with run id.

## Findings

### P1 — Contract Coverage Is Overstated For Runtime Routing

Evidence:

- There are 62 `skills/*/CONTRACT.yaml` files.
- `skills/INDEX.yaml` contains only 43 entries.
- `tools/vbb-contract-runtime.py run --all --dry-run` executes only those 43 indexed entries.
- Missing from `skills/INDEX.yaml`: 19 contracts, including all front-pipeline skills, multiple phase-1 detectors, `t-vbb-docker-generate`, and `vibebackbone`.

Impact:

- The documented `62/62 contract coverage` is true for file presence, but false for the executable routing/runtime layer.
- Any agent relying on the router/runtime may silently ignore 19 declared skills.
- The status dashboard can report 100% coverage while the runtime exercises only 69% of contracts.

Recommended fix:

- Make `skills/INDEX.yaml` exhaustive for all 62 contracts.
- Add a linter check: `INDEX.yaml` entries must equal the set of `skills/*/CONTRACT.yaml`.
- Make status dashboard distinguish `contract files`, `indexed contracts`, and `runtime-routable contracts`.

### P1 — Router Can Return False Positives Without Trigger Match

Evidence:

- `tools/vbb-phase-router.py` scores `0.5` when no phase is specified and `1.0` when the agent is compatible.
- Candidate threshold is `>= 0.5`, so compatibility alone can create a route.
- Test result: `pytest -q` fails on `test_phase_router_unknown_phase`; unknown query returned `0-vbb-scope-freeze` in non-strict mode.
- Strict mode shows ambiguity rather than clean no-route for unknown context.

Impact:

- The central promise "classify a task into the right path" is not mechanically safe.
- Unknown or unindexed requests can be routed to unrelated skills.
- Because many skills support the same agents, the router rewards generic compatibility more than semantic relevance.

Recommended fix:

- Require `trigger_score > 0` for a candidate unless an explicit phase-only lookup mode is requested.
- Treat unknown phase as no-route, not as a soft mismatch.
- Add regression tests for unknown query, unindexed skill query, and phase-4/front-pipeline query.

### P1 — Canonical Pilotage Authority Is Ambiguous

Evidence:

- `docs/PILOTAGE.md` declares itself the "Canonical piloting entry point" and puts "This document" at hierarchy position 1.
- `skills/vibebackbone/docs/PILOTAGE.md` says it is the source of truth for the canonical catalog and prevails when a routing skill diverges.
- `skills/vibebackbone/SKILL.md` requires the orchestrator to use `skills/vibebackbone/docs/PILOTAGE.md` as canonical.
- The two pilotage files diverge in version, date, route naming detail, and contract coverage.

Impact:

- Agents can legitimately pick different "canonical" files depending on their entrypoint.
- Governance duplication is not just historical; it affects live routing authority.
- The older pilotage file contains stale coverage data (`22/58`) while claiming precedence for catalog routing.

Recommended fix:

- Declare one authority model explicitly:
  - `docs/PILOTAGE.md` = canonical short router for all agents.
  - `skills/vibebackbone/docs/PILOTAGE.md` = generated/detailed derivative, or archive.
- If both must remain, add a synchronization invariant and test that versions/counts/route names do not diverge.

### P2 — Temporal Traceability Is Unreliable In This Workspace

Evidence:

- Local clock: 2026-05-27.
- `docs/CONTEXT.md`, `docs/AUDIT_STATUS.md`, and latest run directories are dated 2026-06-13.
- Many central artifacts present a future state relative to the current runtime date.

Impact:

- Session resumption cannot tell whether "latest" means actual latest or imported/future-dated state.
- The audit dashboard may be treated as current even when its timestamps are not chronologically valid in this environment.
- Release readiness claims become hard to trust without a provenance note.

Recommended fix:

- Add a provenance policy for imported/generated future-dated artifacts.
- Add a dashboard warning when document dates exceed current system date.
- Add an `observed_at` field to audit/status updates distinct from artifact-internal dates.

### P2 — Recommended Search Workflow Is Broken By Default

Evidence:

- `docs/CONTEXT.md` recommends `python tools/vbb-index.py search "query"`.
- Running the command fails because the local `.vbb/index/manifest.json` does not exist.
- `.vbb/index` is not present in the workspace.

Impact:

- The context discipline model depends on targeted retrieval, but the advertised retrieval path fails on first use.
- Agents may fall back to broad `rg` scans or over-read the repo, increasing context load.

Recommended fix:

- Either build the index as part of setup/checks, or make `search` auto-build on missing index.
- Add a status dashboard field for `index_present`.
- Add CI/test coverage for "fresh clone search works or tells the user exactly what to run".

### P2 — Status And Debt Registers Are Stale Against Current Facts

Evidence:

- `docs/TECH_DEBT.md` still lists incomplete contract coverage as `22/58`, while the repo has 62 contract files.
- `docs/INDEX.md` lists `Skills (58)`.
- `SYSTEM.md` and `AGENTS.md` claim 32 prompts, while `find prompts -type f -name '*.md'` returns 33.
- `docs/AUDIT_STATUS.md` says tests are `69/69 pytest green`, while current pytest is `68 passed, 1 failed`.
- `docs/AUDIT_STATUS.md` lists `risks: []` through the dashboard extractor because it only recognizes `R-*` table rows, not current `SYNERGY-*`, `LANG-*`, `REL-*` ids.

Impact:

- The dashboard and status files no longer form a dependable restart surface.
- Risk visibility depends on identifier format rather than semantic table structure.
- "No P0/P1" and "ready" claims are harder to assess because the visible state is mixed.

Recommended fix:

- Normalize risk IDs or update `tools/vbb-status-dashboard.py` to parse all risk ids in the current table.
- Refresh `docs/INDEX.md`, `SYSTEM.md`, `AGENTS.md`, and `docs/TECH_DEBT.md` from measured counts.
- Add a count-consistency check covering skills, contracts, indexed contracts, prompts, tests, and latest run dates.

## Strengths

- The route model is understandable and compact in `docs/PILOTAGE.md`.
- The repo has clear document hierarchy and session artifacts.
- The linter catches many schema-level contract issues.
- Loop closure is mechanically checkable and passes on the latest listed run when called correctly.
- The audit history is rich enough to explain many past decisions.

## Recommended Remediation Order

1. Fix `skills/INDEX.yaml` exhaustiveness and add a linter gate.
2. Fix router scoring so semantic trigger match is required.
3. Resolve the two-canonical-pilotage problem.
4. Refresh status/debt/count documents from measured state.
5. Repair or auto-build the local search index.
6. Add temporal provenance checks for future-dated artifacts.

## Final Verdict

PARTIAL.

The Vibebackbone pilotage framework is conceptually mature but operationally under-enforced. The weakest point is the gap between declared governance and the tools that are supposed to make it reliable. Until index exhaustiveness, router false positives, and canonical-source ambiguity are fixed, the framework should not claim fully reliable autonomous piloting.
