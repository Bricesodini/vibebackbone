---
run_id: "2026-08-03_worktree-documentary-audit"
artifact_kind: "historical_run_inventory"
status: "HISTORICAL_EVIDENCE_ONLY"
canonical: false
source_state: "origin/main@c8c513d3d5700fcd8ce46660b4ad9b4fb5c78343"
---

# Historical run index

This index versions the fifteen previously untracked documentary runs found
in the detached worktree. It is an archival inventory, not a closeout and not
a certification of any run. The runs are preserved without retroactive
completion of missing governance phases.

| Run | Qualification | Disposition | Current authority |
|---|---|---|---|
| `2026-08-02_canon-adoption-revision` | PROPOSAL_NON_ADOPTED | Preserve as adoption-revision evidence | None |
| `2026-08-02_document-graph-model` | PROPOSAL_NON_ADOPTED | Preserve as superseded design evidence | None; canonical DGM is on main |
| `2026-08-02_document-identity-model` | PROPOSAL_NON_ADOPTED | Preserve as superseded design evidence | None; canonical DIM is on main |
| `2026-08-02_document-model-adoption` | PROPOSAL_NON_ADOPTED | Preserve as adoption planning evidence | None |
| `2026-08-02_document-model-implementation-strategy` | PROPOSAL_NON_ADOPTED | Preserve as implementation design evidence | None |
| `2026-08-02_document-model-integration-plan` | PROPOSAL_NON_ADOPTED | Preserve as integration design evidence | None |
| `2026-08-02_document-model-proof-of-architecture` | HISTORICAL_EVIDENCE | Preserve as PoA evidence | Not a current certification |
| `2026-08-02_document-model-reference-architecture` | PROPOSAL_NON_ADOPTED | Preserve as superseded architecture evidence | None; published reference is on main |
| `2026-08-02_document-tag-specification` | PROPOSAL_NON_ADOPTED | Preserve as superseded DTS evidence | None; published DTS is on main |
| `2026-08-02_documentary-cleanup-living-core-pilot` | HISTORICAL_EVIDENCE | Preserve as pilot findings | Not a current state report |
| `2026-08-03_document-model-canon-integration` | HISTORICAL_EVIDENCE | Preserve as completed-plan evidence | Superseded by publication on main |
| `2026-08-03_f03-governance-alignment` | HISTORICAL_EVIDENCE | Preserve as F-03 investigation evidence | Not current governance |
| `2026-08-03_f03-governance-remediation` | HISTORICAL_EVIDENCE | Preserve as F-03 remediation evidence | Not current governance |
| `2026-08-03_f03-provenance-alignment` | HISTORICAL_EVIDENCE | Preserve as blocked F-03 evidence | Not current governance |
| `2026-08-03_f03-revision` | HISTORICAL_EVIDENCE | Preserve as blocked F-03 evidence | Not current governance |

## Invariants

- The published Documentary Contract v1 on `main` remains the only current
  authority.
- These runs are not canonical merely because they are versioned here.
- Missing run phases remain missing; this index does not close or certify
  them.
- No runtime, distribution, release, or deployment state is certified by
  this archive.
