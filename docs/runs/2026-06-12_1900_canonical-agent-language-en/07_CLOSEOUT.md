# 07_CLOSEOUT — RUN 15 : Canonical Agent Language EN

**Date** : 2026-06-12  
**Route** : STRUCTURED  
**Verdict** : ✅ PASS

---

## Summary

Agent-facing layer translated from FR to EN across 10 files. Terminology canonically mapped (voie→route, RAPIDE→FAST, STRUCTURÉE→STRUCTURED, CLÔTURE→CLOSEOUT, etc.). Human-facing long docs (README, GUIDE, runs, audits) remain French.

### Files translated

| File | Before (lang) | After (lang) | Terminology |
|------|--------------|-------------|-------------|
| AGENTS.md | FR | EN | voie→route, RAPIDE→FAST, STRUCTURÉE→STRUCTURED, CLÔTURE→CLOSEOUT |
| SYSTEM.md | Mixed (core EN, header FR) | Full EN | 4 voies→4 routes |
| CLAUDE.md | FR | EN | voies→routes, counts updated (62/32) |
| docs/PILOTAGE.md | FR | EN | voie→route, all route names, escalade→escalation |
| docs/SESSION_RULES.md | FR | EN | voie→route, escalade→escalation, reprise→re-entry |
| docs/MEMORY_AND_HANDOFF.md | FR | EN | mémoire→memory, clôture→closeout, source de vérité→source of truth |
| prompts/t-p-vbb-phase-router.md | FR | EN | Version bump 2→3, all route names |
| prompts/0-p-vbb-zero-friction.md | FR | EN | Version bump 1→2, all route names |
| docs/router/ROUTER_MATRIX.md | FR | EN | Version bump 1→2, all route names + tables |
| docs/CONTEXT.md | FR | EN | All agent-facing terms |

### Files NOT translated (by design)

- README.md (human-facing FR)
- GUIDE.md (human-facing FR L3 reference)
- docs/runs/** (historical, FR)
- docs/audits/** (historical, FR)
- docs/AUDIT_STATUS.md (audit dashboard, mixed but largely stable)
- docs/ACTIVITY_LOG.md (operational log)

### Canonical terminology

| FR (legacy) | EN (canonical) |
|-------------|---------------|
| voie | route |
| RAPIDE-ZERO | FAST-ZERO |
| RAPIDE-MINIMAL | FAST-MINIMAL |
| RAPIDE / RAPIDE STANDARD | FAST / FAST-STANDARD |
| STRUCTURÉE | STRUCTURED |
| AUDIT | AUDIT |
| CLÔTURE | CLOSEOUT |
| artefact | artifact |
| mémoire | memory |
| contrat | contract |
| escalade / bascule | escalation |
| reprise | re-entry |
| clôture | closeout |
| source de vérité | source of truth |

### FR searchability preserved

Index still finds both languages: "fast zero" → current docs, "rapide zero" → historical runs/skills/GUIDE.

### Checks

| Check | Result |
|-------|--------|
| FR forbidden terms in translated files | ✅ 0 found |
| Internal links resolved | ✅ 24/24 |
| CI locale | ✅ 5/6 PASS (1 WARN closure) |
| Loop closure tests | ✅ 14/14 |
| Contract lint tests | ✅ 15/15 |
| Index tests | ✅ 7/7 |
| Portability tests | ✅ 6/6 |
| vbb-index search EN | ✅ "fast zero", "escalation rule", "source of truth" all found |
| vbb-index search FR | ✅ "rapide zero", "voie" still find historical docs |
| vbb-status-dashboard | ✅ Operational |

### Residual risks

1. **SKILL.md files inside skills/** are still FR — translating them is a separate, larger effort (62 files). Low priority; can be done per-skill during contractualisation.
2. **setup.sh** references FR strings in install messages — cosmetic, not agent-facing.
3. **CONTRACT.yaml files** use FR in description fields — acceptable (machine-validated keys are EN anyway).
4. **GUIDE.md** remains FR — by design, human-facing reference.

### Next action recommended
Resume contractualisation (RUN 09D+, 19 skills remaining) or further stabilization as needed.