---
context_role: audit-dashboard
phase: transverse
status: active
updated: 2026-05-27
temporal_provenance: TEMPORAL_PROVENANCE.md
---

# AUDIT_STATUS — vibebackbone

> Audit status of **vibebackbone-as-a-project** (the repo governed by its own protocol).
> Not a template — see [`templates/`](templates/) for distributable artifacts.

## Global verdict

**`PARTIAL — v1.0-rc.1 ready, post-hardening`**

Global evaluation audit completed (RUN 19, composite score 7.4/10).
v1.0 Hardening phase completed (RUNs 20A–20D):
- Test reliability: 69/69 pytest green, CI 7/7 PASS
- Contract quality: 62/62 valid, machine-facing EN-clean
- Agent language: 52/62 SKILL.md body EN-clean, 10 remaining (Phase 4 + spec-validator)
- Release readiness: CHANGELOG.md, RELEASE_CHECKLIST.md created

New local pilotage audit on 2026-05-27 identified 3 P1 and 3 P2 risks
around indexed-contract coverage, router false positives, canonical pilotage
ambiguity, temporal provenance, search-index availability, and stale status
counts. The remediation pass resolved the 3 P1 risks, resolved PILOT-005,
documented temporal provenance for PILOT-004, and moved PILOT-006 to mitigating. Historical post-hardening risks remain: 2 P2 mitigated (SYNERGY-004
setup.sh monolith, SYNERGY-005 governance duplication).

## Hardening status (RUNs 20A–20D)

| Run | Target | Result |
|-----|--------|--------|
| 20A | Test reliability | ✅ 69/69 pytest green, CI PASS |
| 20B | Contract quality | ✅ 62/62 valid, 44 contracts EN-cleaned |
| 20C | Agent language | ✅ 4 priority SKILL.md EN-translated, 10 remain |
| 20D | Release candidate | ✅ CHANGELOG.md, RELEASE_CHECKLIST.md created |

## Contract runtime status

`run --all --dry-run`: 44 PASS · 16 PARTIAL · 2 BLOCKED

- 16 PARTIAL: expected (dry-run stubs don't satisfy success gates)
- 2 BLOCKED: expected (scope-freeze gate chain)

## Risks identified & status

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| PILOT-001 | P1 | `skills/INDEX.yaml` indexes 43/62 contracts; router/runtime coverage is lower than documented contract-file coverage | Resolved — index now 62/62, linter guard added, runtime executes 62 contracts |
| PILOT-002 | P1 | Phase router can route unknown/unindexed requests from agent/phase scoring without semantic trigger match | Resolved — router now requires trigger match, regression test green |
| PILOT-003 | P1 | Two pilotage files claim canonical authority and diverge (`docs/PILOTAGE.md` v2.2 vs `skills/vibebackbone/docs/PILOTAGE.md` v2.1) | Resolved — root pilotage declared canonical, catalog doc demoted to detailed reference |
| PILOT-004 | P2 | Central status/run artifacts are dated 2026-06-10..13 while local audit date is 2026-05-27 | Resolved — temporal skew documented in `docs/TEMPORAL_PROVENANCE.md`; dashboard reports provenance notes |
| PILOT-005 | P2 | Recommended `vbb-index.py search` workflow fails when local `.vbb/index/manifest.json` is absent | Resolved — search now auto-builds missing local index |
| PILOT-006 | P2 | Status/debt/count documents are stale against measured repo state | Resolved — active status/count docs refreshed; historical run artifacts preserved as history |
| SYNERGY-004 | P2 | setup.sh monolith (25K) | Mitigated (hardened, still long) |
| SYNERGY-005 | P3 | Governance duplication across files | Mitigated (RUN 14 links) |
| LANG-001 | P3 | 11 SKILL.md still have FR body content | Accepted — human-readable narrative remains bilingual; machine-facing contracts are EN-clean |
| LANG-002 | P3 | Prompts still contain FR narrative | Accepted — prompt layer is human-facing by design |
| REL-001 | P3 | No DEPLOYMENT.md or RUNBOOK.md | Resolved — both files exist and are indexed |

## Latest audit note — pilotage framework (2026-05-27)

New audit: [pilotage-framework-20260527-1905.md](audits/pilotage-framework-20260527-1905.md).

This audit was run against the local workspace date `2026-05-27`, which is earlier than several existing central artifacts dated `2026-06-10` through `2026-06-13`. It therefore treats the future-dated status files as evidence with a temporal provenance risk rather than as unquestioned current state.

## Historical risk register

Original triptyque (RUN 04A/04B/04C) identified 22 risks. After hardening:
- 7/12 SYNERGY risks resolved (R-001 R-002 R-003 R-006 R-007 R-010 R-012)
- 4/12 SYNERGY risks mitigated (S-004 setup.sh monolith, S-005 governance duplication, S-009 CI gaps, S-021 skill dir integrity)
- 1/12 SYNERGY risks accepted (S-008 residual FR in human-facing narrative)
- Current P2 count: 2 mitigated, 2 resolved through pilotage remediation, P3: 2 accepted
- P0: 0
- P1: 3 resolved (PILOT-001..003)

Full risk history: [audits/auto-audit-synthesis](../audits/auto-audit-synthesis.md), [global-evaluation-20260613](../audits/global-evaluation-20260613.md)

## Runtime dry-run explanation

| Status | Count | Explanation |
|--------|-------|------------- |
| PASS | 44 | Skill has no success gates, or stub output satisfies them |
| PARTIAL | 16 | Dry-run stubs don't produce skill-specific output (expected) |
| BLOCKED | 2 | scope-freeze gate chain (expected) |

All PARTIAL results are expected dry-run limitations from stub output and now
carry machine-readable partial reason metadata. All BLOCKED results are legitimate
gate dependencies. No actual defects.

## Update policy

- Any execution of an audit skill produces a timestamped report in `docs/audits/` and updates this file.
- Global verdict is recalculated after each audit cycle or by `3-vbb-risk-register`.
- This file is versioned. `docs/SESSION.md` stays local (gitignored).

## Instance note

This is the authentic instance of `AUDIT_STATUS.md` for the vibebackbone repo. A client project adopting vibebackbone gets a blank file generated by `t-vbb-project-context-init`, not a copy of this state.
