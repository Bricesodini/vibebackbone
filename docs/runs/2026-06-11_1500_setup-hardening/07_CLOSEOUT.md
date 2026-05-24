# 07_CLOSEOUT — RUN 08 : setup.sh hardening

**Date** : 2026-06-11  
**Voie** : STRUCTURÉE  
**Verdict** : ✅ PASS

---

## Résumé

Corrections ciblées de sécurité et robustesse dans setup.sh. Aucune réécriture complète. Comportement utilisateur inchangé. Symlinks maintenant relatifs (portabilité accrue). CI locale PASS.

### Corrections appliquées

| SYNERGY | Correction | Lignes |
|---------|-----------|--------|
| SYNERGY-007 (partiel) | Symlinks absolus → relatifs via `relpath()` | Skills + Prompts |
| SYNERGY-012 (reste) | `rm -f + ln -s` → `ln -sfn` (Pi prompts + symlink_if_absent) | 6 occurrences |
| BUG | `readlink` check prompts : `"PROMPTS_SRC"` littéral → `$PROMPTS_SRC` + match relatif | 1 |
| TOCTOU | `symlink_if_absent()` : `rm -f + ln -s` → `ln -sfn` ; ajout match relatif | 1 fonction |
| Portabilité | `_is_vbb_symlink()` : détection de liens VBB indépendante du format | Uninstall 3 checks |

### Nouvelles fonctions

| Fonction | Rôle |
|----------|------|
| `relpath(base, target)` | Calcule un chemin relatif (via python3, fallback absolu) |
| `_is_vbb_symlink(link, expected)` | Vérifie si un symlink pointe vers VBB (absolu ou relatif) |

### Fichiers modifiés
- `setup.sh` — 7 zones modifiées (~30 lignes changées sur 653)

### Comportement utilisateur
- ✅ Inchangé : mêmes fichiers installés, mêmes messages, même `--uninstall`
- ✅ Symlinks relatifs : le repo peut être déplacé sans casser les liens
- ✅ `ln -sfn` : pas de TOCTOU race condition sur les créations de liens

### Tests / CI
- 45/45 tests PASS
- CI locale : 5/6 PASS (1 WARN sur closure du run en cours)

### Risques résiduels
- SYNERGY-004 : setup.sh reste un monolithe (652 lignes) — le refactor complet est reporté
- SYNERGY-005 : duplication install/uninstall non traitée (faible bénéfice/risque)
- SYNERGY-008 : 36/58 skills sans contrat
- 7 P2 restants, 10 P3, 3 ACCEPTED_RISK

### Prochaine action recommandée
**RUN 09 — Contractualisation progressive (SYNERGY-008)**