#!/bin/bash
# setup.sh — Install vibebackbone globally
#
# Four-layer deployment:
#   skills/     → ~/.agents/skills/vibebackbone
#   prompts/    → ~/.agents/prompts/vibebackbone  (universal symlink)
#   AGENTS.md   → per-provider governance
#   SYSTEM.md   → per-provider runtime behavior
#
# ~/.agents/skills/ is the universal location read by Pi, OpenCode, and Codex.
# Claude Code reads ~/.claude/skills/ instead — this script patches its settings.json
# to also point at ~/.agents/skills/, per the official workaround until Claude Code
# natively supports ~/.agents/skills/ (tracking issue: anthropics/claude-code#31005).
#
# Governance + runtime + prompts deployment paths:
#   Claude Code  → ~/.claude/CLAUDE.md        (@import block)
#                → ~/.claude/commands/         (prompt commands vbb-*.md)
#   Codex        → ~/.codex/AGENTS.md         (compiled generated block)
#   OpenCode     → ~/.config/opencode/opencode.json (instructions field)
#                → ~/.config/opencode/commands/ (prompt commands vbb-*.md)
#   Pi           → ~/.pi/agent/AGENTS.md      (symlink)
#   Pi           → ~/.pi/agent/SYSTEM.md      (symlink)
#   Pi           → ~/.pi/agent/prompts/*.md   (symlinks)
#
# Usage:
#   bash setup.sh                  # Install (never overwrites custom files)
#   bash setup.sh --force-governance  # Install and overwrite with backup
#   bash setup.sh --uninstall      # Remove

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
AGENTS_SRC="$REPO_ROOT/AGENTS.md"
SYSTEM_SRC="$REPO_ROOT/SYSTEM.md"
PROMPTS_SRC="$REPO_ROOT/prompts"

GLOBAL_SKILLS="$HOME/.agents/skills"
GLOBAL_PROMPTS="$HOME/.agents/prompts"
LINK_NAME="$GLOBAL_SKILLS/vibebackbone"
PROMPTS_LINK="$GLOBAL_PROMPTS/vibebackbone"

CLAUDE_SETTINGS="$HOME/.claude/settings.json"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
CLAUDE_COMMANDS="$HOME/.claude/commands"

CODEX_AGENTS="$HOME/.codex/AGENTS.md"

PI_AGENTS="$HOME/.pi/agent/AGENTS.md"
PI_SYSTEM="$HOME/.pi/agent/SYSTEM.md"
PI_PROMPTS="$HOME/.pi/agent/prompts"

OPENCODE_JSON="$HOME/.config/opencode/opencode.json"
OPENCODE_COMMANDS="$HOME/.config/opencode/commands"

FORCE_GOVERNANCE=false
[ "${1}" = "--force-governance" ] && FORCE_GOVERNANCE=true

# ── Helpers ─────────────────────────────────────────────────────────────────
# Shared helpers (relpath, _realpath, _is_vbb_symlink, needs_python,
# backup_file, symlink_if_absent, generate_prompt_commands) live in
# setup-lib.sh. The setup-lib.sh file is a pure extraction of the
# pre-Phase-1 inlined helpers — same signatures, same behavior.

# shellcheck source=setup-lib.sh
source "$REPO_ROOT/setup-lib.sh"

# Count skill directories, excluding catalog files such as INDEX.yaml.
count_skills() {
  local dir="$1"
  if [ -d "$dir" ]; then
    # Exclude INDEX.yaml catalog files and the skills/ parent directory itself
    find "$dir" -mindepth 1 -maxdepth 1 -type d ! -name 'INDEX.yaml' | wc -l | tr -d ' '
  else
    echo 0
  fi
}

# Count all prompt templates, including canonical prompts in subdirectories.
count_prompts_total() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -type f -name "*.md" ! -name "README.md" ! -name "INDEX.md" | wc -l | tr -d ' '
  else
    echo 0
  fi
}

# Count root prompt adapter commands. Canonical prompts remain available through
# the universal prompts symlink and Codex prompt-library reference.
count_prompt_adapters() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -maxdepth 1 -type f -name "*.md" ! -name "README.md" ! -name "INDEX.md" | wc -l | tr -d ' '
  else
    echo 0
  fi
}

# ── Uninstall ────────────────────────────────────────────────────────────────

uninstall() {
  # 1. Skills symlink
  if [ -L "$LINK_NAME" ] || [ -d "$LINK_NAME" ]; then
    rm -rf "$LINK_NAME"
    echo "✓ Removed $LINK_NAME"
  fi

  # 2. Prompts universal symlink
  if _is_vbb_symlink "$PROMPTS_LINK" "$PROMPTS_SRC"; then
    rm "$PROMPTS_LINK"
    echo "✓ Removed $PROMPTS_LINK"
  fi

  # 3. Claude Code settings.json
  if [ -f "$CLAUDE_SETTINGS" ] && command -v python3 &>/dev/null; then
    python3 - "$CLAUDE_SETTINGS" <<'PY'
import json, sys
path = sys.argv[1]
with open(path) as f:
    cfg = json.load(f)
skills = cfg.get("skills", [])
cfg["skills"] = [s for s in skills if s != "~/.agents/skills"]
if not cfg["skills"]:
    cfg.pop("skills", None)
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)
print("✓ Removed ~/.agents/skills from Claude Code settings")
PY
  fi

  # 4. Claude Code CLAUDE.md — remove vibebackbone block
  if [ -f "$CLAUDE_MD" ] && command -v python3 &>/dev/null; then
    python3 - "$CLAUDE_MD" <<'PY'
import sys, re
path = sys.argv[1]
with open(path) as f:
    content = f.read()
pattern = r'(?:\n)?# vibebackbone\n(?:@[^\n]*\n)+'
cleaned = re.sub(pattern, '\n', content)
cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
with open(path, "w") as f:
    f.write(cleaned)
print("✓ Removed vibebackbone block from ~/.claude/CLAUDE.md")
PY
  fi

  # 5. Claude prompt commands — remove only generated ones
  if [ -d "$CLAUDE_COMMANDS" ]; then
    for f in "$CLAUDE_COMMANDS"/vbb-*.md; do
      [ -f "$f" ] || continue
      if grep -q "vibebackbone:generated" "$f" 2>/dev/null; then
        rm "$f"
        echo "✓ Removed $(basename "$f")"
      fi
    done
  fi

  # 6. Codex AGENTS.md — remove generated block only
  if [ -f "$CODEX_AGENTS" ] && command -v python3 &>/dev/null; then
    python3 - "$CODEX_AGENTS" <<'PY'
import sys
path = sys.argv[1]
with open(path) as f:
    content = f.read()
start = "<!-- vibebackbone:generated:start -->"
end = "<!-- vibebackbone:generated:end -->"
first = content.find(start)
last = content.rfind(end)
if first != -1 and last != -1 and last >= first:
    last += len(end)
    while last < len(content) and content[last] in "\r\n":
        last += 1
    cleaned = content[:first] + content[last:]
elif first != -1:
    cleaned = content[:first]
else:
    cleaned = content
with open(path, "w") as f:
    f.write(cleaned)
if not cleaned.strip():
    import os
    os.remove(path)
    print("✓ Removed ~/.codex/AGENTS.md (empty after block removal)")
else:
    print("✓ Removed vibebackbone generated block from ~/.codex/AGENTS.md")
PY
  fi

  # 7. Pi symlinks — AGENTS + SYSTEM + prompts
  if _is_vbb_symlink "$PI_AGENTS" "$AGENTS_SRC"; then
    rm "$PI_AGENTS"
    echo "✓ Removed $PI_AGENTS"
  fi
  if _is_vbb_symlink "$PI_SYSTEM" "$SYSTEM_SRC"; then
    rm "$PI_SYSTEM"
    echo "✓ Removed $PI_SYSTEM"
  fi
  if [ -d "$PI_PROMPTS" ]; then
    for f in "$PI_PROMPTS"/*.md; do
      [ -f "$f" ] || continue
      if [ -L "$f" ] && [[ "$(readlink "$f")" == "$PROMPTS_SRC"/* ]]; then
        rm "$f"
      fi
    done
    echo "✓ Removed Pi prompt symlinks from $PI_PROMPTS"
  fi

  # 8. OpenCode instructions
  if [ -f "$OPENCODE_JSON" ] && command -v python3 &>/dev/null; then
    python3 - "$OPENCODE_JSON" "$AGENTS_SRC" "$SYSTEM_SRC" <<'PY'
import json, sys, os
path, agents_src, system_src = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    cfg = json.load(f)
instructions = cfg.get("instructions", [])
cfg["instructions"] = [i for i in instructions if i not in (agents_src, system_src)]
if not cfg["instructions"]:
    cfg.pop("instructions", None)
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)
print("✓ Removed vibebackbone from ~/.config/opencode/opencode.json")
PY
  fi

  # 9. OpenCode prompt commands — remove only generated ones
  if [ -d "$OPENCODE_COMMANDS" ]; then
    for f in "$OPENCODE_COMMANDS"/vbb-*.md; do
      [ -f "$f" ] || continue
      if grep -q "vibebackbone:generated" "$f" 2>/dev/null; then
        rm "$f"
        echo "✓ Removed $(basename "$f")"
      fi
    done
  fi

  echo ""
  echo "✓ vibebackbone uninstalled"
  exit 0
}

[ "${1}" = "--uninstall" ] && uninstall

# ── Core install (pre-flight + universal symlinks) ─────────────────────────
# Core logic moved to core/setup.sh (Phase 2A). Globals set by core_install
# (PROMPTS_AVAILABLE, SYSTEM_AVAILABLE, *_COUNT) feed the per-provider
# sections below.
source "$REPO_ROOT/core/setup.sh"
core_install

# ── 3-5. Claude Code — settings.json + CLAUDE.md block + prompt commands ────
# Claude logic moved to distributions/claude/setup.sh (Phase 2C). Globals
# set by claude_install (CLAUDE_PROMPTS_OK, CLAUDE_PROMPTS_SKIP) feed the
# summary below.
source "$REPO_ROOT/distributions/claude/setup.sh"
claude_install

# ── 6. Codex — compiled AGENTS.md ───────────────────────────────────────────
mkdir -p "$HOME/.codex"

if needs_python; then
  python3 - "$CODEX_AGENTS" "$AGENTS_SRC" "$SYSTEM_SRC" "$SYSTEM_AVAILABLE" "$FORCE_GOVERNANCE" "$PROMPTS_SRC" "$PROMPTS_AVAILABLE" <<'PY'
import sys, os
path, agents_src, system_src, system_available, force_governance, prompts_src, prompts_available = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
force = force_governance.lower() == "true"
system_available_flag = system_available.lower() == "true"
prompts_available_flag = prompts_available.lower() == "true"
START = "<!-- vibebackbone:generated:start -->"
END = "<!-- vibebackbone:generated:end -->"

def replace_generated_block(content, new_block):
    first = content.find(START)
    if first == -1:
        return None
    last = content.rfind(END)
    if last == -1 or last < first:
        return content[:first] + new_block.rstrip() + "\n"
    last += len(END)
    while last < len(content) and content[last] in "\r\n":
        last += 1
    return content[:first] + new_block.rstrip() + "\n" + content[last:]

def build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag):
    lines = [
        "\n<!-- vibebackbone:generated:start -->\n",
        f"<!-- Source: {agents_src} -->\n",
        open(agents_src).read(),
    ]
    if system_available_flag:
        lines.extend([
            "\n---\n",
            f"<!-- Source: {system_src} -->\n",
            open(system_src).read(),
        ])
    if prompts_available_flag:
        lines.extend([
            "\n---\n",
            "# Vibebackbone Prompt Library\n",
            "Prompt templates are available at:\n",
            f"`{os.path.expanduser('~/.agents/prompts/vibebackbone/')}`\n",
            "They are session entrypoints, not skills.\n",
            "Resolve prompt short names to Markdown files before reading them:\n",
            "- `quick-task` -> `1-p-vbb-quick-task.md`\n",
            "- `structured-task` -> `1-p-vbb-structured-task.md`\n",
            "- `audit-task` -> `2-p-vbb-audit-task.md`\n",
            "- `release-check` -> `2-p-vbb-release-check.md`\n",
            "- `session-handoff` -> `t-p-vbb-session-handoff.md`\n",
            "Read the resolved Markdown prompt from that directory and apply it before execution.\n",
            "Do not invent prompt behavior from the name alone. If the prompt file is missing, state that explicitly and proceed only as best-effort.\n",
        ])
    lines.append("\n<!-- vibebackbone:generated:end -->\n")
    return "".join(lines)

if os.path.exists(path):
    with open(path) as f:
        content = f.read()
    has_markers = START in content

    if has_markers:
        new_block = build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag)
        content = replace_generated_block(content, new_block)
        with open(path, "w") as f:
            f.write(content)
        print("✓ Codex: generated block updated")
        sys.exit(0)
    else:
        if force:
            from datetime import datetime as _dt
            backup_path = f"{path}.backup.{_dt.now().strftime('%Y%m%d-%H%M%S')}"
            import shutil
            shutil.copy(path, backup_path)
            print(f"✓ Codex: backup created at {backup_path}")
            new_block = build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag)
            with open(path, "w") as f:
                f.write(new_block)
            print("✓ Codex: generated AGENTS.md created (custom file backed up and replaced)")
        else:
            print("⚠ Codex: existing custom AGENTS.md skipped (use --force-governance)")
        sys.exit(0)

new_block = build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag)
with open(path, "w") as f:
    f.write(new_block)
print("✓ Codex: generated AGENTS.md created")
PY
else
  echo "⚠ Codex: python3 not found — compiled AGENTS.md generation skipped"
fi

# ── 7. Pi — symlinks (AGENTS + SYSTEM + prompts) ────────────────────────────
# Pi logic moved to distributions/pi/setup.sh (Phase 2B). Globals set by
# pi_install (PI_PROMPTS_OK, PI_PROMPTS_SKIP) feed the summary below.
source "$REPO_ROOT/distributions/pi/setup.sh"
pi_install

# ── 8. OpenCode — instructions ───────────────────────────────────────────────
mkdir -p "$HOME/.config/opencode"
if needs_python; then
  python3 - "$OPENCODE_JSON" "$AGENTS_SRC" "$SYSTEM_SRC" "$SYSTEM_AVAILABLE" <<'PY'
import json, sys, os
path, agents_src, system_src, system_available = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
system_available_flag = system_available.lower() == "true"

if os.path.exists(path):
    with open(path) as f:
        cfg = json.load(f)
else:
    cfg = {"$schema": "https://opencode.ai/config.json"}

instructions = cfg.get("instructions", [])
changes = []

if agents_src not in instructions:
    instructions.append(agents_src)
    changes.append("AGENTS.md")

if system_available_flag and system_src not in instructions:
    instructions.append(system_src)
    changes.append("SYSTEM.md")

if changes:
    cfg["instructions"] = instructions
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"✓ OpenCode: {', '.join(changes)} instruction(s) added")
else:
    already = ["AGENTS.md"]
    if system_available_flag:
        already.append("SYSTEM.md")
    print(f"✓ OpenCode: {', '.join(already)} already referenced")
PY
else
  echo "⚠ OpenCode: python3 not found — opencode.json patch skipped"
fi

# ── 9. OpenCode — prompt commands ───────────────────────────────────────────
OPENCODE_PROMPTS_OK=0
OPENCODE_PROMPTS_SKIP=0
generate_prompt_commands "$OPENCODE_COMMANDS" "OpenCode prompts" "OPENCODE_PROMPTS_OK" "OPENCODE_PROMPTS_SKIP"

# ── 10. Hermes (non-destructive, agent-install only) ────────────────────────
# Hermes logic moved to distributions/hermes/setup.sh (Phase 2F). This is
# the LAST install step and is strictly read-only: no ~/.hermes/ writes,
# no profile copy, no secret creation, no proxy mutation. See
# distributions/hermes/AGENT_INSTALL.md for the operator procedure.
echo ""
echo "Hermes/Cody distribution:"
source "$REPO_ROOT/distributions/hermes/setup.sh"
hermes_install

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "✓ Done — $SKILL_COUNT skills · $PROMPT_COUNT prompts ($PROMPT_CANONICAL_COUNT canonical templates + $PROMPT_ADAPTER_COUNT adapter commands)"

echo ""
echo "Installed:"
echo "  Skills  : ~/.agents/skills/vibebackbone"
if [ "$PROMPTS_AVAILABLE" = true ] && [ -L "$PROMPTS_LINK" ]; then
  echo "  Prompts : ~/.agents/prompts/vibebackbone"
fi

echo "Prompt adapters:"
if [ "$PROMPTS_AVAILABLE" = true ]; then
  if [ "$PI_PROMPTS_OK" -gt 0 ] || [ "$PI_PROMPTS_SKIP" -gt 0 ]; then
    echo "  Pi          : $PI_PROMPTS_OK linked / $PI_PROMPTS_SKIP skipped"
  fi
  if [ "$CLAUDE_PROMPTS_OK" -gt 0 ] || [ "$CLAUDE_PROMPTS_SKIP" -gt 0 ]; then
    echo "  Claude Code : $CLAUDE_PROMPTS_OK generated / $CLAUDE_PROMPTS_SKIP skipped"
  fi
  if [ "$OPENCODE_PROMPTS_OK" -gt 0 ] || [ "$OPENCODE_PROMPTS_SKIP" -gt 0 ]; then
    echo "  OpenCode    : $OPENCODE_PROMPTS_OK generated / $OPENCODE_PROMPTS_SKIP skipped"
  fi
  if [ -f "$CODEX_AGENTS" ] && grep -q "Vibebackbone Prompt Library" "$CODEX_AGENTS" 2>/dev/null; then
    echo "  Codex       : prompt library referenced in AGENTS.md"
  fi
fi

if [ "$PI_PROMPTS_SKIP" -gt 0 ] || [ "$CLAUDE_PROMPTS_SKIP" -gt 0 ] || [ "$OPENCODE_PROMPTS_SKIP" -gt 0 ]; then
  echo ""
  echo "Warnings:"
  [ "$PI_PROMPTS_SKIP" -gt 0 ] && echo "  ⚠ Pi prompts          : $PI_PROMPTS_SKIP custom files skipped"
  [ "$CLAUDE_PROMPTS_SKIP" -gt 0 ] && echo "  ⚠ Claude Code prompts : $CLAUDE_PROMPTS_SKIP custom commands skipped"
  [ "$OPENCODE_PROMPTS_SKIP" -gt 0 ] && echo "  ⚠ OpenCode prompts    : $OPENCODE_PROMPTS_SKIP custom commands skipped"
fi

echo "Governance / runtime:"
if [ -f "$CLAUDE_MD" ] && grep -qF "$AGENTS_SRC" "$CLAUDE_MD" 2>/dev/null; then
  echo "  Claude Code : AGENTS + SYSTEM referenced"
fi
if [ -f "$CODEX_AGENTS" ] && grep -q "vibebackbone:generated:start" "$CODEX_AGENTS" 2>/dev/null; then
  if grep -q "Vibebackbone Prompt Library" "$CODEX_AGENTS" 2>/dev/null; then
    echo "  Codex       : AGENTS + SYSTEM + Prompt Library compiled"
  else
    echo "  Codex       : AGENTS + SYSTEM compiled"
  fi
fi
if [ -L "$PI_AGENTS" ] && _is_vbb_symlink "$PI_AGENTS" "$AGENTS_SRC"; then
  echo "  Pi          : AGENTS + SYSTEM symlinked"
fi
if [ -f "$OPENCODE_JSON" ] && python3 -c "
import json, sys
cfg = json.load(open('$OPENCODE_JSON'))
found = '$AGENTS_SRC' in cfg.get('instructions', [])
sys.exit(0 if found else 1)
" 2>/dev/null; then
  echo "  OpenCode    : AGENTS + SYSTEM referenced"
fi

echo ""
echo "To force governance deployment:"
echo "  bash $REPO_ROOT/setup.sh --force-governance"
echo "To update:"
echo "  cd $REPO_ROOT && git pull"
echo "To remove:"
echo "  bash $REPO_ROOT/setup.sh --uninstall"
