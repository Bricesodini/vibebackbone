#!/bin/bash
# tests/test_setup_smoke.sh — Phase 0 safety net for setup.sh refactor.
#
# Verifies, non-destructively, that the current setup.sh + (optional) setup-lib.sh
# keep the same surface and source files. Never runs an actual install/uninstall.
#
# Usage:
#     bash tests/test_setup_smoke.sh

set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETUP="$REPO_ROOT/setup.sh"
SETUP_LIB="$REPO_ROOT/setup-lib.sh"

PASS=0
FAIL=0
WARN=0

ok()   { echo "  PASS  $*"; PASS=$((PASS+1)); }
fail() { echo "  FAIL  $*"; FAIL=$((FAIL+1)); }
warn() { echo "  WARN  $*"; WARN=$((WARN+1)); }

echo "VBB setup.sh smoke test"
echo "  Repo : $REPO_ROOT"
echo ""

# --- 1. Syntax check ---------------------------------------------------------
echo "1. Syntax check"
if [ -f "$SETUP" ]; then
    if bash -n "$SETUP" 2>/dev/null; then
        ok "bash -n setup.sh"
    else
        fail "bash -n setup.sh (parse error)"
    fi
else
    fail "setup.sh not found at $SETUP"
fi

if [ -f "$SETUP_LIB" ]; then
    if bash -n "$SETUP_LIB" 2>/dev/null; then
        ok "bash -n setup-lib.sh"
    else
        fail "bash -n setup-lib.sh (parse error)"
    fi
else
    warn "setup-lib.sh not present (Phase 1 not yet applied — expected during Phase 0)"
fi

# --- 2. Source files presence -----------------------------------------------
echo ""
echo "2. Source files presence"
for path in AGENTS.md skills prompts SYSTEM.md CLAUDE.md; do
    if [ -e "$REPO_ROOT/$path" ]; then
        ok "source present: $path"
    else
        fail "source MISSING: $path"
    fi
done

# --- 3. Critical section markers (Phase 0 contract = no behavior change) -----
echo ""
echo "3. setup.sh + core/setup.sh structure markers (Core in core/, providers in setup.sh)"
# Sections that moved to core/setup.sh in Phase 2A
for marker in \
    "Universal skills symlink" \
    "Universal prompts symlink"
do
    if grep -qF "$marker" "$SETUP_LIB" 2>/dev/null || grep -qF "$marker" "$REPO_ROOT/core/setup.sh" 2>/dev/null; then
        ok "marker present (Core): $marker"
    else
        fail "marker MISSING: $marker"
    fi
done
# Provider-specific sections remain in setup.sh
for marker in \
    "Claude Code — settings.json" \
    "Claude Code — CLAUDE.md block" \
    "Codex — compiled AGENTS.md" \
    "Pi — symlinks" \
    "OpenCode — instructions" \
    "OpenCode — prompt commands" \
    "uninstall"
do
    if grep -qF "$marker" "$SETUP" 2>/dev/null; then
        ok "marker present (provider): $marker"
    else
        fail "marker MISSING (provider): $marker"
    fi
done

# --- 4. Public flags ---------------------------------------------------------
echo ""
echo "4. Public flags (introspection only, no execution)"
if grep -qE '^\[ "\$\{1\}" = "--uninstall" \]' "$SETUP" 2>/dev/null; then
    ok "--uninstall flag handled"
else
    fail "--uninstall flag handler missing"
fi
if grep -qE '^\[ "\$\{1\}" = "--force-governance" \]' "$SETUP" 2>/dev/null; then
    ok "--force-governance flag handled"
else
    fail "--force-governance flag handler missing"
fi

# --- 5. Helper identifiers (Phase 1 candidates) -----------------------------
echo ""
echo "5. Helper identifiers (audit, not removal)"
for helper in relpath _realpath _is_vbb_symlink needs_python backup_file symlink_if_absent generate_prompt_commands; do
    # Either defined in setup.sh (pre-Phase-1) OR sourced via setup-lib.sh (post-Phase-1).
    if [ -f "$SETUP_LIB" ] && grep -qE "^(function )?$helper\s*\(\)" "$SETUP_LIB" 2>/dev/null; then
        ok "helper $helper in setup-lib.sh (Phase 1 active)"
    elif grep -qE "^(function )?$helper\s*\(\)" "$SETUP" 2>/dev/null; then
        ok "helper $helper in setup.sh (Phase 1 not yet applied)"
    else
        warn "helper $helper not found in either setup.sh or setup-lib.sh (refactor may have removed it)"
    fi
done

# --- 6. Idempotence: --help is NOT a real flag -----------------------------
echo ""
echo "6. Unknown flag safety (--help is informational, not destructive)"
if grep -qE '"--help"' "$SETUP" 2>/dev/null; then
    ok "--help handled in setup.sh"
else
    warn "--help not handled — unknown flags fall through to install (acceptable for now)"
fi

# --- 7. No destructive auto-execution at parse time --------------------------
echo ""
echo "7. No top-level destructive calls before --uninstall/--force-governance parse"
# Anything before the --uninstall check that touches $HOME, .claude, .codex, .pi, .opencode
# would be a Phase 0 regression.
DESTRUCTIVE_PATTERNS=(
    'rm -rf "\$HOME'
    'rm -rf "\$LINK_NAME'
    'rm "\$PI_AGENTS"'
    'rm "\$PI_SYSTEM"'
)
EARLY_BAD=0
# Find the line number of the --uninstall check.
UNINSTALL_LINE=$(grep -n -- '--uninstall' "$SETUP" | head -1 | cut -d: -f1 || echo 0)
if [ "$UNINSTALL_LINE" -gt 0 ]; then
    for pat in "${DESTRUCTIVE_PATTERNS[@]}"; do
        # Search lines BEFORE the --uninstall check.
        if head -n "$UNINSTALL_LINE" "$SETUP" | grep -E "$pat" >/dev/null 2>&1; then
            fail "destructive pattern before --uninstall: $pat"
            EARLY_BAD=$((EARLY_BAD + 1))
        fi
    done
    if [ "$EARLY_BAD" -eq 0 ]; then
        ok "no destructive operations before --uninstall check (line $UNINSTALL_LINE)"
    fi
else
    warn "--uninstall check line not found"
fi

# --- Summary -----------------------------------------------------------------
echo ""
echo "----------------------------------------"
echo "PASS=$PASS  FAIL=$FAIL  WARN=$WARN"
echo "----------------------------------------"

if [ "$FAIL" -gt 0 ]; then
    echo "SMOKE TEST FAILED"
    exit 1
fi
echo "SMOKE TEST OK"
exit 0
