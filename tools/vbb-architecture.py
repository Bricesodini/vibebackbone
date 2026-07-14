#!/usr/bin/env python3
"""
VBB Architecture — structured ARCHITECTURE.md parser and relation renderer.

Usage:
    python tools/vbb-architecture.py lint
    python tools/vbb-architecture.py graph
    python tools/vbb-architecture.py graph --write
    python tools/vbb-architecture.py json
"""

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

REPO_ROOT = Path(__file__).parent.parent.resolve()
ARCHITECTURE_PATH = Path("docs/ARCHITECTURE.md")
RELATIONS_PATH = Path("docs/RELATIONS.md")

ARCHITECTURE_TOUCH_GLOBS = [
    ".github/workflows/vbb-contracts.yml",
    "AGENTS.md",
    "SYSTEM.md",
    "docs/AUDIT_STATUS.md",
    "docs/ARCHITECTURE.md",
    "docs/adr/*.md",
    "docs/CONTEXT.md",
    "docs/PILOTAGE.md",
    "docs/PROJECT_MODE.md",
    "docs/RELATIONS.md",
    "docs/SESSION_RULES.md",
    "scripts/vbb-ci-local.sh",
    "skills/t-vbb-dependency-mapper/**",
    "skills/t-vbb-impact-analyzer/**",
    "skills/vibebackbone/**",
    "tests/test_vbb_architecture.py",
    "tools/vbb-architecture.py",
    "tools/vbb-contract-*.py",
    "tools/vbb-phase-router.py",
    "tools/vbb-project-init.py",
    "tools/vbb-status-dashboard.py",
]

REQUIRED_FIELDS = {
    "id",
    "type",
    "status",
    "role",
    "responsibilities",
    "depends_on",
    "impacts",
    "files",
    "contracts",
    "tests",
    "risks",
}

LIST_FIELDS = {
    "responsibilities",
    "depends_on",
    "impacts",
    "files",
    "contracts",
    "tests",
    "risks",
}

VALID_STATUSES = {"active", "planned", "deprecated", "unknown"}
VALID_TYPES = {
    "domain",
    "technical",
    "governance",
    "tooling",
    "distribution",
    "data",
    "ui",
    "external",
}

BLOCK_HEADING_RE = re.compile(r"^##\s+(?:Bloc|Block):\s+(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"```ya?ml\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def _repo_path(repo: Path, rel: Path) -> Path:
    return repo / rel


def _read_architecture(repo: Path) -> str:
    path = _repo_path(repo, ARCHITECTURE_PATH)
    if not path.exists():
        raise FileNotFoundError(f"{ARCHITECTURE_PATH} not found")
    return path.read_text(encoding="utf-8")


def _normalize_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def parse_blocks(text: str) -> Tuple[List[Dict], List[str]]:
    """Extract structured architecture blocks from Markdown."""
    warnings = []
    matches = list(BLOCK_HEADING_RE.finditer(text))
    blocks = []

    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[start:end]
        fence = FENCE_RE.search(section)
        if not fence:
            warnings.append(f"Block '{title}' has no YAML fence")
            continue
        try:
            data = yaml.safe_load(fence.group(1)) or {}
        except yaml.YAMLError as exc:
            data = {"__yaml_error__": str(exc)}
        if not isinstance(data, dict):
            data = {"__yaml_error__": "YAML fence must contain a mapping"}
        data.setdefault("title", title)
        blocks.append(data)

    return blocks, warnings


def validate_blocks(
    blocks: List[Dict], parse_warnings: List[str]
) -> Tuple[List[str], List[str]]:
    """Validate block shape and local dependency references."""
    errors = []
    warnings = list(parse_warnings)
    ids = []

    if not blocks:
        errors.append(
            "No architecture blocks found. Expected headings like '## Bloc: Auth'."
        )
        return errors, warnings

    for i, block in enumerate(blocks):
        label = block.get("title", f"block[{i}]")
        if "__yaml_error__" in block:
            errors.append(f"{label}: invalid YAML: {block['__yaml_error__']}")
            continue

        missing = sorted(REQUIRED_FIELDS - set(block.keys()))
        for field in missing:
            errors.append(f"{label}: missing required field '{field}'")

        block_id = block.get("id")
        if isinstance(block_id, str):
            if not ID_RE.match(block_id):
                errors.append(f"{label}: id '{block_id}' must match {ID_RE.pattern}")
            ids.append(block_id)
        elif block_id is not None:
            errors.append(f"{label}: id must be a string")

        status = block.get("status")
        if status is not None and status not in VALID_STATUSES:
            errors.append(f"{label}: status '{status}' not in {sorted(VALID_STATUSES)}")

        block_type = block.get("type")
        if block_type is not None and block_type not in VALID_TYPES:
            errors.append(f"{label}: type '{block_type}' not in {sorted(VALID_TYPES)}")

        role = block.get("role")
        if role is not None and (not isinstance(role, str) or not role.strip()):
            errors.append(f"{label}: role must be a non-empty string")

        for field in LIST_FIELDS:
            if field in block and not isinstance(block[field], list):
                errors.append(f"{label}: {field} must be a list")

        for risk in _normalize_list(block.get("risks")):
            if not isinstance(risk, dict):
                errors.append(f"{label}: each risk must be a mapping")
                continue
            if "id" not in risk or "level" not in risk or "note" not in risk:
                errors.append(f"{label}: each risk must contain id, level and note")

    duplicate_ids = sorted({block_id for block_id in ids if ids.count(block_id) > 1})
    for block_id in duplicate_ids:
        errors.append(f"Duplicate block id '{block_id}'")

    known = set(ids)
    for block in blocks:
        block_id = block.get("id", block.get("title", "unknown"))
        for dep in _normalize_list(block.get("depends_on")):
            if dep not in known:
                warnings.append(
                    f"{block_id}: depends_on '{dep}' does not match a known block id"
                )

    return errors, warnings


def _iter_architecture_touch_files(repo: Path) -> List[str]:
    """Return existing files considered architecture-sensitive."""
    files = set()
    for pattern in ARCHITECTURE_TOUCH_GLOBS:
        files.update(
            str(path.relative_to(repo))
            for path in repo.glob(pattern)
            if path.is_file() and not path.name.endswith(".bak")
        )
    return sorted(files)


def _pattern_matches(path: str, pattern: str) -> bool:
    """Match repo-relative file paths against ARCHITECTURE.md file patterns."""
    if fnmatch.fnmatch(path, pattern):
        return True
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-3].rstrip("/") + "/")
    return False


def validate_architecture_coverage(repo: Path, blocks: List[Dict]) -> List[str]:
    """Ensure architecture-sensitive files are referenced by at least one block."""
    patterns = []
    for block in blocks:
        patterns.extend(str(item) for item in _normalize_list(block.get("files")))

    errors = []
    for rel_path in _iter_architecture_touch_files(repo):
        if not any(_pattern_matches(rel_path, pattern) for pattern in patterns):
            errors.append(
                f"Architecture-sensitive file '{rel_path}' is not referenced by any block files pattern"
            )
    return errors


def load_architecture(repo: Path) -> Tuple[List[Dict], List[str], List[str]]:
    text = _read_architecture(repo)
    blocks, parse_warnings = parse_blocks(text)
    errors, warnings = validate_blocks(blocks, parse_warnings)
    if not errors:
        errors.extend(validate_architecture_coverage(repo, blocks))
    return blocks, errors, warnings


def render_mermaid(blocks: List[Dict]) -> str:
    """Render a Mermaid dependency graph from architecture blocks."""
    known = {block.get("id") for block in blocks}
    lines = ["graph TD"]
    for block in blocks:
        block_id = block.get("id")
        title = block.get("title", block_id)
        status = block.get("status", "unknown")
        block_type = block.get("type", "unknown")
        label = f"{title}<br/>{block_type} · {status}"
        lines.append(f'  {block_id}["{label}"]')
    for block in blocks:
        block_id = block.get("id")
        for dep in _normalize_list(block.get("depends_on")):
            if dep in known:
                lines.append(f"  {block_id} --> {dep}")
    return "\n".join(lines)


def render_relations(blocks: List[Dict]) -> str:
    """Render docs/RELATIONS.md from architecture blocks."""
    mermaid = render_mermaid(blocks)
    lines = [
        "---",
        "context_role: architecture-relations",
        "phase: transverse",
        "status: generated",
        "source: ARCHITECTURE.md",
        "---",
        "",
        "# RELATIONS — Architecture Projection",
        "",
        "> Generated from `docs/ARCHITECTURE.md` by `tools/vbb-architecture.py graph --write`.",
        "> Do not edit this file as the source of truth.",
        "",
        "## Dependency Graph",
        "",
        "```mermaid",
        mermaid,
        "```",
        "",
        "## Sensitive Zones",
        "",
    ]

    sensitive = []
    for block in blocks:
        risks = _normalize_list(block.get("risks"))
        high = [
            risk
            for risk in risks
            if isinstance(risk, dict) and risk.get("level") in {"P0", "P1"}
        ]
        if high:
            sensitive.append((block, high))

    if sensitive:
        lines.extend(["| Block | Risks |", "|-------|-------|"])
        for block, risks in sensitive:
            risk_text = "; ".join(
                f"{risk.get('id')}: {risk.get('note')}" for risk in risks
            )
            lines.append(f"| `{block.get('id')}` | {risk_text} |")
    else:
        lines.append("No P0/P1 risks declared in architecture blocks.")

    lines.extend(
        [
            "",
            "## Impact Index",
            "",
            "| Block | Depends on | Impacts | Files |",
            "|-------|------------|---------|-------|",
        ]
    )
    for block in blocks:
        depends = (
            ", ".join(f"`{dep}`" for dep in _normalize_list(block.get("depends_on")))
            or "-"
        )
        impacts = (
            ", ".join(str(item) for item in _normalize_list(block.get("impacts")))
            or "-"
        )
        files = (
            ", ".join(f"`{item}`" for item in _normalize_list(block.get("files")))
            or "-"
        )
        lines.append(f"| `{block.get('id')}` | {depends} | {impacts} | {files} |")

    lines.append("")
    return "\n".join(lines)


def cmd_lint(repo: Path) -> int:
    try:
        blocks, errors, warnings = load_architecture(repo)
    except FileNotFoundError as exc:
        print(f"VBB Architecture Linter — BLOCKED: {exc}")
        return 1

    print(
        f"VBB Architecture Linter — {len(errors)} error(s), {len(warnings)} warning(s)"
    )
    print(f"  Blocks: {len(blocks)}")
    for warning in warnings:
        print(f"  WARN: {warning}")
    for error in errors:
        print(f"  ERROR: {error}")
    if errors:
        return 1
    print("  ✓ Architecture blocks valid")
    return 0


def cmd_graph(repo: Path, write: bool) -> int:
    try:
        blocks, errors, warnings = load_architecture(repo)
    except FileNotFoundError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)

    output = render_relations(blocks)
    if write:
        path = _repo_path(repo, RELATIONS_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(f"Generated {RELATIONS_PATH}")
    else:
        print(output)
    return 0


def cmd_json(repo: Path) -> int:
    try:
        blocks, errors, warnings = load_architecture(repo)
    except FileNotFoundError as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "status": "PASS" if not errors else "FAIL",
                "blocks": blocks,
                "errors": errors,
                "warnings": warnings,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and render structured VBB architecture docs."
    )
    parser.add_argument("command", choices=["lint", "graph", "json"])
    parser.add_argument("--repo", default=str(REPO_ROOT), help="Repository root")
    parser.add_argument(
        "--write", action="store_true", help="Write docs/RELATIONS.md for graph command"
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.exists():
        print(f"Repository not found: {repo}", file=sys.stderr)
        return 1

    if args.command == "lint":
        return cmd_lint(repo)
    if args.command == "graph":
        return cmd_graph(repo, args.write)
    if args.command == "json":
        return cmd_json(repo)
    return 1


if __name__ == "__main__":
    sys.exit(main())
