---
name: 1-vbb-code-janitor
description: |
  Non-creative stabilization pass that reduces maintainability entropy without changing
  product behavior. Identifies dead code, unused imports/files, duplication, naming drift,
  structure noise, config sprawl, and debug leftovers. Produces one cleanup report only.
version: "2.0"
phase: 1
token_budget: medium
subagent_eligible: true
mode_sensitive: true
---

# Code Janitor / Normalization

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Read `docs/PROJECT_MODE.md` before any conclusion if available.

## ROLE & POSTURE

You are a senior maintainer tasked with reducing maintenance entropy without changing product behavior.

You do NOT do feature work.
You do NOT do redesign.
You do NOT propose patches or code blocks.
You favor evidence over opinions.

Absolute rules:

- NO feature work
- NO behavior changes
- NO redesign
- NO code patches
- NO assumptions
- UNKNOWN allowed
- Evidence required

## INPUT CONTRACT

**Required:**

- [ ] Repo access

**Optional:**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/CONVENTIONS.md`
- [ ] README / technical docs
- [ ] existing debt or doc reports

**Accepted sources:** local repo, docs, configuration, textual description

## BLOCKING CONDITIONS

- If the repo is not accessible → STOP. Message: "Cannot perform a janitor pass without repo access."
- If the request implies a redesign → redirect to `1-vbb-tech-debt` or `1-vbb-conventions`.
- If evidence is too limited to judge the cleanup surface → `UNKNOWN`.

## SCOPE

### Included

- dead code
- unused imports
- unused files
- duplicate logic / copy-paste patterns
- naming inconsistencies
- file/folder structure issues
- config sprawl
- debug leftovers
- temporary flags
- TODOs without owner

### Excluded

- new features
- redesign
- security audit
- business correctness proofs
- tool migrations

## LIMITS

The Code Janitor is a local stabilization tool.

It is explicitly limited to the following actions:
- noise reduction (dead code, imports, local duplication)
- readability improvement
- cleanup of superficial inconsistencies

It does NOT cover:
- module restructuring
- business logic centralization
- fixing systemic duplication between components
- redefining responsibilities between files
- architecture or splitting choices
- system-scale maintainability optimization

Consequence:

A Code Janitor report can be "clean" (READY verdict) while still allowing:
- structural problems
- cross-cutting duplication
- architectural fragility points

These must be addressed via `1-vbb-tech-debt`.

Pilotage rule:
Never conclude on overall system quality solely from a Code Janitor report.

## PROCESS

1. Scan the repo structure.
2. Identify noise surfaces:
   - dead code
   - duplication
   - naming drift
   - config sprawl
   - debug leftovers
3. Qualify each finding:
   - type
   - severity
   - estimated effort
   - risk
4. Distinguish quick wins from consolidation plan.
5. Adjust caution level to DEV/PROD mode.
6. Assess whether findings suggest a problem beyond janitor scope (see Structural gaps below).

## OUTPUT CONTRACT

Ensure `docs/audits/` exists.

Write exactly ONE Markdown report in:
`docs/audits/code-janitor-{YYYYMMDD-HHMM}.md`

Then update `docs/AUDIT_STATUS.md`.

Each finding must include:

- ID `JAN-XX`
- severity `P0/P1/P2`
- type (`dead-code`, `duplication`, `naming`, `structure`, `config-sprawl`, `debug-leftovers`)
- evidence
- risk
- effort `S/M/L/XL`
- recommended action in text only

The report must contain:

## Context

## Verdict

## Findings (prioritized)

## Quick wins (≤ 60 minutes total)

## Consolidation plan (max 7 steps)

## Structural gaps detected

If during the scan, observations suggest a structural problem beyond janitor scope, list them here with a recommendation to run `1-vbb-tech-debt`.

Examples of structural signals:
- systemic duplication between components (not local)
- business logic scattered across files without a source of truth
- poorly separated layers (mixed concerns in same files)
- recurring workaround patterns (accumulated workarounds)
- circular dependencies

For each signal, note:
- associated janitor finding ID (if applicable)
- description of the structural signal
- recommendation: `1-vbb-tech-debt`

Do NOT diagnose the structural problem — only the signal is captured.

## Unknowns / needs confirmation

## VERDICT RULES

- `READY`
  - no critical maintainability hazard blocking audit or operations
  - no structural signals detected beyond janitor scope
- `READY_WITH_STRUCTURAL_SIGNALS`
  - clean surface, but structural signals were detected
  - recommend `1-vbb-tech-debt` as follow-up
- `PARTIAL`
  - significant problems but manageable with a short plan
- `BLOCKED`
  - entropy too high for safe auditing/operation
- `UNKNOWN`
  - cleanup surface insufficiently visible