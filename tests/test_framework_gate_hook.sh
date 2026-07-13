#!/usr/bin/env bash
# test-framework-gate-hook.sh
# Tests for scripts/hooks/pre-commit-framework-gate (4 cases from Run 4 brief).
# Usage: bash tests/test_framework_gate_hook.sh

set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PRE_COMMIT_HOOK="$REPO_ROOT/scripts/hooks/pre-commit-framework-gate"
COMMIT_MSG_HOOK="$REPO_ROOT/scripts/hooks/commit-msg-framework-gate"
TEST_TMP=$(mktemp -d -t vbb-gate-test-XXXXXX)
trap 'rm -rf "$TEST_TMP"' EXIT

pass=0
fail=0

# Helper: invoke the hook in a fake git environment with given staged files + message
invoke_hook() {
    local label="$1"
    local staged="$2"      # newline-separated list
    local msg="$3"         # commit message

    local fake_git="$TEST_TMP/fake_$label"
    mkdir -p "$fake_git"
    cd "$fake_git"
    git init -q .

    # Create a fake "framework file" matching the gate's prefix list
    local f
    for f in $staged; do
        mkdir -p "$(dirname "$f")"
        echo "x" > "$f"
        git add "$f"
    done

    # Write the commit message to COMMIT_EDITMSG
    printf '%s\n' "$msg" > "$(git rev-parse --git-dir)/COMMIT_EDITMSG"

    # Run the two local framework-gate hooks in Git order.
    "$PRE_COMMIT_HOOK" >/dev/null 2>&1 || return $?
    "$COMMIT_MSG_HOOK" "$(git rev-parse --git-dir)/COMMIT_EDITMSG" >/dev/null 2>&1
    echo $?
}

# Test 1 — WIP commit (prefix wip:) → exit 0
rc=$(invoke_hook "wip" "tools/x.py" "wip: experimental change to test the gate bypass")
if [ "$rc" = "0" ]; then
    echo "  PASS test_1_wip_commit"
    pass=$((pass+1))
else
    echo "  FAIL test_1_wip_commit: expected 0, got $rc"
    fail=$((fail+1))
fi

# Test 2 — declarative commit (fix:) without table/approve → exit 1
rc=$(invoke_hook "no_table" "tools/x.py" "fix(tools): add new tool without evidence table")
if [ "$rc" = "1" ]; then
    echo "  PASS test_2_no_table_blocks"
    pass=$((pass+1))
else
    echo "  FAIL test_2_no_table_blocks: expected 1, got $rc"
    fail=$((fail+1))
fi

# Test 3 — declarative commit WITH evidence table → exit 0
rc=$(invoke_hook "with_table" "tools/x.py" "fix(tools): add new tool
| Claim | Evidence | Status |
|---|---|---|
| tool works | manual test | VERIFIED_FINDING |")
if [ "$rc" = "0" ]; then
    echo "  PASS test_3_with_table_passes"
    pass=$((pass+1))
else
    echo "  FAIL test_3_with_table_passes: expected 0, got $rc"
    fail=$((fail+1))
fi

# Test 4 — declarative commit WITH approve: brice → exit 0
rc=$(invoke_hook "approve" "tools/x.py" "fix(tools): add new tool
approve: brice")
if [ "$rc" = "0" ]; then
    echo "  PASS test_4_approve_brice_passes"
    pass=$((pass+1))
else
    echo "  FAIL test_4_approve_brice_passes: expected 0, got $rc"
    fail=$((fail+1))
fi

# Bonus Test 5 — out-of-repo file (no docs/skills/etc.) → exit 0
rc=$(invoke_hook "out_of_repo" "README.md" "fix(docs): unrelated change")
if [ "$rc" = "0" ]; then
    echo "  PASS test_5_out_of_repo_passes (bonus)"
    pass=$((pass+1))
else
    echo "  FAIL test_5_out_of_repo_passes (bonus): expected 0, got $rc"
    fail=$((fail+1))
fi

# Bonus Test 6 — chore: prefix → exit 0
rc=$(invoke_hook "chore" "tools/x.py" "chore: update something")
if [ "$rc" = "0" ]; then
    echo "  PASS test_6_chore_prefix_passes (bonus)"
    pass=$((pass+1))
else
    echo "  FAIL test_6_chore_prefix_passes (bonus): expected 0, got $rc"
    fail=$((fail+1))
fi

# Bonus Test 7 — feat: prefix WITHOUT table → exit 1
rc=$(invoke_hook "feat_no_table" "tools/x.py" "feat(tools): shiny new feature")
if [ "$rc" = "1" ]; then
    echo "  PASS test_7_feat_no_table_blocks (bonus)"
    pass=$((pass+1))
else
    echo "  FAIL test_7_feat_no_table_blocks (bonus): expected 1, got $rc"
    fail=$((fail+1))
fi

# Test 8 (ADR 0013 Phase 3 prep, R1) — distributions/* is in the whitelist.
# Use an active Pi distribution path with a WIP commit →
# pre-commit-hook should detect it as in_repo (in-scope), not block.
# We use a wip: prefix so commit-msg-hook lets it through.
rc=$(invoke_hook "distrib_wip" "distributions/pi/README.md" "wip: verify distributions whitelist")
if [ "$rc" = "0" ]; then
    echo "  PASS test_8_distributions_in_whitelist (ADR 0013 R1)"
    pass=$((pass+1))
else
    echo "  FAIL test_8_distributions_in_whitelist (ADR 0013 R1): expected 0, got $rc"
    fail=$((fail+1))
fi

# Test 9 — an active OpenCode distribution file
# in-scope + declarative commit WITH table → exit 0
rc=$(invoke_hook "distrib_table" "distributions/opencode/setup.sh" "feat(distributions): update provider adapter
| Claim | Evidence | Status |
|---|---|---|
| hook whitelist updated | diff shows distributions/* added | DONE |
| in-scope detection works | test 8 PASS | DONE |")
if [ "$rc" = "0" ]; then
    echo "  PASS test_9_distributions_with_table (ADR 0013 R1)"
    pass=$((pass+1))
else
    echo "  FAIL test_9_distributions_with_table (ADR 0013 R1): expected 0, got $rc"
    fail=$((fail+1))
fi

# Test 10 (ADR 0013 Phase 3 prep, R1) — path truly out of scope still
# passes silently (exit 0, classified as out-of-repo). This proves
# the protection is NOT weakened for legit out-of-scope paths.
rc=$(invoke_hook "still_out_of_scope" "somewhere_else/foo.md" "wip: trivial out-of-scope change")
if [ "$rc" = "0" ]; then
    echo "  PASS test_10_out_of_scope_still_silent (ADR 0013 R1)"
    pass=$((pass+1))
else
    echo "  FAIL test_10_out_of_scope_still_silent (ADR 0013 R1): expected 0, got $rc"
    fail=$((fail+1))
fi

echo ""
echo "Results: $pass passed, $fail failed"
exit $fail
