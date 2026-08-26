#!/usr/bin/env python3
"""Discover the single applicable repository-local AGENTS.md contract.

The tool deliberately performs no parent walk: it selects AGENTS.md in the
launch directory, otherwise AGENTS.md in that directory's effective Git root.
Its JSON output is a bootstrap trace; the invoking agent must then read the
reported contract before interpreting project state or classifying work.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


def _git_root(cwd: Path) -> Optional[Path]:
    result = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        return None
    return Path(result.stdout.strip()).resolve()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _git_state(path: Path, root: Optional[Path]) -> str:
    if root is None or not _is_within(path, root):
        return "UNKNOWN"
    relative = str(path.relative_to(root))
    tracked = (
        subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
            capture_output=True,
            text=True,
            check=False,
        ).returncode
        == 0
    )
    if not tracked:
        return "UNTRACKED"
    dirty = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "--", relative],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    return "MODIFIED" if dirty else "TRACKED"


def discover(cwd: Path) -> dict:
    launch_dir = cwd.resolve()
    root = _git_root(launch_dir)
    candidates = [launch_dir / "AGENTS.md"]
    if root is not None and root != launch_dir:
        candidates.append(root / "AGENTS.md")

    for candidate in candidates:
        if not candidate.exists() and not candidate.is_symlink():
            continue
        if not candidate.is_file():
            return _result(launch_dir, root, candidate, "INVALID_PATH", "UNKNOWN")
        try:
            resolved = candidate.resolve(strict=True)
            resolved.read_text(encoding="utf-8")
        except (OSError, RuntimeError, UnicodeDecodeError) as exc:
            return _result(
                launch_dir, root, candidate, "UNREADABLE", "UNKNOWN", str(exc)
            )
        if root is None or not _is_within(resolved, root):
            return _result(
                launch_dir,
                root,
                candidate,
                "EXTERNAL_SYMLINK",
                "UNKNOWN",
                "contract target is outside the effective Git root",
            )
        return _result(launch_dir, root, resolved, "READY", _git_state(resolved, root))
    return _result(launch_dir, root, None, "NONE", "UNKNOWN")


def _result(
    launch_dir: Path,
    root: Optional[Path],
    contract: Optional[Path],
    status: str,
    git_state: str,
    detail: Optional[str] = None,
) -> dict:
    return {
        "launch_directory": str(launch_dir),
        "repository_root": str(root) if root else None,
        "local_agent_contract": str(contract) if contract else "NONE",
        "local_agent_contract_status": status,
        "agents_md_git_state": git_state,
        "detail": detail,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="launch directory")
    args = parser.parse_args()
    if not args.cwd.is_dir():
        parser.error(f"not a directory: {args.cwd}")
    result = discover(args.cwd)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["local_agent_contract_status"] in {"READY", "NONE"} else 1


if __name__ == "__main__":
    sys.exit(main())
