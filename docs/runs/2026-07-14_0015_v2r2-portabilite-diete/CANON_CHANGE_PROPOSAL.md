---
run_id: "2026-07-14_0015_v2r2-portabilite-diete"
phase: "03_DECISION"
status: "APPROVED"
agent: "claude-code"
created_at: "2026-07-13T22:25:00Z"
human_validated_by: "Brice — GO explicite « boucler le ponçage, fait tout ce qui permet de finaliser » (2026-07-13), V2-R2 nommément CCP-requis dans le plan validé"
---
# Canon Change Proposal — Diète du boot set (V2-R2)

## Current Canon

AGENTS.md (~896 mots) + SYSTEM.md (~1 041 mots) + CLAUDE.md (~219 mots) forment
le boot set `load_policy: always`. SYSTEM.md restate le triage, le closeout, la
discipline de risque, l'architecture source et les conventions qualité déjà
canoniques dans AGENTS.md ; les deux portent des compteurs manuels
(« 64 skills · 33 prompts », « 63 dirs ») et AGENTS.md cite des chemins
`~/02_Dev` / `/Users/bot`.

## Problem

2 156 mots de boot payés à chaque session par 4 agents ; trois énoncés de la
même règle qui divergent dans le temps (compteurs 63/64, double grammaire) ;
chemins morts qui contredisent la portabilité revendiquée (TD-105). La
duplication est la cause racine des « vérités parallèles » relevées par
l'évaluation externe et l'audit tech-debt.

## Proposed Canon

- AGENTS.md reste **l'unique** énoncé des règles (triage, gates, closeout,
  Rule 12, qualité, credentials).
- SYSTEM.md ne porte que le comportement runtime (posture, plan-first, MVP
  gate, style, artifact grounding) et **pointe** vers AGENTS.md pour le reste.
- Plus aucun compteur maintenu à la main dans les fichiers de boot.
- Plus aucun chemin absolu dépendant d'un HOME ; chemins relatifs au dépôt.
- Cible : boot set ≤ ~1 200 mots, **à contenu normatif constant** (aucune
  exigence supprimée — vérification avant/après par inventaire des règles).

## Benefits

1. ~45 % de contexte de boot en moins, à chaque session, sur les 4 agents.
2. Une règle = un seul endroit → la dérive des énoncés devient impossible.
3. Portabilité réelle (le dépôt fonctionne quel que soit le HOME).

## Risks

- Perte accidentelle d'une exigence pendant la compression → mitigée par
  l'inventaire des règles avant/après (consigné dans 05_EXECUTION) et la
  revue du diff.
- Les agents qui citaient SYSTEM.md pour une règle déplacée doivent suivre le
  pointeur → coût de navigation marginal, assumé.
