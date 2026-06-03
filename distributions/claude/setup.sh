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
#
# Helpers expected (from setup-lib.sh, sourced earlier in setup.sh):
#   needs_python, generate_prompt_commands

# ── Claude entry point ──────────────────────────────────────────────────────
claude_install() {
  claude_install_settings_json
  claude_install_claude_md_block
  claude_install_prompt_commands
}

# 1. Claude Code — settings.json — patch with ~/.agents/skills path
claude_install_settings_json() {
  if needs_python; then
    mkdir -p "$HOME/.claude"
    [ ! -f "$CLAUDE_SETTINGS" ] && echo '{}' > "$CLAUDE_SETTINGS"
    python3 - "$CLAUDE_SETTINGS" <<'PY'
import json, sys
path = sys.argv[1]
with open(path) as f:
    cfg = json.load(f)
skills = cfg.get("skills", [])
entry = "~/.agents/skills"
if entry not in skills:
    skills.append(entry)
    cfg["skills"] = skills
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"✓ Claude Code: settings.json patched with {entry!r}")
else:
    print(f"✓ Claude Code: settings.json already includes {entry!r}")
PY
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
