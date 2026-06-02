#!/usr/bin/env bash
# verify.sh — Hermes/Cody distribution verification (NON-DESTRUCTIVE)
# F-015 step 2: docs first, then verify, then install (deferred).
# This script is read-only: it never writes, copies, or modifies files.
# Exit 0 = PASS, Exit 1 = FAIL.

set -u  # NOT -e: we want every check to run, even if some fail, and report all.

VBB_HOME="${VBB_HOME:-$HOME/02_Dev/vibebackbone}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CODY_CHECK="${CODY_CHECK:-${HERMES_HOME}/bin/cody-check}"

# SCRIPT_DIR: directory of this script (so the script is relocatable).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# REPO_ROOT: parent of scripts/hermes/ (i.e. VBB Core repo root).
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
# If the operator did not explicitly override VBB_HOME, use the auto-detected
# repo root. This makes in-tree runs work without exporting anything.
if [ -z "${VBB_HOME_OVERRIDE:-}" ]; then
    VBB_HOME="$REPO_ROOT"
fi

PASS=0
FAIL=0

# check "name" "eval-test" [hint]
# Runs the eval-test string. On success: PASS+1, prints [PASS]. On failure:
# FAIL+1, prints [FAIL] and optional hint.
check() {
    local name="$1"
    local cmd="$2"
    local hint="${3:-}"
    if eval "$cmd" >/dev/null 2>&1; then
        printf "  [PASS] %s\n" "$name"
        PASS=$((PASS + 1))
    else
        printf "  [FAIL] %s\n" "$name"
        if [ -n "$hint" ]; then
            printf "         hint: %s\n" "$hint"
        fi
        FAIL=$((FAIL + 1))
    fi
}

echo "=== Hermes/Cody distribution verification ==="
echo "VBB_HOME=$VBB_HOME"
echo "HERMES_HOME=$HERMES_HOME"
echo "CODY_CHECK=$CODY_CHECK"
echo ""

echo "--- VBB Core tools ---"
check "VBB_HOME detectable" "[ -d \"$VBB_HOME\" ]"
check "tools/vbb-architecture.py present" "[ -f \"$VBB_HOME/tools/vbb-architecture.py\" ]"
check "tools/vbb-contract-lint.py present" "[ -f \"$VBB_HOME/tools/vbb-contract-lint.py\" ]"
check "tools/vbb-gate-check.py present" "[ -f \"$VBB_HOME/tools/vbb-gate-check.py\" ]"
check "tools/vbb-phase-router.py present (optional)" \
    "[ -f \"$VBB_HOME/tools/vbb-phase-router.py\" ]" \
    "expected: phase router script (optional but recommended)"

# Sanity: the main gate tool must actually run. If Python is missing or the
# file is corrupt, this catches it before a worker ever invokes it.
if [ -f "$VBB_HOME/tools/vbb-gate-check.py" ]; then
    check "tools/vbb-gate-check.py --help runs (sanity)" \
        "command -v python >/dev/null 2>&1 && python \"$VBB_HOME/tools/vbb-gate-check.py\" --help" \
        "expected: python 3.10+ on PATH and vbb-gate-check.py is a valid script"
else
    check "tools/vbb-gate-check.py --help runs (sanity)" \
        "false" \
        "skipped: tools/vbb-gate-check.py not present"
fi

echo ""
echo "--- Hermes profiles ---"
for prof in vbb-cody-orchestrator vbb-fast-worker vbb-struct-worker \
            vbb-audit-worker vbb-close-worker; do
    check "profile $prof present" "[ -f \"$HERMES_HOME/profiles/$prof/SOUL.md\" ]"
done

echo ""
echo "--- SOUL.md portability (F-004) ---"
for prof in vbb-cody-orchestrator vbb-fast-worker vbb-struct-worker \
            vbb-audit-worker vbb-close-worker; do
    soul="$HERMES_HOME/profiles/$prof/SOUL.md"
    if [ -f "$soul" ]; then
        check "$prof contains CODY_CHECK" "grep -q CODY_CHECK \"$soul\""
        check "$prof contains HERMES_HOME" "grep -q HERMES_HOME \"$soul\""
        check "$prof has no hardcoded /Users/bot/.hermes/bin/cody-check" \
            "! grep -q '/Users/bot/.hermes/bin/cody-check' \"$soul\""
    else
        check "$prof contains CODY_CHECK" "false" "skipped: SOUL.md missing"
        check "$prof contains HERMES_HOME" "false" "skipped: SOUL.md missing"
        check "$prof has no hardcoded /Users/bot/.hermes/bin/cody-check" \
            "false" "skipped: SOUL.md missing"
    fi
done

echo ""
echo "--- cody-check resolvability ---"
check "cody-check path is set" "[ -n \"$CODY_CHECK\" ]"
check "cody-check binary present" "[ -x \"$CODY_CHECK\" ]" \
    "expected: $CODY_CHECK (binary provided by Hermes runtime)"

echo ""
if [ "$FAIL" -eq 0 ]; then
    printf "RESULT: PASS (%d checks OK)\n" "$PASS"
    printf "Hermes/Cody distribution is verifiable. install.sh is DEFERRED per F-015.\n"
    exit 0
else
    printf "RESULT: FAIL (%d pass, %d fail)\n" "$PASS" "$FAIL"
    printf "Some prerequisites are missing. See hints above. install.sh is DEFERRED per F-015.\n"
    exit 1
fi
