# ADR 0047 — Shared runtime conformance benchmark

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit request), Codex
**Related POC**: `docs/runs/2026-07-14_2316_runtime-conformance/POC.md`

## Context

Vibebackbone verifies contracts, installation, and repository invariants, but
does not currently compare the observable governance behavior of Pi, OpenCode,
Codex, and Claude Code on the same task set. Provider-specific live commands
also evolve independently and may consume paid model calls.

## Decision

Core owns one provider-neutral conformance protocol with ten versioned scenarios,
a deterministic result evaluator, and optional live command adapters. CI evaluates
recorded or synthetic result envelopes without calling an LLM; live execution is
explicit, read-only by default, and never a release gate until a human promotes a
recorded baseline.

## Consequences

### Positive

- All four distributions are measured against the same routing and safety rules.
- Deterministic CI remains free of model cost and provider availability.
- Live results can expose behavioral drift without granting write permissions.

### Negative / costs

- Provider output must be normalized into a small JSON envelope.
- Live benchmarks remain probabilistic and require explicit credentials.
- Token and cost fields are comparable only when providers expose them.

## Rejected alternatives

- Hard-code one CLI parser per provider: rejected because CLI event schemas are
  external and versioned independently from Core.
- Run four paid agents in every CI build: rejected because it is costly,
  nondeterministic, and requires secrets in the release path.
- Keep only installation smoke tests: rejected because installation does not
  prove correct routing or safe behavior.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| A provider emits prose instead of the envelope | Medium | Medium | Validate strictly and report `INVALID_RESULT` without guessing. |
| A live adapter writes to the fixture repo | Low | High | Default commands are read-only; snapshot Git state before and after. |
| Scenario expectations drift from PILOTAGE | Medium | High | Store scenarios in Core and test their route vocabulary against canonical rules. |

## Rollback

Remove the conformance tool, its scenario manifest, tests, and CI invocation;
existing provider installers and runtime state remain unchanged.
