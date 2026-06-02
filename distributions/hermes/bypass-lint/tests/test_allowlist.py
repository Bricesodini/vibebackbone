"""Tests verifying that allowed/allowlisted paths are exempt from scanning."""

from __future__ import annotations

import os
from pathlib import Path

from vbb_bypass_lint import LintConfig, lint_paths


def test_proxy_dir_is_allowlisted(tmp_dir: Path, allowed_paths_setup: Path):
    """A file under tools/proxy/ that contains forbidden patterns must NOT be flagged."""
    root = allowed_paths_setup
    proxy_file = root / "tools" / "proxy" / "client.py"
    assert proxy_file.exists()
    report = lint_paths([proxy_file], config=LintConfig())
    assert not report.findings, (
        f"tools/proxy/ must be exempt; got findings: {report.findings}"
    )


def test_adr_dir_is_allowlisted(tmp_dir: Path, allowed_paths_setup: Path):
    """A file under docs/adr/ that contains forbidden patterns must NOT be flagged."""
    root = allowed_paths_setup
    adr = root / "docs" / "adr" / "0011-proxy-bypass-prevention.md"
    assert adr.exists()
    report = lint_paths([adr], config=LintConfig())
    assert not report.findings, (
        f"docs/adr/ must be exempt; got findings: {report.findings}"
    )


def test_other_paths_are_NOT_allowlisted(tmp_dir: Path, allowed_paths_setup: Path):
    """A file under tools/ (NOT tools/proxy/) that contains forbidden patterns
    must be flagged. The same is true for prompts/, skills/, scripts/."""
    root = allowed_paths_setup
    bad = root / "tools" / "naughty.sh"
    bad.write_text("ssh root@nas\n", encoding="utf-8")
    report = lint_paths([bad], config=LintConfig())
    assert report.findings, "tools/naughty.sh must NOT be exempt (not under tools/proxy/)"


def test_linter_self_is_allowlisted(tmp_dir: Path):
    """The linter module itself contains all forbidden patterns as regex strings;
    it must be exempt from scanning itself."""
    # As of ADR 0013 Phase 3, the linter lives at
    # distributions/hermes/bypass-lint/vbb-bypass-lint.py, so parents[1]
    # of this test file is the bypass-lint/ dir (was parents[2] = tools/
    # at the old location tools/vbb-bypass-lint/tests/test_allowlist.py).
    linter_path = (
        Path(__file__).resolve().parents[1] / "vbb-bypass-lint.py"
    )
    assert linter_path.exists()
    config = LintConfig()
    # Resolve the linter path against its repo root for the config check.
    config_with_root = LintConfig()
    # We can call is_allowed directly:
    repo_root = linter_path.parent
    assert config.is_allowed(linter_path, repo_root), (
        "linter itself must be allowlisted"
    )


def test_linter_tests_dir_is_allowlisted(tmp_dir: Path):
    """The linter's own tests dir contains example violations on purpose."""
    # As of ADR 0013 Phase 3, this test is at
    # distributions/hermes/bypass-lint/tests/test_allowlist.py, so
    # parents[1] is the bypass-lint/ dir.
    tests_dir = Path(__file__).resolve().parents[1]  # distributions/hermes/bypass-lint/
    config = LintConfig()
    # repo_root from tests_dir: parents[3] of tests_dir = repo root.
    # (Originally tests_dir.parents[2] when at tools/vbb-bypass-lint/tests/
    # resolved to tools/ which was the comment in the old version; the
    # intent is "any ancestor that lets is_allowed compute relative paths",
    # which works at any depth that contains the exempt paths.)
    repo_root = tests_dir.parents[3]  # repo root
    assert config.is_allowed(tests_dir, repo_root), (
        "distributions/hermes/bypass-lint/tests/ must be allowlisted"
    )


def test_repo_proxy_and_adr_dont_trigger_findings(tmp_dir: Path):
    """Regression test: scan the actual repo's proxy cluster and ADR dirs.

    These are not under the tmp_dir sandbox; we resolve against the real repo.
    Either the scan returns 0 findings (exempt) or the regression is real.

    As of ADR 0013 Phase 3, the proxy cluster lives at
    distributions/hermes/proxy/ (was tools/proxy/ before Phase 3).
    The check is guarded by `if <path>.exists():` so missing paths are
    silently skipped (no false failures during transitional periods).
    """
    # parents[2] of this test file = repo root (was parents[3] = repo root
    # when at tools/vbb-bypass-lint/tests/test_allowlist.py).
    repo = Path(__file__).resolve().parents[2]  # repo root
    config = LintConfig()
    # New canonical location (ADR 0013 Phase 3).
    proxy = repo / "distributions" / "hermes" / "proxy"
    # ADR 0001-0005 still in Core at docs/adr/; proxy ADRs 0006-0012
    # moved to distributions/hermes/proxy/adr/ in Phase 2.
    adr_core = repo / "docs" / "adr"
    adr_proxy = repo / "distributions" / "hermes" / "proxy" / "adr"
    if proxy.exists():
        r1 = lint_paths([proxy], config=config)
        assert not r1.findings, f"distributions/hermes/proxy/ regression: {r1.findings[:3]}"
    if adr_core.exists():
        r2 = lint_paths([adr_core], config=config)
        assert not r2.findings, f"docs/adr/ regression: {r2.findings[:3]}"
    if adr_proxy.exists():
        r3 = lint_paths([adr_proxy], config=config)
        assert not r3.findings, f"distributions/hermes/proxy/adr/ regression: {r3.findings[:3]}"
