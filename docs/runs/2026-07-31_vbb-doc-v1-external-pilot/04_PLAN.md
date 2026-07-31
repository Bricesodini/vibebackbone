---
run_id: "2026-07-31_vbb-doc-v1-external-pilot"
phase: "04_PLAN"
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
voie: "STRUCTUREE"
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
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — vbb-doc-v1 external pilot (Backbone Know)

> Plan d'exécution du pilote externe `vbb-doc-v1` sur Backbone Know.
> Le pilote EST la POC ; ce plan décrit la séquence d'actions prévue.

## Cadrage

- **Voie** : STRUCTUREE
- **Adversarial level** : A2_DISTINCT_AGENT_PROXY
- **Cible** : dépôt `/Users/bricesodini/02_dev/Backbone-know` (worktree isolé)
- **Sources autorisées strictement** :
  `docs/DOCUMENT_CONVENTION.md`, sa doc publique référencée (aucune),
  modèle d'adoption (§1), `tools/vbb-document-convention-lint.py`
  + `--help`.
- **Périmètre Backbone Know** : 6 fichiers adoptés (le contrat copié
  + 5 docs représentatifs).
- **Sortie** : verdict `PILOT_PASS_WITH_REVISIONS` + findings destinés
  à un run de remédiation canonique séparé.

## Hors-périmètre

- Modification de Vibe Backbone (canon, contrat, linter, gouvernance).
- Migration aveugle des 1524 fichiers `.md` de Backbone Know.
- Levée des blockers `RR-BK-01..06`.
- Production d'un verdict global READY sur VBB ou BK.

## Séquence d'actions prévue

| Étape | Action | Résultat attendu |
|---|---|---|
| 1 | Lecture intégrale des sources autorisées (VBB) | Contrat + linter compris |
| 2 | Localisation BK + création worktree `pilot/vbb-doc-v1-external` | Worktree prêt |
| 3 | Inventaire de `docs/` BK | Cartographie structure / types / statuts / tags / visibilité / relations |
| 4 | Cartographie vocabulaire BK ↔ vbb-doc-v1 | Table de correspondance avec extensions `project:` |
| 5 | Sélection de 5 docs représentatifs (public / arch / op / exp / hist) | Périmètre arrêté |
| 6 | Copie convention + linter dans BK worktree | Préparation scope |
| 7 | Création `.vbb/document-convention.yaml` (scope = 6 fichiers) | Déclaration d'adoption |
| 8 | Migration des 5 docs vers frontmatter conforme | 5 docs conformes |
| 9 | Exécution linter → itération 1 | Diagnostic(s) identifié(s) |
| 10 | Correction des frictions rencontrées | Diagnostic(s) résolu(s) |
| 11 | Exécution linter → itération 2 | PASS attendu |
| 12 | Test de robustesse (scope étendu) | Confirmation comportement FAIL sur docs non conformes |
| 13 | Rédaction des artefacts 02..07 du run VBB | Preuves + verdict |
| 14 | Rejeu `vbb-gate-check.py` + `vbb-loop-closure-check.py` | Gates PASS |
| 15 | Commit + push sélectif du run VBB | Run archivé |

## Décisions prévues

- **Type de chaque doc migré** :
  - `PRODUCT_BRIEF.md` → `reference`
  - `ARCHITECTURE.md` → `reference`
  - `VBB_GATE_CONTRACT_V1.md` → `governance`
  - `POC_SYS_001_SYSTEM_HYPOTHESIS.md` → `run_artifact`
  - `RELATIONS.md` → `reference`
- **Status de chaque doc migré** : cartographie BK → contrat (lowercase
  obligatoire) ; statuts composés sans équivalent → choix documenté dans
  `02_AUDIT.md` §Cartographie.
- **Visibility de chaque doc** : `public` pour les entrées projet,
  `internal` pour l'architecture, `experimental` pour les POC.
- **Vocabulaire `project:`** : nomspacer toutes les extensions locales
  (`context_role`, `phase` cycle projet, `kind`, `audit_type`, `poc_id`,
  `increment`, `source`) pour respecter §5 sans effacer le vocabulaire
  BK.

## Garde-fous

- **Aucun commit** sur la branche `main` de BK.
- **Aucun push** du worktree BK.
- **Aucun commit** modifiant le canon VBB, le contrat, le linter ou
  les fichiers de gouvernance VBB.
- **Aucun claim** de type `PASS_ADVERSARIAL` ou certification canonique.
- **Findings** : tout constat sur le contrat ou le linter est consigné
  comme finding, jamais corrigé dans ce pilote.

## Risques anticipés

- Frictions du linter sur les tags non canoniques (mitigation : `project:`).
- Statuts composés BK sans équivalent (mitigation : cartographie documentée).
- Vocabulaire `phase` (run-level) sans slot vbb-doc-v1 (mitigation :
  dimension additionnelle préservée).
- Ordre de lecture §7 non imposé techniquement (constat ; finding).

## Handoff vers `05_EXECUTION`

Le journal d'exécution détaillé est dans
[`05_EXECUTION.md`](05_EXECUTION.md).