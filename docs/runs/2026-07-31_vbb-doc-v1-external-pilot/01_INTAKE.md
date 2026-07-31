---
run_id: "2026-07-31_vbb-doc-v1-external-pilot"
phase: "01_INTAKE"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "run_artifact"
visibility: "internal"
status: "ready"
tags: [run, audit, documentation, governance, contract]
relations:
  - "docs/DOCUMENT_CONVENTION.md"
  - "tools/vbb-document-convention-lint.py"
  - "../../02_dev/Backbone-know"  # external target — referenced from evidence, not modified here
voie: "STRUCTUREE"
run_id_value: "2026-07-31_vbb-doc-v1-external-pilot"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "pi"
started_at: "2026-07-31T10:45:00Z"
ended_at: null
next_phase: "02_AUDIT"
artifacts_consumed:
  - "docs/DOCUMENT_CONVENTION.md"
  - "tools/vbb-document-convention-lint.py"
artifacts_produced:
  - "01_INTAKE.md"
  - "INTEGRATION_GATE.md"
  - "POC.md"
---

# 01_INTAKE — vbb-doc-v1 external pilot (Backbone Know)

## Demande reçue

> Réalise le premier pilote externe de la convention documentaire vbb-doc-v1
> sur le dépôt Backbone Know. Adopte strictement le point de vue d'un
> mainteneur qui découvre la convention publique, sans utiliser les
> explications historiques ayant conduit à sa création.
>
> Sources autorisées côté Vibe Backbone :
> - docs/DOCUMENT_CONVENTION.md ;
> - la documentation publique directement référencée par ce contrat ;
> - la déclaration d'adoption modèle ;
> - le linter vbb-document-convention-lint.py et son aide publique.
>
> Le pilote doit comporter deux phases (audit avant migration + adoption
> pilote) et produire un verdict obligatoire :
> PILOT_PASS / PILOT_PASS_WITH_REVISIONS / PILOT_FAIL.
> Ne modifie pas Vibe Backbone pendant ce pilote.

## Reformulation

Vérifier si un dépôt tiers peut adopter vbb-doc-v1 sans accompagnement oral,
en deux phases (audit documentaire puis adoption minimale), sur un worktree
isolé de Backbone Know, en classifiant toutes les frictions selon cinq
catégories (PROJECT_SPECIFIC, DOCUMENTATION_GAP, CONTRACT_AMBIGUITY,
LINTER_GAP, V1_BLOCKER) et en produisant un verdict final structuré.

## Scope

### Dans le périmètre

- Lecture seule des sources autorisées VBB listées ci-dessus.
- Création d'un run de coordination dans `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/`
  pour porter le verdict, les findings, l'identity disclosure A2 et les
  artefacts de preuve.
- Création d'un worktree isolé de Backbone Know sur la branche
  `pilot/vbb-doc-v1-external`.
- Phase 1 — inventaire documentaire complet de `docs/` dans Backbone Know
  (structure, types, statuts, métadonnées, tags, visibilité, relations,
  contradictions, ordre de lecture, éléments inclassables) ; cartographie
  Backbone Know ↔ vbb-doc-v1 ; préservation des preuves.
- Phase 2 — adoption minimale sur un périmètre de 5 documents
  représentatifs (public principal, arch/référence, opérationnel,
  expérimental/recherche, historique/déprécié si présent) ; exécution du
  linter sur Backbone Know ; préservation de diff et sorties.
- Classification de chaque friction dans l'une des cinq catégories.
- Réponse explicite aux 8 questions de closeout.
- Verdict final obligatoire (PILOT_PASS / PILOT_PASS_WITH_REVISIONS / PILOT_FAIL).

### Hors périmètre

- Toute modification de Vibe Backbone (canon, contrat, linter, gouvernance,
  skills, distributions).
- Migration aveugle de toute la documentation de Backbone Know ; seulement
  un périmètre représentatif minimal est adopté.
- Levée des blockers `RR-BK-01..06` de l'audit readiness Backbone Know.
- Production d'un `READY` global sur Vibe Backbone ou Backbone Know.
- Toute décision de promotion de vbb-doc-v1 au-delà de v1.0 dans Vibe Backbone.

### Dépendances détectées

- Dépôt cible externe : `/Users/bricesodini/02_dev/Backbone-know` (branche
  `main` au SHA `661b240`).
- Linter canonique : `tools/vbb-document-convention-lint.py` (Vibe Backbone).
- Run historique `2026-07-31_1400_document-convention-v1-stabilization` —
  volontairement non lu pour respecter la consigne "point de vue mainteneur
  qui découvre".
- `docs/AUDIT_STATUS.md` (Vibe Backbone) : `BLOCKED for Backbone Know
  foundation`. Ce pilote n'est pas un déblocage de release mais une
  validation externe du contrat documentaire ; il coexiste avec l'état
  `BLOCKED` sans le contredire.

## Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : sujet canonique publié (`vbb-doc-v1` v1.0) ;
  consommation par un dépôt tiers ; évaluation de la qualité du contrat
  lui-même ; findings à produire peuvent déclencher un run de remédiation
  canonique ; ligne de base de tous les pilotes externes à venir.

## Voie recommandée

- **Voie** : `STRUCTUREE`
- **Justification** : tâche multi-fichiers avec preuves, contrat publié,
  coordination requise, livrable structuré (8 réponses + verdict) ;
  l'aspect audit du contenu (qualité du canon) est inclus dans la
  STRUCTUREE via le POC qui est le pilote lui-même. ADR non requis :
  aucune décision d'architecture n'est prise par ce pilote, il valide
  un contrat existant.

## Handoff vers `02_AUDIT`

- **Entrées à lire pour la phase suivante** :
  - `docs/DOCUMENT_CONVENTION.md` (sources autorisées)
  - `tools/vbb-document-convention-lint.py` (sources autorisées)
  - `evidence/` (artefacts de preuve à constituer pendant l'audit Backbone Know)
- **Points de vigilance** :
  - Ne jamais lire les runs historiques de conception de la convention.
  - Ne jamais modifier Vibe Backbone / le contrat / le linter.
  - Tout constat négatif sur le contrat ou le linter est consigné comme
    finding, pas corrigé.
  - L'identité disclosed A2_DISTINCT_AGENT_PROXY doit être répétée dans
    `07_CLOSEOUT.md`.

## Assurance initiale

- **Gates applicables** : `OTHER — pilote de validation de contrat publié`
  ; suivi par `tools/vbb-gate-check.py` (clause-aware ADR + POC +
  Integration Gate).
- **Checkpoint visé** : `PRE_IMPLEMENTATION` (gate VBB avant audit Backbone
  Know) puis `CLOSEOUT` (gate de fin de run).
- **Implémentation autorisée à l'intake** : `NON`. Aucune modification de
  Vibe Backbone. Les modifications Backbone Know sont confinées au worktree
  `pilot/vbb-doc-v1-external` et explicitement décrites comme adoption
  pilote minimale (pas de migration globale).

## Adversarial level (ADR 0051, M1-03) — post-cutoff required

Déclaré au triage. Voir matrice critique dans
`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.2 ; le sujet consomme un
canon publié et cible un dépôt externe → déclencheur `A2`.

```yaml
adversarial_level:
  level: "A2"
  level_reason: |
    Le pilote évalue la qualité et la suffisance d'un contrat canonique
    publié (vbb-doc-v1 v1.0) sur un dépôt tiers. Les findings produits
    peuvent déclencher un run de remédiation canonique. La matrice critique
    classe ce type de sujet en A2 (canon, contrats publiés, sujets
    touchant d'autres dépôts). Pas d'acteur humain distinct disponible
    dans cette session → A2_DISTINCT_AGENT_PROXY actif.
  contest_register: []
```

**Identity disclosure A2_DISTINCT_AGENT_PROXY** (cf.
`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §4.3 — trois identités publiées) :

```yaml
attacker_identity:
  agent: "pi"
  llm: "MiniMax-M3"
  system_prompt_version: "distributions/pi/SYSTEM.md rev. 2026-07-13"
```

Ces trois identités doivent également figurer dans `07_CLOSEOUT.md`.

Règles fail-closed : non-conflit ; déclencheur `A2` matche niveau déclaré
`A2` ; pas de contest.

## Certification status (post-cutoff)

```yaml
certification_status:
  declared_status: "UNASSESSED_LEGACY"
  transient_reason: null
  bootstrapped_at: null
  bootstrapped_by: null
  migrating_from: null
  migrating_to: null
  migration_plan_ref: null
```

Note : la convention `vbb-doc-v1` v1.0 est publiée comme référence active,
mais le pilote lui-même n'engage aucune certification canonique ; le
verdict reste local au pilote (PILOT_PASS / PILOT_PASS_WITH_REVISIONS /
PILOT_FAIL) jusqu'à un éventuel run de remédiation séparé.

## Notes

- Le pilote produit uniquement des **findings** sur le contrat et le linter ;
  aucune modification canonique. Tout finding de type `CONTRACT_AMBIGUITY`,
  `DOCUMENTATION_GAP`, `LINTER_GAP` ou `V1_BLOCKER` est à traiter dans un
  run de remédiation séparé (cf. consigne utilisateur).
- L'identité disclosed A2_DISTINCT_AGENT_PROXY doit être répétée dans
  `07_CLOSEOUT.md` pour conformité `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §4.3.
- Le périmètre Backbone Know sera décrit exhaustivement dans `02_AUDIT.md`.