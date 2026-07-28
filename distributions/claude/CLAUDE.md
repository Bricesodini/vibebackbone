---
load_policy: always
context_role: claude-entry-point
phase: transverse
status: active
---

# CLAUDE.md — vibebackbone

You operate under **vibebackbone** governance.

vibebackbone = 4 route families + MVP START gate · catalog via `python tools/vbb-status-dashboard.py`

`load_policy: always` — this is the Claude Code entry point. `@AGENTS.md`
and `@SYSTEM.md` are sourced at session start.

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

- Skills: `skills/` (one dir per skill, each contains SKILL.md)
- Prompts: `prompts/`
- Full catalog: `skills/0-vbb-guide/SKILL.md`

## Fundamental rule

Before any action, classify the task into a route:

1. **FAST** — low risk, direct action (ZERO: activity log only, MINIMAL: patch summary only, STANDARD: full cycle)
2. **STRUCTURED** — plan before modification (contracts, multi-file)
3. **AUDIT** — audit sequence (security, integrity)
4. **CLOSEOUT** — session handoff

For MVP/from-zero work, apply `docs/MVP_START_PROTOCOL.md` through
`0-vbb-rico-readiness` before implementation. If readiness is not READY, ask
blocking questions only.

If in doubt, read `AGENTS.md` section 1 (Mandatory triage).

## Adversarial dimension (post-cutoff, ADR 0051)

Post-cutoff runs (cutoff `2026-07-28_1400`) declare
`adversarial_governance_version: "1.1"` and must declare an
**adversarial level** at intake (default `A1` if undeclared).
Apply the criticality matrix in
`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.2 and the 7 fail-closed
rules of §4.3.

When the task touches governance canon, auth, secrets, data integrity,
published contracts, money, concurrency, deployment, or canon-gating
work: declare `A2` (or higher trigger) and respect
`A2_DISTINCT_AGENT_PROXY` (different LLM family or human reviewer).

`certification_status` accepts `PRE_CERTIFICATION` and `MIGRATION`
post-cutoff (ratified 2026-07-28) for subjects awaiting first
CERTIFIED or in active transition.

The validator `tools/vbb-adversarial-gate.py` is now part of the
canonical toolset; the loop-closure tool accepts `adversarial_governance_version: "1.1"`.

## Typical usage

```bash
# List available skills
ls skills/

# Read the guide
cat skills/0-vbb-guide/SKILL.md

# Choose and apply a skill
# e.g. cat skills/2-vbb-security/SKILL.md then follow the steps
```
