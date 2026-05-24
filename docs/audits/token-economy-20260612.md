# Token Economy Audit — Vibebackbone

**Date** : 2026-06-12  
**Voie** : AUDIT  
**Verdict** : PARTIAL — audit complet, réduction nécessaire

---

## Synthèse

L'audit révèle que le **boot context (L0) pèse ~19 050 tokens**, soit **3.8× la cible de 5 000**. Les 2 principaux contrevenants sont AGENTS.md (5 186) et GUIDE.md (9 271), qui sont chargés à chaque session mais ne devraient l'être qu'à la demande.

## Chiffres clés

| Métrique | Valeur |
|----------|--------|
| Index total | 249 entrées, ~280 700 tokens |
| L0 Boot actuel | ~19 050 tokens |
| L0 Boot cible | ~2 900 tokens |
| Réduction L0 possible | **×6.5 (−16K tokens/session)** |
| Redondances majeures | 4 fichiers documentent l'escalade |
| Top lourd | GUIDE.md (9 271), AGENTS.md (5 186) |

## Top 5 fichiers trop lourds pour leur couche

| Fichier | Tokens | Couche actuelle | Couche cible | Action |
|---------|--------|----------------|--------------|--------|
| GUIDE.md | 9 271 | L0 | L3 | Ne charger qu'à la demande |
| AGENTS.md | 5 186 | L0 | L3 | Réduire à bloc @import pour Claude |
| prompts/t-p-vbb-phase-router.md | 3 766 | L1 | L1 | Condenser (matrice extraite) |
| README.md | 3 567 | L4 | L4 | OK (archive) |
| docs/AUDIT_STATUS.md | 1 721 | L0 | L1 | Déplacer en L1 |

## Architecture cible L0–L4

| Couche | Contenu | Tokens | Chargé quand |
|--------|---------|--------|--------------|
| **L0 Boot** | CONTEXT.md + SYSTEM.md + CLAUDE.md + ACTIVITY_LOG.md | ~2 900 | Chaque session |
| **L1 Router** | AUDIT_STATUS.md + PILOTAGE.md + phase-router.md + MEMORY_AND_HANDOFF.md | ~8 200 | Choix voie/phase |
| **L2 Contract** | SKILL.md ciblé + CONTRACT.yaml + prompt canonique | ~4 500 | Exécution skill |
| **L3 Reference** | GUIDE.md + AGENTS.md + README + DEPLOYMENT + AGENTIC_RP | ~21 400 | À la demande |
| **L4 Archive** | docs/runs/ + docs/audits/ | ~75 000 | Via vbb-index.py seulement |

## Redondances majeures

- **Escalade** : décrite dans GUIDE.md §3.1, PILOTAGE.md §1, SESSION_RULES.md §4, AGENTS.md §4 → 4 copies
- **Voies RAPIDE/STRUCTURÉE/AUDIT/CLÔTURE** : 10+ mentions dans GUIDE.md, dupliquées dans PILOTAGE.md et SESSION_RULES.md
- **Phases 01–07** : GUIDE.md les détaille, puis AGENTIC_RUN_PROTOCOL.md les répète

## Plan RUN 14 proposé

| Step | Action | Gain tokens |
|------|--------|-------------|
| 14A | AGENTS.md boot → @import only (Claude) | −5 186 |
| 14B | GUIDE.md → L3 reference | −9 271 |
| 14C | Router matrix extraction | −1 500 |
| 14D | Redondances escalade → lien canonique | −2 000 |
| 14E | AUDIT_STATUS risques split | −800 |
| 14F | Cleanup .bak + artefacts racine | nettoyage |

**Total estimé** : −18 700 tokens/session

## Risque de perte d'efficacité

- **Faible** : les contenus sont déplacés, pas supprimés
- **Mitigation** : vbb-index.py + INDEX.yaml permettent de retrouver tout à la demande
- **Fallback** : CONTEXT.md pointe vers les outils de recherche