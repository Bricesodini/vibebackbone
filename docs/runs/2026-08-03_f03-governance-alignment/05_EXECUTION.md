# F03-GOVERNANCE-ALIGNMENT — Evidence

## Scope

Only the three authorized artifacts and the root `SYSTEM.md` symlink were
read. No source artifact was modified.

## Normative comparison

ADR-0053, lines 36–40, defines v1.2 as operational isolation for A2 and
strengthened independent actor control for A3. It states that model/provider
are disclosure metadata and that v1.1 runs retain their historical semantics.

The governance document's v1.2 preamble, lines 20–42, repeats that split and
defines A2 operational-isolation evidence. Its §1 table, lines 85–90, also
labels the v1.2 A2 actor requirement as operational isolation.

## Exact residual clauses

1. `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:347-349`:
   every A2 counter-proof is required to be produced by a `distinct actor`.
   The clause is inside the general PASS_ADVERSARIAL conditions and has no
   v1.1 qualifier or v1.2 exception.

2. `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:410-411`:
   certification of an A2 subject requires a human decision record, or the
   `A2_DISTINCT_AGENT_PROXY` contract. The proxy alternative is not limited
   to v1.1 in this certification condition.

3. `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:423-425`:
   every confirmed A2 finding requires `witnessed_by` distinct from
   `discovered_by` and a second-agent-or-human test review. This is stated as
   a general certification condition, without a v1.1 qualifier.

## Analysis

The v1.1 compatibility profile is explicitly scoped at lines 229–234 and
defines the distinct-agent proxy for v1.1 runs. That scope does not grammatically
extend to the unqualified conditions above. Therefore those conditions impose
distinct-actor or second-review requirements on v1.2 A2 as well, while ADR-0053
assigns strengthened external independence to A3 and makes actor/provider
identity metadata for A2.

The discrepancy is not caused by `SYSTEM.md`: its lines 79–106 correctly
describe v1.2 A2 operational isolation and v1.1 historical semantics. The root
`SYSTEM.md` is a symlink to `distributions/pi/SYSTEM.md` and therefore carries
the same text.

## Determination

This is a real documentary governance drift in the v1.2 document, not a false
positive. The exact affected clauses are the three ranges listed above. No
correction is executed in this run.

