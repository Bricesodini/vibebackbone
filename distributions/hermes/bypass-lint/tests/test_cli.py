"""End-to-end tests for the CLI surface."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Absolute path to the linter script.
# As of ADR 0013 Phase 3, this test lives at
# distributions/hermes/bypass-lint/tests/test_cli.py, so parents[1]
# is bypass-lint/ (was parents[2] = tools/ at the old location).
LINTER = Path(__file__).resolve().parents[1] / "vbb-bypass-lint.py"


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run the linter as a subprocess and capture output."""
    return subprocess.run(
        [sys.executable, str(LINTER), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
    )


def test_cli_clean_dir_exits_zero(tmp_dir: Path):
    """An empty directory produces no findings and exit 0."""
    p = tmp_dir / "clean.sh"
    p.write_text("# nothing forbidden here\n", encoding="utf-8")
    result = _run([str(p)])
    assert result.returncode == 0, f"unexpected non-zero exit: stderr={result.stderr}"
    assert "No findings" in result.stdout or "0 critical" in result.stdout


def test_cli_critical_violation_exits_nonzero_in_report_mode(tmp_dir: Path):
    """Default (report) mode: a CRITICAL violation produces exit 1."""
    bad = tmp_dir / "bad.sh"
    bad.write_text("ssh root@nas\n", encoding="utf-8")
    result = _run([str(bad)])
    assert result.returncode == 1, (
        f"CRITICAL must produce exit 1, got {result.returncode}; "
        f"stdout={result.stdout!r}; stderr={result.stderr!r}"
    )


def test_cli_strict_mode_blocks_on_high(tmp_dir: Path):
    """--strict mode: HIGH findings should produce exit 1."""
    bad = tmp_dir / "high.sh"
    bad.write_text("mysql -u root -pMyPass db\n", encoding="utf-8")
    result = _run([str(bad), "--strict"])
    assert result.returncode == 1, (
        f"--strict must exit 1 on HIGH; got {result.returncode}; "
        f"stdout={result.stdout!r}; stderr={result.stderr!r}"
    )


def test_cli_strict_mode_clean_dir_exits_zero(tmp_dir: Path):
    """--strict mode with no findings exits 0."""
    p = tmp_dir / "ok.sh"
    p.write_text("echo hello\n", encoding="utf-8")
    result = _run([str(p), "--strict"])
    assert result.returncode == 0


def test_cli_json_output_is_valid_json(tmp_dir: Path):
    """--json output is valid JSON and contains the expected keys."""
    p = tmp_dir / "bad.sh"
    p.write_text("ssh root@nas\n", encoding="utf-8")
    result = _run([str(p), "--json"])
    data = json.loads(result.stdout)
    assert "findings" in data
    assert "stats" in data
    assert "exit_code" in data
    assert "has_critical" in data
    assert data["has_critical"] is True
    assert data["exit_code"] == 1
    assert data["findings"]
    f0 = data["findings"][0]
    for k in ("file", "line", "column", "pattern", "severity", "message", "suggestion"):
        assert k in f0, f"missing key {k} in finding: {f0}"


def test_cli_quiet_mode_suppresses_output(tmp_dir: Path):
    """--quiet suppresses the human-readable output; exit code is preserved."""
    p = tmp_dir / "bad.sh"
    p.write_text("ssh root@nas\n", encoding="utf-8")
    result = _run([str(p), "--quiet"])
    assert result.returncode == 1
    # stdout should be empty
    assert result.stdout.strip() == "", f"expected empty stdout, got {result.stdout!r}"


def test_cli_excludes_passed_globs(tmp_dir: Path):
    """--exclude should suppress matching files."""
    skipped = tmp_dir / "ignored.sh"
    skipped.write_text("ssh root@nas\n", encoding="utf-8")
    result = _run([str(tmp_dir), "--exclude", "ignored.sh", "--quiet"])
    # No findings because the only matching file is excluded.
    assert result.returncode == 0, f"expected clean, got {result.returncode} ({result.stderr})"


def test_cli_severity_threshold_filters(tmp_dir: Path):
    """--severity-threshold CRITICAL hides MEDIUM/HIGH findings from output
    (but they are still counted in stats)."""
    p = tmp_dir / "high.sh"
    p.write_text("mysql -u root -pMyPass db\n", encoding="utf-8")
    result = _run([str(p), "--severity-threshold", "CRITICAL"])
    # HIGH is filtered out (threshold = CRITICAL means only CRITICAL surfaces).
    # Default report mode with no CRITICAL => exit 0
    assert result.returncode == 0, f"expected exit 0 with threshold=CRITICAL, got {result.returncode}; stdout={result.stdout!r}"


def test_cli_help_prints(capsys):
    """Running with --help exits 0 and prints usage."""
    result = _run(["--help"])
    assert result.returncode == 0
    combined = result.stdout + result.stderr
    assert "usage" in combined.lower() or "options" in combined.lower()
