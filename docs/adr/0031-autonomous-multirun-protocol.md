# ADR — 0031-autonomous-multirun-protocol

**Status**: ACCEPTED
**Date**: 2026-07-13
**Route**: STRUCTUREE
**Décideurs**: Brice (GO « boucler le ponçage » + exigence autonomie), Claude (formalisation)
**Liée à**: ADR 0027 (gate loop-closure fiable — prérequis), ADR 0029 (4bis + 40/75)
**Liée à POC**: aucune — règle de gouvernance ; la mécanique de gate sous-jacente a été validée par V2-R1 (tests) et V2-R5a (terrain)

## Contexte

Brice veut pouvoir « laisser itérer en autonomie sur plusieurs runs » en
maintenant l'hygiène audit → plan → implement → vérif/test. Les briques
existent (boucle 7 phases, loop-closure fiable depuis V2-R1, CLOSE-FINAL/
CLOSE-HANDOFF depuis Run 7, règle 40/75 et passe 4bis depuis V2-R4) mais
aucune règle ne borne la conduite d'une séquence de runs sans humain ;
LONG_RUN_RULE.md n'était qu'une fiche index dont la source canonique pointait
un chemin mort (corrigé en V2-R2).

## Décision

`docs/AGENTIC_RUN_PROTOCOL.md` devient l'unique document de conduite des runs,
avec une section « Runs autonomes » canonique :

1. **Séquence déclarée** : la liste des runs prévus est un artefact écrit avant
   le premier run (intake de séquence) — jamais une intention implicite.
2. **Borne humaine** : **3 runs max** sans checkpoint humain ; au-delà →
   CLOSE-HANDOFF et attente. (Révisable par CCP après retour terrain.)
3. **Gate inter-runs** : `python tools/vbb-loop-closure-check.py <run_id>
   --strict` obligatoire après chaque run ; exit ≠ 0 → STOP, pas de run
   suivant, CLOSE-HANDOFF avec blockers.
4. **Clôture** : chaque run terminé produit un **CLOSE-FINAL automatique** ;
   CLOSE-HANDOFF est réservé aux runs **interrompus**.
5. **Stop conditions** (n'importe laquelle) : escalade de risque (Critical
   Rule 2) · gate FAIL (ADR/POC ou loop-closure) · **75 % de contexte**
   (limite dure SESSION_RULES) · fin de séquence · borne humaine atteinte.
6. **Hygiène intra-run inchangée** : chaque run autonome garde la boucle
   complète de sa route, y compris la passe qualité 4bis selon risque.

LONG_RUN_RULE.md devient un stub de redirection (liens entrants préservés) ;
les budgets long-run restent canoniques dans PILOTAGE.md.

## Conséquences

### Positives
- L'autonomie devient bornée, auditable et interruptible sans perte (handoffs).
- Un seul document de conduite des runs (fin de la fiche orpheline).

### Négatives / coûts
- N=3 est un choix initial non validé terrain — assumé, révisable par CCP.

### Neutres
- Aucun outillage nouveau ; comportement supervisé inchangé.

## Alternatives rejetées (≥ 2)

### Alternative A — Autonomie non bornée avec seul le gate loop-closure
- **Pourquoi rejetée** : sans borne humaine, une dérive de scope peut se
  propager sur N runs avant détection ; contraire au human-in-the-loop de Brice.

### Alternative B — Nouvel outil « orchestrateur de séquence »
- **Pourquoi rejetée** : moratoire du ponçage (aucun mécanisme nouveau) ;
  la règle écrite + le gate existant suffisent à ce stade.
