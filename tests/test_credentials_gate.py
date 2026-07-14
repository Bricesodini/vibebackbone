from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = REPO_ROOT / "tools" / "vbb-credentials-gate.py"
SPEC = importlib.util.spec_from_file_location("vbb_credentials_gate", TOOL_PATH)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def _git(repo: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_bytes,
        capture_output=True,
        check=True,
    ).stdout


def _init_repo(path: Path) -> None:
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "tests@example.invalid")
    _git(path, "config", "user.name", "VBB Tests")
    _git(path, "commit", "--allow-empty", "-q", "-m", "base")


def _stage_blob(repo: Path, path: str, content: bytes) -> None:
    blob = _git(repo, "hash-object", "-w", "--stdin", input_bytes=content).decode().strip()
    _git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}")


def _run_tool(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL_PATH), "--repo", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.mark.parametrize(
    ("value", "rule"),
    [
        ("AK" + "IA" + "A" * 16, "aws-access-key"),
        ("gh" + "p_" + "B" * 36, "github-token"),
        ("-----BEGIN " + "PRIVATE KEY-----", "private-key-boundary"),
        ('api_key = "' + "Q7mN4pR8sT2vW6xY" + '"', "generic-credential-assignment"),
    ],
)
def test_detects_high_confidence_and_generic_values(value: str, rule: str) -> None:
    assert rule in gate.detect_rules(value)


@pytest.mark.parametrize(
    "value",
    [
        'api_key = "VBB_SYNTHETIC_NOT_A_SECRET"',
        'api_key = "${API_KEY}"',
        'password = "example-placeholder"',
        "ordinary documentation line",
    ],
)
def test_ignores_placeholders_and_ordinary_content(value: str) -> None:
    assert gate.detect_rules(value) == []


def test_staged_mode_blocks_without_printing_the_value(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    value = "Q7mN4pR8sT2vW6xY"
    _stage_blob(tmp_path, "tools/fixture.py", f'api_key = "{value}"\n'.encode())

    result = _run_tool(tmp_path, "--staged")

    assert result.returncode == 1
    assert "tools/fixture.py:1" in result.stderr
    assert "generic-credential-assignment" in result.stderr
    assert value not in result.stdout + result.stderr


def test_justified_exception_is_visible_and_allowed(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    value = "AK" + "IA" + "C" * 16
    content = value + " # vbb: allow-credential-example reason=unit-fixture\n"
    _stage_blob(tmp_path, "docs/example.md", content.encode())

    result = _run_tool(tmp_path, "--staged")

    assert result.returncode == 0
    assert "[ALLOW]" in result.stdout
    assert "reason=unit-fixture" in result.stdout
    assert value not in result.stdout + result.stderr


def test_exception_without_reason_still_blocks(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    value = "AK" + "IA" + "D" * 16
    content = value + " # vbb: allow-credential-example\n"
    _stage_blob(tmp_path, "docs/example.md", content.encode())

    result = _run_tool(tmp_path, "--staged")

    assert result.returncode == 1


def test_deletions_and_binary_blobs_are_ignored(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    value = "AK" + "IA" + "E" * 16
    _stage_blob(tmp_path, "tools/old.py", (value + "\n").encode())
    _git(tmp_path, "commit", "-q", "-m", "old fixture")
    _git(tmp_path, "update-index", "--force-remove", "tools/old.py")

    deletion = _run_tool(tmp_path, "--staged")
    assert deletion.returncode == 0

    _git(tmp_path, "reset", "-q", "--hard", "HEAD")
    _stage_blob(tmp_path, "assets/fixture.bin", b"prefix\x00" + value.encode())
    binary = _run_tool(tmp_path, "--staged")
    assert binary.returncode == 0


def test_range_mode_and_zero_base_fallback(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    base = _git(tmp_path, "rev-parse", "HEAD").decode().strip()
    value = "gh" + "p_" + "F" * 36
    _stage_blob(tmp_path, "tools/range.py", (value + "\n").encode())
    _git(tmp_path, "commit", "-q", "-m", "range fixture")
    head = _git(tmp_path, "rev-parse", "HEAD").decode().strip()

    explicit = _run_tool(tmp_path, "--range", base, head)
    zero_base = _run_tool(tmp_path, "--range", "0" * 40, head)

    assert explicit.returncode == 1
    assert zero_base.returncode == 1
    assert value not in explicit.stdout + explicit.stderr


def test_zero_base_on_initial_commit_scans_from_empty_tree(tmp_path: Path) -> None:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "tests@example.invalid")
    _git(tmp_path, "config", "user.name", "VBB Tests")
    value = "AK" + "IA" + "G" * 16
    _stage_blob(tmp_path, "tools/initial.py", (value + "\n").encode())
    _git(tmp_path, "commit", "-q", "-m", "initial fixture")
    head = _git(tmp_path, "rev-parse", "HEAD").decode().strip()

    result = _run_tool(tmp_path, "--range", "0" * 40, head)

    assert result.returncode == 1
    assert "tools/initial.py:1" in result.stderr
    assert value not in result.stdout + result.stderr


def test_invalid_range_returns_usage_error_without_traceback(tmp_path: Path) -> None:
    _init_repo(tmp_path)

    result = _run_tool(tmp_path, "--range", "missing-base", "HEAD")

    assert result.returncode == 2
    assert "[credentials] ERROR:" in result.stderr
    assert "Traceback" not in result.stderr


def test_hook_blocks_the_same_staged_finding(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    (tmp_path / "tools").mkdir(exist_ok=True)
    (tmp_path / "scripts" / "hooks").mkdir(parents=True)
    (tmp_path / "tools" / TOOL_PATH.name).write_bytes(TOOL_PATH.read_bytes())
    hook_source = REPO_ROOT / "scripts" / "hooks" / "pre-commit-framework-gate"
    hook_path = tmp_path / "scripts" / "hooks" / hook_source.name
    hook_path.write_bytes(hook_source.read_bytes())
    hook_path.chmod(0o755)
    value = "Q8nP5rS9tU3wX7yZ"
    _stage_blob(tmp_path, "tools/blocked.py", f'secret = "{value}"\n'.encode())

    result = subprocess.run(
        ["bash", str(hook_path)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "credentials gate failed" in result.stderr
    assert value not in result.stdout + result.stderr
