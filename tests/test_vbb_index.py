#!/usr/bin/env python3
"""
Tests for tools/vbb-index.py

Positive tests:
  1. build creates manifest.json
  2. search returns results
  3. search --json returns valid JSON
  4. stats works
  5. Minimal repo doesn't crash

Negative tests:
  6. search without build → auto-builds
  7. .vbb/ is gitignored

Usage:
    pytest tests/test_vbb_index.py -q
    python3 tests/test_vbb_index.py
"""

import sys
import json
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-index.py"
INDEX_DIR = REPO_ROOT / ".vbb" / "index"


def _run_index(args: list) -> tuple:
    result = subprocess.run(
        [sys.executable, str(TOOL)] + args,
        capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_build_creates_manifest():
    """build creates .vbb/index/manifest.json with entries."""
    rc, out, err = _run_index(["build"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    assert INDEX_DIR.exists(), "Index dir not created"
    manifest = INDEX_DIR / "manifest.json"
    assert manifest.exists(), "Manifest not created"
    data = json.loads(manifest.read_text())
    assert data["total_entries"] > 0, f"Expected entries > 0, got {data['total_entries']}"


def test_search_returns_results():
    """search returns results for a known term."""
    _run_index(["build"])  # ensure built
    rc, out, err = _run_index(["search", "contract"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    assert "contract" in out.lower() or "CONTRACT" in out, f"Expected 'contract' in results\n{out}"


def test_search_json():
    """search --json returns valid JSON."""
    _run_index(["build"])
    rc, out, err = _run_index(["search", "rapide", "--json"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    data = json.loads(out)
    assert isinstance(data, list)
    if len(data) > 0:
        assert "path" in data[0], f"Expected 'path' in result\n{data[0]}"
        assert "score" in data[0], f"Expected 'score' in result\n{data[0]}"


def test_stats():
    """stats shows entry counts."""
    _run_index(["build"])
    rc, out, err = _run_index(["stats"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    assert "Entries" in out or "entries" in out.lower(), f"Expected entry count\n{out}"


def test_minimal_repo():
    """Minimal repo doesn't crash on build."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "docs").mkdir()
        (repo / "docs" / "CONTEXT.md").write_text("# Context\nMinimal test\n")
        (repo / "skills").mkdir()
        (repo / "skills" / "1-test").mkdir()
        (repo / "skills" / "1-test" / "SKILL.md").write_text("---\nname: test\n---\n# Test\n")

        rc, out, err = _run_index(["build", "--repo", str(repo)])
        assert rc == 0, f"Expected exit 0, got {rc}\n{err}"


def test_search_without_build():
    """search without build → auto-builds a local index."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "docs").mkdir()
        (repo / "docs" / "CONTEXT.md").write_text("# Context\nTest searchable content\n")
        rc, out, err = _run_index(["search", "test", "--repo", str(repo)])
        assert rc == 0, f"Expected auto-build search success\n{out}\n{err}"
        assert (repo / ".vbb" / "index" / "manifest.json").exists(), "Expected manifest to be auto-built"


def test_search_rebuilds_stale_index():
    """search rebuilds when indexed sources changed after manifest creation."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "docs").mkdir()
        context = repo / "docs" / "CONTEXT.md"
        context.write_text("# Context\nOld content\n")
        rc, _, err = _run_index(["build", "--repo", str(repo)])
        assert rc == 0, f"Expected build success\n{err}"

        context.write_text("# Context\nTemporal provenance marker\n")
        rc, out, err = _run_index(["search", "temporal", "--repo", str(repo)])
        assert rc == 0, f"Expected stale index rebuild search success\n{out}\n{err}"
        assert "temporal" in out.lower()


def test_vbb_gitignored():
    """.vbb/ is in .gitignore."""
    gitignore = REPO_ROOT / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        assert ".vbb" in content, f"Expected .vbb in .gitignore\n{content}"

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
