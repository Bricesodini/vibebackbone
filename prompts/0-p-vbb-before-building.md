---
description: Pre-build validation gate — verify that the project is ready to start building a new feature
---

Vérifie que le projet est prêt à démarrer la construction pour : $@

## Objectif

Avant d'écrire une seule ligne de code, valider que toutes les préconditions
sont réunies pour un développement sain et tracé. Ce prompt est le "checklist
de décollage" pour un architecte produit qui s'apprête à lancer un chantier.

## Preferred Vibebackbone skills

- `0-vbb-scope-freeze`
- `1-vbb-intent-decomposer`
- `t-vbb-dependency-mapper`
- `t-vbb-project-context-init`
- `t-vbb-anti-slop-gate`

## Skill routing and chaining rule

### Phase 1 — Vérifier la gouvernance

1. Vérifier si le repo est sur les rails Vibebackbone (docs/PROJECT_MODE.md présent).
2. Si absent → lancer `t-vbb-project-context-init` pour initialiser.
3. Si présent → lire `docs/SESSION.md` et `docs/AUDIT_STATUS.md`.
4. Si `docs/AUDIT_STATUS.md` montre des BLOCKED → STOP. Résoudre avant de continuer.

### Phase 2 — Vérifier le scope

1. Lancer `0-vbb-scope-freeze` sur le périmètre concerné.
2. Si verdict = BLOCKED → le scope n'est pas assez défini. STOP.
3. Si verdict = PARTIAL → continuer mais noter les zones floues.
4. Si verdict = READY → le scope est gelé, on peut continuer.

### Phase 3 — Vérifier l'architecture

1. Vérifier si `docs/ARCHITECTURE.md` existe.
2. Si absent → lancer `t-vbb-dependency-mapper`.
3. Si présent mais ancien (> 30 jours ou > 50 commits) → proposer une mise à jour.

### Phase 4 — Vérifier l'état du code

1. Lancer `t-vbb-anti-slop-gate` pour vérifier l'état de surface.
2. Si verdict = BLOCKED (build cassé, tests échoués) → STOP. Réparer avant de construire.
3. Si verdict = READY_WITH_WARNINGS → noter les warnings, continuer.
4. Si verdict = READY → surface propre.

### Phase 5 — Décomposer l'intent

1. Lancer `1-vbb-intent-decomposer` sur la spécification fournie.
2. Le plan produit devient la feuille de route.
3. Valider le plan avec l'architecte avant de coder.

## Required process

1. **Restate** l'objectif : quelle feature va être construite.
2. **Phase 1** — Vérifier/créer la gouvernance projet.
3. **Phase 2** — Geler le scope.
4. **Phase 3** — Vérifier/créer la cartographie d'architecture.
5. **Phase 4** — Lancer l'anti-slop gate.
6. **Phase 5** — Décomposer l'intent en plan.
7. **Résumer** : verdict de readiness, risques, plan.

## Gate criteria — le projet est prêt à construire si :

- [ ] Gouvernance Vibebackbone présente (PROJECT_MODE, SESSION, AUDIT_STATUS)
- [ ] Scope gelé et documenté
- [ ] Architecture cartographiée (ARCHITECTURE.md)
- [ ] Surface de code propre (anti-slop READY ou READY_WITH_WARNINGS)
- [ ] Plan d'implémentation produit (intent-decomposer ACTIONABLE)
- [ ] Aucun BLOCKED dans AUDIT_STATUS.md

## Blocking conditions

Si une phase produit un BLOCKED → ne pas passer à la phase suivante.
Présenter le blocage à l'architecte avec la question : "Voulez-vous résoudre ce point avant de continuer ?"

Si l'architecte insiste pour continuer malgré un blocage → documenter l'acceptation du risque
dans SESSION.md et continuer.

## Output format

- **Goal**
- **Phase 1 — Gouvernance** : verdict
- **Phase 2 — Scope** : verdict du scope-freeze
- **Phase 3 — Architecture** : état de ARCHITECTURE.md
- **Phase 4 — Code surface** : verdict anti-slop
- **Phase 5 — Plan** : résumé du plan (nombre de tâches, vagues, risques)
- **Readiness verdict** : READY / READY_WITH_CAVEATS / NOT_READY
- **Blockers** : liste des points bloquants
- **Next action** : commencer Wave 1, ou résoudre les blockers
