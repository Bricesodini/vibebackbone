---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run11-multiservice-adr-p1
route: STRUCTURED
updated: 2026-07-12
---

# Run 11 — Multi-service ADR P1 (Gap-03/07/09/11)

> **Route** : STRUCTURED
> **Effort** : M (~50 min, 4 ADR substantiels)
> **Risque canon** : faible (documents de design, 0 modif directe)
> **Pre-merge gate** : REQUIS (route STRUCTURED)
> **Statut** : `READY — prêt à exécuter sur GO utilisateur`

---

## 1. Goal

Produire **4 ADR vibebackbone** pour les gaps **P1** restants en Phase 2 : Gap-03, Gap-07, Gap-09, Gap-11. **Pas d'implémentation runtime** (out of scope per consigne §3, comme Run 8 et 9).

**Avec ce run, la couche design est complète pour tous les gaps P0+P1 sauf 4 (Gap-08, 12, 13, 15), qui forment Run 12.**

---

## 2. Findings source

| ID | Finding | Gap | Sévérité | Étape Phase 2 |
|----|---------|-----|----------|---------------|
| **Gap-03** | Pas de codegen AGENTS.md / CLAUDE.md depuis source canonique | `01_GAP_ANALYSIS.md` | P1 | Étape 5 (Codegen) |
| **Gap-07** | Pas de discipline outillée de co-évolution | idem | P1 | Étape 4 (Gates & co-évolution) |
| **Gap-09** | Pas de mécanisme canon vs extension | idem | P1 | Étape 2 (Discipline) |
| **Gap-11** | Pas de vbb-contract-lint archetype-aware | idem | P1 | Étape 4 (Gates & co-évolution) |

**Source** : [`docs/strategy/vbb-evolution-multi-service-support/`](../../../strategy/vbb-evolution-multi-service-support/)

---

## 3. ADR à créer

### ADR-0012 — Codegen AGENTS.md / CLAUDE.md (Gap-03)

**Décision** : étendre `tools/vbb-architecture.py` (qui fait déjà codegen `ARCHITECTURE.md` → `RELATIONS.md`) pour ajouter un mode `agents --write` qui génère `AGENTS.md` (racine) et `distributions/claude/CLAUDE.md` depuis une source canonique (`docs/CONTEXT.md` + `docs/PILOTAGE.md` + Critical Rules 1-13).

**Justification** : aujourd'hui, modifier une Critical Rule demande de reporter manuellement dans 3+ fichiers. Drift silencieux possible.

### ADR-0013 — Discipline outillée de co-évolution (Gap-07)

**Décision** : étendre `t-vbb-impact-analyzer` (existant) pour générer une **séquence de tâches coordonnées** chez les consommateurs lors d'un breaking change. Chaque tâche = entrée dans `IMPACT_LOG.md` (cf. ADR-0010) + checklist de migration par consumer.

**Justification** : aujourd'hui, la co-évolution est entièrement manuelle. Le passage à l'échelle (N services) la rend impraticable.

### ADR-0014 — Mécanisme canon vs extension (Gap-09)

**Décision** : introduire le dossier `docs/extensions/<pattern>/` avec un fichier `MANIFEST.yaml` qui déclare :
- pattern: <slug>
- canon_implications: <none | additive | breaking>
- conflicts_with: <list of patterns>
- status: <experimental | beta | stable | deprecated>

Un outil `vbb-extension-register` lit le dossier et expose les extensions actives. Le but : permettre aux projets d'étendre le framework localement (par exemple `docs/extensions/multi-service-database-per-service/`) sans modifier le canon.

**Justification** : sans mécanisme d'extension, chaque évolution de vibebackbone force un canon change. Avec, les projets peuvent adopter des patterns localement.

### ADR-0015 — vbb-contract-lint archetype-aware (Gap-11)

**Décision** : étendre `tools/vbb-contract-lint.py` pour rendre les règles **contextuelles** au `project_archetype` (cf. ADR-0006) :
- `api_service` : active toutes les règles actuelles
- `read_only_consumer` : ajoute règle « pas d'`outputs.artifact` exposé »
- `worker` : ajoute règle « au moins un trigger (event/queue/cron) »
- `library` : assouplit les règles (pas d'obligation de `outputs.artifact` runtime)

Le `project_archetype` est lu depuis `docs/CONTEXT.md` (frontmatter).

**Justification** : sans cette adaptation, tous les projets sont validés par les mêmes règles, ce qui force les workarounds en prose.

---

## 4. Alternatives rejetées (considérées globalement)

Pour chaque ADR, ≥ 2 alternatives rejetées sont documentées dans le fichier. Pattern commun :

- **Alternative A** : « ne rien outiller, garder en prose/conversation » — rejetée (régression silencieuse).
- **Alternative B** : « intégrer dans un outil canonique existant sans distinction claire » — rejetée (séparation des concerns).

Pour les détails spécifiques à chaque ADR, voir le fichier correspondant.

---

## 5. Excluded

- ❌ Implémentation runtime des gaps — out of scope per consigne §3
- ❌ Création d'outils concrets (`vbb-extension-register`, etc.) — Runs 13+
- ❌ Création de templates concrets (`MANIFEST.yaml.template`) — Runs 13+
- ❌ Modification effective de `t-vbb-impact-analyzer` ou `vbb-contract-lint.py` — Runs 13+
- ❌ ADR pour Gap-08, 12, 13, 15 — Run 12
- ❌ Modification du canon `CONVENTIONS.md` ou `PILOTAGE.md`

---

## 6. Files impact summary

| File | Type | Impact |
|------|------|--------|
| `docs/adr/0012-codegen-agents-claudemd.md` | nouveau ADR | +130 lignes |
| `docs/adr/0013-co-evolution-discipline.md` | nouveau ADR | +120 lignes |
| `docs/adr/0014-canon-vs-extension.md` | nouveau ADR | +130 lignes |
| `docs/adr/0015-contract-lint-archetype-aware.md` | nouveau ADR | +120 lignes |
| `docs/adr/README.md` | index | +4 lignes |
| `docs/runs/2026-07-12_run11-multiservice-adr-p1/01_INTAKE.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run11-multiservice-adr-p1/05_PATCH_SUMMARY.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run11-multiservice-adr-p1/07_CLOSEOUT.md` | artefact | nouveau |
| `docs/ACTIVITY_LOG.md` | activity log | +1 ligne |

**Total** : 9 fichiers (4 nouveaux ADR + 1 index + 3 artefacts + 1 log entry)

---

## 7. Verification (pre-merge gate REQUIS, route STRUCTURED)

```bash
# P.R2 §1 — Lint (ne doit pas casser)
python tools/vbb-contract-lint.py
# Attendu : 0 erreur, 0 warning

# P.R2 §5 — Documentation coherence
ls docs/adr/001[2-5]-*.md
# Attendu : 4 fichiers présents (0012, 0013, 0014, 0015)
grep -c "^| \[001[2-5]\]" docs/adr/README.md
# Attendu : 4 références

# Sanity check : canon non lié intact
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md tools/vbb-contract-lint.py tools/vbb-architecture.py tools/vbb-multiservice-lint.py
# Attendu : vide
```

---

## 8. Acceptance criteria

Run 11 est **COMPLET** si :

- ✅ 4 ADR créés (`docs/adr/001[2-5]-*.md`)
- ✅ Chaque ADR suit le template
- ✅ Chaque ADR a ≥ 2 alternatives rejetées
- ✅ `docs/adr/README.md` mis à jour avec 4 références
- ✅ Aucun canon non lié touché
- ✅ Aucun outil / template / skill créé
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
- [`../../../docs/adr/0005-db-orientation-context-extension.md`](../../../adr/0005-db-orientation-context-extension.md) — ADR Gap-01 (dépendance Gap-11)
- [`../../../docs/adr/0006-project-archetype-context-extension.md`](../../../adr/0006-project-archetype-context-extension.md) — ADR Gap-02 (dépendance Gap-11)