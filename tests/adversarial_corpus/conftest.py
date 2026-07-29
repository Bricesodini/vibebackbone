"""Corpus-local pytest configuration.

Pre-merge gate 5b (`docs/REFERENCE/pre-merge-gate.md`) runs

    python -m pytest tests/adversarial_corpus/ -q

as a separately reported check. While no CONFIRMED adversarial finding has been
registered, that directory holds no test and pytest exits 5
(``EXIT_NOTESTSCOLLECTED``), which breaks the gate's `&&` chain and makes the
canonical block unrunnable.

An empty corpus is a legitimate state — it means no CONFIRMED finding is
outstanding — so this hook maps exit 5 to exit 0 **for corpus-only runs**.

This is not a way to pass with no coverage. The obligation "every CONFIRMED
finding has a corpus entry" is carried by ``tests/test_corpus_mandatory.py`` in
the main suite: if a CONFIRMED finding exists without its entry, that test
fails, and an empty corpus stops being legitimate. Genuine corpus failures still
exit 1 and are untouched here.
"""

from pathlib import Path

EXIT_NO_TESTS_COLLECTED = 5
CORPUS_DIR = Path(__file__).parent.resolve()


def _targets_corpus_only(session) -> bool:
    """True when every collection argument points inside the corpus directory.

    Guards against neutralising exit 5 for a whole-suite run that happened to
    collect nothing; only an explicit corpus-scoped invocation is covered.
    """
    args = [str(arg).split("::", 1)[0] for arg in session.config.args]
    if not args:
        return False
    for arg in args:
        try:
            resolved = Path(arg).resolve()
        except (OSError, ValueError):
            return False
        if resolved != CORPUS_DIR and CORPUS_DIR not in resolved.parents:
            return False
    return True


def pytest_sessionfinish(session, exitstatus):
    if exitstatus != EXIT_NO_TESTS_COLLECTED:
        return
    if session.testscollected:
        return
    if _targets_corpus_only(session):
        session.exitstatus = 0
