#!/usr/bin/env python3
"""
Tests for Phase 2 Run 1 extensions to tools/vbb-loop-closure-check.py

Covers 3 new checks:
  - --validate-claims (P0-1.1)
  - --validate-plan (P0-2.1)
  - --validate-test-audit (P0-3.1)

Each check is invoked against a synthetic run directory. We build a
COMPLETE valid run (all required phases for STRUCTUREE) so the loop
closure check passes, then add the specific artifact under test.

Usage:
    pytest tests/test_loop_closure_p2.py -q
"""

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-loop-closure-check.py"
PYTHON = sys.executable

# A minimal frontmatter for STRUCTUREE phase artifacts
_FM = textwrap.dedent("""\
    ---
    run_id: "{run_id}"
    phase: "{phase}"
    voie: "STRUCTUREE"
    status: "READY"
    agent: "claude-code"
    started_at: "2026-05-23T10:00:00Z"
    ended_at: "2026-05-23T10:30:00Z"
    next_phase: null
    artifacts_consumed: []
    artifacts_produced: []
    ---

    # {phase}

    {body}
""")


def _write(path: Path, run_id: str, phase: str, body: str) -> None:
    path.write_text(_FM.format(run_id=run_id, phase=phase, body=body))


def _build_complete_run(run_dir: Path, run_id: str) -> None:
    """Build a STRUCTUREE run with all 4 required phases (PASS loop-closure)."""
    _write(run_dir / "01_INTAKE.md", run_id, "01_INTAKE", "## Objectif\n\ntest.")
    _write(run_dir / "04_PLAN.md", run_id, "04_PLAN", "stub plan for closure")
    _write(run_dir / "05_EXECUTION.md", run_id, "05_EXECUTION", "stub execution")
    _write(run_dir / "07_CLOSEOUT.md", run_id, "07_CLOSEOUT", "stub closeout")


def _invoke(run_dir: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(TOOL), str(run_dir), *flags],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# P0-1.1 — --validate-claims
# ---------------------------------------------------------------------------


def test_claims_coherent_passes() -> None:
    run_id = "2026-06-13_1200_claims-good"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / run_id
        run_dir.mkdir()
        _build_complete_run(run_dir, run_id)
        # overwrite 07_CLOSEOUT with a coherent version
        body = textwrap.dedent("""\
            ## Résultat

            - fixed: bar alignment (Evidence: pytest 24/24 PASS)
            - passes: contract lint clean

            ## Décisions prises

            - aligned docs (KNOWN LIMITATION: out-of-repo doc)
        """)
        (run_dir / "07_CLOSEOUT.md").write_text(
            _FM.format(
                run_id=run_id,
                phase="07_CLOSEOUT",
                body=body,
            )
        )
        proc = _invoke(run_dir, "--validate-claims", "--json")
        assert proc.returncode == 0, (
            f"expected 0, got {proc.returncode}\n"
            f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
        )


def test_claims_unsupported_fails() -> None:
    run_id = "2026-06-13_1201_claims-bad"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / run_id
        run_dir.mkdir()
        _build_complete_run(run_dir, run_id)
        # overwrite 07_CLOSEOUT with an unsupported claim
        body = textwrap.dedent("""\
            ## Résultat

            - fixed: bar alignment

            ## Décisions prises

            (none)
        """)
        (run_dir / "07_CLOSEOUT.md").write_text(
            _FM.format(
                run_id=run_id,
                phase="07_CLOSEOUT",
                body=body,
            )
        )
        proc = _invoke(run_dir, "--validate-claims", "--json")
        assert "MISSING_EVIDENCE" in proc.stdout or proc.returncode != 0, (
            f"expected MISSING_EVIDENCE or non-zero, got rc={proc.returncode}\n"
            f"stdout: {proc.stdout}"
        )


# ---------------------------------------------------------------------------
# P0-2.1 — --validate-plan
# ---------------------------------------------------------------------------

_PLAN_COMPLETE_BODY = textwrap.dedent("""\
    ## Objectif

    Reformulate the existing module.

    ## Pré-conditions

    - python 3.11 available

    ## Étapes ordonnées

    | # | Action | Fichiers cibles | Validation | Rollback |
    |---|--------|-----------------|------------|----------|
    | 1 | Reformat | foo.py | pytest | git revert |

    ## Critères d'acceptation (Definition of Done)

    - [ ] All tests pass

    ## Plan de rollback global

    git revert

    ## Risques identifiés

    - Side effect on callers

    ## Analyse d'impact

    - **Effectuée ?** : OUI (via t-vbb-impact-analyzer)
    - **Périmètre d'impact** : foo.py
    - **Risques d'effet de bord** : Aucun identifié
""")


def test_plan_complete_passes() -> None:
    run_id = "2026-06-13_1202_plan-good"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / run_id
        run_dir.mkdir()
        _build_complete_run(run_dir, run_id)
        # overwrite 04_PLAN with a complete plan
        (run_dir / "04_PLAN.md").write_text(
            _FM.format(
                run_id=run_id,
                phase="04_PLAN",
                body=_PLAN_COMPLETE_BODY,
            )
        )
        proc = _invoke(run_dir, "--validate-plan", "--json")
        assert proc.returncode == 0, (
            f"expected 0, got {proc.returncode}\n"
            f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
        )


def test_plan_missing_sections_fails() -> None:
    run_id = "2026-06-13_1203_plan-bad"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / run_id
        run_dir.mkdir()
        _build_complete_run(run_dir, run_id)
        # overwrite 04_PLAN with an incomplete plan
        body = textwrap.dedent("""\
            ## Objectif

            Test plan.

            ## Risques identifiés

            - one risk
        """)
        (run_dir / "04_PLAN.md").write_text(
            _FM.format(
                run_id=run_id,
                phase="04_PLAN",
                body=body,
            )
        )
        proc = _invoke(run_dir, "--validate-plan", "--json")
        assert "MISSING_SECTION" in proc.stdout or proc.returncode != 0, (
            f"expected MISSING_SECTION, got rc={proc.returncode}\nstdout: {proc.stdout}"
        )


# ---------------------------------------------------------------------------
# P0-3.1 — --validate-test-audit
# ---------------------------------------------------------------------------


def test_test_audit_with_recent_report_passes() -> None:
    run_id = "2026-06-13_1204_test-audit-ok"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / run_id
        run_dir.mkdir()
        _build_complete_run(run_dir, run_id)
        # create a fresh report in a temp audits dir
        empty_audits = Path(tmp) / "empty_audits"
        empty_audits.mkdir()
        (empty_audits / "test-coverage-FRESH.md").write_text("# fresh")
        proc = _invoke(
            run_dir,
            "--validate-test-audit",
            "--audits-dir",
            str(empty_audits),
            "--json",
        )
        assert proc.returncode == 0, (
            f"expected 0, got {proc.returncode}\n"
            f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
        )


def test_claims_fixed_price_not_detected_as_bugfix() -> None:
    """Regression: '- fixed-price contract signed' must NOT be detected as
    a bugfix claim (CLAIM_VERB_RE must require 'fixed' followed by ':',
    not 'fixed' as a word-prefix).
    """
    run_id = "2026-06-13_1209_fixed-price"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / run_id
        run_dir.mkdir()
        _build_complete_run(run_dir, run_id)
        # closeout with the regression pattern
        body = textwrap.dedent("""\
            ## Résultat

            - fixed-price contract signed (Evidence: pm_decision.md §3)
            - passes: contract lint clean

            ## Décisions prises

            (none)
        """)
        (run_dir / "07_CLOSEOUT.md").write_text(
            _FM.format(
                run_id=run_id,
                phase="07_CLOSEOUT",
                body=body,
            )
        )
        proc = _invoke(run_dir, "--validate-claims", "--json")
        assert proc.returncode == 0, (
            f"expected 0, got {proc.returncode}\n"
            f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
        )
        import json

        report = json.loads(proc.stdout)
        # Must be a real PASS, not a silent false positive
        assert report.get("exit_intent") == "PASS", (
            f"expected PASS, got {report.get('exit_intent')!r}\n"
            f"errors: {report.get('errors')}"
        )
        # No error must mention 'fixed-price' as a missed claim
        for err in report.get("errors", []):
            assert "fixed-price" not in str(err).lower(), (
                f"false positive on 'fixed-price': {err}"
            )


def test_test_audit_no_surface_marker_passes() -> None:
    run_id = "2026-06-13_1205_no-test-surface"
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / run_id
        run_dir.mkdir()
        _build_complete_run(run_dir, run_id)
        # overwrite 05_EXECUTION with a no-test-surface marker
        body = textwrap.dedent("""\
            ## No test surface

            Documentation-only run.
        """)
        (run_dir / "05_EXECUTION.md").write_text(
            _FM.format(
                run_id=run_id,
                phase="05_EXECUTION",
                body=body,
            )
        )
        empty_audits = Path(tmp) / "empty_audits"
        empty_audits.mkdir()
        proc = _invoke(
            run_dir,
            "--validate-test-audit",
            "--audits-dir",
            str(empty_audits),
            "--json",
        )
        assert proc.returncode == 0, (
            f"expected 0, got {proc.returncode}\n"
            f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
        )


if __name__ == "__main__":
    test_claims_coherent_passes()
    test_claims_unsupported_fails()
    test_claims_fixed_price_not_detected_as_bugfix()
    test_plan_complete_passes()
    test_plan_missing_sections_fails()
    test_test_audit_with_recent_report_passes()
    test_test_audit_no_surface_marker_passes()
    print("OK — 7 tests passed")
