---
context_role: impact-analysis
phase: 02_AUDIT
status: active
run_id: 2026-07-27_1612_engineering-knowledge-governance
updated: 2026-07-27
---

# Impact analysis — Engineering knowledge governance

## Change analyzed

Introduce a generic engineering-knowledge lifecycle linked to delivery
closeout, with evidence-based maturity, mandatory independent review,
human-controlled promotion, unique final authority and governed supersession.

## Direct impact

| Surface | Expected impact | Compatibility |
|---|---|---|
| `AGENTS.md` | Compact critical rule for Knowledge Harvest and governed promotion | Additive |
| `docs/AGENTIC_RUN_PROTOCOL.md` | Delivery loop hands off observations to a separate knowledge run | Additive; seven phases preserved |
| `docs/CONVENTIONS.md` | Evidence, authority and non-regression principles | Additive canon change |
| `docs/ARCHITECTURE.md` | New responsibility and relations in Governance Core/Audit Memory | Additive architecture change |
| `docs/templates/07_CLOSEOUT.md.template` | Required learning disposition | Template contract change |
| `prompts/canonical/07-p-vbb-closeout.md` | Ask the harvest question and prohibit promotion | Prompt behavior change |
| `GUIDE.md` | Explain the two loops and documentary boundaries | Additive |
| `docs/DISTRIBUTIONS.md` | Record Core placement and four-runtime impact | Additive decision log |

## Indirect impact

- `tools/vbb-loop-closure-check.py` may need a backward-compatible validation
  for new closeouts without invalidating historical runs.
- Tests must cover the template/prompt invariant and historical compatibility.
- `docs/INDEX.md`, `README.md` and architecture relations may need navigation
  updates.
- A knowledge-record template introduces a staging artefact that must remain
  explicitly non-authoritative.

## External impact

| Distribution | Impact |
|---|---|
| Pi | Inherits the Core closeout prompt and governance; no runtime-specific rule |
| OpenCode | Inherits the same Core semantics; generated command exposure must be checked |
| Codex | Compiled governance block must include the compact rule after setup |
| Claude | Core prompt/governance imports must expose the same lifecycle |

No provider-specific implementation is justified. The proposal belongs in
Core; adapters only propagate or expose it.

## Documentary responsibility impact

| Artefact | Sole responsibility after change |
|---|---|
| Knowledge governance | Lifecycle, roles, evidence gates and promotion rules |
| Engineering standard | Normative reusable rule: what is required |
| Playbook | Operational procedure: how to apply a practice |
| Contract | Verifiable obligations at a boundary |
| ADR | Rationale and consequences of a contextual decision |
| Guide | Non-normative explanation and navigation |
| Run/review/closeout | Evidence and disposition, never final authority |
| Knowledge record | Maturity and evidence history, never final authority |

## Final classification

**CONDITIONAL**

The design is additive and can preserve historical runs, but it changes Core
governance and closeout contracts. Integration is conditional on:

1. independent review of the complete proposal;
2. final human approval;
3. an accepted ADR and GO POC;
4. a backward-compatible enforcement strategy;
5. four-distribution propagation review.

## UNKNOWN areas

- Measured closeout friction after adoption.
- Whether a dedicated validator is necessary in v1 or can be deferred until
  a real promotion corpus exists.
- The minimum diversity profile for every possible claimed scope; the proposal
  therefore requires explicit independence arguments instead of a universal
  project count.
