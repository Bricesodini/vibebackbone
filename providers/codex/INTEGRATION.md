# Codex Integration

## Quick start

```bash
bash init-codex.sh
```

Then configure your Codex environment variables.

## Configuration

1. **Set environment variables** — `export CODEX_API_KEY=...`
2. **Read** `/AGENTS.md` — Operational triage and governance
3. **Read** `SYSTEM.md` — Planning protocol and risk discipline
4. **Reference** `skills/vibebackbone/docs/PILOTAGE.md` — Full governance model

## Codex + vibebackbone

vibebackbone **IS** a Codex v2.0 implementation:

- **vibecodex governance** — AGENTS.md defines the operational model
- **Sequence [0→1→2→3]** — Phase-gated audit sequence with preconditions
- **Risk-register consolidation** — Phase [3] collects all risks and verdicts
- **Multi-provider** — Agents (Pi, Claude, OpenCode, Codex) use same grammar

## Audit sequence

Follow strictly:

```
[0] scope-freeze → [0] audit-readiness
       ↓
[1] dependency-mapper → [1] conventions → [1] tech-debt
       ↓
[2] security → [2] api-auditor → [2] db-robustness → [2] data-integrity → [2] ops → [2] ci
       ↓
[3] risk-register
```

**Preconditions:**
- Never [1] without [0]
- Never [2] without [0] + [1] dependency-mapper
- [3] must be last

## Skill execution

Each skill defines:

1. **INPUT CONTRACT** — Prerequisites (what data/state must exist?)
2. **BLOCKING CONDITIONS** — Failure modes (what stops this skill?)
3. **PROCESS** — Execution steps (what to do?)
4. **OUTPUT CONTRACT** — Deliverables (what's produced?)
5. **VERDICT RULES** — Success criteria (how to evaluate?)

Check INPUT CONTRACT before executing. Escalate if BLOCKING CONDITION detected.

## Risk management

Codex emphasizes **risk-register consolidation**:

- **[0]** : Identify scope and readiness risks
- **[1]** : Surface structural risks (tech-debt, conventions)
- **[2]** : Deep-dive audit risks (security, integrity, ops)
- **[3]** : Consolidate all findings into risk-register

Risk-register output:
- **P0** (Critical) : Blocks deployment
- **P1** (Major) : Must fix before release
- **P2** (Minor) : Fix in next version
- **P3** (Info) : Document and monitor

## Planning protocol

Codex agents follow the planning protocol:

1. **Plan** — Read skill spec, draft approach
2. **Read-only** — Validate preconditions, check artifacts
3. **Execute** — Run PROCESS steps, generate OUTPUT
4. **Document** — Write report to `docs/audits/[skill]-[date].md`
5. **Consolidate** — Update `docs/AUDIT_STATUS.md` with findings

## Session state management

Codex maintains shared state via:

- **docs/SESSION.md** — Active task, decision context (local, gitignored)
- **docs/AUDIT_STATUS.md** — Audit dashboard with status per phase (local, gitignored)
- **docs/audits/** — Timestamped formal reports (local, gitignored)

SESSION.md is **shared** across all providers (Pi, Claude, OpenCode, Codex).

## Environment variables

```bash
# Required
export CODEX_API_KEY="sk-..."        # Your Codex API key

# Optional
export CODEX_MODEL="claude-opus-4.7" # Default model for agents
export CODEX_TIMEOUT="3600"          # Timeout in seconds (default: 1 hour)
export VBB_PROVIDER="codex"          # Declare provider (auto-detected)
export VBB_MODE="CONSUMER"           # Mode: CONSUMER or DISTRIBUTION
```

## Multi-provider coordination

If running alongside Pi, Claude Code, or OpenCode:

- **Shared governance** : `/AGENTS.md`, `/SYSTEM.md`, `/README.md`
- **Shared state** : `docs/PROJECT_MODE.md`, `docs/SESSION.md`
- **Provider-specific** : `.codex/env.sh`, `.pi/`, `.claude/`, `.opencode/`

PROJECT_MODE.md declares the current mode (CONSUMER, DISTRIBUTION).

## Troubleshooting

**"Phase [2] skill failed"** → Check if [0] and [1] completed first. Review BLOCKING CONDITION for skill.

**"Risk-register incomplete"** → Ensure all [0], [1], [2] skills executed. [3] collects findings from all phases.

**"API key invalid"** → Check `export CODEX_API_KEY=...` is set and valid.

**"Multi-provider conflict"** → Each provider writes to its own .codex/, .pi/, .claude/ directories. Use `docs/PROJECT_MODE.md` to signal current mode.

**"Need full governance reference"** → Read `/AGENTS.md` (triage), then `SYSTEM.md` (planning), then `skills/vibebackbone/docs/PILOTAGE.md` (full model).

## Support

- **Skill execution** → Read SKILL.md INPUT CONTRACT and BLOCKING CONDITIONS
- **Governance** → See `/AGENTS.md` § Triage and SYSTEM.md § Planning protocol
- **Risk management** → See `/skills/3-vbb-risk-register/SKILL.md` for consolidation rules
- **Multi-provider** → See `docs/INSTALLATION.md`
