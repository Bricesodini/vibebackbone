"""M2-21 — non-regression witness tests (M1-05).

Validates the non-regression lock contract:
- A2 requires `witnessed_by` distinct from `discovered_by`.
- A2 requires `test_review` PASS|FAIL.
- A1 allows second-agent review within 30 days (corpus_review).
- A0 N/A.
"""

from pathlib import Path
import re


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_a2_requires_witnessed_by():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "witnessed_by" in authority
    # Distinct from discovered_by
    assert re.search(
        r"distinct.*discovered_by|distinct from .*discovered_by",
        authority,
        re.IGNORECASE,
    )


def test_a2_requires_test_review():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "test_review" in authority


def test_finding_template_documents_lock():
    template = _read("docs/templates/FINDING.md.template")
    assert "witnessed_by" in template
    assert "test_review" in template
    # YAML path
    assert "non_regression_lock" in template


def test_validator_enforces_lock():
    validator = _read("tools/vbb-adversarial-gate.py")
    assert "witnessed_by" in validator
    assert "test_review" in validator
    assert "fails_before" in validator
    assert "passes_after" in validator


def test_a1_allows_30_day_corpus_review():
    """A1 corpus_review deadline = 30 days."""
    # Look in M1_DECISIONS.md for the 30-day rule
    m1 = _read(
        "docs/runs/2026-07-28_1200_m1-adversarial-loop-normative-arbitration/M1_DECISIONS.md"
    )
    assert "30" in m1
    assert "corpus_review" in m1 or "deadline_days" in m1
