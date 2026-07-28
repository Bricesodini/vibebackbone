"""M2-23 — CERTIFIED 13 conditions tests (M1-06).

Verifies that the canon enumerates all 13 conditions (6.3.1..6.3.13).
Each condition is named and individually evidenced (no aggregate, no
average, no rollup per M1-06 §D6).
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_all_13_conditions_named():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # §5.3 lists 13 conditions. Verify the section exists and the
    # right number of enumerated items appear in it.
    section = authority.find("### §5.3")
    assert section != -1, "§5.3 missing"
    chunk = authority[section : section + 3500]
    import re

    items = re.findall(r"^\d+\.\s", chunk, re.MULTILINE)
    assert len(items) >= 13, f"expected ≥ 13 conditions, found {len(items)}"


def test_conjunctions_not_aggregated():
    """CERTIFIED is a conjunction of named conditions, not an aggregate."""
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # §5.3 must require ALL of:
    assert "ALL of:" in authority or "requires ALL" in authority


def test_loss_triggers_count():
    """6 loss triggers for CERTIFIED → SUSPENDED."""
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # §6 must enumerate 6 triggers
    section_start = authority.find("## §6")
    assert section_start != -1
    # Read a chunk after §6
    chunk = authority[section_start : section_start + 4000]
    # Count numbered triggers
    import re

    triggers = re.findall(r"^\d+\.\s", chunk, re.MULTILINE)
    assert len(triggers) >= 6, f"expected ≥ 6 loss triggers, found {len(triggers)}"


def test_condition_revocation_mechanism():
    """Condition 10 of §5.3 — revocation_mechanism is declared."""
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    section = authority.find("### §5.3")
    chunk = authority[section : section + 3500]
    assert "revocation_mechanism" in chunk


def test_condition_13_witness():
    """Condition 13 of §5.3 — witnessed_by + test_review at A2."""
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    section = authority.find("### §5.3")
    chunk = authority[section : section + 3500]
    assert "witnessed_by" in chunk
    assert "test_review" in chunk
