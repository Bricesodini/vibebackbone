# v1.1.0 Release Candidate Checklist

**Version**: `1.1.0-rc.2`
**Candidate subject**: technical metadata commit; exact SHA is recorded in
the isolated run evidence carrier after commit
**CANDIDATE_SHA**: <recorded in `docs/runs/2026-08-01_1200_rc2-candidate/evidence/raw/00_candidate_sha.txt` after the candidate commit exists>
**Future annotated tag**: `v1.1.0-rc.2`
**Status**: Candidate preparation — independent revalidation pending
**Supersedes**: `v1.1.0-rc.1` (SHA `58e51ee`) for evidence traceability (see CHANGELOG §1.1.0-rc.2)

This checklist is the release-facing contract for `V=1.1.0-rc.2`. The exact
40-character candidate SHA is carried by the run evidence artifact once the
technical subject commit exists; no document in that subject commit may
contain its own final SHA.

## Release identity

- [x] `package.json.version` is exactly `1.1.0-rc.2`
- [x] `CHANGELOG.md` contains exactly one current `1.1.0-rc.2` release section
  (and one `[1.1.0-rc.1]` section marked superseded)
- [x] Candidate subject is the commit containing only the necessary release
  metadata changes (6 corpus entries + temporal provenance update + version
  bump + changelog + checklist)
- [ ] Evidence carrier records the exact full `CANDIDATE_SHA`
- [ ] Future tag `v1.1.0-rc.2` is created only after independent READY
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
- [ ] RR-BK-06 package is rebound to the exact candidate SHA (and resolved by
  a genuinely distinct actor — see `04_DECISION_REGISTRY.md` §brice_decision)

## Prohibited before independent revalidation

- create or move `v1.1.0-rc.2`;
- create `P`;
- push, merge, publish, or claim certification.

## Provenance notes

- The `docs/TEMPORAL_PROVENANCE.md` `updated` field has been re-anchored to
  `2026-08-01` in this candidate to resolve F8.
- The 6 adversarial-corpus entries (RR-BK-02, RR-BK-03, RR-BK-05, RR-BK-06,
  F8, F9) are part of the candidate commit, not local-only files.
- No governance artefacts (REVISE-C v3, CC-11 refactor v2) have been modified
  in this candidate.
