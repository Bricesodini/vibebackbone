---
context_role: navigation-index
phase: transverse
status: active
updated: 2026-05-23
---

# INDEX — Carte de navigation du dépôt

> Carte rapide. Pour le **routage opérationnel** d'une tâche, voir
> [`PILOTAGE.md`](PILOTAGE.md). Pour la **gouvernance**, voir
> [`../AGENTS.md`](../AGENTS.md) et [`../SYSTEM.md`](../SYSTEM.md).

## Point d'entrée

| Rôle | Fichier |
|------|---------|
| MOC central, premier-fichier-à-lire | [`CONTEXT.md`](CONTEXT.md) |
| Routage opérationnel des tâches | [`PILOTAGE.md`](PILOTAGE.md) |
| Mode du dépôt | [`PROJECT_MODE.md`](PROJECT_MODE.md) |
| État des audits | [`AUDIT_STATUS.md`](AUDIT_STATUS.md) |
| Mémoire de reprise (local, gitignored) | `SESSION.md` |

## Protocole agentique

| Sujet | Fichier |
|-------|---------|
| Les 7 phases | [`AGENTIC_RUN_PROTOCOL.md`](AGENTIC_RUN_PROTOCOL.md) |
| Règles de session (rester / changer) | [`SESSION_RULES.md`](SESSION_RULES.md) |
| Mémoire officielle vs conversation | [`MEMORY_AND_HANDOFF.md`](MEMORY_AND_HANDOFF.md) |
| Templates d'artefacts | [`templates/`](templates/) |
| Artefacts de run produits | [`runs/`](runs/) |

## Gouvernance racine

| Sujet | Fichier |
|-------|---------|
| Grammaire opérationnelle | [`../AGENTS.md`](../AGENTS.md) |
| Comportement runtime | [`../SYSTEM.md`](../SYSTEM.md) |
| Point d'entrée Claude Code / Cursor | [`../CLAUDE.md`](../CLAUDE.md) |

## Catalogue

| Type | Localisation | Catalogue |
|------|--------------|-----------|
| Skills (58) | [`../skills/`](../skills/) | [`../skills/INDEX.yaml`](../skills/INDEX.yaml) |
| Prompts spécialisés (24) + 1 router | [`../prompts/`](../prompts/) | — |
| Prompts canoniques (7) | [`../prompts/canonical/`](../prompts/canonical/) | — |

## Audits

| Type | Localisation |
|------|--------------|
| Rapports d'audit horodatés | [`audits/`](audits/) |
| Traces du runtime de contrat | [`audits/vbb-runtime/`](audits/vbb-runtime/) |

## Outils

| Outil | Chemin |
|-------|--------|
| Linter des contrats | [`../tools/vbb-contract-lint.py`](../tools/vbb-contract-lint.py) |
| Runtime des contrats | [`../tools/vbb-contract-runtime.py`](../tools/vbb-contract-runtime.py) |
| Phase router (lookup) | [`../tools/vbb-phase-router.py`](../tools/vbb-phase-router.py) |
| CI locale | [`../scripts/vbb-ci-local.sh`](../scripts/vbb-ci-local.sh) |

## Documentation longue (humain)

| Sujet | Fichier |
|-------|---------|
| Guide pédagogique complet | [`../GUIDE.md`](../GUIDE.md) |
| Architecture des prompts (3 couches) | [`../PROMPTS_ARCHITECTURE.md`](../PROMPTS_ARCHITECTURE.md) |
| Déploiement | [`DEPLOYMENT.md`](DEPLOYMENT.md) |
| Troubleshooting | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |
| Runtime des contrats — doc | [`archive/vbb-contract-runtime.md`](archive/vbb-contract-runtime.md) |
