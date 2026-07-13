---
context_role: reduction-plan-v2
phase: strategy
status: proposal — awaiting GO Brice (aucune exécution avant GO)
updated: 2026-07-13
scope: rebase de 02_PLAN_REDUCTION.md sur l'état réel (SESSION.md 2026-07-13 + tech-debt-20260713-1728.md)
relation: remplace le séquencement de 02_PLAN_REDUCTION.md ; les 8 invariants (§1 de la V1) restent la référence inchangée
---

# 03 — Plan de réduction V2 (rebase du 2026-07-13)

> **Pourquoi un rebase** : la V1 (02_PLAN_REDUCTION.md) a été rédigée alors que les
> 13 runs de `00_ROADMAP.md` étaient déjà exécutés et pushés (session 2026-07-12,
> closeouts commités) — une partie de la V1 était donc DONE ou OBSOLETE à la naissance.
> Depuis : audit tech-debt global (2026-07-13 17:28, verdict `PARTIAL`, 5×P1 TD-101→105)
> et priorité déclarée dans SESSION.md : « run STRUCTURED limité à TD-101 + TD-102 ».

---

## 1. Classement des runs V1 contre l'état réel

| Run V1 | Intitulé | Classement | Justification (état documenté) |
|--------|----------|------------|-------------------------------|
| RA-1 | Réconciliation des vérités | **PARTIAL** | Compteurs AGENTS.md (64/33) désormais exacts (audit tech-debt §inventory) ; **restent** : chemins morts `~/02_Dev` + `/Users/bot` (TD-105, actifs dans AGENTS.md, PILOTAGE.md, RUNBOOK.md, LONG_RUN_RULE.md), double grammaire VibeCodex du `~/.claude/CLAUDE.md` global, compteur « 63 dirs » de CLAUDE.md repo, état stale AUDIT_STATUS/TECH_DEBT (TD-107). |
| RA-2 | Moratoire + park runs 8-11 | **OBSOLETE** | Les runs multi-service 8-11 ont été **exécutés** le 2026-07-12 (18 ADR, `vbb-multiservice-lint.py` livré, commits `eb62f55`→`e00e88a`). Le principe du moratoire est repris en garde-fou V2 (§4), plus comme run. |
| RB-1 | Audits scopés (`scope` janitor/tech-debt/db-robustness) | **TODO** | A-001/A-002 toujours orphelins : aucun run 1-13 ne les couvre ; aucun paramètre `scope` dans les SKILL.md concernés. Demande prioritaire Brice. |
| RB-2 | Routage vers projets consommateurs | **TODO** | Aucune étape « passe qualité scopée » dans le template/prompt closeout. Doublon trame (699 L) toujours ouvert. |
| RB-3 | Autonomie multi-runs (protocole unique) | **PARTIAL → bloqué** | Le contrat long-run est déjà canonisé dans PILOTAGE (LONG_RUN_RULE.md n'est plus qu'une fiche index — mais son pointeur canonique est un chemin mort `~/02_Dev`, TD-105). **Bloquant nouveau** : TD-101 — `vbb-loop-closure-check` auto-sélectionne le mauvais run ; inutilisable comme gate inter-runs tant que non corrigé. |
| RB-4 | Règle 40 % contexte | **TODO** | Rien dans SESSION_RULES.md ; l'outil compactor existe. Inchangé. |
| RB-5 | POC→ADR concret | **PARTIAL** | Largement couvert depuis : contrat de verdict POC enforcé (`07e1e24`), remédiation méthodologie POC close (`f2a7f05`, audit systemic-poc 2026-07-13), 18 ADR exercés. Reliquat (template POC allégé + exemple backbone_knowledge) → backlog. |
| RC-1 | Quick wins (= Runs 1+2+3) | **DONE** | Commits `d261430`, `c7cabb4`, `78c1f2f` (closeouts 2026-07-12). |
| RC-2 | Canon descriptions (= Runs 4+5) | **DONE** | Canon ≤500 chars dans CONVENTIONS + warning lint (`c07d5e0`) ; compressions livrées, linter à 0 warning (`696b776`). |
| RC-3 | Handoff vs closeout (= Run 7) | **DONE** | `kind` auto, SESSION_RULES §Handoff vs Closeout, split `CLOSE-HANDOFF`/`CLOSE-FINAL` dans PILOTAGE (`634f2c1`, CCP approuvé). |
| RC-4 | Régime documentaire étendu | **PARTIAL** | Canons SKILL.md/ADR posés (Run 12 livré, 13/13). **Restent** : canon handoff ≤150 lignes, spec proportionnelle à l'effort, politique d'archivage 90 j — framework **et** projets consommateurs. |
| RC-5 | Diète du boot set | **TODO** | Boot set toujours ~2 150 mots ; à fusionner avec les éditions TD-105 (mêmes fichiers AGENTS/SYSTEM, les toucher une seule fois). |
| RC-6 | Census du catalogue | **TODO** | Non commencé. Note : le runtime dry-run (`43 PASS / 19 PARTIAL / 2 BLOCKED`) mesure la conformité des contrats, **pas l'usage** — il ne peut pas servir de base au census (cf. backlog §3). |

**Corrections de route** (vs V1) : RA-1 était FAST-STANDARD → son reliquat touche le boot
set (canon) et la gouvernance : **STRUCTURED + CCP**. RB-4 était FAST-MINIMAL isolé →
absorbé dans V2-R4, qui passe **STRUCTURED** (il modifie le template/prompt closeout, un
contrat de gouvernance). Depuis Run 7, les clôtures se déclarent `CLOSE-HANDOFF` ou
`CLOSE-FINAL` (plus « CLOSEOUT » générique) : **CLOSE-FINAL après tout run terminé,
CLOSE-HANDOFF réservé aux pauses en pleine boucle.**

---

## 2. V2 — 6 runs (V2-R5 en deux temps)

> **Prérequis avant V2-R1** (conditions du GO) :
> 1. **Réconcilier le worktree non propre** : les fichiers non suivis actuels
>    (audits A-E, strategy multi-service, roadmap, `.pi-subagents/`, `docs/INDEX.md`
>    modifié) doivent être commités en lot(s) dédié(s) ou explicitement affectés à un
>    run — aucun ne doit être supprimé ni laissé en ambiguïté.
> 2. **Gate ADR + POC + intégration** passé pour V2-R1 (`tools/vbb-gate-check.py
>    <run_dir>`, `can_code_start=true`) — cf. AGENTS.md règle 11 : pas de code avant.

| # | Route | Contenu | Sources | Effort | Dépend de |
|---|-------|---------|---------|--------|-----------|
| **V2-R1** Gates fiables | STRUCTURED | Résolution de run **partagée** dashboard/CI/loop-closure à **deux sélecteurs** (« dernier run existant » / « dernier run clôturé », populations distinctes) + tests des noms mixtes (TD-101) ; installateur de hooks **canonique** composant les deux hooks testés, dépréciation de l'autre entrée (TD-102) ; **liaison ADR stricte** dans `vbb-gate-check.py` — une ADR explicitement référencée est vérifiée elle-même, jamais de bascule vers une ADR globale acceptée — + test de non-régression (défaut découvert à la préparation du run, ADR-0027 décision 3). Check d'impact Core→4 distributions (Rule 12) consigné dans `docs/DISTRIBUTIONS.md`. | TD-101, TD-102, défaut gate-linkage (= priorité déclarée SESSION.md) | M | prérequis worktree + gate |
| **V2-R2** Portabilité + vérité unique + diète boot | STRUCTURED (canon, CCP) | **Deux lots distincts.** **Lot Core (repo, commitable)** : purge `~/02_Dev` et `/Users/bot` → dépôt courant / `$VBB_HOME` (TD-105) ; réconciliation AUDIT_STATUS/TECH_DEBT sur entrées vérifiées uniquement (TD-107) ; compteur CLAUDE.md « 63 » ; dédup AGENTS/SYSTEM/CLAUDE (RC-5, cible ≤ ~1 200 mots). Chaque modification Core passe le **check d'impact sur les 4 distributions** (pi, opencode, codex, claude — Critical Rule 12) et s'enregistre dans `docs/DISTRIBUTIONS.md` §Decisions log. **Lot état externe (hors repo, non commitable)** : `~/.claude/CLAUDE.md` global devient pointeur vers le canon VBB (fin de la double grammaire VibeCodex) — opération d'état machine utilisateur, documentée dans le closeout mais exécutée et validée séparément avec Brice. | TD-105, TD-107, RA-1, RC-5, Rule 12 | M | — |
| **V2-R3** Audits scopés | STRUCTURED | Paramètre `scope` pour `1-vbb-code-janitor`, `1-vbb-tech-debt`, `2-vbb-db-robustness` + protocole d'itération par petits scopes (inventaire → passes → registre consolidé). Check d'impact Core→4 distributions (Rule 12) consigné dans `docs/DISTRIBUTIONS.md`. | RB-1 (A-001/A-002 orphelins) | M | — |
| **V2-R4** Closeout consommateurs + compaction | STRUCTURED | Étape « passe qualité scopée » dans template/prompt closeout, **déclenchée selon le risque du chantier** (données/auth/prod/multi-fichier → obligatoire ; FAST-ZERO/MINIMAL → optionnelle), pas systématique (RB-2) ; règle de compaction dans SESSION_RULES.md : **40 % de fenêtre = seuil indicatif** (compactor + mini-handoff recommandés), **75 % = limite dure** (compaction obligatoire avant toute nouvelle action) (RB-4). Check d'impact Core→4 distributions (Rule 12) consigné dans `docs/DISTRIBUTIONS.md`. | RB-2, RB-4 | M | V2-R3 (le scope doit exister) |
| **V2-R5a** Audit terrain trame | AUDIT — **lecture seule** (hors repo VBB) | Janitor + tech-debt **scopés** sur trame : constats et registre uniquement, **zéro patch** (doublon `ProjectConfigPage.tsx` 699 L ×2, `IdeasPage.tsx` 1 513 L, périmètre à confirmer par l'inventaire de scopes). Valide V2-R3/R4 en conditions réelles. | RB-2 terrain, éval. externe 2026-07-13 | S | V2-R3, V2-R4 |
| **V2-R5b** Remédiation trame | STRUCTURED (dans trame) | Remédiation des findings de V2-R5a — **GO Brice dédié requis** sur la sélection des findings avant tout patch ; plan → implémentation → vérif/tests → closeout dans le repo trame. | findings V2-R5a | M | V2-R5a + **GO Brice** |
| **V2-R6** Autonomie multi-runs | STRUCTURED | Protocole « run autonome » : N runs max sans checkpoint humain, loop-closure obligatoire entre runs (fiable après V2-R1), **`CLOSE-FINAL` automatique après chaque run terminé** — `CLOSE-HANDOFF` réservé aux **runs interrompus** (pause en pleine boucle, jamais en fin de run) —, stop conditions (escalade, gate FAIL, limite dure 75 % de contexte). Réparer le pointeur canonique de LONG_RUN_RULE.md au passage. Check d'impact Core→4 distributions (Rule 12) consigné dans `docs/DISTRIBUTIONS.md`. | RB-3 | M | V2-R1, V2-R4 |

```
prérequis (worktree + gate) ──► V2-R1 ──────────────► V2-R6
V2-R2 (parallèle R1)
V2-R3 ──► V2-R4 ──► V2-R5a ──► [GO Brice] ──► V2-R5b
                         └────────────────────────────► V2-R6
```

Cadence indicative : 1 run par session, ~5-7 sessions. Chaque run terminé : 1 route =
1 `CLOSE-FINAL` ; toute pause en cours de run = `CLOSE-HANDOFF`. CCP requis pour V2-R2.

---

## 3. Backlog (hors V2, réexaminer après V2-R6)

- **TD-103** — lot Ruff autofix sûr, puis typage par module (ne pas promouvoir au gate avant baseline verte).
- **TD-104** — tests de caractérisation `vbb-executor` avant tout nettoyage (631 L, 0 test).
- **TD-106** — fonctions longues : uniquement à l'occasion d'un changement fonctionnel couvert.
- **RC-4 reliquat** — canon handoff ≤150 lignes, spec proportionnelle, archivage 90 j.
- **RC-6** — census catalogue. ⚠️ Le runtime dry-run (43 PASS / 19 PARTIAL / 2 BLOCKED)
  mesure la **conformité des contrats**, pas l'usage réel : il ne constitue **pas** une
  base de census. Le census exige une mesure d'usage dédiée (log d'invocation ou tally
  manuel sur ≥2 semaines) avant toute classification ; GO humain obligatoire sur toute
  liste d'archive.
- **RB-5 reliquat** — template POC allégé + exemple backbone_knowledge.
- Multi-service : couche design 100 % (18 ADR) ; implémentation restante = décision séparée, hors périmètre réduction.

---

## 4. Garde-fous

- **Moratoire reformulé** (ex-RA-2, désormais garde-fou) : aucun **nouvel élément de
  catalogue** (skill, prompt) ni **mécanisme exposé à l'utilisateur** pendant V2 — le
  paramètre `scope` (V2-R3) est l'unique exception. Les **helpers internes, scripts et
  tests nécessaires aux runs V2** (ex. fonction de résolution partagée et installateur
  canonique de V2-R1) restent autorisés.
- **Règle d'impact Core → distributions (Critical Rule 12)** : tout run structurel
  touchant le Core (V2-R1, V2-R2, V2-R3, V2-R4, V2-R6) exécute le check d'impact sur
  les quatre distributions (pi, opencode, codex, claude) et consigne la décision dans
  `docs/DISTRIBUTIONS.md` §Decisions log avant son closeout.
- **CCP** requis pour V2-R2 (boot set = canon). GO humain pour toute archive (backlog RC-6).
- « Ne pas convertir cette roadmap en refactor global » (consigne de l'audit tech-debt) :
  V2 n'ouvre ni TD-103 ni TD-106 ; ils restent bornés au backlog.
- Ce document remplace le **séquencement** de la V1 ; les 8 invariants I1-I8 de la V1
  restent la grille de lecture. 02_PLAN_REDUCTION.md est conservé pour traçabilité.

---

## 5. Métriques de sortie V2 (mise à jour)

| Métrique | Baseline 2026-07-13 | Cible fin V2 |
|----------|--------------------|--------------|
| Loop-closure sélectionne le bon run | non (TD-101) | oui, testé |
| Installateurs de hooks concurrents | 2 | 1 canonique |
| Chemins morts dans les surfaces actives | ≥4 fichiers (TD-105) | 0 |
| Grammaires de triage actives | 2 (VBB + VibeCodex global) | 1 |
| Boot set (CLAUDE+AGENTS+SYSTEM) | ~2 150 mots | ≤ ~1 200 |
| Skills anti-slop acceptant `scope` | 0 | ≥3 |
| Passe qualité scopée au closeout consommateur | non | canonisée, **déclenchée selon risque** + audit trame V2-R5a livré (remédiation V2-R5b sur GO dédié) |
| Règle de compaction codifiée | non | 40 % indicatif / **75 % limite dure** |
| Protocole run autonome avec loop-closure inter-runs | non | canonisé (`CLOSE-FINAL` automatique par run terminé, `CLOSE-HANDOFF` réservé aux runs interrompus) |

**Statut** : ⏸️ EN ATTENTE GO Brice. Si GO → V2-R1 (priorité déjà déclarée dans SESSION.md).
