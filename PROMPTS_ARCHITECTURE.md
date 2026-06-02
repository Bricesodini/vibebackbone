# PROMPTS_ARCHITECTURE — Guide utilisateur des prompts Vibebackbone

**Version** : 1.0 | **Date** : 2026-06-13
**Basé sur** : `docs/archive/prompt-migration/PROMPTS_ALIGNMENT_DECISION.md` · `docs/archive/prompt-migration/PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md`

---

## Vue d'ensemble

Les prompts Vibebackbone sont organisés en **trois couches** :

```
prompts/
├── canonical/          ← 7 prompts de phase (01–07) — référence générique
├── (racine)            ← 25 prompts spécialisés — domaine ou contexte précis
└── t-p-vbb-phase-router.md  ← Matrice de décision — lequel utiliser ?
```

**Règle de base** :
- Utiliser les **canoniques** par défaut, pour n'importe quel contexte
- Utiliser les **spécialisés** quand le domaine ou le contexte est précis
- Consulter le **router** en cas de doute

---

## Comment démarrer

### Noms courts deployes

Les agents peuvent recevoir des noms courts. Ils doivent etre resolus vers les
fichiers Markdown reels avant lecture :

| Nom court | Fichier prompt |
|-----------|----------------|
| `quick-task` | `1-p-vbb-quick-task.md` |
| `structured-task` | `1-p-vbb-structured-task.md` |
| `audit-task` | `2-p-vbb-audit-task.md` |
| `release-check` | `2-p-vbb-release-check.md` |
| `session-handoff` | `t-p-vbb-session-handoff.md` |

### 1. Ouvrir une session

```
t-p-vbb-start-session
```
ou directement :
```
canonical/01-p-vbb-intake
```

### 2. Créer le dossier de run

```
docs/runs/YYYY-MM-DD_HHmm_slug/
```

Exemple : `docs/runs/2026-05-18_1430_auth-audit/`

### 3. Consulter le router si besoin

```
prompts/t-p-vbb-phase-router.md
```

Le router répond à : "Je suis en phase X, voie Y, avec les artefacts Z — quel prompt ?"

---

## Les 4 familles de voies d'exécution

Les MVP ou projets démarrés depuis zéro passent d'abord par le MVP START gate :
`docs/MVP_START_PROTOCOL.md` + skill `0-vbb-rico-readiness`. Si la readiness
n'est pas `READY`, aucun code applicatif ne démarre.

### Voie RAPIDE

Pour les tâches à faible risque, locales et réversibles.

```
01-p-vbb-intake → [1-p-vbb-quick-task] → 07-p-vbb-closeout
```

**Exemple** : corriger une typo, renommer une variable, ajuster un message d'erreur.

**Sessions** : 1 (tout peut tenir dans une session)

**Artefacts** :
```
docs/runs/YYYY-MM-DD_HHmm_slug/
├── 01_INTAKE.md
├── 05_EXECUTION.md
└── 07_CLOSEOUT.md
```

**Note** : `1-p-vbb-quick-task` enchaîne INTAKE + EXECUTION en un seul prompt.

---

### Voie STRUCTURÉE

Pour les tâches qui touchent des contrats de données, plusieurs fichiers, ou de l'auth.

```
01-p-vbb-intake
    ↓
04-p-vbb-plan
    ↓
05-p-vbb-execution (Run 1, Run 2...)
    ↓  ← NOUVELLE SESSION OBLIGATOIRE
06-p-vbb-review
    ↓
07-p-vbb-closeout
```

**Exemple** : ajouter une validation de formulaire avec cohérence DB, refactoriser un module avec dépendances.

**Sessions** : 4–6 minimum (séparation executor/reviewer obligatoire)

**Artefacts** :
```
docs/runs/YYYY-MM-DD_HHmm_slug/
├── 01_INTAKE.md
├── 04_PLAN.md
├── 05_EXECUTION.md
├── 06_REVIEW.md
└── 07_CLOSEOUT.md
```

**Alternative compacte** : `1-p-vbb-structured-task` enchaîne INTAKE + PLAN + EXECUTION en une session. Compléter avec 06_REVIEW et 07_CLOSEOUT séparément.

---

### Voie AUDIT

Pour les tâches qui touchent la sécurité, l'intégrité des données, la conformité, ou un risque systémique.

```
01-p-vbb-intake
    ↓  ← NOUVELLE SESSION RECOMMANDÉE
02-p-vbb-audit
    ↓  ← NOUVELLE SESSION OBLIGATOIRE
03-p-vbb-decision
    ↓
04-p-vbb-plan
    ↓
05-p-vbb-execution
    ↓  ← NOUVELLE SESSION OBLIGATOIRE
06-p-vbb-review
    ↓
07-p-vbb-closeout
```

**Exemple** : audit sécurité avant déploiement, vérification d'intégrité des données, audit conformité RGPD.

**Sessions** : 7–9 (séparation des rôles stricte)

**Artefacts** :
```
docs/runs/YYYY-MM-DD_HHmm_slug/
├── 01_INTAKE.md
├── 02_AUDIT.md
├── 03_DECISION_RECORD.md
├── 04_PLAN.md
├── 05_EXECUTION.md
├── 06_REVIEW.md
└── 07_CLOSEOUT.md

docs/audits/
└── {type}-YYYYMMDD-HHMM.md    ← rapport d'audit horodaté persistant
```

**Alternatives spécialisées** :
- Sécurité : `2-p-vbb-security-pipeline`
- Pre-release complet : `2-p-vbb-release-check`
- Dette technique : `1-p-vbb-tech-debt`

---

### Voie CLÔTURE

Pour fermer une session, produire un handoff, ou préparer une reprise.

```
07-p-vbb-closeout
```
ou
```
t-p-vbb-session-handoff
```

**Exemple** : fin de journée, pause longue, transmission à un autre agent.

---

## Les 7 prompts canoniques

| Prompt | Phase | Rôle | Interdit |
|--------|-------|------|---------|
| `01-p-vbb-intake` | INTAKE | Cadrer, classifier, recommander | Exécuter, auditer en profondeur |
| `02-p-vbb-audit` | AUDIT | Observer, constater, recommander | Corriger, modifier des fichiers |
| `03-p-vbb-decision` | DECISION | Décider, documenter le rationale | Planifier en détail, implémenter |
| `04-p-vbb-plan` | PLAN | Décomposer en runs, définir les tests | Modifier des fichiers, coder |
| `05-p-vbb-execution` | EXECUTION | Appliquer un run | Dépasser le scope, reviewer soi-même |
| `06-p-vbb-review` | REVIEW | Évaluer indépendamment | Implémenter, modifier des fichiers |
| `07-p-vbb-closeout` | CLOSEOUT | Clôturer, documenter, transmettre | Corriger, rouvrir le scope |

---

## Les 25 prompts spécialisés

### Par domaine

| Domaine | Prompts |
|---------|---------|
| **Session** | `t-p-vbb-start-session`, `t-p-vbb-session-handoff` |
| **Triage / Cadrage** | `0-p-vbb-triage`, `0-p-vbb-plan`, `0-p-vbb-before-building` |
| **Exécution compacte** | `1-p-vbb-quick-task`, `1-p-vbb-structured-task` |
| **Documentation** | `1-p-vbb-doc-feature`, `1-p-vbb-post-refacto-coherence` |
| **Évaluation** | `1-p-vbb-tech-debt`, `1-p-vbb-legacy-level`, `2-p-vbb-db-sanity` |
| **Gouvernance** | `1-p-vbb-project-init` |
| **Audit spécialisé** | `2-p-vbb-audit-task`, `2-p-vbb-security-pipeline`, `2-p-vbb-release-check` |
| **Décision** | `2-p-vbb-mode-transition`, `t-p-vbb-branch-policy-check` |
| **Risques** | `3-p-vbb-risk-register` |
| **Qualité** | `4-p-vbb-anti-slop`, `4-p-vbb-after-building` |
| **Infrastructure** | `4-p-vbb-deploy-docker` |
| **Git** | `t-p-vbb-git-sync`, `t-p-vbb-sequenced-ship`, `t-p-vbb-branch-policy-check` |

---

## Convention d'artefacts

### Nommage du dossier de run

```
docs/runs/YYYY-MM-DD_HHmm_slug/
```

- **YYYY-MM-DD** : date (ex: 2026-05-18)
- **HHmm** : heure de démarrage (ex: 1430)
- **slug** : description courte en kebab-case (ex: `auth-audit`, `feature-payment`, `fix-login`)
- Exemple : `docs/runs/2026-05-18_1430_auth-audit/`

### Artefacts par phase

| Phase | Fichier | Obligatoire |
|-------|---------|-------------|
| 01 | `01_INTAKE.md` | ✅ Toujours |
| 02 | `02_AUDIT.md` | Si voie AUDIT |
| 03 | `03_DECISION_RECORD.md` | Si décision formelle |
| 04 | `04_PLAN.md` | Si plan > 5 min |
| 05 | `05_EXECUTION.md` | Si exécution |
| 06 | `06_REVIEW.md` | Si changements validés |
| 07 | `07_CLOSEOUT.md` | ✅ Toujours |

### Rapports d'audit horodatés

```
docs/audits/{type}-YYYYMMDD-HHMM.md
```

Exemples :
- `docs/audits/security-20260518-1445.md`
- `docs/audits/tech-debt-20260518-1442.md`
- `docs/audits/release-check-20260518-1500.md`

---

## Règles de session

| Transition | Nouvelle session |
|-----------|-----------------|
| INTAKE → AUDIT | ⚠️ Recommandée |
| AUDIT → DECISION | ✅ Obligatoire |
| DECISION → PLAN | ⚠️ Recommandée |
| PLAN → EXECUTION | ⚠️ Recommandée |
| EXECUTION → REVIEW | ✅ Obligatoire |
| REVIEW → EXECUTION (modifs) | ✅ Obligatoire |
| REVIEW → CLOSEOUT | ⚠️ Recommandée |

Source complète : `docs/SESSION_RULES.md`

---

## Index rapide — par besoin

| Je veux... | Prompt |
|-----------|--------|
| Démarrer une session | `t-p-vbb-start-session` |
| Cadrer une tâche inconnue | `canonical/01-p-vbb-intake` ou `0-p-vbb-triage` |
| Exécuter une tâche simple | `1-p-vbb-quick-task` |
| Planifier une tâche complexe | `canonical/04-p-vbb-plan` ou `0-p-vbb-plan` |
| Exécuter une tâche structurée | `1-p-vbb-structured-task` |
| Auditer (domaine générique) | `canonical/02-p-vbb-audit` |
| Auditer la sécurité | `2-p-vbb-security-pipeline` |
| Auditer la dette technique | `1-p-vbb-tech-debt` |
| Vérifier la DB | `2-p-vbb-db-sanity` |
| Valider avant un release | `2-p-vbb-release-check` |
| Prendre une décision post-audit | `canonical/03-p-vbb-decision` |
| Compiler les risques | `3-p-vbb-risk-register` |
| Valider avant de construire | `0-p-vbb-before-building` |
| Valider après construction | `4-p-vbb-after-building` |
| Quality gate surface | `4-p-vbb-anti-slop` |
| Déployer avec Docker | `4-p-vbb-deploy-docker` |
| Reviewer un run | `canonical/06-p-vbb-review` |
| Clôturer une session | `canonical/07-p-vbb-closeout` ou `t-p-vbb-session-handoff` |
| Travail long multi-runs | `t-p-vbb-sequenced-ship` |
| Choisir le bon prompt | `t-p-vbb-phase-router` |

---

## Principes de l'architecture

1. **1 session = 1 rôle = 1 intention = 1 sortie exploitable**
2. **Canoniques d'abord** — utiliser les spécialisés seulement si le domaine le justifie
3. **Artefacts nommés** — chaque phase produit un fichier dans `docs/runs/`
4. **Séparation executor/reviewer** — jamais dans la même session
5. **Handoff explicite** — chaque artefact contient les entrées de la phase suivante
6. **Escalade non-secrète** — si le risque augmente, documenter et changer de voie

---

## Références

| Document | Rôle |
|----------|------|
| `prompts/t-p-vbb-phase-router.md` | Matrice de décision des prompts |
| `docs/AGENTIC_RUN_PROTOCOL.md` | Protocole des 7 phases (référence canonique) |
| `docs/SESSION_RULES.md` | Quand rester / changer de session |
| `docs/MEMORY_AND_HANDOFF.md` | Artefacts persistants et handoffs |
| `docs/PILOTAGE.md` | Triage et voies d'exécution |
| `docs/archive/prompt-migration/PROMPTS_ALIGNMENT_DECISION.md` | Décision d'architecture (pourquoi cette structure) |
| `docs/archive/prompt-migration/PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md` | Audit d'alignement (diagnostic original) |

---

_vibebackbone PROMPTS_ARCHITECTURE v1.0 — 2026-06-13_
