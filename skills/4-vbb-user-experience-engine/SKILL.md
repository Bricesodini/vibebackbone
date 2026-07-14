---
name: 4-vbb-user-experience-engine
description: |
  Pass 1/7 of the Vibebackbone front pipeline. Optimizes business UX before
  visual styling by mapping graphic propagation, product surfaces, workflow
  friction, states, and action hierarchy. Use as the mandatory first pass for
  UI/UX, visual architecture, graphic centralization, and surface mapping.
version: "2.5"
phase: 4
token_budget: medium
subagent_eligible: false
mode_sensitive: false
---

# User Experience Engine

Standard reference: `0-vbb-standard`. Read `docs/PILOTAGE.md` and use
`4-vbb-front-pipeline-reference`.

## ROLE & POSTURE

Optimize business workflows before visual styling. The primary objective is
graphic propagation architecture: show where a visual change is controlled,
how it propagates, and where it breaks. This pass does not create a design
system.

Never modify code or backend behavior, make aesthetic decisions, add features,
or propose token/primitive migrations before propagation and surface mapping.

## INPUT CONTRACT

Required: interface evidence (source, screenshots, or flow description), target
user, primary task, usage context, and repository context sufficient to identify
real surfaces.

Ask at most one clarification round.

## BLOCKING CONDITIONS

Stop when interface evidence or the context required to identify real surfaces
remains incomplete after one clarification round.

## SCOPE

Cover propagation architecture, surface cartography, workflow friction, state
coverage, action hierarchy, and flow simplification. Exclude visual styling,
design-system creation, backend behavior and code changes.

## NON-NEGOTIABLE ORDER

1. `SURFACE_PROPAGATION_POINTS`
2. `SHARED_VISUAL_ANCHORS`
3. `SHELL_CONSISTENCY`
4. `LAYOUT_INHERITANCE`
5. `THEME_PROPAGATION`
6. `PRIMITIVE_REGISTRIES` (optional downstream analysis)
7. `TOKEN_REFINEMENT` (optional downstream analysis)

Steps 1–5 establish propagation architecture. Do not propose Button/Card/Badge
registries, new tokens, primitives, or design-system migration before they are
complete. Primitive and token observations may appear only as seeds for pass 4.

## PROCESS

Execute in order:

1. Build `GRAPHIC_PROPAGATION_MAP`: distinguish real and fake control points;
   trace Shell → Layout → Surface → Component inheritance; map change impact,
   break risk, and propagation debt. Include `SHELL_PROPAGATION_ANALYSIS`.
2. Build `SURFACE_CARTOGRAPHY` by semantic name: Level 1 product shells, Level 2
   business surfaces, then Level 3 UI primitives. Never jump to primitives.
3. Model target user, context, primary/secondary tasks, frequency, and criticality.
4. Classify friction as critical, high, or minor and cite its location.
5. Build `STATE_MATRIX`, linking every applicable surface to seven states:
   idle, loading, success, error, empty, disabled, partial.
6. Define primary, secondary, destructive, and contextual actions.
7. Propose a simpler flow without expanding business scope; quantify removed
   steps/frictions and added state coverage.

## OUTPUT CONTRACT

Write `pass-1-output.md` with these sections and exact keys:

### `GRAPHIC_PROPAGATION_MAP` — mandatory

Include:

- propagation points: control point, type, real/fake, propagated surfaces;
- visual inheritance chains;
- change impact: changed value, affected surfaces, break risk;
- propagation debt: surface, problem, correction difficulty;
- `SHELL_PROPAGATION_ANALYSIS` and a one-sentence canonical propagation anchor.

### `SURFACE_CARTOGRAPHY` — mandatory

List semantic surfaces at Levels 1–3 with location, responsibility, and children
where relevant.

### Business UX sections — mandatory

- task model;
- `FRICTION_MAP`;
- `STATE_MATRIX` for all seven states tied to cartographed surfaces;
- `ACTION_HIERARCHY`;
- `SIMPLIFIED_FLOW`;
- measurable simplification;
- structural notes limited to DOM descriptions or pseudocode.

### Pass 4 seeds — optional

- `TOKEN_DEFINITION_MAP` seeds: candidate, source surface, current form,
  centralizability;
- `PRIMITIVE_REGISTRY_CHECK` seeds: primitive, registry location, local
  redefinitions, affected surfaces.

Pass 4 owns the complete token map, registry check, `CENTRALIZATION_GAPS`, and
`CENTRALIZATION_ROADMAP`; pass 1 must not claim them as complete.

## VERDICT RULES

Classify as `GENERIC_DESIGN_SYSTEM_RESPONSE` and set `PASS_STATUS: BLOCKED` if
registries, tokens, primitives, or migration are proposed before
`GRAPHIC_PROPAGATION_MAP` and `SHELL_PROPAGATION_ANALYSIS` are complete.

- Missing/incomplete `GRAPHIC_PROPAGATION_MAP`, `SURFACE_CARTOGRAPHY`, or
  `STATE_MATRIX` → `PASS_STATUS: BLOCKED`.
- Missing critical state coverage → `PASS_STATUS: CRITICAL_PENDING`.
- All mandatory sections complete, ordered, and grounded → `PASS_STATUS: READY`.

Freeze the three mandatory maps for passes 2–7. They are hard preconditions for
pass 4.

Canonical priority: propagation architecture before component abstraction.
