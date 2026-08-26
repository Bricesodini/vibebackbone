---
run_id: "2026-08-26_local-agents-a2-remediation"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-08-26T00:00:00+02:00"
ended_at: "2026-08-26T00:00:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed: ["01_INTAKE.md", "POC.md", "INTEGRATION_GATE.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — local-agents-a2-remediation

## Objectif

Close the confirmed A2 findings without changing the bounded discovery model.

## Pré-conditions

- ADR 0055 is accepted.
- Remediation POC is GO.
- The initial A2 report is preserved as evidence.

## Autorisation d'implémentation

```yaml
implementation_authorization:
  status: "AUTHORIZED"
  required_gate_ids: ["LOCAL-AGENTS-ADR-0055", "LOCAL-AGENTS-REMEDIATION-POC"]
  reasons: ["Gate prerequisites are satisfied."]
```

## Étapes ordonnées

| # | Action | Validation |
|---|---|---|
| 1 | Check the resolved boundary before content access | malformed external symlink fixture |
| 2 | Preserve entry path and report its Git provenance | untracked symlink fixture |
| 3 | Update protocol wording | targeted test and documentation review |

## Plan de rollback global

Revert the dedicated remediation commit; no external runtime state changes.

## Risques identifiés

- Moving validation could alter normal internal-symlink behavior; retain an
  internal symlink regression test.
- Provenance fields could become ambiguous; document entry versus resolved path.

## Critères d'acceptation

- [ ] An invalid-UTF-8 external target returns `EXTERNAL_SYMLINK` before any
  content read.
- [ ] An untracked `AGENTS.md` symlink to a tracked in-root target reports
  `UNTRACKED` for the selected entry and a separate resolved target.
- [ ] Targeted tests, strict A2 gate, and loop closure pass.
