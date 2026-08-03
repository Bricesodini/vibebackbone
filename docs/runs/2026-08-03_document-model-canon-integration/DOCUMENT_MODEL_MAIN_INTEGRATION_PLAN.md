---
run_id: "2026-08-03_document-model-canon-integration"
phase: "planning"
status: "proposed"
scope: "git-integration-plan-only"
---

# DOCUMENT_MODEL_MAIN_INTEGRATION_PLAN

## 1. Objet et état d’ancrage

Ce document prépare exclusivement un port contrôlé vers `main`. Il ne porte
aucun fichier canonique, ne crée aucun commit d’intégration et ne publie rien.

État observé dans le worktree au 2026-08-03 :

| Élément | Valeur |
|---|---|
| Référence publiée | `origin/main@067b8ea6e9a7d9bea65a29340bdc38da1361f039` |
| HEAD courant | `55b3696a5f2b681af73384167717bbb318056152` |
| Branche | `HEAD` détaché |
| Commits au-dessus de `origin/main` | 5 |
| État du worktree | Sale : 3 fichiers suivis modifiés et plusieurs runs non suivis |
| Remote observé | `origin` pointe vers GitHub ; aucun upstream utilisable depuis HEAD détaché |

Le SHA de `origin/main` devra être revérifié immédiatement avant tout futur
port. Le présent plan n’autorise ni création de branche ni intégration.

## 2. Inventaire exact des commits produits

| SHA complet | Sujet | Classification | Décision de port |
|---|---|---|---|
| `64bb43e79bf8ce701e486a69c7cdf847eaf2ff0e` | `feat: add document model validation pilot c0-c2` | `VALIDATION_CAPABILITY` | Cherry-pick séquentiel possible, comme capacité expérimentale/interne, après vérification de la base. |
| `6beae84021967f20b3708b6d873bbb19644ab45c` | `feat: extend document model pilot with dts and dgm` | `VALIDATION_CAPABILITY` | Cherry-pick séquentiel possible après C0–C2 ; ne rend pas DTS/DGM canoniques. |
| `f3035f64872a24e97420f05e2abe7b8e71687165` | `feat: add document transition finding routing pilot` | `VALIDATION_CAPABILITY` | Cherry-pick séquentiel possible après C3–C4 ; routage sans remédiation. |
| `668e3e09e1a2ad0575297278af9b88860420c39d` | `feat: align documentary skills with dtp routing` | `SKILL_ALIGNMENT` | Cherry-pick possible après C0–C5 ; port séparé et validé. |
| `55b3696a5f2b681af73384167717bbb318056152` | `docs(context): restore parseable next action` | `DOCUMENTARY_REMEDIATION` | Port conditionnel seulement après revalidation du contenu F-05 sur la nouvelle base ; reconstruction préférable si le contexte courant diffère. |

Source complémentaire non incluse dans cette chaîne :
`cc7ca86ebfef0e443980f5806db32c4351a1bb4d` (`governance: add governed
artifact drift rule`). Il contient `AGENTS.md` et
`tests/test_document_drift_governance.py`. Il peut fournir le port unique de
Critical Rule 16, mais il ne doit jamais être porté en parallèle d’une autre
copie de cette règle.

## 3. Travaux non committés et expérimentaux

Les éléments suivants ne sont pas des commits portables tels quels :

| Élément | Traitement recommandé |
|---|---|
| Fondations DIM, Ontologie, DGM, DTS, DTP et Architecture de référence dans les runs du 2026-08-02 | Rester matériaux de conception/preuves. Aucun port automatique ; adoption canonique dédiée requise. |
| `AGENTS.md` modifié | Reconstruire un lot CR-16 contrôlé, ou porter `cc7ca86` une seule fois après comparaison exacte. |
| `distributions/pi/SYSTEM.md` modifié | Reconstruire un lot de remédiation documentaire séparé, avec preuve source/projection. |
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` modifié | Reconstruire un lot F-03 atomique seulement après validation de sa portée et de son état final. |
| Runs F-03 et nettoyage du noyau vivant | Conserver comme preuves ; ne pas les confondre avec le canon. Leur port doit être séparé des changements de gouvernance. |

Les documents de stratégie, d’adoption, de roadmap et de Proof of
Architecture ne doivent pas être cherry-pickés comme s’ils constituaient le
contrat documentaire. S’ils sont conservés, leur commit doit être
`EVIDENCE_ONLY` et ne produire aucun effet canonique.

## 4. Lots logiques et ordre de port recommandé

### Lot 0 — Préparation de l’intégration

Créer, dans un futur run autorisé, un worktree propre depuis le SHA alors
observé de `origin/main`. Vérifier l’absence de modifications et enregistrer
le SHA d’ancrage. Le worktree courant reste une source d’examen et n’est pas
réutilisé comme branche d’intégration.

### Lot 1 — Critical Rule 16

Porter exactement une représentation de la règle et son test dédié. La source
préférée est `cc7ca86`, sous réserve d’une comparaison avec l’état approuvé de
`AGENTS.md`. Si le texte a évolué, reconstruire un commit minimal contenant
uniquement `AGENTS.md` et le test, avec nouvelle revue humaine.

### Lot 2 — C0–C2

Porter `64bb43e` tel quel si son application sur la base propre est exacte.
Ce lot fournit l’interface expérimentale, DIM minimal, Ontologie minimale,
fixtures et tests.

### Lot 3 — C3–C4

Porter `6beae84` après le Lot 2. Il étend le même validateur aux tags DTS et aux
relations DGM ; il ne crée pas une seconde interface.

### Lot 4 — C5

Porter `f3035f6` après le Lot 3. Il transforme les résultats en findings et
propositions de route, sans écrire dans les artefacts.

### Lot 5 — Skills alignées

Porter `668e3e0` après C0–C5. Le port comprend les quatre skills, leurs tests et
les preuves de run présentes dans le commit. Aucun autre skill, workflow,
distribution ou template n’est inclus.

### Lot 6 — Remédiations documentaires approuvées

Reconstruire des commits séparés pour CR-16, F-02, F-03 et F-05 uniquement si
leur décision humaine et leur contenu final sont encore valides. Ne pas
porter `55b3696` automatiquement si `docs/CONTEXT.md` ne décrit plus le même
état. F-04 (scope DTS) et F-06 (runtime Pi) restent différés.

### Lot 7 — Adoption canonique

Hors port automatique. Il nécessite le run d’adoption dédié, la décision
humaine d’adoption, les localisations canoniques, l’éventuel ADR d’adoption et
une proposition de changement de canon. Les fondations conceptuelles ne
deviennent pas canoniques par le seul fait d’être committées.

## 5. Matrice de dépendances

```text
Lot 0 (base propre depuis origin/main)
  ↓
Lot 1 (Critical Rule 16)
  ↓
Lot 2 (C0–C2) → Lot 3 (C3–C4) → Lot 4 (C5)
                                      ↓
                                Lot 5 (skills)
                                      ↓
                         Lot 6 (remédiations séparées)
                                      ↓
                         Lot 7 (adoption, décision humaine)
```

Les lots 2, 3 et 4 ne doivent pas être parallélisés car leurs commits
étendent le même validateur et les mêmes tests. Les preuves historiques et
les documents conceptuels peuvent être examinés en parallèle, mais ne sont
pas une dépendance d’exécution pour C0–C5. Les remédiations F-02/F-03/F-05
peuvent être préparées en parallèle après validation de C5, puis portées en
commits distincts.

## 6. Validations et critères d’intégration

| Lot | Validations après port | Critère binaire d’intégration |
|---|---|---|
| 0 | SHA `origin/main`, `git status`, inventaire worktrees/branches | Base exacte, worktree propre, aucun conflit prévisible non documenté. |
| 1 | test CR-16, tests concernés, architecture/contract/convention lint, `git diff --check` | Une seule règle active, test passant, aucune référence interdite. |
| 2 | tests C0–C2, fixtures positives/négatives/UNKNOWN, Ruff, compilation | Contrat C0 stable et DIM/Ontologie en lecture seule, sans mutation. |
| 3 | tests C0–C4, DTS/DGM positifs/négatifs/UNKNOWN, suite ciblée | Compatibilité et relations restent dans l’interface C0 ; aucun verdict nouveau. |
| 4 | tests C0–C5, routage OUI/NON/PLUS TARD, absence d’écriture | Les findings sont gouvernés et les routes restent des propositions. |
| 5 | tests skills, C0–C5, suite complète, lints, propagation Core/distributions | Les quatre skills consomment le même contrat et ne corrigent pas automatiquement. |
| 6 | revue ciblée par lot, tests de gouvernance, source/projection, `git diff --check` | Chaque remédiation est atomique, réversible et limitée à sa décision. |
| 7 | validation complète, revue adversariale, décision humaine explicite | Adoption uniquement après fermeture de toutes les conditions d’adoption. |

Après chaque lot, enregistrer le SHA, le diff, les tests passants et les
limitations. Un échec non expliqué arrête le port ; aucun lot suivant ne peut
le masquer.

## 7. Rollback et atomicité

- Chaque lot doit aboutir à un commit autonome ou à une série explicitement
  indivisible, avec un point de retour identifié avant le lot suivant.
- Un échec avant publication entraîne l’abandon du candidat de travail ou le
  retour au dernier HEAD validé dans le worktree d’intégration ; le worktree
  source reste inchangé.
- Après publication, le rollback recommandé est un revert du lot fautif,
  jamais une réécriture de l’historique publié.
- Les lots de remédiation F-03 ne doivent pas réécrire ADR-0051, ADR-0053 ou
  une autre décision historique.
- Le rollback d’un lot de preuves ne doit pas supprimer les preuves sources
  non portées ; leur conservation est une décision distincte.

## 8. Cherry-pick, reconstruction et maintien expérimental

### Cherry-pickable tels quels, sous réserve de validation sur la nouvelle base

- `64bb43e` ;
- `6beae84` après `64bb43e` ;
- `f3035f6` après `6beae84` ;
- `668e3e0` après C0–C5.

Cette propriété est technique et ne vaut pas adoption canonique.

### À reconstruire proprement

- CR-16 si `cc7ca86` ne correspond plus exactement au texte approuvé ;
- F-02, F-03 et F-05, car leurs modifications actuelles sont hors commits
  atomiques dans ce worktree ;
- toute proposition d’adoption canonique, après décision humaine et
  détermination de l’autorité finale.

`55b3696` est techniquement portable comme patch isolé, mais son contenu est
lié à l’état de transition décrit le 2026-08-02. Il doit donc être comparé à
la nouvelle `docs/CONTEXT.md` avant décision ; sinon il est reconstruit.

### À maintenir expérimental

- les sept fondations conceptuelles non adoptées ;
- les POC, fixtures et rapports C0–C5 ;
- les plans d’intégration, stratégie, roadmap et Proof of Architecture ;
- les runs historiques F-03 et du nettoyage vivant ;
- le runtime Pi tant qu’il n’est pas identifié et certifié séparément.

## 9. Garde-fous d’intégration

Le futur run doit s’arrêter si :

1. `origin/main` a changé depuis l’ancrage ;
2. le worktree d’intégration n’est pas propre ;
3. un port crée une seconde autorité ou une seconde interface C0 ;
4. un document expérimental est présenté comme canonique ;
5. une validation est bloquée ou échoue sans analyse ;
6. un lot dépend d’un ADR, d’un modèle ou d’une autorité absente de main ;
7. une modification touche le runtime Pi, les distributions ou le canon sans
   décision dédiée.

## Verdict

`MAIN_INTEGRATION_REQUIRES_REVISION`

Le plan d’intégration est défini, mais l’intégration ne peut pas être
considérée prête : il faut d’abord un worktree/branche propre depuis le SHA
actuel de `origin/main`, une décision explicite sur les remédiations non
committées et le run d’adoption dédié pour toute canonisation des fondations.
