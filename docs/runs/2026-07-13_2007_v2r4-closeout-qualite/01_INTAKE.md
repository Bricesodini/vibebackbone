---
run_id: "2026-07-13_2007_v2r4-closeout-qualite"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T18:07:00Z"
ended_at: "2026-07-13T18:12:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/strategy/vbb-improvements-roadmap/03_PLAN_REDUCTION_V2.md"
  - "docs/REFERENCE/scoped-audit-protocol.md"
  - "docs/runs/2026-07-13_1902_v2r3-audits-scopes/07_CLOSEOUT.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — v2r4-closeout-qualite

## Demande reçue

> GO Brice (2026-07-13) — V2-R4 : étape « passe qualité scopée » dans le
> template/prompt closeout, **déclenchée selon le risque du chantier**
> (pas systématique) ; règle de compaction dans SESSION_RULES.md :
> **40 % de fenêtre = seuil indicatif**, **75 % = limite dure**.

## Reformulation

Fermer la boucle entre les audits scopés (V2-R3) et les projets consommateurs :
au closeout d'un chantier, une passe qualité restreinte au périmètre touché est
exigée quand le risque le justifie — et la discipline de compaction de contexte
(40 % indicatif / 75 % dur) devient une règle écrite de gouvernance de session.
Couvre RB-2 et RB-4 (constat source : trame — doublon 699 lignes et monolithe
1 513 lignes jamais détectés parce qu'aucune passe qualité ne suivait les chantiers).

## Scope

### Dans le périmètre
- `prompts/canonical/07-p-vbb-closeout.md` — nouvelle étape « passe qualité scopée » (déclencheur selon risque, renvoi au protocole canonique)
- `docs/templates/07_CLOSEOUT.md.template` — section de traçabilité de la passe (EXECUTED / SKIPPED-risque-faible / N/A) + case de checklist
- `docs/SESSION_RULES.md` — règle de compaction 40 % indicatif / 75 % limite dure (alignée sur le critère « context <75% » existant)
- `docs/DISTRIBUTIONS.md` §7 — check d'impact Core→4 distributions (Rule 12)

### Hors périmètre
- L'exécution d'une passe qualité réelle sur trame → run dédié V2-R5a
- Le protocole scopé lui-même (`docs/REFERENCE/scoped-audit-protocol.md`, livré en V2-R3, cité, jamais dupliqué)
- PILOTAGE.md et CONVENTIONS.md (canon intact — SESSION_RULES est une règle de session, précédent Run 7)
- Aucun nouvel élément de catalogue (moratoire V2)

### Dépendances détectées
- ADR : `docs/adr/0029-risk-triggered-closeout-quality-pass.md`
- V2-R3 livré (le paramètre `scope` existe — prérequis du plan V2 satisfait)

## Classification du risque

- **Niveau** : `MODÉRÉ`
- **Justification** : modifie le contrat de closeout (gouvernance transverse,
  consommée par les quatre agents) ; additif — aucun closeout existant n'est
  invalidé, la passe est déclenchée par le risque, pas rétroactive.
