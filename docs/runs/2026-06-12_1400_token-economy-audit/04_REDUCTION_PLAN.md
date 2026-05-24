# 04_REDUCTION_PLAN — RUN 13 : Plan de réduction token

**Date** : 2026-06-12  
**Phase** : 04_PLAN

---

## Réductions proposées (classées par impact)

### P1 — Retirer AGENTS.md du boot (−5 186 tokens)

**Actuel** : AGENTS.md est le bloc compilé inséré dans ~/.claude/CLAUDE.md et ~/.codex/AGENTS.md. Il contient 2 blocs générés de ~2 500 tokens chacun.

**Proposition** : Remplacer le bloc compilé par un pointeur + commande de lookup :
```
# Vibebackbone Governance
@{AGENTS_SRC}  ← Keep this reference line only
```
Le bloc compilé ne doit être régénéré que pour les providers qui n'ont pas `@import` (Codex). Pour Claude Code, l'`@import` suffit.

**Risque** : Codex ne supporte pas `@import`. Garder le bloc compilé pour Codex uniquement.

### P2 — Retirer GUIDE.md du boot (−9 271 tokens)

**Actuel** : GUIDE.md fait 9 271 tokens et est la doc complète, mais n'est pas nécessaire au boot.

**Proposition** : GUIDE.md reste accessible via `skills/0-vbb-guide/SKILL.md`. Ne pas le charger au boot. L'agent peut le lire via `vbb-index.py search` quand nécessaire.

**Risque** : Nouveaux agents peuvent manquer de contexte. Mitigation : CONTEXT.md contient la règle "use vbb-index.py search".

### P3 — Condenser AUDIT_STATUS.md (−800 tokens)

**Actuel** : 1 721 tokens avec table de risque détaillée.

**Proposition** : Déplacer la table de risques vers `docs/AUDIT_STATUS_RISKS.md` et ne garder que le verdict global + pointeur.

### P4 — Condenser le phase router (−1 500 tokens)

**Actuel** : `prompts/t-p-vbb-phase-router.md` fait 3 766 tokens avec matrice complète.

**Proposition** : Extraire la matrice en JSON dans `prompts/router-matrix.json` (~800 tokens). Le prompt ne garde que les règles de routing + fallback. L'agent lit le JSON à la demande.

### P5 — Redondances voies/escalade (−2 000 tokens)

**Actuel** : 4 fichiers décrivent l'escalade (GUIDE.md, PILOTAGE.md, SESSION_RULES.md, AGENTS.md).

**Proposition** : GUIDE.md = source canonique. PILOTAGE.md et SESSION_RULES.md se contentent d'un lien vers GUIDE.md#escalade.

### P6 — Archiver PILOTAGE.md.bak (+ divers nettoyages)

**Actuel** : `skills/vibebackbone/docs/PILOTAGE.md.bak` existe.

**Proposition** : Supprimer le .bak. Nettoyer les 5 artefacts migration racine.

---

## Plan RUN 14 proposé

| Step | Action | Impact |
|------|--------|--------|
| 14A | AGENTS.md boot ↔ reference split | −5 186 L0 tokens |
| 14B | GUIDE.md → L3 reference only | −9 271 L0 tokens |
| 14C | Router matrix extraction | −1 500 L1 tokens |
| 14D | Redondances escalade condensation | −2 000 tokens |
| 14E | AUDIT_STATUS audit split | −800 L0 tokens |
| 14F | Cleanup .bak + artefacts racine | Nettoyage |

**Gain total estimé** : ~18 700 tokens/session (L0 + L1)  
**Risque** : Faible — toutes les réductions déplacent, ne suppriment pas.

---

## Risques de perte d'efficacité

1. **Agents sans GUIDE.md au boot** : Peuvent manquer les conventions. → Mitigation : CONTEXT.md mentionne vbb-index + GUIDE.md accessible via skill.
2. **Codex sans bloc compilé** : Perd le contenu inline. → Mitigation : Garder le bloc compilé pour Codex uniquement.
3. **Router condensé** : Peut mal router si contexte insuffisant. → Mitigation : Fallback explicite vers GUIDE.md.