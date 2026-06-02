# distributions/hermes/ — Hermes/Cody distribution

The currently active distribution of VBB Core for the Hermes agent runtime,
with Cody as the orchestrator.

## What belongs here

- `install/INSTALL.md` (← was `docs/hermes/INSTALL.md`, migrated Phase 2)
- `verify/verify.sh` (← was `scripts/hermes/verify.sh`, migrated Phase 3)
- `proxy/` (← was `tools/proxy/`, 17 source files + fixtures/ + tests/, migrated Phase 3)
- `proxy/adr/` (← was `docs/adr/0006-0012`, 7 ADRs, migrated Phase 2)
- `bypass-lint/` (← was `tools/vbb-bypass-lint.py` + `tools/vbb-bypass-lint/`, migrated Phase 3)
- `profiles-template/` (← planned, was `providers/templates/example-consumer-repo/`, **NOT YET MIGRATED**)
- `docs/` (← was `docs/proxy/`, migrated Phase 2)

## What does NOT belong here

- `~/.hermes/profiles/vbb-*/SOUL.md` — these stay in the runtime, not in the repo
- `skills/`, `prompts/`, `tools/vbb-*.py` — Core canon, not duplicated

## Current state (Phase 3 complete)

Phases 1, 2, and 3 of ADR 0013 (LIGHT REORG) are complete. The Hermes/Cody
distribution now owns its install doc, verify script, proxy cluster (code +
tests + 7 ADRs), and anti-bypass linter under `distributions/hermes/`. The
only remaining item is `profiles-template/` (planned, not yet migrated).
`docs/adr/0001-0005` (Core ADRs) and `tools/vbb-*.py` (Core tools) remain in
their Core locations, untouched.

## Status

Phase 1 (sentinel): DONE
Phase 2 (docs migration): DONE
Phase 3 (scripts/outils/proxy migration): DONE
Phase 4 (Pi/Claude migration): DEFERRED (out of ADR 0013 scope)
Phase 5 (final CI validation): pending Phase 4

## See also

- `distributions/hermes/install/INSTALL.md` — current install doc
- `distributions/hermes/verify/verify.sh` — current verify (28/28 PASS)
- `distributions/hermes/proxy/` — current proxy cluster
- `distributions/hermes/proxy/adr/` — current 7 proxy ADRs
- `distributions/hermes/bypass-lint/` — current anti-bypass linter
- `docs/adr/0013-repo-organization-core-vs-distributions.md` — this decision
- `docs/DISTRIBUTIONS.md` §Hermes/Cody
