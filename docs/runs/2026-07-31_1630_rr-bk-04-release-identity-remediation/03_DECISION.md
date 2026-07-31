---
run_id: "2026-07-31_1630_rr-bk-04-release-identity-remediation"
phase: "03_DECISION"
voie: "AUDIT"
route: "AUDIT"
status: "READY"
agent: "codex/gpt-5"
started_at: "2026-07-31T16:40:00+02:00"
ended_at: "2026-07-31T16:42:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "02_AUDIT_REPORT.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — RR-BK-04

**CANDIDATE_SHA**: `58e51eeebfd057a359eb78393ce16d6df4a05cf3`

## Decision

The exact release candidate is `S=58e51eeebfd057a359eb78393ce16d6df4a05cf3`
with `V=1.1.0-rc.1`. RR-BK-04 is resolved structurally. RR-BK-06 is rebound
to the same SHA but remains intentionally not independently revalidated.

## Future tag contract

- `T`: annotated tag `v1.1.0-rc.1`.
- Message: `Release v1.1.0-rc.1`.
- Creation command, only after independent READY revalidation:

  ```bash
  git tag -a v1.1.0-rc.1 58e51eeebfd057a359eb78393ce16d6df4a05cf3 \
    -m "Release v1.1.0-rc.1"
  ```

- Required postcondition: `git rev-parse v1.1.0-rc.1^{commit}` equals the
  full SHA `58e51eeebfd057a359eb78393ce16d6df4a05cf3`.

## Future post-tag contract

`P` is a future, separate commit created only after `T` exists. It must record
the exact 40-character `CANDIDATE_SHA`, `V`, tag name, tag object SHA, peeled
commit SHA, creation command and immutable verification output. It must not
move or recreate `T`, modify the tagged subject, or be mistaken for `S`.

