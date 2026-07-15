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

### POC validation — 2026-07-15

The live A/B POC confirmed that a compact decision card and contradiction
self-check materially improve Pi exact conformance (27/30 versus 12/30 on the
same three repetitions). Codex `gpt-5.4-mini` was initially blocked by schema
features outside its structured-output subset; the result schema was made
portable by adding explicit primitive types and removing `uniqueItems`, which
does not change the evaluator's semantic checks. Codex then completed 10/10
calls with seven exact results under the baseline prompt and seven under the
compact card; no provider mutation was observed.

| Claim | Evidence | Status |
|---|---|---|
| Pi compact card improves exact conformance | 27/30 versus 12/30 on identical scenarios and repetitions | VALIDATED |
| Codex `gpt-5.4-mini` is runnable | 10/10 calls completed after schema portability fix | VALIDATED |
| Schema portability fix preserves semantic checks | 230 tests passed; architecture lint passed; zero mutations | VALIDATED |

### Follow-up POCs — 2026-07-15

| Claim | Evidence | Status |
|---|---|---|
| Codex result is repeatable | `gpt-5.4-mini`, compact card, 20/30 exact across three repetitions; zero mutations | PARTIAL |
| Card and self-check have separable effects | Pi targeted causal POC: card-only 2/4, self-check-only 1/4, combined prior POC 3/4 | PARTIAL |
| Infrastructure-derived safety signals explain all misses | No complete baseline replay with derived scoring yet | UNVALIDATED |

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
