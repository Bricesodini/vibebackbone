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

# Compute a relative path from $1 (base directory) to $2 (target).
# Both args must be absolute paths.
relpath() {
  local base="$1" target="$2"
  # Use python for correctness (handles edge cases on macOS)
  if command -v python3 &>/dev/null; then
    python3 -c "import os; print(os.path.relpath('$target', '$base'))"
  else
    # Fallback: use perl or absolute path
    echo "$target"
  fi
}

_is_vbb_symlink() {
  # Check if a symlink points to a vibebackbone source path,
  # regardless of whether the target is absolute or relative.
  local link="$1"
  local expected_abs="$2"  # absolute path to source (e.g. $PROMPTS_SRC)
  [ -L "$link" ] || return 1
  local target
  target="$(readlink "$link")"
  # Direct absolute match
  [ "$target" = "$expected_abs" ] && return 0
  # Resolve relative link to absolute for comparison
  local resolved
  resolved="$(cd "$(dirname "$link")" && cd "$(dirname "$target")" && pwd)/$(basename "$target")" 2>/dev/null || return 1
  [ "$resolved" = "$expected_abs" ] && return 0
  return 1
}

needs_python() {
  if ! command -v python3 &>/dev/null; then
    echo "⚠  python3 not found — skipping operation that requires JSON/block editing"
    return 1
  fi
  return 0
}

backup_file() {
  local file="$1"
  if [ -f "$file" ] && [ ! -L "$file" ]; then
    local backup_path="$file.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$file" "$backup_path"
    echo "✓ Backup created: $backup_path"
  fi
}

# Symlink helper: respects FORCE_GOVERNANCE
symlink_if_absent() {
  local src="$1" dst="$2" label="$3"
  if [ -L "$dst" ]; then
    local current
    current="$(readlink "$dst")"
    # Accept both absolute and relative forms of the same target
    if [ "$current" = "$src" ]; then
      echo "✓ $label: already linked"
      return 0
    fi
    local resolved_current
    resolved_current="$(cd "$(dirname "$dst")" && cd "$(dirname "$current")" && pwd)/$(basename "$current")" 2>/dev/null || true
    if [ "$resolved_current" = "$src" ]; then
      echo "✓ $label: already linked (relative)"
      return 0
    fi
  fi
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    if [ "$FORCE_GOVERNANCE" = true ]; then
      backup_file "$dst"
      ln -sfn "$src" "$dst"
      echo "✓ $label: backed up and symlinked"
    else
      echo "⚠ $label: existing custom file skipped (use --force-governance to override)"
    fi
    return 0
  fi
  if [ ! -e "$dst" ]; then
    ln -sfn "$src" "$dst"
    echo "✓ $label: symlink created"
  fi
}

# Count skill directories, excluding catalog files such as INDEX.yaml.
count_skills() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' '
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

# Generate prompt commands for a provider (Claude, OpenCode)
generate_prompt_commands() {
  local dst_dir="$1"
  local label="$2"
  local ok_var="$3"
  local skip_var="$4"
  local ok=0 skip=0

  if [ "$PROMPTS_AVAILABLE" = true ]; then
    mkdir -p "$dst_dir"
    for src in "$PROMPTS_SRC"/*.md; do
      [ -f "$src" ] || continue
      name=$(basename "$src" .md)
      [[ "$name" == "README" || "$name" == "INDEX" ]] && continue
      dst="$dst_dir/vbb-$name.md"
      marker="<!-- vibebackbone:generated from $src -->"

      if [ -f "$dst" ] && ! grep -q "vibebackbone:generated" "$dst" 2>/dev/null; then
        if [ "$FORCE_GOVERNANCE" = true ]; then
          backup_file "$dst"
        else
          echo "⚠ $label: existing custom $(basename "$dst") skipped"
          skip=$((skip + 1))
          continue
        fi
      fi

      {
        echo "---"
        echo "description: Vibebackbone — $name"
        echo "---"
        echo "$marker"
        cat "$src"
        echo ""
        echo "---"
        echo "User request:"
        echo '\$ARGUMENTS'
      } > "$dst"
      ok=$((ok + 1))
    done
    if [ "$skip" -eq 0 ]; then
      echo "✓ $label: $ok commands generated"
    fi
  fi

  eval "$ok_var=\$ok"
  eval "$skip_var=\$skip"
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
import sys, re
path = sys.argv[1]
with open(path) as f:
    content = f.read()
pattern = r'<!-- vibebackbone:generated:start -->.*?<!-- vibebackbone:generated:end -->\n*'
cleaned = re.sub(pattern, '', content, flags=re.DOTALL)
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

# ── Pre-flight checks ─────────────────────────────────────────────────────────

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

PROMPT_COUNT=0
PROMPT_ADAPTER_COUNT=0
if [ "$PROMPTS_AVAILABLE" = true ]; then
  PROMPT_COUNT=$(count_prompts_total "$PROMPTS_SRC")
  PROMPT_ADAPTER_COUNT=$(count_prompt_adapters "$PROMPTS_SRC")
fi

SKILL_COUNT=$(count_skills "$SKILLS_SRC")

# ── 1. Universal skills symlink ──────────────────────────────────────────────
echo "Installing vibebackbone..."
echo "  Repo : $REPO_ROOT"
echo ""

mkdir -p "$GLOBAL_SKILLS"
[ -L "$LINK_NAME" ] && rm "$LINK_NAME"
SKILLS_REL="$(relpath "$GLOBAL_SKILLS" "$SKILLS_SRC")"
ln -sfn "$SKILLS_REL" "$LINK_NAME"
echo "✓ ~/.agents/skills/vibebackbone → skills symlink (Pi, OpenCode, Codex)"

# ── 2. Universal prompts symlink ─────────────────────────────────────────────
if [ "$PROMPTS_AVAILABLE" = true ]; then
  mkdir -p "$GLOBAL_PROMPTS"
  if [ -L "$PROMPTS_LINK" ] && [ "$(readlink "$PROMPTS_LINK")" = "$PROMPTS_SRC" -o "$(readlink "$PROMPTS_LINK")" = "$(relpath "$GLOBAL_PROMPTS" "$PROMPTS_SRC")" ]; then
    echo "✓ Prompts: ~/.agents/prompts/vibebackbone already linked"
  elif [ -e "$PROMPTS_LINK" ] && [ ! -L "$PROMPTS_LINK" ]; then
    if [ "$FORCE_GOVERNANCE" = true ]; then
      backup_file "$PROMPTS_LINK"
      rm -rf "$PROMPTS_LINK"
      PROMPTS_REL="$(relpath "$GLOBAL_PROMPTS" "$PROMPTS_SRC")"
      ln -sfn "$PROMPTS_REL" "$PROMPTS_LINK"
      echo "✓ Prompts: ~/.agents/prompts/vibebackbone backed up and symlinked"
    else
      echo "⚠ Prompts: existing custom ~/.agents/prompts/vibebackbone skipped"
    fi
  else
    [ -L "$PROMPTS_LINK" ] && rm "$PROMPTS_LINK"
    PROMPTS_REL="$(relpath "$GLOBAL_PROMPTS" "$PROMPTS_SRC")"
    ln -sfn "$PROMPTS_REL" "$PROMPTS_LINK"
    echo "✓ Prompts: ~/.agents/prompts/vibebackbone symlinked"
  fi
fi

# ── 3. Claude Code — settings.json ──────────────────────────────────────────
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

# ── 4. Claude Code — CLAUDE.md block ─────────────────────────────────────────
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

# ── 5. Claude Code — prompt commands ─────────────────────────────────────────
CLAUDE_PROMPTS_OK=0
CLAUDE_PROMPTS_SKIP=0
generate_prompt_commands "$CLAUDE_COMMANDS" "Claude prompts" "CLAUDE_PROMPTS_OK" "CLAUDE_PROMPTS_SKIP"

# ── 6. Codex — compiled AGENTS.md ───────────────────────────────────────────
mkdir -p "$HOME/.codex"

if needs_python; then
  python3 - "$CODEX_AGENTS" "$AGENTS_SRC" "$SYSTEM_SRC" "$SYSTEM_AVAILABLE" "$FORCE_GOVERNANCE" "$PROMPTS_SRC" "$PROMPTS_AVAILABLE" <<'PY'
import sys, os, re
path, agents_src, system_src, system_available, force_governance, prompts_src, prompts_available = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
force = force_governance.lower() == "true"
system_available_flag = system_available.lower() == "true"
prompts_available_flag = prompts_available.lower() == "true"

def build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag):
    lines = [
        "\n<!-- vibebackbone:generated:start -->\n",
        "# Vibebackbone Governance\n",
        f"<!-- Source: {agents_src} -->\n",
        open(agents_src).read(),
    ]
    if system_available_flag:
        lines.extend([
            "\n---\n",
            "# Vibebackbone Runtime Behavior\n",
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
            "When the user asks to use a Vibebackbone prompt such as:\n",
            "- `quick-task`\n",
            "- `structured-task`\n",
            "- `audit-task`\n",
            "- `release-check`\n",
            "- `session-handoff`\n",
            "read the matching Markdown prompt from that directory and apply it before execution.\n",
            "Do not invent prompt behavior from the name alone. If the prompt file is missing, state that explicitly and proceed only as best-effort.\n",
        ])
    lines.append("\n<!-- vibebackbone:generated:end -->\n")
    return "".join(lines)

if os.path.exists(path):
    with open(path) as f:
        content = f.read()
    has_markers = "<!-- vibebackbone:generated:start -->" in content

    if has_markers:
        pattern = r'<!-- vibebackbone:generated:start -->.*?<!-- vibebackbone:generated:end -->\n*'
        new_block = build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag)
        content = re.sub(pattern, new_block.rstrip() + "\n", content, flags=re.DOTALL)
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
mkdir -p "$HOME/.pi/agent"
symlink_if_absent "$AGENTS_SRC" "$PI_AGENTS" "Pi: AGENTS.md"
if [ "$SYSTEM_AVAILABLE" = true ]; then
  symlink_if_absent "$SYSTEM_SRC" "$PI_SYSTEM" "Pi: SYSTEM.md"
fi

PI_PROMPTS_OK=0
PI_PROMPTS_SKIP=0

if [ "$PROMPTS_AVAILABLE" = true ]; then
  mkdir -p "$PI_PROMPTS"
  for src in "$PROMPTS_SRC"/*.md; do
    [ -f "$src" ] || continue
    name=$(basename "$src")
    [[ "$name" == "README.md" || "$name" == "INDEX.md" ]] && continue
    dst="$PI_PROMPTS/$name"
    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
      PI_PROMPTS_OK=$((PI_PROMPTS_OK + 1))
      continue
    fi
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
      if [ "$FORCE_GOVERNANCE" = true ]; then
        backup_file "$dst"
        ln -sfn "$src" "$dst"
        PI_PROMPTS_OK=$((PI_PROMPTS_OK + 1))
      else
        echo "⚠ Pi prompts: existing custom $name skipped"
        PI_PROMPTS_SKIP=$((PI_PROMPTS_SKIP + 1))
      fi
      continue
    fi
    if [ ! -e "$dst" ]; then
      ln -sfn "$src" "$dst"
      PI_PROMPTS_OK=$((PI_PROMPTS_OK + 1))
    fi
  done
  if [ "$PI_PROMPTS_SKIP" -eq 0 ]; then
    echo "✓ Pi prompts: $PI_PROMPTS_OK prompts linked"
  fi
fi

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

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "✓ Done — $SKILL_COUNT skills · $PROMPT_COUNT prompts available ($PROMPT_ADAPTER_COUNT adapter commands)"

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
if [ -L "$PI_AGENTS" ] && [ "$(readlink "$PI_AGENTS")" = "$AGENTS_SRC" ]; then
  echo "  Pi          : AGENTS + SYSTEM symlinked"
fi
if [ -f "$OPENCODE_JSON" ] && python3 -c "import json,sys; cfg=json.load(open('$OPENCODE_JSON')); print('$AGENTS_SRC' in cfg.get('instructions',[]))" 2>/dev/null | grep -q True; then
  echo "  OpenCode    : AGENTS + SYSTEM referenced"
fi

echo ""
echo "To force governance deployment:"
echo "  bash $REPO_ROOT/setup.sh --force-governance"
echo "To update:"
echo "  cd $REPO_ROOT && git pull"
echo "To remove:"
echo "  bash $REPO_ROOT/setup.sh --uninstall"
