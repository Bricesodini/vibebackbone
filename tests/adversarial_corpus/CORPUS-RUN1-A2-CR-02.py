"""Corpus guard for RUN1-A2-CR-02: certification rejects stale valid commits."""

import importlib.util
import subprocess
from pathlib import Path


def _resolution():
    path = Path(__file__).resolve().parents[2] / "tools/vbb_run_resolution.py"
    spec = importlib.util.spec_from_file_location("corpus_run1_resolution_cr02", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run1_a2_cr_02_old_commit_is_historical_only(tmp_path):
    resolution = _resolution()
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.name", "VBB"], check=True
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.email", "vbb@example.invalid"],
        check=True,
    )
    run = tmp_path / "runs" / "2026-07-29_1200_target"
    run.mkdir(parents=True)
    (tmp_path / "state").write_text("old\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-m", "old"],
        check=True,
        capture_output=True,
    )
    old = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    (run / "07_CLOSEOUT.md").write_text(
        "```yaml\nadversarial:\n  certification:\n    bound_to:\n"
        f'      run_id: "{run.name}"\n      commit: "{old}"\n```\n',
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-m", "new"],
        check=True,
        capture_output=True,
    )

    assert resolution.verify_bound_subject(run, old)[0] is True
    assert resolution.verify_certification_subject(run, old)[0] is False
