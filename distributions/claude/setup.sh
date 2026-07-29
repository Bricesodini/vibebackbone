#!/bin/bash
# distributions/claude/setup.sh — Claude Code distribution installation.
#
# This file is sourced by the root setup.sh routeur. It is the
# THIRD distribution in the VBB installer (Claude = one of the 4 providers).
#
# Behavior is identical to the pre-Phase-2C inlined §3 + §4 + §5
# "Claude Code" blocks in setup.sh. Extracted verbatim.
#
# Globals expected from the caller (setup.sh):
#   REPO_ROOT, HOME
#   AGENTS_SRC, SYSTEM_SRC, PROMPTS_SRC
#   CLAUDE_SETTINGS, CLAUDE_MD, CLAUDE_COMMANDS
#   FORCE_GOVERNANCE, SYSTEM_AVAILABLE, PROMPTS_AVAILABLE
#
# Side effects (consumed by setup.sh summary):
#   CLAUDE_PROMPTS_OK, CLAUDE_PROMPTS_SKIP
#   CLAUDE_SKILLS_OK, CLAUDE_SKILLS_SKIP
#
# Helpers expected (from setup-lib.sh, sourced earlier in setup.sh):
#   needs_python, generate_prompt_commands

# ── Claude entry point ──────────────────────────────────────────────────────
claude_install() {
  claude_install_settings_json
  claude_install_claude_md_block
  claude_install_prompt_commands
  claude_install_skill_symlinks
}

# 1. Claude Code — settings.json — preserve user settings, do NOT
#    add a `skills` key (which Claude Code does NOT consume for
#    discovery). Discovery happens via ~/.claude/skills/<name>/SKILL.md.
#    See run `2026-07-30_0700_claude-skills-discovery-01` (scope
#    `CLAUDE-SKILLS-DISCOVERY-01`) for the rationale and the
#    fail-before reproduction.
claude_install_settings_json() {
  mkdir -p "$(dirname "$CLAUDE_SETTINGS")"
  if [ ! -f "$CLAUDE_SETTINGS" ]; then
    echo '{}' > "$CLAUDE_SETTINGS"
    echo "✓ Claude Code: settings.json created (empty)"
  else
    echo "✓ Claude Code: settings.json preserved (untouched — no longer patched)"
  fi
}

# 2. Claude Code — CLAUDE.md block — append/replace the vibebackbone block
claude_install_claude_md_block() {
  echo ""
  echo "Deploying governance (AGENTS.md + SYSTEM.md)..."

  mkdir -p "$HOME/.claude"
  touch "$CLAUDE_MD"

  if needs_python; then
    python3 - "$CLAUDE_MD" "$AGENTS_SRC" "$SYSTEM_SRC" "$SYSTEM_AVAILABLE" <<'PY'
import sys, re
path, agents_src, system_src, system_available = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
with open(path) as f:
    content = f.read()

system_available_flag = system_available.lower() == "true"

block_lines = ["\n# vibebackbone", f"@{agents_src}"]
if system_available_flag:
    block_lines.append(f"@{system_src}")
new_block = "\n".join(block_lines) + "\n"

pattern = r'(?:\n)?# vibebackbone\n(?:@[^\n]*\n)+'
if re.search(pattern, content):
    content = re.sub(pattern, new_block, content)
    with open(path, "w") as f:
        f.write(content)
    if system_available_flag:
        print("✓ Claude Code: AGENTS.md + SYSTEM.md reference updated")
    else:
        print("✓ Claude Code: AGENTS.md reference updated (SYSTEM.md missing)")
else:
    with open(path, "a") as f:
        f.write(new_block)
    if system_available_flag:
        print("✓ Claude Code: AGENTS.md + SYSTEM.md reference added")
    else:
        print("✓ Claude Code: AGENTS.md reference added (SYSTEM.md missing)")
PY
  else
    echo "⚠ Claude Code: python3 not found — CLAUDE.md patch skipped"
  fi
}

# 3. ~/.claude/commands/vbb-*.md — generate 26 prompt commands
claude_install_prompt_commands() {
  CLAUDE_PROMPTS_OK=0
  CLAUDE_PROMPTS_SKIP=0
  generate_prompt_commands "$CLAUDE_COMMANDS" "Claude prompts" "CLAUDE_PROMPTS_OK" "CLAUDE_PROMPTS_SKIP"
}

# 4. Claude Code — skill discovery via ~/.claude/skills/<name>/SKILL.md.
#
#    Claude Code discovers skills by scanning one directory per skill under
#    `~/.claude/skills/<skill-name>/`, each containing a `SKILL.md` file.
#    This is the canonical discovery mechanism and the only one Claude Code
#    actually consumes at session start (the historical `settings.json.skills`
#    key is NOT a discovery mechanism).
#
#    Behavior (see run `2026-07-30_0700_claude-skills-discovery-01` for the
#    rationale and acceptance criteria):
#
#    - enumerate canonical skills from `<REPO_ROOT>/skills/<name>/SKILL.md`
#    - for each, ensure `~/.claude/skills/<name>/SKILL.md` exists as a
#      symlink pointing at the canonical file (absolute path preferred
#      for diagnosability)
#    - idempotent: a second run is a no-op if the link is already correct
#    - fail-closed on collision: a user file or wrong-target link aborts
#      with an explicit error and a non-zero exit
#    - never silently overwrite a user file
#    - never follow a target that escapes the repository
#    - safe under repo paths containing spaces
#
#    Globals consumed:
#      REPO_ROOT, HOME
claude_install_skill_symlinks() {
  local skills_src="$REPO_ROOT/skills"
  local skills_dst="$HOME/.claude/skills"
  local ok=0
  local skip=0
  local fail=0

  if [ ! -d "$skills_src" ]; then
    echo "⚠ Claude Code: skills source directory missing: $skills_src"
    echo "  (skill symlinks skipped — fix REPO_ROOT and re-run)"
    CLAUDE_SKILLS_OK=0
    CLAUDE_SKILLS_SKIP=0
    return 0
  fi

  # Refuse to install if $skills_dst is a symlink. When $skills_dst is a
  # symlink into the source repo (e.g. a leftover `ln -s $REPO_ROOT/skills
  # ~/.claude/skills`), every $dst path resolves to a canonical source
  # file. The legacy-reconcile branch below (`cmp -s $dst $abs_src`) sees
  # the file as identical to itself, mv's it out of the repo, and
  # replaces it with a self-referencing symlink — corrupting the source
  # repo in ~2s for 60+ skills. Fail-closed with explicit recovery.
  # Reproduced 2026-07-28 on a VPS install (see hippo memory).
  if [ -L "$skills_dst" ]; then
    local dst_resolved
    dst_resolved="$(cd "$skills_dst" 2>/dev/null && pwd -P || echo '<unresolvable>')"
    echo "✗ Claude Code: '$skills_dst' is a symlink"
    echo "    resolves to: $dst_resolved"
    if [ "$dst_resolved" = "$skills_src" ]; then
      cat <<EOF
  Refusing to install: this would alias the source repo and CORRUPT
    $skills_src (canonical SKILL.md files would be moved to a backup
    dir and replaced by self-referencing symlinks).

  Fix (manual):
    rm '$skills_dst'
    mkdir -p '$skills_dst'
    bash setup.sh    # re-run

  If this symlink is intentional (e.g. shared directory layout), point
  it at a directory OUTSIDE the repo:
    rm '$skills_dst' && ln -s /some/path/outside/repo '$skills_dst'
EOF
    else
      cat <<EOF
  Refusing to install on a symlinked destination — Claude Code expects
    a real directory it owns. Fix:
    rm '$skills_dst' && mkdir -p '$skills_dst'
EOF
    fi
    CLAUDE_SKILLS_OK=0
    CLAUDE_SKILLS_SKIP=0
    return 1
  fi

  mkdir -p "$skills_dst"

  local skill_dir
  for skill_dir in "$skills_src"/*/; do
    [ -d "$skill_dir" ] || continue
    local name
    name=$(basename "$skill_dir")
    local src="$skill_dir/SKILL.md"
    local dst_dir="$skills_dst/$name"
    local dst="$dst_dir/SKILL.md"

    # Source must exist
    if [ ! -f "$src" ]; then
      echo "⚠ Claude Code: $src missing — skip '$name'"
      skip=$((skip + 1))
      continue
    fi

    # Refuse to recurse: if the source path is INSIDE $HOME/.claude/skills,
    # bail fail-closed (would create nested links).
    case "$src" in
      "$skills_dst"/*)
        echo "✗ Claude Code: source '$src' is inside destination '$skills_dst' — refuse to recurse"
        fail=$((fail + 1))
        continue
        ;;
    esac

    # Compute absolute source path
    local abs_src
    abs_src="$(cd "$(dirname "$src")" && pwd)/$(basename "$src")"

    # Destination directory collision handling
    if [ -e "$dst_dir" ] && [ ! -d "$dst_dir" ]; then
      echo "✗ Claude Code: '$dst_dir' exists but is not a directory — refuse"
      fail=$((fail + 1))
      continue
    fi
    if [ -e "$dst_dir" ] && [ ! -L "$dst_dir/SKILL.md" ] && [ ! -e "$dst_dir/SKILL.md" ]; then
      # directory exists but file is missing — nothing to do, mkdir -p handled it
      :
    fi

    # Destination SKILL.md handling
    if [ -L "$dst" ]; then
      # Existing symlink: check target
      local current_target
      current_target="$(readlink "$dst")"
      if [ "$current_target" = "$abs_src" ]; then
        # Already correct
        ok=$((ok + 1))
        continue
      else
        echo "✗ Claude Code: '$dst' symlink points to '$current_target' (expected '$abs_src') — refuse"
        fail=$((fail + 1))
        continue
      fi
    elif [ -e "$dst" ]; then
      # Non-symlink at destination. Most common case on legacy installs:
      # a previous setup.sh copied SKILL.md into ~/.claude/skills/ instead
      # of symlinking it. When the copy is byte-identical to the canonical
      # source, we auto-reconcile by moving it to a timestamped backup
      # directory and creating the symlink in its place. When the copy
      # differs, it is a user customization and we refuse to touch it.
      if [ ! -f "$dst" ]; then
        # Non-regular (directory, socket, fifo, etc.) — keep current refuse
        echo "✗ Claude Code: '$dst' exists but is not a regular file or symlink — refuse"
        fail=$((fail + 1))
        continue
      fi
      if cmp -s "$dst" "$abs_src"; then
        # Legacy copy is byte-identical to canonical — safe to reconcile.
        # Lazy-init a single timestamped backup dir for the whole run so
        # all auto-reconciliations land in one recoverable place.
        if [ -z "${CLAUDE_BACKUP_DIR:-}" ]; then
          CLAUDE_BACKUP_DIR="$skills_dst.bak.$(date +%s)"
          if ! mkdir -p "$CLAUDE_BACKUP_DIR"; then
            echo "✗ Claude Code: failed to create backup dir '$CLAUDE_BACKUP_DIR' — refused '$dst'"
            fail=$((fail + 1))
            continue
          fi
          echo "  (backing up identical legacy copies to $CLAUDE_BACKUP_DIR)"
        fi
        if mv "$dst" "$CLAUDE_BACKUP_DIR/$name.SKILL.md"; then
          if ln -s "$abs_src" "$dst"; then
            ok=$((ok + 1))
            continue
          else
            # Best-effort restore so the user's data is not stranded
            mv "$CLAUDE_BACKUP_DIR/$name.SKILL.md" "$dst" 2>/dev/null || true
            echo "✗ Claude Code: failed to create symlink '$dst' after moving legacy copy — restored"
            fail=$((fail + 1))
            continue
          fi
        else
          echo "✗ Claude Code: failed to move legacy copy '$dst' to backup — refused"
          fail=$((fail + 1))
          continue
        fi
      else
        # Real file with different content — user customization, do not touch.
        echo "✗ Claude Code: '$dst' differs from canonical '$abs_src' — refused (user customization preserved)"
        echo "  Inspect with: diff '$dst' '$abs_src'"
        echo "  To accept the canonical version: remove '$dst' and re-run setup.sh"
        fail=$((fail + 1))
        continue
      fi
    fi

    # Create destination directory and symlink
    mkdir -p "$dst_dir"
    if ln -s "$abs_src" "$dst"; then
      ok=$((ok + 1))
    else
      echo "✗ Claude Code: failed to create symlink '$dst' -> '$abs_src'"
      fail=$((fail + 1))
    fi
  done

  CLAUDE_SKILLS_OK=$ok
  CLAUDE_SKILLS_SKIP=$skip

  if [ "$fail" -gt 0 ]; then
    echo "✗ Claude Code: $fail skill symlink(s) FAILED — install is not complete"
    return 1
  fi
  echo "✓ Claude Code: $ok skill symlink(s) created in $skills_dst"
}
