# t-p-vbb-phase-router — Vibebackbone triage decision

**Version** : 3.0 | **Date** : 2026-06-12

---

## Route decision

0. **MVP START gate**: new MVP/from-zero project, RICO, initial brief, or code requested before framing → skill `0-vbb-rico-readiness` via `docs/MVP_START_PROTOCOL.md`; if not READY, blocking questions only
1. **FAST-ZERO**: safe micro-task, ≤ 3 files, no escalation → `0-p-vbb-zero-friction` (Activity Log only)
2. **FAST-MINIMAL**: small non-trivial task, low risk → `0-p-vbb-zero-friction` (Activity Log + 05_PATCH_SUMMARY)
3. **FAST**: simple task, low risk → `canonical/01-p-vbb-intake` → `05_EXECUTION` (or `1-p-vbb-quick-task` in one prompt)
4. **STRUCTURED**: multi-file task, contracts, or impact > 1 domain → `canonical/01-p-vbb-intake` → full phases
5. **AUDIT**: security, DB, integrity, compliance, systemic risk → AUDIT route mandatory
6. **CLOSEOUT**: end of session or re-entry → `canonical/07-p-vbb-closeout` or `t-p-vbb-session-handoff`

**In doubt** → start with `canonical/01-p-vbb-intake` or `0-p-vbb-triage`.

---

## Mandatory escalations

- Execution reveals unexpected risk → **stop**, document, route AUDIT
- FAST touches: data, auth, security, compliance, prod → **escalate** to STRUCTURED or AUDIT
- Specialized prompt may saturate context → **split** into sessions
- MVP/from-zero readiness is PARTIAL, BLOCKED, or UNKNOWN → **no code**, ask or document blocking questions
- Data not modeled → **no persistence**
- Architecture not defined → **no implementation**

---

## Fallbacks

- `python tools/vbb-index.py search "query"` — find prompt or skill by keyword
- `python tools/vbb-status-dashboard.py` — repo state
- `docs/router/ROUTER_MATRIX.md` — detailed matrix (phases 01-07, alternatives, sequences, conventions)

---

## Canonical vs. specialized

**Canonical** by default (generic, maintainable). **Specialized** when the context is precise and the prompt covers the exact case.

Details: `docs/router/ROUTER_MATRIX.md` § "Base rule" and § "When to use canonical / specialized"

---

_vibebackbone PHASE ROUTER v3.0 — 2026-06-12 · Lightweight router, detailed matrix in docs/router/ROUTER_MATRIX.md_
