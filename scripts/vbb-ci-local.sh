#!/usr/bin/env bash
# vbb-ci-local.sh — Local CI for vibebackbone
# Runs the same checks as the GitHub Actions workflow.
# Portable: macOS + Linux. Works from any subdirectory.

set -euo pipefail

# ── Resolve repo root ──────────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="python3"
PASS=0
FAIL=0
WARN=0

# ── Helpers ─────────────────────────────────────────────────────────
run_check() {
  local label="$1"
  shift
  echo -n "  $label ... "
  local out
  if out=$("$@" 2>&1); then
    echo "✅ PASS"
    PASS=$((PASS + 1))
  else
    echo "❌ FAIL"
    echo "$out" | sed 's/^/    /'
    FAIL=$((FAIL + 1))
  fi
}

run_check_warn() {
  local label="$1"
  shift
  echo -n "  $label ... "
  local out
  if out=$("$@" 2>&1); then
    echo "✅ PASS"
    PASS=$((PASS + 1))
  else
    echo "⚠️  WARN (non-blocking)"
    echo "$out" | sed 's/^/    /'
    WARN=$((WARN + 1))
  fi
}

# ── Checks ─────────────────────────────────────────────────────────

echo "=== VBB Local CI ==="
echo ""

echo "[1/6] Contract lint"
run_check "Lint 0 errors" "$PYTHON" tools/vbb-contract-lint.py

echo ""
echo "[2/6] Contract runtime dry-run"
run_check "Runtime dry-run" "$PYTHON" tools/vbb-contract-runtime.py run --all --dry-run

echo ""
echo "[3/6] Loop closure (latest run)"
# WARN is acceptable if the latest run has unknown voie (ad-hoc session)
run_check_warn "Closure check" "$PYTHON" tools/vbb-loop-closure-check.py

echo ""
echo "[4/7] Loop closure tests"
run_check "test_loop_closure.py" "$PYTHON" tests/test_loop_closure.py

echo ""
echo "[5/7] Portability tests"
run_check "test_portability.py" "$PYTHON" tests/test_portability.py

echo ""
echo "[6/7] Project init tests"
run_check "test_project_init.py" "$PYTHON" tests/test_project_init.py

echo ""
echo "[7/7] Pytest suite"
run_check "pytest tests/" "$PYTHON" -m pytest tests/ -q

# ── Summary ─────────────────────────────────────────────────────────

echo ""
TOTAL=$((PASS + FAIL + WARN))
echo "=== Results: ${PASS} passed, ${FAIL} failed, ${WARN} warnings ==="

if [ "$FAIL" -gt 0 ]; then
  echo "❌ CI FAILED"
  exit 1
else
  echo "✅ CI PASSED"
  exit 0
fi