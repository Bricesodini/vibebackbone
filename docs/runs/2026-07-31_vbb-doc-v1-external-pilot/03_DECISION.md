---
run_id: "2026-07-31_vbb-doc-v1-external-pilot"
phase: "03_DECISION"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "run_artifact"
visibility: "internal"
status: "ready"
tags: [run, audit, documentation, governance, contract]
relations:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "INTEGRATION_GATE.md"
  - "POC.md"
run_id_value: "2026-07-31_vbb-doc-v1-external-pilot"
route: "STRUCTUREE"
adversarial_level: "A2"
attacker_identity:
  agent: "pi"
  llm: "MiniMax-M3"
  system_prompt_version: "distributions/pi/SYSTEM.md rev. 2026-07-13"
  distinct_actor: "A2_DISTINCT_AGENT_PROXY"
  external_review_eligibility: "ELIGIBLE"
verdict: "PILOT_PASS_WITH_REVISIONS"
started_at: "2026-07-31T10:45:00Z"
ended_at: "2026-07-31T11:30:00Z"
agent: "pi"
next_phase: "05_EXECUTION"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
artifacts_consumed:
  - "02_AUDIT.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — vbb-doc-v1 external pilot (Backbone Know)

## Verdict

**`PILOT_PASS_WITH_REVISIONS`**

L'adoption de `vbb-doc-v1` v1.0 est **possible sans accompagnement oral**
sur un périmètre minimal mais représentatif. Le linter produit
**`VBB-DOC-V1: PASS`** après une seule correction triviale. Trois
révisions sont **bloquantes pour la Release Candidate** d'une
éventuelle v1.1 ; quatre améliorations peuvent attendre une version
ultérieure.

## Justification

L'inventaire Phase 1 a identifié 10 frictions potentielles ; le pilote
Phase 2 en a rencontré **une seule** (F-PH2-01, triviale). Le verdict
n'est pas `PILOT_PASS` parce que les frictions F-PH1-07 et F-PH1-10
(et dans une moindre mesure F-PH1-02) rendent le passage à l'échelle
incertain et constituent des obstacles **structurels** à une adoption
fiable sur des dépôts de la taille de Backbone Know.

Le verdict n'est pas `PILOT_FAIL` parce que le contrat, le linter et le
mécanisme d'extension `project:` suffisent pour le périmètre minimal
demandé par la consigne du pilote.

## Décomposition des révisions

### Bloquantes pour la Release Candidate (RC v1.1)

Ces révisions empêchent une adoption fiable sur des dépôts de taille
moyenne ou grande. Elles doivent être traitées avant qu'une RC v1.1 ne
soit publiée.

| ID | Friction | Résolution proposée | Justification RC |
|---|---|---|---|
| **F-PH1-10** | Pas de mécanisme d'adoption progressive / waivers pour grands dépôts | Permettre une déclaration d'adoption **multi-roots** où chaque root peut être adoptée indépendamment, OU introduire un concept de `waivers:` dans `.vbb/document-convention.yaml` listant des fichiers explicitement exclus temporairement avec une raison | Sans ce mécanisme, l'ajout d'un seul nouveau fichier non conforme casse l'adoption globale, ce qui est incompatible avec un cycle de release normal. Friction **structurelle**. |
| **F-PH1-02** | Statuts composés BK (`FROZEN`, `generated`, `closed`, `planned`, `completed_design_only`, `normative`, `frozen_with_open_questions`) — aucun mécanisme d'extension de domaine | Introduire dans §4 un mécanisme explicite de **status extension namespacée** (ex : `project:status:closed`, `project:status:frozen-with-open-questions`) ET clarifier que `frozen` du contrat ≠ `FROZEN` d'un projet tiers ; OU introduire un domaine `extended` qui liste les statuts autorisés en extension | Sans ce mécanisme, les projets tiers doivent choisir entre dégrader leur vocabulaire (perte d'information) ou être non conformes. Friction **structurelle**. |
| **F-PH1-07** | Linter ne signale pas les docs hors-scope qui devraient être adoptés | Ajouter une commande `vbb-document-convention-lint.py --suggest-scope <root>` qui scanne le dépôt, identifie les `.md` non adoptés potentiellement conformes, et propose une extension de scope | Sans cette guidance, un mainteneur ne sait pas s'il a oublié des fichiers ; l'adoption reste silencieusement partielle. Friction **d'expérience mainteneur** mais corrélée à F-PH1-10. |

### Améliorations post-RC (peuvent attendre v1.2 ou ultérieure)

| ID | Friction | Résolution proposée |
|---|---|---|
| F-PH1-01 | Statut BK uppercase vs lowercase contrat | Préciser dans §4 que le linter normalise la casse et que les frontmatters doivent utiliser la casse lowercase du tableau |
| F-PH1-06 | Ordre de lecture §7 non imposé techniquement | Ajouter une commande `vbb-doc-v1-read-order <root>` qui imprime l'ordre canonique en vérifiant que les fichiers existent et sont adoptés |
| F-PH1-08 | Linter ne vérifie pas l'existence des fichiers dans `relations` | Ajouter un mode `--strict` qui vérifie l'existence des fichiers listés dans `relations` |
| F-PH1-09 | Linter ne vérifie pas la cohérence interne du scope | Ajouter un check : toute relation vers un fichier `.md` doit pointer vers un fichier adopté |

## Frictions effectivement rencontrées (corrigées)

| ID | Friction | Catégorie | Correction |
|---|---|---|---|
| F-PH2-01 | Tag `research` non canonique | PROJECT_SPECIFIC | `project:domain:research` |

## Frictions non retenues comme findings

Les éléments suivants ne sont **pas** des findings du pilote — ce sont
des extensions valides du mécanisme `project:` du contrat §5 :

- Vocabulaire `context_role` (15+ valeurs) → `tags: [project:role:<rôle>]`
- Vocabulaire `phase` (cycle projet BK) → `tags: [project:phase:<cycle>]`
- Vocabulaire `kind`, `audit_type`, `poc_id`, `increment` → `tags: [project:kind:...]`, etc.

Le contrat §5 prévoit explicitement les extensions namespacées et le
pilote valide leur utilisation.

## Handoff vers `05_EXECUTION`

Le journal d'exécution est dans [`05_EXECUTION.md`](05_EXECUTION.md).
Le pilote a effectivement été exécuté en Phase 2 avant la rédaction
de cet artefact (le pilote est la POC elle-même ; le closeout documente
a posteriori ce qui a été fait).

## Handoff vers `07_CLOSEOUT`

Les 8 questions de closeout sont répondues dans
[`07_CLOSEOUT.md`](07_CLOSEOUT.md). L'identity disclosure
A2_DISTINCT_AGENT_PROXY y est répétée.

## ADR / canon

Aucune décision d'architecture n'est prise par ce pilote ; aucun ADR
n'est requis. Tous les findings sont destinés à un **run de remédiation
séparé** conformément à la consigne de l'utilisateur.

## Note sur l'A2

Le pilote évalue un contrat canonique publié et cible un dépôt externe ;
le niveau adversarial déclaré est `A2` et l'absence d'acteur humain
distinct a imposé le mode `A2_DISTINCT_AGENT_PROXY`. Les trois
identités (agent, llm, system_prompt_version) sont publiées dans
`01_INTAKE.md`, `02_AUDIT.md`, ici, et seront répétées dans
`07_CLOSEOUT.md`. La review trimestrielle externe (≤ 90 jours) est
**non applicable** à ce pilote isolé (le pilote ne publie pas de canon
ni de release ; il consigne des findings).