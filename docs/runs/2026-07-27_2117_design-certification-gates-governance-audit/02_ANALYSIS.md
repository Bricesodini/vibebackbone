---
run_id: "2026-07-27_2117_design-certification-gates-governance-audit"
phase: "02_AUDIT"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-27T19:18:37Z"
ended_at: "2026-07-27T19:35:55Z"
revised_at: "2026-07-27T19:35:55Z"
next_phase: "03_OPTIONS"
artifacts_consumed:
  - "01_SCOPE.md"
  - "INTEGRATION_GATE.md"
  - "docs/PILOTAGE.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md"
  - "docs/adr/0043-domain-verdict-runtime-status-orthogonality.md"
  - "prompts/canonical/02-p-vbb-audit.md"
  - "prompts/canonical/06-p-vbb-review.md"
  - "prompts/canonical/07-p-vbb-closeout.md"
  - "docs/templates/"
artifacts_produced:
  - "02_ANALYSIS.md"
---

# 02_ANALYSIS — Design and certification assurance

## Résumé exécutif

La gouvernance actuelle n'est pas incorrecte : ADR 0043 permet déjà qu'un
worker s'exécute correctement tout en concluant négativement sur son sujet.
Mais elle agrège encore sous `READY/PARTIAL/BLOCKED/UNKNOWN`, `PASS/FAIL` ou un
champ `verdict` des états d'assurance différents. Cette agrégation rend
possible l'interprétation erronée « produit instable » lorsqu'un gate échoue
uniquement sur la preuve documentaire.

Le besoin est donc démontré, mais il ne justifie ni deux nouvelles phases ni
deux vocabulaires incompatibles. Il justifie une **qualification additive du
gate et des dimensions d'assurance**, avec maintien du verdict historique.

## Méthode et discipline de preuve

- Lecture des autorités et contrats actifs de VBB.
- Comparaison avec ADR 0043, qui borne déjà la relation verdict/statut.
- Analyse des surfaces de gate, review, closeout et `FINAL_STATUS`.
- Mise à l'épreuve sur le scénario utilisateur.
- Classification séparée des faits vérifiés, inférences et inconnues.

Le scénario Backbone Know est un cas d'usage fourni par l'utilisateur. Ses
artefacts complets ne sont pas dans le corpus audité ; il illustre le problème
mais ne sert pas de preuve unique de conformité d'un projet.

## État actuel observé

| Surface | État vérifié | Conséquence |
|---|---|---|
| ADR 0043 | Statut d'exécution et verdict de domaine sont orthogonaux. | Un audit exécuté avec succès peut conclure négativement. |
| `PILOTAGE.md` | Cascade globale `READY/PARTIAL/BLOCKED/UNKNOWN`; `FINAL_STATUS.verdict` décrit le worker. | Aucun axe standard ne dit quelle assurance a échoué. |
| Prompt AUDIT | Agrège les findings en un verdict global. | Une lacune de preuve et une lacune de conception peuvent produire le même résultat. |
| Prompt REVIEW | Une checklist générique produit un verdict unique. | La revue ne doit pas obligatoirement séparer fermeture du comportement et certification de preuve. |
| `INTEGRATION_GATE` | ADR, POC et autorisation de démarrer sont distingués. | Un précédent existe pour exposer plusieurs préconditions sans créer de phase. |
| Knowledge governance | Delivery et knowledge sont deux boucles; le Harvest appartient au closeout. | Le Harvest ne peut pas être un prérequis de conception antérieur à l'implémentation. |
| Protocol 01–07 | Sept phases stables; review est la phase 06 et closeout la phase 07. | Une nouvelle machine de phases serait cassante et inutile. |

## Findings

### GATE-001 — `FAIL` ne porte pas la classe d'assurance

- **Sévérité**: P1
- **Type**: OBSERVATION
- **Niveau de preuve**: VERIFIED_FINDING
- **Trace**:
  - **Observation**: les prompts et templates actifs acceptent un verdict
    agrégé.
  - **Signal**: aucune clé canonique ne distingue fermeture du comportement et
    certification documentaire.
  - **Vérification**: recherche ciblée dans `PILOTAGE.md`,
    `AGENTIC_RUN_PROTOCOL.md`, les prompts 02/06/07 et les templates.
  - **Finding**: le consommateur ne peut pas déterminer mécaniquement si un
    échec rouvre la conception.
- **Décision proposée**: MITIGATE.

### GATE-002 — ADR 0043 est nécessaire mais insuffisant

- **Sévérité**: P2
- **Type**: OBSERVATION
- **Niveau de preuve**: VERIFIED_FINDING
- **Trace**:
  - **Observation**: ADR 0043 sépare domaine et runtime.
  - **Signal**: Design et certification sont deux conclusions à l'intérieur du
    domaine, non un statut runtime.
  - **Vérification**: texte de la décision et alternative de schéma différée.
  - **Finding**: la proposition complète ADR 0043; elle ne doit ni le remplacer
    ni remapper implicitement verdict et statut.
- **Décision proposée**: ACCEPTED comme contrainte de conception.

### GATE-003 — Un `Design PASS` peut être stable sans certification complète

- **Sévérité**: P1
- **Type**: OBSERVATION
- **Niveau de preuve**: VERIFIED_FINDING
- **Trace**:
  - **Observation**: les autorités séparent déjà décision, plan, review,
    closeout, preuve et Knowledge Harvest.
  - **Signal**: leurs critères de fermeture ne portent pas sur le même objet.
  - **Vérification**: protocole 01–07, prompts 03/06/07 et gouvernance de
    connaissance.
  - **Finding**: l'état « comportement fermé, preuve non certifiée » est valide
    et doit être représentable sans contradiction.
- **Décision proposée**: MITIGATE par états orthogonaux.

### GATE-004 — Une ambiguïté documentaire peut néanmoins rouvrir le Design

- **Sévérité**: P1
- **Type**: OBSERVATION
- **Niveau de preuve**: VERIFIED_FINDING
- **Trace**:
  - **Observation**: une contradiction de contrat, transaction, concurrence ou
    historique est exprimée dans un document mais affecte le comportement.
  - **Signal**: classer tout défaut documentaire comme certification serait un
    faux cloisonnement.
  - **Vérification**: responsabilités des ADR, contrats et décisions dans les
    autorités actives.
  - **Finding**: la classification doit dépendre de l'objet affecté, pas du
    fichier où l'écart est découvert.
- **Décision proposée**: reclassification obligatoire vers Design lorsque
  l'écart change ou rend ambigu le comportement observable.

### GATE-005 — L'autorisation d'implémentation est une décision distincte

- **Sévérité**: P1
- **Type**: OBSERVATION
- **Niveau de preuve**: VERIFIED_FINDING
- **Trace**:
  - **Observation**: le gate actuel combine ADR, POC et linkage pour produire
    `can_code_start`.
  - **Signal**: deux PASS d'assurance ne couvrent pas nécessairement sécurité,
    readiness MVP, POC ou décision humaine.
  - **Vérification**: `vbb-gate-check.py`, `PILOTAGE.md` et règles Core.
  - **Finding**: `implementation_authorized` ne doit jamais être inféré du seul
    couple Design/Certification.
- **Décision proposée**: conserver un état d'autorisation explicite avec raisons.

### GATE-006 — Le Knowledge Harvest n'appartient pas au Design Gate

- **Sévérité**: P1
- **Type**: OBSERVATION
- **Niveau de preuve**: VERIFIED_FINDING
- **Trace**:
  - **Observation**: le Harvest intervient après la delivery dans
    `07_CLOSEOUT`.
  - **Signal**: il ne ferme aucun comportement observable et n'est pas
    disponible avant implémentation.
  - **Vérification**: `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` et protocole 01–07.
  - **Finding**: il est un contrôle transverse de closeout; la promotion de
    connaissance possède ensuite ses propres gates.
- **Décision proposée**: ne pas créer un troisième gate de conception; exposer
  son résultat séparément dans le closeout.

### GATE-007 — Une migration substitutive casserait les consommateurs

- **Sévérité**: P1
- **Type**: OBSERVATION
- **Niveau de preuve**: VERIFIED_FINDING
- **Trace**:
  - **Observation**: les outils et artefacts historiques consomment des champs
    `verdict` ou `status` existants.
  - **Signal**: renommer `FAIL` en `DESIGN_FAIL` ou supprimer le verdict
    agrégé modifie les parseurs et l'interprétation historique.
  - **Vérification**: templates, dashboard, protocoles et ADR 0043.
  - **Finding**: seule une extension versionnée et rétrocompatible est sûre.
- **Décision proposée**: migration additive, cutoff futur, fallback legacy.

## Sémantique recommandée

Conserver `PASS/FAIL` ou le vocabulaire possédé par le gate, mais toujours
qualifier **le gate qui parle** :

```yaml
gate_result:
  gate_id: "design-contract-closure"
  family: "DESIGN"
  verdict: "PASS"
  assurance_state: "CERTIFIED"
  blockers: []
```

Un gate de certification utilise la même structure avec
`family: CERTIFICATION`. `FAIL` reste ainsi simple et local; il ne signifie
plus implicitement que tout le produit est instable.

États minimaux suggérés pour chaque résultat :

- `PASS`
- `FAIL`
- `NOT_ASSESSED`
- `NOT_APPLICABLE`

`UNKNOWN` peut rester un verdict d'audit lorsque la preuve disponible ne permet
pas de conclure. Il ne doit pas être encodé comme `false`.

## Cycle documentaire

Le cycle proposé par la demande est pertinent mais incomplet s'il place toute
certification avant l'implémentation. Chaque certification doit porter un
`checkpoint`, un `subject` et un `gate_id`. Le cycle robuste est :

```text
Design
→ Design Gate PASS
→ Pre-implementation Certification Gate PASS
→ explicit Implementation Authorization
→ Implementation
→ Delivery/Documentary Certification
→ Closeout + Knowledge Harvest
```

Règle de retour : un finding de certification qui révèle une contradiction
substantive du comportement réouvre le Design Gate. Un finding de preuve,
référence, oracle ou traçabilité reste dans Certification.

Il n'existe pas de scalaire global « certification ». Les résultats sont une
collection append-only par checkpoint :

- `PRE_IMPLEMENTATION` certifie le dossier nécessaire à l'autorisation;
- `POST_IMPLEMENTATION` certifie la preuve de livraison;
- un autre checkpoint doit déclarer son sujet et ses préconditions.

L'agrégat d'un checkpoint est `FAIL` si un gate requis échoue,
`NOT_ASSESSED` si un gate requis manque, `PASS` si tous les gates requis
passent, et `NOT_APPLICABLE` seulement lorsqu'un profil le déclare.

## Revues indépendantes

Deux checklists sont justifiées, sans imposer deux nouvelles phases :

### Revue de Design

- contrat observable complet et non contradictoire;
- invariants, transactions, SQL, concurrence, historique;
- cas limites et états d'erreur;
- décisions ADR applicables;
- absence de choix métier masqué par une formulation documentaire.

### Revue de Certification

- provenance, indépendance et suffisance des preuves;
- oracles reproductibles;
- cohérence et liens entre autorités;
- traçabilité exigences → décisions → preuves;
- références valides et absence de vérité parallèle;
- déclarations de closeout et Knowledge Harvest lorsque la revue porte sur la
  livraison finale.

Une même session indépendante peut exécuter les deux checklists si les deux
verdicts restent séparés et si le reviewer n'est pas l'auteur. Pour les sujets
à risque élevé, deux reviewers distincts restent préférables.

## Knowledge Harvest

Classification :

- **pas Design Gate**;
- **pas gate pré-implémentation autonome**;
- **contrôle obligatoire de closeout**, vérifiable dans la certification finale;
- si une observation devient candidate, elle ouvre la boucle autonome de
  connaissance déjà gouvernée.

Un Harvest absent peut faire échouer la certification du closeout sans invalider
rétroactivement le Design PASS ni le comportement livré.

## Verdict global de l'analyse

**READY** — le besoin, ses frontières et une solution rétrocompatible sont
suffisamment établis pour comparer les options.

## UNKNOWN

- Les parseurs externes non publiés ne sont pas observables.
- Le volume réel de gates consommateurs devra être remesuré dans un futur run.
- Le corpus complet Backbone Know n'est pas disponible dans ce dépôt.
