# distributions/pi/ — Pi distribution (anticipated)

Anticipated distribution of VBB Core for the Pi agent runtime. **NOT YET
ACTIVE** — placeholder for future implementation (ADR 0013 Phase 4).

## Why anticipated

Pi is mentioned by root `SYSTEM.md` (Pi-specific frontmatter) and by
`setup.sh` (deploys `~/.pi/agent/SYSTEM.md` as a symlink). Current state
is minimal: a single `.pi/subagent-overrides.json` and a symlink in `setup.sh`.

## What would belong here (future state)

- `SYSTEM.md` (← current root `SYSTEM.md`, with symlink for compat)
- `overrides.template.json` (← current `.pi/subagent-overrides.json`)
- `install/` (future install doc), `verify/` (future verify script)

## Status

Placeholder. Created in ADR 0013 Phase 1; no migration yet. Phase 4 is
gated on Brice accepting ADR 0013.

## See also

- `SYSTEM.md` (root, current), `setup.sh` (Pi deployment block)
- `docs/DISTRIBUTIONS.md` — canonical definition
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
