#!/usr/bin/env bash
# install-vbb-pre-commit.sh
# Installs a VBB pre-commit hook that verifies the loop-closure invariant
# before any commit touching docs/runs/.
#
# Usage:
#   bash scripts/install-vbb-pre-commit.sh
#
# The hook fires only when at least one file under docs/runs/{slug}/ is staged.
# It extracts the run_id from the staged path and calls vbb-loop-closure-check.py.
# If the check fails, the commit is blocked with an actionable error message.

set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
HOOK_PATH="$REPO_ROOT/.git/hooks/pre-commit"

cat > "$HOOK_PATH" << 'HOOK_BODY'
#!/usr/bin/env bash
# VBB pre-commit hook — loop closure check
# Auto-installed by scripts/install-vbb-pre-commit.sh

REPO_ROOT="$(git rev-parse --show-toplevel)"
STAGED="$(git diff --cached --name-only)"

# Only fire when a docs/runs/{slug}/ file is staged
if ! echo "$STAGED" | grep -q "^docs/runs/[^/]*/"; then
    exit 0
fi

# Extract run_id (slug) from the first matching staged path
RUN_ID="$(echo "$STAGED" | grep "^docs/runs/[^/]*/" | head -1 | cut -d/ -f3)"

if [ -z "$RUN_ID" ]; then
    exit 0
fi

echo "[vbb] Checking loop closure for run: $RUN_ID"

if ! python3 "$REPO_ROOT/tools/vbb-loop-closure-check.py" "$RUN_ID"; then
    echo ""
    echo "[vbb] BLOCKED: loop-closure-check failed for run '$RUN_ID'."
    echo "[vbb] Resolve the missing or invalid artifacts, then retry the commit."
    echo "[vbb] To bypass (not recommended): git commit --no-verify"
    exit 1
fi
HOOK_BODY

chmod +x "$HOOK_PATH"
echo "✓ VBB pre-commit hook installed at: $HOOK_PATH"
