# distributions/pi/ — Pi distribution

The currently active distribution of VBB Core for the Pi agent runtime.
**ACTIVE** as of ADR 0013 Phase 4 (2026-06-13). Pi-specific runtime files
live here; a symlink at the repo root preserves runtime compatibility with
Pi's `mode projet` and with `setup.sh` (which deploys
`~/.pi/agent/SYSTEM.md` as a symlink).

## What lives here (migrated in ADR 0013 Phase 4)

- `SYSTEM.md` (← was `SYSTEM.md` at root, tracked `git mv`; root is now a
  relative symlink → `distributions/pi/SYSTEM.md`).
- `overrides.template.json` (← was `.pi/subagent-overrides.json`, untracked
  `mv`; the `.pi/` directory is empty and remains gitignored for future
  Pi-local state). Consumed by `tools/vbb-llm-healthcheck.py` (patched
  in Phase 4 to point at the new path).

## What does NOT belong here

- `~/.pi/agent/` (user-side Pi agent home, populated by `setup.sh`).
- `.pi/` (the gitignored directory at repo root — left intact for
  Pi-local session state).
- `tools/vbb-llm-healthcheck.py` — VBB Core tool, not distribution-owned;
  only its path *reference* was patched.

## What does NOT need to change

- `setup.sh` — already uses `$REPO_ROOT/SYSTEM.md` as a path, and the
  symlink at the root resolves transparently. No patch required.
- `AGENTS.md`, `GUIDE.md`, `CONVENTIONS.md`, `PILOTAGE.md` — VBB Core
  canon, untouched by Phase 4.

## Status

Active. 2 files live here as canonical sources of truth, 1 symlink at
the root preserves runtime compatibility, 1 Core tool (`vbb-llm-healthcheck.py`)
patched to read the new path. Phase 5 (final CI validation) is out of
scope for this run.

## See also

- `SYSTEM.md` (symlink at root → `distributions/pi/SYSTEM.md`)
- `distributions/README.md` — index of all distributions
- `docs/DISTRIBUTIONS.md` — canonical definition
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
- `setup.sh` (Pi deployment block, untouched)
