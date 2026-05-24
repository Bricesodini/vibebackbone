#!/usr/bin/env python3
"""
VBB Context Compactor — produces a short, reliable, re-injectable summary
of a run or set of runs.

Usage:
    python tools/vbb-context-compactor.py docs/runs/<run_id>
    python tools/vbb-context-compactor.py docs/runs/<run_id> --stdout
    python tools/vbb-context-compactor.py docs/runs/<run_id> --output <path>

Reads all phase artifacts in a run directory and produces CONTEXT_SUMMARY.md
with: objective, current status, decisions, files changed, risks, next action,
re-entry prompt.
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Optional


def read_file(path: Path) -> str:
    """Read a file, return content or empty string if unreadable."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    fm_raw = content[3:end].strip()
    # Minimal YAML parsing (no dependency)
    result = {}
    for line in fm_raw.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            key = key.strip().strip('"').strip("'")
            val = val.strip().strip('"').strip("'")
            if val:
                result[key] = val
    return result


def extract_sections(content: str) -> dict:
    """Extract ## sections from markdown content."""
    sections = {}
    current_section = None
    current_lines = []
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()
    return sections


def extract_files_changed(content: str) -> list:
    """Extract file paths mentioned in content (heuristic)."""
    # Match common patterns: `path/to/file`, path/to/file.md, etc.
    patterns = [
        r'`([a-zA-Z0-9_/.-]+\.[a-zA-Z0-9]+)`',  # `file.ext`
        r'([a-zA-Z0-9_/.-]+\.(?:py|sh|yml|yaml|md|json|toml))',  # bare file.ext
    ]
    files = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            f = match.group(1)
            # Filter obvious non-files
            if any(skip in f.lower() for skip in ["example", "http", "todo", "fixme"]):
                continue
            if len(f) < 4:
                continue
            files.add(f)
    return sorted(files)


def compact_run(run_dir: Path) -> str:
    """Read a run directory and produce a context summary."""
    if not run_dir.exists():
        print(f"Error: run directory not found: {run_dir}", file=sys.stderr)
        sys.exit(1)

    if not run_dir.is_dir():
        print(f"Error: not a directory: {run_dir}", file=sys.stderr)
        sys.exit(1)

    # Read all phase artifacts in order
    phase_files = sorted(run_dir.glob("*.md"))
    if not phase_files:
        print(f"Error: no markdown files found in {run_dir}", file=sys.stderr)
        sys.exit(1)

    all_content = ""
    frontmatter = {}
    all_sections = {}

    for pf in phase_files:
        content = read_file(pf)
        all_content += content + "\n\n"
        fm = extract_frontmatter(content)
        frontmatter.update(fm)
        sections = extract_sections(content)
        all_sections.update(sections)

    # Extract key information
    run_id = frontmatter.get("run_id", run_dir.name)
    voie = frontmatter.get("voie", "UNKNOWN")
    status = frontmatter.get("status", "UNKNOWN")
    agent = frontmatter.get("agent", "local")

    # Build objective from intake or first section
    objective = ""
    for key in ["Objectif", "Objective", "Résumé", "Summary", "Scope", "INTAKE"]:
        if key in all_sections:
            objective = all_sections[key][:300]
            break
    if not objective:
        # Take first non-empty section
        for v in all_sections.values():
            if v.strip():
                objective = v[:300]
                break

    # Build current status from closeout or summary
    current_status = ""
    for key in ["Verdict", "Statut global", "Résumé", "Current status", "Summary",
                "Statut", "CLOSEOUT", "Résultats"]:
        if key in all_sections:
            current_status = all_sections[key][:300]
            break

    # Build decisions
    decisions = ""
    for key in ["Décisions", "Decisions", "Key decisions", "Décision", "Choix"]:
        if key in all_sections:
            decisions = all_sections[key][:500]
            break

    # Collect files changed
    files_changed = extract_files_changed(all_content)

    # Build risks section
    risks = ""
    for key in ["Risques résiduels", "Risques", "Risks", "Risques résiduels",
                "Risques résiduels", "ACCEPTED_RISK"]:
        if key in all_sections:
            risks = all_sections[key][:500]
            break

    # Next action
    next_action = ""
    for key in ["Prochaine action", "Next action", "Next steps", "Suite"]:
        if key in all_sections:
            next_action = all_sections[key][:300]
            break

    # Build re-entry prompt
    reentry = (
        f"Reprise du run {run_id} ({voie}). "
        + (f"Statut: {current_status[:100]}. " if current_status else "")
        + (f"Prochaine action: {next_action[:150]}." if next_action else "")
    )

    # Assemble summary
    lines = [
        "# Context Summary",
        "",
        f"**Run**: {run_id}  ",
        f"**Voie**: {voie}  ",
        f"**Agent**: {agent}  ",
        "",
        "## Objective",
        "",
        objective or "_(not found in artifacts)_",
        "",
        "## Current status",
        "",
        current_status or "_(not found in artifacts)_",
        "",
        "## Decisions",
        "",
        decisions or "_(no decisions recorded)_",
        "",
        "## Files changed",
        "",
    ]
    if files_changed:
        for f in files_changed:
            lines.append(f"- `{f}`")
    else:
        lines.append("_(no files identified)_")

    lines.extend([
        "",
        "## Risks",
        "",
        risks or "_(no risks recorded)_",
        "",
        "## Next action",
        "",
        next_action or "_(no next action recorded)_",
        "",
        "## Re-entry prompt",
        "",
        f"> {reentry}",
        "",
    ])

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="VBB Context Compactor — produce a short summary of a run"
    )
    parser.add_argument(
        "run_path",
        type=str,
        help="Path to the run directory (e.g. docs/runs/2026-06-11_0900_lot1c-quick-wins/)"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write summary to stdout instead of file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write summary to a custom path instead of <run>/CONTEXT_SUMMARY.md"
    )

    args = parser.parse_args()

    run_dir = Path(args.run_path)

    if not run_dir.exists():
        print(f"Error: run directory not found: {run_dir}", file=sys.stderr)
        return 1

    summary = compact_run(run_dir)

    if args.stdout:
        print(summary)
        return 0

    output_path = Path(args.output) if args.output else run_dir / "CONTEXT_SUMMARY.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(summary, encoding="utf-8")
    print(f"✓ Context summary written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())