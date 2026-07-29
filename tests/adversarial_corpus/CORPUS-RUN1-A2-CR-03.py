"""Corpus guard for RUN1-A2-CR-03: REOPENED P0 blocks READY."""

import importlib.util
from pathlib import Path


def _dashboard():
    path = Path(__file__).resolve().parents[2] / "tools/vbb-status-dashboard.py"
    spec = importlib.util.spec_from_file_location("corpus_run1_dashboard_cr03", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run1_a2_cr_03_reopened_p0_is_active(tmp_path):
    dashboard = _dashboard()
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "AUDIT_STATUS.md").write_text(
        "| ID | Severity | Status | Description |\n"
        "|---|---|---|---|\n"
        "| R-P0 | P0 | REOPENED | active again |\n",
        encoding="utf-8",
    )
    risks = dashboard.get_open_risks(tmp_path)
    assert [(risk["id"], risk["severity"]) for risk in risks] == [("R-P0", "P0")]
    assert dashboard.effective_verdict("READY", "BLOCKED") == "BLOCKED"
