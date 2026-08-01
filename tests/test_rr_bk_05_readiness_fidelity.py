"""Deterministic RR-BK-05 fail-closed measurement fixtures."""

import importlib.util
from pathlib import Path


TOOL = Path(__file__).parents[1] / "tools" / "vbb-status-dashboard.py"
spec = importlib.util.spec_from_file_location("dashboard_rr_bk_05", TOOL)
assert spec and spec.loader
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)

SUBJECT = {"repo": "/fixture/repo", "sha": "sha-current"}


def source(rows: str, header: str = "Description") -> str:
    return (
        "## Active risks\n\n"
        f"| ID | Severity | Status | {header} |\n"
        "|---|---|---|---|\n"
        f"{rows}"
    )


def parse(text: str, name: str = "fixture.md"):
    return dashboard.parse_risk_source(text, name, SUBJECT)


def test_exact_rr_bk_05_reproduction_before_alias_fix_shape_is_now_visible():
    parsed = parse(
        source(
            "| RR-BK-03 | P1 | OPEN | dashboard masks active risks |\n",
            header="Description and reopen trigger",
        )
    )
    assert parsed["state"] == "OK"
    assert parsed["risks"][0]["id"] == "RR-BK-03"


def test_no_active_risk_is_a_valid_empty_measurement():
    assert parse(source(""))["state"] == "OK"
    assert parse(source(""))["risks"] == []


def test_active_blocking_and_nonblocking_risks_are_retained():
    parsed = parse(
        source(
            "| BLOCK | P0 | OPEN | blocks readiness |\n"
            "| NOTE | P3 | OPEN | nonblocking note |\n"
        )
    )
    assert [r["id"] for r in parsed["risks"]] == ["BLOCK", "NOTE"]


def test_resolved_and_explicitly_accepted_risks_do_not_count_as_active():
    parsed = parse(
        "## Active risks\n\n"
        "| ID | Severity | Status | Description | Owner | Scope |\n"
        "|---|---|---|---|---|---|\n"
        "| DONE | P1 | RESOLVED | fixed | | repository |\n"
        "| ACCEPT | P1 | ACCEPTED | bounded acceptance | release-owner | repository |\n"
    )
    assert parsed["state"] == "OK"
    assert parsed["risks"]
    active = [
        r
        for r in parsed["risks"]
        if r["status"].lower().startswith(("open", "mitigating", "deferred"))
    ]
    assert active == []


def test_other_subject_is_out_of_scope_and_preserved():
    parsed = parse(
        "## Active risks\n\n"
        "| ID | Severity | Status | Description | Subject |\n"
        "|---|---|---|---|---|\n"
        "| OTHER | P1 | OPEN | other candidate | sha-other |\n"
    )
    assert parsed["state"] == "OK"
    assert parsed["risks"] == []
    assert parsed["out_of_scope"][0]["id"] == "OTHER"


def test_absent_malformed_and_unknown_status_are_not_empty_successes():
    assert dashboard.measure_risk_sources([], SUBJECT)["state"] == "SOURCE_ABSENT"
    assert parse("## Active risks\n\nnot a table\n")["state"] == "SOURCE_INVALID"
    assert (
        parse(source("| BAD | P1 | MAYBE | unknown status |\n"))["state"]
        == "SOURCE_INVALID"
    )


def test_duplicate_conflict_and_contradictory_sources_block_measurement():
    duplicate = parse(
        source("| DUP | P1 | OPEN | first |\n| DUP | P2 | OPEN | conflicting |\n")
    )
    assert duplicate["state"] == "SOURCE_INVALID"
    left = parse(source("| SAME | P1 | OPEN | left |\n"), "left.md")
    right = parse(source("| SAME | P1 | RESOLVED | right |\n"), "right.md")
    assert (
        dashboard.measure_risk_sources([left, right], SUBJECT)["state"]
        == "SOURCE_CONTRADICTORY"
    )


def test_same_sha_is_exposed_and_reproducible():
    parsed = parse(source("| SAME | P1 | OPEN | same candidate |\n"))
    assert parsed["subject"]["sha"] == "sha-current"
    assert parsed["risks"][0]["source"] == "fixture.md"


def test_missing_required_source_forces_unknown_health():
    measurement = {"state": "SOURCE_ABSENT", "risks": [], "subject": SUBJECT}
    health = dashboard.measure_repository_health(Path("/fixture/repo"), [], measurement)
    assert health["verdict"] == "UNKNOWN"
    assert "SOURCE_ABSENT" in health["reasons"][0]
