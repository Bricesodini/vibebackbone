#!/usr/bin/env bash
# vbb-ci-local.sh — Local CI for vibebackbone
# Runs the same checks as the GitHub Actions workflow.
# Portable: macOS + Linux. Works from any subdirectory.

set -euo pipefail

# ── Resolve repo root ──────────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [ -z "${PYTHON:-}" ]; then
  if command -v python >/dev/null 2>&1; then
    PYTHON="python"
  else
    PYTHON="python3"
  fi
fi
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

require_python_modules() {
  local missing
  missing=$("$PYTHON" - <<'PY'
import importlib.util
mods = {
    "yaml": "pyyaml",
    "pytest": "pytest",
    "ruff": "ruff",
    "mypy": "mypy",
}
missing = [pkg for mod, pkg in mods.items() if importlib.util.find_spec(mod) is None]
print(" ".join(missing))
PY
)
  if [ -n "$missing" ]; then
    echo "Missing Python dependencies: $missing"
    echo "Run: $PYTHON -m pip install -r requirements-dev.txt"
    exit 1
  fi
}

# ── Checks ─────────────────────────────────────────────────────────

echo "=== VBB Local CI ==="
echo ""

require_python_modules

echo "[1/12] Contract lint"
run_check "Lint 0 errors" "$PYTHON" tools/vbb-contract-lint.py

echo ""
echo "[2/12] Architecture lint"
run_check "Architecture valid" "$PYTHON" tools/vbb-architecture.py lint

echo ""
echo "[3/12] Contract runtime dry-run"
run_check "Runtime dry-run" "$PYTHON" tools/vbb-contract-runtime.py run --all --dry-run

echo ""
echo "[4/12] Credentials gate (staged additions)"
run_check "Credentials clean" "$PYTHON" tools/vbb-credentials-gate.py --staged

echo ""
echo "[5/12] Ruff check"
run_check "Ruff check" "$PYTHON" -m ruff check tools tests

echo ""
echo "[6/12] Ruff format check"
run_check "Ruff format check" "$PYTHON" -m ruff format --check tools tests

echo ""
echo "[7/12] Mypy"
run_check "Mypy" "$PYTHON" -m mypy tools

echo ""
echo "[8/12] Loop closure (latest run)"
# WARN is acceptable if the latest run has unknown voie (ad-hoc session)
run_check_warn "Closure check" "$PYTHON" tools/vbb-loop-closure-check.py

echo ""
echo "[9/12] Loop closure tests"
run_check "test_loop_closure.py" "$PYTHON" tests/test_loop_closure.py

echo ""
echo "[10/12] Portability tests"
run_check "test_portability.py" "$PYTHON" tests/test_portability.py

echo ""
echo "[11/12] Project init tests"
run_check "test_project_init.py" "$PYTHON" tests/test_project_init.py

echo ""
echo "[12/12] Pytest suite"
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
