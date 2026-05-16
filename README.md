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

### Pi (natif)

**Pi** lit automatiquement ce repo via `.pi/`. Aucune configuration manuelle nécessaire.

```bash
# 1. Cloner le repo dans votre workspace Pi
git clone https://github.com/bricesodini/vibebackbone ~/vibebackbone

# 2. Pi découvre automatiquement :
#    - skills/ → catalogue de skills
#    - AGENTS.md → grammaire opérationnelle
#    - SYSTEM.md → comportement runtime
#    - .pi/ → configuration Pi

# 3. Utilisation directe :
pi "Lance un audit de sécurité selon vibebackbone"
pi "Applique le skill code-janitor sur ce projet"
```

**Fichiers clés :** `AGENTS.md` + `SYSTEM.md` + `.pi/` → découverte auto

---

### Claude Code (Anthropic)

Claude Code lit automatiquement `CLAUDE.md` à la racine du projet cible.

```bash
# 1. Dans votre projet cible, créer CLAUDE.md :
cp chemin/vers/vibebackbone/CLAUDE.md ./CLAUDE.md

# 2. Rendre les skills accessibles :
ln -s chemin/vers/vibebackbone/skills ./skills-vbb

# 3. Utilisation :
claude "Lance un audit de securite selon vibebackbone"
```

**Fichiers clés :** `CLAUDE.md` (détection auto) + skills accessibles par chemin relatif

---

### Codex (OpenAI — terminal)

Codex utilise un fichier `.codex.md` ou des instructions en début de session.

```bash
# 1. Dans votre projet cible, charger le contexte :
cat chemin/vers/vibebackbone/AGENTS.md >> .codex.md

# 2. Lier les skills :
ln -s chemin/vers/vibebackbone/skills ./skills-vbb

# 3. Utilisation :
codex "Audite la securite de ce projet selon vibebackbone"
```

**Alternative :** Copier `AGENTS.md` dans le fichier d'instructions système de Codex.

**Fichiers clés :** `.codex.md` ou system prompt personnalisé + skills accessibles

---

### OpenCode (local)

OpenCode utilise `~/.opencode.md` (global) ou `.opencode.md` (projet).

```bash
# 1. Config globale (tous les projets) :
cat chemin/vers/vibebackbone/AGENTS.md >> ~/.opencode.md

# 2. Config projet (projet spécifique) :
cat chemin/vers/vibebackbone/AGENTS.md >> .opencode.md
echo "skills_dir: chemin/vers/vibebackbone/skills" >> .opencode.md

# 3. Utilisation :
opencode "Audite la securite de ce projet selon vibebackbone"
```

**Fichiers clés :** `~/.opencode.md` (global) ou `.opencode.md` (projet) + skills accessibles

---

### Cursor

Cursor utilise `.cursorrules` ou le dossier `.cursor/rules/`.

```bash
# 1. Dans votre projet cible :
cp chemin/vers/vibebackbone/AGENTS.md .cursorrules

# 2. Lier les skills (optionnel, Cursor peut naviguer) :
ln -s chemin/vers/vibebackbone/skills skills-vbb

# 3. Coller dans Cursor Chat :
"Applique vibebackbone sur ce projet : audite la securite"
```

**Fichiers clés :** `.cursorrules` (détection auto)

---

### Approche transversale (tous les agents)

La méthode universelle qui fonctionne avec **n'importe quel agent LLM**, sans dépendre d'un fichier de config spécifique.

```bash
# 1. Cloner vibebackbone quelque part sur votre machine
git clone https://github.com/bricesodini/vibebackbone ~/.vibebackbone

# 2. Dans chaque nouveau projet, créer un alias ou script :
echo "VIBE=~/.vibebackbone" >> .env

# 3. Pour n'importe quel agent, le pattern est toujours le même :
```

**Le contrat universel** — à coller dans le contexte de n'importe quel agent :

```
Tu operationnes sous la gouvernance vibebackbone.
Fichiers racine : chemin/vers/vibebackbone/AGENTS.md
Comportement runtime : chemin/vers/vibebackbone/SYSTEM.md
Catalogue skills : chemin/vers/vibebackbone/skills/
Prompts : chemin/vers/vibebackbone/prompts/
Pilotage : chemin/vers/vibebackbone/skills/vibebackbone/docs/PILOTAGE.md

57 skills disponibles. Triage obligatoire avant action.
```

**Résumé des points d'entrée par agent :**

| Agent | Fichier d'entrée | Mécanisme |
|-------|-----------------|-----------|
| **Pi** | `.pi/` + `AGENTS.md` + `SYSTEM.md` | Découverte automatique |
| **Claude Code** | `CLAUDE.md` | Détection auto à la racine |
| **Codex** | `.codex.md` ou system prompt | Injection manuelle |
| **OpenCode** | `~/.opencode.md` ou `.opencode.md` | Injection globale ou projet |
| **Cursor** | `.cursorrules` ou `.cursor/rules/` | Détection auto à la racine |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Instructions globales |
| **Tous les autres** | Contrat universel (à coller en début de session) | Injection manuelle |

---

## Pourquoi "vibebackbone"?

Parce que c'est l'épine dorsale (*backbone*) de vos *vibes* de développement. La colonne vertébrale qui fait tenir droit un projet quand tout le reste voudrait partir en cacahuète.

---

## Démarrage rapide (30 secondes)

```bash
# 1. Clone
git clone https://github.com/bricesodini/vibebackbone ~/.vibebackbone

# 2. Dans votre projet, créez le point d'entree
echo "VibeBackbone: ~/.vibebackbone" > CLAUDE.md     # Claude Code
# ou
cat ~/.vibebackbone/AGENTS.md > .cursorrules          # Cursor

# 3. Utilisez
pi "Applique vibebackbone sur ce projet"
```

---

## Licence

MIT — libre d'utilisation, de modification, de partage.

---

**vibebackbone** — par Brice, pour les agents qui en avaient marre de faire n'importe quoi.
