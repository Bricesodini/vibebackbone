"""Corpus guard for RUN1-A2-01: qualified risk headers cannot hide P0."""

import importlib.util
from pathlib import Path


def _dashboard():
    root = Path(__file__).resolve().parents[2]
    path = root / "tools" / "vbb-status-dashboard.py"
    spec = importlib.util.spec_from_file_location("corpus_run1_dashboard", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run1_a2_01_description_variants_preserve_active_p0(tmp_path):
    dashboard = _dashboard()
    docs = tmp_path / "docs"
    docs.mkdir()
    for header in (
        "Description & reopen trigger",
        "Description and reopen triggers",
        "Description/reopen triggers (release gate)",
    ):
        (docs / "AUDIT_STATUS.md").write_text(
            f"| ID | Severity | Status | Owner | {header} |\n"
            "|---|---|---|---|---|\n"
            "| `RUN1-P0` | P0 | OPEN | owner | active |\n",
            encoding="utf-8",
        )
        risks = dashboard.get_open_risks(tmp_path)
        assert [(risk["id"], risk["severity"]) for risk in risks] == [("RUN1-P0", "P0")]
