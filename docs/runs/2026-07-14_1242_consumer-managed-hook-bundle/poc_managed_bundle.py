#!/usr/bin/env python3
"""Disposable POC for ADR 0034. Not product code."""

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUNDLE = {
    "scripts/install-vbb-hooks.sh": "scripts/install-vbb-hooks.sh",
    "scripts/hooks/pre-commit-framework-gate": "scripts/hooks/pre-commit-framework-gate",
    "scripts/hooks/commit-msg-framework-gate": "scripts/hooks/commit-msg-framework-gate",
    "tools/vbb-credentials-gate.py": "tools/vbb-credentials-gate.py",
    "tools/vbb-loop-closure-check.py": "tools/vbb-loop-closure-check.py",
    "tools/vbb_run_resolution.py": "tools/vbb_run_resolution.py",
    "requirements.txt": ".vbb/requirements.txt",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sync(source_root: Path, target: Path, force: bool = False) -> None:
    manifest_path = target / ".vbb/managed-files.json"
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"files": {}}
    planned = []
    for source_rel, target_rel in BUNDLE.items():
        source = source_root / source_rel
        dest = target / target_rel
        recorded = old["files"].get(target_rel)
        if dest.exists() and not force:
            if recorded is None or digest(dest) != recorded:
                raise RuntimeError(f"managed conflict: {target_rel}")
        planned.append((source, dest, target_rel))

    new_files = {}
    for source, dest, target_rel in planned:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        new_files[target_rel] = digest(dest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps({"schema_version": 1, "files": new_files}, sort_keys=True) + "\n")


def main() -> None:
    results = []
    with tempfile.TemporaryDirectory(prefix="vbb-managed-poc-") as tmp:
        target = Path(tmp) / "consumer"
        target.mkdir()
        subprocess.run(["git", "init", "-q", str(target)], check=True)
        docs = target / "docs/CONTEXT.md"
        docs.parent.mkdir()
        docs.write_text("PROJECT_TRUTH_SENTINEL\n")

        sync(ROOT, target)
        results.append(("fresh bundle + manifest", (target / ".vbb/managed-files.json").exists()))
        subprocess.run(["bash", "scripts/install-vbb-hooks.sh"], cwd=target, check=True, capture_output=True)
        results.append(("canonical hooks installed", (target / ".git/hooks/pre-commit").exists() and (target / ".git/hooks/commit-msg").exists()))

        before = (target / ".vbb/managed-files.json").read_text()
        sync(ROOT, target)
        results.append(("unchanged refresh idempotent", before == (target / ".vbb/managed-files.json").read_text()))

        custom = target / "scripts/hooks/pre-commit-framework-gate"
        custom.write_text(custom.read_text() + "\n# LOCAL_SENTINEL\n")
        untouched = target / "tools/vbb-credentials-gate.py"
        untouched_before = untouched.read_bytes()
        try:
            sync(ROOT, target)
            conflict = False
        except RuntimeError:
            conflict = True
        results.append(("customization blocks", conflict and "LOCAL_SENTINEL" in custom.read_text()))
        results.append(("conflict causes no partial copy", untouched.read_bytes() == untouched_before))
        results.append(("project truth preserved", docs.read_text() == "PROJECT_TRUTH_SENTINEL\n"))

    for label, passed in results:
        print(f"{'PASS' if passed else 'FAIL'} {label}")
    print(f"SCORE {sum(p for _, p in results)}/{len(results)}")
    raise SystemExit(0 if all(p for _, p in results) else 1)


if __name__ == "__main__":
    main()
