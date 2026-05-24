# GUIDE — Piloter vibebackbone au quotidien

**Version** : 1.0 · **Date** : 2026-05-18 · **Public** : humains (devs, leads, PM)
**Couche** : L3 — référence, pas chargé au boot. Charger via `tools/vbb-index.py search` ou skill `0-vbb-guide`.

Ce guide est un compagnon **pédagogique** du `README.md`. Le README dit *ce qu'est* vibebackbone. Ce guide dit *comment l'utiliser pour de vrai*, avec des cas d'usages concrets, des dialogues réalistes avec un agent, et les pièges à éviter.

> Si vous avez 30 minutes, lisez les sections 1 à 5.
> Si vous avez 5 minutes, lisez la section 2 ("L'intuition en 3 minutes") puis la cheatsheet finale.

---

## Sommaire

1. [Pour qui, pour quoi](#1-pour-qui-pour-quoi)
2. [L'intuition en 3 minutes](#2-lintuition-en-3-minutes)
3. [Le modèle mental (concepts clés)](#3-le-modèle-mental-concepts-clés)
4. [Installation et configuration](#4-installation-et-configuration)
5. [Premier pas guidé — un exemple complet](#5-premier-pas-guidé--un-exemple-complet)
6. [Six cas d'usages détaillés](#6-six-cas-dusages-détaillés)
7. [Pilotage au quotidien](#7-pilotage-au-quotidien)
8. [Configuration avancée](#8-configuration-avancée)
9. [Anti-patterns — ce qui casse vibebackbone](#9-anti-patterns--ce-qui-casse-vibebackbone)
10. [FAQ pratique](#10-faq-pratique)
11. [Cheatsheet](#11-cheatsheet)
12. [Où aller ensuite](#12-où-aller-ensuite)

---

## 1. Pour qui, pour quoi

### Ce guide s'adresse à vous si

- Vous **codez avec un ou plusieurs agents** (Claude Code, Codex CLI, Cursor, OpenCode, Continue, Qwen local…) et trouvez que ça part trop souvent en vrille.
- Vous voulez **comprendre la logique** de vibebackbone sans relire 8 docs de référence.
- Vous voulez voir **comment ça se passe concrètement** : quels mots taper, quels fichiers regarder, comment savoir si l'agent fait n'importe quoi.

### Ce guide ne remplace pas

| Document | Pour quoi |
|----------|-----------|
| `README.md` | Quoi, pourquoi, installation rapide |
| `docs/CONTEXT.md` | MOC / routeur central persistant (premier fichier à lire au démarrage) |
| `AGENTS.md` | Grammaire opérationnelle canonique (lue par les agents) |
| `SYSTEM.md` | Comportement runtime (lu par Pi) |
| `docs/PILOTAGE.md` | Règles de triage et d'escalade (référence) |
| `docs/AGENTIC_RUN_PROTOCOL.md` | Les 7 phases formalisées (référence) |
| `PROMPTS_ARCHITECTURE.md` | Architecture des 3 couches de prompts |

Ce guide **agrège et raconte**. Les autres docs **définissent et formalisent**.

---

## 2. L'intuition en 3 minutes

### Le problème

Un agent IA livré sans cadre fait trois choses prévisibles :

1. Il **mélange les rôles** : il audite, décide, code et review dans la même session — donc le review est complice du code.
2. Il **oublie ce qu'il a fait** : pas de trace persistante, pas de handoff, le contexte se perd à chaque pause.
3. Il **dérive du scope** : on lui demande de corriger une typo, il refactorise trois modules.

### La solution vibebackbone

Une grammaire à **quatre composants**, qu'on injecte dans le contexte de l'agent :

```
┌─────────────────────────────────────────────────────────┐
│  4 VOIES                                                │
│  Chaque tâche est triée dans une voie unique :          │
│  RAPIDE · STRUCTURÉE · AUDIT · CLÔTURE                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  7 PHASES                                               │
│  Une tâche traverse 1 à 7 phases canoniques :           │
│  INTAKE → AUDIT → DECISION → PLAN →                     │
│  EXECUTION → REVIEW → CLOSEOUT                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  32 PROMPTS                                             │
│  7 canoniques (un par phase) + 24 spécialisés           │
│  + 1 router Markdown pour choisir                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  58 SKILLS                                              │
│  Unités de capacité injectables, chacune avec un        │
│  SKILL.md standardisé                                   │
└─────────────────────────────────────────────────────────┘
```

**Règle d'or unique** :

```
1 session = 1 rôle = 1 intention = 1 sortie exploitable
```

Si vous ne devez retenir qu'une chose, c'est ça.

### Ce que ça change concrètement

- Vous **savez où vous en êtes** dans le cycle de travail à tout moment (quelle phase, quelle voie, quel artefact attendu).
- L'agent **refuse de dériver** : on lui a dit ce qu'il ne doit pas faire dans cette phase.
- L'humain a **une trace lisible** dans `docs/runs/YYYY-MM-DD_HHmm_slug/` à chaque étape importante.
- Le **review n'est jamais fait par l'executor** — séparation de session obligatoire.

---

## 3. Le modèle mental (concepts clés)

### 3.1 Les 4 voies — comment trier une tâche

| Voie | Quand | Sessions | Artefacts | Exemples |
|------|-------|----------|-----------|----------|
| **RAPIDE** | Risque faible, action locale et réversible | 1 | 01 + 05 + 07 | Fix typo, renommer variable, ajuster un message |
| **STRUCTURÉE** | Touche contrat de données, multi-fichiers, ou auth | 4–6 | 01 + 04 + 05 + 07 | Validation de formulaire avec cohérence DB |
| **AUDIT** | Sécurité, intégrité données, conformité, risque systémique | 7–9 | 01 + 02 + 03 + 07 | Pré-déploiement, vérif RGPD, audit XSS |
| **CLÔTURE** | Fin de session, pause longue, transmission | 1 | 07 | Handoff de fin de journée |

#### Niveaux de la voie RAPIDE

La voie RAPIDE dispose de 3 niveaux internes pour réduire la friction :

| Niveau | Quand | Artefacts requis | Traçabilité |
|--------|-------|------------------|-------------|
| **RAPIDE-ZERO** | Micro-tâche sûre, ≤ 3 fichiers, zéro risque | Aucun `docs/runs/` | `docs/ACTIVITY_LOG.md` uniquement |
| **RAPIDE-MINIMAL** | Petite tâche non triviale | `05_PATCH_SUMMARY` | Activity Log + patch summary |
| **RAPIDE STANDARD** | Workflow RAPIDE classique | 01 + 05 + 07 | Cycle complet |

**Conditions d'éligibilité RAPIDE-ZERO** (toutes doivent être vraies) :
- Risque faible (aucun impact runtime)
- Pas de sécurité impliquée
- Pas de base de données impliquée
- Pas de migration
- Pas d'impact architecture
- Pas de contrat impacté
- Idéalement ≤ 3 fichiers modifiés

Si une condition n'est pas remplie → **RAPIDE-MINIMAL** (si ≤ 5 fichiers) ou **RAPIDE STANDARD** / **STRUCTURÉE**.

**Triage en 4 questions** (dans cet ouitre) :

```
1. Touche données / auth / état prod ?       → STRUCTURÉE
2. Touche sécurité / conformité / intégrité ? → AUDIT
3. Aucune des deux ?                          → RAPIDE
4. C'est une fin de session ?                 → CLÔTURE
```

**Règle d'escalade absolue** : si une tâche commencée en RAPIDE révèle un impact sur les données, l'auth, la sécurité ou la prod → **stop immédiat**, on passe en STRUCTURÉE ou AUDIT. On ne continue jamais comme si de rien n'était.

### 3.2 Les 7 phases — la machine d'état canonique

```
01_INTAKE      Cadrer, classifier, recommander la voie
02_AUDIT       Observer, constater (lecture seule)
03_DECISION    Décider, documenter le rationale
04_PLAN        Décomposer en runs, définir les tests
05_EXECUTION   Appliquer un run (et un seul)
06_REVIEW      Évaluer indépendamment (executor ≠ reviewer)
07_CLOSEOUT    Clôturer, documenter, transmettre
```

Chaque phase **produit un artefact nommé** dans `docs/runs/YYYY-MM-DD_HHmm_slug/` :

| Phase | Fichier produit |
|-------|----------------|
| 01 | `01_INTAKE.md` |
| 02 | `02_AUDIT_REPORT.md` (+ rapport horodaté dans `docs/audits/`) |
| 03 | `03_DECISION_RECORD.md` |
| 04 | `04_FIX_PLAN.md` |
| 05 | `05_PATCH_SUMMARY_RUN_N.md` |
| 06 | `06_REVIEW_RUN_N.md` |
| 07 | `07_CLOSEOUT.md` |

**Toutes les voies ne traversent pas toutes les phases.** Une voie RAPIDE est typiquement `01 → 05 → 07`. Une voie AUDIT est `01 → 02 → 03 → 04 → 05 → 06 → 07`.

### 3.3 Les 3 couches de prompts

```
prompts/
├── canonical/                        ← 7 prompts (un par phase)
│   ├── 01-p-vbb-intake.md
│   ├── 02-p-vbb-audit.md
│   ├── ...
│   └── 07-p-vbb-closeout.md
├── (racine)                          ← 24 prompts spécialisés + 1 router
│   ├── 0-p-vbb-triage.md
│   ├── 1-p-vbb-quick-task.md
│   ├── 2-p-vbb-security-pipeline.md
│   └── ...
└── t-p-vbb-phase-router.md           ← le router (Markdown)
```

**Quand utiliser quoi** :

- **Canoniques** : par défaut, pour n'importe quel contexte. Génériques, multi-LLM.
- **Spécialisés** : quand le domaine est précis (sécurité, DB, déploiement Docker…).
- **Router** : en cas de doute. C'est une matrice de décision pure Markdown — pas un script.

Détails : voir `PROMPTS_ARCHITECTURE.md`.

### 3.4 Les 62 skills

Un **skill** est une unité de capacité réutilisable, packagée comme un dossier avec un `SKILL.md` standardisé. Exemples : `2-vbb-security`, `1-vbb-tech-debt`, `t-vbb-deploy-runtime`.

Vous n'invoquez **presque jamais** un skill directement. Les prompts les orchestrent pour vous. Mais vous pouvez les lire si vous voulez comprendre ce que l'agent va faire.

Catalogue complet : `skills/0-vbb-guide/SKILL.md`.

### 3.5 La séparation executor / reviewer

C'est **le** principe non-négociable de vibebackbone :

> **Un agent qui exécute ne peut pas reviewer son propre travail dans la même session.**

Concrètement :
- Session 1 : `05-p-vbb-execution` → produit `05_PATCH_SUMMARY_RUN_01.md`
- Session 2 (nouvelle, obligatoire) : `06-p-vbb-review` → produit `06_REVIEW_RUN_01.md`

Pourquoi ? Parce qu'un agent qui vient de coder a un biais cognitif énorme pour valider son propre code. Une nouvelle session redonne du regard neuf.

---

## 4. Installation et configuration

### 4.1 Installation globale

```bash
git clone <url-vibebackbone> ~/vibebackbone
cd ~/vibebackbone
bash setup.sh
```

`setup.sh` déploie quatre couches :

| Couche | Cible | Quoi |
|--------|-------|------|
| **Skills** | `~/.agents/skills/vibebackbone` | Les 62 skills (lecture universelle) |
| **Prompts** | `~/.agents/prompts/vibebackbone` | Les 24 prompts spécialisés + 1 router (symlink universel) |
| **AGENTS.md** | Par provider | Grammaire opérationnelle |
| **SYSTEM.md** | Par provider | Comportement runtime |

### 4.2 Configuration par provider

| Provider | Fichiers patchés | Comment ça marche |
|----------|------------------|-------------------|
| **Claude Code** | `~/.claude/settings.json` + `~/.claude/CLAUDE.md` + `~/.claude/commands/vbb-*.md` | Bloc `@import` injecté dans CLAUDE.md ; commandes `/vbb-*` disponibles |
| **Codex CLI** | `~/.codex/AGENTS.md` | Bloc compilé généré dans AGENTS.md global |
| **OpenCode** | `~/.config/opencode/opencode.json` + commandes | Champ `instructions` mis à jour |
| **Pi** | `~/.pi/agent/AGENTS.md` + `SYSTEM.md` + prompts | Symlinks directs |
| **Cursor / Continue** | Manuel | Voir section 4.4 |

### 4.3 Vérifier l'installation

Après `bash setup.sh`, vérifiez :

```bash
# Skills bien symlinkés
ls -la ~/.agents/skills/vibebackbone | head -3

# Claude Code voit vibebackbone
grep -A2 "vibebackbone" ~/.claude/CLAUDE.md | head -10

# Commandes Claude générées
ls ~/.claude/commands/vbb-*.md 2>/dev/null | wc -l
```

Si tout est OK, ouvrez Claude Code dans un projet et tapez `/` — vous devriez voir les commandes `vbb-*`.

### 4.4 Pour Cursor, Continue, et autres providers non packagés

Ces providers ne lisent pas `~/.agents/` automatiquement. Deux options :

**Option A — copier-coller dans les règles du projet**

```bash
# Dans le projet
cat ~/vibebackbone/AGENTS.md ~/vibebackbone/SYSTEM.md > .cursorrules
```

**Option B — injecter à chaque session**

Au début d'une session, demander à l'agent :
> "Lis `~/vibebackbone/AGENTS.md` et `~/vibebackbone/SYSTEM.md` avant de commencer. Respecte la grammaire vibebackbone."

### 4.5 Initialiser un projet sur les rails vibebackbone

Dans un repo donné, créer `docs/PROJECT_MODE.md` :

```bash
mkdir -p docs
cat > docs/PROJECT_MODE.md <<EOF
# PROJECT MODE — $(basename $(pwd))

**Mode** : DEV | STAGING | PROD
**Niveau de discipline** : LIGHT | STANDARD | STRICT
**Date d'initialisation** : $(date +%Y-%m-%d)

## Contexte

[Décrire le projet en 2-3 phrases]

## Contraintes spécifiques

- [Auth, prod, données sensibles, etc.]
EOF
```

Ce fichier est le **signal** que le repo est sur les rails. Sans lui, l'agent doit le proposer en début de session.

---

## 5. Premier pas guidé — un exemple complet

**Scénario** : vous avez un bug d'affichage trivial (message d'erreur mal traduit). On va le corriger en voie RAPIDE.

### Étape 1 — Ouvrir la session

Dans Claude Code, taper :

```
/vbb-quick-task

J'ai un message d'erreur en anglais qui devrait être en français
dans src/auth/login.tsx ligne 42. Texte actuel: "Invalid credentials".
Doit être: "Identifiants invalides".
```

### Étape 2 — Observer ce que l'agent fait

L'agent va :

1. **Restater** la demande (1-2 phrases).
2. **Classer** la voie : RAPIDE (action locale, réversible).
3. **Créer** `docs/runs/2026-05-18_1430_fix-error-message/01_INTAKE.md` minimal.
4. **Appliquer** la modification.
5. **Produire** `docs/runs/2026-05-18_1430_fix-error-message/05_PATCH_SUMMARY_RUN_01.md`.
6. **Conclure** : voie RAPIDE complète, pas de 06_REVIEW nécessaire.

### Étape 3 — Vérifier l'artefact

```bash
ls docs/runs/2026-05-18_1430_fix-error-message/
# 01_INTAKE.md
# 05_PATCH_SUMMARY_RUN_01.md
```

Ouvrez `05_PATCH_SUMMARY_RUN_01.md` — vous devez y lire :
- Fichier modifié
- Diff appliqué
- Résultat attendu
- Tests effectués (si applicable)

### Étape 4 — Clôturer (optionnel pour RAPIDE)

Pour une RAPIDE, le 07_CLOSEOUT n'est pas obligatoire. Vous pouvez :
- soit fermer la session telle quelle ;
- soit demander `/vbb-session-handoff` pour archiver proprement.

### Ce que vous venez d'apprendre

- Une session vibebackbone produit toujours **au moins un artefact persistant**.
- Le triage en voie est **explicite** (RAPIDE ici).
- L'agent **ne dérive pas** : il ne refactorise pas tout `login.tsx`, il change juste la chaîne.
- Le dossier `docs/runs/` devient votre **journal de bord** automatique.

---

## 6. Six cas d'usages détaillés

### Cas 1 — Fix rapide (voie RAPIDE)

**Quand** : typo, message d'erreur, renommage local, ajustement CSS mineur.

**Prompt à utiliser** : `1-p-vbb-quick-task` (ou commande `/vbb-quick-task`).

**Séquence** :

```
01_INTAKE (implicite ou minimal)
   ↓
05_EXECUTION
   ↓
[07_CLOSEOUT optionnel]
```

**Sessions** : 1 seule.

**Artefacts** :
```
docs/runs/2026-05-18_1430_fix-typo/
├── 01_INTAKE.md              (minimal — peut être 3 lignes)
└── 05_PATCH_SUMMARY_RUN_01.md
```

**Piège** : la tâche révèle un risque (par exemple, la "typo" est en réalité dans un fichier de config d'auth). **Stop, on escalade en STRUCTURÉE.**

---

### Cas 2 — Feature avec validation DB (voie STRUCTURÉE)

**Quand** : ajout d'un champ de formulaire qui touche la DB, refactor multi-fichiers, modification d'un contrat d'API.

**Prompt à utiliser** : `1-p-vbb-structured-task` (compact, 1 session) ou enchaînement canonique (4-6 sessions, plus rigoureux).

**Séquence canonique** :

```
Session 1: 01_INTAKE
   ↓ [nouvelle session recommandée]
Session 2: 04_PLAN
   ↓ [nouvelle session recommandée]
Session 3: 05_EXECUTION (RUN 01)
   ↓ [NOUVELLE SESSION OBLIGATOIRE]
Session 4: 06_REVIEW (RUN 01)
   ↓ [optionnel : session 5 si modifs]
Session 5: 07_CLOSEOUT
```

**Artefacts** :
```
docs/runs/2026-05-18_1430_add-email-validation/
├── 01_INTAKE.md
├── 04_FIX_PLAN.md
├── 05_PATCH_SUMMARY_RUN_01.md
├── 06_REVIEW_RUN_01.md
└── 07_CLOSEOUT.md
```

**Exemple de dialogue** (session 1, INTAKE) :

> **Vous** : `/vbb-intake` — Je veux ajouter une validation d'email côté front ET back, avec un check unicité en DB.
>
> **Agent** : Reformule, classifie en STRUCTURÉE (touche DB + multi-fichiers), produit `01_INTAKE.md`, recommande de passer en session 04_PLAN.

**Piège classique** : tenter de faire INTAKE + PLAN + EXECUTION dans une seule session pour aller vite. **Ne pas faire ça** sur du STRUCTURÉE — sauf si vous utilisez `1-p-vbb-structured-task` qui packe explicitement les 3 phases.

---

### Cas 3 — Audit sécurité pré-déploiement (voie AUDIT)

**Quand** : avant un release prod, après un changement d'auth, suite à une alerte CVE.

**Prompt à utiliser** : `2-p-vbb-security-pipeline` (audit ciblé sécurité) ou `2-p-vbb-release-check` (audit complet 14 skills).

> **Avertissement** : `2-p-vbb-release-check` mobilise 14 skills en 4 waves. Si votre contexte LLM est < 200 K tokens ou si le repo a > 50 fichiers actifs, **lancer wave par wave** dans des sessions séparées. Détails dans `prompts/2-p-vbb-release-check.md` section "Alignement protocole agentique".

**Séquence canonique** :

```
Session 1: 01_INTAKE
   ↓ [NOUVELLE SESSION OBLIGATOIRE]
Session 2: 02_AUDIT
   ↓ [NOUVELLE SESSION OBLIGATOIRE]
Session 3: 03_DECISION (GO / CONDITIONAL / NO_GO)
   ↓
Si NO_GO → Session 4: 04_PLAN (corrections)
              ↓
           Session 5: 05_EXECUTION
              ↓ [NOUVELLE SESSION OBLIGATOIRE]
           Session 6: 06_REVIEW
              ↓
           Session 7: 07_CLOSEOUT
Si GO → Session 4: 07_CLOSEOUT (directement)
```

**Artefacts** :
```
docs/runs/2026-05-18_1430_security-audit/
├── 01_INTAKE.md
├── 02_AUDIT_REPORT.md
├── 03_DECISION_RECORD.md
├── ...

docs/audits/
└── security-20260518-1445.md    ← rapport horodaté persistant
```

**Mise à jour obligatoire** : `docs/AUDIT_STATUS.md` doit être mis à jour avec le verdict.

---

### Cas 4 — Refactor multi-fichiers (voie STRUCTURÉE)

**Quand** : extraction d'un module, unification d'un pattern dupliqué, migration de signature.

**Approche recommandée** : décomposer en **2 ou 3 runs** dans le PLAN.

**Exemple de PLAN** :

```markdown
## RUN 01 — Extraction du module
**Fichiers** : src/lib/auth.ts (nouveau), src/auth/*.ts (modifs)
**Test** : compile + tests unitaires existants passent

## RUN 02 — Migration des callers
**Fichiers** : src/components/login/*.tsx, src/api/auth/*.ts
**Test** : tests d'intégration verts

## RUN 03 — Suppression du code mort
**Fichiers** : src/auth/legacy/*.ts
**Test** : aucune référence ne subsiste
```

**Chaque run** est exécuté puis reviewé séparément avant le suivant :

```
05_EXECUTION_RUN_01 → 06_REVIEW_RUN_01 → 05_EXECUTION_RUN_02 → 06_REVIEW_RUN_02 → ...
```

**Bénéfice** : si un run casse, on revient au précédent sans tout perdre.

---

### Cas 5 — Reprise après pause (voie CLÔTURE puis nouvelle session)

**Quand** : fin de journée, pause de plusieurs jours, transmission à un collègue ou un autre agent.

**Avant la pause** :

```
/vbb-session-handoff
```

L'agent met à jour `docs/SESSION.md` avec :
- Contexte
- Actions en cours
- Décisions prises
- Points ouverts

Il produit aussi `07_CLOSEOUT.md` dans le dossier de run si une session formelle était en cours.

**À la reprise** (nouvelle session) :

L'agent **lit automatiquement** :
1. `docs/CONTEXT.md` (carte du contexte projet, premier fichier à lire)
2. `docs/PROJECT_MODE.md` (le projet est-il sur les rails ?)
3. `docs/SESSION.md` (où en étions-nous ?)
4. `docs/AUDIT_STATUS.md` (quels risques connus ?)

Il vous propose de **reprendre sur les actions en suspens** sans vous reposer les questions auxquelles vous avez déjà répondu.

---

### Cas 6 — Pre-release check complet (voie AUDIT)

**Quand** : juste avant `git tag v1.0`, avant un déploiement prod, après une refonte majeure.

**Prompt** : `2-p-vbb-release-check`.

**14 skills en 4 waves** :

```
Wave 1 — Sécurité & Risques (obligatoire)
  → security, systemic-risk, data-integrity

Wave 2 — Infrastructure & Ops (obligatoire)
  → db-robustness, ops, ci, legal

Wave 3 — Qualité produit (parallèle possible)
  → api-auditor, performance, accessibility, analytics, spec-validator

Wave 4 — Transition & Consolidation (obligatoire)
  → mode-transition-gate, risk-register
```

**Verdict final** :
- 🟢 **GO** — tous les audits READY
- 🟡 **CONDITIONAL_GO** — risques résiduels acceptés par l'humain
- 🔴 **NO_GO** — au moins un BLOCKED en Wave 1 ou 2

**Sortie attendue** : un `03_DECISION_RECORD.md` signé (rationale) + un rapport persistant dans `docs/audits/release-check-YYYYMMDD-HHMM.md`.

> **Important** : le verdict NO_GO **doit** déclencher un cycle de corrections (04_PLAN → 05_EXECUTION) avant de re-lancer le release-check. Ne pas shipper en passant outre.

---

## 7. Pilotage au quotidien

### 7.1 Comment choisir la voie en 10 secondes

```
La tâche touche-t-elle UN de ces éléments ?
─ contrat de données (DB, API, validation)
─ authentification, sessions, permissions
─ état de production
─ comportement critique multi-fichiers
─ changement structurel significatif
                │
                ├── Oui ──→ STRUCTURÉE (au minimum)
                │
                └── Non
                     │
                     La tâche touche-t-elle UN de ces éléments ?
                     ─ sécurité, intégrité données
                     ─ conformité, RGPD, légal
                     ─ risque systémique
                                │
                                ├── Oui ──→ AUDIT
                                │
                                └── Non ──→ RAPIDE
```

### 7.2 Comment lire un artefact de run

Ouvrez n'importe quel fichier dans `docs/runs/.../` et cherchez :

| Section | Ce qu'elle dit |
|---------|----------------|
| **Voie** (en-tête) | RAPIDE / STRUCTURÉE / AUDIT / CLÔTURE |
| **Statut** | OPEN / IN_PROGRESS / COMPLETE / BLOCKED |
| **Handoff** (fin) | Prochaine phase + entrées attendues + agent recommandé |
| **Points de vigilance** | Risques détectés, à surveiller au run suivant |

**Astuce de pilotage** : si vous découvrez un run sans `07_CLOSEOUT.md`, **la session n'est pas terminée**. Vous savez où reprendre.

### 7.3 Quand changer de session

| Transition | Nouvelle session |
|-----------|-----------------|
| INTAKE → AUDIT | ⚠️ Recommandée |
| AUDIT → DECISION | ✅ **Obligatoire** |
| DECISION → PLAN | ⚠️ Recommandée |
| PLAN → EXECUTION | ⚠️ Recommandée |
| EXECUTION → REVIEW | ✅ **Obligatoire** |
| REVIEW → EXECUTION (modifs) | ✅ **Obligatoire** |
| REVIEW → CLOSEOUT | ⚠️ Recommandée |

**Règle simple à retenir** : *l'agent qui a exécuté ne peut pas reviewer*, et *l'agent qui a audité ne peut pas décider seul*.

### 7.4 Comment escalader proprement

Vous (ou l'agent) êtes en voie RAPIDE et vous découvrez que la tâche touche l'auth :

```markdown
1. STOP toute modification en cours
2. Documentez l'escalade dans 01_INTAKE.md (section "Escalades")
3. Reclassez la tâche en STRUCTURÉE (ou AUDIT)
4. Reprenez à 01_INTAKE avec la nouvelle voie
```

**Ne jamais continuer comme si de rien n'était.** C'est la règle d'escalade non-négociable.

### 7.5 Quand utiliser un prompt canonique vs un spécialisé

| Cas | Choix |
|-----|-------|
| Tâche générique, domaine pas précis | Canonique `01-p-vbb-intake` puis suite |
| Domaine identifié (sécurité, DB, Docker…) | Spécialisé |
| Vous hésitez | Consulter `prompts/t-p-vbb-phase-router.md` |
| Pas de prompt qui colle | Canonique par défaut |

---

## 8. Configuration avancée

### 8.1 Personnaliser le mode du projet

`docs/PROJECT_MODE.md` peut spécifier :

```markdown
**Mode** : DEV | STAGING | PROD
**Niveau de discipline** : LIGHT | STANDARD | STRICT
```

- **STRICT** : voie AUDIT obligatoire pour tout ce qui touche prod/data ; review obligatoire même en STRUCTURÉE.
- **STANDARD** (défaut) : règles vibebackbone classiques.
- **LIGHT** : voie RAPIDE acceptable même pour des modifs multi-fichiers si le risque reste local.

### 8.2 Désactiver / activer des skills

Vous ne voulez pas que l'agent invoque un skill donné ? Renommez son `SKILL.md` en `SKILL.md.disabled` ou supprimez le symlink dans `~/.agents/skills/`.

### 8.3 Travailler à plusieurs agents

vibebackbone est conçu **dès l'origine pour la séparation des rôles entre agents** :

| Agent | Bon pour |
|-------|----------|
| **Claude Code (Sonnet/Opus)** | INTAKE, DECISION, REVIEW, raisonnement complexe |
| **Codex CLI** | EXECUTION (RUN_N), application de patches |
| **Qwen local** | Compaction de contexte, résumés, génération boilerplate |
| **Cursor / Continue** | EXECUTION live, micro-itérations |

**Bonne pratique** : faire le PLAN avec Claude (raisonnement), l'EXECUTION avec Codex (rapidité), le REVIEW avec Claude (regard indépendant).

### 8.4 Compaction de contexte (modèles locaux)

Pour les modèles locaux à fenêtre limitée, **toujours compacter avant 75 %** du contexte disponible. Détails : `AGENTS.md` section 12 (Discipline de contexte LLM).

Outil disponible : MCP `local-llm` → `llm_compress_context`.

### 8.5 Logger les délégations

Pour tracker le ROI des délégations cloud vs local :

```bash
# Via MCP local-llm
llm_log_delegation --task_type compression --provider qwen3.5-9b
```

---

## 9. Anti-patterns — ce qui casse vibebackbone

### ❌ Anti-pattern 1 — "Je fais tout dans la même session pour aller vite"

**Symptôme** : INTAKE + AUDIT + DECISION + PLAN + EXECUTION + REVIEW dans un seul prompt.

**Pourquoi c'est cassé** : aucune séparation de rôle, l'agent valide son propre travail, le contexte sature, les artefacts se mélangent.

**Correctif** : respecter au minimum **EXECUTION → REVIEW dans deux sessions distinctes**.

---

### ❌ Anti-pattern 2 — "Je modifie pendant un audit"

**Symptôme** : phase 02_AUDIT qui contient des `git diff` de corrections.

**Pourquoi c'est cassé** : un audit est en **lecture seule**. Si l'auditeur corrige, il ne peut plus auditer objectivement.

**Correctif** : produire le `02_AUDIT_REPORT.md` complet, **puis** ouvrir une session 04_PLAN pour décider quoi corriger.

---

### ❌ Anti-pattern 3 — "J'invente une voie qui n'existe pas"

**Symptôme** : "voie EXPRESS", "voie HOTFIX", "voie REFACTOR"…

**Pourquoi c'est cassé** : la grammaire devient locale au projet, plus aucun agent ne sait quoi faire.

**Correctif** : utiliser les 4 voies canoniques (RAPIDE / STRUCTURÉE / AUDIT / CLÔTURE). Si vraiment un cas manque, modifier `docs/PILOTAGE.md` (avec audit).

---

### ❌ Anti-pattern 4 — "Je modifie les docs de gouvernance sans audit"

**Symptôme** : edit direct de `AGENTS.md`, `PILOTAGE.md`, `SYSTEM.md`.

**Pourquoi c'est cassé** : ces fichiers sont la **source de vérité**. Les modifier sans trace fait dériver tout le système.

**Correctif** : toute modification de gouvernance passe par voie AUDIT minimum, avec `02_AUDIT_REPORT.md` et `03_DECISION_RECORD.md`.

---

### ❌ Anti-pattern 5 — "Je laisse la session ouverte indéfiniment"

**Symptôme** : `docs/SESSION.md` qui contient des actions vieilles d'une semaine.

**Pourquoi c'est cassé** : la mémoire de session devient obsolète, l'agent reprend sur du contexte périmé.

**Correctif** : à chaque fin de bloc de travail (>30 min sans suite), faire un `07_CLOSEOUT` ou un `t-p-vbb-session-handoff`.

---

### ❌ Anti-pattern 6 — "Je shippe en passant outre un NO_GO"

**Symptôme** : `2-p-vbb-release-check` retourne NO_GO, vous le notez "à voir plus tard" et déployez.

**Pourquoi c'est cassé** : c'est exactement le scénario que vibebackbone est conçu pour empêcher.

**Correctif** : un NO_GO déclenche **obligatoirement** un cycle de correction (`04_PLAN` → `05_EXECUTION` → `06_REVIEW`) avant de relancer le release-check. Sinon, documenter explicitement un CONDITIONAL_GO avec rationale signé.

---

### ❌ Anti-pattern 7 — "Je copie-colle l'output de l'agent sans vérifier les artefacts"

**Symptôme** : vous lisez la réponse de l'agent dans le chat mais ne regardez jamais `docs/runs/`.

**Pourquoi c'est cassé** : la mémoire conversationnelle se perd, les artefacts sont incomplets, vous ne pouvez pas reprendre.

**Correctif** : **chaque** fin de session, ouvrez le dossier de run et vérifiez que les fichiers attendus existent.

---

## 10. FAQ pratique

### Q1 — "vibebackbone, c'est obligatoire pour tout ?"

**Non.** Sur du proof-of-concept, du throwaway code, ou un fix de 30 secondes, c'est overkill. La voie RAPIDE est faite pour ça, et même elle peut être implicite si le risque est nul.

**Règle empirique** : si la modif est censée être dans une PR, vibebackbone vaut le coup.

---

### Q2 — "Comment je sais que l'agent suit vraiment vibebackbone ?"

Trois signaux à vérifier :

1. Il **mentionne la voie** en début de réponse ("classification : RAPIDE").
2. Il **crée un dossier** `docs/runs/YYYY-MM-DD_HHmm_slug/` avec au moins un fichier.
3. Il **refuse certaines actions** ("je ne peux pas reviewer mon propre code, ouvrons une nouvelle session").

Si l'un de ces signaux manque, l'agent ne suit pas la grammaire — relancez avec une référence explicite à `AGENTS.md`.

---

### Q3 — "Je peux mélanger agents (Claude + Codex + Cursor) ?"

**Oui, c'est même encouragé.** vibebackbone est explicitement multi-LLM. La seule contrainte : les artefacts dans `docs/runs/` doivent être lisibles par tous (Markdown standard, pas de format propriétaire).

---

### Q4 — "Pourquoi tant de prompts ? 32 c'est beaucoup."

C'est l'arbitrage hybride documenté dans `PROMPTS_ARCHITECTURE.md` :
- **7 canoniques** suffisent pour 80 % des cas.
- **24 spécialisés** existent pour les contextes précis (sécurité, DB, Docker…).
- **1 router** vous aide à choisir.

Vous n'avez **pas besoin de connaître les 32**. Vous utilisez le router en cas de doute.

---

### Q5 — "Et si je veux modifier vibebackbone lui-même ?"

C'est exactement le cycle qui a produit ce guide :
1. Audit (`PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md`)
2. Décision (`PROMPTS_ALIGNMENT_DECISION.md`)
3. Plan + Execution + Review + Closeout
4. Documentation (ce guide)

vibebackbone se modifie **avec vibebackbone**. La méta-cohérence est vérifiée.

---

### Q6 — "Combien de temps ça prend une voie STRUCTURÉE ?"

| Sous-tâche | Temps |
|------------|-------|
| INTAKE | 5 min |
| PLAN | 10-20 min |
| EXECUTION (par run) | variable, 30 min - 2 h |
| REVIEW | 15-30 min |
| CLOSEOUT | 5 min |

Pour une feature de complexité moyenne : **2 à 4 heures wall-clock**, réparties sur 4-6 sessions courtes (parfois sur plusieurs jours).

---

### Q7 — "Je suis dev solo, est-ce que la séparation executor/reviewer fait sens ?"

**Oui, même en solo.** La séparation est entre **sessions**, pas entre **personnes**. Une nouvelle session = un agent qui repart à vide, sans biais de validation.

C'est comme se relire le lendemain plutôt qu'à chaud.

---

### Q8 — "Que faire si l'agent invente un prompt qui n'existe pas ?"

C'est une dérive classique. Réagir :

> "Stop. Cite-moi le chemin exact du prompt que tu invoques. S'il n'existe pas dans `prompts/` ou `prompts/canonical/`, choisis-en un réel ou crée explicitement le besoin dans un 01_INTAKE."

---

## 11. Cheatsheet

### Triage en 4 questions

```
1. Touche données/auth/prod ?       → STRUCTURÉE
2. Touche sécurité/conformité ?     → AUDIT
3. Aucun des deux ?                 → RAPIDE
4. Fin de session ?                 → CLÔTURE
```

### Les 7 phases et leurs artefacts

```
01_INTAKE       → 01_INTAKE.md
02_AUDIT        → 02_AUDIT_REPORT.md (+ docs/audits/{type}-YYYYMMDD-HHMM.md)
03_DECISION     → 03_DECISION_RECORD.md
04_PLAN         → 04_FIX_PLAN.md
05_EXECUTION    → 05_PATCH_SUMMARY_RUN_N.md
06_REVIEW       → 06_REVIEW_RUN_N.md
07_CLOSEOUT     → 07_CLOSEOUT.md
```

### Transitions de session obligatoires

```
AUDIT → DECISION        ✅ Obligatoire
EXECUTION → REVIEW      ✅ Obligatoire
REVIEW → EXECUTION      ✅ Obligatoire (si modifs)
```

### Commandes Claude Code (post-setup)

```
/vbb-quick-task         Voie RAPIDE
/vbb-structured-task    Voie STRUCTURÉE compacte
/vbb-intake             Phase 01 canonique
/vbb-audit              Phase 02 canonique
/vbb-decision           Phase 03 canonique
/vbb-plan               Phase 04 canonique
/vbb-execution          Phase 05 canonique
/vbb-review             Phase 06 canonique
/vbb-closeout           Phase 07 canonique
/vbb-session-handoff    Handoff de session
/vbb-phase-router       Consulter le router
/vbb-security-pipeline  Audit sécurité ciblé
/vbb-release-check      Pre-release complet (14 skills)
```

(Liste complète : `ls ~/.claude/commands/vbb-*.md`)

### Fichiers à connaître

| Fichier | Rôle |
|---------|------|
| `docs/CONTEXT.md` | MOC / routeur central persistant (premier fichier à lire, versionné) |
| `AGENTS.md` | Grammaire (lue par les agents) |
| `SYSTEM.md` | Runtime Pi |
| `docs/PROJECT_MODE.md` | Signal de mode du repo |
| `docs/SESSION.md` | Brouillon local éphémère (gitignoré) |
| `docs/AUDIT_STATUS.md` | Tableau de bord audits |
| `docs/PILOTAGE.md` | Référence triage |
| `docs/AGENTIC_RUN_PROTOCOL.md` | Référence 7 phases |
| `prompts/t-p-vbb-phase-router.md` | Quel prompt utiliser ? |
| `PROMPTS_ARCHITECTURE.md` | Architecture des prompts |

### Les 6 principes irréductibles

```
1. 1 session = 1 rôle = 1 intention = 1 sortie exploitable
2. Executor ≠ Reviewer (toujours)
3. Audit = lecture seule (toujours)
4. Artefact nommé à chaque phase importante
5. Handoff explicite à la fin de chaque phase
6. Escalade immédiate si le risque change de classe
```

---

## 12. Où aller ensuite

### Vous voulez approfondir

- **Comprendre l'architecture des prompts** → `PROMPTS_ARCHITECTURE.md`
- **Lire le routeur central de contexte** → `docs/CONTEXT.md`
- **Lire le protocole 7 phases formel** → `docs/AGENTIC_RUN_PROTOCOL.md`
- **Voir les règles de session** → `docs/SESSION_RULES.md`
- **Voir le catalogue des 62 skills** → `skills/0-vbb-guide/SKILL.md`
- **Comprendre la mémoire et les handoffs** → `docs/MEMORY_AND_HANDOFF.md`

### Vous voulez contribuer

- **Proposer un skill** → `CONTRIBUTING.md`
- **Proposer un prompt** → ouvrir une issue, expliquer le besoin

### Vous voulez tester en conditions réelles

Commencez petit :

1. Choisir une tâche concrète de votre projet (1 typo, 1 petit refactor, 1 audit léger).
2. Suivre la voie correspondante de bout en bout.
3. Vérifier les artefacts produits.
4. Ajuster `docs/PROJECT_MODE.md` selon votre ressenti (STRICT / STANDARD / LIGHT).

Au bout de 5 tâches, la grammaire devient automatique.

---

## Annexe — Glossaire rapide

| Terme | Définition |
|-------|------------|
| **Voie** | Classe de tâche (RAPIDE / STRUCTURÉE / AUDIT / CLÔTURE) |
| **Phase** | Étape canonique d'un cycle (01–07) |
| **Run** | Itération d'exécution numérotée (RUN_01, RUN_02…) |
| **Artefact** | Fichier Markdown produit par une phase, persistant dans `docs/runs/` |
| **Handoff** | Bloc en fin d'artefact qui transmet à la phase suivante |
| **Skill** | Unité de capacité réutilisable (dossier avec `SKILL.md`) |
| **Prompt** | Template de session prêt à invoquer |
| **Canonique** | Prompt générique d'une phase (01–07) |
| **Spécialisé** | Prompt orienté domaine précis |
| **Router** | Matrice Markdown qui aide à choisir un prompt |
| **Escalade** | Passage d'une voie moins stricte à une voie plus stricte |
| **Mode** | Niveau de discipline du projet (LIGHT / STANDARD / STRICT) |

---

_vibebackbone GUIDE v1.0 — 2026-05-18 — pour les humains qui pilotent des agents._
