"""Corpus guard for RUN1-A2-02: invented full SHAs are not Git subjects."""

import importlib.util
import subprocess
from pathlib import Path


def _resolution():
    root = Path(__file__).resolve().parents[2]
    path = root / "tools" / "vbb_run_resolution.py"
    spec = importlib.util.spec_from_file_location("corpus_run1_resolution", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run1_a2_02_invented_sha_is_rejected(tmp_path):
    resolution = _resolution()
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    run = tmp_path / "runs" / "run1"
    run.mkdir(parents=True)
    invented = "a" * 40
    (run / "07_CLOSEOUT.md").write_text(
        "```yaml\n"
        "adversarial:\n"
        "  certification:\n"
        "    bound_to:\n"
        '      run_id: "run1"\n'
        f'      commit: "{invented}"\n'
        "```\n",
        encoding="utf-8",
    )
    ok, reason = resolution.verify_bound_subject(run, invented)
    assert ok is False
    assert "not a Git commit object" in reason
