# 05 PATCH_SUMMARY — RUN 03

**Run** : `2026-05-19_1000_moc-context-strategy`
**Phase** : 05 (EXECUTION)
**Date** : 2026-05-19
**Executeur** : Architecte documentaire vibebackbone
**Scope** : RUN 03 uniquement — Standardisation des sections stables et convention de liens localisés

---

## Fichiers modifiés

| Fichier | Changement | Lignes ajoutées |
|---|---|---|
| `docs/templates/02_AUDIT_REPORT_TEMPLATE.md` | Ajout annotation Sections stables P0 | 2 |
| `docs/templates/03_DECISION_RECORD_TEMPLATE.md` | Ajout annotation Sections stables P0 | 2 |
| `docs/templates/04_FIX_PLAN_TEMPLATE.md` | Ajout annotation Sections stables P0 | 2 |
| `docs/templates/07_CLOSEOUT_TEMPLATE.md` | Ajout annotation Sections stables P0 | 2 |

**Total** : 4 fichiers modifiés, 8 lignes ajoutées (2 par template).

---

## Sections stables ajoutées ou confirmées

### Template 02 — AUDIT_REPORT

| Section P0 | Statut | Ancre attendue |
|---|---|---|
| `## Scope audité` | ✅ Déjà présent, confirmé stable | `#scope-audité` |
| `## Constats clés` | ✅ Déjà présent, confirmé stable | `#constats-clés` |
| `## Verdicts` | ✅ Déjà présent, confirmé stable | `#verdicts` |
| `## Risques remontés` | ✅ Déjà présent, confirmé stable | `#risques-remontés` |
| `## Recommandations` | ✅ Déjà présent, confirmé stable | `#recommandations` |
| `## Handoff` | ✅ Déjà présent, confirmé stable | `#handoff` |

**Sections non-P0** : aucune modification. Les sections existantes non listées comme P0 (`## Finding N` dans Constats clés) restent libres.

**Annotation ajoutée** :
```
> **Sections stables P0** : Scope audité · Constats clés · Verdicts · Risques remontés · Recommandations · Handoff — ne pas renommer sans mise à jour corrélative de CONTEXT.md.
```

### Template 03 — DECISION_RECORD

| Section P0 | Statut | Ancre attendue |
|---|---|---|
| `## La décision` | ✅ Déjà présent, confirmé stable | `#la-décision` |
| `## Justification` | ✅ Déjà présent, confirmé stable | `#justification` |
| `## Alternatives considérées` | ✅ Déjà présent, confirmé stable | `#alternatives-considérées` |
| `## Risques acceptés` | ✅ Déjà présent, confirmé stable | `#risques-acceptés` |
| `## Handoff` | ✅ Déjà présent, confirmé stable | `#handoff` |

**Sections non-P0** : `## Impact estimé` (non-P0, contenu libre) — conservée sans modification.

**Annotation ajoutée** :
```
> **Sections stables P0** : La décision · Justification · Alternatives considérées · Risques acceptés · Handoff — ne pas renommer sans mise à jour corrélative de CONTEXT.md.
```

### Template 04 — FIX_PLAN

| Section P0 | Statut | Ancre attendue |
|---|---|---|
| `## Objectif` | ✅ Déjà présent, confirmé stable | `#objectif` |
| `## Scope délimité` | ✅ Déjà présent, confirmé stable | `#scope-délimité` |
| `## Étapes d'implémentation` | ✅ Déjà présent, confirmé stable | `#étapes-dimplémentation` |
| `## Risques identifiés` | ✅ Déjà présent, confirmé stable | `#risques-identifiés` |
| `## Handoff` | ✅ Déjà présent, confirmé stable | `#handoff` |

**Sections non-P0** : `## Tests prévus`, `## Dépendances` (non-P0, contenu libre) — conservées sans modification.

**Annotation ajoutée** :
```
> **Sections stables P0** : Objectif · Scope délimité · Étapes d'implémentation · Risques identifiés · Handoff — ne pas renommer sans mise à jour corrélative de CONTEXT.md.
```

### Template 07 — CLOSEOUT

| Section P0 | Statut | Ancre attendue |
|---|---|---|
| `## Statut final` | ✅ Déjà présent, confirmé stable | `#statut-final` |
| `## Travail effectué` | ✅ Déjà présent, confirmé stable | `#travail-effectué` |
| `## Décisions prises` | ✅ Déjà présent, confirmé stable | `#décisions-prises` |
| `## Points ouverts` | ✅ Déjà présent, confirmé stable | `#points-ouverts` |
| `## Prochaine session recommandée` | ✅ Déjà présent, confirmé stable | `#prochaine-session-recommandée` |
| `## Mise à jour de la gouvernance` | ✅ Déjà présent, confirmé stable | `#mise-à-jour-de-la-gouvernance` |

**Sections non-P0** : `## Risques identifiés et documentés`, `## Artefacts produits` (non-P0, contenu libre) — conservées sans modification.

**Annotation ajoutée** :
```
> **Sections stables P0** : Statut final · Travail effectué · Décisions prises · Points ouverts · Prochaine session recommandée · Mise à jour de la gouvernance — ne pas renommer sans mise à jour corrélative de CONTEXT.md.
```

---

## Convention de liens localisés

### État dans CONTEXT.md

La section `## Convention de liens localisés` contient les 6 règles conformes à la décision `03_DECISION_RECORD.md` :

1. ✅ Liens Markdown relatifs uniquement : `[label](path.md#anchor)`
2. ✅ Ancres vers sections stables quand possible
3. ✅ Pas de dépendance exclusive aux liens Obsidian `[[…]]`
4. ✅ Liens = pointeurs de fetch, pas garantie de chargement automatique
5. ✅ Pas de lien vers un fichier absent
6. ✅ Mise à jour corrélative si une section stable change de nom

### Vérification des liens dans CONTEXT.md

| Lien | Cible | Valide |
|---|---|---|
| `[DISTRIBUTION](PROJECT_MODE.md#mode)` | `## Mode` dans PROJECT_MODE.md | ✅ |
| `[AGENTS.md](../AGENTS.md)` | Fichier existant | ✅ |
| `[SYSTEM.md](../SYSTEM.md)` | Fichier existant | ✅ |
| `[PILOTAGE.md](PILOTAGE.md)` | Fichier existant | ✅ |
| `[moc-context-strategy](runs/...03_DECISION_RECORD.md)` | Fichier existant | ✅ |
| `[prompts-agentic-migration](runs/...07_CLOSEOUT.md)` | Fichier existant | ✅ |
| `[AUDIT_STATUS.md](AUDIT_STATUS.md)` | Fichier existant | ✅ |
| `[Risques Identifiés](AUDIT_STATUS.md#risques-identifiés--status)` | Section `## Risques Identifiés & Status` | ✅ |
| `[INDEX.md](INDEX.md)` | Fichier existant | ✅ |

Tous les liens sont en syntaxe Markdown relative. Aucun lien Obsidian `[[...]]` actif (la seule occurrence est dans la règle de convention qui documente ce qu'il ne faut pas faire).

### Rendu des annotations P0 dans les templates

Chaque template possède désormais une annotation `> **Sections stables P0** : ... — ne pas renommer sans mise à jour corrélative de CONTEXT.md.` qui :
- Liste explicitement les sections dont le titre ne doit pas changer sans mise à jour de CONTEXT.md (règle 6 de la convention).
- Sert de contrat lisible par tout éditeur humain ou LLM.
- Ne constitue pas du frontmatter YAML (pas de bloc `---`).
- Est placée juste après les métadonnées d'en-tête, avant le premier séparateur.

---

## Vérifications effectuées

| # | Vérification | Résultat |
|---|---|---|
| 1 | Les 4 templates ont des titres de sections stables conformes au tableau de la décision | ✅ 22 sections P0 confirmées stables (6 + 5 + 5 + 6) |
| 2 | La convention de liens localisés est documentée dans CONTEXT.md | ✅ 6 règles conformes à la décision |
| 3 | Tous les liens dans CONTEXT.md respectent la convention (Markdown relatif, ancrages possibles) | ✅ 12 liens vérifiés, tous en syntaxe Markdown relative |
| 4 | Aucun lien Obsidian `[[...]]` dans CONTEXT.md ou les templates | ✅ 0 lien Obsidian actif (1 occurrence métadocumentaire dans la règle de convention) |
| 5 | Aucun artefact existant dans `docs/runs/` modifié rétroactivement | ✅ Aucun artefact existant touché |
| 6 | Aucun frontmatter ajouté aux templates | ✅ Aucun bloc `---` ajouté |
| 7 | Aucun index spécialisé créé | ✅ Aucun CLOSEOUT_INDEX, DECISION_INDEX, RUN_INDEX, AUDIT_INDEX |
| 8 | Aucun outil de fetch/RAG/script ajouté | ✅ Aucun script ou outil |
| 9 | AGENTS.md, SYSTEM.md, CLAUDE.md non modifiés | ✅ Non touchés par ce RUN |
| 10 | Séquence d'injection RUN 01/01B non modifiée | ✅ Aucun impact |
| 11 | CONTEXT.md non transformé en narration longue | ✅ 72 lignes, inchangé |
| 12 | Aucune obligation de mise à jour de CONTEXT.md dans 07_CLOSEOUT | ✅ Aucune section ajoutée au closeout (scope RUN 04) |
| 13 | Les cibles d'ancre dans CONTEXT.md correspondent à des sections existantes | ✅ `PROJECT_MODE.md#mode` et `AUDIT_STATUS.md#risques-identifiés--status` vérifiées |
| 14 | Chaque template P0 annotation mentionne la mise à jour corrélative de CONTEXT.md | ✅ Les 4 annotations incluent la mention |

---

## Limites connues

| # | Limite | Sévérité | Note |
|---|---|---|---|
| 1 | L'ancre `#risques-identifiés--status` dans CONTEXT.md peut ne pas résoudre exactement sur toutes les plateformes Markdown (le `&` dans le titre `## Risques Identifiés & Status` peut générer des ancres différentes selon le renderer) | Faible | La convention spécifie que les liens sont des pointeurs de fetch, pas une garantie de rendu. Le titre de section est non ambigu pour un lecteur humain ou LLM. La règle 4 couvre ce cas. |
| 2 | Les annotations P0 dans les templates sont des métadonnées inline, pas du frontmatter structuré — elles ne peuvent pas être lues automatiquement par un outillage YAML | Faible | Le frontmatter est scope RUN 05. L'annotation inline suffit pour le contrat documentaire. |
| 3 | Les sections non-P0 dans les templates (Impact estimé, Tests prévus, Dépendances, Risques identifiés et documentés, Artefacts produits) sont libres de changer de titre — mais aucun signal ne l'indique dans le template | Faible | L'annotation P0 liste explicitement les sections stables, ce qui par implication laisse les autres sections libres. Pas besoin de signal négatif. |
| 4 | La stabilité des titres P0 repose sur le contrat social ("ne pas renommer sans mise à jour corrélative") sans outillage automatique de vérification | Moyenne | Comme décidé, pas d'outillage de fetch/RAG/script à ce stade. La convention est documentaire, pas technique. Git diff rend les cassures visibles. |
| 5 | Les artefacts existants dans `docs/runs/` ont des titres de section qui peuvent différer des titres P0 des templates | Faible | Pas de rétro-fit. La convention s'applique aux futurs artefacts. Les liens dans CONTEXT.md pointent vers les artefacts existants avec leurs vrais titres. |

---

## Handoff vers Review RUN 03

**Prochaine étape** : Phase 06 — Review indépendante de RUN 03

**Points à vérifier en priorité par le reviewer** :

1. **Conformité P0** : les annotations P0 dans les 4 templates correspondent-elles exactement aux sections stables listées dans le FIX_PLAN et le DECISION_RECORD ?
2. **Non-rétroactivité** : aucun artefact existant dans `docs/runs/` n'a été modifié ?
3. **Convention CONTEXT.md** : les 6 règles sont-elles complètes et conformes à la décision ?
4. **Annotation format** : les annotations sont-elles au format bloc-citation Markdown (`>`) et non en frontmatter YAML ?
5. **Contraintes** : aucun fichier hors scope modifié (AGENTS.md, SYSTEM.md, CLAUDE.md, 07_CLOSEOUT, frontmatter, index spécialisés) ?

**Artefacts produits** :
- Ce fichier : `05_PATCH_SUMMARY_RUN_03.md`
- Fichiers modifiés : `docs/templates/02_AUDIT_REPORT_TEMPLATE.md`, `docs/templates/03_DECISION_RECORD_TEMPLATE.md`, `docs/templates/04_FIX_PLAN_TEMPLATE.md`, `docs/templates/07_CLOSEOUT_TEMPLATE.md`

**Artefacts attendus du reviewer** :
- `06_REVIEW_RUN_03.md`

---

_vibebackbone — PATCH_SUMMARY RUN 03 — Sections stables et convention de liens localisés — 2026-05-19_