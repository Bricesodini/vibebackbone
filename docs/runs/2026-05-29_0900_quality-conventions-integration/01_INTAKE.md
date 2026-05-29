# 01_INTAKE — Quality Conventions Integration

**Date**: 2026-05-29
**Route**: STRUCTURED
**Run**: 2026-05-29_0900_quality-conventions-integration

## Task

Following the quality audit completed on 2026-05-29, integrate the defined quality work into Vibebackbone without creating `docs/QUALITY_MODEL.md` prematurely.

## Objective

Create or enrich a canonical quality conventions foundation around three pillars:
1. **Readability** — naming, function size, comments
2. **Modularity** — domain orientation, single responsibility, UI isolation
3. **Coherence & Convergence** — one active canonical way, no permanent competing logic

## Deliverables

| # | File | Action |
|---|------|--------|
| 1 | `docs/CONVENTIONS.md` | Create (canonical source) |
| 2 | `docs/templates/CANON_CHANGE_PROPOSAL.md.template` | Create (EN template) |
| 3 | `docs/ARCHITECTURE.md` | Update (add conventions block) |
| 4 | `docs/RELATIONS.md` | Regenerate via `vbb-architecture.py graph --write` |
| 5 | `docs/INDEX.md` | Update (reference CONVENTIONS.md) |
| 6 | `AGENTS.md` | Update (add quality convention rule) |
| 7 | `SYSTEM.md` | Update (add quality convention rule) |
| 8 | `docs/PILOTAGE.md` | Update (add quality convention rule) |
| 9 | `docs/runs/YYYY-MM-DD_*/07_CLOSEOUT.md` | Create closeout |

## Language rule

- All new prompts and skills → **English only**
- Governance docs → may stay consistent with existing repo language
- Agent-actionable artifacts → **English mandatory**

## Verification loop (mandatory before declaring complete)

```bash
python tools/vbb-architecture.py lint
python tools/vbb-architecture.py graph --write
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py
pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

All commands must pass before verdict `IMPLEMENTED_AND_VERIFIED` is allowed.

## Blockers

- Do not create `docs/QUALITY_MODEL.md`
- Do not declare gaps corrected without verification
- Do not modify canon without trace
- Do not add competing logic without migration plan
- Do not edit `docs/RELATIONS.md` manually
- Do not write new skills/prompts in French

## Escalation triggers

- Any lint failure → stop, fix, re-run loop
- Any test failure → stop, fix, re-run loop
- Architecture lint failure → blocked until reference fixed

## Handoff

→ Continue to 05_EXECUTION.md