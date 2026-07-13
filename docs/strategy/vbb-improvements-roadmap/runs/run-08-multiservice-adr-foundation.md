---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run08-multiservice-adr-foundation
route: STRUCTURED
updated: 2026-07-12
---

# Run 08 — Multi-service ADR foundation (Gap-01/02/05/14)

> **Route** : STRUCTURED
> **Effort** : M (~30 min, 4 ADR substantiels)
> **Risque canon** : faible (aucune modif directe de canon — les ADR sont des documents de design)
> **Pre-merge gate** : REQUIS (route STRUCTURED, cf. `docs/REFERENCE/pre-merge-gate.md`)
> **Statut** : `READY — prêt à exécuter sur GO`

---

## 1. Goal

Produire **4 Architecture Decision Records (ADR) vibebackbone** pour les gaps P0/P1 identifiés en Phase 1 `vbb-evolution-multi-service-support` (2026-07-12). Chaque ADR documente le problème, la solution retenue, les alternatives rejetées, et les conséquences — **sans implémentation runtime** (out of scope per consigne §3).

**Note** : Phase 1 interdisait explicitement « Écrire des ADR vibebackbone pour cette évolution ». Phase 2 l'autorise. Run 8 marque le passage Phase 1 → Phase 2 pour ces 4 gaps.

---

## 2. Findings source

| ID | Finding | Gap | Sévérité | Étape Phase 2 |
|----|---------|-----|----------|---------------|
| **Gap-01** | Pas de concept formel d'orientation DB dans l'intent projet | `01_GAP_ANALYSIS.md` §1 | P1 | Étape 1 |
| **Gap-02** | Pas de concept de project_archetype / projet typé | idem | P1 | Étape 1 |
| **Gap-05** | Pas de tracking des contrats consommés (CONTRACTS_CONSUMED.md) | idem | **P0** | Étape 1 |
| **Gap-14** | Pas de CONTEXT.md / PROJECT_MODE.md enrichi | idem | P1 | Étape 2 |

**Source** : [`docs/strategy/vbb-evolution-multi-service-support/`](../../../strategy/vbb-evolution-multi-service-support/) (Phase 1 complète)

---

## 3. Modifications (4 ADR + index)

### ADR-0005 — DB Orientation (Gap-01)

**Fichier** : `docs/adr/0005-db-orientation-context-extension.md`

**Décision** : ajouter une section `## DB Orientation` typée dans `docs/CONTEXT.md`, parmi l'enum canonique : `owned_private` / `shared_external_owned` / `shared_external_readonly` / `polyglot` / `stateless`. Chaque déclaration inclut rationale et référence ADR.

**Justification du choix** : extension pure (pas de canon modifié), permet la dérivation automatique de règles.

### ADR-0006 — Project Archetype (Gap-02)

**Fichier** : `docs/adr/0006-project-archetype-context-extension.md`

**Décision** : ajouter une section `## Project Archetype` typée dans `docs/CONTEXT.md`, parmi l'enum canonique : `frontend_app` / `api_service` / `orchestrator` / `read_only_consumer` / `worker` / `library`. Cette déclaration oriente les templates d'artefact et les linters.

**Justification du choix** : extension cohérente avec ADR-0005 (même schéma projet).

### ADR-0007 — CONTRACTS_CONSUMED canonique (Gap-05)

**Fichier** : `docs/adr/0007-contracts-consumed-canonical-file.md`

**Décision** : créer un nouveau fichier canonique `docs/CONTRACTS_CONSUMED.md` (par projet) + un template `docs/templates/CONTRACTS_CONSUMED.md.template`, documentant structurellement ce que chaque projet **consomme** (api/db/event), **depuis qui**, **dans quelle version**, **avec quelle criticité**. Exploitable par `t-vbb-impact-analyzer` et `vbb-multiservice-lint` (futurs outils).

**Justification du choix** : nouveau fichier (pas de canon modifié), permet l'analyse d'impact cross-service.

### ADR-0008 — CONTEXT.md / PROJECT_MODE.md enrichi (Gap-14)

**Fichier** : `docs/adr/0008-context-project-mode-enrichment.md`

**Décision** : modifier le contenu généré par `tools/vbb-project-init.py` pour produire un `CONTEXT.md` et un `PROJECT_MODE.md` structurés selon un schéma défini : `db_orientation` (cf. ADR-0005), `project_archetype` (cf. ADR-0006), `scope` explicite, `contracts_expected`, `non_goals`. Schéma validé par les outils (lint).

**Justification du choix** : l'enrichissement du contenu généré est distinct du canon ; il est légitime.

### Index — `docs/adr/README.md`

**Modification** : ajouter une table listant les 4 nouveaux ADR avec leur titre court et leur gap source.

---

## 4. Alternatives rejetées (considérées globalement)

Pour chaque ADR, ≥ 2 alternatives rejetées sont documentées dans le fichier. Pattern commun :

- **Alternative A** : « ne rien documenter, garder en prose » — rejetée (impossible à dériver / auditer).
- **Alternative B** : « modifier le canon `CONVENTIONS.md` au lieu d'étendre `CONTEXT.md` » — rejetée (risque canon plus élevé, gain marginal).

Pour les détails spécifiques à chaque ADR, voir le fichier correspondant.

---

## 5. Excluded

- ❌ **Implémentation runtime** des gaps — out of scope per consigne §3 (déploiement, codegen, migration de projets concrets)
- ❌ Création d'outils (`vbb-multiservice-lint.py`, `vbb-orientation-codegen.py`, etc.) — Étape 3+ de Phase 2
- ❌ Modification du canon `CONVENTIONS.md` ou `PILOTAGE.md` — extensions seulement
- ❌ Création de templates concrets (CONTRACTS_CONSUMED.md.template) — décisions seulement, exécution = Run 9+
- ❌ Création d'ADR pour les autres gaps (Gap-03/04/06/07/08/09/10/11/12/13/15) — Runs ultérieurs

---

## 6. Files impact summary

| File | Type | Impact |
|------|------|--------|
| `docs/adr/0005-db-orientation-context-extension.md` | nouveau ADR | +50-80 lignes |
| `docs/adr/0006-project-archetype-context-extension.md` | nouveau ADR | +50-80 lignes |
| `docs/adr/0007-contracts-consumed-canonical-file.md` | nouveau ADR | +50-80 lignes |
| `docs/adr/0008-context-project-mode-enrichment.md` | nouveau ADR | +50-80 lignes |
| `docs/adr/README.md` | index | +10 lignes (4 lignes ADR) |
| `docs/runs/2026-07-12_run08-multiservice-adr-foundation/01_INTAKE.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run08-multiservice-adr-foundation/05_PATCH_SUMMARY.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run08-multiservice-adr-foundation/07_CLOSEOUT.md` | artefact | nouveau |
| `docs/ACTIVITY_LOG.md` | activity log | +1 ligne |

**Total** : 9 fichiers (4 nouveaux ADR + 1 index + 3 artefacts + 1 log entry)

---

## 7. Verification (pre-merge gate REQUIS, route STRUCTURED)

```bash
# P.R2 §1 — Lint (ne doit pas casser)
python tools/vbb-contract-lint.py
# Attendu : 0 erreur, 0 warning (ADR n'affecte pas les contracts)

# P.R2 §2 — Type / schema (N/A, fichiers markdown)

# P.R2 §3 — Tests (N/A, pas de code)

# P.R2 §4 — Build (N/A, pas de code)

# P.R2 §5 — Documentation coherence
ls docs/adr/000[5-8]-*.md
# Attendu : 4 fichiers présents
grep -c "0005-\|0006-\|0007-\|0008-" docs/adr/README.md
# Attendu : 4 références

# Sanity check : canon non lié intact
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md tools/vbb-contract-lint.py tools/vbb-project-init.py
# Attendu : vide
```

---

## 8. Acceptance criteria

Run 8 est **COMPLET** si :

- ✅ 4 ADR créés (`docs/adr/0005-*.md`, `0006-*.md`, `0007-*.md`, `0008-*.md`)
- ✅ Chaque ADR suit le template (`docs/templates/ADR.md.template`)
- ✅ Chaque ADR a ≥ 2 alternatives rejetées
- ✅ `docs/adr/README.md` mis à jour avec les 4 références
- ✅ Aucun canon `CONVENTIONS.md` / `PILOTAGE.md` / `AGENTIC_RUN_PROTOCOL.md` non lié touché
- ✅ Aucun outil (`tools/vbb-*.py`) touché
- ✅ Pre-merge gate (5 P.R2) passé
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

---

## 9. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) — source des gaps
- [`../../../docs/strategy/vbb-evolution-multi-service-support/02_PRIORITIES.md`](../../../strategy/vbb-evolution-multi-service-support/02_PRIORITIES.md) — séquence Phase 2
- [`../../../docs/templates/ADR.md.template`](../../../templates/ADR.md.template) — template ADR
- [`../../../docs/adr/README.md`](../../../adr/README.md) — index ADR