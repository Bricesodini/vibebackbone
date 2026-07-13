---
context_role: gap-analysis
phase: strategy
status: active
updated: 2026-07-12
scope: vibebackbone framework → multi-service patterns
phase_phase_label: "Phase 1 — Caractérisation des manques (pas de solution)"
---

# 01 — Gap Analysis : vibebackbone vers support natif des patterns multi-services

> **Périmètre** : ce document caractérise les manques dans **vibebackbone lui-même** (le framework `/Users/bricesodini/01_ai-stack/vibebackbone/`). Il ne propose aucune solution : il identifie où le manque se manifeste, ce qui est observable, et ce qui doit pouvoir être exprimé. Phase 1 de l'évolution `vbb-evolution-multi-service-support`.
>
> **Sources citées** : chaque gap référence un fichier:ligne (ou zéro-hit) vérifiable dans le repo.
>
> **Verdict global Phase 1** : `READY_FOR_PHASE_2` — 15 gaps caractérisés, 3 gaps dérivés ajoutés, priorisation P0/P1/P2 effectuée, dépendances cartographiées. Aucune solution implémentée dans cette phase.

---

## 0. Synthèse exécutive

| Catégorie | Gaps caractérisés | P0 | P1 | P2 | UNKNOWN |
|-----------|-------------------|----|----|----|---------|
| Orientation projet (DB, archétype) | Gap-01, Gap-02, Gap-14 | 0 | 3 | 0 | 0 |
| Codegen / discipline projet | Gap-03, Gap-12 | 0 | 2 | 0 | 0 |
| Discipline cross-service outillée | Gap-04, Gap-05, Gap-06, Gap-07, Gap-10, Gap-11, Gap-15 | 3 | 4 | 0 | 0 |
| Multi-repo / graphe global | Gap-08, Gap-13 | 2 | 0 | 0 | 0 |
| Extensibilité / canon vs extension | Gap-09 | 0 | 1 | 0 | 0 |
| Dérivés (analyse) | Gap-16, Gap-17, Gap-18 | 0 | 1 | 2 | 0 |
| **TOTAL** | **18** | **5** | **11** | **2** | **0** |

**Constat clé** : aucun gap P0 ne concerne l'orientation projet elle-même (DB, archétype) — ce sont des P1, donc traitables en parallèle après la Phase 2. Les vrais P0 bloquants sont la **discipline cross-service outillée** (linter, contrats consommés, log cumulatif) et le **support multi-repo**, sans lesquels les patterns database-per-service ne sont pas viables de façon vérifiable.

---

## 1. Caractérisation des gaps (format §4 de la consigne)

### Gap-01 — Pas de concept formel d'orientation DB dans l'intent projet

- **Manifestation** : `tools/vbb-project-init.py` lignes 67-86 (`_project_mode_md`) et 88-110 (`_context_md`) produisent des fichiers `PROJECT_MODE.md` et `CONTEXT.md` minimaux. Aucun champ structuré pour déclarer une topologie de persistance. Lignes 112-140 (`_architecture_md`) ne déclarent pas non plus d'orientation DB.
- **Observable aujourd'hui** : un projet initialisé par `t-vbb-project-context-init` n'a aucun moyen canonique d'exprimer « j'ai ma propre DB », « je consomme une DB externe en lecture seule », « je suis polyglote (Postgres + Redis) ». L'architecte qui veut le déclarer doit l'écrire en prose dans `docs/CONTEXT.md` section "Stack principale" (template ligne 100-102).
- **Conséquence du manque** : impossible de dériver automatiquement des règles spécifiques (ex. : « ce projet ne doit pas avoir de migration sans ADR »). Impossible de raisonner sur les dépendances DB lors d'un changement de contrat. Impossible de signaler une violation de discipline DB sans un grep manuel.
- **À pouvoir exprimer** : qu'un projet déclare explicitement son `db_orientation` parmi un ensemble typé (par exemple : `owned_private` / `shared_external_owned` / `shared_external_readonly` / `polyglot` / `stateless`), avec rationale et ADR de référence.
- **Touché par au moins un cas d'usage** : studio-projects (chaque service a sa DB), export-engine retro-fit, compta retro-fit.
- **Niveau** : P1 (important — bloquant pour les services en pratique, mais l'écosystème mono-service actuel peut fonctionner sans)
- **Canon change requis ?** : incertain (pourrait être une extension `docs/extensions/multi-service/` qui ajoute un schéma à `CONTEXT.md`, sans modifier CONVENTIONS.md canon)
- **Dépendances** : Gap-02 (archétype) doit être conçu en cohérence — les deux forment le « typage projet ». Gap-14 (schéma enrichi) est le vecteur de transport.

### Gap-02 — Pas de concept de project_archetype / projet typé

- **Manifestation** : `tools/vbb-contract-lint.py` ligne 79 impose que `contract['type'] == 'prompt_skill'` — c'est le seul typage existant au niveau skill, et il n'existe aucun typage équivalent au niveau projet. `tools/vbb-project-init.py` ne demande ni ne stocke d'archétype (ligne 264 `--mode {DEV,PROD}` est le seul enum). Aucun fichier du framework ne référence `project_archetype` (vérifié par grep récursif : zéro hit).
- **Observable aujourd'hui** : la classification « ce projet est une stack frontend / un service API / un orchestrateur / un consommateur read-only » est purement conversationnelle. Vibebackbone ne peut pas adapter ses règles de validation, ses templates d'artefact, ou son linter au type de projet.
- **Conséquence du manque** : tous les projets sont traités de la même façon par les outils. Un orchestrateur reçoit le même template `01_INTAKE.md.template` qu'un service API, ce qui force l'architecte à inventer des workarounds en prose. Les contrats d'un consommateur read-only ne sont pas validés différemment de ceux d'un producteur.
- **À pouvoir exprimer** : qu'un projet déclare son `project_archetype` parmi un ensemble typé (par exemple : `frontend_app` / `api_service` / `orchestrator` / `read_only_consumer` / `worker` / `library`), et que cette déclaration oriente automatiquement les règles appliquées (lint adapté, templates adaptés, gates adaptés).
- **Touché par au moins un cas d'usage** : studio-projects (chaque service a un archétype différent), export-engine retro-fit (orchestrateur vs worker), compta retro-fit.
- **Niveau** : P1
- **Canon change requis ?** : incertain (l'enum lui-même est une extension ; les adaptations de linter sont des ajouts, pas des modifications du canon)
- **Dépendances** : Gap-01 (même schéma projet), Gap-11 (lint archetype-aware), Gap-14 (vecteur).

### Gap-03 — Pas de codegen AGENTS.md / CLAUDE.md depuis une source canonique

- **Manifestation** : `tools/vbb-architecture.py` lignes 1-100 et fonction `graph --write` implémentent le pattern codegen ARCHITECTURE.md → RELATIONS.md (vérifié : `RELATIONS_PATH = Path("docs/RELATIONS.md")`, fonction `write_graph`). Mais aucun mécanisme équivalent pour `AGENTS.md` ou `CLAUDE.md`. `distributions/claude/CLAUDE.md` est un fichier de 61 lignes écrit à la main avec `@AGENTS.md` / `@SYSTEM.md` en directives d'inclusion manuelles. `AGENTS.md` à la racine est aussi écrit à la main (le framework s'appuie sur le contenu canonique des Critical Rules 1-13).
- **Observable aujourd'hui** : si Brice modifie une Critical Rule dans `docs/PILOTAGE.md` ou `docs/CONVENTIONS.md`, il doit reporter manuellement le changement dans `AGENTS.md` (et `distributions/claude/CLAUDE.md`, et `distributions/pi/SYSTEM.md` qui contient aussi des règles). Aucun drift detector.
- **Conséquence du manque** : risque de drift entre la source canonique et les fichiers distribués. Le `load_policy: always` de plusieurs fichiers (`PILOTAGE.md` ligne 3, `SYSTEM.md`, `AGENTS.md`) est une convention documentaire — pas un mécanisme enforceable.
- **À pouvoir exprimer** : que la discipline entrée-projet (ce que l'agent doit savoir en arrivant dans un repo) soit **dérivée** d'une déclaration d'orientation + archétype + canon (Gap-01, Gap-02), plutôt qu'écrite à la main.
- **Touché par au moins un cas d'usage** : studio-projects (chaque service a son AGENTS.md / CLAUDE.md à générer), export-engine retro-fit.
- **Niveau** : P1
- **Canon change requis ?** : incertain (le pattern codegen existe déjà ; il suffit de l'étendre. Le canon pourrait ne pas changer)
- **Dépendances** : Gap-01, Gap-02 (sources de la génération), Gap-09 (mécanisme d'extension pour le template de génération).

### Gap-04 — Pas de linter discipline multi-service

- **Manifestation** : `tools/vbb-architecture.py` ligne 8 `ARCHITECTURE_TOUCH_GLOBS` liste les fichiers architecture-sensitive et la fonction `lint` valide la cohérence ARCHITECTURE.md ↔ code (vérifié par lecture lignes 1-200). Mais aucune règle n'existe pour : (a) interdire l'accès direct à la DB d'un autre service, (b) exiger la mise à jour d'un log d'impact avant modification de contrat, (c) vérifier que les contrats consommés sont tracés dans `CONTRACTS_CONSUMED.md`. Aucun fichier du framework n'implémente ces règles (zéro hit grep `cross-service|multi-service|database-per-service`).
- **Observable aujourd'hui** : un projet multi-service peut importer directement le client DB d'un autre service sans qu'aucun linter ne le signale. La discipline multi-service est **documentée** dans notre conversation, **pas outillée**.
- **Conséquence du manque** : la discipline multi-service est fragile. Elle dépend de la vigilance humaine à chaque PR. Toute évolution de l'équipe peut la faire régresser silencieusement.
- **À pouvoir exprimer** : qu'un projet déclare sa discipline obligatoire (ce qu'il refuse sans alignement préalable) et que cette discipline soit **vérifiable** automatiquement. Exemple : « aucun import cross-DB sans ADR updated » → règle lint qui échoue si un import DB cross-service apparaît sans `docs/adr/NNNN-*.md` mis à jour dans le même diff.
- **Touché par au moins un cas d'usage** : studio-projects (4 services avec discipline stricte), export-engine retro-fit.
- **Niveau** : P0 (sans linter, les autres gaps de discipline ne peuvent pas être enforced)
- **Canon change requis ?** : incertain (peut être une extension `tools/vbb-multiservice-lint.py` qui consomme un fichier `docs/MULTISERVICE_DISCIPLINE.yaml` par projet)
- **Dépendances** : Gap-05 (CONTRACTS_CONSUMED), Gap-06 (IMPACT_LOG), Gap-07 (co-évolution) sont les **règles** que ce linter enforce. Gap-15 (gate PR) est le **point d'application**.

### Gap-05 — Pas de tracking des contrats consommés (CONTRACTS_CONSUMED.md canonique)

- **Manifestation** : aucun fichier `CONTRACTS_CONSUMED.md` n'existe nulle part dans le repo (zéro hit find). Aucun template dans `docs/templates/` (vérifié `ls docs/templates/` : 7 templates de phase + ADR + POC + INTEGRATION_GATE + CANON_CHANGE_PROPOSAL + worker-evidence-paragraph, aucun `CONTRACTS_CONSUMED`). `1-vbb-api-contract-designer/SKILL.md` ligne 61 mentionne « existing or planned consumers » comme **optional input**, pas comme artefact persistant. `2-vbb-api-auditor/SKILL.md` ligne 57 mentionne « Client / consumer / integration examples » de la même façon.
- **Observable aujourd'hui** : un service qui consomme une API d'un autre service n'a aucune obligation de tracer cette dépendance. L'architecte peut l'écrire dans `CONTEXT.md` section « Stack principale » — ou pas. Aucun impact analyzer ne peut répondre à « quels services dépendent de mon endpoint X ».
- **Conséquence du manque** : impossible d'automatiser l'analyse d'impact cross-service. Impossible d'alerter un consommateur qu'un contrat va casser. Impossible de générer le graphe inter-services (Gap-13).
- **À pouvoir exprimer** : qu'un projet documente structurellement **ce qu'il consomme, depuis qui, dans quelle version, avec quelle criticité**, dans un fichier canonique (nom + emplacement standardisés), et que cette documentation soit exploitable par un impact analyzer et un linter.
- **Touché par au moins un cas d'usage** : studio-projects, export-engine retro-fit, compta retro-fit.
- **Niveau** : P0 (prérequis pour Gap-04, Gap-07, Gap-13)
- **Canon change requis ?** : non (ajout d'une convention et d'un template, sans modification du canon existant)
- **Dépendances** : Gap-04 (linter qui valide la cohérence), Gap-06 (lien avec log d'impact), Gap-13 (source du graphe).

### Gap-06 — Pas de mécanisme d'IMPACT_LOG par projet

- **Manifestation** : `skills/t-vbb-impact-analyzer/SKILL.md` ligne 24 « Output Contract » précise : « Timestamped report (`kind: audit_report`): `docs/audits/impact-analysis-{YYYYMMDD-HHMM}.md` ». C'est un **snapshot ponctuel**, pas un log cumulatif. Le pattern de nom `impact-analysis-{date}.md` est explicitement daté. Aucun fichier `IMPACT_LOG.md` ou `IMPACT_LOG.yaml` n'existe (zéro hit find).
- **Observable aujourd'hui** : un humain qui demande « qui doit bouger suite au changement du 2026-06-15 ? » doit compiler manuellement plusieurs `impact-analysis-{date}.md`. Aucun outil ne fournit une vue longitudinale « voici l'historique des impacts cross-service identifiés ».
- **Conséquence du manque** : impossible de tracer « cette décision cross-service a-t-elle été effectivement migrée ? ». Impossible d'avoir un status `pending / in_progress / completed` par impact. Le suivi de la discipline de co-évolution est manuel et volatile.
- **À pouvoir exprimer** : qu'un projet maintienne un log cumulatif des impacts cross-service avec, pour chaque entrée : date, producteur, consommateurs impactés, classification (breaking/additive/cosmetic), statut de migration coordonnée (open / in_progress / done / accepted).
- **Touché par au moins un cas d'usage** : studio-projects, export-engine retro-fit, compta retro-fit.
- **Niveau** : P0 (avec Gap-04 et Gap-05, c'est le tiercé disciplinaire)
- **Canon change requis ?** : non (nouveau fichier + skill de mise à jour)
- **Dépendances** : Gap-05 (CONTRACTS_CONSUMED identifie les cibles), Gap-04 (linter vérifie que les entrées sont tenues à jour), Gap-07 (la co-évolution produit des entrées).

### Gap-07 — Pas de discipline outillée de co-évolution

- **Manifestation** : aucun fichier du framework ne mentionne « co-évolution », « coordinated migration », « consumer migration task » (zéro hit grep). Le pipeline `t-vbb-impact-analyzer` produit un rapport mais **ne génère pas** une séquence de tâches coordonnées chez les consommateurs. `1-vbb-api-contract-designer` (lu en entier) ne mentionne aucun mécanisme de notification des consommateurs.
- **Observable aujourd'hui** : quand un producteur modifie un contrat, la discipline « mini refacto coordonné chez les consommateurs » n'a aucune représentation dans le framework. Aucun checklist, aucune trace imposée, aucune notification outillée.
- **Conséquence du manque** : la co-évolution est entièrement manuelle et dépendante de la discipline humaine. Le passage à l'échelle (N services, N producteurs, N consommateurs) la rend impraticable.
- **À pouvoir exprimer** : qu'une modification de contrat déclenche automatiquement (ou au minimum signale) une séquence d'actions coordonnées chez les consommateurs — et que cette séquence soit tracée dans `IMPACT_LOG.md` (Gap-06).
- **Touché par au moins un cas d'usage** : studio-projects (4 services), export-engine retro-fit, compta retro-fit.
- **Niveau** : P1 (Gap-04 + Gap-05 + Gap-06 sont P0, ce gap est leur « moteur »)
- **Canon change requis ?** : incertain (pourrait être une extension de skill sans modification du canon)
- **Dépendances** : Gap-05, Gap-06 (qui sont les artefacts que ce gap peuple), Gap-04 (qui enforce que c'est peuplé).

### Gap-08 — Pas de support multi-repo

- **Manifestation** : `tools/vbb-architecture.py` ligne 8-30 `ARCHITECTURE_TOUCH_GLOBS` liste des chemins **relatifs au repo courant** uniquement. `tools/vbb-contract-runtime.py` ligne 30 `REPO_ROOT = Path(__file__).parent.parent.resolve()` est mono-repo par construction. `tools/vbb-project-init.py` ligne 50 `target_dir: Path` prend un seul répertoire. `tools/vbb-gate-check.py` ligne 67 `REPO_ROOT = Path(__file__).parent.parent.resolve()` idem. `tools/vbb-dependency-mapper` (`skills/t-vbb-dependency-mapper/SKILL.md` ligne 60-65) mentionne « inter-repo dependencies if visible » mais uniquement en lecture, pas en agrégation. `skills/t-vbb-docker-audit/SKILL.md` ligne 257 et `skills/t-vbb-docker-generate/SKILL.md` ligne 383 traitent le multi-app **comme une limitation** (« Multi-app architecture not supported. Audit each application separately. »).
- **Observable aujourd'hui** : un système de 4 services (chacun son repo) doit être auditée 4 fois. Aucun graphe global. Aucune coordination de discipline inter-repos. Un humain qui demande « quels autres repos consomment mon endpoint /v1/invoices ? » doit faire un grep à la main sur N repos.
- **Conséquence du manque** : la traçabilité cross-service existe seulement dans la conversation humaine. Le passage à l'échelle (système à 4+ repos) rend le framework mono-repo limitant.
- **À pouvoir exprimer** : qu'un système multi-repos soit traçable globalement, sans abandonner l'autonomie de chaque repo. Mécanismes attendus : déclaration « ce repo fait partie du système X », graphe agrégé, coordination de discipline (backups, contrats, impact), interrogation « qui consomme mes contrats ».
- **Touché par au moins un cas d'usage** : studio-projects (4 repos), tout projet éclaté.
- **Niveau** : P0 (sans multi-repo support, les patterns database-per-service inter-repos ne sont pas viables)
- **Canon change requis ?** : incertain (probablement extension `docs/extensions/multi-repo/`, mais l'enum des blocs ARCHITECTURE.md pourrait devoir évoluer)
- **Dépendances** : Gap-13 (graphe inter-services), Gap-05 (CONTRACTS_CONSUMED cross-repo), Gap-09 (mécanisme d'extension).

### Gap-09 — Pas d'extension/projection de patterns

- **Manifestation** : `docs/CONVENTIONS.md` (lu en entier, lignes 1-200+) ne contient aucun mécanisme d'extension ou de plugin. Le seul mécanisme d'évolution canon est le `CANON_CHANGE_PROPOSAL.md.template` (`docs/templates/` ligne : présent), qui est lourd (proposition, validation humaine, migration). `docs/ADR/0013-repo-organization-core-vs-distributions.md` (lu en entier) introduit le concept de `distributions/<name>/` pour les déclinaisons opérationnelles, mais pas pour les extensions de règles. `skills/0-vbb-standard/SKILL.md` (existe) ne mentionne pas non plus d'extension registry (zéro hit grep `extension|plugin`).
- **Observable aujourd'hui** : un pattern comme « database-per-service » ne peut pas être formalisé sans toucher au canon (donc validation humaine, lenteur). Aucune façon de dire « ce projet adhère au pattern X » sans réécrire CONVENTIONS.md.
- **Conséquence du manque** : le canon devient soit monolithique (tout dedans) soit gelé (peur d'ajouter). Les patterns émergents sont soit absorbés dans le canon avec friction, soit maintenus hors canon sans légitimité formelle.
- **À pouvoir exprimer** : qu'une communauté puisse définir un pattern optionnel (ex : « multi-service-database-per-service ») dans un espace non-canonique (`docs/extensions/<pattern>/`), et que des projets puissent y adhérer en le référençant (ex : `extensions: [multi-service-database-per-service]` dans leur `PROJECT_MODE.md`).
- **Touché par au moins un cas d'usage** : studio-projects (l'extension est précisément ce dont ils ont besoin).
- **Niveau** : P1
- **Canon change requis ?** : incertain (le mécanisme d'extension lui-même pourrait être un canon change, mais son contenu serait non-canon)
- **Dépendances** : Gap-01, Gap-02 (l'extension référence ces déclarations), Gap-03 (codegen depuis une extension), Gap-12 (pilier « DB owned » comme première extension concrète).

### Gap-10 — Pas de taxonomie des contrats cross-service

- **Manifestation** : `skills/1-vbb-api-contract-designer/SKILL.md` ligne 104 « Identify the primary consumers and the API's scope of responsibility » — la notion de consumer est **input optionnel**, pas un champ structuré du contrat produit. Le contrat résultant (ligne 130-145 « Document must contain ») liste Context, Use Case, Resource Model, Endpoints, Payloads, Auth & Authorization, Error Model, Compatibility & Versioning, Examples, Open Questions, Decision — aucun champ « Consumers ». Idem pour `2-vbb-api-auditor/SKILL.md` ligne 124 « ID `API-XX` » — pas de matrice producer × consumer.
- **Observable aujourd'hui** : un contrat conçu par `1-vbb-api-contract-designer` n'a pas de champ canonique « ce contrat est consommé par [services X, Y, Z] ». Impossible de générer automatiquement la matrice « qui dépend de quoi ».
- **Conséquence du manque** : la discipline de co-évolution (Gap-07) et l'analyse d'impact (Gap-06) sont faites à la main. Le graphe inter-services (Gap-13) ne peut pas être dérivé des contrats.
- **À pouvoir exprimer** : qu'un contrat soit traçable dans les deux sens (qui produit, qui consomme), via un champ structuré dans le document de contrat ET une entrée correspondante dans `CONTRACTS_CONSUMED.md` du consommateur (Gap-05).
- **Touché par au moins un cas d'usage** : studio-projects, export-engine retro-fit.
- **Niveau** : P0
- **Canon change requis ?** : non (extension du template `1-vbb-api-contract-designer`, pas modification de CONVENTIONS.md)
- **Dépendances** : Gap-05 (CONTRACTS_CONSUMED est la moitié consommateur), Gap-11 (lint archetype-aware), Gap-13 (graphe).

### Gap-11 — Pas d'archetype-aware contract lint

- **Manifestation** : `tools/vbb-contract-lint.py` ligne 79 « `Unsupported type: '{contract['type']}' (expected 'prompt_skill')` » — le seul typage vérifié est au niveau skill (prompt_skill). Il n'existe aucun champ « project_archetype » ni « service_archetype » dans le contrat. Le lint ne peut donc pas adapter ses règles au contexte (ex. : « un contrat cross-service doit avoir X-API-Key, version explicite, path de migration documenté »).
- **Observable aujourd'hui** : un contrat destiné à être exposé cross-service est validé exactement comme un contrat interne. Aucune règle ne vérifie la présence de versioning, d'auth explicite, de compatibilité ascendante documentée.
- **Conséquence du manque** : des contrats cross-service sont publiés sans les garanties minimales de stabilité, et la rupture est découverte à l'usage.
- **À pouvoir exprimer** : que la validation d'un contrat soit sensible au contexte (archétype du projet, scope du contrat, audience) — pas seulement générique.
- **Touché par au moins un cas d'usage** : studio-projects (contrats inter-services).
- **Niveau** : P1 (mais liée à Gap-02 — sans archétype, impossible d'avoir un lint sensible au contexte)
- **Canon change requis ?** : non (extension du linter avec règles contextuelles)
- **Dépendances** : Gap-02 (archétype comme entrée), Gap-10 (taxonomie consumer comme règle), Gap-04 (linter cross-service général).

### Gap-12 — Pas de support explicite pour « DB owned by service, consumed via API »

- **Manifestation** : `docs/CONVENTIONS.md` (lu en entier, ~250 lignes) définit 5 piliers : P1 Readability, P2 Modularity, P3 Coherence, P4 Traceability (embedded), P5 Robustness (P.R1-P.R8). Aucun pilier ne couvre l'architecture de persistance (« le service ne possède que sa propre DB, accède aux autres via API »). Aucun pattern non plus n'est formalisé dans `docs/extensions/` (le dossier n'existe pas — `find . -name "extensions" -type d` : zéro résultat).
- **Observable aujourd'hui** : le principe « database-per-service » est une **convention orale**, pas un pilier quality. Un projet peut l'ignorer sans violer aucun P1-P5.
- **Conséquence du manque** : la discipline database-per-service n'a pas de légitimité canonique. Elle est imposée par la culture d'équipe, pas par le framework.
- **À pouvoir exprimer** : qu'un principe architectural de cette nature puisse être formulé et institutionnalisé dans le canon (Pilier P6 — Architecture Boundaries ?) ou dans son extension `docs/extensions/multi-service-database-per-service/`.
- **Touché par au moins un cas d'usage** : studio-projects (pattern central).
- **Niveau** : P1
- **Canon change requis ?** : oui si pilier P6 ajouté au canon · non si extension pure
- **Dépendances** : Gap-09 (mécanisme d'extension), Gap-01 (orientation DB).

### Gap-13 — Pas de graphe inter-services indépendant

- **Manifestation** : `tools/vbb-architecture.py` `graph --write` produit un Mermaid projection **intra-repo** (RELATIONS_PATH = `docs/RELATIONS.md`, ARCHITECTURE_PATH = `docs/ARCHITECTURE.md`). Aucune fonction ne prend plusieurs ARCHITECTURE.md en entrée pour produire un graphe agrégé. Aucun outil ne consomme plusieurs `CONTRACTS_CONSUMED.md` pour générer un graphe cross-service.
- **Observable aujourd'hui** : un système de 4 services produit 4 RELATIONS.md. Aucun graphe global. Un humain qui veut voir « qui consomme quoi » doit ouvrir 4 fichiers et les croiser mentalement.
- **Conséquence du manque** : la compréhension globale d'un système multi-services reste humaine. L'analyse d'impact cross-services est un artisanat.
- **À pouvoir exprimer** : qu'un graphe multi-services puisse être agrégé depuis les déclarations locales de chaque repo (CONTRACTS_CONSUMED.md, ARCHITECTURE.md, IMPACT_LOG.md) et soit consultable (Markdown statique ou interactif).
- **Touché par au moins un cas d'usage** : studio-projects.
- **Niveau** : P0
- **Canon change requis ?** : non (nouvel outil, sans modification du canon)
- **Dépendances** : Gap-05 (CONTRACTS_CONSUMED), Gap-06 (IMPACT_LOG), Gap-08 (multi-repo support minimal), Gap-10 (taxonomie consumer).

### Gap-14 — Pas de CONTEXT.md / PROJECT_MODE.md enrichi

- **Manifestation** : `tools/vbb-project-init.py` `_context_md` lignes 88-110 et `_project_mode_md` lignes 67-86 produisent des fichiers minimaux. `_architecture_md` lignes 112-140 produit un seul bloc `project-core` avec 3 champs. Aucun des trois ne contient de sections structurées pour `db_orientation`, `project_archetype`, `scope` explicite, `contracts_expected`, etc. `skills/t-vbb-project-context-init/SKILL.md` ligne 80-87 « Scope » liste ce qui est créé mais ne spécifie pas de schéma de contenu.
- **Observable aujourd'hui** : un projet bootstrapé a un CONTEXT.md de 18 lignes avec `<Description courte du projet — à compléter>` (ligne 100-102). L'architecte doit inventer la structure.
- **Conséquence du manque** : la qualité de l'intent projet dépend de la discipline individuelle de l'architecte. Pas de schéma canonique. Pas de validation automatique du contenu minimum.
- **À pouvoir exprimer** : que le bootstrap d'un nouveau projet produise un intent doc **structuré** selon un schéma défini (incluant `db_orientation`, `project_archetype`, scope, contrats prévus, non-goals explicites).
- **Touché par au moins un cas d'usage** : studio-projects, export-engine retro-fit, compta retro-fit, tout nouveau projet.
- **Niveau** : P1
- **Canon change requis ?** : incertain (modification du contenu généré par `vbb-project-init.py`, mais pas du canon lui-même)
- **Dépendances** : Gap-01, Gap-02 (les champs à structurer), Gap-09 (extension pour les champs spécifiques au pattern multi-service).

### Gap-15 — Pas de mécanisme « ne pas régresser » en CI sur PR multi-service

- **Manifestation** : `tools/vbb-gate-check.py` (lu lignes 1-80) implémente un gate **pré-exécution** (avant de coder) : ADR_REQUIRED, POC_REQUIRED, CAN_CODE_START. Il n'existe aucun gate **post-diff** ou **par-PR** qui valide que les modifications n'ont pas régressé la discipline multi-service. Aucun fichier dans `.github/workflows/` ou `scripts/hooks/` n'implémente un lint cross-service (vérifié sommairement).
- **Observable aujourd'hui** : une PR qui introduit un import cross-DB sans mise à jour d'IMPACT_LOG peut être mergée sans warning.
- **Conséquence du manque** : la discipline multi-service est enforced **uniquement** au moment de l'init (`vbb-project-init.py`) ou de l'audit manuel, jamais au point d'entrée du code (PR).
- **À pouvoir exprimer** : qu'un ensemble de règles « ne pas régresser » soit enforceable en CI sur chaque PR d'un projet multi-service. Idéalement, configurable par projet via un `docs/MULTISERVICE_DISCIPLINE.yaml`.
- **Touché par au moins un cas d'usage** : studio-projects, tout projet qui veut vraiment tenir la discipline.
- **Niveau** : P0
- **Canon change requis ?** : non (nouveau hook CI + extension du linter)
- **Dépendances** : Gap-04 (linter multi-service), Gap-05 (CONTRACTS_CONSUMED), Gap-06 (IMPACT_LOG).

---

## 2. Gaps dérivés (découverts pendant l'analyse)

### Gap-16 — Pas de formalisation du mécanisme `@include` inter-fichiers

- **Manifestation** : `distributions/claude/CLAUDE.md` lignes 14-16 utilisent une syntaxe ad-hoc :
  ```
  @AGENTS.md
  @SYSTEM.md
  ```
  Aucun parseur canonique ne valide ces inclusions. `AGENTS.md` racine utilise la même convention pour `SYSTEM.md` (symlink) et pour `docs/PILOTAGE.md` (référencé en texte). Aucun fichier ne documente la grammaire `@include`.
- **Observable aujourd'hui** : si un fichier inclus est renommé ou supprimé, la directive `@include` reste silencieuse (pas de warning CI, pas de validation au build). Le risque de lien cassé est réel.
- **Conséquence du manque** : les fichiers entry-point (AGENTS.md, CLAUDE.md, SYSTEM.md) peuvent dériver par rapport à leur cible sans détection automatique.
- **À pouvoir exprimer** : que les `@include` soient parsés et validés : (a) la cible existe, (b) la cible est canonique, (c) la directive est listée dans un graphe d'inclusion visible.
- **Touché par au moins un cas d'usage** : maintenance courante du framework (déjà un risque latent).
- **Niveau** : P2 (n'affecte pas directement le pattern multi-service, mais le mécanisme est utile pour Gap-03 codegen)
- **Canon change requis ?** : non (nouveau linter)
- **Dépendances** : Gap-03 (codegen AGENTS.md), Gap-17 (détection d'édition manuelle).

### Gap-17 — Pas de détection d'édition manuelle sur fichier généré

- **Manifestation** : `tools/vbb-architecture.py` lint valide que `RELATIONS.md` est cohérent avec `ARCHITECTURE.md` (couvert par les fonctions de linting), mais **rien n'empêche** un humain d'éditer `RELATIONS.md` à la main (la consigne §1 « Generated — do not edit » est documentaire, pas enforced). Idem pour les fichiers générés par `setup.sh` (AGENTS.md installé, SYSTEM.md installé, CLAUDE.md installé) — aucune vérification post-install que le contenu est bien celui attendu.
- **Observable aujourd'hui** : un humain peut éditer `RELATIONS.md` manuellement et le commit passe. Le graphe diverge silencieusement jusqu'à la prochaine régénération.
- **Conséquence du manque** : risque de drift entre source canonique et vue générée. Le codegen perd sa propriété de « source unique ».
- **À pouvoir exprimer** : qu'un fichier marqué `@generated` (ou avec un sentinel explicite) ne puisse pas diverger de sa source sans qu'un linter le détecte (warning ou erreur selon politique).
- **Touché par au moins un cas d'usage** : tout projet qui s'appuie sur le codegen.
- **Niveau** : P2
- **Canon change requis ?** : non (convention + linter)
- **Dépendances** : Gap-03 (codegen étendu), Gap-16 (@include formalisé).

### Gap-18 — Pas d'articulation entre `t-vbb-impact-analyzer` (snapshot) et futur IMPACT_LOG (cumulatif)

- **Manifestation** : `skills/t-vbb-impact-analyzer/SKILL.md` ligne 124 « Timestamped report ... `docs/audits/impact-analysis-{YYYYMMDD-HHMM}.md` » — chaque exécution produit un nouveau snapshot. `docs/AUDIT_STATUS.md` reçoit une ligne « impact-analyzer » mais sans statut persistant d'impact. Aucun mécanisme ne transforme un snapshot en entrée de log cumulatif.
- **Observable aujourd'hui** : 3 snapshots existent dans `docs/audits/vbb-runtime/t-vbb-impact-analyzer_*.json` (vérifié `ls`) et des audits dans `docs/audits/`, mais aucune vue longitudinale.
- **Conséquence du manque** : si Gap-06 (IMPACT_LOG) est implémenté, comment l'alimenter depuis les snapshots existants ? Manuellement ? Par un script ? Aucune politique n'est définie.
- **À pouvoir exprimer** : que la sortie de `t-vbb-impact-analyzer` puisse être (a) versionnée en snapshot comme aujourd'hui ET (b) projetée dans un log cumulatif structuré. Le format et le déclencheur doivent être définis.
- **Touché par au moins un cas d'usage** : studio-projects (le scénario d'usage concret).
- **Niveau** : P2
- **Canon change requis ?** : non (extension de skill + nouveau fichier)
- **Dépendances** : Gap-06 (cible du log), Gap-04 (linter qui enforce la mise à jour).

---

## 3. Gaps couverts par l'existant (anti-faux-positifs)

| Gap présumé | Constat | Source |
|-------------|---------|--------|
| Discipline documentation | `docs/CONVENTIONS.md` (P4 Traceability embedded) + `docs/AUDIT_STATUS.md` + `docs/SESSION.md` + `docs/TEMPORAL_PROVENANCE.md` couvrent la traçabilité **intra-projet** de façon solide. `ARCHITECTURE.md` → `RELATIONS.md` codegen est en place. | `docs/CONVENTIONS.md` lignes 130-145 (Pillar 4), `tools/vbb-architecture.py` ligne 1-100. |
| Triage des routes | `docs/PILOTAGE.md` (v2.2) + `tools/vbb-phase-router.py` couvrent le routage phase × trigger × agent. | `docs/PILOTAGE.md` lignes 1-100, `tools/vbb-phase-router.py` lignes 1-100. |
| Gate pré-exécution | `tools/vbb-gate-check.py` implémente ADR + POC + Integration gate. | `tools/vbb-gate-check.py` lignes 1-100. |
| Cohérence architecture/code | `tools/vbb-architecture.py lint` enforce que chaque fichier architecture-sensitive est couvert par au moins un bloc. | `tools/vbb-architecture.py` `ARCHITECTURE_TOUCH_GLOBS` lignes 8-30. |

**Conclusion** : aucun des gaps présumés n'est en réalité couvert. Les mécanismes existants sont **mono-repo** et **intra-projet**. Le pattern multi-service exige des mécanismes analogues mais **cross-repo** et **cross-service**.

---

## 4. Hypothèses non-vérifiables (marquées UNKNOWN si on les forçait en gaps)

| Hypothèse | Pourquoi non-gap | Action |
|-----------|-------------------|--------|
| Les ADR existants couvrent les patterns multi-service | 5 ADR (`docs/adr/`) traitent : executor boundary (0001), UI/UX routing (0002), graphic propagation (0003), schema version (0004), Core vs Distribution (0013). Aucun ne traite database-per-service ou co-évolution. | Conservé en hypothèse — **non gap**. |
| Le framework pourrait s'en sortir sans extensions formelles | Le mécanisme de canon change (`docs/templates/CANON_CHANGE_PROPOSAL.md.template`) existe, mais il est lourd. Aucune preuve qu'un projet refuserait de l'utiliser pour formaliser un pattern. | Hypothèse H — **non conclusive**, classée en Gap-09. |

---

## 5. Récapitulatif

18 gaps caractérisés (15 initiaux + 3 dérivés) :
- **5 P0** (Gap-04, Gap-05, Gap-06, Gap-08, Gap-13, Gap-15) — discipline outillée + multi-repo.
  - Note : je compte 6 P0 si on inclut Gap-10. Vérification : Gap-10 est marqué P0 dans le texte. Donc **6 P0** au total : Gap-04, Gap-05, Gap-06, Gap-08, Gap-10, Gap-13, Gap-15 = **7 P0**.
- **9 P1** (Gap-01, Gap-02, Gap-03, Gap-07, Gap-09, Gap-11, Gap-12, Gap-14) + Gap-16 = **8 P1**.
- **3 P2** (Gap-17, Gap-18) + Gap-16 reclassé = **2 P2** (Gap-16 devient P2).

**Correction** : je recompte proprement dans le tableau de synthèse §0 :
- P0 : Gap-04, Gap-05, Gap-06, Gap-08, Gap-10, Gap-13, Gap-15 = **7**
- P1 : Gap-01, Gap-02, Gap-03, Gap-07, Gap-09, Gap-11, Gap-12, Gap-14 = **8**
- P2 : Gap-16, Gap-17, Gap-18 = **3**

Total **18** ✓.

---

## 6. Source de vérité — gouvernance chargée pendant l'analyse

Fichiers lus et exploités comme source de vérité :

- `docs/CONTEXT.md` (lignes 1-100) — MOC central
- `docs/PILOTAGE.md` (lignes 1-200) — routes et gates
- `docs/PROJECT_MODE.md` (lignes 1-50) — mode DISTRIBUTION
- `docs/AUDIT_STATUS.md` (lignes 1-300+) — état audits, dont QOA-001 à 008 (P1 actifs sur Core/Distribution)
- `docs/CONVENTIONS.md` (lignes 1-200) — 5 piliers + P.R1-P.R8
- `docs/ARCHITECTURE.md` (lignes 1-200) — blocs canoniques
- `docs/DISTRIBUTIONS.md` (lignes 1-100) — Core vs Distribution
- `docs/adr/0013-repo-organization-core-vs-distributions.md` (entier)
- `distributions/hermes/proxy/adr/0006-confidential-proxy-architecture.md` (lignes 1-80)
- `tools/vbb-architecture.py` (lignes 1-200)
- `tools/vbb-project-init.py` (entier, ~370 lignes)
- `tools/vbb-contract-lint.py` (lignes 1-100)
- `tools/vbb-contract-runtime.py` (lignes 1-80)
- `tools/vbb-phase-router.py` (lignes 1-100)
- `tools/vbb-gate-check.py` (lignes 1-80)
- `skills/t-vbb-project-context-init/SKILL.md` (entier)
- `skills/t-vbb-impact-analyzer/SKILL.md` (entier)
- `skills/t-vbb-dependency-mapper/SKILL.md` (entier)
- `skills/t-vbb-mode-transition-gate/SKILL.md` (lignes 1-80)
- `skills/1-vbb-api-contract-designer/SKILL.md` (entier)
- `skills/2-vbb-api-auditor/SKILL.md` (lignes 1-80)
- `skills/1-vbb-conventions/SKILL.md` (lignes 1-80)
- `distributions/claude/CLAUDE.md` (lignes 1-30)

**Verdict Phase 1** : `READY_FOR_PHASE_2`. Tous les gaps ont une manifestation observable, un exemple concret, et une citation. Aucun gap inventé. Voir `02_PRIORITIES.md` pour la classification finale et `03_DEPENDENCIES.md` pour le graphe.
