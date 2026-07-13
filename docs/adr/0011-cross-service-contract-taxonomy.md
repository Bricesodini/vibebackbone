---
template_id: "ADR"
version: "1.0"
lane_eligible:
  - "STRUCTUREE"
  - "AUDIT"
related:
  - "docs/adr/README.md"
  - "docs/CONVENTIONS.md#pr3--gate-before-action"
---

# ADR — 0011-cross-service-contract-taxonomy

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-10  
**Liée à POC**: vide

## Contexte

Le skill `1-vbb-api-contract-designer` produit aujourd'hui des contrats (CONTRACT.yaml, schéma, outputs) qui décrivent ce qu'un service **expose**. Mais aucun champ ne capture explicitement **qui consomme** ce contrat. Conséquence : la discipline multi-service est unilatérale — le producteur déclare son API sans savoir qui la consomme, et le consommateur documente sa consommation (cf. ADR-0007) sans référence explicite au contrat producteur.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-10 : `1-vbb-api-contract-designer/SKILL.md` ligne 61 mentionne « existing or planned consumers » comme **optional input** (pas comme artefact persistant). Idem pour `2-vbb-api-auditor/SKILL.md` ligne 57.

Conséquence concrète : impossible de fermer la boucle `producer ↔ consumer` au niveau framework. Le linter multi-service (ADR-0009) ne peut pas valider la cohérence des deux côtés.

## Décision

**Étendre `1-vbb-api-contract-designer` pour ajouter un champ obligatoire `Consumers` dans le `CONTRACT.yaml` produit, typé selon une taxonomie canonique.**

### Schéma du champ `consumers`

```yaml
# Dans CONTRACT.yaml — outputs.artifact.kind = "contract_schema"
consumers:
  - service: <slug>           # ex. "studio-auth"
    type: <internal | external>
    version_pinned: <semver>  # ex. "v2.1"
    contract_consumed_ref: <path to docs/CONTRACTS_CONSUMED.md of that service>
    criticality: <critical | medium | low>   # hérité de CONTRACTS_CONSUMED, dupliqué pour query rapide
```

### Taxonomie canonique du champ `type`

| Valeur | Sens |
|--------|------|
| `internal` | Consommateur dans le même écosystème (même organisation, même réseau) |
| `external` | Consommateur tiers (autre organisation, public, etc.) |

### Validation croisée

Le champ `consumers` est validé en miroir avec `CONTRACTS_CONSUMED.md` (cf. ADR-0007) du service consommateur :
- Pour chaque `consumers[*]`, il existe une entrée correspondante dans `CONTRACTS_CONSUMED.md` du service cible.
- Le champ `criticality` doit correspondre.

Cette validation est outillée par `vbb-multiservice-lint.py` (cf. ADR-0009, règle `consumers_cross_ref`).

### Modifications du skill `1-vbb-api-contract-designer`

1. **PROCESS** : nouvelle étape obligatoire « Identify consumers » — l'architecte déclare les consommateurs connus ou `null` (si le service n'a pas encore de consommateurs).
2. **OUTPUT CONTRACT** : le template `CONTRACT.yaml` inclut le bloc `consumers:` avec liste vide par défaut.
3. **VALIDATION LOOP** : vérification que `consumers` est défini (peut être `[]`), pas absent.
4. **EXAMPLES** : ajout d'un exemple concret avec 2 consumers typés.

### Modifications symétriques de `2-vbb-api-auditor`

Le skill `2-vbb-api-auditor` doit vérifier que les `consumers` déclarés sont à jour (toujours actifs) et que la cohérence avec les `CONTRACTS_CONSUMED.md` correspondants est respectée. C'est la garantie du **double-écriture** (producer + consumer).

## Conséquences

### Positives
- La boucle `producer ↔ consumer` est fermée au niveau framework.
- L'analyse d'impact cross-service devient exhaustive (tous les producteurs savent qui ils nourrissent).
- Le linter multi-service (ADR-0009) peut valider la cohérence des deux côtés.
- La discipline devient vérifiable outillée (vs conversationnelle).

### Négatives / coûts
- Tous les `CONTRACT.yaml` existants doivent être enrichis (migration ponctuelle, ~5 minutes par service).
- Le skill `1-vbb-api-contract-designer` doit être modifié (modification du canon skill — Run 10+).
- Le skill `2-vbb-api-auditor` doit être modifié symétriquement.
- La taxonomie `internal/external` est un enum extensible (peut grandir).

### Neutres
- `CONTRACTS_PROVIDED.md` (symétrique côté producteur) reste à définir dans un ADR futur.
- `t-vbb-impact-analyzer` peut être étendu pour exploiter `consumers` (out of scope ce run).

## Alternatives rejetées (≥ 2)

### Alternative A — Inférer les consumers depuis `CONTRACTS_CONSUMED.md` (sans déclaration explicite)
- **Description** : ne pas demander au producteur de déclarer ses consumers ; inférer la liste en croisant tous les `CONTRACTS_CONSUMED.md`.
- **Pourquoi rejetée** : inférence fragile (pas tous les projets déclarent encore `CONTRACTS_CONSUMED.md` — bootstrapping). Déclaration explicite est plus robuste.

### Alternative B — Champ optionnel `consumers` (non obligatoire)
- **Description** : garder le champ optionnel comme aujourd'hui.
- **Pourquoi rejetée** : optionnel = jamais rempli. L'objectif est de fermer la boucle, ce qui demande l'obligation.

### Alternative C — Stocker dans un fichier séparé `CONTRACT_CONSUMERS.yaml`
- **Description** : nouveau fichier par contrat, séparé du `CONTRACT.yaml`.
- **Pourquoi rejetée** : dispersion. Le `CONTRACT.yaml` est déjà l'artefact canonique du contrat ; étendre ce fichier est plus cohérent.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Les producteurs existants ne déclarent pas leurs consumers | forte | moyen | Le skill `1-vbb-api-contract-designer` exige le champ à la prochaine utilisation ; un script de migration (out of scope) peut pré-remplir |
| Incohérence entre `consumers` (producer) et `CONTRACTS_CONSUMED.md` (consumer) | moyenne | moyen | Le linter multi-service (ADR-0009) détecte l'incohérence |
| Le champ `criticality` est dupliqué (déjà dans `CONTRACTS_CONSUMED.md`) | faible | faible | Acceptable — la duplication est mineure et permet une query rapide côté producer |

## Hypothèses

- L'enum `type: internal | external` est suffisant pour le cas d'usage actuel.
- Les `CONTRACT.yaml` existants sont en nombre limité (peu de services multi-service aujourd'hui).
- Le skill `1-vbb-api-contract-designer` est l'endroit canonique pour la déclaration ; pas d'autre voie.

## Références

- ADR lié (dépendance) : [`0007-contracts-consumed-canonical-file.md`](0007-contracts-consumed-canonical-file.md)
- ADR lié (consommateur du champ) : [`0009-multiservice-lint-discipline.md`](0009-multiservice-lint-discipline.md)
- Skills liés :
  - [`skills/1-vbb-api-contract-designer/SKILL.md`](../../skills/1-vbb-api-contract-designer/SKILL.md) (cible modification)
  - [`skills/2-vbb-api-auditor/SKILL.md`](../../skills/2-vbb-api-auditor/SKILL.md) (cible modification symétrique)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-10
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - "0007-contracts-consumed-canonical-file.md"
blocks:
  - "1-vbb-api-contract-designer modification (Run 10+)"
  - "2-vbb-api-auditor modification (Run 10+)"
  - "0009-multiservice-lint-discipline.md (validation cross-ref)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```