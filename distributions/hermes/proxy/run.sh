#!/usr/bin/env bash
# Vibebackbone privacy proxy — daemon launcher (POC).
#
# Usage:
#   ./distributions/hermes/proxy/run.sh                  # uses default config path
#   VBB_PROXY_CONFIG=/path/to/config.yaml ./distributions/hermes/proxy/run.sh
#
# The script computes the repo root from its own location and adds it
# to PYTHONPATH so `python -m proxy.daemon` resolves (post-Phase 3
# migration: proxy now lives under distributions/hermes/proxy/).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export PYTHONPATH="${REPO_ROOT}/distributions/hermes${PYTHONPATH:+:${PYTHONPATH}}"
cd "${REPO_ROOT}"

exec python3 -m proxy.daemon "$@"
