#!/bin/bash
# distributions/hermes/setup.sh — Hermes/Cody distribution setup.
#
# This file is sourced by the root setup.sh routeur. It is the
# SIXTH (and last) distribution in the VBB installer (Hermes/Cody).
#
# CONTRACT (Phase 2F — NON-DESTRUCTIVE):
#   - No writes to ~/.hermes/
#   - No profile installation
#   - No secrets creation
#   - No proxy mutation
#   - No SOUL.md modification
#   - No CI / no install.sh destructive script
#
# What it DOES do:
#   1. Verify essential Hermes files are present in the repo
#   2. Print the locations of the key components (verify, proxy client,
#      proxy CLI, example configs, AGENT_INSTALL.md)
#   3. Run distributions/hermes/verify/verify.sh if --check is passed
#   4. Exit 0 if all essential files are present
#   5. Exit 1 if any essential file is missing
#
# Hermes/Cody installation is **agent-mediated**, NOT automatic.
# See distributions/hermes/AGENT_INSTALL.md for the full operator
# procedure (backups, profile copy, proxy wiring, permissions).
#
# Globals expected from the caller (setup.sh):
#   REPO_ROOT, HOME
#
# Globals set here (consumed by setup.sh summary):
#   HERMES_STATUS (ok|missing)
#   HERMES_PROXY_PRESENT (true|false)

# ── Hermes entry point ──────────────────────────────────────────────────────
hermes_install() {
  hermes_preflight
  hermes_print_components
  hermes_run_verify_if_requested
}

# 1. Pre-flight: check essential files are present
hermes_preflight() {
  local missing=0

  for f in \
      "$REPO_ROOT/distributions/hermes/verify/verify.sh" \
      "$REPO_ROOT/distributions/hermes/proxy/client.py" \
      "$REPO_ROOT/distributions/hermes/proxy/cli.py" \
      "$REPO_ROOT/distributions/hermes/proxy/config.example.yaml" \
      "$REPO_ROOT/distributions/hermes/proxy/actions.example.yaml" \
      "$REPO_ROOT/distributions/hermes/AGENT_INSTALL.md"
  do
    if [ ! -f "$f" ]; then
      echo "  ✗ missing: $f"
      missing=$((missing + 1))
    fi
  done

  if [ "$missing" -gt 0 ]; then
    HERMES_STATUS="missing"
  else
    HERMES_STATUS="ok"
  fi

  # Detect proxy runtime presence (informational only, never required)
  if [ -d "$REPO_ROOT/distributions/hermes/proxy/tests" ] || \
     [ -d "$REPO_ROOT/distributions/hermes/proxy/__pycache__" ]; then
    HERMES_PROXY_PRESENT="true"
  else
    HERMES_PROXY_PRESENT="false"
  fi
}

# 2. Print the location of useful components (no side effects)
hermes_print_components() {
  if [ "$HERMES_STATUS" = "missing" ]; then
    echo "  ⚠ Hermes: some essential files missing (see above) — see distributions/hermes/AGENT_INSTALL.md"
    return 0
  fi

  echo "  Hermes components (this repo):"
  echo "    verify              : distributions/hermes/verify/verify.sh"
  echo "    proxy client (lib)  : distributions/hermes/proxy/client.py"
  echo "    proxy cli           : distributions/hermes/proxy/cli.py"
  echo "    proxy config (ex.)  : distributions/hermes/proxy/config.example.yaml"
  echo "    proxy actions (ex.) : distributions/hermes/proxy/actions.example.yaml"
  echo "    agent install guide : distributions/hermes/AGENT_INSTALL.md"
  if [ "$HERMES_PROXY_PRESENT" = "true" ]; then
    echo "    proxy runtime       : present (stdlib + tests in distributions/hermes/proxy/)"
  fi
  echo ""
  echo "  Hermes is AGENT-INSTALL ONLY — bash setup.sh does NOT install"
  echo "  ~/.hermes/ profiles, secrets, or proxy runtime. Read"
  echo "  distributions/hermes/AGENT_INSTALL.md before any operator action."
}

# 3. Optionally run verify.sh in non-destructive check mode
hermes_run_verify_if_requested() {
  # Only run if --hermes-verify flag was passed to setup.sh
  if [ "${HERMES_VERIFY:-false}" != "true" ]; then
    return 0
  fi
  if [ "$HERMES_STATUS" = "missing" ]; then
    echo "  ⚠ Hermes verify skipped: essential files missing"
    return 0
  fi
  echo ""
  echo "  Running distributions/hermes/verify/verify.sh (non-destructive check)..."
  if bash "$REPO_ROOT/distributions/hermes/verify/verify.sh"; then
    echo "  ✓ Hermes verify: PASS"
  else
    echo "  ✗ Hermes verify: FAIL — see output above"
  fi
}
