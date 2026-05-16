#!/bin/bash
# init-opencode.sh — Installation vibebackbone pour OpenCode
# Usage: bash init-opencode.sh [--context fresh|existing]

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

echo "🟢 Installing vibebackbone for OpenCode"
echo "   Context: $CONTEXT"
echo ""

# Create .opencode directory for OpenCode configuration
mkdir -p .opencode

# Copy example config if available
if [ -f "$SCRIPT_DIR/example-config.json" ]; then
  cp "$SCRIPT_DIR/example-config.json" .opencode/config.json
  echo "✓ Created .opencode/config.json"
fi

# Initialize PROJECT_MODE.md if fresh installation
if [ "$CONTEXT" = "fresh" ]; then
  mkdir -p docs
  cat > docs/PROJECT_MODE.md << 'EOF'
# PROJECT_MODE — vibebackbone consumer (OpenCode)

**Mode** : CONSUMER
**Provider** : OpenCode
**Gouvernance** : vibebackbone v1.0
**Date** : [Installation date]

## Voies activées
- [x] RAPIDE — corrections mineures
- [x] STRUCTURÉE — features & refactoring
- [x] AUDIT — security, integrity, ops
- [x] CLÔTURE — session handoff

## Configuration
- Provider: OpenCode (distribution standard)
- Distribution: GitHub (fork and contribute)
- Entry point: `/README.md`
- Contribution guide: `/CONTRIBUTING.md`
- License: `/LICENSE` (MIT)

## Workflows
1. Fork vibebackbone on GitHub
2. Create branch for your contribution
3. Follow skill template: skills/[phase]-vbb-[name]/SKILL.md
4. Validate INPUT CONTRACT and BLOCKING CONDITIONS
5. Submit PR with test evidence
6. Community review and merge

## Distribution
- Skills are open-source (MIT license)
- Prompts are reusable templates
- Governance is transparent and versioned
- Community can fork, extend, contribute
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
  echo "✓ Updated .gitignore"
fi

echo ""
echo "✓ OpenCode setup complete"
echo ""
echo "Next steps:"
echo "1. Fork vibebackbone on GitHub (or clone locally)"
echo "2. Read /README.md for skills catalog"
echo "3. Read /CONTRIBUTING.md for contribution guidelines"
echo "4. Create branch for your skill or feature"
echo "5. Follow skill template: skills/[phase]-vbb-[name]/SKILL.md"
echo "6. Validate and test your contribution"
echo "7. Submit PR with evidence"
echo ""
echo "Quick reference:"
echo "  - Skills location: /skills/"
echo "  - Contribution guide: /CONTRIBUTING.md"
echo "  - License: /LICENSE (MIT)"
echo "  - Session memory: docs/SESSION.md (local)"
echo "  - Audit dashboard: docs/AUDIT_STATUS.md (local)"
echo ""
