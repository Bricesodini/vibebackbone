---
context_role: mvp-start-protocol
phase: phase_0
status: active
updated: 2026-05-27
---

# MVP_START_PROTOCOL — Readiness before implementation

This document is the mandatory entry point for any project started from zero
with Vibebackbone. It defines the pre-implementation gate that keeps the agent
in framing mode until the base brief is complete enough for controlled
execution.

## 1. Philosophy

### No code before readiness

Until the base specification is sufficiently complete, the agent stays in
framing mode. It must not create application code, migrations, endpoints,
models, UI components, Docker structure, persistence logic, or business logic.

### Think before implementation

The first output of a new MVP is not code. It is a clarified brief, a bounded
scope, visible risks, and enough architecture intent to prevent accidental
construction.

### Separate responsibilities

Implementation must preserve explicit responsibility boundaries:

- product intent before architecture
- architecture before execution
- business logic separate from API transport
- persistence separate from business rules
- UI separate from domain behavior

### Architecture before execution

Before implementation starts, the project must have at least a minimal
architecture direction: main modules, data ownership, API boundaries if any,
and deployment constraints. Detailed architecture may evolve, but the first
execution run must not start from an undefined structure.

### Refuse best-effort coding

When the brief is incomplete, the agent must not silently infer the missing
parts and "do its best". It produces blocking questions only.

### Clarify ambiguous zones before construction

Critical ambiguity blocks implementation. Non-critical ambiguity may be recorded
as accepted uncertainty only if it does not affect data, security, persistence,
architecture, or core user flows.

## 2. RICO / initial brief validation

The initial brief is implementation-ready only when the following elements are
explicit enough to guide a controlled MVP:

| Required element | Minimum expectation |
|---|---|
| Product objective | What outcome the MVP must enable |
| Target users | Who uses it and in what context |
| Problem solved | The concrete pain or need addressed |
| MVP journey | The main user path from start to completed value |
| MVP scope | What is included in the first usable version |
| Explicit out-of-scope | What must not be built now |
| Technical constraints | Stack, integrations, platform, runtime or tooling constraints |
| Deployment constraints | Local only, staging, production, hosting, environment expectations |
| Initial data model | Main entities, relationships, ownership, persistence needs |
| Acceptance criteria | Observable conditions for saying the MVP works |
| Critical risks | Data, security, legal, operational, delivery or product risks |

The brief may be concise. It must still be explicit.

## 3. Blocking questions

If the brief is incomplete, the agent does not code.

Expected behavior:

- produce only a prioritized list of blocking questions;
- group questions by impact: product, users, data, architecture, deployment,
  security, acceptance;
- explain why each question blocks implementation;
- avoid silent assumptions;
- avoid approximate implementation;
- avoid "I will do my best" execution.

Blocking question output must end with one of:

- `BLOCKED`: implementation cannot start;
- `PARTIAL`: limited framing can continue, but no application code can start;
- `READY`: implementation may proceed to structured planning.

## 4. Architecture invariants

The following invariants apply to any MVP started under this protocol:

- business logic, API transport, persistence and UI responsibilities stay
  separated;
- no monolithic file is created as the default implementation shape;
- each module has a clear responsibility;
- every API endpoint or command is tied to an identified use case;
- every persistence object maps to an explicit data model element;
- any structuring decision with long-term impact gets a short ADR;
- technical debt is traced explicitly when accepted;
- architecture is reasoned about before execution starts.

## 5. Authorization to code

Implementation may start only when the readiness gate returns `READY`.

Minimum deliverables before code:

- a base brief covering all RICO required elements, or explicit `not applicable`
  entries where justified;
- a list of MVP use cases and non-goals;
- an initial data model if any persistence, import/export, account state or
  business state is involved;
- architecture boundaries sufficient to place code without creating a
  monolith;
- deployment constraints sufficient to avoid incompatible infrastructure
  choices;
- acceptance criteria for the first implementation run;
- critical risks either resolved, mitigated, or explicitly accepted.

If readiness is `BLOCKED` or `UNKNOWN`, no application code is allowed.

If readiness is `PARTIAL`, the agent may continue framing, produce a plan, or
ask targeted questions. It still must not create application code, migrations,
endpoints, models, UI components, Docker structure, persistence logic, or
business logic.

## 6. Relationship to other documents

- `docs/CONTEXT.md` remains the lightweight router and points here.
- `docs/PILOTAGE.md` decides the route and escalation behavior.
- `docs/AGENTIC_RUN_PROTOCOL.md` defines the phase sequence and artifact
  requirements.
- `docs/ARCHITECTURE.md` is produced only after readiness validation. It records
  architecture decisions and boundaries, not raw product framing.
- `0-vbb-rico-readiness` is the executable skill that applies this protocol.
