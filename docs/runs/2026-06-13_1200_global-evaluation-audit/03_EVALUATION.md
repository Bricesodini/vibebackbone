---
phase: 03
route: AUDIT
run_id: 2026-06-13_1200_global-evaluation-audit
date: 2026-06-13
---

# 03_EVALUATION — Dimension analysis

## 1. Governance architecture (8.5/10)

**Strengths**:
- Clear hierarchy: CONTEXT → PILOTAGE → PROJECT_MODE → SESSION → AUDIT_STATUS
- No parallel truth between files
- 7 governance files with explicit roles
- AGENTS.md compiled as @import block (post RUN 14A)
- SYSTEM.md defines stance, planning, risk, session, editing, communication
- CLAUDE.md minimal boot entry (172 words)
- Memory hierarchy: conversational < local < official versioned

**Weaknesses**:
- AGENTIC_RUN_PROTOCOL.md still in FR (phase descriptions, invariant text)
- No DEPLOYMENT.md or RUNBOOK.md (open since RUN 16)
- CONTEXT.md relies on manual closeout updates; no staleness detection
- PROJECT_MODE.md not present in this repo (DISTRIBUTION mode, by design)

## 2. Contract coverage and quality (8.0/10)

**Strengths**:
- 62/62 contracts exist — full coverage achieved
- 0 lint errors
- Schema includes: id, version, type, formalization_level, entrypoint, compatibility,
  inputs, outputs, gates, events, routing, state_policy, limits
- 62/62 have events + gates + routing + state_policy
- 21/62 have blocking_conditions (appropriate — not all skills need gates)
- Verdict mapping defined for critical audit skills

**Weaknesses**:
- 20/62 CONTRACT.yaml files have FR text in events reasons / gates descriptions
- 16 PARTIAL verdicts without remediation tracking
- 2 BLOCKED verdicts propagated from scope-freeze chain (expected, but not auto-resolving)
- No contract versioning policy (all at "0.3")
- No schema validation beyond lint (e.g., no JSON Schema for CONTRACT.yaml)

## 3. Runtime/tooling readiness (6.5/10)

**Strengths**:
- 7 operational tools, all functional
- Contract lint: catches structural errors
- Contract runtime: dry-run validates execution semantics
- Index: 287 entries, full-text search
- Dashboard: project state at a glance
- Compactor: run summarization
- Loop closure: closeout completeness check
- Project init: bootstrap new projects

**Weaknesses**:
- **No executor**: contracts declare on_fail/on_success events but nothing executes them
- Contract runtime is dry-run only; no "live" execution mode
- No webhook/hook system for CI integration
- Tools are Python scripts, not installable package
- No plugin/extension mechanism for custom tools
- No automated dashboard refresh (manual run required)

## 4. Token economy (8.5/10)

**Strengths**:
- Boot context: ~2,500 tokens (87% reduction from 19,050)
- L0–L4 layer architecture documented and enforced
- AGENTS.md compiled as @import block (363 words vs old 5,186)
- GUIDE.md pushed to L3 reference (on demand only)
- Per-skill token budgets (low/medium/high)
- Index enables targeted retrieval vs. full load
- Individual skills: 200–600 words each (very LLM-friendly)

**Weaknesses**:
- L1 triage layer still ~4,200 tokens; not yet optimized
- No automatic context compaction trigger (agent must remember to compact)
- Some FR text in contracts adds noise for non-FR-reading models
- Total corpus ~490K tokens — large for full-index queries on smaller models

## 5. Context freshness (7.0/10)

**Strengths**:
- CONTEXT.md updated via closeout workflow (not ad hoc)
- SESSION.md local, not versioned — avoids stale committed state
- AUDIT_STATUS.md tracks live risk items
- Activity log records recent actions
- Index rebuilt during significant changes
- Compactor enables clean handoffs

**Weaknesses**:
- No staleness detection: CONTEXT.md can drift if closeout is skipped
- Activity log entries marked PENDING (not resolved) — accumulating debt
- 3 pre-protocol runs without closeout — permanent gap
- No TTL or freshness indicator on governance files
- No automated "is CONTEXT.md current?" check

## 6. Auditability (8.0/10)

**Strengths**:
- 17 audit reports in docs/audits/
- Self-audit triptych completed (RUN 04A/04B/04C)
- Auto-audit synthesis consolidated (RUN 05)
- SYNERGY risk register tracked: 7/12 resolved, 5 mitigated, 0 P0/P1
- Token economy audit quantified (RUN 13)
- Contract runtime provides mechanical verification
- Closeout files provide decision trail
- Run history: 40 directories with named artifacts

**Weaknesses**:
- Phase 0 skills (scope-freeze, audit-readiness) never run on this repo itself
- Phase 2 systemic-risk, ops audits not run
- Phase 3 risk-register not run (needs ≥2 Phase 2 audits first)
- AUDIT_STATUS.md verdict still PARTIAL (not PRODUCTION-READY)
- 2-vbb-spec-validator not run (formal spec validation)

## 7. CI/test maturity (6.0/10)

**Strengths**:
- 2 GitHub workflows: smoke + contracts
- OS matrix: ubuntu-latest + macos-latest
- Permissions minimised: contents: read
- PyYAML version pinned
- Local CI script: 5/6 PASS
- 7 test suites, ~68 test cases
- Contract lint: 15 tests (positive + negative)
- Contract runtime: 62 contracts dry-run

**Weaknesses**:
- **Pytest completely broken** (7/7 test files fail on `name` fixture)
- Tests only work via direct `python3 tests/test_X.py` execution
- No CI test for pytest compatibility
- No coverage reporting
- No mutation testing
- Smoke test only checks install, not functional correctness
- Missing negative tests for: contract-runtime, dashboard, compactor, index
- No integration tests (tool chain as a whole)
- No regression test for SYNERGY fixes

## 8. Multi-agent portability (8.0/10)

**Strengths**:
- Explicit support for 5 providers (Claude Code, Codex, Pi, OpenCode, Cursor/Continue manual)
- setup.sh handles all auto-supported providers
- Artifact format: Markdown standard (no lock-in)
- Skills injectable via `~/.agents/skills/` (universal directory)
- Prompts deployable per-provider
- AGENTS.md + SYSTEM.md governance layer agent-agnostic
- Guide documents multi-agent delegation patterns

**Weaknesses**:
- setup.sh is tested on macOS (author's machine), linux CI; no Windows testing
- No automated compatibility test per provider
- Cursor/Continue require manual setup (documented but not automated)
- No versioning handshake: if vibebackbone updates, how does the agent know?
- No provider-specific behavior testing

## 9. Adoption/friction (7.0/10)

**Strengths**:
- FAST-ZERO/MINIMAL/STANDARD eliminates friction for micro-tasks
- setup.sh single-command install
- 62 skills immediately available after install
- Comprehensive GUIDE.md (pedagogical)
- Cheatsheet + FAQ in GUIDE
- `vbb-index.py search "query"` for discovery

**Weaknesses**:
- README and GUIDE in FR — significant barrier for non-FR adopters
- 7 SKILL.md files with residual FR terms
- setup.sh is 25K monolith — intimidating to audit
- No interactive/onboarding wizard
- No "quick start" in EN
- No visual architecture diagram (only ASCII in README)
- Learning curve: 7 phases × 4 routes × 32 prompts = significant conceptual load

## 10. Formal Skill readiness (5.5/10)

**Strengths**:
- Contract schema is complete and machine-parseable
- All 62 contracts have events, gates, routing, state_policy
- formalization_level field exists (all "declarative")
- Verdict mapping defined for audit skills
- Agent compatibility declared per contract

**Weaknesses**:
- No executor/runtime to actually run Formal Skills
- No hook system (on_fail → trigger another skill)
- No state machine (contract state transitions)
- No formal schema validation (no JSON Schema / Pydantic model)
- FR text in 20 contracts would break machine parsing in some contexts
- No skill composition protocol (how to chain skills programmatically)
- No versioning/diff mechanism for contract evolution

## 11. Local/smaller-model enablement (7.5/10)

**Strengths**:
- L0 boot ~2.5K tokens: fits any model with ≥8K context
- Skills 200–600 words each: load one at a time
- Explicit step-by-step instructions: compensate for weaker planning
- Token budget hints per skill
- Contract gates provide structure and guardrails
- FAST-ZERO route: minimal overhead for simple tasks
- vbb-index.py enables targeted retrieval instead of full load

**Weaknesses**:
- Without executor, smaller models must interpret all rules (cognitive load)
- FR terms in contracts reduce reliability for EN-only models
- GUIDE.md (9.3K words in FR) not accessible to EN-only small models
- No "mini" mode or simplified governance for resource-constrained models
- No benchmark: has Vibebackbone actually been tested with Qwen 27B or similar?

## 12. Product/release readiness (5.0/10)

**Strengths**:
- 62 skills, 32 prompts — substantive catalog
- Install mechanism works (setup.sh + CI)
- Governance docs coherent
- Self-audited
- MIT license
- GitHub-hosted

**Weaknesses**:
- No tagged release (no v1.0)
- No DEPLOYMENT.md or RUNBOOK.md
- Pytest fixtures broken
- No CHANGELOG.md (product changelog skill exists but hasn't produced one for itself)
- No CONTRIBUTING.md
- No release checklist executed
- README/GUIDE in FR limits market
- AUDIT_STATUS.md verdict = PARTIAL (not PRODUCTION-READY)
- 7 SKILL.md files with FR residual
- 20 CONTRACT.yaml files with FR descriptions

---

## Crosscutting observations

1. **The system is more mature than its test infrastructure suggests**. The tools
   work reliably via direct execution; the pytest issue is a fixture wiring bug, not
   a functional failure.

2. **Language duality is a strategic choice, not an accident**. FR for human narrative,
   EN for agent-facing. But the boundary is still blurring in contracts and some skills.

3. **Contract events are the clearest gap**: they describe what should happen but
   nothing makes it happen. This is the single most important architectural decision
   ahead: stay declarative (v1.0) or build an executor (v2.0).

4. **The token economy work is genuinely good**. An 87% boot reduction with no loss
   of information is rare in governance systems.

5. **Run discipline is the strongest cultural signal**. 92% closeout over 40 runs
   shows the governance is actually followed, not just documented.

---

## Handoff

→ 04_SCORECARD: formalize scores