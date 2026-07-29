#!/usr/bin/env python3
"""
Tests for tools/vbb-loop-closure-check.py

Positive tests (exit 0):
  1. RAPIDE  : 01_INTAKE + 05_EXECUTION + 07_CLOSEOUT
  2. STRUCTUREE : 01_INTAKE + 04_PLAN + 05_EXECUTION + 07_CLOSEOUT
  3. AUDIT   : 01_INTAKE + 02_AUDIT + 03_DECISION + 07_CLOSEOUT
  4. CLOTURE : 07_CLOSEOUT only (no 01_INTAKE)
  5. RAPIDE-ZERO : closeout with voie=RAPIDE-ZERO → PASS (no phases required)
  6. RAPIDE-MINIMAL : 05_PATCH_SUMMARY only → PASS

Negative tests (exit 1):
  7. Missing 07_CLOSEOUT
  8. Missing required phase for voie (STRUCTUREE without 04_PLAN)
  9. Missing 01_INTAKE for non-CLOTURE voie
  10. Frontmatter missing required field
  11. Frontmatter placeholder not replaced
  12. Run directory not found
  13. Invalid voie value

Usage:
    pytest tests/test_loop_closure.py -q
    python3 tests/test_loop_closure.py
"""

import os
import sys
import subprocess
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-loop-closure-check.py"


def _controlled_env(**overrides: str) -> dict[str, str]:
    """Make subprocess tests independent from the invoking shell's VBB state."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("VBB_")}
    env.update(overrides)
    return env


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_FM = textwrap.dedent("""\
    ---
    run_id: "{run_id}"
    phase: "{phase}"
    voie: "{voie}"
    status: "READY"
    agent: "claude-code"
    started_at: "2026-05-23T10:00:00Z"
    ended_at: "2026-05-23T10:30:00Z"
    next_phase: null
    artifacts_consumed: []
    artifacts_produced: []
    ---

    # {phase}
""")


def _make_artifact(path: Path, run_id: str, phase: str, voie: str) -> None:
    path.write_text(_VALID_FM.format(run_id=run_id, phase=phase, voie=voie))


def _add_frontmatter_fields(path: Path, fields: str) -> None:
    content = path.read_text()
    path.write_text(content.replace("---\n", f"---\n{fields}", 1))


def _add_valid_assurance(
    intake_path: Path,
    closeout_path: Path,
    *,
    authorization_status: str = "AUTHORIZED",
) -> None:
    _add_frontmatter_fields(intake_path, 'assurance_governance_version: "1.0"\n')
    _add_frontmatter_fields(
        closeout_path, 'assurance_governance_version: "1.0"\nkind: "CLOSEOUT"\n'
    )
    required_ids = '["design-pre"]' if authorization_status == "AUTHORIZED" else "[]"
    closeout_path.write_text(
        closeout_path.read_text()
        + textwrap.dedent(
            f"""

            ## Assurance

            ```yaml
            ASSURANCE_STATUS:
              schema_version: "1.0"
              subject: "test delivery"
              gate_results:
                - gate_id: "design-pre"
                  gate_family: "DESIGN"
                  checkpoint: "PRE_IMPLEMENTATION"
                  subject: "observable behavior"
                  verdict: "PASS"
                  evidence: ["test fixture"]
                  reasons: ["contract is complete"]
              implementation_authorization:
                status: "{authorization_status}"
                required_gate_ids: {required_ids}
                reasons: ["explicit fixture decision"]
            ```
            """
        )
    )


def _run(run_id: str, runs_dir: Path, extra_args=None):
    """Invoke vbb-loop-closure-check.py and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, str(TOOL)]
    if extra_args:
        cmd.extend(extra_args)
    cmd.extend([run_id, "--runs-dir", str(runs_dir)])
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=_controlled_env(),
    )
    return result.returncode, result.stdout, result.stderr


def _add_bound_subject(closeout: Path, run_id: str, commit: str) -> None:
    closeout.write_text(
        closeout.read_text()
        + textwrap.dedent(
            f"""

            ```yaml
            adversarial:
              certification:
                run_id: "{run_id}"
                candidate_id: "test-candidate"
                bound_to:
                  run_id: "{run_id}"
                  commit: "{commit}"
                  corpus_version: "1"
            ```
            """
        )
    )


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------


def test_rapide_complete():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_rapide"
        d.mkdir()
        rid = "2026-01-01_1000_rapide"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out, f"Expected PASS in output\n{out}"


def test_structuree_complete():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_struct"
        d.mkdir()
        rid = "2026-01-01_1000_struct"
        for phase in ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out


def test_path_and_bare_id_resolve_the_same_run():
    """F9 is fixed only to prevent subject divergence in exact verification."""
    with tempfile.TemporaryDirectory() as tmp:
        runs = Path(tmp)
        d = runs / "2026-01-01_1000_struct"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")

        id_result = subprocess.run(
            [sys.executable, str(TOOL), rid, "--runs-dir", str(runs)],
            capture_output=True,
            text=True,
            env=_controlled_env(),
        )
        path_result = subprocess.run(
            [sys.executable, str(TOOL), str(d), "--runs-dir", str(runs)],
            capture_output=True,
            text=True,
            env=_controlled_env(),
        )
        assert id_result.returncode == path_result.returncode == 0
        assert f"Run     : {rid}" in id_result.stdout
        assert f"Run     : {rid}" in path_result.stdout


def test_expected_commit_requires_matching_bound_subject():
    with tempfile.TemporaryDirectory() as tmp:
        runs = Path(tmp)
        subprocess.run(
            ["git", "init", str(runs)],
            check=True,
            capture_output=True,
            env=_controlled_env(),
        )
        subprocess.run(
            ["git", "-C", str(runs), "config", "user.name", "VBB Test"],
            check=True,
            env=_controlled_env(),
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(runs),
                "config",
                "user.email",
                "vbb@example.invalid",
            ],
            check=True,
            env=_controlled_env(),
        )
        (runs / "candidate").write_text("candidate\n")
        subprocess.run(
            ["git", "-C", str(runs), "add", "candidate"],
            check=True,
            env=_controlled_env(),
        )
        subprocess.run(
            ["git", "-C", str(runs), "commit", "-m", "candidate"],
            check=True,
            capture_output=True,
            env=_controlled_env(),
        )
        d = runs / "2026-01-01_1000_bound"
        d.mkdir()
        rid = d.name
        commit = subprocess.run(
            ["git", "-C", str(runs), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            env=_controlled_env(),
        ).stdout.strip()
        for phase in ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        _add_bound_subject(d / "07_CLOSEOUT.md", rid, commit)

        rc, out, err = _run(
            rid,
            runs,
            extra_args=["--expected-commit", commit, "--strict"],
        )
        assert rc == 0, out + err
        assert "release subject bound" in out

        rc, out, err = _run(
            rid,
            runs,
            extra_args=["--expected-commit", "b" * 40, "--strict"],
        )
        assert rc == 2
        assert "does not match expected commit" in out + err


def test_expected_commit_requires_explicit_run():
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "--runs-dir",
                tmp,
                "--expected-commit",
                "a" * 40,
                "--strict",
            ],
            capture_output=True,
            text=True,
            env=_controlled_env(),
        )
        assert proc.returncode == 64
        assert "explicit run" in proc.stdout + proc.stderr


def test_expected_commit_empty_is_invalid_and_fail_closed():
    """An explicitly supplied empty SHA must never disable certification."""
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "2026-07-29_1941_run1-exact-release-measurement",
                "--runs-dir",
                tmp,
                "--expected-commit",
                "",
                "--strict",
                "--json",
            ],
            capture_output=True,
            text=True,
            env=_controlled_env(),
        )
        assert proc.returncode != 0
        assert '"exit_intent": "FAIL"' in proc.stdout
        assert '"reason": "invalid_or_empty_expected_commit"' in proc.stdout


def test_expected_commit_invalid_variants_fail_closed():
    for value in ("   ", "abc", "g" * 40):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "2026-07-29_1941_run1-exact-release-measurement",
                    "--runs-dir",
                    tmp,
                    "--expected-commit",
                    value,
                    "--strict",
                    "--json",
                ],
                capture_output=True,
                text=True,
                env=_controlled_env(),
            )
            assert proc.returncode != 0
            assert "invalid_or_empty_expected_commit" in proc.stdout

    # A full-hex SHA reaches Git object validation and must still fail closed.
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "2026-07-29_1941_run1-exact-release-measurement",
                "--runs-dir",
                tmp,
                "--expected-commit",
                "f" * 40,
                "--strict",
                "--json",
            ],
            capture_output=True,
            text=True,
            env=_controlled_env(),
        )
        assert proc.returncode != 0


def test_audit_complete():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_audit"
        d.mkdir()
        rid = "2026-01-01_1000_audit"
        for phase in ["01_INTAKE", "02_AUDIT", "03_DECISION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "AUDIT")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out


def test_historical_run_without_knowledge_version_remains_valid():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_historical"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, out


def test_governance_v1_accepts_valid_harvest():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_knowledge-valid"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\nknowledge_harvest: "NONE"\n',
        )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, out
        assert "Knowledge Harvest disposition" in out


def test_post_cutover_run_cannot_omit_knowledge_governance():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_knowledge-omitted"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "knowledge_governance_version is required" in out
        assert "knowledge_harvest" in out


def test_governance_v1_accepts_observation_recorded():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_knowledge-observation"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "OBSERVATION_RECORDED"\n',
        )
        _add_valid_assurance(d / "01_INTAKE.md", d / "07_CLOSEOUT.md")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, out


def test_governance_v1_accepts_evidence_linked():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_knowledge-evidence"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "EVIDENCE_LINKED"\n',
        )
        _add_valid_assurance(d / "01_INTAKE.md", d / "07_CLOSEOUT.md")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, out


def test_historical_run_without_assurance_remains_valid():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-07-27_2117_historical-assurance"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\nknowledge_harvest: "NONE"\n',
        )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, out


def test_assurance_v1_accepts_explicit_authorization():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_assurance-valid"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\nknowledge_harvest: "NONE"\n',
        )
        _add_valid_assurance(d / "01_INTAKE.md", d / "07_CLOSEOUT.md")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, out
        assert "gate assurance status" in out


def test_assurance_v1_is_fail_closed_without_authorization_record():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_assurance-no-authorization"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md",
            'knowledge_governance_version: "1.0"\n'
            'assurance_governance_version: "1.0"\n',
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "NONE"\n'
            'assurance_governance_version: "1.0"\n'
            'kind: "CLOSEOUT"\n',
        )
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ```yaml
                    ASSURANCE_STATUS:
                      schema_version: "1.0"
                      subject: "test delivery"
                      gate_results: []
                    ```
                    """
                )
            )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "implementation_authorization must be a mapping" in out


def test_not_authorized_does_not_allow_executed_closeout():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_assurance-inferred"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\nknowledge_harvest: "NONE"\n',
        )
        _add_valid_assurance(
            d / "01_INTAKE.md",
            d / "07_CLOSEOUT.md",
            authorization_status="NOT_AUTHORIZED",
        )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "requires explicit AUTHORIZED status" in out


def test_certification_fail_requires_handoff_and_preserves_design_result():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_certification-fail"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md",
            'knowledge_governance_version: "1.0"\n'
            'assurance_governance_version: "1.0"\n',
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "NONE"\n'
            'assurance_governance_version: "1.0"\n'
            'kind: "CLOSEOUT"\n',
        )
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ```yaml
                    ASSURANCE_STATUS:
                      schema_version: "1.0"
                      subject: "test delivery"
                      gate_results:
                        - gate_id: "design-pre"
                          gate_family: "DESIGN"
                          checkpoint: "PRE_IMPLEMENTATION"
                          subject: "observable behavior"
                          verdict: "PASS"
                          evidence: ["fixture"]
                          reasons: ["design closed"]
                        - gate_id: "cert-post"
                          gate_family: "CERTIFICATION"
                          checkpoint: "POST_IMPLEMENTATION"
                          subject: "documentary evidence"
                          verdict: "FAIL"
                          evidence: ["fixture"]
                          reasons: ["proof missing"]
                      implementation_authorization:
                        status: "AUTHORIZED"
                        required_gate_ids: ["design-pre"]
                        reasons: ["explicit pre-implementation decision"]
                    ```
                    """
                )
            )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "Certification FAIL or NOT_ASSESSED requires kind HANDOFF" in out


def test_design_fail_requires_handoff():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_design-fail"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md",
            'knowledge_governance_version: "1.0"\n'
            'assurance_governance_version: "1.0"\n',
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "NONE"\n'
            'assurance_governance_version: "1.0"\n'
            'kind: "CLOSEOUT"\n',
        )
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ```yaml
                    ASSURANCE_STATUS:
                      schema_version: "1.0"
                      subject: "test delivery"
                      gate_results:
                        - gate_id: "design-pre"
                          gate_family: "DESIGN"
                          checkpoint: "PRE_IMPLEMENTATION"
                          subject: "initial behavior"
                          verdict: "PASS"
                          evidence: ["fixture"]
                          reasons: ["initial design closed"]
                        - gate_id: "design-post"
                          gate_family: "DESIGN"
                          checkpoint: "POST_IMPLEMENTATION"
                          subject: "reopened behavior"
                          verdict: "FAIL"
                          evidence: ["fixture"]
                          reasons: ["substantive contradiction"]
                      implementation_authorization:
                        status: "AUTHORIZED"
                        required_gate_ids: ["design-pre"]
                        reasons: ["explicit pre-implementation decision"]
                    ```
                    """
                )
            )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "Design FAIL or NOT_ASSESSED requires kind HANDOFF" in out


def test_authorized_rejects_blank_reason_and_evidence():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_blank-assurance"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md",
            'knowledge_governance_version: "1.0"\n'
            'assurance_governance_version: "1.0"\n',
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "NONE"\n'
            'assurance_governance_version: "1.0"\n'
            'kind: "CLOSEOUT"\n',
        )
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ```yaml
                    ASSURANCE_STATUS:
                      schema_version: "1.0"
                      subject: "test delivery"
                      gate_results:
                        - gate_id: "design-pre"
                          gate_family: "DESIGN"
                          checkpoint: "PRE_IMPLEMENTATION"
                          subject: "observable behavior"
                          verdict: "PASS"
                          evidence: [""]
                          reasons: ["design closed"]
                      implementation_authorization:
                        status: "AUTHORIZED"
                        required_gate_ids: ["design-pre"]
                        reasons: [""]
                    ```
                    """
                )
            )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "evidence must contain non-empty strings" in out
        assert "reasons must contain non-empty strings" in out


def test_certification_not_assessed_requires_handoff():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_cert-not-assessed"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md",
            'knowledge_governance_version: "1.0"\n'
            'assurance_governance_version: "1.0"\n',
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "NONE"\n'
            'assurance_governance_version: "1.0"\n'
            'kind: "CLOSEOUT"\n',
        )
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ```yaml
                    ASSURANCE_STATUS:
                      schema_version: "1.0"
                      subject: "test delivery"
                      gate_results:
                        - gate_id: "design-pre"
                          gate_family: "DESIGN"
                          checkpoint: "PRE_IMPLEMENTATION"
                          subject: "observable behavior"
                          verdict: "PASS"
                          evidence: ["fixture"]
                          reasons: ["design closed"]
                        - gate_id: "cert-post"
                          gate_family: "CERTIFICATION"
                          checkpoint: "POST_IMPLEMENTATION"
                          subject: "documentary proof"
                          verdict: "NOT_ASSESSED"
                          evidence: ["fixture"]
                          reasons: ["review not performed"]
                      implementation_authorization:
                        status: "AUTHORIZED"
                        required_gate_ids: ["design-pre"]
                        reasons: ["explicit decision"]
                    ```
                    """
                )
            )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "Certification FAIL or NOT_ASSESSED requires kind HANDOFF" in out


def _add_not_applicable_assurance(closeout_path: Path, *, declared: bool) -> None:
    body_lines = [
        "```yaml",
        "ASSURANCE_STATUS:",
        '  schema_version: "1.0"',
        '  subject: "test delivery"',
        "  gate_results:",
        '    - gate_id: "design-pre"',
        '      gate_family: "DESIGN"',
        '      checkpoint: "PRE_IMPLEMENTATION"',
        '      subject: "observable behavior"',
        '      verdict: "PASS"',
        '      evidence: ["fixture"]',
        '      reasons: ["design closed"]',
        '    - gate_id: "cert-na"',
        '      gate_family: "CERTIFICATION"',
        '      checkpoint: "POST_IMPLEMENTATION"',
        '      subject: "non-applicable proof"',
        '      verdict: "NOT_APPLICABLE"',
        '      evidence: ["fixture"]',
        '      reasons: ["profile excludes this proof"]',
    ]
    if declared:
        body_lines.extend(
            [
                "      applicability:",
                '        profile_id: "docs-only-profile-v1"',
                '        status: "NOT_APPLICABLE"',
                '        evidence: ["profile declaration fixture"]',
            ]
        )
    body_lines.extend(
        [
            "  implementation_authorization:",
            '    status: "AUTHORIZED"',
            '    required_gate_ids: ["design-pre"]',
            '    reasons: ["explicit decision"]',
            "```",
        ]
    )
    with closeout_path.open("a") as handle:
        handle.write("\n" + "\n".join(body_lines) + "\n")


def test_not_applicable_requires_profile_declaration():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000-not-applicable-missing-profile"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md",
            'knowledge_governance_version: "1.0"\n'
            'assurance_governance_version: "1.0"\n',
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "NONE"\n'
            'assurance_governance_version: "1.0"\n'
            'kind: "CLOSEOUT"\n',
        )
        _add_not_applicable_assurance(d / "07_CLOSEOUT.md", declared=False)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "applicability is required for NOT_APPLICABLE" in out


def test_not_applicable_accepts_declared_profile():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000-not-applicable-declared"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md",
            'knowledge_governance_version: "1.0"\n'
            'assurance_governance_version: "1.0"\n',
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\n'
            'knowledge_harvest: "NONE"\n'
            'assurance_governance_version: "1.0"\n'
            'kind: "CLOSEOUT"\n',
        )
        _add_not_applicable_assurance(d / "07_CLOSEOUT.md", declared=True)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, out


def test_governance_v1_rejects_version_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_knowledge-mismatch"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "2.0"\nknowledge_harvest: "NONE"\n',
        )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "must match 01_INTAKE.md" in out


def test_governance_rejects_unsupported_version():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2099-01-01_1000_knowledge-unsupported"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "2.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "2.0"\nknowledge_harvest: "NONE"\n',
        )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "unsupported '2.0'" in out


def test_governance_v1_rejects_missing_harvest():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_knowledge-missing"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md", 'knowledge_governance_version: "1.0"\n'
        )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "knowledge_harvest" in out


def test_governance_v1_rejects_invalid_harvest():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_knowledge-invalid"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        _add_frontmatter_fields(
            d / "01_INTAKE.md", 'knowledge_governance_version: "1.0"\n'
        )
        _add_frontmatter_fields(
            d / "07_CLOSEOUT.md",
            'knowledge_governance_version: "1.0"\nknowledge_harvest: "PROMOTED"\n',
        )
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, out
        assert "PROMOTED" in out


def test_cloture_complete():
    """CLOTURE voie: only 07_CLOSEOUT required, no 01_INTAKE."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_cloture"
        d.mkdir()
        rid = "2026-01-01_1000_cloture"
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "CLOTURE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out


def test_rapide_zero():
    """RAPIDE-ZERO voie: closeout with voie=RAPIDE-ZERO → PASS (no required phases)."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_zero"
        d.mkdir()
        rid = "2026-01-01_1000_zero"
        # RAPIDE-ZERO only needs a closeout with the voie set
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "RAPIDE-ZERO")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out
        assert "RAPIDE-ZERO" in out


def test_rapide_minimal():
    """RAPIDE-MINIMAL voie: 05_PATCH_SUMMARY only → PASS."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_minimal"
        d.mkdir()
        rid = "2026-01-01_1000_minimal"
        patch = textwrap.dedent(f"""\
            ---
            run_id: "{rid}"
            phase: "05_PATCH_SUMMARY"
            voie: "RAPIDE-MINIMAL"
            status: "DONE"
            agent: "claude-code"
            started_at: "2026-05-23T10:00:00Z"
            ended_at: "2026-05-23T10:30:00Z"
            artifacts_produced: []
            ---

            # Patch Summary
        """)
        (d / "05_PATCH_SUMMARY.md").write_text(patch)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out
        assert "RAPIDE-MINIMAL" in out


# ---------------------------------------------------------------------------
# Negative tests
# ---------------------------------------------------------------------------


def test_missing_closeout():
    """RAPIDE run missing 07_CLOSEOUT → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_no-closeout"
        d.mkdir()
        rid = "2026-01-01_1000_no-closeout"
        _make_artifact(d / "01_INTAKE.md", rid, "01_INTAKE", "RAPIDE")
        _make_artifact(d / "05_EXECUTION.md", rid, "05_EXECUTION", "RAPIDE")
        # 07_CLOSEOUT.md intentionally absent
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out, f"Expected FAIL in output\n{out}"
        assert "07_CLOSEOUT" in out, f"Expected '07_CLOSEOUT' mentioned\n{out}"


def test_missing_required_phase():
    """STRUCTUREE run missing 04_PLAN → FAIL with 04_PLAN in error."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_no-plan"
        d.mkdir()
        rid = "2026-01-01_1000_no-plan"
        # 04_PLAN intentionally absent
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out, f"Expected FAIL\n{out}"
        assert "04_PLAN" in out, f"Expected '04_PLAN' in error output\n{out}"


def test_missing_intake_non_cloture():
    """RAPIDE run without 01_INTAKE → FAIL even if 07_CLOSEOUT exists."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_no-intake"
        d.mkdir()
        rid = "2026-01-01_1000_no-intake"
        # 07_CLOSEOUT has voie=RAPIDE — not CLOTURE, so 01_INTAKE is required
        _make_artifact(d / "05_EXECUTION.md", rid, "05_EXECUTION", "RAPIDE")
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "01_INTAKE" in out, f"Expected '01_INTAKE' in error\n{out}"


def test_missing_frontmatter_field():
    """07_CLOSEOUT.md missing required field 'status' → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_bad-fm"
        d.mkdir()
        rid = "2026-01-01_1000_bad-fm"
        _make_artifact(d / "01_INTAKE.md", rid, "01_INTAKE", "RAPIDE")
        _make_artifact(d / "05_EXECUTION.md", rid, "05_EXECUTION", "RAPIDE")
        # closeout without 'status'
        bad = textwrap.dedent(f"""\
            ---
            run_id: "{rid}"
            phase: "07_CLOSEOUT"
            voie: "RAPIDE"
            agent: "claude-code"
            started_at: "2026-05-23T10:00:00Z"
            ended_at: "2026-05-23T10:30:00Z"
            artifacts_produced: []
            ---

            # Closeout
        """)
        (d / "07_CLOSEOUT.md").write_text(bad)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "status" in out, f"Expected 'status' mentioned in error\n{out}"


def test_placeholder_not_replaced():
    """07_CLOSEOUT.md with <placeholder> values → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_placeholder"
        d.mkdir()
        rid = "2026-01-01_1000_placeholder"
        placeholder = textwrap.dedent("""\
            ---
            run_id: "<run_id>"
            phase: "07_CLOSEOUT"
            voie: "CLOTURE"
            status: "READY"
            agent: "claude-code"
            started_at: "<ISO8601>"
            ended_at: "<ISO8601>"
            artifacts_produced: []
            ---

            # Closeout
        """)
        (d / "07_CLOSEOUT.md").write_text(placeholder)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "placeholder" in out, f"Expected 'placeholder' in error\n{out}"


def test_run_not_found():
    """Non-existent run_id → FAIL immediately."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, _ = _run("nonexistent-run-id", Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out


def test_invalid_voie():
    """01_INTAKE with unknown voie value → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_bad-voie"
        d.mkdir()
        rid = "2026-01-01_1000_bad-voie"
        bad_voie = textwrap.dedent(f"""\
            ---
            run_id: "{rid}"
            phase: "01_INTAKE"
            voie: "INVENTED"
            status: "READY"
            agent: "claude-code"
            started_at: "2026-05-23T10:00:00Z"
            ended_at: "2026-05-23T10:30:00Z"
            artifacts_produced: []
            ---

            # Intake
        """)
        (d / "01_INTAKE.md").write_text(bad_voie)
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "INVENTED" in out, f"Expected bad voie value in error\n{out}"


# ---------------------------------------------------------------------------
# Dogfood: PR #3 run must pass its own check
# ---------------------------------------------------------------------------


def test_pr3_run_passes():
    """The PR #3 run artifact set must satisfy the closure invariant."""
    rc, out, _ = _run(
        "2026-05-23_1800_artifact-verify-lot-c",
        REPO_ROOT / "docs" / "runs",
    )
    assert rc == 0, f"PR #3 run should pass the loop-closure check\n{out}"
    assert "PASS" in out


# ---------------------------------------------------------------------------
# --strict mode (VBB COMPLETE gate semantics)
# ---------------------------------------------------------------------------


def test_strict_fail_returns_exit_2():
    """--strict on a FAIL run_id → exit 2 (GATE_BLOCKED) + blocking msg on stderr."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_strict-fail"
        d.mkdir()
        rid = "2026-01-01_1000_strict-fail"
        # Build a STRUCTUREE run missing 04_PLAN → FAIL
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        rc, out, err = _run(rid, Path(tmp), extra_args=["--strict"])
        assert rc == 2, f"Expected exit 2 (GATE_BLOCKED), got {rc}\nstderr:\n{err}"
        assert "GATE FAILED" in err, f"Expected GATE FAILED on stderr\nstderr:\n{err}"
        assert "FINAL_STATUS=COMPLETE is not allowed" in err, (
            f"Expected explicit COMPLETE-forbidden message\nstderr:\n{err}"
        )
        assert rid in err, f"Expected run_id in blocking message\nstderr:\n{err}"


def test_strict_no_run_id_returns_exit_64():
    """--strict without any run_id (no positional, no env) → exit 64 (USAGE_ERROR)."""
    # Use a fresh empty runs-dir so auto-detect cannot find a run.
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "empty_runs"
        empty.mkdir()
        cmd = [sys.executable, str(TOOL), "--strict", "--runs-dir", str(empty)]
        # Ensure VBB_RUN_ID is unset for this test
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=_controlled_env(),
        )
        assert result.returncode == 64, (
            f"Expected exit 64 (USAGE_ERROR), got {result.returncode}\nstderr:\n{result.stderr}"
        )
        assert "GATE FAILED" in result.stderr
        assert "--run_id required" in result.stderr, (
            f"Expected explicit 'required' message\nstderr:\n{result.stderr}"
        )


def test_strict_pass_returns_exit_0():
    """--strict on a PASS run_id → exit 0 (no blocking message)."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_strict-pass"
        d.mkdir()
        rid = "2026-01-01_1000_strict-pass"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        rc, out, err = _run(rid, Path(tmp), extra_args=["--strict"])
        assert rc == 0, (
            f"Expected exit 0 on PASS, got {rc}\nstdout:\n{out}\nstderr:\n{err}"
        )
        assert "PASS" in out
        # On PASS, the strict gate does NOT emit a blocking message
        assert "GATE FAILED" not in err, (
            f"Strict PASS should be silent on stderr\nstderr:\n{err}"
        )


def test_strict_rejects_unrequested_long_run_extension():
    """The recorded 840/180/no-extension contradiction must block closure."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_long-run-invalid"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ## LONG_RUN_SUMMARY

                    ```yaml
                    FINAL_STATUS:
                      elapsed_seconds: 840
                      budget_initial: 180
                      progress_emitted: true
                      progress_count: 1
                      extension_requested: false
                      timeout_closeout_emitted: false
                      verdict: COMPLETE
                    ```
                    """
                )
            )
        rc, out, err = _run(rid, Path(tmp), extra_args=["--strict"])
        assert rc == 2, f"Expected strict block, got {rc}\n{out}\n{err}"
        assert "extension_requested is false" in out


def test_strict_accepts_traced_long_run_extension():
    """A bounded extension with progress and a durable request remains valid."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_long-run-valid"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ```yaml
                    EXTENSION_REQUEST:
                      reason: "bounded verification"
                      additional_time_seconds: 300
                      scope_unchanged: true
                      risk_changed: false
                    ```

                    ## LONG_RUN_SUMMARY

                    ```yaml
                    FINAL_STATUS:
                      elapsed_seconds: 400
                      budget_initial: 180
                      progress_emitted: true
                      progress_count: 1
                      extension_requested: true
                      timeout_closeout_emitted: false
                      verdict: EXTENDED
                    ```
                    """
                )
            )
        rc, out, err = _run(rid, Path(tmp), extra_args=["--strict"])
        assert rc == 0, f"Expected strict pass, got {rc}\n{out}\n{err}"


def test_strict_rejects_elapsed_beyond_granted_extensions():
    """An extension flag alone cannot grant more than the durable requests."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_long-run-undergranted"
        d.mkdir()
        rid = d.name
        for phase in ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        with (d / "07_CLOSEOUT.md").open("a") as handle:
            handle.write(
                textwrap.dedent(
                    """
                    ```yaml
                    EXTENSION_REQUEST:
                      additional_time_seconds: 300
                    ```
                    ```yaml
                    FINAL_STATUS:
                      elapsed_seconds: 700
                      budget_initial: 180
                      progress_emitted: true
                      progress_count: 1
                      extension_requested: true
                      timeout_closeout_emitted: false
                      verdict: EXTENDED
                    ```
                    """
                )
            )
        rc, out, _ = _run(rid, Path(tmp), extra_args=["--strict"])
        assert rc == 2
        assert "exceeds granted budget 480s" in out


def test_default_mode_retrocompatible_exit_codes():
    """Default mode (no --strict) preserves original exit codes: 1 for FAIL, 0 for PASS."""
    with tempfile.TemporaryDirectory() as tmp:
        # FAIL case: STRUCTUREE missing 04_PLAN
        d_fail = Path(tmp) / "2026-01-01_1000_default-fail"
        d_fail.mkdir()
        rid_fail = "2026-01-01_1000_default-fail"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d_fail / f"{phase}.md", rid_fail, phase, "STRUCTUREE")
        rc_fail, out_fail, _ = _run(rid_fail, Path(tmp))  # no extra_args
        assert rc_fail == 1, (
            f"Default mode FAIL should still be exit 1, got {rc_fail}\n{out_fail}"
        )

        # PASS case: complete RAPIDE
        d_pass = Path(tmp) / "2026-01-01_1000_default-pass"
        d_pass.mkdir()
        rid_pass = "2026-01-01_1000_default-pass"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d_pass / f"{phase}.md", rid_pass, phase, "RAPIDE")
        rc_pass, out_pass, _ = _run(rid_pass, Path(tmp))
        assert rc_pass == 0, (
            f"Default mode PASS should still be exit 0, got {rc_pass}\n{out_pass}"
        )


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
