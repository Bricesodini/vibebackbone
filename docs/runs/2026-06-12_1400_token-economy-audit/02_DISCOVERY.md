# 02_DISCOVERY — RUN 13 : Token Economy Audit

**Date** : 2026-06-12  
**Phase** : 02_DISCOVERY

---

## Données brutes

### Index global
- 249 entrées indexées
- ~280,700 tokens estimés
- Répartition : skill (105), run (88), prompt (33), audit (15), doc (8)

### Top 20 fichiers les plus lourds (tokens estimés)

| # | Fichier | Tokens | Couche actuelle |
|---|---------|--------|----------------|
| 1 | GUIDE.md | 9 271 | L0/L1 |
| 2 | AGENTS.md | 5 186 | L0 |
| 3 | prompts/t-p-vbb-phase-router.md | 3 766 | L1 |
| 4 | README.md | 3 567 | L4 |
| 5 | docs/PILOTAGE.md | 1 722 | L1 |
| 6 | docs/AUDIT_STATUS.md | 1 721 | L0 |
| 7 | docs/DEPLOYMENT.md | 1 434 | L3 |
| 8 | docs/CONTEXT.md | 1 274 | L0 |
| 9 | prompts/canonical/07-p-vbb-closeout.md | 2 455 | L2 |
| 10 | prompts/canonical/06-p-vbb-review.md | 1 818 | L2 |
| 11 | SYSTEM.md | 1 047 | L0 |
| 12 | docs/MEMORY_AND_HANDOFF.md | 998 | L1 |
| 13 | docs/AGENTIC_RUN_PROTOCOL.md | 956 | L3 |
| 14 | skills/1-vbb-intent-decomposer/SKILL.md | 4 587 | L3 |
| 15 | skills/1-vbb-code-doc-coherence-auditor/SKILL.md | 3 811 | L3 |
| 16 | skills/2-vbb-spec-validator/SKILL.md | 3 749 | L3 |
| 17 | skills/1-vbb-code-doc-gap-integrator/SKILL.md | 3 684 | L3 |
| 18 | prompts/canonical/01-p-vbb-intake.md | 1 692 | L2 |
| 19 | prompts/canonical/02-p-vbb-audit.md | 1 680 | L2 |
| 20 | skills/t-vbb-docker-generate/SKILL.md | 3 211 | L3 |

### Coût L0 (boot context) estimé

| Fichier | Tokens | Observation |
|---------|--------|------------|
| AGENTS.md | 5 186 | **Trop lourd pour L0** — contient 2 blocs compilés (Claude + Codex) |
| GUIDE.md | 9 271 | **Beaucoup trop lourd** — manuel complet dans L0 |
| docs/CONTEXT.md | 1 274 | Acceptable |
| docs/AUDIT_STATUS.md | 1 721 | Acceptable mais pourrait être plus court |
| SYSTEM.md | 1 047 | Acceptable |
| CLAUDE.md | 343 | OK |
| docs/ACTIVITY_LOG.md | 238 | OK |
| **Total L0 actuel** | **~19 050** | **Devrait être ≤ 5 000** |

### Redondances majeures

| Concept | AGENTS.md | GUIDE.md | PILOTAGE.md | SESSION_RULES | DEPLOYMENT | AGENTIC_RP |
|---------|-----------|----------|-------------|---------------|------------|------------|
| voie RAPIDE | 2 | 10 | 4 | 4 | 0 | 0 |
| escalade | 4 | 9 | 5 | 5 | 2 | 0 |
| RAPIDE-ZERO | 2 | 2 | 1 | 2 | 1 | 2 |
| 01_INTAKE | 0 | 16 | 1 | 3 | 0 | 3 |
| 07_CLOSEOUT | 0 | 13 | 1 | 5 | 0 | 5 |

**Constat** : GUIDE.md documente les voies, les phases et l'escalade en détail — puis PILOTAGE.md, SESSION_RULES.md et AGENTS.md redisent chacun une version simplifiée. 4 fichiers décrivent la même escalade.