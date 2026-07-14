# POC — non-interactive runtime adapters

**Status**: CONCLUDED
**Date**: 2026-07-14
**Linked ADR**: `docs/adr/0047-runtime-conformance-benchmark.md`
**Linked run**: `docs/runs/2026-07-14_2316_runtime-conformance/`

## Hypothesis

Each supported runtime exposes a non-interactive command surface that can run
a read-only conformance prompt without changing the Core protocol.

## Test

```bash
codex exec --help
claude --help
pi --help
opencode run --help
```

## Success criterion

GO if all four installed CLIs expose non-interactive execution and at least
three expose a machine-readable output mode.

## Observed result

- Codex: `exec`, `--sandbox read-only`, `--ephemeral`, `--json`, output schema.
- Claude Code: `--print`, plan permission mode, JSON output and JSON schema.
- Pi: `--print`, `--mode json`, `--no-session`, read-only tool allowlist.
- OpenCode: `run`, JSON event format; permissions remain denied unless approved.
- Metric: 4/4 non-interactive, 4/4 machine-readable.

Verdict: GO

The shared protocol can remain provider-neutral while command templates stay
configurable and version-specific.
