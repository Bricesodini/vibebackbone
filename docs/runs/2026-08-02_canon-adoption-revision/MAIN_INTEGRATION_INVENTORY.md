---
run_id: 2026-08-02_canon-adoption-revision
phase: audit
status: active
---

# Main Integration Inventory

## Exact Git tuple observed on 2026-08-02

| Property | Observed value |
| --- | --- |
| Current worktree | `/Users/bricesodini/.codex/worktrees/3d91/vibebackbone` |
| Current branch | Detached `HEAD` |
| Current SHA | `668e3e09e1a2ad0575297278af9b88860420c39d` |
| Remote main SHA | `067b8ea6e9a7d9bea65a29340bdc38da1361f039` |
| Remote-main verification | `git ls-remote origin refs/heads/main` returns the same SHA |
| Commits reachable from HEAD but not main | 4 (`origin/main...HEAD`: `0 4`) |
| Upstream | Unavailable because HEAD is detached |
| Dry merge against current main | No textual conflict reported |
| Worktree state at review start | Dirty: 4 modified tracked files and 15 untracked Markdown files |
| Worktree state after this analysis | The same 4 modified tracked files, plus the 15 pre-existing untracked files and these 4 revision-run documents |

## Local commits since `origin/main`

| SHA | Subject | Classification | Scope |
| --- | --- | --- | --- |
| `64bb43e79bf8ce701e486a69c7cdf847eaf2ff0e` | `feat: add document model validation pilot c0-c2` | VALIDATION_CAPABILITY | C0 common result contract, C1 DIM/C2 Ontology validation, tests, fixtures, run evidence. |
| `6beae84021967f20b3708b6d873bbb19644ab45c` | `feat: extend document model pilot with dts and dgm` | VALIDATION_CAPABILITY | C3 DTS and C4 DGM extension, tests, fixtures, closeout evidence. |
| `f3035f64872a24e97420f05e2abe7b8e71687165` | `feat: add document transition finding routing pilot` | VALIDATION_CAPABILITY | C5 governed finding and decision-routing pilot, tests, fixtures, closeout evidence. |
| `668e3e09e1a2ad0575297278af9b88860420c39d` | `feat: align documentary skills with dtp routing` | SKILL_ALIGNMENT | Four documentary skills, alignment tests, bounded run evidence. |

`cc7ca86ebfef0e443980f5806db32c4351a1bb4d` (`governance: add governed
artifact drift rule`) is a relevant local source on
`codex/main-based-reconciliation`, not an ancestor of this detached HEAD. Its
Critical Rule 16 content is represented again in the current uncommitted
`AGENTS.md` remediation. It must be ported once, never twice.

## Modified, uncommitted, and evidence artefacts

| Group | Paths | Classification | Integration treatment |
| --- | --- | --- | --- |
| F-01 documentary remediation | `AGENTS.md` | DOCUMENTARY_REMEDIATION | Preserve as the single CR-16 port, after confirming it matches the approved text. |
| F-02 adversarial alignment | `distributions/pi/SYSTEM.md` | DOCUMENTARY_REMEDIATION | Separate source-level distribution correction; verify `SYSTEM.md` symlink/projection behaviour. |
| F-03 provenance correction | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | DOCUMENTARY_REMEDIATION | Preserve ADR 0051 history and make ADR 0053 the v1.2 alignment provenance. |
| F-05 navigation correction | `docs/CONTEXT.md` | DOCUMENTARY_REMEDIATION | Requires the separate next-action repair before this lot can pass its full suite. |
| Conceptual model material | Seven run directories: `document-identity-model`, `document-graph-model`, `document-tag-specification`, `document-model-integration-plan`, `document-model-implementation-strategy`, `document-model-reference-architecture`, `document-model-proof-of-architecture` | MODEL_FOUNDATION / EVIDENCE_ONLY pending adoption decision | Preserve as run evidence; do not promote merely by committing. |
| Cleanup pilot evidence | `docs/runs/2026-08-02_documentary-cleanup-living-core-pilot/` | EVIDENCE_ONLY | Commit only with the corresponding remediation lot after validation. |
| Adoption proposals | `docs/runs/2026-08-02_document-model-adoption/` | EVIDENCE_ONLY | Preserve as proposal material; no canonical effect. |
| This revision | `docs/runs/2026-08-02_canon-adoption-revision/` | EVIDENCE_ONLY | Commit as the read-only decision record if requested. |

No identified path is `UNRELATED` within this worktree’s visible change set.
Other registered worktrees and branches are out of this candidate and must not
be staged, removed, or treated as integration inputs without a separate human
decision.

## Predictable conflicts and constraints

1. **No present textual merge conflict:** current remote main is the merge
   base and the dry merge is clean.
2. **Duplicate CR-16 risk:** both `cc7ca86` and the uncommitted `AGENTS.md`
   hold the same responsibility. The integration branch must port exactly one
   representation.
3. **Current test contract conflict:** the F-05 edit removes the dashboard’s
   mandatory next-action input. This is the A-01 blocker, not a reason to
   discard the other remediation changes.
4. **Future-main risk:** any movement of remote main after this inventory can
   conflict in `AGENTS.md`, `docs/CONTEXT.md`, governance documents, skills,
   tests, or the validator. Re-verify the remote SHA immediately before port
   and again before merge.
