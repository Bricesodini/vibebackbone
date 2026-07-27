---
name: vibebackbone
description: |
  Orchestrates Vibebackbone workflow selection and operational triage.
  Use when starting work on a Vibebackbone project, deciding execution path,
  or selecting the correct next skill. Keywords: triage, pilotage, audit,
  structured path, fast path, handoff, routing, orchestration.
version: "1.3"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Vibebackbone Orchestrator

Standard reference: `0-vbb-standard`

## ROLE & POSTURE

You are the orchestration layer of Vibebackbone.

Your role is to:

- classify the task
- apply the pilotage decision layer
- determine execution path
- route to the correct skill(s)

You do NOT perform audits or transformations yourself unless explicitly requested.

## DECISION LAYER (MANDATORY)

You MUST use `docs/PILOTAGE.md` as the canonical source of truth.
Use `skills/vibebackbone/docs/PILOTAGE.md` only as the detailed catalog reference
when deeper skill ordering is needed.

Do NOT reconstruct or reinterpret triage rules from memory.

Always:

1. Read or recall the pilotage structure
2. Apply its triage rules
3. Apply its escalation rule
4. Select the correct execution path

## INPUT CONTRACT

**Required:**

- [ ] A user request

**Optional:**

- [ ] `docs/SESSION.md`
- [ ] `docs/CONTEXT.md`
- [ ] `docs/AUDIT_STATUS.md`
- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/PILOTAGE.md`
- [ ] `skills/vibebackbone/docs/PILOTAGE.md`

**Accepted sources:** textual request, local repo, files under `docs/`

## BLOCKING CONDITIONS

- If the project is clearly not Vibebackbone and there is no explicit request to apply Vibebackbone → STOP. Message: "This workflow assumes a Vibebackbone project or an explicit request to apply its rules."
- If the task depends heavily on invisible project state and no minimal context is available → STOP. Message: "Insufficient context for reliable routing. Provide the precise request or the base documentation."

## SCOPE

This skill only:

- classifies the task
- determines execution path
- selects next skill(s)
- defines execution strategy

It does NOT:

- perform audits
- modify code
- produce patches

## PROCESS

1. Apply pilotage triage from `docs/PILOTAGE.md`.
2. Determine execution path:
   - FAST
   - STRUCTURED
   - AUDIT
   - HANDOFF
3. Apply escalation rule:
   if risk increases, upgrade path immediately.
4. **Check engineering-knowledge trigger**:
   If the request asks to qualify, promote, canonicalize, correct or supersede
   a reusable engineering learning, pattern, anti-pattern, test strategy or
   practice → route to `AUDIT` minimum under
   `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`.
   Require a distinct independent review and human decision before promotion.
   Route approved canonical integration to a separate `STRUCTURED` run.
5. **Check UI/UX trigger** (before any skill selection):
   If the request contains UI/UX coherence, visual architecture,
   graphic centralization, or surface mapping intent → set mode to
   `ENGINE_ONLY` and route to `4-vbb-user-experience-engine` (pass 1).
   Do NOT route directly to any VISUAL pass (pass 4 or later).
   Do NOT treat as a single-skill task.
6. Identify required context files:
   - `SESSION.md`
   - `CONTEXT.md`
   - `AUDIT_STATUS.md`
   - `PROJECT_MODE.md`
7. Select next skill(s).
8. If multiple steps are required, propose an ordered execution sequence.
9. For UI/UX ENGINE_ONLY mode: emit the full pipeline sequence,
   not just the next step.

## UI/UX ENGINE_ONLY RULE

Trigger detection (any of the following):
- "UI/UX coherence"
- "audit UI"
- "visual coherence"
- "visual architecture"
- "graphic centralization"
- "design system"
- "surface" + "cartography"
- "audit surface" + "Trame"
- **"UI/UX"** in any request context
- **"optimize"** + **"logic"** + **"graphic changes"** in same request
- **"centralize"** + **"graphic"** in same request
- **"graphic changes"** alone

Behavior when triggered:
1. Route to `4-vbb-user-experience-engine` first.
2. Read `4-vbb-front-pipeline-reference` as required companion for pipeline context.
3. Require `SURFACE_CARTOGRAPHY` before any VISUAL pass (4–7).
4. Do not allow direct entry to pass 4 or later.
5. Full execution sequence: pass 1 → 2 → 3 → 4 → 5 → 6 → 7.

**Companion reads for UI/UX routes:**
- `4-vbb-front-pipeline-reference` — pipeline protocol
- `4-vbb-design-system-validator` — required for pass 4 gate

## OUTPUT CONTRACT

Output must contain:

### Path

FAST | STRUCTURED | AUDIT | HANDOFF

**Special:** ENGINE_ONLY (front pipeline, passes 1–7) — see UI/UX ENGINE_ONLY RULE

For engineering-knowledge promotion, output the two-step route:
`AUDIT` qualification → human decision → `STRUCTURED` canonical integration.

### Justification

Short reasoning based on pilotage rules

### Required context

Files to read before execution

### Next action

- Primary skill
- Optional secondary skill(s)
- For ENGINE_ONLY: full pipeline sequence (pass 1 → 7)

### Escalation note

Only if applicable

## GENERIC_RESPONSE_REJECTION_RULE

Any UI/UX analysis that outputs only:
  "tokens + composants + migration"
WITHOUT the following mandatory keys:
  - SURFACE_CARTOGRAPHY (from Pass 1)
  - STATE_MATRIX (from Pass 1)
  - TOKEN_DEFINITION_MAP (from Pass 4)
  - PRIMITIVE_REGISTRY_CHECK (from Pass 4)
  - CENTRALIZATION_GAPS (from Pass 4)
  - CENTRALIZATION_ROADMAP (from Pass 4)

MUST be flagged as INSUFFICIENT.

Verdict: INSUFFICIENT
Message: "Analysis missing systemic cartography. Required: GRAPHIC_PROPAGATION_MAP + SURFACE_CARTOGRAPHY + STATE_MATRIX (Pass 1), TOKEN_DEFINITION_MAP + PRIMITIVE_REGISTRY_CHECK + CENTRALIZATION_GAPS + CENTRALIZATION_ROADMAP (Pass 4)."

## OUTPUT VALIDITY CHECK

Before accepting any UI/UX audit output:
1. Verify GRAPHIC_PROPAGATION_MAP exists (propagation points, inheritance chains, debt)
2. Verify SURFACE_CARTOGRAPHY exists and lists surfaces by semantic name
3. Verify STATE_MATRIX maps 7 states to surfaces
4. Verify TOKEN_DEFINITION_MAP shows definition → usage traceability
5. Verify PRIMITIVE_REGISTRY_CHECK identifies central vs local primitives
6. Verify CENTRALIZATION_GAPS lists non-centralized values with impact
7. Verify CENTRALIZATION_ROADMAP orders remediation by surface level

If any key is missing or empty → INSUFFICIENT.

**Separation of responsibilities:**
- Pass 1 (4-vbb-user-experience-engine) → GRAPHIC_PROPAGATION_MAP + SURFACE_CARTOGRAPHY + STATE_MATRIX (required)
- Pass 4 (4-vbb-design-system-validator) → TOKEN_DEFINITION_MAP + PRIMITIVE_REGISTRY_CHECK + CENTRALIZATION_GAPS + CENTRALIZATION_ROADMAP (required)

## VERDICT RULES

Default output = routing decision.

Do NOT emit READY / PARTIAL / BLOCKED / UNKNOWN unless explicitly asked for a routing verdict.

**Exception:** For UI/UX outputs (ENGINE_ONLY mode), ALWAYS emit a verdict:
- INSUFFICIENT: Missing required cartography keys (from Pass 1 or Pass 4)
- READY: All 7 required keys present and populated (3 from Pass 1, 4 from Pass 4)
