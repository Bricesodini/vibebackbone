---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-05-28
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
- **Contracts** : 63/63 (100%) — machine-facing EN-clean
- **SKILL.md EN** : partial — see [AUDIT_STATUS.md](AUDIT_STATUS.md#risks-identified--status)
- **Architecture** : structured source active → [ARCHITECTURE.md](ARCHITECTURE.md) · projection [RELATIONS.md](RELATIONS.md)
- **Front pipeline** : surface-first routing active (ADR-0002) → ENGINE_ONLY mode for UI/UX requests
- **Centralization audit** : pass 4 produces `TOKEN_DEFINITION_MAP` + `CENTRALIZATION_ROADMAP`
- **Tests** : 80/80 pytest green, CI 8/8 PASS, 0 warnings
- **Token economy** : L0 boot ~2.5K tokens (87% reduction from 19K)
- **Next action** : Test surface-first routing in real conditions → verify orchestrator detects UI/UX triggers correctly
- **Key decisions** : [ADR-0002](docs/adr/0002-surface-first-routing-ui-ux.md) — surface-first routing + centralization audit

## Risks / audits

- **Global verdict** : 🟡 PARTIAL → [AUDIT_STATUS.md](AUDIT_STATUS.md)
- **P0/P1** : 0 open, 1 mitigating P1 · **P2** : 0 open, 2 historical mitigated · Detail: [AUDIT_STATUS.md](AUDIT_STATUS.md#risks-identified--status)

## Structural artifacts

| Dir | Content |
|-----|---------|
| `docs/` | Governance, runs, audits → [INDEX.md](INDEX.md) |
| `docs/ARCHITECTURE.md` | Canonical structured architecture source |
| `docs/RELATIONS.md` | Generated architecture projection |
| `docs/TECH_DEBT.md` | Lightweight source-based technical debt register |
| `skills/` | 63 skills · 63 contracts (100%) → [skills/](../skills/) |
| `prompts/` | 33 prompts (7 canonical + 25 specialized + 1 router) → [prompts/](../prompts/) |

## Open points

1. 🟡 Residual FR in agent-facing assets — *low*
2. 🟡 Temporal skew acknowledged in [TEMPORAL_PROVENANCE.md](TEMPORAL_PROVENANCE.md) — *low*
3. ⬜ EN README/GUIDE for international adoption — *medium*
4. ⬜ Implementation-readiness stabilization before reuse — *high*

## Key decisions

1. [ADR-0002](docs/adr/0002-surface-first-routing-ui-ux.md) — surface-first routing + centralization audit (2026-05-28)

## Quick search

Latest closed runs: 2026-06-13 (hardening ×4, global evaluation), 2026-06-12 (token-refactor ×3, canonical-en), 2026-06-11 (5 contractualisation/setup), 2026-06-10 (6 audit/ci/lot0). Closeouts: `docs/runs/*/07_CLOSEOUT.md`
