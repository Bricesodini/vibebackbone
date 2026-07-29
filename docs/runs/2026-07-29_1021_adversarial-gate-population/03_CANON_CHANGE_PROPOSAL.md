---
run_id: "2026-07-29_1021_adversarial-gate-population"
phase: "03_DECISION"
status: "PROPOSED"
agent: "claude-opus-5 (Claude Code)"
created_at: "2026-07-29T09:00:00Z"
human_validated_by: ""
proposed_by: "human (product architect), reframing of run finding G1"
adr_link: "docs/adr/0052-governance-compatibility-gate.md"
---

# Canon Change Proposal — Governance Compatibility Gate (GCG)

## Current Canon

Le canon actuel traite l'évolution de la gouvernance par un unique mécanisme : le
**cutoff**. `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` déclare
`cutoff 2026-07-28_1400`, et `AGENTS.md` / `SYSTEM.md` en dérivent l'obligation
de déclarer un niveau adverse pour les runs post-cutoff.

Le cutoff répond à une seule question : *« cette règle s'applique-t-elle à cet
artefact ? »* Il ne répond pas à celles qui suivent :

- l'artefact non conforme est-il migrable sans fabriquer de preuve ?
- la non-conformité est-elle historique et acceptée, ou actuelle et réparable ?
- une revendication publiée reste-t-elle valide après un changement de canon ?

Aucun document canonique ne définit ces réponses. Aucun outil ne les mesure.

## Problem

Mesure à `6b0daf4` : **2 runs conformes sur 13** dans la population post-cutoff.
Onze artefacts sont non conformes à un canon qu'ils n'ont, pour la plupart, pas
pu respecter — deux d'entre eux ont *construit* l'outillage qui les juge.

Le défaut n'est pas le taux. Le défaut est que le framework n'a **aucune manière
canonique de dire pourquoi**. Il en résulte trois pathologies observées :

1. **Le gate se réduit à sa population la plus favorable.** `--latest` ne mesurait
   qu'un run. Le vert du CI était réel et sans valeur : il portait sur le meilleur
   échantillon d'une population défaillante à 85 %.

2. **La dette et le défaut sont indiscernables.** `2026-07-28_1400` (le validateur
   n'existait pas) et `2026-07-29_0840` (le validateur existait, la règle a
   échoué) produisent le même `exit=2`. Un gate qui ne les distingue pas force à
   choisir entre bloquer tout le travail futur sur un passé irréparable, ou
   désactiver le gate.

3. **La pression vers la falsification est structurelle.** Sans catégorie pour
   « non conforme et non reconstructible », la seule façon d'obtenir le vert est
   d'écrire un bloc de preuve qui n'a pas d'antécédent, ou de rétrograder un
   niveau. Le canon actuel rend le mensonge plus accessible que la vérité.

Une évolution de gouvernance rend aujourd'hui l'historique **automatiquement
faux**. C'est un défaut de conception du canon, pas des artefacts.

## Proposed Canon

Ajouter un **sixième pilier de gouvernance** : la compatibilité de gouvernance.

### Principe canonique

> Une évolution de la gouvernance ne rend jamais automatiquement l'historique
> faux. Le framework distingue explicitement les artefacts historiquement
> valides, les migrations déterministes possibles, les non-conformités
> historiques et les preuves non reconstructibles. Toute migration préserve
> l'intégrité historique et ne fabrique jamais de preuve nouvelle.

### Classification — six catégories

Chaque artefact soumis à une règle datée reçoit exactement une catégorie :

| Catégorie | Sens | Bloquant |
|---|---|---|
| `CURRENT` | conforme au canon actuel | non |
| `HISTORICAL_VALID` | antérieur au cutoff de la règle ; conforme au canon qui lui était applicable | non |
| `MIGRATION_AVAILABLE` | migration déterministe possible depuis les artefacts contemporains, sans inventer de preuve | non, mais compté |
| `HISTORICAL_NONCOMPLIANCE` | applicable mais non respecté, preuve non reconstructible ; dette enregistrée | non, mais compté et visible |
| `CURRENT_NONCOMPLIANCE` | artefact postérieur à l'outillage, règle applicable, échec réel et réparable maintenant | **oui** |
| `OVERCLAIM` | revendique un résultat positif (PASS, CERTIFIED) sans structure validable | **oui, immédiat** |
| `UNKNOWN` | provenance ou compatibilité indéterminable | **oui, jusqu'à décision humaine** |

Les deux dernières lignes sont des ajouts au périmètre initialement proposé.
Leur justification :

- **`CURRENT_NONCOMPLIANCE`** — sans elle, tout défaut actuel peut se ranger sous
  la dette historique. La catégorie qui absout devient la catégorie par défaut, et
  GCG se transforme en machine à blanchir la dette. La frontière est objective :
  l'artefact est-il postérieur à l'existence de l'outil qui le juge ?

- **`OVERCLAIM`** — une omission est inerte ; une revendication fausse est active.
  `2026-07-30_0500_final-publication-of-v1.1-certification` déclare
  `adversarial_status: PASS_ADVERSARIAL` et `certification_status: CERTIFIED` sans
  bloc validable. Classer cela en `UNKNOWN` le mettrait dans une file d'attente
  d'audit ; cela doit bloquer immédiatement. `OVERCLAIM` est la seule catégorie
  qui **ne peut jamais être migrée** : elle se résout par retrait de la
  revendication, ou par production d'une attestation dérivée vérifiable.

### Migration — ce qui est autorisé et ce qui ne l'est pas

Une migration **peut** : déplacer une information, convertir un format, compléter
un champ déductible sans ambiguïté depuis un artefact contemporain.

Une migration **ne peut jamais** : inventer un résultat, modifier une
certification passée, changer un niveau de gouvernance pour faire passer un gate.

Sources interdites pour toute migration : la mémoire de l'agent, l'inférence, les
artefacts postérieurs au run migré, l'outillage qui n'existait pas à sa date.

### Verdict à trois lectures orthogonales

Le gate cesse de produire un booléen. Il produit trois mesures qu'aucune règle ne
permet de dériver l'une de l'autre :

```
conformité actuelle    : N artefacts CURRENT sur M applicables
dette historique       : N artefacts HISTORICAL_NONCOMPLIANCE, enregistrés
certification obtenue  : liste explicite des sujets réellement CERTIFIED
```

Un vert de conformité ne vaut pas certification. Une dette enregistrée ne vaut pas
conformité. Une certification passée ne se déduit pas d'un gate vert.

### Cutoff — obligation de déclaration

Toute nouvelle règle de gouvernance déclare sa `version` et sa `date d'entrée en
vigueur`. Une règle sans cutoff déclaré est inapplicable rétroactivement : elle ne
peut produire que `CURRENT` ou `CURRENT_NONCOMPLIANCE` sur les artefacts
postérieurs à sa publication, et `HISTORICAL_VALID` sur tous les autres.

### Points d'intervention

1. au démarrage d'une session gouvernée — via un **acte de compatibilité mis en
   cache**, invalidé par changement de version de canon ou apparition de runs ;
2. après toute évolution du canon ;
3. avant toute certification `READY` lorsqu'une migration est en attente.

## Benefits

1. Le framework peut faire évoluer sa gouvernance sans invalider ni réécrire son
   patrimoine documentaire — capacité aujourd'hui absente.
2. La dette devient un objet compté et visible plutôt qu'un échec indistinct.
3. La falsification cesse d'être la voie la plus courte vers le vert :
   `HISTORICAL_NONCOMPLIANCE` est toujours moins coûteux que fabriquer une preuve.
4. Le verdict cesse de pouvoir être satisfait par relabellisation ou par choix de
   population.
5. `OVERCLAIM` rend détectable la classe de défaut la plus dangereuse — celle où
   une surface publie un résultat positif que rien ne soutient.

## Risks

1. **La dette devient confortable.** Si `HISTORICAL_NONCOMPLIANCE` est non
   bloquante, rien ne pousse à la résorber. *Mitigation* : la dette est comptée,
   affichée au dashboard, et le passage à `READY` global exige qu'elle soit
   explicitement acceptée par une décision humaine tracée — jamais par défaut.

2. **La frontière historique/actuel se déplace avec le temps.** Ce qui est
   `CURRENT_NONCOMPLIANCE` aujourd'hui deviendra tentant à reclasser en dette
   demain. *Mitigation* : la frontière est ancrée sur une donnée objective et
   immuable — la date d'existence de l'outil, pas la date du jour.

3. **Coût de démarrage de session.** Un scan complet est incompatible avec la
   latence d'une session. *Mitigation* : acte mis en cache, invalidé par version
   de canon et par apparition de runs, jamais recalculé sans raison.

4. **Complexité ajoutée au canon.** Six catégories là où il y avait un booléen.
   *Mitigation* : la classification est produite par un outil, pas par le jugement
   de l'agent ; l'agent lit un acte, il ne le dérive pas.

5. **Risque de portée.** GCG est décrit sur la dimension adverse, mais s'applique
   à toute règle datée. *Mitigation* : la première implémentation ne livre qu'un
   jeu de règles (adversarial 1.1), l'architecture restant générique. Aucune
   extension à d'autres dimensions n'est autorisée sans nouvelle proposition.

## Decision requested

Adopter GCG comme **pilier de gouvernance** (et non comme outil), avec les six
catégories ci-dessus, dont `CURRENT_NONCOMPLIANCE` et `OVERCLAIM` qui n'étaient
pas dans la proposition initiale.

Cette proposition reste `PROPOSED` jusqu'à validation humaine (Critical Rule 9).
L'implémentation livrée par ce run est **l'instrument de mesure**, pas
l'application du pilier : elle classe et rapporte, elle ne migre rien.
