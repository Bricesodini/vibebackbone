---
run_id: "2026-07-29_1021_adversarial-gate-population"
phase: "02_DISPOSITION_MATRIX"
status: "PROPOSED"          # PROPOSED -> ARRETEE requiert validation humaine
arbitration_required: true
agent: "claude-opus-5 (Claude Code)"
measured_at_commit: "6b0daf4785d652b23931b80aafba57979e69d9b4"
produced_at: "2026-07-29T08:40:00Z"
---

# 02_DISPOSITION_MATRIX — classification des 10 runs post-cutoff non conformes

**Cet artefact ne modifie rien.** Il classe. Aucun bloc adverse ne sera écrit,
créé ou corrigé tant que ce document porte `status: PROPOSED`.

## 1. Règle de reconstructibilité appliquée

Un bloc adverse rétroactif n'est autorisé que si **les artefacts du run lui-même,
datés du run**, portent la substance exigée par le schéma 1.1 : identités
attaquant/défenseur, surfaces déclarées et non explorées, findings avec état et
confiance, verdict, incertitude résiduelle.

Sont **interdits** comme sources de reconstruction :

- la mémoire ou l'inférence de l'agent ;
- les artefacts d'un run postérieur ;
- le raisonnement « ce qui a dû être fait » ;
- l'outillage qui n'existait pas à la date du run.

Quand la substance manque, la disposition est `HISTORICAL_NON_RECONSTRUCTIBLE`.
Cette valeur **n'est pas une conformité** et ne le devient jamais : elle est une
dette enregistrée, comptée séparément, et visible dans le verdict du gate.

## 2. Dispositions possibles

| Disposition | Sens | Effet sur le gate |
|---|---|---|
| `RECONSTRUCTIBLE` | substance adverse présente dans les artefacts contemporains ; le bloc peut être assemblé sans inférence | doit devenir CONFORMANT |
| `SCHEMA_REPAIR` | bloc présent, substance présente, champs non conformes au schéma | doit devenir CONFORMANT |
| `HISTORICAL_DEBT_ATTESTED` | le run a déclaré contemporainement l'absence d'évaluation, avec motif opposable | dette, non bloquant, comptée |
| `HISTORICAL_NON_RECONSTRUCTIBLE` | ni substance ni déclaration contemporaine | dette, non bloquant, comptée |
| `CURRENT_NON_CONFORMANCE` | défaut actuel réparable par un travail actuel | **bloquant** |
| `ARBITRATION_REQUIRED` | la classification dépend d'une décision normative que l'agent n'a pas autorité à rendre | **bloquant jusqu'à arbitrage** |

Aucune disposition ne permet de baisser un `adversarial_level`. La révision de
niveau est traitée en §4, hors de cette table, et n'est jamais un moyen d'obtenir
le vert.

## 3. Matrice

### 3.1 — `2026-07-28_1400_m2-adversarial-loop-implementation`

- **Déclaration contemporaine** : `adversarial_status: NOT_ASSESSED — no vbb-adversarial-gate.py yet`
- **Substance dans les artefacts du run** : aucune. Le run *construit* la dimension adverse.
- **Analyse** : le validateur n'existait pas quand le run s'est clos ; le run l'a
  écrit. Reconstruire un bloc validé par un outil que le run a lui-même produit
  ensuite serait un anachronisme, pas une preuve.
- **Disposition proposée** : `HISTORICAL_DEBT_ATTESTED`
- **Motif d'opposabilité** : déclaration explicite, datée, avec cause vérifiable
  (absence d'outil), inscrite au closeout d'origine.

### 3.2 — `2026-07-28_1600_r0-adversarial-audit-of-m2-implementation`

- **Déclaration contemporaine** : aucune dans le frontmatter ; l'`ASSURANCE_STATUS`
  porte `9 confirmed falsifications + 3 new via re-attack-the-attacker`.
- **Substance dans les artefacts du run** : `02_AUDIT.md`, `03_DECISION.md`,
  `06_INDEPENDENT_REVIEW.md` — le run **est** une campagne adverse.
- **Analyse** : la substance existe et est contemporaine. Ce qui manque est la
  *forme* : le schéma 1.1 n'était pas encore le format de sortie.
- **Disposition proposée** : `RECONSTRUCTIBLE` — **sous réserve** de vérification
  ligne à ligne que les 12 falsifications portent un état et une confiance
  déductibles sans inférence. Si un seul finding exige d'être qualifié
  a posteriori → bascule en `HISTORICAL_NON_RECONSTRUCTIBLE` pour le run entier.
- **Vérification exigée avant écriture** : audit des 12 findings, tracé.

### 3.3 — `2026-07-28_1800_r1-r0-findings-normative-arbitration`

- **Déclaration contemporaine** : aucune revendication adverse. Le run introduit
  `PRE_CERTIFICATION` / `MIGRATION` comme statuts.
- **Substance** : arbitrage normatif, pas de campagne.
- **Analyse** : le sujet du run est une décision de canon, pas un artefact attaqué.
  Le frontmatter déclare `A2` — cohérent avec « canon-gating » — mais un run
  d'arbitrage produit-il une campagne, ou consomme-t-il celle du run arbitré ?
  Le canon ne tranche pas explicitement ce cas.
- **Disposition proposée** : `ARBITRATION_REQUIRED`
- **Question à trancher** : un run d'arbitrage normatif doit-il porter sa propre
  campagne adverse, ou une attestation dérivée du run audité qu'il arbitre ?

### 3.4 — `2026-07-28_2000_m2-bis-adversarial-loop-bootstrap-deployment`

- **Déclaration contemporaine** : `adversarial_status: NOT_ASSESSED — no A1/A2 validator run on M2-BIS itself`
- **Substance** : aucune campagne sur M2-BIS ; le run déploie l'outillage.
- **Analyse** : identique à §3.1 — auto-application impossible à la date du run.
- **Disposition proposée** : `HISTORICAL_DEBT_ATTESTED`

### 3.5 — `2026-07-28_2200_a2-certification-of-m2-bis-bootstrap`

- **Déclaration contemporaine** : bloc `adversarial:` **présent**, 14 findings.
- **Défaut mesuré** : `[S1] adv-a2-defender-identity` absent ;
  `[S2] adv-finding-{0..13}-confidence` et `-state` invalides (28 échecs).
- **Analyse** : la substance est là, le schéma ne l'est pas. Les valeurs de
  `confidence`/`state` sont-elles **présentes mais hors énumération** (réparable
  sans inférence) ou **absentes** (non réparable sans qualifier après coup) ?
  Cette distinction décide de la disposition et n'est pas encore tranchée.
- **Disposition proposée** : `SCHEMA_REPAIR` **si et seulement si** les valeurs
  existent et sont seulement mal orthographiées ; sinon
  `HISTORICAL_NON_RECONSTRUCTIBLE`.
- **Vérification exigée avant écriture** : inspection des 14 findings.

### 3.6 — `2026-07-28_2300_r2-a2-arbitration-of-a2-findings`

- **Déclaration contemporaine** : `adversarial_status: NOT_REQUIRED — R2 n'est pas une A2 ; c'est un arbitrage`
- **Conflit** : le frontmatter déclare `adversarial_level: "A2"`.
- **Analyse** : le run affirme **contemporainement** que son sujet ne requiert pas
  de campagne, tout en se déclarant A2. Ce n'est pas une rétrogradation
  a posteriori — la contradiction est d'origine. Elle révèle que le canon
  confond deux choses : le **niveau de criticité du sujet** et l'**obligation de
  conduire une campagne**.
- **Disposition proposée** : `ARBITRATION_REQUIRED`
- **Question à trancher** : `adversarial_level: A2` implique-t-il toujours
  l'obligation d'une campagne, ou existe-t-il un `adversarial_status: NOT_REQUIRED`
  légitime pour un sujet A2 ? Si oui, le gate doit l'accepter explicitement ;
  s'il n'existe pas, ce run est en dette.

### 3.7 — `2026-07-29_0100_m3-remediation-of-a2-findings`

- **Déclaration contemporaine** : `adversarial_status: REMEDIATION_COMPLETE_AWAITING_RETEST`, `certification_status: NOT_CERTIFIED`
- **Substance** : `02_FAILS_BEFORE.md`, `04_PASSES_AFTER.md`, `05_TEST_REPORT.md`,
  `06_REVIEW.md` — matériau de non-régression complet et daté.
- **Analyse** : le run déclare correctement qu'il attend un retest ; le retest est
  `2026-07-29_0300`. La substance adverse propre au run est de la remédiation,
  pas de l'attaque.
- **Disposition proposée** : `RECONSTRUCTIBLE` en tant que bloc à
  `adversarial_status: REMEDIATION_COMPLETE_AWAITING_RETEST` — c'est-à-dire un
  bloc conforme au schéma qui **ne revendique aucun PASS**. La forme manque, le
  fond est déjà honnête.
- **Note** : son `status: "READY"` avec `NOT_CERTIFIED` relève de G3 (lot R3),
  pas de cette matrice.

### 3.8 — `2026-07-29_0300_a2-retry-certification-of-m3-remediation`

- **Déclaration contemporaine** : `02_ADVERSARIAL_CAMPAIGN.md` porte une table
  d'indépendance attaquant/défenseur sur 5 dimensions, `04_NON_REGRESSION_LOCK.md`,
  `03_FINDINGS.md`, `06_INDEPENDENT_REVIEW.md`.
- **Analyse** : c'est le cas le plus complet du corpus. Le run a même anticipé son
  propre échec : *« check_a2_distinct_identity retournerait FAIL … Cette campagne
  ne peut donc pas se décerner PASS_ADVERSARIAL »*. Toutes les données du schéma
  1.1 sont présentes et datées.
- **Disposition proposée** : `RECONSTRUCTIBLE` — assemblage direct, aucune
  inférence requise. **Le bloc devra reproduire l'auto-échec**, pas le masquer :
  `adv-a2-distinct` doit rester FAIL, et la certification rester NOT_CERTIFIED.
- **Priorité** : la plus haute des `RECONSTRUCTIBLE` — c'est le cas de référence
  qui prouve que la reconstruction n'est pas un blanchiment.

### 3.9 — `2026-07-29_0840_audit-remediation`

- **Défaut mesuré** : bloc présent, `[S1] adv-a2-distinct` FAIL —
  `attacker.llm == defender.llm == claude-opus-5`.
- **Analyse** : ce n'est pas de la dette historique. Le run est postérieur à
  l'outillage, le bloc existe, le défaut est réel et **actuel** : il n'y a pas eu
  d'acteur distinct.
- **Disposition proposée** : `CURRENT_NON_CONFORMANCE` — **bloquant**.
- **Voie de résolution** : R5 uniquement. Un acteur réellement distinct doit
  conduire la revue. L'audit externe reçu le 2026-07-29 est le candidat ; son
  identité LLM exacte doit être obtenue pour renseigner `attacker_identity`.
  Aucune autre voie n'est acceptable : modifier les identités déclarées pour
  passer le check serait une falsification.

### 3.10 — `2026-07-30_0500_final-publication-of-v1.1-certification`

- **Déclaration contemporaine** : `adversarial_status: PASS_ADVERSARIAL`,
  `certification_status: CERTIFIED`. **Aucun bloc `adversarial:` validable.**
- **Analyse** : c'est le cas le plus grave de la matrice, et il diffère en nature
  de tous les autres. Les neuf autres runs *omettent* une déclaration ; celui-ci
  **affirme un PASS et une certification** sans porter la structure qui permettrait
  de les valider. Une revendication positive non validable est plus dangereuse
  qu'une omission.
- **Disposition proposée** : `ARBITRATION_REQUIRED`, traitée en priorité P0.
- **Questions à trancher** :
  1. Le `PASS_ADVERSARIAL` revendiqué est-il dérivé de `2026-07-30_0100`
     (certification A2 auth, seul run conforme au gate) ? Si oui, une
     **attestation dérivée** explicite est requise, avec lien vérifiable — pas une
     recopie du verdict.
  2. Si le PASS n'est dérivable d'aucun run conforme, la revendication doit être
     retirée et `certification_status` révisé. Cela toucherait la certification
     v1.1 publiée.
- **Interdiction explicite** : ne pas fabriquer un bloc adverse pour rendre ce run
  vert. Si la revendication n'est pas soutenue, c'est la revendication qui tombe.

## 4. Révisions de niveau — aucune proposée

Aucune rétrogradation d'`adversarial_level` n'est proposée par cette matrice.

Deux runs (§3.3, §3.6) posent une question de niveau, mais elle est reclassée en
question **normative** (« A2 implique-t-il obligation de campagne ? ») et non en
question de niveau (« ce run est-il vraiment A2 ? »). La différence est
volontaire : la première se tranche par le canon et s'applique uniformément ; la
seconde se tranche run par run et ouvre exactement la porte que la consigne
interdit.

Si l'arbitrage conclut qu'un niveau a été mal déclaré à l'origine, la révision
exigera : la trace du niveau initial, la justification au regard de la matrice
§1.2, et une validation humaine distincte de l'agent qui la propose.

## 5. Synthèse

| Disposition | Runs | Bloquant |
|---|---|---|
| `RECONSTRUCTIBLE` (sous vérification) | §3.2, §3.7, §3.8 | non |
| `SCHEMA_REPAIR` ou dégradation | §3.5 | non |
| `HISTORICAL_DEBT_ATTESTED` | §3.1, §3.4 | non |
| `HISTORICAL_NON_RECONSTRUCTIBLE` | — (aucun à ce stade) | non |
| `CURRENT_NON_CONFORMANCE` | §3.9 | **oui** |
| `ARBITRATION_REQUIRED` | §3.3, §3.6, §3.10 | **oui** |

**Aucun run n'est classé conforme par cette matrice.** Trois exigent une décision
normative humaine, un exige un acteur A2 distinct, quatre exigent une vérification
de substance avant toute écriture.

## 6. Conditions d'arrêt de la matrice

Ce document passe en `status: ARRETEE` quand :

1. les trois questions d'arbitrage (§3.3, §3.6, §3.10) sont tranchées par décision
   humaine tracée ;
2. les vérifications de substance (§3.2, §3.5) sont exécutées et consignées ;
3. la révision §3.10 est rendue, y compris si elle invalide une certification
   publiée.

Tant que ces trois conditions ne sont pas remplies, **aucun bloc adverse n'est
écrit**.
