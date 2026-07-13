#!/usr/bin/env bash
# install-framework-gate-hook.sh — DÉPRÉCIÉ (ADR-0027, TD-102).
#
# Ce script installait pre-commit-framework-gate sous un nom que Git
# n'exécute pas par défaut (.git/hooks/pre-commit-framework-gate), donnant
# un faux sentiment de couverture. L'installateur canonique compose les
# deux hooks testés dans .git/hooks/pre-commit et .git/hooks/commit-msg.
#
# Redirige vers : scripts/install-vbb-hooks.sh

set -euo pipefail

echo "[DEPRECATED] install-framework-gate-hook.sh → install-vbb-hooks.sh" >&2
echo "[DEPRECATED] L'installateur canonique compose framework gate + loop closure." >&2

exec bash "$(dirname "$0")/install-vbb-hooks.sh"
