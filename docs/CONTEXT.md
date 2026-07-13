---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-06-02
temporal_provenance: TEMPORAL_PROVENANCE.md
---

# CONTEXT.md — MOC / Persistent central router

> First file to read at startup. **This file points to — it does not duplicate.**

## Identity

- **Name** : vibebackbone
- **Mode** : [DISTRIBUTION](PROJECT_MODE.md#mode)
- **Purpose** : Distribution catalog of skills, prompts and governance for LLM agents
- **Governance** : [AGENTS.md](../AGENTS.md) · [SYSTEM.md](../SYSTEM.md) · [PILOTAGE.md](PILOTAGE.md)
- **MVP start** : new MVP/from-zero work must pass [MVP_START_PROTOCOL.md](MVP_START_PROTOCOL.md) before implementation

## Active context

- **Route** : STRUCTURED
- **Phase** : v1.0 Hardening — complete
- **Version** : 1.0.0-rc.1
- **Contracts** : 64/64 (100%) — machine-facing EN-clean, contract lint 0 errors
- **Quality conventions**: 5 pillars canonical in [CONVENTIONS.md](CONVENTIONS.md) v1.1 (Readability, Modularity, Coherence, Traçabilité, Robustness P.R1–P.R8)
- **SKILL.md EN** : partial — see [AUDIT_STATUS.md](AUDIT_STATUS.md#risks-identified--status)
- **Architecture** : structured source active → [ARCHITECTURE.md](ARCHITECTURE.md) · projection [RELATIONS.md](RELATIONS.md)
- **Front pipeline**: propagation-first routing active (ADR-0002 + ADR-0003)
  - ENGINE_ONLY mode for UI/UX requests
  - GRAPHIC_PROPAGATION_MAP mandatory in Pass 1 (step 0bis before SURFACE_CARTOGRAPHY)
  - Pass 4→5 gate: 7 keys required (3 from Pass 1, 4 from Pass 4)
  - HARD BLOCK: GENERIC_DESIGN_SYSTEM_RESPONSE before propagation map
- **Centralization audit** : pass 4 produces `TOKEN_DEFINITION_MAP` + `CENTRALIZATION_ROADMAP`
- **Tests** : 142 passed, 3 skipped (145 collected) — see [AUDIT_STATUS.md](AUDIT_STATUS.md)
- **Token economy** : L0 boot ~2.5K tokens (87% reduction from 19K)
- **Next action** : accumulate comparable subagent runs before any canonisation; explicit gate-link enforcement remains a bounded P2 decision
- **Key decisions** : [ADR-0002](docs/adr/0002-surface-first-routing-ui-ux.md) — surface-first routing + centralization audit

## Risks / audits

- **Global verdict** : 🟡 PARTIAL → [AUDIT_STATUS.md](AUDIT_STATUS.md)
- **Latest methodology audit** : [POC + subagents (2026-07-13)](audits/systemic-poc-subagents-methodology-20260713-1551.md) — recommendation advisory accepted; `SYS-POC-001` remediation READY
- **POC/subagents P0/P1** : `SYS-POC-001` resolved; `SYS-POC-002` and `SYS-SUB-001` mitigated · Detail: [AUDIT_STATUS.md](AUDIT_STATUS.md)

## Structural artifacts

| Dir | Content |
|-----|---------|
| `docs/` | Governance, runs, audits → [INDEX.md](INDEX.md) |
| `docs/ARCHITECTURE.md` | Canonical structured architecture source |
| `docs/RELATIONS.md` | Generated architecture projection |
| `docs/CONVENTIONS.md` | Quality conventions (5 pillars, v1.1) |
| `docs/TECH_DEBT.md` | Lightweight source-based technical debt register |
| `skills/` | 64 skills · 64 contracts (100%) → [skills/](../skills/) |
| `prompts/` | 33 prompts (7 canonical + 25 specialized + 1 router) → [prompts/](../prompts/) |

## Open points

1. 🟡 Residual FR in agent-facing assets — *low*
2. 🟡 Temporal skew acknowledged in [TEMPORAL_PROVENANCE.md](TEMPORAL_PROVENANCE.md) — *low*
3. ⬜ EN README/GUIDE for international adoption — *medium*
4. ✅ Deep framework remediation implemented — `docs/runs/2026-06-02_1220_deep-framework-remediation/`
5. 🟡 Quality audit gaps (AI governance skill, migration policy) — *high*
6. ✅ OPS-001/002/003 CLOSED — robustness findings resolved (2026-05-28 + 2026-05-29)
7. ✅ Documentation foundation pass — `AGENTS.md` compacted, stale 0641 audit archived, active findings extracted (2026-06-02)
8. ✅ LLM load surface pass — installed Codex AGENTS repaired, historical root docs archived, large skill hotspots mapped (2026-06-02)
9. 🔴 Quality organization audit — Core/Distribution boundary, Hermes proxy migration, loop closure, and dashboard risk visibility require remediation (2026-06-02)

## Key decisions

2. [ADR-0003](docs/adr/0003-graphic-propagation-map.md) — GRAPHIC_PROPAGATION_MAP: Propagation Architecture First (2026-05-28)

## Quick search

Latest closed runs: 2026-06-13 (hardening ×4, global evaluation), 2026-06-12 (token-refactor ×3, canonical-en), 2026-06-11 (5 contractualisation/setup), 2026-06-10 (6 audit/ci/lot0). Closeouts: `docs/runs/*/07_CLOSEOUT.md`
