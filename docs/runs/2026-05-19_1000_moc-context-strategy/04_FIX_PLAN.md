# 04_FIX_PLAN — Intégration de CONTEXT.md comme MOC / routeur central persistant

**Date** : 2026-05-19  
**Planner** : Architecte documentaire vibebackbone  
**Status** : Plan prêt pour exécution  
**Basé sur** : `03_DECISION_RECORD.md` — Verdict CONDITIONAL_GO

---

## Objectif

Intégrer `docs/CONTEXT.md` comme MOC / routeur central persistant de contexte pour tout agent vibebackbone, avec convention de liens localisés, tout en clarifiant les rôles respectifs de `CONTEXT.md` et `SESSION.md`, en standardisant les sections stables, et en mettant à jour les fichiers de gouvernance nécessaires pour que `CONTEXT.md` soit réellement lu en position 0 d'injection.

---

## Scope délimité

- **Domaine** : Architecture documentaire, gouvernance d'injection de contexte
- **Fichiers créés** : `docs/CONTEXT.md` (RUN 01)
- **Fichiers modifiés** : `AGENTS.md`, `SYSTEM.md`, `CLAUDE.md`, `docs/PILOTAGE.md`, `docs/INDEX.md`, `docs/MEMORY_AND_HANDOFF.md`, `docs/SESSION_RULES.md`, `skills/t-vbb-project-context-init/SKILL.md`, `prompts/t-p-vbb-start-session.md`, templates d'artefacts
- **Hors scope** :
  - Création de `CLOSEOUT_INDEX.md`, `DECISION_INDEX.md`, `RUN_INDEX.md` ou `AUDIT_INDEX.md`
  - Outil automatique de fetch sectionnel, RAG local, scripts de retrieval
  - Suppression ou refactor de `SESSION.md`
  - Modification du code applicatif

---

## RUN 01 — Création + activation minimale de `docs/CONTEXT.md`

### Objectif

Créer `docs/CONTEXT.md` comme MOC / routeur central persistant et mettre à jour les fichiers strictement nécessaires pour qu'il soit lu en position 0 d'injection par tout agent au démarrage normal.

### Fichiers à créer

| Fichier | Action |
|---|---|
| `docs/CONTEXT.md` | Créer — 40 à 80 lignes max |

### Contenu attendu de `docs/CONTEXT.md`

Le fichier doit contenir, dans l'ordre :

1. **Frontmatter léger** — `context_role: moc-central`, `status: active`, `updated: YYYY-MM-DD`
2. **Identité du projet** — nom, mode (lien vers `PROJECT_MODE.md`), vocation courte
3. **Contexte actif** — tâche en cours ou dernière tâche connue, voie active
4. **Runs récents** — 3 à 5 derniers runs avec lien vers `07_CLOSEOUT.md` de chacun
5. **Décisions actives** — 3 à 5 décisions récentes avec lien vers `03_DECISION_RECORD.md`
6. **Risques / audits** — pointeur vers `AUDIT_STATUS.md#risques-identifies--status` + résumé one-liner
7. **Artefacts structurants** — carte courte de `docs/`, `skills/`, `prompts/` avec liens vers sections stables
8. **Points ouverts** — 3 à 5 points ouverts max
9. **Convention de liens localisés** — rappel synthétique des 6 règles (Markdown relatif, sections stables, pas Obsidian-only, pointeurs de fetch, pas de lien vers fichier absent, mise à jour corrélative)
10. **Historique des modifications** — table `Date | Section | Changement`

Règles de contenu :
- **Pointe vers, ne duplique pas.** Si une section dépasse 15 lignes de résumé, la transformer en lien vers un fichier dédié.
- Liens Markdown relatifs exclusivement (`[label](path.md#anchor)`).
- Ancres vers sections stables quand possible.
- Pas de lien vers un fichier qui n'existe pas encore.

### Fichiers à modifier

| Fichier | Changement attendu | Détail |
|---|---|---|
| `AGENTS.md` | Insérer `docs/CONTEXT.md` en position 0 dans la hiérarchie documentaire (section 2) | Ajouter une ligne avant l'entrée PILOTAGE : `0. docs/CONTEXT.md → MOC / routeur central persistant (premier fichier à lire)` |
| `SYSTEM.md` | Ajouter `docs/CONTEXT.md` en tête de la séquence d'injection dans `vibebackbone execution rule` | Ajouter avant `docs/PILOTAGE.md` : `- docs/CONTEXT.md` |
| `CLAUDE.md` | Ajouter `docs/CONTEXT.md` dans les fichiers de gouvernance listés | Ajouter une ligne : `- docs/CONTEXT.md — MOC / routeur central persistant (lire en premier)` |
| `docs/PILOTAGE.md` | Ajouter `docs/CONTEXT.md` dans l'onboarding session et la hiérarchie documentaire | Dans "Onboarding d'une session" : ajouter étape 0 "Lire `docs/CONTEXT.md` pour l'état du projet". Dans "Hiérarchie documentaire" : insérer en position 0 |
| `prompts/t-p-vbb-start-session.md` | Ajouter `docs/CONTEXT.md` comme premier fichier à lire | Dèjà présent dans la liste, vérifier qu'il est en premier |
| `skills/t-vbb-project-context-init/SKILL.md` | Confirmer que `docs/CONTEXT.md` est dans le SCOPE | Déjà listé. Vérifier cohérence avec les sections stables attendues |

### Risques

| Risque | Sévérité | Mitigation |
|---|---|---|
| `CONTEXT.md` est créé mais ignoré par les agents parce qu'aucun fichier de gouvernance ne le référence encore | Élevée | Mise à jour simultanée de `AGENTS.md`, `SYSTEM.md`, `CLAUDE.md`, `PILOTAGE.md` — c'est la condition du CONDITIONAL_GO |
| `CONTEXT.md` grossit au-delà de 80 lignes dès sa création | Faible | Contrôler strictement la portée : pas de duplication, liens vers, pas de narration |
| Liens cassés vers des sections stables qui n'existent pas encore | Moyenne | Ne pas créer de lien vers une section qui n'existe pas. Utiliser des liens de fichier seuls tant que les ancres ne sont pas vérifiées |

### Tests de vérification

1. **Injection position 0** : un agent lisant `AGENTS.md` section 2 voit `CONTEXT.md` comme premier fichier de la hiérarchie.
2. **Injection position 0** : un agent lisant `SYSTEM.md` section `vibebackbone execution rule` voit `CONTEXT.md` en tête.
3. **Injection position 0** : un agent lisant `CLAUDE.md` section fichiers de gouvernance voit `CONTEXT.md`.
4. **Injection position 0** : un agent suivant l'onboarding de `PILOTAGE.md` lit `CONTEXT.md` avant tout autre fichier.
5. **Lecture du prompt start-session** : `docs/CONTEXT.md` apparaît en premier dans la liste de priorité de lecture.
6. **Skills project-context-init** : le SCOPE liste `docs/CONTEXT.md` comme artefact canonique.
7. **Aucun agent ne peut ignorer CONTEXT.md au démarrage normal** : les 4 principaux points d'entrée (`AGENTS.md`, `SYSTEM.md`, `CLAUDE.md`, `PILOTAGE.md`) + le prompt de démarrage le référencent en position 0.

### Critères d'acceptation

- [ ] `docs/CONTEXT.md` existe, fait 40–80 lignes, contient les 10 sections listées.
- [ ] `AGENTS.md` référence `docs/CONTEXT.md` en position 0 de la hiérarchie documentaire.
- [ ] `SYSTEM.md` référence `docs/CONTEXT.md` en tête de la séquence d'injection.
- [ ] `CLAUDE.md` référence `docs/CONTEXT.md` dans les fichiers de gouvernance.
- [ ] `docs/PILOTAGE.md` référence `docs/CONTEXT.md` dans l'onboarding et la hiérarchie documentaire.
- [ ] `prompts/t-p-vbb-start-session.md` liste `docs/CONTEXT.md` en premier.
- [ ] `skills/t-vbb-project-context-init/SKILL.md` inclut `docs/CONTEXT.md` dans le SCOPE.
- [ ] Aucun lien cassé dans `docs/CONTEXT.md`.
- [ ] Aucune duplication de contenu existant — `CONTEXT.md` pointe vers, ne copie pas.

### Handoff vers exécution

- Créer `docs/CONTEXT.md` avec le contenu spécifié.
- Modifier simultanément les 5 fichiers d'injection (`AGENTS.md`, `SYSTEM.md`, `CLAUDE.md`, `PILOTAGE.md`, prompt start-session).
- Vérifier le skill `project-context-init` pour cohérence.
- Commit groupé pour atomicité.

---

## RUN 02 — Clarification documentaire `CONTEXT.md` / `SESSION.md`

### Objectif

Clarifier les rôles respectifs de `CONTEXT.md` et `SESSION.md` dans les fichiers de gouvernance, pour éviter que `CONTEXT.md` ne devienne un second `SESSION.md` ou que `SESSION.md` ne soit utilisé comme carte persistante.

### Fichiers à modifier

| Fichier | Changement attendu | Détail |
|---|---|---|
| `docs/MEMORY_AND_HANDOFF.md` | Ajouter `CONTEXT.md` dans la catégorie "Mémoire officielle" de la hiérarchie de mémoire, avec son rôle explicite | Ajouter une entrée : `docs/CONTEXT.md — MOC / routeur central persistant | Permanent | Tous`. Clarifier que `SESSION.md` est le brouillon éphémère gitignoré. |
| `docs/SESSION_RULES.md` | Ajouter une note distinguant `CONTEXT.md` (carte persistante) de `SESSION.md` (brouillon éphémère) | Dans la section "Rester dans la même session", préciser que `CONTEXT.md` est lu en premier et persiste entre les sessions, tandis que `SESSION.md` est local et éphémère. |
| `docs/INDEX.md` | Ajouter une entrée pour `CONTEXT.md` dans les sections "Par rôle" et "Gouvernance" | Dans "Je suis un agent exécutant une tâche" : ajouter "0. Lire `CONTEXT.md` pour l'état du projet". Dans "Gouvernance" : insérer `CONTEXT.md` en position 0. |
| `docs/PILOTAGE.md` | Compléter si RUN 01 n'a pas couvert la hiérarchie documentaire complète | Vérifier que la hiérarchie documentaire dans PILOTAGE liste `CONTEXT.md` en position 0. Si non traité au RUN 01, traiter ici. |

### Risques

| Risque | Sévérité | Mitigation |
|---|---|---|
| `MEMORY_AND_HANDOFF.md` devient confus si `CONTEXT.md` est placé au même niveau que `SESSION.md` | Moyenne | Catégoriser explicitement : `CONTEXT.md` dans "Mémoire officielle" (versionné), `SESSION.md` dans "Mémoire de session" (gitignoré) |
| `SESSION_RULES.md` ne mentionne pas `CONTEXT.md` et les agents continuent à lire `SESSION.md` en premier | Faible | Ajout d'une clause explicite dans `SESSION_RULES.md` : "Au démarrage, lire `CONTEXT.md` avant `SESSION.md`." |
| `INDEX.md` duplique le rôle de `CONTEXT.md` | Faible | `INDEX.md` reste un navigateur complet (par rôle, par objectif). `CONTEXT.md` est un routeur d'injection (état courant, décisions actives, liens ciblés). La distinction est explicite dans les deux fichiers. |

### Tests de vérification

1. **Rôles distincts** : `MEMORY_AND_HANDOFF.md` liste `CONTEXT.md` dans "Mémoire officielle" et `SESSION.md` dans "Mémoire de session". Pas de chevauchement.
2. **Ordre de lecture** : `SESSION_RULES.md` mentionne `CONTEXT.md` comme premier fichier à lire au démarrage, `SESSION.md` comme brouillon local.
3. **Navigation** : `INDEX.md` pointe vers `CONTEXT.md` comme premier fichier dans la section agent, et documente que `INDEX.md` est un complément de navigation, pas un substitut.
4. **Non-duplication** : le contenu de `CONTEXT.md` ne duplique pas le contenu de `SESSION.md` et inversement.

### Critères d'acceptation

- [ ] `MEMORY_AND_HANDOFF.md` liste `CONTEXT.md` en "Mémoire officielle" et `SESSION.md` en "Mémoire de session" avec rôles distincts.
- [ ] `SESSION_RULES.md` mentionne explicitement l'ordre : `CONTEXT.md` en premier, `SESSION.md` comme brouillon.
- [ ] `INDEX.md` référence `CONTEXT.md` en position 0 pour les agents et dans la section Gouvernance.
- [ ] `PILOTAGE.md` a été vérifié et, si nécessaire, mis à jour pour la hiérarchie documentaire incluant `CONTEXT.md` en position 0.
- [ ] Aucune confusion possible entre le rôle de `CONTEXT.md` et celui de `SESSION.md` après lecture de ces 4 fichiers.

### Handoff vers exécution

- Modifier `MEMORY_AND_HANDOFF.md` : ajouter `CONTEXT.md` dans la table "Mémoire officielle" et clarifier la distinction de rôle.
- Modifier `SESSION_RULES.md` : ajouter la clause de lecture prioritaire de `CONTEXT.md`.
- Modifier `INDEX.md` : ajouter `CONTEXT.md` dans les sections "Par rôle" (agent) et "Gouvernance".
- Vérifier `PILOTAGE.md` : si la hiérarchie n'est pas complète, compléter.

---

## RUN 03 — Standardisation des liens localisés et sections stables

### Objectif

Identifier les titres canoniques à stabiliser dans les artefacts critiques et définir une convention de liens localisés applicable à tout le dépôt.

### Fichiers à analyser

| Fichier | Sections stables à vérifier / stabiliser |
|---|---|
| `03_DECISION_RECORD.md` (templates et existants) | `## La décision`, `## Justification`, `## Alternatives considérées`, `## Risques acceptés`, `## Handoff` |
| `07_CLOSEOUT.md` (templates et existants) | `## Statut final`, `## Travail effectué`, `## Décisions prises`, `## Points ouverts`, `## Prochaine session recommandée`, `## Mise à jour de la gouvernance` |
| `02_AUDIT_REPORT.md` (templates et existants) | `## Scope audité`, `## Constats clés`, `## Verdicts`, `## Risques remontés`, `## Recommandations`, `## Handoff` |
| `04_FIX_PLAN.md` (templates et existants) | `## Objectif`, `## Scope délimité`, `## Étapes d'implémentation`, `## Risques identifiés`, `## Handoff` |

### Travail attendu

1. **Inventorier les sections stables actuelles** dans chaque template et chaque artefact existant dans `docs/runs/`.
2. **Identifier les écarts** entre les sections existantes et les sections stables listées dans la décision (`03_DECISION_RECORD.md`).
3. **Stabiliser les titres** dans les templates pour qu'ils correspondent aux ancres attendues par `CONTEXT.md` et les liens localisés.
4. **Définir une convention de liens localisés** documentée dans `CONTEXT.md` section `## Convention de liens localisés` et applicable partout :
   - Liens Markdown relatifs uniquement : `[label](path.md)`
   - Ancres vers sections stables : `[label](path.md#section-stable)`
   - Pas de dépendance exclusive aux liens Obsidian `[[...]]`
   - Liens comme pointeurs de fetch, pas comme garantie de chargement automatique
   - Pas de lien vers un fichier qui n'existe pas encore
   - Mise à jour corrélative des liens dans `CONTEXT.md` quand une section stable change de nom

### Fichiers à modifier

| Fichier | Changement attendu |
|---|---|
| `docs/templates/03_DECISION_RECORD_TEMPLATE.md` | Stabiliser les titres de sections pour correspondre aux ancres attendues |
| `docs/templates/07_CLOSEOUT_TEMPLATE.md` | Stabiliser les titres de sections pour correspondre aux ancres attendues |
| `docs/templates/02_AUDIT_REPORT_TEMPLATE.md` | Stabiliser les titres de sections pour correspondre aux ancres attendues |
| `docs/templates/04_FIX_PLAN_TEMPLATE.md` | Stabiliser les titres de sections pour correspondre aux ancres attendues |
| `docs/CONTEXT.md` | Section `## Convention de liens localisés` — déjà créée au RUN 01, vérifier conformité |
| Artefacts existants dans `docs/runs/` | Aucune modification rétroactive — les anciens artefacts conservent leurs titres. La convention s'applique aux futurs artefacts. |

### Risques

| Risque | Sévérité | Mitigation |
|---|---|---|
| Les artefacts existants dans `docs/runs/` ont des titres qui ne correspondent pas aux ancres standardisées | Faible | Pas de rétro-fit. La convention s'applique aux futurs artefacts. Les liens dans `CONTEXT.md` pointeront vers les artefacts existants avec leurs titres actuels. |
| Les templates deviennent trop rigides et freinent l'écriture naturelle | Faible | Seuls les titres de section P0 sont stabilisés. Le contenu des sections reste libre. |
| La convention de liens est perçue comme une contrainte technique et non adoptée | Faible | La convention est documentaire, pas technique. Pas d'outillage imposé. Adoption progressive par cohérence. |

### Tests de vérification

1. **Templates** : chaque template d'artefact structurant a des titres de section qui correspondent aux ancres listées dans le tableau de la décision.
2. **Convention documentée** : `CONTEXT.md` section `## Convention de liens localisés` liste les 6 règles.
3. **Cohérence** : les liens dans `CONTEXT.md` utilisent la convention (Markdown relatif, ancre vers section stable quand possible).
4. **Non-rétroactivité** : les artefacts existants dans `docs/runs/` ne sont pas modifiés.

### Critères d'acceptation

- [ ] Les 4 templates (`02`, `03`, `04`, `07`) ont des titres de sections stables conformes au tableau de la décision.
- [ ] La convention de liens localisés est documentée dans `CONTEXT.md`.
- [ ] Tous les liens dans `CONTEXT.md` respectent la convention (Markdown relatif, ancrages possibles).
- [ ] Aucun lien Obsidian `[[...]]` dans `CONTEXT.md` ou les fichiers de gouvernance modifiés.
- [ ] Les artefacts existants dans `docs/runs/` ne sont pas rétroactivement modifiés.

### Handoff vers exécution

- Modifier les 4 templates pour stabiliser les titres de section.
- Vérifier que `CONTEXT.md` section `## Convention de liens localisés` est cohérente avec les règles de la décision.
- Vérifier les liens dans `CONTEXT.md` pour conformité.
- Ne pas modifier les artefacts existants.

---

## RUN 04 — Mise à jour de la phase `07_CLOSEOUT`

### Objectif

Ajouter l'obligation de mettre à jour `docs/CONTEXT.md` lors d'une clôture formelle (phase 07), sans recopier le closeout complet dans `CONTEXT.md`.

### Fichiers à modifier

| Fichier | Changement attendu | Détail |
|---|---|---|
| `docs/templates/07_CLOSEOUT_TEMPLATE.md` | Ajouter une section `## Mise à jour de CONTEXT.md` avec les instructions | Après la section "Mise à jour de la gouvernance", ajouter : "Mettre à jour `docs/CONTEXT.md` avec : statut du run, lien vers ce closeout, décisions actives si nécessaire, points ouverts, prochaine action." |
| `docs/CONTEXT.md` | Vérifier que les sections `## Runs récents`, `## Décisions actives`, `## Points ouverts` sont structurées pour recevoir ces mises à jour | Format attendu : tableau `Date | Run | Statut | Lien` pour les runs ; liste de décisions avec lien ; liste de points ouverts avec priorité |

### Contenu attendu de la section ajoutée au template closeout

```markdown
## Mise à jour de CONTEXT.md

**Obligation** : à chaque closeout formel, mettre à jour `docs/CONTEXT.md`.

Ajouter uniquement :
- **Statut** : verdict du run (succès, partiel, escalade)
- **Lien vers run** : `[YYYY-MM-DD_HHmm_slug](runs/YYYY-MM-DD_HHmm_slug/07_CLOSEOUT.md)`
- **Décisions actives** : si une décision a été prise, ajouter le lien vers `03_DECISION_RECORD.md`
- **Points ouverts** : si des points ouverts subsistent, les ajouter à la section correspondante
- **Prochaine action** : type et objectif de la prochaine session recommandée

Ne PAS recopier le contenu du closeout dans CONTEXT.md.
```

### Comportement pour les tâches RAPIDES

Pour les tâches en voie RAPIDE (pas de cycle formel 01-07) :
- Pas d'obligation de mettre à jour `CONTEXT.md`.
- Si l'agent estime qu'un événement significatif s'est produit (décision, risque identifié, changement de mode), il peut mettre à jour `CONTEXT.md` à sa discrétion.
- La mise à jour discrétionnaire suit le même format que la mise à jour obligatoire.

### Risques

| Risque | Sévérité | Mitigation |
|---|---|---|
| `CONTEXT.md` devient un journal de tous les runs et dépasse 80 lignes | Moyen | Seuls les 3 à 5 runs les plus récents sont listés. Les runs plus anciens sont accessibles via `INDEX.md` ou `docs/runs/`. |
| Les agents omettent la mise à jour de `CONTEXT.md` lors du closeout | Moyen | Le template `07_CLOSEOUT_TEMPLATE.md` inclut la section obligatoire. Le skill de closeout doit la vérifier. |
| Duplication entre closeout et `CONTEXT.md` | Faible | Règle stricte : `CONTEXT.md` ne contient que statut + lien + points ouverts + prochaine action. Le closeout complet reste dans `07_CLOSEOUT.md`. |

### Tests de vérification

1. **Template** : le template `07_CLOSEOUT_TEMPLATE.md` inclut la section `## Mise à jour de CONTEXT.md`.
2. **Format** : la section spécifie les 5 éléments à ajouter (statut, lien, décisions, points ouverts, prochaine action).
3. **Non-duplication** : la section explicite clairement "Ne PAS recopier le contenu du closeout".
4. **Tâches RAPIDES** : le comportement pour les tâches RAPIDES est documenté (mise à jour discrétionnaire).
5. **Structure de CONTEXT.md** : les sections `## Runs récents`, `## Décisions actives`, `## Points ouverts` sont structurées pour recevoir ces mises à jour.

### Critères d'acceptation

- [ ] Le template `07_CLOSEOUT_TEMPLATE.md` contient la section `## Mise à jour de CONTEXT.md`.
- [ ] La section spécifie les 5 éléments obligatoires et l'interdiction de duplication.
- [ ] Le comportement pour les tâches RAPIDES est documenté.
- [ ] `CONTEXT.md` a des sections structurées pour recevoir les mises à jour de closeout.
- [ ] Le closeout existant du run courant (`docs/runs/2026-05-19_1000_moc-context-strategy/07_CLOSEOUT.md`, quand il sera produit) pourra servir de premier test.

### Handoff vers exécution

- Modifier `docs/templates/07_CLOSEOUT_TEMPLATE.md`.
- Vérifier la structure des sections correspondantes dans `CONTEXT.md`.
- Documenter le comportement pour les tâches RAPIDES (soit dans le template, soit dans `SESSION_RULES.md`).

---

## RUN 05 — Frontmatter minimal des artefacts

### Objectif

Ajouter uniquement les champs P0 de frontmatter aux templates d'artefacts structurants. Reporter les champs avancés à une phase ultérieure.

### Champs P0 à ajouter

| Champ | Description | Obligatoire | Exemple |
|---|---|---|---|
| `context_role` | Rôle de l'artefact dans le contexte projet | Oui | `moc-central`, `audit-report`, `decision-record`, `fix-plan`, `closeout`, `audit-status`, `session-draft` |
| `phase` | Phase du cycle agentique (01-07) | Oui | `02`, `03`, `04`, `05`, `06`, `07` |
| `status` | Statut de l'artefact | Oui | `active`, `completed`, `superseded`, `draft` |
| `run_id` | Identifiant du run | Oui | `2026-05-19_1000_moc-context-strategy` |
| `updated` | Date de dernière mise à jour | Oui | `2026-05-19` |

### Champs reportés (P1, pour phase ultérieure)

| Champ | Pourquoi reporté |
|---|---|
| `topics` | Nécessite une taxonomie qui n'est pas encore définie |
| `related` | Redondant avec les liens localisés si `CONTEXT.md` joue son rôle de routeur |
| `context_priority` | Nécessite une calibration empirique de la charge de contexte |
| `load_policy` | Nécessite un outillage de fetch sectionnel qui n'existe pas encore |

### Fichiers à modifier

| Template | Frontmatter P0 attendu |
|---|---|
| `docs/templates/01_INTAKE_TEMPLATE.md` | `context_role`, `phase: "01"`, `status`, `run_id`, `updated` |
| `docs/templates/02_AUDIT_REPORT_TEMPLATE.md` | `context_role`, `phase: "02"`, `status`, `run_id`, `updated` |
| `docs/templates/03_DECISION_RECORD_TEMPLATE.md` | `context_role`, `phase: "03"`, `status`, `run_id`, `updated` |
| `docs/templates/04_FIX_PLAN_TEMPLATE.md` | `context_role`, `phase: "04"`, `status`, `run_id`, `updated` |
| `docs/templates/05_PATCH_SUMMARY_RUN_TEMPLATE.md` | `context_role`, `phase: "05"`, `status`, `run_id`, `updated` |
| `docs/templates/06_REVIEW_RUN_TEMPLATE.md` | `context_role`, `phase: "06"`, `status`, `run_id`, `updated` |
| `docs/templates/07_CLOSEOUT_TEMPLATE.md` | `context_role`, `phase: "07"`, `status`, `run_id`, `updated` |

### Frontmatter de `docs/CONTEXT.md`

Le frontmatter de `CONTEXT.md` (créé au RUN 01) doit déjà comporter les champs P0 :
- `context_role: moc-central`
- `phase: transverse`
- `status: active`
- `run_id` : N/A (fichier permanent, pas lié à un run)
- `updated` : date de dernière modification

### Risques

| Risque | Sévérité | Mitigation |
|---|---|---|
| Le frontmatter alourdit les artefacts sans valeur ajoutée immédiate | Faible | Les 5 champs P0 sont minimaux et immédiatement utiles pour les agents LLM. Le coût est négligeable. |
| Les artefacts existants n'ont pas de frontmatter | Faible | Pas de rétro-fit. La convention s'applique aux futurs artefacts. Les artefacts existants restent valides. |
| Conflit avec les champs existants des templates (Date, Status, etc.) | Moyen | Aligner les champs P0 avec les champs existants. `status` dans le frontmatter = même valeur que `Status` dans le corps. `updated` dans le frontmatter = même date que `Date` dans le corps. Pas de duplication sémantique — le frontmatter est pour les agents, le corps est pour les humains. |

### Tests de vérification

1. **Templates** : chaque template d'artefact (01 à 07) a un frontmatter YAML avec les 5 champs P0.
2. **Cohérence** : les valeurs de `status` dans le frontmatter correspondent aux valeurs du corps du document.
3. **CONTEXT.md** : le frontmatter de `CONTEXT.md` a les 5 champs P0 (avec `run_id: permanent` ou similaire).
4. **Non-rétroactivité** : les artefacts existants dans `docs/runs/` ne sont pas modifiés.
5. **Champs P1 absents** : aucun des champs reportés (`topics`, `related`, `context_priority`, `load_policy`) n'apparaît dans les templates.

### Critères d'acceptation

- [ ] Les 7 templates d'artefacts (01 à 07) ont un frontmatter YAML avec les 5 champs P0.
- [ ] `docs/CONTEXT.md` a un frontmatter avec les 5 champs P0.
- [ ] Les valeurs de `status` sont cohérentes entre frontmatter et corps.
- [ ] Aucun champ P1 dans les templates.
- [ ] Les artefacts existants dans `docs/runs/` ne sont pas modifiés.

### Handoff vers exécution

- Modifier les 7 templates d'artefacts pour ajouter le frontmatter P0.
- Vérifier le frontmatter de `CONTEXT.md`.
- Ne pas modifier les artefacts existants.

---

## RUN 06 — Vérification globale et closeout

### Objectif

Vérifier la cohérence globale de l'intégration de `docs/CONTEXT.md` comme MOC / routeur central persistant. Confirmer que les critères de la condition du CONDITIONAL_GO sont levés. Préparer le handoff final.

### Fichiers à vérifier

| Fichier | Vérification |
|---|---|
| `docs/CONTEXT.md` | Contenu complet, 40–80 lignes, sections stables présentes, liens valides, frontmatter P0 |
| `AGENTS.md` | `docs/CONTEXT.md` en position 0 dans la hiérarchie documentaire |
| `SYSTEM.md` | `docs/CONTEXT.md` en tête de la séquence d'injection |
| `CLAUDE.md` | `docs/CONTEXT.md` dans les fichiers de gouvernance |
| `docs/PILOTAGE.md` | `docs/CONTEXT.md` dans l'onboarding et la hiérarchie documentaire |
| `docs/MEMORY_AND_HANDOFF.md` | `CONTEXT.md` en "Mémoire officielle", `SESSION.md` en "Mémoire de session", rôles distincts |
| `docs/SESSION_RULES.md` | Clause de lecture prioritaire de `CONTEXT.md` |
| `docs/INDEX.md` | `CONTEXT.md` référencé dans les sections "Par rôle" et "Gouvernance" |
| `prompts/t-p-vbb-start-session.md` | `docs/CONTEXT.md` en premier dans la liste de lecture |
| `skills/t-vbb-project-context-init/SKILL.md` | `docs/CONTEXT.md` dans le SCOPE |
| `docs/templates/07_CLOSEOUT_TEMPLATE.md` | Section `## Mise à jour de CONTEXT.md` présente |
| Templates d'artefacts (01 à 07) | Frontmatter P0 présent |

### Vérifications spécifiques

1. **Références croisées cohérentes** : tous les fichiers qui référencent `docs/CONTEXT.md` le font de manière cohérente (même rôle, même position dans la séquence d'injection).
2. **Aucune contradiction** : aucun fichier ne définit `SESSION.md` comme persistant ou `CONTEXT.md` comme éphémère.
3. **Aucune duplication excessive** : `CONTEXT.md` ne duplique pas le contenu de `PILOTAGE.md`, `INDEX.md`, ou `SESSION.md`.
4. **Liens Markdown relatifs valides** : tous les liens dans `CONTEXT.md` et les fichiers de gouvernance modifiés pointent vers des fichiers et sections existantes.
5. **Convention de liens respectée** : pas de liens Obsidian `[[...]]` exclusifs, liens comme pointeurs de fetch, pas de liens vers fichiers absents.
6. **Sections stables conformes** : les titres de section dans `CONTEXT.md` correspondent à la liste du decision record.
7. **Templates conformes** : les 7 templates ont le frontmatter P0 et les titres de sections stables.

### Risques

| Risque | Sévérité | Mitigation |
|---|---|---|
| Des incohérences résiduelles subsistent entre les fichiers modifiés | Faible | Vérification systématique par checklist. |
| Des liens cassés sont introduits involontairement | Faible | Vérification manuelle de chaque lien dans `CONTEXT.md`. |
| La condition du CONDITIONAL_GO n'est pas entièrement levée | Élevée | Le RUN 06 doit confirmer que les 7 fichiers de la condition sont mis à jour. Si un fichier est manquant, le RUN 06 le signale comme bloquant. |

### Tests de vérification

1. **Condition CONDITIONAL_GO levée** : les 7 fichiers listés dans le decision record (`AGENTS.md`, `SYSTEM.md`, `CLAUDE.md`, `PILOTAGE.md`, `INDEX.md`, `MEMORY_AND_HANDOFF.md`, `skills/t-vbb-project-context-init/SKILL.md`) référencent `docs/CONTEXT.md` au début de leur séquence de lecture respective.
2. **Injection position 0** : un agent lisant n'importe lequel des principaux points d'entrée voit `CONTEXT.md` comme premier fichier à lire.
3. **Non-duplication** : `CONTEXT.md` ne duplique pas le contenu d'autres fichiers de gouvernance.
4. **Rôles clairs** : `CONTEXT.md` = carte persistante versionnée, `SESSION.md` = brouillon éphémère gitignoré — la distinction est explicite dans au moins 3 fichiers différents.
5. **Liens valides** : tous les liens Markdown dans `CONTEXT.md` pointent vers des fichiers et sections existantes.
6. **Convention de liens** : aucune dépendance exclusive aux liens Obsidian. Tous les liens sont en syntaxe Markdown relative.

### Critères d'acceptation

- [ ] Les 7 fichiers de la condition du CONDITIONAL_GO référencent `docs/CONTEXT.md` en position 0.
- [ ] `CONTEXT.md` est court (40–80 lignes), contient les 10 sections attendues.
- [ ] Aucun agent ne peut ignorer `CONTEXT.md` au démarrage normal.
- [ ] Les rôles de `CONTEXT.md` et `SESSION.md` sont clairement distingués dans au moins 3 fichiers.
- [ ] Aucune duplication excessive entre `CONTEXT.md` et les autres fichiers de gouvernance.
- [ ] Les 7 templates d'artefacts ont le frontmatter P0.
- [ ] Le template `07_CLOSEOUT_TEMPLATE.md` inclut la section de mise à jour de `CONTEXT.md`.
- [ ] Tous les liens dans `CONTEXT.md` sont valides.
- [ ] La convention de liens localisés est documentée et respectée.

### Handoff final

- Confirmer la levée de la condition du CONDITIONAL_GO.
- Produire le `07_CLOSEOUT.md` du run courant.
- Mettre à jour `docs/CONTEXT.md` avec le statut du run `2026-05-19_1000_moc-context-strategy`.
- Archiver le plan comme exécuté.

---

## Vue d'ensemble des runs

| RUN | Objectif | Fichiers principaux | Critère d'acceptation principal |
|---|---|---|---|
| 01 | Créer `CONTEXT.md` + activation injection position 0 | `docs/CONTEXT.md`, `AGENTS.md`, `SYSTEM.md`, `CLAUDE.md`, `PILOTAGE.md`, prompt start-session, skill context-init | Aucun agent ne peut ignorer `CONTEXT.md` au démarrage |
| 02 | Clarifier rôles `CONTEXT.md` / `SESSION.md` | `MEMORY_AND_HANDOFF.md`, `SESSION_RULES.md`, `INDEX.md`, `PILOTAGE.md` | Rôles distincts explicites dans ≥3 fichiers |
| 03 | Standardiser sections stables + convention de liens | Templates `02`, `03`, `04`, `07`, `CONTEXT.md` | Templates conformes, convention documentée, liens valides |
| 04 | Mettre à jour closeout pour inclure `CONTEXT.md` | `07_CLOSEOUT_TEMPLATE.md`, `CONTEXT.md` | Obligation de mise à jour documentée, pas de duplication |
| 05 | Ajouter frontmatter P0 aux templates | Templates `01` à `07`, `CONTEXT.md` | 5 champs P0 dans chaque template, pas de champ P1 |
| 06 | Vérification globale + closeout | Tous les fichiers modifiés | Condition CONDITIONAL_GO levée, cohérence vérifiée |

---

## Dépendances entre runs

```
RUN 01 ──→ RUN 02 ──→ RUN 03 ──→ RUN 04 ──→ RUN 05 ──→ RUN 06
  │           │           │           │           │          │
  │           │           │           │           │          └── Vérification globale
  │           │           │           │           └── Frontmatter (peut tourner en parallèle de RUN 04)
  │           │           │           └── Closeout (nécessite RUN 01 + RUN 03)
  │           │           └── Sections stables (nécessite RUN 01)
  │           └── Clarification rôles (nécessite RUN 01)
  └── Création CONTEXT.md + activation injection
```

- **RUN 01** est le prérequis de tous les autres runs.
- **RUN 02** nécessite que `CONTEXT.md` existe (RUN 01).
- **RUN 03** nécessite que `CONTEXT.md` existe avec sa convention de liens (RUN 01).
- **RUN 04** nécessite `CONTEXT.md` (RUN 01) et les sections stables stabilisées (RUN 03).
- **RUN 05** est relativement indépendant mais logiquement suit RUN 04.
- **RUN 06** vérifie l'ensemble et nécessite que tous les runs précédents soient complétés.

---

## Risques transversaux

| Risque | Sévérité | Runs impactés | Mitigation |
|---|---|---|---|
| `CONTEXT.md` grandit au-delà de 80 lignes | Moyen | 01, 04 | Règle stricte : pointer vers, ne pas dupliquer. Si section > 15 lignes, transformer en lien. |
| Les agents continuent à lire `SESSION.md` en premier | Élevée | 01, 02 | Condition du CONDITIONAL_GO : mise à jour simultanée des 5+ fichiers d'injection. Clarification dans `SESSION_RULES.md` et `MEMORY_AND_HANDOFF.md`. |
| Les sections stables sont renommées sans mise à jour de `CONTEXT.md` | Moyen | 03 | Git diff rend les cassures visibles. Les sections stables sont listées dans le decision record. |
| Sur-ingénierie prématurée (index spécialisés, outillage) | Faible | Tous | Ne pas créer d'index spécialisés. Ne pas implémenter de fetch automatique. La convention est documentaire, pas technique. |
| Les artefacts existants dans `docs/runs/` sont modifiés rétroactivement | Faible | 03, 05 | Pas de rétro-fit. La convention s'applique aux futurs artefacts uniquement. |

---

_vibebackbone — 04_FIX_PLAN — MOC / Routeur central CONTEXT.md — 2026-05-19_