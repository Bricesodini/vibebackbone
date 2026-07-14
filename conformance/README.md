# Runtime conformance benchmark

This benchmark compares Pi, OpenCode, Codex, and Claude Code against the same
ten routing and safety scenarios. The protocol is Core-owned; provider commands
are adapters only.

## Deterministic CI

```bash
python tools/vbb_runtime_conformance.py self-test
pytest tests/test_runtime_conformance.py -q
```

This path performs no network request and no LLM call. It validates the 4 × 10
matrix, route vocabulary, required behavioral signals, read-only policy, result
schema, duplicate/missing detection, and the live mutation guard.

## Inspect one benchmark prompt

```bash
python tools/vbb_runtime_conformance.py prompt \
  --provider codex \
  --scenario structured_architecture_change
```

## Run a live sample

Live mode can consume provider credits and is never automatic:

```bash
python tools/vbb_runtime_conformance.py run \
  --provider codex \
  --scenario fast_zero_typo \
  --workspace /path/to/clean/disposable/repo \
  --results /tmp/codex-vbb-results.jsonl \
  --confirm-live
```

Use a clean disposable Git repository. The runner compares `git status` before
and after every call and fails if the provider changes the workspace. Run
`--provider all --scenario all` only when forty model calls are intentional.

Evaluate recorded results without invoking providers:

```bash
python tools/vbb_runtime_conformance.py evaluate \
  --results /tmp/codex-vbb-results.jsonl \
  --provider codex --json
```

Unavailable token and cost metrics remain `null`; they are never inferred.
