# 01_INTAKE — RUN 14B : Token Economy Refactor — Router Matrix Extraction

**Date** : 2026-06-12  
**Voie** : STRUCTURÉE  
**Objectif** : Réduire le poids du router context sans perdre la capacité de triage voie/phase/skill

---

## État actuel

- `prompts/t-p-vbb-phase-router.md` = 15 065 octets / ~3 766 tokens
- Contient : matrice détaillée (7 phases × N contextes), séquences par voie, règles de session, convention artefacts, cas particuliers, index rapide (24 entrées)
- C'est le 3e plus gros fichier contribuant au boot context

## Critique vs. Référence

| Section | Tokens estimés | Critique (boot) | Référence (à la demande) |
|---------|---------------|-----------------|--------------------------|
| Règle de base (canonique vs spécialisé) | ~60 | ✅ | |
| Décision voie (RAPIDE/STRUCTURÉE/AUDIT/CLÔTURE) | ~80 | ✅ | |
| Escalades obligatoires | ~100 | ✅ | |
| Fallback index/dashboard | ~50 | ✅ | |
| Séquences par voie (4 diagrammes) | ~350 | | ✅ |
| Matrice détaillée phases 01-07 | ~1 400 | | ✅ |
| Règles de décision (quand canonique/spécialisé) | ~120 | | ✅ |
| Règles de session (table transitions) | ~150 | | ✅ |
| Convention artefacts | ~120 | | ✅ |
| Cas particuliers | ~250 | | ✅ |
| Index rapide (24 besoins) | ~350 | | ✅ |
| Structure répertoire prompts | ~200 | | ✅ |

## Plan

1. Extraire matrice détaillée + séquences + règles décision + convention artefacts + cas particuliers + index rapide → `docs/ROUTER_MATRIX.md`
2. Réduire `prompts/t-p-vbb-phase-router.md` à : décision voie, escalades, fallback, pointeur matrice
3. Vérifier que l'index peut retrouver la matrice
4. CI locale
5. Documenter gain token