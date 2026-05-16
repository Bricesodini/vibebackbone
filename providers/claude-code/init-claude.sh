#!/bin/bash
# init-claude.sh — Installation vibebackbone pour Claude Code
# Usage: bash init-claude.sh [--context fresh|existing]

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

echo "🔵 Installing vibebackbone for Claude Code"
echo "   Context: $CONTEXT"
echo ""

# Create .claude directory for Claude Code settings
mkdir -p .claude

# Copy example settings if available
if [ -f "$SCRIPT_DIR/example-settings.json" ]; then
  cp "$SCRIPT_DIR/example-settings.json" .claude/settings.json
  echo "✓ Created .claude/settings.json"
fi

# Initialize PROJECT_MODE.md if fresh installation
if [ "$CONTEXT" = "fresh" ]; then
  mkdir -p docs
  cat > docs/PROJECT_MODE.md << 'EOF'
# PROJECT_MODE — vibebackbone consumer (Claude Code)

**Mode** : CONSUMER
**Provider** : Claude Code
**Gouvernance** : vibebackbone v1.0
**Date** : [Installation date]

## Voies activées
- [x] RAPIDE — corrections mineures
- [x] STRUCTURÉE — features & refactoring
- [x] AUDIT — security, integrity, ops
- [x] CLÔTURE — session handoff

## Configuration
- Provider: Claude Code (IDE)
- Entry point: `/CLAUDE.md`
- Triage: `/AGENTS.md` § 3
- Skills catalog: `/README.md`

## Workflows
1. Read `skills/[phase]-vbb-[name]/SKILL.md`
2. Check INPUT CONTRACT and BLOCKING CONDITIONS
3. Execute PROCESS steps
4. Document output in `docs/audits/`
5. Update `docs/AUDIT_STATUS.md` with findings
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
echo "✓ Claude Code setup complete"
echo ""
echo "Next steps:"
echo "1. Open this folder in Claude Code (File → Open Folder)"
echo "2. Read /CLAUDE.md for operational rules"
echo "3. Refer to /README.md for 57 skills catalog"
echo "4. Use /AGENTS.md for triage and escalation rules"
echo "5. Check /docs/INSTALLATION.md for multi-provider context"
echo ""
echo "Quick reference:"
echo "  - Skills location: /skills/"
echo "  - Entry point: /CLAUDE.md"
echo "  - Session memory: docs/SESSION.md (local)"
echo "  - Audit dashboard: docs/AUDIT_STATUS.md (local)"
echo ""
