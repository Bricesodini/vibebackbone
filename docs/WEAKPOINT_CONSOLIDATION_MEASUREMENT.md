# Weakpoint consolidation — measurement and responsibility matrix

**Date**: 2026-07-14  
**Run**: `docs/runs/2026-07-14_0830_weakpoint-responsibility-routing/`  
**Decision**: ADR 0032 — responsibility-first, no skill fusion

## Measurement boundary

Text references are discoverability evidence, not execution telemetry. Historical
runs remain immutable and are excluded from any decision to retire a skill.
The useful measurement is therefore a combination of:

1. published contract identity and effects;
2. active references outside historical runs/audits;
3. strict top-1 routing on representative intentions;
4. full contract and CI verification.

Current inventory before and after this run: **64 skills, 64 contracts, 64
indexed contracts**. No skill is unreferenced on the measured active surface;
the lowest observed active-reference count is 2.

## Responsibility matrix

| Skill | Responsibility | Effect | Distinct contract evidence | Decision |
|---|---|---|---|---|
| `1-vbb-monolith-detector` | concentration and splitting | audit report | file metrics, fan-in, split plans | KEEP |
| `1-vbb-logic-duplication-detector` | duplicated business intent | audit report | semantic clusters, canonical source | KEEP |
| `1-vbb-pattern-inconsistency-detector` | cross-cutting pattern variants | audit report | variant distribution, migration map | KEEP |
| `1-vbb-premature-abstraction-detector` | abstraction cost/benefit | audit report | implementation counts, inline advice | KEEP |
| `1-vbb-code-doc-coherence-auditor` | code↔docs drift | read-only audit | coherence report, no fixes | KEEP |
| `1-vbb-code-doc-gap-integrator` | missing docs implementation | writes documentation | files created, commit-ready handoff | KEEP |
| `vibebackbone` | route classification | no code modification | route + next action | KEEP FIRST |

The code-doc pair cannot be merged without mixing read-only audit and repository
transformation. The four structural detectors share a family but not an output
contract; a multimode wrapper would add routing state rather than remove it.

## Routing corpus

| Intent | Expected skill | Baseline | Additive triggers |
|---|---|---|---|
| Detect god files and split monoliths | `1-vbb-monolith-detector` | ambiguous | PASS |
| Find duplicated business rules | `1-vbb-logic-duplication-detector` | `t-vbb-index` | PASS |
| Find inconsistent API call patterns | `1-vbb-pattern-inconsistency-detector` | `t-vbb-index` | PASS |
| Detect unnecessary interfaces/factories | `1-vbb-premature-abstraction-detector` | PASS | PASS |
| Audit code-documentation drift | `1-vbb-code-doc-coherence-auditor` | PASS | PASS |
| Write missing documentation | `1-vbb-code-doc-gap-integrator` | PASS | PASS |
| Classify task into correct route | `vibebackbone` | no match | PASS |
| Audit security controls | `2-vbb-security` | no match | PASS |

- Baseline: **3/8**.
- After targeted trigger additions: **8/8**, strict mode, zero ambiguity.
- Skill identities changed: **0**.
- Prompts/orchestrator rules changed: **0**.

## W1–W4 decision

| Weakpoint | Evidence | Decision in this run |
|---|---|---|
| W1 catalogue load | overlap exists, but responsibilities differ | matrix + trigger precision; no fusion |
| W2 routing indirection | router corpus exposes misses | keep mandatory triage; improve contracts |
| W3 declarative enforcement | credentials gap confirmed | separate AUDIT; no false closure |
| W4 consumer drift | TER-001 POC is NO-GO | remain deferred pending ownership design |
