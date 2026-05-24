# v1.0 Release Checklist

**Version**: 1.0.0-rc.1  
**Date**: 2026-06-13  
**Status**: Release Candidate

---

## Pre-release checks

### Governance & documentation
- [x] CONTEXT.md reflects current state
- [x] AUDIT_STATUS.md updated
- [x] CHANGELOG.md created
- [x] RELEASE_CHECKLIST.md created
- [x] 7 governance files coherent (no parallel truth)
- [x] No stale TODOs in governance files

### Contract & skill integrity
- [x] 62/62 contracts pass lint (0 errors)
- [x] 62/62 SKILL.md files exist with standardized frontmatter
- [x] Agent-facing language is EN (SKILL.md body, CONTRACT.yaml machine-facing fields)
- [x] Contract runtime dry-run: 25 PASS + 16 PARTIAL + 2 BLOCKED (all expected)

### Test & CI
- [x] pytest: 69/69 green
- [x] CI local: PASS (6/6, 0 warnings on closed runs)
- [x] Loop closure: latest run passes

### Token economy
- [x] L0 boot context: ~2.5K tokens (87% reduction)
- [x] L0–L4 architecture documented
- [x] vbb-index.py builds and searches correctly

### Audit trail
- [x] 17+ audit reports in docs/audits/
- [x] No P0/P1 vulnerabilities
- [x] 92% run closeout rate (37/40)

### Setup & install
- [x] setup.sh tested on macOS and Ubuntu CI
- [x] setup.sh installs for Claude Code, Codex, Pi, OpenCode
- [x] README.md describes installation, usage, and architecture

### Known limitations (documented, not blocking)
- 10/62 SKILL.md files still have FR body content (Phase 4 UX/UI domain + spec-validator, vibebackbone)
- 17/32 prompts in FR (by design — human narrative layer)
- README.md and GUIDE.md in FR (by design)
- 16/62 contract PARTIAL in dry-run (expected — stub outputs don't satisfy success gates)
- 2/62 contract BLOCKED in dry-run (expected — scope-freeze gate chain)
- No Formal Skill executor yet (v2.0 target)
- No DEPLOYMENT.md or RUNBOOK.md yet (post-v1.0)

---

## Release artifacts

| Artifact | Status |
|----------|--------|
| CHANGELOG.md | ✅ Created |
| RELEASE_CHECKLIST.md | ✅ This file |
| CONTEXT.md | ✅ Updated |
| AUDIT_STATUS.md | ✅ Updated |
| Git tag | ⬜ Not yet (awaiting explicit instruction) |

---

## Post-release (v1.1 considerations)

1. Translate remaining 10 SKILL.md files to EN (spec-validator, Phase 4 UX/UI)
2. Translate 17 prompts to EN (or provide EN alternatives)
3. Create DEPLOYMENT.md and RUNBOOK.md
4. Add JSON Schema for CONTRACT.yaml validation
5. Add negative tests for contract-runtime and tools
6. Smaller-model benchmarking (Qwen 27B, etc.)
7. Design Formal Skill executor prototype (v2.0)
8. Produce EN README + GUIDE for international adoption