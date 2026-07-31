#!/usr/bin/env python3
"""Deterministic vbb-doc-v1 validator with progressive-scope guidance."""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

CONTRACT = "vbb-doc-v1"
VERSION = "1.0"
TAGS = {
    "documentation",
    "governance",
    "contract",
    "reference",
    "template",
    "review",
    "run",
    "audit",
    "decision",
    "adr",
    "migration",
    "adoption",
    "public",
    "internal",
    "experimental",
    "deprecated",
    "frozen",
    "historical",
    "release",
    "architecture",
    "security",
    "quality",
    "distribution",
}
TYPES = {
    "reference",
    "governance",
    "run_artifact",
    "audit_report",
    "decision_record",
    "adr",
    "template",
    "adoption",
    "migration_report",
    "historical",
}
STATUS = {
    "reference": {"active", "draft", "deprecated", "frozen"},
    "governance": {"active", "draft", "deprecated", "frozen"},
    "adoption": {"active", "draft", "deprecated", "frozen"},
    "template": {"active", "deprecated", "experimental", "frozen"},
    "run_artifact": {"ready", "partial", "blocked", "unknown"},
    "audit_report": {"ready", "partial", "blocked", "unknown"},
    "decision_record": {"proposed", "accepted", "rejected", "superseded"},
    "adr": {"proposed", "accepted", "rejected", "superseded"},
    "migration_report": {"ready", "partial", "blocked", "unknown"},
    "historical": {"historical"},
}
REQUIRED = {
    "document_convention",
    "version",
    "type",
    "status",
    "visibility",
    "tags",
    "relations",
}
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def _yaml(path: Path):
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text) or {}
    result = {}
    for line in text.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def _frontmatter(path: Path):
    match = FM_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        return None
    if yaml is not None:
        return yaml.safe_load(match.group(1)) or {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def _list(value):
    if isinstance(value, str):
        return [value]
    return [str(item) for item in (value or [])]


def load_declaration(root: Path):
    path = root / ".vbb/document-convention.yaml"
    if not path.exists():
        return None, ["adoption declaration missing: .vbb/document-convention.yaml"]
    data = _yaml(path)
    errors = []
    if data.get("document_convention") != CONTRACT:
        errors.append(
            "version absent or unknown: document_convention must be vbb-doc-v1"
        )
    if str(data.get("version")) != VERSION:
        errors.append(f"version absent or unknown: version must be {VERSION}")
    if data.get("adoption") != "adopted":
        errors.append("adoption must be adopted")
    scope = data.get("scope") or {}
    if not isinstance(scope, dict) or not _list(scope.get("roots")):
        errors.append("scope.roots must contain at least one root")
    for index, waiver in enumerate(data.get("waivers") or []):
        if (
            not isinstance(waiver, dict)
            or not waiver.get("path")
            or not waiver.get("reason")
        ):
            errors.append(f"waivers[{index}] requires path and reason")
    return data, errors


def _waived(rel, waivers):
    return any(
        fnmatch.fnmatch(rel, str(item.get("path", "")))
        for item in waivers
        if isinstance(item, dict)
    )


def paths(root: Path, declaration: dict):
    scope = declaration.get("scope") or {}
    excludes = _list(scope.get("excludes"))
    waivers = declaration.get("waivers") or []
    result = []
    for item in _list(scope.get("roots")):
        candidate = root / item
        found = (
            [candidate]
            if candidate.is_file()
            else sorted(candidate.rglob("*.md"))
            if candidate.is_dir()
            else []
        )
        for path in found:
            rel = path.relative_to(root).as_posix()
            if not any(
                fnmatch.fnmatch(rel, pattern) for pattern in excludes
            ) and not _waived(rel, waivers):
                result.append(path)
    return sorted(set(result))


def validate(root: Path):
    declaration, errors = load_declaration(root)
    if errors:
        return errors
    files = paths(root, declaration)
    if not files:
        errors.append("adopted scope contains no documents")
    for path in files:
        rel = path.relative_to(root).as_posix()
        fm = _frontmatter(path)
        if fm is None:
            errors.append(f"{rel}: metadata/frontmatter missing")
            continue
        errors.extend(
            f"{rel}: metadata mandatory field absent: {key}"
            for key in sorted(REQUIRED - fm.keys())
        )
        if fm.get("document_convention") != CONTRACT:
            errors.append(f"{rel}: version absent or unknown")
        if str(fm.get("version")) != VERSION:
            errors.append(f"{rel}: incompatible version")
        typ = fm.get("type")
        if typ not in TYPES:
            errors.append(f"{rel}: unknown document type {typ!r}")
            continue
        if fm.get("status") not in STATUS[typ]:
            errors.append(f"{rel}: invalid status {fm.get('status')!r} for type {typ}")
        if fm.get("visibility") not in {"public", "internal", "experimental"}:
            errors.append(f"{rel}: invalid visibility")
        tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
        for tag in tags:
            if tag not in TAGS and not str(tag).startswith("project:"):
                errors.append(f"{rel}: unknown tag {tag}")
        extensions = fm.get("status_extensions", [])
        extensions = [extensions] if isinstance(extensions, str) else extensions
        for extension in extensions or []:
            if not str(extension).startswith("project:status:"):
                errors.append(
                    f"{rel}: invalid status extension {extension!r}; use project:status:<value>"
                )
        relations = fm.get("relations") if isinstance(fm.get("relations"), list) else []
        if typ == "adoption" and not any(
            "DOCUMENT_CONVENTION.md" in str(item) for item in relations
        ):
            errors.append(f"{rel}: required relation to DOCUMENT_CONVENTION.md missing")
        if (
            typ in {"adr", "decision_record", "audit_report", "migration_report"}
            and not relations
        ):
            errors.append(f"{rel}: required evidence relation missing")
        if typ == "run_artifact" and not fm.get("run_id"):
            errors.append(f"{rel}: run_id missing")
        if typ == "audit_report" and not all(
            fm.get(key) for key in ("run_id", "route", "subject", "verdict")
        ):
            errors.append(f"{rel}: audit report metadata incomplete")
        if (
            typ == "template"
            and "_TEMPLATE.md" in path.name
            and fm.get("status") != "deprecated"
        ):
            errors.append(f"{rel}: legacy template used as current template")
        if fm.get("status") == "historical" and typ != "historical":
            errors.append(f"{rel}: active document classified as historical")
        if typ == "historical" and fm.get("status") != "historical":
            errors.append(f"{rel}: historical document is not classified as historical")
    return errors


def suggest_scope(root: Path):
    declaration, errors = load_declaration(root)
    if errors:
        return errors
    adopted = {path.relative_to(root).as_posix() for path in paths(root, declaration)}
    excludes = _list((declaration.get("scope") or {}).get("excludes"))
    print("VBB-DOC-V1: SCOPE SUGGESTIONS")
    for path in sorted((root / "docs").rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if rel in adopted or any(fnmatch.fnmatch(rel, pattern) for pattern in excludes):
            continue
        print(
            f"- {rel}: {'candidate' if _frontmatter(path) else 'missing frontmatter'}"
        )
    return []


def main():
    parser = argparse.ArgumentParser(
        description="Check an adopted repository against vbb-doc-v1."
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument(
        "--suggest-scope", action="store_true", help="list docs outside declared scope"
    )
    args = parser.parse_args()
    errors = (
        suggest_scope(Path(args.root).resolve())
        if args.suggest_scope
        else validate(Path(args.root).resolve())
    )
    if errors:
        print("VBB-DOC-V1: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    if not args.suggest_scope:
        print("VBB-DOC-V1: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
