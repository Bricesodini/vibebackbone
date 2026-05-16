#!/bin/bash
# init-codex.sh — Installation vibebackbone pour Codex
# Usage: bash init-codex.sh [--context fresh|existing]

set -e

# Parse arguments
CONTEXT="fresh"  # Default
while [ $# -gt 0 ]; do
  case "$1" in
    --context)
      CONTEXT="$2"
      shift 2
      ;;
    *)
      CONTEXT="$1"  # Positional argument for backward compatibility
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🔴 Installing vibebackbone for Codex"
echo "   Context: $CONTEXT"
echo ""

# Create .codex directory for Codex configuration
mkdir -p .codex

# Copy example env if available
if [ -f "$SCRIPT_DIR/example-env.sh" ]; then
  cp "$SCRIPT_DIR/example-env.sh" .codex/env.sh
  echo "✓ Created .codex/env.sh"
fi

# Initialize PROJECT_MODE.md if fresh installation
if [ "$CONTEXT" = "fresh" ]; then
  mkdir -p docs
  cat > docs/PROJECT_MODE.md << 'EOF'
# PROJECT_MODE — vibebackbone consumer (Codex)

**Mode** : CONSUMER
**Provider** : Codex
**Gouvernance** : vibebackbone v1.0 (Codex v2.0)
**Date** : [Installation date]

## Voies activées
- [x] RAPIDE — corrections mineures
- [x] STRUCTURÉE — features & refactoring
- [x] AUDIT — security, integrity, ops [0→1→2→3 sequence]
- [x] CLÔTURE — session handoff

## Configuration
- Provider: Codex (governance framework)
- Entry point: /AGENTS.md
- Runtime: SYSTEM.md
- Full model: skills/vibebackbone/docs/PILOTAGE.md
- API: export CODEX_API_KEY=...

## Audit sequence [0→1→2→3]
Phase [0] : Readiness (scope-freeze, audit-readiness)
Phase [1] : Structure (conventions, tech-debt, dependency-mapper)
Phase [2] : Deep audits (security, integrity, ops, api, db)
Phase [3] : Consolidation (risk-register)

## Risk management
- P0 (Critical) : Blocks deployment
- P1 (Major) : Must fix before release
- P2 (Minor) : Fix next version
- P3 (Info) : Document and monitor

All findings consolidated in phase [3] risk-register.
EOF
  echo "✓ Created docs/PROJECT_MODE.md (fresh context)"
else
  echo "⊘ Keeping existing docs/PROJECT_MODE.md (existing context)"
fi

# Create session templates if not present
mkdir -p docs/audits
[ ! -f docs/SESSION.md ] && touch docs/SESSION.md && echo "✓ Created docs/SESSION.md (local, gitignored)"
[ ! -f docs/AUDIT_STATUS.md ] && touch docs/AUDIT_STATUS.md && echo "✓ Created docs/AUDIT_STATUS.md (local, gitignored)"

# Verify .gitignore includes local artifacts
if ! grep -q "docs/SESSION.md" .gitignore 2>/dev/null; then
  echo "" >> .gitignore
  echo "# vibebackbone session artifacts" >> .gitignore
  echo "docs/SESSION.md" >> .gitignore
  echo "docs/AUDIT_STATUS.md" >> .gitignore
  echo "docs/audits/" >> .gitignore
  echo "# Codex environment (local secrets)" >> .gitignore
  echo ".codex/env.sh" >> .gitignore
  echo "✓ Updated .gitignore"
fi

echo ""
echo "✓ Codex setup complete"
echo ""
echo "Next steps:"
echo "1. Set Codex API credentials: export CODEX_API_KEY=..."
echo "2. Source .codex/env.sh for configuration"
echo "3. Read /AGENTS.md for triage and operational rules"
echo "4. Read /SYSTEM.md for planning protocol"
echo "5. Execute audit sequence [0→1→2→3]"
echo "6. Check /docs/INSTALLATION.md for multi-provider context"
echo ""
echo "Quick reference:"
echo "  - Skills location: /skills/"
echo "  - Triage reference: /AGENTS.md"
echo "  - Planning protocol: /SYSTEM.md"
echo "  - Governance model: skills/vibebackbone/docs/PILOTAGE.md"
echo "  - Risk consolidation: skills/3-vbb-risk-register/SKILL.md"
echo "  - Session memory: docs/SESSION.md (local)"
echo "  - Audit dashboard: docs/AUDIT_STATUS.md (local)"
echo ""
