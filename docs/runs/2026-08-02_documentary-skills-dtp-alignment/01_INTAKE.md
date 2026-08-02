---
run_id: "2026-08-02_documentary-skills-dtp-alignment"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "ready"
agent: "codex"
started_at: "2026-08-02T00:00:00Z"
ended_at: null
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.2"
artifacts_produced:
  - "01_INTAKE.md"
  - "POC.md"
  - "07_CLOSEOUT.md"
---

# 01_INTAKE — Documentary skills DTP alignment

## Objective

Align only the four requested documentary skills with the experimental C0-C5
validator and Critical Rule 16. The skills must observe, qualify, request a
human decision and propose a route without executing remediation.

## Scope

In scope:

- `1-vbb-doc-harmonizer`;
- `1-vbb-code-doc-coherence-auditor`;
- `1-vbb-code-doc-gap-integrator`;
- `t-vbb-project-context-init`;
- focused behavioral contract tests and this run's evidence.

Out of scope:

- repository cleanup or mass classification;
- changes to canon, documents, tags or frontmatter;
- distributions, templates, workflows and other skills;
- migration, archive, deletion, push, tag or merge.

## Governance

- C5 basis: `DOCUMENT_TRANSITION_ROUTING_PILOT_READY`.
- Validator: `tools/vbb-document-model-validation.py` C0-C5 interface.
- Drift rule: Critical Rule 16; no silent correction.
- Human responses: `OUI`, `NON`, `PLUS_TARD`.
- An unknown or ambiguous fact remains `UNKNOWN`.

## Stop criteria

Stop if a skill infers authority from path/date/name, creates an authority
without a human decision, executes a route after `OUI`, introduces a parallel
model, or modifies an artefact outside the declared run evidence.
