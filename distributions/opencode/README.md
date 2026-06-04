# distributions/opencode/ — OpenCode distribution

The currently active distribution of VBB Core for the OpenCode agent
runtime. **ACTIVE** as of ADR 0013 Phase 4 (2026-06-13). OpenCode-specific
runtime files live here; the routeur at root sources this file via
`distributions/opencode/setup.sh`.

## What lives here (migrated in ADR 0013 Phase 4)

- `setup.sh` (← was inlined §8+§9 "OpenCode" blocks in the monolithic
  `setup.sh`; extracted verbatim in Phase 2E — no refactor, no content
  change). Manages `opencode.json` "instructions" field and prompt
  commands.

## What does NOT belong here

- `~/.config/opencode/` (user-side OpenCode home, populated by
  `setup.sh`).
- `opencode.json` at the user side — runtime-owned, untouched by
  Phase 2E.

## What does NOT need to change

- `distributions/opencode/setup.sh` globals (`REPO_ROOT`, `HOME`,
  `AGENTS_SRC`, `SYSTEM_SRC`, `OPENCODE_JSON`, `OPENCODE_COMMANDS`,
  `FORCE_GOVERNANCE`, `SYSTEM_AVAILABLE`) are already documented in
  the file header; no patch required.
- VBB Core files (`GUIDE.md`, `CONVENTIONS.md`, `PILOTAGE.md`) —
  unchanged.

## Status

Active. 1 file lives here (`setup.sh`). Runtime side
(`~/.config/opencode/`) populated by the routeur.
