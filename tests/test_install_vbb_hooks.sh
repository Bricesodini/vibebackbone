#!/usr/bin/env bash
# test_install_vbb_hooks.sh — tests de l'installateur canonique (ADR-0027, TD-102).
# Vérifie dans un repo git temporaire :
#   1. install-vbb-hooks.sh installe .git/hooks/pre-commit ET commit-msg, exécutables
#   2. le pre-commit composé contient les DEUX étages (framework gate + loop closure)
#   3. les deux anciens installateurs redirigent (message DEPRECATED) et produisent
#      la même installation canonique
# Usage: bash tests/test_install_vbb_hooks.sh

set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_TMP=$(mktemp -d -t vbb-hooks-test-XXXXXX)
trap 'rm -rf "$TEST_TMP"' EXIT

pass=0
fail=0

check() {
    local label="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "  ✓ $label"
        pass=$((pass + 1))
    else
        echo "  ✗ $label (expected: $expected, got: $actual)"
        fail=$((fail + 1))
    fi
}

make_fixture() {
    local dir="$1"
    mkdir -p "$dir/scripts/hooks" "$dir/tools"
    cp "$REPO_ROOT/scripts/install-vbb-hooks.sh" \
       "$REPO_ROOT/scripts/install-framework-gate-hook.sh" \
       "$REPO_ROOT/scripts/install-vbb-pre-commit.sh" "$dir/scripts/"
    cp "$REPO_ROOT/scripts/hooks/pre-commit-framework-gate" \
       "$REPO_ROOT/scripts/hooks/commit-msg-framework-gate" "$dir/scripts/hooks/"
    cp "$REPO_ROOT/tools/vbb-credentials-gate.py" "$dir/tools/"
    git -C "$dir" init -q
}

# --- Cas 1 : installateur canonique ------------------------------------------
FIX1="$TEST_TMP/canonical"
make_fixture "$FIX1"
out1="$(bash "$FIX1/scripts/install-vbb-hooks.sh" 2>&1)"; rc1=$?
check "canonical: exit 0" "0" "$rc1"
check "canonical: pre-commit installé + exécutable" "yes" \
    "$([ -x "$FIX1/.git/hooks/pre-commit" ] && echo yes || echo no)"
check "canonical: commit-msg installé + exécutable" "yes" \
    "$([ -x "$FIX1/.git/hooks/commit-msg" ] && echo yes || echo no)"
check "canonical: étage framework gate présent" "yes" \
    "$(grep -q "pre-commit-framework-gate" "$FIX1/.git/hooks/pre-commit" && echo yes || echo no)"
check "canonical: étage loop-closure présent" "yes" \
    "$(grep -q "vbb-loop-closure-check.py" "$FIX1/.git/hooks/pre-commit" && echo yes || echo no)"
check "canonical: interpréteur résolu par dépendance" "yes" \
    "$(grep -q "import yaml" "$FIX1/.git/hooks/pre-commit" && echo yes || echo no)"
check "canonical: aucun python3 hardcodé pour loop closure" "yes" \
    "$(! grep -q 'if ! python3 .*vbb-loop-closure-check.py' "$FIX1/.git/hooks/pre-commit" && echo yes || echo no)"

# --- Cas 2 : ancien installateur framework-gate → redirection -----------------
FIX2="$TEST_TMP/deprecated_framework"
make_fixture "$FIX2"
out2="$(bash "$FIX2/scripts/install-framework-gate-hook.sh" 2>&1)"; rc2=$?
check "deprecated framework-gate: exit 0" "0" "$rc2"
check "deprecated framework-gate: message DEPRECATED" "yes" \
    "$(echo "$out2" | grep -q "DEPRECATED" && echo yes || echo no)"
check "deprecated framework-gate: installation canonique produite" "yes" \
    "$(grep -q "vbb-loop-closure-check.py" "$FIX2/.git/hooks/pre-commit" && echo yes || echo no)"

# --- Cas 3 : ancien installateur vbb-pre-commit → redirection ------------------
FIX3="$TEST_TMP/deprecated_precommit"
make_fixture "$FIX3"
out3="$(bash "$FIX3/scripts/install-vbb-pre-commit.sh" 2>&1)"; rc3=$?
check "deprecated vbb-pre-commit: exit 0" "0" "$rc3"
check "deprecated vbb-pre-commit: message DEPRECATED" "yes" \
    "$(echo "$out3" | grep -q "DEPRECATED" && echo yes || echo no)"
check "deprecated vbb-pre-commit: étage framework gate non perdu" "yes" \
    "$(grep -q "pre-commit-framework-gate" "$FIX3/.git/hooks/pre-commit" && echo yes || echo no)"

# --- Cas 4 : dépendance credentials absente → fail closed --------------------
FIX4="$TEST_TMP/missing_credentials_gate"
make_fixture "$FIX4"
rm "$FIX4/tools/vbb-credentials-gate.py"
out4="$(bash "$FIX4/scripts/install-vbb-hooks.sh" 2>&1)"; rc4=$?
check "missing credentials gate: exit 1" "1" "$rc4"
check "missing credentials gate: erreur explicite" "yes" \
    "$(echo "$out4" | grep -q "vbb-credentials-gate.py" && echo yes || echo no)"

echo ""
echo "RESULT: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
