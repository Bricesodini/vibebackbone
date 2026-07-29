"""Corpus-local pytest configuration.

Pre-merge gate 5b (`docs/REFERENCE/pre-merge-gate.md`) runs

    python -m pytest tests/adversarial_corpus/ -q

as a separately reported check. While no CONFIRMED adversarial finding has been
registered, that directory holds no test and pytest exits 5
(``EXIT_NOTESTSCOLLECTED``), which breaks the gate's `&&` chain and makes the
canonical block unrunnable.

An empty corpus is a legitimate state — it means no CONFIRMED finding is
outstanding — so this hook maps exit 5 to exit 0 **for corpus-only runs**.

This is not a way to pass with no coverage. The obligation "every CONFIRMED
finding has a corpus entry" is carried by ``tests/test_corpus_mandatory.py`` in
the main suite: if a CONFIRMED finding exists without its entry, that test
fails, and an empty corpus stops being legitimate. Genuine corpus failures still
exit 1 and are untouched here.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

EXIT_NO_TESTS_COLLECTED = 5
CORPUS_DIR = Path(__file__).parent.resolve()
REPO_ROOT = CORPUS_DIR.parent.parent


def load_tool(tool_filename: str, module_name: str):
    """Import a hyphenated tool from tools/ as a module.

    The module is registered in ``sys.modules`` before execution: dataclasses
    resolve ``cls.__module__`` through that registry, and an unregistered module
    makes ``@dataclass`` fail with an opaque AttributeError.
    """
    path = REPO_ROOT / "tools" / tool_filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def adversarial_gate():
    """The adversarial gate validator, shared by corpus entries."""
    return load_tool("vbb-adversarial-gate.py", "vbb_adversarial_gate_corpus")


def pytest_collect_file(parent, file_path):
    """Collect ``CORPUS-<id>.py`` entries.

    ``t-vbb-adversarial-corpus`` mandates the ``CORPUS-<id>.py`` filename, which
    matches neither ``test_*.py`` nor ``*_test.py``. Without this hook pytest
    collects nothing here, so the corpus would report "no tests ran" even when
    fully populated — the obligation would look satisfied while executing zero
    guards.
    """
    if file_path.suffix == ".py" and file_path.name.startswith("CORPUS-"):
        return pytest.Module.from_parent(parent, path=file_path)
    return None


def _targets_corpus_only(session) -> bool:
    """True when every collection argument points inside the corpus directory.

    Guards against neutralising exit 5 for a whole-suite run that happened to
    collect nothing; only an explicit corpus-scoped invocation is covered.
    """
    args = [str(arg).split("::", 1)[0] for arg in session.config.args]
    if not args:
        return False
    for arg in args:
        try:
            resolved = Path(arg).resolve()
        except (OSError, ValueError):
            return False
        if resolved != CORPUS_DIR and CORPUS_DIR not in resolved.parents:
            return False
    return True


def pytest_sessionfinish(session, exitstatus):
    if exitstatus != EXIT_NO_TESTS_COLLECTED:
        return
    if session.testscollected:
        return
    if _targets_corpus_only(session):
        session.exitstatus = 0
