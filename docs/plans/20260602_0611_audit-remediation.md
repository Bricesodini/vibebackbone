# Plan de remediation — Audit vibebackbone 2026-06-02

**Source :** `docs/audits/20260602_0649_audit_vibebackbone.md`
**Route :** STRUCTURED multi-runs (3 P1 séquencés, pas de parallèle — touches à des zones différentes du framework).
**Mode :** modifications dans `~/02_Dev/vibebackbone/` (le framework).
**Verdict audit :** PARTIAL — sain structurellement, souffre de redondances + conventions implicites.

## Findings (rappel)

| ID | Sévérité | Catégorie | Titre court |
|---|---|---|---|
| VBB-AUDIT-001 | **P1** | Prompts | Double système prompts (lifecycle + canonical) non-réconcilié |
| VBB-AUDIT-002 | **P1** | Conventions | P.R1–P.R8 référencés mais nichés sous Pillar 5, pas exposés en `##` |
| VBB-AUDIT-005 | **P1** (escaladé) | Skills | Versioning SKILL.md frontmatter ≠ CONTRACT.yaml, non-détecté par vbb-contract-lint.py |
| VBB-AUDIT-003 | P2 | Skills | Cluster 5 skills "detector" sans matrice de désambiguïsation |
| VBB-AUDIT-004 | P2 | Skills | Cluster 3 skills "doc coherence" sans orchestrateur |
| VBB-AUDIT-006 | P2 | Workers | vbb-audit-worker SOUL.md format artefact vs 0-vbb-audit-readiness format |
| VBB-AUDIT-007 | P2 | Workers | 4 SOUL.md workers structure divergente |
| VBB-AUDIT-008 | P3 | Outils | cody-check `index-search` mapping vers vbb-index.py non documenté |
| VBB-AUDIT-009 | P3 | Conventions | Pillar 1 "20 lignes/fonction" non enforced |
| VBB-AUDIT-010 | P3 | Outils | cody-check --help non routé |
| VBB-AUDIT-011 | P3 | Skills | INDEX.yaml 64 vs 65 dossiers (drift) |

## Plan d'exécution — Séquencement des P1

### Run 1 — STRUCTURED — VBB-AUDIT-002 (P.R1–P.R8 exposés en section `##`)

**Pourquoi d'abord** : changement le plus simple, 1 seul fichier `docs/CONVENTIONS.md`, pas de risque de régression ailleurs. Permet de valider la pipeline "audit → plan → fix → closeout" sur un cas maîtrisé avant les runs plus risqués.

| Champ | Valeur |
|---|---|
| Route | STRUCTURED |
| Worker | `vbb-struct-worker` |
| Complexité | **1/5** (modif cosmétique de TOC + sous-sections) |
| Fichiers | `docs/CONVENTIONS.md` (1 seul) |
| Dépendances | aucune |
| Risque | très faible (doc-only, pas de code, pas de tooling) |
| Validation | `git diff` rend visible ; `python tools/vbb-contract-runtime.py --dry-run` toujours vert (pas de contrat touché) ; lint markdown |
| Durée estimée | 15-30 min |

**Tâche concrète** : promouvoir les `### P.R1` à `### P.R1` sont déjà des sous-sections de Pillar 5 — promouvoir en `## P.R1 — ...` standalone + ajouter une section "## P.R1–P.R8 — Operational Principles" en haut de CONVENTIONS.md avec table de mapping 1 ligne par P.R, et cross-référencer depuis chaque SOUL.md (4 fichiers `.hermes/profiles/vbb-*-worker/SOUL.md`).

### Run 2 — STRUCTURED — VBB-AUDIT-005 (lint version SKILL.md ↔ CONTRACT.yaml)

**Pourquoi après 002** : touche au tooling Python (`tools/vbb-contract-lint.py`), zone plus sensible. Si 001 a des side-effects sur des fichiers YAML, mieux vaut avoir validé 002 avant.

| Champ | Valeur |
|---|---|
| Route | STRUCTURED |
| Worker | `vbb-struct-worker` |
| Complexité | **3/5** (nouvelle règle lint + decision auto-fix vs manual + impact sur 3+ skills) |
| Fichiers | `tools/vbb-contract-lint.py` (ajout règle), `skills/INDEX.yaml` (potentiel), 3+ `skills/*/CONTRACT.yaml` à aligner |
| Dépendances | aucune (peut tourner en // avec 003) |
| Risque | moyen (le linter peut casser d'autres checks s'il est appelé par la CI) |
| Validation | `python tools/vbb-contract-lint.py` exit 0 ; re-run sur les 65 skills ; test sur un skill `version: "1.5"` délibérément divergent pour vérifier que la règle catche |
| Durée estimée | 60-90 min |

**Tâche concrète** : ajouter une règle "SKILL.md frontmatter `version:` == `CONTRACT.yaml` `version:`" dans `vbb-contract-lint.py`. Décider la politique (fail ou warn) — recommandation **warn** d'abord pour ne pas casser les 65 skills d'un coup. Fournir un script de fix (ou doc) pour aligner.

### Run 3 — STRUCTURED — VBB-AUDIT-001 (réconciliation prompts)

**Pourquoi en dernier** : le plus risqué (27+7 prompts, dual-system). Plusieurs stratégies possibles (mapping legacy→canonique, dépréciation, fusion). Demande une décision de fond de Brice.

| Champ | Valeur |
|---|---|
| Route | STRUCTURED (probablement dérive en chantier dette) |
| Worker | `vbb-struct-worker` (premier jet : table de mapping) puis décision Brice |
| Complexité | **4/5** (27 prompts, dual naming, drift sémantique à inventorier) |
| Fichiers | `prompts/canonical/INDEX.yaml` (nouveau), `prompts/0-p-*.md` + `prompts/1-p-*.md` (frontmatter ou sommaire), possiblement `skills/INDEX.yaml` |
| Dépendances | **bloqué par décision Brice** : (a) déprécier `prompts/N-p-*` au profit de canonical, (b) les garder comme extensions lifecycle, (c) fusionner. Recommandation **(b)** avec INDEX explicite. |
| Risque | élevé (touche au routing, à l'adoption par les agents) |
| Validation | grep croisé : aucun agent SOUL.md ne référence un prompt déprécié sans renvoi canonique ; tous les prompts legacy ont un frontmatter `status: legacy\|lifecycle` ; INDEX.yaml liste les 33+7 prompts avec leur statut |
| Durée estimée | 90-120 min (run 1) + décision + 60 min (run 2) |

**Tâche concrète** : produire `prompts/canonical/INDEX.yaml` listant les 7 canoniques + les 26 legacy avec pour chacun : id, titre, statut (canonical/legacy/lifecycle), mapping vers le canonique le plus proche. Frontmatter `status:` ajouté à chaque prompt legacy. Décision finale = Brice.

## Hors P1 — P2/P3 backlog

| ID | Sévérité | Route suggérée | Priorité |
|---|---|---|---|
| VBB-AUDIT-003 | P2 | STRUCTURED | bas — peut attendre après les P1 |
| VBB-AUDIT-004 | P2 | STRUCTURED | bas — idem |
| VBB-AUDIT-006 | P2 | STRUCTURED | moyen — risque de confusion pour l'orchestrateur |
| VBB-AUDIT-007 | P2 | STRUCTURED | bas — template commun, refacto progressif |
| VBB-AUDIT-008 | P3 | FAST | quick win (doc tools) |
| VBB-AUDIT-009 | P3 | chantier dette | out of scope framework-level (radon/flake8 setup) |
| VBB-AUDIT-010 | P3 | FAST | quick win (cody-check --help) |
| VBB-AUDIT-011 | P3 | FAST | quick win (index sync check) |

## Ordre d'exécution

```
Run 1 (VBB-AUDIT-002)  ──→  Run 2 (VBB-AUDIT-005)  ──→  Run 3 (VBB-AUDIT-001, 2 itérations)
   ~30 min                     ~90 min                       ~150 min
                                                                 │
                                                                 ↓
                                                          Décision Brice
                                                          (legacy vs canonical)
```

**Pas de parallélisme** : les 3 P1 touchent des fichiers disjoints mais le risque cumulatif (3 modifs framework-level non-testées) justifie le séquentiel pour pouvoir rollback indépendamment.

## Garde-fous

- Chaque run produit son `docs/runs/<date>_<id>/07_CLOSEOUT.md` avec `FINAL_STATUS`.
- Brice valide entre chaque run (pas de batching).
- Si Run 1 révèle un side-effect inattendu, Run 2 est reporté jusqu'à stabilisation.
- Run 3 (P1 prompts) demande une décision explicite Brice AVANT exécution.

## Pré-requis vérifiés

- `~/02_Dev/vibebackbone` sur main, working tree avec modifs pré-existantes non commitées (à investiguer : `docs/PILOTAGE.md`, `prompts/1-p-vbb-structured-task.md`).
- `~/.hermes/bin/cody-check` fonctionnel.
- `python tools/vbb-contract-lint.py` disponible.
- Artefact `docs/audits/20260602_0649_audit_vibebackbone.md` créé.
- `docs/AUDIT_STATUS.md` sera mis à jour en parallèle par Cody avec le verdict du présent plan.
