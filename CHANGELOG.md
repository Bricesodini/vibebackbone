# Changelog

Tous les changements notables pour le projet vibebackbone sont documentés ici.

Le format de ce fichier suit [Keep a Changelog](https://keepachangelog.com/).
Ce projet respecte le [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-05-16

### ✨ Nouveau

- **57 skills orchestrés** complètement documentés et testés
  - Phase [0] : 5 skills (readiness, scope-freeze, audit-readiness, guide, standard)
  - Phase [1] : 16 skills (structure, conventions, tech-debt, code-janitor, doc-harmonizer, etc.)
  - Phase [2] : 12 skills (security, api-auditor, db-robustness, data-integrity, ops, ci, etc.)
  - Phase [3] : 1 skill (risk-register - consolidation)
  - Phase [4] : 10 skills (UX/UI front-pipeline)
  - Transverse : 13 skills (deploy, docker, git, testing, etc.)

- **24 prompts de pilotage** pour tous les cycles (quick, structured, audit, etc.)

- **Grammaire opérationnelle canonique** :
  - AGENTS.md : 325 lignes, spécification complète
  - SYSTEM.md : 146 lignes, comportement runtime Pi
  - PILOTAGE.md : 323 lignes, source de vérité opérationnelle
  - CLAUDE.md : Point d'entrée pour Claude Code, Cursor, Codex

- **Conformité multi-agent** :
  - Pi (agents autonomes)
  - Claude Code (IDE Claude)
  - Cursor (IDE Cursor)
  - Codex (architecture vibecodex v2.0)
  - OpenCode (standards ouverts)

- **Artefacts de distribution** :
  - LICENSE (MIT)
  - CONTRIBUTING.md
  - CODE_OF_CONDUCT.md (Contributor Covenant v2.0)

### 🔧 Changements techniques

- Hiérarchie documentaire stricte : PILOTAGE.md > PROJECT_MODE.md > SESSION.md > AUDIT_STATUS.md
- Discipline de contexte LLM (limiter saturation, compaction avant 75%)
- Escalade immédiate si risque (données, auth, sécurité, conformité, prod)
- Séquence d'audit [0→1→2→3] avec préconditions explicites
- Convention de nommage cohérente : `{phase}-vbb-{intent}` (skills), `{phase}-p-vbb-{name}` (prompts)

### 📚 Documentation

- README.md complet (298 lignes) avec guide d'installation et tableau des 57 skills
- docs/PILOTAGE.md avec ordering canonique et intentions
- docs/PROJECT_MODE.md déclarant le mode DISTRIBUTION
- docs/SESSION.md template pour mémoire locale
- docs/AUDIT_STATUS.md template pour dashboard d'audits

### 🔐 Sécurité

- Audit de sécurité complet (`2-vbb-security` skill disponible)
- Risk-register (`3-vbb-risk-register` skill)
- Escalade explicite pour vulnérabilités

### 🚀 Infrastructure

- Templates de déploiement (deploy.sh, nginx.conf, security-headers.conf)
- Docker support via `t-vbb-docker-generate` skill
- Git synchronisation via `t-vbb-git-sync` skill
- CI/CD via `2-vbb-ci` skill

---

## Fonctionnalités futures (v1.x)

- [ ] Support Kubernetes manifests (helm charts)
- [ ] Support Terraform (IaC templates)
- [ ] Monitoring/alerting (Prometheus, Grafana)
- [ ] Load testing scripts (K6, JMeter)
- [ ] Database migrations tooling
- [ ] Advanced analytics dashboard

---

## Notes pour développeurs

**Versions antérieures** : vibebackbone v0.x a été développé et testé en interne pendant 6 mois avant la v1.0.

**Stabilité** : La v1.0 est considérée comme production-ready. Les API et structures de skills/prompts sont stables.

**Backward compatibility** : Aucune garantie de BC avant v2.0. Les évolutions de grammaire seront signalées dans les releases notes.

---

Pour les changements détaillés, consultez :
- [AGENTS.md](AGENTS.md) — Grammaire opérationnelle
- [skills/vibebackbone/docs/PILOTAGE.md](skills/vibebackbone/docs/PILOTAGE.md) — Logique opérationnelle
- [skills/](skills/) — Catalogues des 57 skills
