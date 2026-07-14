---
name: t-vbb-index
description: |
  Local text index for fast information retrieval across the Vibebackbone
  repo. No vector DB, no embeddings, no external dependencies. Searches
  docs, skills, contracts, prompts, and run artifacts. Keywords: index,
  search, find, lookup, retrieval, text search.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# VBB Index

Read `skills/vibebackbone/docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a local search index.

Your role is to accelerate access to information without loading all documentation.

## INPUT CONTRACT

Required: a search query. Optional: repository path and JSON output mode.

## BLOCKING CONDITIONS

Stop only when the repository is unreadable. A missing index is recoverable by
building it or falling back to canonical context.

## SCOPE

Local text indexing and retrieval only; no semantic inference, embeddings,
external service, or source modification.

## PROCESS

```bash
python tools/vbb-index.py build              # build index
python tools/vbb-index.py search "fast"      # search
python tools/vbb-index.py search "..." --json # JSON output
python tools/vbb-index.py stats              # stats
```

## AGENTIC RULE

Before scanning long docs, use `tools/vbb-index.py search` when available.
Fallback to `docs/CONTEXT.md` if index is absent.

## OUTPUT CONTRACT

Return status, bounded search results, summary and next action. Index builds may
update `.vbb/index/manifest.json`.

## VERDICT RULES

- `PASS`: query completed with bounded results, including an empty result set.
- `PARTIAL`: fallback search used or index evidence is incomplete.
- `BLOCKED`: repository content cannot be read.
