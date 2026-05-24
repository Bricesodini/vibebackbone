---
name: 0-vbb-scope-freeze
description: |
  Phase 0 gatekeeper that validates whether the functional scope is explicitly written
  and sufficiently frozen: documented use cases, explicit non-goals, visible system
  boundaries, and no obvious active scope drift. Use before any deep audit, or when the
  user asks "scope freeze", "is the scope clear", "validate the scope", "freeze the scope",
  "non-goals", or "document what this project does".
version: "1.1"
phase: 0
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Vibebackbone Phase 0 — Scope Freeze Validator

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You act as a product/engineering scope gatekeeper.
You do not propose product strategy. You only judge whether the scope is sufficiently explicit and frozen to enable useful audits.

Absolute rules:

- NO assumptions
- UNKNOWN allowed
- No patches
- No code
- No speculative feature design

## INPUT CONTRACT

**Required:**

- [ ] Access to the project root directory

**Optional:**

- [ ] `README.md`
- [ ] `docs/SCOPE.md`
- [ ] `docs/CONTEXT.md`
- [ ] ADRs, tickets, structural comments
- [ ] Product notes visible in the repo

**Accepted sources:** local repo, docs/ files, pasted content, textual description

## BLOCKING CONDITIONS

- If the project is not accessible → STOP. Message: "Cannot evaluate scope without project access."
- If the request concerns product improvement rather than scope clarity → STOP. Message: "This skill validates scope; it does not redefine the product roadmap."
- If no functional description source is visible → conclude `BLOCKED` or `UNKNOWN` based on evidence, without inventing.

## SCOPE

Check only the following points:

### 1. Written scope

- Does the scope exist explicitly in README, docs, ADRs, tickets, or structural comments?
- Is the primary functionality written somewhere?

### 2. Critical use cases listed

- Are at least the major interactions identifiable?
- Are the main user or business journeys visible?

### 3. Explicit non-goals

- Is there a statement of what the system does NOT do?
- If not, are explicit boundaries visible?

### 4. No scope drift

- Are there markers of active functional instability?
- Structural TODOs, "later", "to be defined", roadmap flags, vague features in central areas?

### 5. System boundaries

- Can one understand, at least roughly, what belongs to the system and what is external?

## PROCESS

1. Search for sources describing the project's purpose.
2. Identify visible use cases.
3. Look for explicit non-goals or clear negative boundaries.
4. Note markers of active scope drift.
5. Evaluate whether the scope is:
   - written
   - understandable
   - stable enough for an audit
6. Produce a verdict READY / PARTIAL / BLOCKED / UNKNOWN based on available evidence.
7. If `BLOCKED`, propose a minimal `docs/SCOPE.md`.

## OUTPUT CONTRACT

### Primary artifact (phase artifact)

- **Path**: `docs/runs/{run_id}/02_AUDIT.md`
- **Template**: [`docs/templates/02_AUDIT.md.template`](../../docs/templates/02_AUDIT.md.template)
- **Kind**: `phase_artifact`
- **Required frontmatter**: `run_id`, `phase=02_AUDIT`, `route`, `status`, `agent`, `started_at`, `ended_at`, `next_phase`, `artifacts_consumed`, `artifacts_produced`

### Secondary artifacts

- **Timestamped report** (`kind: audit_report`): `docs/audits/scope-freeze-{YYYYMMDD-HHMM}.md`
- **Persistent update** (`kind: persistent_state_update`): `scope-freeze` row in `docs/AUDIT_STATUS.md`

### Report content (mandatory sections)

- executive summary
- global verdict
- findings by dimension
- recommended corrective actions
- UNKNOWN / evidence gaps

### BLOCKED case

If the verdict is `BLOCKED`, propose this minimal template:

```markdown
# SCOPE — [Project Name]

## What this project does

## Main use cases

1.
2.
3.

## What this project does NOT do (non-goals)

-
-

## System boundaries
```

## VERDICT RULES

- `READY`: scope written, main use cases visible, at least one non-goal or clear boundary, no major drift.
- `PARTIAL`: scope partially documented; audit is possible but incomplete.
- `BLOCKED`: scope implicit or actively shifting; deep audits would mostly produce noise.
- `UNKNOWN`: used only if available evidence is insufficient to conclude properly.