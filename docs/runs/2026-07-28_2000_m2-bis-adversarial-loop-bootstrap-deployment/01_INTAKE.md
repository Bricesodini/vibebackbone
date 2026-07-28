---
run_id: "2026-07-28_2000_m2-bis-adversarial-loop-bootstrap-deployment"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "ACTIVE"
kind: "BOOTSTRAP_DEPLOYMENT"
posture: "consume-rem01-rem02-m2-deferred"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
started_at: "2026-07-28T20:00:00Z"
ended_at: "2026-07-28T20:15:00Z"
agent: "external implementer (distinct session, distinct provider)"
artifacts_produced:
  - "01_INTAKE.md"
source_runs_consumed:
  - "2026-07-28_1002_adversarial-loop-governance-design (M0)"
  - "2026-07-28_1200_m1-adversarial-loop-normative-arbitration (M1)"
  - "2026-07-28_1400_m2-adversarial-loop-implementation (M2)"
  - "2026-07-28_1600_r0-adversarial-audit-of-m2-implementation (R0)"
  - "2026-07-28_1800_r1-r0-findings-normative-arbitration (R1)"
---

# INTAKE — M2-BIS Bootstrap + Déploiement opérationnel

## Décisions humaines (RATIFIÉES)

| ID | Décision |
|---|---|
| **REM-01** | **ACCEPTÉ** — implémenter statuts PRE_CERTIFICATION + MIGRATION |
| **REM-02** | **ACCEPTÉ** — étendre `vbb-loop-closure-check.py` pour schéma 1.1 |
| **PRE_CERTIFICATION** | **RATIFIÉ** — 6ᵉ valeur de `certification_status` |
| **MIGRATION** | **RATIFIÉ** — 7ᵉ valeur de `certification_status` |
| **SELF_HOSTING** | **NON RETENU** |

## Périmètre strict (verbatim du brief)

**Travaux autorisés :**

1. **Bootstrap** — Implémenter statuts `PRE_CERTIFICATION` + `MIGRATION`
   conformément aux arbitrages R1.
2. **Outillage** — Étendre `vbb-loop-closure-check.py` et
   `vbb-adversarial-gate.py` pour reconnaître le schéma 1.1 et les
   nouveaux statuts.
3. **Déploiement** — Consommer les éléments différés de M2 :
   - outils ;
   - templates ;
   - skills ;
   - prompts ;
   - tests ;
   - distributions.

**Hors périmètre (interdictions) :**

- ❌ Modifier les décisions M1.
- ❌ Modifier les niveaux A0/A1/A2.
- ❌ Modifier ADR 0051 hors adaptations strictement nécessaires
  aux statuts ratifiés.
- ❌ Introduire SELF_HOSTING.
- ❌ Ouvrir une nouvelle évolution de gouvernance.

**Aucune nouvelle décision normative autorisée.**

## Vérifications imposées

| Vérification | Statut attendu |
|---|---|
| Tous les findings R1 concernés sont fermés | ✅ via exécution REM-01..08 |
| Aucun nouveau statut n'est introduit | ✅ scope strict aux statuts ratifiés |
| Compatibilité ascendante conservée | ✅ additif pur |
| Projets existants restent migrables | ✅ schema 1.1 additif |
| Anciens workflows fonctionnent | ✅ P.R2 toujours green |

## Source normative unique

| Source | Rôle |
|---|---|
| `M1_DECISIONS.md` (M1-01..M1-06) | décisions normatives |
| `2026-07-28_1400/.../M2_DEFERRED_ITEMS.md` | 31 entrées à consommer |
| `2026-07-28_1800/.../03_DECISION.md` (R1) | qualifications + REM-01..10 |
| `2026-07-28_1800/.../07_CLOSEOUT.md` (R1) | bootstrap tranché |

## Plan d'exécution

### Tier 1 — Bootstrap canon (REM-01)

1. Étendre `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §10 + nouveau §11 :
   statuts PRE_CERTIFICATION + MIGRATION + conditions.
2. Étendre `GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 :
   énumérations `certification_status` + nouveau bloc
   `transient_reason` + `bootstrapped_at`.

### Tier 2 — Outillage (REM-02 + M2-24)

1. Étendre `tools/vbb-loop-closure-check.py` (REM-02) :
   accepter `adversarial_governance_version: "1.1"`,
   `certification_status: PRE_CERTIFICATION | MIGRATION`,
   valider bloc `adversarial` v1.1.
2. Créer `tools/vbb-adversarial-gate.py` (M2-24) :
   validator ≥ 500 lignes, schema 1.1, fail-closed, A0/A1/A2.

### Tier 3 — Templates (M2-26..M2-28)

1. `docs/templates/FINDING.md.template` (M2-26, NEW)
2. `docs/templates/ADVERSARIAL_CAMPAIGN.md.template` (M2-26, NEW)
3. `docs/templates/07_CLOSEOUT.md.template` (M2-27, extended)
4. `docs/templates/06_REVIEW.md.template` (M2-27, extended)
5. `docs/templates/01_INTAKE.md.template` (M2-28, extended)

### Tier 4 — Skills (M2-29, M2-30)

1. `skills/2-vbb-adversarial-campaign/SKILL.md` (NEW)
2. `skills/t-vbb-adversarial-corpus/SKILL.md` (NEW)
3. `skills/0-vbb-pilotage/SKILL.md` (extended)
4. `skills/0-vbb-standard/SKILL.md` (extended)

### Tier 5 — Prompts (M2-31)

1. `prompts/0-p-vbb-triage.md` (extended)
2. `prompts/07-p-vbb-closeout.md` (extended)
3. `prompts/2-p-vbb-audit-task.md` (extended)
4. `prompts/1-p-vbb-structured-task.md` (extended)

### Tier 6 — Tests (M2-14, M2-18, M2-21, M2-23, NEW)

11 tests NEW ou MODIFY (cf. M2_DEFERRED_ITEMS.md Tier 6).

### Tier 7 — Distributions (CR#12, M2-32, M2-33)

1. `distributions/pi/SYSTEM.md` (étendu)
2. `distributions/opencode/AGENTS.md` (étendu)
3. `distributions/codex/AGENTS.md` (étendu)
4. `distributions/claude/CLAUDE.md` (étendu)
5. `docs/DISTRIBUTIONS.md` §Decisions log (étendu)

### Tier 8 — Cutoff / ramp / validation (M2-34 actif, M2-35..37 partiels)

1. M2-34 cutoff **déjà actif** (déclaré dans M2, ADR 0051, etc.).
2. M2-35 R0 advisory — applicable dès Tier 2 livré.
3. M2-36 `vbb-gate-check.py --json` post-canon.
4. M2-37 `pytest tests/ -q` (toute la nouvelle suite verte).

## Contraintes

- ❌ Aucune déviation de M1.
- ❌ Aucun enrichissement de périmètre.
- ❌ Aucune modification des décisions A0/A1/A2.
- ✅ Strict consumption R1 + M2_DEFERRED_ITEMS.

## Livrables

- `01_INTAKE.md` (ce fichier)
- `04_PLAN.md`
- `05_EXECUTION.md`
- `06_INDEPENDENT_REVIEW.md` (PARTIAL disclosed)
- `07_CLOSEOUT.md`
- Proposition de commit (message + liste fichiers)