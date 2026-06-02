#!/usr/bin/env bash
# Vibebackbone privacy proxy — daemon launcher (POC).
#
# Usage:
#   ./tools/proxy/run.sh                  # uses default config path
#   VBB_PROXY_CONFIG=/path/to/config.yaml ./tools/proxy/run.sh
#
# The script computes the repo root from its own location and adds it
# to PYTHONPATH so `python -m tools.proxy.daemon` resolves.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export PYTHONPATH="${REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
cd "${REPO_ROOT}"

exec python3 -m tools.proxy.daemon "$@"
