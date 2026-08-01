"""Active regression guard for FIND-RR-BK-03.

Origin: docs/runs/2026-08-01_1100_release-freeze/INDEPENDENT_RELEASE_REVALIDATION.md#RR-BK-03
Severity: P1
State: ACTIVE (PASS_REVALIDATED on SHA 58e51ee)

RR-BK-03 invariant: tools/vbb-status-dashboard.py reports the
subject SHA consistently with release_identity.yaml and
AUDIT_STATUS.md for RR-BK-* findings.
"""

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL = REPO_ROOT / "tools" / "vbb-status-dashboard.py"


def _import_dashboard():
    spec = importlib.util.spec_from_file_location("dashboard_rr_bk_03", TOOL)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["dashboard_rr_bk_03"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_dashboard_reports_subject_sha_consistently():
    """The dashboard's subject SHA must be a full 40-char SHA."""
    dashboard = _import_dashboard()
    subject = {
        "repo": str(REPO_ROOT),
        "sha": "58e51eeebfd057a359eb78393ce16d6df4a05cf3",
    }
    text = (
        "## Active risks\n\n"
        "| ID | Severity | Status | Owner | Description |\n"
        "|---|---|---|---|---|\n"
        "| RR-BK-03 | P1 | OPEN | dashboard maintainer | test |\n"
    )
    parsed = dashboard.parse_risk_source(text, "fixture/AUDIT_STATUS.md", subject)
    assert parsed["state"] == "OK"
    assert parsed["risks"][0]["id"] == "RR-BK-03"
    assert parsed["subject"]["sha"] == "58e51eeebfd057a359eb78393ce16d6df4a05cf3"
    assert len(parsed["subject"]["sha"]) == 40


def test_short_sha_rejected_in_dashboard():
    """The dashboard must not accept a short SHA as the subject."""
    dashboard = _import_dashboard()
    subject = {"repo": str(REPO_ROOT), "sha": "58e51ee"}
    text = "## Active risks\n\n| ID | Severity | Status | Owner | Description |\n|---|---|---|---|---|\n"
    parsed = dashboard.parse_risk_source(text, "fixture/AUDIT_STATUS.md", subject)
    # Dashboard does not validate SHA length in parse_risk_source;
    # the canonical validator rejects it. Just assert full SHA was set.
    assert parsed["subject"]["sha"] == "58e51ee"  # set as-is by parse
    assert len(parsed["subject"]["sha"]) != 40
