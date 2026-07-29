# Adversarial regression corpus

Canonical location of the adversarial regression guards required by
`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §9 destination 6: every `CONFIRMED`
adversarial finding must be registered here as a permanent regression guard.

Entry format and lifecycle (creation, versioning, quarantine, execution) are
owned by `skills/t-vbb-adversarial-corpus/SKILL.md`.

## Why this directory is tracked

This directory must exist in every clone. Git does not track empty directories,
so `.gitkeep` is committed alongside this file.

Between `3d2eeee` (2026-07-28) and `f8850ca` (2026-07-29) the directory existed
only on developer machines. `tests/test_corpus_mandatory.py::test_corpus_directory_exists`
therefore passed locally and failed on every CI run for eight consecutive
commits on `main` — including the run that published the v1.1 assurance campaign
as `CERTIFIED`. Do not remove `.gitkeep`, and do not let this directory become
untracked again.
