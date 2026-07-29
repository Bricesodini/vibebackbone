---
run_id: "2026-07-29_1050_gcg-conceptual-model"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_MODEL_CONSOLIDATION"
adversarial_level: "A2"
scope_id: "GCG-MODEL-01"
agent: "claude-opus-5 (Claude Code)"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
adr_link: "docs/adr/0051-adversarial-assurance-dimension.md"
started_at: "2026-07-29T08:50:00Z"
ended_at: null
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/runs/2026-07-29_1021_adversarial-gate-population/ (tous artefacts)"
artifacts_produced:
  - "01_INTAKE.md (this file)"
  - "04_PLAN.md"
  - "05_EXECUTION.md"
  - "07_CLOSEOUT.md"
  - "docs/REFERENCE/governance-compatibility-model.md"
---

# 01_INTAKE — GCG-MODEL-01

## 1. Demande reçue

Stabiliser le modèle conceptuel du *Governance Compatibility Gate* avant de
poursuivre l'implémentation. Sept points : GCG comme capacité autonome ;
séparation Scanner / Migration Engine ; contrôle au démarrage de session ;
formalisation du cutoff ; réserve sur le SHA git comme frontière normative ;
renommage de `OUT_OF_SCOPE` ; report de `G7` à un run dédié.

## 2. Objectif

Produire le modèle conceptuel stabilisé, et **aligner le code existant sur ce
modèle** afin qu'aucune vérité parallèle ne subsiste entre la spécification et
l'instrument.

Ce run ne poursuit pas l'implémentation : il n'ajoute aucune capacité. Il
corrige la conception livrée par `2026-07-29_1021` sur trois points où elle
était fautive, et documente le modèle.

## 3. Corrections traitées

| ID | Objet | Nature |
|---|---|---|
| `C1` | Frontière normative dérivée de git au lieu d'être déclarée par le canon | **correction de conception** |
| `C2` | `OUT_OF_SCOPE` nomme un périmètre alors qu'il décrit un cycle de vie | **correction de nommage + garde manquant** |
| `C3` | Scanner / Arbitration / Migration Engine non séparés explicitement | **formalisation** |

`C1` était signalé comme incertitude résiduelle dans le closeout de `1021` : le
mapping commit → identité de run avait été établi par lecture d'artefacts, pas
mécaniquement. La déclaration canonique supprime l'incertitude plutôt que de la
documenter.

`C2` cachait un défaut : la catégorie n'avait aucune limite. Un run clos et
défaillant pouvait se déclarer « en attente d'une étape ultérieure » et échapper
au blocage — même vecteur de blanchiment que le ledger, sous un autre nom.

## 4. Scope

### Dans le périmètre
- `docs/REFERENCE/governance-compatibility-model.md` (`PROPOSED`).
- Alignement de `tools/vbb-governance-compat.py` et de ses tests.
- Formalisation du contrat de déclaration de règle (deux bornes).

### Hors périmètre
- Migration Engine — non implémenté, et ne doit pas l'être avant le ledger.
- Contrôle au démarrage de session — spécifié, non implémenté.
- `G7` (hook pre-commit) — reporté à un run dédié, sur décision explicite.
- Les trois questions normatives ouvertes — relèvent de l'arbitration humaine.

## 5. Classification du risque

- **Niveau** : `MODÉRÉ`
- **Justification** : le run corrige un modèle non encore câblé et non encore
  appliqué. Aucun artefact de gouvernance existant n'est modifié. Le risque
  principal est de figer un modèle prématurément — mitigé par le statut
  `PROPOSED`.

## 6. Voie recommandée

`STRUCTUREE`, `adversarial_level: A2` (canon-gating). `A2_DISTINCT_AGENT_PROXY`
non satisfait : même agent que `1021`.

## 7. Handoff vers `04_PLAN`
