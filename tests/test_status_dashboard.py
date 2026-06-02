#!/usr/bin/env python3
"""
Tests for tools/vbb-status-dashboard.py

Positive tests:
  1. Valid repo → readable status output
  2. --json produces valid JSON with expected fields
  3. --full includes extra details
  4. Contract count is correct
  5. Latest runs detected
  6. Next action detected

Negative tests:
  7. Minimal repo (no docs/) → does not crash
  8. Non-existent repo → error

Usage:
    pytest tests/test_status_dashboard.py -q
    python3 tests/test_status_dashboard.py
"""

import sys
import json
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-status-dashboard.py"


def _run_dashboard(args: list) -> tuple:
    result = subprocess.run(
        [sys.executable, str(TOOL)] + args,
        capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_valid_repo():
    """Valid repo → readable status output with key fields."""
    rc, out, err = _run_dashboard([])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    for field in ["Skills", "Contracts", "Test suites", "Verdict"]:
        assert field in out, f"Expected '{field}' in output\n{out}"


def test_json_output():
    """--json produces valid JSON with expected fields."""
    rc, out, err = _run_dashboard(["--json"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    data = json.loads(out)
    for field in ["repo", "skills", "contracts", "contract_coverage",
                  "tests", "latest_runs", "risks", "next_action"]:
        assert field in data, f"Missing field '{field}' in JSON\n{out}"
    assert isinstance(data["skills"], int)
    assert isinstance(data["contracts"], int)
    assert isinstance(data["contract_coverage"], float)


def test_full_mode():
    """--full includes extra details (activity log)."""
    rc, out, err = _run_dashboard(["--full"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    assert "VBB STATUS" in out


def test_contract_count():
    """Contract count matches expected value (positive for current repo)."""
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert data["contracts"] > 0, f"Expected positive contract count, got {data['contracts']}"
    assert data["skills"] > 0, f"Expected positive skill count, got {data['skills']}"
    assert data["contracts"] <= data["skills"], \
        f"Contracts ({data['contracts']}) should not exceed skills ({data['skills']})"


def test_latest_runs():
    """Latest runs are detected."""
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert isinstance(data["latest_runs"], list)
    assert len(data["latest_runs"]) > 0, "Expected at least one latest run"
    assert data["latest_runs"][0]["voie"] != "UNKNOWN"
    assert data["latest_runs"][0]["verdict"] != "UNKNOWN"


def test_temporal_local_date_exposed():
    """Temporal provenance includes local workspace date in JSON output."""
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert "local_date" in data
    assert isinstance(data["temporal_notes"], list)


def test_next_action():
    """Next action is detected (non-empty for real repo)."""
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert isinstance(data["next_action"], str)
    assert len(data["next_action"]) > 0, "Expected non-empty next action"


def test_minimal_repo():
    """Minimal repo without docs/ → does not crash."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        skills = repo / "skills"
        skills.mkdir()
        (skills / "1-test-skill").mkdir()
        (skills / "1-test-skill" / "SKILL.md").write_text("---\\nname: test\\n---\\n# Test\\n")

        rc, out, err = _run_dashboard(["--repo", str(repo)])
        assert rc == 0, f"Expected exit 0 for minimal repo, got {rc}\n{err}"
        assert "Skills" in out, f"Expected 'Skills' in output\n{out}"


def test_nonexistent_repo():
    """Non-existent repo → error + exit 1."""
    rc, out, err = _run_dashboard(["--repo", "/nonexistent/path"])
    assert rc == 1, f"Expected exit 1, got {rc}"

# --- Direct execution fallback ---

if __name__ == "__main__":
    try:
        import pytest
        sys.exit(pytest.main([__file__, "-q"]))
    except ImportError:
        passed = failed = 0
        for _name, _fn in sorted(globals().items()):
            if _name.startswith("test_") and callable(_fn):
                try:
                    _fn()
                    print("  PASS " + _name)
                    passed += 1
                except AssertionError as _e:
                    print("  FAIL " + _name + ": " + str(_e))
                    failed += 1
        total = passed + failed
        print("Results: %d/%d passed, %d failed" % (passed, total, failed))
        sys.exit(0 if failed == 0 else 1)
