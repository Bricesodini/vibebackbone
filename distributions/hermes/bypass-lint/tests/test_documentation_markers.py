"""Tests for documentation markers and test-context suppression.

The linter must NOT flag lines that:
  - contain a documentation marker (interdit, bypass, do not, ne pas, …)
  - are inside a pytest.raises / @pytest.fixture / test_negative block
"""

from __future__ import annotations

from pathlib import Path

from vbb_bypass_lint import LintConfig, lint_paths


def test_documentation_marker_interdit(tmp_dir: Path):
    """A line saying 'ssh ... est interdit' must be ignored."""
    f = tmp_dir / "doc.md"
    f.write_text(
        "## Forbidden binaries\n"
        "ssh root@nas is **interdit** and must go through the proxy.\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings, f"interdit marker should suppress: {report.findings}"


def test_documentation_marker_bypass(tmp_dir: Path):
    """A line with 'bypass' marker is documentation, not a violation."""
    f = tmp_dir / "doc.md"
    f.write_text(
        "If you want a **bypass** of the proxy, you must NOT. Use the proxy.\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings


def test_documentation_marker_do_not(tmp_dir: Path):
    f = tmp_dir / "doc.md"
    f.write_text(
        "Do not run `ssh root@nas` directly; use the proxy.\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings


def test_documentation_marker_ne_pas(tmp_dir: Path):
    f = tmp_dir / "doc.md"
    f.write_text(
        "Ne pas utiliser `ssh user@server` ; passer par le proxy.\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings


def test_documentation_marker_exemple_negatif(tmp_dir: Path):
    f = tmp_dir / "doc.md"
    f.write_text(
        "Exemple négatif : ssh user@host est interdit.\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings


def test_documentation_marker_anti_pattern(tmp_dir: Path):
    f = tmp_dir / "doc.md"
    f.write_text(
        "Anti-pattern : docker login direct doit être évité.\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings


def test_test_context_pytest_raises(tmp_dir: Path):
    """A line preceded by pytest.raises should be treated as a test context."""
    f = tmp_dir / "test_foo.py"
    f.write_text(
        "import pytest\n"
        "def test_negative():\n"
        "    with pytest.raises(ProxyError):\n"
        '        ssh_root = "ssh root@nas"  # noqa: this is a test\n',
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    # Test-context lines AND noqa-bypass-doc lines must be skipped.
    assert not report.findings, f"pytest.raises context must be skipped: {report.findings}"


def test_test_context_pytest_fixture(tmp_dir: Path):
    f = tmp_dir / "test_foo.py"
    f.write_text(
        "import pytest\n"
        "@pytest.fixture\n"
        'def fake_ssh():\n'
        '    return "ssh root@nas"  # for negative test only\n',
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings


def test_test_context_marker(tmp_dir: Path):
    f = tmp_dir / "test_foo.py"
    f.write_text(
        "def test_negative_case():\n"
        '    cmd = "ssh root@nas"  # expected violation\n',
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert not report.findings, f"expected violation marker must skip: {report.findings}"


def test_plain_violation_still_flagged(tmp_dir: Path):
    """A line WITHOUT any documentation/test marker must still be flagged."""
    f = tmp_dir / "tool.sh"
    f.write_text(
        "# Run ssh to deploy\n"
        "ssh deploy@prod\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    assert report.findings, "plain violation must be flagged"


def test_mixed_lines_only_violation_flagged(tmp_dir: Path):
    f = tmp_dir / "tool.sh"
    f.write_text(
        "ssh root@nas is **interdit** and bypass pattern.\n"
        "ssh root@nas\n",
        encoding="utf-8",
    )
    report = lint_paths([f], config=LintConfig())
    # Only the second line should be flagged.
    assert len(report.findings) == 1, f"expected 1 finding, got {len(report.findings)}"
    assert report.findings[0].line == 2
