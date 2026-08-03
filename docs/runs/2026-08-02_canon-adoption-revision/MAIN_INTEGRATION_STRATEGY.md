---
run_id: 2026-08-02_canon-adoption-revision
phase: planning
status: proposed
---

# Main Integration Strategy

## Recommendation: a new integration branch from verified `origin/main`

Create a new branch from the remote SHA verified at run start, then port only
approved atomic lots. Do not rebase or merge the current detached worktree.

This preserves a readable main-facing history, avoids carrying an ambiguous
dirty worktree or unrelated registered worktrees, and makes rollback a normal
revert of a small published lot. It also retains the existing pilot commits as
auditable sources without treating their branch topology as authority.

| Option | Decision | Reason |
| --- | --- | --- |
| Rebase then merge | Not recommended | The candidate is detached and has both uncommitted remediation and proposal evidence; rebasing obscures the selective adoption boundary. |
| Merge main into current branch | Not recommended | Adds a merge commit without resolving the dirty-state, detached-HEAD, or duplicate-CR-16 problems. |
| Port selective lots alone | Necessary but insufficient | Provides atomicity, but must happen on a clean branch from the verified current main. |
| New integration branch from main | Recommended | Combines selective porting, a clean base, explicit review, and reversible commits. |

## Controlled sequence for the future run

1. Verify `origin/main` with `git ls-remote`; record its exact SHA as the
   integration anchor. If it differs from this report, repeat conflict and
   validation assessment before porting.
2. Create the integration branch from that SHA. Keep the present worktree and
   all source worktrees unchanged.
3. Port the approved lots in dependency order, using the source commits when
   they match the approved scope and reconstructing only the explicitly
   approved uncommitted remediation/evidence as new atomic commits.
4. Resolve A-01 as an independent minimal correction before declaring the
   living-core remediation validated.
5. Validate each lot locally, then validate their accumulated candidate using
   DIM → Ontology → DGM → DTS → DTP, repository linters, and the full suite.
6. Require the human adoption decision before creating the dedicated canonical
   contract/ADR lot. Do not tag, push, merge, or publish distributions without
   separate authorization.

## Final integration lots

| Lot | Sources and files | Dependencies | Required validation | Rollback | Separately integrable |
| --- | --- | --- | --- | --- | --- |
| 1. Model foundations as evidence | The seven conceptual-model run directories | None | Markdown/convention checks; evidence review | Revert evidence commit only | Yes, but does not adopt a contract. |
| 2. C0-C5 validation capability | `64bb43e`, `6beae84`, `f3035f6`: validator, its pilot tests/fixtures, pilot run evidence | Lot 1 only if the evidence must travel together; technically independent | Pilot tests, positive/negative/UNKNOWN fixtures, Ruff, compilation | Revert C0-C5 commits in reverse order | Yes, as experimental/internal capability. |
| 3. Documentary-skill alignment | `668e3e0`: four skills, test, alignment run evidence | Lot 2 | Alignment tests plus C0-C5 tests | Revert the skill-alignment commit | Yes after Lot 2; skills remain consumers, not canonical model definitions. |
| 4. Living-core correction | Approved F-01/F-02/F-03/F-05 edits, cleanup-pilot evidence, and the A-01 next-action repair | A-01 must pass; CR-16 port exactly once | Focused dashboard test, full suite, applicable governance/document validation, source/projection check | One revertable remediation commit; do not rewrite ADR 0051 | Yes after A-01, but it is not model adoption. |
| 5. Canonical adoption and contract | Approved canonical documents, new dedicated adoption ADR, official validator/skill declarations if approved | Lots 1-4 and A-02 through A-07 | Full candidate validation, governance/adversarial review, human adoption decision | Revert adoption commit; preserve ADR and evidence history | No: this is the adoption boundary. |
| 6. Historical evidence publication | Adoption, revision, and relevant historical run records | The lot they evidence | Link/provenance review, convention lint | Revert evidence-only commit | Yes, provided it makes no canon claim. |

The exact file list for Lot 5 cannot be fixed without the human canonical-boundary
decision (A-03/A-04); defining it now would pre-empt that decision.

## Merge and publication guard

The only eligible merge candidate is a clean integration branch whose tested
HEAD is anchored to a recorded remote-main SHA. Push, merge, tag creation, and
distribution publication remain separate human-authorized operations. A Pi
runtime claim is prohibited until the distinct L-02 runtime run completes.
