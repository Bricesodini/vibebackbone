#!/usr/bin/env python3
"""
Tests for tools/vbb-review-threshold-poc.py (P0-4 POC, 2026-06-13).

Covers the calibration cases used in the POC report:
  - T1 (doc simple): README.md, docs/CONTEXT.md
  - T2 (tests): tests/foo.py, distributions/*/tests/test_*.py
  - T3 (tooling local non critique): tools/vbb-architecture.py
  - T4 (templates/skills/distrib-READMEs): docs/templates/*, skills/*, core.README.md
  - T5 (gouvernance Core): AGENTS.md, CONVENTIONS.md, docs/CONTEXT.md
  - T6 (architecture/hooks/CI): scripts/hooks/*, .github/workflows/*.yml
  - T7 (proxy/credentials): distributions/*/proxy/config.py
  - T8 (production write surface): distributions/*/proxy/actions.py

Plus: MAX-wins resolution, empty-list edge, unknown-path warning.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-review-threshold-poc.py"
PYTHON = sys.executable


def _run(*paths: str, json_mode: bool = False) -> subprocess.CompletedProcess:
    args = [PYTHON, str(TOOL), *paths]
    if json_mode:
        args.append("--json")
    return subprocess.run(args, capture_output=True, text=True)


# --- Per-tier calibration ---------------------------------------------------

def test_t1_doc_simple() -> None:
    p = _run("README.md", json_mode=True)
    assert p.returncode == 0
    r = json.loads(p.stdout)
    assert r["tier"] == "T1", f"README.md should be T1, got {r['tier']}"


def test_t2_tests() -> None:
    """Plain test files (no security surface) must classify as T2."""
    p = _run("tests/test_foo.py", "tests/test_status_dashboard.py",
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T2", f"plain tests should be T2, got {r['tier']}"


def test_t2_tests_in_security_surface_escalates_to_t7() -> None:
    """Tests inside the bypass-lint directory match both T2 and T7.
    With MAX-wins, the credential surface (T7) must win."""
    p = _run("distributions/hermes/bypass-lint/tests/test_allowlist.py",
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T7", (
        f"bypass-lint tests should escalate to T7 (MAX-wins), got {r['tier']}"
    )


def test_t3_tooling_local() -> None:
    p = _run("tools/vbb-architecture.py", json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T3", f"vbb-architecture.py should be T3, got {r['tier']}"


def test_t4_distrib_readme_and_skills() -> None:
    p = _run("core.README.md",
             "distributions/hermes/bypass-lint/README.md",
             "skills/t-vbb-test-coverage-mapper/SKILL.md",
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T4", f"distrib-readme + skills should be T4, got {r['tier']}"


def test_t5_governance_core() -> None:
    p = _run("AGENTS.md", "CONVENTIONS.md", "docs/CONTEXT.md",
             "docs/DISTRIBUTIONS.md", "docs/adr/0013-foo.md",
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T5", f"governance files should be T5, got {r['tier']}"


def test_t6_hooks_and_ci() -> None:
    p = _run("scripts/hooks/pre-commit-framework-gate",
             ".github/workflows/smoke.yml",
             "tools/vbb-gate-check.py",
             "tools/vbb-status-dashboard.py",
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T6", f"hooks/CI/gate-check should be T6, got {r['tier']}"


def test_t7_proxy_credentials() -> None:
    p = _run("distributions/hermes/proxy/config.py",
             "distributions/hermes/proxy/runtime/secrets.yaml",
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T7", f"proxy/credentials should be T7, got {r['tier']}"


def test_t8_production_write_surface() -> None:
    p = _run("distributions/hermes/proxy/actions.py",
             "distributions/hermes/proxy/audit.py",
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T8", f"proxy actions/audit should be T8, got {r['tier']}"


def test_t8_specific_files_only() -> None:
    """T8 must be restricted to actions.py and audit.py, not catch-all words
    like 'purge' or 'destroy' (those don't exist in VBB anyway, but the
    pattern must not over-match if someone adds such files)."""
    p = _run("some/purge/file.py", "some/destroy/log.txt",
             json_mode=True)
    r = json.loads(p.stdout)
    # these should NOT match T8 (no proxy path)
    assert r["tier"] != "T8", (
        f"generic 'purge'/'destroy' should not auto-classify as T8, got {r['tier']}"
    )


# --- Resolution rule --------------------------------------------------------

def test_max_wins_resolution() -> None:
    """When multiple tiers match across files, the MAX tier must win."""
    p = _run("README.md",                          # T1
             "tests/test_foo.py",                  # T2
             "distributions/hermes/proxy/actions.py",  # T8
             json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] == "T8", f"MAX should be T8, got {r['tier']}"
    # All three tiers should appear in matched_tiers
    matched = r.get("matched_tiers", [])
    assert any("T1" in m for m in matched)
    assert any("T2" in m for m in matched)
    assert any("T8" in m for m in matched)


# --- Edge cases -------------------------------------------------------------

def test_unmapped_path_warns() -> None:
    p = _run("some/random/unknown.xyz", json_mode=True)
    r = json.loads(p.stdout)
    assert r["tier"] is None
    assert r["tier_rank"] == 0
    assert "warning" in r
    assert "no tier matched" in r["warning"]


def test_text_output_format() -> None:
    p = _run("README.md")
    out = p.stdout
    assert "VBB Review-Tier POC" in out
    assert "Tier proposé" in out
    assert "T1" in out


# --- Dry-run guarantee ------------------------------------------------------

def test_no_side_effects() -> None:
    """POC must not write to disk, not commit, not push. Smoke check via git status."""
    before = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).stdout
    p = _run("tools/vbb-loop-closure-check.py",
             "distributions/hermes/proxy/actions.py")
    after = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).stdout
    assert before == after, (
        f"git status changed during POC run (side-effect!):\nbefore={before}\nafter={after}"
    )
    assert p.returncode == 0


if __name__ == "__main__":
    tests = [
        test_t1_doc_simple,
        test_t2_tests,
        test_t2_tests_in_security_surface_escalates_to_t7,
        test_t3_tooling_local,
        test_t4_distrib_readme_and_skills,
        test_t5_governance_core,
        test_t6_hooks_and_ci,
        test_t7_proxy_credentials,
        test_t8_production_write_surface,
        test_t8_specific_files_only,
        test_max_wins_resolution,
        test_unmapped_path_warns,
        test_text_output_format,
        test_no_side_effects,
    ]
    for t in tests:
        t()
        print(f"  OK  {t.__name__}")
    print(f"\nOK — {len(tests)} tests passed")
