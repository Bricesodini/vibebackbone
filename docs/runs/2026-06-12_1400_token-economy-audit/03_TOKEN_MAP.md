# 03_TOKEN_MAP — RUN 13 : Carte des couches token

**Date** : 2026-06-12  
**Phase** : 03_DECISION

---

## Carte actuelle vs cible

### L0 — Boot context (chargé à chaque session)

**Cible** : ≤ 5 000 tokens

| Fichier | Tokens actuel | Couche actuelle | Couche cible | Action |
|---------|--------------|----------------|--------------|--------|
| docs/CONTEXT.md | 1 274 | L0 | L0 | ✅ Garder tel quel |
| SYSTEM.md | 1 047 | L0 | L0 | ✅ Garder |
| CLAUDE.md | 343 | L0 | L0 | ✅ Garder |
| docs/ACTIVITY_LOG.md | 238 | L0 | L0 | ✅ Garder |
| **AGENTS.md** | **5 186** | L0 | **L3** | **Retirer du boot** — ne charger qu'à l'exécution |
| **GUIDE.md** | **9 271** | L0 | **L3** | **Retirer du boot** — référence, pas boot |
| docs/AUDIT_STATUS.md | 1 721 | L0 | L1 | Déplacer en L1 — pas nécessaire au boot |

**Total L0 actuel** : ~19 050  
**Total L0 cible** : ~2 900 (×6.5 réduction)

### L1 — Router context (choisir voie/phase/skill)

| Fichier | Tokens | Observation |
|---------|--------|------------|
| docs/AUDIT_STATUS.md | 1 721 | Nécessaire pour le verdict |
| docs/PILOTAGE.md | 1 722 | Décisions de voie |
| prompts/t-p-vbb-phase-router.md | 3 766 | Router principal |
| docs/MEMORY_AND_HANDOFF.md | 998 | Handoff de session |
| **Total L1** | **~8 207** | Acceptable mais router pourrait être condensé |

### L2 — Contract context (vérifier/exécuter un skill)

| Fichier | Tokens | Observation |
|---------|--------|------------|
| prompts/canonical/*.md (7) | ~12 000 | Chargé par phase |
| skill SKILL.md ciblé | 1 500–4 500 | Un seul à la fois |
| skill CONTRACT.yaml | 300–650 | Un seul à la fois |
| **Total L2 par exécution** | **~3 000–6 000** | OK — usage ciblé |

### L3 — Full skill/reference

| Fichier | Tokens | Observation |
|---------|--------|------------|
| AGENTS.md | 5 186 | Référence complète, pas boot |
| GUIDE.md | 9 271 | Manuel complet |
| README.md | 3 567 | Reference |
| docs/DEPLOYMENT.md | 1 434 | Déploiement |
| docs/AGENTIC_RUN_PROTOCOL.md | 956 | Protocole |
| **Total L3** | **~21 414** | Référence, indexé, chargé à la demande |

### L4 — Archive/history

| Catégorie | Entrées | Tokens estimés |
|-----------|---------|---------------|
| docs/runs/**/* | 88 | ~60 000 |
| docs/audits/**/* | 15 | ~15 000 |
| **Total L4** | **103** | **~75 000** |

---

## Résumé cible

| Couche | Tokens actuel | Tokens cible | Réduction |
|--------|--------------|--------------|-----------|
| L0 Boot | ~19 050 | ~2 900 | **×6.5** |
| L1 Router | ~8 207 | ~8 207 | stable |
| L2 Contract | ~4 500/skill | ~4 500/skill | stable |
| L3 Reference | ~21 414 | ~21 414 | stable |
| L4 Archive | ~75 000 | ~75 000 | indexé seulement |

**Gain principal** : L0 réduit de 19K → 2.9K tokens = **16K tokens économisés par session**.