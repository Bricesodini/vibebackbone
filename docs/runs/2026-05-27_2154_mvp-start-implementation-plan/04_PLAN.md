---
run_id: "2026-05-27_2154_mvp-start-implementation-plan"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-05-27T20:00:00Z"
ended_at: "2026-05-27T20:25:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/audits/mvp-start-readiness-20260527-2142.md"
  - "docs/runs/2026-05-27_2142_mvp-start-readiness-audit/03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — MVP Start Protocol Implementation Runs

## Objectif

Integrer le MVP Start Protocol et le readiness gate RICO sans creer de verite parallele entre gouvernance, router executable, prompts, skills, contrats et documentation publique.

## Hypotheses de plan

- MVP START est planifie comme un **gate/pre-route obligatoire avant STRUCTURED EXECUTION** pour les projets demarres depuis zero. Cette option minimise la refonte de la taxonomie "4 routes" tout en satisfaisant "route MVP START ou equivalent".
- Aucun nouveau prompt specialise n'est cree dans le plan de base. `0-p-vbb-before-building.md` devient l'entree de pre-build post-RICO, et le router pointe vers `0-vbb-rico-readiness` pour le demarrage MVP. Si un prompt dedie est exige plus tard, l'ajouter en run optionnel.
- Les documents historiques de run/audit restent immuables. Les docs actives et release/status sont harmonisees.

## Pre-conditions

- Charger l'audit : `docs/audits/mvp-start-readiness-20260527-2142.md`.
- Verifier l'etat git avant chaque run : `git status --short`.
- Ne pas commencer un run si le precedent n'a pas ete valide ou explicitement marque `PARTIAL`.
- Utiliser `apply_patch` pour les edits manuels.

## Run 0 — Baseline et garde-fous

**But** : figer l'etat de depart et confirmer les compteurs avant patch.

**Fichiers cibles** : aucun edit attendu.

**Actions**

1. Relever `git status --short`.
2. Relever compteurs :
   - `find skills -mindepth 1 -maxdepth 1 -type d | wc -l`
   - `find skills -mindepth 2 -maxdepth 2 -name CONTRACT.yaml | wc -l`
   - `find prompts -type f -name '*.md' | wc -l`
3. Lancer :
   - `python tools/vbb-contract-lint.py`
   - `python tools/vbb-phase-router.py "rico readiness mvp start" --dry-run`

**Sortie attendue**

- Baseline connue : 62 skills, 62 contracts, 33 prompts.
- Router RICO absent confirme.

**Rollback**

- Aucun, lecture seule.

## Run 1 — Protocole canonique MVP Start

**But** : creer la source de verite du cadrage avant implementation.

**Fichiers cibles**

- `docs/MVP_START_PROTOCOL.md`
- `docs/INDEX.md`

**Actions**

1. Creer `docs/MVP_START_PROTOCOL.md` avec sections obligatoires :
   - philosophie : no code before readiness, architecture avant execution, refus du best-effort coding ;
   - RICO / brief initial : objectif produit, utilisateurs, probleme, parcours MVP, perimetre, hors-scope, contraintes, data model initial, criteres d'acceptation, risques critiques ;
   - questions bloquantes : comportement `BLOCKED` et sortie questions priorisees ;
   - invariants d'architecture : business/API/persistence/UI separes, pas de fichier monolithique, ADR pour decisions structurantes ;
   - autorisation de codage : livrables et criteres avant passage a implementation.
2. Ajouter `MVP_START_PROTOCOL.md` a `docs/INDEX.md` dans les points d'entree/protocole.
3. Ne pas encore modifier `CONTEXT.md`, pour garder le protocole testable en isolation.

**Validation**

- Le document existe et contient les 5 sections.
- `rg -n "no code before readiness|RICO|questions bloquantes|Autorisation de codage" docs/MVP_START_PROTOCOL.md`.

**Rollback**

- Supprimer `docs/MVP_START_PROTOCOL.md` et retirer son entree de `docs/INDEX.md`.

## Run 2 — Skill `0-vbb-rico-readiness`

**But** : rendre le gate executable et contractualise.

**Fichiers cibles**

- `skills/0-vbb-rico-readiness/SKILL.md`
- `skills/0-vbb-rico-readiness/CONTRACT.yaml`
- `skills/INDEX.yaml`

**Actions**

1. Creer le dossier `skills/0-vbb-rico-readiness/`.
2. Rediger `SKILL.md` selon `0-vbb-standard` :
   - role : evaluer readiness MVP depuis RICO/brief initial ;
   - posture : pas de code, pas d'hypotheses silencieuses, UNKNOWN autorise ;
   - input contract : brief/RICO, objectif produit, utilisateurs, parcours, data model initial, contraintes, acceptance criteria ;
   - blocking conditions : brief absent, data model absent si persistence demandee, architecture absente si code demande ;
   - output : `READY` -> cahier des charges de base exploitable ; `BLOCKED` -> questions bloquantes priorisees.
3. Rediger `CONTRACT.yaml` v0.3 :
   - `id: 0-vbb-rico-readiness`
   - phase_scope : `phase_0`, `mvp_start`, `readiness`, `validation`
   - triggers : `rico`, `mvp start`, `readiness`, `brief initial`, `no code before readiness`, `questions bloquantes`, `cahier des charges`
   - artifact primaire : `docs/runs/{run_id}/02_AUDIT.md` ou `01_INTAKE.md` selon decision ; recommende `02_AUDIT.md` car c'est un gate evaluatif.
4. Ajouter l'entree au bon emplacement dans `skills/INDEX.yaml`, proche des autres `0-vbb-*`.

**Validation**

- `python tools/vbb-contract-lint.py`
- `python tools/vbb-phase-router.py "rico readiness mvp start" --dry-run`
- Le router doit retourner `0-vbb-rico-readiness` dans les premiers resultats.
- Compteurs attendus apres run : 63 skills, 63 contracts, 33 prompts.

**Rollback**

- Supprimer le dossier du skill et retirer l'entree `skills/INDEX.yaml`.

## Run 3 — Gouvernance et protocole agentique

**But** : ancrer "no code before readiness" dans les fichiers canoniques.

**Fichiers cibles**

- `docs/PILOTAGE.md`
- `docs/AGENTIC_RUN_PROTOCOL.md`
- `AGENTS.md`
- `SYSTEM.md`

**Actions**

1. Dans `docs/PILOTAGE.md` :
   - ajouter une section "MVP START gate" avant la table ou dans la table ;
   - definir conditions d'entree : nouveau projet, MVP depuis zero, brief/RICO incomplet, demande de coder sans cadrage ;
   - definir sortie : `READY` vers STRUCTURED EXECUTION, `BLOCKED` vers questions bloquantes.
2. Dans `docs/AGENTIC_RUN_PROTOCOL.md` :
   - ajouter un paragraphe "Readiness validation before execution" ;
   - interdire `05_EXECUTION` applicatif si readiness `BLOCKED` ou `UNKNOWN` ;
   - ajouter escalades : ambiguite critique -> questions ; architecture non definie -> pas de code ; donnees non modelisees -> pas de persistence.
3. Dans `AGENTS.md` et `SYSTEM.md` :
   - ajouter la regle canonique sous forme courte ;
   - pointer vers `docs/MVP_START_PROTOCOL.md` sans dupliquer tout le protocole.
4. Garder la taxonomie lisible : "4 route families + MVP START gate" si l'hypothese du plan est conservee.

**Validation**

- `rg -n "MVP START|no code before readiness|readiness|persistence" docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md AGENTS.md SYSTEM.md`
- Relecture manuelle : aucune contradiction avec la hierarchie documentaire.

**Rollback**

- Revert ciblé des paragraphes ajoutes dans les quatre fichiers.

## Run 4 — Prompts et router documentaire

**But** : empecher les points d'entree de session de contourner le gate.

**Fichiers cibles**

- `prompts/t-p-vbb-phase-router.md`
- `docs/router/ROUTER_MATRIX.md`
- `prompts/0-p-vbb-before-building.md`
- `prompts/canonical/01-p-vbb-intake.md`
- Optionnel : `prompts/1-p-vbb-project-init.md`

**Actions**

1. Dans `prompts/t-p-vbb-phase-router.md` :
   - ajouter MVP START gate avant FAST/STRUCTURED ;
   - router RICO/MVP depuis zero vers `0-vbb-rico-readiness`.
2. Dans `docs/router/ROUTER_MATRIX.md` :
   - ajouter une ligne Phase 01 / MVP START ;
   - ajouter une sequence "MVP START -> readiness -> STRUCTURED".
3. Dans `prompts/0-p-vbb-before-building.md` :
   - le transformer en gate pre-build post-RICO ;
   - ajouter `0-vbb-rico-readiness` comme skill prioritaire en phase 2 ou pre-phase.
4. Dans `prompts/canonical/01-p-vbb-intake.md` :
   - ajouter detection "projet depuis zero / MVP / brief incomplet" ;
   - phase suivante : `02_AUDIT` via `0-vbb-rico-readiness`, pas `05_EXECUTION`.
5. Mettre a jour `prompts/1-p-vbb-project-init.md` seulement si le demarrage projet doit pointer explicitement vers MVP Start apres initialisation gouvernance.

**Validation**

- `rg -n "MVP START|0-vbb-rico-readiness|RICO|no code before readiness" prompts docs/router/ROUTER_MATRIX.md`
- `python tools/vbb-phase-router.py "mvp start rico readiness" --dry-run`

**Rollback**

- Revert ciblé des prompts et de la matrice.

## Run 5 — Routeur leger et documentation vivante

**But** : rendre le protocole decouvrable sans gonfler `CONTEXT.md`.

**Fichiers cibles**

- `docs/CONTEXT.md`
- `docs/PROJECT_MODE.md` uniquement si une mention est strictement necessaire ; par defaut, ne pas modifier.
- `docs/AUDIT_STATUS.md`

**Actions**

1. Dans `docs/CONTEXT.md` :
   - ajouter une ligne courte dans `Identity` ou `Structural artifacts` : nouveau projet/MVP from zero -> `MVP_START_PROTOCOL.md`.
   - ajouter un open point ou next action uniquement si le chantier n'est pas fini.
2. Dans `docs/AUDIT_STATUS.md` :
   - mettre a jour la note MVP start de `PARTIAL` vers le statut reel du chantier ;
   - ajouter le risque residual si un arbitrage reste ouvert.
3. Ne pas transformer `CONTEXT.md` en protocole narratif.

**Validation**

- `wc -l docs/CONTEXT.md` : verifier que le fichier reste court.
- `rg -n "MVP_START_PROTOCOL|MVP START|0-vbb-rico-readiness" docs/CONTEXT.md docs/AUDIT_STATUS.md`.

**Rollback**

- Retirer les lignes ajoutees.

## Run 6 — Harmonisation compteurs et narration publique

**But** : aligner README, guide, release/status et provider docs sur l'inventaire mesure.

**Fichiers cibles**

- `README.md`
- `GUIDE.md`
- `PROMPTS_ARCHITECTURE.md`
- `CLAUDE.md`
- `CHANGELOG.md`
- `RELEASE_CHECKLIST.md`
- `docs/INDEX.md`
- `docs/CONTEXT.md`
- `docs/AUDIT_STATUS.md`

**Actions**

1. Recalculer compteurs apres Runs 1-5 :
   - skills/contracts : probablement 63/63 ;
   - prompts : 33 si aucun prompt cree, 34 si prompt dedie ajoute.
2. Harmoniser toutes les occurrences actives :
   - `62 skills` -> `63 skills` ;
   - `62 contracts` -> `63 contracts` ;
   - prompt count selon inventaire ;
   - phase 0 count : `5` -> `6` si `0-vbb-rico-readiness` ajoute.
3. Corriger drift existant :
   - `CHANGELOG.md` 32 prompts -> 33 prompts dans rc.1, ou ajouter `Unreleased` selon decision ;
   - `CLAUDE.md` 32 prompts -> compteur reel.
4. Harmoniser la narration route :
   - "4 route families + MVP START gate" partout, ou variante choisie.
5. Ne pas modifier les artefacts historiques dans `docs/runs/` ou rapports immuables.

**Validation**

- `rg -n "62 skills|62 contracts|32 prompts|33 prompts|4 routes|v1.0.0-rc.1|v1.0 Hardening" README.md GUIDE.md PROMPTS_ARCHITECTURE.md CLAUDE.md CHANGELOG.md RELEASE_CHECKLIST.md docs/INDEX.md docs/CONTEXT.md docs/AUDIT_STATUS.md AGENTS.md SYSTEM.md`
- Recompter avec `find`.

**Rollback**

- Revert ciblé des docs publiques.

## Run 7 — Validation globale et closeout

**But** : verifier que l'integration fonctionne bout en bout et documenter l'etat final.

**Fichiers cibles**

- `docs/runs/<implementation-run>/06_REVIEW.md`
- `docs/runs/<implementation-run>/07_CLOSEOUT.md`
- `docs/AUDIT_STATUS.md`
- Optionnel : `docs/SESSION.md`

**Actions**

1. Lancer validations :
   - `python tools/vbb-contract-lint.py`
   - `python tools/vbb-contract-runtime.py --all --dry-run`
   - `python tools/vbb-phase-router.py "rico readiness mvp start" --dry-run`
   - `python tools/vbb-phase-router.py "no code before readiness" --dry-run`
   - `bash scripts/vbb-ci-local.sh`
2. Verifier compteurs :
   - `find skills -mindepth 1 -maxdepth 1 -type d | wc -l`
   - `find skills -mindepth 2 -maxdepth 2 -name CONTRACT.yaml | wc -l`
   - `find prompts -type f -name '*.md' | wc -l`
3. Verifier coherence documentaire cible :
   - aucun `32 prompts` actif restant ;
   - aucune mention active de 62 skills/contracts si 63 est l'inventaire reel ;
   - `MVP_START_PROTOCOL.md` reference depuis `CONTEXT`, `PILOTAGE`, router, prompts.
4. Produire closeout avec :
   - fichiers modifies ;
   - regles ajoutees ;
   - validations executees ;
   - dettes restantes.

**Sortie attendue**

- Contract lint PASS.
- Runtime dry-run attendu documente.
- Router RICO match `0-vbb-rico-readiness`.
- CI locale PASS ou failures documentees.
- Closeout complet.

**Rollback**

- Si contrat/router casse : rollback Run 2 et Run 4 en premier.
- Si incoherence documentaire seule : rollback Run 6 uniquement.
- Si protocole canonique pose probleme : rollback Run 3 puis Run 1.

## Run optionnel A — Prompt dedie MVP Start

**Condition d'activation** : si l'on veut une commande/session explicite `0-p-vbb-mvp-start.md`.

**Fichiers cibles**

- `prompts/0-p-vbb-mvp-start.md`
- `PROMPTS_ARCHITECTURE.md`
- `README.md`
- `docs/router/ROUTER_MATRIX.md`
- `prompts/t-p-vbb-phase-router.md`

**Effet compteur**

- Prompts : 34.

**Critere de decision**

- Activer seulement si l'experience multi-agent exige un prompt d'entree distinct du skill. Sinon, eviter un artefact supplementaire.

## Definition of Done globale

- [ ] `docs/MVP_START_PROTOCOL.md` existe et couvre les 5 sections demandees.
- [ ] `0-vbb-rico-readiness` existe avec `SKILL.md` + `CONTRACT.yaml`.
- [ ] `skills/INDEX.yaml` indexe le nouveau skill.
- [ ] Router executable trouve `0-vbb-rico-readiness` pour RICO/MVP/readiness.
- [ ] `docs/CONTEXT.md` pointe vers le protocole sans devenir narratif.
- [ ] `docs/PILOTAGE.md` et `docs/AGENTIC_RUN_PROTOCOL.md` bloquent le code avant readiness.
- [ ] Prompts et router documentaire ne contournent pas le gate.
- [ ] Compteurs harmonises partout dans les docs actives.
- [ ] Contract lint PASS.
- [ ] Runtime dry-run execute et resultat documente.
- [ ] CI locale executee et resultat documente.
- [ ] Closeout final produit.

## Risques identifies

- **Risque 1 — Integration narrative seulement** : mitiger en validant router executable apres Run 2 et Run 4.
- **Risque 2 — Inflation documentaire** : mitiger en gardant `CONTEXT.md` minimal et en centralisant le detail dans `MVP_START_PROTOCOL.md`.
- **Risque 3 — Compteurs divergents apres ajout** : mitiger par Run 6 dedie et verification `rg`.
- **Risque 4 — Confusion scope/architecture** : mitiger dans `MVP_START_PROTOCOL.md` et `AGENTIC_RUN_PROTOCOL.md`.
- **Risque 5 — Prompt dedie inutile** : garder le prompt dedie optionnel.

## Handoff vers `05_EXECUTION`

- **Premiere action concrete** : executer Run 0, puis Run 1.
- **Points de vigilance** :
  - Ne pas commencer par les compteurs ; ils dependent de la decision prompt et du nouveau skill.
  - Ne pas modifier `PROJECT_MODE.md` sauf raison explicite.
  - Ne pas patcher les rapports historiques pour corriger des anciens compteurs.
