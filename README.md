<p align="center">
  <img src="assets/vibebackbone_logo.svg" alt="Vibebackbone" width="480"/>
  <br/>
  <strong style="font-size: 1.4em;">57 skills · 24 prompts · 4 voies d'exécution · 1 grammaire partagée</strong>
</p>

<p align="center">Le système d'orchestration pour agents IA qui transforme le chaos de développement en pilotage prévisible.</p>

---

## Le problème

Vous travaillez avec des agents IA (Claude Code, Codex, Cursor, Qwen, Gemini…). Chaque session est une aventure : le modèle improvise, invente des workflows, oublie le contexte, écrit des trucs qu'il ne fallait pas, et vous devez tout relire. Le code part en sucette. La doc ment. Les audits n'arrivent jamais.

**Vous ne pilotez plus — vous subissez.**

## La solution

**vibebackbone** est un système de pilotage opérationnel pour agents IA. Ce n'est pas un framework, pas une librairie, pas un SaaS. C'est une grammaire de comportement que vous injectez dans le contexte de vos agents.

Le résultat ? Un orchestrateur silencieux qui :

- ✅ **trie** toute tâche en 25 ms (voie rapide, structurée, audit, clôture)
- ✅ **planifie** avant d'agir — fini le code sauvage
- ✅ **audite** la sécurité, l'intégrité des données, les contrats API, la dette technique
- ✅ **maintient** une discipline de contexte LLM (plus de saturation mémoire)
- ✅ **produit** des handoffs propres entre sessions

---

## Ce que contient ce repo

```
vibebackbone/
├── skills/              # 57 skills prêts à injecter
│   ├── 0-vbb-*/        # Phase 0 : Readiness & cadrage (5)
│   ├── 1-vbb-*/        # Phase 1 : Structure & dette technique (16)
│   ├── 2-vbb-*/        # Phase 2 : Audits de fond (12)
│   ├── 3-vbb-*/        # Phase 3 : Consolidation (1)
│   ├── 4-vbb-*/        # Phase 4 : Front-end UX/UI (10)
│   ├── t-vbb-*/        # Transverse : Docker, Git, CI, deploiement (12)
│   └── vibebackbone/   # Orchestrateur principal + PILOTAGE.md
├── prompts/             # 24 prompts de pilotage
├── docs/                # Gouvernance vibebackbone du repo
│   ├── PROJECT_MODE.md  # Mode distribution
│   ├── SESSION.md       # Session memory (gitignoré)
│   ├── AUDIT_STATUS.md  # Audit dashboard (gitignoré)
│   └── audits/          # Rapports d'audit (gitignoré)
├── AGENTS.md            # Grammaire opérationnelle canonique (325 lignes)
├── SYSTEM.md            # Comportement runtime Pi (146 lignes)
├── CLAUDE.md            # Point d'entree universel pour Claude Code / Cursor
├── .gitignore           # Ignore les artefacts de session locale
└── .pi/                 # Configuration Pi
    ├── agents/          # Supervisor template
    └── taskplane.json   # Config taskplane
```

### Les 57 skills en un coup d'œil

| Phase | Foyer | Skills |
|-------|-------|--------|
| **🔰 0** | Readiness & cadrage | Guide, Pilotage, Scope-freeze, Audit-readiness, Standard |
| **🔧 1** | Structure & dette | Code-janitor, Conventions, Formatter, Tech-debt, Monolith-detector, Logic-duplication-detector, Pattern-inconsistency-detector, Error-handling-auditor, Premature-abstraction-detector, Test-mirage-detector, Intent-decomposer, Code-doc-coherence-auditor, Code-doc-gap-integrator, Doc-harmonizer, API-contract-designer, ADR |
| **🔬 2** | Audits de fond | API-auditor, DB-robustness, Data-integrity, Security, Systemic-risk, Ops, CI, Legal, Performance, Accessibility, Analytics, Spec-validator |
| **📋 3** | Consolidation | Risk-register |
| **🎨 4** | Front-end UX/UI | User-experience-engine, Interaction-coherence, Visual-identity-layer, Visual-identity-gatekeeper, Design-system-validator, Micro-interaction-refiner, Cognitive-load-optimizer, Front-pipeline-reference, Security-remediation, Product-changelog |
| **🛠️ t-** | Transverse | Dependency-mapper, Impact-analyzer, Docker-audit, Docker-generate, Deploy-runtime, Git-sync, Commit-ready, Test-coverage-mapper, Session-handoff, Project-context-init, Anti-slop-gate, Mode-transition-gate |

Chaque skill est un fichier `SKILL.md` standardisé, indépendant, injectable dans n'importe quel agent LLM.

**Templates inclus :**
- `t-vbb-deploy-runtime/templates/deploy.sh` — script de déploiement Docker complet avec backup, rollback, healthcheck
- `t-vbb-docker-generate/templates/nginx/` — reverse-proxy production-ready (nginx.conf + security-headers.conf)

### Les 24 prompts

Des templates de session prêts à l'emploi couvrant tout le cycle :

| Phase | Prompts |
|-------|---------|
| **0** | Before-building, Plan, Triage |
| **1** | Doc-feature, Legacy-level, Post-refacto-coherence, Project-init, Quick-task, Structured-task, Tech-debt |
| **2** | Audit-task, DB-sanity, Mode-transition, Release-check, Security-pipeline |
| **3** | Risk-register |
| **4** | After-building, Anti-slop, Deploy-docker |
| **t** | Branch-policy-check, Git-sync, Sequenced-ship, Session-handoff, Start-session |

---

## Comment ça marche

```
Tâche entrante
    │
    ▼
┌──────────────────────────────────────────────────┐
│  TRIAGE (via PILOTAGE.md)                        │
│                                                  │
│  Voie RAPIDE    → exécution directe              │  (risque faible)
│  Voie STRUCTURÉE → plan + exécution cadrée       │  (contrats, multi-fichiers)
│  Voie AUDIT     → séquence d'audit complète      │  (sécurité, intégrité)
│  Voie CLÔTURE   → handoff + session memory       │  (fin de session)
└──────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────┐
│  EXÉCUTION (via skill correspondant)             │
│                                                  │
│  Chaque skill = 1 fichier SKILL.md               │
│  Frontmatter standardisé (name, description,     │
│  version, phase, token_budget, mode_sensitive)   │
│  Input contract → Steps → Output contract        │
└──────────────────────────────────────────────────┘
    │
    ▼
Résultat prévisible, traçable, reproductible
```

L'agent ne décide plus tout seul. Il suit une grammaire documentée, lisible et vérifiable.

---

## 🔧 Installation

vibebackbone s'installe **une seule fois** dans `~/.agents/skills/` — le répertoire universel
auto-découvert par Pi, OpenCode et Codex. Claude Code est patché automatiquement.

```bash
# 1. Cloner vibebackbone
git clone https://github.com/bricesodini/vibebackbone ~/vibebackbone

# 2. Installer les 57 skills globalement
bash ~/vibebackbone/setup.sh
```

C'est tout. Les 57 skills sont disponibles pour tous vos agents, dans tous vos projets.

**Ce que fait `setup.sh` :**
- Crée un symlink `~/.agents/skills/vibebackbone → ~/vibebackbone/skills/`
- Patche `~/.claude/settings.json` pour Claude Code (workaround issue [#31005](https://github.com/anthropics/claude-code/issues/31005))
- Les mises à jour se font via `git pull` (le symlink suit automatiquement)

### Découverte par provider

| Provider | Mécanisme | Configuration |
|----------|-----------|---------------|
| **Pi** | Auto (natif) | `~/.agents/skills/` — aucune action requise |
| **OpenCode** | Auto (natif) | `~/.agents/skills/` — aucune action requise |
| **Codex** | Auto (natif) | `~/.agents/skills/` — aucune action requise |
| **Claude Code** | Via settings | `setup.sh` patche `~/.claude/settings.json` automatiquement |

### Vérifier l'installation

```bash
ls ~/.agents/skills/vibebackbone/
# → 0-vbb-scope-freeze  1-vbb-conventions  2-vbb-security  3-vbb-risk-register  ...
```

### Mise à jour

```bash
cd ~/vibebackbone && git pull
# Le symlink suit automatiquement — aucune réinstallation requise
```

---

## 💬 Utilisation par agent

### Pi

```bash
pi "Lance un audit de sécurité selon vibebackbone"
pi "Applique le skill conventions sur ce projet"
pi "Génère un risk-register pour ce repo"

# Ou via commande explicite
/skill:2-vbb-security
/skill:3-vbb-risk-register
```

### Claude Code

Après `setup.sh`, les skills sont disponibles directement :

```bash
claude "Lance un audit de sécurité selon vibebackbone"
claude "Applique le skill 1-vbb-conventions"
```

### OpenCode

```bash
opencode "Audite la sécurité de ce projet selon vibebackbone"
opencode "Applique 1-vbb-tech-debt"
```

### Codex

```bash
codex "Audite la sécurité selon vibebackbone"
codex "Lance la séquence [0→1→2→3]"
```

---

## Pourquoi "vibebackbone"?

Parce que c'est l'épine dorsale (*backbone*) de vos *vibes* de développement. La colonne vertébrale qui fait tenir droit un projet quand tout le reste voudrait partir en cacahuète.

---

## Licence

MIT — libre d'utilisation, de modification, de partage.

---

**vibebackbone** — par Brice, pour les agents qui en avaient marre de faire n'importe quoi.
