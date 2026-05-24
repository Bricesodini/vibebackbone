# Changelog

All notable changes to vibebackbone are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-rc.1] — 2026-06-13

### Added

- **62 skills** covering readiness (5), structure (16), audits (12), consolidation (1), front-end (10), and transverse (13) — each with standardized SKILL.md and CONTRACT.yaml
- **32 prompts** (7 canonical + 24 specialized + 1 router) for session entrypoints across all 7 agentic phases
- **Full contract coverage**: 62/62 CONTRACT.yaml files with events, gates, routing, state_policy, and limits defined
- **Contract linter** (`vbb-contract-lint.py`): validates all 62 contracts against schema in <1s
- **Contract runtime** (`vbb-contract-runtime.py`): dry-run execution of contracts with gate evaluation
- **Text index** (`vbb-index.py`): 287 entries, ~291K tokens indexed for targeted retrieval
- **Status dashboard** (`vbb-status-dashboard.py`): terminal and JSON status output for repo state
- **Context compactor** (`vbb-context-compactor.py`): run summarization for context handoff
- **Loop closure checker** (`vbb-loop-closure-check.py`): validates run artifacts against voie requirements
- **Project initializer** (`vbb-project-init.py`): bootstrap governance files for new projects
- **4 agentic routes**: FAST-ZERO, FAST-MINIMAL, FAST-STANDARD, STRUCTURED, AUDIT, CLOSEOUT with clear triage rules
- **7-phase protocol**: INTAKE → AUDIT → DECISION → PLAN → EXECUTION → REVIEW → CLOSEOUT with named artifacts per phase
- **Token economy architecture**: 5-layer boot model (L0–L4) reducing boot context from ~19K to ~2.5K tokens (87% reduction)
- **Agent-facing EN harmonization**: all 62 SKILL.md and 62 CONTRACT.yaml machine-facing fields in English
- **7 governance files**: CONTEXT.md, AGENTS.md, SYSTEM.md, CLAUDE.md, PILOTAGE.md, SESSION_RULES.md, MEMORY_AND_HANDOFF.md
- **7 test suites** with 69 tests covering contracts, loop closure, portability, project init, index, dashboard, and context compaction
- **2 GitHub workflows**: smoke (install test) and contracts (lint + runtime + test)
- **Self-auditing capability**: 17 audit reports produced using vibebackbone's own skills
- **setup.sh**: single-command install for Claude Code, Codex, Pi, OpenCode, and Cursor

### Changed

- **Boot context**: reduced from ~19K tokens to ~2.5K tokens (87% reduction) via @import compilation and L0–L4 layer architecture
- **Contract coverage**: expanded from 22/58 (38%) to 62/62 (100%) across 9 contractualization runs
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