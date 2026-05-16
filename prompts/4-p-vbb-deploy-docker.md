---
description: Run a full Vibebackbone Docker deployment pipeline
---

Handle this as a Vibebackbone DEPLOY-DOCKER pipeline: $@

Objective:
Execute a full Docker deployment pipeline grounded in Vibebackbone governance,
with audit-before-generate and generate-before-deploy sequencing, and
zero-data-loss gates at every stage.

Preferred Vibebackbone skills:

- `t-vbb-docker-audit`
- `t-vbb-docker-generate`
- `t-vbb-deploy-runtime`

Skill routing rule:

- Use `t-vbb-docker-audit` as mandatory stage 1 (read-only scan).
- Use `t-vbb-docker-generate` as stage 2 only after audit verdict is READY or PARTIAL.
- Use `t-vbb-deploy-runtime` as stage 3 only after generate verdict is READY or PARTIAL.
- If any stage returns BLOCKED, stop the pipeline and report why.
- If any stage returns UNKNOWN, report and ask for confirmation before continuing.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Confirm why this task follows the DEPLOY-DOCKER pipeline (touches infrastructure, containers, production state, or data integrity).
3. State which governance files are available and relevant.
4. Execute stage 1 — DOCKER AUDIT:
   - Run `t-vbb-docker-audit`
   - Verify that `docs/audits/docker-audit-*.md` was written (mandatory output)
   - If BLOCKED → stop and report
5. Execute stage 2 — DOCKER GENERATE:
   - Run `t-vbb-docker-generate`
   - Verify it reads the audit report from `docs/audits/` (not LLM context alone)
   - Verify that `docs/audits/docker-generate-*.md` was written (mandatory output)
   - Verify that `docker-services.map` was created
   - Generate all Docker artifacts (Dockerfile, compose files, .env, nginx, .dockerignore, service map)
   - Validate compose syntax
   - If BLOCKED → stop and report
6. Execute stage 3 — DEPLOY RUNTIME:
   - Run `t-vbb-deploy-runtime`
   - Verify that deploy.sh reads `docker-services.map` (not heuristics alone)
   - Generate deploy.sh with integrity gates
   - Validate build (dev)
   - If BLOCKED → stop and report
7. Produce final deployment report.

Verdict cascade rule (from PILOTAGE.md):

- READY → continue in all environments
- PARTIAL → dev: continue with warning, staging: confirm with user, prod: BLOCKED
- BLOCKED → stop immediately
- UNKNOWN → dev: confirm with user, staging+: stop

Pipeline execution rules:

- Each stage depends on the previous stage's verdict.
- A PARTIAL verdict allows continuation with explicit warnings.
- A BLOCKED verdict stops the pipeline completely.
- An UNKNOWN verdict requires user confirmation before proceeding.
- Never skip a stage.
- Never execute stages out of order.
- If the target environment is dev only, the pipeline can run in Voie STRUCTURÉE.
- If the target environment includes staging or prod, the pipeline runs in Voie AUDIT.

Recommended pre-audits (non-blocking but strongly recommended for prod):

- `2-vbb-ops`
- `2-vbb-data-integrity`
- `2-vbb-security`
- `2-vbb-db-robustness`

If `docs/AUDIT_STATUS.md` exists, check these pre-audits before stage 3.
If any pre-audit is BLOCKED, warn and ask for explicit confirmation before deploy.

Constraints:

- Do not present the pipeline as complete if any stage was skipped.
- Do not claim Vibebackbone compliance unless governance has been detected and read.
- If governance is missing, say so explicitly and continue as best-effort.
- Zero-data-loss gates in deploy.sh are non-negotiable for staging and prod.
- Never force-continue past a BLOCKED verdict.

Output format:

- Goal
- Why this follows DEPLOY-DOCKER pipeline
- Pipeline path (STRUCTURED or AUDIT)
- Governance used
- Stage 1 — Audit
  - Skill used
  - Verdict
  - Key findings
  - Warnings
- Stage 2 — Generate
  - Skill used
  - Verdict
  - Artifacts created
  - Validation results
  - Warnings
- Stage 3 — Runtime
  - Skill used
  - Verdict
  - deploy.sh status
  - Build test result
  - Pre-audits status
  - Warnings
- Overall pipeline verdict: READY | PARTIAL | BLOCKED
- Next steps
- Escalation needed: yes/no
- Missing evidence / uncertainties
