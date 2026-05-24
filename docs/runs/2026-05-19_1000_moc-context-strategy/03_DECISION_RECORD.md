# 03_DECISION_RECORD — Stratégie de contexte : CONTEXT.md comme MOC central persistant

**Date** : 2026-05-19 10:00  
**Decision-maker** : Brice (propriétaire produit)  
**Status** : Décidée et documentée  
**Basé sur** : Audit MOC / Indexation des Artefacts Structurants Vibebackbone (2026-05-19)

---

## La décision

**Quoi** : Introduire `docs/CONTEXT.md` comme carte persistante du contexte projet, versionnée en git, et point d'entrée de la séquence d'injection de contexte pour tout agent vibebackbone. Ne pas supprimer `docs/SESSION.md`. Clarifier les rôles respectifs de `CONTEXT.md`, `SESSION.md`, `AUDIT_STATUS.md`, `INDEX.md` et `docs/runs/**`. Adopter une convention de liens localisés Markdown-relatifs. Reporter tout index spécialisé et tout outillage automatique à une phase ultérieure.

---

## Quel problème résout-on ?

### Problème constaté

L'audit MOC / Indexation des Artefacts Structurants a identifié un **double vide architectural** :

1. **Absence de point d'entrée de reprise persistant et versionné.**  
   Actuellement, un agent qui ouvre une session doit naviguer empiriquement entre `PILOTAGE.md` (règles opérationnelles), `INDEX.md` (carte de navigation), `PROJECT_MODE.md` (signal de mode), `MEMORY_AND_HANDOFF.md` (conventions mémoire), `SESSION_RULES.md` (règles de session) et `SESSION.md` (brouillon éphémère) pour reconstituer une image complète de l'état du projet. **Aucun de ces fichiers ne joue le rôle de carte de contexte projet versionnée**.  
   - `SESSION.md` est gitignoré et éphémère — il ne survit pas entre les sessions.
   - `INDEX.md` est un navigateur, pas un injecteur — il est conçu pour être consulté, pas pour être injecté en premier dans le contexte d'un agent.
   - `PILOTAGE.md` est opérationnel (règles, voies, escalade) — il ne contient pas la *cartographie* du projet.
   - `PROJECT_MODE.md` est un signal binaire (mode DEV/DISTRIBUTION) — pas un état des lieux.

2. **Confusion entre les rôles de fichiers qui cohabitent dans `docs/`.**  
   `SESSION.md` (brouillon éphémère, gitignoré), `AUDIT_STATUS.md` (tableau de bord, gitignoré), `INDEX.md` (navigateur, versionné), `MEMORY_AND_HANDOFF.md` (conventions, versionné) et les `docs/runs/**` (artefacts persistants, versionnés) ont des cycles de vie et des audiences différents, mais **ces rôles ne sont pas explicitement dissociés dans un document accessible au premier tour de lecture d'un agent**.

3. **Aucune convention de liens localisés.**  
   Les fichiers de gouvernance utilisent des liens Markdown relatifs ponctuellement, mais aucune convention n'exige des liens vers des sections stables, et rien ne distingue le lien-navigation (humain navigant) du lien-fetch (agent récupérant un contenu ciblé). Le style Obsidian `[[...]]` est présent dans certains contextes (skills, templates) mais ne constitue pas une garantie de résolution par un LLM.

### Conséquence

Sans `CONTEXT.md`, chaque agent réinterprète la hiérarchie documentaire à froid, envoie des lectures exploratoires non optimisées, et risque de manquer des artefacts pertinents ou de dupliquer la découverte de contexte déjà faite par des agents précédents.

---

## Pourquoi `CONTEXT.md` plutôt que `CONTEXT_INDEX.md` ?

### Option A — `docs/CONTEXT_INDEX.md` (nom indexé)

- **Description** : Nommer le fichier `CONTEXT_INDEX.md` pour marquer son rôle d'index.
- **Pros** : Explicitation immédiate du rôle d'indexation.
- **Cons** :  
  - Suggère que le fichier est un index passif (navigation) plutôt qu'un routeur actif (injection + contexte).  
  - Crée une attente d'exhaustivité propre à un index (listing complet de tous les fichiers) alors que le besoin est une **carte orientée reprise**, pas un catalogue.  
  - Pollue le namespace avec le suffixe `_INDEX` qui sera aussi utilisé si des index spécialisés sont créés plus tard (`DECISION_INDEX.md`, `RUN_INDEX.md`, etc.), créant une ambiguïté entre le MOC central et les index spécialisés.  
  - Incohérent avec la convention existante (les autres fichiers centraux n'ont pas de suffixe fonctionnel : `PILOTAGE.md`, `SESSION.md`, `PROJECT_MODE.md`).
- **Verdict** : Rejetée — le suffixe `_INDEX` est trompeur et anticipe une structure d'index éclatée qui n'est pas retenue à ce stade.

### Option B — `docs/CONTEXT.md` (nom retenu)

- **Description** : Nommer le fichier `CONTEXT.md` pour marquer son rôle de carte de contexte projet.
- **Pros** :  
  - Nom neutre, cohérent avec la convention vibebackbone (pas de suffixe technique).  
  - Communicate immédiatement son rôle : *c'est le contexte, lisez-le en premier*.  
  - Préserve le suffixe `_INDEX` pour les futurs index spécialisés si le volume du MOC le justifie.  
  - Compatible avec l'injection de contexte : un agent lit `CONTEXT.md` et sait où il est, ce qui existe, et où aller ensuite.
- **Cons** :  
  - Ne porte pas le mot "index" dans le nom — ce qui est intentionnel (le fichier est un MOC, pas un index).
- **Verdict** : Retenue.

---

## Quel est le rôle exact de `CONTEXT.md` ?

`docs/CONTEXT.md` est le **MOC (Map of Content) / routeur central persistant** du projet vibebackbone.

### Ce qu'il est

- Une **carte versionnée** (commit en git) de l'état courant du projet : artefacts existants, liens vers les sections stables, état des audits, structure du dépôt.
- Le **premier fichier injecté** dans le contexte de tout agent lors de l'ouverture d'une session — avant PILOTAGE, avant SESSION, avant AUDIT_STATUS.
- Un **point d'entrée de reprise** : après compaction de contexte ou ouverture d'une nouvelle session, c'est le premier fichier à lire pour savoir où on en est.

### Ce qu'il n'est pas

- Ce n'est pas un **index exhaustif** (rôle de `INDEX.md`, qui reste le navigateur complet du dépôt).
- Ce n'est pas un **brouillon de session** (rôle de `SESSION.md`).
- Ce n'est pas un **tableau de bord d'audit** (rôle de `AUDIT_STATUS.md`).
- Ce n'est pas un **journal de runs** (rôle de `docs/runs/**`).
- Ce n'est pas une **convention de gouvernance** (rôle de `PILOTAGE.md`).

### Contenu attendu

- Identité du projet (nom, mode, vocation).
- Lien vers les sections stables des fichiers de gouvernance (PILOTAGE, PROJECT_MODE, AGENTS.md, SYSTEM.md).
- État résumé des audits et risques (pointeur vers AUDIT_STATUS.md + section `## Risques actifs` si existante).
- Carte des artefacts structurants (docs/, skills/, prompts/, runs/) avec liens vers sections stables.
- Historique succinct des décisions majeures (pointeurs vers les `03_DECISION_RECORD.md` dans `docs/runs/`).
- Convention de liens localisés (cf. section suivante).

### Responsabilités

| Responsabilité | CONTEXT.md | INDEX.md | SESSION.md | AUDIT_STATUS.md |
|---|---|---|---|---|
| Première chose à lire | ✅ | ❌ | ❌ | ❌ |
| Carte du projet (versionnée) | ✅ | ✅ | ❌ | ❌ |
| Point d'entrée de reprise | ✅ | ❌ | ❌ | ❌ |
| Navigation exhaustive | ❌ | ✅ | ❌ | ❌ |
| État de la session courante | ❌ | ❌ | ✅ | ❌ |
| Tableau de bord d'audit | ❌ | ❌ | ❌ | ✅ |
| Éphémère / gitignoré | ❌ | ❌ | ✅ | ✅ |

---

## Quelle est la relation entre CONTEXT.md, SESSION.md, AUDIT_STATUS.md, INDEX.md et docs/runs/** ?

### Carte des rôles

| Fichier | Nature | Versionné | Cycle de vie | Rôle |
|---|---|---|---|---|
| `docs/CONTEXT.md` | MOC / routeur central persistant | ✅ Oui | Permanent — mise à jour à chaque décision ou changement structurel | Premier fichier lu par tout agent. Carte du contexte projet. Point d'entrée de reprise. |
| `docs/SESSION.md` | Brouillon local de session | ❌ Non (gitignoré) | Éphémère — vidé à chaque closeout | Mémoire de reprise pour la session active. Notes ad hoc, état courant, pas de vérité persistante. |
| `docs/AUDIT_STATUS.md` | Tableau de bord des audits et risques | ❌ Non (gitignoré) | Semi-permanent — mis à jour après chaque audit | Vue consolidée des audits passés, verdicts, risques actifs. Miroir des rapports dans `docs/audits/`. |
| `docs/INDEX.md` | Navigateur du dépôt | ✅ Oui | Permanent — mise à jour quand la structure change | Carte de navigation complète. Par rôle, par objectif, avec liens. Conçu pour consultation, pas pour injection en premier. |
| `docs/runs/**` | Artefacts persistants de cycle | ✅ Oui | Permanent — créés par session, jamais supprimés | Audit trail complet. Rapports, décisions, plans, patches, reviews, closeouts. Source de vérité historique. |

### Flux de lecture d'un agent

```
1. docs/CONTEXT.md        → Où suis-je ? Quoi existe ? Quels liens suivre ?
2. docs/SESSION.md        → Où en est la session courante ? (éphémère)
3. docs/AUDIT_STATUS.md   → Quels risques et audits sont actifs ? (tableau de bord)
4. docs/PILOTAGE.md       → Quelles règles appliquer ? (gouvernance opérationnelle)
5. docs/runs/**           → Quelle est l'historique des décisions et actions ? (audit trail)
6. docs/INDEX.md           → Comment naviguer le dépôt en détail ? (navigateur)
```

### Principe de non-duplication

- `CONTEXT.md` **pointe vers** les sections stables d'autres fichiers — il ne duplique pas leur contenu.
- `SESSION.md` peut référencer des décisions, mais la **source de vérité** est dans `docs/runs/**`.
- `AUDIT_STATUS.md` est un **miroir** des rapports dans `docs/audits/` — il ne remplace pas les rapports complets.
- `INDEX.md` est un **complément de navigation**, pas un substitut de `CONTEXT.md`.

---

## Quelle convention de liens localisés adopte-t-on ?

### Règles

1. **Liens Markdown relatifs uniquement.**  
   Exemple : `[PILOTAGE](PILOTAGE.md)`, `[Convention de liens](#convention-de-liens)`, `[Audit sécurité](audits/security-20260516-1445.md)`.  
   ❌ Pas de liens absolus (`/Users/...`), pas de URLs web pour des fichiers locaux.

2. **Liens vers sections stables quand possible.**  
   Exemple : `[Risques identifiés](AUDIT_STATUS.md#risques-identifiés--status)` plutôt que `[AUDIT_STATUS](AUDIT_STATUS.md)` seul.  
   Préférer un ancrage de section vers une section **stable** (i.e., dont le titre ne change pas sans mise à jour de `CONTEXT.md`).

3. **Ne pas dépendre uniquement des liens Obsidian `[[...]]`.**  
   Les liens `[[...]]` sont utiles dans un Vault Obsidian mais ne sont pas résolus par les agents LLM. Dans `CONTEXT.md` et tout fichier de gouvernance vibebackbone, utiliser exclusivement la syntaxe Markdown `[label](path)`.

4. **Les liens sont des pointeurs de fetch, pas une garantie de chargement automatique.**  
   Un lien comme `[Tech Debt](audits/tech-debt-20260516-1442.md#findings)` signifie : *"si tu as besoin du détail du tech debt, va chercher ce fichier à cette section"*.  
   **Il n'implique pas** que l'agent doit charger le contenu de la cible automatiquement dans son contexte. L'agent décide de suivre le lien en fonction de la tâche courante.

5. **Pas de lien vers un fichier qui n'existe pas encore.**  
   Si un artefact est planifié mais pas encore créé, ne pas mettre de lien vers lui. Mentionner son absence comme un point ouvert dans `CONTEXT.md` si pertinent.

6. **Mettre à jour les liens dans `CONTEXT.md` quand les sections stables changent de nom.**  
   `CONTEXT.md` est versionné — un lien cassé sera visible en diff git.

### Sections stables attendues

Les fichiers suivants doivent avoir des **sections stables** (titres qui ne changent pas sans propagation à `CONTEXT.md`) :

| Fichier | Sections stables minimum |
|---|---|
| `docs/CONTEXT.md` | `## Identité du projet`, `## Artefacts structurants`, `## Risques actifs`, `## Décisions récentes`, `## Convention de liens localisés`, `## Historique des modifications` |
| `docs/PILOTAGE.md` | `## Les 4 voies`, `## Règle de triage`, `## Règle d'escalade`, `## Hiérarchie documentaire` |
| `docs/INDEX.md` | `## Par rôle`, `## Par objectif`, `## Gouvernance`, `## Artefacts` |
| `docs/AUDIT_STATUS.md` | `## Tableau de Bord d'Audits`, `## Risques Identifiés & Status`, `## Verdict Global` |
| `docs/SESSION.md` | `## Session active`, `## Actions en cours`, `## Décisions prises`, `## Points ouverts` |
| `docs/PROJECT_MODE.md` | `## Mode`, `## Consignes` |
| `docs/MEMORY_AND_HANDOFF.md` | `## Hiérarchie de mémoire`, `## Handoff` |
| `docs/SESSION_RULES.md` | `## Rester dans la même session`, `## Créer une nouvelle session` |
| `AGENTS.md` | `## Hiérarchie documentaire`, `## Triage opérationnel obligatoire` |

---

## Quels artefacts doivent avoir des sections stables ?

Les artefacts listés dans le tableau ci-dessus sont les **cibles de liens stables**. Ils doivent respecter deux contraintes :

1. **Leur titre de section ne change pas** sans mise à jour corrélative de `CONTEXT.md`.
2. **Leur contenu à ces sections reste structurellement stable** (les données changent, mais la forme du contenu reste prédictible).

### Priorité de stabilité

- **P0 — Structurellement stable, liens actifs vers ces sections requis** : `CONTEXT.md`, `PILOTAGE.md`, `AUDIT_STATUS.md`, `PROJECT_MODE.md`, `AGENTS.md`.
- **P1 — Stable, liens recommandés** : `SESSION.md`, `MEMORY_AND_HANDOFF.md`, `INDEX.md`.
- **P2 — Stable si consulté, liens optionnels** : `SESSION_RULES.md`, `AGENTIC_RUN_PROTOCOL.md`, `TROUBLESHOOTING.md`, `DEPLOYMENT.md`, `RUNBOOK.md`.

---

## Quels fichiers devront être modifiés plus tard ?

### Immédiat (création de CONTEXT.md uniquement)

| Fichier | Modification |
|---|---|
| `docs/CONTEXT.md` | **Créer** — nouveau fichier MOC central persistant |

### Phase suivante (mise à jour de la hiérarchie d'injection)

| Fichier | Modification |
|---|---|
| `AGENTS.md` | Ajouter `docs/CONTEXT.md` en position 0 dans la hiérarchie documentaire (avant PILOTAGE.md). Mettre à jour la section `## Hiérarchie documentaire`. |
| `SYSTEM.md` | Ajouter `docs/CONTEXT.md` au début de la séquence de lecture dans `## vibebackbone execution rule`. |
| `CLAUDE.md` | Ajouter `docs/CONTEXT.md` dans les fichiers de gouvernance listés. |
| `docs/PILOTAGE.md` | Ajouter une référence à `CONTEXT.md` dans `## Onboarding d'une session` et `## Hiérarchie documentaire`. |
| `docs/INDEX.md` | Ajouter une entrée pour `CONTEXT.md` dans `## Par rôle` et `## Gouvernance`. |
| `docs/MEMORY_AND_HANDOFF.md` | Ajouter `CONTEXT.md` dans `## Hiérarchie de mémoire` dans la catégorie "Mémoire officielle". |
| `skills/t-vbb-project-context-init/SKILL.md` | Mettre à jour pour créer `CONTEXT.md` avec les sections stables requises lors de l'initialisation. |

### Phase conditionnelle (si le volume du MOC central devient trop important)

| Fichier | Modification |
|---|---|
| `docs/CLOSEOUT_INDEX.md` | Créer — uniquement si la section "Décisions récentes" de CONTEXT.md dépasse ~80 lignes |
| `docs/DECISION_INDEX.md` | Créer — uniquement si le nombre de 03_DECISION_RECORD.md rend la section "Décisions récentes" de CONTEXT.md illisible |
| `docs/RUN_INDEX.md` | Créer — uniquement si le nombre de runs rend la section "Artefacts structurants" de CONTEXT.md illisible |
| `docs/AUDIT_INDEX.md` | Créer — uniquement si la liste d'audits dans AUDIT_STATUS.md dépasse ~20 entrées |

**Critère de déclenchement** : un index spécialisé est créé **uniquement** quand `CONTEXT.md` devient difficile à scanner en un tour de lecture (~300 lignes ou ~2000 tokens). Ce n'est pas un objectif — c'est un plan de contingence.

---

## Quels risques faut-il éviter ?

### Risque 1 — CONTEXT.md devient un monolithe

- **Description** : `CONTEXT.md` grossit progressivement en dupliquant le contenu d'autres fichiers au lieu de pointer vers eux.
- **Sévérité** : Élevée
- **Mitigation** : Règle stricte — CONTEXT.md **pointe vers**, il ne **duplique pas**. Si une section dépasse 15 lignes de résumé, la transformer en lien vers un fichier dédié. Les index spécialisés (CLOSEOUT_INDEX, DECISION_INDEX, etc.) sont le plan de contingence.

### Risque 2 — SESSION.md et CONTEXT.md sont confondus

- **Description** : Un agent met à jour `CONTEXT.md` comme s'il était éphémère, ou met à jour `SESSION.md` comme s'il était persistant.
- **Sévérité** : Moyenne
- **Mitigation** : Clarification explicite dans `CONTEXT.md` (en-tête) et dans la mise à jour de `MEMORY_AND_HANDOFF.md`. Les rôles sont radicalement différents : CONTEXT.md = carte persistante versionnée, SESSION.md = brouillon éphémère gitignoré.

### Risque 3 — Les liens vers sections stables cassent silencieusement

- **Description** : Une section stable est renommée dans un fichier cible sans mise à jour corrélative dans `CONTEXT.md`.
- **Sévérité** : Moyenne
- **Mitigation** : `CONTEXT.md` est versionné en git — un lien cassé sera visible en diff. Les sections stables sont listées dans cette décision et doivent être traitées comme une interface publique (changement = propagation). Outillage automatique reporté à une phase ultérieure.

### Risque 4 — Sur-ingénierie prématurée des index spécialisés

- **Description** : Créer CLOSEOUT_INDEX, DECISION_INDEX, RUN_INDEX, AUDIT_INDEX avant que le volume ne le justifie.
- **Sévérité** : Faible
- **Mitigation** : Ne pas créer ces index maintenant. Les créer uniquement si `CONTEXT.md` dépasse ~300 lignes ou ~2000 tokens. Cette contrainte est explicite dans la décision.

### Risque 5 — Outillage automatique prématuré (RAG, fetch sectionnel, scripts)

- **Description** : Investir dans du tooling de retrieval automatique avant que le besoin ne soit validé par l'usage.
- **Sévérité** : Faible
- **Mitigation** : Reporter toute automatisation de fetch sectionnel, RAG local, extraction automatique ou script de retrieval à une phase ultérieure. La convention de liens localisés est une convention **documentaire**, pas une spécification **technique**.

### Risque 6 — CONTEXT.md n'est pas injecté en premier

- **Description** : Les agents continuent à lire PILOTAGE.md ou INDEX.md en premier, ignorant CONTEXT.md.
- **Sévérité** : Élevée
- **Mitigation** : La mise à jour de AGENTS.md, SYSTEM.md et CLAUDE.md doit placer `docs/CONTEXT.md` en position 0 dans la séquence d'injection. C'est une **contrainte de la décision** : CONTEXT.md doit être le premier fichier lu par tout agent.

---

## Alternatives considérées

### Option A — Statu quo (pas de CONTEXT.md)

- **Description** : Continuer sans MOC central. Les agents naviguent empiriquement de PILOTAGE → PROJECT_MODE → SESSION → AUDIT_STATUS → INDEX.
- **Verdict** : Rejetée — ne résout pas le problème de point d'entrée de reprise ni la confusion des rôles.

### Option B — Transformer INDEX.md en MOC (au lieu de créer CONTEXT.md)

- **Description** : Augmenter INDEX.md pour jouer le rôle de routeur de contexte en plus de navigateur.
- **Verdict** : Rejetée — INDEX.md est un **navigateur par rôle et par objectif** (structuré pour la consultation). Un MOC d'injection a un rôle différent : être lu en premier, donner l'état courant, pointer vers les sections stables. Fusionner ces deux rôles créerait un fichier qui sert deux objectifs contradictoires (browsable vs inject-first).

### Option C — Créer CONTEXT.md + index spécialisés immédiatement

- **Description** : Créer CONTEXT.md et les 4 index spécialisés (CLOSEOUT, DECISION, RUN, AUDIT) dès maintenant.
- **Verdict** : Rejetée — sur-ingénierie prématurée. Le volume actuel du projet ne justifie pas 4 sous-index.

### Option D — CONTEXT.md comme routeur persistant + convention de liens localisés (retenue)

- **Description** : Créer CONTEXT.md comme MOC central persistant. Adopter la convention de liens localisés. Reporter les index spécialisés et l'outillage automatique.
- **Verdict** : Retenue — minimal, résout le problème immédiatement, préserve l'extensibilité sans l'anticiper.

---

## Décision retenue

**Option D — CONTEXT.md comme routeur persistant + convention de liens localisés**

### Justification

1. Résout le double vide identifié par l'audit (absence de point d'entrée persistant + confusion des rôles).
2. Ne duplique pas — CONTEXT.md pointe vers, il ne remplace pas.
3. Préserve les fichiers existants — pas de suppression, pas de refactor de INDEX.md ou SESSION.md.
4. Extensible — les index spécialisés sont un plan de contingence, pas un blocage.
5. Convention documentaire, pas outillage — la convention de liens localisés est applicable immédiatement sans script ni RAG.
6. Cohérente avec la philosophie vibebackbone — artefacts stables, lisibles par humains et LLM, pas de vérité parallèle.

### Alternatives rejetées et raisons

- **Option A (statu quo)** : ne résout pas le problème.
- **Option B (transformer INDEX.md)** : fusion contradictoire de rôles.
- **Option C (index spécialisés immédiats)** : sur-ingénierie prématurée.

---

## Risques acceptés

| Risque | Sévérité | Justification de l'acceptation |
|--------|----------|-------------------------------|
| Liens vers sections stables cassent silencieusement | Moyenne | Git diff rend les cassures visibles. Les sections stables sont listées dans cette décision. Pas d'outillage automatique à ce stade. |
| Certains agents ignorent CONTEXT.md au début | Faible | La mise à jour de AGENTS.md, SYSTEM.md et CLAUDE.md en phase suivante rend l'injection explicite. Friction temporaire acceptable. |
| Convention de liens localisés partiellement adoptée | Faible | Mesurée par review des diffs. Pas de risque bloquant — un lien relatif cassé est visible. Progressivement adoptée par cohérence. |

---

## Impact estimé

- **Fichiers impactés** : 1 fichier créé (`docs/CONTEXT.md`), 7 fichiers modifiés en phase suivante (AGENTS.md, SYSTEM.md, CLAUDE.md, PILOTAGE.md, INDEX.md, MEMORY_AND_HANDOFF.md, SKILL.md project-context-init)
- **Effort estimé** : 4–6h (création de CONTEXT.md + mise à jour des 7 fichiers de gouvernance)
- **Risque** : Faible (ajout net, pas de suppression, pas de refactor)
- **Dépendances** : Aucune — cette décision est autonome

---

## Contraintes imposées

1. **Créer `docs/CONTEXT.md`** comme MOC / routeur central persistant, versionné en git.
2. **Ne pas supprimer `docs/SESSION.md`** — il conserve son rôle de brouillon éphémère gitignoré.
3. **Clarifier les rôles** : CONTEXT.md = carte persistante versionnée, SESSION.md = brouillon éphémère, AUDIT_STATUS.md = tableau de bord des audits et risques, INDEX.md = navigateur complet, docs/runs/** = audit trail.
4. **Placer `docs/CONTEXT.md` en début de séquence d'injection** — avant PILOTAGE, avant SESSION.
5. **Adopter la convention de liens localisés** : liens Markdown relatifs, liens vers sections stables, pas de dépendance exclusive aux liens Obsidian, liens comme pointeurs de fetch pas comme garantie de chargement automatique.
6. **Ne pas créer d'index spécialisés** (CLOSEOUT_INDEX, DECISION_INDEX, RUN_INDEX, AUDIT_INDEX) à ce stade.
7. **Ne pas implémenter d'outillage automatique** de fetch sectionnel, RAG local, extraction automatique ou script de retrieval — reporter à une phase ultérieure.

---

## Verdict

### ✅ CONDITIONAL_GO

La décision est GO avec une condition :

- **Condition** : la mise à jour de la hiérarchie documentaire (AGENTS.md, SYSTEM.md, CLAUDE.md, PILOTAGE.md, INDEX.md, MEMORY_AND_HANDOFF.md) pour intégrer `docs/CONTEXT.md` en position 0 de la séquence d'injection **doit être exécutée dans la même phase** que la création de `CONTEXT.md`. Si CONTEXT.md est créé sans que la séquence d'injection soit mise à jour, le risque 6 (agents l'ignorant) se matérialise immédiatement.

### Critère de levée de condition

La condition est levée quand les 7 fichiers suivants ont été mis à jour pour référencer `docs/CONTEXT.md` au début de leur séquence de lecture respective :

1. `AGENTS.md` — section `## Hiérarchie documentaire`
2. `SYSTEM.md` — section `## vibebackbone execution rule`
3. `CLAUDE.md` — section `## Fichiers de gouvernance`
4. `docs/PILOTAGE.md` — section `## Onboarding d'une session`
5. `docs/INDEX.md` — section `## Gouvernance`
6. `docs/MEMORY_AND_HANDOFF.md` — section `## Hiérarchie de mémoire`
7. `skills/t-vbb-project-context-init/SKILL.md` — section `## SCOPE`

---

## Handoff

**Phase suivante** : 04_PLAN  
**Agent recommandé** : Planner / Architecte documentaire  
**À transmettre** :  
- Ce decision record  
- Les 7 fichiers à modifier (liste dans "Fichiers devront être modifiés plus tard")  
- Les sections stables attendues (tableau dans "Sections stables attendues")  
- La contrainte de levée de condition (mise à jour simultanée des 7 fichiers)  

**Points de vigilance** :  
- Ne pas implémenter CONTEXT.md sans mettre à jour la hiérarchie d'injection  
- Ne pas dupliquer le contenu d'autres fichiers dans CONTEXT.md (pointer vers, ne pas copier)  
- Ne pas créer les index spécialisés à ce stade  
- Ne pas supprimer ou modifier SESSION.md  

**Priorité** : Haute — ce decision record débloque la résolution d'un vide architectural identifié par audit.

---

_vibebackbone — DECISION MOC / Stratégie de contexte — 2026-05-19_