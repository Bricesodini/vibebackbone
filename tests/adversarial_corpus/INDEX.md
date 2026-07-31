# Adversarial corpus index

Entries registered under `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §9,
destination 6: **mandatory for every `CONFIRMED` finding, no exception**, the
matrix applying regardless of severity.

Lifecycle, entry format, quarantine and promotion are owned by
`skills/t-vbb-adversarial-corpus/SKILL.md`.

## Entry states

- `ACTIVE` — regression guard for a remediated finding, backed by a
  `fails_before` / `passes_after` lock.
- `BEHAVIOUR_PIN` — the finding is CONFIRMED but **not remediated**. There is no
  lock to encode, so the entry pins the current defective behaviour: it fails the
  day the defect changes, forcing the finding to be re-arbitrated and the entry
  rewritten as a real guard. A green run never means "fixed".
- `QUARANTINED` — retained for traceability, excluded from active execution.
- `PROMOTED` — superseded by a canonical test in `tests/`.

## CORPUS-ADVR-RT-01

- **Origin**: `docs/runs/2026-07-30_0100_a2-auth-certification-of-m3-remediation/`
- **Severity**: S3
- **Oracle**: `adv-block-exists` reports PASS, with the reason "adversarial block
  is a non-empty mapping", for a block whose value is `None`.
- **Added**: 2026-07-29
- **State**: BEHAVIOUR_PIN

## CORPUS-ADVR-RT-02

- **Origin**: `docs/runs/2026-07-30_0100_a2-auth-certification-of-m3-remediation/`
- **Severity**: S3
- **Oracle**: `level: '  A2  '` validates silently; the padding is stripped rather
  than rejected or reported.
- **Added**: 2026-07-29
- **State**: BEHAVIOUR_PIN

## CORPUS-ADVR-RT-03

- **Origin**: `docs/runs/2026-07-30_0100_a2-auth-certification-of-m3-remediation/`
- **Severity**: S3
- **Oracle**: CERTIFIED condition 6.3.10 (`revocation_mechanism declared`) is
  listed in the canon and enforced by no `gate_id`.
- **Added**: 2026-07-29
- **State**: BEHAVIOUR_PIN

## Provenance

The three entries above were created on 2026-07-29 to bring the repository into
conformity with §9 as it already stands. This is **not** a rule change and not an
arbitrary backfill: the three findings were `CONFIRMED` in the run that granted
the A2 certification, and §9 required an entry for each of them at that moment.

If the obligation on S3 findings proves unjustified in use, the way to change it
is a `CANON_CHANGE_PROPOSAL` amending §9 — not a silent narrowing of the rule to
match the implementation.

## CORPUS-A2-GP-01

- **Origin**: `docs/runs/2026-07-29_1834_governance-principles/06_INDEPENDENT_REVIEW_A2.md#A2-GP-01`
- **Severity**: S1
- **Oracle**: historical identity remains A2/S1/CONFIRMED/CLASSIFIED
- **Added**: 2026-07-31
- **State**: BEHAVIOUR_PIN

## CORPUS-A2-GP-02

- **Origin**: `docs/runs/2026-07-29_1834_governance-principles/06_INDEPENDENT_REVIEW_A2.md#A2-GP-02`
- **Severity**: S1
- **Oracle**: historical identity remains A2/S1/CONFIRMED/CLASSIFIED
- **Added**: 2026-07-31
- **State**: BEHAVIOUR_PIN

## CORPUS-A2-GP-03

- **Origin**: `docs/runs/2026-07-29_1834_governance-principles/06_INDEPENDENT_REVIEW_A2.md#A2-GP-03`
- **Severity**: S1
- **Oracle**: historical identity remains A2/S1/CONFIRMED/CLASSIFIED
- **Added**: 2026-07-31
- **State**: BEHAVIOUR_PIN

## CORPUS-FIND-RR-BK-05

- **Origin**: `docs/runs/2026-07-31_1530_rr-bk-05-readiness-fidelity/`
- **Severity**: S1
- **Oracle**: canonical dashboard risk-header parsing retains RR-BK-03
- **Added**: 2026-07-31
- **State**: ACTIVE
