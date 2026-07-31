---
run_id: "2026-07-31_external-pilot-remediation-assurance"
phase: "05_EXECUTION"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "run_artifact"
visibility: "internal"
status: "ready"
tags: [run, contract, governance, security]
relations: ["02_AUDIT.md", "04_PLAN.md", "../2026-07-31_vbb-doc-v1-external-pilot/07_CLOSEOUT.md"]
route: "STRUCTURED"
adversarial_level: "A2"
voie: "STRUCTUREE"
agent: "Codex"
started_at: "2026-07-31T12:20:00Z"
ended_at: "2026-07-31T12:40:00Z"
artifacts_produced: ["05_EXECUTION.md"]
---

# Execution record

## Changes applied

- `docs/DOCUMENT_CONVENTION.md`: explicit progressive scope, expiring waivers,
  namespaced project vocabulary, and status extensions.
- `tools/vbb-document-convention-lint.py`: YAML declaration/frontmatter
  handling, exclusions/waivers, status-extension validation, and
  `--suggest-scope` guidance.
- `tests/test_document_convention.py`: real pilot-shaped status, waiver, and
  out-of-scope fixtures.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`: versioned v1.2 A1/A2/A3
  clarification; v1.1 semantics preserved.
- `tools/vbb-adversarial-gate.py`: v1.2 A2 isolation and A3 external
  independence checks, fail-closed; v1.1 compatibility retained.
- `docs/templates/01_INTAKE.md.template` and `07_CLOSEOUT.md.template`:
  declare A3 as a valid level.
- `tests/test_a2_a3_alignment.py`: A2 pass, missing isolation fail, A3
  external-independence fail, and historical v1.1 non-reinterpretation.
- `docs/adr/0053-a2-a3-assurance-alignment.md`: versioned decision record.

## Non-modification proof

No file under `/Users/bricesodini/02_dev/Backbone-know` was written. The
historical pilot run under `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/`
was not edited.

## Required scope demonstrations

- Minimal scope remains valid: document-convention fixture suite passes.
- Extended scope remains explicit: `--suggest-scope` reports candidate files;
  it does not silently claim them adopted.
- A waiver excludes only a named migration gap with reason and expiry.
- An A2 isolation fixture passes without an A3 claim.
- Missing isolation fails closed.
- Historical v1.1 profile is accepted without v1.2 checks.
