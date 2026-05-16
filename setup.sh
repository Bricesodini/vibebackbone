#!/bin/bash
# setup.sh — Install vibebackbone skills globally
#
# Installs the 57 vibebackbone skills into ~/.agents/skills/
# This universal location is auto-discovered by Pi, Claude Code, OpenCode, Codex
# and any agent following the agentskills.io specification.
#
# Usage:
#   bash setup.sh           # Install
#   bash setup.sh --uninstall  # Remove

set -e

SKILLS_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/skills" && pwd)"
GLOBAL_SKILLS="$HOME/.agents/skills"
LINK_NAME="$GLOBAL_SKILLS/vibebackbone"

uninstall() {
  if [ -L "$LINK_NAME" ] || [ -d "$LINK_NAME" ]; then
    rm -rf "$LINK_NAME"
    echo "✓ vibebackbone removed from $GLOBAL_SKILLS"
  else
    echo "Nothing to uninstall (not found at $LINK_NAME)"
  fi
  exit 0
}

[ "${1}" = "--uninstall" ] && uninstall

echo "Installing vibebackbone skills globally..."
echo "  From : $SKILLS_SRC"
echo "  To   : $LINK_NAME"
echo ""

mkdir -p "$GLOBAL_SKILLS"

# Use a symlink so updates (git pull) are reflected immediately
if [ -L "$LINK_NAME" ]; then
  rm "$LINK_NAME"
fi
ln -s "$SKILLS_SRC" "$LINK_NAME"

echo "✓ Done — $(ls "$SKILLS_SRC" | wc -l | tr -d ' ') skills available"
echo ""
echo "Any agent that reads ~/.agents/skills/ will now discover vibebackbone."
echo "To update: cd $(dirname "$SKILLS_SRC") && git pull"
echo "To remove: bash $(dirname "$SKILLS_SRC")/setup.sh --uninstall"
