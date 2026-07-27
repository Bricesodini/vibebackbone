---
run_id: "2026-07-27_2117_design-certification-gates-governance-audit"
phase: "03_OPTIONS"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-27T19:21:46Z"
ended_at: "2026-07-27T19:35:55Z"
revised_at: "2026-07-27T19:35:55Z"
next_phase: "04_RECOMMENDATION"
artifacts_consumed:
  - "02_ANALYSIS.md"
artifacts_produced:
  - "03_OPTIONS.md"
---

# 03_OPTIONS — Gate taxonomy

## Critères

1. Clarté sémantique.
2. Absence de faux signal d'instabilité.
3. Fail-closed sur l'autorisation d'implémentation.
4. Compatibilité historique et outillée.
5. Respect des sept phases.
6. Coût cognitif et opérationnel proportionné.

## Option A — Statu quo avec explication narrative

Conserver les verdicts actuels et demander aux auteurs de préciser librement
la nature de chaque échec.

### Bénéfices

- Aucun coût de migration.
- Aucun risque immédiat pour les parseurs.

### Risques

- La distinction reste non déterministe et non vérifiable.
- Les dashboards et handoffs continuent d'agréger des objets différents.
- La qualité dépend du style de chaque reviewer.

### Évaluation

**PARTIAL** — acceptable à court terme, insuffisant pour résoudre la question.

## Option B — Remplacer `FAIL` par des verdicts spécialisés

Introduire `DESIGN_FAIL`, `CERTIFICATION_FAIL`, `DESIGN_PASS`, etc., et
remplacer les verdicts génériques.

### Bénéfices

- Lecture humaine immédiate.
- Qualification explicite dans une seule chaîne.

### Risques

- Migration cassante des outils, schémas et projets.
- Explosion du vocabulaire combinatoire.
- Conflit avec ADR 0043 si ces valeurs sont réutilisées comme statuts runtime.
- Un gate couvrant plusieurs dimensions reste difficile à représenter.

### Évaluation

**BLOCKED** — coût et risque disproportionnés.

## Option C — Qualifier le gate et ajouter des dimensions d'assurance

Conserver le verdict existant et ajouter :

- un identifiant de gate;
- `gate_family: DESIGN|CERTIFICATION|OTHER`;
- des états d'assurance séparés;
- une autorisation d'implémentation explicite et motivée.

### Bénéfices

- Résout l'ambiguïté sans casser le vocabulaire.
- Compatible avec ADR 0043.
- Permet aux interfaces d'afficher « design fermé, certification en attente ».
- Supporte une adoption progressive et des historiques legacy.

### Risques

- Plusieurs champs doivent rester cohérents.
- Une règle de projection vers le verdict global est nécessaire.
- Les checklists et outils devront être versionnés dans un run futur.

### Évaluation

**READY sous conditions** — meilleur rapport clarté/compatibilité.

## Option D — Deux machines de phases ou un gate autonome Knowledge Harvest

Créer des phases Design/Certification séparées, voire une phase supplémentaire
pour le Harvest.

### Bénéfices

- Séparation procédurale maximale.

### Risques

- Casse l'invariant des sept phases.
- Duplique les responsabilités de REVIEW et CLOSEOUT.
- Transforme une taxonomie d'assurance en nouvelle orchestration.
- Contredit la décision récente de conserver le Harvest dans `07_CLOSEOUT`.

### Évaluation

**REJECTED**.

## Matrice

| Option | Clarté | Compatibilité | Fail-closed | Coût | Verdict |
|---|---:|---:|---:|---:|---|
| A — statu quo | faible | forte | moyen | faible | PARTIAL |
| B — nouveaux verdicts | forte | faible | moyen | fort | BLOCKED |
| C — qualification additive | forte | forte | forte | moyen | READY |
| D — nouvelles phases | forte | faible | forte | très fort | REJECTED |
