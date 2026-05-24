# AUDIT_STATUS — [Your Project]

Dashboard tracking audit progress, findings, and risk status.

## Phase [0] — Readiness

| Skill | Status | Risk | Date | Notes |
|-------|--------|------|------|-------|
| scope-freeze | ⏳ Pending | — | — | Required before [1] |
| audit-readiness | ⏳ Pending | — | — | Gatekeeper for [1] |

**[0] Verdict**: ⏳ Pending

---

## Phase [1] — Structure

| Skill | Status | Risk | Date | Notes |
|-------|--------|------|------|-------|
| dependency-mapper | ⏳ Pending | — | — | **Blocking**: required before [2] |
| conventions | ⏳ Pending | — | — | Code style + naming |
| tech-debt | ⏳ Pending | — | — | Structural issues |
| formatter | ⏳ Pending | — | — | Code formatting |
| code-janitor | ⏳ Pending | — | — | Dead code cleanup |

**[1] Verdict**: ⏳ Pending

---

## Phase [2] — Deep Audits

| Skill | Status | Risk | Date | Notes |
|-------|--------|------|------|-------|
| security | ⏳ Pending | — | — | Vulns, injection, auth |
| api-auditor | ⏳ Pending | — | — | API design + robustness |
| db-robustness | ⏳ Pending | — | — | Database integrity |
| data-integrity | ⏳ Pending | — | — | Data consistency |
| ops | ⏳ Pending | — | — | Deployment + monitoring |
| ci | ⏳ Pending | — | — | CI/CD pipeline |
| impact-analyzer | ⏳ Pending | — | — | Change impact |
| test-coverage-mapper | ⏳ Pending | — | — | Test coverage |

**[2] Verdict**: ⏳ Pending

---

## Phase [3] — Consolidation

| Skill | Status | Risk | Date | Notes |
|-------|--------|------|------|-------|
| risk-register | ⏳ Pending | — | — | Consolidates all findings |

**[3] Verdict**: ⏳ Pending

---

## Risk summary

### P0 (Critical)
Findings that block deployment:

- [ ] [Risk description] — Skill: [skill-name] — Owner: [name]
- [ ] [Risk description] — Skill: [skill-name] — Owner: [name]

**Count**: 0 / ∞ blocking

### P1 (Major)
Findings that must be fixed before release:

- [ ] [Risk description] — Skill: [skill-name] — Owner: [name]

**Count**: 0

### P2 (Minor)
Findings for next version:

- [ ] [Risk description] — Skill: [skill-name] — Owner: [name]

**Count**: 0

### P3 (Info)
Findings to monitor:

- [ ] [Risk description] — Skill: [skill-name] — Owner: [name]

**Count**: 0

---

## Summary

| Metric | Value | Status |
|--------|-------|--------|
| **Skills completed** | 0 / 17 | ⏳ Pending |
| **P0 risks** | 0 | ✓ Clean |
| **P1 risks** | 0 | ✓ Clean |
| **P2 risks** | 0 | — |
| **P3 risks** | 0 | — |
| **Overall verdict** | ⏳ Pending | — |

---

## Release checklist

- [ ] Phase [0] readiness: READY
- [ ] Phase [1] structure: READY
- [ ] Phase [2] audits: READY (or accepted P1/P2 risks)
- [ ] Phase [3] risk-register: COMPLETE
- [ ] P0 risks: 0 (no blockers)
- [ ] P1 risks: mitigated or accepted
- [ ] Team sign-off: obtained
- [ ] Deployment plan: documented

**Release decision**: ⏳ Pending

---

## Notes & escalations

### Escalation 1: [Title]
- **Date**: [DATE]
- **Issue**: [Description]
- **Escalated to**: [Name/team]
- **Status**: OPEN | RESOLVED | DEFERRED
- **Notes**: [Any notes]

---

## Historical reference

Previous audits (if any):

- [Previous audit date]: [Verdict]
- [Previous audit date]: [Verdict]

---

**Last updated**: [DATE TIME]
**Dashboard owner**: [Name]
**Next review**: [Target date]

*Instructions: Update after each skill execution. Use status symbols: ⏳ Pending, ⚙️ In progress, ✓ Complete, ✗ Failed. Use risk levels: P0 (critical), P1 (major), P2 (minor), P3 (info).*
