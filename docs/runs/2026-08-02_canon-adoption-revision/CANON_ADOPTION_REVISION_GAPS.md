---
run_id: 2026-08-02_canon-adoption-revision
phase: audit
status: active
---

# Canon Adoption Revision Gaps

## Scope and fixed decision set

This review turns the prior `DOCUMENT_MODEL_CANON_ADOPTION_REQUIRES_REVISION`
verdict into the closed set below. It does not adopt the model, modify a
canonical authority, or alter Git history. A new condition may be added only
if a demonstrated blocker is found while resolving one of these conditions.

| ID | Adoption condition | Current state and available proof | Remaining gap | Blocking | Minimal action | Decision owner |
| --- | --- | --- | --- | --- | --- | --- |
| A-01 | All required validations are reproducibly green or explicitly governed as not applicable. | Architecture lint, contract lint (one pre-existing warning), convention lint, C0-C5 tests, Ruff, compilation, and `git diff --check` pass. The full suite reports `517 passed, 1 skipped, 1 failed`. | Resolve or explicitly govern the single dashboard failure, then rerun the full suite. | Yes | A separate one-file dashboard-contract correction lot, followed by the focused test and full suite. | Human adoption authority; tooling maintainer executes after approval. |
| A-02 | The candidate change set is clean, attributable, and reviewable. | `HEAD` is detached at `668e3e0`; four tracked files are modified and 15 run/model paths are untracked. | No clean candidate branch or atomic commit grouping yet exists. | Yes | Create a fresh integration branch from the verified remote main and port approved lots atomically; do not include unrelated worktrees. | Human integration authority. |
| A-03 | The canonical boundary of Documentary Contract v1.0 is explicitly approved. | The adoption plan proposes DIM, Ontology, DGM, DTP, DTS, and Reference Architecture as candidates; C0-C5 remains experimental/internal. | Human decision has not fixed what becomes canonical versus implementation-internal. | Yes | Approve or amend the proposed boundary before any canonical document or ADR change. | Human governance authority. |
| A-04 | The v1.0 contract adoption and its compatibility policy have an approved canonical home. | Proposal specifies no silent compatibility inference; no-contract is `UNKNOWN`; migration is DTP-governed. | No approved ADR/canonical contract change exists, and no ADR number is allocated. | Yes | Approve a dedicated adoption change, allocate a new ADR number, and keep ADR 0052 untouched. | Human governance authority. |
| A-05 | The living-core remediation is preserved as a separate, validated correction lot. | F-01/F-02/F-03/F-05 edits are present but uncommitted; their run evidence is untracked. F-04 and F-06 remain deferred. | The remediation has no atomic commit or final validation after the dashboard correction. | Yes | Commit only its four governed documents and its bounded run evidence after A-01 is resolved. | Human cleanup authority. |
| A-06 | Main compatibility is demonstrated against the remote state selected for integration. | `git ls-remote origin refs/heads/main` and local `origin/main` both resolve to `067b8ea6e9a7d9bea65a29340bdc38da1361f039`; `origin/main...HEAD` is `0 4`; a three-way dry merge reports no textual conflict. | Compatibility must be rerun from the new integration branch immediately before merge because main can change. | Yes at merge time | Fetch/verify the exact target SHA, port lots, and run the complete validation sequence on that branch. | Integrator with human merge authority. |
| A-07 | Publication and rollback are approved before any canonical release. | Publication plan orders commits, validations, tags, merge, and distribution publication; rollback avoids tag moves and identity rewrites. | It remains a proposal; no publication decision exists. | Yes | Human approval of the publication and rollback plan for the exact candidate SHA. | Human release authority. |
| L-01 | DTS scope covers the whole living core. | F-04 is an approved `PLUS TARD` debt; artefacts outside the interpretable scope stay `UNKNOWN`. | Scope expansion is deliberately deferred. | No for capability v1.0, yes for a claim of fully tagged living core | Preserve the debt and schedule a separate DTS-scope run. | Human documentary authority. |
| L-02 | Pi runtime is certified against the repository/distribution source. | F-06 is an approved `PLUS TARD` debt; no runtime observation is available. | No source-to-runtime comparison or from-scratch validation. | No for repository capability adoption; yes for runtime certification or deployment claim | Separate runtime anchoring, comparison, redeployment decision, and validation run. | Runtime owner. |
| L-03 | Documentation outside the bounded living core is cleaned. | Explicitly excluded from the first cleanup pilot. | No qualification or remediation decision outside scope. | No | Continue via later bounded DTP runs. | Human documentary authority. |
| L-04 | Git documentary tags exist. | No Git documentary tag has been designed or created. | Publication mechanism is deferred. | No for contract v1.0 adoption; yes if a tag is claimed as the adoption marker | Decide tag semantics and publish only in a separately approved release step. | Human release authority. |
| L-05 | The capability is deployed across multiple Vibe Backbone repositories. | Only this repository has a pilot capability. | No cross-repository migration evidence. | No | Run deliberately scoped external pilots after local adoption. | Human program authority. |

## Status dashboard failure: qualification and reproducible proof

**Finding A-01 is caused by the current documentary remediation, not merely
revealed by it.** The F-05 update to `docs/CONTEXT.md` removed its parseable
`- **Next action**:` line. `tools/vbb-status-dashboard.py` extracts
`next_action` only from that line shape, while
`tests/test_status_dashboard.py::test_next_action` requires a non-empty value.

Reproduce on the candidate worktree:

```text
python tools/vbb-status-dashboard.py --json
# "next_action": ""
python -m pytest tests/test_status_dashboard.py::test_next_action -q -vv
# FAILED: Expected non-empty next action
```

Baseline proof on the clean `main` worktree at the same remote SHA:

```text
cd /private/tmp/vbb-publish-rc2-2026-08-01_0752
python -m pytest tests/test_status_dashboard.py::test_next_action -q -vv
# PASSED
```

The failure is neither independent nor incompatible with the intended state:
`CONTEXT.md` is a navigation/anchoring document, and a concise current action
is compatible with that role. The minimal, separate repair is to restore one
truthful parseable next-action entry in `docs/CONTEXT.md`; it must not copy
canon or transition history. Altering the dashboard contract instead would be
a larger, separately justified tooling change.

## Exit condition

This review becomes ready for a main-integration run only when A-01 through
A-07 are resolved or have an explicit human disposition. L-01 through L-05
remain declared limitations and must not be misrepresented as completed work.
