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
#   bash setup.sh                  # Auto-detect + interactive plan
#   bash setup.sh --auto           # Explicit auto-detect
#   bash setup.sh --provider claude --provider pi
#                                   # Selective install
#   bash setup.sh --dry-run         # Print the plan only
#   bash setup.sh --force-governance # Install and overwrite with backup
#   bash setup.sh --no-interactive   # Skip confirmation prompt
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
DRY_RUN=false
NO_INTERACTIVE=false
UNINSTALL_REQUESTED=false
INSTALL_MODE="auto"
ALL_PROVIDERS=(claude codex pi opencode)
SELECTED_PROVIDERS=()

usage() {
  cat <<'EOF'
Usage:
  bash setup.sh [--auto] [--provider <name>] [--dry-run] [--force-governance] [--no-interactive]
  bash setup.sh --uninstall

Modes:
  --auto                 Install the core + all available providers (default)
  --provider <name>      Install only the named provider(s) in addition to the core
  --force-governance     Allow controlled overwrites with backup when custom files exist
  --dry-run              Print the installation plan only
  --no-interactive       Skip the confirmation prompt
  Interactive mode       Arrow-key checklist, space toggles, enter validates
EOF
}

provider_label() {
  case "$1" in
    claude) echo "Claude Code" ;;
    codex) echo "Codex" ;;
    pi) echo "Pi" ;;
    opencode) echo "OpenCode" ;;
    *) echo "$1" ;;
  esac
}

provider_setup_path() {
  case "$1" in
    claude) echo "$REPO_ROOT/distributions/claude/setup.sh" ;;
    codex) echo "$REPO_ROOT/distributions/codex/setup.sh" ;;
    pi) echo "$REPO_ROOT/distributions/pi/setup.sh" ;;
    opencode) echo "$REPO_ROOT/distributions/opencode/setup.sh" ;;
    *) return 1 ;;
  esac
}

provider_is_selected() {
  local needle="$1" item
  for item in "${SELECTED_PROVIDERS[@]}"; do
    [ "$item" = "$needle" ] && return 0
  done
  return 1
}

provider_select() {
  local provider="$1"
  provider_is_selected "$provider" || SELECTED_PROVIDERS+=("$provider")
}

provider_deselect() {
  local provider="$1" item next=()
  for item in "${SELECTED_PROVIDERS[@]}"; do
    [ "$item" = "$provider" ] && continue
    next+=("$item")
  done
  SELECTED_PROVIDERS=("${next[@]}")
}

provider_toggle() {
  local provider="$1"
  if provider_is_selected "$provider"; then
    provider_deselect "$provider"
  else
    provider_select "$provider"
  fi
}

select_all_providers() {
  SELECTED_PROVIDERS=("${ALL_PROVIDERS[@]}")
}

select_no_providers() {
  SELECTED_PROVIDERS=()
}

enable_selective_mode() {
  if [ "$INSTALL_MODE" != "selective" ]; then
    INSTALL_MODE="selective"
  fi
}

sync_install_mode() {
  if [ "$FORCE_GOVERNANCE" = true ]; then
    INSTALL_MODE="governance"
    return 0
  fi

  if [ "${#SELECTED_PROVIDERS[@]}" -eq "${#ALL_PROVIDERS[@]}" ]; then
    INSTALL_MODE="auto"
  else
    INSTALL_MODE="selective"
  fi
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --help|-h)
        usage
        exit 0
        ;;
      --uninstall)
        UNINSTALL_REQUESTED=true
        ;;
      --auto)
        INSTALL_MODE="auto"
        select_all_providers
        ;;
      --provider)
        shift
        [ "$#" -gt 0 ] || { echo "✗ --provider requires a provider name"; exit 1; }
        enable_selective_mode
        case "$1" in
          all)
            select_all_providers
            INSTALL_MODE="auto"
            ;;
          claude|codex|pi|opencode)
            provider_is_selected "$1" || SELECTED_PROVIDERS+=("$1")
            ;;
          *)
            echo "✗ unknown provider: $1"
            exit 1
            ;;
        esac
        ;;
      --provider=*)
        provider_value="${1#*=}"
        enable_selective_mode
        case "$provider_value" in
          all)
            select_all_providers
            INSTALL_MODE="auto"
            ;;
          claude|codex|pi|opencode)
            provider_is_selected "$provider_value" || SELECTED_PROVIDERS+=("$provider_value")
            ;;
          *)
            echo "✗ unknown provider: $provider_value"
            exit 1
            ;;
        esac
        ;;
      --dry-run)
        DRY_RUN=true
        ;;
      --force-governance)
        FORCE_GOVERNANCE=true
        INSTALL_MODE="governance"
        ;;
      --no-interactive)
        NO_INTERACTIVE=true
        ;;
      *)
        echo "✗ unknown flag: $1"
        usage
        exit 1
        ;;
    esac
    shift
  done

  if [ "${#SELECTED_PROVIDERS[@]}" -eq 0 ] && [ "$UNINSTALL_REQUESTED" = false ]; then
    select_all_providers
  fi

  sync_install_mode
}

validate_selected_providers() {
  local provider path
  for provider in "${SELECTED_PROVIDERS[@]}"; do
    path="$(provider_setup_path "$provider")" || true
    if [ ! -f "$path" ]; then
      echo "✗ missing provider setup: $path"
      exit 1
    fi
  done
}

print_install_plan() {
  local provider
  local mode_label
  case "$INSTALL_MODE" in
    auto) mode_label="auto-detect" ;;
    selective) mode_label="selective install" ;;
    governance) mode_label="advanced/governance" ;;
    *) mode_label="$INSTALL_MODE" ;;
  esac
  echo ""
  echo "Installation plan:"
  echo "  Mode            : $mode_label"
  echo "  Governance      : $( [ "$FORCE_GOVERNANCE" = true ] && echo "overwrite with backup" || echo "preserve existing custom files" )"
  echo "  Dry-run         : $( [ "$DRY_RUN" = true ] && echo "yes" || echo "no" )"
  echo "  Interactive     : $( [ "$NO_INTERACTIVE" = true ] && echo "no" || echo "yes" )"
  echo "  Core            : install"
  for provider in "${ALL_PROVIDERS[@]}"; do
    if provider_is_selected "$provider"; then
      echo "  $(printf '%-14s' "$(provider_label "$provider")") : install"
    else
      echo "  $(printf '%-14s' "$(provider_label "$provider")") : skip"
    fi
  done
}

confirm_installation() {
  if [ "$DRY_RUN" = true ] || [ "$NO_INTERACTIVE" = true ] || [ ! -t 0 ]; then
    return 0
  fi

  local old_stty
  local cursor=0
  local key key2 key3 provider idx
  old_stty="$(stty -g)"
  cleanup_interactive_ui() {
    stty "$old_stty" 2>/dev/null || true
    tput cnorm 2>/dev/null || true
    printf '\n'
  }
  trap cleanup_interactive_ui EXIT INT TERM

  stty -echo -icanon time 0 min 1
  tput civis 2>/dev/null || true

  while true; do
    printf '\033[2J\033[H'
    echo "Installation selection:"
    echo "  Use ↑/↓ to move, Space to toggle, Enter to continue."
    echo "  A: all | N: none | G: governance | D: dry-run | Q: quit"
    echo ""
    for idx in "${!ALL_PROVIDERS[@]}"; do
      provider="${ALL_PROVIDERS[$idx]}"
      if [ "$idx" -eq "$cursor" ]; then
        printf "  > "
      else
        printf "    "
      fi
      printf "[%s] %s\n" "$(provider_is_selected "$provider" && echo x || echo ' ')" "$(provider_label "$provider")"
    done
    echo ""
    echo "  Mode       : $INSTALL_MODE"
    echo "  Dry-run    : $( [ "$DRY_RUN" = true ] && echo on || echo off )"
    echo "  Governance : $( [ "$FORCE_GOVERNANCE" = true ] && echo on || echo off )"
    echo ""
    echo "  Enter to start."

    IFS= read -rsn1 key || exit 1
    case "$key" in
      "")
        break
        ;;
      " ")
        provider_toggle "${ALL_PROVIDERS[$cursor]}"
        ;;
      a|A)
        select_all_providers
        ;;
      n|N)
        select_no_providers
        ;;
      d|D)
        if [ "$DRY_RUN" = true ]; then
          DRY_RUN=false
        else
          DRY_RUN=true
        fi
        ;;
      g|G)
        if [ "$FORCE_GOVERNANCE" = true ]; then
          FORCE_GOVERNANCE=false
        else
          FORCE_GOVERNANCE=true
        fi
        ;;
      q|Q)
        echo "Aborted."
        exit 1
        ;;
      $'\033')
        IFS= read -rsn1 key2 || key2=""
        IFS= read -rsn1 key3 || key3=""
        case "$key2$key3" in
          "[A")
            if [ "$cursor" -gt 0 ]; then
              cursor=$((cursor - 1))
            else
              cursor=$((${#ALL_PROVIDERS[@]} - 1))
            fi
            ;;
          "[B")
            cursor=$(((cursor + 1) % ${#ALL_PROVIDERS[@]}))
            ;;
        esac
        ;;
      $'\r'|$'\n')
        break
        ;;
    esac
    sync_install_mode
  done

  cleanup_interactive_ui
  trap - EXIT INT TERM
  sync_install_mode
}

run_provider_install() {
  case "$1" in
    claude)
      source "$REPO_ROOT/distributions/claude/setup.sh"
      claude_install
      ;;
    codex)
      source "$REPO_ROOT/distributions/codex/setup.sh"
      codex_install
      ;;
    pi)
      source "$REPO_ROOT/distributions/pi/setup.sh"
      pi_install
      ;;
    opencode)
      source "$REPO_ROOT/distributions/opencode/setup.sh"
      opencode_install
      ;;
  esac
}

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

parse_args "$@"

if [ "$UNINSTALL_REQUESTED" = true ]; then
  uninstall
fi

# ── Core install (pre-flight + universal symlinks) ─────────────────────────
# Core logic moved to core/setup.sh (Phase 2A). Globals set by core_install
# (PROMPTS_AVAILABLE, SYSTEM_AVAILABLE, *_COUNT) feed the per-provider
# sections below.
source "$REPO_ROOT/core/setup.sh"
core_preflight
validate_selected_providers
print_install_plan
confirm_installation

if [ "$DRY_RUN" = true ]; then
  echo ""
  echo "✓ Dry-run complete — no files were written"
  exit 0
fi

core_install

PI_PROMPTS_OK=0
PI_PROMPTS_SKIP=0
CLAUDE_PROMPTS_OK=0
CLAUDE_PROMPTS_SKIP=0
OPENCODE_PROMPTS_OK=0
OPENCODE_PROMPTS_SKIP=0
for provider in "${SELECTED_PROVIDERS[@]}"; do
  run_provider_install "$provider"
done

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
if provider_is_selected pi && [ "$PI_PROMPTS_OK" -gt 0 ]; then
  echo "  Pi          : $PI_PROMPTS_OK linked / $PI_PROMPTS_SKIP skipped"
fi
if provider_is_selected claude && [ "$CLAUDE_PROMPTS_OK" -gt 0 ]; then
  echo "  Claude Code : $CLAUDE_PROMPTS_OK generated / $CLAUDE_PROMPTS_SKIP skipped"
fi
if provider_is_selected opencode && [ "$OPENCODE_PROMPTS_OK" -gt 0 ]; then
  echo "  OpenCode    : $OPENCODE_PROMPTS_OK generated / $OPENCODE_PROMPTS_SKIP skipped"
fi
if provider_is_selected codex && [ -f "$CODEX_AGENTS" ] && grep -q "Vibebackbone Prompt Library" "$CODEX_AGENTS" 2>/dev/null; then
  echo "  Codex       : prompt library referenced in AGENTS.md"
fi

if [ "$PI_PROMPTS_SKIP" -gt 0 ] || [ "$CLAUDE_PROMPTS_SKIP" -gt 0 ] || [ "$OPENCODE_PROMPTS_SKIP" -gt 0 ]; then
  echo ""
  echo "Warnings:"
  [ "$PI_PROMPTS_SKIP" -gt 0 ] && echo "  ⚠ Pi prompts          : $PI_PROMPTS_SKIP custom files skipped"
  [ "$CLAUDE_PROMPTS_SKIP" -gt 0 ] && echo "  ⚠ Claude Code prompts : $CLAUDE_PROMPTS_SKIP custom commands skipped"
  [ "$OPENCODE_PROMPTS_SKIP" -gt 0 ] && echo "  ⚠ OpenCode prompts    : $OPENCODE_PROMPTS_SKIP custom commands skipped"
fi

echo "Governance / runtime:"
if provider_is_selected claude && [ -f "$CLAUDE_MD" ] && grep -qF "$AGENTS_SRC" "$CLAUDE_MD" 2>/dev/null; then
  echo "  Claude Code : AGENTS + SYSTEM referenced"
fi
if provider_is_selected codex && [ -f "$CODEX_AGENTS" ] && grep -q "vibebackbone:generated:start" "$CODEX_AGENTS" 2>/dev/null; then
  if grep -q "Vibebackbone Prompt Library" "$CODEX_AGENTS" 2>/dev/null; then
    echo "  Codex       : AGENTS + SYSTEM + Prompt Library compiled"
  else
    echo "  Codex       : AGENTS + SYSTEM compiled"
  fi
fi
if provider_is_selected pi && [ -L "$PI_AGENTS" ] && _is_vbb_symlink "$PI_AGENTS" "$AGENTS_SRC"; then
  echo "  Pi          : AGENTS + SYSTEM symlinked"
fi
if provider_is_selected opencode && [ -f "$OPENCODE_JSON" ] && python3 -c "
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
