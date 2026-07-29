---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
adversarial_level: "A2"
scope_id: "GCG-ARB-01"
agent: "claude-opus-5 (Claude Code)"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
adr_link: "docs/adr/0051-adversarial-assurance-dimension.md"
started_at: "2026-07-29T13:50:00Z"
ended_at: null
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/REFERENCE/governance-compatibility-model.md (v2, PROPOSED, lecture seule)"
  - "docs/runs/2026-07-29_1130_gcg-genericity-stress-test/ (S1–S8)"
  - "docs/runs/2026-07-29_1050_gcg-conceptual-model/ (points ouverts)"
  - "docs/runs/2026-07-29_1021_adversarial-gate-population/ (matrice, P0, questions normatives)"
  - "revue indépendante du 2026-07-29 (F1–F12)"
  - "docs/AUDIT_STATUS.md (risques actifs)"
artifacts_produced:
  - "01_INTAKE.md (this file)"
  - "02_FINDINGS_REGISTER.md"
  - "03_DEPENDENCY_AND_ARBITRATION_MAP.md"
  - "04_PLAN.md"
  - "04_INDEPENDENT_ARBITRATION_REVIEW.md"
  - "05_DECISIONS_REQUIRED.md"
  - "05_EXECUTION.md"
  - "06_RESUMPTION_SEQUENCE.md"
  - "07_CLOSEOUT.md"
---

# 01_INTAKE — GCG-ARB-01

## 1. Demande reçue

La revue conceptuelle indépendante du modèle *Governance Compatibility Gate* a
rempli son objectif : elle a révélé des défauts conceptuels, des contradictions
avec le canon, des faiblesses d'implémentation et plusieurs voies potentielles de
blanchiment que l'auteur principal n'avait pas identifiées.

**La prochaine étape n'est pas de produire une v3 ni de corriger les findings un
par un.** Il s'agit d'ouvrir un run d'arbitrage qui détermine, pour chaque
constat, s'il doit être corrigé mécaniquement, tranché normativement, redéfini
conceptuellement, aligné sur un canon existant, abandonné, ou laissé
explicitement ouvert.

Objectif : *transformer un ensemble de critiques en un espace de décisions
cohérent, avant toute tentative de réparation.*

## 2. Contraintes normatives déclarées

| # | Contrainte | Portée |
|---|---|---|
| C1 | **Modèle GCG v2 en lecture seule.** Aucune modification de `docs/REFERENCE/governance-compatibility-model.md`. | tout le run |
| C2 | **Aucun nouveau concept ajouté au modèle.** | tout le run |
| C3 | **Aucun correctif de code produit.** Ni v3, ni ledger, ni Migration Engine, ni câblage CI. | tout le run |
| C4 | **Aucun finding rétrogradé pour obtenir un état vert.** | tout le run |
| C5 | **Aucun statut historique ni niveau d'assurance attribué sans preuve dérivable.** | tout le run |
| C6 | **Aucune prétention à A2 strict** si le subagent utilise la même famille de modèles. | closeout |
| C7 | **Les divergences agent principal / subagent restent visibles**, non fusionnées. | livrables |
| C8 | **Une CI rouge causée par des constats confirmés ne doit pas être blanchie.** | vérification |
| C9 | Les runs proposés en `06_RESUMPTION_SEQUENCE.md` ne sont **ni ouverts ni exécutés** ici. | livrables |

C1 et C3 sont structurantes. Un défaut identifié ici est **classé et rendu
opposable**, pas réparé. Réparer pendant l'arbitrage produirait exactement le
risque que la mission nomme : *une réparation défensive adaptée aux seuls
contre-exemples connus*.

C5 vaut aussi pour ce run lui-même : l'écart mesuré entre ma propre mesure et
celle du subagent (§`02` GCG-10) est enregistré comme divergence, pas résolu par
choix d'un chiffre.

## 3. Sources du registre

Quatre sources, aucune fusionnée :

| Source | Origine | Constats |
|---|---|---|
| **ST** | `2026-07-29_1130_gcg-genericity-stress-test` | S1–S8 |
| **IR** | revue indépendante du 2026-07-29 (subagent isolé) | F1–F12 |
| **R1021** | `2026-07-29_1021_adversarial-gate-population` §points ouverts | 3 questions normatives, P0, G7, G8, R3–R5 |
| **R1050** | `2026-07-29_1050_gcg-conceptual-model` §points ouverts | invariants sans porteur, G9 |
| **AUD** | `docs/AUDIT_STATUS.md` §Active risks | F8 (provenance temporelle), OPEN |

Deux collisions d'identifiants existent entre ces sources — `IR-F8` (inclusivité
de borne) et `AUD-F8` (provenance temporelle) désignent des choses différentes.
C'est la première raison de renuméroter dans un espace unique `GCG-nn`.

## 4. Méthode

1. Registre unique, un identifiant stable par constat, source conservée.
2. Taxonomie explicite par nature — **et déclaration des cas où elle ne
   discrimine pas**, plutôt qu'un rangement mécanique.
3. Graphe de dépendances : ce qui bloque quoi, ce qui disparaît sous une même
   décision, ce qui ne peut pas être réparé tant qu'une décision est ouverte.
4. Séparation explicite décision normative / correction technique, avec l'axe
   utile : **qui peut clore** (agent, canon, humain, acteur externe).
5. Verdict de viabilité **dérivé** du registre et du graphe, avec sa condition
   de bascule déclarée.
6. Séquence de reprise, non exécutée.

Une revue indépendante en contexte isolé examine la **classification et
l'arbitrage**, pas le modèle. Son mandat exclut de refaire l'audit général et de
défendre le modèle.

## 5. Baseline mesurée avant l'arbitrage

`python tools/vbb-governance-compat.py --json`, dépôt à `6b0daf4` + branche
`feat/governance-compatibility-gate` (`5d4fe34`) :

```
population_total       : 164
population_applicable  : 15
current_conformance    : 2/15
counts                 : HISTORICAL_VALID 148 · CURRENT_NONCOMPLIANCE 8
                         UNKNOWN 4 · CURRENT 2 · OVERCLAIM 1 · PENDING_LIFECYCLE 1
historical_debt        : 0
certification          : NOT_DERIVABLE_FROM_THIS_GATE
verdict                : FAIL
```

Ce verdict rouge est un constat confirmé. C8 interdit de le blanchir : ce run ne
doit ni le faire passer au vert, ni le faire disparaître de la mesure.

## 6. Niveau adverse et convention d'identité

`A2` — le sujet est le canon de gouvernance et l'arbitrage de findings qui
mettent en cause une certification publiée.

**Convention d'identité déclarée** (constat GCG-10 : deux horloges coexistent).
L'identité `2026-07-29_1550` est en **heure locale Europe/Paris**, comme les
runs `0840`, `1021`, `1050`, `1130` ; `started_at: 2026-07-29T13:50:00Z` est le
même instant en UTC. Aucune antidatation ni postdatation : l'heure locale au
moment de l'ouverture était 15:50 CEST. La déclaration est faite parce que le
registre contient un constat sur l'ambiguïté de cette convention, et qu'un run
d'arbitrage ne peut pas exploiter l'ambiguïté qu'il arbitre.
