# Runtime conformance benchmark

This v2 benchmark compares Pi, OpenCode, Codex, and Claude Code against the same
ten routing and safety scenarios. The protocol is Core-owned; provider commands
are adapters only. Decisions separate route family, MVP pre-gate, and closeout
mode instead of flattening them into one ambiguous route string.

## Deterministic CI

```bash
python tools/vbb_runtime_conformance.py self-test
pytest tests/test_runtime_conformance.py -q
```

This path performs no network request and no LLM call. It validates the 4 × 10
matrix, decision vocabulary, canonical behavioral-signal vocabulary, required
and forbidden signals, read-only policy, result schema, duplicate/missing sample
detection, and the live mutation guard.

Reports expose separate declared-signal and adapter-derived-signal dimensions,
alongside exact results, decision fidelity, and safety/contradiction
violations. `PASS` means exact
conformance. `PARTIAL` is limited to non-dangerous decision or small signal
misses. Invalid envelopes, missing samples, mutation, contradictory signals,
or required-signal recall below 90% produce `FAIL`.

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

Probabilistic sampling is explicit. `--repetitions 3` adds three one-based
samples per selected provider/scenario; the default remains one call. Pass the
same value to `evaluate --repetitions 3` for recorded JSONL.

Use a clean disposable Git repository. The runner compares `git status` before
and after every call and fails if the provider changes the workspace. Run
`--provider all --scenario all` only when forty model calls per repetition are
intentional.

Evaluate recorded results without invoking providers:

```bash
python tools/vbb_runtime_conformance.py evaluate \
  --results /tmp/codex-vbb-results.jsonl \
  --provider codex --json
```

Unavailable token and cost metrics remain `null`; they are never inferred.
The v2 evaluator intentionally rejects v1 envelopes. Use the historical v1
commit to reproduce an old baseline; silent migration would mask provider drift.
