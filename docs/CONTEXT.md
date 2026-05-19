---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-05-19
---

# CONTEXT.md — MOC / Routeur central persistant

> Premier fichier à lire au démarrage. Carte du contexte projet, point d'entrée de reprise.
> **Ce fichier pointe vers — il ne duplique pas.** Les liens localisés sont des pointeurs de fetch, pas une garantie de chargement automatique.

## Identité du projet

- **Nom** : vibebackbone
- **Mode** : [DISTRIBUTION](PROJECT_MODE.md#mode)
- **Vocation** : Catalogue de distribution de skills, prompts et gouvernance pour agents LLM
- **Gouvernance** : [AGENTS.md](../AGENTS.md) · [SYSTEM.md](../SYSTEM.md) · [PILOTAGE.md](PILOTAGE.md)

## Contexte actif

- **Voie** : STRUCTURÉE — intégration documentaire (MOC / routeur central)
- **Run** : `2026-05-19_1000_moc-context-strategy` — Création de CONTEXT.md
- **Phase** : 07 (CLOSEOUT) ✅ Complété
- **Prochaine action** : aucun chantier ouvert — maintenance usuelle

## Runs récents

| Date | Run | Statut | Lien |
|------|-----|--------|------|
| 2026-05-19 | moc-context-strategy | ✅ Complet | [closeout](runs/2026-05-19_1000_moc-context-strategy/07_CLOSEOUT.md) |
| 2026-05-18 | prompts-agentic-migration | ✅ Complet | [closeout](runs/2026-05-18_2300_prompts-agentic-migration/07_CLOSEOUT.md) |
| 2026-05-18 | run05-test-cases | ✅ Patch | — |
| 2026-05-18 | reformat-agentic-protocol | ✅ Complété | — |

## Décisions actives

| Décision | Verdict | Lien |
|----------|---------|------|
| CONTEXT.md comme MOC central | GO (condition levée) | [03](runs/2026-05-19_1000_moc-context-strategy/03_DECISION_RECORD.md) |

## Risques / audits

- **Verdict global** : 🟢 PRODUCTION-READY + OPENCODE-READY → [AUDIT_STATUS.md](AUDIT_STATUS.md)
- **Risques P0/P1** : 0
- **Risques P2** : 2 (mitigés) → détail dans [Risques Identifiés](AUDIT_STATUS.md#risques-identifiés--status)

## Artefacts structurants

| Rép | Contenu |
|-----|---------|
| `docs/` | Gouvernance, runs, audits → [INDEX.md](INDEX.md) |
| `skills/` | 57 skills standards → [skills/](../skills/) |
| `prompts/` | 24 prompts de session → [prompts/](../prompts/) |

## Points ouverts

1. 🟡 Runs sans closeout formel (reformat-agentic-protocol, run05-test-cases) — *moyenne*
2. ⬜ DEPLOYMENT.md, RUNBOOK.md, TROUBLESHOOTING.md (post-v1.0) — *basse*
3. ⬜ Harmonisation lexicale « persistant » vs « persistant et versionné » — *basse*
4. ⬜ Section `## Mise à jour de CONTEXT.md` promotion P0 après usage — *basse*

## Convention de liens localisés

1. Liens Markdown relatifs uniquement : `[label](path.md#anchor)`
2. Ancres vers sections stables quand possible
3. Pas de dépendance exclusive aux liens Obsidian `[[…]]`
4. Liens = pointeurs de fetch, pas garantie de chargement automatique
5. Pas de lien vers un fichier absent
6. Mise à jour corrélative si une section stable change de nom

## Historique des modifications

| Date | Section | Changement |
|------|---------|------------|
| 2026-05-19 | Runs récents · Décisions actives · Points ouverts · Contexte actif | RUN 06 : clôture cycle — CONDITIONAL_GO levé, statut final |
| 2026-05-19 | Runs récents · Décisions actives · Contexte actif · Points ouverts | RUN 04 : restructuration tables + prochaine action + priorités |
| 2026-05-19 | Création | Création initiale du MOC central |