---
run_id: "2026-07-27_1612_engineering-knowledge-governance"
phase: "01_INTAKE"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-27T14:12:17Z"
ended_at: "2026-07-27T14:18:00Z"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "user request and explicit run approval"
  - "AGENTS.md"
  - "SYSTEM.md"
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/PROJECT_MODE.md"
  - "docs/SESSION.md"
  - "docs/AUDIT_STATUS.md"
  - "docs/CONVENTIONS.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Engineering knowledge governance

## Demande reçue

Faire évoluer Vibe Backbone pour gouverner la découverte, la qualification,
la maturation, la capitalisation et la réutilisation des apprentissages
d'ingénierie, sans dépendance à une technologie ou à un projet particulier.

## Décision humaine d'ouverture

Brice autorise le run `AUDIT → DECISION → STRUCTURED` pour produire et
qualifier une proposition canonique complète. Cette autorisation n'accepte pas
encore la modification du Core.

Amendements obligatoires :

1. une revue indépendante intervient après l'audit de connaissance et avant
   toute décision humaine de promotion ;
2. les critères de promotion portent sur l'indépendance des validations dans
   le périmètre revendiqué, pas sur un nombre de projets ;
3. une connaissance canonique est immuable : son évolution crée une nouvelle
   version qui repasse par le cycle complet.

## Reformulation

Concevoir une seconde boucle de gouvernance, reliée mais non confondue avec le
cycle de livraison, puis démontrer qu'elle préserve les sept phases, l'unicité
de l'autorité et l'indépendance de la revue.

## Scope

### Dans le périmètre

- Audit du cycle actuel et de ses frontières documentaires.
- Définition des états de maturité et des preuves de promotion.
- Définition du cycle de vie symétrique des patterns et anti-patterns.
- Proposition d'un Knowledge Harvest au closeout.
- Analyse d'impact Core et quatre distributions.
- ADR proposé, POC, plan d'intégration et revue indépendante.

### Hors périmètre

- Acceptation de l'ADR.
- Modification de la gouvernance canonique, des prompts, templates, outils,
  tests, skills ou distributions.
- Promotion d'un apprentissage concret provenant d'un projet particulier.
- Commit ou push avant décision humaine finale.

### Dépendances détectées

- **Liée à ADR** : `docs/adr/0049-engineering-knowledge-governance.md`
- `docs/CONVENTIONS.md` : discipline de changement du canon.
- `docs/AGENTIC_RUN_PROTOCOL.md` : sept phases et clôture.
- `docs/ARCHITECTURE.md` : blocs Governance Core et Audit Memory.
- `docs/DISTRIBUTIONS.md` : propagation vers Pi, OpenCode, Codex et Claude.
- `prompts/canonical/07-p-vbb-closeout.md` et son template.

## Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : changement transversal du Core, de ses responsabilités
  documentaires et du comportement attendu au closeout.

## Voie recommandée

- **Voie** : `AUDIT`, suivie d'une décision puis d'une exécution STRUCTURED
  uniquement après validation humaine finale.
- **Justification** : `GUIDE.md` interdit la modification directe de la
  gouvernance et exige au minimum audit et décision.

## Handoff vers `02_AUDIT`

- **Entrées à lire** : corpus listé dans le frontmatter, architecture,
  distributions, prompts et templates de closeout.
- **Points de vigilance** : ne pas créer une phase 08 implicite, une seconde
  autorité documentaire ou une promotion automatique.
