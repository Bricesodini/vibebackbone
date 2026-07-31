---
status: accepted
date: 2026-07-31
document_convention: vbb-doc-v1
version: "1.0"
type: adr
visibility: public
tags: [adr, governance, contract]
relations:
  - "../audits/document-convention-audit-rc1-20260731.md"
  - "../DOCUMENT_CONVENTION.md"
adr_id: "0052"
decision_status: accepted
decision_makers:
  - "Brice"
  - "Codex implementation run"
consulted:
  - "docs/audits/document-convention-audit-rc1-20260731.md"
  - "docs/audits/release-check-20260729-1902.md"
informed:
  - "Pi"
  - "OpenCode"
  - "Codex"
  - "Claude Code"
---

# ADR 0052 — Public document convention v1

**Status**: ACCEPTED
**Date**: 2026-07-31
**Route**: STRUCTURED
**Decision**: Publish `docs/DOCUMENT_CONVENTION.md` as the sole public authority for `vbb-doc-v1`, preserve historical artifacts, and enforce active/adopted documents with `tools/vbb-document-convention-lint.py`.

## Context

The Release Readiness and Document Convention audits show that the existing documentary rules are practiced but dispersed, with duplicate legacy templates, incomplete metadata, unindexed taxonomies and no dedicated mechanical check.

## Decision

Vibe Backbone adopts a versioned, project-declarable contract named `vbb-doc-v1`. The contract defines document identity, metadata, types, status domains, tags, naming, relations, reading order, visibility/lifecycle, compatibility and migration. Active documents must declare the contract; historical runs retain their original meaning and are never backfilled.

## Consequences

- Third-party projects get one entry point and a deterministic validator.
- Current templates become the only supported template family; legacy copies are retained under an explicit deprecated namespace.
- Existing pre-convention history is evidence, not a failed current adoption.
- The repository's own migration report is a bounded document-convention result, not a release-readiness decision for unrelated blockers.

## Alternatives rejected

### Alternative A — Enrich `docs/INDEX.md` only

Rejected because navigation is not a contract and cannot carry the complete schema, compatibility rules and validator oracle without creating a second authority.

### Alternative B — Rewrite all historical runs

Rejected because it destroys provenance and conflicts with the audits' explicit historical-preservation requirement.

## References

- `docs/audits/document-convention-audit-rc1-20260731.md`
- `docs/audits/release-check-20260729-1902.md`
- `docs/DOCUMENT_CONVENTION.md`
- `tools/vbb-document-convention-lint.py`
