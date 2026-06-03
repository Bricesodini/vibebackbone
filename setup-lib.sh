#!/bin/bash
# setup-lib.sh — Shared helpers for setup.sh (Phase 1 refactor).
#
# This file is sourced by setup.sh (and any future per-distribution
# setup.sh under core/, distributions/hermes/, distributions/pi/,
# distributions/claude/, distributions/codex/, distributions/opencode/).
#
# Behavior is intentionally identical to the pre-Phase-1 inlined helpers
# in setup.sh. Do not introduce new side effects, new flags, or new
# defaults here.
#
# Conventions:
#   - Functions starting with `_` are private to this lib (callers
#     should not rely on them).
#   - Public helpers: relpath, needs_python, backup_file,
#     symlink_if_absent, generate_prompt_commands.
#   - All other globals (REPO_ROOT, PROMPTS_SRC, PROMPTS_AVAILABLE,
#     FORCE_GOVERNANCE) are inherited from the caller (setup.sh) and
#     must remain compatible with the pre-Phase-1 contract.
#
# If you are reading this for the first time, see the pre-Phase-1
# git history of setup.sh for the original definitions; this file is
# a pure extraction (no edits, no fixes, no reformatting beyond the
# leading comment block).

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

# Resolve a path to its real absolute form, following symlinks and resolving
# case-insensitively on macOS (APFS is case-insensitive by default).
_realpath() {
  local path="$1"
  # Try realpath first (cross-platform, follows symlinks)
  if command -v realpath &>/dev/null; then
    realpath "$path" 2>/dev/null && return
  fi
  # macOS fallback: use python for case-insensitive resolution
  if command -v python3 &>/dev/null; then
    python3 -c "
import os, sys
p = '$path'
# Resolve parent case-insensitively on macOS
base = os.path.dirname(p)
name = os.path.basename(p)
try:
    for entry in os.listdir(base if base else '.'):
        if entry.lower() == name.lower():
            print(os.path.join(base, entry) if base else entry)
            break
    else:
        print(p)
except Exception:
    print(p)
" && return
  fi
  echo "$path"
}

_is_vbb_symlink() {
  # Check if a symlink points to a vibebackbone source path,
  # regardless of whether the target is absolute or relative,
  # and case-insensitively on macOS.
  local link="$1"
  local expected_abs="$2"  # absolute path to source (e.g. $PROMPTS_SRC)
  [ -L "$link" ] || return 1
  local target
  target="$(readlink "$link")"
  # Direct absolute match (exact case)
  [ "$target" = "$expected_abs" ] && return 0
  # Case-insensitive check on macOS
  local resolved
  if command -v realpath &>/dev/null; then
    resolved="$(realpath "$link" 2>/dev/null)"
  else
    resolved="$(_realpath "$link")"
  fi
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
    local current resolved_current
    current="$(readlink "$dst")"
    # Accept both absolute and relative forms of the same target
    if [ "$current" = "$src" ]; then
      echo "✓ $label: already linked"
      return 0
    fi
    # Case-insensitive resolution on macOS
    if command -v realpath &>/dev/null; then
      resolved_current="$(realpath "$dst" 2>/dev/null)"
    else
      resolved_current="$(_realpath "$dst")"
    fi
    if [ "$resolved_current" = "$src" ]; then
      echo "✓ $label: already linked (case-insensitive match)"
      return 0
    fi
    # Symlink exists but points to a different target → replace
    rm "$dst"
    ln -sfn "$src" "$dst"
    echo "✓ $label: symlink updated (was pointing elsewhere)"
    return 0
  fi
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    if [ "$FORCE_GOVERNANCE" = true ]; then
      backup_file "$dst"
      rm "$dst"
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

      if [ -L "$dst" ]; then
        # Existing symlink → always replace (covers old source, case-insensitivity)
        rm "$dst"
      elif [ -f "$dst" ]; then
        if grep -q "vibebackbone:generated" "$dst" 2>/dev/null; then
          # Our own generated file → replace
          rm "$dst"
        elif [ "$FORCE_GOVERNANCE" = true ]; then
          # Custom file + force → backup and replace
          backup_file "$dst"
          rm "$dst"
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
