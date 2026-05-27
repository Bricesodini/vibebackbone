---
run_id: "2026-05-27_2142_mvp-start-readiness-audit"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "codex"
started_at: "2026-05-27T19:50:00Z"
ended_at: "2026-05-27T20:05:00Z"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "README.md"
  - "GUIDE.md"
  - "PROMPTS_ARCHITECTURE.md"
  - "CHANGELOG.md"
  - "RELEASE_CHECKLIST.md"
  - "CLAUDE.md"
  - "skills/INDEX.yaml"
  - "tools/vbb-phase-router.py"
artifacts_produced:
  - "02_AUDIT.md"
  - "docs/audits/mvp-start-readiness-20260527-2142.md"
---

# 02_AUDIT — MVP Start Readiness Integration

## Perimetre audite

Audit pre-implementation de la consigne "MVP Start Protocol + Readiness Gate + Harmonisation documentaire". Le run reste en lecture seule vis-a-vis des fichiers cibles ; seuls les artefacts d'audit sont produits.

## Methode

- Lecture des fichiers de gouvernance actifs : `CONTEXT`, `PILOTAGE`, `PROJECT_MODE`, `SESSION`, `AUDIT_STATUS`.
- Lecture des docs de navigation et de narration : `README`, `GUIDE`, `PROMPTS_ARCHITECTURE`, `CHANGELOG`, `RELEASE_CHECKLIST`, `CLAUDE`.
- Lecture des surfaces de routage : `prompts/t-p-vbb-phase-router.md`, `docs/router/ROUTER_MATRIX.md`, `tools/vbb-phase-router.py`, `skills/INDEX.yaml`.
- Mesures locales :
  - `find skills -mindepth 1 -maxdepth 1 -type d | wc -l` -> 62
  - `find skills -mindepth 2 -maxdepth 2 -name CONTRACT.yaml | wc -l` -> 62
  - `find prompts -type f -name '*.md' | wc -l` -> 33
  - `python tools/vbb-phase-router.py "rico readiness mvp start" --dry-run` -> no matching contracts
  - `python tools/vbb-contract-lint.py` -> 0 error

## Findings

| # | Dimension | Severite | Evidence | Verdict |
|---|-----------|----------|----------|---------|
| 1 | Route MVP absente | `HIGH` | `docs/PILOTAGE.md:13-22` liste les routes actuelles sans entree MVP START ; `prompts/t-p-vbb-phase-router.md:9-15` ne route pas le demarrage MVP. | La consigne exige une nouvelle route ou equivalent ; l'etat actuel ne peut pas bloquer explicitement un projet from-zero incomplet. |
| 2 | Readiness gate non canonique | `HIGH` | `docs/AGENTIC_RUN_PROTOCOL.md:22-32` decrit 01..07 sans phase explicite de readiness ; `docs/AGENTIC_RUN_PROTOCOL.md:47-54` ne prevoit pas de sortie bloquante "no code before readiness". | Le protocole actuel encadre les phases, mais n'a pas de gate MVP pre-execution formel. |
| 3 | Router executable incapable de detecter RICO/MVP start | `HIGH` | `tools/vbb-phase-router.py` route uniquement via `skills/INDEX.yaml` + `routing.triggers`; la commande `python tools/vbb-phase-router.py "rico readiness mvp start" --dry-run` retourne "No matching contracts found." | Le nouveau skill doit etre indexe avec triggers explicites, sinon l'integration restera seulement documentaire. |
| 4 | Point d'entree de demarrage projet incomplet | `MEDIUM` | `docs/CONTEXT.md:37-44` pointe vers `docs/`, `skills/`, `prompts/`, mais pas vers un protocole MVP ; `docs/INDEX.md` n'a pas d'entree MVP start. | `CONTEXT.md` peut rester leger, mais doit pointer vers `MVP_START_PROTOCOL.md` et clarifier le passage obligatoire avant code. |
| 5 | Distinction cadrage / architecture absente | `MEDIUM` | `README.md:46-51` presente les docs de pilotage sans distinguer cahier des charges, architecture et etat projet ; `docs/AGENTIC_RUN_PROTOCOL.md:56-66` passe de PLAN vers EXECUTION sans condition architecture/cadrage. | La consigne demande de clarifier que `ARCHITECTURE.md` est produit apres readiness et ne contient pas le cadrage brut. |
| 6 | Compteurs actifs globalement coherents, mais fragiles apres ajout | `MEDIUM` | Mesures locales : 62 skills, 62 contracts, 33 prompts. `README.md:4`, `README.md:35`, `docs/CONTEXT.md:43-44`, `docs/INDEX.md` sont alignes sur 62/33. | L'ajout de `0-vbb-rico-readiness` imposera 63 skills/63 contracts. Un prompt dedie imposerait 34 prompts ; sinon rester a 33. |
| 7 | Incoherences documentaires existantes | `HIGH` | `CHANGELOG.md:13` annonce 32 prompts alors que les mesures et `README.md:4` annoncent 33 ; `CLAUDE.md:5` et `CLAUDE.md:22` annoncent 32 prompts. `CHANGELOG.md:22` annonce "4 agentic routes" mais enumere FAST-ZERO, FAST-MINIMAL, FAST-STANDARD, STRUCTURED, AUDIT, CLOSEOUT. | Il existe deja des divergences de compteurs et de narration avant l'implementation. |
| 8 | Etat rc/v1 ambigu mais explicable | `MEDIUM` | `docs/CONTEXT.md:24-30` indique v1.0 hardening complete, version 1.0.0-rc.1 et next action tag v1.0.0 ; `CHANGELOG.md:8` est rc.1 ; `RELEASE_CHECKLIST.md:1-3` est checklist v1.0 pour 1.0.0-rc.1. | La narration release doit etre harmonisee : rc.1 pret pour tag v1.0.0, pas v1 final deja publie. |
| 9 | Prompt before-building proche mais insuffisant | `MEDIUM` | `prompts/0-p-vbb-before-building.md` impose scope, architecture, anti-slop et intent, mais autorise `READY_WITH_CAVEATS` et ne couvre pas les champs RICO minimaux demandes. | Peut etre reutilise ou remplace, mais ne suffit pas comme protocole MVP Start canonique. |
| 10 | Skill existants partiellement recouvrants | `INFO` | `0-vbb-scope-freeze` valide scope/non-goals/boundaries ; `0-vbb-audit-readiness` valide audibilite ; `1-vbb-intent-decomposer` decompose une spec. | `0-vbb-rico-readiness` doit combiner brief produit, readiness de construction et questions bloquantes sans dupliquer les audits de fond. |

## Verdict global

- **Statut** : `PARTIAL`
- **Justification** : l'integration est faisable avec un perimetre clair, mais le depot contient deja des divergences de compteurs/statuts et ne possede pas encore de gate canonique "no code before readiness". Le risque principal est une integration seulement narrative, non connectee au routeur executable, aux contrats et aux prompts.

## Manques d'evidence / UNKNOWN

- Decision ouverte : creer un nouveau prompt specialise `0-p-vbb-mvp-start.md` ou integrer MVP START dans `0-p-vbb-before-building.md` et le router existant.
- Decision ouverte : le compteur public doit-il afficher "5 routes" ou conserver "4 routes" avec MVP START comme sous-route de STRUCTURED. La consigne accepte "route MVP START ou equivalent", mais le langage public devra etre unique.
- Non execute dans ce run : `vbb-contract-runtime.py --all --dry-run` et CI locale complete, reserves a l'apres-implementation.

## Recommandations

1. Creer `docs/MVP_START_PROTOCOL.md` comme document canonique, court mais complet : philosophie, RICO minimal, questions bloquantes, invariants architecture, autorisation de codage.
2. Modifier `docs/CONTEXT.md` uniquement comme routeur leger : ajouter une reference obligatoire au protocole et une ligne "new project from zero -> MVP_START_PROTOCOL before implementation".
3. Modifier `docs/PILOTAGE.md`, `prompts/t-p-vbb-phase-router.md` et `docs/router/ROUTER_MATRIX.md` avec une route MVP START ou une sous-route explicite bloquante.
4. Modifier `docs/AGENTIC_RUN_PROTOCOL.md` pour ajouter le gate readiness avant 05_EXECUTION et les escalades : ambiguite critique -> questions ; architecture non definie -> pas de code ; donnees non modelisees -> pas de persistence.
5. Creer `skills/0-vbb-rico-readiness/SKILL.md` et `CONTRACT.yaml` v0.3, puis l'ajouter a `skills/INDEX.yaml`.
6. Ajouter les triggers contractuels : `rico`, `mvp start`, `readiness`, `brief initial`, `no code before readiness`, `questions bloquantes`, `cahier des charges`.
7. Harmoniser les compteurs apres ajout : probablement 63 skills / 63 contracts / 33 ou 34 prompts selon decision prompt.
8. Corriger les divergences actuelles : `CHANGELOG.md` 32 -> 33 prompts, `CLAUDE.md` 32 -> 33 prompts, formulation "4 routes" incoherente avec les sous-routes FAST.
9. Ne pas modifier les rapports historiques de `docs/runs/` et `docs/audits/` sauf index/etat vivant ; les traiter comme evidence historique.
10. Apres patch, executer : contract lint, runtime dry-run, CI locale, test router cible, mesure compteurs skills/contracts/prompts.

## Handoff vers `03_DECISION`

- **Decisions a arbitrer** :
  - MVP START comme 5e route publique ou comme route de demarrage equivalent rattachee a STRUCTURED.
  - Creation ou non d'un prompt specialise dedie.
  - Mise a jour du CHANGELOG historique rc.1 vs ajout d'une section Unreleased.
- **Points de vigilance** :
  - Ne pas commencer l'execution applicative dans les prompts si RICO readiness est BLOCKED.
  - Maintenir `CONTEXT.md` comme pointeur, pas comme protocole.
  - Synchroniser Markdown, contrat et routeur executable dans la meme sequence.
