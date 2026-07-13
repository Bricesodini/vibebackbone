---
run_id: "2026-07-12_1400_audit-E-skill-descriptions"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "claude-code"
started_at: "2026-07-12T14:00:00Z"
ended_at: "2026-07-12T14:30:00Z"
next_phase: null
artifacts_consumed:
  - "skills/0-vbb-standard/SKILL.md"
  - "skills/*/SKILL.md (all 64)"
  - "skills/INDEX.yaml"
  - "tools/vbb-phase-router.py"
  - "tools/vbb-contract-lint.py"
  - "tools/vbb-contract-runtime.py"
  - "tools/vbb-context-compactor.py"
  - "tools/vbb-status-dashboard.py"
  - "tools/vbb-index.py"
  - "setup.sh"
  - "setup-lib.sh"
  - "distributions/codex/setup.sh"
  - "docs/audits/doc-context-20260602-1329.md"
  - "docs/AUDIT_STATUS.md"
  - "docs/CONTEXT.md"
artifacts_produced:
  - "docs/audits/audit-E-skill-descriptions-20260712-1400.md"
---

# Audit E — Descriptions des skills et « auto-réduction Codex »

**Date** : 2026-07-12
**Périmètre** : les 64 `SKILL.md` du repo, focalisation sur le champ `description:` du frontmatter, et le mécanisme que Brice a vu en action (« Codex a automatiquement réduit le descriptif des skills car trop long »).
**Question auditée** :
1. Quelle est la longueur réelle des descriptions ?
2. Existe-t-il un mécanisme canon ou automatique qui tronque les descriptions ?
3. Que sait-on de la « auto-réduction Codex » mentionnée par Brice ?
4. Quel est le risque si la description est tronquée automatiquement (perte d'information, mauvais routage) ?
**Verdict** : `PARTIAL — la « auto-réduction Codex » est un mécanisme **de remplacement de bloc généré** dans `~/.codex/AGENTS.md`, pas une troncature des descriptions SKILL.md. Les descriptions du repo ne sont **pas** tronquées automatiquement. Aucun canon de longueur. Phase 1 a les descriptions les plus longues (506 chars moyenne, 10/16 > 500 chars).`

---

## Résumé

Brice se souvient de messages Codex indiquant que les descriptions des skills ont été « automatiquement réduites car trop longues ». L'investigation révèle que **ce n'est pas exactement ce qui s'est passé** :

1. **Le mécanisme de « auto-réduction » existe** mais concerne `~/.codex/AGENTS.md` (le fichier **installé** chez l'utilisateur), pas les `SKILL.md` du repo.
2. Il s'agit d'un **remplacement de bloc généré** entre marqueurs `<!-- vibebackbone:generated:start -->` / `<!-- vibebackbone:generated:end -->`, opéré par `distributions/codex/setup.sh` lors d'un re-run de `setup.sh`.
3. L'audit `doc-context-20260602-1329.md` documente cette réduction : `~/.codex/AGENTS.md` est passé de **253.8 KB / 7296 lignes → 12.3 KB / 344 lignes** (réduction de 95%).
4. **Aucune troncature automatique des `description:`** des `SKILL.md` in-repo n'a été trouvée. Le champ reste à la main.

**Distribution actuelle des descriptions in-repo** :
- **64 skills**, total **27,581 chars**, moyenne **430 chars/description**.
- **Aucune cible canon** de longueur (`docs/CONVENTIONS.md` et `0-vbb-standard/SKILL.md` vérifient la *précision*, pas la longueur).
- **20 skills > 500 chars**, **0 skill > 1000 chars**, **max = 669 chars** (`1-vbb-logic-duplication-detector`).
- Phase 1 (`1-vbb-*`) a les descriptions les plus longues : **506 chars moyenne, 10/16 > 500 chars**.
- Phase 4 (`4-vbb-*`) a les descriptions les plus courtes : **360 chars moyenne** (front pipeline déjà compacté).

**5 findings** (0 P0, 2 P1, 3 P2). Le P1 principal est l'absence de canon de longueur, qui laisse les descriptions dériver.

---

## Findings

### P1 (2)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-E-001** | **Aucun canon de longueur** pour les `description:` des `SKILL.md`. `docs/CONVENTIONS.md` (Pillar 1 Readability) parle de « clear, descriptive names over abbreviations » et de `target around 20 lines per function`, mais **rien sur la longueur des descriptions**. `skills/0-vbb-standard/SKILL.md` ligne 75-85 (PROCESS) exige « description is precise enough for Pi routing » — c'est un test de **précision**, pas de longueur. | `grep -n "description" docs/CONVENTIONS.md` → 0 hit pertinent. `0-vbb-standard/SKILL.md` ligne 75-85 ne donne pas de cible numérique. | Pas de juge objectif pour « cette description est trop longue ». Pas de moyen de refuser une PR qui ajoute une description à 1500 chars. |
| **AUDIT-E-002** | Le mécanisme dit « **Codex auto-réduit les descriptions** » est en fait un **bloc-remplacement** dans `~/.codex/AGENTS.md`, **pas une troncature des descriptions** des SKILL.md du repo. Si Brice pense que les descriptions sont auto-tronquées, il peut y avoir une **confusion de modèle mental** : il pourrait croire qu'une PR avec une description à 800 chars sera « corrigée automatiquement » au prochain setup.sh, ce qui est faux. | `distributions/codex/setup.sh` : la fonction `replace_generated_block()` ne touche **que** le bloc entre `<!-- vibebackbone:generated:start -->` et `<!-- vibebackbone:generated:end -->`. Les descriptions des `SKILL.md` sont inlinées via `open(agents_src).read()` mais ne sont pas elles-mêmes tronquées. `docs/audits/doc-context-20260602-1329.md` ligne 25 confirme la réduction sur `~/.codex/AGENTS.md`, pas sur les SKILL.md. | Confusion possible : si Brice demande « tronque la description de cette skill », un agent pourrait appliquer le mauvais mécanisme (modifier `setup.sh` au lieu de raccourcir manuellement la description). |

### P2 (3)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-E-003** | **Phase 1 (`1-vbb-*`) a les descriptions les plus longues** : moyenne 506 chars, 10/16 skills > 500 chars. La plus longue (`1-vbb-logic-duplication-detector`, 669 chars / 13 lignes) inclut keywords + phrase d'introduction + description de comportement + redirection vers une autre skill. | Distribution par phase : `1-vbb: avg 506 chars, 10/16 > 500` ; `0-vbb: 423/7` ; `2-vbb: 417/12` ; `3-vbb: 415/1` ; `4-vbb: 360/10` ; `t-vbb: 417/17`. | Charge cognitive pour qui scanne les skills. Risque LLM si un agent doit digérer plusieurs descriptions d'un coup (par exemple dans `vbb-status-dashboard --review-tier`). |
| **AUDIT-E-004** | Les **5 SKILL.md > 400 lignes** (LLM-LOAD-002 dans AUDIT_STATUS, statut **Open**) ne sont pas les mêmes que les 20 descriptions > 500 chars. Ce sont deux problèmes distincts : (a) corps de la skill trop long (LLM-LOAD-002, reconnu, non traité) ; (b) description du frontmatter trop longue (non reconnu). Le couplage est faible — les deux peuvent être traités indépendamment. | `docs/AUDIT_STATUS.md` ligne 197 : `LLM-LOAD-002 (P2) : Five SKILL.md files exceed 13 KB`. Audit D du 2026-07-12 confirme 5 SKILL.md > 400 lignes (520, 430, 429, 409, 397). Pour les descriptions, 20 skills > 500 chars (cf. AUDIT-E-003). | Suivi dispersé : LLM-LOAD-002 est tracked, mais aucune entrée pour les descriptions longues. |
| **AUDIT-E-005** | **Aucun linter ne valide** la longueur de la `description:`. `tools/vbb-contract-lint.py` valide `contract_schema_version`, gates, routing — **rien sur la description SKILL.md**. `tools/vbb-phase-router.py` consomme `routing.triggers` du CONTRACT.yaml, **pas la description**. | `grep -n "description" tools/vbb-*.py` : seul `vbb-context-compactor.py:31` extrait le frontmatter, mais pour `run_id, voie, status, agent` (pas description). | Pas de garde-fou CI. Une PR qui ajoute une description à 2000 chars passe. |

---

## Investigation du mécanisme « Codex auto-réduction »

### Chronologie reconstituée

| Date | Événement | Source |
|------|-----------|--------|
| 2026-06-02 | Audit `doc-context-20260602-1329.md` documente : « Installed Codex governance `~/.codex/AGENTS.md` reduced from 253.8 KB / 7296 lines to 12.3 KB / 344 lines » | `docs/audits/doc-context-20260602-1329.md` ligne 25 |
| 2026-06-02 | Audit identifie aussi « **5 SKILL.md files exceed 13 KB** » comme risque LLM-LOAD-002 | `docs/audits/doc-context-20260602-1329.md` ligne 56-60 |
| 2026-06-02 | `setup.sh` réparé pour « replace from first generated marker to last generated marker » | AUDIT_STATUS.md ligne 197 (LLM-LOAD-001) |
| 2026-06-13 | Hardening Run 20C : « Agent language: 53/64 SKILL.md body EN-clean, 10 remaining (Phase 4 + spec-validator) » | AUDIT_STATUS.md ligne 38 |
| 2026-06-29 | Quality adoption audit (PASS) ; LANG-001 et LANG-002 acceptés | AUDIT_STATUS.md ligne 220-230 |

### Le mécanisme, en clair

`distributions/codex/setup.sh` (sourcé depuis `setup.sh`) installe `~/.codex/AGENTS.md` avec un bloc généré entre `<!-- vibebackbone:generated:start -->` et `<!-- vibebackbone:generated:end -->`. La fonction `replace_generated_block()` :

1. Cherche le **premier** `START` dans le fichier existant.
2. Cherche le **dernier** `END` dans le fichier existant.
3. Remplace le contenu entre les deux par le nouveau bloc construit par `build_block()`.
4. Le bloc construit inclut `AGENTS.md` + `SYSTEM.md` + une section « Vibebackbone Prompt Library ».

**Quand setup.sh est ré-exécuté**, si l'utilisateur a manuellement ajouté du contenu entre les marqueurs ou si une version précédente a laissé du contenu stale après le END, ce contenu est écrasé. C'est la « auto-réduction ».

**Ce que ce mécanisme ne fait PAS** :
- Il ne touche pas aux `SKILL.md` du repo.
- Il ne tronque pas la `description:` du frontmatter.
- Il ne s'applique qu'à `~/.codex/AGENTS.md` (pas aux autres providers).

### Pourquoi Brice a vu « descriptions réduites »

Le bloc généré dans `~/.codex/AGENTS.md` contient :
- Le contenu de `AGENTS.md` (150 lignes).
- Le contenu de `SYSTEM.md` (201 lignes).
- Une section « Vibebackbone Prompt Library » (~20 lignes).

Soit ~370 lignes au total. Mais le fichier avait 7296 lignes, dont la majorité était du **contenu stale** ou des **générations imbriquées** (le bug « nested-marker » mentionné dans l'audit). La « réduction » a donc éliminé ~6900 lignes de bruit, **pas réduit les descriptions elles-mêmes**.

L'impression de « descriptions réduites » vient probablement du fait que la **densité d'information utile par ligne** a augmenté : avant, le fichier était 7296 lignes dont 90% de bruit ; après, il est 344 lignes dont 100% d'information canonique. Mais aucune description de skill n'a été raccourcie individuellement.

---

## Distribution statistique des descriptions

### Distribution par longueur

| Bucket | Count | % |
|--------|-------|---|
| < 300 chars | 3 | 5% |
| 300-400 chars | 21 | 33% |
| 400-500 chars | 20 | 31% |
| 500-600 chars | 13 | 20% |
| 600-700 chars | 7 | 11% |
| > 700 chars | 0 | 0% |

**P50 = ~430 chars · P90 = ~580 chars · P99 = ~670 chars**.

### Top 10 des descriptions les plus longues

| # | Skill | Chars | Lignes |
|---|-------|-------|--------|
| 1 | `1-vbb-logic-duplication-detector` | 669 | 13 |
| 2 | `1-vbb-premature-abstraction-detector` | 643 | 14 |
| 3 | `1-vbb-test-mirage-detector` | 616 | 13 |
| 4 | `2-vbb-spec-validator` | 600 | 12 |
| 5 | `1-vbb-intent-decomposer` | 598 | 11 |
| 6 | `1-vbb-code-doc-coherence-auditor` | 594 | 11 |
| 7 | `0-vbb-audit-readiness` | 588 | 11 |
| 8 | `1-vbb-adr` | 582 | 11 |
| 9 | `1-vbb-monolith-detector` | 574 | 12 |
| 10 | `t-vbb-deploy-runtime` | 573 | 12 |

### Distribution par phase

| Phase | Skills | Avg chars | > 500 chars | Remarque |
|-------|--------|-----------|-------------|----------|
| `0-vbb-*` | 7 | 423 | 1 | Phase 0 (gatekeepers) |
| `1-vbb-*` | 16 | **506** | **10** | **Phase la plus lourde** |
| `2-vbb-*` | 12 | 417 | 3 | Phase 2 (audits) |
| `3-vbb-*` | 1 | 415 | 0 | Risk register |
| `4-vbb-*` | 10 | **360** | 1 | **Phase la plus légère** |
| `t-vbb-*` | 17 | 417 | 5 | Transverse |
| `vibebackbone` | 1 | 382 | 0 | Orchestrateur |

### FR vs EN dans les descriptions

Toutes les descriptions sont en **anglais** (vérifié sur 64 skills). Quelques markers FR résiduels (`détect`, `fichier`) dans 4 skills (`2-vbb-legal`, `2-vbb-spec-validator`, `4-vbb-visual-identity-layer`, `t-vbb-session-handoff`), mais ce sont des artefacts dans le **keywords** list (qui peut mélanger langues), pas une rédaction FR.

---

## Comparaison : ce qui est canon vs ce qui est pratique

### Canon

| Aspect | Statut | Référence |
|--------|--------|-----------|
| Champ `description:` obligatoire dans frontmatter | ✅ | `0-vbb-standard/SKILL.md` (validation) |
| Description doit être **précise pour Pi routing** | ✅ | `0-vbb-standard/SKILL.md` PROCESS étape 6 |
| Description doit contenir des **keywords** | ✅ (implicite) | Toutes les descriptions ont une ligne `Keywords: ...` |
| **Longueur cible** | ❌ | Aucune référence numérique |
| **Linter sur la longueur** | ❌ | `vbb-contract-lint.py` ne valide pas la description |
| **Auto-troncature** | ❌ | Aucun mécanisme trouvé |

### Pratique observée

| Pattern | Valeur |
|---------|--------|
| Médiane | ~430 chars |
| Plus longue | 669 chars |
| Plus courte | 36 chars (`t-vbb-status-dashboard`) |
| Médiane des keywords lists | 7-8 keywords par description |
| Structure typique | 3-4 lignes de prose + 1 ligne `Keywords: ...` |

---

## Manifestation concrète du risque

Si Brice ajoute aujourd'hui un nouveau skill `5-vbb-something-new` avec une description à **1500 chars**, voici ce qui se passe :

1. ✅ La skill est créée avec succès (pas de validation de longueur).
2. ✅ `vbb-contract-lint.py` passe (ne valide pas la description).
3. ✅ Le routing fonctionne (utilise `routing.triggers` du CONTRACT.yaml, pas la description).
4. ⚠️ Si un humain lit `skills/5-vbb-something-new/SKILL.md`, il voit un frontmatter obèse.
5. ⚠️ Si un agent LLM scanne la liste des descriptions (par exemple pour un dashboard ou un picker), il doit digérer 1500 chars pour cette skill.
6. ⚠️ Aucun mécanisme ne le corrige automatiquement.

---

## Recommandations (texte seulement)

| ID reco | Description | Effort | Pré-requis |
|---------|-------------|--------|-----------|
| R-E-1 | Ajouter dans `docs/CONVENTIONS.md` (Pillar 1 Readability) une cible indicative : « `SKILL.md` frontmatter `description:` cible **≤ 500 chars / ≤ 10 lignes** · au-delà, justifier en tête de la description. » | S | Aucun |
| R-E-2 | Étendre `tools/vbb-contract-lint.py` avec un check **non-bloquant** : warning si `description` > 500 chars ou > 10 lignes. (Ne pas fail, juste warn, pour ne pas casser l'historique.) | S | R-E-1 |
| R-E-3 | Documenter explicitement dans `0-vbb-standard/SKILL.md` que « la description n'est **pas** auto-tronquée — c'est un champ à la main, validé pour sa précision, pas sa longueur ». Évite la confusion de modèle mental avec le mécanisme `setup.sh` de `distributions/codex/setup.sh`. | S | Aucun |
| R-E-4 | Compresser manuellement les **10 descriptions > 500 chars de Phase 1** vers la cible 500 chars. Chaque compression doit préserver les `Keywords:` (utiles pour le routing) et la première phrase (utilisée par les humains). | M | R-E-1 |
| R-E-5 | Promouvoir `LLM-LOAD-002` de P2 à P1 (cf. Audit D du 2026-07-12). Les 5 SKILL.md > 400 lignes sont un risque reconnu et non traité. | S | Décision humaine |
| R-E-6 | Ajouter une entrée dans `docs/AUDIT_STATUS.md` pour le risque « descriptions > 500 chars » (analogue à LLM-LOAD-002 mais sur la description, pas le body). | S | R-E-1 |

---

## Quick wins

1. **QW-E-1** — Vérifier les 10 descriptions Phase 1 > 500 chars et identifier celles qui peuvent être raccourcies sans perte de keywords. Coûte 15 minutes, ~30 chars de gain moyen par description.
2. **QW-E-2** — Ajouter dans `0-vbb-standard/SKILL.md` ligne 75-85 (PROCESS) une mention explicite : « The `description:` field is NOT auto-truncated — it is hand-maintained and validated for precision (triggers, keywords), not for length. Codegen mechanisms (`setup.sh` → `distributions/codex/setup.sh`) do NOT touch this field. » Coûte 5 minutes, évite la confusion.
3. **QW-E-3** — Lancer `awk '/^description: \|/{flag=1; next} /^---$/{if(flag){flag=0; exit}} flag{print}' skills/*/SKILL.md | wc -c` pour reproduire la mesure. Coûte 1 minute.

---

## Unknowns / needs confirmation

| ID | Question | Conséquence |
|----|----------|-------------|
| UN-E-1 | Brice confirme-t-il que la « auto-réduction » dont il se souvient concerne bien `~/.codex/AGENTS.md` et **pas** les descriptions in-repo ? | Si non, il y a un autre mécanisme à découvrir |
| UN-E-2 | La cible de 500 chars est-elle acceptable, ou faut-il viser plus court (300-400 chars) ? | Choix R-E-1 |
| UN-E-3 | Le warning `vbb-contract-lint` doit-il être promoted en **error** (fail CI) au-delà d'un seuil (par exemple 1000 chars) ? | Choix R-E-2 |
| UN-E-4 | Y a-t-il une **politique de compaction automatique** pour les nouvelles descriptions (par exemple, pre-commit hook qui refuse > 700 chars) ? | Si oui, R-E-2 est plus strict |

---

## Verdict

`PARTIAL — la « auto-réduction Codex » est un mécanisme de **bloc-remplacement** dans `~/.codex/AGENTS.md`, **pas une troncature des descriptions SKILL.md`. Aucune description n'est tronquée automatiquement. Le repo a 20 descriptions > 500 chars (concentrées sur Phase 1) sans canon de longueur. Quick wins : QW-E-1 (compresser 10 descriptions Phase 1), QW-E-2 (documenter la non-auto-troncature), QW-E-3 (reproduire la mesure). Recommandations plus lourdes : R-E-1 (canon), R-E-2 (linter warning), R-E-4 (compression manuelle). Couplage avec Audit D (SKILL.md body > 400 lignes, LLM-LOAD-002 P2 Open) à traiter en même temps.