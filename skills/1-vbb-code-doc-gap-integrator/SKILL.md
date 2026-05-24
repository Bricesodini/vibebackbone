---
name: 1-vbb-code-doc-gap-integrator
description: |
  Scans repository code to identify documentable units, cross-references against
  existing documentation, and writes missing feature documentation to close the gaps.
  Produces a gap report and creates or updates doc files. This is a builder skill —
  it writes documentation that does not yet exist. Never modifies code.
  Supports two modes: COMPLETE (single agent does all steps) and DELEGATED
  (cloud scouts and prepares, local fills templates per gap).
version: "2.0"
phase: 1
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Code-Doc Gap Integrator

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a documentation builder.

Your role is to detect what exists in the code but is not documented,
then write the missing files to close the gaps.

You do NOT modify code.
You do NOT delete existing files.
You write ONLY missing or incomplete documentation files.
You do NOT re-harmonize existing docs — that is the role of `1-vbb-doc-harmonizer`.

Absolute rules:

- No code changes
- No file deletions
- No doc↔doc harmonization (out of scope)
- UNKNOWN allowed
- Evidence required: each gap must point to a real file/directory in the code
- Prefer concrete doc over abstract doc

## INPUT CONTRACT

**Required:**

- [ ] Repo access (source code + existing documentation)

**Optional:**

- [ ] `docs/PILOTAGE.md`
- [ ] `docs/INDEX.md`
- [ ] `docs/ARCHITECTURE.md`
- [ ] Target scope (module, directory, feature) — if absent, scope = entire repo
- [ ] Write threshold: `HIGH` or `HIGH+MEDIUM` — default: `HIGH+MEDIUM`
- [ ] Known gaps (hints provided by the user)
- [ ] Doc file naming convention (if known)

**Accepted sources:** local repo, code files, existing documentation

## USER QUESTIONS

Before starting the scan, ask the user the following questions.
All are optional — if the user doesn't answer, use defaults.

| Question | Purpose | Default if absent |
|----------|---------|-------------------|
| **What scope do you want to cover?** (module, directory, feature, or entire repo) | Bound the scan and reduce context to process | Entire repo |
| **Are there modules or features you know are undocumented?** | Speed up detection and prioritize | No hints — full scan |
| **What write threshold?** (`HIGH` only or `HIGH+MEDIUM`) | Control the volume of files produced | `HIGH+MEDIUM` |

Do NOT ask more than 3 questions. Do NOT re-prompt if the user skips a question.
Use defaults silently.

## BLOCKING CONDITIONS

- If the repo is not accessible → STOP. Message: "Cannot scan an inaccessible repository."
- If the repo contains no source code files → STOP. Message: "No source code detected — nothing to document."
- If the repo is empty or nearly empty (fewer than 5 files) → STOP. Message: "Repository too embryonic for productive gap analysis."
- If the request is about doc↔doc harmonization → redirect to `1-vbb-doc-harmonizer`.

## SCOPE

### Repo zones

- Source code = all application sources (src/, app/, lib/, modules/, packages/, etc.)
- Config = configuration files affecting runtime (e.g. .env.example, docker-compose, config/)
- Existing docs = `docs/`, `README.md`, `.md` files at root

### Included

- scan of documentable units in code
- inventory of existing documentation
- code↔doc cross-referencing to identify gaps
- writing of missing files
- reporting orphaned files (doc without corresponding code)

### Excluded

- code/config modifications
- file deletions
- doc↔doc harmonization between existing files
- rewriting correct existing files
- technical debt audit (→ `1-vbb-tech-debt`)
- dependency mapping (→ `t-vbb-dependency-mapper`)

## EXECUTION MODES

This skill supports two execution modes, selected based on available models:

### COMPLETE mode — single agent

Used when a single agent is available, or when the model has sufficient
context to process the entire repo.

The agent executes the 4 steps sequentially (see PROCESS below).
The default template is applied directly at step 4.

### DELEGATED mode — cloud prepares, local executes

Used when a local model is available as a subagent.
The cloud model (orchestrator) executes steps 1-3 and prepares
micro-contexts. The local model executes step 4 per gap.

Distribution:

| Step | Responsible | Reason |
|-------|-------------|--------|
| 1 — Scan code | ☁️ Cloud | Requires broad visibility, judging what is documentable |
| 2 — Scan docs | ☁️ Cloud | Requires scanning all files |
| 3 — Cross-reference + diff | ☁️ Cloud | Requires severity judgment, comparison |
| 4 — Write files | 🖥️ Local | Focused work, template filling, reduced scope |

In DELEGATED mode, the cloud prepares a micro-context per gap (see MICRO-CONTEXT CONTRACT).
The local model receives each micro-context and produces a file.

## PROCESS

Execute strictly in order. Each step produces output that feeds the next.
Do not skip steps. Do not merge steps.

### Step 1 — Scan code

Scan the repo and identify **documentable units**.

If a target scope was provided, limit the scan to that scope.

A unit is documentable if it meets **at least one** of these conditions:

- It's an API endpoint or route (public or internal)
- It's a module with ≥ 3 public exports
- It's a directory dedicated to a functional feature (e.g. `src/auth/`, `src/billing/`)
- It's a configuration file affecting runtime behavior
- It's a type/interface/contract defining a public surface
- It's a utility script with documentable flags or options
- It's a reusable UI component

Do NOT include:

- Tests (unless test setup is a documentable procedure)
- Generated boilerplate (e.g. default scaffolding)
- Purely internal files with no public surface

For each unit, note:

| Field | Description |
|---|---|
| **Name** | Unit name (feature, module, endpoint) |
| **Location** | Path in repo |
| **Type** | `endpoint` / `module` / `feature` / `config` / `contract` / `script` / `component` |
| **Surface** | Exports, routes, or public entry points |

### Step 2 — Scan existing documentation

Scan `docs/` and `.md` files at root.

For each file, note:

| Field | Description |
|---|---|
| **File** | Doc file path |
| **Subject** | Feature/module/topic documented |
| **Covered** | List of referenced or implicated code units |

Determine the **naming convention** of existing files:
- Directory structure (flat, `docs/features/`, `docs/modules/`, etc.)
- Naming pattern (`{name}.md`, `{name}-note.md`, etc.)
- Recurring sections in existing files

If ≥ 3 files follow a coherent structure → capture it as **detected convention**.
Otherwise → note "No convention detected — default template applicable".

### Step 3 — Code↔doc cross-referencing

Compare the two inventories:

- **GAP** = documentable code unit WITHOUT corresponding doc file
- **ORPHAN** = doc file WITHOUT corresponding code unit (deleted code, renamed, or anticipated doc)
- **COVERED** = code unit WITH existing doc file

Classify each gap by severity:

- **HIGH** = public API endpoint, core feature, production config
- **MEDIUM** = important internal module, data contract, reusable component
- **LOW** = secondary utility, internal script, helper type

Filter by the write threshold (default: `HIGH+MEDIUM`).

**In DELEGATED mode**: this is where the cloud prepares micro-contexts
(see MICRO-CONTEXT CONTRACT). Each retained gap becomes a task for the local model.

### Step 4 — Write missing files

For each gap classified HIGH or MEDIUM (per threshold):

1. Determine the file path per the detected convention or fallback:
   - If detected convention → follow it
   - If `docs/features/` exists → `docs/features/{name}.md`
   - If `docs/` is flat → `docs/{name}.md`
   - Otherwise → `docs/{name}.md`
2. Apply the **default template** (see below), unless a structure
   convention was detected in existing files — in which case imitate
   that structure instead.
3. Fill the file based ONLY on observed code.
4. Do NOT invent content not observable in the code.

For LOW gaps:
- List them in the report but do NOT write a file immediately.

For orphans:
- List them in the report with a recommendation (archive, update, or confirm as anticipated doc).
- Do NOT delete or move orphaned files.

## DEFAULT TEMPLATE

Default template for feature files.
Used when no structure convention is detected in existing files.

If a convention is detected (≥ 3 coherent files), imitate that convention instead.

```markdown
# {name}

## About

{1-3 sentences: what this module/feature does, inferred from observed code}

## Location

`{path in repo}`

## Public surface

{list of exports, endpoints, props, or entry points observed}

## Configuration

{if applicable: variables, flags, options read by the module}
{otherwise: "No specific configuration detected."}

## Direct dependencies

{modules/packages directly imported by this code}
```

Each field is directly observable in the code.
The model doesn't have to invent — just read and reformulate.

Filling rules:

- `About`: reformulate in clear language what the code does. No excessive jargon.
- `Location`: exact path, no vague description.
- `Public surface`: list real names (functions, classes, endpoints). No paraphrase.
- `Configuration`: if the module reads variables or flags, list them. Otherwise, write the standard sentence.
- `Direct dependencies`: list ONLY direct imports from the module. Not indirect dependencies.

## MICRO-CONTEXT CONTRACT

In DELEGATED mode, the cloud prepares a micro-context for each gap.
This micro-context is everything the local model needs to execute step 4.

Micro-context format:

```markdown
## Task: write the file for {module_name}

### Template to follow
{default template OR detected convention}

### Module source code
{content of the module's main files — not the entire repo, only relevant files}

### Nearby existing files (for style reference)
{1-2 existing files of the same type, as style reference, if available}

### Instruction
Fill the template above based solely on the provided code.
Do not invent anything not observable in the code.
Write the file to: {target_path}
```

Micro-context preparation rules:

- Include ONLY the relevant module's files, not the entire repo.
- Limit source code to what's needed to understand the module.
- If the module is too large, include public entry files + types.
- Nearby existing files serve as style reference, not content to copy.
- If no nearby file exists, omit this section.

## SUPPORT BOUNDARY

Supported:
- Code→doc gap detection in a structured repo
- Writing missing files for HIGH and MEDIUM units
- Reporting doc→code orphans
- Targeted scope on a module or directory if requested
- DELEGATED mode with micro-context preparation for local model

Not supported (refuse explicitly):
- Harmonization between existing files → `1-vbb-doc-harmonizer`
- Code modification → entirely out of scope
- File deletion or moves → propose in text only
- Technical debt audit → `1-vbb-tech-debt`
- Dependency mapping → `t-vbb-dependency-mapper`
- Change impact analysis → `t-vbb-impact-analyzer`

## OUTPUT CONTRACT

Ensure `docs/audits/` exists.

Write exactly ONE Markdown report in:
`docs/audits/code-doc-gap-{YYYYMMDD-HHMM}.md`

Then update `docs/AUDIT_STATUS.md`.

The report must contain:

```markdown
## Verdict

## Execution mode

COMPLETE / DELEGATED

## Scanned scope

{applied scope: entire repo, or targeted module/feature}

## Documentable units (code inventory)

| Name | Location | Type | Surface |
|------|----------|------|---------|
| ... | ... | ... | ... |

## Existing documentation (doc inventory)

| File | Subject | Units covered |
|------|---------|--------------|
| ... | ... | ... |

## Detected convention

{description of naming/structure convention, or "None — default template applied"}

## Code↔doc matrix

| Code unit | Doc file | Status | Severity |
|-----------|----------|--------|----------|
| ... | — | GAP | HIGH |
| — | ... | ORPHAN | — |
| ... | ... | COVERED | — |

## Files written

| Unit | Created file | Template used | Summary |
|------|-------------|---------------|---------|
| ... | docs/features/auth.md | default | Documents the authentication middleware |

## Orphans detected

| Doc file | Recommendation |
|----------|---------------|
| ... | Archive / Update / Confirm anticipated |

## LOW gaps not written

| Unit | Location | Reason |
|------|----------|--------|
| ... | ... | Insufficient priority |

## Unknowns
```

In addition to the report, the skill MUST create the missing documentation files
identified in step 4.

## VERDICT RULES

- `READY`
  - all HIGH and MEDIUM gaps (per threshold) have been filled with written files
  - code→doc coverage is complete or near-complete
- `PARTIAL`
  - some gaps could not be filled (ambiguity, scope too large, UNKNOWN)
  - files were written but coverage remains incomplete
- `BLOCKED`
  - unable to scan code effectively (incoherent structure, giant monofile)
  - or unable to determine a coherent file path
- `UNKNOWN`
  - insufficient code surface to produce a reliable inventory