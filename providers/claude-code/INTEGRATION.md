# Claude Code Integration

## Quick start

```bash
bash init-claude.sh
```

Then open this project in Claude Code.

## Configuration

1. **Open in Claude Code** — File → Open Folder
2. **Read `/CLAUDE.md`** — Operational rules and triage
3. **Reference `/README.md`** — Catalog of 57 skills
4. **Reference `/AGENTS.md`** — Triage and escalation rules

## Operational modes (voies)

- **RAPIDE** — Direct implementation (low risk, single skill)
- **STRUCTURÉE** — Plan before modification (multi-file, contracts)
- **AUDIT** — Sequence [0→1→2→3] with formal audit reports
- **CLÔTURE** — Session handoff (save state to docs/SESSION.md)

## Workflow

Each skill is a structured task:

1. **Read** `skills/[phase]-vbb-[name]/SKILL.md`
   - ROLE & POSTURE
   - INPUT CONTRACT (preconditions)
   - BLOCKING CONDITIONS (failure modes)
   - SCOPE
   - PROCESS (steps)
   - OUTPUT CONTRACT
   - VERDICT RULES

2. **Check** INPUT CONTRACT — do you have the data/state required?

3. **Check** BLOCKING CONDITIONS — will any of these stop the skill?

4. **Execute** PROCESS steps

5. **Generate** OUTPUT and document in `docs/audits/[skill]-[date].md`

6. **Update** `docs/AUDIT_STATUS.md` with findings

## Triage example

**Scenario**: "Add user authentication"

- Affects auth system? → **AUDIT** (phase [2] security review)
- Changes contracts? → **STRUCTURÉE** (plan first)
- Simple bug fix? → **RAPIDE** (direct fix)

Reference: `/AGENTS.md` § 3 (Triage opérationnel)

## Context caching

These files are excellent candidates for Claude Code prompt caching:

- `AGENTS.md` — Operational grammar (325 lines, stable)
- `SYSTEM.md` — Pi runtime behavior (146 lines, stable)
- `skills/vibebackbone/docs/PILOTAGE.md` — Operational governance (323 lines, stable)

Benefit: Faster response + lower token cost on repeated tasks.

## Session memory

Local session state (gitignored):

- `docs/SESSION.md` — Resume context (active tasks, decisions)
- `docs/AUDIT_STATUS.md` — Audit dashboard (status, risks, actions)
- `docs/audits/` — Timestamped reports

Use `docs/SESSION.md` to capture handoff notes when leaving the session.

## Troubleshooting

**"Skill not applicable"** → Check INPUT CONTRACT. Your project may lack required artifacts (README.md, ARCHITECTURE.md, etc.)

**"BLOCKING CONDITION triggered"** → Read the condition description. Common: scope-freeze required before audit, or dependency-mapper must run before security review.

**"Need to understand governance"** → Start with `AGENTS.md` § 1-3 (10 min read), then `SYSTEM.md` § Runtime (5 min).

## Support

- **Questions about skills** → Read SKILL.md PROCESS and PROCESS sections again
- **Architecture questions** → See `skills/vibebackbone/docs/PILOTAGE.md`
- **Multi-provider questions** → See `docs/INSTALLATION.md`
