---
date: 2026-07-14
scope: prompts/**/*.md
skill: 1-vbb-formatter
verdict: READY
---

# Prompt language enforcement audit

## Context

`docs/CONVENTIONS.md` requires English for prompts and agent-actionable
artifacts. The current catalog contains 33 Markdown prompts. A deterministic
French-marker inventory identifies 18 affected files and 15 already-English
files. The seven canonical prompts are affected.

## Verdict

**READY for a bounded migration.** The convention is unambiguous and no new
policy is required. Translation must preserve machine tokens, paths, phase
names, verdict enums, artifact names, links and behavioral thresholds.

## Convention → Enforcement map

| Convention | Current evidence | Enforcement |
|---|---|---|
| Prompts are English-only | 18/33 contain French prose markers | Translate only affected files |
| Machine-facing tokens remain stable | Commands, paths, links, route/verdict enums | Compare before/after executable-token and destination inventories; translate human placeholders |
| One canonical behavior | Prompt responsibility matrix | No file moves, merges or routing changes |
| Four distributions inherit Core | Shared `prompts/` catalog | Record Core propagation; no adapter fork |

## Findings (prioritized)

### FL-01 — P1 — inconsistent-rules

- **Evidence**: French prose is present in 18 prompts, including all seven
  canonical phase prompts.
- **Risk**: agent language depends on entrypoint and conflicts with the active
  English-only convention.
- **Effort**: L.
- **Recommendation**: translate the 19 affected files in two non-overlapping
  batches, then review the combined diff against stable machine tokens.

### FL-02 — P2 — ci-gap

- **Evidence**: no current automated check detects a return of French prose in
  prompt instructions.
- **Risk**: future edits can silently reintroduce the same drift.
- **Effort**: S.
- **Recommendation**: add a deterministic regression test over prompt prose
  using a conservative French-marker vocabulary and explicit machine-token
  exclusions; reject only unambiguous markers.

## Activation plan (phased)

1. Inventory the 33 files and freeze structural token/link baselines.
2. Translate the 18 affected files without renaming or moving them.
3. Review canonical and specialized batches separately, including embedded
   human-readable output templates.
4. Add a conservative language-regression test.
5. Compare machine tokens, links, files and routing aliases before/after.
6. Run prompt inventory checks, full tests and P.R2.

## CI / Pre-commit / Editor alignment

The regression test belongs in the existing pytest/local/remote CI path. No new
dependency or editor integration is necessary.

## Exceptions policy

Canonical route/status enums, file names, proper nouns and quoted historical
examples may remain unchanged. An exception must not permit French instructional
prose.

## Unknowns / needs confirmation

None. Brice explicitly requested the English migration on 2026-07-14.

```yaml
FINAL_STATUS:
  verdict: COMPLETE
  findings: [FL-01, FL-02]
  affected_prompts: 18
  total_prompts: 33
```
