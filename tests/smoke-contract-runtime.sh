#!/bin/bash
# VBB Contract Runtime — Smoke Tests
# Phase 3.1 Runtime Stabilization

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="python3"
LINTER="$PYTHON tools/vbb-contract-lint.py"
RUNTIME="$PYTHON tools/vbb-contract-runtime.py"

PASS=0
FAIL=0

assert() {
    local label="$1"
    local cmd="$2"
    echo -n "  $label ... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo "PASS"
        PASS=$((PASS+1))
    else
        echo "FAIL"
        FAIL=$((FAIL+1))
    fi
}

echo "=== VBB Runtime Smoke Tests ==="
echo ""

echo "[Linter]"
assert "linter exits 0" "$LINTER"
assert "linter finds 0 errors" "$LINTER 2>&1 | grep -q '0 error'"

echo ""
echo "[Router]"
assert "router --list works" "$PYTHON tools/vbb-phase-router.py --list | grep -q '0-vbb-scope-freeze'"
assert "router route 'scope freeze'" "$PYTHON tools/vbb-phase-router.py 'scope freeze' | grep -q '0-vbb-scope-freeze'"
assert "router route 'mode transition'" "$PYTHON tools/vbb-phase-router.py 'mode transition' | grep -q 't-vbb-mode-transition-gate'"

echo ""
echo "[Runtime validate]"
assert "validate passes" "$RUNTIME validate"

echo ""
echo "[Runtime execute]"
result=$($RUNTIME run 0-vbb-scope-freeze 2>&1)
assert "runtime executes without crash" "echo \"\$result\" | grep -q 'contract_id'"
assert "status field present" "echo \"\$result\" | grep -q 'status'"
assert "trace written" "test -f docs/audits/vbb-runtime/0-vbb-scope-freeze_latest.json"

echo ""
echo "[Runtime modes]"
assert "runtime with --dry-run" "$RUNTIME run 0-vbb-scope-freeze --dry-run | $PYTHON -c 'import json,sys; d=json.load(sys.stdin); assert d.get(\"dry_run\")==True'"

echo ""
echo "[Router integration]"
assert "runtime --query route" "$RUNTIME run 0-vbb-scope-freeze --query 'scope freeze' | grep -q 'Routed:'"

echo ""
echo "[Traces]"
assert "trace is valid JSON" "$PYTHON -c 'import json; json.load(open(\"docs/audits/vbb-runtime/0-vbb-scope-freeze_latest.json\"))'"
assert "trace has required fields" "$PYTHON -c 'import json; d=json.load(open(\"docs/audits/vbb-runtime/0-vbb-scope-freeze_latest.json\")); assert all(k in d for k in [\"contract_id\",\"status\",\"gates\",\"outputs\"])'"
assert "trace events declared" "$PYTHON -c 'import json; d=json.load(open(\"docs/audits/vbb-runtime/0-vbb-scope-freeze_latest.json\")); assert d[\"events\"][\"declared\"] == True'"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="

if [ $FAIL -gt 0 ]; then
    exit 1
fi
echo "SMOKE TESTS: PASS"