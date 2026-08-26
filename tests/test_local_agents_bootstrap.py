"""Regression coverage for the bounded repository-local AGENTS.md bootstrap."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "tools" / "vbb-local-agents.py"


def _git(path: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(path), *args], check=True, capture_output=True)


def _init_repo(path: Path) -> None:
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "tests@example.invalid")
    _git(path, "config", "user.name", "VBB tests")


def _tracked_contract(path: Path, content: str = "# local operations\n") -> Path:
    contract = path / "AGENTS.md"
    contract.write_text(content, encoding="utf-8")
    _git(path, "add", "AGENTS.md")
    _git(path, "commit", "-qm", "add contract")
    return contract


def _discover(path: Path) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(TOOL), "--cwd", str(path)],
        capture_output=True,
        text=True,
    )
    return result.returncode, json.loads(result.stdout)


def test_no_contract_preserves_historical_bootstrap():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _init_repo(repo)
        code, result = _discover(repo)
        assert code == 0
        assert result["local_agent_contract"] == "NONE"
        assert result["local_agent_contract_status"] == "NONE"


def test_tracked_modified_and_untracked_contracts_are_visible():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _init_repo(repo)
        contract = _tracked_contract(repo)
        code, result = _discover(repo)
        assert code == 0
        assert result["local_agent_contract"] == str(contract.resolve())
        assert result["agents_md_git_state"] == "TRACKED"

        contract.write_text("# changed operations\n", encoding="utf-8")
        code, result = _discover(repo)
        assert code == 0
        assert result["agents_md_git_state"] == "MODIFIED"

        _git(repo, "checkout", "--", "AGENTS.md")
        _git(repo, "rm", "--cached", "AGENTS.md")
        code, result = _discover(repo)
        assert code == 0
        assert result["agents_md_git_state"] == "UNTRACKED"


def test_nested_repository_uses_its_contract_and_never_walks_to_parent():
    with tempfile.TemporaryDirectory() as tmp:
        parent = Path(tmp)
        _init_repo(parent)
        _tracked_contract(parent, "# parent contract\n")
        service = parent / "service"
        service.mkdir()
        _init_repo(service)
        contract = _tracked_contract(service, "# service contract\n")

        code, result = _discover(service)
        assert code == 0
        assert result["repository_root"] == str(service.resolve())
        assert result["local_agent_contract"] == str(contract.resolve())


def test_launch_subdirectory_falls_back_to_effective_git_root():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _init_repo(repo)
        contract = _tracked_contract(repo)
        child = repo / "src" / "feature"
        child.mkdir(parents=True)
        code, result = _discover(child)
        assert code == 0
        assert result["local_agent_contract"] == str(contract.resolve())


def test_external_symlink_stops_bootstrap():
    with (
        tempfile.TemporaryDirectory() as tmp,
        tempfile.TemporaryDirectory() as outside_tmp,
    ):
        repo = Path(tmp)
        _init_repo(repo)
        outside = Path(outside_tmp) / "AGENTS.md"
        outside.write_text("# outside\n", encoding="utf-8")
        os.symlink(outside, repo / "AGENTS.md")
        code, result = _discover(repo)
        assert code == 1
        assert result["local_agent_contract_status"] == "EXTERNAL_SYMLINK"


def test_local_contract_is_operational_and_entrypoints_load_it_before_session():
    contract = (REPO / "docs" / "LOCAL_AGENT_CONTRACTS.md").read_text(encoding="utf-8")
    session_prompt = (REPO / "prompts" / "t-p-vbb-start-session.md").read_text(
        encoding="utf-8"
    )
    before_building = (REPO / "prompts" / "0-p-vbb-before-building.md").read_text(
        encoding="utf-8"
    )

    assert "not a second\ngovernance layer" in contract
    assert "non-applicable" in contract
    assert session_prompt.index("$PWD/AGENTS.md") < session_prompt.index(
        "docs/SESSION.md"
    )
    assert before_building.index("$PWD/AGENTS.md") < before_building.index(
        "docs/SESSION.md"
    )
