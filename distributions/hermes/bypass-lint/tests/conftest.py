"""Shared pytest fixtures for vbb-bypass-lint tests."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

# The linter file is named "vbb-bypass-lint.py" (hyphenated), so we cannot
# import it with a normal `import vbb_bypass_lint` statement. Load it
# explicitly via importlib under the alias `vbb_bypass_lint`.
# As of ADR 0013 Phase 3, this conftest lives at
# distributions/hermes/bypass-lint/tests/conftest.py, so parents[1] is
# the bypass-lint/ directory (was parents[2] when at tools/vbb-bypass-lint/tests/).
BYPASS_LINT_DIR = Path(__file__).resolve().parents[1]
LINTER_PATH = BYPASS_LINT_DIR / "vbb-bypass-lint.py"
if str(BYPASS_LINT_DIR) not in sys.path:
    sys.path.insert(0, str(BYPASS_LINT_DIR))

_SPEC = importlib.util.spec_from_file_location("vbb_bypass_lint", str(LINTER_PATH))
assert _SPEC is not None and _SPEC.loader is not None, (
    f"failed to load linter spec from {LINTER_PATH}"
)
linter = importlib.util.module_from_spec(_SPEC)
sys.modules["vbb_bypass_lint"] = linter
_SPEC.loader.exec_module(linter)


@pytest.fixture
def linter_module():
    """Return the imported linter module for direct API access."""
    return linter


@pytest.fixture
def tmp_dir(tmp_path: Path) -> Path:
    """A clean temporary directory (alias for readability)."""
    return tmp_path


@pytest.fixture
def allowed_paths_setup(tmp_dir: Path):
    """Create the canonical Vibebackbone layout under tmp_dir.

    Layout produced::

        tmp_dir/
          SOUL.md                 (NOT created — caller decides)
          tools/
            proxy/                (allowed path)
              client.py           (must NOT be flagged)
            some_tool.py          (caller may add content)
          docs/
            adr/                  (allowed path)
              0011-foo.md         (must NOT be flagged)
            guide.md              (caller may add content)
          prompts/
          skills/
          scripts/

    Returns the root Path.  Marked as a "function" scope so each test gets a
    fresh sandbox.
    """
    root = tmp_dir
    (root / "tools" / "proxy").mkdir(parents=True)
    (root / "tools" / "proxy" / "client.py").write_text(
        '"""Reference list of forbidden patterns (must NOT be flagged)."""\n'
        'FORBIDDEN = [\n'
        '    "ssh root@nas",\n'
        '    "gh auth login",\n'
        '    "docker login",\n'
        '    "vault read secret/data",\n'
        ']\n',
        encoding="utf-8",
    )
    (root / "docs" / "adr").mkdir(parents=True)
    (root / "docs" / "adr" / "0011-proxy-bypass-prevention.md").write_text(
        "# ADR 0011 — bypass prevention\n\n"
        "ssh, scp, rsync are **interdit** (forbidden).\n"
        "gh auth is **bypass** pattern.\n"
        "Use proxy_nas_exec instead.\n",
        encoding="utf-8",
    )
    (root / "prompts").mkdir(parents=True)
    (root / "skills").mkdir(parents=True)
    (root / "scripts").mkdir(parents=True)
    return root
