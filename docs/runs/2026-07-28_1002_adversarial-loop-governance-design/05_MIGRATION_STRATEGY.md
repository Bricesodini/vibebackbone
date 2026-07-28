---
run_id: "2026-07-28_1002_adversarial-loop-governance-design"
phase: "05_MIGRATION_STRATEGY"
voie: "AUDIT"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
design_version: "0.2"
agent: "claude-code"
started_at: "2026-07-28T09:05:00Z"
ended_at: "2026-07-28T10:05:00Z"
revised_at: "2026-07-28T10:05:00Z"
next_phase: "06_INDEPENDENT_REVIEW"
artifacts_consumed:
  - "02_AUDIT.md"
  - "03_DECISION.md"
  - "04_DESIGN_DOSSIER.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md"
  - "docs/DISTRIBUTIONS.md"
artifacts_produced:
  - "05_MIGRATION_STRATEGY.md"
---

# 05_MIGRATION_STRATEGY — Adopting adversarial assurance without invalidating baselines

> Proposal. No migration step is authorized by this run.

## 1. Migration principles

| # | Principle | Enforcement |
|---|---|---|
| P1 | **Additive only** | Schema `1.1` removes and renames nothing; v1.0 readers keep working |
| P2 | **Objective cutoff, not opt-in** | Reuse the ADR 0050 precedent: a run key and an ISO timestamp decide applicability |
| P3 | **No retroactive invalidation** | Pre-cutoff subjects are `UNASSESSED_LEGACY`, which is **not** `NOT_CERTIFIED` and **not** a failure |
| P4 | **Never rewrite history** | No existing run, audit, closeout or baseline is edited or reclassified |
| P5 | **Enforcement ramps, semantics do not** | The vocabulary and validator land together (D10); only the *blocking scope* is phased |
| P6 | **Consumers adopt through their own governed change** | Vibebackbone does not modify consumer repositories, per the assurance v1 precedent |
| P7 | **Reversible** | Rollback is "stop requiring the new fields"; no data migration to undo |

## 2. Phase plan

| Phase | Content | Route | Gate to the next phase |
|---|---|---|---|
| **M0 — Design** | This run: audit, decisions, design dossier, migration strategy, independent review | `AUDIT` | Human decision on the proposal |
| **M1 — Decision** | ADR `00XX`, `CANON_CHANGE_PROPOSAL`, human approval, four-distribution impact review (CR#12) | `AUDIT` → decision | ADR `ACCEPTED` |
| **M2 — Contract** | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (new single authority), schema `1.1`, templates, `tools/vbb-adversarial-gate.py` + tests, cutoff declaration | `STRUCTURED` | P.R2 loop green, independent review PASS |
| **M3 — Corpus bootstrap** | Seed the corpus from historical evidence (`docs/audits/`, resolved `AUDIT_STATUS` risks, remediation runs) as `origin: HISTORICAL` | `STRUCTURED` | Corpus executes green; no gate failure is created retroactively |
| **M4 — Enforcement ramp** | Advisory → blocking, by level (§4) | `STRUCTURED` | Measured false-block rate below the declared threshold |
| **M5 — Distribution propagation** | `pi`, `opencode`, `codex`, `claude`: prompts, skills, boot-set references; `DISTRIBUTIONS.md` §Decisions log | `STRUCTURED` | Runtime conformance checks pass on all four |
| **M6 — Consumer availability** | Documented adoption path; each consumer opens its own governed run | n/a | Per consumer |

M2 and M3 must not be merged: bootstrapping a corpus while the contract is
still moving would bind entries to a schema that may still change.

## 3. Legacy semantics

### 3.1 Cutoff rule

```yaml
adversarial_governance_version: "1.1"
cutoff_run_key: "<YYYY-MM-DD_HHmm of the M2 integration run>"
cutoff_timestamp: "<ISO8601 UTC of the M2 integration commit>"
```

- At or after the cutoff: formal runs with an intake or closeout declare
  `adversarial_governance_version` and carry a valid `adversarial` block, or
  a valid `A0` declaration.
- Before the cutoff: runs remain valid under their original protocol. Readers
  preserve legacy semantics when the block is absent.

### 3.2 The three legacy readings

| Situation | Status | Meaning |
|---|---|---|
| Pre-cutoff subject, never assessed adversarially | `UNASSESSED_LEGACY` | Neither certified nor failed. **No baseline is invalidated.** |
| Pre-cutoff subject, later re-assessed on request | Normal v1.1 statuses, bound to the *current* state | The old record is preserved; a new record is created |
| Post-cutoff subject with no adversarial block | `NOT_ASSESSED` → fail-closed | A contract violation, not a legacy case |

**The distinction between `UNASSESSED_LEGACY` and `NOT_CERTIFIED` is the core
anti-invalidation device.** A repository that adopts v1.1 does not wake up with
a red dashboard; it wakes up with an honest "not yet assessed" on everything
that predates the contract.

### 3.3 What legacy runs never trigger

- No re-opening of a closed run.
- No re-run of a historical gate.
- No downgrade of an existing `READY` baseline (e.g. the current
  `AUDIT_STATUS.md` global verdict).
- No retroactive finding creation. A defect discovered *today* in legacy code
  is a **new** finding with `detection_mode: EXPLORATORY` and today's run as
  its origin, not a retroactive failure of the run that shipped it.

## 4. Enforcement ramp

| Stage | Duration signal | `A2` subjects | `A1` subjects | `A0` declarations |
|---|---|---|---|---|
| **R0 — Advisory** | From M2 | Validator warns | Validator warns | Warn if missing |
| **R1 — A2 blocking** | After N ≥ 3 `A2` runs completed under R0 without validator defects | **Blocking** | Warn | Warn |
| **R2 — A1 blocking** | After the measured false-block rate on `A1` is below the declared threshold | Blocking | **Blocking** | Blocking (declaration required) |

**Grace rule [R:ADVR-09].** Enforcement applies to runs whose `run_id` is at or
after the stage's activation key. A run already in flight when a stage
activates completes under the previous stage. This prevents the ramp from
stalling work that started under different rules.

**Why `A2` first.** `A2` subjects are the lowest-volume and highest-consequence
population; blocking them first buys the most assurance for the least friction,
and produces the evidence needed to calibrate `A1`.

## 5. Bootstrap of the corpus (M3)

Sources, in priority order:

1. resolved findings recorded in `docs/audits/` reports;
2. risks that appeared and were closed in `docs/AUDIT_STATUS.md` history;
3. remediation runs whose review cycles (`06_REVIEW_RUN_0n`) closed a blocker;
4. designed hazards derived from the criticality matrix classes that have no
   historical finding yet (`origin: DESIGNED_HAZARD`).

Rules:

- Bootstrapped entries carry `origin: HISTORICAL` and the source path.
- A bootstrapped entry that **fails on import** creates a new, current finding
  through the normal lifecycle — it does not retroactively fail the run that
  originally closed the risk.
- The initial corpus version is `1.0`; every subsequent change bumps it, since
  the version participates in certification binding (§6.3.8 of the dossier).

## 6. Distribution propagation (M5, Critical Rule 12)

| Distribution | Surface touched | Promote-or-keep |
|---|---|---|
| `pi` | `SYSTEM.md` posture reference, prompts | Generic rule → Core |
| `opencode` | Agent profile boot set | Generic rule → Core |
| `codex` | Agent profile boot set, conformance fixtures | Generic rule → Core |
| `claude` | `CLAUDE.md` entry point, skills index | Generic rule → Core |

Only the *invocation glue* stays in `distributions/`; the levels, statuses,
verdict conditions and finding schema are Core. Both directions are recorded in
`docs/DISTRIBUTIONS.md` §Decisions log.

## 7. Risks of the migration itself

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| MR-01 | **Process theater** — campaigns written to satisfy the gate, with shallow attack lists | S1 | Reproductions must be executable oracles; `ADVERSARIAL_REVIEW` challenges the attack list, not the verdict (§9.3); empty-campaign signal tracked (§7.3) |
| MR-02 | **Enforcement drift** (repeat of W3) — vocabulary ships, validator does not | S1 | D10: validator ships in the same run as the schema |
| MR-03 | **Bureaucratic overload** on small changes | S2 | `A0`/`A1` levels; `A0` requires one declared line; corpus runs mechanically with no human cost |
| MR-04 | **Corpus rot** — entries quarantined or deleted to keep the suite green | S2 | Quarantine policy with owner, expiry and visibility; deletion requires risk-acceptance authority (§7.2) |
| MR-05 | **Certification staleness** — `CERTIFIED` claimed for a state that has moved | S2 | Certification bound to run + commit + corpus version; state divergence suspends the claim (§6.3) |
| MR-06 | **Two registers** — findings in records and in `AUDIT_STATUS.md` | S2 | `AUDIT_STATUS.md` becomes a view; single source rule (§5.4.3) |
| MR-07 | **Reviewer scarcity** in a solo-maintained repository — `A2` requires a distinct actor | S2 | A distinct *role and session* with a pre-registered attack list is the minimum; genuine actor independence is declared when unavailable, exactly as P.R8 requires today |
| MR-08 | **Level inflation** — everything classified `A2`, the ramp stalls | S3 | The matrix is trigger-based, not judgment-based; level and its `level_reason` are reviewable |

## 8. Rollback

| Trigger | Action |
|---|---|
| False-block rate above the declared threshold at any ramp stage | Return to the previous stage; keep the vocabulary |
| Systematic empty campaigns with no findings over N `A2` runs | Suspend `A1` enforcement, keep `A2`, re-examine the attack-list requirement |
| Schema defect discovered after M2 | Schema `1.2` through a new governed run; `1.1` records remain readable |
| Full abandonment | Stop requiring the new fields. Records already written stay valid and readable; nothing must be deleted or rewritten (P7) |

Rollback never deletes finding records or corpus entries: they are evidence,
and evidence survives the governance that requested it.
