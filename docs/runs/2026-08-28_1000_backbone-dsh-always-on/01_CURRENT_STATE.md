---
context_role: audit-state
phase: 01_CURRENT_STATE
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A0
experimental_protocol: DSH-only
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T10:00:00Z"
ended_at: "2026-08-28T10:45:00Z"
next_phase: "02_HYPOTHESIS"
artifacts_consumed:
  - "AGENTS.md"
  - "docs/CONTEXT.md"
  - "docs/MEMORY_AND_HANDOFF.md"
  - "docs/audits/conventions-20260516-1438.md"
  - "docs/runs/2026-08-26_2105_memory-authority-seam/01_INTAKE.md"
  - "docs/runs/2026-08-26_2105_memory-authority-seam/POC.md"
artifacts_produced:
  - "01_CURRENT_STATE.md"
baselined_by: "OBSERVED_ONLY"
baseline_cleaning: "NONE"
related:
  - "docs/adr/0055-memory-authority-seam.md"
  - "docs/runs/2026-08-26_2105_memory-authority-seam/POC.md"
  - "docs/document-model/DOCUMENT_MODEL_REFERENCE_ARCHITECTURE.md"
---

# 01_CURRENT_STATE — baseline observée (non nettoyée)

> Ce document observe l'état de départ de l'expérimentation. Il ne le nettoie
> pas. Aucune fusion, aucun commit, aucun cherry-pick n'a été pratiqué sur le
> working tree pour « fabriquer » une base propre. Tout ce qui est non tracké
> ou modified est documenté tel quel dans §1.

## 0. Pourquoi ce run existe

Le brief utilisateur demande d'expérimenter dans DeepSeek Harness la forme la
plus simple et la plus robuste d'un environnement VibeBackbone où Backbone est
toujours présent, indépendamment du niveau de rigueur (A0 / A1 / A2). Trois
constats motivent ce run :

1. Le canon VBB existe déjà, dispersé entre Core (VBB repo), distribution
   (pi/codex/claude/opencode) et runtime (DSH presets). Aucune doctrine ne dit
   quels actifs doivent être présents au démarrage d'une session DSH
   quelconque, et lesquels peuvent varier.
2. ADR 0055 a tranché la couture d'autorité canon ↔ mémoire (ACCEPTED
   2026-08-26), mais cette couture est validée par POC uniquement — jamais
   exercée par une session DSH réelle observant un changement canonique
   complet (D0 → D3).
3. La lignée `cordis-memory-kernel-poc → kernel vbbk` existe et a été audité
   (campagne A2 du 2026-08-26, 45 vectors). Mais aucune expérience n'a encore
   évalué si le `vbbk` consolidé satisfait réellement la définition de
   Backbone Memory posée par le brief §5–§8.

Ce run teste les invariants A/B/C + intégration Backbone Memory sans rien
ajouter aux distributions et sans créer de routeur automatique de presets.

## 1. État Git observé (baseline non modifiée)

| Champ | Valeur observée |
|---|---|
| HEAD | `c8c513d3d5700fcd8ce46660b4ad9b4fb5c78343` |
| Date HEAD | 2026-08-03 01:44:01 +0200 |
| Message HEAD | `Merge pull request #4 from Bricesodini/codex/document-model-publication-closeout` |
| Branche | `main` |
| Worktree modifié vs HEAD | **3 fichiers** (sujet différent — résolution locale d'ADR) |
| Entrées non-trackées | **6 groupes**, dont ADR 0055, le run `memory-authority-seam`, le run `project-local-adr-resolution`, et le run `qualification-harness-arch-2-slice-2u` (2026-08-28) |
| Statut global | `MIXED` — non-mergeable en l'état, mais ne touchant pas l'expérimentation |

### 1.1 Fichiers modified (hors-sujet pour ce run)

Ces trois fichiers sont marqués modified par un autre chantier en parallèle
(`docs/runs/2026-08-26_project-local-adr-resolution/01_INTAKE.md`). Ils ne
doivent **pas** être absorbés dans une baseline de ce run.

| Fichier | Hash working-tree (sha256) |
|---|---|
| `docs/DISTRIBUTIONS.md` | `f2bcc18721d82b17ee357118cca7c03fc08c594b21d4343ffe43ae56e46b5475` |
| `tests/test_gate_check_adr_linkage.py` | `caf6c5dfa580c3fd92ee7c453eac38a8103a26196c43e24c35c08c958a7f75e6` |
| `tools/vbb-gate-check.py` | `b183a08be5be7a1e8d0fc04f532b8b4127f593cf40ed7f00249e7890de305b2e` |

### 1.2 Entrées non-trackées pertinentes à ce run

| Entrée | Hash (sha256, échantillon) | Statut |
|---|---|---|
| `docs/adr/0055-memory-authority-seam.md` | `22fb28db3961cbc068a0ded1ce7e622bccf5791082f502c24726e00088d31591` | contexte préexistant observable, **non absorbé** |
| `docs/runs/2026-08-26_2105_memory-authority-seam/01_INTAKE.md` | `2a0573132771352db91e1de027bd7a44ff8288dede779a6898e2c5289b94134c` | idem |
| `docs/runs/2026-08-26_2105_memory-authority-seam/POC.md` | `83faeb4ced1c3a23035f98a2a800de45b2a827498cc1ddb69f52ec3b4c1e833f` | idem |
| `docs/runs/2026-08-26_2105_memory-authority-seam/poc/seam_check.py` | `9f5c22250445b780e2550795907385f51a1595afd0cb71185eff9ba00f1e920a` | idem (vérificateur falsifiable) |
| `docs/runs/2026-08-26_2105_memory-authority-seam/poc/fixtures/canon/art_db_choice.md` | `563f611e6e78af208457d41b2232ed30e111b047b3b104845acd5bc9e34afae6` | idem (fixture canon de référence) |

Le dossier `docs/runs/2026-08-26_2105_memory-authority-seam/poc/fixtures/`
contient en outre 4 autres artefacts canon de référence (`art_export_v1`,
`art_export_v2`, `art_shopping_list`, `art_ui_stack`) et 6 fixtures vault
adversariaux (T1 à T6).

### 1.3 Pourquoi ces entrées ne sont pas baseline

Trois raisons, par ordre d'importance :

1. **Commande explicite du brief utilisateur** : ne pas « committer
   artificiellement pour ce run ».
2. **Honnêteté expérimentale** : un run qui falsifie sa baseline se ment à
   lui-même. La couture d'autorité teste précisément les cas où l'état
   observable est mixte (memory stale, canon supersédé), et cette falsification
   commence au niveau du workspace.
3. **Cas réel** : la doctrine doit fonctionner dans un workspace imparfait,
   c'est-à-dire avec des fichiers modified hors-sujet et des artefacts
   expérimentaux non trackés côtoyant le canon publié.

### 1.4 Runs frères encore en cours (non-encore-fermés)

| Run | État observable |
|---|---|
| `2026-08-26_project-local-adr-resolution/` | `01_INTAKE.md` + `07_CLOSEOUT.md` + `POC.md` présents — **clos sans promotion** |
| `2026-08-28_qualification-harness-arch-2-slice-2u/` | `evidence/` (2 captures horodatées 2026-08-28T15:09) + `poc/` — qualification en cours, hors-scope de ce run |

Ces runs sont mentionnés pour mémoire, pas absorbés.

## 2. Inventaire DSH-only — les 6 presets installés

Tous les chemins ci-dessous suivent la convention DSH de
`$HOME/.dsh/.agent-presets/` (en dehors du dépôt VBB, par design — règle
§12 de `AGENTS.md` séparant Core, Distribution et runtime utilisateur).

| Preset | `name:` | `agent.cordis.yml` | Skills | Kernel | Audit |
|---|---|---|---|---|---|
| `vibebackbone` | Vibebackbone | 18 896 B | `vbb-prompt-library` | — | — |
| `vbbk` | VBBK | 8 924 B | `vbbk-authority-seam` | 6 fichiers (`auth`, `entry`, `extraction`, `tools`, `vault`, `verifier`) | `2026-08-26_vbbk-quality-campaign/` (CAMPAIGN + REMEDIATION_PLAN + SYNTHESIS) |
| `cordis-memory-kernel-poc` | Backbone Memory | 16 290 B | — | **9 fichiers** (extraction, hooks, index, lib, plugin, retrieval-tool, retrieval-wiring, user_authority + `package.json`) | — |
| `cordis-memory-poc` | Cordis Memory POC | 11 922 B | — | — | — |
| `cordis-poc` | A0 Native Summarizer POC | 14 130 B | — | — | — |
| `code-goalaware` | PTC — Goal-Aware Code Mode | 15 756 B | — | — | — |

Notes d'observation :

- **Aucun preset ne porte l'étiquette « backbone always-on »**. `vibebackbone`
  est le preset de gouvernance pure ; `vbbk` est une spécialisation à mémoire
  active. Le brief demande une doctrine située entre les deux.
- **Aucune étiquette de tier** (A0 / A1 / A2) n'est portée par un preset. Le
  niveau adversariale est déclaré par run (`adversarial_level:`), pas par
  preset.
- **Aucun preset ne charge `vbb-memory-seam-check`** (le vérificateur Python
  d'ADR 0055 n'a pas encore été promu de `poc/seam_check.py` vers
  `tools/vbb-memory-seam-check.py`).
- **Seul `vbbk` a une campagne d'audit adossée** : 45 vectors, 7 bypasses
  patchés, I2 distinct-identity encore dû (note SYNTHESIS §What is still NOT
  covered).

## 3. Le candidat testé : `vbbk`

Le brief §5 demande que « Backbone Memory soit intégré comme partie
obligatoire ». La direction utilisateur (§point 2) confirme que :

- la lignée historique est `cordis-memory-kernel-poc → expérimentations →
  kernel vbbk` ;
- **le candidat à tester est `vbbk`**, pas une réécriture ;
- l'expérience doit rester libre de conclure `validé / partiel / falsifié`.

| Composant | Rôle observé |
|---|---|
| `kernel/auth.js` | autorisation humaine one-shot token (single-use, secrète) |
| `kernel/entry.js` | capture (écoute `agent/inbox/inserted`) |
| `kernel/extraction.js` | extracteur heuristique model-free (pipeline 5 étapes M6.1) |
| `kernel/tools.js` | surfaces outils (`vbbk_seam_check`, `vbbk_projection_list`, `vbbk_candidate_create`, `vbbk_working_set`, `vbbk_authority_token_mint`, `vbbk_promote`, `vbbk_rebuild_projections`) |
| `kernel/vault.js` | stockage vault JSON avec `subject_key` par `candidate` |
| `kernel/verifier.js` | équivalent JS de `seam_check.py` (codes d'erreur stables, defence-in-depth) |

**Limites assumées**, à reconfirmer par E5/E6 :

1. I2 distinct-identity non exécuté (SYNTHESIS §What is still NOT covered
   n°1).
2. JS ↔ Python parity (codes identiques sur fixtures identiques) non
   ré-exécutée depuis la remédiation.
3. Live session attacks non testés (sortie de la surface statique).
4. Backbone Memory portability (chemins absolus de `cordis-memory-kernel-poc`)
   reste un sujet séparé.

## 4. La lignée `cordis-memory-kernel-poc` (référence, non testée)

Ancien POC ; ne sera pas ré-exécuté dans ce run, conformément à la
direction §2 utilisateur. Conservé pour référence architecturale.

| Fichier kernel | Observation |
|---|---|
| `extraction/`, `hooks.js`, `index.js`, `lib/`, `plugin.js`, `retrieval-tool.js`, `retrieval-wiring.mjs`, `user_authority/` | structure plus dispersée que `vbbk` ; 9 fichiers vs 6 pour `vbbk` |
| `package.json` | présence d'un manifeste npm (absent côté `vbbk`) |

## 5. Briques canoniques VBB déjà existantes (à réutiliser)

| Brique | Localisation | Statut |
|---|---|---|
| ADR 0055 memory-authority-seam | `docs/adr/0055-memory-authority-seam.md` | ACCEPTED 2026-08-26 (non-tracké, voir §1.2) |
| POC seam_check.py + fixtures | `docs/runs/2026-08-26_2105_memory-authority-seam/poc/` | GO (6/6 cas adversariaux rejetés) ; non-promu |
| Documentary Contract v1.0 | `docs/document-model/` (6 fichiers : DIM, Ontology, DGM, DTS, DTP, Référence) | adopted (`.vbb/document-convention.yaml`) |
| ADR catalogue (0001 → 0055) | `docs/adr/` | 55 ADRs ; distribution impact géré par règle §12 |
| `MEMORY_AND_HANDOFF.md` | `docs/` | 3 niveaux de mémoire versionnés |
| `tools/vbb-architecture.py` | `tools/` | graphe canonique, générateur `docs/RELATIONS.md` |
| `tools/vbb-status-dashboard.py` | `tools/` | mesure de l'état global |
| `tools/vbb-gate-check.py` | `tools/` | gate ADR/POC/integration (modified hors-sujet, voir §1.1) |
| `tools/vbb-context-compactor.py` | `tools/` | compaction contexte session |
| `tools/vbb-credentials-gate.py` | `tools/` | non concerné ici |
| `tools/vbb-adversarial-gate.py` | `tools/` | adversarial gate A2 (ADR 0051, ADR 0053) |
| Skills canoniques | `skills/` (64 skills, 7 sections normalisées) | catalog stable |
| Prompts | `prompts/` (5 phases canoniques + spécialisés + router) | catalog stable |

## 6. Mapping — invariants du brief ↔ actifs existants

Le brief pose 4 axes (§2–§9) : A — logique de travail, B — capabilities, C —
rigueur documentaire, M — intégration Backbone Memory. Le tableau ci-dessous
note ce qui est en place, partiel, ou manquant **avant** que ce run propose
quoi que ce soit.

### 6.1 Invariant A — Logique de travail toujours active (brief §2)

| Sous-exigence | Actif observé | Statut |
|---|---|---|
| Cycle « comprendre → contexte → canon → agir borné → vérifier → documenter → continuité » | persona text de `vbbk` agent.cordis.yml (cf. citations de la première passe) | **partiel** : présent dans le persona `vbbk`, **absent** du persona `vibebackbone` |
| Discipline « ne pas modifier avant de comprendre, ne pas inventer de vérité parallèle, distinguer faits / hypothèses / décisions » | `MEMORY_AND_HANDOFF.md` §Anti-patterns + ADR 0055 §C1 | **présent** dans Core, mais **pas relié au runtime DSH** |
| Périmètre explicite | règle de plans `04_PLAN.md` (STRUCUTRED) | **partiel** : vaut en mode plan-first, pas en runtime générique |
| `docs/SESSION.md` gitignored | `.gitignore` confirmé dans audit conventions | **présent** |

### 6.2 Invariant B — Capabilities / skills discovery (brief §3)

| Sous-exigence | Actif observé | Statut |
|---|---|---|
| Skills exposés en discovery | `tools/vbb-architecture.py` inventorie `skills/` | **présent** |
| Skill VBBK authority-seam | `$HOME/.dsh/.agent-presets/vbbk/skills/vbbk-authority-seam/SKILL.md` | **présent pour `vbbk`**, **absent pour `vibebackbone`** |
| Skill prompt-library | `$HOME/.dsh/.agent-presets/vibebackbone/skills/vbb-prompt-library/SKILL.md` | **présent pour `vbbbone`**, **point d'entrée prompts canon** |
| Chargement progressif (pas d'injection totale) | catalogues skills, pas de « tout dans prompt » | **partiel** : par défaut DSH charge `SKILL.md` à la demande — mais le persona peut forcer l'inclusion |
| Skills Backbone Memory dans `vibebackbone` preset | **aucun** | **manquant** |
| `vbb-memory-seam-check` exposé aux presets | **absent** (non-promu) | **manquant** |

### 6.3 Invariant C — Rigueur documentaire (brief §4)

| Sous-exigence | Actif observé | Statut |
|---|---|---|
| Canon courant identifiable | `CONTEXT.md` + `INDEX.md` + `AUDIT_STATUS.md` + `MEMORY_AND_HANDOFF.md` | **présent** (3 niveaux de mémoire articulés) |
| Version active / superseded / experimental / historique | ADR 0055 §C2 (`projection` reflects canon) + Documentary Contract v1.0 | **partiel** : modèle conceptuel présent, **pas d'outil DSH de navigation** canon/superseded |
| Archivage progressif | `docs/archive/` existe ; logique de supersession ADR 0049 ; `seam_check.py` détecte `PROJECTION_STALE_SUPERSEDED` | **présent pour les ADR**, **non généralisé aux artefacts non-ADR** (README, SPEC ad hoc) |
| Pas de vérité parallèle — détection | `seam_check.py` T1 (CANDIDATE_CONTRADICTION_UNFLAGGED) + T4 (CONFLICT_AUTO_RESOLVED) | **présent dans le vérificateur**, **pas exécuté dans un run DSH réel** |
| Canon comme état navigable | `docs/document-model/` DIM + Ontology, ADR 0049 lifecycle, ADR 0055 C4 projection map | **partiel** : modèle conceptuel riche ; **pas de dérivation mécanique** CURRENT_CANON/ACTIVE_DECISIONS/SUPERSEDED/HISTORICAL |

### 6.4 Invariant M — Backbone Memory gouvernée (brief §5–§9)

| Sous-exigence | Actif observé | Statut |
|---|---|---|
| Distinction fait canonique / décision / hypothèse / expérience / working / superseded / historique | ADR 0055 §C2 (3 classes : `projection`, `candidate`, `working`) | **partiel** : 3 classes seulement ; le brief demande 8 catégories sémantiques |
| Promotion par gate | ADR 0055 §C3 ; `seam_check.py` `--selftest` valide | **présent** (POC) |
| Autorisation humaine explicite traçable | vbbk `kernel/auth.js` (post P2.a, secret module-privé) + A5 d'ADR 0055 (`PROMOTION_WITHOUT_AUTHORIZATION`) | **présent côté `vbbk`**, **non vérifié en session DSH** |
| Synchronisation canon ↔ mémoire (D0 → D3, brief §7) | ADR 0055 §C5 + `seam_check.py` T2 (`PROJECTION_STALE_SUPERSEDED`) + T5 (round-trip rebuild) | **logique présente, jamais démontrée dans une vraie session DSH** |
| Memory ≠ canon (détection divergence) | ADR 0055 §C5 + `seam_check.py` | **présent** |
| Memory indisponible → Backbone continue (F6) | non testé | **manquant** |

## 7. Lacunes identifiées vis-à-vis du brief

Synthèse des observations §6, en miroir exact des invariants posés par
l'utilisateur.

| # | Lacune | Sévérité pour ce run |
|---|---|---|
| L1 | Aucun preset DSH n'a explicitement le rôle « backbone always-on » ; le brief demande une doctrine, pas un kernel supplémentaire | majeure |
| L2 | Le vérificateur `seam_check.py` n'est pas promu en `tools/vbb-memory-seam-check.py` ; n'est donc exposé à aucune session | majeure |
| L3 | La distinction 8-cat du brief §6 n'est pas alignée sur les 3 classes d'ADR 0055 (`projection`/`candidate`/`working`) | moyenne — jonction à arbitrer en E3/E5 |
| L4 | Aucun mécanisme DSH ne détecte un README historique présenté comme actif (F2) | moyenne — expérience agentique requise |
| L5 | Aucun mécanisme DSH ne détecte la récence prise comme autorité (F3) | moyenne — expérience agentique requise |
| L6 | Aucun mécanisme DSH ne détecte deux documents concurrents (F4) | moyenne — expérience agentique requise |
| L7 | Aucun test n'a été mené sur F6 (Memory indisponible, Backbone continue) | moyenne — script de dégradation à concevoir en E6 |
| L8 | I2 distinct-identity du kernel `vbbk` non exécutée | basse pour ce run (notre A0/A1 cible est indépendant, mais à rappeler si E5 pousse A2) |
| L9 | runtine Pi `NOT_ASSESSED` dans `.vbb/document-convention.yaml` | hors-sujet (autre chantier), mais à garder en tête |

## 8. Décisions implicites déjà prises avant E1 (rappel)

Toutes prises par ADR ou POC antérieurs, ne sont **pas re-débattues** dans ce
run :

- ADR 0049 — gouvernance du savoir d'ingénierie : le canon ne change que par
  une nouvelle version gouvernée.
- ADR 0050 — assurance Design / Certification : FINAL_STATUS et
  ASSURANCE_STATUS orthogonaux.
- ADR 0051 + 0053 — dimension adversariale post-cutoff (`1.2`).
- ADR 0052 + 0054 — Documentary Contract v1.0.
- ADR 0055 — couture canon ↔ mémoire (ACCEPTED 2026-08-26, A1+A2+A5
  amendements). Cette couture est la **référence contractuelle** des E3, E4,
  E5.
- POC seam_check.py 2026-08-26 — verdict GO.
- vbbk quality campaign 2026-08-26 — 45 vectors, 7 patchs (P0 path traversal,
  P1.a field filter, P1.b absolute path, P2.a drop getSecret export, P2.b
  nested canonical claim, P2.c intra-canon contradiction). T10.2 (oversized
  value, DoS surface) déféré.

## 9. Hors-périmètre confirmé pour ce run

Répétition du §14 du brief, paraphrasé :

- Aucune modification Core au-delà des outils déjà existants.
- Aucune modification des distributions.
- Aucun routeur automatique de presets.
- Aucune nouvelle autorité de canon.
- Aucune promotion automatique d'une sortie LLM vers le canon.
- Aucune duplication d'outils existants.
- Aucune extension inter-harness.
- Le workspace reste **non commité** et **non nettoyé** durant tout le run.

## 10. Provenance de E1

| Information | Valeur |
|---|---|
| Run créé | `2026-08-28T10:00:00Z` (déclaré ; cohérent avec timeline des autres artefacts 2026-08-28) |
| Source primaire du contenu | lecture directe du working tree (`ls`, `git status`, `git rev-parse`, `sha256sum`, lecture des `agent.cordis.yml`, `preset.yml`, `SKILL.md`, `SYNTHESIS.md`, ADR 0055, seam_check.py) |
| Méthode | observation + lecture, **sans modification** |
| Falsifiabilité | E1 peut être ré-exécuté à tout moment en rejouant exactement les mêmes lectures ; seules les valeurs de HEAD / hashes changeront |
| Dépendance à un sous-agent | aucune — E1 ne dépend d'aucun autre preset/kernel que ceux déjà installés |

## 11. Ce qui reste à faire dans E1 (fermeture)

- [x] Baseline Git observée, hashes capturés, modified et untracked documentés
- [x] Inventaire DSH presets
- [x] Cartographie invariants ↔ actifs
- [x] Lacunes identifiées vis-à-vis du brief
- [x] Hors-périmètre réaffirmé
- [x] Provenance capturée
- [ ] Re-exécution de `seam_check.py --selftest` pour preuve de stabilité
      du vérificateur (à reporter ici par E2 si nécessaire, ou laisser en
      héritage de POC 2026-08-26)

---

## 12. Handoff vers `02_HYPOTHESIS.md`

Entrées à lire pour la phase suivante :

- §6 (mapping invariants ↔ existants) — base objective, non hypothétique
- §7 (lacunes identifiées) — ce que l'expérience doit trancher
- §8 (décisions implicites acquises) — ce qui **ne** doit pas être re-débattu

Points de vigilance pour E2 :

- L'hypothèse centrale du brief (§1) doit être reformulée en **une
  hypothèse falsifiable unique**, pas une collection. Si plusieurs
  hypothèses sont nécessaires, elles doivent être numérotées et chaque
  falsification listée explicitement.
- La distinction 3-classes d'ADR 0055 (`projection`/`candidate`/`working`)
  vs la distinction 8-cat du brief §6 doit être résolue : soit on reconnait
  que les 3 classes sont **canoniques** et que les 8 catégories sont des
  **étiquettes sémantiques** projetées sur les classes (gagnant) ; soit
  on constate qu'il faut une 4ᵉ classe (perdant : ouvre une nouvelle
  source d'autorité). E2 doit choisir entre les deux avec falsification.
- L'expérience F2/F3/F4 (brief §12) doit utiliser le couple « fixtures
  déterministes + revue déterministe des propriétés observables »,
  conformément à la décision utilisateur du point 3. Aucune revue
  purement lexicale fragile.

Verdict E1 : `READY` → E2 peut démarrer.
