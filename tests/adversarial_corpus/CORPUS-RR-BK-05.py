"""Active regression guard for FIND-RR-BK-05.

Origin: docs/runs/2026-07-31_1530_rr-bk-05-readiness-fidelity/
Severity: P1
State: ACTIVE (PASS_REVALIDATED on SHA 58e51ee)

RR-BK-05 invariant: the corpus shipped with the candidate SHA
contains tests for FIND-RR-BK-05.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_DIR = REPO_ROOT / "tests" / "adversarial_corpus"


def test_corpus_contains_rr_bk_05_entry():
    """The shipped corpus must contain a RR-BK-05 entry."""
    candidates = list(CORPUS_DIR.glob("CORPUS-*RR-BK-05*.py"))
    assert candidates, "No CORPUS entry for RR-BK-05 found in shipped corpus"


def test_corpus_entry_is_valid_python():
    """Each CORPUS-RR-BK-05 file must be syntactically valid Python."""
    import ast

    candidates = list(CORPUS_DIR.glob("CORPUS-*RR-BK-05*.py"))
    assert candidates
    for f in candidates:
        source = f.read_text()
        ast.parse(source)  # raises SyntaxError if invalid
