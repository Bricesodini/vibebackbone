---
status: accepted
date: 2026-08-26
document_convention: vbb-doc-v1
type: adr
visibility: public
tags: [adr, governance, bootstrap, agents]
adr_id: "0055"
decision_status: accepted
decision_makers:
  - "Brice — explicit implementation authorization"
---

# ADR 0055 — Repository-local AGENTS.md operational bootstrap

**Status**: ACCEPTED
**Date**: 2026-08-26

## Context

VBB installs provider-level governance, but did not define a portable,
observable handoff to a repository-local `AGENTS.md` before session state and
mission classification. A local repository can consequently have operating
rules that are visible in Git without being part of the declared bootstrap.

## Decision

VBB treats an applicable `AGENTS.md` as a repository-local **operational
contract**, not as repository governance. Before interpreting `SESSION.md` or
classifying a mission, an agent discovers the contract in the launch directory
and then, when different, the effective Git root. It does not search arbitrary
parents. The contract may name bounded sources needed to understand the
repository, but it cannot change VBB route selection, gates, assurance,
closeout, or Core↔distribution rules.

The discovery reports presence, loadability, canonical path and Git state.
Tracked, modified and untracked contracts are all readable; provenance is
reported rather than silently used as a trust decision. An unreadable contract,
or an external symlink stops the bootstrap. A clause that purports to alter VBB
governance is non-applicable and reported; it never silently changes the VBB
process.

## Consequences

- Session entrypoints must run the generic discovery before `SESSION.md`.
- Provider adapters receive the same Core rule; no consumer or Studio-specific
  path is added.
- The protocol is deterministic and does not mechanically infer semantic
  conflicts in arbitrary prose; it gives local prose no authority over the VBB
  process.

## Alternatives rejected

- Git-root-only discovery: it misses an explicitly launched nested scope.
- Recursive parent search: it makes unrelated parent governance implicit.
- Ignoring untracked files: it defeats the safety purpose of the local contract.

## Risks

| Risk | Mitigation |
|---|---|
| Provider bypasses the protocol | Anchor the rule in every entrypoint and test the Core tool. |
| Local prose attempts to govern VBB | Treat the clause as non-applicable and make it visible. |
| Symlink escapes repository | Refuse external targets. |
