# ADR 0001 — Formal Executor Boundary

**Status**: Accepted  
**Date**: 2026-05-28  
**Route**: STRUCTURED

## Context

The implementation-readiness audit identified `IMPL-002`: Vibebackbone contracts
are complete and linted, but runtime enforcement is still declarative. Agents
read `SKILL.md`, `CONTRACT.yaml`, `PILOTAGE.md` and governance docs, then apply
the rules by interpretation.

The new structured `docs/ARCHITECTURE.md` and generated `docs/RELATIONS.md`
make dependencies and impact zones machine-readable, but they do not themselves
execute gates, route transitions or state updates.

## Decision

Vibebackbone keeps Markdown/YAML governance as the source of truth, and defines
the future formal executor as a bounded layer that consumes those sources.

The executor may:

- discover skills from `skills/INDEX.yaml`;
- load and validate `CONTRACT.yaml`;
- evaluate `gates.before`, `gates.success` and `gates.after`;
- route a request to candidate skills;
- validate expected artifacts exist after a run;
- consume structured architecture blocks from `docs/ARCHITECTURE.md`;
- emit machine-readable run status.

The executor must not:

- replace `SKILL.md` as the human-readable behavior contract;
- rewrite governance policy on its own;
- make product or architecture decisions without a documented artifact;
- treat generated projections such as `docs/RELATIONS.md` as canonical truth;
- import the vibebackbone repository's historical audit state into downstream projects.

## Consequences

- `docs/ARCHITECTURE.md` remains the architecture source of truth.
- `docs/RELATIONS.md` remains a generated projection.
- `tools/vbb-architecture.py lint` is a pre-executor guard for architecture rigor.
- The next runtime implementation should start by enforcing existing contracts,
  not by inventing a new contract schema.
- Downstream projects must be initialized with fresh governance state.

## Open Follow-Up

Before implementing the executor, define:

- the minimal command interface;
- the JSON status schema;
- failure semantics for `PARTIAL`, `BLOCKED` and `FAIL`;
- how run artifacts are passed between phases;
- which operations remain agent-only versus executable.
