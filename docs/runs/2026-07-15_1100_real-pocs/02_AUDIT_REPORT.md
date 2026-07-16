---
run_id: "2026-07-15_1100_real-pocs"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "codex"
started_at: "2026-07-15T11:00:00+02:00"
ended_at: "2026-07-15T11:18:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "ADR.md"
  - "POC.md"
artifacts_produced:
  - "02_AUDIT_REPORT.md"
---

# 02_AUDIT_REPORT — Real hypothesis POCs — 20260715

**Scope**: H-003, H-005, H-006 et H-007.
**Méthode**: fixtures temporaires, commandes réelles, lecture seule du dépôt.

## Résultats

| Hypothèse | Evidence | Résultat | Décision |
|---|---|---|---|
| H-003 | API stdlib démarrée et `/health` vérifiée ; Next CLI absente ; daemon Docker indisponible ; FastAPI importable mais non démarrable à cause d'une incompatibilité Starlette (`on_startup`) | `PIVOT` | Le principe est utile, mais le critère « deux familles réelles » n'est pas atteint. Rejouer dans un environnement Next/Docker authentifié. |
| H-005 | Quatre findings réels sélectionnés depuis `systemic-risks-20260713-2355.md` ; aucune baseline de durée/coût comparable | `PIVOT` | La sélection ciblée est faisable, mais l'efficacité n'est pas prouvée. |
| H-006 | Le rapport réel sépare quatre findings primaires d'un secondaire mis en backlog ; aucune action automatique secondaire | `PIVOT` | Le mécanisme est compatible avec le périmètre, mais sa valeur doit être observée pendant un vrai contre-audit reproductif. |
| H-007 | 1 091 chemins suivis, aucun nom suspect, 5 occurrences de contenu classées faux positifs connus, 0 suppression | `PIVOT` | Le scan est sûr et utile pour le triage, mais aucun vrai positif ne permet de mesurer le rappel. |

## Détails H-003

Le profil d'autorité a été appliqué conceptuellement : `next build + route
smoke`, `docker build`, et démarrage + requête HTTP pour une API. La fixture API
stdlib a répondu correctement. La tentative FastAPI a révélé une incompatibilité
de versions au démarrage, ce qui confirme qu'un simple import vert n'est pas une
preuve d'exécutabilité. En revanche, l'absence de Next CLI et du daemon Docker
empêche une conclusion complète.

## Détails H-005 / H-006

Les quatre identifiants `SYS-POST-001` à `SYS-POST-004` ont été sélectionnés
comme validation primaire. Un élément secondaire a été conservé avec l'action
`backlog`; aucune dérive automatique n'a été déclenchée. Le critère de coût
reste inconnu : aucun audit complet comparable n'a été exécuté dans la même
session.

## Détails H-007

Le corpus `git ls-tree -r HEAD` contient 1 091 chemins. Aucun nom ne correspond
aux motifs `<|...|>`, `tool_call` ou blocs `BEGIN_/END_`. Cinq contenus contiennent
ces chaînes dans des documents ou outils qui les expliquent explicitement ; ils
ont été classés faux positifs. Le runner n'a effectué aucune suppression.

## Verdict global

**PARTIAL / PIVOT**. Aucun POC réel ne justifie encore une intégration du cœur.
H-006 est le plus proche d'un GO fonctionnel, mais il reste à prouver sur une
validation où un secondaire est découvert naturellement et où le coût est
mesuré. H-003 doit être rejoué dans un environnement disposant de Next.js et
Docker ; H-007 doit être évalué sur un corpus contenant des vrais positifs
contrôlés.

## FINAL_STATUS

```yaml
EXTENSION_REQUEST:
  reason: "Trois POC réels et la consolidation documentaire ont dépassé le budget initial."
  additional_time_seconds: 300
  scope_unchanged: true
  next_bounded_step: "Consolider les verdicts et fermer la run sans intégration Core."
  risk_changed: false
```

```yaml
FINAL_STATUS:
  elapsed_seconds: 420
  budget_initial: 180
  progress_emitted: true
  progress_count: 1
  extension_requested: true
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - "docs/runs/2026-07-15_1100_real-pocs/"
  tests_run:
    - "API fixture startup + HTTP /health"
    - "Next CLI availability probe"
    - "Docker daemon probe"
    - "4 real findings selected and separated"
    - "1,091 tracked paths filesystem scan"
  tests_missing:
    - "Next.js build + route smoke"
    - "Docker build"
    - "Comparable full-audit timing"
    - "Controlled true-positive contamination corpus"
  risks:
    - "Environment limitations prevent three definitive GO verdicts."
  open_points:
    - "Re-run H-003 with Next/Docker available."
    - "Run H-005/H-006 on a naturally discovered secondary finding."
    - "Measure H-007 recall/false-positive rate on a controlled corpus."
```
