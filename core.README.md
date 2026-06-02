# core.README.md — VBB Core sentinel

This repository is VBB Core, the agent-agnostic method (skills, prompts,
governance, tools, canonical docs).

## What lives here (Core canon)

- `skills/`, `prompts/`, `tools/vbb-*.py`, `providers/`, `tests/`, `scripts/hooks/`
- `docs/ARCHITECTURE.md`, `docs/RELATIONS.md`, `docs/DISTRIBUTIONS.md`, `docs/templates/`, `docs/adr/0001-0004` (Core ADRs)
- `AGENTS.md`, `README.md`, `GUIDE.md`, `CONVENTIONS.md`, `PILOTAGE.md`
- `setup.sh` — multi-provider installer (deploys to `~/.agents/`, `~/.pi/`, `~/.codex/`, `~/.claude/`)

## What does NOT live here (Distribution-only)

- `distributions/` — operational declinations for specific agent runtimes (ADR 0013)
- `~/.hermes/profiles/vbb-*/` — Hermes runtime state, never in the repo
- `distributions/hermes/proxy/`, `distributions/hermes/install/INSTALL.md`, `distributions/hermes/verify/verify.sh`, `distributions/hermes/bypass-lint/` — moved out of Core by ADR 0013 Phases 2-3
- `docs/adr/0006-0012` — proxy-distribution ADRs, currently UNTRACKED, moving in Phase 3
- `.pi/`, `.claude/` — distribution-specific config (moving in Phase 4)

## Status

Active. Core is the current state of the repo. The 6 sentinels from
ADR 0013 Phase 1 are additive only — no file has been moved or renamed.

## See also

- `docs/DISTRIBUTIONS.md` — canonical definition
- `distributions/README.md` — distribution catalog
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
