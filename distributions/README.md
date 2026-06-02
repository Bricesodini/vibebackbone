# distributions/ — VBB Core distributions catalog

This folder hosts operational declinations of VBB Core for specific agent
runtimes (Hermes/Cody, Pi, future Codex/OpenCode).

## Mechanism (generic, 5 steps)

1. Create `distributions/<name>/`.
2. Add `distributions/<name>/README.md` pointing to Core canon.
3. Optionally add `distributions/<name>/SYSTEM.md` (runtime overrides).
4. Add a deployment block in `setup.sh` (multi-provider installer).
5. Document the decision in `docs/DISTRIBUTIONS.md` §Decisions log and
   in a new ADR if the structural change is non-trivial.

## Active

- `hermes/` — currently the active distribution (see `distributions/hermes/README.md`)

## Anticipated

- `pi/` — anticipation, root `SYSTEM.md` and `setup.sh` already deploy
  to `~/.pi/agent/SYSTEM.md` (see `distributions/pi/README.md`)

## Reserve

- `examples/` — for future micro-clients, templates, or example
  distributions (see `distributions/examples/README.md`)

## Status

Placeholder. This folder is created in ADR 0013 Phase 1; subfolders are
populated in subsequent phases (2-5) gated on Brice's ADR acceptance.

## See also

- `docs/DISTRIBUTIONS.md` — canonical definition of Core vs Distribution
- `AGENTS.md` Critical Rule #11 — propagation rules
- `core.README.md` — Core sentinel
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
