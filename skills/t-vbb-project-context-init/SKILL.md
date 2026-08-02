---
name: t-vbb-project-context-init
description: |
  Bootstraps vibebackbone governance in a target project that has none.
  Creates docs/{PROJECT_MODE,CONTEXT,AUDIT_STATUS,INDEX}.md, docs/runs/,
  docs/audits/, docs/adr/, docs/templates/ (7 phase templates) and updates
  .gitignore. Optionally installs a VBB-managed canonical hook bundle with
  provenance checks. Project-owned documents are generated once by default.
version: "1.1"
phase: transverse
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Project Context Init

Standard reference: `0-vbb-standard`

## ROLE & POSTURE

You are a vibebackbone governance bootstrapper.

Your role is to prepare an existing project to operate under VBB:
create missing governance files, configure `.gitignore`,
copy phase templates.

You do NOT modify project code.
You do NOT delete existing files.
You do NOT force overwrite without explicit confirmation.

Absolute rules:

- Idempotent: skip if file already exists (unless explicit `--overwrite`).
- Non-destructive: `--overwrite` applies only to project-owned documents.
- Existing Git hooks require `--overwrite-hook`; customized managed assets
  require the separate `--overwrite-managed` flag.
- Evidence required: clearly report files created, skipped, or in error.
- Negotiate the documentary contract through the C0-C5 validator before
  claiming conformity. Never infer authority from a path, date or filename.
- A missing contract is `UNKNOWN`; an old compatible contract is reported
  explicitly; a migration-required contract becomes a finding and awaits
  `OUI`, `NON` or `PLUS_TARD`.
- A fresh initialization declares a target contract only; it does not claim
  that existing artefacts already conform.

## INPUT CONTRACT

**Required:**

- [ ] Access to the target repo (current directory or explicit path)

**Optional:**

- [ ] Project name (to populate `docs/CONTEXT.md`)
- [ ] Initial mode (`DEV` or `PROD`, default: `DEV`)
- [ ] `--overwrite` flag to force rewriting existing files
- [ ] `--install-hook` to install the managed canonical hook bundle
- [ ] `--overwrite-hook` / `--overwrite-managed` only after explicit approval
- [ ] `--dry-run` flag to preview without writing

## BLOCKING CONDITIONS

- If `tools/vbb-project-init.py` cannot be found → STOP.
  Message: "The tool tools/vbb-project-init.py is missing. Check VBB installation."
- If the target directory does not exist → STOP. Ask for path confirmation.
- If the project is already fully on VBB rails (all files present) →
  signal that it is already initialized, offer `--overwrite` for update.

## SCOPE

### Included

- creation of `docs/PROJECT_MODE.md`
- creation of `docs/CONTEXT.md` (with project name)
- creation of `docs/AUDIT_STATUS.md` (skeleton)
- creation of `docs/INDEX.md`
- creation of `docs/runs/README.md` (copied from VBB)
- creation of `docs/audits/README.md`
- creation of `docs/adr/README.md`
- copy of `docs/templates/*.md.template` (7 phase templates)
- update of `.gitignore` (SESSION.md entries)
- optional managed bundle under `scripts/`, `tools/`, and `.vbb/`, followed by
  canonical pre-commit and commit-msg hook installation

### Excluded

- modifying project code
- modifying existing CI/CD configuration
- creating an initialization run in the target project
- deleting or replacing existing governance files without explicit flag

## PROCESS

1. Verify that `tools/vbb-project-init.py` is accessible.
2. Check whether the project is already on VBB rails:
   - `ls docs/PROJECT_MODE.md docs/CONTEXT.md docs/AUDIT_STATUS.md` → if all exist → PARTIAL (partial update possible).
3. Run the C0-C5 documentary-contract check in read-only mode. Record the
   observed contract version, identity/representation evidence, ontology,
   relations, compatibility and confidence. Keep missing or incomplete values
   `UNKNOWN`.
4. Run dry-run to preview:
   ```bash
   python3 tools/vbb-project-init.py --target-dir <path> --dry-run
   ```
5. Present the contract findings and the file summary to the user. Ask
   explicitly for `OUI`, `NON` or `PLUS_TARD`; no finding response writes an
   artefact by itself.
6. If user confirms and the route is authorized, run actual initialization:
   ```bash
   python3 tools/vbb-project-init.py \
     --target-dir <path> \
     --project-name "<Project Name>" \
     --mode DEV
   ```
7. Verify created files and report skips; do not claim existing-artefact
   conformity unless the validator evidence supports it.
8. Guide the user to complete `docs/CONTEXT.md`:
   - Project description
   - Main stack
   - Expected operating mode
9. Report that the canonical hooks can be installed from the VBB checkout:
   ```bash
   python3 tools/vbb-project-init.py --target-dir <path> --install-hook
   ```
   On refresh, never combine permissions implicitly: `--overwrite-hook` replaces
   generated Git hooks; `--overwrite-managed` adopts customized runtime assets.
10. Produce the `07_CLOSEOUT.md` of the initialization run.

## OUTPUT CONTRACT

### Primary artifact (phase artifact)

- **Path**: `docs/runs/{run_id}/07_CLOSEOUT.md`
- **Template**: [`docs/templates/07_CLOSEOUT.md.template`](../../docs/templates/07_CLOSEOUT.md.template)
- **Kind**: `phase_artifact`
- **Required frontmatter**: `run_id`, `phase=07_CLOSEOUT`, `route`, `status`, `agent`, `started_at`, `ended_at`, `artifacts_consumed`, `artifacts_produced`

### Secondary artifacts

- **`docs/PROJECT_MODE.md`** (`kind: persistent_state_update`) — created if absent.
- **`docs/CONTEXT.md`** (`kind: persistent_state_update`) — created if absent.
- **`docs/AUDIT_STATUS.md`** (`kind: persistent_state_update`) — created if absent.

### Expected output content

- list of files created
- list of files skipped (already existing)
- any errors
- next step: complete `docs/CONTEXT.md`

## VERDICT RULES

- `PASS`
  - at least core files created (`PROJECT_MODE.md`, `CONTEXT.md`, `AUDIT_STATUS.md`)
  - `.gitignore` updated
- `PARTIAL`
  - some files skipped (existing) but core OK
  - templates missing (VBB source not found) but base governance created
- `BLOCKED`
  - tool `vbb-project-init.py` not found
  - target directory inaccessible
  - system write errors
- `UNKNOWN`
  - project state indeterminable before execution
