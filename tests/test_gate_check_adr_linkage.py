"""Non-regression for ADR-0027 decision 3 — strict ADR linkage in the gate.

Observed defect (2026-07-13): an intake explicitly linked to ADR-0027
(PROPOSED) also cited ADR-0026 (ACCEPTED) as a consumed artifact; the gate
declared the ADR requirement satisfied via the unrelated accepted ADR.

Rule under test: when an ADR is explicitly referenced, the gate verifies
THAT one — never falling back to a globally accepted ADR.
"""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-gate-check.py"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("vbb_gate_check_adr_test", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def gate_env(tmp_path: Path, monkeypatch):
    """Gate module wired to a temp ADR dir + a run dir factory."""
    gate = _load_gate_module()
    adr_dir = tmp_path / "adr"
    adr_dir.mkdir()
    gate.ADR_DIR = adr_dir

    def write_adr(name: str, status: str) -> Path:
        p = adr_dir / name
        p.write_text(
            f"# ADR — {name}\n\n**Status**: {status}\n**Date**: 2026-07-13\n",
            encoding="utf-8",
        )
        return p

    def make_run(intake_text: str) -> Path:
        run_dir = tmp_path / "run"
        run_dir.mkdir(exist_ok=True)
        (run_dir / "01_INTAKE.md").write_text(intake_text, encoding="utf-8")
        return run_dir

    return gate, write_adr, make_run


def test_linked_proposed_adr_blocks_despite_accepted_bystander(gate_env) -> None:
    """The exact 2026-07-13 false-PASS scenario, now expected BLOCKED."""
    gate, write_adr, make_run = gate_env
    write_adr("0026-global-audit.md", "ACCEPTED")
    linked = write_adr("0027-shared-run-resolution.md", "PROPOSED")
    run_dir = make_run(
        "# 01_INTAKE\n"
        "artifacts_consumed:\n"
        '  - "docs/adr/0026-global-audit.md"\n'
        "## Dépendances détectées\n"
        "- ADR : `docs/adr/0027-shared-run-resolution.md` (PROPOSED)\n"
    )
    ok, path, blocker = gate.check_adr(run_dir)
    assert ok is False
    assert path == linked
    assert blocker == "ADR_NOT_ACCEPTED"


def test_linked_accepted_adr_passes_with_correct_path(gate_env) -> None:
    gate, write_adr, make_run = gate_env
    write_adr("0026-global-audit.md", "ACCEPTED")
    linked = write_adr("0027-shared-run-resolution.md", "ACCEPTED")
    run_dir = make_run(
        "# 01_INTAKE\n"
        '  - "docs/adr/0026-global-audit.md"\n'
        "Liée à ADR: docs/adr/0027-shared-run-resolution.md\n"
    )
    ok, path, blocker = gate.check_adr(run_dir)
    assert ok is True
    assert path == linked
    assert blocker == ""


def test_explicit_ref_never_falls_back_to_global(gate_env) -> None:
    """Single explicit (unlabeled) reference to a PROPOSED ADR: no keyword
    fallback may rescue the gate, even with an accepted ADR on disk whose
    slug matches the intake keywords."""
    gate, write_adr, make_run = gate_env
    write_adr("0001-storage-database-policy.md", "ACCEPTED")
    proposed = write_adr("0042-new-storage-contract.md", "PROPOSED")
    run_dir = make_run(
        "# 01_INTAKE\n"
        "Changer le storage et le contract de la database.\n"
        "Voir docs/adr/0042-new-storage-contract.md\n"
    )
    ok, path, blocker = gate.check_adr(run_dir)
    assert ok is False
    assert path == proposed
    assert blocker == "ADR_NOT_ACCEPTED"


def test_missing_referenced_adr_file_blocks(gate_env) -> None:
    gate, _write_adr, make_run = gate_env
    run_dir = make_run("# 01_INTAKE\nLiée à ADR: docs/adr/0099-ghost-decision.md\n")
    ok, path, blocker = gate.check_adr(run_dir)
    assert ok is False
    assert path is None
    assert blocker == "ADR_REF_NOT_FOUND"


def test_keyword_fallback_preserved_without_any_explicit_ref(gate_env) -> None:
    """Non-regression of the historical behavior: a run citing no ADR at all
    may still satisfy the gate via an accepted ADR matching its keywords."""
    gate, write_adr, make_run = gate_env
    accepted = write_adr("0001-storage-policy.md", "ACCEPTED")
    run_dir = make_run("# 01_INTAKE\nMigrer le storage applicatif.\n")
    ok, path, blocker = gate.check_adr(run_dir)
    assert ok is True
    assert path == accepted
    assert blocker == ""


def test_project_local_adr_resolves_from_run_git_root(tmp_path: Path) -> None:
    gate = _load_gate_module()
    project = tmp_path / "project"
    run_dir = project / "docs" / "runs" / "run"
    adr_dir = project / "docs" / "adr"
    run_dir.mkdir(parents=True)
    adr_dir.mkdir()
    (project / ".git").mkdir()
    adr = adr_dir / "0026-local.md"
    adr.write_text("**Status**: ACCEPTED\n", encoding="utf-8")
    (run_dir / "01_INTAKE.md").write_text(
        "API contract\nLiée à ADR: docs/adr/0026-local.md\n", encoding="utf-8"
    )
    ok, path, blocker = gate.check_adr(run_dir)
    assert (ok, path, blocker) == (True, adr, "")


def test_core_namespace_is_explicit_and_project_namespace_wins_duplicates(tmp_path: Path) -> None:
    gate = _load_gate_module()
    project = tmp_path / "project"
    core = tmp_path / "core"
    run_dir = project / "docs" / "runs" / "run"
    for root in (project, core):
        (root / "docs" / "adr").mkdir(parents=True)
    (project / ".git").mkdir()
    project_adr = project / "docs/adr/0026-shared.md"
    core_adr = core / "docs/adr/0026-shared.md"
    project_adr.write_text("**Status**: ACCEPTED\n", encoding="utf-8")
    core_adr.write_text("**Status**: ACCEPTED\n", encoding="utf-8")
    run_dir.mkdir(parents=True)
    (run_dir / "01_INTAKE.md").write_text(
        "Liée à ADR: project:docs/adr/0026-shared.md\n", encoding="utf-8"
    )
    assert gate.check_adr(run_dir, core_root=core)[0:2] == (True, project_adr)
    (run_dir / "01_INTAKE.md").write_text(
        "Liée à ADR: vbb:docs/adr/0026-shared.md\n", encoding="utf-8"
    )
    assert gate.check_adr(run_dir, core_root=core)[0:2] == (True, core_adr)


def test_core_missing_and_absolute_authorized_reference(tmp_path: Path) -> None:
    gate = _load_gate_module()
    project = tmp_path / "project"
    core = tmp_path / "core"
    run_dir = project / "docs/runs/run"
    (project / "docs/adr").mkdir(parents=True)
    (core / "docs/adr").mkdir(parents=True)
    (project / ".git").mkdir()
    run_dir.mkdir(parents=True)
    (run_dir / "01_INTAKE.md").write_text(
        "Liée à ADR: vbb:docs/adr/0099-missing.md\n", encoding="utf-8"
    )
    assert gate.check_adr(run_dir, core_root=core)[2] == "ADR_REF_NOT_FOUND"
    absolute = project / "docs/adr/0026-absolute.md"
    absolute.write_text("**Status**: ACCEPTED\n", encoding="utf-8")
    (run_dir / "01_INTAKE.md").write_text(
        f"Liée à ADR: {absolute}\n", encoding="utf-8"
    )
    ok, path, blocker = gate.check_adr(run_dir, core_root=core)
    assert (ok, path, blocker) == (True, absolute, "")


def test_unqualified_duplicate_adr_fails_closed(tmp_path: Path) -> None:
    gate = _load_gate_module()
    project = tmp_path / "project"
    core = tmp_path / "core"
    run_dir = project / "docs/runs/run"
    for root in (project, core):
        (root / "docs/adr").mkdir(parents=True)
        (root / "docs/adr/0026-shared.md").write_text(
            "**Status**: ACCEPTED\n", encoding="utf-8"
        )
    (project / ".git").mkdir()
    run_dir.mkdir(parents=True)
    (run_dir / "01_INTAKE.md").write_text(
        "Liée à ADR: docs/adr/0026-shared.md\n", encoding="utf-8"
    )
    ok, path, blocker = gate.check_adr(run_dir, core_root=core)
    assert (ok, path, blocker) == (False, None, "AMBIGUOUS_ADR_REF")


def test_project_root_unavailable_fails_closed(tmp_path: Path) -> None:
    gate = _load_gate_module()
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "01_INTAKE.md").write_text(
        "Liée à ADR: docs/adr/0026-ghost.md\n", encoding="utf-8"
    )
    ok, path, blocker = gate.check_adr(run_dir, project_root=tmp_path / "missing")
    assert (ok, path, blocker) == (False, None, "PROJECT_ROOT_UNAVAILABLE")


def test_traversal_and_symlink_escape_fail_closed(tmp_path: Path) -> None:
    gate = _load_gate_module()
    project = tmp_path / "project"
    outside = tmp_path / "outside"
    run_dir = project / "docs/runs/run"
    (project / "docs/adr").mkdir(parents=True)
    run_dir.mkdir(parents=True)
    outside.mkdir()
    (outside / "0026-escape.md").write_text("**Status**: ACCEPTED\n", encoding="utf-8")
    (project / "docs/adr/0026-link.md").symlink_to(outside / "0026-escape.md")
    (run_dir / "01_INTAKE.md").write_text(
        "Liée à ADR: docs/adr/../adr/0026-escape.md\n", encoding="utf-8"
    )
    assert gate.check_adr(run_dir, project_root=project)[0] is False


def test_malformed_scoped_traversal_cannot_fall_back(tmp_path: Path) -> None:
    gate = _load_gate_module()
    project = tmp_path / "project"
    (project / "docs/adr").mkdir(parents=True)
    (project / ".git").mkdir()
    (project / "docs/adr/0001-storage-policy.md").write_text(
        "**Status**: ACCEPTED\n", encoding="utf-8"
    )
    run_dir = project / "docs/runs/run"
    run_dir.mkdir(parents=True)
    (run_dir / "01_INTAKE.md").write_text(
        "storage contract\nproject:../docs/adr/0001-storage-policy.md\n",
        encoding="utf-8",
    )
    ok, path, blocker = gate.check_adr(run_dir)
    assert (ok, path, blocker) == (False, None, "ADR_PATH_OUTSIDE_AUTHORIZED_ROOT")
