#!/usr/bin/env python3
"""
VBB Project Init
Bootstrap vibebackbone governance files in a target project.

Usage:
    python3 tools/vbb-project-init.py [OPTIONS]

Options:
    --target-dir DIR     Target project root (default: current directory)
    --project-name NAME  Project name used in CONTEXT.md (default: dir name)
    --mode DEV|PROD      Initial project mode (default: DEV)
    --overwrite          Overwrite project-owned documents (default: skip)
    --backup             Back up existing files before overwriting (.bak)
    --dry-run            Show what would be created/skipped without writing
    --install-hook       Install VBB pre-commit hook in target .git/hooks/
    --overwrite-hook     Replace existing generated Git hooks
    --overwrite-managed  Adopt/replace customized VBB-managed hook assets

Files created in the target project (if absent):
    docs/PROJECT_MODE.md
    docs/CONTEXT.md
    docs/AUDIT_STATUS.md
    docs/INDEX.md
    docs/runs/README.md        (copied from VBB distribution)
    docs/audits/README.md
    docs/adr/README.md
    docs/templates/*.md.template  (7 phase templates, copied from VBB)
    .gitignore                 (SESSION.md entries appended if absent)
    .vbb/managed-files.json  (created only with --install-hook)
    scripts/hooks/* and tools required by the canonical hook (VBB-managed)

Idempotent: existing files are reported as SKIP unless --overwrite is passed.
Non-destructive: --install-hook refuses existing Git hooks unless
--overwrite-hook is passed, and refuses customized managed assets unless
--overwrite-managed is passed. Project documents are never included in the
managed runtime bundle.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import List, Tuple

VBB_ROOT = Path(__file__).parent.parent.resolve()
TEMPLATES_SRC = VBB_ROOT / "docs" / "templates"
RUNS_README_SRC = VBB_ROOT / "docs" / "runs" / "README.md"
HOOK_INSTALLER_REL = "scripts/install-vbb-hooks.sh"
MANAGED_MANIFEST_REL = ".vbb/managed-files.json"
MANAGED_HOOK_BUNDLE = {
    "scripts/install-vbb-hooks.sh": "scripts/install-vbb-hooks.sh",
    "scripts/hooks/pre-commit-framework-gate": "scripts/hooks/pre-commit-framework-gate",
    "scripts/hooks/commit-msg-framework-gate": "scripts/hooks/commit-msg-framework-gate",
    "tools/vbb-credentials-gate.py": "tools/vbb-credentials-gate.py",
    "tools/vbb-loop-closure-check.py": "tools/vbb-loop-closure-check.py",
    "tools/vbb_run_resolution.py": "tools/vbb_run_resolution.py",
    "requirements.txt": ".vbb/requirements.txt",
}

GITIGNORE_ENTRIES = [
    "# VBB — local session state (not versioned)",
    "docs/SESSION.md",
    "docs/SESSION.*.md",
    "docs/local/",
    ".pi/",
]


# ---------------------------------------------------------------------------
# Content generators for governance files
# ---------------------------------------------------------------------------


def _project_mode_md(mode: str, today: str) -> str:
    return f"""\
---
context_role: project-mode
phase: transverse
status: active
updated: {today}
---

# Project Mode

**Mode actuel : {mode}**

## Transitions de mode

- `DEV` → `PROD` : passer par `t-vbb-mode-transition-gate` (produit un artefact d'audit).
- Toute modification suit la voie STRUCTUREE et produit un closeout dans `docs/runs/`.

## Référence

Ce fichier est lu en début de session par les skills `mode_sensitive`.
Sa modification doit être tracée dans `docs/AUDIT_STATUS.md`.
"""


def _context_md(project_name: str, today: str) -> str:
    return f"""\
---
context_role: moc
phase: transverse
status: active
updated: {today}
---

# {project_name}

> Routeur central du projet. Lire en premier à chaque session.

## Description

<Description courte du projet — à compléter>

## Stack principale

- <À compléter>

## Mode

Voir [PROJECT_MODE.md](PROJECT_MODE.md).

## Runs récents

Aucun run pour l'instant. Voir [docs/runs/](runs/).

## Liens clés

- [AUDIT_STATUS.md](AUDIT_STATUS.md) — tableau de bord audits
- [INDEX.md](INDEX.md) — carte de navigation
- [runs/](runs/) — artefacts de run vibebackbone
"""


def _audit_status_md(today: str) -> str:
    return f"""\
---
context_role: audit-status
phase: transverse
status: active
updated: {today}
---

# Audit Status

Aucun audit lancé.

Pour démarrer : `0-vbb-scope-freeze` puis `0-vbb-audit-readiness`.

## Verdict global

`NOT_RUN` — aucun audit formel lancé.

## Par skill

| Skill | Statut | Raison |
|-------|--------|--------|
| — | NOT_RUN | Projet fraîchement initialisé |

## Risks

Aucun risque tracé pour l'instant.
"""


def _index_md(project_name: str, today: str) -> str:
    return f"""\
---
context_role: index
phase: transverse
status: active
updated: {today}
---

# Index — {project_name}

## Gouvernance vibebackbone

- [CONTEXT.md](CONTEXT.md) — vue globale projet (MOC)
- [PROJECT_MODE.md](PROJECT_MODE.md) — mode DEV / PROD
- [AUDIT_STATUS.md](AUDIT_STATUS.md) — tableau de bord audits
- [ARCHITECTURE.md](ARCHITECTURE.md) — source canonique structurée de l'architecture
- [RELATIONS.md](RELATIONS.md) — projection générée depuis ARCHITECTURE.md

## Mémoire de session

- `SESSION.md` — local, gitignoré (machine courante)
- `SESSION.*.md` — variantes locales

## Artefacts versionnés

- [runs/](runs/) — artefacts de run (01_INTAKE → 07_CLOSEOUT)
- [audits/](audits/) — rapports d'audit horodatés
- [adr/](adr/) — Architecture Decision Records

## Templates

- [templates/](templates/) — modèles de phase (01_INTAKE … 07_CLOSEOUT)
"""


def _architecture_md(project_name: str, today: str) -> str:
    return f"""\
---
context_role: canonical-architecture
phase: transverse
status: draft
updated: {today}
---

# ARCHITECTURE — {project_name}

Source canonique structurée de l'architecture du projet.

Chaque bloc significatif doit être décrit avec une section `## Bloc: ...` et
une fence YAML contenant au minimum : `id`, `type`, `status`, `role`,
`responsibilities`, `depends_on`, `impacts`, `files`, `contracts`, `tests`,
`risks`.

Les vues graphiques et relations doivent être générées depuis ce fichier, pas
maintenues comme vérité parallèle.

## Bloc: Project Core

```yaml
id: project-core
type: governance
status: planned
role: Boundary placeholder for the initial project architecture.
responsibilities:
  - define project boundaries
depends_on: []
impacts:
  - project framing
files:
  - docs/ARCHITECTURE.md
  - docs/RELATIONS.md
contracts: []
tests: []
risks: []
```
"""


def _relations_md() -> str:
    return """\
---
context_role: architecture-relations
phase: transverse
status: generated
source: ARCHITECTURE.md
---

# RELATIONS — Architecture Projection

> Generated from `docs/ARCHITECTURE.md`. Do not edit this file as the source
> of truth.

Run the architecture projection tool from the vibebackbone distribution when
available:

```bash
python tools/vbb-architecture.py graph --write
```
"""


def _audits_readme_md() -> str:
    return """\
# docs/audits/

Rapports d'audit horodatés produits par les skills vibebackbone.

Format : `{skill}-{YYYYMMDD-HHMM}.md`

Ces fichiers sont versionnés (contrairement à `SESSION.md`).
"""


def _adr_readme_md() -> str:
    return """\
# docs/adr/

Architecture Decision Records.

Format : `{nnnn}-{slug}.md` (lowercase, zéro-paddé sur 4 chiffres)

Exemple : `0001-choix-framework-api.md`
"""


# ---------------------------------------------------------------------------
# .gitignore helper
# ---------------------------------------------------------------------------


def _update_gitignore(target_dir: Path, dry_run: bool) -> Tuple[str, bool]:
    """Append VBB SESSION.md entries to .gitignore if not already present.

    Returns (action_label, changed).
    """
    gi = target_dir / ".gitignore"
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""

    # Check if any of our entries are already present
    already_has_session = "docs/SESSION.md" in existing

    if already_has_session:
        return "SKIP (.gitignore: VBB entries already present)", False

    block = "\n" + "\n".join(GITIGNORE_ENTRIES) + "\n"
    if dry_run:
        return "CREATE/APPEND (.gitignore: add VBB SESSION.md entries)", True

    gi.write_text(existing + block, encoding="utf-8")
    return "APPEND (.gitignore: added VBB SESSION.md entries)", True


# ---------------------------------------------------------------------------
# Pre-commit hook helper
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    """Return a content hash without exposing file contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_managed_manifest(path: Path, force: bool) -> dict:
    if not path.exists():
        return {"schema_version": 1, "files": {}}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("schema_version") != 1 or not isinstance(
            manifest.get("files"), dict
        ):
            raise ValueError("unsupported schema")
        return manifest
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if force:
            return {"schema_version": 1, "files": {}}
        raise RuntimeError(
            f"invalid managed manifest {MANAGED_MANIFEST_REL}: {exc}"
        ) from exc


def _sync_managed_hook_bundle(target_dir: Path, force: bool, dry_run: bool) -> str:
    """Preflight then copy the VBB-owned hook runtime bundle."""
    manifest_path = target_dir / MANAGED_MANIFEST_REL
    manifest = _load_managed_manifest(manifest_path, force)
    recorded_files = manifest["files"]
    planned = []

    for source_rel, target_rel in MANAGED_HOOK_BUNDLE.items():
        source = VBB_ROOT / source_rel
        dest = target_dir / target_rel
        if not source.is_file():
            raise RuntimeError(f"managed source missing: {source_rel}")
        if dest.exists() and not force:
            recorded_hash = recorded_files.get(target_rel)
            if recorded_hash is None:
                raise RuntimeError(
                    f"unmanaged target exists: {target_rel}; "
                    "use --overwrite-managed to adopt it"
                )
            if _sha256(dest) != recorded_hash:
                raise RuntimeError(
                    f"managed target was customized: {target_rel}; "
                    "preserved (use --overwrite-managed to replace)"
                )
        planned.append((source, dest, target_rel))

    if dry_run:
        return f"DRY-RUN (would sync {len(planned)} managed hook assets)"

    # Preserve provenance for any asset retired from the current bundle. The
    # initializer does not delete consumer files implicitly.
    new_hashes = dict(recorded_files)
    for source, dest, target_rel in planned:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        new_hashes[target_rel] = _sha256(dest)

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_manifest = manifest_path.with_suffix(".json.tmp")
    temporary_manifest.write_text(
        json.dumps(
            {"schema_version": 1, "owner": "vibebackbone", "files": new_hashes},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary_manifest.replace(manifest_path)
    return f"DONE ({len(planned)} managed hook assets synced)"


def _install_hook(
    target_dir: Path,
    overwrite_hook: bool,
    overwrite_managed: bool,
    dry_run: bool,
) -> str:
    """Synchronize the managed bundle and run the canonical hook installer."""
    existing_hooks = [
        path
        for path in (
            target_dir / ".git" / "hooks" / "pre-commit",
            target_dir / ".git" / "hooks" / "commit-msg",
        )
        if path.exists()
    ]
    if existing_hooks and not overwrite_hook:
        names = ", ".join(path.name for path in existing_hooks)
        raise RuntimeError(
            f"existing Git hook(s): {names}; preserved "
            "(use --overwrite-hook to replace)"
        )

    bundle_label = _sync_managed_hook_bundle(target_dir, overwrite_managed, dry_run)
    if dry_run:
        return f"{bundle_label}; would run: bash {HOOK_INSTALLER_REL}"

    installer = target_dir / HOOK_INSTALLER_REL
    result = subprocess.run(
        ["bash", str(installer)],
        cwd=str(target_dir),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (
            result.stderr.strip()
            or result.stdout.strip()
            or f"exit {result.returncode}"
        )
        raise RuntimeError(f"canonical hook installer failed: {detail}")
    return "DONE (managed bundle synced; canonical hooks installed)"


# ---------------------------------------------------------------------------
# Main init logic
# ---------------------------------------------------------------------------


def init_project(
    target_dir: Path,
    project_name: str,
    mode: str,
    overwrite: bool,
    backup: bool,
    dry_run: bool,
    install_hook: bool,
    overwrite_hook: bool,
    overwrite_managed: bool,
) -> Tuple[List[str], List[str], List[str]]:
    """Bootstrap VBB governance files in target_dir.

    Returns (created, skipped, errors).
    """
    today = date.today().isoformat()
    created: List[str] = []
    skipped: List[str] = []
    errors: List[str] = []

    # --- Collect files to write ---
    files: dict[Path, str] = {
        target_dir / "docs" / "PROJECT_MODE.md": _project_mode_md(mode, today),
        target_dir / "docs" / "CONTEXT.md": _context_md(project_name, today),
        target_dir / "docs" / "AUDIT_STATUS.md": _audit_status_md(today),
        target_dir / "docs" / "ARCHITECTURE.md": _architecture_md(project_name, today),
        target_dir / "docs" / "RELATIONS.md": _relations_md(),
        target_dir / "docs" / "INDEX.md": _index_md(project_name, today),
        target_dir / "docs" / "audits" / "README.md": _audits_readme_md(),
        target_dir / "docs" / "adr" / "README.md": _adr_readme_md(),
    }

    # docs/runs/README.md — copy verbatim from VBB
    if RUNS_README_SRC.exists():
        files[target_dir / "docs" / "runs" / "README.md"] = RUNS_README_SRC.read_text(
            encoding="utf-8"
        )
    else:
        errors.append(f"Source not found: {RUNS_README_SRC}")

    # docs/templates/ — copy all 7 phase templates
    if TEMPLATES_SRC.exists():
        for tpl in sorted(TEMPLATES_SRC.glob("*.md.template")):
            files[target_dir / "docs" / "templates" / tpl.name] = tpl.read_text(
                encoding="utf-8"
            )
    else:
        errors.append(f"Templates directory not found: {TEMPLATES_SRC}")

    # --- Create directories ---
    if not dry_run:
        for d in [
            target_dir / "docs",
            target_dir / "docs" / "runs",
            target_dir / "docs" / "audits",
            target_dir / "docs" / "adr",
            target_dir / "docs" / "templates",
        ]:
            d.mkdir(parents=True, exist_ok=True)

    # --- Write files ---
    for path, content in files.items():
        rel = str(path.relative_to(target_dir))

        if path.exists() and not overwrite:
            skipped.append(rel)
            continue

        if dry_run:
            action = "OVERWRITE" if path.exists() else "CREATE"
            created.append(f"[{action}] {rel}")
            continue

        try:
            if path.exists() and backup:
                backup_path = path.with_suffix(path.suffix + ".bak")
                path.rename(backup_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created.append(rel)
        except OSError as exc:
            errors.append(f"Cannot write {rel}: {exc}")

    # --- .gitignore ---
    gi_label, _ = _update_gitignore(target_dir, dry_run)
    if dry_run or "SKIP" in gi_label:
        skipped.append(f".gitignore ({gi_label})")
    else:
        created.append(f".gitignore ({gi_label})")

    # --- Pre-commit hook (optional) ---
    if install_hook:
        try:
            hook_label = _install_hook(
                target_dir,
                overwrite_hook,
                overwrite_managed,
                dry_run,
            )
        except (OSError, RuntimeError) as exc:
            errors.append(f"Cannot install managed hooks: {exc}")
        else:
            if "SKIP" in hook_label:
                skipped.append(f"pre-commit hook: {hook_label}")
            else:
                created.append(f"pre-commit hook: {hook_label}")

    return created, skipped, errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap vibebackbone governance in a target project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--target-dir",
        metavar="DIR",
        default=".",
        help="Target project root (default: current directory)",
    )
    parser.add_argument(
        "--project-name",
        metavar="NAME",
        default=None,
        help="Project name for CONTEXT.md (default: target directory name)",
    )
    parser.add_argument(
        "--mode",
        choices=["DEV", "PROD"],
        default="DEV",
        help="Initial project mode (default: DEV)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files (default: skip)",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Back up existing files as .bak before overwriting",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created/skipped without writing anything",
    )
    parser.add_argument(
        "--install-hook",
        action="store_true",
        help="Install the VBB-managed canonical hooks (non-destructive)",
    )
    parser.add_argument(
        "--overwrite-hook",
        action="store_true",
        help="Replace existing generated Git hooks",
    )
    parser.add_argument(
        "--overwrite-managed",
        action="store_true",
        help="Adopt or replace customized VBB-managed hook assets",
    )
    args = parser.parse_args()

    target = Path(args.target_dir).resolve()
    if not target.exists():
        print(f"Error: target directory does not exist: {target}", file=sys.stderr)
        return 1

    project_name = args.project_name or target.name

    if args.dry_run:
        print(f"[dry-run] VBB Project Init — target: {target}")
        print(f"[dry-run] project-name: {project_name}  mode: {args.mode}")
        print()

    created, skipped, errors = init_project(
        target_dir=target,
        project_name=project_name,
        mode=args.mode,
        overwrite=args.overwrite,
        backup=args.backup,
        dry_run=args.dry_run,
        install_hook=args.install_hook,
        overwrite_hook=args.overwrite_hook,
        overwrite_managed=args.overwrite_managed,
    )

    prefix = "[dry-run] " if args.dry_run else ""

    if created:
        print(f"{prefix}Files created ({len(created)}):")
        for f in created:
            print(f"  ✓ {f}")

    if skipped:
        print(f"\n{prefix}Files skipped ({len(skipped)}) — already exist:")
        for f in skipped:
            print(f"  — {f}")

    if errors:
        print(f"\n{prefix}Errors ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)

    if not args.dry_run and not errors:
        print(f"\n✓ VBB governance bootstrapped in: {target}")
        print("  Next: fill in docs/CONTEXT.md with your project details.")
        if not args.install_hook:
            print(
                "  Tip : rerun this initializer with --install-hook to install "
                "the managed canonical hooks."
            )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
