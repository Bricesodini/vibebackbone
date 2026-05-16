---
name: 1-vbb-code-doc-gap-integrator
description: |
  Scans repository code to identify documentable units, cross-references against
  existing documentation, and writes missing feature documentation to close the gaps.
  Produces a gap report and creates or updates doc files. This is a builder skill —
  it writes documentation that does not yet exist. Never modifies code.
  Supports two modes: COMPLETE (single agent does all steps) and DELEGATED
  (cloud scouts and prepares, local fills templates per gap).
version: "2.0"
phase: 1
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Code-Doc Gap Integrator

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d'abord.

## ROLE & POSTURE

Tu es un bâtisseur documentaire.

Ton rôle est de détecter ce qui existe dans le code mais n'est pas documenté,
puis d'écrire les fiches manquantes pour combler les écarts.

Tu ne modifies PAS le code.
Tu ne supprimes PAS de fichiers existants.
Tu écris UNIQUEMENT les fichiers documentation manquants ou incomplets.
Tu ne réharmonises PAS la doc existante — c'est le rôle de `1-vbb-doc-harmonizer`.

Règles absolues :

- No code changes
- No file deletions
- No doc↔doc harmonization (out of scope)
- UNKNOWN autorisé
- Evidence required : chaque gap doit pointer vers un fichier/repertoire code réel
- Prefer concrete doc over abstract doc

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo (code source + documentation existante)

**Optionnels :**

- [ ] `docs/PILOTAGE.md`
- [ ] `docs/INDEX.md`
- [ ] `docs/ARCHITECTURE.md`
- [ ] Scope cible (module, répertoire, feature) — si absent, scope = tout le repo
- [ ] Seuil d'écriture : `HIGH` ou `HIGH+MEDIUM` — défaut : `HIGH+MEDIUM`
- [ ] Gaps connus (hints fournis par l'utilisateur)
- [ ] Convention de nommage des fiches (si connue)

**Sources acceptées :** repo local, fichiers de code, documentation existante

## USER QUESTIONS

Avant de démarrer le scan, poser les questions suivantes à l'utilisateur.
Toutes sont optionnelles — si l'utilisateur ne répond pas, utiliser les défauts.

| Question | But | Défaut si absent |
|----------|-----|-----------------|
| **Quel périmètre souhaitez-vous couvrir ?** (module, répertoire, feature, ou tout le repo) | Borner le scan et réduire le contexte à traiter | Tout le repo |
| **Y a-t-il des modules ou features que vous savez non documentés ?** | Accélérer la détection et prioriser | Aucun hint — scan complet |
| **Quel seuil d'écriture ?** (`HIGH` seul ou `HIGH+MEDIUM`) | Contrôler le volume de fiches produites | `HIGH+MEDIUM` |

Ne PAS poser plus de 3 questions. Ne PAS relancer si l'utilisateur passe une question.
Utiliser les défauts silencieusement.

## BLOCKING CONDITIONS

- Si le repo n'est pas accessible → STOP. Message : "Impossible de scanner un dépôt inaccessible."
- Si le repo ne contient aucun fichier de code source → STOP. Message : "Aucun code source détecté — rien à documenter."
- Si le repo est vide ou presque vide (moins de 5 fichiers) → STOP. Message : "Dépôt trop embryonnaire pour une analyse de gaps productive."
- Si la demande porte sur de l'harmonisation doc↔doc → rediriger vers `1-vbb-doc-harmonizer`.

## SCOPE

### Zones du repo

- Code source = toutes les sources applicatives (src/, app/, lib/, modules/, packages/, etc.)
- Config = fichiers de configuration affectant le runtime (ex: .env.example, docker-compose, config/)
- Docs existantes = `docs/`, `README.md`, fichiers `.md` à la racine

### Inclus

- scan des unités documentables dans le code
- recensement la documentation existante
- croisement code↔doc pour identifier les gaps
- écriture des fiches manquantes
- signalement des fiches orphelines (doc sans code correspondant)

### Exclus

- modifications de code/config
- suppression de fichiers
- harmonisation doc↔doc entre fiches existantes
- réécriture de fiches existantes correctes
- audit de dette technique (→ `1-vbb-tech-debt`)
- cartographie de dépendances (→ `t-vbb-dependency-mapper`)

## EXECUTION MODES

Ce skill支持两种执行模式，根据可用模型选择：

### Mode COMPLETE — agent unique

Utilisé quand un seul agent est disponible, ou quand le modèle a suffisamment
de contexte pour traiter tout le repo.

L'agent exécute les 4 étapes séquentiellement (voir PROCESS ci-dessous).
Le template par défaut est appliqué directement à l'étape 4.

### Mode DELEGATED — cloud prépare, local exécute

Utilisé quand un modèle local est disponible comme subagent.
Le modèle cloud (orchestrateur) exécute les étapes 1-3 et prépare
les micro-contextes. Le modèle local exécute l'étape 4 par gap.

Répartition :

| Étape | Responsable | Raison |
|-------|-------------|--------|
| 1 — Scanner le code | ☁️ Cloud | Nécessite de voir large, juger ce qui est documentable |
| 2 — Scanner la doc | ☁️ Cloud | Nécessite de parcourir toutes les fiches |
| 3 — Croisement + diff | ☁️ Cloud | Nécessite jugement de sévérité, comparaison |
| 4 — Écrire les fiches | 🖥️ Local | Travail focalisé, template à remplir, scope réduit |

En mode DELEGATED, le cloud prépare un micro-contexte par gap (voir MICRO-CONTEXT CONTRACT).
Le local reçoit chaque micro-contexte et produit une fiche.

## PROCESS

Exécuter strictement dans l'ordre. Chaque étape produit un output qui alimente la suivante.
Ne pas sauter d'étape. Ne pas merger des étapes.

### Étape 1 — Scanner le code

Parcourir le repo et identifier les **unités documentables**.

Si un scope cible a été fourni, limiter le scan à ce scope.

Une unité est documentable si elle satisfait **au moins une** de ces conditions :

- C'est un endpoint ou route API (public ou interne)
- C'est un module avec ≥ 3 exports publics
- C'est un répertoire dédié à une feature fonctionnelle (ex: `src/auth/`, `src/billing/`)
- C'est un fichier de configuration qui affecte le comportement runtime
- C'est un type/interface/contract qui définit une surface publique
- C'est un script utilitaire avec des flags ou options documentables
- C'est un composant UI réutilisable

Ne PAS inclure :

- Les tests (sauf si le setup de test est une procédure documentable)
- Le boilerplate généré (ex: scaffolding par défaut)
- Les fichiers purement internes sans surface publique

Pour chaque unité, noter :

| Champ | Description |
|---|---|
| **Nom** | Nom de l'unité (feature, module, endpoint) |
| **Emplacement** | Chemin dans le repo |
| **Type** | `endpoint` / `module` / `feature` / `config` / `contract` / `script` / `component` |
| **Surface** | Exports, routes, ou points d'entrée publics |

### Étape 2 — Scanner la documentation existante

Parcourir `docs/` et les fichiers `.md` à la racine.

Pour chaque fiche, noter :

| Champ | Description |
|---|---|
| **Fichier** | Chemin du fichier doc |
| **Sujet** | Feature/module/topic documenté |
| **Couverte** | Liste des unités code référencées ou impliquées |

Déterminer la **convention de nommage** des fiches existantes :
- Structure des répertoires (plat, `docs/features/`, `docs/modules/`, etc.)
- Modèle de nommage (`{nom}.md`, `{nom}-note.md`, etc.)
- Sections récurrentes dans les fiches existantes

Si ≥ 3 fiches suivent une structure cohérente → la capturer comme **convention détectée**.
Sinon → noter "Aucune convention détectée — template par défaut applicable".

### Étape 3 — Croisement code↔doc

Comparer les deux inventaires :

- **GAP** = unité documentable dans le code SANS fiche doc correspondante
- **ORPHELIN** = fiche doc SANS unité code correspondante (code supprimé, renommé, ou doc anticipée)
- **COUVERT** = unité code AVEC fiche doc existante

Classer chaque gap par sévérité :

- **HIGH** = endpoint API public, feature cœur, config de production
- **MEDIUM** = module interne important, contract de données, composant réutilisable
- **LOW** = utilitaire secondaire, script interne, type helper

Filtrer par le seuil d'écriture (défaut : `HIGH+MEDIUM`).

**En mode DELEGATED** : c'est ici que le cloud prépare les micro-contextes
(voir MICRO-CONTEXT CONTRACT). Chaque gap retenu devient une tâche pour le modèle local.

### Étape 4 — Écrire les fiches manquantes

Pour chaque gap classé HIGH ou MEDIUM (selon le seuil) :

1. Déterminer le chemin de la fiche selon la convention détectée ou le fallback :
   - Si convention détectée → la suivre
   - Si `docs/features/` existe → `docs/features/{nom}.md`
   - Si `docs/` plat → `docs/{nom}.md`
   - Sinon → `docs/{nom}.md`
2. Appliquer le **template par défaut** (voir ci-dessous), sauf si une convention
   de structure a été détectée dans les fiches existantes — auquel cas imiter
   cette structure à la place.
3. Remplir la fiche en s'appuyant UNIQUEMENT sur le code observé.
4. Ne PAS inventer de contenu non observable dans le code.

Pour les gaps LOW :
- Les lister dans le rapport mais ne PAS écrire de fiche immédiatement.

Pour les orphelins :
- Les lister dans le rapport avec une recommandation (archiver, mettre à jour, ou confirmer comme doc anticipée).
- Ne PAS supprimer ou déplacer les fiches orphelines.

## DEFAULT TEMPLATE

Template par défaut pour les fiches feature.
Utilisé quand aucune convention de structure n'est détectée dans les fiches existantes.

Si une convention est détectée (≥ 3 fiches cohérentes), imiter cette convention à la place.

```markdown
# {nom}

## À propos

{1-3 phrases : ce que fait ce module/feature, déduit du code observé}

## Emplacement

`{chemin dans le repo}`

## Surface publique

{liste des exports, endpoints, props, ou points d'entrée observés}

## Configuration

{si applicable : variables, flags, options lues par le module}
{sinon : "Aucune configuration spécifique détectée."}

## Dépendances directes

{modules/packages importés directement par ce code}
```

Chaque champ est directement observable dans le code.
Le modèle n'a pas à inventer — juste lire et reformuler.

Règles de remplissage :

- `À propos` : reformuler en français clair ce que le code fait. Pas de jargon excessif.
- `Emplacement` : chemin exact, pas de description vague.
- `Surface publique` : lister les noms réels (fonctions, classes, endpoints). Pas de paraphrase.
- `Configuration` : si le module lit des variables ou flags, les lister. Sinon, écrire la phrase standard.
- `Dépendances directes` : lister UNIQUEMENT les imports directs du module. Pas les dépendances indirectes.

## MICRO-CONTEXT CONTRACT

En mode DELEGATED, le cloud prépare un micro-contexte pour chaque gap.
Ce micro-contexte est tout ce que le modèle local doit recevoir pour exécuter l'étape 4.

Format du micro-contexte :

```markdown
## Tâche : écrire la fiche pour {nom_du_module}

### Template à suivre
{template par défaut OU convention détectée}

### Code source du module
{contenu des fichiers principaux du module — pas tout le repo, uniquement les fichiers pertinents}

### Fiches existantes proches (pour le style)
{1-2 fiches existantes du même type, comme référence de ton, si disponibles}

### Consigne
Remplis le template ci-dessus en te basant uniquement sur le code fourni.
N'invente rien qui n'est pas observable dans le code.
Écris le fichier à : {chemin_cible}
```

Règles de préparation du micro-contexte :

- Inclure UNIQUEMENT les fichiers du module concerné, pas tout le repo.
- Limiter le code source à ce qui est nécessaire pour comprendre le module.
- Si le module est trop gros, inclure les fichiers d'entrée publics + les types.
- Les fiches existantes proches servent de référence de style, pas de contenu à copier.
- Si aucune fiche proche n'existe, omettre cette section.

## SUPPORT BOUNDARY

Supporté :
- Détection de gaps code→doc dans un repo structuré
- Écriture de fiches manquantes pour les unités HIGH et MEDIUM
- Signalement d'orphelins doc→code
- Scope ciblé sur un module ou répertoire si demandé
- Mode DELEGATED avec préparation de micro-contextes pour modèle local

Non supporté (refuser explicitement) :
- Harmonisation entre fiches existantes → `1-vbb-doc-harmonizer`
- Modification de code → outside scope entirely
- Suppression ou déplacement de fichiers → proposer en texte uniquement
- Audit de dette technique → `1-vbb-tech-debt`
- Cartographie de dépendances → `t-vbb-dependency-mapper`
- Analyse d'impact de changement → `t-vbb-impact-analyzer`

## OUTPUT CONTRACT

Assurer l'existence de `docs/audits/`.

Écrire exactement UN rapport Markdown dans :
`docs/audits/code-doc-gap-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

Le rapport doit contenir :

```markdown
## Verdict

## Mode d'exécution

COMPLETE / DELEGATED

## Périmètre scanné

{scope appliqué : tout le repo, ou module/feature ciblé}

## Unités documentables (inventaire code)

| Nom | Emplacement | Type | Surface |
|-----|-------------|------|---------|
| ... | ... | ... | ... |

## Documentation existante (inventaire doc)

| Fichier | Sujet | Unités couvertes |
|---------|-------|-----------------|
| ... | ... | ... |

## Convention détectée

{description de la convention de nommage/structure, ou "Aucune — template par défaut appliqué"}

## Matrice code↔doc

| Unité code | Fiche doc | Statut | Sévérité |
|------------|----------|--------|----------|
| ... | — | GAP | HIGH |
| — | ... | ORPHELIN | — |
| ... | ... | COUVERT | — |

## Fiches écrites

| Unité | Fichier créé | Template utilisé | Résumé |
|-------|-------------|-----------------|--------|
| ... | docs/features/auth.md | défaut | Documente le middleware d'authentification |

## Orphelins détectés

| Fichier doc | Recommandation |
|------------|----------------|
| ... | Archiver / Mettre à jour / Confirmer anticipé |

## Gaps LOW non écrits

| Unité | Emplacement | Raison |
|-------|-------------|--------|
| ... | ... | Priorité insuffisante |

## Unknowns
```

En plus du rapport, le skill DOIT créer les fichiers de fiche manquants
identifiés à l'étape 4.

## VERDICT RULES

- `READY`
  - tous les gaps HIGH et MEDIUM (selon le seuil) ont été comblés par des fiches écrites
  - la couverture code→doc est complète ou quasi complète
- `PARTIAL`
  - certains gaps n'ont pas pu être comblés (ambiguïté, scope trop large, UNKNOWN)
  - des fiches ont été écrites mais la couverture reste incomplète
- `BLOCKED`
  - impossible de scanner le code efficacement (structure incohérente, monofichier géant)
  - ou impossible de déterminer un chemin de fiche cohérent
- `UNKNOWN`
  - surface de code insuffisante pour produire un inventaire fiable