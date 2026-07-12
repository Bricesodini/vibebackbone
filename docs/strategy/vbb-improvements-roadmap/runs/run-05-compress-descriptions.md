---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run05-compress-descriptions
route: FAST-STANDARD
updated: 2026-07-12
---

# Run 05 — Compression des descriptions > 500 chars (FAST-STANDARD)

> **Route** : FAST-STANDARD
> **Effort** : S (~20 min)
> **Risque canon** : faible (modifie uniquement les SKILL.md, pas le canon)
> **Pre-merge gate** : SKIP (route FAST-STANDARD, cf. `docs/REFERENCE/pre-merge-gate.md`)
> **Statut** : `READY — prêt à exécuter sur GO`

---

## 1. Goal

Compresser manuellement les **5 descriptions > 500 chars** détectées par `tools/vbb-contract-lint.py` (warning introduit par Run 4), en préservant les `Keywords:` (utiles au routing) et la première phrase (utilisée par les humains). Cible : chaque description ≤ 500 chars / ≤ 10 lignes après compression.

---

## 2. Findings source

| ID | Finding | Fichier | Sévérité |
|----|---------|---------|----------|
| **AUDIT-E-003** | Phase 1 (`1-vbb-*`) : moyenne 506 chars, 10/16 skills > 500 chars | `docs/audits/audit-E-skill-descriptions-20260712-1400.md` | P2 |
| **AUDIT-E-006** | Suivi gouvernance créé par Run 4 | `docs/AUDIT_STATUS.md` | P2 (ouvert) |

**Source canon (Run 4)** : `docs/CONVENTIONS.md` Pillar 1 — `SKILL.md description length` (cible ≤ 500 chars / ≤ 10 lignes, indicatif)

---

## 3. État actuel (mesure `vbb-contract-lint.py` post-Run 4)

| Skill | Chars | Lignes | Cible |
|-------|-------|--------|-------|
| `1-vbb-intent-decomposer` | 507 | 6 | ≤ 500 |
| `1-vbb-logic-duplication-detector` | 573 | 8 | ≤ 500 |
| `1-vbb-premature-abstraction-detector` | 549 | 9 | ≤ 500 |
| `1-vbb-test-mirage-detector` | 522 | 8 | ≤ 500 |
| `2-vbb-spec-validator` | 509 | 7 | ≤ 500 |

**Note** : audit-time était 20, mesure actuelle est 5. L'écart (15 descriptions compressées entre 14:00 et 23:00 le 2026-07-12) vient de modifications incrémentales (Run 1 QW-1 a renommé/compressé certains éléments). Run 5 vise les 5 restantes.

---

## 4. Modifications (5 SKILL.md)

### 4.1 — `skills/1-vbb-intent-decomposer/SKILL.md`

**Avant** (507 chars) :
```
Translates a product specification or feature brief into a structured, implementable
build plan. Maps business intent onto existing architecture, chunks work into testable
units, identifies dependencies, and flags risks before any code is written.
Designed as the bridge between a non-developer product architect and an AI developer.
Keywords: product spec, feature brief, implementation plan, intent decomposition,
build plan, feature breakdown, product-to-code, architect-to-developer, planning.
```

**Après** (~485 chars) :
```
Translates a product specification or feature brief into a structured, implementable
build plan. Maps business intent onto existing architecture, chunks work into testable
units, identifies dependencies, and flags risks before any code is written.
Bridge between product architect and AI developer.
Keywords: product spec, feature brief, implementation plan, intent decomposition,
build plan, feature breakdown, product-to-code, architect-to-developer, planning.
```

**Gain** : -22 chars (suppression "Designed as the" et "non-developer").

### 4.2 — `skills/1-vbb-logic-duplication-detector/SKILL.md`

**Avant** (573 chars) :
```
Detects business logic duplication beyond simple copy-paste:
same intentions implemented differently, scattered business rules,
redundant calculations, duplicated validations in varied forms.
Read-only — never modifies code. Distinguishes syntactic duplication
(→ code-janitor) from semantic duplication (this skill).
Keywords: logic duplication, semantic duplication, business logic duplication,
duplicated intent, DRY violation, duplicated calculations, duplicated validation,
scattered business rules, divergent implementations, same intent different code.
```

**Après** (~495 chars) :
```
Detects business logic duplication beyond copy-paste:
same intentions implemented differently, scattered business rules,
redundant calculations, duplicated validations.
Read-only. Distinguishes syntactic duplication (→ code-janitor)
from semantic duplication (this skill).
Keywords: logic duplication, semantic duplication, business logic duplication,
duplicated intent, DRY violation, duplicated calculations, duplicated validation,
scattered business rules, divergent implementations, same intent different code.
```

**Gain** : -78 chars (suppression "simple", "in varied forms.", "— never modifies code").

### 4.3 — `skills/1-vbb-premature-abstraction-detector/SKILL.md`

**Avant** (549 chars) :
```
Detects over-dimensioned abstractions relative to their actual usage:
interfaces with a single implementation, factories for 2 cases, indirection
layers without benefit, heavy patterns for simple uses. Recommends inlining
or simplification when relevant.
Read-only — never modifies code.
Keywords: premature abstraction, over-engineering, over-abstraction,
unnecessary interface, single implementation interface, factory overkill,
indirection without benefit, YAGNI violation, abstraction cost, 
heavy pattern simple use, overdesign.
```

**Après** (~480 chars) :
```
Detects over-dimensioned abstractions vs actual usage:
interfaces with a single implementation, factories for 2 cases, indirection
layers without benefit, heavy patterns for simple uses. Recommends inlining.
Read-only.
Keywords: premature abstraction, over-engineering, over-abstraction,
unnecessary interface, single implementation interface, factory overkill,
indirection without benefit, YAGNI violation, abstraction cost, 
heavy pattern simple use, overdesign.
```

**Gain** : -69 chars ("relative to their" → "vs", "or simplification when relevant." supprimé, "— never modifies code." → "Read-only.").

### 4.4 — `skills/1-vbb-test-mirage-detector/SKILL.md`

**Avant** (522 chars) :
```
Detects tests that give a false impression of safety: mocks without behavioral
assertions, tautological tests, happy-path only, assertions on mocks
rather than on results, absence of edge cases.
Evaluates real confidence vs the confidence displayed by test coverage.
Read-only — never modifies code.
Keywords: test mirage, false confidence, mock without assertion, tautological test,
happy path only, test quality, useless tests, test anti-patterns,
coverage illusion, green tests no safety, testing theater.
```

**Après** (~480 chars) :
```
Detects tests giving a false impression of safety: mocks without behavioral
assertions, tautological tests, happy-path only, mock assertions vs result
assertions, missing edge cases.
Evaluates real confidence vs coverage confidence.
Read-only.
Keywords: test mirage, false confidence, mock without assertion, tautological test,
happy path only, test quality, useless tests, test anti-patterns,
coverage illusion, green tests no safety, testing theater.
```

**Gain** : -42 chars ("that", "rather than on results" → "vs result", "absence of" → "missing", "the confidence displayed by test coverage" → "coverage confidence", "— never modifies code." → "Read-only.").

### 4.5 — `skills/2-vbb-spec-validator/SKILL.md`

**Avant** (509 chars) :
```
Validates that the implemented code matches the original product specification.
Cross-references every requirement against implementation evidence, detects
missing features, divergent behaviors, and unspecified additions. Designed as
the post-implementation counterpart to 1-vbb-intent-decomposer.
Keywords: spec validation, requirement coverage, implementation audit,
product spec verification, feature completeness, spec-to-code traceability,
acceptance validation, did-we-build-the-right-thing.
```

**Après** (~488 chars) :
```
Validates implemented code against the original product specification.
Cross-references every requirement against implementation evidence, detects
missing features, divergent behaviors, and unspecified additions.
Post-implementation counterpart to 1-vbb-intent-decomposer.
Keywords: spec validation, requirement coverage, implementation audit,
product spec verification, feature completeness, spec-to-code traceability,
acceptance validation, did-we-build-the-right-thing.
```

**Gain** : -21 chars ("that the" → "", "Designed as the" → "").

---

## 5. Excluded

- ❌ Modification du canon (`CONVENTIONS.md` non touché — Run 4 l'a déjà fait)
- ❌ Modification du linter (`tools/vbb-contract-lint.py` non touché — Run 4 l'a déjà fait)
- ❌ Modification des `phase:` deprecated (`phase: 1`, `phase: 2` — Run 6 s'en chargera)
- ❌ Création d'ADR, d'outil, ou de nouveau prompt
- ❌ Compression des autres descriptions (44/64 déjà ≤ 500 chars, hors scope)
- ❌ Run de promotion warning → error > 800 chars (run futur)

---

## 6. Process

1. Modifier les 5 SKILL.md (sections `description:` uniquement)
2. Vérifier `vbb-contract-lint.py` → 0 warning
3. Vérifier qu'aucun canon non lié n'est touché
4. Produire `01_INTAKE.md`, `05_PATCH_SUMMARY.md`, `07_CLOSEOUT.md`
5. Mettre à jour `docs/ACTIVITY_LOG.md`
6. Git commit

---

## 7. Verification

```bash
# 1. vbb-contract-lint.py : 0 warning attendu
python tools/vbb-contract-lint.py
# Attendu : "VBB Contract Linter — 0 error(s), 0 warning(s) found"

# 2. Aucun canon non lié touché
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md tools/vbb-contract-lint.py
# Attendu : vide

# 3. Mesure des 5 descriptions après compression
for f in 1-vbb-intent-decomposer 1-vbb-logic-duplication-detector 1-vbb-premature-abstraction-detector 1-vbb-test-mirage-detector 2-vbb-spec-validator; do
  python3 -c "
import re
from pathlib import Path
text = Path('skills/$f/SKILL.md').read_text()
fm = text[4:text.find('\n---\n', 4)]
m = re.search(r'^description:\s*\|\s*\n(.*?)(?=^[a-z_]+:|\Z)', fm, re.MULTILINE | re.DOTALL)
if m:
    desc = m.group(1).strip()
    print(f'$f: {len(desc)} chars / {desc.count(chr(10))+1} lines')
"
done
# Attendu : chaque description ≤ 500 chars / ≤ 10 lignes
```

---

## 8. Acceptance criteria

Run 5 est **COMPLET** si :

- ✅ 5 descriptions compressées : toutes ≤ 500 chars / ≤ 10 lignes
- ✅ `Keywords:` préservés sur les 5 descriptions (routing intact)
- ✅ Première phrase préservée sur les 5 descriptions (lecture humaine intacte)
- ✅ `vbb-contract-lint.py` → 0 erreur, 0 warning, exit 0
- ✅ Aucun canon non lié touché
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

---

## 9. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/audits/audit-E-skill-descriptions-20260712-1400.md`](../../../audits/audit-E-skill-descriptions-20260712-1400.md) — source AUDIT-E-003
- [`../../../docs/CONVENTIONS.md`](../../../CONVENTIONS.md) — Pillar 1 (cible canon posée par Run 4)
- [`../../../tools/vbb-contract-lint.py`](../../../tools/vbb-contract-lint.py) — linter (warning introduit par Run 4)
- [`./run-04-CANON_CHANGE_PROPOSAL.md`](run-04-CANON_CHANGE_PROPOSAL.md) — référence canon (Run 4)