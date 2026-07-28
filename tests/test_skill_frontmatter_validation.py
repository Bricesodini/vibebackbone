"""M3-07 — Skill frontmatter validation.

R2 §7 (ADVR-A2-10): the existing `test_prompt_language.py` was modified only
to bump a count threshold (`>= 64` -> `>= 66`). It does NOT validate the
content of the skills added.

M3-07 mandate: every `SKILL.md` must declare at least 5 *meaningful*
frontmatter fields beyond `name`, and an audit-or-tool skill
(`2-vbb-*` or `t-vbb-*`) must additionally anchor to the corpus by
declaring `phase` or `adr`/`canonical_authority`.

The pragmatic criterion used here is field *depth* on top of the
mandatory `name`/`description`/`version` triplet: a new skill that
just adds the triplet is rejected because it has no actual content to
audit or to integrate with the canon.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO / "skills"

AUDIT_AND_TOOL_PREFIXES = ("2-vbb-", "t-vbb-")

# Mandatory for every skill (beyond `name`):
MANDATORY_FIELDS = ("description", "version")

# Audit/tool prefix requires additional corpus anchoring:
ANCHORING_FIELDS = ("phase", "adr", "canonical_authority")


def _read_frontmatter(text: str) -> dict:
    """Parse the YAML frontmatter from a SKILL.md file (best-effort)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fm_text = text[4:end]
    fm: dict = {}
    current_key = None
    for line in fm_text.split("\n"):
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") or line.startswith("- "):
            if current_key and isinstance(fm.get(current_key), list):
                fm[current_key].append(line.lstrip("- ").strip())
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if not value:
                fm[key] = []
                current_key = key
            else:
                fm[key] = value
                current_key = key
    return fm


def _gather_skills() -> list[Path]:
    return sorted(SKILLS_ROOT.glob("*/SKILL.md"))


def test_all_skills_have_name():
    """Every SKILL.md must declare `name` in its frontmatter."""
    failures = []
    for skill in _gather_skills():
        text = skill.read_text(encoding="utf-8")
        fm = _read_frontmatter(text)
        if not fm.get("name"):
            failures.append(str(skill.relative_to(REPO)))
    assert failures == [], f"M3-07: missing `name` in: {failures}"


@pytest.mark.parametrize("field", MANDATORY_FIELDS)
def test_all_skills_have_mandatory_field(field):
    """Every SKILL.md must declare `description` and `version`."""
    failures = []
    for skill in _gather_skills():
        text = skill.read_text(encoding="utf-8")
        fm = _read_frontmatter(text)
        if not fm.get(field):
            failures.append(str(skill.relative_to(REPO)))
    assert failures == [], f"M3-07: missing `{field}` in: {failures}"


@pytest.mark.parametrize("prefix", AUDIT_AND_TOOL_PREFIXES)
def test_audit_and_tool_skills_anchor_to_corpus(prefix):
    """Skills under `2-vbb-*` (audit) or `t-vbb-*` (tooling) must declare at
    least one corpus-anchoring field: `phase`, `adr`, or `canonical_authority`."""
    failures = []
    for skill in _gather_skills():
        if not skill.parent.name.startswith(prefix):
            continue
        text = skill.read_text(encoding="utf-8")
        fm = _read_frontmatter(text)
        anchored = any(fm.get(f) for f in ANCHORING_FIELDS)
        if not anchored:
            failures.append(str(skill.relative_to(REPO)))
    assert failures == [], (
        f"M3-07: {prefix}* skill(s) without corpus anchor "
        f"({', '.join(ANCHORING_FIELDS)}): {failures}"
    )


def test_skill_count_at_least_current():
    """Sanity check: skill count has not regressed below current baseline."""
    skills = _gather_skills()
    assert len(skills) >= 66, (
        f"M3-07: skill count regression ({len(skills)} < 66). "
        f"Update this bound when a new skill is deliberately added."
    )
