# VIBEBACKBONE_AGENTIC_AUDIT

**Cible** : système `vibebackbone` (catalogue de distribution)  
**Date** : 2026-05-18  
**Auditeur** : Strategic Auditor  
**Méthode** : inspection read-only du dépôt + comparaison à un modèle agentique canonique  

---

## 1. Résumé exécutif

`vibebackbone` est un catalogue sophistiqué de 57 skills et 24 prompts définissant une grammaire opérationnelle pour agents LLM. Il dispose d'une hiérarchie documentaire claire (AGENTS.md, SYSTEM.md, PILOTAGE.md interne), d'un triage en 4 voies (rapide, structurée, audit, clôture) et d'une logique de frontmatter standardisée (0-vbb-standard). Les skills codent des rôles séparés (audit vs planification vs exécution) avec interdictions explicites.

Cependant, le système reste un **catalogue de prompts**, pas un moteur d'exécution agentique. Il n'existe pas : d'orchestration programmable, de numérotation de runs, d'artefacts de transition obligatoires entre phases, de mémoire persistante dans le repo, ni de séparation matérielle entre audit et exécution (un même agent lit le skill et exécute). Le `docs/PILOTAGE.md` racine, référencé comme #1 dans la hiérarchie canonique, est absent. La compatibilité multi-LLM repose sur l'injection manuelle de fichiers, non sur un protocole universel. Le système prétend à la traçabilité mais ses artefacts de session sont `gitignore`d.

---

## 2. Cartographie du système actuel

### Fichiers identifiés

| Fichier | Rôle | Statut |
|---------|------|--------|
| `AGENTS.md` | Grammaire opérationnelle canonique (triage, rituels, discipline) | ✅ Existe, versionné |
| `SYSTEM.md` | Comportement runtime Pi (onboarding, artifact grounding, risk discipline) | ✅ Existe, versionné |
| `README.md` | Marketing + installation + description provider | ✅ Existe |
| `CLAUDE.md` | Point d'entrée Claude Code | ✅ Existe |
| `skills/vibebackbone/docs/PILOTAGE.md` | Source de vérité opérationnelle (voies, règles de triage, cascade verdict × env) | ✅ Existe (MAIS pas à la racine) |
| `skills/vibebackbone/SKILL.md` | Orchestrateur (routing uniquement) | ✅ Existe |
| `skills/0-vbb-standard/SKILL.md` | Contrat canonique des skills (frontmatter, sections, verdicts) | ✅ Existe |
| `skills/0-vbb-pilotage/SKILL.md` | Miroir explicatif du pilotage | ✅ Existe |
| `docs/PROJECT_MODE.md` | Signal de mode du repo (DISTRIBUTION) | ✅ Existe, versionné |
| `docs/SESSION.md` | Mémoire de reprise | ✅ Existe, **gitignoré** |
| `docs/AUDIT_STATUS.md` | Tableau de bord d'audit | ✅ Existe, **gitignoré** |
| `docs/PILOTAGE.md` (racine) | Référence opérationnelle canonique #1 | ❌ **ABSENT** |
| `prompts/` | 24 templates de session | ✅ Existent |
| `setup.sh` | Script d'installation cross-provider | ✅ Existe |
| `package.json` | Déclaration pi-package | ✅ Existe |
| `.pi/taskplane.json` | Config taskplane | ✅ Existe (local) |

### Rôles existants (encodés dans les skills)

| Rôle | Skill représentatif | Nature |
|------|---------------------|--------|
| Triage / Orchestration | `vibebackbone`, `0-vbb-pilotage` | Lecture seule / routing |
| Audit (sécurité) | `2-vbb-security` | Lecture seule |
| Audit (structure) | `1-vbb-code-janitor`, `1-vbb-tech-debt` | Lecture seule (rapport uniquement) |
| Audit (risques) | `3-vbb-risk-register` | Consolidation read-only |
| Planification | `1-vbb-intent-decomposer` | Lecture seule (plan uniquement) |
| Exécution (docs) | `t-vbb-project-context-init` | Écriture scaffold |
| Exécution (Docker) | `t-vbb-docker-generate` | Écriture artefacts |
| Clôture | `t-vbb-session-handoff` | Écriture SESSION.md |
| Garde-fou | `t-vbb-anti-slop-gate` | Exécution outils read-only |

### Prompts existants

24 prompts répartis en phases (0, 1, 2, 3, 4, t). Ce sont des points d'entrée de session, pas des scripts exécutables. Exemples : `0-p-vbb-triage.md`, `2-p-vbb-audit-task.md`, `t-p-vbb-session-handoff.md`.

### Scripts existants

| Script | Rôle |
|--------|------|
| `setup.sh` | Installe skills/prompts/gouvernance dans les répertoires provider respectifs (symlinks) |
| `.github/workflows/smoke.yml` | CI minimale (smoke test) |

### Conventions existantes

- Frontmatter SKILL.md standardisé (name, description, version, phase, token_budget, subagent_eligible, mode_sensitive)
- Verdicts normalisés : `READY`, `PARTIAL`, `BLOCKED`, `UNKNOWN`
- Hiérarchie documentaire : §2 AGENTS.md
- Taxonomie des phases : [0] readiness, [1] structure, [2] audits de fond, [3] consolidation, [4] front, [t] transverse

### Flux actuel supposé

```
Tâche entrante
  → Agent lit AGENTS.md + SYSTEM.md
  → Applique triage (4 voies)
  → Lit skill correspondant
  → Exécute selon le skill
  → Produit rapport dans docs/audits/
  → Met à jour docs/AUDIT_STATUS.md
  → En fin de session : met à jour docs/SESSION.md
```

---

## 3. Forces actuelles

1. **Standardisation du contrat skill** : frontmatter uniforme, sections obligatoires (INPUT CONTRACT, BLOCKING CONDITIONS, SCOPE, PROCESS, OUTPUT CONTRACT, VERDICT RULES). C'est un socle solide pour l'interopérabilité.
2. **Séparation des intentions dans les skills** : la plupart des skills audit sont strictement read-only avec interdictions explicites (NO code modification, NO implementation).
3. **Triage en 4 voies** : simple, mémorisable, applicable par tout LLM discipliné.
4. **Règle d'escalade explicite** : une tâche rapide qui découvre un risque doit changer de voie.
5. **Cascades de verdicts** : la règle `verdict × environnement` (READY/PARTIAL/BLOCKED/UNKNOWN × dev/staging/prod) est rarement vue dans des catalogues de prompts et constitue un garde-fou réel.
6. **Support multi-provider** : Claude, Codex, Pi, OpenCode sont tous couverts via setup.sh.
7. **Discipline de contexte LLM** : les règles de compaction et de chargement ciblé (§12 AGENTS.md) sont bien pensées pour les modèles locaux.
8. **SUPPORT BOUNDARY** : l'introduction explicite de "supporté / non supporté" dans certains skills est un garde-fou contre le scope creep.

---

## 4. Faiblesses et risques

### 🔴 Critique

| ID | Faiblesse | Preuve / Impact |
|----|-----------|-----------------|
| C-01 | **`docs/PILOTAGE.md` racine absent** alors que `AGENTS.md` §2 le référence comme priorité #1 | Un nouvel agent qui suit strictement la hiérarchie ne trouve pas le fichier attendu. Cela crée une contradiction documentaire et fragilise l'onboarding. |
| C-02 | **Aucune séparation matérielle entre audit et exécution** | Le même agent lit `2-vbb-security` puis, dans la même session, peut passer à l'implémentation sans changement de contexte LLM. Il n'y a pas de "barrière" artifactuelle obligatoire. |
| C-03 | **SESSION.md et AUDIT_STATUS.md sont gitignorés** | La mémoire de session et l'état d'audit sont éphémères par défaut. La traçabilité revendiquée repose sur des fichiers qui ne survivent pas au clone. |
| C-04 | **Pas de formalisation des runs** | Aucun artefact `04_FIX_PLAN.md`, `05_PATCH_SUMMARY_RUN_1.md`, `06_REVIEW_RUN_1.md`. Un agent peut corriger, re-auditer, corriger à nouveau dans une même session sans artefact intermédiaire. |
| C-05 | **Pas de phase DECISION dédiée** | Il n'existe pas de skill `decision-record` obligatoire entre l'audit et le plan. L'agent est censé "décider" implicitement, sans artefact de décision documenté. |

### 🟠 Haute

| ID | Faiblesse | Preuve / Impact |
|----|-----------|-----------------|
| H-01 | **Aucune orchestration programmable** (`vbb audit`, `vbb plan`, etc. sont absents) | Le système est un catalogue de textes. Aucun outil ne contrôle les transitions. L'agent doit tout décider à chaque session. |
| H-02 | **Aucun registre d'artefacts** | Il n'existe pas d'index des artefacts produits. L'agent doit deviner ce qui existe dans `docs/audits/` sans contrainte de nommage figé. |
| H-03 | **Les skills d'exécution peuvent être audit et exécution en même temps** | `t-vbb-project-context-init` écrit des fichiers et met à jour la gouvernance. Un agent pourrait "auditer" puis "exécuter" dans le même contexte sans notification. |
| H-04 | **Pas de critère de fin explicite pour une session** | Rien ne dit "stop, produis le handoff maintenant". La limite est contextuelle (token budget) ou temporelle, pas fonctionnelle. |
| H-05 | **Pas de numérotation ou d'identifiant de run** | Impossible de reconstruire la séquence exacte des actions d'une session à l'autre sans lire tout l'historique conversationnel. |

### 🟡 Moyenne

| ID | Faiblessse | Preuve / Impact |
|----|-----------|-----------------|
| M-01 | **Les rapports d'audit horizon-datés** (`{YYYYMMDD-HHMM}`) ne sont pas reconnus par un index automatique | L'agent doit lister `docs/audits/` manuellement. Aucun fichier `AUDIT_INDEX.md` ou équivalent. |
| M-02 | **Phase [3] sous-dimensionnée** | Un seul skill (`3-vbb-risk-register`) pour toute la consolidation. Pas de skill de `decision-record`, pas de `closeout`. |
| M-03 | **Prompts et skills sont décorrélés** | Les prompts dans `prompts/` référencent des skills, mais il n'y a pas de vérification automatique que le skill cité existe dans `skills/`. |
| M-04 | **La compatibilité multi-LLM est revendiquée mais non garantie** | Claude Code n'a pas de discovery de skills ; il faut compiler manuellement. Pi a la meilleure intégration. Un agent Qwen local n'a aucun mécanisme structurel pour charger les skills. |
| M-05 | **Nommage hétérogène des skills transverse** : `t-p-vbb-*` vs `t-vbb-*` | Certains transverses commencent par `t-p-vbb-` (si liés à un prompt) et d'autres par `t-vbb-`. Cette dualité de préfixe n'est pas expliquée dans le standard. |

### 🟢 Faible

| ID | Faiblesse | Preuve |
|----|-----------|--------|
| L-01 | Pas de `CONVENTIONS.md` racine pour le dépôt lui-même | Le skill `1-vbb-conventions` est destiné aux projets cibles, pas au catalogue. |
| L-02 | Quelques `.DS_Store` versionnés ou non ignorés proprement | `docs/.DS_Store` visible dans l'arborescence. |
| L-03 | Versionning non imposé techniquement (déjà noté dans AUDIT_STATUS.md) | Les versions sont dans le frontmatter mais non vérifiées automatiquement. |

---

## 5. Analyse du fonctionnement agentique

### Séparation des rôles

- **Read-only vs write** : Bien codée dans les skills (la plupart des skills phase 2 sont explicitement read-only). Cependant, la séparation dépend de la discipline du LLM : il n'y a pas de sandbox, de permission file-system, ou de changement de rôle matériel.
- **Audit vs plan vs exécution** : Théoriquement séparés (phase 2 = audit, phase 1 = plan/structure, t- = exécution). En pratique, un agent qui charge le contexte de plusieurs skills successifs peut tout faire dans la même session.
- **Review indépendante** : **Absente**. Il n'existe pas de skill de "review d'un patch" séparé de l'exécution. Le seul `2-vbb-spec-validator` est un audit post-implémentation, pas une review indépendante d'un run.

### Gestion du contexte

- **Dépendance au contexte conversationnel** : **ÉLEVÉE**. L'agent doit se souvenir de toute la session pour savoir où il en est. Il n'y a pas de "state machine" ou de fichier d'état `CURRENT_PHASE`.
- **Reconstructibilité** : Mauvaise. Sans lire l'historique conversationnel complet, on ne peut pas reconstruire la séquence exacte des actions. Les rapports d'audit horodatés sont dispersés et non indexés.
- **Handoff** : Existe (`t-vbb-session-handoff`) mais produit un `SESSION.md` **gitignoré**. Si l'utilisateur oublie de le committer, la reprise est perdue.
- **Sessions jetables** : **Implicite seulement**. Rien n'oblige à jeter une session après un rôle. L'agent peut continuer indéfiniment.

### Artefacts

- Les skills produisent des rapports dans `docs/audits/` et mettent à jour `docs/AUDIT_STATUS.md`.
- Il n'existe pas : d'artefact INTAKE, d'artefact DECISION, d'artefact FIX_PLAN, d'artefact PATCH_SUMMARY_RUN_N, d'artefact REVIEW_RUN_N, d'artefact CLOSEOUT.
- Le `SESSION.md` est le seul artefact de handoff, et il est éphémère.

### Orchestration

- **Absente**. L'orchestrateur (`vibebackbone/SKILL.md`) ne fait que du routing textuel : il dit quel skill utiliser, mais ne l'exécute pas, ne vérifie pas la sortie, ne passe pas automatiquement à l'étape suivante.
- Il n'existe pas de `vbb audit`, `vbb plan`, `vbb exec`, `vbb review`.
- L'orchestration est "par prompt" : l'utilisateur humain ou l'agent doit décider à chaque tour ce qui vient ensuite.

### Review

- **Pas de skill de review indépendante**. Aucun skill ne prend un patch produit et le valide formellement.
- `2-vbb-spec-validator` est un audit post-implémentation, pas une review de patch.
- Il n'y a pas de "second agent" prévu pour la review : c'est le même agent qui pourrait auto-valider.

### Compatibilité multi-LLM

| LLM | Mécanisme réel | Robustesse |
|-----|----------------|------------|
| **Pi** | Discovery via `skills/` + package.json. Meilleure intégration. | 🟢 Haute |
| **Claude Code** | `CLAUDE.md` + commandes `/vbb-*` + compilation manuelle dans `~/.claude/`. | 🟡 Moyenne — dépend de l'installation setup.sh |
| **Codex** | Bloc compilé `~/.codex/AGENTS.md` + prompts référencés. | 🟡 Moyenne — pas de skill discovery dynamique |
| **OpenCode** | `opencode.json` + commandes. | 🟡 Moyenne — injection manuelle |
| **Qwen / local** | Aucun mécanisme auto-découvrable. L'utilisateur doit copier-coller les prompts. | 🔴 Faible |

**Risque** : les modèles "moins disciplinés" (petits modèles locaux, modèles rapides) vont probablement ignorer les interdictions du SKILL.md et mélanger audit + exécution. Le système repose entièrement sur la "bonne volonté" du LLM.

---

## 6. Écart avec le fonctionnement agentique idéal

### Principe cible

```
1 session = 1 rôle = 1 intention = 1 sortie exploitable
```

### État actuel vs cible

| Critère idéal | État Vibebackbone actuel | Écart |
|---------------|--------------------------|-------|
| 1 session = 1 rôle | Non. Un agent peut enchaîner triage → audit → plan → exécution dans la même session. | **Grand** |
| Mémoire conversationnelle ≠ mémoire officielle | Partiel. AUDIT_STATUS.md et SESSION.md existent mais sont gitignorés. | **Moyen** |
| Artefacts = source de vérité | Faible. Les rapports d'audit horodatés le sont, mais les transitions (INTAKE, DECISION, PLAN) n'ont pas d'artefacts obligatoires. | **Grand** |
| Pas de sessions trop longues | Non encadré. Le token_budget du frontmatter est une indication, pas une limite dure. | **Moyen** |
| Pas d'audit+plan+correction dans le même flux | Non empêché. Le LLM peut tout faire si l'utilisateur le demande. | **Grand** |
| Handoffs propres | Existe (SESSION.md) mais éphémère. Pas de CLOSEOUT formel. | **Moyen** |
| Runs limités | Absent. Pas de numérotation de run. | **Grand** |
| Critères d'acceptation | Présents dans les skills (ACCEPTANCE) mais pas au niveau du run. | **Moyen** |
| Décisions documentées | Aucun skill de DECISION_RECORD obligatoire. | **Grand** |
| Reviews séparées | Absente. | **Critique** |
| Orchestration reproductible | Absente. | **Grand** |

### Pipeline idéal proposé

```
01_INTAKE
02_AUDIT
03_DECISION
04_PLAN
05_EXECUTION_RUN_N
06_REVIEW_RUN_N
07_CLOSEOUT
```

### Disponibilité dans Vibebackbone actuel

| Phase | Existe ? | Forme actuelle | Manque |
|-------|----------|----------------|--------|
| 01_INTAKE | ❌ Non | Implicite (début de session) | Skill/formalisation complète |
| 02_AUDIT | ✅ Oui | Skills phase 0 + phase 2 | Séparation matérielle, index des rapports |
| 03_DECISION | ⚠️ Partiel | Verdicts READY/PARTIAL/BLOCKED | Artefact DECISION_RECORD.md, skill dédié |
| 04_PLAN | ✅ Oui | `1-vbb-intent-decomposer` | Pas de règle "plan validé avant exécution" |
| 05_EXECUTION_RUN_N | ❌ Non | Les skills t- d'exécution | Numérotation, PATCH_SUMMARY_RUN_N.md |
| 06_REVIEW_RUN_N | ❌ Non | `2-vbb-spec-validator` (post-hoc) | Review indépendante pré-livraison |
| 07_CLOSEOUT | ⚠️ Partiel | `t-vbb-session-handoff` | CLOSEOUT.md formel, artefact obligatoire |

---

## 7. Préconisations d'orientation

### Niveau 1 — Corrections simples

| ID | Recommandation | Bénéfice | Coût | Risque | Fichiers | Priorité |
|----|---------------|----------|------|--------|----------|----------|
| N1-01 | Créer `docs/PILOTAGE.md` à la racine (copie ou symlink de `skills/vibebackbone/docs/PILOTAGE.md`) | Élimine la contradiction hiérarchique | 5 min | Zéro | `docs/PILOTAGE.md` | P0 |
| N1-02 | Décider si `SESSION.md` et `AUDIT_STATUS.md` doivent rester gitignorés ou être versionnés partiellement | Résout l'éphéméralité de la traçabilité | 10 min | Faible — risque de committer des états locaux | `.gitignore`, `docs/` | P0 |
| N1-03 | Créer un `docs/INDEX.md` ou `docs/audits/INDEX.md` listant les rapports existants | Facilite la reprise par un nouvel agent | 15 min | Zéro | `docs/INDEX.md` | P1 |
| N1-04 | Normaliser le préfixe des transverses (`t-vbb-*` uniforme, supprimer `t-p-vbb-*`) | Réduit la confusion de nommage | 20 min | Faible — breaking pour les utilisateurs qui référencent les anciens noms | `prompts/*`, skills concernés | P2 |

### Niveau 2 — Restructuration modérée

| ID | Recommandation | Bénéfice | Coût | Risque | Fichiers/Zones | Priorité |
|----|---------------|----------|------|--------|----------------|----------|
| N2-01 | Créer un skill `1-vbb-decision-record` (ou `3-vbb-decision-record`) produisant un artefact DECISION_RECORD.md obligatoire entre audit et plan | Force la documentation explicite des arbitrages | 1h | Moyen — ajoute une étape que certains utilisateurs pourraient trouver lourde | `skills/3-vbb-decision-record/` | P1 |
| N2-02 | Introduire un skill `t-vbb-review-runner` (review indépendante) prenant en entrée un PATCH_SUMMARY et produisant un REVIEW_RUN_N.md | Sépare matériellement l'exécution de la validation | 2h | Moyen — nécessite de formaliser le format de PATCH_SUMMARY | `skills/t-vbb-review-runner/` | P1 |
| N2-03 | Formaliser la numérotation des runs dans `docs/SESSION.md` (Run N, Wave N) | Permet de reconstruire la séquence sans lire le contexte conversationnel | 30 min | Faible | `t-vbb-session-handoff/SKILL.md`, `SESSION.md` template | P1 |
| N2-04 | Ajouter un `docs/RUNS/` ou `docs/runs/` avec un fichier par run (`run-001.md`, `run-002.md`) indexant les patchs et reviews | Devient la mémoire officielle persistante | 45 min | Faible — à ne pas gitignore | `docs/RUNS/`, skills concernés | P2 |
| N2-05 | Créer un skill `0-vbb-intake` formalisant la capture du besoin initial avec un artefact `01_INTAKE.md` | Empêche les sessions de démarrer sans scope explicite | 1h | Moyen — ajoute friction en début de session | `skills/0-vbb-intake/` | P2 |

### Niveau 3 — Évolution structurante

| ID | Recommandation | Bénéfice | Coût | Risque | Fichiers/Zones | Priorité |
|----|---------------|----------|------|--------|----------------|----------|
| N3-01 | Définir un format standard obligatoire pour les artefacts de transition (INTAKE, AUDIT, DECISION, PLAN, PATCH_SUMMARY_RUN_N, REVIEW_RUN_N, CLOSEOUT) avec schéma markdown figé | Rend les artefacts exploitables par des agents sans compréhension conversationnelle | 3h | Moyen — nécessite mise à jour de tous les skills | `0-vbb-standard/SKILL.md`, tous les skills de sortie | P1 |
| N3-02 | Créer un artefact `CURRENT_PHASE.md` ou `STATE.json` dans le repo cible que chaque skill peut lire/écrire pour savoir où il en est | Permet une orchestration à états sans dépendre du contexte conversationnel | 2h | Moyen — format à stabiliser, risque de conflit si deux agents écrivent en parallèle | Nouveau fichier, tous les skills | P2 |
| N3-03 | Rendre `AUDIT_STATUS.md` versionné (partiel) — par exemple via un template commitable et un `.local` gitignoré | Donne une traçabilité persistante sans exposer les états locaux | 45 min | Faible | `docs/AUDIT_STATUS.md`, `.gitignore` | P2 |
| N3-04 | Introduire un `vbb` CLI minimal (même en bash) capable d'écrire/lire le STATE et de valider la présence des artefacts obligatoires | Donne une orchestration programmable concrète | 1-2 jours | Moyen — nouveau langage de script à maintenir | `bin/vbb` ou `cli/` | P3 |

### Niveau 4 — Refonte agentique majeure

| ID | Recommandation | Bénéfice | Coût | Risque | Fichiers/Zones | Priorité |
|----|---------------|----------|------|--------|----------------|----------|
| N4-01 | Transformer `vibebackbone` d'un catalogue de prompts en un **moteur d'exécution agentique** avec orchestration programmable et validation des transitions | Le système devient vraiment reproductible, multi-LLM et traçable sans effort humain | Semaines | Haut — refonte complète du paradigme, incompatible avec l'approche actuelle "texte pur" | Tout le repo | P4 (vision) |
| N4-02 | Implémenter des "agents spécialisés matériels" (via subagent/pi-subagents) où chaque phase est confiée à une instance LLM distincte avec contexte frais | Assure réellement `1 session = 1 rôle` | Semaines | Haut — coût d'inférence, complexité d'orchestration | `agents/`, `orchestrator/` | P4 (vision) |

---

## 8. Modèle cible recommandé

### Agents

| Agent | Rôle | Interdictions | Artefacts produits |
|-------|------|-------------|-------------------|
| Intake Agent | Formaliser le besoin et le scope | Ne planifie pas, n'audit pas | `01_INTAKE.md` |
| Audit Agent | Analyser, ne pas corriger | Ne modifie pas le code, ne planifie pas d'implémentation | `02_AUDIT_REPORT.md` |
| Decision Agent | Documenter les arbitrages pris suite à l'audit | N'implémente pas, ne planifie pas seul | `03_DECISION_RECORD.md` |
| Plan Agent | Transformer la décision en plan technique exécutable | N'implémente pas, ne valide pas | `04_FIX_PLAN.md` |
| Execution Agent N | Implémenter le plan du Run N | N'audit pas, ne review pas son propre code | `05_PATCH_SUMMARY_RUN_N.md` |
| Review Agent N | Valider le patch du Run N indépendamment | Ne corrige pas, ne ré-implémente pas | `06_REVIEW_RUN_N.md` |
| Closeout Agent | Archiver, handoff, et mise à jour de l'état projet | N'introduit pas de nouvelle fonctionnalité | `07_CLOSEOUT.md` + `SESSION.md` |

### Phases

```
01_INTAKE    → scope explicite, non-goals, signal de départ
02_AUDIT     → analyse read-only, verdict, risques identifiés
03_DECISION  → arbitrage humain validé ou auto-arbitrage documenté
04_PLAN      → décomposition en tâches, vagues, dépendances
05_EXECUTION → implémentation par runs numérotés
06_REVIEW    → validation indépendante par run
07_CLOSEOUT  → handoff, mise à jour de l'état, archive des artefacts
```

### Artefacts obligatoires

| Artefact | Quand | Contenu |
|----------|-------|---------|
| `01_INTAKE.md` | Après analyse du besoin | Scope, non-goals, hypothèses, agent assigné |
| `02_AUDIT_REPORT.md` | Après phase d'audit | Findings, risques, verdict |
| `03_DECISION_RECORD.md` | Après audit, avant plan | Ce qui est accepté, mitigué, différé et pourquoi |
| `04_FIX_PLAN.md` | Avant toute exécution | Tâches, vagues, fichiers concernés, critères d'acceptation |
| `05_PATCH_SUMMARY_RUN_N.md` | Après chaque run | Fichiers modifiés, décisions prises en cours, tests passés/échoués |
| `06_REVIEW_RUN_N.md` | Après chaque run | Validation externe du patch, écarts détectés, verdict GO/NO-GO |
| `07_CLOSEOUT.md` | En fin de session | Résumé, prochaine étape, points ouverts, artefacts produits |

### Règles de session

- **Règle fondamentale** : un agent ne peut jamais changer de rôle au cours d'une session. S'il a commencé comme Audit Agent, il termine comme Audit Agent.
- **Règle d'escalade temporelle** : un agent qui termine son rôle génère l'artefact attendu et s'arrête. L'orchestration (humaine ou programmée) lance la session suivante.
- **Règle de contexte minimal** : chaque agent démarre avec seulement les artefacts de la phase immédiatement précédente, jamais avec l'historique conversationnel complet.

### Règles de handoff

- Handoff = livraison des artefacts + `SESSION.md` + `docs/STATE.md` (si applicable).
- Le handoff n'est pas un récit : c'est une liste de faits et la prochaine action attendue.
- Si les artefacts obligatoires de la phase actuelle sont absents, le handoff est **invalide**.

### Règles de review

- Un patch exécuté par un agent doit être reviewé par un autre agent ou un humain **avant** merge.
- La review utilise le `05_PATCH_SUMMARY_RUN_N.md` comme unique source de vérité, pas le code directement (économie de contexte).
- Le verdict est `GO` (continuer), `GO_WITH_FIXES` (corrections définies dans le plan suivant), ou `NO-GO` (re-run obligatoire).

### Règles d'itération

- Un run échoué génère un `05_PATCH_SUMMARY_RUN_N_FAILED.md` et `06_REVIEW_RUN_N_FAILED.md`.
- La reprise se fait en re-partant du plan (`04_FIX_PLAN.md`) avec les échecs documentés.
- Jamais de correction hors scope dans un run : si un problème hors scope est découvert, il est ajouté à `01_INTAKE.md` comme nouvelle entrée future.

### Orchestration

- **Court terme** : orchestration par artefact (l'agent suivant lit les artefacts produits par le précédent).
- **Long terme** : orchestration par outil (`vbb state`, `vbb next`, `vbb validate`) vérifiant la présence des artefacts avant transition.

---

## 9. Roadmap recommandée

### Étape 1 — Stabiliser la vérité documentaire (semaine 1)
- Créer `docs/PILOTAGE.md` racine (N1-01)
- Trancher le statut de versionnement de SESSION.md / AUDIT_STATUS.md (N1-02)
- Créer `docs/INDEX.md` (N1-03)

### Étape 2 — Formaliser les transitions (semaine 1-2)
- Créer skill `0-vbb-intake` + artefact `01_INTAKE.md` (N2-05)
- Créer skill `3-vbb-decision-record` + artefact `03_DECISION_RECORD.md` (N2-01)
- Normaliser les formats de sortie obligatoires dans `0-vbb-standard` (N3-01)

### Étape 3 — Instaurer la review indépendante (semaine 2-3)
- Créer skill `t-vbb-review-runner` + artefact `06_REVIEW_RUN_N.md` (N2-02)
- Créer dossier `docs/RUNS/` et convention de numérotation (N2-04)
- Modifier `t-vbb-session-handoff` pour référencer les artefacts produits dans le closeout (N2-03)

### Étape 4 — Ajouter la machine à états (semaine 3-4)
- Introduire `CURRENT_PHASE.md` ou `STATE.json` (N3-02)
- Adapter les skills pour lire/écrire cet état
- Rendre AUDIT_STATUS.md partiellement versionné (N3-03)

### Étape 5 — Orchestration programmée (mois 2+)
- Concevoir le `vbb` CLI minimal (N3-04)
- Tester sur un projet consommateur pilote
- Itérer

### Étape 6 — Vision long terme (trimestre 2+)
- Évaluer la migration vers un moteur d'exécution agentique avec subagents matériels (N4-01 / N4-02)

---

## 10. Décisions à arbitrer par Brice

Ces décisions ne doivent pas être prises automatiquement par l'agent :

1. **Statut de versionnement de `SESSION.md` et `AUDIT_STATUS.md`** : restent-ils gitignorés ou deviennent-ils partiellement commitables ?
2. **Acceptation de la friction ajoutée par les artefacts obligatoires** : Brice accepte-t-il que chaque session produise désormais 1-2 artefacts formels supplémentaires ?
3. **Priorité de la review indépendante** : est-ce acceptable de multiplier le coût d'inférence (deux sessions LLM par run) pour la séparation des rôles ?
4. **Scope de `vibebackbone` comme "texte pur" vs "moteur exécutable"** : le catalogue doit-il rester un catalogue de prompts, ou évoluer vers un outil CLI avec états ?
5. **Compatibilité avec les petits modèles locaux** : faut-il dégrader volontairement certaines exigences pour rester utilisable sur Qwen/llama.cpp, ou maintenir l'exigence et accepter que certains environnements soient non supportés ?
6. **Gestion des runs échoués** : faut-il autoriser des runs "hotfix" dans la même session ou strictement forcer une nouvelle session avec agent frais ?
7. **Multi-sessions simultanées** : le système doit-il supporter deux agents travaillant sur le même repo en parallèle (risque de conflit sur CURRENT_PHASE.md) ?

---

## 11. Handoff

### Statut
Audit **terminé** — rapport produit, aucune modification apportée au dépôt.

### Artefact produit
- `VIBEBACKBONE_AGENTIC_AUDIT.md` (ce fichier)

### Prochaine session recommandée
- **Agent** : Brice (décision humaine) ou un agent de planification (Niveau 1)
- **Objectif** : Trancher les décisions §10, notamment D-01 (versionnement SESSION.md) et D-04 (texte pur vs moteur exécutable)
- **Entrées** : ce rapport
- **Sortie attendue** : décisions documentées sous forme d'ADR (`1-vbb-adr`) ou dans `docs/PILOTAGE.md`
- **Interdictions** : ne pas implémenter les niveaux 3 ou 4 sans validation des niveaux 1 et 2 ; ne pas modifier la structure des skills existants sans arbitrage sur le breaking change

### Points de vigilance
- Le risque C-01 (`docs/PILOTAGE.md` absent) est symbolique mais gênant pour tout nouvel agent canonique. À corriger en priorité.
- Le risque C-04 (pas d'artefacts de run) est le plus structurel : c'est lui qui empêche Vibebackbone de tenir sa promesse de traçabilité sans le contexte conversationnel.
- Le risque H-01 (pas d'orchestration programmable) est acceptable à court terme si les artefacts sont suffisamment formalisés (orchestration par artefact).
- Le modèle cible §8 est un cap, pas un mandat immédiat. Les niveaux 1 et 2 suffisent à améliorer significativement la maturité agentique sans refonte.

---

_Audit produit selon les critères : critique, précis, orienté système. Aucune recommandation générique sans ancrage dans le dépôt. Chaque préconisation est transformable en plan d'implémentation dans une session séparée._
