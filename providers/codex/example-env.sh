#!/bin/bash
# example-env.sh — Codex environment variables template
# Copy to .codex/env.sh and update with your credentials

# Required: Codex API credentials
export CODEX_API_KEY="sk-..."  # Your Codex API key
export CODEX_ENDPOINT="https://api.codex.dev/v1"  # Codex API endpoint

# Optional: Default configuration
export CODEX_MODEL="claude-opus-4.7"  # Default model for agents
export CODEX_TIMEOUT="3600"  # Timeout in seconds (default: 1 hour)
export CODEX_TEMPERATURE="0.7"  # Sampling temperature

# vibebackbone configuration
export VBB_PROVIDER="codex"  # Provider identifier (auto-detected)
export VBB_MODE="CONSUMER"  # Mode: CONSUMER or DISTRIBUTION
export VBB_GOVERNANCE="v1.0"  # Governance version

# Session configuration
export VBB_SESSION_FILE="docs/SESSION.md"  # Session memory file
export VBB_AUDIT_DASHBOARD="docs/AUDIT_STATUS.md"  # Audit dashboard
export VBB_AUDIT_REPORTS_DIR="docs/audits/"  # Audit reports directory

# Risk management
export VBB_RISK_P0_ACTION="BLOCK_DEPLOYMENT"  # P0 risk action
export VBB_RISK_P1_ACTION="ESCALATE"  # P1 risk action
export VBB_RISK_P2_ACTION="DOCUMENT"  # P2 risk action
export VBB_RISK_P3_ACTION="MONITOR"  # P3 risk action

echo "✓ Codex environment configured"
echo "  API Key: ${CODEX_API_KEY:0:10}..."
echo "  Endpoint: $CODEX_ENDPOINT"
echo "  Model: $CODEX_MODEL"
echo "  Provider: $VBB_PROVIDER"
echo "  Mode: $VBB_MODE"
