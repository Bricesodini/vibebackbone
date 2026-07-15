# Impact analysis — Pi live conformance compatibility

## Change analyzed

Compatibility correction for Pi event output and canonical benchmark signals.

## Direct impact

The shared conformance manifest, result schema, prompt builder, envelope parser,
and focused tests are affected.

## Indirect impact

Pi becomes parseable without weakening raw JSON support. OpenCode, Codex, and
Claude inherit the vocabulary clarification but no adapter command change.

## External impact

No consumer repository, installed distribution, credential, or CI-paid model
execution is affected.

## Final classification

`NON_BREAKING`.

## UNKNOWN areas

Pi's semantic conformance score is unknown until the complete live rerun.
