# PROJECT_MODE — [Your Project Name]

**Mode** : CONSUMER
**Provider** : [Select one: pi | claude-code | opencode | codex]
**Gouvernance** : vibebackbone v1.0
**Date** : [Installation date]

## Voies activées (enabled paths)

- [x] RAPIDE — Low-risk, direct implementation
- [x] STRUCTURÉE — Plan before modification (multi-file changes, contracts)
- [x] AUDIT — Phase-gated audit sequence [0→1→2→3]
- [x] CLÔTURE — Session handoff (save state to docs/SESSION.md)

## Configuration

### Provider setup

Choose your provider:

- **Pi (Pinokio)** — Agent orchestration framework
  - Config: `.pi/taskplane.json`
  - Entry: `SYSTEM.md`

- **Claude Code** — IDE integration
  - Config: `.claude/settings.json`
  - Entry: `CLAUDE.md`

- **OpenCode** — Distribution and contribution
  - Config: `.opencode/config.json`
  - Entry: `README.md` + `CONTRIBUTING.md`

- **Codex** — Governance framework
  - Config: `.codex/env.sh`
  - Entry: `AGENTS.md` + `SYSTEM.md`

### Repository structure

```
.
├── docs/
│   ├── PROJECT_MODE.md          # This file
│   ├── SESSION.md               # Local session memory (gitignored)
│   ├── AUDIT_STATUS.md          # Local audit dashboard (gitignored)
│   ├── audits/                  # Timestamped audit reports (gitignored)
│   └── ARCHITECTURE.md          # Your application architecture
│
├── vibebackbone/                # Skills + prompts + governance
│   ├── skills/                  # 57 orthogonal skills
│   ├── prompts/                 # 24 session templates
│   ├── AGENTS.md                # Triage + escalation rules
│   ├── SYSTEM.md                # Planning protocol
│   └── ...
│
├── .claude/                     # Claude Code config (if using)
├── .pi/                         # Pi config (if using)
├── .opencode/                   # OpenCode config (if using)
├── .codex/                      # Codex config (if using)
│
├── src/                         # Your application code
├── tests/                       # Your application tests
└── .gitignore                   # Ignores local artifacts
```

## Workflows

### Audit sequence [0→1→2→3]

vibebackbone uses a **phase-gated audit sequence**:

1. **Phase [0] — Readiness** (2 skills)
   - Scope-freeze, audit-readiness
   - Precondition: None
   - Decision: Is scope frozen? Proceed to [1]?

2. **Phase [1] — Structure** (5 skills)
   - Conventions, tech-debt, dependency-mapper, formatter, code-janitor
   - Precondition: Phase [0] completed
   - Decision: Does structure pass? Proceed to [2]?

3. **Phase [2] — Deep audits** (8 skills)
   - Security, API, DB, data-integrity, ops, CI, impact, test-coverage
   - Precondition: Phase [0] + Phase [1] dependency-mapper
   - Decision: Do findings pass threshold? Proceed to [3]?

4. **Phase [3] — Consolidation** (1 skill)
   - Risk-register: consolidate all findings from [0-2]
   - Precondition: All [0-2] skills
   - Decision: Are risks acceptable? Release decision.

**Critical rule**: Never [2] without [0] + [1] dependency-mapper.

### Skill execution template

For each skill:

1. **Read** `vibebackbone/skills/[phase]-vbb-[name]/SKILL.md`
2. **Check INPUT CONTRACT** — Do you have required artifacts?
3. **Check BLOCKING CONDITIONS** — Will any of these stop you?
4. **Execute PROCESS** — Follow step-by-step instructions
5. **Generate OUTPUT** — Create deliverables (code, docs, reports)
6. **Document** — Write `docs/audits/[skill]-[date].md`
7. **Update** — Add findings to `docs/AUDIT_STATUS.md`

### Session memory

**docs/SESSION.md** (gitignored, local):
- What's the current task?
- What were recent decisions?
- What's the next action?

Use this to resume context across sessions.

Example:
```markdown
# SESSION — My Project [2026-05-16]

## Current task
Phase [1] conventions audit

## Progress
- ✓ Completed scope-freeze
- ✓ Completed audit-readiness
- ⏭️ Next: 1-vbb-conventions

## Findings so far
- Scope is frozen
- Team aligned on approach
```

### Audit dashboard

**docs/AUDIT_STATUS.md** (gitignored, local):
- Track status per skill
- Note risk level (P0/P1/P2/P3)
- Link to audit reports

Update after each skill execution.

## Decision template

Record decisions for traceability:

```markdown
## Decision [DATE] — [Decision name]

**What** : [What was decided]
**Why** : [Why this decision]
**Impact** : [Who/what is affected]
**Owner** : [Who owns it]
**Status** : [DECIDED | PENDING | DONE]

### Evidence
- Finding from skill X
- Discussion in PR #123
```

## References

### Quick reference

- **Triage rules** — `vibebackbone/AGENTS.md` § 3 (10 min read)
- **Planning protocol** — `vibebackbone/SYSTEM.md` § Planning (5 min read)
- **Skills catalog** — `vibebackbone/README.md` (browse)
- **Full governance** — `vibebackbone/skills/vibebackbone/docs/PILOTAGE.md` (30 min read)

### Provider-specific

- **Claude Code** — `vibebackbone/CLAUDE.md`
- **Pi** — `vibebackbone/SYSTEM.md`
- **OpenCode** — `vibebackbone/CONTRIBUTING.md`
- **Codex** — `vibebackbone/AGENTS.md`

## Support

- **Question**: Read the referenced files above
- **Stuck**: Review docs/SESSION.md to resume context
- **Risk**: Escalate via docs/AUDIT_STATUS.md (P0/P1)

---

**Created by**: vibebackbone init.sh
**Mode**: CONSUMER
**Governance**: vibebackbone v1.0
