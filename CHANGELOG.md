# Changelog

All notable changes to vibebackbone are documented here.

Format: [Semantic Versioning](https://semver.org/)

---

## [1.0.0] — 2026-05-16

### Added

- 57 orthogonal skills across phases [0], [1], [2], [3], [4], [t]
- 24 session prompts covering full operational lifecycle
- `AGENTS.md` — canonical operational grammar (triage, escalation, audit sequence)
- `SYSTEM.md` — Pi runtime behavior and planning protocol
- `CLAUDE.md` — Claude Code entry point with triage table
- `skills/vibebackbone/docs/PILOTAGE.md` — full governance model v2.0
- `setup.sh` — global installer for `~/.agents/skills/`
- MIT License, CONTRIBUTING.md, CODE_OF_CONDUCT.md
- GitHub issue and PR templates

### Skills by phase

**Phase [0] — Readiness (2 skills)**
- `0-vbb-scope-freeze` — Validate scope before audit
- `0-vbb-audit-readiness` — Gatekeeper for phase [1]

**Phase [1] — Structure (5 skills)**
- `1-vbb-dependency-mapper`, `1-vbb-conventions`, `1-vbb-tech-debt`, `1-vbb-formatter`, `1-vbb-code-janitor`

**Phase [2] — Deep audits (8 skills)**
- `2-vbb-security`, `2-vbb-api-auditor`, `2-vbb-db-robustness`, `2-vbb-data-integrity`
- `2-vbb-ops`, `2-vbb-ci`, `2-vbb-impact-analyzer`, `2-vbb-test-coverage-mapper`

**Phase [3] — Consolidation (1 skill)**
- `3-vbb-risk-register`

**Phase [4] — Enhancement**
- UX, performance, and advanced skills

**Phase [t] — Transverse**
- Session handoff, project init, docker, deploy, and utility skills

---

## [0.x] — 2026 (pre-release)

Initial development of the vibebackbone governance system.
