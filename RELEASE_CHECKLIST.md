# v1.1.0 Release Checklist

**Version**: `1.1.0`
**Stable source**: `v1.1.0-rc.2` (SHA `3486300f359ff3b51effb007ed950dd48592556f`)
**STABLE_SHA**: <recorded in `docs/runs/2026-08-01_2200_v1-1-0-stable-promotion/evidence/raw/00_stable_sha.txt` after the stable commit exists>
**Future annotated tag**: `v1.1.0`
**Status**: Stable preparation — publishing pending independent approval
**Predecessor**: `v1.1.0-rc.2` (SHA `3486300f359ff3b51effb007ed950dd48592556f`)

This checklist is the release-facing contract for `V=1.1.0`. The exact
40-character stable SHA is carried by the run evidence artifact once the
stable commit exists; the diff between S_rc and S_stable is exclusively
documentary (version identity, changelog, release checklist, run evidence).

## Release identity

- [x] `package.json.version` is exactly `1.1.0`
- [x] `CHANGELOG.md` contains a current `1.1.0` release section (above the
  `1.1.0-rc.2` and `1.1.0-rc.1` sections)
- [x] Source: `v1.1.0-rc.2` (SHA `3486300f359ff3b51effb007ed950dd48592556f`)
- [ ] Evidence carrier records the exact full `STABLE_SHA`
- [ ] Future tag `v1.1.0` is created only after independent APPROVE
  decision and peels exactly to `STABLE_SHA`
- [ ] RC tag `v1.1.0-rc.2` remains immuable on the remote

## Stable gates (replayed on S_stable)

- [ ] `python tools/vbb-architecture.py lint`
- [ ] `python tools/vbb-contract-lint.py`
- [ ] `python tools/vbb-loop-closure-check.py <run_id> --strict`
- [ ] `python tools/vbb-adversarial-gate.py <run_id> --strict`
- [ ] `python -m pytest tests/adversarial_corpus/ -q`
- [ ] `python -m pytest tests/ -q`
- [ ] `bash scripts/vbb-ci-local.sh`
- [ ] Diff `S_rc..S_stable` contains 0 `FUNCTIONAL_CHANGE` files
- [ ] Tag `v1.1.0` absent locally and on remote before publication
- [ ] Installation from S_stable functional
- [ ] All 4 distributions syntax-checked

## Prohibited before publishing decision

- create or move `v1.1.0`;
- move or delete `v1.1.0-rc.2`;
- push the stable commit without independent approval;
- force-push anything.

## Provenance notes

- The stable commit `S_stable` is committed on branch
  `chore/v1.1.0-stable-promotion` (no rebase, no force-push).
- The diff between S_rc and S_stable MUST be classified as
  `VERSION_IDENTITY`, `RELEASE_DOCUMENTATION`, `RUN_EVIDENCE` —
  never `FUNCTIONAL_CHANGE`.
- Promotion run governance trace: `docs/runs/2026-08-01_2200_v1-1-0-stable-promotion/`.
