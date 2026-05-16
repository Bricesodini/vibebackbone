# Pi (Pinokio) Integration

## Quick start

```bash
bash init-pi.sh
```

Then configure `.pi/taskplane.json` with your project context.

## Configuration

1. **Edit** `.pi/taskplane.json` — Your project metadata and agent config
2. **Read** `SYSTEM.md` — Pi runtime behavior and planning protocol
3. **Reference** `/AGENTS.md` — Agent orchestration and triage rules
4. **Reference** `skills/vibebackbone/docs/PILOTAGE.md` — Operational governance

## Pi agent orchestration

Pi agents follow the vibebackbone triage (RAPIDE/STRUCTURÉE/AUDIT/CLÔTURE).

**SYSTEM.md** specifies:
- Planning protocol (plan → read-only → execution)
- Risk discipline (escalate if threshold exceeded)
- Context LLM discipline (token budgets per skill)
- Multi-provider support (Pi, Claude, OpenCode, Codex)

## Skills routing

Respect the phase dependencies:

- **Phase [0]** : scope-freeze, audit-readiness (preconditions for everything)
- **Phase [1]** : dependency-mapper, conventions, tech-debt, code-janitor, formatter
- **Phase [2]** : security, api-auditor, db-robustness, data-integrity, ci, ops, impact-analyzer, test-coverage-mapper
- **Phase [3]** : risk-register (must be last)

**Critical precondition**: Never launch [2] without [0] + [1] dependency-mapper.

## Agent configuration

Edit `.pi/taskplane.json`:

```json
{
  "project_name": "my-project",
  "mode": "CONSUMER",
  "provider": "pi",
  "governance": "vibebackbone v1.0",
  "agents": [
    {
      "name": "auditor",
      "role": "Audit coordinator",
      "model": "gpt-4",
      "skills_phases": [0, 1, 2, 3]
    }
  ],
  "planning_protocol": "enabled",
  "risk_discipline": "enabled",
  "context_lvm_discipline": "enabled"
}
```

## Monitoring and observability

**Agent memory** (`.pi/hippo-memory/`) — Pi maintains agent state and conversation history

**Execution log** (`.pi/taskplane.json` history) — Track agent decisions and transitions

**Audit trail** (`docs/audits/`) — Formal reports from each skill execution

Use these to debug agent behavior or reconstruct decision history.

## Session memory

Local session state (gitignored):

- `docs/SESSION.md` — Agent resumption context (current task, decisions)
- `docs/AUDIT_STATUS.md` — Audit dashboard (status per phase, risks, actions)
- `docs/audits/` — Timestamped reports (one per skill execution)

Pi agents read `docs/SESSION.md` at startup to resume context.

## Multi-provider coordination

If running alongside Claude Code, OpenCode, or Codex:

- **Shared state** : `skills/`, `prompts/`, `/AGENTS.md`, `/SYSTEM.md`
- **Provider-specific** : `.pi/`, `.claude/`, `.opencode/`, `.codex/` (not shared)
- **Coordination** : Via `docs/PROJECT_MODE.md` (mode declaration) and `docs/SESSION.md` (shared memory)

Each provider reads `PROJECT_MODE.md` to identify the current mode (CONSUMER, DISTRIBUTION).

## Troubleshooting

**"Agent stuck at phase [1]"** → Check if [0] dependency-mapper ran first. Restart with explicit phase sequence.

**"Token budget exceeded"** → Check SYSTEM.md § 11 (Context LLM discipline). Reduce skill complexity or split into sub-tasks.

**"Multi-provider conflict"** → Ensure each provider writes to its own config directory (`.pi/`, `.claude/`, etc.). Shared state via `docs/PROJECT_MODE.md`.

**"Need to understand governance"** → Start with `/AGENTS.md` § 1-3 (15 min), then `SYSTEM.md` § Planning protocol (10 min).

## Support

- **Questions about skills** → Read SKILL.md PROCESS and VERDICT RULES sections
- **Agent orchestration** → See `SYSTEM.md` § Planning protocol
- **Multi-provider** → See `docs/INSTALLATION.md`
