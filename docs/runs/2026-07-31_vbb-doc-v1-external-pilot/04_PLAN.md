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

<!-- RETROACTIVE_STRUCTURAL_REMEDIATION_2026-08-01
     Ajout rétrocompatible des 5 sections canoniques vbb-doc-v1
     (Objectif, Pré-conditions, Étapes ordonnées,
     Critères d'acceptation, Plan de rollback global) exigées par
     le validateur de plan en vigueur au 2026-08-01.

     Le contenu de ces sections est reconstruit à partir des sections
     préexistantes (Cadrage, Hors-périmètre, Séquence d'actions prévue,
     Décisions prévues, Garde-fous) et des artefacts du run
     (01_INTAKE.md, 02_AUDIT.md, 07_CLOSEOUT.md).

     Aucune information factuelle n'est modifiée. Le verdict
     `PILOT_PASS_WITH_REVISIONS`, le périmètre (Backbone Know, 6 fichiers)
     et le déroulement (cf. 05_EXECUTION.md, 07_CLOSEOUT.md) sont
     strictement préservés.

     Cette remédiation est de type INTEGRATION_ONLY. Elle ne modifie
     ni le contenu du candidat de release v1.1.0-rc.2
     (SHA = 3486300f359ff3b51effb007ed950dd48592556f) ni le tag
     v1.1.0-rc.2 associé. Elle est commise sur la branche
     codex/rc2-candidate-prep en tant que P_integration, distinct
     du sujet tagué S.
-->

## Objectif

Réaliser le premier pilote externe de la convention documentaire
`vbb-doc-v1` v1.0 — publiée dans `docs/DOCUMENT_CONVENTION.md` —
sur le dépôt tiers Backbone Know, **sans accompagnement oral**, en
deux phases (audit documentaire puis adoption pilote minimale)
sur un worktree isolé, en classifiant toutes les frictions selon
cinq catégories (PROJECT_SPECIFIC, DOCUMENTATION_GAP,
CONTRACT_AMBIGUITY, LINTER_GAP, V1_BLOCKER), et en produisant un
verdict final obligatoire parmi `PILOT_PASS`,
`PILOT_PASS_WITH_REVISIONS` ou `PILOT_FAIL`, accompagné d'une liste
de findings destinés à un run de remédiation canonique séparé.

Le pilote n'est PAS une modification de Vibe Backbone (canon,
contrat, linter, gouvernance) ni une migration aveugle des
1524 fichiers `.md` de Backbone Know. Il produit une adoption
réelle mais strictement confinée à un périmètre représentatif de
6 fichiers (5 docs migrés + la déclaration d'adoption modèle).

## Pré-conditions

- **Sources autorisées strictement** : `docs/DOCUMENT_CONVENTION.md`
  (et la documentation publique qu'il référence, à savoir aucune
  supplémentaire), la déclaration d'adoption modèle (§1), et
  `tools/vbb-document-convention-lint.py` avec son aide publique
  (`--help`).
- **Lecture interdite** : aucun run historique de stabilisation
  (`docs/runs/2026-07-31_1400_document-convention-v1-stabilization/`,
  `docs/runs/2026-07-30_1230_document-identity-compatibility/`) —
  le pilote reproduit la perspective d'un mainteneur qui découvre.
- **Dépôt cible** : `/Users/bricesodini/02_dev/Backbone-know`,
  branche `main`, SHA `661b240`, working tree propre (sauf un run
  untracked sans impact).
- **Worktree isolé** : `/Users/bricesodini/02_dev/backbone-know-pilot`
  sur branche `pilot/vbb-doc-v1-external`. La branche `main` de BK
  ne reçoit ni commit ni push durant le pilote.
- **Vibe Backbone** : aucun commit modifiant le canon, le contrat,
  le linter ou les fichiers de gouvernance. Le seul ajout autorisé
  est `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/`.
- **Adversarial level A2** déclaré à l'intake avec disclosure
  d'identité (agent, llm, system_prompt_version, distinct_actor,
  external_review_eligibility) répétée dans tous les artefacts
  `01..07` du run et dans `INTEGRATION_GATE.md`.
- **Gate initiale** : `vbb-gate-check.py` peut refuser avant que
  la POC ait son verdict (PENDING par construction ; la POC EST le
  pilote).

## Étapes ordonnées

| # | Étape | Sortie attendue |
|---|---|---|
| 1 | Lecture intégrale des sources autorisées VBB | Contrat + linter + aide compris |
| 2 | Localisation BK + `git worktree add` | Worktree `pilot/vbb-doc-v1-external` créé |
| 3 | Inventaire `docs/` BK (structure, types, statuts, tags, visibilité, relations) | Cartographie brute BK |
| 4 | Cartographie vocabulaire BK ↔ vbb-doc-v1 (incluant extensions `project:`) | Table de correspondance |
| 5 | Sélection des 5 docs représentatifs (public / arch / op / exp / hist) | Périmètre arrêté |
| 6 | Copie `docs/DOCUMENT_CONVENTION.md` + `tools/vbb-document-convention-lint.py` dans BK worktree | Sources adoptées disponibles |
| 7 | Création `.vbb/document-convention.yaml` (scope = 6 fichiers, excludes larges) | Déclaration d'adoption |
| 8 | Migration des 5 docs vers frontmatter conforme (7 champs obligatoires + tags `project:`) | 5 docs adoptés |
| 9 | Exécution linter → itération 1 | Diagnostic(s) éventuel(s) |
| 10 | Correction des frictions rencontrées | Diagnostic(s) résolu(s) |
| 11 | Exécution linter → itération 2 | `VBB-DOC-V1: PASS` attendu |
| 12 | Test de robustesse (scope étendu à 9 fichiers non conformes) | Confirmation comportement FAIL |
| 13 | Rédaction des artefacts `02_AUDIT.md`, `03_DECISION.md`, `05_EXECUTION.md`, `06_REVIEW.md`, `07_CLOSEOUT.md` | Run complet |
| 14 | Rejeu `vbb-gate-check.py` + `vbb-loop-closure-check.py` (claims + plan + assurance) | Gates PASS |
| 15 | Commit + push sélectif (uniquement mon run, sans toucher aux modifications d'autres agents en working tree) | Run archivé sur `origin` |

## Critères d'acceptation

- **CA-1** : Verdict final ∈ {`PILOT_PASS`, `PILOT_PASS_WITH_REVISIONS`,
  `PILOT_FAIL`} clairement prononcé, avec décomposition RC / post-RC
  si `PILOT_PASS_WITH_REVISIONS`.
- **CA-2** : Huit réponses explicites aux questions du brief
  utilisateur dans `07_CLOSEOUT.md`.
- **CA-3** : Linter canonique produit `VBB-DOC-V1: PASS` (exit 0)
  sur le scope déclaré. Sortie préservée dans `evidence/phase2/`.
- **CA-4** : Inventaire Phase 1 documenté dans
  `evidence/phase1/01_inventory_overview.md`, couvrant structure,
  types, statuts, métadonnées, tags, visibilité, relations, ordre
  de lecture, contradictions, doublons, inclassables.
- **CA-5** : Cartographie vocabulaire BK ↔ vbb-doc-v1 documentée
  avec table de correspondance pour `context_role`, `phase`,
  `kind`, `audit_type`, `poc_id`, `increment`, `source`, statuts.
- **CA-6** : 5 docs représentatifs adoptés dans un worktree BK
  isolé, avec frontmatter conforme (7 champs obligatoires + tags
  + relations).
- **CA-7** : Toutes les frictions classifiées dans l'une des 5
  catégories (PROJECT_SPECIFIC / DOCUMENTATION_GAP /
  CONTRACT_AMBIGUITY / LINTER_GAP / V1_BLOCKER).
- **CA-8** : Identity disclosure A2_DISTINCT_AGENT_PROXY répétée
  dans tous les artefacts du run (`01..07` + `INTEGRATION_GATE.md`).
- **CA-9** : Aucune modification de Vibe Backbone (canon, contrat,
  linter, gouvernance). Vérifiable par `git diff` post-commit
  (uniquement `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/`
  doit être ajouté).
- **CA-10** : Backbone Know `main` non touché. Vérifiable par
  `git -C /Users/bricesodini/02_dev/Backbone-know log main`
  (SHA inchangé).
- **CA-11** : Gates VBB PASS au closeout :
  `vbb-gate-check.py` → `can_code_start=true` ;
  `vbb-loop-closure-check.py --strict --validate-claims --validate-plan`
  → `PASS`.

## Plan de rollback global

Le pilote est **non-destructif** par conception, ce qui rend tout
rollback trivial :

- **Vibe Backbone** : le seul fichier ajouté par le pilote est
  `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/`. Aucun fichier
  du canon, du contrat, du linter ou de la gouvernance n'est
  modifié. En cas de regret, suppression simple de ce répertoire
  puis revert du commit (si déjà pushé).
- **Backbone Know** : toutes les modifications sont confinées au
  worktree `/Users/bricesodini/02_dev/backbone-know-pilot`. La
  branche `main` est intacte. En cas de regret :
  ```bash
  git -C /Users/bricesodini/02_dev/Backbone-know worktree remove \
      /Users/bricesodini/02_dev/backbone-know-pilot
  git -C /Users/bricesodini/02_dev/Backbone-know branch -D \
      pilot/vbb-doc-v1-external
  ```
  Aucun commit ni merge n'a été fait sur `main`. Aucune perte
  d'information côté BK.
- **Findings** : ils sont consignés en Markdown dans `02_AUDIT.md`,
  `03_DECISION.md`, `07_CLOSEOUT.md`. Aucune base de données ni
  état runtime à nettoyer.

Aucun rollback de pilote n'est anticipé : la consigne utilisateur
exige que toute correction soit consignée comme finding pour un run
de remédiation séparé, **pas corrigée** dans ce pilote. Le plan
ci-dessus n'existe donc que pour gérer un éventuel abandon
exogène du pilote.

<!-- END RETROACTIVE_STRUCTURAL_REMEDIATION -->

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