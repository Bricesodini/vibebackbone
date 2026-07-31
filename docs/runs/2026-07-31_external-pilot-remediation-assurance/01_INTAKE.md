---
run_id: "2026-07-31_external-pilot-remediation-assurance"
phase: "01_INTAKE"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "run_artifact"
visibility: "internal"
status: "ready"
tags: [run, audit, documentation, governance, contract, security]
relations:
  - "../../DOCUMENT_CONVENTION.md"
  - "../../ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "../../runs/2026-07-31_vbb-doc-v1-external-pilot/07_CLOSEOUT.md"
route: "STRUCTURED"
voie: "STRUCTUREE"
agent: "Codex"
started_at: "2026-07-31T12:00:00Z"
ended_at: "2026-07-31T12:45:00Z"
artifacts_produced: ["01_INTAKE.md", "POC.md", "04_PLAN.md"]
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.2"
adversarial_level: "A2"
attacker_identity:
  agent: "Codex"
  llm: "GPT-5"
  system_prompt_version: "Codex desktop 2026-07-31"
  distinct_actor: "A2_DISTINCT_AGENT_PROXY"
---

# Intake — External Pilot Remediation and Assurance Alignment

## Goal

Consume and independently revalidate every finding in the Backbone Know
external-pilot run; remediate only confirmed RC blockers in `vbb-doc-v1`; and
version a compatible A2/A3 assurance clarification without rewriting historical
runs or declaring release readiness.

## Scope boundary

- Backbone Know is read-only evidence; no file under `/Users/bricesodini/02_dev/Backbone-know` is modified.
- The prior pilot run is append-only evidence.
- This run may change the Vibe Backbone document contract, its linter/tests,
  assurance canon/gates/tests, and this run's evidence.
- No full public-documentation migration and no RC readiness claim.

## Classification

This is `STRUCTURED` with an `AUDIT` component: it changes a published
contract, validator behavior, assurance semantics, tests, and historical-run
interpretation. Effective adversarial level is `A2`; the subject is canon,
published contracts, and gates. A2 proxy mode is used because no genuinely
distinct human actor is available in this session.

## Required decision boundary

The A2/A3 clarification is proposed as a versioned compatibility change. It
may be adopted only with the explicit governance decision recorded in the new
ADR and must be accepted by the human decision-maker before it is called
canonical. Existing v1.1 runs retain their original meaning.

## Pre-existing workspace changes

The source workspace contains unrelated uncommitted changes and untracked
artifacts from completed work. They are outside this worktree and untouched.

## Linked POC

`docs/runs/2026-07-31_external-pilot-remediation-assurance/POC.md`
