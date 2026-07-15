#!/bin/bash
# core/setup.sh — Core VBB installation: pre-flight + universal symlinks.
#
# This file is sourced by the root setup.sh routeur. It is the FIRST
# distribution in the VBB installer (Core = provider-agnostic parts).
#
# Behavior is identical to the pre-Phase-2A inlined Core blocks in
# setup.sh. The 3 Core blocks extracted here:
#   1. Pre-flight checks (AGENTS.md, skills/, prompts/, SYSTEM.md)
#   2. Universal skills symlink (~/.agents/skills/vibebackbone)
#   3. Universal prompts symlink (~/.agents/prompts/vibebackbone)
#
# Globals expected from the caller (setup.sh):
#   REPO_ROOT, AGENTS_SRC, SKILLS_SRC, PROMPTS_SRC, SYSTEM_SRC
#   GLOBAL_SKILLS, GLOBAL_PROMPTS, LINK_NAME, PROMPTS_LINK
#   FORCE_GOVERNANCE
#
# Globals set here (for the rest of setup.sh to consume):
#   PROMPTS_AVAILABLE, SYSTEM_AVAILABLE
#   PROMPT_CANONICAL_COUNT, PROMPT_COUNT, PROMPT_ADAPTER_COUNT
#   SKILL_COUNT
#
# Helpers expected (from setup-lib.sh, sourced earlier in setup.sh):
#   count_skills, count_prompts_total, count_prompt_adapters
#   relpath, _is_vbb_symlink, backup_file

# ── Core entry point ────────────────────────────────────────────────────────
core_install() {
  core_preflight
  core_install_skills_symlink
  core_install_prompts_symlink
}

# 1. Pre-flight checks
core_preflight() {
  if [ ! -f "$AGENTS_SRC" ]; then
    echo "✗ AGENTS.md not found at $AGENTS_SRC — aborting"
    exit 1
  fi

  if [ ! -d "$SKILLS_SRC" ]; then
    echo "✗ skills/ directory not found at $SKILLS_SRC — aborting"
    exit 1
  fi

  PROMPTS_AVAILABLE=false
  if [ -d "$PROMPTS_SRC" ]; then
    PROMPTS_AVAILABLE=true
  else
    echo "⚠ prompts/ not found — prompt deployment skipped"
  fi

  SYSTEM_AVAILABLE=false
  if [ -f "$SYSTEM_SRC" ]; then
    SYSTEM_AVAILABLE=true
  else
    echo "⚠ SYSTEM.md not found — runtime behavior deployment skipped"
  fi

  PROMPT_CANONICAL_COUNT=0
  PROMPT_COUNT=0
  PROMPT_ADAPTER_COUNT=0
  if [ "$PROMPTS_AVAILABLE" = true ]; then
    PROMPT_CANONICAL_COUNT=$(find "$PROMPTS_SRC/canonical" -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    PROMPT_COUNT=$(count_prompts_total "$PROMPTS_SRC")
    PROMPT_ADAPTER_COUNT=$(count_prompt_adapters "$PROMPTS_SRC")
  fi

  SKILL_COUNT=$(count_skills "$SKILLS_SRC")
}

# 2. Universal skills symlink
core_install_skills_symlink() {
  echo "Installing vibebackbone..."
  echo "  Repo : $REPO_ROOT"
  echo ""

  mkdir -p "$GLOBAL_SKILLS"
  [ -L "$LINK_NAME" ] && rm "$LINK_NAME"
  # Use an absolute target: relative links break on macOS when HOME is under
  # /tmp because /tmp resolves through /private/tmp.
  ln -sfn "$SKILLS_SRC" "$LINK_NAME"
  echo "✓ ~/.agents/skills/vibebackbone → skills symlink (Pi, OpenCode, Codex)"
}

# 3. Universal prompts symlink
core_install_prompts_symlink() {
  if [ "$PROMPTS_AVAILABLE" = true ]; then
    mkdir -p "$GLOBAL_PROMPTS"
    if [ -L "$PROMPTS_LINK" ]; then
      if _is_vbb_symlink "$PROMPTS_LINK" "$PROMPTS_SRC"; then
        echo "✓ Prompts: ~/.agents/prompts/vibebackbone already linked"
      else
        # Symlink exists but points to a different source → replace
        rm "$PROMPTS_LINK"
        ln -sfn "$PROMPTS_SRC" "$PROMPTS_LINK"
        echo "✓ Prompts: ~/.agents/prompts/vibebackbone symlink updated (was pointing elsewhere)"
      fi
    elif [ -e "$PROMPTS_LINK" ] && [ ! -L "$PROMPTS_LINK" ]; then
      if [ "$FORCE_GOVERNANCE" = true ]; then
        backup_file "$PROMPTS_LINK"
        rm -rf "$PROMPTS_LINK"
        ln -sfn "$PROMPTS_SRC" "$PROMPTS_LINK"
        echo "✓ Prompts: ~/.agents/prompts/vibebackbone backed up and symlinked"
      else
        echo "⚠ Prompts: existing custom ~/.agents/prompts/vibebackbone skipped"
      fi
    else
      [ -L "$PROMPTS_LINK" ] && rm "$PROMPTS_LINK"
      ln -sfn "$PROMPTS_SRC" "$PROMPTS_LINK"
      echo "✓ Prompts: ~/.agents/prompts/vibebackbone symlinked"
    fi
  fi
}
