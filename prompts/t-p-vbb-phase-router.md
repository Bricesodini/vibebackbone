# t-p-vbb-phase-router — Matrice de décision des prompts Vibebackbone

**Version** : 1.0 | **Date** : 2026-05-18

---

## Mode d'emploi

Ce document est une **matrice de décision**.

Il répond à la question :

> "Je suis en phase X, avec la voie Y, et j'ai les artefacts Z — quel prompt dois-je utiliser ?"

### Structure de l'architecture des prompts

```
prompts/
├── canonical/          ← Prompts de phase génériques (couvrent le protocole 01–07)
│   ├── 01-p-vbb-intake.md
│   ├── 02-p-vbb-audit.md
│   ├── 03-p-vbb-decision.md
│   ├── 04-p-vbb-plan.md
│   ├── 05-p-vbb-execution.md
│   ├── 06-p-vbb-review.md
│   └── 07-p-vbb-closeout.md
│
└── (racine)            ← Prompts spécialisés (domaine ou contexte précis)
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

### Règle de base

**Prompt canonique** = référence générique, applicable dans tous les contextes.
**Prompt spécialisé** = meilleure précision pour un domaine ou un contexte précis.

Utiliser le canonique par défaut. Utiliser le spécialisé quand le contexte le justifie.

---

## Matrice principale

### Phase 01 — INTAKE

| Voie | Contexte | Prompt recommandé | Alternatives spécialisées |
|------|----------|-------------------|--------------------------|
| Toute voie | Début de session, objectif à cadrer | `canonical/01-p-vbb-intake` | `t-p-vbb-start-session` (si reprise de session), `0-p-vbb-triage` (si classification seule) |
| RAPIDE | Tâche simple, risque faible | `canonical/01-p-vbb-intake` → enchaîner `04_PLAN` ou `05_EXECUTION` | `1-p-vbb-quick-task` (si task entière en un seul prompt) |
| STRUCTURÉE | Tâche multi-fichiers ou contrats | `canonical/01-p-vbb-intake` | `0-p-vbb-before-building` (si feature à venir) |
| AUDIT | Sécurité, intégrité, conformité | `canonical/01-p-vbb-intake` | `2-p-vbb-audit-task` (si l'objectif est directement l'audit) |
| CLÔTURE | Fin de session ou reprise | `canonical/01-p-vbb-intake` | `t-p-vbb-start-session` (lecture du contexte seule) |
| Initialisation repo | Premier contact avec un repo non gouverné | `canonical/01-p-vbb-intake` | `1-p-vbb-project-init` (si init de la gouvernance) |

---

### Phase 02 — AUDIT

| Domaine | Contexte | Prompt recommandé | Alternatives spécialisées |
|---------|----------|-------------------|--------------------------|
| Générique | Audit sans domaine précis | `canonical/02-p-vbb-audit` | `2-p-vbb-audit-task` (si domaine à choisir) |
| Sécurité | Vulnérabilités, auth, XSS, injection | `canonical/02-p-vbb-audit` + skill `2-vbb-security` | `2-p-vbb-security-pipeline` (si pipeline complet 4 étapes) |
| Base de données | Sanité DB, migrations, schéma | `canonical/02-p-vbb-audit` + skill `2-vbb-db-robustness` | `2-p-vbb-db-sanity` (si évaluation sanité seule) |
| Intégrité des données | Invariants métier, idempotence, recalculs | `canonical/02-p-vbb-audit` + skill `2-vbb-data-integrity` | — |
| Opérations | Déploiement, monitoring, infra | `canonical/02-p-vbb-audit` + skill `2-vbb-ops` | — |
| CI/CD | Pipeline, tests, build | `canonical/02-p-vbb-audit` + skill `2-vbb-ci` | — |
| Légal / Conformité | RGPD, licences, CGU | `canonical/02-p-vbb-audit` + skill `2-vbb-legal` | — |
| Risques systémiques | Dépendances critiques, SPOF, résilience | `canonical/02-p-vbb-audit` + skill `2-vbb-systemic-risk` | — |
| API / Contrats | Contrats d'interface, breaking changes | `canonical/02-p-vbb-audit` + skill `2-vbb-api-auditor` | — |
| Dette technique | Qualité, complexité, couplage | `canonical/02-p-vbb-audit` + skill `1-vbb-tech-debt` | `1-p-vbb-tech-debt` (si audit dette seul) |
| Legacy | Évaluation du niveau de legacy | `canonical/02-p-vbb-audit` | `1-p-vbb-legacy-level` (si évaluation legacy seule) |
| Qualité de surface | Slop, typos, incohérences de code | `canonical/02-p-vbb-audit` + skill `1-vbb-code-janitor` | `4-p-vbb-anti-slop` (si quality gate seul, read-only) |
| Pre-release | Audit multi-domaines avant déploiement | `canonical/02-p-vbb-audit` × N (une session par domaine) | `2-p-vbb-release-check` (si pre-release gate complet) |

---

### Phase 03 — DECISION

| Contexte | Prompt recommandé | Alternatives spécialisées |
|----------|-------------------|--------------------------|
| Décision post-audit | `canonical/03-p-vbb-decision` | — |
| Décision de mode ou de transition | `canonical/03-p-vbb-decision` | `2-p-vbb-mode-transition` (si verdict dev→prod spécifiquement) |
| Validation de stratégie de branche | `canonical/03-p-vbb-decision` | `t-p-vbb-branch-policy-check` (si branche Git spécifiquement) |
| Consolidation de risques | `canonical/03-p-vbb-decision` | `3-p-vbb-risk-register` (si compilation du registre de risques) |
| Priorisation post-audit multi-domaines | `canonical/03-p-vbb-decision` | `3-p-vbb-risk-register` après `2-p-vbb-release-check` |

---

### Phase 04 — PLAN

| Contexte | Prompt recommandé | Alternatives spécialisées |
|----------|-------------------|--------------------------|
| Plan générique | `canonical/04-p-vbb-plan` | `0-p-vbb-plan` (si plan court, voie rapide) |
| Plan avant feature | `canonical/04-p-vbb-plan` | `0-p-vbb-before-building` ou `4-p-vbb-before-building` (si gate pré-feature) |
| Plan structuré multi-fichiers | `canonical/04-p-vbb-plan` | `1-p-vbb-structured-task` (si task complète avec plan intégré) |
| Plan de déploiement Docker | `canonical/04-p-vbb-plan` | `4-p-vbb-deploy-docker` (si pipeline Docker complet) |
| Plan de cohérence post-refacto | `canonical/04-p-vbb-plan` | `1-p-vbb-post-refacto-coherence` (si post-refactoring) |

---

### Phase 05 — EXECUTION

| Contexte | Prompt recommandé | Alternatives spécialisées |
|----------|-------------------|--------------------------|
| Exécution générique | `canonical/05-p-vbb-execution` | — |
| Tâche rapide (voie RAPIDE) | `canonical/05-p-vbb-execution` | `1-p-vbb-quick-task` (si intake + execution en un seul prompt) |
| Tâche structurée (voie STRUCTURÉE) | `canonical/05-p-vbb-execution` | `1-p-vbb-structured-task` (si plan + execution intégrés) |
| Documentation d'une feature | `canonical/05-p-vbb-execution` | `1-p-vbb-doc-feature` (si documentation seule) |
| Exécution longue multi-runs | `canonical/05-p-vbb-execution` × N | `t-p-vbb-sequenced-ship` (si orchestration longue avec compression contexte) |
| Commit et push | `canonical/05-p-vbb-execution` | `t-p-vbb-git-sync` (si commit/push spécifiquement) |
| Déploiement Docker | `canonical/05-p-vbb-execution` | `4-p-vbb-deploy-docker` (si pipeline Docker complet) |

---

### Phase 06 — REVIEW

| Contexte | Prompt recommandé | Alternatives spécialisées |
|----------|-------------------|--------------------------|
| Review générique (nouvelle session) | `canonical/06-p-vbb-review` | — |
| Validation post-build | `canonical/06-p-vbb-review` | `4-p-vbb-after-building` (si validation complète post-build) |
| Quality gate avant publication | `canonical/06-p-vbb-review` | `4-p-vbb-anti-slop` (si quality gate surface seule, read-only) |

---

### Phase 07 — CLOSEOUT

| Contexte | Prompt recommandé | Alternatives spécialisées |
|----------|-------------------|--------------------------|
| Clôture de session | `canonical/07-p-vbb-closeout` | `t-p-vbb-session-handoff` (si handoff de reprise seul) |
| Clôture avec risk register | `canonical/07-p-vbb-closeout` + `3-p-vbb-risk-register` | — |
| Clôture post-refacto | `canonical/07-p-vbb-closeout` | `1-p-vbb-post-refacto-coherence` (phase 4 du prompt) |

---

## Règles de décision

### Quand utiliser un prompt canonique ?

- Tu démarres une session sans contexte spécifique de domaine
- Tu veux la structure la plus générique et maintenable
- Tu es incertain du prompt spécialisé à utiliser
- Tu formes un agent non familier avec Vibebackbone

### Quand utiliser un prompt spécialisé ?

- Tu sais précisément quel domaine ou outil est concerné
- Le prompt spécialisé couvre exactement ton cas (ex: sécurité, Docker, release)
- Tu veux gagner du temps sur la configuration de phase
- Le prompt spécialisé est noté comme "meilleure précision" dans la matrice

### Règle d'escalade

Si un prompt spécialisé couvre plusieurs phases dans un seul contexte, **vérifier** :
- Peut-il saturer le contexte LLM ? → Si oui, scinder en sessions
- Produit-il tous les artefacts attendus ? → Si non, compléter avec le canonique

---

## Séquences par voie

### Voie RAPIDE

```
01-p-vbb-intake (ou 1-p-vbb-quick-task directement)
    ↓
05-p-vbb-execution
    ↓
07-p-vbb-closeout (ou t-p-vbb-session-handoff)
```

**Prompts alternatifs** : `1-p-vbb-quick-task` enchaîne 01+05 en une session.

---

### Voie STRUCTURÉE

```
01-p-vbb-intake (ou t-p-vbb-start-session)
    ↓
04-p-vbb-plan (ou 0-p-vbb-plan)
    ↓
05-p-vbb-execution (Run 1, Run 2...)
    ↓
06-p-vbb-review      ← NOUVELLE SESSION OBLIGATOIRE
    ↓
07-p-vbb-closeout
```

**Prompts alternatifs** : `1-p-vbb-structured-task` enchaîne 01+04+05. Compléter avec 06 et 07 en sessions séparées.

---

### Voie AUDIT

```
01-p-vbb-intake
    ↓
02-p-vbb-audit       ← NOUVELLE SESSION RECOMMANDÉE
    ↓
03-p-vbb-decision    ← NOUVELLE SESSION OBLIGATOIRE (décideur ≠ auditeur)
    ↓
04-p-vbb-plan
    ↓
05-p-vbb-execution
    ↓
06-p-vbb-review      ← NOUVELLE SESSION OBLIGATOIRE
    ↓
07-p-vbb-closeout
```

**Prompts alternatifs** :
- Audit sécurité : `2-p-vbb-security-pipeline`
- Audit pre-release : `2-p-vbb-release-check`
- Audit dette technique : `1-p-vbb-tech-debt`
- Audit post-refacto : `1-p-vbb-post-refacto-coherence`

---

### Voie CLÔTURE

```
01-p-vbb-intake (ou t-p-vbb-start-session pour lecture contexte)
    ↓
07-p-vbb-closeout (ou t-p-vbb-session-handoff)
```

---

## Règles de session

| Transition | Nouvelle session ? |
|-----------|-------------------|
| 01 → 02 | ⚠️ Recommandée (auditeur distinct) |
| 02 → 03 | ✅ Obligatoire (décideur ≠ auditeur) |
| 03 → 04 | ⚠️ Recommandée (planner distinct) |
| 04 → 05 | ⚠️ Recommandée (exécuteur distinct) |
| 05 → 06 | ✅ Obligatoire (reviewer ≠ exécuteur) |
| 06 → 05 (modifs requises) | ✅ Obligatoire |
| 06 → 07 | ⚠️ Recommandée |
| 05 Run N → 05 Run N+1 | ✅ Même session si <3 runs |

Source : `docs/SESSION_RULES.md`

---

## Convention de nommage des artefacts

| Phase | Artefact | Emplacement |
|-------|----------|------------|
| 01 | `01_INTAKE.md` | `docs/runs/YYYY-MM-DD_HHmm_slug/` |
| 02 | `02_AUDIT_REPORT.md` | `docs/runs/.../` + `docs/audits/{type}-YYYYMMDD-HHMM.md` |
| 03 | `03_DECISION_RECORD.md` | `docs/runs/.../` |
| 04 | `04_FIX_PLAN.md` | `docs/runs/.../` |
| 05 | `05_PATCH_SUMMARY_RUN_N.md` | `docs/runs/.../` |
| 06 | `06_REVIEW_RUN_N.md` | `docs/runs/.../` |
| 07 | `07_CLOSEOUT.md` | `docs/runs/.../` |

**Créer le dossier de run au début de session** :

```
docs/runs/YYYY-MM-DD_HHmm_slug/
```

- `YYYY-MM-DD` : date du jour (ex: 2026-05-18)
- `HHmm` : heure approximative de démarrage (ex: 1430)
- `slug` : description courte (ex: `security-audit`, `feature-auth`, `patch-xss`)
- Exemple complet : `docs/runs/2026-05-18_1430_security-audit/`

---

## Cas particuliers

### Tâche inconnue ou ambiguë

→ Toujours commencer par `canonical/01-p-vbb-intake` ou `0-p-vbb-triage`.

### Audit multi-domaines

→ Une session par domaine d'audit. Ne pas tout mettre dans `2-p-vbb-release-check` si risque de saturation contexte.
→ Utiliser `2-p-vbb-release-check` uniquement si le contexte LLM est large et le périmètre clairement délimité.

### Boucle 05 → 06 → 05 (modifications requises)

```
05-p-vbb-execution (Run 1) → 06-p-vbb-review (MODIFICATIONS REQUISES)
    ↓ nouvelle session
05-p-vbb-execution (Run 2) → 06-p-vbb-review (APPROUVÉ)
    ↓
07-p-vbb-closeout
```

### Escalade en cours d'exécution

Si une exécution (phase 05) révèle un risque inattendu :
→ Arrêter le run, documenter dans le patch summary.
→ Créer une nouvelle session : `01-p-vbb-intake` + voie AUDIT.
→ Ne pas continuer en mode RAPIDE si le risque a escaladé.

### Travail long (contexte LLM limité)

→ Utiliser `t-p-vbb-sequenced-ship` pour orchestrer multi-runs avec compression de contexte.
→ Ou scinder en sessions séparées avec handoff explicite via `t-p-vbb-session-handoff`.

---

## Index rapide — Par besoin

| Besoin | Prompt |
|--------|--------|
| Démarrer une session | `t-p-vbb-start-session` ou `canonical/01-p-vbb-intake` |
| Classifier une tâche | `0-p-vbb-triage` |
| Plan avant une feature | `0-p-vbb-before-building` ou `canonical/04-p-vbb-plan` |
| Tâche simple rapide | `1-p-vbb-quick-task` |
| Tâche structurée | `1-p-vbb-structured-task` |
| Audit dette technique | `1-p-vbb-tech-debt` |
| Évaluer le legacy | `1-p-vbb-legacy-level` |
| Documenter une feature | `1-p-vbb-doc-feature` |
| Audit post-refacto | `1-p-vbb-post-refacto-coherence` |
| Audit générique | `canonical/02-p-vbb-audit` ou `2-p-vbb-audit-task` |
| Audit sécurité | `2-p-vbb-security-pipeline` |
| Audit base de données | `2-p-vbb-db-sanity` |
| Transition dev→prod | `2-p-vbb-mode-transition` |
| Pre-release gate | `2-p-vbb-release-check` |
| Compiler les risques | `3-p-vbb-risk-register` |
| Valider avant de construire | `4-p-vbb-before-building` |
| Valider après construction | `4-p-vbb-after-building` |
| Quality gate surface | `4-p-vbb-anti-slop` |
| Déploiement Docker | `4-p-vbb-deploy-docker` |
| Vérifier la stratégie Git | `t-p-vbb-branch-policy-check` |
| Committer et pusher | `t-p-vbb-git-sync` |
| Travail long multi-runs | `t-p-vbb-sequenced-ship` |
| Clôturer une session | `canonical/07-p-vbb-closeout` ou `t-p-vbb-session-handoff` |

---

_vibebackbone PHASE ROUTER v1.0 — 2026-05-18 · Matrice de décision des prompts_
