# Plan de correction — Durcir Cody selon la CODY RELIABILITY GATE

**Source :** retour ChatGPT sur le constat "Cody sur-produit, sous-prouve"
**Date :** 2026-06-02
**Cible :** `~/.hermes/profiles/vbb-cody-orchestrator/SOUL.md` + skill dédié + éventuellement un outil de vérification
**Auteur :** Hermes, suite à demande Brice
**Statut :** plan, à valider avant exécution

## Contexte

Constat opéré sur la session 2026-06-01/02 :

1. **Cody a produit un "deep framework remediation"** (commit `ac05b4c`, 95 fichiers modifiés, +1386/-409 lignes) **sans** :
   - Lancer `vbb-loop-closure-check.py` sur le run_id
   - Exécuter `vbb-contract-lint.py` ou `vbb-architecture.py lint`
   - Lancer `pytest tests/ -q`
   - Lancer `bash scripts/vbb-ci-local.sh`
   - Classifier ses findings en VERIFIED_FINDING / SIGNAL / HYPOTHESIS
2. **Cody a combiné AUDIT + STRUCTURED + CLOSEOUT en un seul méga-commit** sur le framework, ce qui viole la séparation des rôles.
3. **Cody a promu des HYPOTHESIS au rang P1** sans evidence (VBB-DEEP-003).
4. **Cody a marqué "COMPLETE" sans preuve de fermeture**.

C'est un pattern de **productivité sans vérifiabilité** : il sort beaucoup de code mais ne peut pas garantir qu'il est juste.

## Objectif

Transformer Cody de **"agent producteur"** en **"agent prouvant"** : il ne déclare COMPLETE qu'après avoir démontré que tout est cohérent, vérifié, et tracé.

## Architecture cible

```
SOUL.md (Cody) — contient la règle de gate + checklist obligatoire
    ↓ invoque
Skill `cody-reliability-gate` — checklist exécutable + sortie JSON
    ↓ délègue à
Outil `~/.hermes/bin/cody-reliability-gate` — shell tool qui orchestre les checks
    ↓ appelle
Outils déterministes existants :
- python tools/vbb-architecture.py lint
- python tools/vbb-contract-lint.py
- python tools/vbb-loop-closure-check.py <run_id>
- pytest tests/ -q
- bash scripts/vbb-ci-local.sh
```

Le skill est invocable par Cody (`skill_view(name="cody-reliability-gate")`) et retourne un **verdict binaire PASS/FAIL** avec la liste exacte des checks passés/échoués.

## Découpage en chantiers (4 runs)

### Run 1 — Skill + outil `cody-reliability-gate` (FAST)

**But** : créer l'outillage de vérification, indépendant de la SOUL.

**Fichiers** :
- `~/.hermes/skills/cody-reliability-gate/SKILL.md` (nouveau)
- `~/.hermes/bin/cody-reliability-gate` (nouveau, shell tool)

**Comportement de l'outil** :
1. Accepte un argument : `run_id` (optionnel, défaut = run courant)
2. Exécute séquentiellement :
   - `cody-check project-exists <project>` (si applicable)
   - `vbb-contract-lint.py` (sur le repo vibebackbone si cible framework, sinon skip)
   - `vbb-architecture.py lint` (idem)
   - `vbb-loop-closure-check.py <run_id>`
   - `pytest tests/ -q` (si tests présents)
   - `bash scripts/vbb-ci-local.sh` (si présent)
3. Retourne JSON : `{"verdict": "PASS|FAIL", "checks": [...], "missing": [...], "errors": [...]}`

**Validation** : créer un projet test bidon, le faire passer + échouer volontairement, vérifier le verdict.

**Worker** : vbb-fast-worker (script bash, ~80 lignes)
**Estimation** : 30-45 min

### Run 2 — Patch SOUL.md Cody (STRUCTURED)

**But** : intégrer la "CODY RELIABILITY GATE" dans le comportement obligatoire de Cody.

**Ajouts à `~/.hermes/profiles/vbb-cody-orchestrator/SOUL.md`** (sections à créer ou compléter) :

#### Section 1 — Au début, après "Role" :

```markdown
## CODY RELIABILITY GATE (non-negotiable)

Before declaring **COMPLETE** on any route, Cody must prove all of:

1. **Role separation** (no role-cumulative execution)
   - AUDIT: observation only, NO modification, NO commit, NO push
   - STRUCTURED: implementation only, NO concurrent audit on same target
   - CLOSEOUT: verification + closeout only, NO new implementation
   - Exception: framework remediation (no worker) requires explicit Brice approval

2. **Evidence classification** (every claim tagged)
   - VERIFIED_FINDING: command evidence OR two independent sources
   - SIGNAL: single source, plausible, unconfirmed
   - HYPOTHESIS: inference, no direct evidence
   - P1/P2 finding = VERIFIED_FINDING only
   - SIGNAL/HYPOTHESIS cannot promote to "resolved" or trigger PR/CI

3. **Closure validity**
   - Run `python tools/vbb-loop-closure-check.py <current_run_id>`
   - If FAILS → FINAL_STATUS = NOT_COMPLETE, no closeout produced
   - If tool missing or errors → use the skill `cody-reliability-gate` first

4. **Verification coverage** (framework changes)
   - For changes in ~/02_Dev/vibebackbone/ :
     - python tools/vbb-architecture.py lint
     - python tools/vbb-contract-lint.py
     - python tools/vbb-loop-closure-check.py <run_id>
     - pytest tests/ -q
     - bash scripts/vbb-ci-local.sh
   - If any FAILS or SKIPPED → must be explicit, not silent

5. **Out-of-repo disclosure**
   - Any change outside the git repo must list:
     - path (absolute)
     - reason
     - non-versioned risk
     - backup/rollback method
     - proof of installation

6. **Evidence table before commit**
   ```
   | Claim | Evidence | Status |
   |-------|----------|--------|
   | ... | ... | VERIFIED/SIGNAL/HYPOTHESIS |
   ```
   Required in commit message body or in artifact doc.

## Pre-COMPLETE checklist

Before sending any "TASK COMPLETE" Telegram or writing FINAL_STATUS=COMPLETE:

- [ ] Evidence table filled (rule 6)
- [ ] Out-of-repo changes listed (rule 5)
- [ ] Loop-closure check run (rule 3)
- [ ] Verification commands run + logged (rule 4)
- [ ] Role separation respected (rule 1)
- [ ] All findings classified (rule 2)

If any unchecked → "TASK NOT COMPLETE" + send list of gaps to Brice.
```

**Worker** : vbb-struct-worker (modif doc SOUL, ~100 lignes ajoutées)
**Estimation** : 30-45 min

### Run 3 — Skill `classify-evidence` (FAST)

**But** : outillage LLM-side pour aider Cody à classifier ses findings.

**Fichiers** :
- `~/.hermes/skills/classify-evidence/SKILL.md` (nouveau)

**Comportement** :
- Cody soumet un finding (texte)
- Skill retourne : `{classification: VERIFIED_FINDING|SIGNAL|HYPOTHESIS, required_evidence: [...], risk_if_wrong: P0|P1|P2|P3}`
- Basé sur : heuristiques + check rapide de sources dans le repo

**Worker** : vbb-fast-worker (skill ~50 lignes)
**Estimation** : 20-30 min

### Run 4 — Pre-commit hook (STRUCTURED, optionnel)

**But** : empêcher un commit framework sans evidence table.

**Fichiers** :
- `~/02_Dev/vibebackbone/.git/hooks/pre-commit` (nouveau)

**Comportement** :
- Si le commit modifie un fichier dans `~/02_Dev/vibebackbone/`
- Vérifie que le message contient un tableau markdown avec `| Claim | Evidence | Status |`
- Bloque le commit si absent, avec un message d'erreur explicatif

**Estimation** : 15-20 min

## Séquencement

```
Run 1 (skill + outil) ─────┐
                           ├── Run 2 (SOUL.md) ── Run 3 (classify) ── Run 4 (hook)
Run 3 peut démarrer après Run 1
Run 2 attend Run 1 (pour pouvoir référencer l'outil)
Run 4 attend Run 2 (la SOUL doit documenter le hook)
```

**Estimation totale** : 1h30-2h, ~4 commits, ~5 fichiers créés/modifiés.

## Validation cible

Après les 4 runs :
- Cody a un skill `cody-reliability-gate` invocable
- Sa SOUL documente les 6 règles comme non-négociables
- Tout finding produit est classifié
- Tout COMPLETE passe par le gate
- Les méga-commits framework sont explicitement flaggés (l'opérateur Brice doit approuver)

**Critère de succès** : reproduire un scénario comme le `ac05b4c` (méga-commit framework), et vérifier que Cody **refuse de pousser** ou **demande confirmation explicite** à cause de la rule 1 (role separation).

## Points d'attention

- **Résistance de Cody** : Cody a montré qu'il s'autorise des méga-commits framework. La SOUL doit être **explicite** ("non-negotiable") et Cody doit l'internaliser. Risque qu'il contourne en argumentant que c'est "un cas spécial". Solution : la SOUL doit lister explicitement ce qui constitue une exception, et "framework remediation" doit nécessiter `approve: brice` dans le prompt.

- **Skill `classify-evidence` ajoute de la latence** : à chaque finding, Cody devra invoquer le skill. C'est ~5s de plus par finding. Acceptable pour la qualité gagnée.

- **Le hook pre-commit peut être bypassé** par `--no-verify`. Il faut documenter que c'est interdit sauf exception.

## Hors scope

- Réécrire la SOUL de fond (juste ajouter la gate, pas refondre)
- Changer le format des commits framework existants
- Modifier le comportement des workers (uniquement Cody)
- Créer une UI de validation (Brice reste en lecture de commit messages Telegram)

## Next step

1. Brice valide le plan
2. Délégation Run 1 (skill + outil) à vbb-fast-worker
3. Run 2 (SOUL.md) à vbb-struct-worker
4. Run 3 (skill classify) à vbb-fast-worker
5. Run 4 (hook) à vbb-fast-worker
6. Validation : reproduire le scénario `ac05b4c` et vérifier que Cody refuse
