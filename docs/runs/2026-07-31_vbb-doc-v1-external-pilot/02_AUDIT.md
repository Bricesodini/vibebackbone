---
run_id: "2026-07-31_vbb-doc-v1-external-pilot"
phase: "02_AUDIT"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "run_artifact"
visibility: "internal"
status: "partial"
tags: [run, audit, documentation, governance, contract]
relations:
  - "01_INTAKE.md"
  - "INTEGRATION_GATE.md"
  - "POC.md"
  - "evidence/phase1/01_inventory_overview.md"
  - "evidence/phase2/05_linter_final_scope.txt"
  - "evidence/phase2/06_declaration_final.yaml"
  - "docs/DOCUMENT_CONVENTION.md"
  - "tools/vbb-document-convention-lint.py"
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
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "evidence/phase1/01_inventory_overview.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "evidence/phase2/"
---

# 02_AUDIT — vbb-doc-v1 external pilot (Backbone Know)

## Résumé exécutif

Le pilote **adopte** `vbb-doc-v1` v1.0 sur un périmètre minimal mais
représentatif de Backbone Know (5 documents + le contrat lui-même) dans
un worktree isolé. Le linter canonique produit **`VBB-DOC-V1: PASS`**
avec une seule correction triviale (1 tag namespacé). Le verdict est
**`PILOT_PASS_WITH_REVISIONS`** : l'adoption minimale est possible sans
accompagnement oral, mais le passage à l'échelle d'un grand dépôt (1524
fichiers `.md`) révèle trois révisions bloquantes pour la Release
Candidate et quatre améliorations post-RC.

## Sources de l'audit

| Source | Lecture | Statut |
|---|---|---|
| `docs/DOCUMENT_CONVENTION.md` (VBB) | intégrale | source primaire |
| `tools/vbb-document-convention-lint.py` (VBB) | intégrale + exécution | source primaire |
| `--help` du linter | intégrale | confirme l'interface publique |
| `docs/DOCUMENT_CONVENTION.md` (BK, copie) | intégrale | copie conforme |
| Dépôt Backbone Know (`/Users/bricesodini/02_dev/Backbone-know`) | échantillonnage (méta-docs + 3 formats d'audit + ADR + runs + templates + 5 docs adoptés) | read-only sauf worktree pilote |

## Périmètre Backbone Know inventorié

- **Total** : 1524 fichiers `.md` dans `docs/` (worktree SHA `661b240`).
- **Méta-docs racine** : 33 fichiers (CONTEXT, PROJECT_MODE, INDEX,
  DECISIONS, AUDIT_STATUS, RELATIONS, ARCHITECTURE, PRODUCT_BRIEF,
  contrats V1, incréments I1/I2, phases P06, modèles, POCs).
- **Sous-répertoires** : `adr/` (17), `audits/` (~82, 3 formats
  coexistants), `runs/` (~140), `templates/` (11), `gates/`,
  `engineering/`, `research-formulas/`, `benchmarks/` (artefacts
  générés), `model-lab/` (artefacts générés).

Le détail de l'inventaire et la cartographie vocabulaire BK ↔ vbb-doc-v1
sont préservés dans
[`evidence/phase1/01_inventory_overview.md`](evidence/phase1/01_inventory_overview.md).

## Périmètre Phase 2 adopté

6 fichiers adoptés (5 docs BK + le contrat copié) :

| # | Fichier | Catégorie vbb-doc-v1 | Cartographie effective |
|---|---|---|---|
| 1 | `docs/DOCUMENT_CONVENTION.md` | contrat copié | `type: reference`, `status: active`, `visibility: public`, `tags: [documentation, governance, contract, reference]`, relations vers `.vbb/document-convention.yaml` + `tools/vbb-document-convention-lint.py` |
| 2 | `docs/PRODUCT_BRIEF.md` | public principal | `type: reference`, `status: active`, `visibility: public`, `tags: [documentation, project:role:product-brief, project:phase:phase_0]` |
| 3 | `docs/ARCHITECTURE.md` | arch/référence | `type: reference`, `status: active`, `visibility: internal`, `tags: [documentation, architecture, project:role:canonical-architecture, project:phase:transverse]`, relations vers `CONTEXT.md` + `RELATIONS.md` |
| 4 | `docs/VBB_GATE_CONTRACT_V1.md` | opérationnel | `type: governance`, `status: frozen` (mapping de `ACCEPTED`), `visibility: internal`, `tags: [contract, governance, project:contract:..., project:contract-version:v1]`, relations vers `DOCUMENT_CONVENTION.md` + `gates/I2_IMPLEMENTATION_GATE.yaml` |
| 5 | `docs/POC_SYS_001_SYSTEM_HYPOTHESIS.md` | expérimental/recherche | `type: run_artifact`, `status: blocked` (mapping de `completed_design_only` + `t09_human_review: pending`), `visibility: experimental`, `tags: [run, experimental, project:kind:poc-report, project:poc-id:POC_SYS_001, project:domain:research]`, `run_id`, `route`, `verdict: blocked` |
| 6 | `docs/RELATIONS.md` | historique/généré | `type: reference`, `status: frozen` (mapping de `generated`), `visibility: internal`, `tags: [documentation, architecture, project:role:architecture-relations, project:source:generated, project:phase:transverse]`, relations vers `ARCHITECTURE.md` + `tools/vbb-architecture.py` |

Tous les vocabulaires propres à Backbone Know (`context_role`,
`phase` cycle projet, `increment`, `kind`, `audit_type`, `poc_id`,
`source`, `agent`, `adversarial_level`, `attacker_identity`, etc.) sont
préservés soit comme **dimensions additionnelles** du frontmatter
(quand utiles), soit comme **extensions namespacées `project:`**
(quand sémantiquement optionnelles), conformément à §5 du contrat.

## Sortie du linter

Sortie finale (`scope = 6 fichiers adoptés`, excluant le reste de `docs/`) :

```
VBB-DOC-V1: PASS
EXIT=0
```

Fichier préservé : [`evidence/phase2/05_linter_final_scope.txt`](evidence/phase2/05_linter_final_scope.txt).

**Première exécution** : `VBB-DOC-V1: FAIL` — un seul diagnostic :
`docs/POC_SYS_001_SYSTEM_HYPOTHESIS.md: unknown tag research`.
Le tag `research` n'est pas dans la liste canonique §5 ; corrigé en
`project:domain:research`. Une seule itération a suffi.

**Test de robustesse** (scope étendu à 9 fichiers incluant 3 docs non
conformes) : `VBB-DOC-V1: FAIL` avec 24 diagnostics — comportement
attendu. Fichier préservé :
[`evidence/phase2/04_linter_extended_scope.txt`](evidence/phase2/04_linter_extended_scope.txt).
**Conséquence** : le linter ne propose aucun mécanisme d'adoption
progressive ; tout fichier hors-scope qui devrait être dans le scope
casse l'adoption sans guidance.

## Frictions rencontrées

Classifiées selon les cinq catégories. Détail dans
[`03_DECISION.md`](03_DECISION.md).

### Frictions effectivement rencontrées (pendant le pilote)

| ID | Friction | Catégorie | Sévérité | Action |
|---|---|---|---|---|
| F-PH2-01 | Tag `research` non canonique | PROJECT_SPECIFIC | LOW | Corrigé : `project:domain:research` |

### Frictions anticipées par l'inventaire et confirmées

| ID | Friction | Catégorie | Sévérité |
|---|---|---|---|
| F-PH1-01 | Statut BK uppercase vs lowercase contrat | CONTRACT_AMBIGUITY | MEDIUM |
| F-PH1-02 | Statuts composés BK (`FROZEN`, `generated`, `closed`, `planned`, `completed_design_only`, `normative`, `frozen_with_open_questions`) — aucun mécanisme d'extension de domaine | DOCUMENTATION_GAP | HIGH |
| F-PH1-03 | Vocabulaire `context_role` (15+ valeurs) propre à BK | PROJECT_SPECIFIC | LOW (résolu par `project:role:`) |
| F-PH1-04 | Vocabulaire `phase` (cycle projet BK) sans slot vbb-doc-v1 | PROJECT_SPECIFIC | LOW (résolu par `project:phase:`) |
| F-PH1-05 | Vocabulaire `kind`, `audit_type`, `poc_id`, `increment` | PROJECT_SPECIFIC | LOW (résolu par `project:kind:`, `project:audit-type:`, etc.) |
| F-PH1-06 | Ordre de lecture canonique §7 non imposé techniquement | DOCUMENTATION_GAP | MEDIUM |
| F-PH1-07 | Linter ne signale pas les docs hors-scope qui devraient être adoptés | LINTER_GAP | HIGH |
| F-PH1-08 | Linter ne vérifie pas l'existence des fichiers listés dans `relations` | LINTER_GAP | LOW |
| F-PH1-09 | Linter ne vérifie pas la cohérence interne du scope (relations pointent vers fichiers adoptés) | LINTER_GAP | LOW |
| F-PH1-10 | Pas de mécanisme d'adoption progressive / waivers pour grands dépôts | V1_BLOCKER | HIGH |

## Décisions de correspondance retenues

- **Convention de casse** : `status` est normalisé en lowercase dans le frontmatter conforme. Le linter impose cette normalisation. Un mainteneur doit lire §4 + observer la sortie du linter pour inférer la règle.
- **Cartographie `context_role` → `type: reference` + `tags: [project:role:<rôle>]`** : conserve le vocabulaire BK sans forcer l'effacement.
- **Cartographie `kind: poc-report` → `type: run_artifact`** : un POC est un artefact de run ; le `kind` original est préservé comme tag namespacé.
- **Cartographie `audit_type: data-integrity` → `type: audit_report`** : le contenu du rapport est `audit_report` ; `audit_type` préservé comme tag.
- **Statut `generated` (RELATIONS.md) → `status: frozen`** : un fichier généré est considéré comme figé tant qu'il n'est pas régénéré.
- **Statut `ACCEPTED` (VBB_GATE_CONTRACT_V1) → `status: frozen`** : un contrat de gate ACCEPTED est opérationnellement verrouillé.
- **Statut `completed_design_only` (POC_SYS_001) → `status: blocked`** : POC non implémenté + revue humaine en attente = bloqué.
- **Vocabulaire `phase` (BK, run-level)** : préservé comme dimension additionnelle du frontmatter (champ `phase` non conforme vbb-doc-v1 mais non interdit).

## Constat global

L'adoption minimale de `vbb-doc-v1` sur Backbone Know est **possible
sans accompagnement oral** pour un périmètre restreint (6 fichiers).
Le contrat, le linter et le mécanisme d'extension `project:` sont
suffisants pour ce périmètre. L'extrapolation à l'ensemble du dépôt
(1524 fichiers) révèle trois révisions **bloquantes** pour une Release
Candidate.

Le détail des révisions et leur séparation RC / post-RC sont dans
[`03_DECISION.md`](03_DECISION.md) et [`07_CLOSEOUT.md`](07_CLOSEOUT.md).

## Preuves préservées

- [`evidence/phase1/01_inventory_overview.md`](evidence/phase1/01_inventory_overview.md) — inventaire Phase 1
- [`evidence/phase2/01_linter_first_run.txt`](evidence/phase2/01_linter_first_run.txt) — première sortie linter (FAIL : `unknown tag research`)
- [`evidence/phase2/02_linter_second_run.txt`](evidence/phase2/02_linter_second_run.txt) — après correction
- [`evidence/phase2/03_git_diff_modified.txt`](evidence/phase2/03_git_diff_modified.txt) — diff des 5 docs modifiés
- [`evidence/phase2/04_linter_extended_scope.txt`](evidence/phase2/04_linter_extended_scope.txt) — test scope étendu
- [`evidence/phase2/05_linter_final_scope.txt`](evidence/phase2/05_linter_final_scope.txt) — sortie finale PASS
- [`evidence/phase2/06_declaration_final.yaml`](evidence/phase2/06_declaration_final.yaml) — déclaration d'adoption finale