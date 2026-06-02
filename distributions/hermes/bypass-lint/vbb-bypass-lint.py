#!/usr/bin/env python3
"""
vbb-bypass-lint v0.1 — Anti-bypass linter for the Vibebackbone confidentiality proxy.

Reference: ADR 0011 (docs/adr/0011-proxy-bypass-prevention.md) §3 "Règle 1 — Liste
close des outils sensibles" (10 categories of forbidden patterns).

Scope (default):
  - SOUL.md (if present at repo root)
  - tools/ (excluding tools/proxy/ and tools/vbb-bypass-lint*)
  - prompts/
  - skills/
  - scripts/
  - docs/ only with --docs (excluding docs/adr/)

Allowed paths (always exempt):
  - tools/proxy/  (proxy code itself, contains the reference list)
  - docs/adr/     (ADR reference docs)
  - tools/vbb-bypass-lint.py and tools/vbb-bypass-lint/  (this linter and its tests)

Mode:
  - report  (default): prints findings; exit 0 unless at least one CRITICAL
  - strict (--strict): exit non-zero on HIGH+CRITICAL
  - json (--json): machine-readable output
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable


# --------------------------------------------------------------------------- #
# Severity levels (ordered)
# --------------------------------------------------------------------------- #

SEVERITY_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}


# --------------------------------------------------------------------------- #
# Default configuration
# --------------------------------------------------------------------------- #

# Default allowed paths (always exempt from scanning).
# Each entry is matched as a prefix against the absolute, resolved file path.
DEFAULT_ALLOWED_PATHS = (
    "tools/proxy",
    "docs/adr",
    "tools/vbb-bypass-lint.py",
    "tools/vbb-bypass-lint",
    "tools/vbb-bypass-lint/tests",
)

# Default allowed file extensions. Files outside these extensions are skipped.
DEFAULT_ALLOWED_EXTENSIONS = (
    ".py", ".sh", ".md", ".yaml", ".yml", ".toml", ".json",
)

# Default directories / files to ignore at every scan (gitignore-equivalent).
DEFAULT_EXCLUDE_GLOBS = (
    ".git/",
    ".venv/",
    "venv/",
    "node_modules/",
    "dist/",
    "build/",
    "__pycache__/",
    ".pytest_cache/",
    ".vbb/",
    ".pi/",
    ".claude/",
    ".github/",
    "*.pyc",
    "*.pyo",
    "*.egg-info/",
)

# Default documentation markers — lines containing any of these tokens are
# treated as documentation / examples and skipped even if they match a
# forbidden pattern. Comparison is case-insensitive.
DEFAULT_DOCUMENTATION_MARKERS = (
    "interdit",
    "bypass",
    "do not",
    "don't",
    "ne pas",
    "forbidden",
    "exemple négatif",
    "anti-pattern",
    "test négatif",
    "noqa: bypass-doc",
    "DOC_CONTEXT",
    "WHITELIST",
    # Citations: lines that wrap a quote in French guillemets «...»
    # are documenting an existing pattern rather than running it.
    "«",
    "»",
    # ADR cross-references of the form NNNN:line-line.
    "0011:",
    "0010:",
    "0009:",
    "0007:",
    "0006:",
)

# Test-context markers — patterns adjacent to pytest markers.
TEST_CONTEXT_MARKERS = (
    "pytest.raises",
    "@pytest.fixture",
    "@pytest.mark",
    "expected violation",
    "test_negative",
)


# --------------------------------------------------------------------------- #
# Forbidden patterns extracted from ADR 0011 §3 Règle 1
# --------------------------------------------------------------------------- #

# Each pattern is (regex, severity, human message).
# Regex anchoring is intentionally context-aware ("ssh " or "ssh$", etc.)
# to avoid false positives like "ssh-style" or "github" containing "git".
DEFAULT_FORBIDDEN_PATTERNS = (
    # 1. ssh / scp / rsync (with target non-localhost) — CRITICAL
    (
        r"\b(?:ssh|scp|rsync)\s+[^\s]*@(?!localhost\b|127\.0\.0\.1\b|::1\b)",
        "CRITICAL",
        "Direct invocation of ssh/scp/rsync against a non-localhost target. "
        "Use tools/proxy/client.py with action 'nas_exec' instead.",
    ),
    (
        r"\b(?:ssh|scp|rsync)\s+-[A-Za-z0-9]*\s+(?!.*localhost)",
        "CRITICAL",
        "Direct invocation of ssh/scp/rsync with explicit flags. "
        "Use tools/proxy/client.py with action 'nas_exec' instead.",
    ),
    # 2. gh auth / gh auth login / gh repo clone / gh secret — CRITICAL
    (
        r"\bgh\s+auth\b",
        "CRITICAL",
        "Direct gh auth invocation. Use tools/proxy/client.py with a proxy_gh_* action.",
    ),
    (
        r"\bgh\s+auth\s+login\b",
        "CRITICAL",
        "Direct gh auth login. Use tools/proxy/client.py with action 'gh_login'.",
    ),
    (
        r"\bgh\s+repo\s+clone\b",
        "CRITICAL",
        "Direct gh repo clone. Use tools/proxy/client.py with action 'gh_repo_clone'.",
    ),
    (
        r"\bgh\s+secret\b",
        "CRITICAL",
        "Direct gh secret access. Use tools/proxy/client.py with action 'gh_secret'.",
    ),
    # 3. docker login / podman login / docker push to private registry — CRITICAL
    (
        r"\bdocker\s+login\b",
        "CRITICAL",
        "Direct docker login. Use tools/proxy/client.py with action 'docker_login'.",
    ),
    (
        r"\bpodman\s+login\b",
        "CRITICAL",
        "Direct podman login. Use tools/proxy/client.py with action 'podman_login'.",
    ),
    (
        r"\bdocker\s+push\s+[A-Za-z0-9._/-]+\.(?:ghcr\.io|registry\.internal|private)",
        "CRITICAL",
        "Docker push to a private registry. Use tools/proxy/client.py with action 'docker_push'.",
    ),
    # 4. cat .env / printenv / env | grep (SECRET/TOKEN/KEY/PASSWORD) — CRITICAL
    (
        r"\bcat\s+\.env\b",
        "CRITICAL",
        "Direct read of .env. Use tools/proxy/client.py with action 'env_read'.",
    ),
    (
        r"\bcat\s+[^\s|;&]*\b(?:SECRET|TOKEN|API_KEY|PASSWORD|PASSWD|PRIVATE_KEY|API_TOKEN)\b",
        "CRITICAL",
        "Direct read of a file containing a SECRET/TOKEN/KEY/PASSWORD. "
        "Use tools/proxy/client.py with action 'secret_read'.",
    ),
    (
        r"\bprintenv\s+(?:\$[\w]*|\b)(?:SECRET|TOKEN|API_KEY|PASSWORD|PASSWD|PRIVATE_KEY|API_TOKEN)\b",
        "CRITICAL",
        "Direct printenv of a SECRET/TOKEN/KEY/PASSWORD. "
        "Use tools/proxy/client.py with action 'secret_read'.",
    ),
    (
        r"\benv\s*\|\s*grep\s+(?:-[A-Za-z]+\s+)*(?:SECRET|TOKEN|API_KEY|PASSWORD|PASSWD|PRIVATE_KEY|API_TOKEN)",
        "CRITICAL",
        "env | grep of a SECRET/TOKEN/KEY/PASSWORD. "
        "Use tools/proxy/client.py with action 'secret_read'.",
    ),
    # 5. aws configure / gcloud auth / az login — CRITICAL
    (
        r"\baws\s+configure\b",
        "CRITICAL",
        "Direct aws configure. Use tools/proxy/client.py with action 'aws_configure'.",
    ),
    (
        r"\bgcloud\s+auth\b",
        "CRITICAL",
        "Direct gcloud auth. Use tools/proxy/client.py with action 'gcloud_auth'.",
    ),
    (
        r"\baz\s+login\b",
        "CRITICAL",
        "Direct az login. Use tools/proxy/client.py with action 'az_login'.",
    ),
    # 6. mysql / psql / redis-cli with credentials in CLI — HIGH
    (
        r"\bmysql\s+(?:-u|--user=)\s*[^\s]+\s+(?:-p|--password=)\s*\S+",
        "HIGH",
        "Direct mysql with credentials in CLI. Use tools/proxy/client.py with action 'mysql_query'.",
    ),
    (
        r"\bpsql\s+(?:-U|--username=)\s*[^\s]+\s+(?:-W|--password)\s*\S*",
        "HIGH",
        "Direct psql with credentials in CLI. Use tools/proxy/client.py with action 'psql_query'.",
    ),
    (
        r"\bredis-cli\s+(?:-a|--auth)\s+\S+",
        "HIGH",
        "Direct redis-cli with -a/--auth credential. Use tools/proxy/client.py with action 'redis_query'.",
    ),
    # 7. kubectl config / helm secrets — HIGH
    (
        r"\bkubectl\s+config\b",
        "HIGH",
        "Direct kubectl config. Use tools/proxy/client.py with action 'kubectl_config'.",
    ),
    (
        r"\bhelm\s+secrets\b",
        "HIGH",
        "Direct helm secrets. Use tools/proxy/client.py with action 'helm_secrets'.",
    ),
    # 8. vault read / vault write / pass show — CRITICAL
    (
        r"\bvault\s+read\b",
        "CRITICAL",
        "Direct vault read. Use tools/proxy/client.py with action 'vault_read'.",
    ),
    (
        r"\bvault\s+write\b",
        "CRITICAL",
        "Direct vault write. Use tools/proxy/client.py with action 'vault_write'.",
    ),
    (
        r"\bpass\s+show\b",
        "CRITICAL",
        "Direct pass show. Use tools/proxy/client.py with action 'pass_show'.",
    ),
    # 9. curl with Authorization header containing a secret — HIGH
    (
        r"\bcurl\b[^\n]*-H\s+[\"']?Authorization\s*:[^\"'\n]*(?:Bearer|Basic|Token)\s+[A-Za-z0-9._/+=-]{6,}",
        "HIGH",
        "curl with Authorization header carrying a secret. "
        "Use tools/proxy/client.py with the relevant action.",
    ),
    (
        r"\bcurl\b[^\n]*--header\s+[\"']?Authorization\s*:[^\"'\n]*(?:Bearer|Basic|Token)\s+[A-Za-z0-9._/+=-]{6,}",
        "HIGH",
        "curl --header with Authorization header carrying a secret. "
        "Use tools/proxy/client.py with the relevant action.",
    ),
    # 10. python -c "import os; os.environ[...]" — HIGH
    (
        r"\bpython\s+(?:-3\s+)?-c\s+[\"'].*\bimport\s+os\b.*\bos\.environ\b",
        "HIGH",
        "Direct python -c reading os.environ for a secret. "
        "Use tools/proxy/client.py with action 'secret_read'.",
    ),
    (
        r"\bpython3\s+(?:-3\s+)?-c\s+[\"'].*\bimport\s+os\b.*\bos\.environ\b",
        "HIGH",
        "Direct python3 -c reading os.environ for a secret. "
        "Use tools/proxy/client.py with action 'secret_read'.",
    ),
)


# --------------------------------------------------------------------------- #
# Configuration & dataclasses
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class LintConfig:
    """Static configuration for one lint run."""

    allowed_paths: tuple = DEFAULT_ALLOWED_PATHS
    forbidden_patterns: tuple = DEFAULT_FORBIDDEN_PATTERNS
    severity_threshold: str = "LOW"
    exclude_globs: tuple = DEFAULT_EXCLUDE_GLOBS
    documentation_markers: tuple = DEFAULT_DOCUMENTATION_MARKERS
    allowed_extensions: tuple = DEFAULT_ALLOWED_EXTENSIONS
    max_file_size: int = 1 * 1024 * 1024  # 1 MB
    include_docs: bool = False  # --docs
    include_all: bool = False    # --all (no path filtering)

    def is_allowed(self, file_path: Path, root: Path) -> bool:
        """Return True if file_path is in one of the allowed paths.

        Resolution strategy:
        1. Check if any contiguous window of the file's path components
           matches an allowed path (e.g. ('tools','proxy') is a window of
           ('var','...','tools','proxy','client.py')).
        2. Compare the file path relative to root against each allowed entry.
        3. Compare the file's path relative to cwd against each allowed entry.
        """
        try:
            abs_file = file_path.resolve()
        except OSError:
            abs_file = file_path

        file_parts = list(abs_file.parts)
        for allowed in self.allowed_paths:
            allowed_norm = allowed.replace(os.sep, "/").rstrip("/")
            if not allowed_norm:
                continue
            allowed_parts = tuple(allowed_norm.split("/"))
            n = len(allowed_parts)
            # Window match: look for allowed_parts in any contiguous slice
            # of file_parts.
            for i in range(len(file_parts) - n + 1):
                if tuple(file_parts[i:i + n]) == allowed_parts:
                    return True
            # Relative-to-root match.
            try:
                rel_root = (root if not root.is_absolute() else root.resolve())
                rel = abs_file.relative_to(rel_root)
            except (ValueError, OSError):
                rel = None
            if rel is not None:
                rel_str = str(rel).replace(os.sep, "/")
                if rel_str == allowed_norm or rel_str.startswith(allowed_norm + "/"):
                    return True
            # Relative-to-cwd match.
            try:
                rel_cwd = abs_file.relative_to(Path.cwd())
            except ValueError:
                rel_cwd = None
            if rel_cwd is not None:
                rel_cwd_str = str(rel_cwd).replace(os.sep, "/")
                if rel_cwd_str == allowed_norm or rel_cwd_str.startswith(allowed_norm + "/"):
                    return True
        return False

    def is_excluded(self, path: Path) -> bool:
        """Return True if path matches any exclude glob."""
        name = path.name
        rel = str(path)
        rel_posix = rel.replace(os.sep, "/")
        for pat in self.exclude_globs:
            pat_norm = pat.replace(os.sep, "/")
            if pat_norm.endswith("/"):
                if any(part == pat_norm.rstrip("/") for part in rel_posix.split("/")):
                    return True
                if fnmatch.fnmatch(rel_posix, "*/" + pat_norm + "*"):
                    return True
            else:
                if fnmatch.fnmatch(name, pat_norm) or fnmatch.fnmatch(rel_posix, pat_norm):
                    return True
                if fnmatch.fnmatch(rel_posix, "*/" + pat_norm):
                    return True
        return False

    def is_test_context(self, line: str) -> bool:
        """Return True if a line clearly belongs to a test/fixture context."""
        for marker in TEST_CONTEXT_MARKERS:
            if marker.lower() in line.lower():
                return True
        return False

    def is_documentation_line(self, line: str) -> bool:
        """Return True if the line contains a documentation marker."""
        lower = line.lower()
        for marker in self.documentation_markers:
            if marker.lower() in lower:
                return True
        return False


@dataclass
class LintFinding:
    file: str
    line: int
    column: int
    pattern: str
    severity: str
    message: str
    suggestion: str = "Use tools/proxy/client.py with the appropriate proxy_* action."

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LintReport:
    findings: list = field(default_factory=list)
    errors: list = field(default_factory=list)  # IO / parse errors
    stats: dict = field(default_factory=dict)
    has_critical: bool = False
    exit_code: int = 0
    strict: bool = False

    def add(self, finding: LintFinding) -> None:
        self.findings.append(finding)
        if finding.severity == "CRITICAL":
            self.has_critical = True

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def finalize(self) -> None:
        """Compute stats and exit code from findings."""
        by_sev = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for f in self.findings:
            by_sev[f.severity] = by_sev.get(f.severity, 0) + 1
        self.stats = {
            "files_scanned": self.stats.get("files_scanned", 0),
            "findings_total": len(self.findings),
            "by_severity": by_sev,
            "errors_total": len(self.errors),
        }
        if self.strict:
            if any(f.severity in ("HIGH", "CRITICAL") for f in self.findings):
                self.exit_code = 1
        else:
            # report mode (default): only CRITICAL blocks
            if self.has_critical:
                self.exit_code = 1

    def to_dict(self) -> dict:
        return {
            "findings": [f.to_dict() for f in self.findings],
            "errors": list(self.errors),
            "stats": dict(self.stats),
            "has_critical": self.has_critical,
            "exit_code": self.exit_code,
        }


# --------------------------------------------------------------------------- #
# Core scanning logic
# --------------------------------------------------------------------------- #

# Heuristic: lines that look like a shell command (start with $ or #! or
# follow a prompt) are command contexts. Comment-only lines that mention
# "ssh" in prose are not necessarily command contexts.
_SHELL_PROMPT_RE = re.compile(r"^\s*[\$>]\s+")
_SHEBANG_RE = re.compile(r"^\s*#!")


def _is_binary_sample(sample: bytes) -> bool:
    """Heuristic binary detection on a small byte sample."""
    if not sample:
        return False
    # NUL byte => very likely binary
    if b"\x00" in sample:
        return True
    # Heuristic: high ratio of non-text bytes
    text_chars = bytes(range(32, 127)) + b"\n\r\t\f\b"
    non_text = sum(1 for b in sample if b not in text_chars)
    return (non_text / len(sample)) > 0.30


def _is_command_context(line: str, prev_line: str | None) -> bool:
    """Return True if the line looks like a command invocation context."""
    if _SHELL_PROMPT_RE.match(line):
        return True
    if _SHEBANG_RE.match(line):
        return False
    # In a fenced code block in markdown, every line is command context.
    if prev_line is not None and prev_line.strip().startswith("```"):
        return True
    # Inline backticks containing the matched command are command context.
    if "`" in line and any(kw in line for kw in ("ssh", "gh ", "docker ", "kubectl", "vault ", "pass ", "curl ", "mysql", "psql", "redis-cli", "helm ", "aws ", "gcloud ", "az ")):
        return True
    return False


def _scan_file(
    file_path: Path,
    root: Path,
    config: LintConfig,
    report: LintReport,
) -> None:
    """Scan a single file and append findings to the report."""
    try:
        # Skip files beyond the size limit (security: do not slurp large files).
        size = file_path.stat().st_size
        if size > config.max_file_size:
            report.add_error(
                f"skipped (size {size} > {config.max_file_size}): {file_path}"
            )
            return

        with file_path.open("rb") as fh:
            sample = fh.read(min(8192, size))
            if _is_binary_sample(sample):
                return  # binary file: silently skip
            fh.seek(0)
            raw = fh.read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = raw.decode("latin-1")
            except Exception:
                report.add_error(f"undecodable: {file_path}")
                return
    except OSError as exc:
        report.add_error(f"unreadable ({exc}): {file_path}")
        return

    # File-level scope checks.
    if config.is_allowed(file_path, root):
        return  # exempt
    if file_path.suffix.lower() not in config.allowed_extensions:
        return

    # Decide whether this is a test file. A file is "test context" if its
    # name matches the conventional test naming, or if it contains
    # test markers anywhere. In test files, we apply multi-line test
    # context awareness: a line within the body of a function whose
    # decorator or signature is test-related is exempt.
    name_lower = file_path.name.lower()
    is_test_file = (
        name_lower.startswith("test_")
        or name_lower.endswith("_test.py")
        or "/tests/" in str(file_path).replace(os.sep, "/")
        or "tests" in file_path.parts
    )

    # Track fenced-code-block state for .md files.
    in_fence = False
    # Test-context state: line index of the last @pytest.fixture or pytest.raises
    # Lines within TEST_CONTEXT_WINDOW after that marker are exempt.
    TEST_CONTEXT_WINDOW = 50
    last_test_marker_line = -TEST_CONTEXT_WINDOW * 2
    prev = ""
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence

        # Update test-marker state before per-line checks.
        if is_test_file and config.is_test_context(line):
            last_test_marker_line = lineno

        # Documentation marker — skip.
        if config.is_documentation_line(line):
            prev = line
            continue

        # Test context window — skip.
        if is_test_file and (lineno - last_test_marker_line) <= TEST_CONTEXT_WINDOW:
            prev = line
            continue

        # Only flag in command contexts (shell prompt, fenced block, inline backticks)
        # for prose .md files. .py/.sh files assume command-like per line.
        is_md = file_path.suffix.lower() == ".md"
        if is_md and not in_fence and not _is_command_context(line, prev):
            prev = line
            continue

        # Run every forbidden pattern against the line.
        for pattern, severity, message in config.forbidden_patterns:
            match = re.search(pattern, line)
            if not match:
                continue
            # Sanitize excerpt (cap to 200 chars, no trailing whitespace noise)
            excerpt = line.strip()[:200]
            # File path is reported as relative-to-root when possible
            # (so the output is short and CI-friendly); otherwise we
            # fall back to the absolute path. This is what protects
            # the linter from crashing on files outside the repo
            # (e.g. /tmp/...), which was a real bug fixed in V3.
            try:
                rel_path = file_path.relative_to(root)
            except ValueError:
                rel_path = file_path
            finding = LintFinding(
                file=str(rel_path) if file_path.is_absolute() else str(file_path),
                line=lineno,
                column=(match.start() + 1),
                pattern=pattern,
                severity=severity,
                message=message,
                suggestion="Use tools/proxy/client.py with the appropriate proxy_* action.",
            )
            # We attach the excerpt separately (not in the dataclass to keep it pure);
            # we render it on output instead.
            finding._excerpt = excerpt  # type: ignore[attr-defined]
            report.add(finding)
        prev = line


def _resolve_targets(
    targets: list[Path],
    config: LintConfig,
) -> Iterable[Path]:
    """Resolve input paths into a deduplicated stream of files to scan."""
    seen: set = set()
    for target in targets:
        if not target.exists():
            continue
        if target.is_file():
            if target.resolve() in seen:
                continue
            if config.is_excluded(target):
                continue
            seen.add(target.resolve())
            yield target
            continue
        # directory walk
        for path in sorted(target.rglob("*")):
            if not path.is_file():
                continue
            if path.resolve() in seen:
                continue
            if config.is_excluded(path):
                continue
            seen.add(path.resolve())
            yield path


def lint_paths(paths: list[Path], config: LintConfig | None = None) -> LintReport:
    """Public API: scan the given paths and return a LintReport."""
    cfg = config or LintConfig()
    report = LintReport()

    # Determine the common root for relative paths.
    # Strategy: if any input is a directory, use it as the root. Otherwise, use
    # the first input file's parent. If multiple roots are mixed, use the
    # longest common parent.
    roots: list[Path] = []
    for p in paths:
        try:
            roots.append(p.resolve())
        except OSError:
            pass
    if not roots:
        report.stats["files_scanned"] = 0
        report.finalize()
        return report
    if len(roots) == 1:
        root = roots[0] if roots[0].is_dir() else roots[0].parent
    else:
        # Find longest common parent (Path.parents is a property, use commonpath)
        try:
            common = Path(os.path.commonpath([str(r) for r in roots]))
            root = common
        except (ValueError, OSError):
            root = roots[0] if roots[0].is_dir() else roots[0].parent

    files_to_scan: list[Path] = []
    for f in _resolve_targets(paths, cfg):
        files_to_scan.append(f)

    report.stats["files_scanned"] = len(files_to_scan)
    for file_path in files_to_scan:
        _scan_file(file_path, root, cfg, report)
    report.finalize()
    return report


# --------------------------------------------------------------------------- #
# Default target computation
# --------------------------------------------------------------------------- #

def default_targets(repo_root: Path) -> list[Path]:
    """Return the default set of paths to scan (report mode)."""
    targets: list[Path] = []
    soul = repo_root / "SOUL.md"
    if soul.exists():
        targets.append(soul)
    for sub in ("tools", "prompts", "skills", "scripts"):
        p = repo_root / sub
        if p.exists():
            targets.append(p)
    return targets


def all_targets(repo_root: Path) -> list[Path]:
    """Return the entire repository (--all)."""
    return [repo_root]


def docs_targets(repo_root: Path) -> list[Path]:
    """Return docs/ (excluding docs/adr/)."""
    docs = repo_root / "docs"
    if not docs.exists():
        return []
    return [docs]


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _format_text_report(report: LintReport) -> str:
    """Human-readable report (default)."""
    lines = []
    lines.append(f"vbb-bypass-lint v0.1 — scanning {report.stats.get('files_scanned', 0)} files")
    if not report.findings:
        lines.append("No findings.")
    else:
        for f in report.findings:
            excerpt = getattr(f, "_excerpt", "")
            lines.append("")
            lines.append(f"[{f.severity}] {f.file}:{f.line}:{f.column} — pattern: {f.pattern}")
            lines.append(f"  Message: {f.message}")
            lines.append(f"  Suggestion: {f.suggestion}")
            if excerpt:
                lines.append(f"  Excerpt: {excerpt}")
    if report.errors:
        lines.append("")
        lines.append("Errors encountered during scan:")
        for err in report.errors:
            lines.append(f"  - {err}")
    sev = report.stats.get("by_severity", {})
    lines.append("")
    lines.append(
        f"Summary: {sev.get('CRITICAL', 0)} critical, {sev.get('HIGH', 0)} high, "
        f"{sev.get('MEDIUM', 0)} medium, {sev.get('LOW', 0)} low"
    )
    lines.append(f"Exit code: {report.exit_code}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vbb-bypass-lint",
        description="Anti-bypass linter for the Vibebackbone confidentiality proxy "
                    "(ADR 0011 §3 Règle 1).",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Paths to scan (files or directories). If omitted, default "
             "targets are used: SOUL.md, tools/, prompts/, skills/, scripts/ "
             "(tools/proxy/ and tools/vbb-bypass-lint* always exempt).",
    )
    parser.add_argument(
        "--severity-threshold",
        choices=("LOW", "MEDIUM", "HIGH", "CRITICAL"),
        default="LOW",
        help="Minimum severity to surface (default: LOW).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON output.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress human-readable output; rely on exit code only.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Additional exclude glob (can be passed multiple times).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: exit non-zero on HIGH+CRITICAL (default is "
             "report mode, which only blocks on CRITICAL).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan the entire repository (no path filtering).",
    )
    parser.add_argument(
        "--docs",
        action="store_true",
        help="Include docs/ in the scan (excluding docs/adr/).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root for path resolution (default: current directory).",
    )

    args = parser.parse_args(argv)

    root: Path = args.root.resolve()
    if args.all:
        targets = [root]
    elif args.paths:
        targets = [p if p.is_absolute() else (root / p) for p in args.paths]
    else:
        targets = default_targets(root)
        if args.docs:
            targets.extend(docs_targets(root))

    # Build config: merge exclude globs.
    exclude_globs = list(DEFAULT_EXCLUDE_GLOBS) + list(args.exclude)
    config = LintConfig(
        allowed_paths=DEFAULT_ALLOWED_PATHS,
        forbidden_patterns=DEFAULT_FORBIDDEN_PATTERNS,
        severity_threshold=args.severity_threshold,
        exclude_globs=tuple(exclude_globs),
        documentation_markers=DEFAULT_DOCUMENTATION_MARKERS,
        allowed_extensions=DEFAULT_ALLOWED_EXTENSIONS,
        include_docs=args.docs,
        include_all=args.all,
    )

    report = lint_paths(targets, config=config)
    report.strict = bool(args.strict)
    report.finalize()  # re-finalize to honor --strict

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    elif not args.quiet:
        print(_format_text_report(report))

    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
