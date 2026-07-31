---
run_id: "2026-07-31_1630_rr-bk-04-release-identity-remediation"
phase: "06_REVALIDATION_PACKET"
route: "AUDIT"
status: "PREPARED_NOT_EXECUTED"
candidate_sha: "58e51eeebfd057a359eb78393ce16d6df4a05cf3"
---

# RR-BK-06 — exact-SHA independent revalidation packet

This packet is rebound exactly to `CANDIDATE_SHA=58e51eeebfd057a359eb78393ce16d6df4a05cf3`.
It is prepared for a distinct independent actor and is not executed by this
run.

## Exact subject preflight

```bash
EXPECTED_COMMIT=58e51eeebfd057a359eb78393ce16d6df4a05cf3
git clone --no-local <repository> /tmp/vbb-independent-revalidation
git -C /tmp/vbb-independent-revalidation checkout --detach "$EXPECTED_COMMIT"
test "$(git -C /tmp/vbb-independent-revalidation rev-parse HEAD)" = "$EXPECTED_COMMIT"
```

## Blocking gates

```bash
RUN_ID=2026-07-31_1630_rr-bk-04-release-identity-remediation
EXPECTED_COMMIT=58e51eeebfd057a359eb78393ce16d6df4a05cf3

python tools/vbb-architecture.py lint
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py "$RUN_ID" \
  --expected-commit "$EXPECTED_COMMIT" --strict
python tools/vbb-adversarial-gate.py "$RUN_ID" \
  --expected-commit "$EXPECTED_COMMIT" --strict
python -m pytest tests/adversarial_corpus/ -q
python -m pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

The independent actor must also confirm exact-SHA remote CI and verify that
`v1.1.0-rc.1` does not yet exist. The future tag check is `PENDING_RELEASE_OWNER`,
not PASS, until the authorized release owner creates it after READY.

## Machine-readable release identity

```yaml
release_identity:
  tuple: "R=(V,S,C,T,P)"
  V: "1.1.0-rc.1"
  S: "58e51eeebfd057a359eb78393ce16d6df4a05cf3"
  C:
    package_json_version: "1.1.0-rc.1"
    changelog_heading: "## [1.1.0-rc.1] — 2026-07-31"
    checklist_version: "1.1.0-rc.1"
    checklist_candidate_sha: "58e51eeebfd057a359eb78393ce16d6df4a05cf3"
  T:
    name: "v1.1.0-rc.1"
    kind: "annotated"
    message: "Release v1.1.0-rc.1"
    creation_command: "git tag -a v1.1.0-rc.1 58e51eeebfd057a359eb78393ce16d6df4a05cf3 -m \"Release v1.1.0-rc.1\""
    peeled_commit: "58e51eeebfd057a359eb78393ce16d6df4a05cf3"
    created: false
  P:
    status: "FUTURE_CONTRACT_ONLY"
    created: false
    subject: "A separate post-tag evidence carrier commit"
    required_contents:
      - "tag name and exact tag object SHA"
      - "peeled commit SHA equal to S"
      - "V and full S"
      - "immutable tag verification output"
    forbidden: "Do not move T or replace S"
```

## Verdict authority

Only the distinct independent actor may issue a certification verdict for
RR-BK-06. This packet itself makes no such claim.

