---
run_id: "2026-07-29_1941_run1-exact-release-measurement"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "codex"
started_at: "2026-07-29T19:41:32+02:00"
ended_at: "2026-07-29T19:45:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md"
  - "docs/adr/0046-readiness-integrity-enforcement.md"
  - "docs/adr/0051-adversarial-assurance-dimension.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Run 1 exact release measurement

## Demande reçue

Execute only Run 1, “Make release measurement exact and honest”, from a clean
and isolated `origin/main` baseline. The authorized findings are `RR-BK-02` and
`RR-BK-03`; `F9` is included only if strictly required to prevent two
resolutions of the same release subject.

## Reformulation

Make release verification bind to one explicit `run_id` and Git SHA, and make
the dashboard include every active risk so no open P0, P1 or P2 can yield a
measured `READY`. Do not revisit the release `NO_GO` decision or start Run 2.

## Isolation Git

```yaml
git_isolation:
  method: "temporary clone created directly from the configured origin remote"
  historical_workspace: "/Users/bricesodini/01_ai-stack/vibebackbone"
  isolated_clone: "/tmp/vbb-run1-Uhlfod/repo"
  branch: "codex/run1-exact-release-measurement"
  base_sha: "6b0daf4785d652b23931b80aafba57979e69d9b4"
  origin_main_sha: "6b0daf4785d652b23931b80aafba57979e69d9b4"
  baseline_status: "clean"
```

The historical workspace is read-only for this run. No file, index, branch or
untracked artifact from that workspace is imported into the clone.

## Scope

### In scope

- `RR-BK-02`: exact release subject (`run_id` plus expected Git SHA);
- negative selection cases: missing, wrong and future-selected runs;
- release closure blocking on the explicit subject;
- `RR-BK-03`: exact extraction of the canonical active-risk table;
- measured `BLOCKED` for open P0/P1 and measured non-`READY` for open P2;
- `F9` only if path/ID ambiguity can select or report a different subject;
- coherence tests for Core, local CI and GitHub gate command surfaces;
- four-distribution smoke verification without adapter redesign;
- bounded A2 falsification of subject substitution, risk masking and false
  `READY`.

### Out of scope

- the `NO_GO` release decision;
- historical governance-principles runs or their corpus obligations;
- versions, changelog, release checklist, tags or release candidates;
- `F11`, `F12`, `F13`, provider research and all vNext work;
- Run 2 or any release publication.

### Dependencies detected

- shared resolution: `tools/vbb_run_resolution.py`;
- release-relevant gates: `tools/vbb-adversarial-gate.py` and
  `tools/vbb-loop-closure-check.py`;
- readiness measurement: `tools/vbb-status-dashboard.py`;
- command coherence: `scripts/vbb-ci-local.sh`,
  `.github/workflows/vbb-contracts.yml` and
  `docs/REFERENCE/pre-merge-gate.md`;
- accepted design authorities: ADR 0027, ADR 0046 and ADR 0051.

## Classification du risque

- **Level**: `HIGH`
- **Reason**: this changes governance gate behavior used by release and all four
  supported distributions.

## Voie recommandée

- **Route**: `STRUCTUREE`
- **Reason**: A2 gate behavior, multiple Core consumers and published
  operational contracts are affected.

## Handoff vers `04_PLAN`

- Read the three accepted ADRs, the POC, the integration gate and the affected
  tests before implementation.
- Stop if the POC is not `GO` or `can_code_start` is not `true`.
- Do not convert a failed negative proof into a documented exception.

## Assurance initiale

- Applicable gates: `DESIGN` (`RUN1-EXACT-SUBJECT`,
  `RUN1-RISK-MEASUREMENT`), `ADVERSARIAL` (`RUN1-A2-FALSIFICATION`) and
  `CERTIFICATION` (`RUN1-COMMAND-COHERENCE`).
- Target checkpoint: `PRE_IMPLEMENTATION`.
- Implementation authorized at intake: `NO`.

Liée à ADR: `docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md`

POC reference:
`docs/runs/2026-07-29_1941_run1-exact-release-measurement/POC.md`

## Adversarial level

```yaml
adversarial_level:
  level: "A2"
  level_reason: "Release and governance gate behavior is an A2 trigger."
  contest_register: []
defender_identity:
  agent: "codex"
  llm: "gpt-5"
  provider: "openai"
  system_prompt_version: "codex-desktop-2026-07-29"
  session: "current"
```

The distinct attacker identity will be published by the review actor. The
implementer cannot self-declare `PASS_ADVERSARIAL`.

## Certification status

```yaml
certification_status:
  declared_status: "PRE_CERTIFICATION"
  transient_reason: "Run 1 implementation has not started and A2 review is pending."
  bootstrapped_at: "2026-07-29T17:41:32Z"
  bootstrapped_by: "codex"
```
