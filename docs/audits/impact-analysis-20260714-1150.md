---
audit_type: impact_analysis
date: 2026-07-14
auditor: codex
scope: layered_credentials_enforcement
verdict: READY
classification: CONDITIONAL
---

# Impact analysis — layered credentials enforcement

## Change analyzed

Add one Core stdlib scanner, call it from the canonical pre-commit framework
gate, local CI and GitHub Actions, and cover it with unit/integration tests.

## Direct impact

- `contract-tooling` gains credentials detection as a responsibility and one
  architecture-sensitive tool/test pair.
- Local commits touching in-scope files can now be blocked before commit.
- Pull requests and pushes can be blocked by the same detector in range mode.

## Indirect impact

- `architecture-source` and `distribution-setup` consume the GitHub workflow.
- Hook installation remains delegated to the versioned script, so existing
  installed hooks inherit the new behavior without reinstalling.
- Local CI check count changes and must remain aligned with its displayed total.

## External impact

| Distribution | Impact | Adapter change |
|---|---|---|
| Pi | inherits Core hook/tool when operating this repo | none |
| OpenCode | inherits Core hook/tool when operating this repo | none |
| Codex | inherits Core hook/tool when operating this repo | none |
| Claude Code | inherits Core hook/tool when operating this repo | none |

No provider runtime state or consumer repository is modified. A bounded
verification established that `vbb-project-init --install-hook` currently exits
`0` while leaving the consumer hook absent because it copies only a deprecated
redirect whose canonical target is missing. This pre-existing consumer
packaging issue is not fixed here because it requires an ownership/copy-update
decision (SEC-CRED-005 / TER-001).

## Contracts, APIs and schemas

- No published skill contract, API, data schema or stored state changes.
- New CLI contract: `--staged` and `--range BASE HEAD`, exit `0` clean and
  non-zero on findings or invalid Git inputs.
- Exception marker becomes a reviewed source convention, not a distribution
  configuration file.

## Classification

**`CONDITIONAL`** because blocking behavior changes commit and CI outcomes.
It becomes acceptable and non-breaking for clean changes only if the POC,
positive/negative regression corpus, hook integration, range behavior and full
P.R2 all pass before activation.

## UNKNOWN

- Hook state in external consumer repos cannot be inventoried here; the
  project-init packaging path is confirmed broken and tracked separately.
- Coverage of unknown future credential formats is inherently incomplete.
