---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run09-multiservice-adr-discipline
route: STRUCTURED
updated: 2026-07-12
---

# Run 09 — Multi-service ADR disciplinaire (Gap-04/06/10)

> **Route** : STRUCTURED
> **Effort** : M (~40 min, 3 ADR substantiels + index)
> **Risque canon** : faible (aucune modif directe de canon — ADR = documents de design)
> **Pre-merge gate** : REQUIS (route STRUCTURED)
> **Statut** : `READY — prêt à exécuter sur GO utilisateur`

---

## 1. Goal

Produire **3 Architecture Decision Records (ADR) vibebackbone** pour le **tiercé disciplinaire P0** identifié en Phase 1 multi-service : Gap-04, Gap-06, Gap-10. Chaque ADR documente la décision de design pour un outil ou un artefact canonique à créer. **Pas d'implémentation runtime** (out of scope per consigne §3, comme Run 8).

**Pourquoi "disciplinaire"** : ce tiercé forme le **noyau dur** de la discipline multi-service outillée. Sans ADR validés, l'implémentation runtime (Gap-04 `vbb-multiservice-lint.py`, Gap-06 `IMPACT_LOG.md`, Gap-10 extension du contract designer) ne peut pas démarrer sans risque de drift.

---

## 2. Findings source

| ID | Finding | Gap | Sévérité | Étape Phase 2 |
|----|---------|-----|----------|---------------|
| **Gap-04** | Pas de linter discipline multi-service | `01_GAP_ANALYSIS.md` | **P0** | Étape 3 (Outillage) |
| **Gap-06** | Pas d'IMPACT_LOG cumulatif | idem | **P0** | Étape 2 (Discipline) |
| **Gap-10** | Pas de taxonomie contrats cross-service | idem | **P0** | Étape 2 (Discipline) |

**Source** : [`docs/strategy/vbb-evolution-multi-service-support/`](../../../strategy/vbb-evolution-multi-service-support/) (Phase 1, ADR Run 8 = Gap-01/02/05/14)

**Dépendances (cf. ADR-0007)** : Gap-04 et Gap-06 consomment `docs/CONTRACTS_CONSUMED.md` (Gap-05/ADR-0007, ACCEPTED). Gap-10 étend `1-vbb-api-contract-designer` (skill existant, canon transversal).

---

## 3. Modifications (3 ADR + index)

### ADR-0009 — Linter discipline multi-service (Gap-04, P0)

**Fichier** : `docs/adr/0009-multiservice-lint-discipline.md`

**Décision** : créer `tools/vbb-multiservice-lint.py` qui valide, pour chaque projet multi-service, trois familles de règles :

1. **Pas d'accès direct DB cross-service** : si le projet déclare `db_orientation: shared_external_*`, grep les imports/sources pour interdire l'usage direct du client DB d'un autre service (sans passer par une API documentée).
2. **IMPACT_LOG à jour** : si `docs/IMPACT_LOG.md` existe (cf. ADR-0010), vérifier qu'au moins une entrée existe si le projet a des contrats consommés (cf. ADR-0007).
3. **CONTRACTS_CONSUMED à jour** : si `docs/CONTRACTS_CONSUMED.md` existe (cf. ADR-0007), vérifier `Last updated < 90 jours`.

Le linter consomme un fichier `docs/MULTISERVICE_DISCIPLINE.yaml` (par projet) qui configure quelles règles s'appliquent (allow-list / deny-list). Le linter est **non-bloquant par défaut** (warning seul), bloquant seulement si `--strict` (mode CI).

**Justification** : la discipline multi-service est aujourd'hui purement conversationnelle (cf. AUDIT-C et notre conversation). Un linter outillé permet de détecter les régressions avant merge.

### ADR-0010 — IMPACT_LOG cumulatif (Gap-06, P0)

**Fichier** : `docs/adr/0010-impact-log-cumulative.md`

**Décision** : créer un nouveau fichier canonique `docs/IMPACT_LOG.md` (par projet), maintenu cumulativement, qui trace chaque **changement de contrat** (own ou consumed) avec :

| Date | Type | Contrat | Avant | Après | Services impactés | Lien run |
|------|------|---------|-------|-------|-------------------|----------|
| 2026-07-15 | `breaking` | `GET /v1/users` | `v1` | `v2` | `studio-auth`, `studio-orders` | run-2026-07-15-… |

Le log est **append-only** (jamais d'édition rétroactive). Une skill `t-vbb-impact-log-update` est créée pour faciliter l'entrée (l'utilisateur remplit un formulaire, la skill formate la ligne).

**Justification** : sans log cumulatif, l'analyse d'impact cross-service est impossible à reconstruire a posteriori. Le log sert d'**historique vérifiable**.

### ADR-0011 — Taxonomie contrats cross-service (Gap-10, P0)

**Fichier** : `docs/adr/0011-cross-service-contract-taxonomy.md`

**Décision** : étendre `1-vbb-api-contract-designer` pour ajouter un champ obligatoire **`Consumers`** dans `CONTRACT.yaml` (outputs.artifact.kind = `contract_schema` ou similaire). Chaque consumer est typé :

```yaml
consumers:
  - service: <slug>
    type: <internal | external>
    version_pinned: <semver>
    contract_consumed_ref: <path to docs/CONTRACTS_CONSUMED.md>
```

Cette taxonomie rend le lien **producteur ↔ consommateurs** explicite, permettant à `vbb-multiservice-lint` (ADR-0009) de valider la cohérence : tout `consumers[*]` doit avoir une entrée correspondante dans `CONTRACTS_CONSUMED.md` du service cible.

**Justification** : sans cette taxonomie, la discipline multi-service est unilatérale (le producteur déclare ce qu'il expose, mais ne sait pas qui consomme). La taxonomie ferme la boucle.

---

## 4. Alternatives rejetées (considérées globalement)

Pour chaque ADR, ≥ 2 alternatives rejetées sont documentées dans le fichier. Pattern commun :

- **Alternative A** : « ne pas outiller, garder la discipline conversationnelle » — rejetée (régression silencieuse possible).
- **Alternative B** : « intégrer dans un outil existant (e.g. `vbb-contract-lint`) » — rejetée (séparation des concerns : `vbb-contract-lint` valide les contrats au niveau framework, `vbb-multiservice-lint` valide la discipline au niveau projet).

Pour les détails spécifiques à chaque ADR, voir le fichier correspondant.

---

## 5. Excluded

- ❌ **Implémentation runtime** des gaps — out of scope per consigne §3
- ❌ Création d'outils concrets (`tools/vbb-multiservice-lint.py`, `skills/t-vbb-impact-log-update/`) — Runs 10+
- ❌ Création de templates concrets (`docs/IMPACT_LOG.md.template`) — Runs 10+
- ❌ Modification effective de `1-vbb-api-contract-designer` (juste ADR sur l'extension) — Runs 10+
- ❌ ADR pour les gaps restants (Gap-03, 07, 08, 09, 11, 12, 13, 15) — Runs ultérieurs
- ❌ Modification du canon `CONVENTIONS.md` ou `PILOTAGE.md`

---

## 6. Files impact summary

| File | Type | Impact |
|------|------|--------|
| `docs/adr/0009-multiservice-lint-discipline.md` | nouveau ADR | +120 lignes |
| `docs/adr/0010-impact-log-cumulative.md` | nouveau ADR | +130 lignes |
| `docs/adr/0011-cross-service-contract-taxonomy.md` | nouveau ADR | +120 lignes |
| `docs/adr/README.md` | index | +6 lignes (3 lignes ADR) |
| `docs/runs/2026-07-12_run09-multiservice-adr-discipline/01_INTAKE.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run09-multiservice-adr-discipline/05_PATCH_SUMMARY.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run09-multiservice-adr-discipline/07_CLOSEOUT.md` | artefact | nouveau |
| `docs/ACTIVITY_LOG.md` | activity log | +1 ligne |

**Total** : 8 fichiers (3 nouveaux ADR + 1 index + 3 artefacts + 1 log entry)

---

## 7. Verification (pre-merge gate REQUIS, route STRUCTURED)

```bash
# P.R2 §1 — Lint (ne doit pas casser)
python tools/vbb-contract-lint.py
# Attendu : 0 erreur, 0 warning

# P.R2 §5 — Documentation coherence
ls docs/adr/000[9]|001[01]-*.md
# Attendu : 3 fichiers présents (0009, 0010, 0011)
grep -c "^| \[0009\]\|^| \[0010\]\|^| \[0011\]" docs/adr/README.md
# Attendu : 3 références

# Sanity check : canon non lié intact
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md tools/vbb-contract-lint.py skills/1-vbb-api-contract-designer/SKILL.md
# Attendu : vide
```

---

## 8. Acceptance criteria

Run 9 est **COMPLET** si :

- ✅ 3 ADR créés (`docs/adr/0009-*.md`, `0010-*.md`, `0011-*.md`)
- ✅ Chaque ADR suit le template
- ✅ Chaque ADR a ≥ 2 alternatives rejetées
- ✅ `docs/adr/README.md` mis à jour avec les 3 références
- ✅ Aucun canon non lié touché
- ✅ Aucun outil / template / skill créé (Run 10+)
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
- [`../../../docs/adr/0007-contracts-consumed-canonical-file.md`](../../../adr/0007-contracts-consumed-canonical-file.md) — dépendance ADR-0009/0010
- [`../../../skills/1-vbb-api-contract-designer/SKILL.md`](../../../skills/1-vbb-api-contract-designer/SKILL.md) — cible extension ADR-0011