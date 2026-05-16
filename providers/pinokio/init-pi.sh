#!/bin/bash
# init-pi.sh — Installation vibebackbone pour Pi (Pinokio)
# Usage: bash init-pi.sh [--context fresh|existing]

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

echo "🟡 Installing vibebackbone for Pi (Pinokio)"
echo "   Context: $CONTEXT"
echo ""

# Create .pi directories for Pi configuration
mkdir -p .pi/agents
mkdir -p .pi/hippo-memory

# Copy example taskplane.json if available
if [ -f "$SCRIPT_DIR/example-taskplane.json" ]; then
  cp "$SCRIPT_DIR/example-taskplane.json" .pi/taskplane.json
  echo "✓ Created .pi/taskplane.json"
else
  # Create minimal taskplane.json if template doesn't exist
  cat > .pi/taskplane.json << 'EOF'
{
  "project_name": "vibebackbone-consumer",
  "mode": "CONSUMER",
  "provider": "pi",
  "governance": "vibebackbone v1.0",
  "entry_point": "SYSTEM.md",
  "triage_reference": "AGENTS.md",
  "skills_catalog": "README.md",
  "agents": [
    {
      "name": "supervisor",
      "role": "Audit coordinator",
      "model": "claude-opus-4.7",
      "skills_phases": [0, 1, 2, 3]
    }
  ],
  "planning_protocol": "enabled",
  "risk_discipline": "enabled",
  "context_llm_discipline": "enabled"
}
EOF
  echo "✓ Created .pi/taskplane.json (minimal)"
fi

# Initialize PROJECT_MODE.md if fresh installation
if [ "$CONTEXT" = "fresh" ]; then
  mkdir -p docs
  cat > docs/PROJECT_MODE.md << 'EOF'
# PROJECT_MODE — vibebackbone consumer (Pi)

**Mode** : CONSUMER
**Provider** : Pi (Pinokio)
**Gouvernance** : vibebackbone v1.0
**Date** : [Installation date]

## Voies activées
- [x] RAPIDE — corrections mineures
- [x] STRUCTURÉE — features & refactoring
- [x] AUDIT — security, integrity, ops
- [x] CLÔTURE — session handoff

## Configuration
- Provider: Pi (Pinokio agent framework)
- Runtime config: .pi/taskplane.json
- Entry point: `/SYSTEM.md`
- Triage: `/AGENTS.md` § 3
- Skills catalog: `/README.md`

## Agent workflows
1. Read phase [0] preconditions (scope-freeze, audit-readiness)
2. Execute phase [1] skills (structure, conventions, tech-debt)
3. Execute phase [2] skills (security, integrity, ops)
4. Consolidate in phase [3] (risk-register)

## Skills routing
- Never [2] without [0] + [1] dependency-mapper
- Respect INPUT CONTRACT and BLOCKING CONDITIONS per skill
- Document output in docs/audits/[skill]-[date].md
- Update docs/AUDIT_STATUS.md after each phase
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
  echo "# Pi hippo memory (optional)" >> .gitignore
  echo ".pi/hippo-memory/" >> .gitignore
  echo "✓ Updated .gitignore"
fi

echo ""
echo "✓ Pi setup complete"
echo ""
echo "Next steps:"
echo "1. Edit .pi/taskplane.json with your project context"
echo "2. Read /SYSTEM.md for Pi runtime behavior"
echo "3. Refer to /AGENTS.md for agent orchestration rules"
echo "4. Configure .pi/agents/ for your specific agents"
echo "5. Check /docs/INSTALLATION.md for multi-provider context"
echo ""
echo "Quick reference:"
echo "  - Skills location: /skills/"
echo "  - Entry point: /SYSTEM.md"
echo "  - Config: .pi/taskplane.json"
echo "  - Session memory: docs/SESSION.md (local)"
echo "  - Audit dashboard: docs/AUDIT_STATUS.md (local)"
echo ""
