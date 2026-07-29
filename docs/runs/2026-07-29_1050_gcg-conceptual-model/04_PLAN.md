---
run_id: "2026-07-29_1050_gcg-conceptual-model"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "PARTIAL"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T08:50:00Z"
ended_at: null
artifacts_produced:
  - "docs/REFERENCE/governance-compatibility-model.md"
  - "tools/vbb-governance-compat.py (aligné)"
  - "tests/test_governance_compat_gate.py (aligné + 2 tests)"
---

# 04_PLAN — GCG-MODEL-01

## Objectif

Stabiliser le modèle conceptuel du GCG et supprimer tout écart entre la
spécification et l'instrument livré par `2026-07-29_1021`.

## Pré-conditions

- Run `2026-07-29_1021` clos en `HANDOFF`, scanner livré rouge et non câblé.
- Aucun ledger, aucune migration appliquée : le modèle peut encore changer sans
  invalider de décision.
- Trois questions normatives en attente d'arbitrage — inchangées par ce run.

## Étapes ordonnées

1. Écrire `docs/REFERENCE/governance-compatibility-model.md` en `PROPOSED`.
2. `C1` — remplacer la borne dérivée de git par deux bornes déclarées
   (`applies_from`, `enforcement_effective_from`), le SHA devenant preuve.
3. `C2` — renommer `OUT_OF_SCOPE` en `PENDING_LIFECYCLE` et lui donner sa limite
   stricte manquante.
4. Ajouter les tests portant les invariants `I6` et la fenêtre de dette bornée.
5. Vérifier qu'aucun écart ne subsiste entre le document et le code.

## Critères d'acceptation

| # | Critère | État |
|---|---|---|
| A1 | Le modèle est écrit et porte `PROPOSED` | ✅ |
| A2 | Aucune frontière normative n'est dérivée d'un artefact technique | ✅ bornes déclarées, SHA en `enforcement_evidence` |
| A3 | `PENDING_LIFECYCLE` ne peut pas couvrir un artefact existant qui échoue | ✅ test dédié |
| A4 | La fenêtre de dette est bornée des deux côtés | ✅ test dédié |
| A5 | Scanner / Arbitration / Engine explicitement séparés | ✅ modèle §2, docstring du scanner |
| A6 | Le verdict mesuré est inchangé par le renommage | ✅ `2/13`, exit 2 |
| A7 | Suite verte, outillage statique propre | ✅ 8 tests GCG, ruff/mypy PASS |
| A8 | Migration Engine implémenté | ❌ délibérément — voir Risques |

## Plan de rollback global

Le run ajoute un document et modifie deux fichiers non câblés dans la CI.
`git revert` du commit restaure l'état de `7e011f8` sans effet sur la
gouvernance, les blocs adverses ou la CI.

## Risques identifiés

1. **Figer un modèle sur une seule règle instrumentée.** Le modèle est générique,
   une seule règle l'éprouve. *Mitigation* : statut `PROPOSED`, et §7 du modèle
   interdit l'extension à une autre dimension sans nouvelle proposition.
2. **Le Migration Engine reste spécifié mais absent.** *Décision* : ne pas
   l'implémenter avant que le ledger existe. Un moteur sans ledger n'aurait
   d'autre source que le jugement de l'agent — exactement ce que le modèle
   interdit (invariant I1).
3. **`PENDING_LIFECYCLE` reste un vecteur si sa limite est relâchée plus tard.**
   *Mitigation* : la limite est portée par un test, pas par une convention.
4. **`A2_DISTINCT_AGENT_PROXY` non satisfait.** Même agent que `1021`. Le modèle
   qui interdit à un composant d'observer et de juger simultanément est écrit
   par l'agent qui a écrit l'instrument. C'est déclaré, pas résolu.

## Suite

Inchangée : arbitrage humain des trois questions, puis ledger, puis moteur, puis
câblage. `G7` fera l'objet d'un run dédié après stabilisation du GCG.
