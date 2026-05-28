---
name: 4-vbb-front-pipeline-reference
description: |
  Canonical reference for the 7-pass Vibebackbone front pipeline. Defines execution modes,
  subsystem boundaries (ENGINE vs VISUAL), gate conditions, scope locks, and rollback protocol.
  This is a decision and protocol reference, not an execution pass.
version: "2.3"
phase: 4
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Front Pipeline Reference

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a pipeline reference.
You must NOT execute the pipeline in place of passes.
You define:

- execution modes
- subsystems
- gates
- scope locks
- rollback protocol

**ENGINE_ONLY trigger rule:**
Any UI/UX, visual architecture, graphic coherence, or design centralization request
must enter `ENGINE_ONLY`.
VISUAL_ONLY or FULL_RELEASE mode is only allowed after validation
of `SURFACE_CARTOGRAPHY` via pass 1.

## INPUT CONTRACT

**Required:**

- [ ] A request related to Vibebackbone front pipeline

**Optional:**

- [ ] current pass state
- [ ] already produced artifacts
- [ ] need for ENGINE / VISUAL / FULL_RELEASE clarification

## BLOCKING CONDITIONS

- If request is not about front pipeline → STOP. Message: "This resource documents only the Vibebackbone front pipeline."
- If no execution mode is provided during pipeline start → STOP and explicitly request the mode.

## SCOPE

### Subsystems

- ENGINE: passes 1-4
- VISUAL: passes 5-7

### Modes

- `ENGINE_ONLY`
- `VISUAL_ONLY`
- `FULL_RELEASE`

### Gates

- pass 1 → 2
- pass 2 → 3
- pass 3 → 4
- pass 4 → 5
- pass 5 → 6
- pass 6 → 7
- pass 7 → delivery

### Scope locks

- pass 1 locks: task flow, action hierarchy, GRAPHIC_PROPAGATION_MAP, SURFACE_CARTOGRAPHY, STATE_MATRIX
- pass 2 locks: canonical patterns
- pass 3 locks: approved structural changes
- pass 4 locks: token coverage, centralization audit
- pass 5 locks: visual snapshot

### Rollback

- triggered by pass 7 verdict `ROLLBACK`

## PROCESS

1. **Detect entry intent.** If request is UI/UX / visual / design,
   force `ENGINE_ONLY` (no direct entry to pass 4+).
2. Determine mode:
   - `ENGINE_ONLY` → passes 1–4 only
   - `VISUAL_ONLY` → **forbidden** without valid `SURFACE_CARTOGRAPHY`
   - `FULL_RELEASE` → passes 1–7 after ENGINE_ONLY
3. Request execution mode if missing and not deducible.
4. Confirm mode.
5. Declare starting pass.
6. Verify upstream preconditions.
7. Remind subsystem boundaries.
8. Apply gates and scope locks.
9. **For ENGINE_ONLY only:** validate that pass 1 will produce
   `GRAPHIC_PROPAGATION_MAP` before any progression.

## OUTPUT CONTRACT

Output must contain:

- execution mode
- subsystem concerned
- starting pass
- preconditions
- relevant upstream gates
- active scope locks
- rollback protocol if requested

## VALIDITY CRITERIA

A pass output is INVALID if it contains only:
  - token lists without GRAPHIC_PROPAGATION_MAP + SURFACE_CARTOGRAPHY
  - primitive component proposals without propagation context
  - migration plans without CENTRALIZATION_ROADMAP

A pass output is VALID only if:
  - Pass 1: GRAPHIC_PROPAGATION_MAP + SURFACE_CARTOGRAPHY + STATE_MATRIX
  - Pass 4: TOKEN_DEFINITION_MAP + PRIMITIVE_REGISTRY_CHECK + CENTRALIZATION_GAPS + CENTRALIZATION_ROADMAP
  - All passes: No direct primitive proposals before propagation map complete

## SEPARATION OF RESPONSIBILITIES

| Pass | Required Keys | Optional Seeds |
|------|---------------|----------------|
| Pass 1 (UX Engine) | GRAPHIC_PROPAGATION_MAP, SURFACE_CARTOGRAPHY, STATE_MATRIX | TOKEN_DEFINITION_MAP seeds, PRIMITIVE_REGISTRY_CHECK seeds |
| Pass 4 (Design System) | TOKEN_DEFINITION_MAP, PRIMITIVE_REGISTRY_CHECK, CENTRALIZATION_GAPS, CENTRALIZATION_ROADMAP | — |

## PROPAGATION PRIORITY ORDER

This order is **non-negotiable**. Never move to the next step before current step is complete.

```
1. SURFACE_PROPAGATION_POINTS       ← Identify real visual control points
2. SHARED_VISUAL_ANCHORS            ← Which surfaces share the same style source
3. SHELL_CONSISTENCY                ← Are shells consistent with each other
4. LAYOUT_INHERITANCE               ← How layouts inherit from shells
5. THEME_PROPAGATION                ← How the theme propagates (or doesn't)
6. PRIMITIVE_REGISTRIES             ← Button, Badge, etc. — only after steps 1–5
7. TOKEN_REFINEMENT                  ← Add/modify tokens — only after steps 1–6
```

**Rule:** Steps 1–5 = PROPAGATION ARCHITECTURE (Pass 1)
Steps 6–7 = DESIGN SYSTEM CREATION (Pass 4+)

## GENERIC_OUTPUT_DETECTION

If output contains phrases like:
  - "let's start with tokens"
  - "create Button/Badge/Tooltip"
  - "migration to design system"
WITHOUT prior GRAPHIC_PROPAGATION_MAP → REJECT and return to pass 1.

## GATE ENFORCEMENT

| Gate | Requirement |
|------|-------------|
| pass 1 → 2 | GRAPHIC_PROPAGATION_MAP + SURFACE_CARTOGRAPHY must exist |
| pass 2 → 3 | CANONICAL_PATTERNS must reference SURFACE_CARTOGRAPHY |
| pass 3 → 4 | GRAPHIC_PROPAGATION_MAP + SURFACE_CARTOGRAPHY + STATE_MATRIX must be frozen |
| pass 4 → 5 | All 7 required keys must be populated (3 from Pass 1, 4 from Pass 4) |

**Pass 4 → 5 gate detail (7 keys required):**

| Key | Source | Requirement |
|-----|--------|-------------|
| GRAPHIC_PROPAGATION_MAP | Pass 1 | Must document propagation points + inheritance chains |
| SURFACE_CARTOGRAPHY | Pass 1 | Must exist, Level 1–2 named |
| STATE_MATRIX | Pass 1 | Must map 7 states to surfaces |
| TOKEN_DEFINITION_MAP | Pass 4 | Must show definition → usage traceability |
| PRIMITIVE_REGISTRY_CHECK | Pass 4 | Must identify central vs local primitives |
| CENTRALIZATION_GAPS | Pass 4 | Must list non-centralized values with impact |
| CENTRALIZATION_ROADMAP | Pass 4 | Must order remediation by surface level |

If any key is missing or empty → HARD BLOCK, return to appropriate pass.

## REJECTION PATTERN: GENERIC_DESIGN_SYSTEM_RESPONSE

If response proposes, BEFORE GRAPHIC_PROPAGATION_MAP + SHELL_PROPAGATION_ANALYSIS:
- Button wrappers / registries
- Card registry
- Badge registry
- Primitives (Button, Input, etc.)
- Token expansion
- Design system migration

→ This is GENERIC_DESIGN_SYSTEM_RESPONSE
→ Return PASS_STATUS: BLOCKED

## VERDICT RULES

This resource does not emit READY / PARTIAL / BLOCKED by default.

Expected output:

- protocol clarification
- gate reminder
- mode reminder
- generic_output detection if applicable