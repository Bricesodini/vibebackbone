# distributions/hermes/ — Hermes/Cody distribution

The currently active distribution of VBB Core for the Hermes agent runtime,
with Cody as the orchestrator.

## What belongs here (future state)

- `install/INSTALL.md` (← current `docs/hermes/INSTALL.md`)
- `verify/verify.sh` (← current `scripts/hermes/verify.sh`)
- `proxy/` (← current `tools/proxy/`, 17 files)
- `proxy/adr/` (← current `docs/adr/0006-0012`, 7 ADRs)
- `bypass-lint/` (← current `tools/vbb-bypass-lint.py` + `tools/vbb-bypass-lint/`)
- `profiles-template/` (← current `providers/templates/example-consumer-repo/`)
- `docs/` (← current `docs/proxy/`)

## What does NOT belong here

- `~/.hermes/profiles/vbb-*/SOUL.md` — these stay in the runtime, not in the repo
- `skills/`, `prompts/`, `tools/vbb-*.py` — Core canon, not duplicated

## Current state (Phase 1 = this run)

`distributions/hermes/` is EMPTY (sentinel only). The 7 source locations
above are still in their current positions. Phases 2-3 (gated on Brice
accepting ADR 0013) will migrate them. Until then, this distribution
behaves identically to its current state — no behavioral change.

## Status

Placeholder. Sentinel created, migration pending.

## See also

- `docs/hermes/INSTALL.md` — current install doc (will move Phase 2)
- `scripts/hermes/verify.sh` — current verify (will move Phase 3)
- `tools/proxy/` — current proxy (will move Phase 3)
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
- `docs/DISTRIBUTIONS.md` §Hermes/Cody
