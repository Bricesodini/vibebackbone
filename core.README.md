# core.README.md — VBB Core sentinel

This repository is VBB Core, the agent-agnostic method (skills, prompts,
governance, tools, canonical docs).

## What lives here (Core canon)

- `skills/`, `prompts/`, `tools/vbb-*.py`, `tests/`, `scripts/hooks/`
- `docs/ARCHITECTURE.md`, `docs/RELATIONS.md`, `docs/DISTRIBUTIONS.md`, `docs/templates/`, `docs/adr/0001-0004` (Core ADRs)
- `AGENTS.md`, `README.md`, `GUIDE.md`, `CONVENTIONS.md`, `PILOTAGE.md`
- `setup.sh` (routeur, ~356 LOC) + `setup-lib.sh` (helpers) + `core/setup.sh` (universal symlinks)
- `distributions/<name>/setup.sh` — distribution code (per-provider glue, **not** Core canon)

## What does NOT live here (Distribution-only)

- `distributions/hermes/proxy/`, `distributions/hermes/install/INSTALL.md`, `distributions/hermes/verify/verify.sh`, `distributions/hermes/bypass-lint/` — Hermes distribution code (per ADR 0013 Phases 2-3)
- `distributions/hermes/proxy/adr/0006-0012` — proxy-distribution ADRs (per ADR 0013 Phase 2)
- **Distribution runtime** (outside the repo): `~/.hermes/profiles/vbb-*/`, `~/.claude/`, `~/.codex/`, `~/.pi/`, `~/.config/opencode/` — generated/populated by the corresponding `distributions/<name>/setup.sh`, never in this repo
- `providers/` — reserved for future templates (currently contains only `templates/example-consumer-repo/`)

## Status

Active. Core is the current state of the repo. Setup Split (Phase 0+1 → 2F,
2026-06-13/14) complete: `setup.sh` is a routeur that sources 5
distribution-level `setup.sh` files; `setup-lib.sh` holds shared helpers.

## See also

- `docs/DISTRIBUTIONS.md` — canonical definition of Core vs Distribution code vs Distribution runtime
- `distributions/README.md` — distribution catalog and "how to add a distribution"
- `docs/DEPLOYMENT.md` §3bis — Setup architecture (routeur + helpers + per-dist files)
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
