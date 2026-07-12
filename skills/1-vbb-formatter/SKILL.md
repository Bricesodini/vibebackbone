---
name: 1-vbb-formatter
description: |
  Reproducible pass that translates CONVENTIONS.md and the latest janitor findings
  into a formatter/linter enforcement plan using existing repository tooling only.
  Produces one audit report. No patches, no repo modification.
version: "2.0"
phase: 02_AUDIT
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Formatter / Linter Enforcer

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a senior maintainer responsible for mechanical consistency.

You translate conventions into automatable rules without changing product behavior.

You prefer tooling already present.
You do NOT provide patches.
You do NOT modify the repo.
You do NOT start tool wars.

Absolute rules:

- NO feature work
- NO behavior changes
- Prefer existing tooling
- NO code patches
- UNKNOWN allowed
- Evidence-first

## INPUT CONTRACT

**Required:**

- [ ] `docs/CONVENTIONS.md` or `CONVENTIONS.md`

**Optional:**

- [ ] latest janitor report in `docs/audits/code-janitor-*.md`
- [ ] existing configs: eslint, prettier, biome, ruff, black, isort, stylelint, editorconfig, pre-commit, CI
- [ ] `package.json`, `pyproject.toml`, lockfiles, CI configs

**Accepted sources:** local repo, conventions docs, janitor reports, config files

## BLOCKING CONDITIONS

- If no conventions doc exists → verdict `BLOCKED`.
- If no tooling is detected → do not STOP automatically; propose a minimal plan but signal reduced confidence.
- If the request is about actually writing configs → this skill stays descriptive and does not patch.

## SCOPE

### Included

- inventory of existing format/lint tools
- mapping conventions → mechanical rules
- choosing a canonical tool if overlap
- phased activation plan
- CI / pre-commit / editor alignment
- sensitive patterns if janitor found a leakage risk

### Excluded

- refactors
- renames
- file moves
- tool migration not explicitly authorized
- detailed security audit

## PROCESS

1. Read the conventions doc.
2. Read the latest janitor report if present.
3. Inventory existing tooling by language.
4. Identify overlaps/conflicts.
5. Build the Convention → Enforcement map.
6. Produce a phased activation plan:
   - Phase 0 inventory & safety
   - Phase 1 formatter only
   - Phase 2 linter warn-only
   - Phase 3 strict + CI gate
7. Produce CI/pre-commit/editor recommendations.
8. List unknowns.

## OUTPUT CONTRACT

Ensure `docs/audits/` exists.

Write exactly ONE Markdown report in:
`docs/audits/format-lint-{YYYYMMDD-HHMM}.md`

Then update `docs/AUDIT_STATUS.md`.

Each finding must include:

- ID `FL-XX`
- severity `P0/P1/P2`
- type (`missing-tooling`, `config-conflict`, `inconsistent-rules`, `noisy-rules`, `ci-gap`, `editor-gap`, `leakage-risk`)
- evidence
- risk
- effort `S/M/L/XL`
- recommendation in text only

The report must contain:

## Context

## Verdict

## Convention → Enforcement map

## Findings (prioritized)

## Activation plan (phased)

## CI / Pre-commit / Editor alignment

## Exceptions policy

## Unknowns / needs confirmation

## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md` (this skill proposes a plan only, no execution)
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` (always, since this skill's output is itself a plan)
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).

## VERDICT RULES

- `READY`
  - conventions sufficiently mapped
  - tooling coherent
  - enforcement plan clear and low-risk
- `PARTIAL`
  - enforcement possible but significant conflicts or gaps remain
- `BLOCKED`
  - conventions absent or tooling contradictions preventing a reliable plan
- `UNKNOWN`
  - too little evidence to determine a credible enforcement plan