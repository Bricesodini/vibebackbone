# Patch summary — Pi live conformance compatibility

## Behavior

- Pi's fenced JSON result inside its native JSON event stream is now accepted.
- Signals are constrained to fourteen canonical identifiers across manifest,
  JSON Schema, prompt, and evaluator.
- Unknown or paraphrased signal identifiers now fail explicitly.

## Tests

- Added a Pi-shaped fenced event regression.
- Added manifest/schema/runtime vocabulary coherence assertions.
- Preserved the deterministic 40-cell self-test.

## Live evidence

Pi completed 10/10 calls without mutation; semantic conformity is 4/10.
