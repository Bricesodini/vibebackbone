#!/usr/bin/env python3
"""
Tests for tools/vbb-architecture.py

Positive tests:
  1. Current repository architecture lints
  2. graph --write generates RELATIONS.md
  3. json returns parsed blocks

Negative tests:
  4. Missing required field fails
  5. Invalid YAML fails
  6. Unknown dependency warns but does not fail
  7. Architecture-sensitive files must be referenced
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-architecture.py"


VALID_ARCH = """# Architecture

## Bloc: Core

```yaml
id: core
type: governance
status: active
role: Core governance.
responsibilities:
  - route tasks
depends_on: []
impacts:
  - sessions
files:
  - AGENTS.md
  - docs/ARCHITECTURE.md
contracts:
  - vibebackbone
tests:
  - tests/test_core.py
risks:
  - id: CORE-001
    level: P2
    note: Drift risk.
```

## Bloc: Tooling

```yaml
id: tooling
type: tooling
status: active
role: Tooling layer.
responsibilities:
  - validate docs
depends_on:
  - core
impacts:
  - ci
files:
  - tools/example.py
contracts: []
tests:
  - tests/test_tooling.py
risks: []
```
"""


def _run_arch(args: list, cwd=None):
    result = subprocess.run(
        [sys.executable, str(TOOL)] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
    )
    return result.returncode, result.stdout, result.stderr


def _write_arch(repo: Path, content: str = VALID_ARCH) -> None:
    docs = repo / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "ARCHITECTURE.md").write_text(content, encoding="utf-8")


def test_current_repo_architecture_lints():
    """Current repository architecture lints cleanly."""
    rc, out, err = _run_arch(["lint"])
    assert rc == 0, f"Expected lint success\n{out}\n{err}"
    assert "Architecture blocks valid" in out


def test_graph_write_generates_relations():
    """graph --write generates docs/RELATIONS.md in a target repo."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_arch(repo)

        rc, out, err = _run_arch(["graph", "--write", "--repo", str(repo)])
        assert rc == 0, f"Expected graph success\n{out}\n{err}"

        relations = repo / "docs" / "RELATIONS.md"
        assert relations.exists(), "RELATIONS.md not generated"
        content = relations.read_text(encoding="utf-8")
        assert "graph TD" in content
        assert "tooling --> core" in content


def test_json_output():
    """json returns parsed block data."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_arch(repo)

        rc, out, err = _run_arch(["json", "--repo", str(repo)])
        assert rc == 0, f"Expected json success\n{out}\n{err}"
        data = json.loads(out)
        assert data["status"] == "PASS"
        assert len(data["blocks"]) == 2
        assert data["blocks"][0]["id"] == "core"


def test_missing_required_field_fails():
    """Missing required field returns non-zero."""
    bad = VALID_ARCH.replace("contracts: []\n", "", 1)
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_arch(repo, bad)

        rc, out, err = _run_arch(["lint", "--repo", str(repo)])
        assert rc != 0, "Expected lint failure"
        assert "missing required field 'contracts'" in out


def test_invalid_yaml_fails():
    """Invalid YAML returns non-zero."""
    bad = """# Architecture

## Bloc: Broken

```yaml
id: broken
type: [oops
```
"""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_arch(repo, bad)

        rc, out, err = _run_arch(["lint", "--repo", str(repo)])
        assert rc != 0, "Expected lint failure"
        assert "invalid YAML" in out


def test_unknown_dependency_warns_without_failing():
    """Unknown dependency produces a warning but keeps lint pass."""
    content = VALID_ARCH.replace("  - core", "  - missing-block")
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_arch(repo, content)

        rc, out, err = _run_arch(["lint", "--repo", str(repo)])
        assert rc == 0, f"Expected warning-only success\n{out}\n{err}"
        assert "WARN" in out
        assert "missing-block" in out


def test_architecture_sensitive_file_must_be_referenced():
    """Architecture-sensitive files must be covered by a block files pattern."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_arch(repo)
        tool = repo / "tools"
        tool.mkdir()
        (tool / "vbb-architecture.py").write_text("# local architecture tool\n")

        rc, out, err = _run_arch(["lint", "--repo", str(repo)])
        assert rc != 0, "Expected uncovered architecture-sensitive file to fail"
        assert "tools/vbb-architecture.py" in out


def test_architecture_sensitive_glob_can_be_referenced():
    """A files glob can cover architecture-sensitive files."""
    content = VALID_ARCH.replace("  - tools/example.py", "  - tools/vbb-*.py")
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _write_arch(repo, content)
        tool = repo / "tools"
        tool.mkdir()
        (tool / "vbb-architecture.py").write_text("# local architecture tool\n")

        rc, out, err = _run_arch(["lint", "--repo", str(repo)])
        assert rc == 0, f"Expected files glob to cover architecture file\n{out}\n{err}"


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
