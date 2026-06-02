---
run_id: "2026-06-02_1208_deep-framework-audit"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "codex"
started_at: "2026-06-02T10:08:30Z"
ended_at: "2026-06-02T10:18:30Z"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/AUDIT_STATUS.md"
  - "prompts/canonical/02-p-vbb-audit.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "docs/audits/deep-framework-audit-20260602-1208.md"
---

# 02_AUDIT — Deep Framework Audit — 2026-06-02 12:08

## Declaration initiale

- **Route** : AUDIT
- **Type d'audit** : systemique / gouvernance / CI / coherence documentaire
- **Skill utilise** : `vibebackbone` + `0-vbb-audit-readiness` + grille generique
- **Artefact cible** : `docs/audits/deep-framework-audit-20260602-1208.md` + `docs/runs/2026-06-02_1208_deep-framework-audit/02_AUDIT.md`
- **Gouvernance lue** : `docs/CONTEXT.md`, `docs/PILOTAGE.md`, `docs/PROJECT_MODE.md`, `docs/SESSION.md`, `docs/AUDIT_STATUS.md`, `prompts/canonical/02-p-vbb-audit.md`
- **Regle de verification** : un finding est `VERIFIED_FINDING` uniquement si
  soutenu par au moins deux sources distinctes ou une commande confirmee.

## Audit-readiness

**Verdict readiness** : `READY`

Le depot est auditable: structure lisible, documentation riche, boundaries
identifiables, conventions visibles, outils de verification disponibles. Le
readiness n'est pas bloque par les dettes observees; ces dettes sont justement
exploitables par un audit systemique.

## Methode

Commandes non destructrices executees:

- `find` / `rg` / `sed` / `nl` pour inventaire et evidence.
- `python tools/vbb-contract-lint.py` -> PASS, 0 erreur.
- `python tools/vbb-architecture.py lint` -> PASS, 0 erreur.
- `python tools/vbb-contract-runtime.py run --all --dry-run` -> 43 PASS, 19 PARTIAL, 2 BLOCKED.
- `python tools/vbb-loop-closure-check.py` -> FAIL sur le run le plus recent.
- `pytest tests/ -q` -> PASS, 81 tests.
- `bash scripts/vbb-ci-local.sh` -> FAIL avant checks, dependance `pytest` absente pour `python3`.
- `python tools/vbb-status-dashboard.py` -> PARTIAL + latest runs UNKNOWN.
- comparaison `SKILL.md` frontmatter version vs `CONTRACT.yaml` version sur 64 skills.

## Verdict global

**Verdict** : `PARTIAL`

**Justification** : le coeur est sain et verifiable (`contract lint`,
`architecture lint`, runtime dry-run et pytest passent), mais la confiance
operationnelle est entamee par des ecarts concrets: CI locale non reproductible
dans l'environnement courant, dernier run non conforme a l'invariant de
fermeture, versions SKILL/CONTRACT divergentes sur tout le catalogue, index
documentaire stale, dette temporelle future-datee et artefact backup versionne.

## Findings

### VBB-DEEP-001 — CI locale non reproductible selon l'interpreteur

| Champ | Valeur |
|-------|--------|
| **Severity** | P1 |
| **Type** | VIOLATION |
| **Location** | `scripts/vbb-ci-local.sh:12`, environnement local |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: le script fixe `PYTHON="python3"` et teste `pytest`; SIGNAL: `python3` systeme n'a pas pytest; VERIFICATION: `bash scripts/vbb-ci-local.sh` echoue, tandis que `pytest tests/ -q` passe via conda; FINDING: la CI locale n'est pas reproductible dans cet environnement. |
| **Evidence** | `scripts/vbb-ci-local.sh` lignes 12 et 48-63; commande `bash scripts/vbb-ci-local.sh` -> `Missing Python dependencies: pytest`; `pytest tests/ -q` -> 81 passed; `python3` -> `/Applications/Xcode.../python3` sans pytest. |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Rendre `PYTHON` configurable (`PYTHON=${PYTHON:-python3}`), documenter l'environnement attendu, ou faire pointer la CI locale vers l'interpreteur courant quand il satisfait les dependances. |

### VBB-DEEP-002 — Dernier run invalide pour l'invariant de fermeture

| Champ | Valeur |
|-------|--------|
| **Severity** | P1 |
| **Type** | VIOLATION |
| **Location** | `docs/runs/20260602_0817_pr-operational-principles/07_CLOSEOUT.md` |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: `vbb-loop-closure-check.py` exige `01_INTAKE + 04_PLAN + 05_EXECUTION + 07_CLOSEOUT` pour STRUCTUREE et `01_INTAKE + 02_AUDIT + 03_DECISION + 07_CLOSEOUT` pour AUDIT; SIGNAL: le dernier run ne contient qu'un `07_CLOSEOUT.md` sans frontmatter; VERIFICATION: `python tools/vbb-loop-closure-check.py` echoue sur ce run; FINDING: l'invariant P.R4 est contredit par le run le plus recent. |
| **Evidence** | `tools/vbb-loop-closure-check.py` lignes 15-21; `docs/runs/20260602_0817_pr-operational-principles/07_CLOSEOUT.md` lignes 1-7; commande de closure -> FAIL, 2 issues. |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Completer le run avec frontmatter et artefacts attendus, ou reclasser explicitement le run en `CLOTURE` si c'etait un closeout ad hoc. Ajouter un test qui interdit de laisser le dernier run en UNKNOWN dans le dashboard. |

### VBB-DEEP-003 — Versioning SKILL.md vs CONTRACT.yaml divergent sur 64/64 skills

| Champ | Valeur |
|-------|--------|
| **Severity** | P1 |
| **Type** | VIOLATION |
| **Location** | `skills/*/SKILL.md`, `skills/*/CONTRACT.yaml` |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: chaque skill a un frontmatter `version`, chaque contrat a une `version`; SIGNAL: tous les contrats declarent `0.3`, les SKILL.md declarent des versions fonctionnelles variables; VERIFICATION: script de comparaison YAML retourne 64 mismatches sur 64; FINDING: la version n'a pas de semantique unifiee et le linter ne la controle pas. |
| **Evidence** | `python tools/vbb-contract-lint.py` passe a 0 erreur; comparaison locale retourne `mismatches 64`; exemples: `0-vbb-audit-readiness` `1.1` vs `0.3`, `4-vbb-design-system-validator` `3.2` vs `0.3`, `vibebackbone` `1.3` vs `0.3`. |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Decider si `CONTRACT.yaml.version` represente le schema contractuel ou la version du skill. Si c'est le schema, renommer en `contract_schema_version`; si c'est la version du skill, ajouter un check au linter. |

### VBB-DEEP-004 — Index documentaire stale sur le compteur de skills

| Champ | Valeur |
|-------|--------|
| **Severity** | P2 |
| **Type** | VIOLATION |
| **Location** | `docs/INDEX.md:60` |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: `docs/INDEX.md` annonce `Skills (63)`; SIGNAL: README, CONTEXT et filesystem annoncent 64; VERIFICATION: `find skills -mindepth 1 -maxdepth 1 -type d | wc -l` et `grep -c '^  - id:' skills/INDEX.yaml` retournent 64; FINDING: l'index de navigation n'est plus coherent avec la source active. |
| **Evidence** | `docs/INDEX.md` ligne 60; `README.md` lignes 4, 23, 53; `docs/CONTEXT.md` catalogue; commandes d'inventaire -> 64 dirs, 64 SKILL.md, 64 CONTRACT.yaml, 64 index entries. |
| **Decision** | DEFER |
| **Recommendation** | Corriger `docs/INDEX.md` et ajouter un check documentaire simple dans la CI ou le status dashboard pour les compteurs publics. |

### VBB-DEEP-005 — Dette temporelle future-datee toujours active

| Champ | Valeur |
|-------|--------|
| **Severity** | P2 |
| **Type** | TREND |
| **Location** | `docs/AUDIT_STATUS.md`, `docs/runs/`, `docs/audits/` |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: date locale 2026-06-02; plusieurs docs actifs sont dates 2026-06-12, 2026-06-13 ou 2026-06-29; SIGNAL: le status dashboard signale cette provenance; VERIFICATION: `vbb-status-dashboard.py` liste 38 run directories posterieurs a la date locale; FINDING: la dette temporelle est documentee mais reste operationnellement perturbante. |
| **Evidence** | `date` -> 2026-06-02 12:07:56 CEST; `docs/PILOTAGE.md` version datee 2026-06-12; `docs/AUDIT_STATUS.md` updated 2026-06-29; dashboard -> temporal skew acknowledged + 38 run directories after local date. |
| **Decision** | MITIGATED |
| **Recommendation** | Garder la note de provenance, mais ajouter un mode "current workspace date" aux rapports/status pour eviter que les futures notes soient presentees comme etat courant non nuance. |

### VBB-DEEP-006 — Artifact backup versionne dans un dossier de skill canonique

| Champ | Valeur |
|-------|--------|
| **Severity** | P2 |
| **Type** | VIOLATION |
| **Location** | `skills/vibebackbone/docs/PILOTAGE.md.bak` |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: un `.bak` existe dans `skills/vibebackbone/docs`; SIGNAL: il est suivi par git; VERIFICATION: `git ls-files ...` retourne le fichier; FINDING: un backup manuel est versionne dans un module canonique. |
| **Evidence** | `find . -name '*.bak'` -> `skills/vibebackbone/docs/PILOTAGE.md.bak`; `git ls-files` confirme qu'il est versionne; `skills/vibebackbone/SKILL.md` demote son `docs/PILOTAGE.md` comme reference detaillee, pas le `.bak`. |
| **Decision** | DEFER |
| **Recommendation** | Supprimer le `.bak` ou le deplacer dans `docs/archive/` avec justification historique. |

### VBB-DEEP-007 — `CONVENTIONS.md` contient des compteurs historiques stale

| Champ | Valeur |
|-------|--------|
| **Severity** | P3 |
| **Type** | OBSERVATION |
| **Location** | `docs/CONVENTIONS.md:172-174` |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: la traceability section annonce `40+ runs`, `92% closeout rate`, `17 timestamped reports`; SIGNAL: l'inventaire courant est superieur; VERIFICATION: `find docs/runs ...` retourne 55 closeouts / 163 files et `find docs/audits ...` retourne 28 rapports markdown; FINDING: les compteurs historiques ne sont plus a jour. |
| **Evidence** | `docs/CONVENTIONS.md` lignes 172-174; commandes d'inventaire -> 55 closeouts, 28 audits markdown. |
| **Decision** | DEFER |
| **Recommendation** | Remplacer les compteurs fixes par "voir status dashboard" ou generer ces valeurs. |

### VBB-DEEP-008 — Prompt entrypoint names in AGENTS.md do not resolve to files at advertised path

| Champ | Valeur |
|-------|--------|
| **Severity** | P2 |
| **Type** | VIOLATION |
| **Location** | `AGENTS.md`, prompt library deployment |
| **Evidence Level** | VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION: AGENTS indique que `audit-task`, `quick-task`, `structured-task`, `release-check`, `session-handoff` doivent etre lus dans `/Users/bot/.agents/prompts/vibebackbone/`; SIGNAL: ce dossier ne contient aucun fichier dans l'environnement courant; VERIFICATION: `find /Users/bot/.agents/prompts/vibebackbone -maxdepth 2 -type f` retourne vide, tandis que les prompts existent dans le repo sous des noms prefixes (`2-p-vbb-audit-task.md`, etc.); FINDING: la consigne d'entree prompt est non resoluble telle quelle en local. |
| **Evidence** | `AGENTS.md` mentionne les noms courts; `find /Users/bot/.agents/prompts/vibebackbone` -> aucun fichier; `find prompts -name '*.md'` -> 33 fichiers dont `prompts/2-p-vbb-audit-task.md`. |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Installer les prompts via `setup.sh`, ou modifier AGENTS/SYSTEM pour pointer vers les noms deployes reels ou vers le repo local quand il est la source active. |

## Risques consolides

| Risque | Severity | Probabilite | Impact | Action recommandee |
|--------|----------|-------------|--------|--------------------|
| Fausse confiance CI locale | P1 | High | High | Fix interpreter/deps, re-run CI locale complete |
| Invariant de fermeture affaibli | P1 | Medium | High | Completer/reclasser dernier run et rendre dashboard bloquant sur UNKNOWN |
| Metadata skills non fiable | P1 | High | Medium | Clarifier version schema vs skill version |
| Adoption confuse via prompts non installes | P2 | Medium | Medium | Corriger deployment/AGENTS mapping |
| Drift documentaire | P2/P3 | High | Medium | Automatiser compteurs et status |

## Ce qui est hors scope

- Audit exhaustif ligne par ligne des 64 skills.
- Audit des profils Hermes `~/.hermes/profiles/*/SOUL.md` hors repo, sauf traces deja
  presentes dans les closeouts.
- Correction des findings.
- Recalcul complet du risk register.

## Handoff

**Phase suivante** : 03_DECISION

**Nouvelle session recommandee** : Oui. L'auditeur ne doit pas trancher seul les
decisions de remediation.

**A transmettre** : ce rapport + `docs/audits/deep-framework-audit-20260602-1208.md`.

**Priorites proposees** :
1. VBB-DEEP-001 / VBB-DEEP-002: restaurer la confiance verification/closure.
2. VBB-DEEP-003: clarifier le versioning contractuel.
3. VBB-DEEP-008 / VBB-DEEP-004: corriger prompt deployment et compteurs.

PROGRESS:
  phase: testing
  done: "Inventaires, lints contrat/architecture, runtime dry-run, pytest et CI locale executes."
  next: "Decision de remediation separee."
  files_touched: []
  risks: ["CI locale echoue dans l'environnement courant; dernier run closure invalide."]
  estimated_remaining: "n/a"
  needs_extension: false

FINAL_STATUS:
  elapsed_seconds: 630
  budget_initial: 180
  progress_emitted: true
  progress_count: 1
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/runs/2026-06-02_1208_deep-framework-audit/01_INTAKE.md
    - docs/runs/2026-06-02_1208_deep-framework-audit/02_AUDIT.md
    - docs/audits/deep-framework-audit-20260602-1208.md
    - docs/AUDIT_STATUS.md
  tests_run:
    - "python tools/vbb-contract-lint.py"
    - "python tools/vbb-architecture.py lint"
    - "python tools/vbb-contract-runtime.py run --all --dry-run"
    - "python tools/vbb-loop-closure-check.py"
    - "pytest tests/ -q"
    - "bash scripts/vbb-ci-local.sh"
  tests_missing:
    - "Full remediation tests; audit only."
  risks:
    - "Local CI failure due python3 dependency mismatch."
    - "Latest run closure invariant failure."
  open_points:
    - "No remediation applied in audit phase."
