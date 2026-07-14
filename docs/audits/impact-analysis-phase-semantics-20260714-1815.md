---
date: 2026-07-14
skill: t-vbb-impact-analyzer
change: PATT-02 phase semantics reconciliation
classification: NON_BREAKING
verdict: READY
---

# Impact analysis — skill and contract phase semantics

## Change analyzed

Complete the canonical `SKILL.md phase: 02_AUDIT` migration for the 16
`1-vbb-*` skills while retaining `CONTRACT.yaml routing.phase_scope: phase_1`
as the phase router's catalog-tier API. Add an enforcing cross-surface lint.

## Direct impact

- Eleven `skills/1-vbb-*/SKILL.md` frontmatters change from deprecated `1` to
  canonical `02_AUDIT`; five are already canonical.
- `docs/PHASE_TO_SKILLS.md` and `0-vbb-standard` clarify that frontmatter phase
  and contract routing scope are distinct namespaces.
- `vbb-contract-lint.py` validates the 16 Phase-1 pairs; controlled tests cover
  both wrong frontmatter and wrong contract scope.

## Indirect impact

- The catalog becomes internally enforceable rather than relying on human
  comparison.
- Existing phase router calls using `phase_1` remain valid and unchanged.
- Future `1-vbb-*` skills cannot silently reintroduce deprecated frontmatter.

## External impact

Pi, OpenCode, Codex and Claude Code inherit the same Core skill metadata and
linter. No adapter, alias, setup path, installed state or provider API changes.

## Classification

**NON_BREAKING.** The only runtime-consumed value, contract `phase_1`, is
preserved. The modified skill frontmatter follows the already published canon.

## UNKNOWN areas

No external consumer of raw `SKILL.md phase: 1` is declared. If an undeclared
consumer exists, it would observe the intended canonical migration.

```yaml
FINAL_STATUS:
  verdict: COMPLETE
  classification: NON_BREAKING
  risks: []
  open_points: []
```
