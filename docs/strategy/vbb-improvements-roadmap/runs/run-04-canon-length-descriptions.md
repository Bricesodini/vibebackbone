---
context_role: run-spec
phase: 1-pre-execution
status: awaiting-canon-approval
run_id: 2026-07-12_run04-canon-length-descriptions
route: STRUCTURED
updated: 2026-07-12
---

# Run 04 — Canon longueur descriptions SKILL.md (STRUCTURED)

> **Route** : STRUCTURED
> **Effort** : S (~35 min)
> **Risque canon** : semi — modifie `docs/CONVENTIONS.md` (Pillar 1 Readability), ajoute un check `tools/vbb-contract-lint.py`
> **Pre-merge gate** : REQUIS (route STRUCTURED, cf. `docs/REFERENCE/pre-merge-gate.md`)
> **CANON_CHANGE_PROPOSAL** : [`./run-04-CANON_CHANGE_PROPOSAL.md`](run-04-CANON_CHANGE_PROPOSAL.md) (**en attente validation humaine**)
> **Statut** : `READY — bloqué en attente d'approbation canon par Brice`

---

## 1. Goal

Établir une cible canon **indicative** (non-bloquante) pour la longueur du champ `description:` du frontmatter des `SKILL.md`, et instrumenter un **warning non-bloquant** dans `tools/vbb-contract-lint.py` qui signale les dépassements.

**Politique retenue** (cf. HANDOFF §UN-E-2/3/4) :
- Cible canon : **≤ 500 chars / ≤ 10 lignes** (indicative, pas de fail CI)
- Warning console non-bloquant dans `vbb-contract-lint.py`
- Entrée de suivi dans `docs/AUDIT_STATUS.md` (analogue à `LLM-LOAD-002`)
- Pas de pre-commit hook automatique
- **Promotion warning → error à > 800 chars** dans un run futur, après 1 cycle d'observation

**Justification du risque évité** (cf. exchange avec Brice) : la longueur est un **proxy**, pas une garantie de qualité. Une skill peut être précise à 600 chars (mieux qu'une vague à 200 chars). Fail CI brutal forcerait à comprimer au détriment de la **précision**, qui est ce qui sert vraiment le routing.

---

## 2. Findings source

| ID | Finding | Fichier | Sévérité |
|----|---------|---------|----------|
| **AUDIT-E-001** | Aucun canon de longueur pour `description:` des `SKILL.md` | `docs/audits/audit-E-skill-descriptions-20260712-1400.md` | **P1** |
| **AUDIT-E-003** | Phase 1 (`1-vbb-*`) : moyenne 506 chars, 10/16 skills > 500 chars | idem | P2 |
| **AUDIT-E-005** | Aucun linter ne valide la longueur de `description:` | idem | P2 |
| **AUDIT-E-006** (nouveau) | Aucune entrée de suivi dans `AUDIT_STATUS.md` (analogue à LLM-LOAD-002) | idem | P2 — créé par ce run |

**Source audit** : [`docs/audits/audit-E-skill-descriptions-20260712-1400.md`](../../../audits/audit-E-skill-descriptions-20260712-1400.md)

---

## 3. Modifications

### R-E-1 — Cible canon dans `docs/CONVENTIONS.md` (Pillar 1 Readability)

**Modification** : ajout d'une sous-section « `SKILL.md` description length » dans Pillar 1 — Readability, après la sous-section « Comments » (cf. spec, ligne ~25-35 de CONVENTIONS.md).

**Contenu à ajouter** :

```markdown
### SKILL.md description length

The frontmatter `description:` of any `SKILL.md` is the routing surface used
by Pi / Codex / OpenCode to decide which skill to invoke.

**Target (indicative, non-blocking):**

- `description:` content (between the opening `|` and the closing `---`
  of the frontmatter block) should target **≤ 500 chars / ≤ 10 lines**.

**If exceeded:**

- The `tools/vbb-contract-lint.py` emits a **non-blocking** warning
  (no CI gate, no merge block). Rationale: a precise description may
  legitimately exceed the target to cover routing keywords, edge cases,
  or to disambiguate from sibling skills. Length is a proxy, not a
  quality guarantee.

**Hard promotion (future, after ≥ 1 observation cycle):**

- A future run may promote warning → error if `description:` content
  exceeds **800 chars / 15 lines**. This is intentionally left out of
  this run's canon: the policy must be observed before being enforced.

**Reference:** [`docs/audits/audit-E-skill-descriptions-20260712-1400.md`](audits/audit-E-skill-descriptions-20260712-1400.md)
**Tracking:** `AUDIT-E-006` in `docs/AUDIT_STATUS.md`.
```

**Justification** : la cible est explicite, la marge de tolérance est documentée, la promotion future est annoncée (pas cachée). Le mot « indicative » est répété 2 fois pour éviter toute lecture « fail CI ».

### R-E-2 — Warning non-bloquant dans `tools/vbb-contract-lint.py`

**Modification** : ajout d'une fonction `check_description_length(skill_id)` et appel dans `lint_all()`.

**Note technique** : le warning doit lire la `description:` **du frontmatter SKILL.md**, pas de `CONTRACT.yaml`. Donc la fonction doit :
1. Parser le frontmatter SKILL.md (pas le CONTRACT.yaml)
2. Extraire la longueur de `description:` (multi-ligne YAML `|` block)
3. Émettre un warning via stderr (ou print avec préfixe `⚠️`) si > 500 chars OU > 10 lignes
4. **Ne pas** ajouter à `errors` — utiliser une liste séparée `warnings`

**Code à ajouter** (dans `vbb-contract-lint.py`) :

```python
def check_description_length(skill_id: str) -> List[str]:
    """Non-blocking warning if SKILL.md description: exceeds the indicative target."""
    warnings = []
    skill_md = SKILLS_DIR / skill_id / "SKILL.md"
    if not skill_md.exists():
        return warnings

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        warnings.append(f"[{skill_id}] SKILL.md read error: {e}")
        return warnings

    # Extract frontmatter
    if not content.startswith("---\n"):
        return warnings
    end = content.find("\n---\n", 4)
    if end == -1:
        return warnings
    frontmatter = content[4:end]

    # Find description: | block
    desc_match = re.search(r"^description:\s*\|\s*\n(.*?)(?=^[a-z_]+:|\Z)",
                            frontmatter, re.MULTILINE | re.DOTALL)
    if not desc_match:
        return warnings
    desc_text = desc_match.group(1)

    chars = len(desc_text.strip())
    lines = desc_text.strip().count("\n") + 1

    if chars > 500 or lines > 10:
        warnings.append(
            f"[{skill_id}] SKILL.md description: {chars} chars / {lines} lines "
            f"(target: ≤ 500 chars / ≤ 10 lines, cf. CONVENTIONS.md Pillar 1). "
            f"Non-blocking warning — length is a proxy, not a quality guarantee."
        )
    return warnings
```

**Modification de `lint_all()`** :

```python
all_warnings: List[str] = []
# ... (after the existing checks loop)
for skill_id in contract_skills | indexed:
    all_warnings.extend(check_description_length(skill_id))

return len(all_errors), all_errors, all_warnings  # tuple arity change
```

**Modification de `__main__`** :

```python
count, errors, warnings = lint_all()
print(f"VBB Contract Linter — {len(errors)} error(s), {len(warnings)} warning(s) found")
for err in errors:
    print(f"  ✗ {err}")
for warn in warnings:
    print(f"  ⚠️  {warn}")
if count == 0:
    print("  ✓ All contracts valid")
sys.exit(1 if count > 0 else 0)  # warnings do NOT change exit code
```

**Important** : le warning **ne change pas le code de sortie**. `vbb-contract-lint.py` continue de retourner 0 si pas d'erreurs (donc CI ne casse pas). C'est une rupture de signature (tuple arity 2 → 3), donc je vérifie qu'aucun consommateur de `lint_all()` n'existe en dehors de `__main__`.

### AUDIT-E-006 — Entrée de suivi dans `docs/AUDIT_STATUS.md`

**Modification** : ajout d'une entrée analogue à `LLM-LOAD-002` (P2 Open) dans le tableau des risks/load entries de `docs/AUDIT_STATUS.md`.

**Format** (à insérer après l'entrée LLM-LOAD-002) :

```markdown
| AUDIT-E-006 | SKILL.md `description:` length drift (20 skills > 500 chars) | P2 | Open | Run 4 — cible canon ≤ 500 chars + warning non-bloquant dans `vbb-contract-lint.py` + R-E-6 (AUDIT_STATUS tracking). Promotion warning → error > 800 chars dans un run futur après 1 cycle d'observation. |
```

---

## 4. Excluded

- ❌ Modification des skills elles-mêmes (compression des descriptions Phase 1) — Run 5 ultérieur
- ❌ Promotion warning → error > 800 chars — Run futur après observation
- ❌ Pre-commit hook automatique — décision reportée
- ❌ Linter tiers (pre-commit framework) — out of scope
- ❌ Création d'ADR — non requis (changement de conventions, pas d'architecture)
- ❌ Création d'outil nouveau (POC) — la modification est dans un outil existant, pas de création

---

## 5. Process (post-validation canon)

1. **Attente validation** du CANON_CHANGE_PROPOSAL par Brice (porte canon)
2. Modifier `docs/CONVENTIONS.md` (ajout sous-section R-E-1)
3. Modifier `tools/vbb-contract-lint.py` (ajout `check_description_length` + tuple arity)
4. Modifier `docs/AUDIT_STATUS.md` (ajout entrée AUDIT-E-006)
5. Créer artefacts run : `01_INTAKE.md`, `05_PATCH_SUMMARY.md`, `07_CLOSEOUT.md`
6. **Pre-merge gate** (cf. spec §7)
7. Mettre à jour `docs/ACTIVITY_LOG.md`
8. Git commit

---

## 6. Files impact summary

| File | Type | Impact |
|------|------|--------|
| `docs/CONVENTIONS.md` | canon (modif R-E-1) | +15 lignes (sous-section Pillar 1) |
| `tools/vbb-contract-lint.py` | tool (modif R-E-2) | +50 lignes (fonction + appel + tuple arity + main) |
| `docs/AUDIT_STATUS.md` | tracking (modif AUDIT-E-006) | +1 ligne |
| `docs/runs/2026-07-12_run04-canon-length-descriptions/01_INTAKE.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run04-canon-length-descriptions/05_PATCH_SUMMARY.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run04-canon-length-descriptions/07_CLOSEOUT.md` | artefact | nouveau |
| `docs/ACTIVITY_LOG.md` | activity log | +1 ligne |

**Total** : 7 fichiers (3 modifs, 4 nouveaux artefacts)

---

## 7. Verification (pre-merge gate REQUIS, route STRUCTURED)

```bash
# P.R2 #1 — Lint / format
python tools/vbb-contract-lint.py
# Attendu : 0 erreur, ≥ 20 warnings (les 20 descriptions > 500 chars)

# P.R2 #2 — Type / schema (N/A pour modification markdown + ajout fonction Python typée)
python -c "from tools.vbb-contract-lint import lint_all; print('import OK')"
# Attendu : import OK

# P.R2 #3 — Tests (N/A sauf si tests existants pour vbb-contract-lint)
ls tests/ 2>&1 | head
# Vérifier qu'aucun test n'est cassé

# P.R2 #4 — Build (N/A, pas de code build)

# P.R2 #5 — Documentation coherence
git diff docs/CONVENTIONS.md  # +15 lignes, sous-section Pillar 1
grep "AUDIT-E-006" docs/AUDIT_STATUS.md  # 1 hit
test -f docs/runs/2026-07-12_run04-canon-length-descriptions/07_CLOSEOUT.md

# Sanity check : aucun canon non lié touché
git diff docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md
# Attendu : vide

# Sanity check : la signature de lint_all() est bien mise à jour (pas de caller cassé)
grep -rn "lint_all()" tools/ 2>&1 | grep -v __pycache__
# Attendu : seul vbb-contract-lint.py:__main__
```

---

## 8. Acceptance criteria

Run 4 est **COMPLET** si :

- ✅ CANON_CHANGE_PROPOSAL validé par Brice (porte d'entrée canon)
- ✅ `docs/CONVENTIONS.md` : sous-section « SKILL.md description length » ajoutée dans Pillar 1
- ✅ `tools/vbb-contract-lint.py` : `check_description_length()` ajoutée, ≥ 20 warnings émis (les 20 descriptions > 500 chars), 0 erreur, exit code 0
- ✅ `docs/AUDIT_STATUS.md` : entrée `AUDIT-E-006` ajoutée
- ✅ `docs/CONVENTIONS.md` / `PILOTAGE.md` / `AGENTIC_RUN_PROTOCOL.md` / `MVP_START_PROTOCOL.md` / `PHASE_TO_SKILLS.md` non modifiés ailleurs
- ✅ Pre-merge gate (5 vérifications P.R2) passé
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

---

## 9. Liens

- [`./run-04-CANON_CHANGE_PROPOSAL.md`](run-04-CANON_CHANGE_PROPOSAL.md) — proposition canon (gate obligatoire)
- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/audits/audit-E-skill-descriptions-20260712-1400.md`](../../../audits/audit-E-skill-descriptions-20260712-1400.md) — source AUDIT-E-001/003/005
- [`../../../docs/CONVENTIONS.md`](../../../CONVENTIONS.md) — Pillar 1 Readability (cible d'insertion)
- [`../../../tools/vbb-contract-lint.py`](../../../tools/vbb-contract-lint.py) — outil cible R-E-2
- [`../../../docs/templates/CANON_CHANGE_PROPOSAL.md.template`](../../../templates/CANON_CHANGE_PROPOSAL.md.template) — template canon