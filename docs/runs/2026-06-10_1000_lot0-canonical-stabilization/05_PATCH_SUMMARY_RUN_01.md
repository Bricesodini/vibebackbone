# 05_PATCH_SUMMARY_RUN_01 — Lot 0 : Patches appliqués

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

---

## Patches appliqués

| Patch | Fichier | Changement |
|-------|---------|------------|
| PATCH-01 | `README.md` | Banner : 57→58 skills, 31→32 prompts, 7+24+1. Table t-* : ajout Status-report. Arbre : 57→58, 31→32, 12→13 transverses. Titres sections mis à jour. |
| PATCH-02 | `AGENTS.md` | Ligne tag : 57→58 skills, 24→32 prompts (7 canoniques + 24 spécialisés + 1 router) |
| PATCH-03 | `SYSTEM.md` | Ligne tag : 57→58 skills, 24→32 prompts (7 canoniques + 24 spécialisés + 1 router) |
| PATCH-04 | `GUIDE.md` | 57→58 skills, 31→32 prompts, 24→24+1 router, multiples lignes corrigées |
| PATCH-05 | `docs/CONTEXT.md` | Verdict : 🟢 PRODUCTION-READY → 🟡 PARTIAL. Skills 58·22 contrats (38 %). Prompts 32. |
| PATCH-06 | `docs/INDEX.md` | Prompts spécialisés (25) → (24) + 1 router |
| PATCH-07 | `docs/AUDIT_STATUS.md` | 8/58 (14 %) → 22/58 (38 %). 50 non contractés → 36. Mise à jour R-002. |
| PATCH-08 | — | Skills méta documentés dans 04_PLAN.md (pas de modification de SKILL.md) |
| PATCH-09 | `README.md` | Table t-* : ajout `Status-report` |
| PATCH-10 | `docs/SESSION.md` | Ajout entrée Run Lot 0 |

---

## Détail par patch

### PATCH-01 + PATCH-09 : README.md

- Ligne 4 (banner) : `57 skills · 31 prompts` → `58 skills · 32 prompts (7 canoniques + 24 spécialisés + 1 router)`
- Ligne 35 (arbre skills) : `57 skills prêts à injecter` → `58 skills prêts à injecter`
- Ligne 41 (arbre t-*) : `(12)` → `(13)`
- Ligne 43 (arbre prompts) : `31 prompts (7 canoniques + 24 spécialisés + 1 router)` → `32 prompts (7 canoniques + 24 spécialisés + 1 router)`
- Ligne 62 : `Les 57 skills` → `Les 58 skills`
- Ligne 71 (table t-*) : ajout `Status-report` à la liste
- Ligne 79 : `Les 31 prompts` → `Les 32 prompts`
- Ligne 88 : `← 24 prompts spécialisés` → `← 24 prompts spécialisés + 1 router`
- Ligne 190 : `Installer les 57 skills` → `Installer les 58 skills`
- Ligne 192 : `Les 57 skills sont disponibles` → `Les 58 skills sont disponibles`

### PATCH-02 : AGENTS.md

- Ligne 350 : `57 skills · 24 prompts · 4 voies` → `58 skills · 32 prompts (7 canoniques + 24 spécialisés + 1 router) · 4 voies`

### PATCH-03 : SYSTEM.md

- Ligne 5 : `57 skills · 24 prompts · 4 voies` → `58 skills · 32 prompts (7 canoniques + 24 spécialisés + 1 router) · 4 voies`

### PATCH-04 : GUIDE.md

- Ligne 82 : `31 PROMPTS` → `32 PROMPTS`
- Ligne 88 : `57 SKILLS` → `58 SKILLS`
- Ligne 168 : `24 prompts spécialisés` → `24 prompts spécialisés + 1 router`
- Ligne 184 : `Les 57 skills` → `Les 58 skills`
- Ligne 220 : `Les 57 skills` → `Les 58 skills`
- Ligne 221 : `Les 24 prompts` → `Les 24 prompts spécialisés + 1 router`
- Ligne 786 : `31 c'est beaucoup` → `32 c'est beaucoup`
- Ligne 793 : `Les 31` → `Les 32`
- Ligne 926 : `catalogue des 57 skills` → `catalogue des 58 skills`

### PATCH-05 : docs/CONTEXT.md

- Ligne 48 : `🟢 PRODUCTION-READY + OPENCODE-READY` → `🟡 PARTIAL — not yet mechanically audited`
- Ligne 57 : `58 skills · 22 CONTRACT.yaml indexés` → `58 skills · 22 contrats mécaniques (38 %)`
- Ligne 58 : `24 prompts de session` → `32 prompts (7 canoniques + 24 spécialisés + 1 router)`

### PATCH-06 : docs/INDEX.md

- Ligne 47 : `Prompts spécialisés (25)` → `Prompts spécialisés (24) + 1 router`

### PATCH-07 : docs/AUDIT_STATUS.md

- Ligne 20 : `8 skills sur 58 (14 %)` → `22 skills sur 58 (38 %)`
- Ligne 34 (R-002) : `8/58 skills (14 %)` → `22/58 skills (38 %)`
- Ligne 56 : `50 skills sur 58 sont NOT_CONTRACTED` → `36 skills sur 58 sont NOT_CONTRACTED`

### PATCH-10 : docs/SESSION.md

- Ajout entrée « Run 2026-06-10 — Lot 0 : Stabilisation canonique » avec statut COMPLET