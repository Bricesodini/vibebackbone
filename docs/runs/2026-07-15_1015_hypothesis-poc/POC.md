---
template_id: "POC"
version: "1.0"
lane_eligible:
  - "AUDIT"
---

# POC — hypothesis-poc-campaign

**Statut**: IN_PROGRESS
**Date**: 2026-07-15
**Liée à ADR**: `ADR.md`
**Liée à RUN**: `docs/runs/2026-07-15_1015_hypothesis-poc/`

## Hypothèse

Nous supposons que les dix propositions du contre-audit peuvent être départagées
par des tests isolés, reproductibles et moins coûteux qu'une intégration directe.

## Plan de POC

| ID | Test isolé | Critère GO |
|---|---|---|
| H-001 | Reclasser 5 findings existants avec les niveaux actuels et le cycle proposé | aucune conséquence non reproduite n'est déclarée validée |
| H-002 | Décomposer 10 findings multi-claims en sous-claims | meilleure précision sans coût moyen > 2x |
| H-003 | Comparer validateurs génériques et validateur d'autorité sur corpus Next/Docker/API | au moins 1 défaut réel détecté uniquement par l'autorité |
| H-004 | Appliquer matrice diagnostic/preuve à 10 findings | au moins 2 décisions améliorées sans ambiguïté de statut |
| H-005 | Exécuter un contre-audit ciblé sur 4 findings | coût < 50% d'un audit complet, périmètre stable |
| H-006 | Séparer validation primaire et découvertes secondaires dans le même rapport | zéro dérive d'action hors périmètre |
| H-007 | Scanner un corpus temporaire de noms/contenus LLM | détection utile, zéro suppression automatique, faux positifs classés |
| H-008 | Rejouer le traitement de 5 orphelins | aucun orphelin supprimé par inférence seule |
| H-009 | Annoter 10 commandes avec résultat/couverture/limitation/blocage | aucune conclusion globale à partir d'un test partiel |
| H-010 | Comparer synthèses longues vs synthèses structurées sur mêmes preuves | meilleure décision, sans métrique de longueur comme objectif |

## Règle de décision

- **GO** : critère atteint et bénéfice observable.
- **NO-GO** : critère non atteint ou duplication manifeste.
- **PIVOT** : signal utile mais format ou périmètre à réduire.

## Résultat observé

Le runner isolé retourne **10/10** mécanismes passants. Les contrôles dépôt
retournent `232 passed, 1 skipped`, contract lint sans erreur, architecture lint
sans erreur et credentials gate PASS. Ce résultat valide la faisabilité des
formats, mais pas encore leur ROI sur des projets réels.

| Groupe | Résultat |
|---|---|
| H-001, H-002, H-004 | PIVOT : format faisable, coût/ambiguïté à mesurer |
| H-003 | PIVOT : fixture framework réelle manquante |
| H-005, H-006 | PIVOT : à rejouer sur un contre-audit réel |
| H-007 | PIVOT : corpus filesystem réel manquant |
| H-008, H-009, H-010 | GO / déjà couvert, aucune intégration nécessaire |

## Décision

Voir `02_AUDIT_REPORT.md` pour les décisions détaillées et les POC réels restant
à exécuter.

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: PIVOT
adr_link: "ADR.md"
hypothesis_validated: partial
metric_observed: "10/10 mechanics; 232 passed, 1 skipped"
metric_threshold: "per hypothesis table"
reproducible: true
verified_at: "2026-07-15T10:42:00+02:00"
verified_by: "codex"
```
