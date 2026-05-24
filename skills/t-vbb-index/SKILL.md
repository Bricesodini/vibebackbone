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

## TOOL

```bash
python tools/vbb-index.py build              # build index
python tools/vbb-index.py search "fast"      # search
python tools/vbb-index.py search "..." --json # JSON output
python tools/vbb-index.py stats              # stats
```

## AGENTIC RULE

Before scanning long docs, use `tools/vbb-index.py search` when available.
Fallback to `docs/CONTEXT.md` if index is absent.