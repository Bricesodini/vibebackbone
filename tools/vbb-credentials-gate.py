#!/usr/bin/env python3
"""Block newly added credential-like content in staged or commit-range diffs.

The gate scans added text lines only. It never prints the matched value and has
no third-party dependency. Exit codes: 0 clean, 1 findings, 2 Git/usage error.
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class AddedLine:
    path: str
    number: int
    text: str


@dataclass(frozen=True)
class Finding:
    path: str
    number: int
    rule: str


@dataclass(frozen=True)
class AllowedExample:
    path: str
    number: int
    reason: str


HIGH_CONFIDENCE_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b")),
    ("github-fine-grained-token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,255}\b")),
    ("gitlab-token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,255}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,255}\b")),
    ("stripe-live-secret", re.compile(r"\bsk_live_[A-Za-z0-9]{20,255}\b")),
    ("openai-style-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,255}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    (
        "private-key-boundary",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
)

GENERIC_ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|passwd|secret)"
    r"\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+=:@-]{12,})"
)

PLACEHOLDER_VALUE = re.compile(
    r"(?i)(?:example|dummy|fake|fixture|placeholder|redacted|changeme|"
    r"not[_-]?a[_-]?secret|synthetic|your[_-])"
)

ALLOW_MARKER = re.compile(r"vbb:\s*allow-credential-example\s+reason=([A-Za-z0-9._-]+)")

HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


class GitError(RuntimeError):
    """Raised when a Git command required by the gate fails."""


def _git(
    repo: Path,
    args: Sequence[str],
    *,
    input_bytes: bytes | None = None,
) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_bytes,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise GitError(detail or f"git {' '.join(args)} failed")
    return result.stdout


def _decode_git_path(value: str) -> str:
    value = value.strip()
    if value == "/dev/null":
        return value
    if value.startswith('"'):
        try:
            value = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            pass
    return value[2:] if value.startswith("b/") else value


def parse_added_lines(diff: bytes) -> list[AddedLine]:
    """Extract added text lines and their new-file line numbers from a Git diff."""
    lines = diff.decode("utf-8", errors="replace").splitlines()
    added: list[AddedLine] = []
    current_path: str | None = None
    current_line = 0
    in_hunk = False

    for raw in lines:
        if raw.startswith("diff --git "):
            current_path = None
            in_hunk = False
            continue
        if not in_hunk and raw.startswith("+++ "):
            path = _decode_git_path(raw[4:])
            current_path = None if path == "/dev/null" else path
            continue
        if raw.startswith("@@ "):
            match = HUNK_HEADER.match(raw)
            in_hunk = match is not None
            if match:
                current_line = int(match.group(1))
            continue
        if not in_hunk or current_path is None:
            continue
        if raw.startswith("+"):
            added.append(AddedLine(current_path, current_line, raw[1:]))
            current_line += 1
        elif raw.startswith("-") or raw.startswith("\\ No newline"):
            continue
        else:
            current_line += 1

    return added


def detect_rules(text: str) -> list[str]:
    """Return rule names without returning or exposing the matched value."""
    high_confidence = [
        name for name, pattern in HIGH_CONFIDENCE_RULES if pattern.search(text)
    ]
    if high_confidence:
        return high_confidence

    generic = GENERIC_ASSIGNMENT.search(text)
    if generic and not PLACEHOLDER_VALUE.search(generic.group(1)):
        return ["generic-credential-assignment"]
    return []


def scan_added_lines(
    lines: Sequence[AddedLine],
) -> tuple[list[Finding], list[AllowedExample]]:
    findings: list[Finding] = []
    allowed: list[AllowedExample] = []
    for line in lines:
        rules = detect_rules(line.text)
        if not rules:
            continue
        marker = ALLOW_MARKER.search(line.text)
        if marker:
            allowed.append(AllowedExample(line.path, line.number, marker.group(1)))
            continue
        findings.extend(Finding(line.path, line.number, rule) for rule in rules)
    return findings, allowed


def staged_diff(repo: Path) -> bytes:
    return _git(
        repo,
        (
            "diff",
            "--cached",
            "--unified=0",
            "--no-color",
            "--no-ext-diff",
            "--no-textconv",
            "--find-renames",
            "--diff-filter=ACMR",
        ),
    )


def _resolved_commit(repo: Path, ref: str) -> str:
    return _git(repo, ("rev-parse", "--verify", f"{ref}^{{commit}}")).decode().strip()


def _fallback_base(repo: Path, head: str) -> str:
    try:
        return _resolved_commit(repo, f"{head}^1")
    except GitError:
        return _git(repo, ("mktree",), input_bytes=b"").decode().strip()


def range_diff(repo: Path, base: str, head: str) -> bytes:
    resolved_head = _resolved_commit(repo, head)
    if not base or set(base) == {"0"}:
        resolved_base = _fallback_base(repo, resolved_head)
    else:
        resolved_base = _resolved_commit(repo, base)
    return _git(
        repo,
        (
            "diff",
            resolved_base,
            resolved_head,
            "--unified=0",
            "--no-color",
            "--no-ext-diff",
            "--no-textconv",
            "--find-renames",
            "--diff-filter=ACMR",
        ),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan newly added Git lines for credential-like content."
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--staged",
        action="store_true",
        help="scan HEAD-to-index additions (default)",
    )
    modes.add_argument(
        "--range",
        nargs=2,
        metavar=("BASE", "HEAD"),
        help="scan additions between two commits; an empty/all-zero BASE uses HEAD^",
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = args.repo.resolve()
    try:
        diff = range_diff(repo, *args.range) if args.range else staged_diff(repo)
    except GitError as error:
        print(f"[credentials] ERROR: {error}", file=sys.stderr)
        return 2

    added = parse_added_lines(diff)
    findings, allowed = scan_added_lines(added)
    for example in allowed:
        print(
            f"{example.path}:{example.number}: [ALLOW] credential example "
            f"allowed (reason={example.reason})"
        )
    for finding in findings:
        print(
            f"{finding.path}:{finding.number}: [{finding.rule}] possible credential "
            "in added content",
            file=sys.stderr,
        )

    if findings:
        print(
            f"[credentials] FAIL: {len(findings)} finding(s); "
            "matched values were not printed",
            file=sys.stderr,
        )
        return 1
    print(f"[credentials] PASS: 0 findings, {len(added)} added text line(s) scanned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
