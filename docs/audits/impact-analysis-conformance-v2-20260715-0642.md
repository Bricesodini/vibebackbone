# Impact analysis — runtime conformance v2

## Change analyzed

Replace the ambiguous v1 runtime result envelope with the ADR 0048 decision
model and multidimensional evaluation.

## Direct impact

The Core-owned manifest, schema, evaluator, tests, documentation, architecture
projection, and four-provider prompt contract change together.

## Indirect impact

Deterministic CI exercises the new envelope. Live calls remain opt-in and
read-only, but old recorded output requires the historical v1 implementation.

## External impact

No distribution setup or installed runtime state changes.

## Final classification

`BREAKING` for benchmark JSON; bounded and intentional.

## UNKNOWN areas

Provider-specific v2 output reliability requires future live samples.
