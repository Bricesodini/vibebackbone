---
document_convention: "vbb-doc-v1"
version: "1.0"
type: "reference"
status: "active"
visibility: "public"
tags: [documentation, governance, contract]
relations:
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "tools/vbb-document-convention-lint.py"
---

# Vibe Backbone Document Convention v1

This document is the public, versioned contract for documents that claim
adoption of Vibe Backbone document convention `vbb-doc-v1`. It is standalone:
a project may adopt it without knowing Vibe Backbone's history.

## 1. Identity and adoption

The official identity is `vbb-doc-v1`; its initial semantic release is `1.0`.
A project adopts it by creating `.vbb/document-convention.yaml`:

```yaml
document_convention: vbb-doc-v1
version: "1.0"
adoption: adopted
scope:
  roots:
    - docs/DOCUMENT_CONVENTION.md
    - docs/templates
  excludes:
    - docs/archive
    - docs/runs/*
  historical_before: "2026-07-31"
waivers:
  - path: docs/legacy/example.md
    reason: migration wave 2
    expires: "2026-09-30"
```

`adoption: adopted` is a claim about the declared scope only. The declaration
must be committed, and `python tools/vbb-document-convention-lint.py <root>` is
the reference check. A third-party project may choose different roots, but it
must not omit the declaration, the convention reference document, or the
validator result from its adoption evidence.

Scopes are progressive. `scope.roots` may contain several independently
adopted roots, and `waivers` may temporarily exclude a named path or glob only
when a non-empty reason and expiry are recorded. A waiver is an explicit
migration gap, not a conformance claim for the waived file. The validator
checks the active scope and `--suggest-scope` lists Markdown files outside it
so a maintainer can expand adoption deliberately.

## 2. Document types

The v1 types are: `reference`, `governance`, `run_artifact`, `audit_report`,
`decision_record`, `adr`, `template`, `adoption`, `migration_report`, and
`historical`. A document has exactly one primary type. `historical` is a
lifecycle classification, not a permission to use a historical document as
current authority.

## 3. Minimum metadata

Every active adopted Markdown document has YAML frontmatter with:

```yaml
document_convention: vbb-doc-v1
version: "1.0"
type: reference            # one v1 type
status: active              # valid in the type's status domain
visibility: public          # public | internal | experimental
tags: [documentation]      # non-empty, from the v1 vocabulary
relations: []               # explicit list; required even when empty
```

`run_artifact` additionally requires `run_id` and `phase`. `audit_report`
requires `run_id`, `route`, `subject`, and `verdict`. `adr` requires `adr_id`
and `decision_status`. `adoption` requires `adoption: adopted` and `scope`.
Templates may use placeholders for content fields, but their metadata must be
complete and machine-readable.

## 4. Status domains

`status` is type-specific; values must not be mixed across domains.

| Type | Allowed status values |
|---|---|
| reference, governance, adoption | `active`, `draft`, `deprecated`, `frozen` |
| template | `active`, `deprecated`, `experimental`, `frozen` |
| run_artifact | `ready`, `partial`, `blocked`, `unknown` |
| audit_report | `ready`, `partial`, `blocked`, `unknown` |
| decision_record, adr | `proposed`, `accepted`, `rejected`, `superseded` |
| migration_report | `ready`, `partial`, `blocked`, `unknown` |
| historical | `historical` |

Other status dimensions remain named dimensions: audit severity (`P0`-`P3`),
adversarial severity (`S0`-`S3`), knowledge maturity, gate verdict and debt
status. They must use qualified keys such as `severity`, `gate_verdict` or
`knowledge_maturity`, never overload document `status`.

Project-specific compound status semantics remain explicit through an optional
`status_extensions` list whose values must use the `project:status:<value>`
namespace. The primary `status` stays in the v1 type domain; the extension
preserves project meaning without silently redefining the contract domain.

## 5. Initial tag vocabulary

The initial controlled tags are:
`documentation`, `governance`, `contract`, `reference`, `template`, `review`,
`run`, `audit`, `decision`, `adr`, `migration`, `adoption`, `public`,
`internal`, `experimental`, `deprecated`, `frozen`, `historical`, `release`,
`architecture`, `security`, `quality`, `distribution`.

Tags are lowercase kebab-case. Project-local tags must use a namespace such as
`project:payments`; an unknown unnamespaced tag is invalid.

The `project:` namespace is the supported vocabulary bridge for domain tags
such as `project:role:product-brief`, `project:phase:phase_0`, and
`project:domain:research`. New shared/canonical tags require a versioned
contract decision; a consumer project does not need to wait for that decision
to preserve local business vocabulary.

## 6. Naming

Use lowercase kebab-case for slugs and `UPPER_SNAKE_CASE.md` for phase artifacts.
Runs use `docs/runs/YYYY-MM-DD_HHmm_slug/`. ADRs use `docs/adr/NNNN-slug.md`.
Templates use `<name>.md.template`; the old `*_TEMPLATE.md` family is
deprecated and must not be referenced by adoption declarations or new runs.
Audit reports use `<subject>-YYYYMMDD-HHMM.md`.

## 7. Relations and canonical reading order

`relations` contains repository-relative paths or stable IDs. Required links:
an adoption declaration links to this contract; a run artifact links to its
intake or parent run; an audit links to its evidence; a decision/ADR links to
the audit or POC that triggered it; a migration report links to the source
audit and the validator output. Missing required relations are errors.

Read in this order when orienting in an adopted project:
1. adoption declaration;
2. this contract;
3. project context and mode;
4. pilotage/routing;
5. architecture and conventions;
6. active decision/ADR and audit evidence;
7. run artifacts and closeout;
8. historical/archive material only as evidence.

## 8. Lifecycle and visibility

`public` is safe for external readers; `internal` is project-operational;
`experimental` is explicitly non-authoritative. `deprecated` remains readable
but must point to its replacement. `frozen` is authoritative but changeable
only through a versioned decision. `historical` is immutable evidence and must
not be used as the current source of truth. An active document cannot be
classified `historical`, and a historical document cannot silently claim
`active`.

## 9. Compatibility and migration

v1 readers accept only `vbb-doc-v1` version `1.x`; unknown major versions are
incompatible and fail closed. A future v2 must publish a migration guide and
declare whether it is backward-compatible. Migration is additive: declare the
new version, map statuses/tags/types, validate the active scope, then switch
the adoption declaration. Historical artifacts retain their original version;
they are never rewritten. A migration report records source version, target
version, scope, exclusions, unresolved gaps, and validator output.

## 10. R1-R8 resolution map

R1: legacy templates carry explicit `deprecated` metadata and redirect text.
R2: current phase templates 02-06 include all governance versions.
R3: machine-facing keys and controlled values are English; narrative language
is declared per document, removing ambiguity from the contract.
R4: this file is the unified public authority.
R5: audit reports use the standard metadata and `AUDIT_REPORT.md.template`.
R6: status and tag taxonomies are mapped above by type and domain.
R7: loose artifacts are excluded only when explicitly historical or outside the
adopted scope; no active loose artifact may masquerade as a run artifact.
R8: relations and canonical reading order are explicit above and checked by the
linter.

## 11. Conformance result

The conformance claim for any project is the tuple `(declaration, scope,
validator version, validator result, commit)`. This document alone never
proclaims conformance; the validator must be run on the claimed repository.
