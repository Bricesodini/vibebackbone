---
run_id: "2026-07-29_1130_gcg-genericity-stress-test"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "PARTIAL"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T09:30:00Z"
ended_at: null
artifacts_produced:
  - "02_STRESS_TEST.md"
  - "docs/REFERENCE/governance-compatibility-model.md (révision v2)"
  - "05_EXECUTION.md"
  - "07_CLOSEOUT.md"
---

# 04_PLAN — GCG-STRESS-01

## Objectif

Déterminer si le *Governance Compatibility Gate* est un modèle générique ou une
spécialisation de la dimension adverse, en l'appliquant à des règles de
gouvernance indépendantes. Produire un verdict argumenté et, si le modèle
révèle des limites, une version révisée.

Ce run ne produit **aucun code** et ne poursuit **aucune implémentation**.

## Pré-conditions

- `docs/REFERENCE/governance-compatibility-model.md` en v1, statut `PROPOSED`.
- Working tree propre à `f7e21a3`.
- `vbb-gate-check.py` : `ADR_REQUIRED: False`, `POC_REQUIRED: False` — le run ne
  produit pas de code, le gate d'autorisation d'implémentation est sans objet.
- Contraintes C1 (pas de code), C2 (pas d'ADR 0052), C3 (pas d'implémentation)
  actives — `01_INTAKE.md` §2.

## Étapes ordonnées

1. **Fait** — Sélectionner des règles candidates par **distance structurelle
   croissante**, avant d'examiner ce qu'on y trouverait.
2. **Fait** — Règle B (`engineering-knowledge 1.0`) : même population,
   obligation différente. Mesurer population gouvernée et non-conformités.
3. **Fait** — Règle C (ADR 0042, layout des skills) : population non datée et
   mutable. Mesurer l'état, examiner comment le canon a réellement traité sa
   propre migration.
4. **Fait** — Règle D (ADR 0033, credentials) : pas de population, un flux.
   Test de frontière : le modèle doit se déclarer inapplicable.
5. **Fait** — Confronter le modèle aux enforcers réels du canon
   (`vbb-loop-closure-check.py`, `vbb-contract-lint.py`, `vbb-adversarial-gate.py`).
6. **Fait** — Consigner les constats dans `02_STRESS_TEST.md`, chaque
   affirmation adossée à une commande exécutée.
7. **Fait** — Réviser le modèle en v2 sur les seuls points que le test a
   invalidés.
8. **Non fait, délibéré** — corriger `S1` dans `tools/vbb-governance-compat.py`
   (contrainte C1).
9. **Non fait, délibéré** — ADR 0052 (contrainte C2), ledger, Migration Engine,
   câblage CI (contrainte C3).

## Critères d'acceptation

| # | Critère | État |
|---|---|---|
| A1 | Au moins une deuxième règle **indépendante** de la dimension adverse est traitée | ✅ trois : ADR 0049, 0042, 0033 |
| A2 | Chaque affirmation est adossée à une **mesure**, pas à un raisonnement | ✅ commandes tracées dans `05_EXECUTION.md` |
| A3 | Le test peut **échouer** — il existe un résultat qui invaliderait le modèle | ✅ il a partiellement échoué : 4 constats de défaut |
| A4 | Le modèle est révisé sur les points invalidés, **pas ailleurs** | ✅ noyau de classification inchangé |
| A5 | Aucun code produit ou modifié | ❌ **non tenu** — 5 entrées de corpus imposées par §9 destination 6 ; `tools/` inchangé. Écart déclaré : `05_EXECUTION.md` §4 |
| A6 | Aucune canonisation prématurée | ✅ modèle reste `PROPOSED` |
| A7 | Les limites du test lui-même sont déclarées | ✅ `02_STRESS_TEST.md` §8 |

## Plan de rollback global

Le run ajoute un répertoire de run et modifie un seul fichier existant
(`docs/REFERENCE/governance-compatibility-model.md`, statut `PROPOSED`, non
canonique, non référencé par un gate). Aucun code, aucun test, aucune CI
touchés. Rollback = `git revert` du commit, sans effet de bord.

## Risques identifiés

1. **Un stress test conduit par l'auteur du modèle valide surtout l'auteur.**
   Mitigation partielle : les règles ont été choisies pour maximiser la distance
   structurelle **avant** d'examiner leur contenu, et le critère de réussite est
   symétrique (le modèle doit aussi savoir se déclarer inapplicable). Mitigation
   insuffisante : `A2_DISTINCT_AGENT_PROXY` n'est pas satisfait. Déclaré au
   closeout, non compensé.

2. **La v2 spécifie plus qu'elle ne sécurise.** Trois invariants ajoutés, zéro
   test ajouté — la couverture exécutable passe de 3/8 à 3/11. Le modèle paraît
   plus solide en étant, mécaniquement, tout aussi fragile. Mitigation : le
   constat est écrit dans le modèle lui-même (§5), pas seulement ici.

3. **`S1` reste ouvert dans le code.** Le scanner est plus permissif que
   l'enforcer qu'il enveloppe. Latent aujourd'hui, actif dès la première
   auto-déclaration rétroactive. *Décision* : ne pas corriger (C1), enregistrer
   comme bloquant explicite du câblage CI.

4. **La généricité démontrée est interne.** Quatre règles du même canon, même
   équipe, même style. Une règle externe pourrait invalider §3.6. Déclaré en
   `02_STRESS_TEST.md` §8 et dans le modèle §7.

5. **Le périmètre d'arbitrage humain peut doubler.** Si les 9 runs de la
   question ouverte 4 sont des `OVERCLAIM`, une deuxième règle entre en dette.
   Ce run rend la question visible ; il ne la tranche pas.
