# PROMPTS_ALIGNMENT_DECISION

**Décision d'architecture post-audit — Alignement des prompts lanceurs Vibebackbone**

| Métadonnée | Valeur |
|-----------|--------|
| Date | 2026-05-18 |
| Fondée sur | `PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md` |
| Décideur | Brice Sodini |
| Voie | DECISION (post-audit, pré-exécution) |
| Statut | ✅ Validée |

---

## 1. Décision retenue

**Approche hybride Markdown** — Architecture à trois couches :

1. **Couche canonique** : 7 nouveaux prompts (01–07) couvrant le protocole agentic en 7 phases
2. **Couche spécialisée** : 24 prompts existants conservés tels quels (ou minimalement adaptés)
3. **Couche router** : Document Markdown `t-p-vbb-phase-router.md` guidant le choix du prompt selon phase et artefacts

**Cette approche abandonne** :
- ❌ L'orchestrateur exécutable (sequencer en tant qu'agent)
- ❌ La création d'une CLI `vbb`
- ❌ La machine à états (state machine)
- ❌ L'automatisation du routage

**Cette approche retient** :
- ✅ La clarté documentaire
- ✅ La flexibilité utilisateur
- ✅ La compatibilité avec les 24 prompts existants
- ✅ La légèreté (documentation, pas code)

---

## 2. Justification

### Pourquoi pas Option B (Sequencer exécutable) ?

L'Option B proposait un orchestrateur centralisé qui routerait automatiquement les utilisateurs à travers les 7 phases. Mais :

1. **Rigidité** : Un orchestrateur exécutable force une seule voie; les utilisateurs perte flexibilité pour branches non-linéaires
2. **Maintenance** : Chaque évolution du protocole nécessiterait une réécriture de l'orchestrateur
3. **Duplication de responsabilité** : Le sequencer redoublerait le triage déjà présent dans `0-p-vbb-triage`
4. **Philosophie vibebackbone** : La gouvernance privilégie les documents décisionnels + LLM guidance plutôt que les automates

### Pourquoi pas Option C (Remplacer les 24 existants) ?

L'Option C proposait de créer une série canonique 01-07 et déprécier les 24 existants. Mais :

1. **Perte de valeur opérationnelle** : Les 24 prompts existent, fonctionnent, et ont du contexte utilisateur
2. **Migration utilisateurs coûteuse** : Forcer le migration rompt les workflows en place
3. **Réduction de capacité** : Certains prompts (security-pipeline, deploy-docker, sequenced-ship) sont bien pensés; les jeter serait dommage

### Pourquoi l'approche hybride Markdown ?

1. **Cohabitation naturelle** : Canonique + spécialisés coexistent sans conflit
2. **Guidage documentaire** : Le phase-router est une matrice de décision (Markdown = lisible, maintenable)
3. **Flexibilité maximale** : Utilisateurs choisissent leur chemin; pas de forcing
4. **Évolutif** : Ajouter un nouveau prompt spécialisé ne casse rien
5. **Légèreté** : Pas de code, pas d'état machine à maintenir

---

## 3. Architecture cible

### Structure des prompts

```
prompts/
├── canonical/
│   ├── 01-p-vbb-intake.md          [NOUVEAU]
│   ├── 02-p-vbb-audit.md           [NOUVEAU]
│   ├── 03-p-vbb-decision.md        [NOUVEAU]
│   ├── 04-p-vbb-plan.md            [NOUVEAU]
│   ├── 05-p-vbb-execution.md       [NOUVEAU]
│   ├── 06-p-vbb-review.md          [NOUVEAU]
│   └── 07-p-vbb-closeout.md        [NOUVEAU]
│
├── specialized/
│   ├── 0-p-vbb-triage.md           [EXISTANT, minimal adapt]
│   ├── 0-p-vbb-plan.md             [EXISTANT, adapt]
│   ├── 0-p-vbb-before-building.md  [EXISTANT, adapt]
│   ├── 1-p-vbb-quick-task.md       [EXISTANT, adapt]
│   ├── 1-p-vbb-structured-task.md  [EXISTANT, adapt]
│   ├── ... (18 autres spécialisés)
│   └── t-p-vbb-session-handoff.md  [EXISTANT]
│
└── routers/
    └── t-p-vbb-phase-router.md     [NOUVEAU — guide de choix]
```

### Le phase-router : une matrice de décision

`t-p-vbb-phase-router.md` contient une table de décision :

| Phase | Artefacts présents | Voie (rapide/structurée/audit/clôture) | Prompt canonique | Alternatives spécialisées | Conditions d'utilisation |
|-------|-------------------|----------------------------------------|------------------|---------------------------|--------------------------|
| 01_INTAKE | None | Toute voie | `01-p-vbb-intake` | `0-p-vbb-triage`, `t-p-vbb-start-session` | Toujours |
| 02_AUDIT | 01_INTAKE.md | Structurée / Audit | `02-p-vbb-audit` | `2-p-vbb-security-pipeline`, `2-p-vbb-release-check` | Si domaine spécialisé |
| 03_DECISION | 02_AUDIT_REPORT.md | Toute voie | `03-p-vbb-decision` | `3-p-vbb-risk-register`, `2-p-vbb-mode-transition` | Post-audit |
| ... | ... | ... | ... | ... | ... |

**Utilisation** : "Je suis en phase 02_AUDIT avec un problème de sécurité → consulter la ligne 02_AUDIT, colonnes 'spécialisées' → utiliser `2-p-vbb-security-pipeline`"

### Artefacts nommés persistants

Chaque phase produit un artefact nommé horodaté :

| Phase | Artefact persistant |
|-------|-------------------|
| 01_INTAKE | `01_INTAKE_YYYYMMDD_HHMMSS.md` |
| 02_AUDIT | `02_AUDIT_REPORT_YYYYMMDD_HHMMSS.md` |
| 03_DECISION | `03_DECISION_RECORD_YYYYMMDD_HHMMSS.md` |
| 04_PLAN | `04_FIX_PLAN_YYYYMMDD_HHMMSS.md` |
| 05_EXECUTION | `05_PATCH_SUMMARY_RUN_N_YYYYMMDD_HHMMSS.md` |
| 06_REVIEW | `06_REVIEW_RUN_N_YYYYMMDD_HHMMSS.md` |
| 07_CLOSEOUT | `07_CLOSEOUT_YYYYMMDD_HHMMSS.md` |

**Emplacement** : `docs/runs/YYYYMMDD_HHMMSS_<session-name>/`

---

## 4. Ce qui est autorisé

✅ **CRÉER** :
- 7 nouveaux prompts canoniques (01–07)
- Document `t-p-vbb-phase-router.md` (Markdown pur, guide de décision)
- Documentation `PROMPTS_ARCHITECTURE.md` (guide utilisateur)
- Nommage clair des artefacts à chaque phase

✅ **ADAPTER** (minimal) :
- `0-p-vbb-plan` — clarifier INTAKE vs PLAN
- `0-p-vbb-before-building` + `4-p-vbb-before-building` — fusionner
- `1-p-vbb-structured-task` — ajouter noms d'artefacts
- `1-p-vbb-quick-task` — ajouter noms d'artefacts
- `2-p-vbb-release-check` — clarifier les 4 waves (pas les scinder, juste documenter)

✅ **CONSERVER** :
- Les 24 prompts existants (ou presque)
- Leur logique actuelle
- Leur utilité spécialisée

✅ **DOCUMENTER** :
- Quand appeler chaque prompt (matrice phase-router)
- Quel artefact chaque prompt produit
- Comment les phases s'enchaînent

---

## 5. Ce qui reste interdit

❌ **NE PAS CRÉER** :
- Orchestrateur exécutable (sequencer en tant qu'agent qui route automatiquement)
- CLI `vbb` (script bash, python, ou node)
- Machine à états (state machine, automate)
- Service ou agent qui "décide à la place de l'utilisateur"

❌ **NE PAS MODIFIER** (sauf adaptations listées ci-dessus) :
- Les 24 prompts spécialisés existants
- La logique interne des skills (57 skills restent inchangés)
- Les templates de phase (docs/templates/)

❌ **NE PAS INVENTER** :
- Nouvelles voies de gouvernance
- Nouveaux fichiers de gouvernance (PROJECT_MODE.md, SESSION.md, etc.)
- Nouvelles phases du protocole 7 phases

---

## 6. Ordre des runs révisé

### RUN 02 — Créer les prompts canoniques 01–07

**Objectif** : Créer une série de référence qui couvre le protocole agentic complet

**Tâches** :
- [ ] `01-p-vbb-intake` — intake canonique (triage + contexte + gouvernance)
- [ ] `02-p-vbb-audit` — audit canonique (générique, invoque les domaines via router)
- [ ] `03-p-vbb-decision` — decision canonique (consolide décisions post-audit)
- [ ] `04-p-vbb-plan` — plan canonique (détail plan prêt pour exécution)
- [ ] `05-p-vbb-execution` — execution canonique (exécution, produit patch summary)
- [ ] `06-p-vbb-review` — review canonique (review indépendante)
- [ ] `07-p-vbb-closeout` — closeout canonique (clôture + mise à jour docs/SESSION.md)

**Contraintes** :
- Chacun produit un artefact nommé persistant
- Chacun inclut un handoff explicite vers la phase suivante
- Pas d'exécution de skills; juste la structure de phase

**Artefact** : 7 nouveaux fichiers dans `prompts/canonical/`

---

### RUN 03 — Créer le phase-router Markdown

**Objectif** : Créer une matrice de décision documentant quand utiliser quel prompt

**Tâches** :
- [ ] Construire matrice : phase | artefacts | voie | prompt canonique | alternatives spécialisées
- [ ] Documenter conditions d'utilisation (quand appeler une alternative)
- [ ] Créer exemples concrets : "Je suis en audit sécurité → consulter ligne 02_AUDIT → utiliser `2-p-vbb-security-pipeline`"
- [ ] Lister les redondances résolues

**Contraintes** :
- Pure Markdown, pas de logique exécutable
- À jour avec les 24 prompts spécialisés ET les 7 canoniques

**Artefact** : `t-p-vbb-phase-router.md` (matrice + guide)

---

### RUN 04 — Adapter les prompts critiques

**Objectif** : Améliorer les 5 prompts critiques existants sans les réécrire

**Tâches** :
- [ ] `0-p-vbb-plan` — clarifier INTAKE vs PLAN; ajouter artefacts nommés
- [ ] `0-p-vbb-before-building` + `4-p-vbb-before-building` — fusionner; simplifier
- [ ] `1-p-vbb-structured-task` — ajouter noms d'artefacts (01_INTAKE, 04_PLAN, 05_PATCH_SUMMARY)
- [ ] `1-p-vbb-quick-task` — ajouter noms d'artefacts (01_INTAKE, 05_PATCH_SUMMARY)
- [ ] `2-p-vbb-release-check` — documenter les 4 waves; clarifier handoff

**Contraintes** :
- Changements mineurs uniquement (noms, handoffs, clarté)
- Logique métier inchangée
- Pas de réécriture complète

**Artefact** : Versions adaptées des 5 prompts critiques

---

### RUN 05 — Tester sur 3 cas réels

**Objectif** : Valider que la combinaison (canonique + spécialisés + router) fonctionne

**Tâches** :
- [ ] **Cas 1 (RAPIDE)** : Utiliser `01-p-vbb-intake` → consult router → utiliser `1-p-vbb-quick-task` → `07-p-vbb-closeout`
- [ ] **Cas 2 (STRUCTURÉE)** : `01-p-vbb-intake` → `04-p-vbb-plan` → `1-p-vbb-structured-task` → `06-p-vbb-review` → `07-p-vbb-closeout`
- [ ] **Cas 3 (AUDIT complet)** : `01-p-vbb-intake` → `02-p-vbb-audit` (invoque spécialisés) → `03-p-vbb-decision` → `04-p-vbb-plan` → `05-p-vbb-execution` → `06-p-vbb-review` → `07-p-vbb-closeout`

**Validation** :
- Artefacts nommés créés à chaque phase
- Handoffs explicites respectés
- Router guide correctement vers prompts appropriés
- Sessions ne dépassent pas capacité contexte

**Artefact** : Résultats de test + feedback

---

### RUN 06 — Documenter l'architecture des prompts

**Objectif** : Créer un guide utilisateur et documentaire

**Tâches** :
- [ ] Créer `PROMPTS_ARCHITECTURE.md` (guide utilisateur complet)
- [ ] Mettre à jour `AGENTS.md` avec la nouvelle architecture
- [ ] Créer `docs/PROMPTS_DECISION_LOG.md` (log de cette décision)
- [ ] Créer exemples concrets (workflows par voie)
- [ ] Documenter la migration des utilisateurs existants

**Artefact** : Docs complets + exemples d'usage

---

## 7. Handoff vers RUN 02

**Prochaine session** :

| Paramètre | Valeur |
|-----------|--------|
| **Agent** | Claude Opus 4.7 (création de prompts complexes) |
| **Objectif** | Créer 7 prompts canoniques 01–07 |
| **Entrées** | Audit + décision (ce document) + templates |
| **Sortie attendue** | 7 fichiers `.md` dans `prompts/canonical/` |
| **Voie** | EXECUTION → REVIEW → CLOSEOUT |
| **Durée estimée** | 3–4 h |

**Interdictions pour RUN 02** :
- ❌ Ne pas modifier les 24 existants
- ❌ Ne pas créer le router (c'est RUN 03)
- ❌ Ne pas tester (c'est RUN 05)

---

## Conclusion

Cette décision privilégie **clarté documentaire** et **flexibilité** sur **automatisation**. Les utilisateurs gardent le contrôle; le phase-router les guide sans les forcer. La cohabitation (canonique + spécialisés) préserve l'investissement dans les 24 prompts existants tout en apportant une référence claire (7 canoniques).

**Prêt pour RUN 02 ?**

---

**Document signé** : Brice Sodini  
**Date** : 2026-05-18  
**Validé** : ✅
