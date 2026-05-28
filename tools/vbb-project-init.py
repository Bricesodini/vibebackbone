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
    --overwrite          Overwrite existing files (default: skip)
    --backup             Back up existing files before overwriting (.bak)
    --dry-run            Show what would be created/skipped without writing
    --install-hook       Install VBB pre-commit hook in target .git/hooks/

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
    scripts/install-vbb-pre-commit.sh  (copied from VBB; --install-hook runs it)

Idempotent: existing files are reported as SKIP unless --overwrite is passed.
Non-destructive: --install-hook checks for existing .git/hooks/pre-commit
before installing; aborts if one already exists unless --overwrite is passed.
"""

import sys
import argparse
import shutil
from datetime import date
from pathlib import Path
from typing import List, Tuple

VBB_ROOT = Path(__file__).parent.parent.resolve()
TEMPLATES_SRC = VBB_ROOT / "docs" / "templates"
RUNS_README_SRC = VBB_ROOT / "docs" / "runs" / "README.md"
HOOK_SCRIPT_SRC = VBB_ROOT / "scripts" / "install-vbb-pre-commit.sh"

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

def _install_hook(target_dir: Path, overwrite: bool, dry_run: bool) -> str:
    """Copy install-vbb-pre-commit.sh and optionally run it.

    Returns action label.
    """
    import subprocess

    # Copy the script
    dest_scripts = target_dir / "scripts"
    hook_dest = dest_scripts / "install-vbb-pre-commit.sh"

    if not HOOK_SCRIPT_SRC.exists():
        return "SKIP (scripts/install-vbb-pre-commit.sh not found in VBB distribution)"

    if not dry_run:
        dest_scripts.mkdir(parents=True, exist_ok=True)
        if not hook_dest.exists() or overwrite:
            shutil.copy2(HOOK_SCRIPT_SRC, hook_dest)
            hook_dest.chmod(0o755)

    # Check existing hook
    git_hook = target_dir / ".git" / "hooks" / "pre-commit"
    if git_hook.exists() and not overwrite:
        return (
            "SKIP (install-hook: .git/hooks/pre-commit already exists; "
            "run with --overwrite to replace)"
        )

    if dry_run:
        return "DRY-RUN (would run: bash scripts/install-vbb-pre-commit.sh)"

    try:
        result = subprocess.run(
            ["bash", str(hook_dest)],
            cwd=str(target_dir),
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return f"DONE (pre-commit hook installed)"
        else:
            return f"ERROR installing hook: {result.stderr.strip()}"
    except Exception as exc:
        return f"ERROR: {exc}"


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
        files[target_dir / "docs" / "runs" / "README.md"] = RUNS_README_SRC.read_text(encoding="utf-8")
    else:
        errors.append(f"Source not found: {RUNS_README_SRC}")

    # docs/templates/ — copy all 7 phase templates
    if TEMPLATES_SRC.exists():
        for tpl in sorted(TEMPLATES_SRC.glob("*.md.template")):
            files[target_dir / "docs" / "templates" / tpl.name] = tpl.read_text(encoding="utf-8")
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
        hook_label = _install_hook(target_dir, overwrite, dry_run)
        if "SKIP" in hook_label or "ERROR" in hook_label:
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
        help="Install VBB pre-commit hook in .git/hooks/ (non-destructive)",
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
        print(f"  Next: fill in docs/CONTEXT.md with your project details.")
        if not args.install_hook:
            print(
                f"  Tip : install the pre-commit hook with:\n"
                f"        bash scripts/install-vbb-pre-commit.sh"
            )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
