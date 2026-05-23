---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-05-23
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

- **Voie** : RAPIDE — hygiène documentaire (Lot F+G)
- **Run** : `2026-05-23_2100_hygiene-lot-f-g` — PR #6 en cours
- **Phase** : 07 (CLOSEOUT) ✅ Complété
- **Prochaine action** : merge `feat/artifact-loop-closure` → main

## Runs récents

| Date | Run | Statut | Lien |
|------|-----|--------|------|
| 2026-05-23 | hygiene-lot-f-g | ✅ Complet | [closeout](runs/2026-05-23_2100_hygiene-lot-f-g/07_CLOSEOUT.md) |
| 2026-05-23 | phase2-contracts-lot-5b | ✅ Complet | [closeout](runs/2026-05-23_2000_phase2-contracts-lot-5b/07_CLOSEOUT.md) |
| 2026-05-23 | bootstrap-project-client-lot-e | ✅ Complet | [closeout](runs/2026-05-23_1900_bootstrap-project-client-lot-e/07_CLOSEOUT.md) |
| 2026-05-23 | artifact-verify-lot-c | ✅ Complet | [closeout](runs/2026-05-23_1800_artifact-verify-lot-c/07_CLOSEOUT.md) |
| 2026-05-23 | contracts-artifact-schema-lot-b-d | ✅ Complet | [closeout](runs/2026-05-23_1700_contracts-artifact-schema-lot-b-d/07_CLOSEOUT.md) |
| 2026-05-23 | artifact-infra-lot-a | ✅ Complet | [closeout](runs/2026-05-23_1600_artifact-infra-lot-a/07_CLOSEOUT.md) |
| 2026-05-19 | moc-context-strategy | ✅ Complet | [closeout](runs/2026-05-19_1000_moc-context-strategy/07_CLOSEOUT.md) |

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
| `skills/` | 58 skills · 22 CONTRACT.yaml indexés → [skills/](../skills/) |
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