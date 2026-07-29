#!/usr/bin/env python3
"""Select only closeouts changed between a trusted base and a candidate HEAD.

The zero ``github.event.before`` used for a first branch push is not a Git
base.  In that case callers must provide a fetched default-branch ref so the
selector can derive a merge-base.  There is deliberately no historical
``git ls-files`` fallback: an unknown base is a hard error.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ZERO_SHA = "0" * 40


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _commit(repo: Path, rev: str) -> str | None:
    if not rev or rev == ZERO_SHA:
        return None
    result = _git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}")
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _trusted_base(repo: Path, requested: str, default_ref: str) -> str | None:
    direct = _commit(repo, requested)
    if direct:
        return direct
    default = _commit(repo, default_ref)
    if not default:
        return None
    head = _commit(repo, "HEAD")
    if not head:
        return None
    merge_base = _git(repo, "merge-base", default, head)
    if merge_base.returncode != 0 or not merge_base.stdout.strip():
        return None
    return merge_base.stdout.strip()


def select_changed_closeouts(
    repo: Path, requested_base: str, head: str, default_ref: str
) -> list[str]:
    resolved_head = _commit(repo, head)
    if not resolved_head:
        raise ValueError("candidate HEAD is not a valid commit")
    if resolved_head != _commit(repo, "HEAD"):
        raise ValueError("candidate HEAD does not match the evaluated checkout")
    base = _trusted_base(repo, requested_base, default_ref)
    if not base:
        raise ValueError(
            "no reliable Git base: provide a valid before SHA or a fetched "
            "default-branch ref"
        )
    result = _git(
        repo,
        "diff",
        "--name-only",
        "--diff-filter=ACMR",
        base,
        resolved_head,
        "--",
        "docs/runs/*/07_CLOSEOUT.md",
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "git diff failed")
    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--default-ref", required=True)
    args = parser.parse_args()
    try:
        for path in select_changed_closeouts(
            args.repo, args.base_sha, args.head_sha, args.default_ref
        ):
            print(path)
    except ValueError as exc:
        print(f"changed-run selection failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
