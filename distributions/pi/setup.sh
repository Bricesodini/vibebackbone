#!/bin/bash
# distributions/pi/setup.sh — Pi distribution installation.
#
# This file is sourced by the root setup.sh routeur. It is the
# SECOND distribution in the VBB installer (Pi = one of the 4 providers).
#
# Behavior is identical to the pre-Phase-2B inlined §7 "Pi — symlinks"
# block in setup.sh. Extracted verbatim.
#
# Globals expected from the caller (setup.sh):
#   REPO_ROOT, HOME
#   AGENTS_SRC, SYSTEM_SRC, PROMPTS_SRC
#   PI_AGENTS, PI_SYSTEM, PI_SKILLS_LINK, PI_PROMPTS
#   FORCE_GOVERNANCE, SYSTEM_AVAILABLE, PROMPTS_AVAILABLE
#
# Side effects (consumed by setup.sh summary):
#   PI_PROMPTS_OK, PI_PROMPTS_SKIP
#
# Helpers expected (from setup-lib.sh, sourced earlier in setup.sh):
#   symlink_if_absent, backup_file

# ── Pi entry point ──────────────────────────────────────────────────────────
pi_install() {
  pi_install_skills_symlink
  pi_install_agents_symlink
  pi_install_system_symlink
  pi_install_prompts_symlinks
}

# Pi resolves user skills from ~/.pi/agent/skills. Keep a provider-local link
# to the Core skills tree so a fresh HOME behaves like an existing install.
pi_install_skills_symlink() {
  mkdir -p "$(dirname "$PI_SKILLS_LINK")"
  symlink_if_absent "$SKILLS_SRC" "$PI_SKILLS_LINK" "Pi: skills"
}

# 1. ~/.pi/agent/AGENTS.md — symlink to repo's AGENTS.md
pi_install_agents_symlink() {
  mkdir -p "$HOME/.pi/agent"
  symlink_if_absent "$AGENTS_SRC" "$PI_AGENTS" "Pi: AGENTS.md"
}

# 2. ~/.pi/agent/SYSTEM.md — symlink to repo's SYSTEM.md (if available)
pi_install_system_symlink() {
  if [ "$SYSTEM_AVAILABLE" = true ]; then
    symlink_if_absent "$SYSTEM_SRC" "$PI_SYSTEM" "Pi: SYSTEM.md"
  fi
}

# 3. ~/.pi/agent/prompts/*.md — symlinks to repo's prompts/*.md
pi_install_prompts_symlinks() {
  PI_PROMPTS_OK=0
  PI_PROMPTS_SKIP=0

  if [ "$PROMPTS_AVAILABLE" = true ]; then
    mkdir -p "$PI_PROMPTS"
    for src in "$PROMPTS_SRC"/*.md; do
      [ -f "$src" ] || continue
      name=$(basename "$src")
      [[ "$name" == "README.md" || "$name" == "INDEX.md" ]] && continue
      dst="$PI_PROMPTS/$name"
      if [ -L "$dst" ]; then
        # Existing symlink → always replace (covers old source, case-insensitivity)
        rm "$dst"
      elif [ -e "$dst" ] && [ ! -L "$dst" ]; then
        if [ "$FORCE_GOVERNANCE" = true ]; then
          backup_file "$dst"
          rm "$dst"
        else
          echo "⚠ Pi prompts: existing custom $name skipped"
          PI_PROMPTS_SKIP=$((PI_PROMPTS_SKIP + 1))
          continue
        fi
      fi
      ln -sfn "$src" "$dst"
      PI_PROMPTS_OK=$((PI_PROMPTS_OK + 1))
    done
    if [ "$PI_PROMPTS_SKIP" -eq 0 ]; then
      echo "✓ Pi prompts: $PI_PROMPTS_OK prompts linked"
    fi
  fi
}
