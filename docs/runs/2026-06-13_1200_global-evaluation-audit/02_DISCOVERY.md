---
phase: 02
route: AUDIT
run_id: 2026-06-13_1200_global-evaluation-audit
date: 2026-06-13
---

# 02_DISCOVERY — Raw findings

## Data collected

### Governance architecture

7 governance files form a clear hierarchy:
- L0: CONTEXT.md (MOC/router, 259 words)
- L1: AGENTS.md (363 words, compiled boot block), SYSTEM.md (641 words), CLAUDE.md (172 words)
- L1+: PILOTAGE.md (386 words), SESSION_RULES.md (206 words), MEMORY_AND_HANDOFF.md (266 words)

Total boot context: ~2,293 words ≈ 2,500 tokens (down from ~19,050)

Document hierarchy explicit: CONTEXT → PILOTAGE → PROJECT_MODE → SESSION → AUDIT_STATUS

No parallel truth detectable. AGENTS.md now compiled as @import block (not full text).

### Contract coverage

62/62 CONTRACT.yaml files exist. 0 lint errors.

Structure: all 62 have: id, version, type, formalization_level, entrypoint, compatibility,
inputs, outputs, gates, events, routing, state_policy, limits.

21/62 have blocking_conditions. All have verdict_mapping or status enums.

Contract sophistication:
- events: 62/62 ✅
- gates: 62/62 ✅
- routing: 62/62 ✅
- state_policy: 62/62 ✅
- blocking: 21/62 (34%)

Dry-run results: 25 PASS · 16 PARTIAL · 2 BLOCKED

**FR in contracts**: 20/62 CONTRACT.yaml files have FR descriptions in events.gates.reason fields.

### SKILL.md language

62/62 SKILL.md files confirmed EN-clean via structured verification (verified in RUN 18B).

Residual check: 7 files still match FR term patterns. Analysis shows these are **technical
cognates** (security/sécurité, audit, risk/risque, validation, configuration) that are
legitimate English borrowings in technical context, plus some FR terms in body text that
escaped the route-term sweep:
- 2-vbb-performance: 55 FR terms (substantial FR body text)
- 2-vbb-spec-validator: 70 FR terms
- 3-vbb-risk-register: 37 FR terms
- 4-vbb-front-pipeline-reference: 8 FR terms
- 4-vbb-micro-interaction-refiner: 8 FR terms
- 4-vbb-product-changelog: 28 FR terms
- 4-vbb-security-remediation: 42 FR terms

**Re-classification**: The RUN 18B closeout declared "0 FR route terms" (voie, RAPIDE, etc.).
The remaining FR terms are domain vocabulary, not route language. However, 4 files
(performance, spec-validator, risk-register, security-remediation) have substantial FR
body content (28–70 terms) suggesting incomplete translation.

### Token economy

Current L0 boot: ~2,500 tokens (87% reduction from 19,050)

L0–L4 architecture:
- L0 Boot (~2.5K): CONTEXT + SYSTEM + CLAUDE + ACTIVITY_LOG
- L1 Triage (~4.2K): AUDIT_STATUS + PILOTAGE + phase-router + MEMORY_HANDOFF
- L2 Contract (~4.5K): SKILL.md + CONTRACT.yaml + canonical prompt
- L3 Reference (~12.8K): GUIDE + AGENTS + README + DEPLOYMENT
- L4 Archive (~75K+): runs/ + audits/ (indexed, not loaded)

All SKILL.md total: 45,843 words (~318K chars) across 62 files.
Individual skills: 200–600 words each.
All prompts total: 17,649 words (~120K chars) across 32 files.

### Runtime/tooling

7 tools operational:
1. vbb-contract-lint.py — 0 errors on 62 contracts ✅
2. vbb-contract-runtime.py — 62 contracts dry-run ✅
3. vbb-index.py — 287 entries, ~291K tokens indexed ✅
4. vbb-status-dashboard.py — JSON + terminal output ✅
5. vbb-context-compactor.py — run summarization ✅
6. vbb-loop-closure-check.py — closeout validation ✅
7. vbb-project-init.py — project bootstrap ✅

No executor, no hooks, no trigger system. Contracts declare events but nothing executes them.

### CI/Tests

2 GitHub workflows: smoke.yml + vbb-contracts.yml
- Both run on push + PR
- Both test ubuntu-latest + macos-latest
- Permissions: contents: read ✅
- PyYAML pinned >=6.0,<7.0 ✅

Local CI: 5/6 PASS, 1 WARN (active run closure)

**Pytest broken**: All 7 test files use `name` as a parameter in test function signatures,
which pytest interprets as a fixture request. 7/7 errors. Tests work when run directly
(`python3 tests/test_X.py`) but not via `pytest`.

Test coverage: contract-lint (15 tests), loop-closure (14 tests), portability, project-init,
status-dashboard, vbb-index, context-compactor = ~68–69 test cases.

No negative test coverage for contract-runtime, dashboard, compactor, or index tools.

### Auditability

17 audit reports in docs/audits/. Key ones:
- Security audit (2 reports)
- Tech-debt audit
- CI audit
- Auto-audit synthesis
- Token-economy audit

AUDIT_STATUS.md tracks all risk items. 22 risks identified in RUN 05 synthesis.
SYNERGY risks: 7/12 resolved, 5 mitigated. 0 P0, 0 P1.

### Runs

40 run directories. 37 with formal closeout (92%). 3 pre-protocol runs without.

Latest runs focused on: contractualization (9 runs), token economy (4 runs),
skill language EN (2 runs), CI/tests (4 runs), audits (6 runs).

### Multi-agent portability

Explicit support: Claude Code, Codex CLI, Pi, OpenCode.
Cursor/Continue: manual setup documented.
setup.sh handles all 5 auto-supported providers.

Cross-agent artifact format: Markdown standard, no proprietary format. ✅

### Human-facing docs

README.md: FR (by design, product positioning)
GUIDE.md: FR (by design, pedagogical companion)
Both are comprehensive but FR-only limits international adoption.

### Context freshness

CONTEXT.md updated through closeout workflow.
SESSION.md is gitignored/local.
Activity log tracked.
Index rebuilt on each significant change.

No staleness detection mechanism. No automated check for outdated CONTEXT.md.

---

## Handoff

→ 03_EVALUATION: score each dimension