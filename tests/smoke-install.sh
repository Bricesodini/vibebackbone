#!/bin/bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_HOME="$(mktemp -d)"
echo "Testing install with HOME=$TMP_HOME"

# Run first install (should create everything)
HOME="$TMP_HOME" bash "$ROOT/setup.sh"

# Check prompts deployed
assert_dir_has_files() {
  local dir="$1"
  shift
  if [ -d "$dir" ]; then
    local count
    count="$(find "$dir" "$@" 2>/dev/null | wc -l | tr -d ' ')"
    [ "$count" -gt 0 ]
  else
    echo "✗ Directory missing: $dir"
    exit 1
  fi
}

test -L "$TMP_HOME/.agents/prompts/vibebackbone"
test -d "$TMP_HOME/.pi/agent/prompts"
assert_dir_has_files "$TMP_HOME/.pi/agent/prompts" -type l -name '*.md'
assert_dir_has_files "$TMP_HOME/.claude/commands" -name 'vbb-*.md'
assert_dir_has_files "$TMP_HOME/.config/opencode/commands" -name 'vbb-*.md'

# Check generated markers in commands
[ -d "$TMP_HOME/.claude/commands" ] && grep -qR "vibebackbone:generated" "$TMP_HOME/.claude/commands"
[ -d "$TMP_HOME/.config/opencode/commands" ] && grep -qR "vibebackbone:generated" "$TMP_HOME/.config/opencode/commands"

grep -n "Vibebackbone Prompt Library" "$TMP_HOME/.codex/AGENTS.md" >/dev/null

# Check skills + governance still deployed
test -L "$TMP_HOME/.agents/skills/vibebackbone"
grep -n "vibebackbone/AGENTS.md" "$TMP_HOME/.claude/CLAUDE.md" >/dev/null
grep -n "vibebackbone/SYSTEM.md" "$TMP_HOME/.claude/CLAUDE.md" >/dev/null
grep -n "vibebackbone:generated:start" "$TMP_HOME/.codex/AGENTS.md" >/dev/null
grep -n "Vibebackbone Runtime Behavior" "$TMP_HOME/.codex/AGENTS.md" >/dev/null
ls -l "$TMP_HOME/.pi/agent/AGENTS.md" >/dev/null
ls -l "$TMP_HOME/.pi/agent/SYSTEM.md" >/dev/null
python3 -m json.tool "$TMP_HOME/.config/opencode/opencode.json" >/dev/null

# Run second install (should be idempotent)
HOME="$TMP_HOME" bash "$ROOT/setup.sh"

# Run force-governance (should back up and overwrite)
HOME="$TMP_HOME" bash "$ROOT/setup.sh" --force-governance

# Uninstall
HOME="$TMP_HOME" bash "$ROOT/setup.sh" --uninstall

# Verify clean removal of prompts
test ! -e "$TMP_HOME/.agents/prompts/vibebackbone"
if [ -d "$TMP_HOME/.claude/commands" ]; then
  count="$(find "$TMP_HOME/.claude/commands" -name 'vbb-*.md' 2>/dev/null | wc -l | tr -d ' ')"
  [ "$count" -eq 0 ]
fi
if [ -d "$TMP_HOME/.config/opencode/commands" ]; then
  count="$(find "$TMP_HOME/.config/opencode/commands" -name 'vbb-*.md' 2>/dev/null | wc -l | tr -d ' ')"
  [ "$count" -eq 0 ]
fi
if [ -d "$TMP_HOME/.pi/agent/prompts" ]; then
  count="$(find "$TMP_HOME/.pi/agent/prompts" -type l 2>/dev/null | wc -l | tr -d ' ')"
  [ "$count" -eq 0 ]
fi

# Verify clean removal of governance
test ! -L "$TMP_HOME/.pi/agent/AGENTS.md"
test ! -L "$TMP_HOME/.pi/agent/SYSTEM.md"

echo "✓ smoke install passed"
