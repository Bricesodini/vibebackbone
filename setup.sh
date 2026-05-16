#!/bin/bash
# setup.sh — Install vibebackbone globally
#
# ~/.agents/skills/ is the universal location read by Pi, OpenCode, and Codex.
# Claude Code reads ~/.claude/skills/ instead — this script patches its settings.json
# to also point at ~/.agents/skills/, per the official workaround until Claude Code
# natively supports ~/.agents/skills/ (tracking issue: anthropics/claude-code#31005).
#
# Governance (AGENTS.md) is deployed per-provider to their confirmed global paths:
#   Claude Code  → ~/.claude/CLAUDE.md        (@import syntax, native)
#   Codex        → ~/.codex/AGENTS.md         (symlink)
#   OpenCode     → ~/.config/opencode/opencode.json (instructions field)
#   Pi           → ~/.pi/agent/AGENTS.md      (symlink)
#
# Usage:
#   bash setup.sh             # Install
#   bash setup.sh --uninstall # Remove

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
AGENTS_SRC="$REPO_ROOT/AGENTS.md"
GLOBAL_SKILLS="$HOME/.agents/skills"
LINK_NAME="$GLOBAL_SKILLS/vibebackbone"
CLAUDE_SETTINGS="$HOME/.claude/settings.json"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
CODEX_AGENTS="$HOME/.codex/AGENTS.md"
PI_AGENTS="$HOME/.pi/agent/AGENTS.md"
OPENCODE_JSON="$HOME/.config/opencode/opencode.json"

# ── Helpers ─────────────────────────────────────────────────────────────────

# Append $content to $file if $marker is not already present
append_if_absent() {
  local file="$1" marker="$2" content="$3"
  if ! grep -qF "$marker" "$file" 2>/dev/null; then
    printf '%s\n' "$content" >> "$file"
    return 0
  fi
  return 1
}

# Create symlink if target does not exist; skip with warning if it does
symlink_if_absent() {
  local src="$1" dst="$2" label="$3"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    echo "✓ $dst already linked (${label})"
  elif [ ! -e "$dst" ]; then
    ln -s "$src" "$dst"
    echo "✓ $dst → symlink created (${label})"
  else
    echo "⚠  $dst exists with custom content — skipping (${label})"
    echo "   Add manually: ln -sf $src $dst"
  fi
}

# ── Uninstall ────────────────────────────────────────────────────────────────

uninstall() {
  # 1. Skills symlink
  if [ -L "$LINK_NAME" ] || [ -d "$LINK_NAME" ]; then
    rm -rf "$LINK_NAME"
    echo "✓ Removed $LINK_NAME"
  fi

  # 2. Claude Code settings.json
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

  # 3. Claude Code CLAUDE.md — remove vibebackbone block
  if [ -f "$CLAUDE_MD" ]; then
    python3 - "$CLAUDE_MD" <<'PY'
import sys, re
path = sys.argv[1]
with open(path) as f:
    content = f.read()
cleaned = re.sub(r'\n# vibebackbone\n@[^\n]+\n', '', content)
with open(path, "w") as f:
    f.write(cleaned)
print("✓ Removed vibebackbone @import from ~/.claude/CLAUDE.md")
PY
  fi

  # 4. Codex AGENTS.md symlink
  if [ -L "$CODEX_AGENTS" ] && [ "$(readlink "$CODEX_AGENTS")" = "$AGENTS_SRC" ]; then
    rm "$CODEX_AGENTS"
    echo "✓ Removed $CODEX_AGENTS"
  fi

  # 5. Pi AGENTS.md symlink
  if [ -L "$PI_AGENTS" ] && [ "$(readlink "$PI_AGENTS")" = "$AGENTS_SRC" ]; then
    rm "$PI_AGENTS"
    echo "✓ Removed $PI_AGENTS"
  fi

  # 6. OpenCode opencode.json — remove instructions entry
  if [ -f "$OPENCODE_JSON" ] && command -v python3 &>/dev/null; then
    python3 - "$OPENCODE_JSON" "$AGENTS_SRC" <<'PY'
import json, sys, os
path, agents_src = sys.argv[1], sys.argv[2]
with open(path) as f:
    cfg = json.load(f)
instructions = cfg.get("instructions", [])
cfg["instructions"] = [i for i in instructions if i != agents_src]
if not cfg["instructions"]:
    cfg.pop("instructions", None)
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)
print("✓ Removed vibebackbone from ~/.config/opencode/opencode.json")
PY
  fi

  echo ""
  echo "✓ vibebackbone uninstalled"
  exit 0
}

[ "${1}" = "--uninstall" ] && uninstall

# ── 1. Universal skills symlink ──────────────────────────────────────────────
echo "Installing vibebackbone..."
echo "  Repo : $REPO_ROOT"
echo ""

mkdir -p "$GLOBAL_SKILLS"
[ -L "$LINK_NAME" ] && rm "$LINK_NAME"
ln -s "$SKILLS_SRC" "$LINK_NAME"
echo "✓ ~/.agents/skills/vibebackbone → skills symlink (Pi, OpenCode, Codex)"

# ── 2. Claude Code — settings.json ──────────────────────────────────────────
if command -v python3 &>/dev/null; then
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
    print(f"✓ Added {entry!r} to Claude Code settings")
else:
    print(f"✓ Claude Code settings already include {entry!r}")
PY
else
  echo "⚠  python3 not found — Claude Code settings patch skipped"
fi

# ── 3. Governance — AGENTS.md per provider ───────────────────────────────────

echo ""
echo "Deploying governance (AGENTS.md)..."

# Claude Code: @import syntax (native — no content duplication)
mkdir -p "$HOME/.claude"
touch "$CLAUDE_MD"
if append_if_absent "$CLAUDE_MD" "vibebackbone/AGENTS.md" \
    "$(printf '\n# vibebackbone\n@%s' "$AGENTS_SRC")"; then
  echo "✓ ~/.claude/CLAUDE.md — @import added (Claude Code)"
else
  echo "✓ ~/.claude/CLAUDE.md already references vibebackbone"
fi

# Codex: symlink ~/.codex/AGENTS.md
mkdir -p "$HOME/.codex"
symlink_if_absent "$AGENTS_SRC" "$CODEX_AGENTS" "Codex"

# Pi: symlink ~/.pi/agent/AGENTS.md
mkdir -p "$HOME/.pi/agent"
symlink_if_absent "$AGENTS_SRC" "$PI_AGENTS" "Pi"

# OpenCode: patch ~/.config/opencode/opencode.json → instructions field
mkdir -p "$HOME/.config/opencode"
if command -v python3 &>/dev/null; then
  python3 - "$OPENCODE_JSON" "$AGENTS_SRC" <<'PY'
import json, sys, os
path, agents_src = sys.argv[1], sys.argv[2]
if os.path.exists(path):
    with open(path) as f:
        cfg = json.load(f)
else:
    cfg = {"$schema": "https://opencode.ai/config.json"}
instructions = cfg.get("instructions", [])
if agents_src not in instructions:
    instructions.append(agents_src)
    cfg["instructions"] = instructions
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print("✓ ~/.config/opencode/opencode.json — instructions entry added (OpenCode)")
else:
    print("✓ opencode.json already includes vibebackbone/AGENTS.md")
PY
else
  echo "⚠  python3 not found — OpenCode patch skipped"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "✓ Done — $(ls "$SKILLS_SRC" | wc -l | tr -d ' ') skills · governance deployed to 4 providers"
echo ""
echo "  Skills (all providers) : ~/.agents/skills/vibebackbone/"
echo "  Claude Code            : ~/.claude/settings.json + ~/.claude/CLAUDE.md"
echo "  Codex                  : ~/.codex/AGENTS.md"
echo "  Pi                     : ~/.pi/agent/AGENTS.md"
echo "  OpenCode               : ~/.config/opencode/opencode.json"
echo ""
echo "To update : cd $REPO_ROOT && git pull"
echo "To remove : bash $REPO_ROOT/setup.sh --uninstall"
