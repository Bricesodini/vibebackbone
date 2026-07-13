"""Regression matrix for the POC verdict contract."""

import importlib.util
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-gate-check.py"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("vbb_gate_check_poc_test", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("verdict_line", "expected_ok", "expected_reason"),
    [
        ("- **Verdict** : GO", True, ""),
        ("Verdict: GO", True, ""),
        ("Décision: GO", True, ""),
        ("- **Verdict** : NO-GO", False, "POC_VERDICT_NO_GO"),
        ("- **Verdict** : PIVOT", False, "POC_VERDICT_PIVOT"),
        ("- **Verdict** : UNKNOWN", False, "POC_VERDICT_ABSENT"),
    ],
)
def test_check_poc_verdict_matrix(
    tmp_path: Path,
    verdict_line: str,
    expected_ok: bool,
    expected_reason: str,
) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "POC.md").write_text(
        f"# POC\n\n## Décision\n\n{verdict_line}\n",
        encoding="utf-8",
    )

    gate = _load_gate_module()
    ok, poc_path, reason = gate.check_poc(run_dir)

    assert ok is expected_ok
    assert poc_path == run_dir / "POC.md"
    assert reason == expected_reason


def test_check_poc_requires_artifact(tmp_path: Path) -> None:
    gate = _load_gate_module()

    ok, poc_path, reason = gate.check_poc(tmp_path)

    assert ok is False
    assert poc_path is None
    assert reason == "MISSING_POC"
