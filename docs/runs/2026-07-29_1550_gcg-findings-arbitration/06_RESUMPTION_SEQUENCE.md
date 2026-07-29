---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "06_RESUMPTION_SEQUENCE"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T13:50:00Z"
ended_at: null
artifacts_consumed:
  - "02_FINDINGS_REGISTER.md"
  - "03_DEPENDENCY_AND_ARBITRATION_MAP.md"
  - "05_DECISIONS_REQUIRED.md"
artifacts_produced:
  - "06_RESUMPTION_SEQUENCE.md (this file)"
---

# 06_RESUMPTION_SEQUENCE — GCG-ARB-01

**Aucun de ces runs n'est ouvert ni exécuté.** Ce document est une proposition
de séquence, dérivée du graphe de `03` et des décisions de `05`. Chaque run a un
objectif unique et une condition d'arrêt qui peut être atteinte en **échec**.

## 0. Vue d'ensemble

> **Révisée après revue indépendante** (`04_INDEPENDENT_ARBITRATION_REVIEW.md`).
> R-1 est déplacée après R-2/R-3 (l'ordre initial était circulaire) et sa
> condition d'arrêt réécrite (elle ne pouvait pas échouer) ; R-2 et R-3
> reçoivent des conditions d'échec atteignables (les précédentes l'étaient par
> aucune des options recommandées) ; **R-5 ouvre avec sa condition d'échec déjà
> remplie** ; R-7 perd la moitié de son objet, mesurée dans ce run ; un run
> **R-A** est ajouté en tête pour les corrections mécaniques sans décision.

```
   R-A  corrections sans décision (dont GCG-36) ─────── préalable à R-0
         │
         ▼
   R-0  P0 certification publiée ────────────────────── indépendant, immédiat
   R-7  instruction du dernier fait en suspens ─────── indépendant, à tout moment

   R-2  coordonnée (D1) ──┐
   R-3  population (D2) ──┤
                          ├──► R-1 préséance déclaré/dérivé (D4)
                          │              │
                          │              ▼
                          │         R-4 bornes (D3)
                          │              │
                          │              ▼
                          │         R-5 prédicats (D5·D6·D7)
                          │              │
                          │              ▼
                          │         R-6 totalité (GCG-14+03)
                          │              │
                          └──────────────┴──► R-8 honnêteté
                                                    │
                                                    ▼
                                             R-9 ADR ou absorption
```

---

## R-A — Corriger ce qui ne demande aucune décision
**Priorité P0 pour GCG-36 · aucune dépendance · préalable à R-0**

| | |
|---|---|
| **Objectif unique** | appliquer les six corrections que `03` §4.2 établit comme exécutables sans décision préalable |
| **Décisions préalables** | aucune |
| **Findings fermés** | GCG-36, GCG-15, GCG-19, GCG-22, GCG-24 ; volet code de GCG-09 |
| **Contenu** | rétablir la primauté d'`OVERCLAIM` sur la lecture historique (ordre des branches de `classify_run`) · résolveur de closeout unique (I11) · ordre dérivé du contenu au lieu de `st_mtime` · corriger le tableau §5 ou retirer le ratio · supprimer §6.2 et son cache · corriger le commentaire d'en-tête affirmant faussement que les deux bornes sont lues du canon |
| **Invariants à tester** | **I5, les deux branches** — le test existant ne couvre que « jamais ledgerable » ; il faut un second test avec une fixture **antérieure à `applies_from`**, démontré rouge avant d'être vert |
| **Livrable de mesure obligatoire** | le nombre d'`OVERCLAIM` bloquants nouvellement issus des 148 `HISTORICAL_VALID` après réparation de GCG-36 |
| **Indépendance requise** | A1 pour l'exécution ; **relecture croisée obligatoire du tableau §5**, qu'une relecture par l'auteur a déjà laissé passer faux — puis corrigé faux une seconde fois |
| **Condition d'arrêt** | le test I5 « ancienneté » est vert après avoir été démontré rouge, et le nombre de nouveaux bloquants est publié. **Échec** si la réparation de GCG-36 fait apparaître des `OVERCLAIM` dont la revendication est en réalité soutenue : le prédicat serait alors trop large et la question remonte à D5 |

Rien dans cette séquence n'autorise le ledger, le Migration Engine ou le câblage
CI. Ils restent bloqués jusqu'à R-6 inclus, pour la raison donnée en `03` §4.1 :
enregistrer des dispositions contre des classifications provisoires produirait
exactement la dette que le modèle prétend gouverner.

---

## R-0 — Statuer sur la certification v1.1 publiée
**Priorité P0 · dépend de R-A pour sa preuve · ne doit pas attendre le modèle**

| | |
|---|---|
| **Objectif unique** | établir si le `PASS_ADVERSARIAL` de `2026-07-30_0500` est dérivable de `2026-07-30_0100`, et en tirer la conséquence sur `certification_status` |
| **Décisions préalables** | aucune. **Dépendance de preuve** : R-A doit fermer GCG-36 d'abord, faute de quoi le P0 repose sur une classification qu'un renommage suffit à faire disparaître |
| **Findings fermés** | GCG-26, GCG-27 |
| **Invariants à tester** | I5 (`OVERCLAIM` jamais ledgerable, jamais adouci par l'ancienneté) ; la primauté d'`OVERCLAIM` sur la lecture historique |
| **Indépendance requise** | **A2 avec acteur réellement distinct.** Le sujet est une certification publiée ; l'agent qui a produit le constat ne peut pas arbitrer seul son effet sur une revendication publique |
| **Condition d'arrêt** | soit une **attestation dérivée** avec lien vérifiable vers le run source est produite, soit la revendication est retirée et `certification_status` révisé. Le run s'arrête aussi en **échec** si la dérivabilité ne peut être ni établie ni réfutée : dans ce cas il enregistre une non-conformité actuelle non reconstructible et **ne referme rien** |
| **Interdits reconduits** | fabriquer un bloc adverse ; rétrograder un niveau pour obtenir le vert ; traiter la mutation post-clôture comme de la dette |

---

## R-1 — Établir la préséance entre statut déclaré et classification dérivée
**Priorité P1 · dépend de R-2 et R-3**

| | |
|---|---|
| **Objectif unique** | répondre à D4 : quelle règle de préséance entre `certification_status` (déclaré, par sujet) et une catégorie GCG (dérivée, par couple *(artefact, règle)*) ? |
| **Décisions préalables** | R-2, R-3 — les trois apports propres de GCG dépendent tous de la fenêtre de dette |
| **Findings fermés** | GCG-11, GCG-34 ; oriente GCG-12, GCG-35 |
| **Invariants à tester** | **I4** — la règle de préséance retenue ne doit jamais permettre de dériver une certification d'un verdict de conformité. Un test doit échouer si une catégorie GCG suffit à établir un `certification_status` |
| **Livrable obligatoire** | **l'inventaire des artefacts en divergence effective** : combien de runs reçoivent aujourd'hui un verdict bloquant sous un vocabulaire et non bloquant sous l'autre. Zéro est un résultat recevable ; il doit être mesuré, pas supposé |
| **Indépendance requise** | subagent en contexte isolé, mandat : construire un artefact que la règle de préséance retenue classe **moins sévèrement** que l'un des deux vocabulaires pris seul |
| **Condition d'arrêt** | la règle de préséance est écrite au canon **et** l'inventaire de divergence est publié **et** le subagent n'a pas trouvé d'artefact affaibli par la règle. **Échec** si la règle retenue est moins stricte que le maximum des deux vocabulaires sur un artefact réel |

> **Condition d'arrêt réécrite (RA-F-G).** La version initiale exigeait un
> mapping exhaustif et déclarait l'échec *« si une catégorie ne peut être ni
> mappée ni justifiée »*. « Justifiée comme apport propre » est toujours
> disponible à un agent compétent : aucun critère indépendant, aucun
> falsificateur, aucun artefact exigé. **Le seul run capable d'annuler les huit
> autres avait une condition d'arrêt infalsifiable.** La version ci-dessus exige
> une mesure et un adversaire.

---

## R-2 — Établir une coordonnée attestée, ou constater qu'il n'y en a pas
**Priorité P0 · aucune dépendance de modèle · parallélisable avec R-3**

| | |
|---|---|
| **Objectif unique** | répondre à D1 : définir la coordonnée d'un artefact et **mesurer l'effet du changement avant de décider** |
| **Décisions préalables** | aucune |
| **Findings fermés** | GCG-02, GCG-10, GCG-13 |
| **Invariants à tester** | I8 — dont l'énoncé doit être amendé pour distinguer **frontière normative** (déclarée) et **fait sur un artefact** (dérivé). C'est le point de divergence V1 : le run doit trancher, pas hériter |
| **Livrable de mesure obligatoire** | le nombre exact de reclassements sur les 164 runs, **publié avant la décision**, avec la liste des artefacts qui traversent la frontière et dans quel sens |
| **Indépendance requise** | subagent en contexte isolé, mandat : **produire un artefact dont l'auteur contrôle la coordonnée retenue** |
| **Condition d'arrêt, réécrite** | la coordonnée retenue est **hors d'atteinte de l'auteur de l'artefact**, démontré par l'échec du mandat adverse ci-dessus. **Échec explicite et attendu** si la coordonnée retenue reste réglable par l'auteur (`git commit --date`, `GIT_COMMITTER_DATE`, réécriture d'historique) : le run doit alors **déclarer qu'il n'a produit qu'une détection**, jamais qu'il a fermé D1 |

> **Condition d'arrêt réécrite (RA-F-D).** La version initiale déclarait l'échec
> *« si aucune coordonnée non choisie n'est disponible »* — sortie
> **inatteignable** par les options que je recommandais alors (A et B, toutes
> deux fondées sur l'historique git), puisqu'elles produisent bien une
> coordonnée, simplement pas une coordonnée attestée. Le run aurait rapporté un
> succès avec le concept toujours cassé. Le critère porte désormais sur
> l'**inatteignabilité par l'auteur**, qui est mesurable et falsifiable.

---

## R-3 — Attester l'immuabilité, ou restreindre le périmètre
**Priorité P0 · aucune dépendance de modèle · parallélisable avec R-2**

| | |
|---|---|
| **Objectif unique** | répondre à D2 : rendre `immutable` vérifiable, ou restreindre explicitement le modèle |
| **Décisions préalables** | aucune |
| **Findings fermés** | GCG-01, GCG-21, GCG-17 (superseded), GCG-35 partiellement |
| **Invariants à tester** | le mode dégradé de §3.6 : un test doit démontrer qu'une population non attestée **perd** les catégories historiques, et non qu'elle les conserve par déclaration |
| **Livrable de mesure obligatoire** | la liste des 14 closeouts mutés (sur 157 suivis), avec pour chacun la nature de la mutation : correction de forme, écriture de verdict, autre. `b9084e2` est déjà instruit par R-0 |
| **Indépendance requise** | subagent en contexte isolé, mandat : **muter un closeout clos sans que le mécanisme retenu le détecte** |
| **Condition d'arrêt, réécrite** | le mécanisme retenu résiste au mandat adverse ci-dessus. **Échec explicite et attendu** si la mutation passe — notamment par réécriture d'historique, l'historique de ce dépôt n'étant pas signé (243 commits sur 244 en `%G? = N`). Le run doit alors déclarer qu'il n'a produit qu'une **détection** et remonter la question du substrat |

> **Condition d'arrêt réécrite (RA-F-D).** Même défaut que R-2 : la sortie en
> échec (*« si aucune population ne peut satisfaire la propriété »*) était
> inatteignable par l'option que je recommandais (dérivation de l'historique
> git), qui détecte les mutations connues sans établir l'immuabilité. Le critère
> porte désormais sur la résistance à une tentative de contournement.

---

## R-4 — Déclarer les deux bornes au canon
**Priorité P1 · dépend de R-2 et R-3**

| | |
|---|---|
| **Objectif unique** | répondre à D3 : inscrire au canon `applies_from` et `enforcement_effective_from` avec valeur, unité, fuseau et **inclusivité borne par borne** |
| **Décisions préalables** | R-2 (quelle horloge), R-3 (quelle population) |
| **Findings fermés** | GCG-09, GCG-08, GCG-18, GCG-33 ; rend GCG-12 exécutable |
| **Invariants à tester** | I8 (la frontière est déclarée par le canon) — avec un test qui **échoue si le code porte une borne absente du canon**, ce qui est le défaut actuel ; I10, dont la résolution unique « la plus inclusive » doit être scindée en deux directions |
| **Indépendance requise** | A1 suffit — la décision est de forme. L'exécution touche le canon : revue humaine requise |
| **Condition d'arrêt** | `grep enforcement_effective_from docs/` retourne une déclaration canonique, le commentaire faux de `vbb-governance-compat.py` est corrigé, et le sort de `2026-07-28_2000_m2-bis` est écrit. **Discipline** : décider l'inclusivité **avant** de regarder son effet sur `m2-bis` |

---

## R-5 — Fermer les trois voies de blanchiment
**Priorité P1 · dépend de R-4**

| | |
|---|---|
| **Objectif unique** | répondre à D5, D6 et D7 : le prédicat de revendication, l'ensemble ledgerable, et le sens de l'absence du porteur |
| **Décisions préalables** | R-4 |
| **Findings fermés** | GCG-04, GCG-05, GCG-06, GCG-07, GCG-20 |
| **Invariants à tester** | I2 (anti-blanchiment) — le test actuel ne couvre qu'une direction ; il faut **trois** tests de mutation, un par voie, chacun démontré capable d'échouer avant d'être cru. I5, I6 (les deux branches), I11 |
| **Indépendance requise** | **subagent en contexte isolé, mandat explicitement adverse** : trouver une **cinquième** voie. Un run qui ferme les voies connues et n'en cherche pas d'autre est précisément la réparation défensive que ce chantier surveille |
| **Condition d'arrêt, réécrite** | les trois voies sont fermées **et** un test de mutation par voie a été démontré rouge avant d'être vert **et** le mandat adverse n'a pas trouvé de cinquième voie. **Échec** si une cinquième voie est trouvée : le run enregistre et s'arrête, il ne l'inclut pas dans le même lot |

> **Condition d'arrêt réécrite (RA-F-A).** La version initiale déclarait l'échec
> *« si une quatrième voie est trouvée »*. **Elle était déjà remplie avant
> l'ouverture du run** : la quatrième voie est GCG-36, découverte par la revue
> de cet arbitrage. Elle est traitée en R-A, avant ce run, parce qu'elle ne
> demande aucune décision. R-5 ouvre donc avec quatre voies connues et cherche
> la cinquième — ce qui est le seul sens que la condition puisse avoir.

---

## R-6 — Applicabilité complète et totalité de la classification
**Priorité P1 · dépend de R-5 · dernier avant toute implémentation**

| | |
|---|---|
| **Objectif unique** | implémenter les trois sources d'applicabilité **et** rendre la table des catégories totale, dans le même run |
| **Décisions préalables** | R-2, R-4, R-5 |
| **Findings fermés** | GCG-14, GCG-03, GCG-16 |
| **Invariants à tester** | I9 (un scanner n'est jamais plus permissif que l'enforcer qu'il enveloppe) — avec un test différentiel scanner/enforcer sur toute la population, pas un test de forme. **Totalité** : un test qui échoue si un artefact applicable n'entre dans aucune catégorie |
| **Indépendance requise** | subagent en contexte isolé, mandat : construire un artefact applicable qui n'entre dans aucune catégorie |
| **Condition d'arrêt** | le test différentiel passe sur les 164 runs et le test de totalité est démontré capable d'échouer. **Interdiction stricte** : ne pas corriger GCG-14 seul — voir `03` §3.1, cela remplace un défaut latent par un défaut actif |

---

## R-7 — Instruire le dernier fait en suspens
**Priorité P2 · aucune dépendance de modèle · exécutable à tout moment**

| | |
|---|---|
| **Objectif unique** | établir par mesure le fait que l'arbitrage attend encore, **sans le classer** |
| **Décisions préalables** | aucune |
| **Findings fermés** | GCG-32 (D11) |
| **Contenu** | inspection des 14 findings de `2026-07-28_2200` : les valeurs `confidence`/`state` sont-elles **présentes hors énumération** (réparation de schéma) ou **absentes** (non reconstructible) ? |
| **Invariants à tester** | aucun. Ce run **mesure**, il ne classe pas |
| **Indépendance requise** | A1. Le run ne produit aucune classification |
| **Condition d'arrêt** | le fait est établi et écrit, par citation des 14 entrées. **Échec** si l'inspection ne permet pas de trancher entre présent-hors-énumération et absent : le run enregistre une non-conformité historique non reconstructible plutôt que de qualifier après coup |

> **Réduite après revue (RA-F-I).** La version initiale portait aussi
> l'instruction des 9 dispositions de connaissance de GCG-28, en la différant.
> **La mesure coûtait deux commandes et a été faite dans le run d'arbitrage
> lui-même** : les 9 closeouts ne portent le mot « harvest » qu'en clé de
> frontmatter. Le fait est établi ; seule sa **qualification** en `OVERCLAIM`
> dépend encore de D5, donc de R-5. Différer une mesure bon marché dans un
> chantier dont la thèse est « mesurer avant de décider » était incohérent.

---

## R-8 — Rétablir l'honnêteté documentaire
**Priorité P2 · dépend de R-5 (le jeu d'invariants doit être stable)**

| | |
|---|---|
| **Objectif unique** | recompter la couverture réelle une fois le jeu d'invariants stable |
| **Décisions préalables** | R-5 |
| **Findings fermés** | GCG-23 ; clôture définitive de GCG-22 ouverte par R-A |
| **Contenu** | recompter la couverture **après** stabilisation du jeu d'invariants. **I5 n'est pas couvert** : le test existant construit sa fixture *dans* la fenêtre et n'exerce que « jamais ledgerable » ; sa seconde branche reçoit un porteur en R-A. I6 n'est couvert qu'à moitié. Le porteur d'I4 est tautologique |
| **Invariants à tester** | I4 doit recevoir un porteur non tautologique, ou être déclaré sans porteur |
| **Indépendance requise** | A1, mais **relecture croisée obligatoire du tableau de couverture** : c'est précisément le tableau qu'une relecture par l'auteur a laissé passer faux dans les deux sens |
| **Condition d'arrêt** | chaque ligne du tableau est adossée à un test nommé et exécuté, ou déclarée sans porteur. **Interdit** : publier un nouveau ratio avant que le jeu d'invariants soit stable — retirer le ratio est préférable à en publier un second faux |

---

## R-9 — Décider : ADR 0052, amendement d'ADR 0051, ou abandon
**Priorité P1 · dépend de tout ce qui précède**

| | |
|---|---|
| **Objectif unique** | reprendre le verdict de viabilité de `03` §7 avec les décisions rendues, et statuer |
| **Décisions préalables** | R-A, R-0, R-1 à R-6 |
| **Findings fermés** | clôture du registre, ou report explicite de ce qui reste |
| **Invariants à tester** | l'ensemble, avec le ratio de couverture réel |
| **Indépendance requise** | **A2 avec acteur réellement distinct** (D12). Un ADR de canon certifié par l'agent qui l'a écrit est la configuration que ce chantier combat depuis le début |
| **Condition d'arrêt** | le verdict `REQUIRES_REDESIGN` est révisé en `REPAIRABLE_CORE` — auquel cas l'ADR est rédigeable — ou confirmé, ou remplacé par `DUPLICATES_EXISTING_CANON` si R-1 a conclu à l'absorption. **Échec acceptable** : si R-2 ou R-3 s'est arrêté en échec, R-9 constate que le modèle est sans sujet et le dit |

---

## Runs portés, hors séquence

| Run | Objet | Statut |
|---|---|---|
| **G7** | défaut du hook pre-commit — un run en cours ne peut être committé sans être clos | **différé par décision explicite de l'utilisateur**, run dédié |
| **R3 / R4 / R5** | plan de remédiation du run `1021`, entiers | non planifiés ici |
| **D9 / D10** | questions normatives héritées (campagne d'un run d'arbitrage ; `A2` implique-t-il campagne) | à trancher hors séquence GCG — elles portent sur le canon adverse, pas sur le modèle |
| **D8** | épinglage des constats produits hors run | à instruire ; conditionne la durabilité de ce registre lui-même |

## Ce que la séquence ne promet pas

- Elle ne garantit pas que le modèle survivra. R-2, R-3 et R-9 ont chacun une
  condition d'arrêt en échec qui conclut à l'absence de sujet — et depuis la
  revue, ces sorties sont **atteignables**, ce qu'elles n'étaient pas.
- Elle ne réduit pas la charge d'arbitrage humain : **R-5 peut la doubler**, si
  D5 qualifie les 9 dispositions de connaissance comme des revendications. Le
  fait est désormais établi ; seule la qualification manque.
- Elle ne fournit pas l'acteur A2 distinct que R-0 et R-9 exigent. C'est une
  ressource, pas une étape.
- **Elle n'épingle pas ses propres constats.** GCG-36 est né dans ce run et n'a
  aucune entrée de corpus, parce que la contrainte C3 interdisait d'écrire du
  code et que l'obligation d'épinglage se déclenche sur un closeout déclarant
  des findings `CONFIRMED`. C'est GCG-25 s'appliquant à lui-même, et cela rend
  **D8** plus urgente qu'il n'y paraissait.
