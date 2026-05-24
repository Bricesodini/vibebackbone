---
audit_type: global_evaluation
date: 2026-06-13
auditor: self-audit (AUDIT route)
scope: full_system
verdict: MATURING — strong governance, gaps in runtime enforcement and test infrastructure
---

# Global Evaluation — Vibebackbone

**Date**: 2026-06-13  
**Type**: Fine-grained global evaluation audit  
**Route**: AUDIT  
**Verdict**: 🟡 MATURING — governance-complete, runtime enforcement incomplete

---

## 1. Executive Summary

Vibebackbone has undergone 40 runs, 37 closeouts (92%), 17 audit reports, and a systematic
contractualization campaign. The system achieves 62/62 contract coverage, 62/62 SKILL.md EN
harmonization, and a boot context reduced from ~19K to ~2.5K tokens (87% reduction). The
governance architecture is coherent, the contract schema is structurally complete, and CI
guardrails exist. However: runtime enforcement remains declarative-only (no executor hooks),
7/62 SKILL.md files still carry FR residual terms, 20/62 CONTRACT.yaml files have FR
descriptions in events/gates, pytest fixtures are broken (7/7 test files fail on `name`
fixture), and the README/GUIDE remain in FR (by design). The system is **not yet ready
for a tagged release as a formal product**, but is mature as a Markdown/Contract governance
framework ready for early adopters.

---

## 2. System Inventory

### 2.1 Artifacts

| Category | Count | Status |
|----------|-------|--------|
| Skills (SKILL.md) | 62 | ✅ 62/62 exist |
| Contracts (CONTRACT.yaml) | 62 | ✅ 62/62 exist |
| Prompts | 32 | ✅ 7 canonical + 24 specialized + 1 router |
| Governance files | 7 | ✅ CONTEXT, PILOTAGE, SESSION_RULES, MEMORY_AND_HANDOFF, AGENTS, SYSTEM, CLAUDE |
| CI workflows | 2 | ✅ smoke.yml + vbb-contracts.yml |
| Test suites | 7 | ⚠️ Broken fixtures (7 errors) |
| Tools | 7 | ✅ contract-lint, contract-runtime, index, dashboard, compactor, loop-closure, project-init |
| Run directories | 40 | ✅ 92% closeout rate |
| Audit reports | 17 | ✅ Security, tech-debt, CI, token-economy, synthesis |
| Templates | 7 | ✅ 01–07 phase templates |

### 2.2 Run History

- 40 run directories since 2026-05-18
- 37 with formal closeout (92%)
- 3 pre-protocol runs without closeout (documented)
- Key milestones: Lot 0–1C stabilization, SYNERGY risk remediation, contractualization wave,
  token economy refactor, SKILL.md EN harmonization

---

## 3. Before/After Comparison

| Dimension | Before | After | Delta |
|-----------|--------|-------|-------|
| Contract coverage | 22/58 (38%) | 62/62 (100%) | +40 contracts |
| Boot context | ~19,050 tokens | ~2,500 tokens | −87% |
| SKILL.md language | FR | EN (62/62 clean) | Full harmonization |
| Contract dry-run | 15/43 tested | 25 PASS + 16 PARTIAL + 2 BLOCKED | Full coverage |
| Test suites | ~3 ad hoc | 7 suites (broken fixtures) | +4 suites |
| Tools | 3 (lint, runtime, dashboard) | 7 (+index, compactor, loop-closure, project-init) | +4 tools |
| Audits completed | 0 formal | 17 reports | Full triptych |
| FAST route | Heavy (no levels) | ZERO/MINIMAL/STANDARD | 3-level friction reduction |
| Memory | docs only | compactor + index + dashboard | Active tooling |
| SYNERGY risks | 12 identified | 7 resolved, 5 mitigated | P0/P1 = 0 |
| Governance duplication | 10+ broken links | Canonical links established | Resolved |

---

## 4. Dimension Scores

See 04_SCORECARD.md for the detailed 0–10 scoring.

---

## 5. Key Findings

### 5.1 Strengths

1. **Governance coherence**: 7 governance files form a clear hierarchy, no parallel truth
2. **Contract schema completeness**: 62/62 contracts with events, gates, routing, state_policy
3. **Boot context economy**: 87% reduction, L0/L1/L2/L3/L4 architecture documented
4. **Run discipline**: 92% closeout rate across 40 runs, 7-phase protocol enforced
5. **Multi-agent design**: Explicit support for Claude Code, Codex, Pi, OpenCode
6. **FAST friction reduction**: ZERO/MINIMAL/STANDARD levels eliminate overhead for micro-tasks
7. **Self-auditing**: The system was used to audit itself (RUN 04A/B/C triptych)
8. **Tool chain**: 7 operational tools, all functional, with dry-run and reporting
9. **Contract lint & runtime**: 0 lint errors, 25/43 PASS on dry-run
10. **Documented token economy**: Explicit L0–L4 layer model with token counts

### 5.2 Weaknesses

1. **No runtime executor**: Contracts are declarative-only; no hook/trigger/state machine
2. **Pytest fixtures broken**: All 7 test files use `name` as a pytest parameter (not fixture),
   causing 7/7 errors when run via `pytest`
3. **FR residual in contracts**: 20/62 CONTRACT.yaml files have FR descriptions in events.gates
4. **FR residual in 7 SKILL.md**: Still carry 8–70 FR terms each
5. **README/GUIDE in FR**: By design, but limits adoption for non-FR communities
6. **setup.sh monolith**: 25K single script, documented but not decomposed
7. **No negative test coverage**: Contract lint has negative tests, but runtime/tools lack them
8. **PARTIAL verdicts unexplained**: 16/43 contract runs return PARTIAL without clear remediation path
9. **No DEPLOYMENT.md/RUNBOOK.md**: Listed as open point since RUN 16
10. **Loop closure check WARN**: Most recent run flagged as missing frontmatter

---

## 6. Formal Skill Readiness

**Verdict: NOT YET — justified but not ready**

The contract schema is structurally complete to become a Formal Skill specification.
However, three prerequisites are unmet:

1. **No executor**: Formal Skills require runtime hooks (on_fail, on_success, gates)
   that actually execute, not just declare intent
2. **FR descriptions in contracts**: Machine-readable contracts must be language-neutral
3. **Broken test fixtures**: Before forking to Formal Skill, the test infrastructure
   must be reliable

**Recommendation**: Continue in Markdown/Contract mode for v1.0. Plan Formal Skill fork
for v2.0 after executor/hook/state machine is implemented.

---

## 7. Local/Smaller Model Enablement

Vibebackbone's architecture is **well-suited** for smaller models (Qwen 27B, etc.):

- **L0 boot is ~2.5K tokens** → fits comfortably in smaller context windows
- **Skills are 200–600 words each** → can be loaded one at a time
- **Explicit steps in SKILL.md** → reduces reasoning overhead
- **Contract gates** → provide structure that compensates for weaker planning
- **Token budget field** → per-skill budget hints for context management

**Limitation**: Without an executor, the smaller model must interpret and follow all
declarative rules on its own. A Formal Skill runtime would significantly reduce the
cognitive burden on smaller models by making rules executable rather than interpretable.

---

_vibebackbone Global Evaluation Audit — 2026-06-13_