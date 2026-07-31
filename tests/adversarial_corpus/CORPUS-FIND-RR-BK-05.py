"""Active regression guard for FIND-RR-BK-05.

Origin: docs/runs/2026-07-31_1530_rr-bk-05-readiness-fidelity/
Severity: S1
State: ACTIVE
"""

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL = REPO_ROOT / "tools" / "vbb-status-dashboard.py"
spec = importlib.util.spec_from_file_location("dashboard_rr_bk_05_corpus", TOOL)
assert spec and spec.loader
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)


def test_rr_bk_05_canonical_header_cannot_mask_active_risk():
    subject = {"repo": "/fixture/repo", "sha": "sha-current"}
    text = (
        "## Active risks\n\n"
        "| ID | Severity | Status | Owner | Description and reopen trigger |\n"
        "|---|---|---|---|---|\n"
        "| RR-BK-03 | P1 | OPEN | dashboard maintainer | active risk |\n"
    )
    parsed = dashboard.parse_risk_source(text, "fixture/AUDIT_STATUS.md", subject)
    assert parsed["state"] == "OK"
    assert [risk["id"] for risk in parsed["risks"]] == ["RR-BK-03"]
    assert parsed["risks"][0]["source"] == "fixture/AUDIT_STATUS.md"
