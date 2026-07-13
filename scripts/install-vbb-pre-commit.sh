#!/usr/bin/env bash
# install-vbb-pre-commit.sh — DÉPRÉCIÉ (ADR-0027, TD-102).
#
# Ce script écrasait .git/hooks/pre-commit avec la seule vérification
# loop-closure, perdant le framework gate. L'installateur canonique
# compose les deux hooks testés.
#
# Redirige vers : scripts/install-vbb-hooks.sh

set -euo pipefail

echo "[DEPRECATED] install-vbb-pre-commit.sh → install-vbb-hooks.sh" >&2
echo "[DEPRECATED] L'installateur canonique compose framework gate + loop closure." >&2

exec bash "$(dirname "$0")/install-vbb-hooks.sh"
