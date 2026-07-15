# ADR 0048 — Runtime conformance decision model v2

**Status**: ACCEPTED
**Date**: 2026-07-15
**Route**: STRUCTUREE
**Decision makers**: Brice (explicit correction request), Codex
**Related ADR**: `docs/adr/0047-runtime-conformance-benchmark.md`
**Related POC**: `docs/runs/2026-07-15_0636_conformance-v2/POC.md`

## Context

The first Pi live baseline produced only 4/10 exact scenario passes while
matching 31/33 required behavioral signals and making no mutation. Investigation
showed that v1 conflated route family, MVP pre-gate, and closeout disposition;
did not supply the route vocabulary to Pi; accepted contradictory signals; and
collapsed every deviation into one binary failure.

## Decision

Replace the v1 flat `route` result with a v2 `decision` object containing
`route_family`, `pre_gate`, and `closeout_mode`. Publish all output vocabularies
in the prompt, add scenario-specific forbidden signals, report decision,
required-signal, contradiction, and safety dimensions separately, and support
explicit repeated samples through a one-based `sample_id`.

The v2 evaluator stays strict. It does not silently upgrade v1 provider output;
historical v1 evidence remains reproducible from Git history.

## Consequences

### Positive

- The benchmark reflects PILOTAGE's distinction between route, pre-gate, and
  closeout disposition.
- Safety behavior is visible even when exact decision fidelity fails.
- Contradictory signals and probabilistic variance become measurable.

### Negative / costs

- Existing v1 JSONL cannot be evaluated by the v2 tool without checking out the
  v1 implementation.
- Provider prompts and recorded fixtures must emit the new envelope.

## Rejected alternatives

- Normalize provider route strings in adapters: rejected because it would hide
  non-conformance.
- Keep the flat route and only add aliases: rejected because aliases cannot
  represent a pre-route MVP gate and closeout mode without semantic ambiguity.
- Silently migrate v1 output: rejected because live providers could appear v2
  conformant while continuing to emit the obsolete contract.

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Decision model drifts from PILOTAGE | Medium | High | Cross-surface tests and one manifest-owned vocabulary |
| PARTIAL hides a critical failure | Low | High | Mutation, missing results, forbidden signals, or low signal recall remain FAIL |
| Repetitions consume unexpected credits | Medium | Medium | Default remains one; explicit positive `--repetitions` required |

## Rollback

Revert the v2 manifest, schema, evaluator, tests, and documentation together.
Do not retain a mixed v1/v2 protocol.
