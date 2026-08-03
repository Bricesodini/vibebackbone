---
run_id: 2026-08-03_f03-governance-remediation
route: STRUCTURED
adversarial:
  level: A2
  attacker_identity:
    agent: "Meitner"
    llm: "independent subagent"
    system_prompt_version: "bounded-a2-review"
    session: "019fc4a8-02b8-79b0-a5c9-5901e8a6bb48"
  defender_identity:
    agent: "Codex"
    llm: "primary agent"
    system_prompt_version: "current-session-governance"
  campaign_ref: docs/runs/2026-08-03_f03-governance-remediation/ADVERSARIAL_CAMPAIGN.md
  corpus_version: "not_applicable_static_document_review"
  exploration_performed: true
  surfaces_declared:
    - counter-proof wording at docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:347-349
    - compatibility with ADR-0053
  surfaces_unexplored:
    - all other governance sections
    - validators and runtime behavior
    - candidate documentary model
    - main integration and publication
  verdict: PASS_ADVERSARIAL
  residual_uncertainty: "The campaign covers only the authorized passage; it does not certify the worktree or other governance surfaces."
  non_claim: "A declared attack surface was exercised at a declared depth by a declared actor, and no unremediated confirmed finding remains within that scope. Absence of finding is bounded evidence, never proof."
  findings: []
status: closed
conformity_status: PASS_CONFORMITY
adversarial_status: PASS_ADVERSARIAL
certification_status: PRE_CERTIFICATION
verdict: F03_CLOSED
---

# F03-GOVERNANCE-REMEDIATION — Closeout

```yaml
adversarial:
  level: A2
  attacker_identity:
    agent: "Meitner"
    llm: "independent subagent"
    system_prompt_version: "bounded-a2-review"
    session: "019fc4a8-02b8-79b0-a5c9-5901e8a6bb48"
  defender_identity:
    agent: "Codex"
    llm: "primary agent"
    system_prompt_version: "current-session-governance"
  campaign_ref: docs/runs/2026-08-03_f03-governance-remediation/ADVERSARIAL_CAMPAIGN.md
  corpus_version: "not_applicable_static_document_review"
  exploration_performed: true
  surfaces_declared:
    - counter-proof wording at docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:347-349
    - compatibility with ADR-0053
  surfaces_unexplored:
    - all other governance sections
    - validators and runtime behavior
    - candidate documentary model
    - main integration and publication
  verdict: PASS_ADVERSARIAL
  residual_uncertainty: "The campaign covers only the authorized passage; it does not certify the worktree or other governance surfaces."
  non_claim: "A declared attack surface was exercised at a declared depth by a declared actor, and no unremediated confirmed finding remains within that scope. Absence of finding is bounded evidence, never proof."
  findings: []
```

## Verdict

`F03_CLOSED`

The confirmed F03 drift was corrected in the authorized passage only. The
wording now distinguishes v1.2 A2 operational isolation, v1.1 historical
distinct-actor semantics, and A3 strengthened external independence.

No merge, push, tag, publication, adoption, or unrelated source modification
was performed. The pre-existing dirty worktree and convention-lint
precondition remain explicitly outside this run's remediation scope.
