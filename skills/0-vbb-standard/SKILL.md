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
2. Check frontmatter completeness.
3. Check required sections.
4. Check whether `mode_sensitive` logic is handled correctly.
5. Check whether the report/output format matches Vibebackbone requirements.
6. Check whether the description is precise enough for Pi routing.
7. Check whether internal references use only canonical skills that exist in the same catalog.
8. Check whether `SUPPORT BOUNDARY` is present for execution skills (recommended, not mandatory yet).
9. Flag any violation against absolute rules.

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