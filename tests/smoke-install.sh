#!/bin/bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_HOME="$(mktemp -d)"
echo "Testing install with HOME=$TMP_HOME"

# Run first install (should create everything)
HOME="$TMP_HOME" bash "$ROOT/setup.sh"

# Regression: old Codex files may contain nested generated markers. A reinstall
# must replace the whole generated region, not only the first inner block.
cat > "$TMP_HOME/.codex/AGENTS.md" <<'EOF'
custom prefix
<!-- vibebackbone:generated:start -->
outer stale
<!-- vibebackbone:generated:start -->
inner stale
<!-- Source: /Users/bricesodini/01_ai-stack/vibebackbone/AGENTS.md -->
<!-- vibebackbone:generated:end -->
outer stale tail
<!-- vibebackbone:generated:end -->
custom suffix
EOF
HOME="$TMP_HOME" bash "$ROOT/setup.sh" > "$TMP_HOME/install-nested.log"
test "$(grep -c "vibebackbone:generated:start" "$TMP_HOME/.codex/AGENTS.md")" -eq 1
test "$(grep -c "vibebackbone:generated:end" "$TMP_HOME/.codex/AGENTS.md")" -eq 1
! grep -q "/Users/bricesodini/01_ai-stack" "$TMP_HOME/.codex/AGENTS.md"
grep -q "custom prefix" "$TMP_HOME/.codex/AGENTS.md"
grep -q "custom suffix" "$TMP_HOME/.codex/AGENTS.md"

HOME="$TMP_HOME" bash "$ROOT/setup.sh" > "$TMP_HOME/install-second.log"
grep -qE "Done — [0-9]+ skills" "$TMP_HOME/install-second.log"

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
grep -n "quick-task.*1-p-vbb-quick-task.md" "$TMP_HOME/.codex/AGENTS.md" >/dev/null
grep -n "structured-task.*1-p-vbb-structured-task.md" "$TMP_HOME/.codex/AGENTS.md" >/dev/null

# Check skills + governance still deployed
test -L "$TMP_HOME/.agents/skills/vibebackbone"
grep -n "vibebackbone/AGENTS.md" "$TMP_HOME/.claude/CLAUDE.md" >/dev/null
grep -n "vibebackbone/SYSTEM.md" "$TMP_HOME/.claude/CLAUDE.md" >/dev/null
grep -n "vibebackbone:generated:start" "$TMP_HOME/.codex/AGENTS.md" >/dev/null
grep -n "SYSTEM.md" "$TMP_HOME/.codex/AGENTS.md" >/dev/null
ls -l "$TMP_HOME/.pi/agent/AGENTS.md" >/dev/null
ls -l "$TMP_HOME/.pi/agent/SYSTEM.md" >/dev/null
python3 -m json.tool "$TMP_HOME/.config/opencode/opencode.json" >/dev/null

# Run second install already happened above (should be idempotent)

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
