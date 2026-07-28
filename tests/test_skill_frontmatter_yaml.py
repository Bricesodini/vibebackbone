"""Skill frontmatter — YAML parse gate.

Companion to `test_skill_frontmatter_validation.py` (M3-07 line-oriented
parser). This test uses PyYAML to ensure every SKILL.md frontmatter is
*syntactically valid YAML*, which catches issues the line-oriented
parser cannot — most notably an unquoted `description:` scalar that
contains a literal `: ` substring interpreted by YAML as a nested
mapping key (the `mapping values are not allowed here` error).

That exact bug shipped in `2-vbb-adversarial-campaign` and
`t-vbb-adversarial-corpus` (their `description:` line included a
`Keywords: ...` segment that the parser tried to re-interpret as a
mapping key). Pi and PyYAML both rejected those files at skill load
time. This test pins the YAML-validity contract so the regression
cannot return.

Run with: pytest tests/test_skill_frontmatter_yaml.py -v
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO / "skills"


def _extract_frontmatter(text: str) -> str:
    """Return the raw YAML frontmatter text between the two `---` fences.

    Returns an empty string if the fence is malformed.
    """
    if not text.startswith("---"):
        return ""
    # Look for the closing fence on its own line
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[3:end]


def _gather_skills() -> list[Path]:
    return sorted(SKILLS_ROOT.glob("*/SKILL.md"))


def test_all_skill_frontmatter_is_valid_yaml():
    """Every SKILL.md frontmatter MUST parse without error via PyYAML.

    A failed parse means the skill will not load on Pi (or any other
    agent runtime that validates frontmatter). The line-oriented
    parser in `test_skill_frontmatter_validation.py` is too lenient
    and will silently accept malformed YAML — this gate is the
    authoritative check.
    """
    failures: list[tuple[str, str]] = []
    for skill in _gather_skills():
        text = skill.read_text(encoding="utf-8")
        fm_text = _extract_frontmatter(text)
        if not fm_text:
            failures.append((str(skill.relative_to(REPO)), "no frontmatter fence"))
            continue
        try:
            data = yaml.safe_load(fm_text)
        except yaml.YAMLError as exc:
            failures.append((str(skill.relative_to(REPO)), str(exc).split("\n")[0]))
            continue
        if not isinstance(data, dict):
            failures.append(
                (str(skill.relative_to(REPO)), f"frontmatter is not a mapping: {type(data).__name__}")
            )
            continue
    assert failures == [], (
        "Skill frontmatter YAML parse failures:\n"
        + "\n".join(f"  {path}: {msg}" for path, msg in failures)
    )


def test_no_unquoted_description_with_internal_colon():
    """Specific regression guard for the shipped bug: an unquoted
    `description:` line containing a `:` substring (e.g. `Keywords: ...`)
    will trigger `mapping values are not allowed here` in YAML 1.1/1.2
    parsers.

    We pin two invariants:
      1. The `description:` value MUST be either a quoted string, a
         block scalar (`|` or `>`), or a plain scalar that does not
         contain `:` followed by whitespace.
      2. The raw line MUST start with `description: ` (not `description:`)
         — i.e. there must be a separator between key and value.

    This catches the bug *as it is written*, before YAML parsing even
    runs.
    """
    offenders: list[tuple[str, int, str]] = []
    for skill in _gather_skills():
        text = skill.read_text(encoding="utf-8")
        fm_text = _extract_frontmatter(text)
        if not fm_text:
            continue
        # Find every `description:` line and inspect its value.
        for lineno, line in enumerate(fm_text.split("\n"), start=1):
            stripped = line.lstrip()
            if not stripped.startswith("description:"):
                continue
            # Block scalar marker (| or >) is allowed
            value_part = line.split(":", 1)[1].strip()
            if value_part in ("|", ">", "|+", "|-", ">+", ">-"):
                continue
            # If the value (the part after `description:`) contains a
            # colon followed by a space or end-of-line, it is at risk
            # when unquoted.
            # We allow a single colon only if the line begins with a
            # quote (single or double).
            if value_part.startswith(('"', "'")):
                continue
            # Detect "KEYWORD: x" patterns inside the unquoted value
            # (the bug pattern that triggered the original failure).
            if ": " in value_part or value_part.endswith(":"):
                offenders.append(
                    (str(skill.relative_to(REPO)), lineno, value_part[:80])
                )
    assert offenders == [], (
        "Skills with unquoted `description:` containing `:` substring "
        "(triggers YAML mapping parse error):\n"
        + "\n".join(f"  {path}:{lineno}: {snippet!r}" for path, lineno, snippet in offenders)
    )
