#!/usr/bin/env python3
"""
VBB Index — local text index for fast information retrieval.
No vector DB, no embeddings, no external dependencies.

Usage:
    python tools/vbb-index.py build              # build index
    python tools/vbb-index.py search "rapide zero" # search
    python tools/vbb-index.py stats               # index stats
    python tools/vbb-index.py build --repo <path>  # build for custom repo
    python tools/vbb-index.py search "..." --json # JSON output
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).parent.parent.resolve()
INDEX_DIR = REPO_ROOT / ".vbb" / "index"
MANIFEST_PATH = INDEX_DIR / "manifest.json"

# Sources to index (relative to repo root)
INDEX_SOURCES = [
    "docs/CONTEXT.md",
    "docs/AUDIT_STATUS.md",
    "docs/ACTIVITY_LOG.md",
    "docs/TEMPORAL_PROVENANCE.md",
    "README.md",
    "GUIDE.md",
    "AGENTS.md",
    "CLAUDE.md",
    "SYSTEM.md",
]

INDEX_GLOBS = [
    "docs/runs/**/*.md",
    "docs/audits/**/*.md",
    "docs/router/**/*.md",
    "skills/*/SKILL.md",
    "skills/*/CONTRACT.yaml",
    "prompts/**/*.md",
]

KIND_MAP = {
    "docs/runs": "run",
    "docs/audits": "audit",
    "docs/router": "router",
    "skills/": "skill",
    "CONTRACT.yaml": "contract",
    "prompts/": "prompt",
}


def _iter_index_files(repo: Path) -> List[Path]:
    """Return all files that should be represented in the local index."""
    files = []
    for rel in INDEX_SOURCES:
        fpath = repo / rel
        if fpath.exists() and fpath.is_file():
            files.append(fpath)
    for glob_pattern in INDEX_GLOBS:
        files.extend(fpath for fpath in sorted(repo.glob(glob_pattern)) if fpath.is_file())
    return files


def _index_is_stale(repo: Path, manifest_path: Path) -> bool:
    """Return true when indexed sources are newer than the manifest."""
    if not manifest_path.exists():
        return True
    try:
        manifest_mtime = manifest_path.stat().st_mtime
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except OSError:
        return True
    except json.JSONDecodeError:
        return True
    indexed_paths = {entry.get("path") for entry in manifest.get("entries", [])}
    source_paths = {str(fpath.relative_to(repo)) for fpath in _iter_index_files(repo)}
    if indexed_paths != source_paths:
        return True
    for fpath in _iter_index_files(repo):
        try:
            if fpath.stat().st_mtime > manifest_mtime:
                return True
        except OSError:
            continue
    return False


def _classify(path: str) -> str:
    """Classify a path into a kind."""
    for prefix, kind in KIND_MAP.items():
        if prefix in path:
            return kind
    return "doc"


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return max(1, len(text) // 4)


def _extract_headings(text: str) -> List[str]:
    """Extract markdown headings (## and #)."""
    headings = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                headings.append(heading)
    return headings[:20]  # cap at 20


def _extract_keywords(text: str) -> List[str]:
    """Extract simple keywords from text (lowercase, >3 chars, word frequency)."""
    words = re.findall(r'[a-zA-ZàâéèêëïîôùûüçÀÂÉÈÊËÏÎÔÙÛÜÇ]{4,}', text.lower())
    # Count and return top 15 unique by frequency
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    # Stop words
    stops = {"dans", "pour", "avec", "sans", "cette", "elles", "leurs", "aussi",
             "that", "this", "with", "from", "have", "been", "were", "will"}
    for s in stops:
        freq.pop(s, None)
    top = sorted(freq.keys(), key=lambda w: freq[w], reverse=True)[:15]
    return top


def _extract_title(path: str, text: str) -> str:
    """Extract a title from path or first heading."""
    # Try first heading
    for line in text.split("\n")[:10]:
        if line.strip().startswith("#"):
            return line.strip().lstrip("#").strip()
    # Fallback: filename
    return Path(path).stem.replace("-", " ").replace("_", " ")


def _read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def build_index(repo: Path) -> Dict:
    """Build the text index from repo sources."""
    entries = []
    index_dir = repo / ".vbb" / "index"
    manifest_path = index_dir / "manifest.json"

    for fpath in _iter_index_files(repo):
        rel = str(fpath.relative_to(repo))
        text = _read_file(fpath)
        entry = {
            "path": rel,
            "title": _extract_title(rel, text),
            "kind": _classify(rel),
            "tokens_estimate": _estimate_tokens(text),
            "headings": _extract_headings(text),
            "keywords": _extract_keywords(text),
            "updated_at": _get_mtime(fpath),
        }
        entries.append(entry)

    manifest = {
        "version": "1.0",
        "repo": str(repo),
        "entries": entries,
        "total_entries": len(entries),
        "total_tokens": sum(e["tokens_estimate"] for e in entries),
    }

    # Write index
    index_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def _get_mtime(path: Path) -> str:
    try:
        import os
        t = os.path.getmtime(path)
        from datetime import datetime
        return datetime.fromtimestamp(t).isoformat()[:10]
    except OSError:
        return "unknown"


def search_index(query: str, repo: Path, json_mode: bool = False) -> List[Dict]:
    """Search the index for entries matching the query."""
    manifest_path = repo / ".vbb" / "index" / "manifest.json"
    if _index_is_stale(repo, manifest_path):
        build_index(repo)

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    query_terms = [w.lower() for w in re.findall(r'[a-zA-ZàâéèêëïîôùûüçÀÂÉÈÊËÏÎÔÙÛÜÇ]{3,}', query)]
    if not query_terms:
        return []

    results = []
    for entry in manifest.get("entries", []):
        score = 0
        # Title match (weight 3)
        title_lower = entry.get("title", "").lower()
        for term in query_terms:
            if term in title_lower:
                score += 3

        # Heading match (weight 2)
        headings_text = " ".join(entry.get("headings", [])).lower()
        for term in query_terms:
            if term in headings_text:
                score += 2

        # Path match (weight 2)
        path_lower = entry.get("path", "").lower()
        for term in query_terms:
            if term in path_lower:
                score += 2

        # Keyword match (weight 1)
        keywords = [k.lower() for k in entry.get("keywords", [])]
        for term in query_terms:
            if term in keywords:
                score += 1

        if score > 0:
            # Extract short excerpt from title/keywords
            excerpt = entry.get("title", "")
            kw = entry.get("keywords", [])[:5]
            if kw:
                excerpt += f" [{', '.join(kw)}]"

            results.append({
                "path": entry["path"],
                "title": entry.get("title", ""),
                "score": score,
                "kind": entry.get("kind", "doc"),
                "excerpt": excerpt[:120],
            })

    # Sort by score descending
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:20]


def show_stats(repo: Path) -> str:
    """Show index statistics."""
    manifest_path = repo / ".vbb" / "index" / "manifest.json"
    if not manifest_path.exists():
        return "Index not found. Run 'python tools/vbb-index.py build' first."

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    total = manifest.get("total_entries", 0)
    tokens = manifest.get("total_tokens", 0)
    entries = manifest.get("entries", [])

    by_kind = {}
    for e in entries:
        k = e.get("kind", "unknown")
        by_kind[k] = by_kind.get(k, 0) + 1

    lines = [
        "VBB Index Stats",
        "=" * 40,
        f"  Entries    : {total}",
        f"  Tokens est.: {tokens:,}",
        "",
        "  By kind:",
    ]
    for kind in sorted(by_kind.keys()):
        lines.append(f"    {kind:<12}: {by_kind[kind]}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="VBB Index — local text index for fast retrieval"
    )
    sub = parser.add_subparsers(dest="command")

    build_p = sub.add_parser("build", help="Build the index")
    build_p.add_argument("--repo", type=str, default=None)

    search_p = sub.add_parser("search", help="Search the index")
    search_p.add_argument("query", type=str)
    search_p.add_argument("--json", action="store_true", dest="json_mode")
    search_p.add_argument("--repo", type=str, default=None)

    stats_p = sub.add_parser("stats", help="Show index statistics")
    stats_p.add_argument("--repo", type=str, default=None)

    args = parser.parse_args()

    repo = Path(args.repo) if getattr(args, "repo", None) else REPO_ROOT

    if args.command == "build":
        manifest = build_index(repo)
        print(f"✓ Index built: {manifest['total_entries']} entries, ~{manifest['total_tokens']:,} tokens")
        return 0

    elif args.command == "search":
        results = search_index(args.query, repo, json_mode=getattr(args, "json_mode", False))
        if not results:
            return 1
        if getattr(args, "json_mode", False):
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            for r in results:
                print(f"  [{r['score']:>2}] {r['path']}")
                print(f"       {r['title']}")
                print(f"       {r['excerpt'][:100]}")
                print()
        return 0

    elif args.command == "stats":
        print(show_stats(repo))
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
