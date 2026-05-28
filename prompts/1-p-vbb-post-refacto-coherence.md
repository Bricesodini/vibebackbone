---
description: Post-refactoring code↔doc coherence pipeline — audit, gap fill, harmonize, and prepare clean handoff
---

Réalise un audit complet de cohérence code↔documentation post-refactoring pour : $@

## Objectif

Après une phase lourde de refactoring, debugging, ou réduction de dette technique,
remettre le projet sur des bases saines en vérifiant que TOUTE la documentation
reflète fidèlement l'état réel du code.

Le pipeline complet :

1. Auditer la cohérence code↔doc (détection des écarts)
2. Combler les gaps (écriture de la doc manquante)
3. Harmoniser la doc (élimination des redondances)
4. Produire un handoff propre pour repartir

## Preferred Vibebackbone skills

- `1-vbb-code-doc-coherence-auditor`
- `1-vbb-code-doc-gap-integrator`
- `1-vbb-doc-harmonizer`
- `t-vbb-session-handoff`

## Skill routing and chaining rule

### Phase 1 — Audit de cohérence

Lancer `1-vbb-code-doc-coherence-auditor` en premier.
C'est le pilier : il produit l'état des lieux complet et détermine si les phases suivantes
sont nécessaires.

Si l'utilisateur n'a pas précisé le scope, lui demander avant de lancer le scan :
"Quel périmètre ? Tout le repo, ou des modules spécifiques ?"

- "Quels modules ont été refactorés récemment ?"

Après le rapport d'audit, analyser le verdict :

| Verdict      | Action                                                           |
| ------------ | ---------------------------------------------------------------- |
| `COHERENT`   | Passer directement à la Phase 4 (handoff). Le projet est propre. |
| `PARTIAL`    | Continuer en Phase 2 pour les gaps HIGH/MEDIUM uniquement.       |
| `FRAGMENTED` | Continuer en Phase 2 + Phase 3. Le chantier est plus lourd.      |
| `UNKNOWN`    | Demander clarification à l'utilisateur avant de continuer.       |

### Phase 2 — Comblement des gaps

Lancer `1-vbb-code-doc-gap-integrator` pour écrire la documentation manquante.

Utiliser le rapport du coherence-auditor comme **hint list** :

- Passer les gaps MISSING identifiés comme `gaps connus` à l'input du gap-integrator
- Cibler le scope sur les zones refactorées si spécifiées
- Seuil d'écriture : `HIGH+MEDIUM` en mode `PARTIAL`, `ALL` en mode `FRAGMENTED`

Ne PAS lancer le gap-integrator si le verdict du coherence-auditor est `COHERENT`.

### Phase 3 — Harmonisation documentaire

Lancer `1-vbb-doc-harmonizer` pour :

- Traiter les écarts `REDUNDANT` identifiés par le coherence-auditor
- Consolider la documentation après l'ajout des fiches manquantes (Phase 2)
- Proposer un plan d'archivage pour les documents obsolètes

Cette phase est optionnelle si le nombre de REDUNDANT est faible (< 3) et de sévérité LOW.

### Phase 4 — Handoff de clôture

Lancer `t-vbb-session-handoff` pour sceller l'état propre du projet.

Le handoff doit inclure :

- Résumé du travail de remédiation effectué
- Verdicts des 3 passes (audit → gap fill → harmonisation)
- Écarts résiduels assumés (LOW non traités, orphelins intentionnels)
- Prochaines actions recommandées

### Règle de cascade des verdicts

Si un verdict de la phase N est `BLOCKED`, ne pas lancer la phase N+1.
Demander à l'utilisateur de résoudre le blocage.

Si le gap-integrator produit un verdict `READY`, passer à la phase suivante.
Si `PARTIAL`, continuer mais signaler les gaps restants dans le handoff final.
Si `BLOCKED`, arrêter et demander clarification.

### Fallback manuel

Le fallback manuel n'est autorisé que si une skill nommée est absente du `[Skills]` actif.
Si tu tombes en fallback, nommer la skill manquante et expliquer pourquoi.

## Required process

1. **Restate** l'objectif en une phrase.
2. **Demander** le périmètre et les zones refactorées (si non fournis).
3. **Phase 1** — Lancer `1-vbb-code-doc-coherence-auditor`.
4. **Analyser** le verdict et décider des phases suivantes.
5. **Phase 2** — Lancer `1-vbb-code-doc-gap-integrator` (si nécessaire), avec les hints du rapport d'audit.
6. **Phase 3** — Lancer `1-vbb-doc-harmonizer` (si nécessaire), avec les REDUNDANT du rapport d'audit.
7. **Phase 4** — Lancer `t-vbb-session-handoff`.
8. **Résumer** le pipeline complet et l'état final.

---

## Closeout sequence (mandatory — run after Phase 4 handoff)

After the Phase 4 handoff is produced:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <docs modified during the pipeline>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> The coherence pipeline produces and modifies persistent artifacts (audit reports, gap docs, harmonized doc) — they must be committed and pushed. Do not stop after the handoff. The post-refacto coherence loop is not closed until git push is done.

## Constraints

- Ne pas sauter la Phase 1 (audit). C'est la fondation de tout le pipeline.
- Ne pas lancer le gap-integrator sans lui passer le rapport d'audit comme hint list.
- Ne pas lancer le doc-harmonizer sans lui passer les écarts REDUNDANT détectés.
- Ne pas confondre : le coherence-auditor détecte, le gap-integrator écrit, le doc-harmonizer consolide.
- Distinguer clairement les orphelins intentionnels (architecture, guides) des orphelins accidentels.
- La Phase 4 (handoff) est toujours exécutée, même si le verdict est `COHERENT` (pour tracer).
- Si l'utilisateur interrompt le pipeline à une phase, produire un handoff partiel avec l'état connu.
- Respecter la règle de cascade des verdicts : BLOCKED → arrêt, PARTIAL → continuer avec avertissement.

## Output format

- **Goal** : résumé en 1 phrase
- **Scope** : périmètre audité
- **Phase 1 — Verdict** : verdict du coherence-auditor + résumé
- **Phase 2 — Gap fill** : (si exécutée) verdict + fiches écrites
- **Phase 3 — Harmonisation** : (si exécutée) verdict + actions
- **Phase 4 — Handoff** : résumé du handoff final
- **État final** : `prêt à repartir` | `prêt avec réserves` | `remédiation nécessaire`
- **Écarts résiduels** : ce qui reste à traiter
- **Prochaine action recommandée**
