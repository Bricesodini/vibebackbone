---
audit_id: "impact-analysis-skill-english-migration-20260714-2145"
skill: "t-vbb-impact-analyzer"
status: "READY"
classification: "NON_BREAKING"
date: "2026-07-14"
---

# Impact analysis — Skill English migration

## Change analyzed

Translate remaining active French prose in five skills and extend the existing
conservative prompt-language guard to all 64 skills.

## Direct impact

Five `SKILL.md` files and `tests/test_prompt_language.py`.

## Indirect impact

Agent instructions become language-consistent. IDs, paths, commands, verdicts,
contract routing triggers and output requirements remain stable.

## External impact

All four distributions inherit the English Core catalog. No adapter, setup path
or installed runtime state changes in this repository.

## Final classification

**NON_BREAKING.** The change translates prose in place and preserves structural
and machine-facing contracts.

## UNKNOWN areas

No invocation telemetry measures multilingual trigger recall. Reopen only on a
demonstrated routing miss.

```yaml
FINAL_STATUS:
  verdict: READY
  tests_run:
    - "conservative French marker inventory"
  tests_missing: []
  risks: []
  open_points: []
```
