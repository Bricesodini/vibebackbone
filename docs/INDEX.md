---
context_role: navigation-index
phase: transverse
status: active
updated: 2026-07-14
---

# INDEX — Carte de navigation du dépôt

> Carte rapide. Pour le **routage opérationnel** d'une tâche, voir
> [`PILOTAGE.md`](PILOTAGE.md). Pour la **gouvernance**, voir
> [`../AGENTS.md`](../AGENTS.md) et [`../SYSTEM.md`](../SYSTEM.md).

## Point d'entrée

| Rôle | Fichier |
|------|---------|
| MOC central, premier-fichier-à-lire | [`CONTEXT.md`](CONTEXT.md) |
| Conventions qualité transverses | [`CONVENTIONS.md`](CONVENTIONS.md) |
| Demarrage MVP depuis zero | [`MVP_START_PROTOCOL.md`](MVP_START_PROTOCOL.md) |
| Routage opérationnel des tâches | [`PILOTAGE.md`](PILOTAGE.md) |
| Mode du dépôt | [`PROJECT_MODE.md`](PROJECT_MODE.md) |
| État des audits | [`AUDIT_STATUS.md`](AUDIT_STATUS.md) |
| Provenance temporelle | [`TEMPORAL_PROVENANCE.md`](TEMPORAL_PROVENANCE.md) |
| Registre léger de dette technique | [`TECH_DEBT.md`](TECH_DEBT.md) |
| Mémoire de reprise (local, gitignored) | `SESSION.md` |
| Sentinel Core README | [`../core.README.md`](../core.README.md) |

## Conventions

| Sujet | Fichier |
|-------|--------|
| Conventions qualité | [`CONVENTIONS.md`](CONVENTIONS.md) |
| Gouvernance de la connaissance d'ingénierie | [`ENGINEERING_KNOWLEDGE_GOVERNANCE.md`](ENGINEERING_KNOWLEDGE_GOVERNANCE.md) |
| Gouvernance des gates Design/Certification | [`GATE_ASSURANCE_GOVERNANCE.md`](GATE_ASSURANCE_GOVERNANCE.md) |
| Template de changement de canon | [`templates/CANON_CHANGE_PROPOSAL.md.template`](templates/CANON_CHANGE_PROPOSAL.md.template) |
| Template de dossier de connaissance | [`templates/KNOWLEDGE_RECORD.md.template`](templates/KNOWLEDGE_RECORD.md.template) |

## Protocole agentique

| Sujet | Fichier |
|-------|---------|
| Les 7 phases | [`AGENTIC_RUN_PROTOCOL.md`](AGENTIC_RUN_PROTOCOL.md) |
| Boucle d'apprentissage gouvernée | [`ENGINEERING_KNOWLEDGE_GOVERNANCE.md`](ENGINEERING_KNOWLEDGE_GOVERNANCE.md) |
| Assurance Design/Certification et autorisation | [`GATE_ASSURANCE_GOVERNANCE.md`](GATE_ASSURANCE_GOVERNANCE.md) |
| Readiness avant implementation MVP | [`MVP_START_PROTOCOL.md`](MVP_START_PROTOCOL.md) |
| Règles de session (rester / changer) | [`SESSION_RULES.md`](SESSION_RULES.md) |
| Mémoire officielle vs conversation | [`MEMORY_AND_HANDOFF.md`](MEMORY_AND_HANDOFF.md) |
| Architecture canonique structurée | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Projection graphique des relations | [`RELATIONS.md`](RELATIONS.md) |
| Templates d'artefacts | [`templates/`](templates/) |
| Artefacts de run produits | [`runs/`](runs/) |

## Gouvernance racine

| Sujet | Fichier |
|-------|---------|
| Grammaire opérationnelle | [`../AGENTS.md`](../AGENTS.md) |
| Comportement runtime | [`../SYSTEM.md`](../SYSTEM.md) |
| Point d'entrée Claude Code | [`../CLAUDE.md`](../CLAUDE.md) |

## Catalogue

| Type | Localisation | Catalogue |
|------|--------------|-----------|
| Skills | [`../skills/`](../skills/) | [`../skills/INDEX.yaml`](../skills/INDEX.yaml) |
| Prompts spécialisés et router | [`../prompts/`](../prompts/) | — |
| Prompts canoniques | [`../prompts/canonical/`](../prompts/canonical/) | — |

## Maturité

| Statut | Sens | Exemples |
|--------|------|----------|
| **Stable core** | Canonique, installé par défaut, base du système | `../AGENTS.md`, `../SYSTEM.md`, `../setup.sh`, `../setup-lib.sh`, `../core/setup.sh`, `../skills/`, `../prompts/` |
| **Distribution active** | Code spécifique à un runtime agentique, installé via le routeur | `../distributions/{claude,codex,pi,opencode}/` |
| **Optionnel / externe** | Réside hors dépôt et dépend de l’environnement machine | `~/.agents/`, `~/.claude/`, `~/.codex/`, `~/.pi/`, `~/.config/opencode/` |
| **POC / expérimental** | Preuve de concept ou transition, à ne pas confondre avec le core | `../docs/strategy/p0-4-review-matrix-poc.md` |
| **Template / réserve** | Gabarit ou réserve de futures intégrations | `../providers/templates/`, `../distributions/examples/` |
| **Archive** | Historique conservé pour traçabilité | `archive/`, `archive/prompt-migration/` |

## Audits

| Type | Localisation |
|------|--------------|
| Rapports d'audit horodatés | [`audits/`](audits/) |
| Traces du runtime de contrat | [`audits/vbb-runtime/`](audits/vbb-runtime/) |
| Audits/plans archivés ou supplantés | [`archive/`](archive/) |
| Migration historique des prompts | [`archive/prompt-migration/`](archive/prompt-migration/) |

## Outils

| Outil | Chemin |
|-------|--------|
| Linter des contrats | [`../tools/vbb-contract-lint.py`](../tools/vbb-contract-lint.py) |
| Runtime des contrats | [`../tools/vbb-contract-runtime.py`](../tools/vbb-contract-runtime.py) |
| Linter / projection architecture | [`../tools/vbb-architecture.py`](../tools/vbb-architecture.py) |
| Phase router (lookup) | [`../tools/vbb-phase-router.py`](../tools/vbb-phase-router.py) |
| Index textuel local | [`../tools/vbb-index.py`](../tools/vbb-index.py) |
| Dashboard d'état généré | [`../tools/vbb-status-dashboard.py`](../tools/vbb-status-dashboard.py) |
| CI locale | [`../scripts/vbb-ci-local.sh`](../scripts/vbb-ci-local.sh) |

## Documentation longue (humain)

| Sujet | Fichier |
|-------|---------|
| Guide pédagogique complet | [`../GUIDE.md`](../GUIDE.md) |
| Architecture des prompts (3 couches) | [`../PROMPTS_ARCHITECTURE.md`](../PROMPTS_ARCHITECTURE.md) |
| Déploiement | [`DEPLOYMENT.md`](DEPLOYMENT.md) |
| Troubleshooting | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |
| Runtime des contrats — doc | [`archive/vbb-contract-runtime.md`](archive/vbb-contract-runtime.md) |
