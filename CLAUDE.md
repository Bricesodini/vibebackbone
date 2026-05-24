# CLAUDE.md — vibebackbone

You operate under **vibebackbone** governance.

**vibebackbone = 62 skills · 32 prompts · 4 routes (FAST, STRUCTURED, AUDIT, CLOSEOUT)**

## Governance files

- `docs/CONTEXT.md` — MOC / persistent central router (read first)
- `AGENTS.md` — Canonical operational grammar
- `SYSTEM.md` — Pi runtime behavior
- `docs/PILOTAGE.md` — Operational piloting v2.0

```
@AGENTS.md
@SYSTEM.md
```

## Shortcuts (paths relative to vibebackbone repo)

- Skills: `skills/` (62 dirs, each contains SKILL.md)
- Prompts: `prompts/` (32 templates)
- Full catalog: `skills/0-vbb-guide/SKILL.md`

## Fundamental rule

Before any action, classify the task into a route:

1. **FAST** — low risk, direct action (ZERO: activity log only, MINIMAL: patch summary only, STANDARD: full cycle)
2. **STRUCTURED** — plan before modification (contracts, multi-file)
3. **AUDIT** — audit sequence (security, integrity)
4. **CLOSEOUT** — session handoff

If in doubt, read `AGENTS.md` section 1 (Mandatory triage).

## Typical usage

```bash
# List available skills
ls skills/

# Read the guide
cat skills/0-vbb-guide/SKILL.md

# Choose and apply a skill
# e.g. cat skills/2-vbb-security/SKILL.md then follow the steps
```