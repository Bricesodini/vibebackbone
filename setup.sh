#!/bin/bash
# setup.sh — Install vibebackbone skills globally
#
# ~/.agents/skills/ is the universal location read by Pi, OpenCode, and Codex.
# Claude Code reads ~/.claude/skills/ instead — this script patches its settings.json
# to also point at ~/.agents/skills/, per the official workaround until Claude Code
# natively supports ~/.agents/skills/ (tracking issue: anthropics/claude-code#31005).
#
# Usage:
#   bash setup.sh             # Install
#   bash setup.sh --uninstall # Remove

set -e

SKILLS_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/skills" && pwd)"
GLOBAL_SKILLS="$HOME/.agents/skills"
LINK_NAME="$GLOBAL_SKILLS/vibebackbone"
CLAUDE_SETTINGS="$HOME/.claude/settings.json"

uninstall() {
  # Remove symlink
  if [ -L "$LINK_NAME" ] || [ -d "$LINK_NAME" ]; then
    rm -rf "$LINK_NAME"
    echo "✓ Removed $LINK_NAME"
  fi

  # Remove ~/.agents/skills from Claude Code settings
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

  echo "✓ vibebackbone uninstalled"
  exit 0
}

[ "${1}" = "--uninstall" ] && uninstall

# ── 1. Universal symlink ────────────────────────────────────────────────────
echo "Installing vibebackbone skills globally..."
echo "  From : $SKILLS_SRC"
echo "  To   : $LINK_NAME"
echo ""

mkdir -p "$GLOBAL_SKILLS"
[ -L "$LINK_NAME" ] && rm "$LINK_NAME"
ln -s "$SKILLS_SRC" "$LINK_NAME"

echo "✓ ~/.agents/skills/vibebackbone → symlink created (Pi, OpenCode, Codex)"

# ── 2. Claude Code patch ────────────────────────────────────────────────────
# Claude Code does not natively read ~/.agents/skills/ (issue #31005).
# Patch ~/.claude/settings.json to add the path explicitly.
if command -v python3 &>/dev/null; then
  mkdir -p "$HOME/.claude"
  if [ ! -f "$CLAUDE_SETTINGS" ]; then
    echo '{}' > "$CLAUDE_SETTINGS"
  fi
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
  echo "⚠  python3 not found — Claude Code patch skipped"
  echo "   Add manually to ~/.claude/settings.json: {\"skills\": [\"~/.agents/skills\"]}"
fi

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "✓ Done — $(ls "$SKILLS_SRC" | wc -l | tr -d ' ') skills available"
echo ""
echo "  Pi, OpenCode, Codex : auto-discovered via ~/.agents/skills/"
echo "  Claude Code          : configured via ~/.claude/settings.json"
echo ""
echo "To update : cd $(dirname "$SKILLS_SRC") && git pull"
echo "To remove : bash $(dirname "$SKILLS_SRC")/setup.sh --uninstall"
