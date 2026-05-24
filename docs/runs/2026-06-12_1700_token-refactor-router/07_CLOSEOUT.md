# 07_CLOSEOUT — RUN 14B : Token Economy Refactor — Router Matrix Extraction

**Date** : 2026-06-12  
**Voie** : STRUCTURÉE  
**Verdict** : ✅ PASS

---

## Résumé

Router condensé de 3 766 → 488 tokens (**87% réduction**). Matrice détaillée extraite vers `docs/router/ROUTER_MATRIX.md` (L3 référence, pas chargé au boot). Logique de triage intégralement préservée. Index mis à jour pour couvrir `docs/router/`.

### Fichiers modifiés

| Fichier | Tokens avant | Tokens après | Gain | Réduction |
|---------|-------------|-------------|------|-----------|
| **prompts/t-p-vbb-phase-router.md** | 3 766 | 488 | **−3 278** | **87%** |
| docs/router/ROUTER_MATRIX.md (nouveau) | 0 | 3 744 | L3 ref | non chargé au boot |
| tools/vbb-index.py | — | — | — | +1 glob (`docs/router/**/*.md`), +1 kind |

### Gain token estimé

| Couche | Avant | Après | Gain |
|--------|-------|-------|------|
| L1 Router (chargé au triage) | 3 766 | 488 | **−3 278** |
| L3 Référence (à la demande) | 0 | 3 744 | +3 744 (non boot) |

**Net boot saving** : **−3 278 tokens/session**

### Règles critiques préservées

| Règle | Router | Matrix |
|-------|--------|--------|
| RAPIDE-ZERO exclusions | ✅ §1 | ✅ Phase 01 table |
| RAPIDE-MINIMAL | ✅ §2 | ✅ Phase 01 table |
| STRUCTURÉE multi-fichiers | ✅ §4 | ✅ Phase 01 + 04 tables |
| AUDIT obligatoire (secu/DB/CI) | ✅ §5 | ✅ Phase 02 table (12 domaines) |
| CLÔTURE handoff | ✅ §6 | ✅ Phase 07 table |
| Escalades obligatoires | ✅ §Escalades | ✅ §Cas particuliers |
| Fallback index/dashboard | ✅ §Fallbacks | ✅ (via index search) |
| Canonique vs spécialisé | ✅ §Règle | ✅ §"Règle de base" + détails |
| Séquences par voie | pointeur → matrix | ✅ 4 diagrammes complets |
| Convention artefacts | pointeur → matrix | ✅ §Convention |
| Transitions session | pointeur → matrix | ✅ §Règles de session |
| Cas particuliers | pointeur → matrix | ✅ §Cas particuliers |

### Ce qui a changé

- **prompts/t-p-vbb-phase-router.md** : 12 sections détaillées → 4 sections compactes (décision voie, escalades, fallbacks, règle canonique/spécialisé). Version bump 1.0 → 2.0.
- **docs/router/ROUTER_MATRIX.md** : nouveau fichier L3 contenant la matrice complète (7 phases, alternatives, séquences, conventions, cas particuliers).
- **tools/vbb-index.py** : `INDEX_GLOBS` ajouté `"docs/router/**/*.md"`, `KIND_MAP` ajouté `"docs/router" → "router"`. Index reconstruit (258 entries).

### Ce qui n'a PAS changé

- AGENTS.md, GUIDE.md, CONTEXT.md — aucun touché
- skills/, contracts — aucun touché
- CI workflows — aucun touché
- Autres prompts — aucun touché
- Aucune logique métier de routing supprimée

### Cumul token economy (14A + 14B)

| Source | Avant | Après | Gain total |
|--------|-------|-------|-----------|
| AGENTS.md (L0) | 5 186 | 726 | −4 460 |
| GUIDE.md (L0→L3) | 9 271 | 0 (L3) | −9 271 |
| Router (L1) | 3 766 | 488 | −3 278 |
| **Total boot** | | | **−17 009** |

### Prochaine action recommandée
**RUN 14C — Redondances docs → liens canoniques**