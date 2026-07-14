---
name: 0-vbb-standard
description: |
  Defines the canonical Vibebackbone skill contract for Pi.
  Use when creating, adapting, reviewing, or validating any Vibebackbone skill.
  Keywords: skill standard, frontmatter, validation, report template, Pi compatibility,
  skill contract, mode-sensitive, subagent.
version: "1.1"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Vibebackbone Skill Standard

## ROLE & POSTURE

You are the canonical reference for all Vibebackbone skills.

Your role is to define and validate:

- expected structure
- frontmatter
- reporting format
- hard rules
- Pi compatibility

You do not perform repo audits.
You validate skill design and skill consistency.

## INPUT CONTRACT

**Required:**

- [ ] A `SKILL.md` to create, adapt, or validate

**Optional:**

- [ ] An existing skill
- [ ] A functional need to transform into a skill
- [ ] A comparison between Claude / Codex / Pi versions

**Accepted sources:** pasted content, file path, textual description

## BLOCKING CONDITIONS

- If no skill or skill need is provided → STOP. Message: "No skill to normalize or validate."
- If the request concerns a repo audit rather than a skill → STOP. Message: "This resource defines skill standards, not project auditing."

## SCOPE

This skill defines:

- mandatory flat frontmatter
- filesystem path / parent directory ↔ `name` compatibility
- mandatory section layout
- report template
- verdict taxonomy
- severity taxonomy
- subagent brief pattern
- absolute rules
- Pi-oriented routing description quality

Phase values use two explicit namespaces. `SKILL.md` frontmatter follows the
agentic lifecycle (for example, every `1-vbb-*` skill uses `02_AUDIT`), while
`CONTRACT.yaml` keeps the stable catalog routing scope (the same skills use
`routing.phase_scope: phase_1`). These values are intentionally not identical.

Routing triggers have one case-insensitive exact owner across the catalog.
Adjacent responsibilities use qualified action or stage phrases; they do not
share a generic trigger and rely on catalog order or hidden numeric priority.

Formal artifact kinds are closed: `phase_artifact`, `audit_report`,
`design_document`, `release_document`, `infrastructure_file`, `ADR`, and
`persistent_state_update`. A `1-vbb-*` skill with a line-start normative
instruction to write a report or document must declare a non-null primary
artifact. The same rule applies to `4-vbb-*` skills with a normative `Emit:` or
`Update (or create)` instruction and to bounded transverse report writers.
Conditional or alternative files remain structured outputs unless their paths
are deterministic enough to declare separately.

### Optional sections (for execution skills)

- `SUPPORT BOUNDARY` — explicit list of supported and unsupported cases

Canonical SUPPORT BOUNDARY format:

```markdown
## SUPPORT BOUNDARY

Supported:
- <supported case 1>
- <supported case 2>

Not supported (refuse explicitly):
- <unsupported case 1> → <reason>
- <unsupported case 2> → <reason>
```

Rule: any skill that writes to the repo (phase 1, transverse execution)
should include this section. Read-only skills (phase 0, 2, 3)
are exempt — their scope is naturally bounded by their audit role.

## PROCESS

1. Check skill name format and filesystem path / parent directory compatibility.
2. Check frontmatter phase and contract routing scope against their distinct canonical namespaces.
3. Check frontmatter completeness.
4. Check required sections.
5. Check whether `mode_sensitive` logic is handled correctly.
6. Check whether the report/output format matches Vibebackbone requirements.
7. Check whether the description is precise enough for Pi routing.
8. Check whether internal references use only canonical skills that exist in the same catalog.
9. Check that routing triggers have no case-insensitive exact duplicate owner.
10. Check normative authored outputs against formal primary/secondary artifacts.
11. Check whether `SUPPORT BOUNDARY` is present for execution skills (recommended, not mandatory yet).
12. Flag any violation against absolute rules.

> **Note on description handling.** The `description:` field is NOT auto-truncated by any vibebackbone mechanism. It is hand-maintained and validated for **precision** (triggers, keywords) per step 6, not for length. The `setup.sh` → `distributions/codex/setup.sh` codegen pipeline operates on `~/.codex/AGENTS.md` via block replacement (`<!-- vibebackbone:generated:start -->` / `<!-- vibebackbone:generated:end -->` markers) and does NOT touch skill descriptions in this repo.

## OUTPUT CONTRACT

Output must contain:

- compliance status
- missing or invalid sections
- frontmatter issues
- path/name alignment issues
- Pi compatibility issues
- structural fixes required
- optional improvements

## VERDICT RULES

Use:

- `READY` if the skill is compliant
- `PARTIAL` if structurally usable but incomplete
- `BLOCKED` if the skill breaks core Vibebackbone contract
- `UNKNOWN` if evidence is insufficient
