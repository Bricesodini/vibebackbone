# ADR 0004 — Contract Schema Version Semantics

**Status**: Accepted  
**Date**: 2026-06-02  
**Route**: STRUCTURED

## Context

The deep framework audit identified `VBB-DEEP-003`: all skills had a functional
version in `SKILL.md` frontmatter while each `CONTRACT.yaml` also exposed
`version: "0.3"`. The two values differed for 64/64 skills, creating an
ambiguous metadata model.

Existing tooling already used `CONTRACT.yaml.version` as a schema selector for
contract features such as `outputs.artifact`. Treating that field as the
functional skill version would require rewriting every contract whenever a skill
behavior changes, and would break the existing schema-gating role.

## Decision

`SKILL.md` frontmatter `version` is the functional skill version.

`CONTRACT.yaml.contract_schema_version` is the explicit contract schema version.
The existing `CONTRACT.yaml.version` field remains as a compatibility alias and
must match `contract_schema_version` while legacy consumers still read it.

The contract linter enforces:

- `contract_schema_version` is present;
- the schema version is supported;
- `version` and `contract_schema_version` match when both are present.

## Consequences

- The 64/64 version mismatch is no longer interpreted as a defect.
- Runtime and executor tooling read `contract_schema_version`, falling back to
  `version` for backward compatibility.
- Future schema upgrades change `contract_schema_version` and its alias.
- Future skill behavior releases change only `SKILL.md` frontmatter unless the
  machine-facing contract schema also changes.

