---
load_policy: reference
context_role: agentic-protocol
phase: transverse
status: active
updated: 2026-05-23
---

# AGENTIC_RUN_PROTOCOL — Les 7 phases

vibebackbone formalise tout travail agentique en 7 phases nommées 01..07.
Chaque phase a un rôle unique, un artefact unique, un handoff unique.

## Principe

```
1 session = 1 rôle = 1 intention = 1 sortie exploitable
```

Une phase ne déborde pas sur la suivante. Si elle déborde, c'est une nouvelle
session avec un nouveau rôle.

## Les 7 phases

| # | Nom | Rôle | Artefact | Lecture seule ? |
|---|-----|------|----------|-----------------|
| 01 | `INTAKE` | Cadrer la demande, choisir la voie | [`templates/01_INTAKE.md.template`](templates/01_INTAKE.md.template) | ✅ |
| 02 | `AUDIT` | Constater, mesurer, conclure sans patcher | [`templates/02_AUDIT.md.template`](templates/02_AUDIT.md.template) | ✅ |
| 03 | `DECISION` | Trancher entre options | [`templates/03_DECISION.md.template`](templates/03_DECISION.md.template) | ✅ |
| 04 | `PLAN` | Décrire la séquence d'actions | [`templates/04_PLAN.md.template`](templates/04_PLAN.md.template) | ✅ |
| 05 | `EXECUTION` | Faire les changements | [`templates/05_EXECUTION.md.template`](templates/05_EXECUTION.md.template) | ❌ |
| 06 | `REVIEW` | Vérifier conformité au plan et DoD | [`templates/06_REVIEW.md.template`](templates/06_REVIEW.md.template) | ✅ |
| 07 | `CLOSEOUT` | Consolider, transmettre, marquer fin | [`templates/07_CLOSEOUT.md.template`](templates/07_CLOSEOUT.md.template) | ✅ |

## Invariant de clôture

Toute boucle produit au minimum :

```
docs/runs/{slug}/
├── 01_INTAKE.md
├── 0X_<phase métier>.md   ← ≥1
└── 07_CLOSEOUT.md
```

Phases minimales par voie (voir [`PILOTAGE.md`](PILOTAGE.md) pour le triage) :

| Voie | Phases obligatoires | Phases conditionnelles |
|------|---------------------|------------------------|
| `RAPIDE-ZERO` | Aucun (`docs/runs/` non requis) | Activity Log uniquement |
| `RAPIDE-MINIMAL` | 05_PATCH_SUMMARY seul | Activity Log requis |
| `RAPIDE` | 01 + 05 + 07 | 04 si plan non trivial |
| `STRUCTUREE` | 01 + 04 + 05 + 07 | 06 si DoD critique |
| `AUDIT` | 01 + 02 + 03 + 07 | 04 + 05 si remédiation incluse |
| `CLOTURE` | 07 seul | 06 si bilan d'une session longue |

## Readiness before execution

For any MVP or project started from zero, `05_EXECUTION` is forbidden until the
MVP START gate has returned `READY`.

The gate is defined in [`MVP_START_PROTOCOL.md`](MVP_START_PROTOCOL.md) and
executed by `0-vbb-rico-readiness`.

If readiness is:

- `READY` -> continue to `04_PLAN` / STRUCTURED execution.
- `PARTIAL` -> continue framing only; no application code.
- `BLOCKED` or `UNKNOWN` -> stop and output blocking questions only.

Hard escalations:

- critical ambiguity -> questions before plan
- architecture not defined -> no code
- data not modeled -> no persistence
- deployment constraints absent while infra is requested -> no Docker/runtime
  structure
- acceptance criteria absent for core behavior -> no implementation run

## Cycle complet

```
01 INTAKE   →  cadre, choisit la voie
02 AUDIT    →  constate (voie AUDIT)
03 DECISION →  arbitre (voie AUDIT, parfois STRUCTUREE)
04 PLAN     →  séquence (voie STRUCTUREE)
05 EXECUTION→  fait (voie STRUCTUREE, RAPIDE)
06 REVIEW   →  vérifie (optionnel)
07 CLOSEOUT →  consolide (toutes voies)
```

## Governed learning after delivery

The delivery cycle does not promote reusable knowledge. Its closeout performs a
Knowledge Harvest and records `NONE`, `OBSERVATION_RECORDED` or
`EVIDENCE_LINKED`.

If an observation merits qualification, it opens a separate run:

```text
Observation → Candidate → Knowledge audit → Independent review
→ Human decision → Structured integration → Canonical
```

That run reuses phases 01–07. There is no phase 08, and the knowledge record,
run, review and closeout remain evidence rather than authority. The canonical
lifecycle lives in
[`ENGINEERING_KNOWLEDGE_GOVERNANCE.md`](ENGINEERING_KNOWLEDGE_GOVERNANCE.md).

## Règles dures

- Une phase ne commence qu'après la production de l'artefact de la phase
  précédente (sauf cas explicites listés ci-dessus).
- Une phase ne se termine qu'après l'écriture de son propre artefact.
- L'artefact `07_CLOSEOUT.md` est toujours le dernier produit d'un run.
- Un run sans `07_CLOSEOUT.md` est un run inachevé — `t-vbb-commit-ready`
  refuse le commit dans ce cas (à partir de PR #3 du plan d'artefacts).

## Format des artefacts

Tous les artefacts suivent la convention frontmatter définie dans
[`runs/README.md`](runs/README.md) :

```yaml
---
run_id: "YYYY-MM-DD_HHmm_slug"
phase: "0X_NAME"
voie: "RAPIDE-ZERO|RAPIDE-MINIMAL|RAPIDE|STRUCTUREE|AUDIT|CLOTURE"
status: "READY|PARTIAL|BLOCKED|UNKNOWN"
knowledge_governance_version: "1.0"
agent: "claude-code|codex|pi|opencode"
started_at: "ISO8601 UTC"
ended_at: "ISO8601 UTC"
next_phase: "0X_NAME | null"
artifacts_consumed: [...]
artifacts_produced: [...]
---
```

For `07_CLOSEOUT.md`, runs declaring `knowledge_governance_version: "1.0"`
also declare:

```yaml
knowledge_harvest: "NONE|OBSERVATION_RECORDED|EVIDENCE_LINKED"
```

## Liens

- [`runs/README.md`](runs/README.md) — convention et invariant de clôture
- [`PILOTAGE.md`](PILOTAGE.md) — règle de triage par voie
- [`SESSION_RULES.md`](SESSION_RULES.md) — quand rester, quand changer
- [`MEMORY_AND_HANDOFF.md`](MEMORY_AND_HANDOFF.md) — mémoire officielle vs conversation

## Runs autonomes (ADR-0031)

Conduite canonique d'une **séquence de runs sans checkpoint humain** :

1. **Séquence déclarée** — la liste des runs prévus est écrite AVANT le premier
   run (intake de séquence). Jamais d'enchaînement implicite.
2. **Borne humaine** — **3 runs max** sans validation humaine ; au-delà →
   `CLOSE-HANDOFF` et attente. (Révisable par CCP.)
3. **Gate inter-runs** — après chaque run :
   `python tools/vbb-loop-closure-check.py <run_id> --strict`.
   Exit ≠ 0 → STOP : pas de run suivant, `CLOSE-HANDOFF` avec blockers.
4. **Clôture** — chaque run terminé produit un **`CLOSE-FINAL` automatique** ;
   `CLOSE-HANDOFF` est réservé aux runs **interrompus** (pause en pleine boucle).
5. **Stop conditions** (n'importe laquelle interrompt la séquence) :
   escalade de risque (AGENTS.md Critical Rule 2) · gate FAIL (ADR/POC ou
   loop-closure) · **75 % de contexte** (limite dure,
   [`SESSION_RULES.md` §Context compaction](SESSION_RULES.md)) · fin de
   séquence · borne humaine atteinte.
6. **Hygiène intra-run inchangée** — chaque run autonome exécute la boucle
   complète de sa route (phases ci-dessus), y compris la passe qualité scopée
   selon risque (`prompts/canonical/07-p-vbb-closeout.md` étape 4bis).

Budgets temps long-run (PROGRESS, extensions, FINAL_STATUS) : canoniques dans
[`PILOTAGE.md`](PILOTAGE.md) §LONG-RUN OUTPUT CONTRACT.
