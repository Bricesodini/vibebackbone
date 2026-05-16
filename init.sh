#!/bin/bash
# init.sh — Universal installer pour vibebackbone
# Détecte provider + contexte (fresh/existing) + configure automatiquement
# Usage: bash init.sh [--provider pi|claude|opencode|codex] [--auto]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ============================================================================
# Helper functions
# ============================================================================

show_usage() {
  cat << 'EOF'
vibebackbone universal installer

Usage: bash init.sh [OPTIONS]

Options:
  --provider [pi|claude|opencode|codex]  Explicit provider selection
  --auto                                  Auto-detect provider from environment
  --help                                  Show this help message

Examples:
  bash init.sh --provider claude          # Install for Claude Code
  bash init.sh --auto                      # Auto-detect from environment
  bash init.sh                             # Interactive selection

Environment variables:
  VBB_PROVIDER                            Force provider (pi|claude|opencode|codex)
  VBB_CONTEXT                             Force context (fresh|existing)

EOF
}

# ============================================================================
# Phase 1: Detect provider
# ============================================================================

detect_provider() {
  # 1. Check explicit flag
  if [ -n "$EXPLICIT_PROVIDER" ]; then
    echo "$EXPLICIT_PROVIDER"
    return
  fi

  # 2. Check environment variable
  if [ -n "$VBB_PROVIDER" ]; then
    echo "$VBB_PROVIDER"
    return
  fi

  # 3. Check for provider-specific files
  [ -f ".pi/taskplane.json" ] && echo "pi" && return
  [ -f ".claude/settings.json" ] && echo "claude" && return
  [ -f ".opencode/config.json" ] && echo "opencode" && return
  [ -f ".codex/env.sh" ] && echo "codex" && return

  # 4. Interactive prompt
  if [ -z "$AUTO_DETECT" ]; then
    echo "No provider detected in environment. Which provider?"
    echo ""
    echo "  1) Pi (Pinokio)     — Agent framework"
    echo "  2) Claude Code      — IDE integration"
    echo "  3) OpenCode         — Distribution standard"
    echo "  4) Codex            — Governance framework"
    echo ""
    read -p "Choice [1-4]: " choice
    case $choice in
      1) echo "pi" ;;
      2) echo "claude" ;;
      3) echo "opencode" ;;
      4) echo "codex" ;;
      *) echo "Invalid choice: $choice"; exit 1 ;;
    esac
  else
    # Auto-detect failed, exit
    echo "Auto-detect failed: no provider-specific files found and VBB_PROVIDER not set"
    exit 1
  fi
}

# ============================================================================
# Phase 2: Detect context (fresh vs existing)
# ============================================================================

detect_context() {
  # 1. Check environment variable
  if [ -n "$VBB_CONTEXT" ]; then
    echo "$VBB_CONTEXT"
    return
  fi

  # 2. Check if docs/PROJECT_MODE.md exists
  if [ -f "docs/PROJECT_MODE.md" ]; then
    echo "existing"
  else
    echo "fresh"
  fi
}

# ============================================================================
# Phase 3: Delegate to targeted installer
# ============================================================================

delegate_to_provider() {
  local provider="$1"
  local context="$2"

  case "$provider" in
    pi)
      echo "→ Delegating to providers/pinokio/init-pi.sh"
      bash "$SCRIPT_DIR/providers/pinokio/init-pi.sh" --context "$context"
      ;;
    claude)
      echo "→ Delegating to providers/claude-code/init-claude.sh"
      bash "$SCRIPT_DIR/providers/claude-code/init-claude.sh" --context "$context"
      ;;
    opencode)
      echo "→ Delegating to providers/opencode/init-opencode.sh"
      bash "$SCRIPT_DIR/providers/opencode/init-opencode.sh" --context "$context"
      ;;
    codex)
      echo "→ Delegating to providers/codex/init-codex.sh"
      bash "$SCRIPT_DIR/providers/codex/init-codex.sh" --context "$context"
      ;;
    *)
      echo "Unknown provider: $provider"
      exit 1
      ;;
  esac
}

# ============================================================================
# Main execution
# ============================================================================

main() {
  # Parse command-line arguments
  while [ $# -gt 0 ]; do
    case "$1" in
      --provider)
        EXPLICIT_PROVIDER="$2"
        shift 2
        ;;
      --auto)
        AUTO_DETECT=1
        shift
        ;;
      --help)
        show_usage
        exit 0
        ;;
      *)
        echo "Unknown option: $1"
        show_usage
        exit 1
        ;;
    esac
  done

  echo "=========================================="
  echo "vibebackbone universal installer"
  echo "=========================================="
  echo ""

  # Detect provider
  PROVIDER="$(detect_provider)"
  echo "✓ Provider: $PROVIDER"

  # Detect context
  CONTEXT="$(detect_context)"
  echo "✓ Context: $CONTEXT"

  echo ""

  # Delegate to provider-specific installer
  delegate_to_provider "$PROVIDER" "$CONTEXT"

  echo ""
  echo "=========================================="
  echo "✓ Installation complete!"
  echo "=========================================="
  echo ""
  echo "Provider: $PROVIDER"
  echo "Context: $CONTEXT"
  echo ""
  echo "Next steps:"
  case "$PROVIDER" in
    pi)
      echo "  1. Edit .pi/taskplane.json with your project context"
      echo "  2. Read /SYSTEM.md for Pi runtime behavior"
      echo "  3. Start executing skills following the phase sequence [0→1→2→3]"
      ;;
    claude)
      echo "  1. Open this folder in Claude Code (File → Open Folder)"
      echo "  2. Read /CLAUDE.md for operational rules"
      echo "  3. Pick a skill and follow PROCESS steps"
      ;;
    opencode)
      echo "  1. Fork vibebackbone on GitHub"
      echo "  2. Read /CONTRIBUTING.md for contribution guidelines"
      echo "  3. Create branch for your skill or feature"
      ;;
    codex)
      echo "  1. Set Codex API credentials: export CODEX_API_KEY=..."
      echo "  2. Source .codex/env.sh for configuration"
      echo "  3. Execute audit sequence [0→1→2→3]"
      ;;
  esac
  echo ""
  echo "Documentation:"
  echo "  - Entry point: /README.md"
  echo "  - Triage rules: /AGENTS.md"
  echo "  - Provider setup: providers/$PROVIDER/INTEGRATION.md"
  echo "  - Multi-provider: docs/INSTALLATION.md"
  echo ""
}

# Run main
main "$@"
