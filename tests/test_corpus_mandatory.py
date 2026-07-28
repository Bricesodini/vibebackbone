"""ADVERSARIAL_ASSURANCE §9 destination 6 — corpus mandatory.

Verifies that every CONFIRMED finding must produce a corpus entry.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_corpus_mandatory_for_confirmed():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # §9 row 6 must say "MANDATORY" or equivalent
    assert "corpus" in authority.lower()
    # Destination 6 row
    assert "Mandatory" in authority or "MANDATORY" in authority


def test_six_destinations_listed():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # §9 must enumerate 6 destinations
    section = authority.find("## §9")
    assert section != -1, "§9 section missing"
    chunk = authority[section : section + 5000]
    # Count numbered rows (destination rows start with "1." through "6.")
    import re

    # The destinations are numbered 1..6 with a destination column.
    rows = re.findall(r"^\|\s*\d+\s*\|", chunk, re.MULTILINE)
    # Or use the "Destination" heading rows
    if not rows:
        rows = re.findall(r"^\d+\.\s", chunk, re.MULTILINE)
    assert len(rows) >= 6, f"expected ≥ 6 destination rows, found {len(rows)}"


def test_corpus_skill_exists():
    skill = _read("skills/t-vbb-adversarial-corpus/SKILL.md")
    assert "corpus" in skill.lower()
    assert "CONFIRMED" in skill


def test_corpus_directory_exists():
    """The corpus directory is created as part of the v1.1 contract."""
    corpus_dir = REPO_ROOT / "tests" / "adversarial_corpus"
    assert corpus_dir.is_dir(), "tests/adversarial_corpus must exist"
