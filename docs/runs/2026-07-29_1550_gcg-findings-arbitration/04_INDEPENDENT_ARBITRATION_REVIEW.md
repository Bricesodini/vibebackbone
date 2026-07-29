---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "04_INDEPENDENT_ARBITRATION_REVIEW"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
agent: "claude-opus-5 (Claude Code) — revue par subagent isolé a2f715163e55cc42e"
started_at: "2026-07-29T14:20:00Z"
ended_at: "2026-07-29T14:30:00Z"
artifacts_consumed:
  - "02_FINDINGS_REGISTER.md"
  - "03_DEPENDENCY_AND_ARBITRATION_MAP.md"
  - "05_DECISIONS_REQUIRED.md"
  - "06_RESUMPTION_SEQUENCE.md"
artifacts_produced:
  - "04_INDEPENDENT_ARBITRATION_REVIEW.md (this file)"
---

# 04_INDEPENDENT_ARBITRATION_REVIEW — GCG-ARB-01

## 1. Mandat et indépendance obtenue

Le subagent a reçu pour sujet **la classification et l'arbitrage**, pas le
modèle. Mandat explicite : chercher les findings mal regroupés, les corrections
locales masquant un défaut conceptuel, les décisions normatives présentées à
tort comme techniques, les incompatibilités avec le canon, les risques de
réparation défensive, et les findings qui devraient invalider une hypothèse
fondamentale. Interdiction de refaire l'audit général et de défendre le modèle.

| Dimension | État |
|---|---|
| contexte | **isolé** — nouveau contexte, aucun accès à la conversation de l'agent principal |
| dépôt | **lecture seule** ; démonstration conduite en répertoire temporaire, dépôt non modifié |
| famille de LLM | **identique** (`claude-opus-5`) — `A2_DISTINCT_AGENT_PROXY` **non satisfait**, contrainte C6 |
| orientation | aucune conclusion suggérée ; consigne explicite de ne pas se calibrer sur l'attente de l'agent principal |

Le subagent a lu les quatre livrables, le modèle, le stress test, le rapport de
la première revue, l'outil, la suite de tests et le canon d'assurance ; il a
exécuté 8 commandes de mesure et une démonstration.

**Onze constats, `F-A` à `F-K`.** Aucun n'a été écarté sur les faits. J'ai
re-vérifié moi-même les six qui portent contre mon arbitrage.

## 2. Constats, avec ma vérification

### F-A — Une quatrième voie de blanchiment, et c'est la plus propre
**Vérifiée à la source par l'agent principal. Constat le plus important de la revue.**

`classify_run` teste `identity < ADVERSARIAL_APPLIES_FROM → HISTORICAL_VALID`
en **ligne 176**, avant le test `OVERCLAIM` en **ligne 197**. Un closeout portant
`adversarial_status: PASS_ADVERSARIAL` + `certification_status: CERTIFIED` sans
bloc validable, renommé sous une identité antérieure à `applies_from`, devient
`HISTORICAL_VALID` : non bloquant, exclu du dénominateur.

Démonstration du subagent (répertoire temporaire, dépôt intact), corps de
closeout identique dans les trois cas :

```
2026-07-28_1500_in-window-claims  → OVERCLAIM        blocking=True
2026-07-27_0900_renamed-claims    → HISTORICAL_VALID blocking=False
2026-06-01_0900_ancient-claims    → HISTORICAL_VALID blocking=False
```

**Ce que j'ai vérifié moi-même et qui aggrave le constat** : le commentaire
immédiatement au-dessus de la branche `OVERCLAIM`, lignes 195-196, dit :

> *An unsupported positive claim outranks every other reading, including the
> historical one. Age does not make a false PASS less believed.*

**L'ordre des branches rend ce commentaire faux.** C'est la deuxième fausse
déclaration active dans le même fichier, après celle des deux bornes (GCG-09).
Le modèle §4.2 affirme la même primauté, et I5 la formule comme *« jamais
adouci par l'ancienneté »*.

Quatre conséquences pour l'arbitrage, toutes acceptées :

1. `03` §2 et §4.1 comptaient **trois** voies de blanchiment. Il y en a
   **quatre**. La quatrième neutralise la seule catégorie que le modèle déclare
   non migrable et immédiatement bloquante.
2. La condition d'arrêt de `R-5` (« échec si une quatrième voie est trouvée »)
   **est déjà remplie avant l'ouverture du run**.
3. `03` §3.9 affirmait que D0 ne dépend d'aucune autre décision. La question de
   dépôt est bien indépendante ; **la preuve ne l'est pas** :
   `2026-07-30_0500` renommé sous une identité pré-cutoff cesse d'être un
   `OVERCLAIM`, et le P0 repose sur cette classification.
4. **GCG-22 est réfuté dans sa direction de correction.** J'affirmais que I5
   devait être listé *couvert* parce que
   `test_overclaim_outranks_the_historical_reading` existe. Ce test construit sa
   fixture à `APPLIES_FROM + 1h`, donc **dans** la fenêtre : il n'exerce que
   « jamais ledgerable ». La branche que je citais comme preuve de couverture —
   « jamais adouci par l'ancienneté » — est précisément **la branche cassée**.
   J'ai corrigé un tableau de couverture dans le sens de la **surestimation**,
   c'est-à-dire le mode d'échec exact que je reprochais au modèle.

→ Nouveau constat **GCG-36** au registre, P0. `GCG-22` réécrit.

### F-B — La table de duplication de `03` §3.6 est fausse sur la plupart de ses lignes
**Acceptée. Le chiffre « 5/8 » est retiré.**

La table assimile des classifications GCG **dérivées, par couple (artefact,
règle)** à des `certification_status` **déclarés, par sujet**. La ligne la plus
fausse est `CURRENT ↔ CERTIFIED` : `CURRENT` est `gate_exit == 0`, un
sous-processus ; `CERTIFIED` est un statut soumis à treize conditions du canon
(§5.3.1), dont une décision humaine enregistrée, un `witnessed_by` distinct du
`discovered_by`, un liage au corpus et une cadence de revue ≤ 90 jours.

**Le subagent a raison sur le point de fond, et il est sévère à juste titre** :
en écrivant cette équivalence, mon analyse dérive une certification d'un verdict
de conformité — c'est-à-dire commet, dans le document qui les poursuit, la
collapse qu'I4 interdit et que `build_act` empêche en écrivant
`NOT_DERIVABLE_FROM_THIS_GATE` en dur.

`PENDING_LIFECYCLE ↔ NOT_APPLICABLE` est fausse pour une raison que le modèle
lui-même documente : §4.1 explique que le nom précédent `OUT_OF_SCOPE` était
faux parce qu'un run en cours n'est pas hors périmètre. Ma table le réintroduit.

**Ce qui survit** : GCG-11 tel qu'écrit au registre — la vérité parallèle
**déclaré vs dérivé**, dont l'instance est réelle (un run pré-cutoff déclarant
`NOT_CERTIFIED` est bloquant sous le canon et `HISTORICAL_VALID` sous GCG).
Ce qui tombe, c'est le **comptage** et la conséquence d'ordonnancement qu'il
portait.

→ `03` §3.6 réécrite ; D4 rétrogradée de « décision de périmètre » à
« réconciliation déclaré/dérivé ».

### F-C — La dérivation du verdict est incohérente
**Acceptée sur l'incohérence. Le verdict est reconstruit, pas maintenu par inertie.**

J'écartais `INSUFFICIENT_EVIDENCE` au motif que *« le manque de preuve porte sur
l'ampleur, pas sur l'existence »*, et `REPAIRABLE_CORE` au motif qu'*« on ne peut
pas qualifier de bornée une correction dont on ne connaît pas encore la forme »*
— c'est-à-dire une question d'ampleur. Les deux éliminations ne peuvent pas
tenir ensemble. Le subagent a raison.

**Correction de fait sur un sous-point** : le subagent note que le vocabulaire
de verdict (`REPAIRABLE_CORE`, `REQUIRES_REDESIGN`, …) n'existe nulle part dans
le dépôt et en déduit que je l'ai auto-défini. Le vocabulaire vient de l'énoncé
de mission, ce que le subagent ne pouvait pas savoir depuis son contexte isolé.
**Ce qui reste vrai de son constat** : ce vocabulaire n'est réconcilié avec
aucun autre, en particulier pas avec le `NOT_CANONICAL_YET` du stress test, qui
reste le verdict en vigueur du run `1130`. Deux verdicts sur le même sujet sans
mapping — Critical Rule 5, dans le document qui la cite trois fois.

Également accepté : la condition de bascule §7.3 était **malformée**. Sa
troisième branche admettait « une absorption assumée dans le canon existant »
comme route vers `REPAIRABLE_CORE`, alors que l'absorption *est* la définition
de `DUPLICATES_EXISTING_CANON`.

→ `03` §7 réécrite intégralement.

### F-D — Aucune des attestations que je recommande n'en est une dans ce dépôt
**Vérifiée par l'agent principal. C'est le constat qui me vise le plus directement.**

`git log --format='%G?'` sur 244 commits → **243 `N`, 1 `E`. Aucune signature.**
Les dates d'auteur et de committer sont réglables (`git commit --date`,
`GIT_COMMITTER_DATE`) et l'historique est réinscriptible.

Donc mes recommandations D1-A (coordonnée = date d'auteur git), D1-B (identité
vérifiée contre l'historique) et D2-B (immuabilité dérivée de l'historique)
**détectent** les deux contre-exemples connus — le renommage de répertoire et
l'édition post-clôture — sans **établir** la propriété.

**C'est la définition de la réparation défensive que ce run avait pour charte
d'empêcher, et elle était dans mes propres recommandations.** J'applique le test
déclaré-vs-établi avec force à GCG-01 et GCG-02, puis je ne l'applique pas à mes
propres remèdes. Seules D1-C et D2-C sont de véritables attestations, et je les
marque toutes deux comme sans population qualifiante aujourd'hui.

Conséquence directe : les conditions d'arrêt en échec de `R-2` et `R-3` sont
**inatteignables** par les options que je recommandais. Les deux runs auraient
rapporté un succès avec le concept toujours cassé.

→ D1 et D2 réécrites, recommandations retirées, une option de substrat ajoutée.

### F-E — La « divergence » V3 est une erreur de mesure résoluble, et mon explication était fausse
**Acceptée sans réserve.**

Je conservais deux mesures (74/105 vs 94/123) en les déclarant irréductibles, et
j'attribuais l'écart à GCG-15 (« deux résolveurs ne comptent pas la même
population »). Le subagent a re-mesuré sous trois résolveurs :

| Résolveur | Mesurés | Désaccord | Écart max |
|---|---|---|---|
| `07_CLOSEOUT.md` seul | 106 | 75 | 22,08 h |
| repli `*CLOSEOUT*.md` | 106 | 75 | 22,08 h |
| + identités à granularité jour | **123** | **90** | **29,0 h** |

**Les deux résolveurs donnent une population identique.** L'attribution à
GCG-15 est fausse. Tout l'écart vient de l'inclusion des identités à
**granularité jour**, où l'« écart » est un artefact de comparaison entre un
intervalle de 24 h et un instant — le cas même que GCG-08 et le modèle §3.5
discutent.

Le subagent formule le reproche exactement : *« Préserver un désaccord est une
bonne discipline ; le préserver au lieu de le mesurer est l'apparence de la
discipline. »* Accepté. Corrigé aussi : « la majorité du corpus est concernée »
est 75 sur 164, soit 46 % — une majorité du sous-ensemble mesuré seulement.

→ GCG-10 réécrit, V3 retirée de la table des divergences.

### F-F — La recommandation D7-A reproduit la pathologie que le registre nomme
**Acceptée.**

D7-A remplaçait une **absence invérifiable** par une **déclaration
invérifiable** (« ouvert, phase N »). Le défaut de GCG-05 est que le scanner
observe le *fait* de l'absence et non le *motif* ; une auto-déclaration de motif
n'est pas davantage vérifiable. Le basculement du défaut vers *bloquant* est un
gain réel ; l'échappatoire survit sous forme déclarée. Et je n'ai pas retourné
sur ma propre recommandation l'instrument du registre — GCG-01, « un booléen
déclaré que rien n'atteste ».

**Mal-regroupement accepté** : GCG-19 (`st_mtime` départage plusieurs porteurs
**présents**) n'a rien à voir avec D7 (qui demande ce que signifie **l'absence**
du porteur). Aucune des trois options de D7 ne le décide. Il est décidable
aujourd'hui, à coût normatif nul, et je le bloquais derrière une décision sans
rapport. GCG-15 est dans la même position, et le registre le disait lui-même
sans en tirer la conséquence d'ordonnancement.

→ GCG-19 et GCG-15 sortis de D7.

### F-G — L'ordre D4 → D1/D2 est circulaire, et la condition d'arrêt de R-1 ne peut pas échouer
**Acceptée.**

`03` §3.6 place D4 en premier « par économie » et écrit dans le même paragraphe
que les trois apports propres dépendent de D1 et D2. §7.3 boucle : si D1/D2 sont
sans réponse, le verdict devient `DUPLICATES_EXISTING_CANON`, qui est la réponse
B de D4. **D4 est déterminée par D1/D2 et ne peut donc pas les précéder.**

Et la condition d'arrêt de R-1 — « échec si une catégorie ne peut être ni mappée
ni justifiée » — est vide : « justifiée comme apport propre » est toujours
disponible, sans critère indépendant ni falsificateur. **Le seul run capable
d'annuler les huit autres avait une condition d'arrêt infalsifiable.**

→ Séquence réordonnée, conditions d'arrêt de R-1, R-2 et R-3 réécrites.

### F-H — `closure_authority` est annoncé comme structurant et ne l'est pas
**Acceptée.**

`02` §3 déclare que cet axe structure `03`. Il ne le structure pas — `03` est
structuré par D0–D7. Et cinq des sept entrées `AGENT` sont subordonnées à une
décision (GCG-12, 14, 18, 19, 20). L'axe confond **qui exécute** et **qui
décide**, ce qui est exactement la distinction qu'il devait porter.

→ `02` §3 corrigé, la valeur `AGENT` scindée.

### F-I — GCG-28 est laissé `PLAUSIBLE` alors que le fait est mesurable en deux commandes
**Acceptée et re-mesurée par l'agent principal.**

Vérifié sur les 9 closeouts : **tous portent une disposition positive en
frontmatter et aucun ne porte de section Knowledge Harvest dans le corps**. Les
seules occurrences du mot sont la clé de frontmatter, et pour deux d'entre eux
une reprise à l'intérieur d'un bloc YAML.

Le registre avait raison de dire que **qualifier** les 9 en `OVERCLAIM` dépend
de D5. Il avait tort de laisser cette dépendance bloquer **l'établissement du
fait**, dans un document dont la thèse est « mesurer avant de décider ».

→ GCG-28 passe de `PLAUSIBLE` à `CONFIRMED` sur le fait, la qualification
restant suspendue à D5. R-7 perd la moitié de son objet.

### F-J — GCG-34 attaque le seul usage ajouté de la seconde borne, et n'est relié à aucune décision
**Acceptée.**

GCG-34 (P3, `Décision liée: —`) conteste la lecture de la largeur de fenêtre
comme indicateur de qualité de publication. **Or c'est le seul gain que S7
revendiquait pour la seconde borne.** Et le modèle §7 concède que
`enforcement_effective_from` et la fenêtre de dette sont « non corroborés ».

Le subagent conclut : *« Une idée qui n'a jamais été instanciée n'est pas
montrée résiliente par le fait de survivre à une attaque — elle est non
falsifiée parce que non testée. »* Cela porte directement contre la première
élimination de `03` §7.1 (`ABANDON` écarté au motif que la distinction à deux
bornes a résisté), à laquelle GCG-34 n'était pas relié.

→ GCG-34 relié à D4 et à §7.1 ; l'élimination d'`ABANDON` réécrite.

### F-K — Constats mineurs, tous vérifiables
**Tous acceptés.**

| Point | Vérification |
|---|---|
| « 14 des 164 closeouts » | **faux dénominateur.** `git ls-files 'docs/runs/*/07_CLOSEOUT.md' \| wc -l` → **157**. 164 est le nombre de répertoires. Le 14 est correct |
| `04_INDEPENDENT_ARBITRATION_REVIEW.md` cité comme existant en `02` §1 | vrai au moment de la revue : le fichier n'existait pas encore. **Corrigé par le présent fichier** |
| le run lui-même est l'unique `PENDING_LIFECYCLE` vivant | vérifié. Non fautif — le run est ouvert — mais la baseline de `01` §5 est présentée comme neutre alors que l'unique occupant de la catégorie signalée est le run qui mesure. Rend **GCG-30** concret |
| D1 ne peut pas rendre les entrées du modèle non choisies même si elle est tranchée | vrai : les sources 2 et 3 de §3.4 restent écrites par l'auteur par conception. L'union est fail-closed, donc ce n'est pas un trou — mais D1 telle que formulée n'est atteignable que pour le **positionnement** |

## 3. Ce que la revue a validé

Cité pour être opposable, non par courtoisie. Le subagent liste explicitement ce
qui a résisté à son examen :

- **L'espace d'identifiants** — la collision `IR-F8` / `AUD-F8` est réelle, la
  renumérotation nécessaire, la colonne *source* préservée.
- **La scission GCG-01 / GCG-21** — défaut de modèle et défaut de preuve se
  réparent à des endroits différents ; les fusionner en aurait caché un.
- **La scission GCG-26 / GCG-27 et l'escalade de GCG-27** — `git log -p`
  confirme `b9084e2`. L'argument que la mutation change la *nature* du problème
  est jugé correct, et la règle dérivée (« aucune disposition de dette n'est
  admissible ») suit.
- **D6 est jugée la meilleure analyse du lot** — l'observation que retirer
  `HISTORICAL_VALID` de `LEDGERABLE` *est* la décision A prise silencieusement
  est jugée juste et non évidente, et vérifiée contre le code.
- **`03` §3.1 — GCG-14 et GCG-03 doivent être réparés ensemble** — jugé correct
  et non évident, avec l'instance réelle confirmée.
- **GCG-33 conservé en `PARTLY_REFUTED`** plutôt qu'effacé, avec le motif
  (effacer une réfutation est du blanchiment documentaire) — jugé juste.
- **C3 a tenu** — aucun code modifié. Le subagent juge que refuser de corriger
  même les items gratuits était la bonne posture.
- **GCG-09, GCG-12, GCG-19, GCG-24 reproduisent exactement.**
- **`R-5` et `R-6` sont les meilleurs runs de la séquence** — tests de mutation
  démontrés rouges avant d'être verts, mandat adverse explicite de chercher une
  quatrième voie, test différentiel scanner/enforcer sur toute la population,
  interdiction stricte de corriger GCG-14 seul.
- **Les interdits de D0** sont jugés exactement justes et correctement reconduits
  dans R-0.
- **Le mécanisme de GCG-25 est exact** — rien n'épingle F1–F12.

## 4. Divergences résiduelles

Deux seulement, et aucune ne porte sur un fait.

| # | Point | Subagent | Agent principal | Statut |
|---|---|---|---|---|
| **W1** | provenance du vocabulaire de verdict | auto-défini par l'agent, « verdict *sélectionné* puis argumenté » | vocabulaire **fourni par l'énoncé de mission**, non inventé — information indisponible depuis un contexte isolé | **résolu par le contexte.** Le reste du constat tient : aucune réconciliation avec `NOT_CANONICAL_YET` |
| **W2** | portée de F-D | « la bascule est plus déterminée que conditionnelle » → `DUPLICATES_EXISTING_CANON` proche d'acquis | F-D établit qu'**aucun substrat d'attestation n'existe aujourd'hui**, pas qu'aucun ne peut être créé : signer les commits, ou épingler une empreinte à la clôture, sont des options ouvertes que ni lui ni moi n'avons évaluées en coût | **ouvert, versé à D2.** Ma position réduit la portée de son constat : je la signale comme telle |

## 5. Limites déclarées de la revue

Reprises telles quelles :

- E1–E5 de la première revue non rejouées ; la démonstration F-A est propre au
  subagent, en répertoire temporaire.
- Runs `1021` et `1050` non lus intégralement ; GCG-32, GCG-C1/C2/C5 et
  R3/R4/R5 non vérifiés.
- Aucune tentative systématique de casser le modèle au-delà de F-A, qui a
  émergé en vérifiant la revendication de couverture de GCG-22.
- `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` lu sélectivement ; une lecture complète
  pourrait modifier son jugement sur la ligne `UNASSESSED_LEGACY` de F-B.
- Suite de tests non exécutée intégralement.
- **`A2_DISTINCT_AGENT_PROXY` non satisfait** — même famille de modèle que
  l'agent principal et que la revue F1–F12. Le subagent le déclare lui-même.

## 6. Effet sur les livrables

| Livrable | Modifications imposées par la revue |
|---|---|
| `02_FINDINGS_REGISTER.md` | **GCG-36** ajouté (P0, quatrième voie) · GCG-22 réécrit et sa correction inversée · GCG-28 `PLAUSIBLE` → `CONFIRMED` sur le fait · GCG-10 réécrit, attribution GCG-15 retirée · dénominateur 164 → 157 · §3 `closure_authority` corrigé |
| `03_DEPENDENCY_AND_ARBITRATION_MAP.md` | §2 graphe réordonné (D4 après D1/D2) · §3.6 table de duplication réécrite, « 5/8 » retiré · §3.9 corrigé (D0 dépend de GCG-36 pour sa preuve) · §4.1 quatrième voie ajoutée · §6 V3 retirée · **§7 réécrite intégralement** |
| `05_DECISIONS_REQUIRED.md` | D1 et D2 réécrites, recommandations retirées (F-D) · D4 rétrogradée · D7-A retirée comme recommandation · GCG-19 et GCG-15 sortis de D7 · tableau final mis à jour |
| `06_RESUMPTION_SEQUENCE.md` | R-1 déplacée après R-2/R-3 et sa condition d'arrêt réécrite · R-2 et R-3 dotées de conditions d'échec atteignables · **R-5 rouvre avec la quatrième voie déjà au périmètre** · R-7 réduite · R-8 corrigée (I5 n'est pas couvert) |

Les modifications sont appliquées. **Les constats d'origine ne sont pas
effacés** : chaque section réécrite porte la trace de ce qu'elle disait et de
qui l'a réfutée.
