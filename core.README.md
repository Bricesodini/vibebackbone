# core.README.md — VBB Core sentinel

This repository is VBB Core, the runtime-neutral framework shared by the Pi,
OpenCode, Codex and Claude Code adapters.

## What lives here (Core canon)

- `skills/`, `prompts/`, `tools/vbb-*.py`, `tests/`, `scripts/hooks/`
- `docs/ARCHITECTURE.md`, `docs/RELATIONS.md`, `docs/DISTRIBUTIONS.md`, `docs/templates/`, `docs/adr/0001-0004` (Core ADRs)
- `AGENTS.md`, `README.md`, `GUIDE.md`, `CONVENTIONS.md`, `PILOTAGE.md`
- `setup.sh` (routeur, ~675 LOC) + `setup-lib.sh` (helpers) + `core/setup.sh` (universal symlinks)
- `distributions/<name>/setup.sh` — distribution code (per-provider glue, **not** Core canon)

## What does NOT live here (Distribution-only)

- **Distribution runtime** (outside the repo): `~/.claude/`, `~/.codex/`,
  `~/.pi/`, `~/.config/opencode/` — generated or populated by the corresponding
  `distributions/<name>/setup.sh`, never in this repo
- `providers/` — reserved for future templates (currently contains only `templates/example-consumer-repo/`)

## Status

Active. Core is the current state of the repo. `setup.sh` routes to four
distribution-level adapters; `setup-lib.sh` holds shared helpers. Hermes/Cody
was retired by ADR 0025.

## See also

- `docs/DISTRIBUTIONS.md` — canonical definition of Core vs Distribution code vs Distribution runtime
- `distributions/README.md` — distribution catalog and "how to add a distribution"
- `docs/DEPLOYMENT.md` §3bis — Setup architecture (routeur + helpers + per-dist files)
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
