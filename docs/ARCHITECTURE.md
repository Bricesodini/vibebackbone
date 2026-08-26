---
context_role: canonical-architecture
phase: transverse
status: active
updated: 2026-08-26
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
  - Require governed capitalization after qualified implementation
  - Keep AGENTS.md as a compact source file, not a recursively generated artifact
  - Load one bounded repository-local operational contract before project state
depends_on: []
impacts:
  - task triage
  - audit routing
  - session startup
  - session closeout
  - engineering knowledge promotion
files:
  - AGENTS.md
  - SYSTEM.md
  - docs/CONTEXT.md
  - docs/PILOTAGE.md
  - docs/PROJECT_MODE.md
  - docs/SESSION_RULES.md
  - docs/CONVENTIONS.md
  - docs/LOCAL_AGENT_CONTRACTS.md
  - tools/vbb-local-agents.py
  - skills/vibebackbone/**
contracts:
  - vibebackbone
  - 0-vbb-pilotage
  - 0-vbb-standard
tests:
  - tests/test_loop_closure.py
  - tests/test_status_dashboard.py
  - tests/test_local_agents_bootstrap.py
risks:
  - id: GOV-001
    level: P2
    note: Governance duplication can create conflicting operational truth.
  - id: GOV-002
    level: P2
    note: A local operational contract must not alter VBB governance or escape its Git-root boundary.
```

## Bloc: Documentary Contract

```yaml
id: documentary-contract
type: governance
status: active
role: Canonical documentary model for identity, qualification, relations, transition and contract observability.
responsibilities:
  - Define stable documentary identity independently of path or representation
  - Qualify artefacts on orthogonal ontology dimensions
  - Record provenance and competing documentary relations
  - Route documentary findings through human decision before remediation
  - Expose documentary contract compatibility without granting authority
depends_on:
  - governance-core
impacts:
  - document authority
  - documentary transitions
  - agent startup and routing
  - source and projection provenance
files:
  - docs/document-model/DOCUMENT_IDENTITY_MODEL.md
  - docs/document-model/DOCUMENT_ONTOLOGY.md
  - docs/document-model/DOCUMENT_GRAPH_MODEL.md
  - docs/document-model/DOCUMENT_TAG_SPECIFICATION.md
  - docs/document-model/DOCUMENT_TRANSITION_PROTOCOL.md
  - docs/document-model/DOCUMENT_MODEL_REFERENCE_ARCHITECTURE.md
  - .vbb/document-convention.yaml
contracts:
  - vbb-doc-v1
tests:
  - tests/test_document_model_validation_pilot.py
  - tests/test_documentary_skills_dtp_alignment.py
risks:
  - id: DOC-001
    level: P1
    note: Unqualified artefacts must remain UNKNOWN and historical evidence must not become current authority.
```

## Bloc: Engineering Knowledge Governance

```yaml
id: engineering-knowledge-governance
type: governance
status: active
role: Single authority for reusable engineering-learning maturity, evidence,
  independent review, human promotion and governed supersession.
responsibilities:
  - Require Knowledge Harvest at formal closeout
  - Separate delivery PASS from knowledge promotion
  - Define OBSERVATION, CANDIDATE, VALIDATED and CANONICAL maturity
  - Qualify evidence independence against the claimed scope
  - Require knowledge audit, distinct independent review and human decision
  - Move promoted rules to one final authority
  - Prevent direct semantic edits to canonical knowledge versions
depends_on:
  - governance-core
impacts:
  - audit routing
  - decision authority
  - independent review
  - session closeout
  - canonical change integration
  - knowledge record lifecycle
files:
  - docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md
  - docs/templates/KNOWLEDGE_RECORD.md.template
contracts: []
tests:
  - tests/test_loop_closure.py
  - tests/test_engineering_knowledge_governance.py
risks:
  - id: KNO-001
    level: P1
    note: A candidate, playbook or run can create parallel truth if treated as authority.
  - id: KNO-002
    level: P1
    note: Scope inflation can promote evidence beyond the independence it demonstrates.
```

## Bloc: Gate Assurance Governance

```yaml
id: gate-assurance-governance
type: governance
status: active
role: Canonical taxonomy and schema for Design, Certification and Other gate assurance.
responsibilities:
  - Preserve local PASS and FAIL while qualifying gate family and checkpoint
  - Keep subject assurance orthogonal to runtime FINAL_STATUS
  - Enforce explicit fail-closed implementation authorization
  - Define separate Design and Certification review profiles
  - Preserve historical runs and consumer projects
  - Keep Knowledge Harvest at closeout
depends_on:
  - governance-core
  - engineering-knowledge-governance
impacts:
  - pre-implementation gates
  - independent review
  - implementation authorization
  - closeout
  - four-distribution governance
files:
  - docs/GATE_ASSURANCE_GOVERNANCE.md
  - docs/templates/01_INTAKE.md.template
  - docs/templates/04_PLAN.md.template
  - docs/templates/06_REVIEW.md.template
  - docs/templates/07_CLOSEOUT.md.template
  - prompts/canonical/06-p-vbb-review.md
  - prompts/canonical/07-p-vbb-closeout.md
  - tools/vbb-loop-closure-check.py
contracts: []
tests:
  - tests/test_loop_closure.py
risks:
  - id: ASR-001
    level: P1
    note: Misclassifying a behavioral contradiction as Certification can preserve a false Design PASS.
  - id: ASR-002
    level: P1
    note: Inferring authorization from PASS verdicts can bypass required gates.
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
  - Distinguish SKILL.md functional versions from CONTRACT.yaml schema versions
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
  - docs/REFERENCE/scoped-audit-protocol.md
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
  - Map advertised prompt short names to concrete Markdown files
depends_on:
  - governance-core
  - skills-catalog
  - engineering-knowledge-governance
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
role: Local validation, security gates, dry-run runtime, route lookup, measured status and closure tooling.
responsibilities:
  - Lint skill contracts
  - Prevent newly added credential-like content from entering commits and CI
  - Bootstrap project-owned governance once and refresh VBB-managed hook assets only with verified provenance
  - Execute contract dry-runs
  - Route queries to skills
  - Report documentary and measured repository status separately
  - Enforce structured long-run declarations during strict closure
  - Evaluate provider-neutral runtime conformance with decomposed decisions,
    multidimensional safety scoring and no mandatory LLM calls
depends_on:
  - skills-catalog
  - governance-core
impacts:
  - CI confidence
  - release readiness
  - implementation-readiness audits
files:
  - pyproject.toml
  - requirements-dev.txt
  - tools/vbb-contract-lint.py
  - tools/vbb-contract-runtime.py
  - tools/vbb-executor.py
  - tools/vbb-phase-router.py
  - tools/vbb-project-init.py
  - tools/vbb-status-dashboard.py
  - tools/vbb-loop-closure-check.py
  - tools/vbb-gate-check.py
  - tools/vbb-credentials-gate.py
  - tools/vbb_run_resolution.py
  - tools/vbb_runtime_conformance.py
  - conformance/**
  - scripts/hooks/pre-commit-framework-gate
  - scripts/install-vbb-hooks.sh
contracts:
  - t-vbb-status-dashboard
  - t-vbb-index
  - t-vbb-mode-transition-gate
  - t-vbb-deploy-runtime
tests:
  - tests/test_contract_lint.py
  - tests/test_executor.py
  - tests/test_status_dashboard.py
  - tests/test_loop_closure.py
  - tests/test_run_resolution.py
  - tests/test_gate_check_adr_linkage.py
  - tests/test_credentials_gate.py
  - tests/test_install_vbb_hooks.sh
  - tests/test_project_init.py
  - tests/test_static_quality_ci.py
  - tests/test_runtime_conformance.py
risks:
  - id: TOOL-001
    level: P2
    note: Formal executor boundary is active and directly tested; nested status, depth progression, circular gate blocking, YAML loading and closeout writing are characterized by tests/test_executor.py, and the module passes mypy.
  - id: TOOL-002
    level: P2
    note: Run resolution is shared via tools/vbb_run_resolution.py (ADR-0027, TD-101) with two declared selectors (latest existing / latest closed). Hook installation converges on scripts/install-vbb-hooks.sh (TD-102); legacy installers are deprecated redirects.
  - id: TOOL-003
    level: P1
    note: Credentials enforcement is shared by the staged hook and commit-range CI through tools/vbb-credentials-gate.py (ADR-0033); detection is differential and intentionally not exhaustive.
  - id: TOOL-004
    level: P2
    note: Consumer hook assets use a SHA-256 provenance manifest and full-bundle preflight (ADR-0034); project-owned documents remain generated-once and are never part of managed refresh.
  - id: TOOL-005
    level: P1
    note: Effective readiness conservatively combines documentary truth with local Git, source-integrity and explicitly parsed open-risk measurements; missing, invalid or contradictory risk sources are UNKNOWN/blocking, and each result exposes the exact repository SHA (ADR-0046, RR-BK-05).
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
  - Replace stale Codex generated governance blocks, including nested legacy markers
  - Migrate legacy Codex governance symlinks without following writes into Core sources
  - Reject compilation when a canonical governance source contains runtime markers
  - Source routeur `setup.sh` (no provider logic inline) into per-distribution `setup.sh`
  - Limit official provider support to Pi, OpenCode, Codex and Claude Code
  - Compare observable governance behavior through one shared Core protocol
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
  - setup.sh                          # routeur (sources Core + four provider adapters)
  - setup-lib.sh                      # shared helpers (relpath, symlink, backup, prompt commands)
  - core/setup.sh                     # pre-flight + universal symlinks (~116 LOC)
  - distributions/claude/setup.sh     # settings.json + CLAUDE.md block + 26 commands
  - distributions/codex/setup.sh      # compiled AGENTS.md block (VBB:START/END markers)
  - distributions/pi/setup.sh         # symlinks AGENTS + SYSTEM + 26 prompts
  - distributions/opencode/setup.sh   # opencode.json instructions + 26 commands
  - conformance/**                    # shared scenarios, schema, and CLI adapters
  - tools/vbb_runtime_conformance.py  # deterministic evaluator + opt-in live runner
  - tests/test_setup_smoke.sh
  - scripts/vbb-ci-local.sh
  - .github/workflows/vbb-contracts.yml
  - docs/DEPLOYMENT.md
contracts: []
tests:
  - tests/test_setup_smoke.sh
  - tests/smoke-install.sh
  - tests/test_runtime_conformance.py
risks:
  - id: SETUP-001
    level: P1
    note: Adapter counts can diverge from canonical catalog counts.
  - id: SETUP-002
    level: P1
    note: Runtime destinations must never be followed into Core sources; Codex migration and uninstall enforce this boundary under ADR-0046.
  - id: SETUP-003
    level: P2
    note: Optional live adapters depend on external provider CLI schemas; deterministic CI remains provider-neutral and network-free under ADR-0047.
```

## Bloc: Quality Conventions

```yaml
id: quality-conventions
name: Quality Conventions
type: governance
status: active
role: Canonical quality conventions covering P1 Readability, P2 Modularity,
  P3 Coherence & Convergence, P4 Traceability/Traçabilité (embedded), and
  P5 Robustness (P.R1–P.R8). Single source of truth for structural standards.
  Defined in docs/CONVENTIONS.md — this block mirrors it for architecture coverage.
principle: One architecture block should represent one clear responsibility.
responsibilities:
  - Define five quality pillars (readability, modularity, coherence, traceability, robustness)
  - Provide canon change process template
  - Reference quality rules from all governance files
  - Support verification loops before implementation declaration
  - Enforce fail-explicit rule, gate-before-action, invariant protection
  - Enforce regression prevention and independent review preferred
  - Maintain traceability through ADRs, run artifacts, audit reports,
    ARCHITECTURE.md, risk register, session handoff, and temporal provenance
depends_on:
  - governance-core
  - architecture-source
  - engineering-knowledge-governance
impacts:
  - code readability standards
  - module organization
  - canonical change discipline
  - test quality
  - documentation standards
  - error handling consistency
  - invariant protection
  - regression prevention
files:
  - docs/CONVENTIONS.md
  - docs/templates/CANON_CHANGE_PROPOSAL.md.template
  - docs/runs/2026-05-29_1000_robustness-audit/ROBUSTNESS_AUDIT.md
  - docs/runs/2026-05-29_1000_robustness-audit/PILLAR_5_PROPOSAL.md
contracts:
  - 1-vbb-conventions
  - 1-vbb-formatter
  - 1-vbb-code-janitor
  - t-vbb-anti-slop-gate
tests:
  - tests/test_vbb_architecture.py
risks:
  - id: QUAL-001
    level: P2
    note: Multiple convention sources can create confusion if not properly cross-referenced.
  - id: QUAL-002
    level: P2
    note: "P.R8 (independent review preferred) is a soft rule — self-review without disclosure cannot be detected technically and relies on human discipline."
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
  - engineering-knowledge-governance
impacts:
  - session resume
  - release readiness
  - implementation risk register
files:
  - docs/AUDIT_STATUS.md
  - docs/audits/*.md
  - docs/archive/**/*.md
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

## Bloc: External Dependencies

```yaml
id: external-dependencies
type: external
status: active
role: Inventory of out-of-repo dependencies the framework relies on at runtime or install time.
responsibilities:
  - Declare external systems, databases, APIs and third-party services
  - Provide canonical references for cross-service discipline
  - Distinguish in-repo distributions from out-of-repo runtimes
  - Surface declared external dependencies to multi-service discipline (Run 8-11)
depends_on:
  - governance-core
  - architecture-source
impacts:
  - impact analysis
  - cross-service coordination
  - install posture
  - supported-provider runtime posture
files:
  - docs/ARCHITECTURE.md
  - docs/DISTRIBUTIONS.md
contracts: []
tests: []
risks:
  - id: EXT-001
    level: P2
    note: This block is a placeholder declaration. Real external dependencies to be enumerated in subsequent runs (multi-service discipline).
  - id: EXT-002
    level: P2
    note: Drift between declared and actual external dependencies can silently break install/runtime posture.
```
