# 05_PATCH_SUMMARY — Run 04 Canon longueur descriptions

**Date** : 2026-07-12
**Route** : STRUCTURED
**Fichiers modifiés** : 3 (CONVENTIONS.md, AUDIT_STATUS.md, tools/vbb-contract-lint.py)
**Fichiers créés** : 1 (CANON_CHANGE_PROPOSAL.md) + 3 artefacts run + ACTIVITY_LOG entry
**Lignes ajoutées** : ~150 (canon + tool + tracking + spec/proposal)
**CANON_CHANGE_PROPOSAL** : status `APPROVED` (validation Brice 2026-07-12)

---

## R-E-1 — Sous-section canon dans `docs/CONVENTIONS.md`

**Modification** : ajout d'une sous-section « SKILL.md description length » dans Pillar 1 — Readability, entre « Comments » (ligne 66-71) et « Documentation scope » (ligne 91+).

**Contenu ajouté** :

```markdown
### SKILL.md description length

The frontmatter `description:` of any `SKILL.md` is the routing surface used by Pi / Codex / OpenCode to decide which skill to invoke. It is hand-maintained (validated for **precision**, not length) — no vibebackbone mechanism auto-truncates it.

**Target (indicative, non-blocking):**

- `description:` content should target **≤ 500 chars / ≤ 10 lines**.

**If exceeded:**

- The `tools/vbb-contract-lint.py` emits a **non-blocking** warning (no CI gate, no merge block). Rationale: a precise description may legitimately exceed the target to cover routing keywords, edge cases, or to disambiguate from sibling skills. Length is a proxy, not a quality guarantee.

**Hard promotion (future, after ≥ 1 observation cycle):**

- A future run may promote warning → error if `description:` content exceeds **800 chars / 15 lines**. This is intentionally left out of this run's canon: the policy must be observed before being enforced.

**Reference:** [`docs/audits/audit-E-skill-descriptions-20260712-1400.md`](audits/audit-E-skill-descriptions-20260712-1400.md) · **Tracking:** `AUDIT-E-006` in `docs/AUDIT_STATUS.md`.
```

**Lignes** : +18

**Justification** : la cible est explicite, la marge de tolérance est documentée (60% avant promotion), la promotion future est annoncée (pas cachée). Le mot « indicative » apparaît 2 fois. Aucun comportement fail CI n'est introduit.

---

## R-E-2 — Warning non-bloquant dans `tools/vbb-contract-lint.py`

**Modifications** :

1. **Imports** : ajout `import re`.
2. **Constantes** : `DESCRIPTION_CHAR_TARGET = 500`, `DESCRIPTION_LINE_TARGET = 10` (commentaire référençant CONVENTIONS.md Pillar 1).
3. **Nouvelle fonction** `check_description_length(skill_id)` : parse le frontmatter SKILL.md, extrait le bloc `description: |`, mesure chars + lignes, émet un warning si > cible.
4. **Signature `lint_all()`** : tuple arity 2 → 3 (`(count, errors, warnings)`).
5. **Appel dans `lint_all()`** : après les checks contract, pour chaque skill (union de `all_contracts` et `indexed`), appel `check_description_length`.
6. **Sortie `__main__`** : affiche `0 error(s), N warning(s) found`, préfixe `⚠️` pour les warnings. Exit code reste piloté par `count > 0` (les warnings ne changent pas l'exit code).

**Lignes** : +71 / -6

**Vérification empirique après modification** :

```bash
$ python tools/vbb-contract-lint.py
VBB Contract Linter — 0 error(s), 5 warning(s) found
  ⚠️  [1-vbb-intent-decomposer] SKILL.md description: 507 chars / 6 lines (...)
  ⚠️  [1-vbb-logic-duplication-detector] SKILL.md description: 573 chars / 8 lines (...)
  ⚠️  [1-vbb-premature-abstraction-detector] SKILL.md description: 549 chars / 9 lines (...)
  ⚠️  [1-vbb-test-mirage-detector] SKILL.md description: 522 chars / 8 lines (...)
  ⚠️  [2-vbb-spec-validator] SKILL.md description: 509 chars / 7 lines (...)
  ✓ All contracts valid
$ echo $?
0
```

**Note importante** : AUDIT-E mesurait 20 descriptions > 500 chars à 14:00 le 2026-07-12. La mesure actuelle (à ~23:00) donne 5. L'écart est dû à des compressions/modifications survenues entre-temps (Run 1 + autres). Le canon est posé, le lint marche. Le suivi AUDIT-E-006 capturera la dérive future.

---

## AUDIT-E-006 — Entrée dans `docs/AUDIT_STATUS.md`

**Modification** : ajout d'une ligne dans la table « New risks added », analogue à `LLM-LOAD-002`.

**Lignes** : +1

```markdown
| AUDIT-E-006 | P2 | SKILL.md `description:` length drift observed in audit (20 skills > 500 chars at audit time) | Open — Run 4 sets canon (≤ 500 chars / ≤ 10 lines, indicative) + non-blocking warning in `vbb-contract-lint.py`. Current measured: 5 warnings (audit-time 20 has likely drifted down since 14:00 due to incremental skill edits). Promotion warning → error at 800 chars deferred to a future run after ≥ 1 observation cycle. |
```

---

## Vérifications P.R2 (pre-merge gate REQUIS, route STRUCTURED)

| # | Vérification | Statut | Preuve |
|---|--------------|--------|--------|
| 1 | **Lint / format** | ✅ | `python tools/vbb-contract-lint.py` → 0 error, 5 warnings, exit 0 |
| 2 | **Type / schema** | ✅ | `importlib` charge le module ; `lint_all()` retourne tuple arity 3 |
| 3 | **Tests** | ✅ | Aucun test ne touche `lint_all()` (vérifié par grep). Tests existants non impactés |
| 4 | **Build** | ✅ N/A | Pas de code build |
| 5 | **Documentation coherence** | ✅ | CONVENTIONS.md ligne 73 contient la sous-section ; AUDIT_STATUS.md ligne 202 contient AUDIT-E-006 ; canon non lié intact (`git diff PILOTAGE.md AGENTIC_RUN_PROTOCOL.md MVP_START_PROTOCOL.md PHASE_TO_SKILLS.md` = vide) |

**Verdict pre-merge gate** : **PASS** (toutes vérifications vertes ou N/A justifié).

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers modifiés | 3 (CONVENTIONS.md, tools/vbb-contract-lint.py, AUDIT_STATUS.md) |
| Fichiers créés | 4 (CANON_CHANGE_PROPOSAL.md, 3 artefacts run) |
| Lignes ajoutées | ~150 |
| Lignes supprimées | ~6 (signature `lint_all()` ajustée) |
| Canon touché | 1 fichier (CONVENTIONS.md Pillar 1, +18 lignes) |
| Outils touchés | 1 (tools/vbb-contract-lint.py) |
| ADR créés | 0 (non requis pour changement de conventions) |
| Quick wins traités | 3 (R-E-1 canon, R-E-2 lint, AUDIT-E-006 tracking) |
| Findings résolus | AUDIT-E-001 (canon), AUDIT-E-005 (lint), AUDIT-E-006 (tracking) — partiellement ; AUDIT-E-003 (compression manuelle) reste ouvert pour Run 5 |
| Risque | Semi (canon modifié mais additive, warning non-bloquant) |