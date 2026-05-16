# Example Consumer Project — vibebackbone

This is a minimal example of a project that uses vibebackbone for operational governance.

## Structure

```
example-consumer-repo/
├── README.md                      # This file
├── docs/
│   ├── PROJECT_MODE.md            # Mode: CONSUMER, Provider: [your choice]
│   ├── SESSION.md                 # Session memory (local, gitignored)
│   ├── AUDIT_STATUS.md            # Audit dashboard (local, gitignored)
│   ├── audits/                    # Audit reports (local, gitignored)
│   └── ARCHITECTURE.md            # Your app architecture
├── src/                           # Your application code
├── tests/                         # Your application tests
├── .gitignore                     # Ignores local session artifacts
└── vibebackbone/                  # Clone or npm link
    ├── skills/
    ├── prompts/
    ├── AGENTS.md                  # Operational grammar
    ├── SYSTEM.md                  # Pi runtime behavior
    ├── CLAUDE.md                  # Claude entry point
    ├── README.md                  # Skills catalog (57 skills)
    └── ...
```

## Getting started

### 1. Setup vibebackbone for your provider

```bash
# Clone vibebackbone (if not present)
git clone https://github.com/vibebackbone/vibebackbone.git

# Run universal installer
bash vibebackbone/init.sh --provider [claude|pi|opencode|codex]

# Example: Claude Code
bash vibebackbone/init.sh --provider claude
```

This creates:
- `docs/PROJECT_MODE.md` — Declares mode and provider
- `docs/SESSION.md` — Session memory (gitignored)
- `docs/AUDIT_STATUS.md` — Audit dashboard (gitignored)
- `.claude/settings.json` (or `.pi/`, `.opencode/`, `.codex/` depending on provider)

### 2. Read governance documentation

- **Quick start** → `vibebackbone/CLAUDE.md` (if using Claude Code)
- **Triage rules** → `vibebackbone/AGENTS.md` § 3
- **Skills catalog** → `vibebackbone/README.md` (57 skills with phases [0-4])
- **Full governance** → `vibebackbone/skills/vibebackbone/docs/PILOTAGE.md`

### 3. Execute skills following phase sequence

vibebackbone uses a **phase-gated audit sequence [0→1→2→3]**:

**Phase [0] — Readiness**
- `0-vbb-scope-freeze` — Define scope and preconditions
- `0-vbb-audit-readiness` — Verify readiness for structured audits

**Phase [1] — Structure**
- `1-vbb-dependency-mapper` — Map code dependencies
- `1-vbb-conventions` — Verify naming and coding standards
- `1-vbb-tech-debt` — Identify technical debt
- `1-vbb-formatter` — Standardize code formatting

**Phase [2] — Deep audits**
- `2-vbb-security` — Security vulnerability review
- `2-vbb-api-auditor` — API design and robustness
- `2-vbb-db-robustness` — Database integrity and resilience
- `2-vbb-data-integrity` — Data consistency checks
- `2-vbb-ci` — CI/CD pipeline audit
- `2-vbb-ops` — Operational readiness
- `2-vbb-impact-analyzer` — Change impact analysis
- `2-vbb-test-coverage-mapper` — Test coverage analysis

**Phase [3] — Consolidation**
- `3-vbb-risk-register` — Consolidate all findings into risk register

### 4. Execute a skill

Each skill is self-contained. To execute:

```bash
# 1. Read the skill documentation
cat vibebackbone/skills/1-vbb-conventions/SKILL.md

# 2. Check preconditions (INPUT CONTRACT)
# Does your project have the required files/state?

# 3. Check blocking conditions
# Will any of these stop the skill execution?

# 4. Execute PROCESS steps
# Follow the step-by-step instructions

# 5. Document results
# Create docs/audits/[skill]-[date].md with findings

# 6. Update dashboard
# Add findings to docs/AUDIT_STATUS.md
```

### 5. Use session memory

**docs/SESSION.md** (gitignored, local) — Save your progress and resume context:

```markdown
# SESSION — My Project [2026-05-16]

## Current task
- Executing phase [1] conventions audit
- Last skill: 1-vbb-conventions (completed 14:30)

## Next steps
1. Execute 1-vbb-tech-debt
2. Review findings in docs/audits/
3. Update docs/AUDIT_STATUS.md

## Decisions made
- Chose CONSUMER mode (not DISTRIBUTION)
- Using Claude Code for skill execution
- Need to run security audit before release
```

When you resume the next day:
```bash
# Read SESSION.md
cat docs/SESSION.md

# Continue from where you left off
cat vibebackbone/skills/1-vbb-tech-debt/SKILL.md
```

### 6. Check audit dashboard

**docs/AUDIT_STATUS.md** (gitignored, local) — Track progress:

```markdown
# AUDIT_STATUS — My Project

| Phase | Skill | Status | Risk | Date |
|-------|-------|--------|------|------|
| [0] | scope-freeze | ✓ READY | None | 2026-05-16 |
| [0] | audit-readiness | ✓ READY | None | 2026-05-16 |
| [1] | dependency-mapper | ⏭️ PENDING | None | — |
| [1] | conventions | ⏭️ PENDING | None | — |
| [1] | tech-debt | ⏭️ PENDING | None | — |
| [2] | security | ⏭️ PENDING | None | — |
| [2] | api-auditor | ⏭️ PENDING | None | — |
```

---

## Multi-provider usage

You can use multiple providers on the same project:

```bash
# Install for Claude Code
bash vibebackbone/init.sh --provider claude

# Later, install for Pi (if you have Pi agents)
bash vibebackbone/init.sh --provider pi

# Both will:
# - Read docs/PROJECT_MODE.md (shared mode declaration)
# - Read docs/SESSION.md (shared resumption context)
# - Use isolated config (.claude/, .pi/)
# - No conflicts
```

---

## Troubleshooting

### "How do I understand the triage?"

Read `vibebackbone/AGENTS.md` § 3 (Triage opérationnel). 10-minute read covers all 4 modes (RAPIDE, STRUCTURÉE, AUDIT, CLÔTURE).

### "How do I know which skill to use?"

1. Check your task type (bug fix, feature, security, refactor)
2. Match to phase: [0] readiness, [1] structure, [2] audits, [3] consolidation
3. Pick skill from `vibebackbone/README.md` catalog
4. Read SKILL.md to validate preconditions

Example:
- Task: "Audit our API design"
- Phase: [2] audits
- Skill: `2-vbb-api-auditor`
- Read: `vibebackbone/skills/2-vbb-api-auditor/SKILL.md`

### "How do I escalate findings to team?"

1. Document in `docs/audits/[skill]-[date].md`
2. Update `docs/AUDIT_STATUS.md` with risk level (P0/P1/P2/P3)
3. Commit and push for team review
4. Note: docs/SESSION.md and docs/AUDIT_STATUS.md are gitignored (local only) — republish via docs/audits/ (gitignored but timestamped)

### "Multi-provider conflict?"

Each provider has isolated config:
- Claude Code → `.claude/settings.json`
- Pi → `.pi/taskplane.json`
- OpenCode → `.opencode/config.json`
- Codex → `.codex/env.sh`

No conflicts as long as each writes to its own directory.

---

## Key files

- `docs/PROJECT_MODE.md` — Mode and provider declaration (created by init.sh)
- `docs/SESSION.md` — Session memory (gitignored, created by init.sh)
- `docs/AUDIT_STATUS.md` — Audit dashboard (gitignored, created by init.sh)
- `docs/audits/` — Timestamped reports (gitignored)
- `vibebackbone/AGENTS.md` — Operational grammar (triage + escalation)
- `vibebackbone/SYSTEM.md` — Pi runtime (planning + risk discipline)
- `vibebackbone/CLAUDE.md` — Claude entry point (quick reference)
- `vibebackbone/README.md` — Skills catalog (57 skills, 24 prompts)

---

## Next steps

1. **Setup** — Run `bash vibebackbone/init.sh --provider [your choice]`
2. **Read** — Start with `vibebackbone/CLAUDE.md` (if Claude) or `vibebackbone/AGENTS.md` § 3
3. **Pick a skill** — From `vibebackbone/README.md` that matches your task
4. **Execute** — Follow PROCESS steps in SKILL.md
5. **Document** — Save findings to `docs/audits/` and update dashboard
6. **Resume** — Use `docs/SESSION.md` to pick up tomorrow

---

**Example created by**: Claude Code
**vibebackbone version**: v1.0.0
**Installation method**: Universal installer (init.sh)
