#!/usr/bin/env python3
"""
Tests for P0-4 review-tier integration into tools/vbb-status-dashboard.py.

Covers:
  - --review-tier flag (text + JSON output)
  - --tier alias
  - default dashboard unchanged when no flag
  - blocking always False, mode always "advisory"
  - JSON contract: all 7 fields present
  - working-tree paths default

Usage:
    pytest tests/test_status_dashboard_review_tier.py -q
"""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
DASH = REPO_ROOT / "tools" / "vbb-status-dashboard.py"
PYTHON = sys.executable


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(DASH), *args],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )


# --- Flag presence and default behavior -------------------------------------

def test_help_lists_review_tier_flag() -> None:
    p = _run("--help")
    assert p.returncode == 0
    assert "--review-tier" in p.stdout
    assert "--tier" in p.stdout


def test_default_dashboard_unchanged_without_flag() -> None:
    """Without --review-tier, the dashboard shows its normal verdict view."""
    p = _run()
    assert p.returncode == 0
    assert "VBB STATUS" in p.stdout
    # The tier-advisory header must NOT appear in default view
    assert "Review-Tier Advisory" not in p.stdout


# --- Text output ------------------------------------------------------------

def test_review_tier_text_output_structure() -> None:
    p = _run("--review-tier")
    assert p.returncode == 0
    out = p.stdout
    assert "Review-Tier Advisory" in out
    assert "blocking=" in out
    assert "ADVISORY only" in out
    # Tier line is either "Tier : Tn" or "Tier : UNMAPPED"
    assert "Tier :" in out


# --- JSON contract ----------------------------------------------------------

def test_review_tier_json_has_all_required_fields() -> None:
    p = _run("--review-tier", "--json")
    assert p.returncode == 0, f"stderr={p.stderr}"
    data = json.loads(p.stdout)
    required = {
        "review_tier", "label", "reasons", "suggested_actions",
        "blocking", "confidence", "mode",
    }
    assert required.issubset(data.keys()), (
        f"missing fields: {required - data.keys()}\ngot: {data}"
    )


def test_review_tier_json_always_advisory() -> None:
    """blocking must be False, mode must be 'advisory' — every time."""
    p = _run("--review-tier", "--json")
    data = json.loads(p.stdout)
    assert data["blocking"] is False
    assert data["mode"] == "advisory"


def test_review_tier_json_confidence_value() -> None:
    p = _run("--review-tier", "--json")
    data = json.loads(p.stdout)
    assert data["confidence"] in {"low", "medium", "high"}


def test_review_tier_json_reasons_is_list() -> None:
    p = _run("--review-tier", "--json")
    data = json.loads(p.stdout)
    assert isinstance(data["reasons"], list)


def test_review_tier_json_suggested_actions_is_list() -> None:
    p = _run("--review-tier", "--json")
    data = json.loads(p.stdout)
    assert isinstance(data["suggested_actions"], list)


# --- Alias ------------------------------------------------------------------

def test_tier_alias_matches_review_tier() -> None:
    p1 = _run("--review-tier", "--json")
    p2 = _run("--tier", "--json")
    assert p1.returncode == p2.returncode == 0
    d1 = json.loads(p1.stdout)
    d2 = json.loads(p2.stdout)
    assert d1["review_tier"] == d2["review_tier"]
    assert d1["label"] == d2["label"]


# --- Sanity on a known tier -------------------------------------------------

def test_review_tier_t6_for_status_dashboard_change() -> None:
    """If tools/vbb-status-dashboard.py is in the working tree, tier should
    be T6 (architecture / hooks / CI tool)."""
    p = _run("--review-tier", "--json")
    data = json.loads(p.stdout)
    # The dashboard itself is untracked (we're in the middle of editing it).
    # When vbb-status-dashboard.py is in the diff, it must classify T6.
    if data.get("files_analyzed", 0) > 0 and "tools/vbb-status-dashboard.py" in str(data):
        assert data["review_tier"] == "T6", (
            f"status-dashboard edit should be T6, got {data['review_tier']}"
        )


if __name__ == "__main__":
    tests = [
        test_help_lists_review_tier_flag,
        test_default_dashboard_unchanged_without_flag,
        test_review_tier_text_output_structure,
        test_review_tier_json_has_all_required_fields,
        test_review_tier_json_always_advisory,
        test_review_tier_json_confidence_value,
        test_review_tier_json_reasons_is_list,
        test_review_tier_json_suggested_actions_is_list,
        test_tier_alias_matches_review_tier,
        test_review_tier_t6_for_status_dashboard_change,
    ]
    for t in tests:
        t()
        print(f"  OK  {t.__name__}")
    print(f"\nOK — {len(tests)} tests passed")
