#!/usr/bin/env bash
# install-framework-gate-hook.sh
# Installe le hook pre-commit-framework-gate vers .git/hooks/.
#
# Note : le hook porte un nom distinctif (pre-commit-framework-gate) pour
# ne pas écraser le hook pre-commit existant installé par
# scripts/install-vbb-pre-commit.sh (qui fait le loop-closure check).
# Pour activer les DEUX hooks, configure core.hooksPath vers un dossier
# contenant les deux (ex: scripts/hooks/ + un symlink vers le loop-closure
# hook), OU chaîne-les manuellement dans un pre-commit unique.
#
# Usage:
#   bash scripts/install-framework-gate-hook.sh

set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
HOOK_SRC="$REPO_ROOT/scripts/hooks/pre-commit-framework-gate"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit-framework-gate"

if [ ! -f "$HOOK_SRC" ]; then
    echo "ERROR: hook source not found: $HOOK_SRC" >&2
    exit 1
fi

cp "$HOOK_SRC" "$HOOK_DST"
chmod +x "$HOOK_DST"

COMMIT_MSG_SRC="$REPO_ROOT/scripts/hooks/commit-msg-framework-gate"
COMMIT_MSG_DST="$REPO_ROOT/.git/hooks/commit-msg"

if [ -f "$COMMIT_MSG_SRC" ]; then
    cp "$COMMIT_MSG_SRC" "$COMMIT_MSG_DST"
    chmod +x "$COMMIT_MSG_DST"
    echo "✓ Commit-msg hook installed at: $COMMIT_MSG_DST"
fi

echo "✓ Framework gate hook installed at: $HOOK_DST"
echo "  Source: $HOOK_SRC"
echo "  Note: this hook is named 'pre-commit-framework-gate' to coexist with"
echo "  the existing 'pre-commit' loop-closure hook. Activate via:"
echo "    git config core.hooksPath scripts/hooks/"
echo "  (then symlink or copy the loop-closure hook into scripts/hooks/pre-commit)"
