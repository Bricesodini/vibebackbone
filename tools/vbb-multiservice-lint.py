#!/usr/bin/env python3
"""
VBB Multiservice Linter — Phase 2 multi-service discipline (ADR-0009)

Validates multiservice discipline rules per project:
  1. DB isolation — if db_orientation: shared_external_*, forbid direct DB access
     to other services without going through a documented API.
  2. IMPACT_LOG freshness — if CONTRACTS_CONSUMED.md exists, verify IMPACT_LOG.md
     exists with at least one entry.
  3. CONTRACTS_CONSUMED freshness — verify Last updated < max_age_days.

Configuration: docs/MULTISERVICE_DISCIPLINE.yaml (per-project).

Modes:
  (default)       warnings only, exit 0
  --strict        warnings become errors, exit 2 if any violation
  --json          output machine-readable JSON

References:
  ADR-0009 (Gap-04): https://internal/docs/adr/0009-multiservice-lint-discipline.md
  ADR-0007 (Gap-05): CONTRACTS_CONSUMED schema (consumed by rule #3)
  ADR-0010 (Gap-06): IMPACT_LOG schema (consumed by rule #2)
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Repo-relative paths (mirror tools/vbb-contract-lint.py pattern)
REPO_ROOT = Path(__file__).parent.parent.resolve()
DOCS_DIR = REPO_ROOT / "docs"

# Per-project configuration file
DISCIPLINE_FILE = DOCS_DIR / "MULTISERVICE_DISCIPLINE.yaml"

# Artifacts consumed
CONTRACTS_CONSUMED_FILE = DOCS_DIR / "CONTRACTS_CONSUMED.md"
IMPACT_LOG_FILE = DOCS_DIR / "IMPACT_LOG.md"
CONTEXT_FILE = DOCS_DIR / "CONTEXT.md"

# Default config (overridable by per-project file)
DEFAULT_CONFIG: Dict = {
    "schema_version": "1.0",
    "rules": {
        "db_isolation": {"enabled": True, "severity": "warning"},
        "impact_log_required": {"enabled": True, "severity": "warning"},
        "contracts_consumed_freshness": {
            "enabled": True,
            "severity": "warning",
            "max_age_days": 90,
        },
    },
    "allowlist": {"db_isolation": []},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VBB Multiservice Linter — discipline rules for multi-service projects"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Treat violations as errors (exit 2)"
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output JSON"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DISCIPLINE_FILE,
        help="Path to discipline config (default: docs/MULTISERVICE_DISCIPLINE.yaml)",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> Optional[Dict]:
    """Load YAML without external dependency: try PyYAML, fallback to minimal parser."""
    try:
        import yaml  # type: ignore

        with path.open() as f:
            return yaml.safe_load(f)
    except ImportError:
        # PyYAML not available — for now, no-project mode
        return None
    except Exception:
        return None


def load_config(path: Path) -> Dict:
    """Load per-project config, falling back to defaults."""
    if not path.exists():
        return dict(DEFAULT_CONFIG)
    loaded = load_yaml(path)
    if not isinstance(loaded, dict):
        return dict(DEFAULT_CONFIG)
    # Merge: defaults < per-project
    merged = dict(DEFAULT_CONFIG)
    merged_rules = dict(DEFAULT_CONFIG["rules"])
    if "rules" in loaded:
        for k, v in loaded["rules"].items():
            merged_rules[k] = {**merged_rules.get(k, {}), **v}
    merged["rules"] = merged_rules
    if "allowlist" in loaded:
        merged["allowlist"] = loaded["allowlist"]
    return merged


def get_db_orientation(context_path: Path) -> Optional[str]:
    """Extract db_orientation from CONTEXT.md if declared."""
    if not context_path.exists():
        return None
    try:
        content = context_path.read_text(encoding="utf-8")
    except Exception:
        return None
    # Frontmatter YAML (between --- markers)
    if not content.startswith("---\n"):
        return None
    end = content.find("\n---\n", 4)
    if end == -1:
        return None
    fm = content[4:end]
    m = re.search(r"^db_orientation:\s*(\S+)", fm, re.MULTILINE)
    if m:
        return m.group(1).strip().strip("\"'")
    return None


def rule_db_isolation(
    config: Dict, context_path: Path = CONTEXT_FILE
) -> List[Dict]:
    """If db_orientation: shared_external_*, warn about direct DB cross-access."""
    rule_cfg = config["rules"].get("db_isolation", {})
    if not rule_cfg.get("enabled", False):
        return []
    violations = []
    db_orientation = get_db_orientation(context_path)
    if db_orientation and "shared_external" in db_orientation:
        # Heuristic: search imports for client DB packages of other services
        # (out of scope for first version — placeholder for future POC)
        # The check requires a list of "allowed patterns" + "forbidden client packages"
        # which would be project-specific. For now, we surface a hint, not a violation.
        violations.append(
            {
                "rule": "db_isolation",
                "severity": rule_cfg.get("severity", "warning"),
                "message": (
                    f"db_orientation={db_orientation} declared. "
                    "Verify no direct DB client imports of other services "
                    "(manual review or extend this linter with project-specific allowlist)."
                ),
                "evidence": f"context.md declares db_orientation={db_orientation}",
            }
        )
    return violations


def rule_impact_log_required(config: Dict) -> List[Dict]:
    """If CONTRACTS_CONSUMED.md exists, require IMPACT_LOG.md with >= 1 entry."""
    rule_cfg = config["rules"].get("impact_log_required", {})
    if not rule_cfg.get("enabled", False):
        return []
    violations = []
    if not CONTRACTS_CONSUMED_FILE.exists():
        return violations  # No consumed contracts → rule N/A

    if not IMPACT_LOG_FILE.exists():
        violations.append(
            {
                "rule": "impact_log_required",
                "severity": rule_cfg.get("severity", "warning"),
                "message": (
                    "CONTRACTS_CONSUMED.md exists but IMPACT_LOG.md is missing. "
                    "Per ADR-0010, every consumed contract change should be logged."
                ),
                "evidence": "IMPACT_LOG.md not found",
            }
        )
        return violations

    # Count table rows (rough heuristic — first column count after header separator)
    try:
        content = IMPACT_LOG_FILE.read_text(encoding="utf-8")
        # Count `| YYYY-MM-DD |` style entries
        entries = re.findall(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|", content, re.MULTILINE)
        if len(entries) == 0:
            violations.append(
                {
                    "rule": "impact_log_required",
                    "severity": rule_cfg.get("severity", "warning"),
                    "message": "IMPACT_LOG.md exists but has 0 entries.",
                    "evidence": f"IMPACT_LOG.md has 0 dated entries",
                }
            )
    except Exception as e:
        violations.append(
            {
                "rule": "impact_log_required",
                "severity": "warning",
                "message": f"Failed to read IMPACT_LOG.md: {e}",
                "evidence": str(e),
            }
        )
    return violations


def rule_contracts_consumed_freshness(config: Dict) -> List[Dict]:
    """If CONTRACTS_CONSUMED.md exists, verify Last updated < max_age_days."""
    rule_cfg = config["rules"].get("contracts_consumed_freshness", {})
    if not rule_cfg.get("enabled", False):
        return []
    if not CONTRACTS_CONSUMED_FILE.exists():
        return []
    max_age = rule_cfg.get("max_age_days", 90)
    violations = []
    try:
        content = CONTRACTS_CONSUMED_FILE.read_text(encoding="utf-8")
    except Exception as e:
        violations.append(
            {
                "rule": "contracts_consumed_freshness",
                "severity": "warning",
                "message": f"Failed to read CONTRACTS_CONSUMED.md: {e}",
                "evidence": str(e),
            }
        )
        return violations

    # Find "Last updated" line (case-insensitive)
    m = re.search(r"Last\s+updated\s*[:=]\s*(\d{4}-\d{2}-\d{2})", content, re.IGNORECASE)
    if not m:
        violations.append(
            {
                "rule": "contracts_consumed_freshness",
                "severity": rule_cfg.get("severity", "warning"),
                "message": (
                    "CONTRACTS_CONSUMED.md has no 'Last updated' field. "
                    f"Add one (format YYYY-MM-DD), then re-run."
                ),
                "evidence": "No 'Last updated' field found",
            }
        )
        return violations

    try:
        last_updated = datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        violations.append(
            {
                "rule": "contracts_consumed_freshness",
                "severity": rule_cfg.get("severity", "warning"),
                "message": f"Last updated date '{m.group(1)}' is malformed.",
                "evidence": m.group(1),
            }
        )
        return violations

    age = (datetime.now().date() - last_updated).days
    if age > max_age:
        violations.append(
            {
                "rule": "contracts_consumed_freshness",
                "severity": rule_cfg.get("severity", "warning"),
                "message": (
                    f"CONTRACTS_CONSUMED.md last updated {age} days ago "
                    f"(threshold: {max_age} days). Refresh consumed contracts."
                ),
                "evidence": f"Last updated: {m.group(1)} ({age} days ago)",
            }
        )
    return violations


def lint(config: Dict) -> Tuple[List[Dict], List[Dict]]:
    """Run all enabled rules. Returns (errors, warnings)."""
    errors: List[Dict] = []
    warnings: List[Dict] = []
    for v in rule_db_isolation(config):
        (errors if v["severity"] == "error" else warnings).append(v)
    for v in rule_impact_log_required(config):
        (errors if v["severity"] == "error" else warnings).append(v)
    for v in rule_contracts_consumed_freshness(config):
        (errors if v["severity"] == "error" else warnings).append(v)
    return errors, warnings


def format_text(errors: List[Dict], warnings: List[Dict]) -> str:
    lines = [
        f"VBB Multiservice Linter — {len(errors)} error(s), {len(warnings)} warning(s) found"
    ]
    for e in errors:
        lines.append(f"  ✗ [{e['rule']}] {e['message']}")
        lines.append(f"      evidence: {e['evidence']}")
    for w in warnings:
        lines.append(f"  ⚠️  [{w['rule']}] {w['message']}")
        lines.append(f"      evidence: {w['evidence']}")
    if not errors and not warnings:
        lines.append("  ✓ No violations")
    return "\n".join(lines)


def format_json(errors: List[Dict], warnings: List[Dict]) -> str:
    return json.dumps(
        {
            "tool": "vbb-multiservice-lint",
            "version": "0.1.0",
            "errors": errors,
            "warnings": warnings,
            "summary": {
                "errors_count": len(errors),
                "warnings_count": len(warnings),
            },
        },
        indent=2,
    )


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    errors, warnings = lint(config)

    # In strict mode, warnings become errors
    if args.strict:
        errors = errors + warnings
        warnings = []

    output = format_json(errors, warnings) if args.json_output else format_text(errors, warnings)
    print(output)

    if errors:
        return 2  # GATE_BLOCKED
    return 0


if __name__ == "__main__":
    sys.exit(main())