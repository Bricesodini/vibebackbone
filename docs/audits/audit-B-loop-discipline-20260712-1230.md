---
run_id: "2026-07-12_1230_audit-B-loop-discipline"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "claude-code"
started_at: "2026-07-12T12:30:00Z"
ended_at: "2026-07-12T13:00:00Z"
next_phase: null
artifacts_consumed:
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "docs/CONVENTIONS.md"
  - "docs/PILOTAGE.md"
  - "docs/REFERENCE/pre-merge-gate.md"
  - "prompts/canonical/01-p-vbb-intake.md"
  - "prompts/canonical/02-p-vbb-audit.md"
  - "prompts/canonical/03-p-vbb-decision.md"
  - "prompts/canonical/04-p-vbb-plan.md"
  - "prompts/canonical/05-p-vbb-execution.md"
  - "prompts/canonical/06-p-vbb-review.md"
  - "prompts/canonical/07-p-vbb-closeout.md"
  - "skills/1-vbb-code-janitor/SKILL.md"
  - "skills/1-vbb-tech-debt/SKILL.md"
  - "skills/1-vbb-monolith-detector/SKILL.md"
  - "skills/1-vbb-conventions/SKILL.md"
  - "skills/1-vbb-formatter/SKILL.md"
artifacts_produced:
  - "docs/audits/audit-B-loop-discipline-20260712-1230.md"
---

# Audit B — Discipline de boucle `audit > plan > implémentation > vérification`

**Date** : 2026-07-12
**Périmètre** : la boucle canonique vibebackbone telle que définie par `AGENTIC_RUN_PROTOCOL.md` + `CONVENTIONS.md` P.R2 + `pre-merge-gate.md`, et son adoption par les prompts canoniques et les skills Phase 1 / Phase 2.
**Question auditée** : est-ce que les agents qui exécutent dans vibebackbone suivent **toujours** la règle « audit → plan → implémentation → vérification » ? Où sont les fuites ?
**Verdict** : `PARTIAL — canon bien défini mais adoption partielle`. La boucle est correcte dans les documents de gouvernance, mais **2 prompts canoniques sur 7** (02-audit, 03-decision) ne référencent pas P.R2 ni le pre-merge-gate, et **5 skills de la famille `1-vbb-*`** n'ont aucune référence aux phases, gates ou P.R2.

---

## Résumé

La boucle canonique est **bien formalisée** :
- 7 phases nommées 01..07 (`AGENTIC_RUN_PROTOCOL.md`).
- P.R2 = « One Verification Loop » avec 5 commandes obligatoires (`CONVENTIONS.md` Pillar 5, P.R2 ; canon dans `pre-merge-gate.md`).
- Le gate pré-exécution (`vbb-gate-check.py`) empêche de commencer à coder sans ADR + POC + Integration (`PILOTAGE.md`).

**Mais** l'adoption est inégale :
- `prompts/canonical/02-p-vbb-audit.md` : 0 référence à P.R2, pre-merge-gate, verification loop, 05_EXECUTION.
- `prompts/canonical/03-p-vbb-decision.md` : 0 référence à P.R2, pre-merge-gate.
- `prompts/canonical/05-p-vbb-execution.md` : 0 référence à P.R2 ou pre-merge-gate (mais a un pré-check anti-dette).
- 5 skills `1-vbb-*` (janitor, tech-debt, monolith-detector, conventions, formatter) : 0 référence à P.R2 ou au pre-merge-gate canonique.
- Aucun skill ne documente explicitement l'**enchaînement** « ce skill est la phase X du run » dans son `SKILL.md`.

**4 findings** (0 P0, 2 P1, 2 P2). Pas de P0 car la gouvernance existe, mais le risque est que les skills `1-vbb-*` soient lancés par des agents qui ne savent pas qu'ils doivent ensuite enchaîner sur `04_PLAN` + `05_EXECUTION` + pre-merge-gate.

---

## Findings

### P1 (2)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-B-001** | Les prompts canoniques `02-p-vbb-audit.md` et `03-p-vbb-decision.md` **ne mentionnent jamais** P.R2, pre-merge-gate, ou la séquence « 5 vérifications obligatoires ». Un agent qui termine une AUDIT (phase 02) ne reçoit pas, dans son prompt, l'instruction explicite d'enchaîner sur 04_PLAN ou de noter dans son rapport ce qui déclenchera P.R2 plus tard. | `grep -c "P\.R2\|pre-merge\|verification loop" prompts/canonical/*.md` → 02-audit: 0 ; 03-decision: 0. | Boucle rompue possible entre 02 AUDIT et 04 PLAN : un agent peut s'arrêter à l'audit sans produire de plan, et le run suivant ne sait pas qu'il doit partir de cet audit. |
| **AUDIT-B-002** | `05-p-vbb-execution.md` (le prompt qui pilote l'implémentation) **ne référence pas P.R2 ni le pre-merge-gate canonique**. Il demande seulement « Les tests sont-ils passés ? » (1 question sur 5 commandes obligatoires). Un agent qui exécute n'a pas dans son prompt la liste explicite des 5 commandes à lancer. | `grep -n "P\.R\|loop\|vérification\|verification" prompts/canonical/05-p-vbb-execution.md` → 1 hit, ligne 234 (à propos de git push, pas de P.R2). | Implémentation qui se déclare `COMPLETE` sans avoir lancé la boucle pre-merge-gate. Dépend uniquement de la discipline humaine du worker. |

### P2 (2)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-B-003** | 5 skills Phase 1 — `1-vbb-code-janitor`, `1-vbb-tech-debt`, `1-vbb-monolith-detector`, `1-vbb-conventions`, `1-vbb-formatter` — n'ont **aucune référence** à P.R2, au pre-merge-gate, ou aux phases 01..07 dans leur SKILL.md. | `grep -c "P\.R\|05_EXECUTION\|06_REVIEW\|gate" skills/1-vbb-{code-janitor,tech-debt,monolith-detector,conventions,formatter}/SKILL.md` → 0 partout. | Un agent qui lance `1-vbb-tech-debt` n'a aucune indication dans son prompt que le résultat doit alimenter 04_PLAN et qu'une remédiation éventuelle devra passer par P.R2. Le skill est "READ-ONLY" mais le lien avec la suite du run n'est pas explicité. |
| **AUDIT-B-004** | Aucun skill ne documente explicitement **à quelle phase il appartient**. La cartographie phase ↔ skill est implicite (reconstruite par le routeur et par l'humain) mais aucun SKILL.md ne contient un frontmatter `phase: 02_AUDIT` ou `phase: 04_PLAN` qui permettrait à un agent de s'auto-positionner. | `head -10 skills/1-vbb-tech-debt/SKILL.md` : frontmatter `phase: 1` (token budget ?). Aucun frontmatter `phase: 02_AUDIT`. | Confusion possible : un agent qui ouvre `1-vbb-tech-debt` ne sait pas s'il doit lui-même passer à 04_PLAN après ou s'arrêter là. |

---

## Adoption par prompt canonique

| Prompt canon | Réf. P.R2 / pre-merge / 05_EXECUTION | Verdict adoption |
|-------------|---------------------------------------|------------------|
| `01-p-vbb-intake.md` | 4 hits | ✅ Adopte |
| `02-p-vbb-audit.md` | 0 hit | ❌ N'adopte pas |
| `03-p-vbb-decision.md` | 0 hit | ❌ N'adopte pas |
| `04-p-vbb-plan.md` | 2 hits | ✅ Adopte |
| `05-p-vbb-execution.md` | 0 hit (mais pré-check anti-dette) | ⚠️ Partiel |
| `06-p-vbb-review.md` | 2 hits | ✅ Adopte |
| `07-p-vbb-closeout.md` | 1 hit | ✅ Adopte |

**3 prompts sur 7** n'adoptent pas explicitement P.R2 ou la séquence de vérification.

## Adoption par skill (échantillon)

| Skill | Réf. P.R / pre-merge / 06_REVIEW | Verdict |
|-------|-----------------------------------|---------|
| `1-vbb-code-janitor` | 0 | ❌ |
| `1-vbb-tech-debt` | 0 | ❌ |
| `1-vbb-monolith-detector` | 0 | ❌ |
| `1-vbb-conventions` | 0 | ❌ |
| `1-vbb-formatter` | 0 | ❌ |
| `1-vbb-adr` | 0 (mention "DECISION" oui) | ⚠️ |
| `1-vbb-api-contract-designer` | 0 | ❌ |
| `1-vbb-intent-decomposer` | 0 | ❌ |

**Sur 8 skills `1-vbb-*` échantillonnés, 8 n'ont aucune référence à P.R2 ou au pre-merge-gate.**

---

## Trou concret (manifestation)

Si Brice lance aujourd'hui la commande suivante (façon Cody) :
```
Skill: 1-vbb-tech-debt
Task: auditer le setup.sh
```

L'agent qui exécute :
1. Ouvre `skills/1-vbb-tech-debt/SKILL.md`.
2. Lit la skill, produit `docs/audits/tech-debt-{date}.md`.
3. **Ne reçoit pas** l'instruction explicite : « ton audit doit contenir un champ `next_phase: 04_PLAN` pour orienter le run suivant ».
4. **Ne reçoit pas** l'instruction : « si tu identifies des findings P0/P1, le run suivant doit appliquer la boucle P.R2 avant de marquer COMPLETE ».
5. Risque : un autre agent ouvre `01-p-vbb-intake.md` pour le run suivant et **ne sait pas** qu'il doit reprendre les findings P0/P1 du précédent.

La boucle n'est pas fermée par les prompts et les skills eux-mêmes. Elle est fermée par le pilote (Cody) et par l'humain.

---

## Comparaison avec ce qui existe bien

| Aspect | Statut | Référence |
|--------|--------|-----------|
| Phases 01-07 nommées | ✅ Défini canoniquement | `docs/AGENTIC_RUN_PROTOCOL.md` |
| P.R2 (5 vérifications) | ✅ Défini canoniquement | `docs/REFERENCE/pre-merge-gate.md` |
| Pre-execution gate | ✅ Défini | `tools/vbb-gate-check.py` |
| Adoption par 01-intake | ✅ | `prompts/canonical/01-p-vbb-intake.md` |
| Adoption par 04-plan | ✅ | `prompts/canonical/04-p-vbb-plan.md` |
| Adoption par 06-review | ✅ | `prompts/canonical/06-p-vbb-review.md` |
| Adoption par 07-closeout | ✅ | `prompts/canonical/07-p-vbb-closeout.md` |
| Adoption par 02-audit | ❌ | gap |
| Adoption par 03-decision | ❌ | gap |
| Adoption par 05-execution | ⚠️ | partiel (pré-check anti-dette seulement) |
| Adoption par skills 1-vbb-* | ❌ | gap |
| Auto-positionnement phase ↔ skill | ❌ | gap |

---

## Recommandations (texte seulement)

| ID reco | Description | Effort | Pré-requis |
|---------|-------------|--------|-----------|
| R-B-1 | Ajouter dans `prompts/canonical/02-p-vbb-audit.md` une section explicite : « AUDIT ne conclut jamais seul. Si findings P0/P1, le rapport DOIT contenir une section `## Next Phase : 04_PLAN` qui résume les inputs du plan à venir ». | S | Aucun |
| R-B-2 | Ajouter dans `prompts/canonical/03-p-vbb-decision.md` une section : « DECISION produit un ADR. Si l'ADR est `ACCEPTED`, le run suivant DOIT être 04_PLAN puis 05_EXECUTION, et l'exécution DOIT passer P.R2 avant COMPLETE ». | S | Aucun |
| R-B-3 | Refondre `prompts/canonical/05-p-vbb-execution.md` pour inclure le bloc canonique des 5 vérifications P.R2 en référence explicite (avec `@pre-merge-gate.md`). Le pré-check anti-dette est conservé mais ne remplace pas P.R2. | M | R-B-1 |
| R-B-4 | Ajouter dans le frontmatter de tous les skills `1-vbb-*` une ligne `phase: 02_AUDIT` (ou `04_PLAN`, etc.) selon leur rôle canonique. Permettre aux agents de s'auto-positionner. | M | Cartographie phase ↔ skill à établir |
| R-B-5 | Ajouter dans chaque skill `1-vbb-*` une section `## After this skill runs` qui décrit explicitement la transition attendue (ex : « après ce skill, le run suivant est 04_PLAN si findings P0/P1 »). | M | R-B-4 |

---

## Quick wins

1. **QW-B-1** — Éditer `prompts/canonical/02-p-vbb-audit.md` pour ajouter une section « Next Phase : 04_PLAN si findings P0/P1 ». 5 minutes. Démontre R-B-1.
2. **QW-B-2** — Éditer `prompts/canonical/05-p-vbb-execution.md` pour inclure le bloc canonique `@pre-merge-gate.md` (référence au canon unique). 5 minutes. Démontre R-B-3.
3. **QW-B-3** — Lister dans `docs/INDEX.md` (ou nouveau fichier `docs/PHASE_TO_SKILLS.md`) la cartographie phase ↔ skill. 10 minutes. Démontre R-B-4.

---

## Unknowns / needs confirmation

| ID | Question | Conséquence |
|----|----------|-------------|
| UN-B-1 | Brice veut-il une **cartographie phase ↔ skill** formelle (frontmatter) ou suffit-il d'un index Markdown ? | Impacte R-B-4 |
| UN-B-2 | Les skills `1-vbb-*` doivent-ils **exiger** un run-id en entrée (pour s'inscrire dans une boucle) ou restent-ils autonomes ? | Change la nature du gate |
| UN-B-3 | Le pré-check anti-dette de `05-p-vbb-execution` doit-il rester ou être remplacé par P.R2 ? | Choix d'implémentation R-B-3 |

---

## Verdict

`PARTIAL — gouvernance canon correcte, adoption inégale, 3 prompts et 5 skills sans ancrage explicite à la boucle P.R2`. Recommandations classées S/M, quick wins disponibles. À traiter **avant** que la Phase 2 de l'évolution multi-service n'ajoute de nouveaux skills (sinon le gap grossit).