# Canon Change Proposal — Gate documentation coherence

- Status: APPROVED
- Human validation: Brice, message `go`, 2026-07-13
- Scope: wording-only alignment of existing executable behavior
- Canon touched: `GUIDE.md`, `docs/templates/INTEGRATION_GATE.md.template`
- Behavior change: none; implemented and tested in R1
- Distribution placement: Core, per `docs/DISTRIBUTIONS.md` decision log

## Proposed change

Document `SUPERSEDED` as an accepted ADR status, add AUDIT to the eligible
template lanes, and state explicitly that PIVOT is blocking.

## Rejected alternative

Leave the prose divergent from the executable gate. Rejected because it would
preserve two competing contracts.
