---
context_role: roadmap
phase: strategy
status: active
updated: 2026-07-12
scope: vibebackbone framework → 12 runs progressifs d'amélioration
phase_phase_label: "Roadmap — planification des runs"
---

# 00 — Roadmap : amélioration progressive de vibebackbone

> **Source** : `01_FINDINGS_INDEX.md` (37 findings : 18 Phase 1 multi-service + 4A + 4B + 3C + 3D + 5E).
>
> **Principe** : chaque run est **indépendant**, **shippable**, avec son propre closeout (`docs/runs/{id}/07_CLOSEOUT.md`). La roadmap respecte la doctrine « 1 route = 1 modification = 1 closeout ».
>
> **Cadence** : 1-2 runs par session, ~7-13 semaines pour l'ensemble.
>
> **Statut** : `READY — en attente GO Brice sur Run 1`.

---

## 0. Synthèse — 13 runs planifiés

| # | Route | Thème | Effort | Findings traités | Canon ? | Statut |
|---|-------|-------|--------|------------------|---------|--------|
| **Run 1** | FAST-STANDARD | Quick wins purs #1 (non-canon, 4-5 fichiers) | S | E-002, C-001, D-003, A-003 | non | **READY** |
| **Run 2** | FAST-MINIMAL | Prompts canoniques adoptent P.R2 (3 fichiers) | S | B-001, B-002 | non | READY |
| **Run 3** | FAST-STANDARD | Phase frontmatter sur 5 skills `1-vbb-*` (5 fichiers) | S | B-004 | non | READY |
| **Run 4** | STRUCTURED | Canon longueur descriptions + linter warning | M | E-001, E-004, E-005 | **oui** (CONVENTIONS) | READY après Run 4 |
| **Run 5** | FAST-STANDARD | Compression 10 descriptions Phase 1 (>500 chars) | M | E-003 | non | après Run 4 |
| **Run 6** | STRUCTURED | Loop discipline : 5 skills `1-vbb-*` réfèrent P.R2 + 0-vbb-standard étendu | M | B-003, B-004 (suite) | semi | après Run 3 |
| **Run 7** | STRUCTURED | Handoff vs closeout (kind field + route split + SESSION.history) | M | C-001, C-002, C-003 | **oui** (PILOTAGE) | après Run 1 |
| **Run 8** | STRUCTURED | Multi-service Gap-05/10 : CONTRACTS_CONSUMED + taxonomy consumer (ADR 0015) | M-L | Gap-05, Gap-10 | non (extension) | parallèle dès GO |
| **Run 9** | STRUCTURED | Multi-service Gap-04/06/15 : linter discipline + IMPACT_LOG + CI gate (ADR 0016) | L | Gap-04, Gap-06, Gap-15 | non | après Run 8 |
| **Run 10** | STRUCTURED | Multi-service Gap-01/02/14 : schema projet (db_orientation + project_archetype) (ADR 0014) | M | Gap-01, Gap-02, Gap-14 | non (extension) | parallèle dès GO |
| **Run 11** | STRUCTURED | Multi-service Gap-08/13 : multi-repo + graphe inter-services (ADR 0017) | L | Gap-08, Gap-13 | non (extension) | après Run 8 |
| **Run 12** | STRUCTURED | Length canon + Hermes proxy ADR split + LLM-LOAD-002 P1 | L | D-001, D-002, D-003 | **oui** (CONVENTIONS) | après Run 4 |
| **Run 13** | CLOSEOUT | Synthèse finale + commit + SESSION.md | S | — | — | après Run 12 |

**Total findings adressés** : 37/37.
**Risque canon** : 3 runs (Run 4, Run 7, Run 12) ouvrent `docs/CONVENTIONS.md` ou `docs/PILOTAGE.md` — **CANON_CHANGE_PROPOSAL requis**.

---

## 1. Dépendances entre runs (DAG simplifié)

```
Run 1 (QW #1) ───┐
                  ├──► Run 7 (handoff/closeout)
Run 2 (P.R2 prompts) ──► Run 6 (P.R2 skills) ──► Run 4 (canon descrip.) ──► Run 5 (compression)
                                                                │
                                                                └► Run 12 (length canon + ADRs)

Run 3 (phase frontmatter) ──► Run 6

Run 8 (Gap-05/10) ──► Run 9 (Gap-04/06/15) ──► Run 11 (Gap-08/13)
                                  │
Run 10 (Gap-01/02/14) ───────────┘
                                                          │
                                                          ▼
                                                       Run 13 (CLOSEOUT)
```

**Runs parallélisables** : Run 1/2/3/8/10 peuvent démarrer en parallèle (pas de dépendance forte entre eux).
**Runs sériels** : Run 9 après Run 8 ; Run 11 après Run 9 ; Run 12 après Run 4 ; Run 6 après Run 3.

---

## 2. Run 1 — Quick wins purs #1 (FAST-STANDARD)

> Spec complète : `runs/run-01-quick-wins-batch1.md` (à exécuter après GO).

**Thème** : 4 quick wins purs, sans dépendance, non-canon. Démontre la viabilité de l'approche par runs progressifs.

| Quick win | Fichier | Effort | Statut |
|-----------|---------|--------|--------|
| **AUDIT-E-002** | `skills/0-vbb-standard/SKILL.md` | S | READY |
| **AUDIT-C-001** | `docs/templates/07_CLOSEOUT.md.template` | S | READY |
| **AUDIT-D-003 (1/2)** | `GUIDE.md` (TOC) | S | READY |
| **AUDIT-D-003 (2/2)** | `README.md` (TOC) | S | READY |
| **AUDIT-A-003** | `docs/ARCHITECTURE.md` (premier bloc External Dependencies) | S | READY |

**Total fichiers** : 5 (4 si on compte GUIDE + README comme 1 logique).
**Risque canon** : aucun.
**Pre-merge gate** : SKIP (route FAST, voir `docs/REFERENCE/pre-merge-gate.md`).
**Closeout** : `docs/runs/2026-07-12_run01-quick-wins-batch1/07_CLOSEOUT.md` + entrée ACTIVITY_LOG.

**Livrables attendus** :
- 5 fichiers édités
- `07_CLOSEOUT.md` avec sections standard
- 1 ligne ACTIVITY_LOG

---

## 3. Run 2 — Prompts canoniques adoptent P.R2 (FAST-MINIMAL)

**Thème** : ajouter les références à P.R2 / pre-merge-gate / 04_PLAN dans les prompts canoniques 02-audit, 03-decision, 05-execution.

| Quick win | Fichier | Effort |
|-----------|---------|--------|
| **AUDIT-B-001 (1/2)** | `prompts/canonical/02-p-vbb-audit.md` (ajouter section « Next Phase ») | S |
| **AUDIT-B-001 (2/2)** | `prompts/canonical/03-p-vbb-decision.md` (idem) | S |
| **AUDIT-B-002** | `prompts/canonical/05-p-vbb-execution.md` (référence `@pre-merge-gate.md`) | S |

**Total fichiers** : 3 (≤ 3 → FAST-MINIMAL OK).
**Risque canon** : aucun (prompts sont des guides, pas canon).
**Pre-merge gate** : SKIP.

---

## 4. Run 3 — Phase frontmatter sur 5 skills `1-vbb-*` (FAST-STANDARD)

**Thème** : ajouter `phase: 02_AUDIT` (ou équivalent) en frontmatter des skills d'audit, et créer `docs/PHASE_TO_SKILLS.md`.

| Fichier | Effort |
|---------|--------|
| `docs/PHASE_TO_SKILLS.md` (nouveau) | S |
| `skills/1-vbb-code-janitor/SKILL.md` | S |
| `skills/1-vbb-tech-debt/SKILL.md` | S |
| `skills/1-vbb-monolith-detector/SKILL.md` | S |
| `skills/1-vbb-conventions/SKILL.md` | S |
| `skills/1-vbb-formatter/SKILL.md` | S |
| `skills/0-vbb-standard/SKILL.md` (mise à jour canon) | S |

**Total fichiers** : 7 (> 3 → FAST-STANDARD).
**Risque canon** : semi (touche `0-vbb-standard`). Décision : modifier le standard OU ouvrir une exception. Recommandation : ouvrir `docs/PHASE_TO_SKILLS.md` séparément, garder `0-vbb-standard` intact.

---

## 5. Run 4 — Canon longueur descriptions + linter warning (STRUCTURED)

**Thème** : introduire une cible canonique dans `CONVENTIONS.md` Pillar 1 Readability et un warning non-bloquant dans `vbb-contract-lint.py`.

**Risque canon** : OUI — `CONVENTIONS.md` est canon. **CANON_CHANGE_PROPOSAL requis** (`docs/templates/CANON_CHANGE_PROPOSAL.md.template`).

| Fichier | Effort | Canon ? |
|---------|--------|---------|
| `docs/CONVENTIONS.md` (ajout section « Description length target ») | S | **oui** |
| `tools/vbb-contract-lint.py` (warning non-bloquant) | M | non (extension) |
| `docs/AUDIT_STATUS.md` (entrée AUDIT-E-004) | S | non |

**Total fichiers** : 3.
**Pre-merge gate** : REQUIRED.

---

## 6. Run 5 — Compression 10 descriptions Phase 1 (FAST-STANDARD)

**Thème** : compresser manuellement les 10 descriptions `1-vbb-*` > 500 chars vers cible 500 chars.

| Fichier | Effort |
|---------|--------|
| `skills/1-vbb-logic-duplication-detector/SKILL.md` (669 → 500) | S |
| `skills/1-vbb-premature-abstraction-detector/SKILL.md` (643 → 500) | S |
| `skills/1-vbb-test-mirage-detector/SKILL.md` (616 → 500) | S |
| `skills/2-vbb-spec-validator/SKILL.md` (600 → 500) | S |
| `skills/1-vbb-intent-decomposer/SKILL.md` (598 → 500) | S |
| `skills/1-vbb-code-doc-coherence-auditor/SKILL.md` (594 → 500) | S |
| `skills/0-vbb-audit-readiness/SKILL.md` (588 → 500) | S |
| `skills/1-vbb-adr/SKILL.md` (582 → 500) | S |
| `skills/1-vbb-monolith-detector/SKILL.md` (574 → 500) | S |
| `skills/t-vbb-deploy-runtime/SKILL.md` (573 → 500) | S |

**Total fichiers** : 10 (FAST-STANDARD).
**Risque canon** : aucun.
**Pré-requis** : Run 4 doit avoir posé la cible canon.

---

## 7. Run 6 — Loop discipline skills 1-vbb-* (STRUCTURED)

**Thème** : les 5 skills `1-vbb-*` réfèrent explicitement à P.R2 / 05_EXECUTION / 06_REVIEW dans leur SKILL.md.

| Fichier | Effort |
|---------|--------|
| `skills/1-vbb-code-janitor/SKILL.md` (section « After this skill runs ») | S |
| `skills/1-vbb-tech-debt/SKILL.md` | S |
| `skills/1-vbb-monolith-detector/SKILL.md` | S |
| `skills/1-vbb-conventions/SKILL.md` | S |
| `skills/1-vbb-formatter/SKILL.md` | S |

**Total fichiers** : 5.
**Risque canon** : non (modification de skills, pas du standard).
**Pré-requis** : Run 3 (cartographie phase↔skill créée).

---

## 8. Run 7 — Handoff vs closeout (STRUCTURED)

**Thème** : discrimination explicite entre handoff et closeout.

| Fichier | Effort | Canon ? |
|---------|--------|---------|
| `docs/templates/07_CLOSEOUT.md.template` (déjà fait Run 1) | — | non |
| `docs/PILOTAGE.md` (route split : `CLOSE-HANDOFF` / `CLOSE-FINAL`) | M | **oui** |
| `docs/SESSION_RULES.md` (clarification) | S | semi |
| `prompts/canonical/07-p-vbb-closeout.md` (calcul kind auto) | S | non |
| `docs/SESSION.history/2026-07-12_init.md` (premier handoff archivé) | S | non (gitignored) |

**Risque canon** : OUI — `PILOTAGE.md` est canon. **CANON_CHANGE_PROPOSAL requis**.

---

## 9. Run 8 — Multi-service Gap-05/10 (STRUCTURED)

**Thème** : poser les fondations du tiercé disciplinaire multi-service.

| Fichier | Effort |
|---------|--------|
| `docs/templates/CONTRACTS_CONSUMED.md.template` (nouveau) | M |
| `docs/CONTRACT_DESIGN.md.template` (extension avec champ Consumers) | M |
| `skills/1-vbb-api-contract-designer/SKILL.md` (mention Consumers obligatoire) | S |
| `docs/adr/0015-contracts-consumed-taxonomy.md` (nouvel ADR) | M |
| `docs/INDEX.md` (référence nouvelle convention) | S |

**Risque canon** : non (extensions).

---

## 10. Run 9 — Multi-service Gap-04/06/15 (STRUCTURED)

**Thème** : outillage de la discipline multi-service.

| Fichier | Effort |
|---------|--------|
| `tools/vbb-multiservice-lint.py` (nouveau) | L |
| `docs/templates/IMPACT_LOG.md.template` (nouveau) | M |
| `skills/t-vbb-multiservice-impact/SKILL.md` (nouveau, mise à jour de t-vbb-impact-analyzer) | M |
| `scripts/hooks/pre-commit-multiservice` (nouveau) | M |
| `docs/adr/0016-multiservice-discipline.md` (nouvel ADR) | M |

**Risque canon** : non.

---

## 11. Run 10 — Multi-service Gap-01/02/14 (STRUCTURED)

**Thème** : schéma enrichi pour les projets multi-service.

| Fichier | Effort |
|---------|--------|
| `tools/vbb-project-init.py` (ajout sections db_orientation, project_archetype) | M |
| `docs/extensions/multi-service/README.md` (nouveau) | S |
| `docs/ARCHITECTURE.md` (type bloc enrichi) | S |
| `docs/adr/0014-orientation-extension-schema.md` (nouvel ADR) | M |

**Risque canon** : non (extensions).

---

## 12. Run 11 — Multi-service Gap-08/13 (STRUCTURED)

**Thème** : support multi-repo + graphe inter-services.

| Fichier | Effort |
|---------|--------|
| `tools/vbb-multirepo-init.py` (nouveau) | L |
| `tools/vbb-multiservice-graph.py` (nouveau) | L |
| `docs/MULTIREPO.yaml.example` (nouveau) | M |
| `docs/adr/0017-multi-repo-support.md` (nouvel ADR) | M |

**Risque canon** : non (mais touche `vbb-architecture.py` potentiellement — à vérifier).

---

## 13. Run 12 — Length canon + Hermes ADR split (STRUCTURED)

**Thème** : canon de longueur + compaction des ADRs et SKILL.md outliers.

| Fichier | Effort | Canon ? |
|---------|--------|---------|
| `docs/CONVENTIONS.md` (ajout cibles SKILL.md, ADR, Guide, Audit) | S | **oui** |
| `tools/vbb-md-length-check.py` (nouveau, warning) | M | non |
| `distributions/hermes/proxy/adr/0006-*.md` (split ADR + annexe A) | M | non |
| `distributions/hermes/proxy/adr/0007-*.md` (idem) | M | non |
| `distributions/hermes/proxy/adr/0008-*.md` (idem) | M | non |
| `distributions/hermes/proxy/adr/0009-*.md` (split + annexes A,B) | M | non |
| `distributions/hermes/proxy/adr/0010-*.md` (idem) | M | non |
| `distributions/hermes/proxy/adr/0011-*.md` (idem) | M | non |
| `skills/4-vbb-user-experience-engine/SKILL.md` (compresser 520 → 300) | M | non |
| `skills/1-vbb-intent-decomposer/SKILL.md` (idem 430) | M | non |
| `skills/1-vbb-code-doc-coherence-auditor/SKILL.md` (idem 429) | M | non |
| `skills/1-vbb-code-doc-gap-integrator/SKILL.md` (idem 409) | M | non |
| `skills/2-vbb-spec-validator/SKILL.md` (idem 397) | M | non |
| `docs/AUDIT_STATUS.md` (promotion LLM-LOAD-002 P2 → P1) | S | non |

**Risque canon** : OUI (CONVENTIONS.md). **CANON_CHANGE_PROPOSAL requis**.

---

## 14. Run 13 — CLOSEOUT final

**Thème** : synthèse globale, commit final, SESSION.md, mise à jour CONTEXT.md.

| Fichier | Effort |
|---------|--------|
| `docs/runs/2026-XX-XX_run13-final-closeout/01_INTAKE.md` | S |
| `docs/runs/2026-XX-XX_run13-final-closeout/04_PLAN.md` | S |
| `docs/runs/2026-XX-XX_run13-final-closeout/05_PATCH_SUMMARY.md` | S |
| `docs/runs/2026-XX-XX_run13-final-closeout/07_CLOSEOUT.md` | S |
| `docs/CONTEXT.md` (mise à jour synthèse) | S |
| `docs/SESSION.md` (vidage) | S |
| `docs/INDEX.md` (référence aux nouveaux artefacts) | S |
| `CHANGELOG.md` (entrée release) | S |
| git commit + push | S |

---

## 15. Estimation globale

| Métrique | Valeur |
|----------|--------|
| Nombre de runs | 13 |
| Effort total | ~50-60 heures |
| Cadence | 1-2 runs/semaine |
| Durée totale | ~7-13 semaines |
| Risque canon | 3 runs (4, 7, 12) — CANON_CHANGE_PROPOSAL requis |
| ADR vibebackbone à produire | 4 (0014, 0015, 0016, 0017) + ADR-0013bis (extensions) |
| Nouveaux outils Python | 3 (`vbb-multiservice-lint`, `vbb-multiservice-graph`, `vbb-multirepo-init`, `vbb-md-length-check`) |
| Nouveaux skills | 1 (`t-vbb-multiservice-impact`) |

---

## 16. Garde-fous

### Risques identifiés

| ID | Risque | Mitigation |
|----|--------|-----------|
| R-RM-1 | Canon creep : tentation d'ajouter trop de choses dans `CONVENTIONS.md` | Runs 4, 7, 12 isolent chaque canon change avec CANON_CHANGE_PROPOSAL |
| R-RM-2 | Dérive de la roadmap au fil des runs | `01_FINDINGS_INDEX.md` est la source de vérité ; `00_ROADMAP.md` est régénéré à chaque batch de 3 runs |
| R-RM-3 | Sous-estimation du chemin critique multi-service | Runs 8-11 sont **séquentiels** (Gap-05 → Gap-04 → Gap-08). Pas de raccourci. |
| R-RM-4 | Confusion handoff/closeout pendant la séquence | SESSION.md est mis à jour à chaque closeout ; `kind: HANDOFF\|CLOSEOUT` ajouté dès Run 1 |

### Garde-fous structurels

- **1 run = 1 closeout** : chaque run produit un `07_CLOSEOUT.md` complet
- **Pre-merge gate** obligatoire pour STRUCTURED (Runs 4, 6, 7, 8, 9, 10, 11, 12)
- **CANON_CHANGE_PROPOSAL** obligatoire pour les 3 runs canon (4, 7, 12)
- **ADR vibebackbone** obligatoire pour les 4 ajouts de mécanique (Gap-05/04/08 + extensions)

---

## 17. Action immédiate

**Statut** : ⏸️ EN ATTENTE GO Brice.

**Run 1 prêt à exécuter** : spec complète dans `runs/run-01-quick-wins-batch1.md`.

**Si GO** : exécuter Run 1 (5 fichiers, ~30 min, FAST-STANDARD), closeout, commit, puis revenir pour Run 2.

**Si modifications souhaitées** : indiquer quelles modifications (cadence, scope, runs).

---

## 18. Liens

- [`01_FINDINGS_INDEX.md`](01_FINDINGS_INDEX.md) — index exhaustif des 37 findings
- [`runs/run-01-quick-wins-batch1.md`](runs/run-01-quick-wins-batch1.md) — spec Run 1 prête à exécuter
- `docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md` — source Phase 1
- `docs/audits/audit-{A..E}-*.md` — sources 5 audits