#!/usr/bin/env bash
# install-vbb-hooks.sh — installateur CANONIQUE des hooks locaux VBB (ADR-0027, TD-102).
#
# Compose les deux comportements déjà testés en une installation unique :
#   .git/hooks/pre-commit  : 1) framework gate (scripts/hooks/pre-commit-framework-gate,
#                               testé par tests/test_framework_gate_hook.sh)
#                            2) loop-closure check sur les runs stagés
#                               (comportement de l'ancien install-vbb-pre-commit.sh)
#   .git/hooks/commit-msg  : framework gate commit-msg
#                               (scripts/hooks/commit-msg-framework-gate)
#
# Les hooks installés DÉLÈGUENT aux scripts versionnés dans scripts/hooks/ :
# une mise à jour du dépôt met à jour le comportement sans réinstallation.
#
# Remplace (dépréciés, redirigent ici) :
#   scripts/install-framework-gate-hook.sh
#   scripts/install-vbb-pre-commit.sh
#
# Usage:
#   bash scripts/install-vbb-hooks.sh

set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
FRAMEWORK_PRE_COMMIT="$REPO_ROOT/scripts/hooks/pre-commit-framework-gate"
FRAMEWORK_COMMIT_MSG="$REPO_ROOT/scripts/hooks/commit-msg-framework-gate"
CREDENTIALS_GATE="$REPO_ROOT/tools/vbb-credentials-gate.py"

for src in "$FRAMEWORK_PRE_COMMIT" "$FRAMEWORK_COMMIT_MSG" "$CREDENTIALS_GATE"; do
    if [ ! -f "$src" ]; then
        echo "ERROR: hook source not found: $src" >&2
        exit 1
    fi
done

mkdir -p "$HOOKS_DIR"

# --- pre-commit : framework gate PUIS loop-closure -------------------------
cat > "$HOOKS_DIR/pre-commit" << 'HOOK_BODY'
#!/usr/bin/env bash
# VBB canonical pre-commit hook — installed by scripts/install-vbb-hooks.sh
# Stage 1: framework gate | Stage 2: loop-closure check (staged docs/runs/)

REPO_ROOT="$(git rev-parse --show-toplevel)"

# Resolve an interpreter that can execute the versioned VBB tooling. Provider
# shells may expose different environments as `python` and `python3`.
PYTHON_BIN="${PYTHON_OVERRIDE:-}"
if [ -z "$PYTHON_BIN" ]; then
    for candidate in python python3; do
        if command -v "$candidate" >/dev/null 2>&1 && \
                "$candidate" -c 'import yaml' >/dev/null 2>&1; then
            PYTHON_BIN="$candidate"
            break
        fi
    done
fi
if [ -z "$PYTHON_BIN" ]; then
    echo "[vbb] BLOCKED: no Python interpreter with PyYAML is available." >&2
    echo "[vbb] Install project dependencies or set PYTHON_OVERRIDE." >&2
    exit 1
fi

# Stage 1 — framework gate (versioned, tested)
if ! bash "$REPO_ROOT/scripts/hooks/pre-commit-framework-gate"; then
    exit 1
fi

# Stage 2 — loop-closure check, fires only when docs/runs/{slug}/ is staged
STAGED="$(git diff --cached --name-only)"
if echo "$STAGED" | grep -q "^docs/runs/[^/]*/"; then
    RUN_ID="$(echo "$STAGED" | grep "^docs/runs/[^/]*/" | head -1 | cut -d/ -f3)"
    if [ -n "$RUN_ID" ]; then
        echo "[vbb] Checking loop closure for run: $RUN_ID"
        if ! "$PYTHON_BIN" "$REPO_ROOT/tools/vbb-loop-closure-check.py" "$RUN_ID"; then
            echo ""
            echo "[vbb] BLOCKED: loop-closure-check failed for run '$RUN_ID'."
            echo "[vbb] Resolve the missing or invalid artifacts, then retry."
            echo "[vbb] To bypass (not recommended): git commit --no-verify"
            exit 1
        fi
    fi
fi
HOOK_BODY
chmod +x "$HOOKS_DIR/pre-commit"

# --- commit-msg : framework gate --------------------------------------------
cat > "$HOOKS_DIR/commit-msg" << 'HOOK_BODY'
#!/usr/bin/env bash
# VBB canonical commit-msg hook — installed by scripts/install-vbb-hooks.sh
REPO_ROOT="$(git rev-parse --show-toplevel)"
exec bash "$REPO_ROOT/scripts/hooks/commit-msg-framework-gate" "$1"
HOOK_BODY
chmod +x "$HOOKS_DIR/commit-msg"

echo "✓ VBB canonical hooks installed:"
echo "    $HOOKS_DIR/pre-commit  (framework gate + loop closure)"
echo "    $HOOKS_DIR/commit-msg  (framework gate)"
echo "  Hooks delegate to scripts/hooks/ — repo updates apply without reinstall."
