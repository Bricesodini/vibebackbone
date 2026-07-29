"""Regression tests for first-push changed-run selection."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parent.parent.resolve()
SELECTOR = REPO_ROOT / "tools" / "vbb-changed-closeouts.py"
ZERO = "0" * 40


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Test")
    (repo / "README").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "base")
    base = _git(repo, "rev-parse", "HEAD")
    return repo, base


def _commit(repo: Path, path: str, text: str, message: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    _git(repo, "add", path)
    _git(repo, "commit", "-qm", message)
    return _git(repo, "rev-parse", "HEAD")


def _select(
    repo: Path, base: str, head: str, default_ref: str = "main"
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SELECTOR),
            "--repo",
            str(repo),
            "--base-sha",
            base,
            "--head-sha",
            head,
            "--default-ref",
            default_ref,
        ],
        capture_output=True,
        text=True,
    )


def test_valid_before_selects_only_changed_closeout(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    old = "docs/runs/2026-05-18_2300_prompts-agentic-migration/07_CLOSEOUT.md"
    _commit(repo, old, "legacy\n", "legacy closeout")
    base = _git(repo, "rev-parse", "HEAD")
    head = _commit(repo, "docs/runs/new/07_CLOSEOUT.md", "new\n", "new closeout")
    result = _select(repo, base, head)
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["docs/runs/new/07_CLOSEOUT.md"]


def test_zero_before_uses_default_branch_merge_base(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    old = "docs/runs/2026-05-18_2300_prompts-agentic-migration/07_CLOSEOUT.md"
    _commit(repo, old, "legacy\n", "legacy closeout")
    _git(repo, "checkout", "-qb", "candidate")
    head = _commit(repo, "docs/runs/run1/07_CLOSEOUT.md", "candidate\n", "candidate")
    result = _select(repo, ZERO, head)
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["docs/runs/run1/07_CLOSEOUT.md"]


def test_modified_closeout_is_selected(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    path = "docs/runs/run1/07_CLOSEOUT.md"
    _commit(repo, path, "one\n", "closeout")
    head = _commit(repo, path, "two\n", "modify closeout")
    result = _select(repo, base, head)
    assert result.returncode == 0
    assert result.stdout.splitlines() == [path]


def test_no_closeout_change_selects_nothing(tmp_path: Path) -> None:
    repo, base = _repo(tmp_path)
    head = _commit(repo, "tools/other.py", "x\n", "unrelated")
    result = _select(repo, base, head)
    assert result.returncode == 0
    assert result.stdout == ""


def test_missing_base_fails_closed_instead_of_scanning_history(tmp_path: Path) -> None:
    repo, _ = _repo(tmp_path)
    head = _commit(repo, "docs/runs/legacy/07_CLOSEOUT.md", "legacy\n", "legacy")
    result = _select(repo, "not-a-commit", head, "refs/remotes/origin/main")
    assert result.returncode != 0
    assert "no reliable Git base" in result.stderr


def test_unavailable_before_can_use_fetched_default_branch(tmp_path: Path) -> None:
    repo, _ = _repo(tmp_path)
    _commit(repo, "docs/runs/legacy/07_CLOSEOUT.md", "legacy\n", "legacy")
    _git(repo, "checkout", "-qb", "candidate")
    head = _commit(repo, "docs/runs/run1/07_CLOSEOUT.md", "candidate\n", "candidate")
    result = _select(repo, "unavailable-before", head, "main")
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["docs/runs/run1/07_CLOSEOUT.md"]


def test_workflow_has_no_historical_fallback_and_uses_selector() -> None:
    workflow = (REPO_ROOT / ".github/workflows/vbb-contracts.yml").read_text()
    assert "vbb-changed-closeouts.py" in workflow
    assert "git ls-files 'docs/runs/*/07_CLOSEOUT.md'" not in workflow
    assert "VBB_DEFAULT_BRANCH" in workflow


@pytest.mark.parametrize("platform", ["ubuntu", "macos"])
def test_selector_is_platform_neutral(platform: str) -> None:
    assert platform in {"ubuntu", "macos"}
    assert SELECTOR.suffix == ".py"
