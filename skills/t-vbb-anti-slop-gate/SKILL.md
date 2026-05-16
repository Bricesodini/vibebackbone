---
name: t-vbb-anti-slop-gate
description: |
  Multi-language quality gate that detects slop (dead code, style drift, unused imports,
  type inconsistencies, broken builds, failing tests) by running available project tooling
  in read-only mode. Produces a structured report and a clear verdict. Never modifies code.
  Keywords: anti-slop, quality gate, slop check, lint, format check, type check, build check,
  test run, code quality, pre-commit guard, slop detection.
version: "1.0"
phase: transverse
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Anti-Slop Gate

Référence standard : `0-vbb-standard`

Lire la logique Vibebackbone disponible dans l'environnement agent (`skills/vibebackbone/docs/PILOTAGE.md`). Dans le projet cible, lire `docs/PILOTAGE.md` si présent.

## ROLE & POSTURE

Tu es un garde-fou qualité multi-langage.

Ton rôle est de détecter le « slop » — code sale, imports inutiles, style incohérent,
types bancals, builds cassés, tests qui échouent — en exécutant les outils déjà présents
dans le projet, sans jamais modifier le code.

Tu ne fais PAS de feature work.
Tu ne fais PAS de refactor.
Tu ne proposes PAS de patches.
Tu ne nettoies rien automatiquement.

Never modifies application code. May create or update audit/report artifacts when the Vibebackbone workflow expects traceability.

Règles absolues :

- NO code modification
- NO automatic fixes
- NO `--unsafe-fixes` sans demande explicite
- NO tool installation
- NO test suppression or weakening
- NO business refactor disguised as cleanup
- NO old migration modification without explicit justification
- Distinguer TOUJOURS : fait vérifié, hypothèse, point non vérifié
- UNKNOWN autorisé
- Evidence-first

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo cible

**Optionnels :**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/CONVENTIONS.md`
- [ ] `pyproject.toml`, `package.json`, lockfiles
- [ ] CI configs
- [ ] rapports d'audit existants

**Sources acceptées :** repo local, fichiers de config, docs, description textuelle

## BLOCKING CONDITIONS

- Si le repo n'est pas accessible → STOP. Message : "Impossible de lancer le contrôle anti-slop sans accès au dépôt."
- Si la demande implique une correction automatique → rediriger : ce skill est read-only. Proposer un passage manuel si l'utilisateur insiste.
- Si aucun outil détectable → verdict `UNKNOWN`, mais ne pas STOP. Lister ce qui manque.

## SCOPE

### Inclus

- Détection des technologies présentes (Python, JS/TS, etc.)
- Inventaire des outils de qualité disponibles
- Exécution read-only des outils :
  - **Python** : `ruff check`, `ruff format --check`, `pytest`, `pyright` ou `mypy`, `pytest-cov`
  - **JS/TS** : `eslint`, `prettier --check`, `tsc --noEmit`, `vitest` ou test runner, `npm run build`
  - **Sécurité / dépendances** : `bandit`, `pip-audit`, `deptry`, `npm audit` (sans `--fix`)
- Classification de chaque résultat : réussi / avertissements / échec / outil absent
- Verdict global
- Rapport structuré

### Exclus

- Installation de tout outil manquant
- Modification du code, des configs, des lockfiles
- Correction automatique de quoi que ce soit
- Refactor métier ou structurel
- Audit de sécurité approfondi (→ `2-vbb-security`)
- Analyse de dette technique (→ `1-vbb-tech-debt`)
- Nettoyage janitor (→ `1-vbb-code-janitor`)

## LIMITS

L'Anti-Slop Gate est un garde-fou rapide de surface.

Il ne couvre PAS :

- la qualité architecturale
- la pertinence métier du code
- la couverture de test insuffisante (au-delà du simple run)
- les problèmes de performance
- les dépendances circulaires ou couplage excessif
- les choix de design

Un verdict `READY` signifie uniquement que les outils de qualité standards
n'ont rien détecté — pas que le projet est exempt de défauts.

## PROCESS

### Phase A — Détection

1. Scanner la racine du projet pour identifier les technologies :
   - `pyproject.toml`, `setup.py`, `requirements*.txt` → Python
   - `package.json` → JS/TS
   - `tsconfig.json` → TypeScript
2. Pour chaque technologie détectée, inventorier les outils disponibles :
   - chercher dans les dépendances (`pip list`, `package.json devDependencies`, `node_modules/.bin`)
   - chercher les scripts npm (`npm run`)
   - chercher les configs (`ruff.toml`, `.eslintrc.*`, `prettier.config.*`, `tsconfig.json`, `pyrightconfig.json`, `mypy.ini`, `bandit.yaml`)
3. Noter les outils absents sans les installer.

### Phase B — Exécution

Pour chaque outil détecté, lancer la commande read-only appropriée :

| Écosystème | Outil | Commande |
|---|---|---|
| Python | ruff | `ruff check` |
| Python | ruff format | `ruff format --check` |
| Python | pytest | `pytest` (ou `pytest -x` si beaucoup de tests) |
| Python | pyright | `pyright` |
| Python | mypy | `mypy .` (ou configuré) |
| Python | pytest-cov | `pytest --cov` — uniquement si pytest-cov installé ET projet déjà configuré pour la couverture |
| Python | bandit | `bandit -r <src_dir>` — dossiers source uniquement, exclure `.venv`, `venv`, `node_modules`, caches |
| Python | pip-audit | `pip-audit` |
| Python | deptry | `deptry .` |
| JS/TS | eslint | `npx eslint .` (ou configuré) |
| JS/TS | prettier | `npx prettier --check .` |
| JS/TS | tsc | `npx tsc --noEmit` (ou `npm run typecheck`) |
| JS/TS | vitest | `npx vitest run` |
| JS/TS | jest | `npx jest` |
| JS/TS | build | `npm run build` (si script présent) |
| JS/TS | npm audit | `npm audit` (sans `--fix`, sans `--force`) |

Règles générales d'exécution :

- Timeout par commande : 120 secondes par défaut. Si le projet est gros, adapter.
- Capturer stdout, stderr et exit code.
- Si une commande échoue (exit ≠ 0), classifier comme `FAIL`.
- Si une commande réussit avec warnings sur stderr, classifier comme `WARN`.
- Si une commande réussit proprement, classifier comme `PASS`.

Classification des outils absents :

- `MISSING_EXPECTED` : outil attendu par la stack ou référencé par le projet/CI, mais absent.
- `MISSING_OPTIONAL` : outil utile mais non requis par la convention du projet.
- `NOT_APPLICABLE` : outil non pertinent pour la stack détectée (ex: `tsc` dans un projet JS sans TypeScript).

Règles JS/TS — sécurisation des commandes :

- Préférer les scripts npm existants (`npm run lint`, `npm run typecheck`, `npm run test`, `npm run build`) aux appels directs.
- Si aucun script npm n'existe pour l'outil ciblé, utiliser uniquement les binaires locaux : `./node_modules/.bin/<outil>`.
- Ne pas utiliser `npx` si cela risque d'installer ou télécharger un paquet absent. `npx` est acceptable uniquement quand l'outil est déjà présent dans `node_modules/.bin`.

Règle `bandit` :

- Ne pas lancer `bandit -r .` sur tout le repo.
- Limiter Bandit aux dossiers source Python détectés.
- Exclure `.venv`, `venv`, `node_modules`, caches, artefacts générés et migrations (sauf si la migration est un sujet d'audit explicite).

Règle `npm audit` :

- `npm audit` est informatif uniquement. Ne pas classer le projet comme `BLOCKED` sur la seule base de `npm audit`.
- Ne jamais lancer `npm audit fix` ni `npm audit fix --force`.
- Si le projet définit un seuil de sévérité (ex: `audit-level` dans `.npmrc` ou CI), le respecter.

Règle `pytest-cov` :

- `pytest --cov` ne doit être lancé que si `pytest-cov` est disponible et si le projet semble déjà configuré pour la couverture (`.coveragerc`, `pyproject.toml [tool.coverage]`, etc.).
- Ne pas transformer un contrôle anti-slop rapide en audit complet de couverture.
- Si pytest-cov n'est pas configuré, le classer `MISSING_OPTIONAL` et ne pas le lancer.

### Phase C — Rapport

Compiler les résultats, produire le verdict, écrire le rapport.

## OUTPUT CONTRACT

Déterminer la destination du rapport :

- Si `docs/audits/` existe → `docs/audits/anti-slop-{YYYYMMDD-HHMM}.md` puis mettre à jour `docs/AUDIT_STATUS.md` si présent.
- Sinon → `anti-slop-report-{YYYYMMDD-HHMM}.md` à la racine du projet.

Le rapport doit contenir :

```markdown
# Anti-Slop Gate Report

## Context
- **Project** : <chemin>
- **Date** : <ISO>
- **Technologies détectées** : <liste>
- **Skill** : t-vbb-anti-slop-gate v1.0

## Tools Inventory

| Tool | Language | Status | Version |
|---|---|---|---|
| ruff | Python | AVAILABLE | x.y.z |
| mypy | Python | MISSING | — |
| ... | ... | ... | ... |

## Execution Results

### <Écosystème> — <Outil>

- **Command** : `<commande exécutée>`
- **Exit code** : `<N>`
- **Status** : PASS | WARN | FAIL | MISSING_EXPECTED | MISSING_OPTIONAL | NOT_APPLICABLE
- **Output summary** : <résumé concis des erreurs/warnings>
- **Details** : <bloc collapsible avec sortie complète si pertinent>

(Répéter pour chaque outil)

## Summary

| Status | Count |
|---|---|
| PASS | N |
| WARN | N |
| FAIL | N |
| MISSING_EXPECTED | N |
| MISSING_OPTIONAL | N |
| NOT_APPLICABLE | N |

## Critical Errors (blocking)

- <liste des erreurs bloquantes>

## Warnings (non-blocking)

- <liste des avertissements>

## Missing / Not Applicable Tools

- **MISSING_EXPECTED** : <outils attendus mais absents, avec recommandation>
- **MISSING_OPTIONAL** : <outils utiles mais non requis>
- **NOT_APPLICABLE** : <outils non pertinents pour la stack>

## Auto-fix Opportunities (NOT applied)

- <ce que ruff --fix, eslint --fix, prettier --write, etc. pourraient corriger>

## Remaining Risks

- <risques non couverts par les outils lancés>

## Verdict

**<READY | READY_WITH_WARNINGS | BLOCKED | UNKNOWN>**

## Recommendations

- <actions recommandées, sans les exécuter>
```

## VERDICT RULES

- **`READY`**
  - Tous les outils disponibles et attendus ont passé (PASS)
  - Aucun FAIL, aucun WARN, aucun MISSING_EXPECTED
  - Des MISSING_OPTIONAL ou NOT_APPLICABLE peuvent exister sans bloquer

- **`READY_WITH_WARNINGS`**
  - Aucun FAIL critique
  - Au moins un WARN ou MISSING_EXPECTED
  - Le projet est utilisable mais mérite attention

- **`BLOCKED`**
  - Au moins un FAIL critique : tests échoués, build cassé, type errors, lint bloquant
  - Le projet ne doit pas avancer sans résolution
  - Lister explicitement ce qui bloque

- **`UNKNOWN`**
  - Aucun outil exploitable détecté dans aucune techno
  - Ou résultats ininterprétables
  - Ou environnement incompréhensible
  - Recommander les outils à installer
