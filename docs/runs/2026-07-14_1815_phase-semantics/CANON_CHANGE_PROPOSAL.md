# Canon change proposal — clarify dual phase namespaces

**Status**: APPROVED
**Human validation**: Brice (`Go`, 2026-07-14)

## Current canon

`PHASE_TO_SKILLS.md` deprecates `SKILL.md phase: 1` in favor of `02_AUDIT` but
does not distinguish contract `routing.phase_scope: phase_1`.

## Proposed clarification

State explicitly that the frontmatter is the agentic lifecycle namespace and
the contract field is the backward-compatible catalog routing namespace. Enforce
the pair for all `1-vbb-*` skills.

## Migration

Update eleven frontmatters; preserve sixteen contract scopes; add blocking lint.

## Rollback

Atomic revert of documentation, frontmatters, linter and tests.
