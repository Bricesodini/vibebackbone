---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T13:50:00Z"
ended_at: "2026-07-29T14:45:00Z"
artifacts_produced:
  - "02_FINDINGS_REGISTER.md"
  - "03_DEPENDENCY_AND_ARBITRATION_MAP.md"
  - "04_INDEPENDENT_ARBITRATION_REVIEW.md"
  - "05_DECISIONS_REQUIRED.md"
  - "06_RESUMPTION_SEQUENCE.md"
  - "07_CLOSEOUT.md"
---

# 04_PLAN — GCG-ARB-01

## Objectif

Transformer les constats accumulés sur le *Governance Compatibility Gate* en un
**espace de décisions cohérent**, avant toute tentative de réparation. Déterminer
pour chaque constat s'il doit être corrigé mécaniquement, tranché normativement,
redéfini conceptuellement, aligné sur un canon existant, abandonné, ou laissé
explicitement ouvert.

Ce run ne produit **aucun code**, ne modifie **pas le modèle**, et n'ouvre
**aucun** des runs qu'il propose.

## Pré-conditions

- `docs/REFERENCE/governance-compatibility-model.md` en v2, statut `PROPOSED`.
- Working tree propre à `5d4fe34`, branche `feat/governance-compatibility-gate`.
- `vbb-gate-check.py` : `CAN_CODE_START: False` (`MISSING_POC`). **Honoré en
  n'écrivant aucun code** — voir `05_EXECUTION.md` §3.
- Contraintes C1–C9 actives (`01_INTAKE.md` §2).

## Étapes ordonnées

1. **Fait** — Constituer le registre unique à partir de cinq sources (ST, IR,
   R1021, R1050, AUD), en renumérotant dans un espace `GCG-nn` pour résoudre la
   collision `IR-F8` / `AUD-F8`.
2. **Fait** — Classer par nature selon la taxonomie fournie, **et déclarer les
   quatre cas où elle ne discrimine pas**, plutôt que de ranger mécaniquement.
3. **Fait** — Ajouter l'axe `closure_authority`, qui est le discriminant réel.
4. **Fait** — Produire le graphe de dépendances et vérifier les neuf relations
   exigées par la mission.
5. **Fait** — Séparer décision normative et correction technique, avec les cinq
   questions de la mission pour chacun des constats.
6. **Fait** — Dériver un verdict de viabilité et déclarer sa condition de
   bascule.
7. **Fait** — Proposer une séquence de reprise, non exécutée.
8. **Fait** — Déléguer la revue de la classification et de l'arbitrage à un
   subagent en contexte isolé, mandat non orienté, dépôt en lecture seule.
9. **Fait** — Vérifier moi-même les constats de la revue qui portent contre mon
   arbitrage, puis répercuter les corrections **en conservant la trace des
   énoncés réfutés**.
10. **Non fait, délibéré** — corriger GCG-36, GCG-22, GCG-24, GCG-19, GCG-15 et
    le commentaire faux de `vbb-governance-compat.py` (contrainte C3), bien que
    `03` §4.2 les établisse comme exécutables sans décision.
11. **Non fait, délibéré** — écrire une entrée de corpus pour GCG-36
    (contrainte C3). Écart déclaré : `05_EXECUTION.md` §4.
12. **Non fait, délibéré** — trancher une décision normative, ouvrir un run de
    la séquence, rédiger l'ADR 0052.

## Critères d'acceptation

| # | Critère | État |
|---|---|---|
| A1 | Registre unique, identifiants stables, sources conservées, doublons éliminés sans fusion artificielle | ✅ 36 entrées + 6 portées ; 4 cas de non-discrimination déclarés ; 1 scission (GCG-01/21) justifiée |
| A2 | Chaque constat porte les 9 champs minimaux exigés | ✅ dont preuve reproductible pour chacun |
| A3 | Taxonomie explicite, non appliquée mécaniquement | ✅ `02` §3 déclare où elle échoue et ajoute l'axe utile |
| A4 | Graphe de dépendances, avec les 9 relations exigées vérifiées | ✅ `03` §2, §3 — dont 3 relations différentes de l'attendu |
| A5 | Décision normative et correction technique séparées, sans décision silencieuse | ✅ `05` — 13 décisions posées, aucune prise ; 5 abstentions déclarées |
| A6 | Verdict **dérivé** du registre et des dépendances, non choisi pour préserver le travail | ⚠️ **partiellement tenu.** La dérivation initiale était incohérente (RA-F-C) ; elle a été reconstruite après revue. Le verdict n'a pas changé, sa justification a été refaite |
| A7 | Au moins un subagent en contexte isolé examine la classification | ✅ 11 constats, aucun écarté sur les faits, 6 re-vérifiés par l'agent principal |
| A8 | Divergences agent / subagent visibles, non fusionnées | ✅ `04` §4 (W1, W2) et `03` §6 (V1, V2, V3-résolue) |
| A9 | Aucun code produit | ✅ `git status` : seul `docs/runs/2026-07-29_1550_*/` est nouveau |
| A10 | Aucun finding rétrogradé, aucune CI blanchie | ✅ le verdict `2/15 FAIL` est inchangé ; GCG-28 est **monté** en confiance, aucun ne descend |
| A11 | Séquence de reprise proposée, non ouverte | ✅ `06` — 10 runs proposés, 0 ouvert |

## Plan de rollback global

Le run ajoute un répertoire de run et **ne modifie aucun fichier existant**.
Rollback = suppression du répertoire, sans effet de bord. Aucun code, aucun test,
aucune CI, aucun document canonique touché.

## Risques identifiés

1. **Un arbitrage conduit par l'auteur du modèle protège le modèle.**
   Mitigation : revue en contexte isolé, mandat explicitement orienté vers la
   recherche de réparations défensives *dans l'arbitrage*. Résultat mesuré : la
   revue a trouvé une **quatrième voie de blanchiment** (GCG-36), établi que
   **mes propres recommandations D1/D2 étaient des réparations défensives**
   (RA-F-D), et montré que ma correction de GCG-22 était fausse dans le sens de
   la surestimation. La mitigation a fonctionné. Elle reste insuffisante :
   `A2_DISTINCT_AGENT_PROXY` n'est pas satisfait (même famille de modèle).

2. **Le verdict peut être choisi puis justifié.** C'est arrivé : la revue a
   montré que ma dérivation initiale était incohérente et plus généreuse envers
   le noyau que le registre ne le soutient. `03` §7 est réécrite et §7.4 pose
   désormais le test d'impartialité **dans les deux directions**.

3. **Un registre peut geler un désaccord au lieu de le mesurer.** C'est arrivé
   (GCG-10, divergence V3). Corrigé : la mesure était à une commande.

4. **GCG-36 n'est épinglé par aucune entrée de corpus.** Né dans ce run,
   `CONFIRMED`, et non déclaré dans le bloc adverse — parce que le déclarer
   forcerait à écrire du code contre C3. C'est GCG-25 s'appliquant à ce run
   lui-même. Le constat vit dans `02`, un document versionné ; il n'est pas
   verrouillé contre un changement silencieux. **Décision D8 rendue urgente.**

5. **Le run est lui-même l'unique `PENDING_LIFECYCLE` vivant** de la population
   qu'il mesure, donc non bloquant et hors dénominateur. Non fautif — le run est
   ouvert — mais la baseline de `01` §5 n'est pas la mesure neutre qu'elle
   paraît. Rend **GCG-30** concret.
