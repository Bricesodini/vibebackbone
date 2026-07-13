# ADR — 0028-scoped-audit-protocol

**Status**: ACCEPTED
**Date**: 2026-07-13
**Route**: STRUCTUREE
**Décideurs**: Brice (GO roadmap V2), Claude (formalisation)
**Liée à**: ADR 0027 (V2-R1) ; findings AUDIT-A-001 / AUDIT-A-002
**Liée à POC**: aucune — pas d'hypothèse d'intégration à prototyper (gate : `poc_required=false`)

## Contexte

Les skills anti-slop (`1-vbb-code-janitor`, `1-vbb-tech-debt`,
`2-vbb-db-robustness`) produisent un rapport unique pour le repo entier. Sur un
projet à N blocs, les findings de natures différentes se mélangent et
l'actionnabilité s'effondre (AUDIT-A-001/002, vérifié aussi sur le projet
consommateur trame : monolithes et doublons frontend jamais remontés). Le
CONTRACT.yaml de janitor et tech-debt expose déjà `scope_filter` en input
optionnel, mais aucun SKILL.md ne le documente : le contrat promettait, le
prompt ignorait. Brice demande explicitement le choix de la granularité et des
passes itératives par petit scope.

## Décision

1. **Paramètre `scope` documenté** dans les trois SKILL.md : optionnel ; valeurs
   acceptées = id de bloc `docs/ARCHITECTURE.md`, chemin de répertoire, ou label
   métier explicite ; absent → analyse globale (comportement actuel, inchangé).
   Avec scope : l'analyse est restreinte au périmètre, le rapport est nommé
   `{skill}-{scope-slug}-{YYYYMMDD-HHMM}.md`, chaque finding porte son scope.
   `2-vbb-db-robustness/CONTRACT.yaml` gagne `scope_filter` (aligné sur les deux autres).
2. **Protocole d'itération canonique unique** :
   `docs/REFERENCE/scoped-audit-protocol.md` (reference-only, même statut que
   `pre-merge-gate.md`) — inventaire des scopes (blocs ARCHITECTURE.md par
   défaut) → une passe par scope → registre consolidé
   `{skill}-register-{YYYYMMDD}.md` (un verdict par scope + P0/P1 agrégés).
   Les trois skills citent ce chemin, aucun ne duplique le protocole.

## Conséquences

### Positives
- Granularité au choix (global ↔ bloc ↔ répertoire) sans nouveau skill.
- Rapports actionnables par périmètre ; registre consolidé pour la vue globale.
- Contrat et prompt réalignés (fin de la promesse `scope_filter` non tenue).
- Directement exploitable sur les projets consommateurs (V2-R4/R5a).

### Négatives / coûts
- Une passe par scope = plus d'invocations (coût tokens) ; assumé, c'est le but
  (petits contextes maîtrisés plutôt qu'un rapport monolithique).
- Trois SKILL.md s'allongent (~25 lignes chacun) — compensé par la référence unique.

### Neutres
- Aucun canon modifié ; aucun outil Python touché.

## Alternatives rejetées (≥ 2)

### Alternative A — Un nouveau skill « orchestrateur d'audits scopés »
- **Pourquoi rejetée** : violerait le moratoire V2 (nouvel élément de catalogue) ;
  le protocole en référence + paramètre suffit.

### Alternative B — Scope uniquement par glob/chemin (sans blocs ARCHITECTURE)
- **Pourquoi rejetée** : perd le lien avec la carte architecturale existante ;
  les blocs ARCHITECTURE.md sont déjà l'inventaire canonique des périmètres.
