---
run_id: "2026-07-28_1600_r0-adversarial-audit-of-m2-implementation"
phase: "01_INTAKE"
voie: "AUDIT"
status: "ACTIVE"
kind: "ADVERSARIAL_AUDIT"
target: "M2 implementation of adversarial loop governance"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"   # declared per ADR 0051 §Compatibility; v1.0 closure tool does not validate this field
started_at: "2026-07-28T16:00:00Z"
ended_at: "2026-07-28T16:15:00Z"
audit_type: "ADVERSARIAL_FALSIFICATION"
posture: "seek-to-falsify"
agent: "external adversarial auditor (distinct session, distinct provider, fresh context)"
source_runs_consumed:
  - "2026-07-28_1002_adversarial-loop-governance-design"
  - "2026-07-28_1200_m1-adversarial-loop-normative-arbitration"
  - "2026-07-28_1400_m2-adversarial-loop-implementation"
artifacts_produced:
  - "01_INTAKE.md"
---

# INTAKE — R0 Audit adversarial de l'implémentation M2

## Cadre normatif

Voie **AUDIT** — uniquement lecture, aucune modification.

**Posture adversariale stricte** :
- Chercher à **falsifier**, jamais à confirmer.
- Toute hypothèse par défaut : *« M2 a introduit une contradiction »*.
- Tout scénario de falsification qui ne trouve rien doit documenter
  *pourquoi il a échoué*, pas se retirer.

## Périmètre (8 fichiers)

| Fichier | Source M2 |
|---|---|
| `docs/adr/0051-adversarial-assurance-dimension.md` | NEW |
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | NEW |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | extended |
| `docs/CONVENTIONS.md` | extended |
| `docs/AGENTIC_RUN_PROTOCOL.md` | extended |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | extended |
| `docs/REFERENCE/pre-merge-gate.md` | extended |
| `docs/runs/2026-07-28_1400_m2-adversarial-loop-implementation/MIGRATION.md` | NEW |

**Hors périmètre** : `M2_DEFERRED_ITEMS.md`, scripts/outillage, templates,
skills, prompts, distributions. Tout différé M2 est réputé *non encore
soumis à M2* et donc *hors audit*.

## Sources canoniques de comparaison (lecture seule)

| Référence | Rôle |
|---|---|
| `M1_DECISIONS.md` §M1-01..M1-06 | source normative unique de M2 |
| `M1_DECISIONS.md` §8 | liste des 37 modifications attendues |
| `docs/adr/0049-engineering-knowledge-governance.md` | gouvernance des connaissances |
| `docs/adr/0050-design-certification-assurance-schema.md` | ADR schema 1.0 |
| `docs/PILOTAGE.md` (pre-M2, via `git show`) | référence triptyque |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` (pre-M2, via `git show`) | schéma 1.0 de référence |
| `AGENTS.md` CR#5 (no parallel truth) | méta-règle d'autorité |

## Hypothèses de falsification (à attaquer en R0)

> Chaque hypothèse ci-dessous est ce qu'on cherche à **prouver**.
> On ne présume rien ; on cherche à démentir M2.

### H1 — Conflit d'autorité
M2 a-t-il créé une **double autorité** sur l'adversarial ?
- `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (NEW) vs.
  `GATE_ASSURANCE_GOVERNANCE.md` (extended)
- M1-01 Option C : *split strict* — deux autorités non chevauchantes.

### H2 — Boucle impossible
M2 a-t-il introduit une **boucle non résoluble** ?
- A2_PROXY ↔ last_external_review ≤ 90j
- certification.owner cadence ≤ 90j ↔ SLA breach → SUSPENDED
- 13 conditions CERTIFIED ↔ 6 loss triggers

### H3 — Fail-open involontaire
M2 a-t-il laissé un **escape** par défaut (rien ne s'applique jamais) ?
- Niveau A0 par défaut.
- `NOT_REQUIRED` quand corpus vide.
- Cutoff `2026-07-28T14:00:00Z` ↔ `PRE_IMPLEMENTATION` retroactif.

### H4 — Régression compatibilité
M2 casse-t-il les **anciens workflows** ?
- Projets utilisant GATE 1.0 sans schémas adversariaux.
- Statut `ASSURANCE_STATUS.schema_version: "1.0"` (v1.1 additif ?).

### H5 — Ambiguïté normative
M2 contient-il des **termes non définis** ?
- `coherence_review`, `producers`, `ADVERSARIAL_REVIEW` profile.
- `corpus`, `attacker_identity` (proxy), `revocation_mechanism`.

### H6 — Conflit statuts ancien/nouveau
- `CERTIFIED` (M2) vs `certified` (pré-M2 Gate Assurance) — cas distinguished ?
- `adversarial_status: NOT_ASSESSED` vs `NOT_REQUIRED` vs `UNASSESSED_LEGACY`.

### H7 — Contournement A0/A1/A2
- `A2_DISTINCT_AGENT_PROXY` peut-il tourner en boucle interne ?
- Adversarial loop peut-il être auto-convoqué ?

### H8 — Règles CERTIFIED/SUSPENDED incohérentes
- 13 conditions vs 6 loss triggers : est-ce que *toute* condition perdue
  suspend `CERTIFIED` ?
- Auto-`SUSPENDED` via SLA : ce statut est-il *réversible* ?

### H9 — Migration impossible
- Ancien projet solo (sans concurrence d'agents) peut-il atteindre A2 ?
- Cutoff 2026-07-28T14:00:00Z : projet créé après ne peut-il plus rien certifier ?

### H10 — Conflit ADR
- ADR 0051 contredit-il ADR 0050 ?
- ADR 0051 contredit-il ADR 0049 ?

### H11 — Cas limite dépôt solo
- `last_external_review` exige LLM distinct ; que se passe-t-il sans LLM ?
- `A2_DISTINCT_AGENT_PROXY` exige `attacker_identity` à 3 composants ;
  impossible si provider figé.

### H12 — Inflation documentaire
- 21 KB `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` + 12 KB ADR 0051 + 7 extensions
  canoniques : est-ce de la duplication ?

## Plan d'attaque (R0)

1. **Cartographie textuelle** — extraction automatique des sections
   concernées dans les 8 fichiers M2.
2. **Diff pre-M2 / post-M2** — comparaison avec versions git pour
   `GATE_ASSURANCE_GOVERNANCE.md`, `PILOTAGE.md`, `CONVENTIONS.md`,
   `AGENTIC_RUN_PROTOCOL.md`, `ENGINEERING_KNOWLEDGE_GOVERNANCE.md`,
   `pre-merge-gate.md`.
3. **Confrontation M1 ↔ M2** — pour chaque M2-NN réel (sur les 6 livrés
   + les 31 différés, mais on ignore les différés), vérifier que M2 a
   appliqué exactement la décision M1.
4. **Tests statiques adversariaux** — pour chaque hypothèse H1..H12,
   exécuter un scénario de falsification en texte (pas d'exécution de
   code).
5. **Recoupements** — pour chaque finding, recouper avec au moins une
   autre source (M1, ADR, canon existant).
6. **Limites d'audit** — déclarer ce que R0 ne peut pas prouver
   (comportement runtime, dépendances de M2-BIS).

## Critère d'arrêt

- Si **≥ 1 finding** confirmé : produire `02_AUDIT.md` avec findings
  structurés (reproduction, gravité, impact, classification).
- Si **0 finding** confirmé : produire `02_AUDIT.md` avec la liste
  exhaustive des 12 hypothèses attaquées + pourquoi chacune échoue +
  limites de l'audit.

## Livrables

- `01_INTAKE.md` (ce fichier)
- `02_AUDIT.md` (campagne adversariale + findings ou échecs documentés)
- `03_INDEPENDENT_REVIEW.md` (revue distincte — peut être PARTIAL si
  même auteur que M2, à documenter)
- `04_CLOSEOUT.md` (FINAL_STATUS structuré)

## Contraintes

- ❌ Aucune modification des 8 fichiers M2 ni d'aucun canon.
- ❌ Aucun commit, aucun push.
- ❌ Aucun arbitrage, aucune décision de gouvernance.
- ✅ Lecture seule, falsification, traçabilité.