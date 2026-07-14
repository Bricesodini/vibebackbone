# Patch summary — runtime conformance benchmark

## Core behavior

- `conformance/runtime-scenarios.json`: ten shared routing/safety scenarios.
- `conformance/result-schema.json`: strict provider result envelope.
- `conformance/runtime-adapters.json`: four read-only/plan CLI adapters.
- `tools/vbb_runtime_conformance.py`: prompt generation, deterministic
  evaluation, metrics, optional live execution, Git mutation protection.

## Verification

- `tests/test_runtime_conformance.py`: matrix, negative, parser, adapter,
  consent, CLI, metric, and mutation coverage.
- `scripts/vbb-ci-local.sh`: deterministic self-test promoted to check 4/13.
- `.github/workflows/vbb-contracts.yml`: same network-free self-test.
- `tests/test_static_quality_ci.py`: local/remote parity assertions.
- `scripts/install-vbb-hooks.sh` and `tests/test_install_vbb_hooks.sh`: resolve
  a Python interpreter with PyYAML instead of hard-coding `python3` in the
  installed loop-closure stage.

## Canonical propagation

- ADR 0047 and POC document the Core-owned protocol decision.
- `docs/ARCHITECTURE.md` and generated `docs/RELATIONS.md` map the surface.
- `docs/DISTRIBUTIONS.md` records promote-to-Core for all four providers.

## Rollback

Revert the new conformance files and remove their CI/architecture references;
restore the previous hook template only if all supported environments guarantee
the same `python3` dependencies.
