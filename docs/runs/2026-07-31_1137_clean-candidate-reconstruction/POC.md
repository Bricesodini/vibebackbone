---
run_id: "2026-07-31_1137_clean-candidate-reconstruction"
phase: "POC"
type: "poc"
status: "active"
---

# POC — reconstruction de pré-candidat et liaison exacte

## Hypothèse

Une branche neuve issue de `6b0daf4785d652b23931b80aafba57979e69d9b4`, alimentée par des commits atomiques bornés, peut produire un sujet mesurable sans dépendance à `latest`, au HEAD implicite ou à un worktree externe.

## Périmètre et méthode

- Comparer les arbres et diffs avant reprise.
- Exécuter les tests négatifs des parseurs, corpus et liaisons exactes.
- Valider dans un clone `--no-local` avec SHA et run déclarés.
- Ne pas produire de tag, merge, push ou certification.

## Critères de sortie

- Provenance et arbre propres, tous les rapports déclarant le même `repository_sha` et `run_id`.
- Les erreurs de liaison produisent `UNKNOWN`, `ERROR` ou `FAIL`, jamais un verdict favorable.
- Les findings confirmés possèdent une entrée corpus et un verrou de non-régression.

## Décision: GO

Le POC est borné, falsifiable et nécessaire avant l’intégration; il autorise l’exécution technique du pré-candidat, sans autoriser une publication ou une certification.
