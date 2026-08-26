---
run_id: "2026-08-26_local-agents-a2-remediation"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-08-26T00:00:00+02:00"
ended_at: "2026-08-26T00:00:00+02:00"
next_phase: "06_A2_INDEPENDENT_REVIEW"
artifacts_consumed: ["04_PLAN.md"]
artifacts_produced: ["05_EXECUTION.md"]
---

# 05_EXECUTION — local-agents-a2-remediation

## Résumé

The resolver now decides the effective-Git-root boundary before content is
read. The selected `AGENTS.md` entry retains its own Git provenance, while the
resolved target is exposed separately.

## Actions effectuées

| # | Action | Statut | Validation |
|---|---|---|---|
| 1 | Move boundary check before `read_text` | `DONE` | invalid UTF-8 external symlink test |
| 2 | Separate selected and resolved contract paths | `DONE` | untracked entry to tracked target test |
| 3 | Update protocol wording | `DONE` | targeted documentation assertions |

## Tests / validations passées

- `python -m pytest tests/test_local_agents_bootstrap.py -q` — `8 passed`.
- `python -m ruff check tools/vbb-local-agents.py tests/test_local_agents_bootstrap.py` — PASS.
- `python -m ruff format --check tools/vbb-local-agents.py tests/test_local_agents_bootstrap.py` — PASS.

## Fichiers modifiés

```
tools/vbb-local-agents.py
tests/test_local_agents_bootstrap.py
docs/LOCAL_AGENT_CONTRACTS.md
docs/runs/2026-08-26_local-agents-a2-remediation/
```
