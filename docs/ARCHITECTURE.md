---
context_role: canonical-architecture
phase: transverse
status: active
updated: 2026-05-29
---

# ARCHITECTURE — Canonical Structured Source

This file is the canonical architecture source for vibebackbone.

Each architecture block is human-readable Markdown with a structured YAML body.
Derived views such as `docs/RELATIONS.md`, graphs, sensitivity maps and impact
indexes must be generated from this file.

Architecture-sensitive files must be referenced by at least one block `files:`
pattern. The rule is enforced by `python tools/vbb-architecture.py lint`.

Required block fields:

- `id`
- `type`
- `status`
- `role`
- `responsibilities`
- `depends_on`
- `impacts`
- `files`
- `contracts`
- `tests`
- `risks`

Valid statuses: `active`, `planned`, `deprecated`, `unknown`.

## Bloc: Governance Core

```yaml
id: governance-core
type: governance
status: active
role: Canonical operational grammar for routing, escalation, session behavior and project truth.
responsibilities:
  - Define route families and escalation rules
  - Preserve document hierarchy
  - Prevent parallel truth between governance, sessions and code
depends_on: []
impacts:
  - task triage
  - audit routing
  - session startup
  - session closeout
files:
  - AGENTS.md
  - SYSTEM.md
  - docs/CONTEXT.md
  - docs/PILOTAGE.md
  - docs/PROJECT_MODE.md
  - docs/SESSION_RULES.md
  - docs/CONVENTIONS.md
  - skills/vibebackbone/**
contracts:
  - vibebackbone
  - 0-vbb-pilotage
  - 0-vbb-standard
tests:
  - tests/test_loop_closure.py
  - tests/test_status_dashboard.py
risks:
  - id: GOV-001
    level: P2
    note: Governance duplication can create conflicting operational truth.
```

## Bloc: Skills Catalog

```yaml
id: skills-catalog
type: distribution
status: active
role: Catalog of reusable agent skills and their machine-facing contracts.
responsibilities:
  - Store SKILL.md files
  - Store CONTRACT.yaml files
  - Maintain indexed contract coverage
depends_on:
  - governance-core
impacts:
  - route execution
  - audit skills
  - structured task support
files:
  - skills/*/SKILL.md
  - skills/*/CONTRACT.yaml
  - skills/INDEX.yaml
contracts:
  - skills/INDEX.yaml
tests:
  - tests/test_contract_lint.py
  - tests/smoke-contract-runtime.sh
risks:
  - id: SKILL-001
    level: P1
    note: Contract index drift reduces route and runtime coverage.
```

## Bloc: Prompt Library

```yaml
id: prompt-library
type: distribution
status: active
role: Session entrypoints and routing prompts layered around the skill catalog.
responsibilities:
  - Provide canonical phase prompts
  - Provide specialized route prompts
  - Expose a Markdown phase router
depends_on:
  - governance-core
  - skills-catalog
impacts:
  - session entry
  - user-facing workflow selection
  - provider command generation
files:
  - prompts/*.md
  - prompts/canonical/*.md
  - PROMPTS_ARCHITECTURE.md
contracts: []
tests:
  - tests/smoke-install.sh
risks:
  - id: PROMPT-001
    level: P2
    note: Adapter deployment can diverge from canonical prompt inventory.
```

## Bloc: Contract Tooling

```yaml
id: contract-tooling
type: tooling
status: active
role: Local validation, dry-run runtime, route lookup and dashboard tooling.
responsibilities:
  - Lint skill contracts
  - Execute contract dry-runs
  - Route queries to skills
  - Report repository status
depends_on:
  - skills-catalog
  - governance-core
impacts:
  - CI confidence
  - release readiness
  - implementation-readiness audits
files:
  - tools/vbb-contract-lint.py
  - tools/vbb-contract-runtime.py
  - tools/vbb-executor.py
  - tools/vbb-phase-router.py
  - tools/vbb-project-init.py
  - tools/vbb-status-dashboard.py
contracts:
  - t-vbb-status-dashboard
  - t-vbb-index
  - t-vbb-mode-transition-gate
  - t-vbb-deploy-runtime
tests:
  - tests/test_contract_lint.py
  - tests/test_status_dashboard.py
risks:
  - id: TOOL-001
    level: P2
    note: Formal executor was declarative-only (ADR-0001); vbb-executor.py now provides state machine, gate evaluation, and artifact lifecycle. Runtime enforcement boundary established.
```

## Bloc: Architecture Source

```yaml
id: architecture-source
type: governance
status: active
role: Structured source of truth for blocks, dependencies, impacts, files, contracts, tests and risks.
responsibilities:
  - Describe architecture blocks
  - Feed generated relation views
  - Support impact analysis before coding
depends_on:
  - governance-core
  - contract-tooling
impacts:
  - dependency mapping
  - refactoring impact analysis
  - sensitive zone visualization
  - agentic coding framing
files:
  - docs/ARCHITECTURE.md
  - docs/RELATIONS.md
  - docs/adr/*.md
  - docs/PILOTAGE.md
  - tools/vbb-architecture.py
  - tests/test_vbb_architecture.py
  - scripts/vbb-ci-local.sh
  - .github/workflows/vbb-contracts.yml
  - skills/t-vbb-dependency-mapper/SKILL.md
  - skills/t-vbb-impact-analyzer/SKILL.md
contracts:
  - t-vbb-dependency-mapper
  - t-vbb-impact-analyzer
tests:
  - tests/test_vbb_architecture.py
risks:
  - id: ARCH-001
    level: P1
    note: The projection must never become a competing source of truth.
```

## Bloc: Distribution Setup

```yaml
id: distribution-setup
type: distribution
status: active
role: Installer and provider adapters for global vibebackbone usage.
responsibilities:
  - Install skills and prompts through symlinks or generated commands
  - Deploy AGENTS.md and SYSTEM.md to supported providers
  - Support idempotent install and uninstall
depends_on:
  - governance-core
  - skills-catalog
  - prompt-library
impacts:
  - Claude Code integration
  - Codex integration
  - Pi integration
  - OpenCode integration
files:
  - setup.sh
  - tests/smoke-install.sh
  - scripts/vbb-ci-local.sh
  - .github/workflows/vbb-contracts.yml
  - docs/DEPLOYMENT.md
contracts: []
tests:
  - tests/smoke-install.sh
risks:
  - id: SETUP-001
    level: P1
    note: Adapter counts can diverge from canonical catalog counts.
```

## Bloc: Quality Conventions

```yaml
id: quality-conventions
type: governance
status: active
role: Canonical quality conventions covering readability, modularity, and coherence. Single source of truth for structural standards.
principle: One architecture block should represent one clear responsibility.
responsibilities:
  - Define quality pillars (readability, modularity, coherence)
  - Provide canon change process template
  - Reference quality rules from all governance files
  - Support verification loops before implementation declaration
depends_on:
  - governance-core
  - architecture-source
impacts:
  - code readability standards
  - module organization
  - canonical change discipline
  - test quality
  - documentation standards
files:
  - docs/CONVENTIONS.md
  - docs/templates/CANON_CHANGE_PROPOSAL.md.template
contracts:
  - 1-vbb-conventions
  - 1-vbb-formatter
  - 1-vbb-code-janitor
tests:
  - tests/test_vbb_architecture.py
risks:
  - id: QUAL-001
    level: P2
    note: Multiple convention sources can create confusion if not properly cross-referenced.
```

## Bloc: Audit Memory

```yaml
id: audit-memory
type: data
status: active
role: Persistent audit, risk and session-state memory for the repository.
responsibilities:
  - Track global audit status
  - Store timestamped audit reports
  - Preserve run artifacts and closeouts
  - Document temporal provenance
depends_on:
  - governance-core
  - architecture-source
impacts:
  - session resume
  - release readiness
  - implementation risk register
files:
  - docs/AUDIT_STATUS.md
  - docs/audits/*.md
  - docs/runs/**/*.md
  - docs/TEMPORAL_PROVENANCE.md
  - docs/TECH_DEBT.md
  - docs/templates/CANON_CHANGE_PROPOSAL.md.template
contracts:
  - 3-vbb-risk-register
  - t-vbb-session-handoff
tests:
  - tests/test_context_compactor.py
  - tests/test_status_dashboard.py
risks:
  - id: MEM-001
    level: P2
    note: Historical or future-dated evidence must not be copied as live downstream state.
```
