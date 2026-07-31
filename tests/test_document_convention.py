"""Mechanical contract tests for vbb-doc-v1."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "tools/vbb-document-convention-lint.py"

def write_scope(tmp_path: Path, body: str | None = None) -> Path:
    body = body or VALID
    (tmp_path / ".vbb").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / ".vbb/document-convention.yaml").write_text(
        "document_convention: vbb-doc-v1\nversion: \"1.0\"\nadoption: adopted\nscope:\n  roots:\n    - docs\n",
        encoding="utf-8",
    )
    (tmp_path / "docs/document.md").write_text(body, encoding="utf-8")
    return tmp_path

def run(root: Path, *args):
    return subprocess.run([sys.executable, str(LINTER), str(root), *args], capture_output=True, text=True)

VALID = """---
document_convention: vbb-doc-v1
version: "1.0"
type: reference
status: active
visibility: public
tags: [documentation]
relations: []
---
# Document
"""

def test_valid_document_set_passes(tmp_path):
    assert run(write_scope(tmp_path, VALID)).returncode == 0

def test_invalid_metadata_taxonomies_and_version_fail(tmp_path):
    bad = VALID.replace('version: "1.0"', 'version: "2.0"').replace("tags: [documentation]", "tags: [unknown-tag]").replace("status: active", "status: ready")
    result = run(write_scope(tmp_path, bad))
    assert result.returncode != 0
    assert "incompatible version" in result.stdout
    assert "unknown tag" in result.stdout
    assert "invalid status" in result.stdout

def test_legacy_and_historical_inconsistencies_fail(tmp_path):
    root = write_scope(tmp_path, VALID)
    (root / "docs/OLD_TEMPLATE.md").write_text(VALID.replace("type: reference", "type: template"), encoding="utf-8")
    (root / "docs/active.md").write_text(VALID.replace("status: active", "status: historical"), encoding="utf-8")
    result = run(root)
    assert result.returncode != 0
    assert "legacy template used as current template" in result.stdout
    assert "active document classified as historical" in result.stdout

def test_missing_metadata_and_required_relation_fail(tmp_path):
    root = write_scope(tmp_path, "---\ndocument_convention: vbb-doc-v1\nversion: \"1.0\"\ntype: audit_report\nstatus: ready\nvisibility: public\ntags: [audit]\nrelations: []\n---\n")
    result = run(root)
    assert result.returncode != 0
    assert "audit report metadata incomplete" in result.stdout
    assert "required evidence relation missing" in result.stdout


def test_status_extension_and_waiver_are_explicit(tmp_path):
    root = write_scope(
        tmp_path,
        VALID.replace("status: active", "status: frozen\nstatus_extensions: [project:status:frozen-with-open-questions]"),
    )
    (root / "docs/waived.md").write_text("not migrated yet", encoding="utf-8")
    (root / ".vbb/document-convention.yaml").write_text(
        """document_convention: vbb-doc-v1
version: "1.0"
adoption: adopted
scope:
  roots: [docs]
waivers:
  - path: docs/waived.md
    reason: migration wave 2
    expires: "2026-09-30"
""",
        encoding="utf-8",
    )
    assert run(root).returncode == 0


def test_suggest_scope_is_non_blocking_and_actionable(tmp_path):
    root = write_scope(tmp_path)
    (root / ".vbb/document-convention.yaml").write_text(
        "document_convention: vbb-doc-v1\nversion: \"1.0\"\nadoption: adopted\nscope:\n  roots: [docs/document.md]\n",
        encoding="utf-8",
    )
    (root / "docs/unadopted.md").write_text(VALID, encoding="utf-8")
    result = run(root, "--suggest-scope")
    assert result.returncode == 0
    assert "docs/unadopted.md" in result.stdout
