---
run_id: "2026-08-03_f03-revision"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-08-03T00:00:00Z"
ended_at: null
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/runs/2026-08-03_f03-provenance-alignment/06_INDEPENDENT_REVIEW.md"
artifacts_produced:
  - "04_PLAN.md"

implementation_authorization:
  status: "AUTHORIZED"
  required_gate_ids: ["f03-revision-scope"]
  reasons: ["Décision humaine explicite limitée aux deux findings F03 confirmés."]

adr_status:
  adr: "docs/adr/0053-a2-a3-assurance-alignment.md"
  verdict: "PASS"

poc_status:
  poc: "not-required-doc-revision"
  verdict: "GO"
---

# 04_PLAN — F03-REVISION

| # | Action | Fichier cible | Validation |
|---|---|---|---|
| 1 | Retirer l’obligation résiduelle de proxy distinct du chemin v1.2 | `distributions/pi/SYSTEM.md` | Revue textuelle contre ADR-0053 |
| 2 | Fixer `updated` à la dernière révision gouvernée pertinente | `distributions/pi/SYSTEM.md` | Comparaison avec ADR-0053 `2026-07-31` |
| 3 | Vérifier la représentation racine | `SYSTEM.md` | `readlink`, `cmp`, hash |
| 4 | Exécuter la revue A2 et les linters concernés | run et dépôt | gate adversarial, tests, linters |

Rollback : restaurer uniquement les deux lignes modifiées de
`distributions/pi/SYSTEM.md`; aucune autre surface n’est concernée.

## Objectif

Conserver la trace de la révision ciblée de F-03, limitée à la représentation
SYSTEM et à sa métadonnée, sans modifier l’autorité ADR ni le candidat
documentaire.

## Pré-conditions

- décision humaine F-03 explicite et bornée ;
- ADR-0053 disponible comme autorité de comparaison ;
- absence d’autorisation d’adoption canonique, de merge ou de publication ;
- les findings hors périmètre restent ouverts ou différés.

## Étapes ordonnées

1. Ancrer les deux modifications autorisées.
2. Vérifier la source et la représentation racine SYSTEM.
3. Rejouer la revue A2 ciblée et les validations applicables.
4. Enregistrer le finding résiduel et arrêter le run si le périmètre est
   dépassé.

## Critères d'acceptation

- seules les deux corrections autorisées sont évaluées ;
- les résultats passants et les findings résiduels sont distingués ;
- aucune adoption ni intégration n'est revendiquée ;
- l'état bloqué reste explicite si une autorité hors périmètre demeure
  ambiguë.

## Plan de rollback global

Restaurer les deux lignes ciblées de `distributions/pi/SYSTEM.md` et annuler
uniquement les artefacts de ce run ; ne pas modifier ADR-0053, les fondations
documentaires ni `main`.

## Risques identifiés

- la revue peut confirmer un drift hors périmètre ;
- la validation de SYSTEM ne certifie pas le runtime Pi déployé ;
- le résultat ne permet pas à lui seul l'adoption canonique.
