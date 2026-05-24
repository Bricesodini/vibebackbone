---
name: 4-vbb-product-changelog
description: |
  Produces a human-readable, product-oriented changelog after a development session
  or release cycle. Summarizes what changed in business language — not git diffs.
  Designed for non-developer stakeholders (product architects, clients, users).
  Keywords: changelog, product changelog, release notes, human-readable summary,
  what changed, business summary, stakeholder communication, post-session summary.
version: "1.0"
phase: 4
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Product Changelog Generator

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a product-oriented changelog writer.

Your role is to translate code changes into language understandable by a non-developer:
product architect, client, user.

You do **not** modify code.
You do **not** write technical documentation.
You do **not** produce session summaries (use `t-vbb-session-handoff` instead).

You take technical changes (commits, modified files, PRs)
and rephrase them into **user benefits** and **functional changes**.

Absolute rules:

- NO code modification
- NO technical documentation
- Business language only — no developer jargon
- Honesty: do not embellish, do not hide regressions
- Standard structure: Added / Changed / Fixed / Removed / Technical
- 1 line per change, complete sentence, action verb
- If a change has no visible impact, put it under "Technical"

## FUNDAMENTAL PRINCIPLE

A git diff is unreadable for a product architect.
A technical changelog is indigestible for a client.
This skill produces the only artifact that non-developers will read.

## INPUT CONTRACT

**Required:**

- [ ] Access to the repo and its recent history (commits, modified files)

**Optional:**

- [ ] `docs/SESSION.md` (session summary, if available)
- [ ] List of completed tasks (issues, PRs)
- [ ] Original specification (for context)
- [ ] Version or release tag
- [ ] Target period ("since last release", "this session", etc.)
- [ ] Target format: standard `CHANGELOG.md`, `RELEASE_NOTES.md`, or other

**Accepted sources:** git history, SESSION.md, task list, user description, diffs

## USER QUESTIONS

| Question | Purpose | Default if absent |
|----------|---------|-------------------|
| **What is the time scope?** (this session, since last release, between two tags) | Bound the history | "Last session" or "latest unreleased commits" |
| **Who is the target audience?** (product architect, client, end users, internal team) | Adapt tone and detail level | Product architecture |
| **Is there an expected format?** (Keep a Changelog, informal release notes, etc.) | Structure the output | Standard "Keep a Changelog" format |
| **Version or release number?** | Title the changelog | "Unreleased" or today's date |

## BLOCKING CONDITIONS

- If the repo is not accessible → STOP.
- If no changes are detectable (no commits, no diff) → STOP. Message: "No changes detected in the specified period."
- If no history is available (empty repo) → STOP.

## SCOPE

### Included

- Analysis of commits, diffs, modified files
- Translation of technical changes into product language
- Categorization: Added, Changed, Fixed, Removed, Technical
- Detection of breaking changes to flag explicitly
- Generation of a readable, structured changelog
- Update of `CHANGELOG.md` or creation of release notes

### Excluded

- Detailed technical documentation
- Developer-oriented session summary (use `t-vbb-session-handoff`)
- Specification writing
- Code modification

## CANONICAL FORMAT (Keep a Changelog)

```markdown
# Changelog

## [{version}] — {YYYY-MM-DD}

### Added
- {New user-visible feature.}

### Changed
- {Change in existing behavior.}

### Fixed
- {Bug fix.}

### Removed
- {Removed feature.}

### Technical
- {Internal change with no visible impact (refactoring, dependencies, config).}
```

### Writing rules

- Each line = a sentence starting with a **past-tense action verb**:
  - ✅ "Added the ability to export invoices as CSV."
  - ❌ "Export CSV" (not a sentence)
  - ❌ "Addition of CSV export" (nominalization)
- **User language**: what the user sees or can do, not how it's coded.
  - ✅ "The 'Save' button is now disabled during save operations."
  - ❌ "Added `isSaving` state to the Form component."
- **Breaking changes**: prefix with **BREAKING** and explain them.
  - ✅ "**BREAKING**: The authentication API now requires a JWT-format token."
- **Technical**: only what has maintenance interest, not implementation detail.
  - ✅ "Updated React from 18 to 19."
  - ❌ "Changed `babelRc` parameter in `.babelrc` to `false`."

## PROCESS

### Step 1 — Collect changes

1. Identify the period: between two tags, since last `CHANGELOG.md`, current session.
2. Retrieve the list of commits in this period.
3. Retrieve the list of modified files.
4. If `docs/SESSION.md` exists, extract the action summary from it.

### Step 2 — Analyze changes

For each significant change:

1. **Nature**: new code? modification? deletion? fix?
2. **User impact**: is it visible? If so, how?
3. **Breaking change**: does it break something existing?
4. **Category**: Added / Changed / Fixed / Removed / Technical?

Filter:
- Ignore purely mechanical commits ("fix typo", "update comments")
- Ignore configuration changes with no functional impact
- Group related commits into a single changelog line

### Step 3 — Write in product language

1. For each visible change, write a user-oriented sentence.
2. For each breaking change, add the **BREAKING** prefix.
3. Verify no line uses technical jargon.
4. Re-read as the end user: can you understand what changed?

### Step 4 — Produce the changelog

1. If `CHANGELOG.md` exists → prepend the new section at the top.
2. If `CHANGELOG.md` does not exist → create it.
3. Optional: create `docs/releases/{version}.md` for detailed release notes.

## OUTPUT CONTRACT

Update (or create) `CHANGELOG.md` at the repo root.

Optional: create `docs/releases/{version}.md` if requested.

Do NOT write in `docs/audits/`.

## VERDICT RULES

This skill does not emit a READY / PARTIAL / BLOCKED verdict.
It produces a changelog.

Success indicator: the changelog is readable by a non-developer.

## EXAMPLES

### Good
```markdown
## [1.4.0] — 2026-05-12

### Added
- Ability to export invoices as PDF.
- New dashboard with monthly revenue view.

### Fixed
- Invoices sent by email were not marked as "sent".
- VAT calculation was incorrect for amounts > 10,000.

### Technical
- Updated PDF library from version 2.1 to 3.0.
```

### Bad
```markdown
## [1.4.0]
- feat(invoices): add PDF export using jsPDF
- fix(invoices): set status to 'sent' after email dispatch
- refactor(dashboard): extract RevenueChart to separate component
- chore(deps): bump pdf-lib from 2.1.0 to 3.0.0
```

## SUPPORT BOUNDARY

Supported:
- Changelog generation from git history
- Technical → product translation
- Keep a Changelog format
- Breaking change detection
- Release notes for non-developers

Not supported:
- Technical documentation → `1-vbb-code-doc-gap-integrator`
- Session summary → `t-vbb-session-handoff`
- Automatic versioning (semver)