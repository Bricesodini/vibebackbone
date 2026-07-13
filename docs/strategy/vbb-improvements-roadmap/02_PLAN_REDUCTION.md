---
context_role: reduction-plan
phase: strategy
status: proposal — awaiting GO Brice
updated: 2026-07-13
scope: vibebackbone framework → réduction sans perte d'essence (« poncer plutôt qu'ajouter »)
relation: réordonne 00_ROADMAP.md (runs discipline conservés, runs multi-service 8-11 PARKED) ; source findings 01_FINDINGS_INDEX.md + évaluation externe 2026-07-13
---

# 02 — Plan de réduction : poncer sans perdre l'essence

> **Origine** : évaluation externe du framework (2026-07-13) + examen de deux projets
> consommateurs (trame, backbone_knowledge). Constats clés :
> 1. Les bénéfices process sont réels (hygiène, traçabilité, reprise, vérification).
> 2. Les skills qualité-code n'atteignent jamais le code des projets consommateurs
>    (doublon 699 lignes + monolithe 1 513 lignes non détectés dans trame).
> 3. Le cérémonial documentaire est surdimensionné (trame : ~3,2 mots de doc / ligne de code).
> 4. Des vérités parallèles actives corrompent la calibration des agents (chemins morts,
>    compteurs divergents, double grammaire VibeCodex/VBB).
> 5. `00_ROADMAP.md` annonce « 37/37 findings adressés » : **faux** — 11 findings sont
>    orphelins (A-001, A-002, A-004, Gap-03, 07, 09, 11, 12, 16, 17, 18), dont les deux
>    qui portent la granularité des audits (A-001/A-002).

---

## 1. Le noyau intouchable — 8 invariants

Tout ce qui suit vise à **renforcer** ces invariants. Règle de ponçage : un élément du
framework qui ne sert directement aucun invariant est candidat à fusion ou archive ;
tout ajout futur doit citer l'invariant qu'il sert.

| ID | Invariant | Support actuel |
|----|-----------|----------------|
| I1 | Itération progressive par **petits runs scopés**, boucle systématique `audit → plan → implement → vérif/test` | AGENTIC_RUN_PROTOCOL (phases 02→07), routes PILOTAGE |
| I2 | **Handoff** = artefact de pause en pleine boucle (human-in-the-loop) | templates 07, docs/handoffs |
| I3 | **Closeout** = fin de boucle : vérif artefacts, commit, push, clean tree | pre-merge-gate, prompt 07-p-vbb-closeout |
| I4 | **Skills anti-slop** (janitor, tech-debt, db-robustness, data-integrity…) avec **choix de granularité du scope** | skills présents, granularité **absente** (A-001/A-002) |
| I5 | **Autonomie disciplinée** : plusieurs runs sans humain en maintenant I1 | AGENTIC_RUN_PROTOCOL + LONG_RUN_RULE (à consolider) |
| I6 | **Compaction de contexte à ~40 %** de fenêtre | vbb-context-compactor (outil OK, règle non codifiée) |
| I7 | **POC successifs → ADR** pour tout non-trivial | vbb-gate-check + Critical Rule 11 |
| I8 | **Conventions canoniques** (CONVENTIONS.md, P1-P5, P.R1-P.R8) | présent, canon de longueur manquant |

---

## 2. Les runs — 3 axes

### Axe A — Assainir (vérité unique)

| Run | Route | Contenu | Effort |
|-----|-------|---------|--------|
| **RA-1** Réconciliation | FAST-STANDARD | Chemins morts : `/Users/bot/.agents/prompts/` (AGENTS.md §Prompt Library), `~/02_Dev/vibebackbone/` (AGENTS.md règle 11, LONG_RUN_RULE.md) → repo réel `~/01_ai-stack/vibebackbone`. Compteurs divergents (63/64 skills, 27/33 prompts) : générer ou supprimer, ne plus maintenir à la main. Corriger le claim « 37/37 » de 00_ROADMAP + réintégrer les 11 findings orphelins dans 01_FINDINGS_INDEX. Trancher la double grammaire : `~/.claude/CLAUDE.md` global (VibeCodex) devient un **pointeur** vers le canon VBB ; une seule famille de skills (vibecodex-\* globaux vs vbb-\* repo). | S-M |
| **RA-2** Moratoire | décision (0 fichier) | Aucun nouveau skill/prompt/outil pendant la phase de réduction, sauf le paramètre `scope` (RB-1). Runs 8-11 multi-service de 00_ROADMAP → **PARKED**, réveil après la phase de réduction. | 0 |

### Axe B — Outiller les invariants (ce qui manque réellement)

| Run | Route | Invariant | Contenu | Effort |
|-----|-------|-----------|---------|--------|
| **RB-1** Audits scopés | STRUCTURED | I4 | Paramètre `scope` (répertoire / module / feature) pour `1-vbb-code-janitor`, `1-vbb-tech-debt`, `2-vbb-db-robustness` (+ `2-vbb-data-integrity` si S). Protocole d'itération : inventaire des scopes → passes successives petit scope par petit scope → registre consolidé. Couvre **A-001, A-002** (orphelins de la roadmap). | M |
| **RB-2** Routage consommateurs | FAST-STANDARD | I4 | La checklist closeout (template 07 + prompt) gagne une étape « passe qualité scopée sur le périmètre touché » : janitor + monolith-detector + logic-duplication-detector avec `scope` = fichiers du chantier. Premier terrain : trame (doublon `ProjectConfigPage.tsx` 699 L, `IdeasPage.tsx` 1 513 L). | S |
| **RB-3** Autonomie multi-runs | STRUCTURED | I5 | Consolider AGENTIC_RUN_PROTOCOL.md + LONG_RUN_RULE.md en **un** protocole « run autonome » : N runs max sans checkpoint humain, `vbb-loop-closure-check` obligatoire entre runs, auto-handoff à chaque frontière de run, stop conditions (escalade de risque, gate FAIL, seuil contexte I6). Deux docs → un. | M |
| **RB-4** Règle 40 % contexte | FAST-MINIMAL | I6 | Codifier dans SESSION_RULES.md : à ~40 % de fenêtre consommée → `vbb-context-compactor` + mini-handoff. L'outil existe ; seule la règle manque. | S |
| **RB-5** POC→ADR concret | FAST-MINIMAL | I7 | Rendre le gate moins abstrait : template POC allégé (hypothèse falsifiable, flux testé, verdict) + exemple canonique tiré de backbone_knowledge (POC_001). 1 page, pas de nouveau mécanisme. | S |

### Axe C — Poncer (réduction)

| Run | Route | Invariant | Contenu | Effort |
|-----|-------|-----------|---------|--------|
| **RC-1** Quick wins | FAST | I8 | = Runs 1+2+3 de 00_ROADMAP (specs déjà écrites : `runs/run-01-*`, `run-02-*`). Inchangés. | S |
| **RC-2** Canon descriptions | STRUCTURED (canon) | I8 | = Runs 4+5 fusionnés : cible ≤500 chars dans CONVENTIONS + warning `vbb-contract-lint` + compression des 10 descriptions Phase 1. CANON_CHANGE_PROPOSAL requis. | M |
| **RC-3** Handoff vs closeout | STRUCTURED (canon) | I2, I3 | = Run 7 : champ `kind: HANDOFF\|CLOSEOUT`, split de route dans PILOTAGE, SESSION.history. CANON_CHANGE_PROPOSAL requis. | M |
| **RC-4** Régime documentaire | STRUCTURED (canon) | I8 | Canons de longueur étendus : SKILL.md ≤300 lignes, ADR 100-200, **handoff ≤150 lignes**, **spec proportionnelle à l'effort du chantier** (une spec de sidebar ne coûte plus 935 lignes). Politique d'archivage : runs/handoffs > 90 jours → archive indexée (framework **et** projets consommateurs). Absorbe Run 12 ; le split des ADRs Hermes passe en annexe optionnelle. | M |
| **RC-5** Diète du boot set | STRUCTURED (canon) | I8 | Dédupliquer AGENTS.md / SYSTEM.md / CLAUDE.md (pre-merge gate, closeout, planning énoncés 2-3×). Cible : boot set ≤ ~1 200 mots (actuel ~2 150). | M |
| **RC-6** Census du catalogue | AUDIT puis décision | I4, I8 | La télémétrie vbb-runtime ne mesure pas l'usage réel (~150 passes uniformes = lint, pas invocations). Mettre en place un census léger (log d'invocation ou tally manuel sur 2 semaines), puis classer les 64 skills : **Noyau / Situationnel / Archive**. Cible indicative ~40-45 actifs. **GO humain obligatoire** sur la liste d'archive. | M |

---

## 3. Séquencement proposé (~8 sessions, 1 run = 1 closeout)

```
S1 : RA-1 + RA-2 + RC-1        (assainir + quick wins déjà spec'd)
S2 : RB-1                      (granularité des audits — valeur la plus attendue)
S3 : RB-2 + RB-4               (routage consommateurs + règle 40 %)
S4 : première passe terrain    (janitor/tech-debt scopés sur trame, valide RB-1/RB-2)
S5 : RC-3 + RB-5               (handoff/closeout canon + POC concret)
S6 : RB-3                      (autonomie multi-runs)
S7 : RC-2 + RC-4               (canons de longueur + régime documentaire)
S8 : RC-5 + RC-6 + closeout    (boot set + census + synthèse)
→ ensuite seulement : réveil des runs multi-service PARKED (8-11) si toujours pertinents.
```

Dépendances dures : RB-2 après RB-1 (le scope doit exister) · S4 après RB-1/RB-2 ·
RC-4 après RC-2 (le premier canon de longueur pose le mécanisme).

---

## 4. Métriques de sortie (mesurables)

| Invariant | Métrique | Baseline | Cible |
|-----------|----------|----------|-------|
| — | Chemins morts dans les canons | ≥3 | 0 |
| — | Compteurs maintenus à la main | oui | générés ou supprimés |
| I4 | Skills anti-slop acceptant `scope` | 0 | ≥3 (janitor, tech-debt, db-robustness) |
| I4 | Passe qualité scopée exécutée sur trame | 0 | ≥1 (doublon 699 L fermé) |
| I5 | Runs autonomes finissant par loop-closure PASS ou handoff | non mesuré | 100 % |
| I6 | Règle 40 % codifiée + appliquée | non | oui |
| I8 | Descriptions ≤500 chars | 10 hors cible | 100 % |
| I8 | Boot set (CLAUDE+AGENTS+SYSTEM) | ~2 150 mots | ≤ ~1 200 |
| I8 | Skills actifs | 64 | ~40-45 (après GO census) |
| — | Ratio doc/code des nouveaux chantiers consommateurs | trame ≈ 3,2 mots/ligne | suivi, tendance ↓ |

---

## 5. Garde-fous

- **CANON_CHANGE_PROPOSAL** requis : RC-2, RC-3, RC-4, RC-5 (CONVENTIONS, PILOTAGE, boot set).
- **GO humain** requis : liste d'archive RC-6, réveil des runs multi-service.
- **Aucune suppression sans archive** : skills et docs retirés vont dans `docs/archive/` indexé.
- 00_ROADMAP.md est régénéré après GO (règle R-RM-2 de la roadmap elle-même) —
  ce document est la proposition, pas une seconde roadmap concurrente.
