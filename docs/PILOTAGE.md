# Operational Piloting — vibebackbone

**Version** : 2.2 | **Date** : 2026-06-12 | **Status** : Canonical piloting entry point

---

## Role

Canonical operational entry point for any agent or human piloting vibebackbone. Minimal decision grid: classify, escalate, switch routes.

---

## The 4 routes

| Route | When | Minimum action | Escalate if |
|-------|------|----------------|-------------|
| **FAST-ZERO** | Safe micro-task, ≤ 3 files | `docs/ACTIVITY_LOG.md` only | Risk detected → STRUCTURED |
| **FAST-MINIMAL** | Small non-trivial task | `05_PATCH_SUMMARY` | Risk detected → STRUCTURED |
| **FAST** (STANDARD) | Simple task, low risk | Act directly | Data/auth/security impact → AUDIT |
| **STRUCTURED** | Architecture, contracts, multi-file | Read mode+session+audit → expose plan | Security → AUDIT |
| **AUDIT** | Security, integrity, compliance, systemic risk | Timestamped report in `docs/audits/`, read-only | — |
| **CLOSEOUT** | End of session, handoff, pause | Summarize · decisions · open points → `SESSION.md` + `AUDIT_STATUS.md` | — |

Full details (sequences, alternatives, artifact conventions): [ROUTER_MATRIX.md](router/ROUTER_MATRIX.md)

---

## Triage rule

```
1. Touches data/auth/prod ? → STRUCTURED minimum
2. Touches security/integrity/compliance ? → AUDIT
3. Neither ? → FAST
4. End of session ? → CLOSEOUT
```

---

## Escalation rule

FAST task that reveals impact on data, auth, security, compliance, production, or systemic behavior → **escalate immediately** to STRUCTURED or AUDIT. Never finish in FAST if the risk has changed.

Full procedure (stop, partial closeout, new session): [SESSION_RULES.md § Escalation](SESSION_RULES.md#escalation--new-session)

---

## Verdict cascade × environment

| Verdict | Dev | Staging | Prod |
|---------|-----|---------|------|
| **READY** | Continue | Continue | Continue |
| **PARTIAL** | Continue (warning) | Continue if user confirms | **BLOCK** |
| **BLOCKED** | Stop immediately | Stop immediately | Stop immediately |
| **UNKNOWN** | Continue if user confirms | **Stop** | **Stop** |

Principle: "Fail open = fail dangerous."

---

## Document hierarchy

0. `docs/CONTEXT.md` → MOC, first file to read
1. **This document** → canonical piloting
2. `docs/PROJECT_MODE.md` → mode signal
3. `docs/SESSION.md` → local, gitignored
4. `docs/AUDIT_STATUS.md` → audit dashboard
5. `docs/audits/` · `docs/runs/` → on demand

---

## For more details

- **Route sequences, artifact conventions**: [ROUTER_MATRIX.md](router/ROUTER_MATRIX.md)
- **Session rules**: [SESSION_RULES.md](SESSION_RULES.md)
- **Memory and handoff**: [MEMORY_AND_HANDOFF.md](MEMORY_AND_HANDOFF.md)
- **Repository index**: [docs/INDEX.md](INDEX.md)

---

_vibebackbone Piloting v2.2 — 2026-06-12 · Canonical root entry point_