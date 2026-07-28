---
run_id: "2026-07-28_1400_m2-adversarial-loop-implementation"
phase: "MIGRATION_DOC"
status: "PARTIAL"
---

# Migration — Adoption de la boucle adversariale v1.1

> **Statut.** Document de migration pour l'adoption de
> `adversarial_governance_version: "1.1"` (ADR 0051).

## Cutoff

```yaml
adversarial_governance_version: "1.1"
cutoff_run_key: "2026-07-28_1400"
cutoff_timestamp: "2026-07-28T14:00:00Z"
```

À partir du cutoff :

- Les runs déclarent `adversarial_governance_version: "1.1"` dans
  `01_INTAKE.md` et `07_CLOSEOUT.md`.
- Les closeouts portent un bloc `adversarial` valide, ou une
  déclaration `A0` valide (avec raison explicite).
- Les 5 commandes P.R2 incluent désormais les deux lignes
  conditionnelles de `5b` (vérificateur adversarial + exécution du
  corpus). Avant le cutoff, le bloc retourne code 0 même si les deux
  lignes sont sautées. **Compatibilité ascendante préservée.**

## Sémantique héritage

| Statut | Signification post-cutoff |
|---|---|
| `UNASSESSED_LEGACY` | Sujet pré-cutoff qui n'a jamais été évalué adversarialement. **Distinct de `NOT_CERTIFIED`**. Pas un échec. |

Aucun run pré-cutoff n'est réécrit, ré-évalué ou rétrogradé.

## Phases de migration (rappel du plan M0 §M0..M6)

| Phase | Statut M2 | Note |
|---|---|---|
| **M0 — Design** | ✅ Clos (run `2026-07-28_1002`) | Auto-revue PARTIAL |
| **M1 — Décisions normatives** | ✅ Clos (run `2026-07-28_1200`) | 6 décisions arbitrées |
| **M2 — Implémentation structurée** | ✅ Clos PARTIAL (ce run) | Tier 1-2 implémentés ; Tier 3-7 différés (cf. `M2_DEFERRED_ITEMS.md`) |
| **M3 — Bootstrap du corpus** | ⏸ Différé | Repose sur le validateur + corpus (Tier 3-6) |
| **M4 — Ramp d'enforcement** | ⏸ Différé | R0 actif dès Tier 3 livrés |
| **M5 — Distribution propagation** | ⏸ Différé | CR#12 — 4 distributions |
| **M6 — Disponibilité aux consommateurs** | ⏸ Différé | Documentation adoption |

## Compatibilité ascendante (vérifications explicitement satisfaites)

- ✅ **Aucune règle M1 modifiée** — toutes les modifications du canon
  sont strictes consommatrices de M1-01..M1-06.
- ✅ **Anciens workflows intacts** — `pre-merge-gate.md` reste canonique ;
  les deux lignes conditionnelles de `5b` ne s'activent qu'après le
  cutoff, et `pytest tests/ -q` reste à 255 passed, 1 skipped.
- ✅ **Projets existants migrables** — schéma v1.1 additif (ADR 0050
  §Compatibility), readers v1.0 restent conformants tant qu'ils ne
  voient pas une valeur d'enum étendue.
- ✅ **Documentation cohérente** — cross-références entre
  `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (domaine) et
  `GATE_ASSURANCE_GOVERNANCE.md` (schéma) sont explicites.
- ✅ **Aucun doublon d'autorité** — split strict (M1-01 Option C) :
  une seule autorité par concept. Pas de copie concurrente entre
  canon et run documents.

## Validation P.R2 (déjà green — cf. §Vérification P.R2 du closeout)

| # | Vérification | Statut |
|---|---|---|
| 1 | `vbb-architecture.py lint` | PASS (0 errors, 11 blocks) |
| 2 | `vbb-architecture.py graph --write` | PASS (RELATIONS.md regenerated) |
| 3 | `vbb-contract-lint.py` | PASS (0 errors) |
| 4 | `vbb-loop-closure-check.py <run> --strict` | à exécuter en closeout |
| 5 | `pytest tests/ -q` | PASS (255 passed, 1 skipped) |
| 5b | adversarial gate + corpus | N/A (pre-cutoff effective) |

## Adoption par les consommateurs

Chaque consommateur (projet satellite ou distribution) ouvre son propre
run pour adopter le contrat v1.1 — Vibebackbone ne réécrit personne.

```yaml
consumer_run:
  voie: AUDIT  # mandatory per ADR 0050 §Compatibility
  intake: declare adversarial_governance_version: "1.1"
  cutoff: <consumer_own_cutoff>
  strategy: phase-aligned with M2
```

## Risques de migration résiduels

| ID | Risque | Sévérité | Mitigation |
|---|---|---|---|
| MG-01 | Le validateur `vbb-adversarial-gate.py` n'existe pas encore ; les runs post-cutoff qui déclarent `A2` sont sans filet automatique | S2 | Créé en M2-BIS (cf. `M2_DEFERRED_ITEMS.md` Tier 3) |
| MG-02 | Les 4 distributions ne référencent pas encore la nouvelle autorité | S2 | Propagé en M2-BIS (Tier 7) |
| MG-03 | Les tests adversariaux (13 conditions + corpus + A2 proxy) sont absents | S1 | Ajoutés en M2-BIS (Tier 6) |
| MG-04 | Le corpus lui-même n'est pas encore bootstrapé | S2 | Bootstrap en M3 (run dédié) |

Aucun de ces risques n'est **bloquant** pour les runs existants. Ils
sont des dettes assumées vers M2-BIS et M3.

## Handoff

Le présent run produit :
- 1 ADR (M2-01)
- 1 autorité canonique nouvelle (M2-02)
- 5 fichiers canoniques étendus (M2-03 + 4 extensions Tier 2)
- 1 nouveau bloc `5b` au P.R2 canon
- 31 entrées M2-NN tracées comme différées (`M2_DEFERRED_ITEMS.md`)
- 1 cutoff actif (`2026-07-28T14:00:00Z`)

Le prochain run **M2-BIS** consomme `M2_DEFERRED_ITEMS.md` et la
même source unique `M1_DECISIONS.md`.
