# v1.1.0 Release Candidate Checklist

**Version**: `1.1.0-rc.1`
**Candidate subject**: technical metadata commit; exact SHA is recorded in
the isolated run evidence carrier after commit
**CANDIDATE_SHA**: `58e51eeebfd057a359eb78393ce16d6df4a05cf3`
**Future annotated tag**: `v1.1.0-rc.1`
**Status**: Candidate preparation — independent revalidation pending

This checklist is the release-facing contract for `V=1.1.0-rc.1`. The exact
40-character candidate SHA is carried by the run evidence artifact once the
technical subject commit exists; no document in that subject commit may
contain its own final SHA.

## Release identity

- [x] `package.json.version` is exactly `1.1.0-rc.1`
- [x] `CHANGELOG.md` contains exactly one current `1.1.0-rc.1` release section
- [x] Candidate subject is the commit containing only the necessary release
  metadata changes
- [ ] Evidence carrier records the exact full `CANDIDATE_SHA`
- [ ] Future tag `v1.1.0-rc.1` is created only after independent READY
  revalidation and peels exactly to `CANDIDATE_SHA`
- [ ] Future post-tag commit `P` records the tag object, peeled commit,
  `CANDIDATE_SHA`, `V`, and immutable tag verification without moving the tag

## Blocking gates

- [ ] Fresh `git clone --no-local` is detached at the exact candidate SHA
- [ ] `python tools/vbb-architecture.py lint`
- [ ] `python tools/vbb-contract-lint.py`
- [ ] Explicit run closure and adversarial gates use the exact candidate SHA
- [ ] `python -m pytest tests/adversarial_corpus/ -q`
- [ ] `python -m pytest tests/ -q`
- [ ] `bash scripts/vbb-ci-local.sh`
- [ ] Exact-SHA remote CI is independently confirmed
- [ ] RR-BK-06 package is rebound to the exact candidate SHA

## Prohibited before independent revalidation

- create or move `v1.1.0-rc.1`;
- create `P`;
- push, merge, publish, or claim certification.
