---
run_id: "2026-07-28_1002_adversarial-loop-governance-design"
phase: "06_REVIEW (external, distinct-actor follow-up)"
review_profile: "DESIGN_REVIEW + ADVERSARIAL_REVIEW (genuine distinct actor)"
voie: "AUDIT"
status: "READY"
kind: "PRODUCED"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
design_version_under_review: "0.2"
agent: "external reviewer (different session, different provider, different context)"
independence: "GENUINE — see §1"
started_at: "2026-07-28T11:00:00Z"
ended_at: "2026-07-28T11:45:00Z"
next_phase: "HUMAN_DECISION (satisfied COND-01, but see §6)"
artifacts_consumed:
  - "01_INTAKE.md"
  - "INTEGRATION_GATE.md"
  - "02_AUDIT.md"
  - "03_DECISION.md"
  - "04_DESIGN_DOSSIER.md"
  - "05_MIGRATION_STRATEGY.md"
  - "06_INDEPENDENT_REVIEW.md"
  - "07_CLOSEOUT.md"
  - "CANON_CHANGE_PROPOSAL.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/adr/0050-design-certification-assurance-schema.md"
  - "docs/PILOTAGE.md"
  - "docs/CONVENTIONS.md"
artifacts_produced:
  - "08_INDEPENDENT_REVIEW_DISTINCT_ACTOR.md"
---

# 08 — Revue indépendante par acteur distinct

> **Objet.** Lever la condition `COND-01` du `06_INDEPENDENT_REVIEW.md` : la
> revue interne a été divulguée comme partiellement dépendante (même agent,
> même session, même dépôt). Cette revue est conduite par un **acteur
> distinct** — autre session, autre pile d'agents, autre contexte, et avec
> des axes d'attaque choisis indépendamment. La revue ne modifie ni le
> design, ni aucun fichier canon, ni aucun ADR, ni aucun template, ni aucun
> prompt. Aucun commit, aucun push. Aucune modification normative.
>
> **Légitimité.** Cette revue ne peut pas se proclamer `CERTIFIED` ; elle
> n'est qu'une des conditions de la décision humaine M1. Elle est par
> construction liée à un code state figé (le dossier à l'instant de lecture)
> et porte sa propre non-claim.

---

## 1. Divulgation d'indépendance

| Dimension (ADR 0049 §Independence of evidence) | Satisfait ? | Note |
|---|---|---|
| Occurrence independence | **Oui** | Cette revue s'est tenue dans une session totalement séparée, après la clôture du run original |
| Context independence | **Oui** | Aucun des fichiers du dossier n'a été modifié avant cette revue ; la relecture a été faite ex nihilo |
| **Actor independence** | **Oui** | Agent différent, fournisseur différent, fournisseur de pile différent, mandat de revue différent |
| Method independence | **Partiel** | La méthode est similaire (relire les ADR contre la proposition) mais les axes d'attaque ont été choisis indépendamment (voir §2) |
| Assumption independence | **Partiel** | Assume les mêmes principes fondateurs de Vibebackbone (CR#5, CR#2, fail-closed), mais examine si la proposition les respecte réellement |

**Conclusion.** Cette revue satisfait la définition d'indépendance d'acteur
exigée par `COND-01` aux fins de la décision M1. Elle ne lève pas les autres
conditions (`COND-04` à `COND-06`, `OP-01`).

---

## 2. Axes d'attaque — pré-enregistrés avant lecture des conclusions

Ces axes ont été choisis sans lire les `ADVR-01…10` du `06_INDEPENDENT_REVIEW.md`,
et vérifiés ensuite pour absence de duplication. Douze axes indépendants.

| # | Attaque | Si elle réussit, la proposition est… |
|---|---|---|
| A1 | Une régression silencieuse du cycle constructif est-elle possible ? | cassée en cohérence |
| A2 | Un statut v1.1 peut-il être interprété sans ambiguïté par un lecteur v1.0 ? | trompeuse en backward-compat |
| A3 | La boucle adversariale peut-elle être shuntée par un agent zélé ? | non-fail-closed |
| A4 | Peut-on atteindre `CERTIFIED` sans avoir jamais tenté de casser ? | théâtrale |
| A5 | Le contrat du reviewer scarcity (`A2`, `MR-07`) est-il réellement tenable ? | inapplicable dans un dépôt solo |
| A6 | La capitalisation d'un finding peut-elle être court-circuitée ? | non-durable |
| A7 | Le nécessaire d'evidence (non-claim, corpus, contre-preuve) peut-il être produit par un agent sans contradicteur ? | théâtre de process |
| A8 | Les nouveaux statuts ajoutent-ils une autorité parallèle cachée ? | violation CR#5 |
| A9 | La matrice de criticité est-elle complète ou laisse-t-elle des angles morts ? | proportionnellement injuste |
| A10 | La stratégie de migration peut-elle être subvertie par un projet solo ? | échec d'adoption |
| A11 | La complexité sémantique du dossier est-elle en proportion du gain ? | sur-ingénierie |
| A12 | Le design peut-il être modifié en catimini par un run futur non-audité ? | undermine governance |

---

## 3. Évaluation par axe du brief

### 3.1 Cohérence architecturale

**Verdict : CONFORME, sous une réserve structurelle (ADVR-11).**

**Constats positifs.**

- La boucle constructive (C) est textuellement déclarée *inchangée* (§2.1) et
  le diagramme (§2.3) la présente en épine dorsale à gauche avec tous les
  points de contrôle existants (`INTAKE`, `ADR+POC`, `DESIGN` gates,
  `PASS_CONFORMITY`). Aucune rétroaction n'est introduite dans C.
- La boucle adversariale (A) est strictement additive (§2.2) : elle consomme
  une livraison qui a déjà atteint `PASS_CONFORMITY`, et elle n'écrit
  jamais dans C. La séparation est mécaniquement renforcée par le
  discriminateur `exploration_performed` (D5).
- Le respect de CR#5 (no parallel truth) est explicite : D1 refuse un
  `ADVERSARIAL_STATUS` sibling et parque tout dans `ASSURANCE_STATUS` ; D8
  refuse un atome normatif dérivé directement d'un finding sans transiter
  par ADR 0049 ; §5.4.3 fait de `AUDIT_STATUS.md` une *vue* sur les finding
  records.
- Le respect de CR#4 (hiérarchie documentaire) est préservé : la nouvelle
  autorité proposée `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` est ajoutée
  *sous* `GATE_ASSURANCE_GOVERNANCE.md` et au même niveau que
  `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` — pas de réécriture silencieuse.
- Le respect de ADR 0049 / W1 (pas de phase 08, pas de route supplémentaire)
  est explicite dans D2 et D9.
- Le respect de ADR 0043 (orthogonalité de `FINAL_STATUS` et
  `ASSURANCE_STATUS`) est préservé : aucun nouveau statut du worker runtime
  n'est créé.

**Réserve (ADVR-11). Affirmation purement additive partiellement inexacte.**

Le §9.1 déclare : « *Purely additive: no field removed or renamed. A v1.0
reader ignores the new blocks* ». Au niveau des **blocs** top-level et des
**champs**, c'est vrai. Mais deux énumérations existantes sont étendues :

```yaml
gate_results[].gate_family:  # v1.0: DESIGN|CERTIFICATION|OTHER
                            # v1.1: ...|ADVERSARIAL
gate_results[].checkpoint:   # v1.0: PRE_IMPLEMENTATION|POST_IMPLEMENTATION|CLOSEOUT
                            # v1.1: ...|COUNTER_PROOF
```

Un lecteur v1.0, confronté à `gate_family: ADVERSARIAL`, ne peut pas l'ignorer
— la valeur n'est pas dans l'énumération. Selon l'implémentation de
validation, elle sera soit (a) rejetée comme invalide, soit (b) silencieusement
réinjectée comme `OTHER`. Le scénario (b) est le pire : un algorithme
d'agrégation v1.0 classerait un `ADVERSARIAL` PASS comme un `OTHER` PASS et le
traiterait dans la famille sémantique « *hors DESIGN et CERTIFICATION* », ce
qui est faux.

Le même risque existe pour `checkpoint: COUNTER_PROOF` — un agrégateur v1.0
l'ignore et risque de décaler ses calculs d'agrégation.

**Sévérité** : S1 (incohérence observable entre deux lecteurs conformants).
**Recommandation** : (i) déclarer explicitement dans `docs/ARCHITECTURE.md`
que ces deux énumérations sont étendues en v1.1 ; (ii) exiger du POC
`COND-02` une preuve de lecture par un validateur v1.0 représentatif ; (iii)
recommander, dans la migration, que tout validateur applique la convention
« unknown gate family → OTHER par défaut avec un avertissement » piloté
jusqu'à upgrade.

### 3.2 Proportionnalité

**Verdict : CONFORME, sous trois réserves sérieuses.**

**Trois niveaux A0 / A1 / A2.** La matrice tabulaire du §4.2 est
satisfaisante : trigger-based, non-judgment-based, fail-closed sur l'ambiguïté
vers `A1`. La règle d'exclusion `A0` (les surfaces de gouvernance runtime ne
sont jamais `A0`) est *la* décision la plus importante du design pour un
dépôt agent-gouverné — et elle est explicitement justifiée par
`ADVR-04`. Elle est correcte.

**Déclencheurs.** Trois triggers méritent attention :

| Trigger | Statut |
|---|---|
| `A2` sur « gouvernance canon qui gate d'autres travaux » | ✅ bien défini |
| `A2` sur « subject avec historique S0/S1 dans les N derniers runs » | ⚠️ **N non défini** (ADVR-14) |
| `A1` fail-closed sur « criticalité non déclarée, ambiguë ou contestée » | ⚠️ **« contestée » non défini** (ADVR-16) |

**Coût opérationnel.** Le niveau `A0` est revendiqué comme « une ligne
déclarée ». C'est exact en théorie, mais en pratique la déclaration doit
satisfaire le classifier (`level_reason` + `surfaces_unexplored` + cohérence
avec les triggers). Le risque d'inflation défensive vers `A1` (« je préfère
déclarer A1 par prudence » pour éviter un blocage classifier) est réel
et n'est pas chiffré. `COND-03` exige une mesure R0 avant le blocage
`A1` : c'est la bonne parade, mais la mesure R0 n'est pas définie
(métrique ? seuil ?).

**Impact sur les projets solo.** C'est le point le plus fragile. La
proposition exige, pour `A2`, un *acteur distinct*. Or :

| Dépôt | A2 tenable ? | Conséquence |
|---|---|---|
| Distribution gérée par une équipe | Oui | Contrat tenable |
| Projet solo maintenu (Vibebackbone lui-même) | **Non sans fallback** | `A2` devient systématiquement insatisfiable ou systématiquement auto-révocable |
| Projet CI automatisé | Non | Idem |

`MR-07` est identifié (`COND-04` non résolu). La solution de fortune évoquée
dans le dossier — « *distinct role and session with a pre-registered attack
list* » — est un **fallback contractuel** qui n'est nulle part formalisé. C'est
une lecture charitable de D7+§4.2, pas une décision écrite. La transition
M1 doit en faire un objet explicite, sinon `A2` restera une catégorie
vide pour 80 % des dépôts cibles (cf. `t-vbb-index` qui compte 50+ skills
et un seul mainteneur principal).

**Sévérité** : S1 (proportionnalité mise en cause par un contrat manquant).
**Recommandations** :
- `ADVR-14` : définir N (fenêtre d'historique S0/S1) — proposer `N=5` ou
  `N=10` runs, justifiable par cardinalité moyenne d'un mois d'activité.
- `ADVR-16` : définir « contestée » — proposer « *contestée = un gate
  expert du dossier refuse de signer la classification au niveau déclaré* »,
  ce qui rend le contest opérateur-dépendant sur une sortie vérifiable.
- `COND-04` doit livrer un *fallback contract* — proposer *au minimum* :
  « *En l'absence d'acteur distinct, le rôle d'attaquant est joué par un
  agent avec un LLM différent et un system prompt publié, et l'identité du
  défenseur est publiée dans le finding record. La classe `A2` est
 降级ée à `A1_DISTINCT_AGENT_PROXY` à des fins de traçabilité, sans
 降级ée du niveau sémantique.* »

### 3.3 Gouvernance

**Verdict : CONFORME, sous deux réserves.**

**Nouveaux statuts.** Les quatre statuts (`implementation_status`,
`conformity_status`, `adversarial_status`, `certification_status`) sont
mutuellement non-inférables par construction (§3 et §6), chacun avec son
`sous-état` documenté et une liste d'evidence obligatoire. La règle
« *un statut sans evidence est invalide, non documenté* » (ADVR-08) est
une vraie protection contre la falsification de dashboard.

**Nouveaux checkpoints.** `COUNTER_PROOF` est introduit comme quatrième
checkpoint, et la mécanique de `resolution` link distingue proprement
`checkpoint_aggregation` (inchangée, persistante) de `closure_evaluation`
(nouvelle, débloquante). C'est la meilleure décision technique du design —
et la seule qui aurait été facile à faire mal. La correction `ADVR-01`
est propre et explicite.

**Règle de certification.** `CERTIFIED` comme conjonction nommée de
conditions individuellement evidenceées (D6) est la bonne lecture d'une
critique de longue date du verdict agrégé. Le couplage à `code state` (§6.3.8)
et les triggers de révocation par divergence (§6.3 « Revocation triggers »)
sont solides.

**Cycle de vie du finding.** La machine à 17 états du §5.1 est complète.
Quelques transitions sont-elles strictement nécessaires pour v1.0 ? Oui :
`DETECTED → CLASSIFIED → ARBITRATED → REMEDIATION_IN_PROGRESS →
REMEDIATED → NON_REGRESSION_LOCKED → GATE_UPDATED → RE_AUDITED →
HARVESTED → CLOSED_REMEDIATED`. Les transitions supplémentaires
(`CLOSED_ACCEPTED ← CLOSED_REJECTED ← CLOSED_DUPLICATE ← DEFERRED`)
sont utiles mais peuvent être introduites en v1.1.

**Réserve 1 (ADVR-13). Le `certification.owner` est juridiquement
nécessaire mais opérationnellement non défini.**

Le §6.3 exige un `certification.owner` qui surveille les triggers de
révocation. Mais la surveillance elle-même n'a pas de mécanisme :
- Est-ce un cron ? Un webhook CI ? Une revue trimestrielle humaine ?
- Si l'owner oublie, la `CERTIFIED` reste-t-elle valide ? Le §6.3 dit
  « *Certification never expires by time alone; it expires by state
  divergence* ». Donc oui, l'oubli n'invalide pas. Mais alors l'owner est
  un rôle purement consultatif. Laquelle des deux lectures est la bonne ?
- Aucune des deux lectures n'est articulée.

**Sévérité** : S2 (champ obligatoire mais opération non définie → risque
d'inertie silencieuse).
**Recommandation** : ajouter trois sous-conditions au §6.3 :
- « *6.3.10. Mécanisme de surveillance déclaré : `manual`,
  `cron:<expr>`, ou `webhook:<target>`.* »
- « *6.3.11. Validité de la déclaration : si le mécanisme est
  `manual`, la dernière date de revue est dans `certification.last_reviewed`
  et la `CERTIFIED` est `SUSPENDED` si cette date excède le seuil déclaré
  par `certification.review_cadence`.* »
- « *6.3.12. Révocation automatique : tout changement de l'état des
  triggers observable par le mécanisme déclenche une transition
  `CERTIFIED → SUSPENDED` automatique, sans intervention humaine.* »

**Réserve 2 (ADVR-15). Le split de l'autorité canon est indécis.**

`CANON_CHANGE_PROPOSAL.md` Impact Analysis déclare la création d'une
*nouvelle* autorité `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` mais le
dossier §9 distribue les règles entre `PILOTAGE.md`, `CONVENTIONS.md`,
`GATE_ASSURANCE_GOVERNANCE.md`, et `pre-merge-gate.md`. `COND-05` exige
qu'une seule de ces options soit tranchée. Sans cette décision, le risque
est que la M1 migration choisisse implicitement *les deux* (nouveau fichier
+ modifications dispersées) — ce qui violerait CR#5 *pendant* la migration.

**Sévérité** : S2 (canon transitoire incohérent).
**Recommandation** : la décision M1 doit choisir :

| Option | Conséquence |
|---|---|
| **A. Une seule autorité nouvelle `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`** | Modifie `GATE_ASSURANCE_GOVERNANCE.md` (cite la nouvelle autorité plutôt que de la dupliquer) et `PILOTAGE.md` (pointeur). Plus propre, mais le canon croît. |
| **B. Pas de nouvelle autorité — extension de `GATE_ASSURANCE_GOVERNANCE.md`** | Le canon ne croît pas, mais le fichier existant grossit (+~300 lignes). Risque de dilution. |
| **C. Split strict : `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` pour les statuts, le lifecycle et la matrice ; `GATE_ASSURANCE_GOVERNANCE.md` uniquement pour le schema §9.1** | Le moins mauvais : canon séparé pour le spécifique, gate canon pour le générique. |

**Préférence** : Option C. Elle respecte la séparation sémantique
existante (gate canonique ≠ domaine métier) et limite la duplication.

**Interaction avec ADR existantes.** Vérifié :

- ADR 0043 (orthogonalité runtime/assurance) : respecté.
- ADR 0049 (knowledge governance) : respecté, D8 refuse explicitement le
  court-circuit.
- ADR 0050 (assurance schema) : respecté, le schéma 1.1 est additif avec
  cutoff.
- ADR 0031 (autonomous-run sequences) : *non vérifié* — `COND-06` le
  relève. La lecture charitable est que les runs autonomes s'arrêtent
  dès qu'un `S0`/`S1` requiert une décision humaine, et que c'est
  l'arbitre (humain) qui reprend. La lecture stricte est que la chaîne
  autonome devient fragile. **Réserve secondaire** : ADR 0031 doit être
  citée dans la décision M1 comme interaction à vérifier.

### 3.4 Capitalisation

**Verdict : CONFORME, sous une réserve.**

**Six destinations (§8).** Le tableau de promotion est exhaustif et
exige une réponse explicite pour chaque finding — y compris `NOT_APPLICABLE
+ reason`. C'est conforme au *pattern* de maturité d'ADR 0049. Le
couplage avec le test canonique, la gate, la checklist, la règle
normative (via ADR 0049) et le corpus couvre tous les axes de capitalisation.

**Cas du corpus (§7.2).** Le contrat est strict : tout `CONFIRMED`
finding produit exactement une entrée corpus. C'est la bonne règle. La
*mécanique* de création de l'entrée — qui l'écrit, avec quel oracle, quelle
relecture — n'est pas encore spécifiée. C'est le trou principal.

**Réserve (ADVR-18). L'attaquant écrit le test anti-régression.**

Le finding record exige `non_regression.test_id` + `test_path` +
`fails_before: true` + `passes_after: true`. Mais le seul acteur qui
détient la connaissance de la reproduction est l'attaquant — donc
l'attaquant écrit le test. Trois problèmes :

1. **Biais de confirmation.** L'attaquant qui a trouvé la faille peut
   écrire un test qui rate superficiellement (oracle creux, assertion de
   surface seulement) et qui semble verrouiller. Le test passe après le
   fix sans valider le *comportement*.
2. **Pas de revue indépendante du test.** Le test est validé par le
   reviewer du finding, qui peut être le même agent qui a écrit la
   remediation.
3. **Pas de mécanisme de re-exécution par un tiers.** Le §6.2.7 exige
   `fails_before: true` mais ne vérifie pas que `fails_before` est constaté
   *avant* la remediation par un agent *différent* de l'attaquant.

**Sévérité** : S2 (capitalisation mécaniquement biaisée).
**Recommandation** : ajouter au §5.3 du finding record :
- `non_regression.witnessed_by: "<role>"` — l'agent qui a constaté
  `fails_before` *différent* de `discovered_by`.
- `non_regression.test_review: { reviewer: ..., verdict: PASS|FAIL, date: ... }`
  — un reviewer distinct a validé la qualité de l'oracle.
- Au niveau `A2`, ces deux champs deviennent obligatoires, comme le
  `counter_proof.actor` distinct l'est déjà.

**Connaissance.** Le chemin ADR 0049 (« observation → candidate → audit →
independent review → human → canonical ») est respecté par D8. La
non-promotion directe à `CONVENTIONS.md` ou `AGENTS.md` est explicite,
ce qui ferme la porte au *shortcut normatif*.

### 3.5 Simplicité

**Verdict : SIMPLICITÉ ACCEPTABLE, deux complexités peuvent être supprimées.**

**Carte globale.** Le dossier est dense mais navigable. Les principes
généraux sont respectés :

- Pas de nouvelle autorité cachée (sous réserve du split §3.3).
- Pas de nouvelle phase, pas de nouvelle route.
- Pas de nouveau runtime status (`FINAL_STATUS` reste intact).
- Trois statuts (`IMPLEMENTED`, `CERTAIN`/`UNCERTAIN`, `CERTIFIED`/`SUSPENDED`)
  équivalent à quatre statuts distincts + un fail-closed default — c'est
  minimal.

**Complexités identifiées pour suppression.**

| # | Complexité | Recommandation |
|---|---|---|
| C1 | Le record finding (§5.3) a ~30 champs, dont `history[]` (tableau de transitions), `arbitration` (5 sous-champs), `non_regression` (5 sous-champs), `promotion` (6 sous-champs), `counter_proof` (4 sous-champs), `knowledge` (2 sous-champs) | Restreindre v1.0 à : `finding_id`, `class`, `severity`, `confidence`, `reproduction`, `blast_radius`, `status`, `promotion.destinations`, `non_regression.test_id`, `counter_proof.verdict`. Les autres champs deviennent un *audit log* séparé en `findings/<id>.log.yaml`. Réduction attendue : ~50 %. |
| C2 | La non-claim de `PASS_ADVERSARIAL` est intégrée *littéralement* dans le §6.2 (50 mots). | La remplacer par un pointeur canonique : `non_claim_ref: "ADVERSARIAL_NON_CLAIM_v1"`. La phrase canonique vit dans `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §X. Reduces duplication and risk of drift. |
| C3 | Le diagramme mermaid §2.3 a 25 nœuds, la state machine §5.1 a 17 états. | Pour la documentation, ces diagrammes sont utiles. Pour le runtime, les implémentations devraient être basées sur des automates finis tabulaires — le diagramme devient une projection. Documenter le *runtime encoding* à part. |
| C4 | La règle d'exclusion `A0` (§4.2) est une phrase négative qui cite cinq chemins. | Déplacer la liste vers une variable canonique `A0_EXCLUDED_PATHS` dans `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`. Le trench reste lisible, l'évolution est triviale. |

**Sévérité** : S3 (cosmétique et maintenabilité).
**Recommandation** : appliquer C1, C2, C4 dans la version v1.0 du
schéma ; C3 dans la documentation, sans impact sur le runtime.

---

## 4. Attaques n'ayant pas produit de réserve

| # | Attaque | Résultat |
|---|---|---|
| A1 | Régression silencieuse de C | Aucune. La séparation C/A est garantie par construction (D5, D9). |
| A3 | Shunt de la boucle adversariale par agent zélé | Aucune. D7 interdit explicitement la réduction unilatérale d'assurance par un agent. Le seul levier d'un agent est l'escalade. |
| A6 | Shortcut de capitalisation | Aucune. D8 interdit la promotion directe à `CONVENTIONS.md` ou `AGENTS.md`. |
| A8 | Statut caché parallèle | Aucune. D1 refuse explicitement un `ADVERSARIAL_STATUS` sibling. |
| A10 | Subversion de la migration par projet solo | `MR-07` traité en §3.2. |
| A12 | Modification en catimini | Aucune. La migration exige un ADR + décision humaine + revue indépendante. |

**Bornes de cette preuve.** Comme l'impose le dossier lui-même (§6.2
non-claim), l'absence de réserve additionnelle est une preuve bornée
portant sur 12 attaques et sur un instant de lecture.

---

## 5. Réserves consolidées

| ID | Sévérité | Réserve | Section |
|---|---|---|---|
| `ADVR-11` | S1 | « Purement additif » partiellement inexact : les énumérations `gate_family` et `checkpoint` sont étendues, ce qu'un lecteur v1.0 ne peut pas ignorer proprement | §3.1 |
| `ADVR-12` | S2 | `A2` exige un acteur distinct ; `MR-07` reconnaît le problème sans contrat de repli formel | §3.2 |
| `ADVR-13` | S2 | `certification.owner` est obligatoire mais le mécanisme de surveillance n'est pas défini | §3.3 |
| `ADVR-14` | S2 | Le trigger `A2` sur historique S0/S1 laisse `N` (fenêtre) non définie | §3.2 |
| `ADVR-15` | S2 | Split de l'autorité canon non tranché (COND-05) | §3.3 |
| `ADVR-16` | S2 | Trigger « criticalité contestée → A1 » laisse « contestée » non défini | §3.2 |
| `ADVR-17` | S2 | Le non-regression lock est écrit par l'attaquant, sans témoin ni revue indépendante | §3.4 |
| `ADVR-18` | S3 | Schéma finding record (~30 champs) trop riche pour v1.0 ; simplifiable | §3.5 |

Toutes les réserves ADVR-11 à ADVR-18 sont **nouvelles** et
indépendantes des ADVR-01 à ADVR-10 du self-review. Elles ne font pas
double emploi.

**Cumul de sévérité.** Trois S1+ sur la cohérence structurelle
(`ADVR-11` seule). Cinq S2 sur la gouvernance et la proportionnalité.
Aucun S0 (aucune violation de sécurité, intégrité, canon ou
silencieuse-corruption).

---

## 6. Recommandations

**Avant la décision M1 (CANON_CHANGE_PROPOSAL.md → ACCEPTED).**

1. **Décider le split d'autorité canonique** (`ADVR-15`, `COND-05`).
   Recommandation : Option C (nouvelle autorité
   `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` pour le spécifique ;
   `GATE_ASSURANCE_GOVERNANCE.md` pour le schéma générique).
2. **Spécifier le contrat de repli `A2` pour dépôt solo** (`ADVR-12`,
   `COND-04`). Recommandation : `A2_DISTINCT_AGENT_PROXY` avec
   identité d'attaquant, d'agent LLM, de system prompt, et validation
   par un second agent (ou un humain) du verdict.
3. **Définir N et « contestée »** (`ADVR-14`, `ADVR-16`).
   Recommandations : `N=10` runs ; « contestée » = un gate expert
   identifié refuse la classification déclarée au niveau via une
   objection écrite dans `INTAKE.md`.
4. **Documenter le mécanisme de `certification.owner`** (`ADVR-13`).
   Recommandation : ajouter les sous-conditions 6.3.10–6.3.12
   proposées en §3.3.
5. **Ajouter témoin et revue indépendante au non-regression lock**
   (`ADVR-17`). Recommandation : les champs
   `non_regression.witnessed_by` et `non_regression.test_review`,
   obligatoires à `A2`.

**Avant l'implémentation M2.**

6. **Corriger l'affirmation purement additive** (`ADVR-11`).
   Recommandation : amender le §9.1 pour distinguer *blocs
   additionnels* et *énumérations étendues*, et exiger une
   vérification de lecture par validateur v1.0 représentatif
   (POC COND-02).
7. **Simplifier le schéma finding record pour v1.0** (`ADVR-18`).
   Recommandation : extraire `history[]`, `arbitration` et `knowledge`
   vers un audit log séparé. Réduire à ~15 champs essentiels.
8. **Citer ADR 0031 dans le ADR M1** : vérifier formellement
   l'interaction avec les autonomous-run sequences (COND-06).

**Pendant le ramp R0 (advisory).**

9. **Mesurer le coût réel de `A1` sur des changements ordinaires**
   (COND-03). Recommandation : exécuter au moins 5 runs `A1`
   sous R0, mesurer le temps de campagne moyen, fixer un seuil
   quantitatif (par exemple `<30 min` pour un changement non-sécurité)
   avant de débloquer R1.

---

## 7. Décision argumentée

**Question posée.** *La proposition peut-elle devenir une évolution
canonique de Vibebackbone ?*

**Réponse.** **Oui, sous condition de lever les six préconditions
listées en §6 (items 1–6) avant la rédaction du ADR M1.**

**Argumentation.**

Le dossier `2026-07-28_1002_adversarial-loop-governance-design` est
remarquablement cohérent et exhaustif. Le cartographie du cycle
(`02_AUDIT.md`), les arbitrations structurelles (`03_DECISION.md`),
le design v0.2 (`04_DESIGN_DOSSIER.md`) et la stratégie de migration
(`05_MIGRATION_STRATEGY.md`) forment un ensemble où chaque décision
est justifiable, chaque écart aux ADR existants est explicite, et
chaque limite est reconnue. La culture d'auto-critique du dossier
(ADVR-01 à ADVR-10 du self-review) est saine et a effectivement
fermé dix bloqueurs.

Les huit réserves additionnelles que je lève en tant qu'acteur
distinct ne contredisent pas cette lecture :

- `ADVR-11` (S1) est une correction d'affirmation, pas une erreur
  conceptuelle. Le mécanisme de compatibilité du schéma existe
  déjà dans ADR 0050 ; la proposition l'invoque, elle doit juste
  reconnaître qu'elle l'étend (vs. l'ajouter).
- `ADVR-12` (S2) et `ADVR-14`, `ADVR-16` (S2) sont des *défauts de
  spécification*, pas des contradictions. Ils sont corrigibles dans
  la rédaction du ADR M1.
- `ADVR-13`, `ADVR-15`, `ADVR-17` (S2) sont des points où le design
  *s'engage à moitié*. Le design dit « il faut un owner » sans
  dire « il fait quoi » ; il dit « split d'autorité » sans
  trancher ; il dit « non-regression lock » sans témoin. Tous
  trois sont des compléments logiques, pas des remises en cause.
- `ADVR-18` (S3) est cosmétique.

Aucune réserve ne crée une régression de la gouvernance actuelle.
Aucun principe Vibebackbone n'est violé. La proposition est l'extension
minimale qui satisfasse la séparation des quatre claims et qui
corrige la faille systémique identifiée (AG-01 — absence de devoir
de falsification).

**Cohérence finale avec la règle d'or du dossier.**

> *« Ajouter de la robustesse sans complexifier inutilement la
> boucle principale. »*

La proposition ajoute **un nouveau gate family** dans une
architecture qui en avait déjà trois, **un checkpoint** dans une
architecture qui en avait déjà trois, **trois statuts** dans une
architecture qui en avait zéro (en plus d'`implementation_status`
qu'on peut voir comme un lift de `FINAL_STATUS.status`), **un
mode de review** dans une architecture qui en avait déjà deux. Le
ratio est *un nouveau X par catégorie existante*, ce qui est la
densité minimale pour ajouter une dimension orthogonale. La
proportion est correcte.

**Sort de la condition COND-01.**

Cette revue satisfait la condition `COND-01` (« genuinely independent
review before M1 decision »). Les autres conditions (`COND-02` à
`COND-06`) restent à la charge de la M1 (ADR + décision humaine).
La publication de cette revue, le suivi de ses items S1 (`ADVR-11`)
et l'amorce des items S2 (`ADVR-12`, `ADVR-13`, `ADVR-15`,
`ADVR-17`) sont des prérequis à l'`ACCEPTED` du ADR.

**Criticité de l'avis.**

Cette revue n'est pas un blanc-seing. Elle **ne peut pas signer
un** `PASS_CERTIFIED` sur la proposition. Une décision canonique
engageant 4 distributions et 50+ skills mérite deux lectures
indépendantes minimum. La présente en est une ; une seconde
(humaine, ou par un agent de profil différent) est recommandée
avant `ACCEPTED`.

---

## 8. FINAL_STATUS

```yaml
FINAL_STATUS:
  verdict: "PASS_WITH_CONDITIONS"
  independent_actor: true
  architecture_consistent: true            # confirmé, sous ADVR-11
  additive_design_confirmed: "partial"    # blocs additifs ; énumérations étendues (ADVR-11)
  proportionality_confirmed: "partial"    # A0/A1/A2 ok ; COND-04, ADVR-14, ADVR-16 à lever
  finding_lifecycle_confirmed: true       # complet, ADVR-17 à ajouter
  certification_model_confirmed: "partial"  # D6 correct ; ADVR-13 mécanismes manquants
  simplicity_confirmed: "partial"          # S3 ; ADVR-18 simplifiable
  critical_objections:
    - id: "ADVR-11"
      severity: S1
      title: "Affirmation « purely additive » incomplète"
      description: "Les énumérations gate_family et checkpoint sont étendues en v1.1, ce qu'un lecteur v1.0 ne peut pas ignorer sans risque de réinjection silencieuse en OTHER."
    - id: "ADVR-12"
      severity: S2
      title: "A2 inapplicable en dépôt solo sans fallback contract"
      description: "L'exigence d'acteur distinct (MR-07) n'a pas de contrat de repli formalisé. Vibebackbone est lui-même un dépôt solo."
    - id: "ADVR-13"
      severity: S2
      title: "certification.owner sans mécanisme de surveillance"
      description: "Le owner est obligatoire mais ni sa cadence de revue ni son mécanisme de détection de divergence ne sont définis."
    - id: "ADVR-14"
      severity: S2
      title: "Trigger A2 « historique S0/S1 dans les N derniers runs » : N non défini"
      description: "Sans N explicite, le trigger est soit toothless (N=∞) soit tyrannique (N=1)."
    - id: "ADVR-15"
      severity: S2
      title: "Split d'autorité canonique non tranché (COND-05)"
      description: "Le design propose une nouvelle autorité ADVERSARIAL_ASSURANCE_GOVERNANCE.md tout en gardant des règles dans GATE_ASSURANCE_GOVERNANCE.md ; risque de canon dupliqué."
    - id: "ADVR-16"
      severity: S2
      title: "Trigger « criticalité contestée → A1 » : « contestée » non défini"
      description: "Sans définition opérationnelle, le contest devient soit systématique (toute objection) soit vide (jamais)."
    - id: "ADVR-17"
      severity: S2
      title: "Non-regression lock écrit par l'attaquant sans témoin ni revue indépendante"
      description: "Le finding record exige fails_before / passes_after ; l'oracle est rédigé par l'attaquant sans validation tierce, créant un biais de confirmation."
    - id: "ADVR-18"
      severity: S3
      title: "Schéma finding record trop riche pour v1.0"
      description: "30 champs, dont history[] et des sous-blocs verbeux. Simplifiable à ~15 champs essentiels avec un audit log séparé."
  recommended_changes:
    - "Lever COND-04 (fallback A2 pour dépôt solo) avant M1"
    - "Lever COND-05 (split d'autorité canonique) avant M1"
    - "Définir N (ADVR-14) et « contestée » (ADVR-16) avant M1"
    - "Amender §6.3 pour spécifier le mécanisme de certification.owner (ADVR-13)"
    - "Ajouter witnessed_by et test_review au non-regression lock (ADVR-17)"
    - "Corriger l'affirmation « purely additive » pour distinguer blocs et énumérations (ADVR-11)"
    - "Citer ADR 0031 dans l'interaction M1 (COND-06)"
    - "Mesurer le coût A1 sous R0 (COND-03) avant R1"
  can_become_canonical: true
  implementation_authorized: false         # design proposal only; pas d'implémentation autorisée par cette revue
  next_authorized_action: "Décision humaine M1 sur CANON_CHANGE_PROPOSAL.md après intégration des items §6.1–6.5 ; ADR 00XX rédigé avec les amendements S1 et S2 listés ; suite M2 conditionnée au POC COND-02 (compatibilité v1.0/v1.1) et à la résolution formelle de COND-04/COND-05/COND-06."
```

---

## 9. Conformité aux contraintes de la revue

- ✅ Aucune modification d'un fichier du dossier de design (les 9 fichiers
  existants sont intacts ; seul ce 8e fichier est ajouté).
- ✅ Aucune modification normative (`docs/GATE_ASSURANCE_GOVERNANCE.md`,
  `docs/PILOTAGE.md`, `docs/CONVENTIONS.md`, ADR existants, templates,
  prompts, distributions — tous intacts).
- ✅ Aucun commit, aucun push.
- ✅ Aucun changement de template, de prompt, d'ADR.
- ✅ Production uniquement d'une revue critique.

Cette revue est un *additif* au dossier, pas une mutation. Elle
sert `COND-01` et lève partiellement la condition `HANDOFF` posée
par le `07_CLOSEOUT.md` du run original. La levée complète
appartient à la décision humaine M1.
