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

if { [ -n "${VBB_RUN_ID:-}" ] && [ -z "${VBB_EXPECTED_COMMIT:-}" ]; } ||
  { [ -z "${VBB_RUN_ID:-}" ] && [ -n "${VBB_EXPECTED_COMMIT:-}" ]; }; then
  echo "VBB_RUN_ID and VBB_EXPECTED_COMMIT must be declared together."
  echo "Exact release evidence is fail-closed when either subject field is absent."
  exit 1
fi

echo "[1/16] Contract lint"
run_check "Lint 0 errors" "$PYTHON" tools/vbb-contract-lint.py

echo ""
echo "[2/16] Architecture lint"
run_check "Architecture valid" "$PYTHON" tools/vbb-architecture.py lint

echo ""
echo "[3/16] Contract runtime dry-run"
run_check "Runtime dry-run" "$PYTHON" tools/vbb-contract-runtime.py run --all --dry-run

echo ""
echo "[4/16] Runtime conformance self-test"
run_check "Runtime conformance" "$PYTHON" tools/vbb_runtime_conformance.py self-test

echo ""
echo "[5/16] Hook installer regression"
run_check "Hook installer" bash tests/test_install_vbb_hooks.sh

echo ""
echo "[6/16] Credentials gate (staged additions)"
run_check "Credentials clean" "$PYTHON" tools/vbb-credentials-gate.py --staged

echo ""
echo "[7/16] Ruff check"
run_check "Ruff check" "$PYTHON" -m ruff check tools tests

echo ""
echo "[8/16] Ruff format check"
run_check "Ruff format check" "$PYTHON" -m ruff format --check tools tests

echo ""
echo "[9/16] Mypy"
run_check "Mypy" "$PYTHON" -m mypy tools

echo ""
echo "[10/16] Adversarial gate (explicit run)"
# An implicit latest run is diagnostic convenience, never release evidence.
# VBB_EXPECTED_COMMIT activates exact run+SHA binding for release verification.
if [ -n "${VBB_RUN_ID:-}" ]; then
  run_check "Adversarial gate" "$PYTHON" tools/vbb-adversarial-gate.py \
    "$VBB_RUN_ID" --expected-commit "$VBB_EXPECTED_COMMIT" --strict
else
  echo "  Adversarial gate ... ⏭️  SKIP (VBB_RUN_ID not declared)"
fi

echo ""
echo "[11/16] Adversarial corpus"
# Pre-merge gate 5b, second half. Reported separately from the main suite.
run_check "Adversarial corpus" "$PYTHON" -m pytest tests/adversarial_corpus/ -q

echo ""
echo "[12/16] Loop closure (explicit run)"
if [ -n "${VBB_RUN_ID:-}" ]; then
  run_check "Closure check" "$PYTHON" tools/vbb-loop-closure-check.py \
    "$VBB_RUN_ID" --expected-commit "$VBB_EXPECTED_COMMIT" --strict
else
  echo "  Closure check ... ⏭️  SKIP (VBB_RUN_ID not declared)"
fi

echo ""
echo "[13/16] Loop closure tests"
run_check "test_loop_closure.py" "$PYTHON" tests/test_loop_closure.py

echo ""
echo "[14/16] Portability tests"
run_check "test_portability.py" "$PYTHON" tests/test_portability.py

echo ""
echo "[15/16] Project init tests"
run_check "test_project_init.py" "$PYTHON" tests/test_project_init.py

echo ""
echo "[16/16] Pytest suite"
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
