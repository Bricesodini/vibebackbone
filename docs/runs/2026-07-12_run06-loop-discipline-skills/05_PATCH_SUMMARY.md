# 05_PATCH_SUMMARY — Run 06 Loop discipline skills

**Date** : 2026-07-12
**Route** : FAST-STANDARD
**Fichiers modifiés** : 5 SKILL.md (ajout section `## After this skill runs`)
**Lignes ajoutées** : +70 (14 lignes par skill en moyenne)

---

## Modification uniforme sur les 5 skills `1-vbb-*`

Pour chaque skill, ajout d'une section `## After this skill runs` juste avant `## VERDICT RULES`, qui contient 3 éléments :

1. **Auto-positionnement** : « This is a `02_AUDIT` skill. Read-only — does not modify code. »
2. **Loop position** : description du Consumes / Produces / Hands off to
3. **Référence canonique** : lien vers `docs/REFERENCE/pre-merge-gate.md` (sans dupliquer le contenu — rule "no parallel truth")

**Diff uniforme (14 lignes ajoutées par skill)** :

```diff
 ## Unknowns / ...
+
+## After this skill runs
+
+This is a `02_AUDIT` skill. Read-only — does not modify code.
+
+**Loop position:**
+- Consumes: skill input + repo state [...]
+- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md`
+- Hands off to:
+  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../../prompts/canonical/03-p-vbb-decision.md))
+  - Then `04_PLAN` if findings include P0/P1 [...]
+  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../../REFERENCE/pre-merge-gate.md))
+
+**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../../REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).

 ## VERDICT RULES
```

### Variantes par skill

| Skill | Différence vs template |
|-------|------------------------|
| `1-vbb-code-janitor` | Template standard |
| `1-vbb-tech-debt` | Consumes mentionne « incl. janitor findings if `1-vbb-code-janitor` was run first » |
| `1-vbb-monolith-detector` | Hands off mentionne « (likely, since monolith patterns usually require refactor) » |
| `1-vbb-conventions` | Template standard |
| `1-vbb-formatter` | Hands off : « `04_PLAN` (always, since this skill's output is itself a plan) » |

---

## Vérifications

- [x] **5 SKILL.md ont une section `## After this skill runs`** ✓
- [x] **5 SKILL.md référencent `pre-merge-gate.md` canoniquement** (2 hits par skill : dans la section et dans la dernière ligne Reference) ✓
- [x] **`vbb-contract-lint.py` reste à 0 erreur / 0 warning** ✓ (modifications purement markdown, frontmatter inchangé)
- [x] **Aucun canon non lié touché** : `git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/REFERENCE/pre-merge-gate.md tools/vbb-contract-lint.py` = vide ✓

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers modifiés | 5 SKILL.md |
| Lignes ajoutées | +70 |
| Lignes supprimées | 0 |
| Canon touché | 0 |
| Outils créés | 0 |
| ADR créés | 0 |
| Findings résolus | AUDIT-B-003 (P2) — 5 skills `1-vbb-*` loop-disciplinés |
| Risque | Faible (modifications purement markdown) |