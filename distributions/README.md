# distributions/ — VBB Core distributions catalog

This folder hosts operational declinations of VBB Core for specific agent
runtimes. **Distribution code** lives in this repo (in `distributions/<name>/`);
**distribution runtime** (settings and generated state) lives outside the repo
under `~/.claude/`, `~/.codex/`, `~/.pi/` or `~/.config/opencode/`.

## Mechanism (how to add a new distribution)

The post-Setup-Split procedure (replaces the pre-split "add a deployment
block in `setup.sh`" approach):

1. Create `distributions/<name>/` with at least:
   - `setup.sh` exposing `<name>_install` (sourced by the root `setup.sh`).
   - `README.md` pointing to Core canon and the new distribution's purpose.
2. Optionally add `distributions/<name>/SYSTEM.md` or `CLAUDE.md`
   (provider-specific runtime / governance overrides).
3. Add a routeur line in the root `setup.sh`:
   ```bash
   source "$REPO_ROOT/distributions/<name>/setup.sh"
   <name>_install
   ```
4. If the distribution needs shared helpers, add them to `setup-lib.sh`
   (helpers currently in setup-lib.sh: `relpath`, `_realpath`,
   `_is_vbb_symlink`, `needs_python`, `backup_file`, `symlink_if_absent`,
   `generate_prompt_commands`).
5. Document the decision in `docs/DISTRIBUTIONS.md` §Decisions log and
   create a new ADR if the structural change is non-trivial.

## Active

- `claude/` — Claude Code distribution (settings.json + CLAUDE.md block + 26 prompt commands)
- `codex/` — Codex distribution (compiled AGENTS.md block with VBB:START/END markers)
- `opencode/` — OpenCode distribution (opencode.json instructions + 26 prompt commands)
- `pi/` — Pi distribution (symlinks AGENTS + SYSTEM + 26 prompts)

## Reserve

- `examples/` — for future micro-clients, templates, or example
  distributions (see `distributions/examples/README.md`)

## Status

Setup Split is complete. The four supported distributions own their own
`setup.sh`, sourced by the root routeur. Hermes/Cody was retired by ADR 0025.
See
[`docs/audits/2026-06-14_1800_setup-split-migration-audit/`](../../docs/audits/2026-06-14_1800_setup-split-migration-audit/)
for the migration audit (verdict: DONE).

## See also

- `docs/DISTRIBUTIONS.md` — canonical definition of Core vs Distribution
- `AGENTS.md` Critical Rule #11 (propagation rules) and #12 (Core↔Dist impact check)
- `core.README.md` — Core sentinel
- `docs/DEPLOYMENT.md` §3bis — Setup architecture (routeur + helpers + per-dist files)
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — the decision
