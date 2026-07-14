# Impact analysis — runtime conformance benchmark

## Change analyzed

Add a Core-owned conformance protocol, deterministic evaluator, optional live
command adapters, tests, and CI coverage for Pi, OpenCode, Codex, and Claude Code.

## Direct impact

- Contract tooling gains a read-only benchmark command.
- Distribution setup gains behavioral verification without installer changes.
- CI gains a deterministic fixture evaluation step.

## Indirect impact

- Scenario routing expectations depend on `docs/PILOTAGE.md` vocabulary.
- Architecture and distribution propagation records must name the new surface.
- Provider CLI drift can break optional live commands without breaking CI.

## External impact

- No installed file or existing CLI contract changes.
- Live mode depends on locally installed, authenticated provider CLIs.
- No secret is read by deterministic CI.

## Classification

`CONDITIONAL` — non-breaking for existing consumers; behavior comparison is
only authoritative when a live run is explicitly recorded and reviewed.

## Unknowns

- Provider event schemas may change.
- Token/cost metrics are not uniformly exposed.
- Model nondeterminism requires repeated live samples before release gating.
