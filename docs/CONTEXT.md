---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-05-29
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
- **Quality conventions**: canonical source in [CONVENTIONS.md](CONVENTIONS.md) (readability, modularity, coherence) · change process via [CANON_CHANGE_PROPOSAL template](templates/CANON_CHANGE_PROPOSAL.md.template)
- **SKILL.md EN** : partial — see [AUDIT_STATUS.md](AUDIT_STATUS.md#risks-identified--status)
- **Architecture** : structured source active → [ARCHITECTURE.md](ARCHITECTURE.md) · projection [RELATIONS.md](RELATIONS.md)
- **Front pipeline**: propagation-first routing active (ADR-0002 + ADR-0003)
  - ENGINE_ONLY mode for UI/UX requests
  - GRAPHIC_PROPAGATION_MAP mandatory in Pass 1 (step 0bis before SURFACE_CARTOGRAPHY)
  - Pass 4→5 gate: 7 keys required (3 from Pass 1, 4 from Pass 4)
  - HARD BLOCK: GENERIC_DESIGN_SYSTEM_RESPONSE before propagation map
- **Centralization audit** : pass 4 produces `TOKEN_DEFINITION_MAP` + `CENTRALIZATION_ROADMAP`
- **Tests** : 81/81 pytest green, CI PASS, contract lint 0 errors, architecture lint 0 errors
- **Token economy** : L0 boot ~2.5K tokens (87% reduction from 19K)
- **Next action** : Test front pipeline propagation-first behavior in real conditions
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
| `docs/CONVENTIONS.md` | Quality conventions (readability, modularity, coherence) |
| `docs/TECH_DEBT.md` | Lightweight source-based technical debt register |
| `skills/` | 64 skills · 63 contracts (98%) → [skills/](../skills/) |
| `prompts/` | 33 prompts (7 canonical + 25 specialized + 1 router) → [prompts/](../prompts/) |

## Open points

1. 🟡 Residual FR in agent-facing assets — *low*
2. 🟡 Temporal skew acknowledged in [TEMPORAL_PROVENANCE.md](TEMPORAL_PROVENANCE.md) — *low*
3. ⬜ EN README/GUIDE for international adoption — *medium*
4. ⬜ Implementation-readiness stabilization before reuse — *high*
5. 🟡 Quality audit gaps (OPS-001/002, AI governance skill, migration policy) — *high*

## Key decisions

2. [ADR-0003](docs/adr/0003-graphic-propagation-map.md) — GRAPHIC_PROPAGATION_MAP: Propagation Architecture First (2026-05-28)

## Quick search

Latest closed runs: 2026-06-13 (hardening ×4, global evaluation), 2026-06-12 (token-refactor ×3, canonical-en), 2026-06-11 (5 contractualisation/setup), 2026-06-10 (6 audit/ci/lot0). Closeouts: `docs/runs/*/07_CLOSEOUT.md`
