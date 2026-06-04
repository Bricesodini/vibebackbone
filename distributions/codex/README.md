# distributions/codex/ — Codex distribution

The currently active distribution of VBB Core for the Codex agent
runtime. **ACTIVE** as of ADR 0013 Phase 4 (2026-06-13). Codex-specific
runtime files live here; a symlink at the repo root preserves runtime
compatibility with Codex's compiled `AGENTS.md` block.

## What lives here (migrated in ADR 0013 Phase 4)

- `setup.sh` (← was inlined §6 "Codex — compiled AGENTS.md" block in the
  monolithic `setup.sh`; extracted verbatim in Phase 2D — no refactor,
  no content change). The routeur at root sources this file via
  `distributions/codex/setup.sh`.

## What does NOT belong here

- `~/.codex/` (user-side Codex home, populated by `setup.sh`).
- `AGENTS.md` symlink at the root — kept as symlink for Codex's
  `@import` compatibility.

## What does NOT need to change

- `distributions/codex/setup.sh` globals (`REPO_ROOT`, `HOME`,
  `AGENTS_SRC`, `CODEX_AGENTS`, `FORCE_GOVERNANCE`, `SYSTEM_AVAILABLE`)
  are already documented in the file header; no patch required.
- VBB Core files (`GUIDE.md`, `CONVENTIONS.md`, `PILOTAGE.md`) — unchanged.

## Status

Active. 1 file lives here (`setup.sh`). Runtime side (`~/.codex/`)
populated by the routeur; root-level `AGENTS.md` symlink preserved.
