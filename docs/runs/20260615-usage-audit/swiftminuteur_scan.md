# SwiftMinuteur — Vibe Backbone Usage Audit

**Date**: 2026-06-15
**Project path**: `/Users/bricesodini/02_dev/Swift/Swiftminuteur`
**Project type**: SwiftUI/SwiftData multi-platform app (iOS 18+, iPadOS 18+, macOS 15+)
**VBB adoption**: 🟢 **STRONG** — Project was initialized with VBB governance from commit #1

---

## 1. Governance Docs

| Document | Present | VBB Lineage | Evidence | Active |
|----------|---------|-------------|----------|--------|
| `docs/CONTEXT.md` | ✅ YES | ✅ Confirmed | References "Vibebackbone governance" in commit history table; "Vibe Backbone" in design system section; follows VBB living-context format with Status, Runs, Architecture, Decisions, Bugs, Checklist, Next Action | 🟢 Active (updated 2026-06-14) |
| `docs/PROJECT_MODE.md` | ✅ YES | ✅ Confirmed | References "Vibe Backbone" in MVP criteria; has "Modes Vibebackbone" table (EXPLORE/MVP/HARDEN/MAINTAIN); current mode: EXPLORE | 🟢 Active (updated 2025-06-13) |
| `docs/PILOTAGE.md` | ✅ YES | ✅ Confirmed | VBB-style pilotage: Objectif, Périmètre (In-scope/Out-of-scope), Contraintes, Décisions majeures (D1-D5), Risques with mitigation | 🟢 Active (updated 2025-06-13) |
| `docs/SESSION.md` | ✅ YES | ✅ Confirmed | VBB-style session tracking: État (PAUSED), Ce qui est fait, Décisions actées, Validation (references vbb-loop-closure-check.py, vbb-ci-local.sh), Prochaines étapes, Points de vigilance | 🟢 Active (updated 2026-06-14) |
| `docs/AUDIT_STATUS.md` | ✅ YES | ✅ Confirmed | VBB-style audit status: Statut global (🟡 PARTIAL), Vérifications d'audit table, Dette technique, Historique des audits (5 entries, first: "Initialisation Vibebackbone") | 🟢 Active (updated 2026-06-14) |
| `docs/CONVENTIONS.md` | ✅ YES | ✅ Confirmed | Explicitly states "Ce document complète la gouvernance Vibebackbone"; has Piliers, Sources canoniques, Structure du code, UI/UX, Qualité de code, Tests sections | 🟢 Active (updated 2026-06-14) |
| `docs/MVP_START_PROTOCOL.md` | ✅ YES | ✅ Confirmed | VBB-style MVP protocol: Prérequis, Checklist de readiness, Ce qui N'EST PAS requis, Déclenchement, Définition du MVP; references "Vibe Backbone" for design system | 🟢 Active (updated 2025-06-13) |
| `docs/TEST_CHECKLIST.md` | ✅ YES | ✅ Confirmed | VBB-style test checklist: Onboarding, Dashboard, Actions minuteur, Overtime, Sessions, Dark Mode, Accessibilité, Mode Display, Build macOS | 🟢 Active (undated) |

### Additional Governance Docs (checked, not found)

| Document | Present |
|----------|---------|
| `ARCHITECTURE.md` | ❌ NO |
| `RELATIONS.md` | ❌ NO |
| `INDEX.md` | ❌ NO |
| `TECH_DEBT.md` | ❌ NO |
| `ACTIVITY_LOG.md` | ❌ NO |
| `DECISIONS.md` | ❌ NO |
| `SESSION_RULES.md` | ❌ NO |
| `DEPLOYMENT.md` | ❌ NO |
| `DISTRIBUTIONS.md` | ❌ NO |
| `LLM_PROVIDERS.md` | ❌ NO |
| `LONG_RUN_RULE.md` | ❌ NO |
| `MEMORY_AND_HANDOFF.md` | ❌ NO |
| `RUNBOOK.md` | ❌ NO |
| `TEMPORAL_PROVENANCE.md` | ❌ NO |
| `TROUBLESHOOTING.md` | ❌ NO |

**Assessment**: Core VBB governance docs (8/8) are present and active. Extended docs (0/15) are absent — typical for a project in EXPLORE mode.

---

## 2. Templates

| Element | Present | Details |
|---------|---------|---------|
| `docs/templates/` directory | ❌ NO | Directory does not exist |

**Assessment**: No VBB templates directory. The project may not have needed template-based document generation yet.

---

## 3. Run Artifacts

| Run Directory | Phases Present | Missing Phases | Status |
|---------------|---------------|-----------------|--------|
| `docs/runs/20260613-swiftminuteur-fix/` | `01_INTAKE.md`, `07_CLOSEOUT.md` | 02_AUDIT, 03_DECISION, 04_PLAN, 05_EXECUTION, 05_PATCH_SUMMARY, 06_REVIEW, POC | 🟡 PARTIAL |
| `docs/runs/20260614-swiftminuteur-handoff/` | `01_INTAKE.md`, `07_CLOSEOUT.md` | 02_AUDIT, 03_DECISION, 04_PLAN, 05_EXECUTION, 05_PATCH_SUMMARY, 06_REVIEW, POC | 🟡 PARTIAL |

**Evidence of VBB lineage in runs**:
- `20260614-swiftminuteur-handoff/07_CLOSEOUT.md` (lines 72-77): explicitly runs VBB tools:
  - `python .../vbb-architecture.py lint` ✅
  - `python .../vbb-architecture.py graph --write` ✅
  - `python .../vbb-contract-lint.py` ✅
  - `python .../vbb-loop-closure-check.py ... --strict` ✅
  - `pytest tests/ -q` in vibebackbone ✅
  - `bash scripts/vbb-ci-local.sh` in vibebackbone ✅
- Both runs use VBB-style frontmatter: `run_id`, `phase`, `route`, `voie`, `status`, `agent`, `started_at`, `ended_at`, `artifacts_consumed`, `artifacts_produced`

**Assessment**: 2 runs present with VBB-style structure but only INTAKE + CLOSEOUT phases (FAST-MINIMAL/CLOSEOUT route pattern). Full VBB phase structure (8 phases) not used — consistent with EXPLORE mode fast iteration.

---

## 4. Audit Artifacts

| Audit File | VBB Lineage | Evidence |
|------------|-------------|----------|
| `docs/audits/a11y-20260614-1420.md` | ✅ YES | Explicitly references **"Skill: 2-vbb-accessibility v1.0"** (line 7); follows VBB audit format with Verdict, Metrics, Violations (P0/P1/P2), High-risk components |
| `docs/audits/core-operational-audit-20260614-0749.md` | ✅ YES | VBB-style audit: Verdict (PARTIAL), Résumé exécutif, Périmètre audité, Findings (CORE-001 to CORE-006 with Sévérité/Évidence/Impact/Action), Priorités recommandées |
| `docs/audits/logic-duplication-20260614-1150.md` | ✅ YES | VBB-style audit: Verdict (PARTIAL), Fingerprint clusters, Findings (DUPE-01 to DUPE-03), Divergent implementations, Recommended canonical sources |
| `docs/audits/pass-2-output.md` | ✅ YES | VBB-style interaction coherence audit: Inherited Warnings, Inconsistency Report, Canonical Patterns Reference, Standardization Proposals, Human Decision Required |
| `docs/audits/spec-validation-20260614-1112.md` | ✅ YES | VBB-style validation: Verdict (COVERED), Référence auditée, Exigences vérifiées (REQ-001 to REQ-004), Lecture de conformité, Écarts |
| `docs/audits/tech-debt-20260613-1639.md` | ✅ YES | VBB-style tech debt audit: Verdict (PARTIAL), Repository inventory, Canonical vs legacy mapping, Findings (TD-001 to TD-003), Priority roadmap |
| `docs/audits/tech-debt-20260614-0627.md` | ✅ YES | VBB-style tech debt audit: Verdict (PARTIAL), Findings (TD-001 to TD-005), Priority roadmap |
| `docs/audits/tech-debt-20260614-1150.md` | ✅ YES | VBB-style tech debt audit: Verdict (PARTIAL), Findings (TD-001 to TD-005), VERDICT RULES section |

**Assessment**: 8 audit files, all VBB-style. One explicitly references a VBB skill (`2-vbb-accessibility`). Audit density is high for an EXPLORE-mode project — indicates strong VBB discipline.

---

## 5. ADRs

| Element | Present | Details |
|---------|---------|---------|
| `docs/adr/` directory | ❌ NO | Directory does not exist |

**Assessment**: No ADR directory. Major decisions are tracked inline in `docs/PILOTAGE.md` (D1-D5) and `docs/CONTEXT.md` (D6-D26) rather than in separate ADR files.

---

## 6. Skills / Prompts / Tools References

### VBB References in Project Files

| File | Reference Type | Excerpt |
|------|---------------|---------|
| `.gitignore` (line 33) | `vibebackbone` | `# Vibebackbone / pi workspace` |
| `ScreenTimer/Shared/DesignSystem/DesignTokens.swift` (line 7) | `Vibe Backbone` | `// Derived from the Vibe Backbone document.` |
| `docs/CONTEXT.md` (line 16) | `Vibebackbone` | `feat: initialize project with Vibebackbone governance` |
| `docs/CONTEXT.md` (line 18) | `Vibe Backbone` | `feat: implement design system tokens and UI components from Vibe Backbone` |
| `docs/PROJECT_MODE.md` (line 25) | `Vibe Backbone` | `Design system codé (tokens, composants) aligné sur le Vibe Backbone` |
| `docs/PROJECT_MODE.md` (line 34) | `Vibebackbone` | `### Modes Vibebackbone` |
| `docs/MVP_START_PROTOCOL.md` (line 12) | `Vibe Backbone` | `Tokens SwiftUI ... implémentés et conformes au Vibe Backbone` |
| `docs/AUDIT_STATUS.md` (line 47) | `Vibebackbone` | `Initialisation Vibebackbone` |
| `docs/CONVENTIONS.md` (line 10) | `Vibebackbone` | `Ce document complète la gouvernance Vibebackbone` |
| `docs/SESSION.md` (lines 43-44) | `vbb-` tools | References `vbb-loop-closure-check.py`, `vbb-ci-local.sh` |
| `docs/runs/.../07_CLOSEOUT.md` (lines 72-77) | `vbb-` tools | References `vbb-architecture.py`, `vbb-contract-lint.py`, `vbb-loop-closure-check.py`, `vbb-ci-local.sh` |
| `docs/audits/a11y-20260614-1420.md` (line 7) | `vbb-` skill | `Skill: 2-vbb-accessibility v1.0` |

### Git History VBB References

| Commit | Message |
|--------|---------|
| `6be87f9` (initial) | `feat: initialize ScreenTimer project with Vibebackbone governance` |
| `af9b239` | `feat: implement design system tokens and UI components from Vibe Backbone` |

### Project Boot Files

| File | Present | Details |
|------|---------|---------|
| `AGENTS.md` | ❌ NO | Not present in project root |
| `SYSTEM.md` | ❌ NO | Not present |
| `README.md` | ❌ NO | Not present |

### Git Hooks

| Element | Present | Details |
|---------|---------|---------|
| Custom hooks | ❌ NO | Only default `.sample` hooks from git init |
| `scripts/` directory | ❌ NO | No shell scripts |

### pi Workspace

| Element | Present | Details |
|---------|---------|---------|
| `.pi/` directory | ✅ YES | Contains `agents/supervisor.md` (VBB-style supervisor guidance), `hippo-memory/` (episodic + semantic memory), `taskplane.json` |
| `.pi/agents/supervisor.md` | ✅ YES | VBB-style supervisor template with frontmatter (`name: supervisor`), project-specific guidance section |
| `.pi/taskplane.json` | ✅ YES | Migration `add-supervisor-local-template-v1` applied at 2026-06-15 |

**Assessment**: Strong VBB tooling integration. Design tokens explicitly derived from VBB. Multiple governance docs reference VBB by name. VBB tools (`vbb-architecture.py`, `vbb-contract-lint.py`, `vbb-loop-closure-check.py`, `vbb-ci-local.sh`) are actively used in closeout verification. pi workspace is present with supervisor agent and hippo-memory.

---

## 7. Activity

| Element | Present | Details |
|---------|---------|---------|
| `ACTIVITY_LOG.md` | ❌ NO | Not present |

**Assessment**: No dedicated activity log. Activity is tracked through `docs/SESSION.md`, `docs/CONTEXT.md` runs table, and git history.

---

## 8. Source Code — VBB-Influenced Structure

### Architecture Alignment

The source tree follows VBB-recommended separation:

```
ScreenTimer/
├── ScreenTimerApp.swift          ← @main entry point
├── ContentView.swift              ← Root view + role routing
├── Shared/
│   ├── DesignSystem/
│   │   └── DesignTokens.swift     ← 🎨 Explicitly "Derived from the Vibe Backbone document"
│   ├── Engine/                    ← Pure business logic (TimerEngine, StateMachine, PauseCalculator)
│   ├── Models/                    ← Domain models + projections (17 files)
│   ├── Services/                  ← System adapters + stores (5 files)
│   ├── Views/                     ← Shared UI components
│   ├── ViewModels/                ← View models
│   └── Extensions/                ← Utility extensions
├── Controller/                    ← Admin/parent surfaces (4 files)
├── Display/                      ← Child/viewer surfaces (1 file)
├── History/                      ← History views
└── Platform/                     ← Platform-specific code
```

### Design System Tokens (VBB-derived)

`DesignTokens.swift` explicitly states it is "Derived from the Vibe Backbone document" and references VBB "10 commandements":
- STColor (semantic: running/overtime/paused/idle + backgrounds + accents)
- STTypo (timerHero, timerCard, labelTitle — all monospaced)
- STSpacing (xs=4 through xxl=48)
- STRadius (sm=8, md=16, lg=24)
- STSize (ringHero=280, ringCard=148, cardCompact=88)
- STAnimation (overtimePulse, stateTransition, startSpring)
- STA11y (voiceOverLabel, stateIcon, stateIndicator)

### Key VBB Patterns in Code

| Pattern | Evidence |
|---------|----------|
| Engine/Service separation | `TimerEngine` (pure calc) vs `NotificationManager` (system adapter) |
| Canonical sources | Documented in `CONVENTIONS.md` §Sources canoniques |
| Projection layer | `WorkspaceProjection`, `WorkspacePresentationStore` decouple UI from SwiftData |
| Runtime events | `SessionEvent`, `SessionEventReducer`, `SessionRuntimeLedger` |
| Test seams | `UserNotificationCentering` protocol for notification testability |
| Kill-proof design | Date-based timer math (not counter-based) — documented in PILOTAGE.md |

### Test Coverage

| Test File | Test Count (approx) |
|-----------|---------------------|
| `TimerStateMachineTests.swift` | 25 |
| `TimerEngineTests.swift` | 19 |
| `TimerEngineActionTests.swift` | 15 |
| `TimeFormattingTests.swift` | 12 |
| `NotificationRuleTests.swift` | 8 |
| `PauseCalculatorTests.swift` | 7 |
| `TimerPerimeterOrganizerTests.swift` | 5 |
| `SessionDomainTests.swift` | 2 |
| `SessionRuntimePersistenceTests.swift` | 1 |
| `WorkspacePresentationStoreTests.swift` | 1 |
| `NotificationManagerTests.swift` | 0 (empty) |
| `TimerTimingParityTests.swift` | 0 (empty) |
| **Total** | **~95** |

Documented as 98 tests passing on macOS + iOS (SESSION.md).

---

## 9. Summary Matrix

| VBB Element Category | Count Present | Count Absent | Adoption Level |
|----------------------|---------------|--------------|----------------|
| Core Governance Docs | 8/8 | 0 | 🟢 **FULL** |
| Extended Governance Docs | 0/15 | 15 | 🔴 **NONE** |
| Templates | 0/1 | 1 | 🔴 **NONE** |
| Run Artifacts | 2 runs (partial) | — | 🟡 **PARTIAL** (only INTAKE+CLOSEOUT) |
| Audit Artifacts | 8 audits | — | 🟢 **STRONG** |
| ADRs | 0/1 | 1 | 🔴 **NONE** (decisions in PILOTAGE+CONTEXT) |
| VBB References in Code | 12+ files | — | 🟢 **STRONG** |
| pi Workspace | ✅ | — | 🟢 **PRESENT** |
| Boot Files (AGENTS/README/SYSTEM) | 0/3 | 3 | 🔴 **NONE** |
| Git Hooks / Scripts | 0 | — | 🔴 **NONE** |
| Design System (VBB-derived) | ✅ | — | 🟢 **STRONG** |

---

## 10. Overall Assessment

**VBB Adoption Grade: 🟢 B+ (STRONG, with gaps)**

### Strengths
1. **Initialized with VBB from commit #1** — the project was born on VBB rails
2. **All 8 core governance docs present and actively maintained** — CONTEXT, PROJECT_MODE, PILOTAGE, SESSION, AUDIT_STATUS, CONVENTIONS, MVP_START_PROTOCOL, TEST_CHECKLIST
3. **Design system explicitly derived from VBB** — `DesignTokens.swift` cites "Vibe Backbone document" and "10 commandements"
4. **Active VBB tooling in closeout** — `vbb-architecture.py`, `vbb-contract-lint.py`, `vbb-loop-closure-check.py`, `vbb-ci-local.sh` all used
5. **8 VBB-style audits** — high audit density, one explicitly references VBB skill `2-vbb-accessibility`
6. **pi workspace present** — supervisor agent, hippo-memory, taskplane
7. **VBB architectural patterns** — Engine/Service separation, canonical sources, projection layer, runtime events, test seams

### Gaps
1. **No AGENTS.md, README.md, SYSTEM.md** — project lacks agent boot files
2. **No extended governance docs** — ARCHITECTURE.md, RELATIONS.md, INDEX.md, etc. absent (acceptable for EXPLORE mode)
3. **No templates directory** — not yet needed
4. **No ADR directory** — decisions tracked inline in PILOTAGE/CONTEXT instead
5. **Partial run phases** — only INTAKE+CLOSEOUT (FAST-MINIMAL pattern), no full 8-phase runs
6. **No custom git hooks or scripts** — no VBB pre-commit or CI scripts in project
7. **No ACTIVITY_LOG.md** — activity tracked through SESSION.md and git

### Verdict
SwiftMinuteur is a **well-adopted VBB project** in EXPLORE mode. The core governance skeleton is complete and actively maintained. The project uses VBB tools for closeout verification and follows VBB architectural patterns. Gaps are consistent with EXPLORE-mode fast iteration (no extended docs, partial run phases, no ADRs). The project would benefit from adding AGENTS.md for agent bootstrapping and eventually expanding run phases when moving to MVP mode.
