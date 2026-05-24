---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-06-13
---

# CONTEXT.md — MOC / Persistent central router

> First file to read at startup. **This file points to — it does not duplicate.**

## Identity

- **Name** : vibebackbone
- **Mode** : [DISTRIBUTION](PROJECT_MODE.md#mode)
- **Purpose** : Distribution catalog of skills, prompts and governance for LLM agents
- **Governance** : [AGENTS.md](../AGENTS.md) · [SYSTEM.md](../SYSTEM.md) · [PILOTAGE.md](PILOTAGE.md)

## Active context

- **Route** : STRUCTURED
- **Phase** : v1.0 Hardening — complete
- **Version** : 1.0.0-rc.1
- **Contracts** : 62/62 (100%) — machine-facing EN-clean
- **SKILL.md EN** : 52/62 body-clean (10 remaining: Phase 4 UX/UI + spec-validator)
- **Tests** : 69/69 pytest green, CI 7/7 PASS, 0 warnings
- **Token economy** : L0 boot ~2.5K tokens (87% reduction from 19K)
- **Next action** : Tag v1.0.0 (awaiting explicit instruction)

## Risks / audits

- **Global verdict** : 🟡 PARTIAL → [AUDIT_STATUS.md](AUDIT_STATUS.md)
- **P0/P1** : 0 · **P2** : 2 (mitigated) · Detail: [AUDIT_STATUS.md](AUDIT_STATUS.md#risques-identifiés--status)

## Structural artifacts

| Dir | Content |
|-----|---------|
| `docs/` | Governance, runs, audits → [INDEX.md](INDEX.md) |
| `skills/` | 62 skills · 62 contracts (100%) → [skills/](../skills/) |
| `prompts/` | 32 prompts (7 canonical + 24 specialized + 1 router) → [prompts/](../prompts/) |

## Open points

1. 🟡 10 SKILL.md files with FR body (Phase 4 + spec-validator) — *low*
2. ⬜ DEPLOYMENT.md, RUNBOOK.md (post-v1.0) — *low*
3. ⬜ EN README/GUIDE for international adoption — *medium*

## Quick search

- `python tools/vbb-index.py search "query"` — text index
- `python tools/vbb-status-dashboard.py` — repo state
- `python tools/vbb-context-compactor.py docs/runs/<id>` — run summary

## Run history

Latest closed runs: 2026-06-13 (hardening ×4, global evaluation), 2026-06-12 (token-refactor ×3, canonical-en), 2026-06-11 (5 contractualisation/setup), 2026-06-10 (6 audit/ci/lot0). Closeouts: `docs/runs/*/07_CLOSEOUT.md`