---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run12-multiservice-adr-remaining
route: STRUCTURED
updated: 2026-07-12
---

# Run 12 — Multi-service ADR restants (Gap-08/12/13/15)

> **Route** : STRUCTURED
> **Effort** : M (~50 min, 4 ADR substantiels)
> **Risque canon** : faible (documents de design, 0 modif directe)
> **Pre-merge gate** : REQUIS (route STRUCTURED)
> **Statut** : `READY — prêt à exécuter sur GO utilisateur`

---

## 1. Goal

Produire les **4 derniers ADR** de la couche design Phase 2 : Gap-08, Gap-12, Gap-13, Gap-15. **Pas d'implémentation runtime**.

**Avec ce run, la couche design est complète pour 15/18 gaps** (83%). Restent 3 gaps P2 (Gap-16, 17, 18) → polish futur.

---

## 2. Findings source

| ID | Finding | Gap | Sévérité |
|----|---------|-----|----------|
| **Gap-08** | Pas de support multi-repo | `01_GAP_ANALYSIS.md` | **P0** |
| **Gap-12** | Première extension concrète (multi-service-database-per-service) | idem | P1 |
| **Gap-13** | Pas de `vbb-multiservice-graph.py` (graphe inter-services) | idem | **P0** |
| **Gap-15** | Pas de hook CI « ne pas régresser » (gate enforcement) | idem | **P0** |

---

## 3. ADR à créer

### ADR-0018 — Multi-repo support (Gap-08, P0)

**Décision** : introduire un fichier `docs/MULTIREPO.yaml` (par projet) qui déclare :
- `repos:` — liste des autres repos du système multi-service
- Pour chaque repo : nom, path relatif, role, services fournis
- `tools:` — outils qui traversent les repos (e.g. graph global)

Les outils existants (`vbb-context-compactor`, `vbb-status-dashboard`) sont étendus pour lire `MULTIREPO.yaml` et exposer une vue d'ensemble.

**Justification** : aujourd'hui, un projet mono-repo ne peut pas exprimer qu'il appartient à un système multi-repo. Le graphe global (Gap-13) requiert cette déclaration.

### ADR-0019 — Première extension concrète (Gap-12, P1)

**Décision** : créer `docs/extensions/multi-service-database-per-service/` (première extension concrète selon ADR-0014) avec :
- `MANIFEST.yaml` (cf. ADR-0014)
- `README.md` (comment adopter l'extension)
- `rules.yaml` (règles spécifiques au pattern database-per-service)

**Justification** : sans première extension concrète, le mécanisme d'extension (ADR-0014) reste théorique. Cette extension sert de **POC** et de template pour les suivantes.

### ADR-0020 — Graphe inter-services (Gap-13, P0)

**Décision** : créer `tools/vbb-multiservice-graph.py` qui consomme `CONTRACTS_CONSUMED.md` (cf. ADR-0007), `CONTRACTS_PROVIDED.md` (à définir), et `MULTIREPO.yaml` (cf. ADR-0018) pour générer un graphe d'interdépendances.

Modes : `--text` (résumé humain), `--dot` (format Graphviz), `--json` (machine-readable), `--check-cycle` (détection cycles).

**Justification** : sans graphe, impossible de visualiser les interdépendances et de détecter les cycles.

### ADR-0021 — Gate CI enforcement (Gap-15, P0)

**Décision** : créer `scripts/vbb-ci-local.sh` (script bash canonique) qui exécute en séquence :
1. `python tools/vbb-contract-lint.py`
2. `python tools/vbb-multiservice-lint.py --strict`
3. `python tools/vbb-multiservice-graph.py --check-cycle`
4. `python tools/vbb-architecture.py agents --check`

Exit 0 si tout passe, exit 1 sinon. Le script est le **gate canonique** que les hooks CI (GitHub Actions, GitLab CI, etc.) appellent.

**Justification** : sans gate outillé, la discipline multi-service n'est pas enforceable. Le script bash est portable (pas de dépendance Python dans CI).

---

## 4. Excluded

- ❌ Implémentation runtime (Run 13+)
- ❌ Création effective de `MULTIREPO.yaml` (à faire par chaque projet qui en a besoin)
- ❌ Création effective de `docs/extensions/multi-service-database-per-service/` (Run 13+)
- ❌ Création effective de `vbb-multiservice-graph.py` et `vbb-ci-local.sh` (Run 13+)
- ❌ Polish P2 (Gap-16, 17, 18) — futur Run

---

## 5. Files impact summary

| File | Type | Impact |
|------|------|--------|
| `docs/adr/0018-multirepo-support.md` | nouveau ADR | +120 lignes |
| `docs/adr/0019-first-extension-database-per-service.md` | nouveau ADR | +100 lignes |
| `docs/adr/0020-multiservice-graph.md` | nouveau ADR | +130 lignes |
| `docs/adr/0021-ci-gate-enforcement.md` | nouveau ADR | +130 lignes |
| `docs/adr/README.md` | index | +4 lignes |
| `docs/runs/2026-07-12_run12-multiservice-adr-remaining/01_INTAKE.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run12-multiservice-adr-remaining/05_PATCH_SUMMARY.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run12-multiservice-adr-remaining/07_CLOSEOUT.md` | artefact | nouveau |
| `docs/ACTIVITY_LOG.md` | log | +1 ligne |

---

## 6. Verification (pre-merge gate REQUIS)

```bash
python tools/vbb-contract-lint.py  # Attendu : 0/0
ls docs/adr/001[8-9]-*.md docs/adr/002[01]-*.md  # Attendu : 4 fichiers
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md tools/  # Attendu : vide
```

---

## 7. Acceptance criteria

- ✅ 4 ADR créés (0018, 0019, 0020, 0021)
- ✅ Chaque ADR a ≥ 2 alternatives rejetées
- ✅ Index ADR mis à jour
- ✅ Aucun canon / outil / template touché
- ✅ Pre-merge gate PASS
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

---

## 8. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../../../docs/adr/0007-contracts-consumed-canonical-file.md`](../../../adr/0007-contracts-consumed-canonical-file.md) — dépendance ADR-0020
- [`../../../docs/adr/0014-canon-vs-extension.md`](../../../adr/0014-canon-vs-extension.md) — dépendance ADR-0019
- [`../../../docs/adr/0009-multiservice-lint-discipline.md`](../../../adr/0009-multiservice-lint-discipline.md) — dépendance ADR-0021
- [`../../../docs/adr/0012-codegen-agents-claudemd.md`](../../../adr/0012-codegen-agents-claudemd.md) — dépendance ADR-0021