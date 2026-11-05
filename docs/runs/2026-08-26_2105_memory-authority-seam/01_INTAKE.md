---
run_id: "2026-08-26_2105_memory-authority-seam"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-26T21:05:00Z"
ended_at: "2026-08-26T21:20:00Z"
next_phase: "03_DECISION"
artifacts_consumed:
  - "AGENTS.md"
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "docs/DISTRIBUTIONS.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "docs/adr/0055-memory-authority-seam.md"
---

# 01_INTAKE — memory-authority-seam

## Demande reçue

> « ce qui a été fait avec backbone memory c'est pour la gestion des artefacts
> projets en phase de codage pour gérer la production définir canon, Legacy,
> tout cela avec une couche déterministe. il faut de toute façon l'intégrer
> dans vibe backbone »

Complétée par la revue de l'agent de long cours : ne pas coder l'intégration
tant que la frontière d'autorité n'est pas écrite et falsifiable ; l'objectif
immédiat est le **contrat que n'importe quelle mémoire devra respecter** pour
habiter VibeBackbone sans créer de vérité parallèle.

## Reformulation

Écrire la frontière d'autorité entre le **canon documentaire de VibeBackbone**
(fichiers versionnés, gates model-free) et une **couche mémoire runtime** —
Backbone Memory étant le premier implémenteur candidat, non le sujet. Le
livrable est un ADR de couture accompagné de ses tests de falsification. Aucune
intégration, aucun code, aucune dépendance introduite.

## Scope

### Dans le périmètre

- La frontière d'autorité : qui décide du statut d'un artefact.
- Les trois invariants : `CANONICAL_MEMORY_IS_DERIVED`, `PROMOTION_IS_A_GATE`,
  `NO_PARALLEL_SEMANTIC_AUTHORITY`.
- Le modèle d'état minimal de la mémoire : `projection`, `candidate`, `working`.
- Le protocole de promotion, défini **avant** tout stockage.
- La table de correspondance avec les dimensions déjà canoniques de VBB
  (statut documentaire, assurance, certification, lifecycle, résultat de gate).
- Les cas adversariaux qui rendent la couture falsifiable.

### Hors périmètre

- Toute intégration de Backbone Memory, tout code, tout schéma de vault.
- La qualification architecturale de Backbone Memory (audit ultérieur, I2).
- La qualification distributionnelle : chemins absolus, store pnpm, portabilité
  (audit distinct, qui ne doit pas bloquer l'expérimentation DSH locale).
- La promotion de DSH en cinquième distribution (décision indépendante).
- La réduction du catalogue de skills du preset DSH (chantier distinct).

### Dépendances détectées

- `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` — supersession et promotion du
  savoir canonique ; la couture doit s'y raccorder, pas la doubler.
- `docs/GATE_ASSURANCE_GOVERNANCE.md` — `FINAL_STATUS` / `ASSURANCE_STATUS`,
  autorisation d'implémentation fail-closed.
- `docs/document-model/` et `.vbb/document-convention.yaml` — Documentary
  Contract v1.0 (ADR 0052, ADR 0054) : source du statut documentaire.
- `docs/DISTRIBUTIONS.md` — règle A : impact sur les distributions actives.

## Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : la décision porte sur l'autorité sémantique du canon
  lui-même. Une couture mal posée produit exactement la faute que la règle
  critique #5 interdit — deux sources de vérité sur le statut d'un artefact de
  production — et cette faute est silencieuse jusqu'à la première contradiction.

## Voie recommandée

- **Voie** : `STRUCTUREE`
- **Justification** : changement structurel de Core, touchant le canon de
  gouvernance et diffusant vers toutes les distributions actives. Plan avant
  modification, ADR obligatoire, décision humaine explicite.

## Handoff vers `03_DECISION`

- **Entrées à lire pour la phase suivante** :
  - `docs/adr/0055-memory-authority-seam.md`
  - `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` §promotion et supersession
  - `docs/GATE_ASSURANCE_GOVERNANCE.md` §statuts orthogonaux
  - `docs/document-model/` — contrat documentaire v1.0
- **Points de vigilance** :
  - Le vocabulaire « canon / legacy / production » ne doit pas devenir un
    quatrième axe de statut ; il doit se projeter sur les énumérations
    existantes ou justifier une proposition de canon.
  - Aucune autorité ne peut être accordée à un composant non qualifié.
  - L'ADR reste `PROPOSED` tant qu'un humain n'a pas tranché : c'est la
    condition fail-closed qui empêche le code de démarrer.

## Assurance initiale

- **Gates applicables** : `DESIGN` (couture d'architecture) + `ADVERSARIAL`
  (six cas de falsification définis dans l'ADR).
- **Checkpoint visé** : `PRE_IMPLEMENTATION`
- **Implémentation autorisée à l'intake** : `NON` — seule une décision
  `implementation_authorization.status: AUTHORIZED` explicite peut l'autoriser.

## Adversarial level (ADR 0051 / ADR 0053) — post-cutoff required

```yaml
adversarial_level:
  level: "A2"
  level_reason: "Le sujet est le canon de gouvernance lui-même et l'intégrité
    des données de statut : deux triggers A2 de la matrice de criticité
    (governance canon, data integrity). Le contrat conditionne en outre des
    gates existantes, ce qui relève du canon-gating work."
```

## Certification status (post-cutoff)

```yaml
certification_status:
  declared_status: "NOT_CERTIFIED"
```

## Notes — dérives d'artefacts gouvernés détectées (règle #16)

Qualifiées, non corrigées. Décision humaine requise : `OUI` / `NON` / `PLUS TARD`.

- **D1** — `docs/CONTEXT.md` annonce comme prochaine action « obtenir la décision
  humaine pour la publication vers `main` », et une révision locale sur la
  branche `codex/document-model-main-integration`. L'état réel est `main`, avec
  les intégrations fusionnées (PR #3 et #4, `c8c513d`). Le routeur central est
  donc désaligné de l'état publié.
- **D2** — `docs/templates/01_INTAKE.md.template` déclare
  `adversarial_governance_version: "1.1"` alors que `SYSTEM.md` prescrit `1.2`
  pour les nouveaux runs (ADR 0053). Le présent intake déclare `1.2`.
- **D3** — l'énumération `agent:` des templates (`claude-code|codex|pi|opencode`)
  ne couvre pas le runtime qui exécute ce run. Déclaré `dsh`. Cette dérive est
  la même que celle traitée par la décision en attente sur une cinquième
  distribution (successeur d'ADR 0025).
