---
run_id: "2026-08-02_documentary-cleanup-living-core-pilot"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "codex"
started_at: "2026-08-02T00:00:00Z"
ended_at: "2026-08-02T00:00:00Z"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "POC.md"
artifacts_produced:
  - "02_AUDIT.md"
---

# 02_AUDIT — Living documentary core

## Périmètre et ancrage

| État | Révision observée | Confiance | Observation |
|---|---|---:|---|
| Publié | `origin/main@067b8ea6e9a7d9bea65a29340bdc38da1361f039` | HIGH | Référence distante observable; aucun changement distant effectué. |
| Local | `668e3e09e1a2ad0575297278af9b88860420c39d` | HIGH | HEAD détaché; contient le commit local d’alignement des skills. |
| Worktree | non propre | HIGH | Huit répertoires `docs/runs/` non suivis, dont ce run; aucune modification du noyau ciblé observée. |
| Runtime Pi déployé | `UNKNOWN` | LOW | Aucun snapshot ou chemin de runtime déployé fourni; seule la source suivie `distributions/pi/SYSTEM.md` est observable. |

Le contrat de dépôt observable est `.vbb/document-convention.yaml`,
`document_convention: vbb-doc-v1`, version `1.0`, adoption `adopted`. Son scope
déclaré couvre `docs/DOCUMENT_CONVENTION.md`; il ne fournit pas à lui seul un
tag observable pour les autres artefacts du périmètre.

## Noyau examiné et tuples observés

Les tuples sont des qualifications de travail produites sans changement de
frontmatter. `SCOPED_AUTHORITY` signifie ici une autorité limitée à la
responsabilité explicitement déclarée; `UNKNOWN` est conservé lorsque la preuve
de provenance, de révision ou de relation n’est pas portée par l’artefact.

| Artefact | Tuple `(authority, lifecycle, temporality, primary_function, secondary_functions, load_policy)` | Responsabilité observée | Preuve / confiance |
|---|---|---|---|
| `AGENTS.md` | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [], ALWAYS)` | Règles agent-facing et boot | Frontmatter et §Critical Rules; HIGH pour la responsabilité, MEDIUM pour la révision documentaire |
| `SYSTEM.md` → `distributions/pi/SYSTEM.md` | `(SCOPED_AUTHORITY, ACTIVE, MULTI_PERIOD, REFERENCE, [], ALWAYS)` | Posture runtime Pi/OpenCode; AGENTS reste supérieur | Symlink et déclaration explicite dans le fichier source; MEDIUM, contenu adversarial à arbitrer |
| `docs/CONTEXT.md` | `(SCOPED_AUTHORITY, ACTIVE, MULTI_PERIOD, NAVIGATION, [], ALWAYS)` | Routage et état persistant | `context_role`, `run_id: permanent`, active state; MEDIUM |
| `docs/PILOTAGE.md` | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [], ALWAYS)` | Routage opérationnel | « Canonical piloting entry point »; HIGH |
| `docs/CONVENTIONS.md` | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_ROUTE)` | Conventions qualité et P.R1–P.R8 | Version 1.1, canonical but evolvable; HIGH |
| `docs/ARCHITECTURE.md` | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_ROUTE)` | Source structurée d’architecture | « canonical architecture source »; lint PASS; HIGH |
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | `(CANONICAL, ACTIVE, MULTI_PERIOD, NORMATIVE, [DECISION_RECORD], ON_ROUTE)` | Gouvernance adversariale | Version 1.2 et corps adopté par ADR 0053; frontmatter ADR 0051; MEDIUM |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | `(CANONICAL, ACTIVE, MULTI_PERIOD, NORMATIVE, [DECISION_RECORD], ON_ROUTE)` | Sémantique des gates et ASSURANCE_STATUS | Version 1.0, schema 1.1 dans le corps, références ADR 0050/0051; MEDIUM |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_ROUTE)` | Cycle de vie et promotion du savoir | Version 1.0, ADR 0049; HIGH |
| `docs/DOCUMENT_CONVENTION.md` | `(SCOPED_AUTHORITY, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_DEMAND)` | Contrat `vbb-doc-v1` | Frontmatter et `.vbb/document-convention.yaml`; HIGH |
| `docs/REFERENCE/pre-merge-gate.md` | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_ROUTE)` | Séquence P.R2 et 5b | `canonical: true`, canon unique P.R2; HIGH |
| `PROMPTS_ARCHITECTURE.md` | `(SCOPED_AUTHORITY, ACTIVE, MULTI_PERIOD, REFERENCE, [], ON_ROUTE)` | Cartographie des prompts | Version 1.1 et date dans le corps; absence de frontmatter/contrat explicite; MEDIUM |
| `docs/RELATIONS.md` | `(NON_AUTHORITATIVE, ACTIVE, CURRENT, GENERATED, [REFERENCE], ON_DEMAND)` | Projection du graphe d’architecture | `status: generated`, `source: ARCHITECTURE.md`; HIGH |

## Matrice identité / représentation / relations

| Identité observée | Représentation source | Projection / localisation | Relations critiques | Résultat DIM/DGM/DTS |
|---|---|---|---|---|
| `governance-core` | `AGENTS.md` | `AGENTS.md` | Autorité textuelle, mais décision/relations DGM non explicites | DIM PASS; DGM UNKNOWN; DTS UNKNOWN (tag absent) |
| `runtime-behavior` | `distributions/pi/SYSTEM.md` | `SYSTEM.md` symlink | REPRESENTED_BY et LOCATED_AT observables; runtime déployé inconnu | DIM PASS; DGM partiel/UNKNOWN; DTS UNKNOWN |
| `architecture-source` | `docs/ARCHITECTURE.md` | `docs/RELATIONS.md` | `GENERATED_FROM` déclaré par projection | Source/projection cohérentes textuellement; DGM révision/autorité UNKNOWN; DTS projection tag non canonique |
| `adversarial-governance` | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | même localisation | Références vers gate et outils; ADR de frontmatter/corps divergent | DIM/ontology PASS sur observation; provenance ADR finding |
| `moc-central` | `docs/CONTEXT.md` | même localisation | Références boot; état courant non confirmé par un run actif | DIM/ontology PASS sur observation; freshness finding |

## Findings normalisés — aucune décision prise

| ID | Artefact | Source | Écart observé | Impact potentiel | Confiance | Route avant décision |
|---|---|---|---|---|---:|---|
| LDC-001 | `AGENTS.md` | DTS / DTP | Le boot set observé ne contient que Critical Rules 1–15; la règle de transition documentaire attendue par les skills alignées n’est pas observable dans ce fichier. | Un agent peut ne pas appliquer la non-correction silencieuse sur ce canon. | HIGH | `CANON_CHANGE` possible seulement après OUI et arbitrage du canon |
| LDC-002 | `SYSTEM.md`, `distributions/pi/SYSTEM.md` | DTS / DGM | Source et symlink sont identiques, mais le texte runtime déclare encore la dimension adversariale post-cutoff en v1.1 / ADR 0051 tandis que la gouvernance observée porte une clarification v1.2 / ADR 0053. | Runtime local potentiellement divergent de la gouvernance applicable. | HIGH | `DOCUMENTARY_CORRECTION` ou `CANON_CHANGE` à déterminer après OUI |
| LDC-003 | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | DTS | Frontmatter `adr: "0051"` et corps « adopted by ADR 0053 » ne désignent pas la même décision comme autorité de version 1.2. | Provenance et traçabilité de l’autorité adversariale ambiguës. | HIGH | `DOCUMENTARY_CORRECTION` ou changement de canon selon arbitrage |
| LDC-004 | `docs/GATE_ASSURANCE_GOVERNANCE.md`, `docs/REFERENCE/pre-merge-gate.md`, `docs/CONTEXT.md` | DGM / DTS | Les documents continuent de référencer ADR 0051 pour le cadre adversarial, alors que la clarification v1.2 est attribuée à ADR 0053 ailleurs. Le rôle respectif de 0051 et 0053 n’est pas résolu par le périmètre. | Risque de deux provenances concurrentes lors d’une décision ou d’une certification. | MEDIUM | `UNKNOWN`; aucune route sûre avant clarification humaine |
| LDC-005 | Noyau hors `docs/DOCUMENT_CONVENTION.md` | DTS | Le contrat `vbb-doc-v1@1.0` est adopté, mais son scope déclaré ne couvre pas les autres artefacts examinés; leurs tags DTS ne sont donc pas observables. | Compatibilité documentaire non démontrable sans inventer un tag ou élargir le contrat. | HIGH | `DOCUMENTARY_CORRECTION` seulement après OUI; pas de migration automatique |
| LDC-006 | `docs/CONTEXT.md` | DGM / DTS | Le fichier annonce `updated: 2026-07-29`, `active run: none` et un état de release antérieur à HEAD local `668e3e0` et au run courant. | Un agent peut router depuis un état persistant périmé. | HIGH | `DOCUMENTARY_CORRECTION` après OUI |
| LDC-007 | `PROMPTS_ARCHITECTURE.md` | DIM / DTS | Artefact actif avec version/date dans le corps, mais sans frontmatter d’identité, politique de chargement ou contrat interprétable. | Autorité de cartographie des prompts et provenance de révision partiellement UNKNOWN. | MEDIUM | `PLUS_TARD` recommandé jusqu’à preuve de contrat |
| LDC-008 | Runtime Pi déployé | DIM / DGM / DTS | Aucun état déployé, SHA ou provenance observable dans le périmètre; seule la source Git `distributions/pi/SYSTEM.md` est connue. | Impossible d’affirmer la convergence entre état local et runtime. | HIGH | `UNKNOWN`; aucune remédiation documentaire sûre |

## Contrôles exécutés

- `python tools/vbb-status-dashboard.py --json` : PASS d’exécution, verdict
  global `PARTIAL` à cause du worktree non propre, HEAD détaché, upstream absent
  et risques ouverts préexistants.
- `python tools/vbb-architecture.py lint` : PASS, 0 erreur / 0 warning.
- `python tools/vbb-contract-lint.py` : PASS, 0 erreur / 1 warning préexistant
  non bloquant sur `0-vbb-standard`.
- `python tools/vbb-document-convention-lint.py .` : PASS.
- Probe C0–C4 en lecture seule sur six observations représentatives : DIM et
  Ontologie PASS lorsque les champs sont observables; DTS UNKNOWN pour tags
  absents; DGM UNKNOWN lorsque les relations ne sont pas explicitement
  observables. Le pilote ne scanne pas les fichiers et n’a rien écrit.
- Aucun `graph --write`, aucun correctif, aucun déplacement, aucune suppression.

## Limites

- Le runtime déployé n’est pas vérifiable sans chemin ou snapshot explicite.
- La relation exacte entre ADR 0051 et ADR 0053 ne peut pas être arbitrée par
  lecture du seul périmètre.
- Les absences de tags ne prouvent pas une incompatibilité lorsque le scope du
  contrat les exclut; elles restent des findings de compatibilité UNKNOWN.

## Verdict de phase

`AUDIT_FINDINGS_READY_FOR_HUMAN_DECISION`
