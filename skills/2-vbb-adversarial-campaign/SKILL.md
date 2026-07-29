---
name: 2-vbb-adversarial-campaign
description: |
  Orchestrate adversarial campaigns (A1/A2) on a declared subject by composing technique
  skills into one contracted campaign producing findings, non-regression locks, and a
  `PASS_ADVERSARIAL` verdict or refutation. Use when a deliverable or canon requires
  adversarial assurance per `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.2.
  Keywords: adversarial, campaign, falsification, attack, A1, A2, PASS_ADVERSARIAL,
  A2_DISTINCT_AGENT_PROXY, attacker_identity, non_regression_lock.
context_role: adversarial-campaign-orchestrator
phase: "execution+verification"
status: "active"
version: "1.1"
adr: "0051"
adversarial_level: A2
canonical_authority: "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
template: "docs/templates/ADVERSARIAL_CAMPAIGN.md.template"
finding_template: "docs/templates/FINDING.md.template"
referenced_by:
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md §1 (levels)"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md §3 (A2 contract)"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md §5.2 (PASS_ADVERSARIAL)"
  - "tools/vbb-adversarial-gate.py (validator)"
  - "docs/templates/ADVERSARIAL_CAMPAIGN.md.template"
related_skills:
  - "1-vbb-security (technique provider)"
  - "1-vbb-systemic-risk (technique provider)"
  - "1-vbb-error-handling-auditor (technique provider)"
  - "1-vbb-monolith-detector (technique provider)"
  - "1-vbb-pattern-inconsistency-detector (technique provider)"
---

# 2-vbb-adversarial-campaign — Adversarial campaign orchestrator

## ROLE & POSTURE

Orchestrate an adversarial campaign against a declared subject at a declared
level (A0/A1/A2). Compose existing technique skills into a contracted campaign;
produce a campaign record via `docs/templates/ADVERSARIAL_CAMPAIGN.md.template`
and zero or more findings via `docs/templates/FINDING.md.template`.

This skill is the **orchestrator**. The technique skills (security,
systemic-risk, etc.) are **providers**; this skill sequences them and holds the
campaign contract together.

Posture: the campaign exists to falsify, not to confirm. A campaign that finds
nothing must say what it exercised and what it did not, and never convert that
silence into a claim of correctness.

## INPUT CONTRACT

| Input | Required | Source |
|---|---|---|
| Subject under campaign | yes | upstream run or task brief |
| Declared level | yes | intake's `adversarial_level.level` |
| Declared scope | yes | intake or upstream |
| Corpus version | yes | t-vbb-adversarial-corpus |
| Available techniques | yes | existing 1-vbb-* and 2-vbb-* skills |

## BLOCKING CONDITIONS

Stop and escalate rather than proceed when:

- the declared level is contested and cannot be resolved — fall back to `A1`, the
  more prudent direction, and record the fallback;
- the subject is A2 and no actor distinct from the defender is available, and
  `A2_DISTINCT_AGENT_PROXY` cannot be honoured with its three identity
  disclosures — declare the absence, do not simulate independence;
- `surfaces_unexplored` would be empty, which would assert exhaustive coverage;
- `python tools/vbb-adversarial-gate.py <run_dir> --strict` fails;
- a CONFIRMED finding cannot be given a `fails_before`/`passes_after` lock.

## SCOPE

Use when:

- A delivery or canon must be subjected to adversarial assurance at A1 or A2
  (cf. `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.2 triggers).
- A `CERTIFIED` claim is being prepared (requires `PASS_ADVERSARIAL` or
  `NOT_REQUIRED` per §5.3 condition 6.3.2).
- A specific risk class triggers A2 (auth, secrets, data integrity, canon, etc.).

Do **not** use for:

- A0 subjects (no campaign required).
- Routine verification that is not adversarial (use phase 06 review profiles
  instead).

## PROCESS

### 1. Confirm the level

Re-validate the declared level against the criticality matrix (`§1.2`). If the
level is contested, fall back to `A1`.

### 2. Publish the campaign record

Open `docs/runs/<slug>/ADVERSARIAL_CAMPAIGN.md` using the template. Declare:

- `surfaces_declared` — the surface to be exercised.
- `attack_classes` — the techniques to invoke.
- `depth_bound` — total effort budget, parallel actors, stop criteria.
- `surfaces_unexplored` — explicit list, non-empty.

For A2, publish `attacker_identity` with the three disclosures.

### 3. Execute techniques

Invoke technique skills (security, systemic-risk, etc.) against the declared
surface. Each invocation is bounded by `depth_bound`. Stop when `stop_criteria`
is met or budget is exhausted.

### 4. Record findings

For each issue, open a finding via `docs/templates/FINDING.md.template`. Assign:

- `severity` (S0..S3)
- `confidence` (CONFIRMED, PLAUSIBLE, REFUTED)
- `state` (one of the 17 lifecycle states)
- `reproduction` (steps, expected, observed, oracle)
- For CONFIRMED: `non_regression_lock` with `fails_before: true` and
  `passes_after: true`.

### 5. Validate

Run `python tools/vbb-adversarial-gate.py <run_dir> --strict` to verify the
campaign record and findings against the validator.

### 6. Emit verdict

See `## VERDICT RULES`.

### 7. Promote confirmed findings

For each CONFIRMED finding, route the six destinations per
`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §9. Destination 6 (corpus entry) is
mandatory and is written to `tests/adversarial_corpus/` via
`t-vbb-adversarial-corpus`.

## OUTPUT CONTRACT

| Output | Required | Destination |
|---|---|---|
| Campaign record | yes | `docs/runs/<slug>/ADVERSARIAL_CAMPAIGN.md` |
| 0+ findings | conditional | `docs/runs/<slug>/findings/FIND-*.md` |
| Corpus entries | yes (for CONFIRMED) | `tests/adversarial_corpus/` |
| Verdict | yes | campaign record + 07_CLOSEOUT.md |

> The corpus destination is `tests/adversarial_corpus/`, the directory executed
> by pre-merge gate 5b. An earlier revision of this skill pointed it at
> `docs/adversarial_corpus/`, which has never existed — entries written there
> would have satisfied no check (audit 2026-07-29, finding F17).

## VERDICT RULES

The campaign emits one of:

- `PASS_ADVERSARIAL` — every finding is in a terminal state or S3, no CONFIRMED
  S0/S1 is unremediated (and no CONFIRMED S2 without ACCEPTED_RISK at A2), every
  PLAUSIBLE is promoted or refuted, every remediated finding carries a
  non-regression lock and a COUNTER_PROOF gate result.
- `FAIL_ADVERSARIAL` — at least one of the above fails.
- `IN_CAMPAIGN` / `FINDINGS_OPEN` — intermediate states.
- `NOT_REQUIRED` — when A0 is declared and no A1/A2 trigger fires.

`PASS_ADVERSARIAL` requires the mandatory non-claim attached to the verdict:

> a declared attack surface was exercised at a declared depth by a declared
> actor, and no unremediated confirmed finding remains within that scope. It does
> NOT mean the subject is correct, secure, or free of defects. Absence of finding
> is bounded evidence, never proof.

### Hard rules

1. **No closure without evidence.** A finding is `CLOSED_REMEDIATED` only when
   remediation *and* non-regression lock *and* `COUNTER_PROOF PASS` are present.
2. **Refuted findings are kept.** Negative evidence prevents re-litigation.
3. **A2 distinct actor.** The attacker identity at A2 must be distinct from the
   defender; the campaign cannot use the same agent+LLM as the implementation
   being reviewed.
4. **Corpus mandatory for CONFIRMED.** Every CONFIRMED finding must produce a
   corpus entry via `t-vbb-adversarial-corpus`.
5. **Promotion path.** Promotion to `CONVENTIONS.md` or `AGENTS.md` is forbidden
   without transit through ADR 0049 OBSERVATION → CANONICAL.

### Enforcement boundary

`tools/vbb-adversarial-gate.py` validates the *shape* of the adversarial block —
that a level, a campaign reference, a corpus version, declared surfaces and a
verdict are present and well-formed. It does not resolve a CONFIRMED finding to a
corpus entry; rule 4 is carried by `tests/test_corpus_mandatory.py`. Verify which
check carries an obligation before treating it as enforced.

## Non-claim

This skill orchestrates campaigns; it does not certify subjects. Certification
requires human decision per `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §5.3 condition
6.3.7.
