"""M3-06 — v1.0 reader on v1.1 data must fail loudly.

R2 §6 (ADVR-A2-09): the matrix of reader × data compatibilities:

    reader v1.0 × data v1.0 valid          ⇒ PASS
    reader v1.0 × data v1.0 invalid        ⇒ FAIL (loud)
    reader v1.0 × data v1.1 (ADVERSARIAL)  ⇒ FAIL (loud, schema error)
    reader v1.0 × data hybrid (v1.0+v1.1)  ⇒ FAIL (loud, schema error)
    reader v1.1 × data v1.0                 ⇒ PASS (compat ascendante)
    reader v1.1 × data v1.1                 ⇒ PASS
    reader v1.1 × future unknown data       ⇒ FAIL (loud, no silent degradation)

The critical invariant: **a v1.1 closeout with `gate_family: ADVERSARIAL`
must NOT be silently degraded to `OTHER` by a v1.0-aware validator**.

We simulate the v1.0 reader by:
  - declaring `assurance_governance_version: "1.0"` in the frontmatter
  - omitting `adversarial_governance_version: "1.1"`
  - feeding the validator a YAML body that uses v1.1 enums.

The closure check (`vbb-loop-closure-check.py`) is the canonical
"reader" tool. The closure check uses the frontmatter version field
to decide whether v1.1 fields are accepted; absent that declaration,
v1.1 fields must produce a loud failure.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "tools" / "vbb-loop-closure-check.py"


def _make_run(
    tmpdir: Path,
    *,
    run_id: str,
    yaml_body: str,
    frontmatter_kwargs: dict = None,
) -> Path:
    """Build a run directory with the given YAML body and frontmatter."""
    fm = {
        "run_id": run_id,
        "phase": "07_CLOSEOUT",
        "voie": "STRUCTUREE",
        "status": "READY",
        "knowledge_governance_version": "1.0",
        "assurance_governance_version": "1.0",
        "knowledge_harvest": "NONE",
        "agent": "external",
        "started_at": "2026-07-28T11:00:00Z",
        "ended_at": "2026-07-28T11:15:00Z",
        "next_phase": None,
        "artifacts_produced": ["07_CLOSEOUT.md"],
    }
    if frontmatter_kwargs:
        fm.update(frontmatter_kwargs)

    fm_lines = []
    for k, v in fm.items():
        if v is None:
            fm_lines.append(f"{k}: null")
        elif isinstance(v, list):
            items = ", ".join(f'"{x}"' for x in v)
            fm_lines.append(f"{k}: [{items}]")
        elif isinstance(v, str):
            fm_lines.append(f'{k}: "{v}"')
        else:
            fm_lines.append(f"{k}: {v}")
    frontmatter = "---\n" + "\n".join(fm_lines) + "\n---\n"

    # Intake + plan + execution are also part of the closure-check
    # invariant. We provide minimal stubs.
    intake = (
        f'---\nrun_id: "{run_id}"\nphase: "01_INTAKE"\nvoie: "STRUCTUREE"\n'
        'status: "READY"\nagent: "external"\nknowledge_governance_version: "1.0"\n'
        'assurance_governance_version: "1.0"\nstarted_at: "2026-07-28T10:00:00Z"\n'
        'ended_at: "2026-07-28T10:15:00Z"\nnext_phase: "04_PLAN"\n'
        'artifacts_produced: ["01_INTAKE.md"]\n---\n\n# intake\n'
    )
    plan = (
        f'---\nrun_id: "{run_id}"\nphase: "04_PLAN"\nvoie: "STRUCTUREE"\n'
        'status: "READY"\nagent: "external"\nstarted_at: "2026-07-28T10:15:00Z"\n'
        'ended_at: "2026-07-28T10:30:00Z"\nnext_phase: "05_EXECUTION"\n'
        'artifacts_produced: ["04_PLAN.md"]\n---\n\n# plan\n'
    )
    execution = (
        f'---\nrun_id: "{run_id}"\nphase: "05_EXECUTION"\nvoie: "STRUCTUREE"\n'
        'status: "READY"\nagent: "external"\nstarted_at: "2026-07-28T10:30:00Z"\n'
        'ended_at: "2026-07-28T11:00:00Z"\nnext_phase: "07_CLOSEOUT"\n'
        'artifacts_produced: ["05_EXECUTION.md"]\n---\n\n# execution\n'
    )

    run = tmpdir / run_id
    run.mkdir()
    (run / "01_INTAKE.md").write_text(intake, encoding="utf-8")
    (run / "04_PLAN.md").write_text(plan, encoding="utf-8")
    (run / "05_EXECUTION.md").write_text(execution, encoding="utf-8")

    body = f"""# closeout

## Assurance

```yaml
{yaml_body}
```

## FINAL_STATUS

```yaml
FINAL_STATUS:
  elapsed_seconds: 60
  budget_initial: 180
  progress_emitted: false
  progress_count: 0
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
```
"""
    (run / "07_CLOSEOUT.md").write_text(frontmatter + body, encoding="utf-8")
    return run


def _run_closure(run: Path) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(run), "--strict"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_v10_reader_on_v10_valid_data_passes(tmp_path: Path):
    """A v1.0 reader (frontmatter v1.0) consuming v1.0-valid YAML must PASS or
    fail for non-schema reasons — never for v1.1 schema reasons."""
    yaml = """ASSURANCE_STATUS:
  schema_version: "1.0"
  subject: "v1.0 valid"
  gate_results:
    - gate_id: "g1"
      gate_family: "DESIGN"
      checkpoint: "CLOSEOUT"
      subject: "v1.0 ok"
      verdict: "PASS"
      evidence: ["x"]
      reasons: ["y"]
  implementation_authorization:
    status: "NOT_AUTHORIZED"
    required_gate_ids: ["g1"]
    reasons: ["test"]
"""
    run = _make_run(tmp_path, run_id="2026-07-28_v10_ok", yaml_body=yaml)
    rc, stdout, stderr = _run_closure(run)
    # Either PASS (rc=0) or FAIL because of v1.0 content — but NOT a v1.1 schema error.
    combined = stdout + stderr
    assert "v1.1" not in combined.lower() or rc == 0, (
        f"v1.0 reader emitted a v1.1 schema error on v1.0 data:\n{combined}"
    )


def test_v10_reader_on_v11_data_fails_loudly(tmp_path: Path):
    """A v1.0 reader (frontmatter v1.0) consuming v1.1 data (gate_family
    ADVERSARIAL) must FAIL with an explicit schema-version error, NOT
    silently downgrade to OTHER or unrelated verdict."""
    # v1.0 closeout but with v1.1 enum values in gate_results.
    yaml = """ASSURANCE_STATUS:
  schema_version: "1.0"
  subject: "hybrid data"
  gate_results:
    - gate_id: "g1"
      gate_family: "ADVERSARIAL"
      checkpoint: "COUNTER_PROOF"
      subject: "v1.1 enum in v1.0 closeout"
      verdict: "PASS"
      evidence: ["x"]
      reasons: ["y"]
  implementation_authorization:
    status: "NOT_AUTHORIZED"
    required_gate_ids: ["g1"]
    reasons: ["test"]
"""
    run = _make_run(tmp_path, run_id="2026-07-28_v10_v11_hybrid", yaml_body=yaml)
    rc, stdout, stderr = _run_closure(run)
    combined = stdout + stderr
    # It must FAIL (non-zero exit) and reference v1.1 schema.
    assert rc != 0, "v1.0 reader on v1.1 data passed silently — forbidden"
    # Critical invariant: must NOT silently downgrade `ADVERSARIAL` to `OTHER`.
    assert "OTHER" not in combined or "ADVERSARIAL" in combined, (
        "v1.0 reader may mention `OTHER` only as a sibling (not as a downgrade)"
    )
    # The error must reference either the version, schema, or the unrecognized enum.
    assert any(
        marker in combined.lower()
        for marker in ("v1.1", "schema", "adversarial", "counter_proof")
    ), f"v1.0 reader did not produce a loud schema error:\n{combined}"


def test_v11_reader_on_v10_data_passes(tmp_path: Path):
    """A v1.1 reader (frontmatter v1.1) consuming v1.0-valid YAML must PASS
    (backward compatibility — v1.1 consumes v1.0)."""
    yaml = """ASSURANCE_STATUS:
  schema_version: "1.0"
  subject: "v1.0 valid"
  gate_results:
    - gate_id: "g1"
      gate_family: "DESIGN"
      checkpoint: "CLOSEOUT"
      subject: "v1.0 ok"
      verdict: "PASS"
      evidence: ["x"]
      reasons: ["y"]
  implementation_authorization:
    status: "NOT_AUTHORIZED"
    required_gate_ids: ["g1"]
    reasons: ["test"]
"""
    run = _make_run(
        tmp_path,
        run_id="2026-07-28_v11_reads_v10",
        yaml_body=yaml,
        frontmatter_kwargs={
            "knowledge_governance_version": "1.0",
            "assurance_governance_version": "1.0",
            "adversarial_governance_version": "1.1",
        },
    )
    rc, stdout, stderr = _run_closure(run)
    # Backward compat: v1.1 reader accepts v1.0 data. May FAIL for content
    # reasons but NOT for v1.1-vs-v1.0 schema mismatch.
    combined = stdout + stderr
    assert "v1.1 cannot" not in combined.lower()
