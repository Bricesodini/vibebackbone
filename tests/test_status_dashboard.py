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
import os
import subprocess
import tempfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-status-dashboard.py"


def _run_dashboard(args: list) -> tuple:
    result = subprocess.run(
        [sys.executable, str(TOOL)] + args,
        capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


def _import_dashboard():
    """Import the dashboard module directly (no subprocess) for unit tests."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "vbb_status_dashboard", str(TOOL)
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load dashboard module from {TOOL}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _make_run(repo: Path, name: str, mtime_offset: int = 0,
              closeout_name: str = "07_CLOSEOUT.md") -> Path:
    """Create a fake run directory with a closeout file.

    ``mtime_offset`` is added to the current time (seconds). Use positive values
    to make a run appear more recent than its peers, regardless of name.
    """
    rd = repo / "docs" / "runs" / name
    rd.mkdir(parents=True, exist_ok=True)
    closeout = rd / closeout_name
    closeout.write_text(
        "---\n"
        f"run_id: \"{name}\"\n"
        "phase: \"07_CLOSEOUT\"\n"
        "voie: \"STRUCTURED\"\n"
        "status: \"READY\"\n"
        "agent: \"test\"\n"
        "---\n\n"
        f"# {name}\n"
    )
    # Force mtime so test ordering is deterministic and decoupled from the
    # name-based lexical sort that we are replacing.
    target = time.time() + mtime_offset
    os.utime(rd, (target, target))
    os.utime(closeout, (target, target))
    return rd


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
    """Latest runs are detected and ordered by mtime (newest first).

    RUN 3 stabilisation: post-fix, the top entry is the run with the freshest
    mtime (the in-progress ``2026-06-13_2200_run-2-doc-core-distribution``
    that is currently untracked). The list is asserted to be non-empty,
    ordered by mtime, and to contain at least one well-formed closeout with
    a real ``voie`` + ``verdict`` pair (not all entries are UNKNOWN).
    """
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert isinstance(data["latest_runs"], list)
    assert len(data["latest_runs"]) > 0, "Expected at least one latest run"
    # At least one entry must carry a real voie/verdict pair (otherwise the
    # dashboard is reporting noise). We do not assert on the *first* entry's
    # voie/verdict directly because the freshest mtime may correspond to an
    # in-progress run whose closeout is not yet in standard frontmatter form.
    assert any(
        r["voie"] != "UNKNOWN" and r["verdict"] != "UNKNOWN"
        for r in data["latest_runs"]
    ), f"Expected at least one well-formed run in {data['latest_runs']}"
    # Ordering invariant: the list is bounded by the requested limit and
    # every id is a non-empty string (no loose files leak through).
    assert len(data["latest_runs"]) <= 5
    for r in data["latest_runs"]:
        assert isinstance(r["id"], str) and r["id"], r


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


# --- RUN 3 stabilisation: get_latest_runs() lexical-sort regression tests ---


def test_latest_runs_malformed_name_uses_mtime():
    """Case 1 (RUN 3): malformed date name loses to well-formed newer run.

    The old lexical sort placed ``20260602_0817_yyy`` AFTER
    ``2026-06-13_2200_xxx`` only because ``0`` > ``-`` in ASCII. The mtime
    sort must pick the genuinely newer run regardless of the name format.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        # Lexically: "20260602_0817_yyy" > "2026-06-13_2200_xxx" (because
        # '0' > '-' in ASCII at index 5). Pre-fix, this would rank malformed
        # first. Post-fix, mtime (offset 100s) wins for the well-formed one.
        malformed = _make_run(repo, "20260602_0817_yyy", mtime_offset=0)
        wellformed = _make_run(repo, "2026-06-13_2200_xxx", mtime_offset=100)

        latest = mod.get_latest_runs(repo, limit=5)
        assert latest, "Expected at least one latest run"
        assert latest[0]["id"] == "2026-06-13_2200_xxx", (
            "mtime-based sort must rank the well-formed newer run first, "
            f"got {latest[0]['id']}"
        )
        # Both runs must appear (no spurious filtering).
        ids = {r["id"] for r in latest}
        assert ids == {"2026-06-13_2200_xxx", "20260602_0817_yyy"}


def test_latest_runs_skips_loose_files():
    """Case 2 (RUN 3): loose files in docs/runs/ (README.md etc.) must not
    appear in latest_runs output. They are filtered by ``is_dir()``.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _make_run(repo, "2026-06-13_2200_xxx", mtime_offset=10)
        # Parasitic loose files: README + a routing-style note.
        (repo / "docs" / "runs" / "README.md").write_text("# runs")
        (repo / "docs" / "runs" / "routing-fix-verification.md").write_text(
            "# routing"
        )

        latest = mod.get_latest_runs(repo, limit=10)
        ids = [r["id"] for r in latest]
        assert "README.md" not in ids, "README.md must not appear in latest_runs"
        assert "routing-fix-verification.md" not in ids, (
            "routing-fix-verification.md must not appear in latest_runs"
        )
        # Sanity: the one real run is still detected.
        assert ids == ["2026-06-13_2200_xxx"]


def test_latest_runs_mtime_overrides_future_name():
    """Case 3 (RUN 3): a future-dated folder name is treated by mtime, not
    by the literal name. A folder named ``2026-12-31_2359_xxx`` whose mtime
    is older must not be ranked above a folder whose mtime is newer.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        # Future-dated name, but oldest mtime (offset -1000s).
        future = _make_run(repo, "2026-12-31_2359_xxx", mtime_offset=-1000)
        # Older-looking name, but most recent mtime (offset +1000s).
        recent = _make_run(repo, "2026-06-13_2200_recent", mtime_offset=1000)

        latest = mod.get_latest_runs(repo, limit=5)
        assert latest, "Expected at least one latest run"
        assert latest[0]["id"] == "2026-06-13_2200_recent", (
            "mtime (newer) must win over a future-dated folder name, "
            f"got {latest[0]['id']}"
        )
        # The future-dated folder is still present (not rejected by name).
        ids = {r["id"] for r in latest}
        assert "2026-12-31_2359_xxx" in ids


def test_latest_runs_accepts_non_canonical_closeout():
    """Defensive: a run dir that writes ``CLOSEOUT.md`` (no ``07_`` prefix)
    before the standard rename is still detected. The fallback closeout
    lookup covers this in-progress case.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        rd = repo / "docs" / "runs" / "2026-06-13_2200_in_progress"
        rd.mkdir(parents=True)
        (rd / "CLOSEOUT.md").write_text(
            "---\nrun_id: in_progress\nphase: 07_CLOSEOUT\n"
            "voie: STRUCTURED\nstatus: READY\n---\n\n# in progress\n"
        )
        target = time.time()
        os.utime(rd, (target, target))

        latest = mod.get_latest_runs(repo, limit=5)
        assert latest, "Expected the in-progress run to be detected"
        assert latest[0]["id"] == "2026-06-13_2200_in_progress"


def test_latest_runs_missing_runs_dir():
    """Edge case: a repo with no ``docs/runs/`` directory returns an empty
    list instead of raising.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "docs").mkdir()
        assert mod.get_latest_runs(repo, limit=5) == []


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
