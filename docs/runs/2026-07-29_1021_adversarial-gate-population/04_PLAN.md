---
run_id: "2026-07-29_1021_adversarial-gate-population"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "PARTIAL"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T08:21:00Z"
ended_at: null
artifacts_produced:
  - "tools/vbb-governance-compat.py"
  - "tests/test_governance_compat_gate.py"
  - "02_DISPOSITION_MATRIX.md"
  - "03_CANON_CHANGE_PROPOSAL.md"
scope_change: "reframed mid-run — see §Changement de cadrage"
---

# 04_PLAN — GATE-POPULATION-01

## Changement de cadrage en cours de run

Le run a démarré comme correctif du gate adverse (R1 du plan de remédiation).
En cours d'exécution, l'architecte produit a reformulé la cible : non pas un
correctif, mais une **capacité de gouvernance** — le *Governance Compatibility
Gate*, pilier permettant au canon d'évoluer sans invalider son patrimoine.

Le cadrage est adopté. La matrice de disposition (`02_DISPOSITION_MATRIX.md`),
produite avant la reformulation, devient l'instance manuelle de ce que GCG
généralise. Ses dispositions se mappent sur les catégories GCG ; elle reste
valide comme travail d'arbitrage.

Trois écarts par rapport à la proposition initiale, motivés dans
`03_CANON_CHANGE_PROPOSAL.md` :

1. ajout de `CURRENT_NONCOMPLIANCE` (bloquante) — sans elle, tout défaut actuel
   se range en dette historique et GCG blanchit la dette ;
2. ajout de `OVERCLAIM` (bloquante immédiate, jamais migrable) — une
   revendication positive non soutenue est active là où une omission est inerte ;
3. refus de deux automatismes proposés — le scan de session est **mis en cache**,
   et le run de migration est **proposé**, jamais ouvert automatiquement
   (plan-first, triage).

## Objectif

Doter le framework d'un instrument capable de dire **pourquoi** un artefact est
non conforme à une règle datée, et empêcher que les trois lectures — conformité
actuelle, dette historique acceptée, certification obtenue — s'effondrent en un
booléen unique.

Ce run livre l'instrument de mesure et la classification. Il n'applique aucune
migration et n'écrit aucun bloc adverse.

## Pré-conditions

- `vbb-gate-check.py` : `CAN_CODE_START: True` (ADR 0051 accepté, POC `Verdict: GO`).
- POC exécuté et rouge : agrégation post-cutoff `exit 2`, 10 runs non conformes.
- Working tree propre à `6b0daf4` au démarrage.
- Contrainte d'intake §6.1 active : aucune écriture dans un bloc adverse.

## Étapes ordonnées

1. **Fait** — `01_INTAKE.md` : baseline mesurée, 4 contraintes normatives.
2. **Fait** — `POC.md` : agrégation démontrée rouge avant tout code (`Verdict: GO`).
3. **Fait** — `02_DISPOSITION_MATRIX.md` : 10 runs classés, `status: PROPOSED`.
4. **Fait** — `03_CANON_CHANGE_PROPOSAL.md` : GCG comme pilier, `status: PROPOSED`.
5. **Fait** — `tools/vbb-governance-compat.py` : instrument, rouge (`exit 2`).
6. **Fait** — `tests/test_governance_compat_gate.py` : 6 tests, anti-blanchiment
   vérifié par mutation (ledger prioritaire → test rouge).
7. **Bloqué** — arbitrage des 3 questions normatives (matrice §3.3, §3.6, §3.10).
8. **Bloqué** — statut de `2026-07-30_0500` : `OVERCLAIM` sur certification publiée.
9. **Bloqué** — ADR 0052, à écrire après validation de la proposition de canon.
10. **Bloqué** — `docs/GOVERNANCE_COMPATIBILITY_LEDGER.md`, après arbitrage.
11. **Bloqué** — câblage CI, après ledger et vérifications de substance.

## Critères d'acceptation

| # | Critère | État |
|---|---|---|
| A1 | L'instrument est démontré **capable d'échouer** avant d'être livré | ✅ `exit 2`, 10 bloquants |
| A2 | La règle anti-blanchiment est démontrée capable d'échouer | ✅ mutation vérifiée |
| A3 | La certification n'est dérivable d'aucun verdict de gate | ✅ `NOT_DERIVABLE_FROM_THIS_GATE`, test |
| A4 | Un run ouvert ne fait pas échouer son propre gate | ✅ `OUT_OF_SCOPE`, test |
| A5 | Aucun bloc adverse écrit, créé ou modifié | ✅ vérifiable au diff |
| A6 | Aucun `adversarial_level` rétrogradé | ✅ matrice §4 |
| A7 | La suite de tests reste verte | ✅ 432 passed, 1 skipped |
| A8 | GCG câblé en CI | ❌ délibérément non fait — voir Risques |

## Plan de rollback global

Le run n'a modifié aucun artefact existant : il ajoute deux fichiers de code et
quatre documents de run. Le rollback est `git revert` du commit, sans effet de
bord sur l'historique de gouvernance, sur les blocs adverses ou sur la CI —
laquelle n'est pas câblée sur le nouvel outil.

Aucune migration n'ayant été appliquée, il n'existe aucun état intermédiaire à
défaire.

## Risques identifiés

1. **Câbler GCG maintenant rendrait la CI rouge et bloquerait tout travail.**
   Dix artefacts sont bloquants ; trois exigent un arbitrage humain, un exige un
   acteur A2 distinct. Aucun run ne peut résoudre cela seul. *Décision* : ne pas
   câbler. L'ordre est instrument → arbitrage → ledger → câblage. Câbler avant
   l'arbitrage recréerait la pression que GCG existe pour supprimer.

2. **Une certification publiée est mise en cause.**
   `2026-07-30_0500_final-publication-of-v1.1-certification` est classé
   `OVERCLAIM`. Si l'arbitrage conclut que son `PASS_ADVERSARIAL` n'est dérivable
   d'aucun run conforme, la publication v1.1 devra être révisée. Ce run n'a pas
   autorité pour rendre cette décision ; il la rend visible et opposable.

3. **La dette pourrait devenir confortable.** `HISTORICAL_NONCOMPLIANCE` est non
   bloquante par construction. *Mitigation* : elle est comptée et affichée ; le
   passage à `READY` global devra exiger son acceptation humaine tracée.

4. **Portée de l'instrument.** GCG n'implémente qu'un jeu de règles
   (adversarial 1.1). L'architecture est générique mais aucune extension à une
   autre dimension n'est autorisée sans nouvelle proposition de canon.

5. **`A2_DISTINCT_AGENT_PROXY` non satisfait par ce run.** L'agent est
   `claude-opus-5`, même famille que l'auteur de `2026-07-29_0840`. Ce run ne
   peut pas se certifier lui-même, et ne le revendique pas.

## ADR 0052 — non écrit, et pourquoi

GCG est proposé comme **pilier de gouvernance**. Enregistrer une décision
d'architecture avant validation humaine de la proposition de canon créerait
exactement la vérité parallèle que le dépôt vient de corriger : un ADR
`accepted` face à une proposition `PROPOSED`.

L'ADR sera écrit **après** validation de `03_CANON_CHANGE_PROPOSAL.md`, et il
enregistrera la décision rendue, pas celle espérée.

## Suite — dans l'ordre

| # | Action | Bloqué par |
|---|---|---|
| 1 | Arbitrer les 3 questions normatives | décision humaine |
| 2 | Statuer sur `2026-07-30_0500` (`OVERCLAIM`, P0) | décision humaine |
| 3 | Valider ou amender la proposition de canon | décision humaine |
| 4 | Écrire ADR 0052 sur la décision rendue | #3 |
| 5 | Créer le ledger avec les dispositions arbitrées | #1, #2 |
| 6 | Vérifier la substance de `2026-07-28_1600` et `_2200` | #1 |
| 7 | Câbler GCG dans les trois surfaces CI | #5, #6 |
| 8 | R3 (`status:`), R4 (parité CI), R5 (acteur A2 distinct) | indépendant |
