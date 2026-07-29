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

## CORPUS-S1

- **Origin**: `docs/runs/2026-07-29_1130_gcg-genericity-stress-test/`
- **Severity**: S1
- **Oracle**: the compatibility scanner decides applicability from the run
  identity alone; the canonical enforcer combines three sources by `OR`. A
  subset of a disjunction can only under-report.
- **Added**: 2026-07-29
- **State**: BEHAVIOUR_PIN

## CORPUS-S2

- **Origin**: `docs/runs/2026-07-29_1130_gcg-genericity-stress-test/`
- **Severity**: S1
- **Oracle**: run identity carries no declared timezone; the corpus contains
  both the local-time and the UTC convention, two hours apart, against a
  six-hour debt window.
- **Added**: 2026-07-29
- **State**: BEHAVIOUR_PIN

## CORPUS-S3

- **Origin**: `docs/runs/2026-07-29_1130_gcg-genericity-stress-test/`
- **Severity**: S1
- **Oracle**: the Compatibility Act is mono-rule — one `rule_set`, one flat
  `counts`, one global ratio. It cannot represent one artifact judged by two
  rules.
- **Added**: 2026-07-29
- **State**: BEHAVIOUR_PIN

## CORPUS-S4

- **Origin**: `docs/runs/2026-07-29_1130_gcg-genericity-stress-test/`
- **Severity**: S1
- **Oracle**: no population contract; an undatable artifact is a blocking
  `UNKNOWN` instead of being out of population.
- **Added**: 2026-07-29
- **State**: BEHAVIOUR_PIN

## CORPUS-S5

- **Origin**: `docs/runs/2026-07-29_1130_gcg-genericity-stress-test/`
- **Severity**: S2
- **Oracle**: two divergent closeout resolvers; `2026-07-28_1200_m1` both has
  and has not a closeout depending on who asks.
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
