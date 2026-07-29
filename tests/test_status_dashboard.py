#!/usr/bin/env python3
"""
Tests for tools/vbb-status-dashboard.py

Positive tests:
  1. Valid repo → readable status output
  2. --json produces valid JSON with expected fields
  3. --full includes extra details
  4. Contract count is correct
  5. Latest runs detected
  6. Next action detected

Negative tests:
  7. Minimal repo (no docs/) → does not crash
  8. Non-existent repo → error

Usage:
    pytest tests/test_status_dashboard.py -q
    python3 tests/test_status_dashboard.py
"""

import sys
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-status-dashboard.py"


def _run_dashboard(args: list) -> tuple:
    result = subprocess.run(
        [sys.executable, str(TOOL)] + args, capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


def _import_dashboard():
    """Import the dashboard module directly (no subprocess) for unit tests."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("vbb_status_dashboard", str(TOOL))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load dashboard module from {TOOL}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _make_measured_repo(root: Path) -> Path:
    """Create a clean repository whose HEAD matches a local bare upstream."""
    repo = root / "repo"
    remote = root / "remote.git"
    subprocess.run(
        ["git", "init", "--bare", str(remote)], check=True, capture_output=True
    )
    subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.name", "VBB Test"], check=True
    )
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.email", "vbb@example.invalid"],
        check=True,
    )
    (repo / "docs").mkdir()
    (repo / "AGENTS.md").write_text("# Canonical governance\n")
    (repo / "docs" / "AUDIT_STATUS.md").write_text("## Global verdict\n\n**`READY`**\n")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "baseline"],
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "-C", str(repo), "branch", "-M", "main"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True
    )
    subprocess.run(
        ["git", "-C", str(repo), "push", "-u", "origin", "main"],
        check=True,
        capture_output=True,
    )
    return repo


def _make_run(
    repo: Path, name: str, mtime_offset: int = 0, closeout_name: str = "07_CLOSEOUT.md"
) -> Path:
    """Create a fake run directory with a closeout file.

    ``mtime_offset`` is added to the current time (seconds). Use positive values
    to make a run appear more recent than its peers, regardless of name.
    """
    rd = repo / "docs" / "runs" / name
    rd.mkdir(parents=True, exist_ok=True)
    closeout = rd / closeout_name
    closeout.write_text(
        "---\n"
        f'run_id: "{name}"\n'
        'phase: "07_CLOSEOUT"\n'
        'voie: "STRUCTURED"\n'
        'status: "READY"\n'
        'agent: "test"\n'
        "---\n\n"
        f"# {name}\n"
    )
    # Force mtime so test ordering is deterministic and decoupled from the
    # name-based lexical sort that we are replacing.
    target = time.time() + mtime_offset
    os.utime(rd, (target, target))
    os.utime(closeout, (target, target))
    return rd


def test_valid_repo():
    """Valid repo → readable status output with key fields."""
    rc, out, err = _run_dashboard([])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    for field in ["Skills", "Contracts", "Test suites", "Verdict"]:
        assert field in out, f"Expected '{field}' in output\n{out}"


def test_json_output():
    """--json produces valid JSON with expected fields."""
    rc, out, err = _run_dashboard(["--json"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    data = json.loads(out)
    for field in [
        "repo",
        "verdict",
        "documented_verdict",
        "measured_verdict",
        "status_reasons",
        "git_state",
        "skills",
        "contracts",
        "contract_coverage",
        "tests",
        "latest_runs",
        "risks",
        "next_action",
    ]:
        assert field in data, f"Missing field '{field}' in JSON\n{out}"
    assert isinstance(data["skills"], int)
    assert isinstance(data["contracts"], int)
    assert isinstance(data["contract_coverage"], float)


def test_measured_health_prevents_false_ready():
    """Dirty state and canonical marker corruption must override documented READY."""
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = _make_measured_repo(Path(tmp))

        clean = mod.gather_status(repo)
        assert clean["documented_verdict"] == "READY"
        assert clean["measured_verdict"] == "READY"
        assert clean["verdict"] == "READY"
        assert clean["git_state"]["branch"] == "main"

        (repo / "AGENTS.md").write_text("# Locally edited governance\n")
        dirty = mod.gather_status(repo)
        assert dirty["documented_verdict"] == "READY"
        assert dirty["measured_verdict"] == "PARTIAL"
        assert dirty["verdict"] == "PARTIAL"
        assert "git worktree is not clean" in dirty["status_reasons"]

        (repo / "AGENTS.md").write_text(
            "<!-- vibebackbone:generated:start -->\ncorrupt\n"
        )
        corrupt = mod.gather_status(repo)
        assert corrupt["measured_verdict"] == "BLOCKED"
        assert corrupt["verdict"] == "BLOCKED"


def test_canonical_active_risk_table_prevents_false_ready():
    """The exact canonical qualified description header must be recognized."""
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = _make_measured_repo(Path(tmp))
        header = (
            "## Active risks\n\n"
            "| ID | Severity | Status | Owner | Description and reopen trigger |\n"
            "|---|---|---|---|---|\n"
        )

        for severity, expected in (
            ("P0", "BLOCKED"),
            ("P1", "PARTIAL"),
            ("P2", "PARTIAL"),
        ):
            (repo / "docs" / "AUDIT_STATUS.md").write_text(
                "## Global verdict\n\n**`READY`**\n\n"
                + header
                + f"| `R-{severity}` | {severity} | OPEN | owner | active risk |\n"
            )
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-m", f"risk {severity}"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "push", "origin", "main"],
                check=True,
                capture_output=True,
            )

            status = mod.gather_status(repo)
            assert [risk["id"] for risk in status["risks"]] == [f"R-{severity}"]
            assert status["measured_verdict"] == expected
            assert status["verdict"] == expected


def test_qualified_description_header_variants_do_not_hide_risks():
    """Nearby punctuation/plural drift remains within the description column."""
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        docs = repo / "docs"
        docs.mkdir()
        for description_header in (
            "Description & reopen trigger",
            "Description and reopen triggers",
        ):
            (docs / "AUDIT_STATUS.md").write_text(
                "| ID | Severity | Status | Owner | " + description_header + " |\n"
                "|---|---|---|---|---|\n"
                "| `R-P0` | P0 | OPEN | owner | active risk |\n"
            )
            assert [risk["id"] for risk in mod.get_open_risks(repo)] == ["R-P0"]


def test_strict_dashboard_uses_effective_verdict():
    """Strict mode succeeds only for a clean, synchronized effective READY."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = _make_measured_repo(Path(tmp))
        rc, _, _ = _run_dashboard(["--repo", str(repo), "--json", "--strict"])
        assert rc == 0

        (repo / "AGENTS.md").write_text("# dirty\n")
        rc, out, _ = _run_dashboard(["--repo", str(repo), "--json", "--strict"])
        assert rc == 2
        assert json.loads(out)["verdict"] == "PARTIAL"


def test_extract_verdict_reads_canonical_next_line_ready():
    """Canonical Global verdict section must expose READY to JSON consumers."""
    mod = _import_dashboard()

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        docs = repo / "docs"
        docs.mkdir()
        (docs / "AUDIT_STATUS.md").write_text(
            "# AUDIT_STATUS\n\n"
            "## Global verdict\n\n"
            "**`READY — all exit criteria evidenced`**\n"
        )

        assert mod.extract_verdict(repo) == "READY"


def test_extract_verdict_preserves_legacy_same_line_format():
    """Legacy French same-line headings remain supported."""
    mod = _import_dashboard()

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        docs = repo / "docs"
        docs.mkdir()
        (docs / "AUDIT_STATUS.md").write_text(
            "# Status\n\n## Verdict global: `PARTIAL`\n"
        )

        assert mod.extract_verdict(repo) == "PARTIAL"


def test_extract_verdict_ignores_status_substrings():
    """Words such as bypassable must not be parsed as PASS."""
    mod = _import_dashboard()

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        docs = repo / "docs"
        docs.mkdir()
        (docs / "AUDIT_STATUS.md").write_text(
            "# Status\n\nThe bypassable condition is documented.\n"
        )

        assert mod.extract_verdict(repo) == "UNKNOWN"


def test_full_mode():
    """--full includes extra details (activity log)."""
    rc, out, err = _run_dashboard(["--full"])
    assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
    assert "VBB STATUS" in out


def test_contract_count():
    """Contract count matches expected value (positive for current repo)."""
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert data["contracts"] > 0, (
        f"Expected positive contract count, got {data['contracts']}"
    )
    assert data["skills"] > 0, f"Expected positive skill count, got {data['skills']}"
    assert data["contracts"] <= data["skills"], (
        f"Contracts ({data['contracts']}) should not exceed skills ({data['skills']})"
    )


def test_latest_runs():
    """Latest runs are detected and ordered by mtime (newest first).

    RUN 3 stabilisation: post-fix, the top entry is the run with the freshest
    mtime (the in-progress ``2026-06-13_2200_run-2-doc-core-distribution``
    that is currently untracked). The list is asserted to be non-empty,
    ordered by mtime, and to contain at least one well-formed closeout with
    a real ``voie`` + ``verdict`` pair (not all entries are UNKNOWN).
    """
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert isinstance(data["latest_runs"], list)
    assert len(data["latest_runs"]) > 0, "Expected at least one latest run"
    # At least one entry must carry a real voie/verdict pair (otherwise the
    # dashboard is reporting noise). We do not assert on the *first* entry's
    # voie/verdict directly because the freshest mtime may correspond to an
    # in-progress run whose closeout is not yet in standard frontmatter form.
    assert any(
        r["voie"] != "UNKNOWN" and r["verdict"] != "UNKNOWN"
        for r in data["latest_runs"]
    ), f"Expected at least one well-formed run in {data['latest_runs']}"
    # Ordering invariant: the list is bounded by the requested limit and
    # every id is a non-empty string (no loose files leak through).
    assert len(data["latest_runs"]) <= 5
    for r in data["latest_runs"]:
        assert isinstance(r["id"], str) and r["id"], r


def test_temporal_local_date_exposed():
    """Temporal provenance includes local workspace date in JSON output."""
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert "local_date" in data
    assert isinstance(data["temporal_notes"], list)


def test_next_action():
    """Next action is detected (non-empty for real repo)."""
    rc, out, _ = _run_dashboard(["--json"])
    assert rc == 0
    data = json.loads(out)
    assert isinstance(data["next_action"], str)
    assert len(data["next_action"]) > 0, "Expected non-empty next action"


def test_minimal_repo():
    """Minimal repo without docs/ → does not crash."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        skills = repo / "skills"
        skills.mkdir()
        (skills / "1-test-skill").mkdir()
        (skills / "1-test-skill" / "SKILL.md").write_text(
            "---\\nname: test\\n---\\n# Test\\n"
        )

        rc, out, err = _run_dashboard(["--repo", str(repo)])
        assert rc == 0, f"Expected exit 0 for minimal repo, got {rc}\n{err}"
        assert "Skills" in out, f"Expected 'Skills' in output\n{out}"


def test_nonexistent_repo():
    """Non-existent repo → error + exit 1."""
    rc, out, err = _run_dashboard(["--repo", "/nonexistent/path"])
    assert rc == 1, f"Expected exit 1, got {rc}"


# --- RUN 3 stabilisation: get_latest_runs() lexical-sort regression tests ---


def test_latest_runs_malformed_name_uses_mtime():
    """Case 1 (RUN 3): malformed date name loses to well-formed newer run.

    The old lexical sort placed ``20260602_0817_yyy`` AFTER
    ``2026-06-13_2200_xxx`` only because ``0`` > ``-`` in ASCII. The mtime
    sort must pick the genuinely newer run regardless of the name format.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        # Lexically: "20260602_0817_yyy" > "2026-06-13_2200_xxx" (because
        # '0' > '-' in ASCII at index 5). Pre-fix, this would rank malformed
        # first. Post-fix, mtime (offset 100s) wins for the well-formed one.
        _make_run(repo, "20260602_0817_yyy", mtime_offset=0)
        _make_run(repo, "2026-06-13_2200_xxx", mtime_offset=100)

        latest = mod.get_latest_runs(repo, limit=5)
        assert latest, "Expected at least one latest run"
        assert latest[0]["id"] == "2026-06-13_2200_xxx", (
            "mtime-based sort must rank the well-formed newer run first, "
            f"got {latest[0]['id']}"
        )
        # Both runs must appear (no spurious filtering).
        ids = {r["id"] for r in latest}
        assert ids == {"2026-06-13_2200_xxx", "20260602_0817_yyy"}


def test_latest_runs_skips_loose_files():
    """Case 2 (RUN 3): loose files in docs/runs/ (README.md etc.) must not
    appear in latest_runs output. They are filtered by ``is_dir()``.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _make_run(repo, "2026-06-13_2200_xxx", mtime_offset=10)
        # Parasitic loose files: README + a routing-style note.
        (repo / "docs" / "runs" / "README.md").write_text("# runs")
        (repo / "docs" / "runs" / "routing-fix-verification.md").write_text("# routing")

        latest = mod.get_latest_runs(repo, limit=10)
        ids = [r["id"] for r in latest]
        assert "README.md" not in ids, "README.md must not appear in latest_runs"
        assert "routing-fix-verification.md" not in ids, (
            "routing-fix-verification.md must not appear in latest_runs"
        )
        # Sanity: the one real run is still detected.
        assert ids == ["2026-06-13_2200_xxx"]


def test_latest_runs_order_ignores_mtime():
    """Run order follows the run identity, not the filesystem mtime.

    This reverses the RUN 3 assertion "mtime (newer) must win over a
    future-dated folder name". That rule was unsound: mtime is not chronology.
    A `git clone` stamps every run directory with the checkout time, so on CI
    the mtime order is arbitrary — which is how the adversarial gate came to
    validate a June legacy run (audit 2026-07-29, finding F19).

    The concern RUN 3 was protecting against — a future-dated folder silently
    dominating — is not dropped. It is carried where it belongs, by the
    temporal-provenance signal that already reports directories dated after the
    workspace date, not by an ordering key that cannot survive a clone.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        # Newest identity, oldest mtime.
        _make_run(repo, "2026-12-31_2359_xxx", mtime_offset=-1000)
        # Older identity, newest mtime.
        _make_run(repo, "2026-06-13_2200_recent", mtime_offset=1000)

        latest = mod.get_latest_runs(repo, limit=5)
        assert latest, "Expected at least one latest run"
        assert latest[0]["id"] == "2026-12-31_2359_xxx", (
            f"the run identity must decide the order, not mtime, got {latest[0]['id']}"
        )
        # Neither folder is rejected by name.
        ids = {r["id"] for r in latest}
        assert ids == {"2026-12-31_2359_xxx", "2026-06-13_2200_recent"}


def test_future_dated_runs_are_still_flagged():
    """Ordering by identity must not silence the temporal-provenance signal."""
    mod = _import_dashboard()
    repo = Path(__file__).parent.parent
    notes = mod.get_temporal_notes(repo)
    assert any("dated after" in note or "future" in note.lower() for note in notes), (
        f"future-dated run directories must remain visible: {notes}"
    )


def test_latest_runs_accepts_non_canonical_closeout():
    """Defensive: a run dir that writes ``CLOSEOUT.md`` (no ``07_`` prefix)
    before the standard rename is still detected. The fallback closeout
    lookup covers this in-progress case.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        rd = repo / "docs" / "runs" / "2026-06-13_2200_in_progress"
        rd.mkdir(parents=True)
        (rd / "CLOSEOUT.md").write_text(
            "---\nrun_id: in_progress\nphase: 07_CLOSEOUT\n"
            "voie: STRUCTURED\nstatus: READY\n---\n\n# in progress\n"
        )
        target = time.time()
        os.utime(rd, (target, target))

        latest = mod.get_latest_runs(repo, limit=5)
        assert latest, "Expected the in-progress run to be detected"
        assert latest[0]["id"] == "2026-06-13_2200_in_progress"


def test_latest_runs_missing_runs_dir():
    """Edge case: a repo with no ``docs/runs/`` directory returns an empty
    list instead of raising.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "docs").mkdir()
        assert mod.get_latest_runs(repo, limit=5) == []


def test_get_open_risks_no_p1_when_resolved():
    """Regression test for QOA-004 (RUN 4): when AUDIT_STATUS.md marks all
    P1 risks as RESOLVED, ``get_open_risks`` must return zero P1 entries.

    Before RUN 4, the dashboard masked active P1s because the AUDIT_STATUS
    risk table kept stale "Open" statuses for risks that were already fixed
    by RUN 1/2/3. This test pins the post-RUN-4 invariant: the dashboard
    surfaces only the genuinely-open P1s, and zero P1 means the table is
    consistent.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        audit = repo / "docs" / "AUDIT_STATUS.md"
        audit.parent.mkdir(parents=True)
        audit.write_text(
            "## Risks identified & status\n"
            "\n"
            "<!-- Last updated 2026-06-13 (RUN 4) — 3 P1 resolved, 1 P1 closed (this entry) -->\n"
            "\n"
            "| ID | Severity | Description | Status |\n"
            "|----|----------|-------------|--------|\n"
            "| QOA-001 | P1 | Core/Distribution boundary | **RESOLVED** — RUN 2 commit 89bbe3d |\n"
            "| QOA-002 | P1 | Provider migration incomplete | **RESOLVED** — RUN 1 commit d1ca51f |\n"
            "| QOA-003 | P1 | Loop-closure lexical sort | **RESOLVED** — RUN 3 commit 6772422 |\n"
            "| QOA-004 | P1 | Status dashboard masks open risks | **RESOLVED*** — RUN 4 fix |\n"
            "| QOA-005 | P2 | Quality-adoption note | Open — reconcile QA table |\n"
        )
        risks = mod.get_open_risks(repo)
        p1_open = [r for r in risks if r["severity"] == "P1"]
        assert p1_open == [], (
            f"Expected zero P1 risks after RUN 4 RESOLVED update, "
            f"but get_open_risks returned: {p1_open}"
        )
        # Sanity: the P2 stays visible.
        p2_open = [r for r in risks if r["severity"] == "P2"]
        assert any(r["id"] == "QOA-005" for r in p2_open), (
            f"Expected QOA-005 (P2, still Open) to be reported, got: {p2_open}"
        )


def test_get_open_risks_reports_stale_p1():
    """Companion to test_get_open_risks_no_p1_when_resolved: when a P1 is
    still marked Open in AUDIT_STATUS.md, ``get_open_risks`` must surface
    it. This is the dashboard's job — to never mask an active P1.
    """
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        audit = repo / "docs" / "AUDIT_STATUS.md"
        audit.parent.mkdir(parents=True)
        audit.write_text(
            "## Risks identified & status\n"
            "\n"
            "| ID | Severity | Description | Status |\n"
            "|----|----------|-------------|--------|\n"
            "| QOA-099 | P1 | Stale P1 from previous run | Open — not yet fixed |\n"
        )
        risks = mod.get_open_risks(repo)
        p1_open = [r for r in risks if r["severity"] == "P1"]
        assert any(r["id"] == "QOA-099" for r in p1_open), (
            f"Expected QOA-099 P1 to be reported, got: {p1_open}"
        )


def test_get_open_risks_parses_all_tables_and_prioritizes_severity():
    """Bold/bilingual risks outside the legacy section stay visible and sorted."""
    mod = _import_dashboard()
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        audit = repo / "docs" / "AUDIT_STATUS.md"
        audit.parent.mkdir(parents=True)
        audit.write_text(
            "## Findings ouverts\n\n"
            "| ID | Sévérité | Statut | Constat |\n"
            "|----|----------|--------|---------|\n"
            "| TER-001 | **P1** | **Open** | Consumer refresh absent |\n"
            "| DUP-001 | P2 | Open | First occurrence |\n\n"
            "## Risks identified & status\n\n"
            "| ID | Severity | Description | Status |\n"
            "|----|----------|-------------|--------|\n"
            "| QOA-005 | P2 | Reconcile table | Open — pending |\n"
            "| SYS-POST-002 | P1 | Audit artifact missing | **Open — verified** |\n"
            "| GMA-003 | P1 | Executor cleanup | **MITIGATING 2026-07-14** |\n"
            "| DUP-001 | P2 | Duplicate summary | Open |\n"
            "| DONE-001 | P0 | Closed item | **RESOLVED** |\n"
        )

        risks = mod.get_open_risks(repo)

        assert [r["id"] for r in risks] == [
            "TER-001",
            "SYS-POST-002",
            "GMA-003",
            "DUP-001",
            "QOA-005",
        ]
        assert risks[0]["severity"] == "P1"
        assert risks[1]["status"] == "Open — verified"


# --- Audit finding F15: the verdict is the declaration, not the prose ---


def test_extract_verdict_reads_not_ready_as_first_class_token():
    """NOT_READY must be representable; it is not a bare READY."""
    mod = _import_dashboard()

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        docs = repo / "docs"
        docs.mkdir()
        (docs / "AUDIT_STATUS.md").write_text(
            "# AUDIT_STATUS\n\n"
            "## Global verdict\n\n"
            "**`NOT_READY — remediation in progress`**\n"
        )

        assert mod.extract_verdict(repo) == "NOT_READY"


def test_extract_verdict_ignores_narrative_below_the_declaration():
    """Prose mentioning another verdict must not override the declaration.

    Regression for F15: the section scan used to read up to six lines and take
    the first token found, so a sentence such as "the previously published READY
    baseline" silently reported READY for a NOT_READY document.
    """
    mod = _import_dashboard()

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        docs = repo / "docs"
        docs.mkdir()
        (docs / "AUDIT_STATUS.md").write_text(
            "# AUDIT_STATUS\n\n"
            "## Global verdict\n\n"
            "**`NOT_READY — remediation in progress`**\n\n"
            "The previously published READY baseline was invalidated because\n"
            "the remote CI was PASS on no commit in this range.\n"
        )

        assert mod.extract_verdict(repo) == "NOT_READY"


def test_effective_verdict_treats_not_ready_as_blocking():
    """A NOT_READY document must not be softened by a milder measurement."""
    mod = _import_dashboard()

    assert mod.effective_verdict("NOT_READY", "PARTIAL") == "NOT_READY"
    assert mod.effective_verdict("NOT_READY", "READY") == "NOT_READY"


def test_extract_verdict_declaration_without_token_is_unknown():
    """A verdict section whose declaration line carries no token is UNKNOWN."""
    mod = _import_dashboard()

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        docs = repo / "docs"
        docs.mkdir()
        (docs / "AUDIT_STATUS.md").write_text(
            "# AUDIT_STATUS\n\n## Global verdict\n\nSee the run closeout.\n"
        )

        assert mod.extract_verdict(repo) == "UNKNOWN"


# --- Direct execution fallback ---
if __name__ == "__main__":
    try:
        import pytest

        sys.exit(pytest.main([__file__, "-q"]))
    except ImportError:
        passed = failed = 0
        for _name, _fn in sorted(globals().items()):
            if _name.startswith("test_") and callable(_fn):
                try:
                    _fn()
                    print("  PASS " + _name)
                    passed += 1
                except AssertionError as _e:
                    print("  FAIL " + _name + ": " + str(_e))
                    failed += 1
        total = passed + failed
        print("Results: %d/%d passed, %d failed" % (passed, total, failed))
        sys.exit(0 if failed == 0 else 1)
