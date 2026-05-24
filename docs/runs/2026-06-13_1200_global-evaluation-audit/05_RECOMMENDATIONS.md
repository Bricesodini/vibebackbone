---
phase: 05
route: AUDIT
run_id: 2026-06-13_1200_global-evaluation-audit
date: 2026-06-13
---

# 05_RECOMMENDATIONS — Priority actions

## P1 — Must fix before v1.0 release

### R-01: Fix pytest fixtures

- **Problem**: All 7 test files use `name` as a function parameter, which pytest interprets
  as a fixture request → 7/7 errors
- **Fix**: Remove `name` from test function signatures or use `@pytest.mark.parametrize`
- **Effort**: 2h
- **Impact**: CI reliability, test legitimacy

### R-02: Complete SKILL.md EN cleanup (4 files)

- **Problem**: 4 SKILL.md files still have 28–70 FR terms in body (not just cognates)
  - 2-vbb-spec-validator (70 terms)
  - 2-vbb-performance (55 terms)
  - 4-vbb-security-remediation (42 terms)
  - 3-vbb-risk-register (37 terms)
- **Fix**: Translate remaining FR body content to EN
- **Effort**: 3h
- **Impact**: Cross-agent consistency, smaller-model reliability

### R-03: Translate CONTRACT.yaml FR descriptions

- **Problem**: 20/62 contracts have FR text in events.reason, gates.reason fields
- **Fix**: Translate reason/description fields to EN in all CONTRACT.yaml
- **Effort**: 2h
- **Impact**: Machine readability, Formal Skill readiness

### R-04: Produce CHANGELOG.md

- **Problem**: No product changelog for the repo itself
- **Fix**: Apply 4-vbb-product-changelog skill to vibebackbone
- **Effort**: 2h
- **Impact**: Release readiness, adopter communication

### R-05: Run full release-check

- **Problem**: No pre-release verification ever performed
- **Fix**: Apply 2-p-vbb-release-check (14 skills in 4 waves)
- **Effort**: 4h (wave by wave, separate sessions)
- **Impact**: Release gate confidence

## P2 — Should fix before v1.0 release

### R-06: Create DEPLOYMENT.md + RUNBOOK.md

- **Problem**: Open since RUN 16, no operational documentation
- **Fix**: Write minimal deployment and runbook docs
- **Effort**: 3h
- **Impact**: Professional adoptability

### R-07: Add JSON Schema for CONTRACT.yaml

- **Problem**: Contract lint validates presence but not schema conformance
- **Fix**: Create `schemas/contract.schema.json` and validate against it
- **Effort**: 4h
- **Impact**: Formal Skill readiness, machine validation

### R-08: Add contract versioning policy

- **Problem**: All contracts at "0.3" with no versioning semantics
- **Fix**: Define versioning scheme (semver for contracts) and update
- **Effort**: 2h
- **Impact**: Contract evolution management

### R-09: Add negative tests for contract-runtime and index

- **Problem**: Contract lint has negative tests, but runtime/index/dashboard/compactor don't
- **Fix**: Add error-path test cases to each tool
- **Effort**: 4h
- **Impact**: CI robustness

### R-10: Produce EN README + GUIDE

- **Problem**: README and GUIDE in FR only, limits international adoption
- **Fix**: Translate or produce EN versions (README-en.md, GUIDE-en.md or i18n)
- **Effort**: 8h
- **Impact**: Market reach

## P3 — Post v1.0

### R-11: Design executor prototype

- **Problem**: Contracts declare events but nothing executes them
- **Fix**: Prototype executor that reads CONTRACT.yaml events and triggers chains
- **Effort**: 40h (v2.0 scope)
- **Impact**: Formal Skill foundation

### R-12: Smaller-model benchmarking

- **Problem**: No evidence Vibebackbone actually helps smaller models
- **Fix**: Run structured tests with Qwen 27B, Phi-3, etc. using Vibebackbone governance
- **Effort**: 20h
- **Impact**: Enablement evidence, marketing

### R-13: Contract runtime "live" mode

- **Problem**: Runtime only supports dry-run
- **Fix**: Add execution mode that actually triggers event chains
- **Effort**: 30h (depends on R-11)
- **Impact**: Operational automation

### R-14: Context staleness detector

- **Problem**: CONTEXT.md can drift if closeout is skipped
- **Fix**: Add TTL/freshness indicator and automated check
- **Effort**: 8h
- **Impact**: Context integrity

### R-15: setup.sh decomposition

- **Problem**: 25K monolith script
- **Fix**: Split into modules: install.sh, configure-claude.sh, configure-codex.sh, etc.
- **Effort**: 8h
- **Impact**: Maintainability, auditability

---

## Priority matrix

```
           High impact
               |
    R-01       |  R-05  R-11
    R-02  R-04 |  R-07  R-12
    R-03       |  R-13
               |
  -------------+-------------
   Quick       |   Long
               |
    R-06  R-08 |  R-10  R-14
          R-09 |  R-15
               |
           Low impact
```

**Recommended execution order**:
1. R-01 (pytest fix) — unblocks CI confidence
2. R-02 + R-03 (FR cleanup) — unblocks release quality
3. R-04 (CHANGELOG) — release artifact
4. R-05 (release-check) — release gate
5. R-06 + R-08 (ops docs + versioning) — professional polish
6. Tag v1.0.0
7. R-10 (EN README/GUIDE) — market expansion
8. R-07 + R-09 (schema + negative tests) — infrastructure
9. R-11 + R-13 (executor + live mode) — v2.0 foundation
10. R-12 (smaller-model benchmarking) — enablement evidence

---

## Handoff

→ 06_REVIEW_NOTES: cross-check evaluation