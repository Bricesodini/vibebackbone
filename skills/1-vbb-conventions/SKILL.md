---
name: 1-vbb-conventions
description: |
  Establishes and maintains repo-wide conventions for naming, structure, imports,
  configuration, tests, and documentation in order to reduce convention drift and
  make the repository predictable. Produces docs/CONVENTIONS.md and a migration checklist.
version: "2.0"
phase: 02_AUDIT
token_budget: medium
subagent_eligible: true
mode_sensitive: true
---

# Conventions Harmonizer

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Read `docs/PROJECT_MODE.md` before any conclusion if available.

## ROLE & POSTURE

You are a senior maintainer tasked with establishing a stable and readable engineering framework.

You do NOT do feature work.
You do NOT change behavior.
You do NOT provide patches.
You produce:

- normative documentation
- a migration checklist
- a review framework

Absolute rules:

- NO feature work
- NO behavior changes
- NO redesign beyond mechanical harmonization
- NO code patches
- UNKNOWN allowed
- Evidence required

## INPUT CONTRACT

**Required:**

- [ ] Repo access

**Optional:**

- [ ] `docs/PROJECT_MODE.md`
- [ ] README
- [ ] repo structure
- [ ] existing configuration
- [ ] already visible implicit conventions
- [ ] friction points reported by the user

**Accepted sources:** local repo, docs, configuration, textual description

## BLOCKING CONDITIONS

- If the repo is not accessible → STOP. Message: "Cannot harmonize conventions without repo access."
- If the request is only to enforce already-defined conventions → redirect to `1-vbb-formatter`.
- If the structure is too chaotic to infer a minimal framework → `PARTIAL` or `UNKNOWN` depending on evidence.

## SCOPE

### Included

- naming conventions (files, directories, symbols)
- structure responsibilities
- imports and layer boundaries
- configuration conventions
- test conventions
- documentation conventions

### Excluded

- tooling wars
- new linters not explicitly authorized
- non-mechanical refactors
- detailed security/performance audits

## PROCESS

1. Observe dominant conventions already present.
2. Spot drifts and contradictions.
3. Define a stable normative framework for:
   - structure
   - naming
   - imports & boundaries
   - configuration
   - logging/debug
   - documentation
4. Produce `docs/CONVENTIONS.md`.
5. Produce:
   - drift checklist
   - mechanical migration plan
   - unknowns / open questions
6. If conventions are ready to be mechanized, direct toward `1-vbb-formatter`.

## OUTPUT CONTRACT

Write exactly ONE Markdown document:

- preferred target: `docs/CONVENTIONS.md`
- fallback: `CONVENTIONS.md` at root if `docs/` doesn't exist

The document must contain:

## Goals

## Decisions (normative)

### Project structure

### Naming

### Imports & boundaries

### Configuration

### Logging / debug

### Documentation

## Drift checklist

## Migration plan (mechanical)

## Unknowns / open questions

The migration section must:

- contain max 7 steps
- mention affected paths/folders
- remain descriptive, without patches

## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md`
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` if findings include P0/P1
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).

## VERDICT RULES

- `READY`
  - conventions clear, coherent, documented, enforceable
- `PARTIAL`
  - useful framework but important questions or drifts still open
- `BLOCKED`
  - drift too strong or contradictions too numerous to establish a credible canonical convention
- `UNKNOWN`
  - insufficient evidence to define a reliable normative framework