# Patch summary — runtime conformance v2

## Protocol

- Result schema `2.0` with `sample_id` and decomposed `decision`.
- Scenario-owned required and forbidden signals.
- Manifest-owned decision and signal vocabularies.

## Evaluator

- Exact result and decision rates.
- Required-signal recall.
- Forbidden-signal, mutation, and final-status violations.
- `PARTIAL` only for bounded non-dangerous misses; safety failures stay `FAIL`.

## Execution

- `--repetitions N` for live and recorded sampling; default remains one.
- Provider prompt permits governance skills but forbids subagent delegation.
- v1 results are rejected rather than silently normalized.
