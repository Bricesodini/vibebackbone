# Changelog

All notable changes to vibebackbone are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] — 2026-07-31

## [1.1.0-rc.1] — 2026-07-31

### Release candidate

- Establishes the single release candidate identity for the Backbone Know
  foundation remediation.
- The candidate commit SHA is recorded in the run evidence carrier after the
  technical subject commit; it is not self-embedded in that commit.
- The future annotated tag is `v1.1.0-rc.1`; it must peel to the candidate
  commit exactly and must not be created before independent revalidation.

### Added

- **Setup Split (Phase 0+1 → 2F)**: monolithique `setup.sh` (807 LOC) extrait
  en 7 fichiers (routeur `setup.sh` ~675 LOC + `setup-lib.sh` 209 LOC + `core/setup.sh`
  116 LOC + 4 `distributions/<name>/setup.sh` 74-118 LOC). Phases 2A (core),
  2B (pi), 2C (claude), 2D (codex), 2E (opencode).
- **Phase 2 RUN 1 contractualisation** : `tools/vbb-loop-closure-check.py` étendu
  avec 3 validations opt-in (claims evidence, plan sections, test audit) ;
  templates `docs/templates/ADR.md.template`, `POC.md.template`,
  `INTEGRATION_GATE.md.template` ; pre-commit framework gate étendu.
- **Mode transition keywords** : `tools/vbb-gate-check.py` détecte les transitions
  implicites de mode (deploy/codename/exit) et bloque si `can_code_start=false`.
- **Dashboard review-tier advisory** : `tools/vbb-status-dashboard.py --review-tier
  --json` (T1-T8, opt-in, `blocking=false`, jamais gate/enforce).
- **P0-4 Review Matrix POC** : 8 tiers calibrés sur 8 runs historiques
  (100% accuracy), `tools/vbb-review-threshold-poc.py` (stdlib only).

### Changed

- **Test count** : 69 → **135 passed, 3 skipped (138 collected)**.
- **Skill count** : 63 → **64** (l'orchestrateur `skills/vibebackbone/` est
  désormais compté). Compteur déterministe : `find skills -name SKILL.md | wc -l`.
- **Prompt count** : inchangé à **33** (7 canonical + 25 specialized + 1 router).
- **VBB Core vs Distribution** : séparation explicite entre *distribution code*
  (in repo, `distributions/<name>/`) et *distribution runtime* (outside repo).
  Patcher `AGENTS.md` Critical Rule #12,
  `README.md` tableau, `docs/DISTRIBUTIONS.md` §3.
- **CI workflows** : `vbb-contracts.yml` étendu avec 24 nouveaux tests ;
  `smoke` workflow validé sur 5 phases de split.

### Fixed

- **AUDIT_STATUS.md QOA-001 P1** : Core/Distribution boundary contradiction —
  `README.md`, `AGENTS.md` et `core.README.md` ne disent plus que les
  distributions vivent "outside the repo".
- **CHANGELOG.md compteurs** : synchronisés sur 64 skills / 33 prompts /
  133 tests passed, 1 skipped après retrait des suites Hermes/Cody.

### Removed

- **Hermes/Cody support** (ADR 0025): distribution, proxy, bypass-lint,
  install/verify assets, provider route and exclusive tests removed. Official
  support is limited to Pi, OpenCode, Codex and Claude Code. Historical
  runs/audits remain available and no external `~/.hermes/` state is touched.

## [1.0.0-rc.1] — 2026-06-13

### Added

- **63 skills** covering readiness (6), structure (16), audits (12), consolidation (1), front-end (10), and transverse (13) — each with standardized SKILL.md and CONTRACT.yaml
- **33 prompts** (7 canonical + 25 specialized + 1 router) for session entrypoints across all 7 agentic phases
- **Full contract coverage**: 63/63 CONTRACT.yaml files with events, gates, routing, state_policy, and limits defined
- **Contract linter** (`vbb-contract-lint.py`): validates all 63 contracts against schema in <1s
- **Contract runtime** (`vbb-contract-runtime.py`): dry-run execution of contracts with gate evaluation
- **Text index** (`vbb-index.py`): 287 entries, ~291K tokens indexed for targeted retrieval
- **Status dashboard** (`vbb-status-dashboard.py`): terminal and JSON status output for repo state
- **Context compactor** (`vbb-context-compactor.py`): run summarization for context handoff
- **Loop closure checker** (`vbb-loop-closure-check.py`): validates run artifacts against voie requirements
- **Project initializer** (`vbb-project-init.py`): bootstrap governance files for new projects
- **4 route families + MVP START gate**: FAST (ZERO/MINIMAL/STANDARD), STRUCTURED, AUDIT, CLOSEOUT, with MVP readiness before from-zero implementation
- **7-phase protocol**: INTAKE → AUDIT → DECISION → PLAN → EXECUTION → REVIEW → CLOSEOUT with named artifacts per phase
- **Token economy architecture**: 5-layer boot model (L0–L4) reducing boot context from ~19K to ~2.5K tokens (87% reduction)
- **Agent-facing EN harmonization**: all 63 SKILL.md and 63 CONTRACT.yaml machine-facing fields in English
- **7 governance files**: CONTEXT.md, AGENTS.md, SYSTEM.md, CLAUDE.md, PILOTAGE.md, SESSION_RULES.md, MEMORY_AND_HANDOFF.md
- **7 test suites** with 69 tests covering contracts, loop closure, portability, project init, index, dashboard, and context compaction
- **2 GitHub workflows**: smoke (install test) and contracts (lint + runtime + test)
- **Self-auditing capability**: 17 audit reports produced using vibebackbone's own skills
- **setup.sh**: single-command install for Claude Code, Codex, Pi and OpenCode

### Changed

- **Boot context**: reduced from ~19K tokens to ~2.5K tokens (87% reduction) via @import compilation and L0–L4 layer architecture
- **Contract coverage**: expanded from 22/58 (38%) to 63/63 (100%) across 9 contractualization runs
- **SKILL.md language**: harmonized from mixed FR/EN to consistent EN for agent-facing content across 4 language EN runs (18A/18B/18C/20C)
- **CONTRACT.yaml descriptions**: translated all FR event.reason, gate.reason, and blocking_conditions.message fields to EN (44 contracts modified, 73 translations)
- **Test infrastructure**: converted all 7 test files from custom `test(name, fn)` runner to pytest-compatible `test_*` function names with `__main__` fallback — 69/69 tests green
- **Dashboard EN fix**: `extract_next_action` now matches both FR and EN field names (`prochaine action` / `Next action`)
- **CI script**: added pytest step (7/7), documented WARN behavior, renumbered steps

### Fixed

- **Pytest fixtures**: resolved 7/7 `fixture 'name' not found` errors by converting custom test runners to pytest-compatible function names
- **Loop closure frontmatter**: fixed global-evaluation-audit run to pass closure invariant (added voie, agent, timestamps, 02_AUDIT.md, 03_DECISION.md)
- **SYNERGY risks**: 7/12 resolved (R-001 R-002 R-003 R-006 R-007 R-010 R-012), 5/12 mitigated (R-004 R-005 R-008 R-009 R-021)

### Security

- PyYAML pinned to >=6.0,<7.0
- GitHub workflow permissions set to `contents: read` only
- No P0/P1 vulnerabilities identified in self-audit triptych (security, tech-debt, CI)

### Audit Trail

- 43+ runs with 92% closeout rate (37/40 since protocol adoption)
- 17 audit reports in `docs/audits/`
- 3 auto-audit runs (security, tech-debt, CI) + synthesis
- Global evaluation audit (composite score: 7.4/10)

[1.0.0-rc.1]: https://github.com/bricesodini/vibebackbone/releases/tag/v1.0.0-rc.1
