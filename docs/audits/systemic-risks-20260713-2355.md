---
audit_type: systemic_risk
date: 2026-07-13
auditor: codex
scope: full_repository_post_sanding
verdict: PARTIAL
run_id: 2026-07-13_2351_deep-post-sanding-audit
---

# Systemic risk audit — post-sanding

## Executive summary

Le dépôt est lisible et ses boucles principales sont largement exécutables,
mais trois risques P1 subsistent au niveau système : le formal executor donne
une fausse assurance, le dernier audit final a contourné le protocole AUDIT, et
les surfaces de reprise ne reflètent pas la fin réelle du ponçage.

## Global verdict

**PARTIAL.** Aucun P0 et aucune corruption observée. Les risques sont bornés et
actionnables, mais ils doivent être arbitrés avant de déclarer le framework
robuste dans son propre usage.

## SYS-POST-001 — Formal executor gate semantics are incorrect

| Champ | Valeur |
|---|---|
| Severity | P1 |
| Type | VIOLATION |
| Evidence Level | VERIFIED_FINDING |
| Decision | NEEDS_DECISION |
| Location | `tools/vbb-executor.py:112-113`, `:158-160`, `:387-394` |

**Finding.** `vbb-executor.py` lit `sub_result["status"]` alors que son propre
résultat expose l'état terminal sous `state` et le statut contractuel sous
`outputs.status`. Il passe aussi toujours `depth=1` au lieu de propager
`depth+1`. Un gate bloquant valide est donc vu `BLOCKED`, et un cycle n'atteint
jamais la limite déclarée.

**Evidence trace.** OBSERVATION — lecture des appels récursifs et du schéma de
résultat → SIGNAL — statut et profondeur incohérents → VÉRIFICATION 1 — appel
en mémoire de `execute_skill('0-vbb-audit-readiness')` retourne `BLOCKED` sur
`scope_must_be_frozen` → VÉRIFICATION 2 — contrat cyclique injecté en mémoire
déclenche `RecursionError` malgré `max_gate_depth: 2` → FINDING.

**Impact.** Les déclarations `docs/ARCHITECTURE.md:185` et
`docs/AUDIT_STATUS.md:129` sur l'enforcement formel complet sont trop fortes.
GMA-003 n'est plus une simple dette de tests/typing : un défaut fonctionnel est
confirmé.

**Recommended action.** Ouvrir une remédiation STRUCTURED : tests de
caractérisation d'abord, statut contractuel explicite, propagation `depth+1`,
détection de cycles, puis réévaluation d'IMPL-002.

## SYS-POST-002 — The final external audit bypassed the AUDIT contract

| Champ | Valeur |
|---|---|
| Severity | P1 |
| Type | VIOLATION |
| Evidence Level | VERIFIED_FINDING |
| Decision | NEEDS_DECISION |
| Location | commit `d0eab3c`, `docs/audits/global-evaluation-20260714-0005.md` |

**Finding.** Le commit du dernier audit contient uniquement ACTIVITY_LOG,
AUDIT_STATUS et le rapport persistant. Il ne contient ni `01_INTAKE`, ni
`02_AUDIT_REPORT`, ni run AUDIT, ni `FINAL_STATUS`; son verdict `SOLIDE` n'est
pas dans la taxonomie READY/PARTIAL/BLOCKED/UNKNOWN.

**Evidence trace.** OBSERVATION — contrat canonique
`prompts/canonical/02-p-vbb-audit.md:9-19` et règle de durabilité de
`docs/PILOTAGE.md` → SIGNAL — artefacts obligatoires absents → VÉRIFICATION —
`git show --name-only d0eab3c` liste trois fichiers et `rg FINAL_STATUS` ne
trouve rien dans le rapport → FINDING.

**Impact.** Le contenu factuel du rapport reste utile, mais sa production
illustre exactement son risque n°1 : l'enforcement comportemental reste
facultatif même pour l'audit final du framework.

**Recommended action.** Ne pas supprimer le rapport ; le requalifier comme
évidence contradictoire et exiger un run AUDIT complet pour les prochains
audits finaux.

## SYS-POST-003 — CLOSE-FINAL did not converge active state

| Champ | Valeur |
|---|---|
| Severity | P1 |
| Type | VIOLATION |
| Evidence Level | VERIFIED_FINDING |
| Decision | NEEDS_DECISION |
| Location | `docs/SESSION.md:12-23`, `docs/CONTEXT.md:37-40`, `docs/PILOTAGE.md:54-67` |

**Finding.** La dernière session déclare `CLOSE-FINAL / READY`, mais SESSION
contient encore des actions non triviales et annonce l'audit global « en
cours » après son commit. CONTEXT annonce 133 tests et demande encore de
stabiliser les hooks/loop closure déjà livrés.

**Evidence trace.** OBSERVATION — règle CLOSE-FINAL : vider SESSION et mettre à
jour CONTEXT → SIGNAL — les deux fichiers racontent un état antérieur →
VÉRIFICATION — closeout V2-R6 déclare la fin, commits `ca70f4a`/`d0eab3c` et
mesure 144 tests contredisent SESSION/CONTEXT → FINDING.

**Impact.** Les deux fichiers obligatoires au boot peuvent orienter une nouvelle
session vers un chantier terminé ou lui faire croire qu'un travail clos est
encore actif.

**Recommended action.** Réconcilier les surfaces actives dans une session de
décision/remédiation distincte et remplacer les métriques statiques par des
références générées.

## SYS-POST-004 — Critical-rule number drift

| Champ | Valeur |
|---|---|
| Severity | P2 |
| Type | VIOLATION |
| Evidence Level | VERIFIED_FINDING |
| Decision | DEFER |
| Location | `README.md:77`, `GUIDE.md:10`, `docs/DISTRIBUTIONS.md:427-435`, `distributions/README.md:53` |

**Finding.** Plusieurs surfaces actives disent que la propagation
Core↔Distribution est la Critical Rule #11. Dans AGENTS.md, #11 est désormais
le gate ADR+POC+Integration et la propagation est #12.

**Evidence trace.** OBSERVATION — références numériques multiples → SIGNAL —
renvoi sémantiquement faux → VÉRIFICATION — comparaison directe avec la liste
canonique AGENTS.md → FINDING.

**Impact.** Les liens atteignent la bonne section générale, mais le lecteur est
dirigé vers la mauvaise règle. Le canon de distribution porte lui-même ce drift.

**Recommended action.** Corriger les références actives et préférer des ancres
stables ou des intitulés aux numéros fragiles.

## Existing risk confirmed — TER-001

Le risque de propagation vers les consommateurs existants reste P1 et ouvert.
Cette passe ne répète pas l'expérience terrain ; elle reprend le finding vérifié
dans AUDIT_STATUS et le rapport global précédent. Aucun mécanisme de refresh
consommateur n'est visible dans les quatre adaptateurs.

## Risks consolidated

| Risque | Severity | Probability | Impact | Action |
|---|---|---|---|---|
| Executor gate failure/cycle | P1 | High | High | Remédiation STRUCTURED avant réutilisation. |
| Audit protocol bypass | P1 | High | High | Gate de run obligatoire pour audit final. |
| Active-state drift | P1 | High | Medium | Générer/réconcilier les surfaces boot. |
| Consumer drift | P1 | High | High | Arbitrer TER-001. |
| Rule-number drift | P2 | Medium | Medium | Correction documentaire bornée. |

## Out of scope

Correction du code, modification du canon, audit des runtimes externes et état
GitHub serveur.

```yaml
FINAL_STATUS:
  verdict: COMPLETE
  global_verdict: PARTIAL
  files_touched:
    - docs/audits/systemic-risks-20260713-2355.md
  tests_run:
    - executor nested-gate reproduction
    - executor cycle reproduction
  risks:
    - SYS-POST-001
    - SYS-POST-002
    - SYS-POST-003
    - SYS-POST-004
  open_points:
    - decisions deferred to 03_DECISION
```
