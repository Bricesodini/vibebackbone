#!/usr/bin/env bash
# Vibebackbone privacy proxy — daemon launcher (POC).
#
# Usage:
#   ./distributions/hermes/proxy/run.sh                  # uses default config path
#   VBB_PROXY_CONFIG=/path/to/config.yaml ./distributions/hermes/proxy/run.sh
#
# The script computes the repo root from its own location and adds the
# `distributions/hermes/` directory to PYTHONPATH so `python -m proxy.daemon`
# resolves. Post-Phase 3 migration: proxy now lives at
# `distributions/hermes/proxy/`, so REPO_ROOT is 3 levels up
# (`distributions/hermes/proxy/` → `distributions/hermes/` → `distributions/`
# → repo root). The `proxy` package itself sits under
# `distributions/hermes/proxy/`, so PYTHONPATH must point at
# `distributions/hermes/` for `import proxy.daemon` to succeed.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
export PYTHONPATH="${REPO_ROOT}/distributions/hermes${PYTHONPATH:+:${PYTHONPATH}}"
cd "${REPO_ROOT}"

exec python3 -m proxy.daemon "$@"
