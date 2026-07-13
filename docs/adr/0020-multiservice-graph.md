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

# ADR — 0020-multiservice-graph

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-13  
**Liée à POC**: vide  
**Liée à ADR amont**: 0007 (CONTRACTS_CONSUMED, fournit les données intra-repo), 0018 (MULTIREPO, fournit les données cross-repo)

## Contexte

Vibebackbone a besoin de visualiser les interdépendances entre services (multi-service intra-repo ou multi-repo). Aujourd'hui, aucun outil ne génère ce graphe — l'architecte le reconstruit à la main ou via des outils tiers (Mermaid, draw.io).

Conséquence : impossible de détecter visuellement les cycles (service A dépend de B qui dépend de A), les services isolés (orphelins), ou les hubs (services avec beaucoup de dépendances). L'analyse d'impact reste cognitive.

## Décision

**Créer `tools/vbb-multiservice-graph.py` qui consomme les sources canoniques et génère le graphe des interdépendances.**

### Sources de données

| Source | Données extraites |
|--------|-------------------|
| `docs/CONTRACTS_CONSUMED.md` (ADR-0007) | Edges : `provider → consumer` pour chaque contrat consommé |
| `docs/CONTRACTS_PROVIDED.md` (à définir) | Edges : `provider → consumer` symétriques |
| `docs/MULTIREPO.yaml` (ADR-0018) | Cross-repo edges si défini |

### Modes de sortie

| Mode | Sortie | Usage |
|------|--------|-------|
| `--text` | Résumé humain (liste de services + counts) | Lecture rapide |
| `--dot` | Format Graphviz (`.dot`) | Rendu visuel (via `dot -Tpng`) |
| `--json` | JSON machine-readable | Intégration dashboard |
| `--check-cycle` | Exit 0 si pas de cycle, exit 1 sinon | CI gate (cf. ADR-0021) |

### Algorithme

1. Lire toutes les sources canoniques.
2. Construire un graphe dirigé : nœuds = services, edges = contrats consommés.
3. Si `--check-cycle` : détecter les cycles (DFS).
4. Calculer des métriques (degré entrant, sortant, hubs, orphelins).
5. Sérialiser dans le format demandé.

### Visualisation recommandée

```
$ python tools/vbb-multiservice-graph.py --text
Services: 4
Edges: 7
Cycles: 0
Hubs: studio-auth (3 consumers)
Orphelins: studio-reports (0 deps)

$ python tools/vbb-multiservice-graph.py --dot | dot -Tpng > graph.png
# génère une image PNG du graphe
```

## Conséquences

### Positives
- Visualisation outillée des interdépendances.
- Détection automatique des cycles (intégrable en CI).
- Métriques dérivées (hubs, orphelins).

### Négatives / coûts
- Outil nouveau (~200 lignes Python).
- Dépend de `CONTRACTS_CONSUMED.md` (ADR-0007) — sans ce fichier, graphe vide.
- Le format DOT demande `graphviz` installé pour le rendu (mais optionnel).

### Neutres
- Aucun canon modifié.
- Le `CONTRACTS_PROVIDED.md` symétrique reste à définir (Run futur).

## Alternatives rejetées (≥ 2)

### Alternative A — Utiliser un outil externe (Mermaid live editor, draw.io)
- **Description** : l'architecte dessine le graphe à la main dans un outil externe.
- **Pourquoi rejetée** : non versionnable, non dérivable des sources canoniques, drift possible.

### Alternative B — Générer un fichier Markdown avec une table
- **Description** : produire `docs/SERVICE_GRAPH.md` (table Markdown).
- **Pourquoi rejetée** : pas de visualisation, juste une liste. Ne détecte pas les cycles.

### Alternative C — Script ad-hoc par projet
- **Description** : chaque projet écrit son propre script de graphe.
- **Pourquoi rejetée** : duplication d'effort, incohérence entre projets.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Graphe incomplet car `CONTRACTS_CONSUMED.md` n'est pas encore adopté | forte | moyen | Message « graphe partiel » si moins de X services détectés |
| Faux cycles dus à des références ambiguës | moyenne | faible | Le linter `vbb-multiservice-lint` (ADR-0009) valide la cohérence en amont |
| Le graphe devient trop gros pour être lisible | moyenne | faible | Mode `--dot` avec clustering ; filtres par sous-système |

## Hypothèses

- `CONTRACTS_CONSUMED.md` est adopté (ADR-0007) avant que le graphe ait du sens.
- `MULTIREPO.yaml` est optionnel (le graphe fonctionne en mono-repo).
- Les cycles détectés sont un signal (pas un fail par défaut — sauf `--check-cycle`).

## Références

- ADR amont : [`0007-contracts-consumed-canonical-file.md`](0007-contracts-consumed-canonical-file.md)
- ADR lié : [`0018-multirepo-support.md`](0018-multirepo-support.md)
- ADR consommateur : [`0021-ci-gate-enforcement.md`](0021-ci-gate-enforcement.md) (utilise `--check-cycle`)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-13
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - "0007-contracts-consumed-canonical-file.md"
  - "0018-multirepo-support.md"
blocks:
  - "tools/vbb-multiservice-graph.py (implémentation, Run 13+)"
  - "0021-ci-gate-enforcement.md (utilise --check-cycle)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```