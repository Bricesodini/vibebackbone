# ADR 0049 — Engineering knowledge governance

**Status**: ACCEPTED
**Date**: 2026-07-27
**Route**: AUDIT
**Décideurs**: Brice (explicit final approval), Codex (recording)
**Liée à**: ADR 0029, ADR 0031
**Liée à POC**: `docs/runs/2026-07-27_1612_engineering-knowledge-governance/POC.md`

## Contexte

Vibe Backbone governs the path from intent to qualified delivery through
architecture decisions, contracts, implementation, tests, independent review
and closeout. It does not explicitly govern reusable engineering knowledge
created by that work.

Patterns, anti-patterns, qualification methods, test strategies and development
practices can therefore remain conversational, be promoted on plausibility, or
be copied into the wrong documentary authority. The absence of a lifecycle
also leaves no general non-regression rule for knowledge that has already
become canonical.

## Décision proposée

Add a distinct engineering-knowledge governance loop to Vibe Backbone Core.

The delivery cycle keeps its seven phases. Every formal closeout performs a
Knowledge Harvest and records one disposition:

- `NONE`;
- `OBSERVATION_RECORDED`;
- `EVIDENCE_LINKED`.

An observation selected for maturation opens a separate knowledge run using
the existing phases:

```text
Observation
→ Candidate
→ Evidence accumulation
→ Knowledge audit
→ Independent review
→ Human decision
→ Validated
→ Canonical integration
```

The maturity states are:

1. **OBSERVATION** — one contextual fact, non-reusable and non-normative;
2. **CANDIDATE** — an explicit reusable hypothesis with claimed scope, limits,
   owner, evidence and disconfirmation conditions;
3. **VALIDATED** — the hypothesis is supported by independent validations in
   the claimed scope, a reproducible qualification method, counter-evidence
   search and mandatory independent review;
4. **CANONICAL** — a human has approved promotion, impact and migration are
   bounded, and the rule has moved to exactly one final authority.

Independence is demonstrated, not inferred from project count. The evidence
dossier must distinguish independence of context, implementation or author,
qualification method and underlying assumptions. The required diversity grows
with the scope claimed.

Promotion is never automatic. The audit author and independent reviewer cannot
jointly replace the human decision maker.

The knowledge record is never authoritative. Once promoted, it retains the
history and links to the final authority; it does not repeat the normative
rule.

Canonical knowledge is immutable. Any correction, weakening, extension or
replacement starts a new Observation and traverses the complete lifecycle. The
new canonical version explicitly supersedes the previous one; the old version
remains traceable.

Patterns and anti-patterns use the same lifecycle. An anti-pattern additionally
requires evidence of the recurring failure mechanism and a bounded corrective
alternative when one is known.

## Conséquences

### Positives

- Delivery quality and method improvement become two explicit governed loops.
- Plausible advice is separated from demonstrated reusable knowledge.
- Independent review prevents a knowledge audit from becoming its own
  authority.
- Scope-aware evidence avoids both weak project counting and unjustified
  universal claims.
- Promotion preserves one canonical authority and prevents documentary drift.
- Canonical knowledge gains ADR-like non-regression and supersession.

### Négatives / coûts

- Formal closeouts gain one mandatory disposition.
- Knowledge candidates require evidence maintenance and ownership.
- Promotion to broad scopes becomes deliberately slower.
- Tools and tests need a compatibility strategy for historical runs.

### Neutres

- The seven phases and their numbering remain unchanged.
- Historical runs remain evidence and are not retroactively rewritten.
- No technology, framework, database or project-specific rule enters Core.

## Alternatives rejetées

### Alternative A — Add phase 08 CAPITALIZATION

- **Description** : append a new canonical phase after closeout.
- **Pourquoi rejetée** : breaks the seven-phase contract, tooling and the
  invariant that `07_CLOSEOUT` is the last artefact.

### Alternative B — Store learnings only in closeouts

- **Description** : treat closeouts as the reusable knowledge base.
- **Pourquoi rejetée** : makes evidence artefacts normative and creates
  fragmented parallel truth.

### Alternative C — Promote after audit without independent review

- **Description** : let the knowledge auditor recommend directly to the human.
- **Pourquoi rejetée** : the audit becomes its own quality authority and
  violates the separation principle already used for implementation.

### Alternative D — Require two different projects

- **Description** : make project count the universal independence criterion.
- **Pourquoi rejetée** : project boundaries do not prove independence of
  contexts or assumptions.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Knowledge bureaucracy with little reuse value | moyenne | moyen | Harvest is lightweight; full records exist only for selected observations |
| False independence between similar validations | moyenne | fort | Require an explicit independence profile and reviewer challenge |
| Rule duplicated between record, playbook and standard | moyenne | fort | Final-authority field; promoted record retains links, not normative text |
| Historical closeouts fail new validation | faible | fort | Backward-compatible enforcement and no retroactive mutation |
| Automatic promotion emerges through tooling | faible | fort | Tools may validate evidence shape, never decide promotion |

## Hypothèses

- Existing phase semantics can host a separate knowledge run.
- Human maintainers remain the final authority for canonical promotion.
- Independence can be reviewed through explicit dimensions without a universal
  numeric project threshold.

## Références

- Audit : `docs/runs/2026-07-27_1612_engineering-knowledge-governance/02_AUDIT.md`
- Impact : `docs/audits/impact-analysis-engineering-knowledge-governance-20260727-1612.md`
- POC : `docs/runs/2026-07-27_1612_engineering-knowledge-governance/POC.md`
- Proposal : `docs/runs/2026-07-27_1612_engineering-knowledge-governance/CANON_CHANGE_PROPOSAL.md`

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: GOUVERNANCE
reversible: true
depends_on:
  - docs/runs/2026-07-27_1612_engineering-knowledge-governance/POC.md
blocks:
  - Core engineering-knowledge governance integration
supersedes: []
verified_at: "2026-07-27T15:12:21Z"
verified_by: "Brice"
verified_method: "audit + GO POC + independent Review Run 02 + explicit final human approval"
```
