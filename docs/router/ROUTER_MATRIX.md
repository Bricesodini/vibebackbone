# ROUTER_MATRIX — Detailed prompt decision matrix for Vibebackbone

**Version** : 2.0 | **Date** : 2026-06-12 | **Layer** : L3 — reference, not loaded at boot

> Load via `python tools/vbb-index.py search "router"` or read this file on demand.

Ownership, authority and precedence between canonical prompts, specialized
prompts, this router and installed short names are defined once in
[`PROMPTS_ARCHITECTURE.md` § Matrice de responsabilité et d'autorité](../../PROMPTS_ARCHITECTURE.md).
This document keeps only the detailed phase/context selection matrix.

---

## Prompt architecture structure

```
prompts/
├── canonical/          ← Generic phase prompts (cover protocol 01–07)
│   ├── 01-p-vbb-intake.md
│   ├── 02-p-vbb-audit.md
│   ├── 03-p-vbb-decision.md
│   ├── 04-p-vbb-plan.md
│   ├── 05-p-vbb-execution.md
│   ├── 06-p-vbb-review.md
│   └── 07-p-vbb-closeout.md
│
└── (root)              ← Specialized prompts (domain or specific context)
    ├── 0-p-vbb-triage.md
    ├── 0-p-vbb-plan.md
    ├── 0-p-vbb-before-building.md
    ├── 1-p-vbb-quick-task.md
    ├── 1-p-vbb-structured-task.md
    ├── 1-p-vbb-tech-debt.md
    ├── 1-p-vbb-legacy-level.md
    ├── 1-p-vbb-doc-feature.md
    ├── 1-p-vbb-post-refacto-coherence.md
    ├── 1-p-vbb-project-init.md
    ├── 2-p-vbb-audit-task.md
    ├── 2-p-vbb-db-sanity.md
    ├── 2-p-vbb-mode-transition.md
    ├── 2-p-vbb-release-check.md
    ├── 2-p-vbb-security-pipeline.md
    ├── 3-p-vbb-risk-register.md
    ├── 4-p-vbb-before-building.md
    ├── 4-p-vbb-after-building.md
    ├── 4-p-vbb-anti-slop.md
    ├── 4-p-vbb-deploy-docker.md
    ├── t-p-vbb-start-session.md
    ├── t-p-vbb-branch-policy-check.md
    ├── t-p-vbb-git-sync.md
    ├── t-p-vbb-sequenced-ship.md
    └── t-p-vbb-session-handoff.md
```

### Base rule

**Canonical prompt** = generic reference, applicable in all contexts.
**Specialized prompt** = better precision for a specific domain or context.

Use canonical by default. Use specialized when the context justifies it.

### When to use a canonical prompt?

- Starting a session without a specific domain context
- Wanting the most generic and maintainable structure
- Unsure which specialized prompt to use
- Onboarding an agent unfamiliar with Vibebackbone

### When to use a specialized prompt?

- You know exactly which domain or tool is concerned
- The specialized prompt covers your exact case (e.g. security, Docker, release)
- You want to save time on phase configuration
- The specialized prompt is noted as "better precision" in the matrix

### Escalation rule

If a specialized prompt covers multiple phases in a single context, **verify**:
- Could it saturate the LLM context? → If yes, split into sessions
- Does it produce all expected artifacts? → If no, complement with canonical

---

## Main matrix

### Phase 01 — INTAKE

| Route | Context | Recommended prompt | Specialized alternatives |
|-------|---------|-------------------|--------------------------|
| MVP START gate | New MVP/from-zero project, RICO, initial brief, code requested before framing | `canonical/01-p-vbb-intake` + skill `0-vbb-rico-readiness` | `0-p-vbb-before-building` only after RICO readiness |
| Any route | Session start, objective to frame | `canonical/01-p-vbb-intake` | `t-p-vbb-start-session` (if session re-entry), `0-p-vbb-triage` (if classification only) |
| FAST-ZERO | Safe micro-task, ≤ 3 files | `0-p-vbb-zero-friction` (Activity Log only) | — |
| FAST-MINIMAL | Small non-trivial task | `0-p-vbb-zero-friction` (Activity Log + 05_PATCH_SUMMARY) | — |
| FAST | Simple task, low risk | `canonical/01-p-vbb-intake` → chain `04_PLAN` or `05_EXECUTION` | `1-p-vbb-quick-task` (if entire task in one prompt) |
| STRUCTURED | Multi-file task or contracts | `canonical/01-p-vbb-intake` | `0-p-vbb-before-building` (if upcoming feature) |
| AUDIT | Security, integrity, compliance | `canonical/01-p-vbb-intake` | `2-p-vbb-audit-task` (if objective is directly audit) |
| CLOSEOUT | End of session or re-entry | `canonical/01-p-vbb-intake` | `t-p-vbb-start-session` (context read only) |
| Repo initialization | First contact with ungoverned repo | `canonical/01-p-vbb-intake` | `1-p-vbb-project-init` (if governance init) |

### MVP START gate sequence

```
canonical/01-p-vbb-intake
    ↓
0-vbb-rico-readiness      ← apply docs/MVP_START_PROTOCOL.md
    ↓
READY   → 04-p-vbb-plan / STRUCTURED execution
PARTIAL → framing only, no application code
BLOCKED → blocking questions only
UNKNOWN → stop before implementation
```

Hard blocks:
- architecture not defined → no code
- data not modeled → no persistence
- deployment constraints absent while infra is requested → no Docker/runtime structure
- critical ambiguity → questions before plan

---

### Phase 02 — AUDIT

| Domain | Context | Recommended prompt | Specialized alternatives |
|--------|---------|-------------------|--------------------------|
| Generic | Audit without specific domain | `canonical/02-p-vbb-audit` | `2-p-vbb-audit-task` (if choosing domain) |
| Security | Vulnerabilities, auth, XSS, injection | `canonical/02-p-vbb-audit` + skill `2-vbb-security` | `2-p-vbb-security-pipeline` (if full 4-step pipeline) |
| Database | DB sanity, migrations, schema | `canonical/02-p-vbb-audit` + skill `2-vbb-db-robustness` | `2-p-vbb-db-sanity` (if sanity eval only) |
| Data integrity | Business invariants, idempotency | `canonical/02-p-vbb-audit` + skill `2-vbb-data-integrity` | — |
| Operations | Deployment, monitoring, infra | `canonical/02-p-vbb-audit` + skill `2-vbb-ops` | — |
| CI/CD | Pipeline, tests, build | `canonical/02-p-vbb-audit` + skill `2-vbb-ci` | — |
| Legal / Compliance | GDPR, licenses, T&Cs | `canonical/02-p-vbb-audit` + skill `2-vbb-legal` | — |
| Systemic risk | Critical dependencies, SPOF, resilience | `canonical/02-p-vbb-audit` + skill `2-vbb-systemic-risk` | — |
| API / Contracts | Interface contracts, breaking changes | `canonical/02-p-vbb-audit` + skill `2-vbb-api-auditor` | — |
| Tech debt | Quality, complexity, coupling | `canonical/02-p-vbb-audit` + skill `1-vbb-tech-debt` | `1-p-vbb-tech-debt` (if debt audit only) |
| Legacy | Legacy level evaluation | `canonical/02-p-vbb-audit` | `1-p-vbb-legacy-level` (if legacy eval only) |
| Surface quality | Slop, typos, code inconsistencies | `canonical/02-p-vbb-audit` + skill `1-vbb-code-janitor` | `4-p-vbb-anti-slop` (if quality gate only, read-only) |
| Pre-release | Multi-domain audit before deploy | `canonical/02-p-vbb-audit` × N (one session per domain) | `2-p-vbb-release-check` (if full pre-release gate) |

---

### Phase 03 — DECISION

| Context | Recommended prompt | Specialized alternatives |
|---------|-------------------|--------------------------|
| Post-audit decision | `canonical/03-p-vbb-decision` | — |
| Mode or transition decision | `canonical/03-p-vbb-decision` | `2-p-vbb-mode-transition` (if dev→prod verdict specifically) |
| Branch strategy validation | `canonical/03-p-vbb-decision` | `t-p-vbb-branch-policy-check` (if Git branch specifically) |
| Risk consolidation | `canonical/03-p-vbb-decision` | `3-p-vbb-risk-register` (if compiling risk register) |
| Multi-domain post-audit prioritization | `canonical/03-p-vbb-decision` | `3-p-vbb-risk-register` after `2-p-vbb-release-check` |

---

### Phase 04 — PLAN

| Context | Recommended prompt | Specialized alternatives |
|---------|-------------------|--------------------------|
| Generic plan | `canonical/04-p-vbb-plan` | `0-p-vbb-plan` (if short plan, fast route) |
| Pre-feature plan | `canonical/04-p-vbb-plan` | `0-p-vbb-before-building` or `4-p-vbb-before-building` (if pre-feature gate) |
| Structured multi-file plan | `canonical/04-p-vbb-plan` | `1-p-vbb-structured-task` (if complete task with integrated plan) |
| Docker deployment plan | `canonical/04-p-vbb-plan` | `4-p-vbb-deploy-docker` (if full Docker pipeline) |
| Post-refactor coherence plan | `canonical/04-p-vbb-plan` | `1-p-vbb-post-refacto-coherence` (if post-refactoring) |

---

### Phase 05 — EXECUTION

| Context | Recommended prompt | Specialized alternatives |
|---------|-------------------|--------------------------|
| Generic execution | `canonical/05-p-vbb-execution` | — |
| Fast task (FAST route) | `canonical/05-p-vbb-execution` | `1-p-vbb-quick-task` (if intake + execution in one prompt) |
| Structured task (STRUCTURED route) | `canonical/05-p-vbb-execution` | `1-p-vbb-structured-task` (if plan + execution integrated) |
| Feature documentation | `canonical/05-p-vbb-execution` | `1-p-vbb-doc-feature` (if documentation only) |
| Long multi-run execution | `canonical/05-p-vbb-execution` × N | `t-p-vbb-sequenced-ship` (if long orchestration with context compression) |
| Commit and push | `canonical/05-p-vbb-execution` | `t-p-vbb-git-sync` (if commit/push specifically) |
| Docker deployment | `canonical/05-p-vbb-execution` | `4-p-vbb-deploy-docker` (if full Docker pipeline) |

---

### Phase 06 — REVIEW

| Context | Recommended prompt | Specialized alternatives |
|---------|-------------------|--------------------------|
| Generic review (new session) | `canonical/06-p-vbb-review` | — |
| Post-build validation | `canonical/06-p-vbb-review` | `4-p-vbb-after-building` (if full post-build validation) |
| Pre-publish quality gate | `canonical/06-p-vbb-review` | `4-p-vbb-anti-slop` (if surface quality gate only, read-only) |

---

### Phase 07 — CLOSEOUT

| Context | Recommended prompt | Specialized alternatives |
|---------|-------------------|--------------------------|
| Session closeout | `canonical/07-p-vbb-closeout` | `t-p-vbb-session-handoff` (if re-entry handoff only) |
| Closeout with risk register | `canonical/07-p-vbb-closeout` + `3-p-vbb-risk-register` | — |
| Post-refactor closeout | `canonical/07-p-vbb-closeout` | `1-p-vbb-post-refacto-coherence` (phase 4 of prompt) |

---

## Route sequences

### FAST route

```
01-p-vbb-intake (or 1-p-vbb-quick-task directly)
    ↓
05-p-vbb-execution
    ↓
07-p-vbb-closeout (or t-p-vbb-session-handoff)
```

**Alternatives**: `1-p-vbb-quick-task` chains 01+05 in one session.

---

### STRUCTURED route

```
01-p-vbb-intake (or t-p-vbb-start-session)
    ↓
04-p-vbb-plan (or 0-p-vbb-plan)
    ↓
05-p-vbb-execution (Run 1, Run 2...)
    ↓
06-p-vbb-review      ← NEW SESSION MANDATORY
    ↓
07-p-vbb-closeout
```

**Alternatives**: `1-p-vbb-structured-task` chains 01+04+05. Complete with 06 and 07 in separate sessions.

---

### AUDIT route

```
01-p-vbb-intake
    ↓
02-p-vbb-audit       ← NEW SESSION RECOMMENDED
    ↓
03-p-vbb-decision    ← NEW SESSION MANDATORY (decider ≠ auditor)
    ↓
04-p-vbb-plan
    ↓
05-p-vbb-execution
    ↓
06-p-vbb-review      ← NEW SESSION MANDATORY
    ↓
07-p-vbb-closeout
```

**Alternatives**:
- Security audit: `2-p-vbb-security-pipeline`
- Pre-release audit: `2-p-vbb-release-check`
- Tech debt audit: `1-p-vbb-tech-debt`
- Post-refactor audit: `1-p-vbb-post-refacto-coherence`

---

### CLOSEOUT route

```
01-p-vbb-intake (or t-p-vbb-start-session for context read)
    ↓
07-p-vbb-closeout (or t-p-vbb-session-handoff)
```

---

## Session rules

| Transition | New session? |
|-----------|-------------|
| 01 → 02 | ⚠️ Recommended (distinct auditor) |
| 02 → 03 | ✅ Mandatory (decider ≠ auditor) |
| 03 → 04 | ⚠️ Recommended (distinct planner) |
| 04 → 05 | ⚠️ Recommended (distinct executor) |
| 05 → 06 | ✅ Mandatory (reviewer ≠ executor) |
| 06 → 05 (mods required) | ✅ Mandatory |
| 06 → 07 | ⚠️ Recommended |
| 05 Run N → 05 Run N+1 | ✅ Same session if <3 runs |

Source: `docs/SESSION_RULES.md`

---

## Artifact naming convention

| Phase | Artifact | Location |
|-------|----------|----------|
| 01 | `01_INTAKE.md` | `docs/runs/YYYY-MM-DD_HHmm_slug/` |
| 02 | `02_AUDIT_REPORT.md` | `docs/runs/.../` + `docs/audits/{type}-YYYYMMDD-HHMM.md` |
| 03 | `03_DECISION_RECORD.md` | `docs/runs/.../` |
| 04 | `04_FIX_PLAN.md` | `docs/runs/.../` |
| 05 | `05_PATCH_SUMMARY_RUN_N.md` | `docs/runs/.../` |
| 06 | `06_REVIEW_RUN_N.md` | `docs/runs/.../` |
| 07 | `07_CLOSEOUT.md` | `docs/runs/.../` |

**Create run directory at session start**:

```
docs/runs/YYYY-MM-DD_HHmm_slug/
```

- `YYYY-MM-DD`: current date (e.g. 2026-05-18)
- `HHmm`: approximate start time (e.g. 1430)
- `slug`: short description (e.g. `security-audit`, `feature-auth`, `patch-xss`)
- Full example: `docs/runs/2026-05-18_1430_security-audit/`

---

## Special cases

### Unknown or ambiguous task

→ Always start with `canonical/01-p-vbb-intake` or `0-p-vbb-triage`.

### Multi-domain audit

→ One session per audit domain. Don't put everything in `2-p-vbb-release-check` if risk of context saturation.
→ Use `2-p-vbb-release-check` only if LLM context is large and scope clearly bounded.

### Loop 05 → 06 → 05 (modifications required)

```
05-p-vbb-execution (Run 1) → 06-p-vbb-review (MODIFICATIONS REQUIRED)
    ↓ new session
05-p-vbb-execution (Run 2) → 06-p-vbb-review (APPROVED)
    ↓
07-p-vbb-closeout
```

### Escalation during execution

If execution (phase 05) reveals unexpected risk:
→ Stop the run, document in patch summary.
→ Create new session: `01-p-vbb-intake` + AUDIT route.
→ Do not continue in FAST mode if risk has escalated.

### Long work (limited LLM context)

→ Use `t-p-vbb-sequenced-ship` for multi-run orchestration with context compression.
→ Or split into separate sessions with explicit handoff via `t-p-vbb-session-handoff`.

---

## Quick index — By need

| Need | Prompt |
|------|--------|
| Start a session | `t-p-vbb-start-session` or `canonical/01-p-vbb-intake` |
| Classify a task | `0-p-vbb-triage` |
| Plan before a feature | `0-p-vbb-before-building` or `canonical/04-p-vbb-plan` |
| Simple fast task | `1-p-vbb-quick-task` |
| Structured task | `1-p-vbb-structured-task` |
| Tech debt audit | `1-p-vbb-tech-debt` |
| Evaluate legacy | `1-p-vbb-legacy-level` |
| Document a feature | `1-p-vbb-doc-feature` |
| Post-refactor audit | `1-p-vbb-post-refacto-coherence` |
| Generic audit | `canonical/02-p-vbb-audit` or `2-p-vbb-audit-task` |
| Security audit | `2-p-vbb-security-pipeline` |
| Database audit | `2-p-vbb-db-sanity` |
| Dev→prod transition | `2-p-vbb-mode-transition` |
| Pre-release gate | `2-p-vbb-release-check` |
| Compile risks | `3-p-vbb-risk-register` |
| Validate before building | `4-p-vbb-before-building` |
| Validate after building | `4-p-vbb-after-building` |
| Surface quality gate | `4-p-vbb-anti-slop` |
| Docker deployment | `4-p-vbb-deploy-docker` |
| Check Git strategy | `t-p-vbb-branch-policy-check` |
| Commit and push | `t-p-vbb-git-sync` |
| Long multi-run work | `t-p-vbb-sequenced-ship` |
| Close a session | `canonical/07-p-vbb-closeout` or `t-p-vbb-session-handoff` |

---

_vibebackbone ROUTER MATRIX v2.0 — 2026-06-12 · Extracted from t-p-vbb-phase-router_
