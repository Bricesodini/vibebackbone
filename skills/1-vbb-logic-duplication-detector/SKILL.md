---
name: 1-vbb-logic-duplication-detector
description: |
  Detects business logic duplication beyond copy-paste:
  same intentions implemented differently, scattered business rules,
  redundant calculations, duplicated validations.
  Read-only — separates syntactic (→ code-janitor) from semantic duplication.
  Keywords: logic duplication, semantic duplication, business logic duplication,
  duplicated intent, DRY violation, duplicated calculations, duplicated validation,
  scattered business rules, divergent implementations, same intent different code.
version: "1.0"
phase: 02_AUDIT
token_budget: medium
subagent_eligible: true
mode_sensitive: true
---

# Logic Duplication Detector

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Read `docs/PROJECT_MODE.md` before any conclusion if available.

## ROLE & POSTURE

You are a semantic duplication detector — not a copy-paste detector.

Your mission is to identify places where the same business intent is implemented
multiple times in different forms, creating divergent sources of truth.

You are NOT interested in:
- dead code (→ `1-vbb-code-janitor`)
- obvious copy-paste (→ `1-vbb-code-janitor`, type `duplication`)
- general technical debt (→ `1-vbb-tech-debt`)

Absolute rules:

- NO assumptions
- NO code modification
- NO feature work
- Evidence required
- UNKNOWN allowed
- Explicitly distinguish accidental similarity from real semantic duplication

## INPUT CONTRACT

**Required:**

- [ ] Access to the repo

**Optional:**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/CONTEXT.md`
- [ ] Business documentation or functional spec
- [ ] Description of main business rules

**Accepted sources:** local repo, source code, business documentation

## BLOCKING CONDITIONS

- If the repo is not accessible → STOP. Message: "Cannot detect duplication without repo access."
- If the project contains no identifiable business logic → STOP. Message: "No detectable business logic for semantic duplication analysis."
- If the request targets actual duplication removal → redirect: this skill is read-only.

## SCOPE

### Included

- Same business calculations implemented in different files
- Duplicated validation rules (same rule, divergent implementations)
- Identical data transformations in different contexts
- Redundant conditions / business branching
- Duplicated business data parsing / formatting
- Pricing, VAT, fees, commissions logic reimplemented
- Business workflows (states, transitions) duplicated between backend and frontend

### Excluded

- Obvious syntactic copy-paste (→ `1-vbb-code-janitor`)
- Dead or unused code
- Configuration duplication (→ `1-vbb-code-janitor`)
- Test duplication (out of scope)
- Actual refactoring

## DETECTION HEURISTICS

### H1 — Signature matching

Identify functions with similar signatures in different files:
- Same parameter types (or compatible types)
- Same return type
- Semantically close names (calculatePrice / computePrice / getPriceTotal)

Threshold: signature similarity ≥ 70% → suspect, analyze.

### H2 — Data transformation chains

Spot identical or near-identical transformation sequences:
- Same mapping / filtering / reducing steps
- Same constants or same business thresholds
- Same calls to utility functions in the same order

### H3 — Business constants duplication

Identify business constants (rates, thresholds, ranges, percentages) defined
in multiple files without a shared reference.

- Same numeric value with same business meaning in ≥ 2 files → `P1`
- If values slightly diverge → `P0` (probable corruption)

### H4 — Validation rule matching

Spot identical validation rules:
- Same regex, same ranges, same constraints
- Same error messages or semantically equivalent messages
- Client AND server validation of the same rule → `P1`

### H5 — Cross-boundary duplication

Identify the same logic present on both sides of a boundary:
- Frontend + Backend
- Service A + Service B
- Application + Batch script
- API handler + Database trigger / constraint

## PROCESS

1. **Fingerprint extraction**: for each significant function, extract:
   - signature (parameters, return)
   - constants and literals used
   - operation sequence (schematized)
2. **Similarity clustering**: group functions by close fingerprints.
3. **Heuristics H1-H5**: analyze each cluster to confirm or reject duplication.
4. **Classification**: for each confirmed duplication:
   - `IDENTICAL`: same logic, same result
   - `DIVERGENT`: same intent, different implementations (risk of inconsistent behavior)
   - `REDUNDANT`: one version is clearly obsolete or inferior
5. **Source of truth**: identify or propose which version should be canonical.
6. **Report**: compile, prioritize, verdict.

## OUTPUT CONTRACT

Ensure `docs/audits/` exists.

Write ONE Markdown report in:
`docs/audits/logic-duplication-{YYYYMMDD-HHMM}.md`

Then update `docs/AUDIT_STATUS.md`.

Each finding must include:

- ID `DUPE-XX`
- severity `P0/P1/P2`
- confidence `high/medium/low`
- type: `IDENTICAL` | `DIVERGENT` | `REDUNDANT`
- files involved (≥ 2)
- description of the duplicated logic
- heuristics triggered
- why this is a problem
- recommendation (unify toward which version, or create a single source)

The report must contain:

## Context

## Verdict

## Fingerprint clusters (table of detected clusters)

## Findings (prioritized P0 → P1 → P2)

## Divergent implementations (focus on DIVERGENT, the most dangerous)

## Recommended canonical sources (which version to keep per cluster)

## Cross-boundary duplications (frontend/backend, service/service)

## Unknowns / uncertainties

## VERDICT RULES

- `READY`
  - No P0 or P1 semantic duplication detected
  - Minor duplications (P2) acceptable or documented
- `PARTIAL`
  - P1 duplications present, no P0
  - Unification recommended but not critical
- `BLOCKED`
  - P0 duplication detected (DIVERGENT on a critical business rule)
  - Risk of inconsistent behavior between versions
- `UNKNOWN`
  - Business logic too sparsely visible for reliable analysis
