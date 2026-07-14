---
run_id: "2026-07-14_1615_ready-risk-reconciliation"
phase: "02_AUDIT"
voie: "STRUCTUREE"
status: "READY"
skill: "1-vbb-conventions"
date: "2026-07-14"
---

# Conventions reconciliation audit

## Goals

Requalifier les cinq risques résiduels contre le canon et les mécanismes
effectivement présents. Cet audit ne modifie ni code ni convention.

## Decisions (normative)

### Project structure

La structure canonique est cohérente et couverte par le lint architecture. Aucun
des cinq risques ne démontre un conflit de responsabilité entre modules.

### Naming

L'ambiguïté Python observée historiquement est résolue : Ruff sélectionne `E7`
et `ruff check tools tests --select E741` passe à zéro. Le code Python suit
`snake_case`, interprétation « applicable au langage cible » du canon.

### Imports & boundaries

Hors scope : aucune dérive d'import ou de frontière n'est associée aux cinq
risques étudiés.

### Configuration

Ruff et mypy sont configurés dans `pyproject.toml`, exécutés localement et dans
la CI. `mypy tools` passe à zéro.

### Logging / debug

Hors scope : aucune dérive de logging/debug n'est associée aux cinq risques.

### Documentation

- Le corpus contient encore de nombreuses instructions de prompt en français,
  y compris sous `prompts/canonical/`; il diverge donc littéralement de la règle
  « prompts English only ». Aucun défaut de routage ou de comportement causé
  par cette langue n'est toutefois démontré. Une traduction globale serait un
  changement comportemental non mécanique et reste hors scope.
- 42 fonctions Python de `tools/` et `tests/` dépassent 40 lignes selon l'AST,
  dont plusieurs orchestrateurs CLI. La longueur est un signal, pas une preuve
  de responsabilités multiples. Les chemins critiques sont couverts par la
  suite et les gates ; toute décomposition future doit partir d'un défaut de
  testabilité, de lisibilité ou de responsabilité observé.
- Rule 11 impose déjà ADR + POC + Integration Gate aux travaux non triviaux.
  Le défaut SYS-POC-004 est historique ; le déclencheur futur pertinent est une
  transition canon/architecture/cross-service sans décision durable.
- SYS-SUB-003 est conditionnel à une délégation. L'acceptation s'accompagne des
  quatre contrôles sémantiques existants dans le finding : comptes, citations,
  contradictions et diff sortie→intégration.
- QA-004 et QA-005 sont des risques LOW de finesse de traçabilité, sans échec
  actif. Automatiser tous les générateurs ou créer des ADR par comptage serait
  prématuré.

## Drift checklist

- [x] Ambiguïté de noms Python : résolue mécaniquement par E741 à zéro.
- [x] Fonctions longues : signal réel, aucune décomposition générique justifiée.
- [x] Prompts français : divergence littérale confirmée, impact non démontré.
- [x] Transition POC : gate canonique présent ; surveiller les transitions futures.
- [x] Réintégration : contrôle sémantique requis seulement lorsqu'il y a délégation.
- [x] Provenance/ADR fins : risques LOW bornés, sans action immédiate.

## Migration plan (mechanical)

1. Ne lancer aucune migration globale dans `tools/` ou `prompts/` sur ces seuls
   signaux.
2. Appliquer E741 et mypy via `pyproject.toml`, CI locale et CI distante.
3. Lorsqu'une longue fonction de `tools/` est touchée, vérifier responsabilité
   unique et testabilité avant de décider une extraction.
4. Lorsqu'un prompt est touché ou qu'une cible anglophone est annoncée, décider
   explicitement langue et migration dans le run concerné.
5. Pour une délégation future, inclure comptes, citations, contradictions et
   diff d'intégration dans les critères d'acceptation.
6. Pour toute transition canon/architecture/cross-service post-POC, exiger une
   décision durable liée.
7. Réexaminer génération de provenance et seuil ADR uniquement lors d'un
   changement dédié des générateurs ou de la politique d'architecture.

## Unknowns / open questions

Aucun bloquant pour Wave 4. La readiness globale reste conditionnée par la
revalidation indépendante prévue en Wave 5.

## Verdict

**READY** — conventions lisibles ; écarts résiduels acceptables uniquement avec
owners et déclencheurs explicites dans la décision et le registre.

```yaml
FINAL_STATUS:
  verdict: COMPLETE
  tests_run:
    - "python -m ruff check tools tests --select E741"
    - "mypy tools"
  tests_missing: []
  risks:
    - "French prompt corpus remains a literal convention variance"
    - "42 functions exceed the indicative 40-line target"
  open_points:
    - "Independent READY revalidation remains Wave 5"
```
