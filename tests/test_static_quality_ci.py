"""Regression assertions for the supported static-quality CI gates."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.resolve()


def test_development_manifest_pins_supported_tools() -> None:
    manifest = (REPO_ROOT / "requirements-dev.txt").read_text(encoding="utf-8")

    assert "-r requirements.txt" in manifest
    assert "ruff==0.13.1" in manifest
    assert "mypy==2.1.0" in manifest


def test_remote_ci_installs_and_runs_static_quality_gates() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "vbb-contracts.yml").read_text(
        encoding="utf-8"
    )

    assert "python3 -m pip install -r requirements-dev.txt" in workflow
    assert "python3 -m ruff check tools tests" in workflow
    assert "python3 -m ruff format --check tools tests" in workflow
    assert "python3 -m mypy tools" in workflow
    assert "python3 tools/vbb_runtime_conformance.py self-test" in workflow
    assert "bash tests/test_install_vbb_hooks.sh" in workflow


def test_local_ci_runs_same_static_quality_gates() -> None:
    local_ci = (REPO_ROOT / "scripts" / "vbb-ci-local.sh").read_text(encoding="utf-8")

    assert '"$PYTHON" -m ruff check tools tests' in local_ci
    assert '"$PYTHON" -m ruff format --check tools tests' in local_ci
    assert '"$PYTHON" -m mypy tools' in local_ci
    assert '"$PYTHON" tools/vbb_runtime_conformance.py self-test' in local_ci
    assert "bash tests/test_install_vbb_hooks.sh" in local_ci
    assert "requirements-dev.txt" in local_ci
