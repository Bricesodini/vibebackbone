# POC — Pi fenced result extraction

**Status**: CONCLUDED
**Date**: 2026-07-15
**Linked ADR**: `docs/adr/0047-runtime-conformance-benchmark.md`

## Hypothesis

Pi's native JSON event stream contains the requested conformance object, but as
a fenced JSON string nested in the final assistant message.

## Observation

A direct read-only Pi invocation for `fast_minimal_small_patch` returned:

- the correct `FAST-MINIMAL` route;
- all required result fields inside a `json` Markdown fence;
- descriptive signal prose rather than canonical signal identifiers;
- no reported workspace mutation.

The current extractor only parses strings beginning with `{` or `[`, explaining
the fail-closed error without implying a Pi routing failure.

## Success criterion

GO if the defect is bounded to additive fenced-JSON extraction plus an explicit
provider-neutral signal vocabulary, with no adapter command or safety change.

Verdict: GO
