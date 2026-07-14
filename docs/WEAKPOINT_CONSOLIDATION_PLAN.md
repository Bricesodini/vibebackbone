---
title: "Weakpoint Consolidation — Plan complet d'exécution"
date: 2026-07-14
status: "SUPERSEDED — DO NOT EXECUTE"
scope: "vibebackbone repo uniquement, aucun consommateur"
route: "STRUCTUREE"
adr_required: "docs/adr/0032-weakpoint-consolidation.md (à créer, ACCEPTED)"
superseded_by: "docs/adr/0032-responsibility-first-routing-consolidation.md"
---

# Plan complet : Consolidation des points faibles (W1–W4)

> **Superseded on 2026-07-14.** Do not execute phases A–E below. The validated
> replacement preserves specialized skills and mandatory orchestration, and
> applies only evidence-backed routing triggers. See
> `docs/runs/2026-07-14_0830_weakpoint-responsibility-routing/` and ADR 0032.

## Vue d'ensemble

Quatre points faibles identifiés par évaluation externe (2026-07-14) :

- **W1** — 64 skills, périmètres voisins → charge de routage élevée, risque de mauvais choix par agents
- **W2** — Double indirection prompts → orchestrateur → skill → probabilité élevée de décrochage
- **W3** — Enforcement déclaratif (hook credentials log-only, gate-check --strict optionnel) → risque de non-conformité silencieuse
- **W4** — Millésimes divergents des consommateurs (TER-001), aucune procédure de resync documentée

## Principes de correction

- **Aucun ajout** : pas de nouveau skill, outil, prompt, ou règle de gouvernance.
- **Aucune dénaturation** : routes, gates, hiérarchie, contrats intacts.
- **Canon uniquement** : aucune intervention sur les repos consommateurs.
- **Réversibilité** : archivage via répertoire repo, pas suppression.

## Phases et ordre d'exécution

Exécuter dans cet ordre : A → B → C → D → E → Closeout.

---

## Phase A — Mesure d'usage des skills (canon uniquement)

### Objectif
Compter les références de chaque skill pour identifier ceux jamais utilisés.

### Entrées
- Répertoire `skills/` : tous les skills avec INDEX.yaml
- Répertoire `prompts/` : tous les prompts
- Répertoire `docs/runs` : activity logs, POCs, plans
- Fichier `docs/ACTIVITY_LOG.md`
- Distributions `distributions/pi, /claude, /codex, /opencode`

### Sortie
Créer `docs/WEAKPOINT_CONSOLIDATION_MEASUREMENT.md` avec un tableau :

```
| Skill ID | Ref Count | Locations | Status |
|----------|-----------|-----------|--------|
| 0-vbb-guide | 12 | prompts, runs, vibebackbone skill | KEEP |
| 1-vbb-monolith-detector | 0 | — | MERGE→structural-audit |
| ... | | | |
```

### Procédure
```bash
cd /Users/bricesodini/01_ai-stack/vibebackbone

# Lister tous les skills
ls skills/ | grep "^[0-9]" > /tmp/skills_list.txt

# Compter les références pour chaque skill
# Chercher dans : prompts/, skills/vibebackbone/*, docs/runs/, docs/ACTIVITY_LOG.md
for skill in $(cat /tmp/skills_list.txt); do
  COUNT=$(grep -r "$skill" prompts/ skills/vibebackbone/ docs/runs/ docs/ACTIVITY_LOG.md 2>/dev/null | wc -l)
  echo "$skill: $COUNT refs"
done | tee docs/WEAKPOINT_CONSOLIDATION_MEASUREMENT.md
```

### Critères de succès
- Tableau complété et commité
- Aucun skill supprimé (archivage réversible seulement)
- Identifications des paires/groupes de skills à périmètres voisins notées dans le tableau

---

## Phase B — Consolidation du catalogue de skills

### Objectif
Fusionner les skills à périmètres voisins (identifiés en Phase A) ; archiver (réversible) les skills jamais référencés.

### Paires/groupes identifiés (prédiction basée sur l'existant)
- **Phase 1 détecteurs structurels** : `1-vbb-monolith-detector`, `1-vbb-logic-duplication-detector`, `1-vbb-pattern-inconsistency-detector`, `1-vbb-premature-abstraction-detector` 
  → Fusionner en **`1-vbb-structural-auditor`** avec 4 modes internes (monolith, duplication, pattern, premature-abstraction)
- **Pair code-doc** : `1-vbb-code-doc-coherence-auditor` + `1-vbb-code-doc-gap-integrator` 
  → Fusionner en **`1-vbb-code-doc-auditor`** avec 2 modes (coherence, gap)

### Procédure

1. **Créer les nouveaux skills fusionnés** (example : `1-vbb-structural-auditor`) :
   ```bash
   # Copier un des skills source comme base
   cp -r skills/1-vbb-monolith-detector skills/1-vbb-structural-auditor
   
   # Éditer skills/1-vbb-structural-auditor/SKILL.md
   # - Mettre à jour le rôle et description (auditer les 4 problèmes structurels)
   # - Ajouter une section MODES avec les 4 modes (monolith, duplication, pattern, premature-abstraction)
   # - Exemple :
   #   ## MODES
   #   - monolith: detect over-centralized modules
   #   - duplication: detect logic duplication patterns
   #   - pattern: detect inconsistent patterns
   #   - premature-abstraction: detect premature generalization
   
   # Éditer skills/1-vbb-structural-auditor/CONTRACT.yaml
   # - Mettre à jour le titre et la description pour les 4 cas
   # - Conserver les même conditions de blocage
   ```

2. **Archiver les skills sources** (pas suppression, réversibilité) :
   ```bash
   mkdir -p skills/archive/2026-07-14_structural-auditor-consolidation
   mv skills/1-vbb-monolith-detector skills/archive/2026-07-14_structural-auditor-consolidation/
   mv skills/1-vbb-logic-duplication-detector skills/archive/2026-07-14_structural-auditor-consolidation/
   mv skills/1-vbb-pattern-inconsistency-detector skills/archive/2026-07-14_structural-auditor-consolidation/
   mv skills/1-vbb-premature-abstraction-detector skills/archive/2026-07-14_structural-auditor-consolidation/
   ```

3. **Archiver les skills jamais référencés** (selon la Phase A) :
   ```bash
   mkdir -p skills/archive/2026-07-14_unreferenced-skills
   # Pour chaque skill avec ref_count = 0 identifié en A :
   mv skills/<id> skills/archive/2026-07-14_unreferenced-skills/
   ```

4. **Mettre à jour INDEX.yaml** :
   ```bash
   # Éditer skills/INDEX.yaml
   # - Remplacer les 4 anciens skills par l'entrée unique 1-vbb-structural-auditor
   # - Supprimer les entrées des skills archivés (jamais référencés)
   # - Garder les approx. 15–20 skills actifs et référencés
   # Exemple :
   #   - id: 1-vbb-structural-auditor
   #     contract: ./1-vbb-structural-auditor/CONTRACT.yaml
   ```

5. **Tester et valider** :
   ```bash
   # Vérifier que les contrats YAML des nouveaux skills sont valides
   python tools/vbb-index.py 2>&1 | head -20
   
   # Vérifier que les prompts/skills/runs n'ont pas de références mortes
   # aux skills archivés (ils ne doivent pas être référencés par définition)
   grep -r "1-vbb-monolith-detector" prompts/ docs/runs/ docs/ACTIVITY_LOG.md 2>/dev/null | wc -l
   # Résultat attendu : 0
   ```

### Critères de succès
- Nouveaux skills fusionnés créés et fonctionnels (SKILL.md + CONTRACT.yaml)
- Skills archivés répertoriés et accessibles (réversibilité)
- INDEX.yaml mis à jour, validé avec vbb-index.py
- Aucune référence morte aux skills archivés
- Tests : `pytest tests/ -q` passe

---

## Phase C — Aplatir le routage des prompts

### Objectif
Réécrire les prompts existants en pointeurs directs vers les skills finaux (post-consolidation). Conserver l'indirection orchestrateur uniquement pour ENGINE_ONLY (UI/UX).

### Analyse préalable
Lire `prompts/0-p-vbb-triage.md` et `prompts/canonical/` pour identifier où le routage passe par l'orchestrateur `vibebackbone`.

Ligne clé actuelle :
```
Skill routing rule:
- Invoke `vibebackbone` first for routing decision.
```

Problème : cela crée une indirection systématique. Pour les routes non-ENGINE_ONLY, le prompt doit pointer **directement** vers le skill final.

### Procédure

1. **Éditer `prompts/0-p-vbb-triage.md`** :
   - **Garder** : « If the request mentions UI/UX, visual architecture, graphic centralization, design system, surface mapping, or "modifications graphiques" → classify ENGINE_ONLY and route to `vibebackbone` skill first. »
   - **Remplacer** pour les autres routes : au lieu de « Invoke `vibebackbone` first », diriger directement vers le skill approprié selon la classification.
   - Exemple (avant) :
     ```
     Skill routing rule:
     - Invoke `vibebackbone` first for routing decision.
     - For UI/UX requests: `vibebackbone` will emit ENGINE_ONLY route → `4-vbb-user-experience-engine`
     ```
   - Exemple (après) :
     ```
     Skill routing rule:
     - **UI/UX only**: Invoke `vibebackbone` for ENGINE_ONLY orchestration.
     - **FAST-ZERO** (≤ 3 files): Invoke directly `0-vbb-zero-friction` or project skill.
     - **STRUCTURED** (architecture, contracts): Invoke directly `1-vbb-adr`.
     - **AUDIT**: Invoke directly `2-vbb-security`, `2-vbb-performance`, etc. per scope.
     ```

2. **Éditer les autres prompts** (`1-p-vbb-quick-task.md`, `1-p-vbb-structured-task.md`, etc.) :
   - Remplacer l'indirection par des pointeurs directs vers les skills.
   - Garder le format des prompts (entrée, sortie, procédure).

3. **Valider qu'ENGINE_ONLY reste complexe** (orchestrateur requis) :
   - `prompts/canonical/` et `4-vbb-user-experience-engine` : l'orchestrateur reste, car ENGINE_ONLY bénéficie des 7 passes multi-skills.

### Critères de succès
- Prompts réécrits, pas de référence systématique à l'orchestrateur en dehors de ENGINE_ONLY
- ENGINE_ONLY conserve l'indirection (4-vbb-user-experience-engine + orchestrateur)
- Tests du routage : les prompts ciblent des skills qui existent dans INDEX.yaml
- Aucun prompt ajouté ni supprimé (modification uniquement)

---

## Phase D — Durcir l'enforcement existant

### Objectif
Passer l'enforcement de déclaratif à exécutable : bloquer les secrets ; gate-check --strict par défaut.

### D.1 Hook pre-commit credentials (clôture du gap P0-5-D)

**Fichier à modifier** : `scripts/hooks/pre-commit-credentials` (ou son équivalent dans `scripts/`)

**État actuel** : le hook ne fait que logger « checking credentials ».

**Changement** :
```bash
# Ajouter au hook un blocage réel sur les motifs évidents
# Motifs à bloquer (regex) :
# - Clés AWS : ^(?:AKIA[0-9A-Z]{16}|aws_access_key_id|aws_secret_access_key)
# - Tokens GitHub : ghp_[a-zA-Z0-9]{36}
# - Clés privées SSH : -----BEGIN RSA PRIVATE KEY-----
# - Connexions DB : (password|passwd|pwd)\s*=\s*['\"][^'\"]+['\"]
# - Tokens API génériques : (api_key|api_secret|secret_key|access_token)\s*=\s*['\"][^'\"]+['\"]

# Implémenter avec une fonction qui :
# 1. Récupère les fichiers staged (git diff --cached --name-only)
# 2. Pour chaque fichier, cherche les motifs
# 3. Si motif trouvé : afficher l'erreur et exit 1 (bloquer)
# 4. Sinon : exit 0 (laisser passer)

# Example bash pour démarrer :
#!/bin/bash
set -e
echo "Checking for credentials in staged files..."
found_secret=0
while IFS= read -r file; do
  if git show ":$file" | grep -qiE "(AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}|-----BEGIN RSA PRIVATE KEY)"; then
    echo "ERROR: Potential secret detected in $file"
    found_secret=1
  fi
done < <(git diff --cached --name-only)
if [ $found_secret -eq 1 ]; then
  echo "Commit blocked. Remove secrets and try again."
  exit 1
fi
```

**Procédure** :
```bash
# 1. Éditer scripts/hooks/pre-commit-credentials (ou créer s'absent)
# 2. Implémenter le blocage sur motifs (voir exemple ci-dessus)
# 3. Tester localement :
#    echo "aws_secret_access_key=test" > /tmp/test_creds.txt
#    git add /tmp/test_creds.txt
#    bash scripts/hooks/pre-commit-credentials
#    # Attendu : exit code 1, message d'erreur
# 4. Commiter : "fix(hooks): block credentials in pre-commit, close P0-5-D"
```

### D.2 Gate-check --strict par défaut au closeout STRUCTURED/AUDIT

**Fichier à modifier** : `prompts/canonical/07-p-vbb-closeout.md` (ou prompt closeout équivalent)

**État actuel** : `vbb-gate-check --strict` optionnel ou non invoqué.

**Changement** :
```markdown
## Step 4bis — Security gate (risk-triggered, P.R2)

For routes STRUCTURED and AUDIT, run vbb-gate-check in strict mode BEFORE committing:

\`\`\`bash
python tools/vbb-gate-check.py docs/runs/<run_id> --strict
# Exit code 0 → pass, proceed to commit
# Exit code 1 → FAIL, review blockers and address before commit
\`\`\`

For routes FAST-ZERO/MINIMAL, this step is optional (speed prioritized).
```

**Procédure** :
```bash
# 1. Trouver le prompt de closeout (docs/prompts/canonical/07-p-vbb-closeout.md ou docs/prompts/t-p-vbb-*.md)
# 2. Ajouter ou éditer la section closeout pour invoquer gate-check --strict par défaut en STRUCTURED/AUDIT
# 3. Documenter l'exception pour FAST-ZERO/MINIMAL
```

### Critères de succès
- Hook pre-commit credentials bloque sur motifs évidents (test local : secret non commité)
- Gate-check --strict invoqué par défaut au closeout STRUCTURED/AUDIT (prompte ou script)
- Tests : `pytest tests/ -q` passe

---

## Phase E — Checklist resync consommateur dans DISTRIBUTIONS.md

### Objectif
Documenter une procédure manuelle de re-synchronisation d'un consommateur vers le canon (chemin de traitement TER-001, non destructif).

### Procédure

**Fichier à éditer** : `docs/DISTRIBUTIONS.md`

**Ajouter une nouvelle section** (avant ou après « Decisions log ») :

```markdown
## Consumer Resync Checklist (Manual, Non-Destructive)

When a consumer repo (e.g., `ingest`, `Compta`, `db_projets`) diverges in
governance due to stale millésime or local adaptations, use this checklist
to re-synchronize without destructive operations.

### Pre-resync

1. **Audit current state** : Run `python tools/vbb-status-dashboard.py` in the
   consumer repo to measure divergence (skills, prompts, rules, boot set).
   Document the delta.

2. **Backup governance files** : Commit all open work in the consumer repo.

### Resync steps

1. **Pull canon updates** : `git fetch upstream` (or pull from vibebackbone repo).
   Review the canon ADRs, AGENTS.md, SYSTEM.md, and DISTRIBUTIONS.md changes
   since the consumer's last update.

2. **Update symlinks** (for distributed files like AGENTS.md, prompts) :
   - If the consumer uses symlinks to the canon (recommended), verify they
     point to the latest canon paths.
   - If the consumer has inline copies, manually diff and update.

3. **Test boot set** : Restart a session in the consumer repo. Verify that
   AGENTS.md + SYSTEM.md + CLAUDE.md load without conflicts.

4. **Run gate-check** : Execute vbb-gate-check on any open run dir to ensure
   the updated canon gates are satisfied.

5. **Document decision** : Add an entry to `docs/AUDIT_STATUS.md` (or equivalent)
   noting the resync date and any local overrides that remain (justified).

### Rollback

If resync introduces unexpected breakage, revert the canon updates and
contact the vibebackbone maintainer to diagnose the issue.

---

### Decisions log

[Existing decisions go here]

- **2026-07-14** : Added consumer resync checklist (Phase E, weakpoint consolidation).
  Non-destructive procedure for TER-001 mitigation.
```

**Procédure** :
```bash
# Éditer docs/DISTRIBUTIONS.md
# Ajouter la section Resync Checklist
# Ajouter l'entrée au Decisions log
# Commiter : "docs(distributions): add consumer resync checklist for TER-001 mitigation"
```

### Critères de succès
- Checklist documentée et lisible dans DISTRIBUTIONS.md
- Chemin de traitement TER-001 clair (non destructif, manuel)
- Entrée Decisions log notée

---

## Closeout — Vérifications P.R2 et commits

### Prérequis
- Les 5 phases (A–E) sont complétées.
- Dashboard sans régression : `python tools/vbb-status-dashboard.py` affiche verdict OK.
- Tests verts : `pytest tests/ -q` → 153+ passed.

### Procédure

1. **Vérifier l'intégrité du repo** :
   ```bash
   git status  # Aucun changement accidentel
   python tools/vbb-architecture.py lint  # Architecture source OK
   python tools/vbb-index.py  # INDEX.yaml valide, 100% skills indexés
   ```

2. **Créer l'ADR requis** (s'il n'existe pas) :
   ```bash
   # Créer docs/adr/0032-weakpoint-consolidation.md
   # Statut : ACCEPTED (plan validé par Brice en session 2026-07-14)
   # Contenu : objectif (W1–W4), décisions (fusion/archivage/durcissement/docs), conséquences
   ```

3. **Exécuter le pre-merge gate** (docs/REFERENCE/pre-merge-gate.md) :
   ```bash
   # 5 vérifications obligatoires P.R2 :
   # 1. Tests passent
   # 2. Architecture lint OK
   # 3. Index OK
   # 4. Aucun changement accidentel
   # 5. ADR accepté ou POC GO
   ```

4. **Commiter les phases** (ordre) :
   ```bash
   # A — Mesure
   git add docs/WEAKPOINT_CONSOLIDATION_MEASUREMENT.md
   git commit -m "measure(skills): audit usage across canon, phase A complete"
   
   # B — Consolidation
   git add skills/ skills/archive/ skills/INDEX.yaml
   git commit -m "refactor(skills): consolidate and archive per phase B"
   
   # C — Routage
   git add prompts/
   git commit -m "refactor(prompts): flatten routing, phase C complete"
   
   # D — Enforcement
   git add scripts/hooks/ prompts/canonical/
   git commit -m "fix(hooks): block credentials at pre-commit, phase D complete"
   
   # E — Documentation
   git add docs/DISTRIBUTIONS.md
   git commit -m "docs(distributions): add consumer resync checklist for TER-001"
   
   # ADR
   git add docs/adr/0032-weakpoint-consolidation.md
   git commit -m "docs(adr): 0032 weakpoint consolidation, ACCEPTED"
   ```

5. **Dashboard final** :
   ```bash
   python tools/vbb-status-dashboard.py
   # Attendu : Verdict READY, aucune régression
   ```

6. **Push** (optionnel, selon votre workflow) :
   ```bash
   git push origin main
   ```

---

## Récapitulatif des fichiers à modifier

| Phase | Fichier | Action |
|-------|---------|--------|
| A | `docs/WEAKPOINT_CONSOLIDATION_MEASUREMENT.md` | Créer (tableau d'usage) |
| B | `skills/INDEX.yaml` | Éditer (new skills, remove refs) |
| B | `skills/1-vbb-structural-auditor/` | Créer (fusion) |
| B | `skills/1-vbb-code-doc-auditor/` | Créer (fusion) |
| B | `skills/archive/2026-07-14_*/` | Créer répertoires d'archivage |
| C | `prompts/0-p-vbb-triage.md` | Éditer (aplatir routage) |
| C | `prompts/1-p-vbb-*.md` | Éditer (pointeurs directs) |
| D | `scripts/hooks/pre-commit-credentials` | Éditer (bloquer motifs) |
| D | `prompts/canonical/07-p-vbb-closeout.md` | Éditer (gate-check --strict) |
| E | `docs/DISTRIBUTIONS.md` | Éditer (ajouter resync checklist) |
| Closeout | `docs/adr/0032-weakpoint-consolidation.md` | Créer (ACCEPTED) |

---

## Notes de transition

- **Évaluation de la charge** : Le plan est conçu pour être autonome ; chaque phase a des critères de succès clairs et peut être validée avant de passer à la suivante.
- **Réversibilité** : Archivage via répertoire, pas suppression ; tout change peut être défait en restituant les fichiers archivés.
- **Pas de nouvelle règle** : Chaque changement consolide ou durcit l'existant ; aucun nouveau concept de gouvernance.
- **Millésime du consommateur** : Phase E prépare le chemin, mais ne modifie aucun repo consommateur — c'est une ressource documentée pour vous ou un autre agent.
