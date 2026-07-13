---
kind: "audit_report"
audit_type: "systemic"
run_id: "2026-07-13_1551_poc-subagents-methodology-audit"
status: "PARTIAL"
date: "2026-07-13"
agent: "codex with two independent read-only explorers"
---

# Audit systémique — discipline POC et usage des subagents

> **Remediation note (2026-07-13)** — This report preserves the historical
> audit verdict. `SYS-POC-001` was subsequently resolved by commits `07e1e24`
> and `b29a048`, with independent revalidation in
> `docs/runs/2026-07-13_1653_ready-revalidation/`. See the addendum in the
> original run closeout and the current status in `docs/AUDIT_STATUS.md`.

## Déclaration initiale

- **Route** : AUDIT
- **Type d'audit** : systémique / méthodologique
- **Skill utilisé** : `vibebackbone` → `0-vbb-audit-readiness` → grille générique d'audit systémique
- **Artefact cible** : ce rapport + `docs/runs/2026-07-13_1551_poc-subagents-methodology-audit/02_AUDIT_REPORT.md`
- **Gouvernance lue** : `AGENTS.md`, `docs/{CONTEXT,PILOTAGE,PROJECT_MODE,SESSION,AUDIT_STATUS,CONVENTIONS}.md`, `GUIDE.md`, intake et gate du run
- **Artefacts requis** : rapport persistant, rapport de run et mise à jour de `docs/AUDIT_STATUS.md`
- **Règle de vérification** : un finding n'est `VERIFIED_FINDING` qu'avec deux sources distinctes ou un test confirmé.

## Résumé exécutif

Vibebackbone possède déjà les bonnes briques : ADR pour décider, POC pour tester
une hypothèse, gate pré-exécution, phases de review/closeout, séparation
canon/extension et préférence pour la revue indépendante. Le manque principal
n'est donc pas un nouveau mécanisme, mais une sémantique plus nette et quelques
alignements opérationnels.

Le verdict est **PARTIAL** : la direction méthodologique est saine, mais le gate
POC comporte deux défauts bloquants pour la confiance (`PIVOT` accepté comme GO,
template canonique non parsé) et la transition expérimentation → décision →
implémentation reste parfois implicite. Les subagents ont démontré une valeur
réelle pour borner le contexte du parent, mais pas encore une amélioration
générale de la qualité ou du coût.

## Périmètre et méthode

### Audité

- ADR, conventions, stratégies et templates ;
- gate ADR/POC/Intégration et tests associés ;
- échantillon de POC et de runs récents ;
- ADR multi-services 0007, 0010, 0014, 0017–0024 ;
- workers, orchestrateurs, `subagent_eligible`, providers et traces `.pi-subagents` ;
- handoff, closeout, revue indépendante et préservation du contexte.

### Méthode

Deux explorations read-only en contextes séparés ont été demandées : une sur la
discipline POC/ADR, une sur les subagents. La synthèse parent a ensuite vérifié
les comptes, les regex, les commits de promotion et la réintégration du scout
historique. Les subagents n'ont ni écrit ni décidé.

## Existant — ce qui fonctionne déjà

| Besoin | Mécanisme existant | Lecture audit |
|---|---|---|
| Décision de conception | ADR `PROPOSED/ACCEPTED/REJECTED/SUPERSEDED` | Suffisant ; `ACCEPTED` signifie décidé, pas éprouvé. |
| Expérimentation | `docs/runs/<id>/POC.md` avec hypothèse, test, seuil, résultat | Bonne structure, défaut d'alignement avec le parseur. |
| Autorisation de démarrer | `vbb-gate-check.py` + `INTEGRATION_GATE.md` | Utile et réellement bloquant, mais sémantique trop binaire. |
| Séparation expérimentation/canon | Convention d'isolation + ADR-0014 extensions | Direction cohérente, adoption encore théorique sur plusieurs ADR. |
| Validation d'implémentation | execution/review/closeout + boucle P.R2 | Ne doit pas être confondue avec le GO du POC. |
| Validation terrain | preuves dans projets/runs consommateurs | Existe comme idée, sans signal synthétique commun. |
| Indépendance | P.R8, sessions distinctes, workers dédiés | Solide comme principe, advisory dans l'exécution. |
| Délégation bornée | scout read-only, source fermée, sortie persistée, sole writer | Expérience utile mais échantillon trop petit. |

## Findings

### SYS-POC-001 — Le contrat POC et son gate divergent

| Champ | Valeur |
|---|---|
| **Severity** | P1 |
| **Type** | VIOLATION |
| **Location** | `docs/templates/POC.md.template:41-44`, `tools/vbb-gate-check.py:89-94,297-306` |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Aligner le parseur sur le template, refuser `PIVOT`, ajouter une table de tests verdicts. |

**Evidence trace** : OBSERVATION — le template écrit `- **Verdict** : GO` et
distingue `PIVOT` → SIGNAL — le regex ne tolère pas les marqueurs Markdown et
inclut `PIVOT` dans le motif positif → VÉRIFICATION — le gate a rejeté le POC
conforme du run, puis un test direct du regex a produit : template gras refusé,
GO simple accepté, PIVOT accepté, NO-GO refusé → FINDING.

Impact : faux blocage d'un POC conforme et faux PASS d'une hypothèse qui demande
précisément un pivot. Le second cas peut autoriser une implémentation fondée sur
une hypothèse invalidée.

### SYS-POC-002 — `ACCEPTED` est régulièrement lisible comme « validé » alors que l'expérimentation manque

| Champ | Valeur |
|---|---|
| **Severity** | P1 |
| **Type** | OBSERVATION |
| **Location** | `docs/adr/0018-multirepo-support.md`, `0019`, `0020`, `0021` |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | MITIGATED |
| **Recommendation** | Afficher une maturité dérivée à plusieurs axes ; ne pas ajouter un nouvel enum global. |

**Evidence trace** : OBSERVATION — 23 ADR numérotées sont présentes, 18 portent
un lien POC vide/aucun ; plusieurs ADR acceptées décrivent encore des outils « à
créer » → SIGNAL — le statut de décision ne décrit pas la preuve technique →
VÉRIFICATION — ADR-0018 et ADR-0020 sont acceptées, sans POC lié, avec
implémentation future explicite → FINDING.

Ce n'est pas une faute d'ADR : une décision peut légitimement être acceptée avant
implémentation. Le risque vient de la lecture ambiguë du mot « validé ».

### SYS-POC-003 — Le gate est utile mais sa portée et ses liens restent partiellement implicites

| Champ | Valeur |
|---|---|
| **Severity** | P2 |
| **Type** | VIOLATION |
| **Location** | `GUIDE.md:1063-1119`, `docs/PILOTAGE.md:70-81`, `tools/vbb-gate-check.py` |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Harmoniser la portée, exiger les liens explicites et distinguer travail d'audit de démarrage du code. |

**Evidence trace** : OBSERVATION — GUIDE, PILOTAGE, template et outil utilisent
des formulations différentes → SIGNAL — les déclencheurs et la permission ne
couvrent pas le même domaine → VÉRIFICATION — le run systémique/multi-agent a
déclenché POC mais pas ADR malgré le guide ; `MISSING_LINK` est annoncé dans la
docstring mais jamais émis ; le template Integration n'annonce que STRUCTUREE
alors que PILOTAGE inclut AUDIT → FINDING.

### SYS-POC-004 — La transition POC → implémentation n'a pas toujours une décision durable distincte

| Champ | Valeur |
|---|---|
| **Severity** | P2 |
| **Type** | TREND |
| **Location** | `docs/strategy/p0-4-review-matrix-poc.md`, commits `e3a50d2`, `57fe05d` |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Pour canon/architecture/cross-service, consigner une décision post-POC avant l'intégration. |

**Evidence trace** : OBSERVATION — le POC T1–T8 conclut GO_TO_IMPLEMENTATION et
dit « aucun commit » à court terme → SIGNAL — le prototype a ensuite été importé
par le dashboard → VÉRIFICATION — commit POC `e3a50d2`, puis commit d'intégration
`57fe05d` limité au dashboard et à ses tests, sans decision record dans ce commit
→ FINDING.

L'intégration est advisory et testée ; le problème est la lisibilité de la
transition, pas sa qualité technique.

### SYS-SUB-001 — L'expérience subagent prouve la traçabilité, pas la qualité générale

| Champ | Valeur |
|---|---|
| **Severity** | P1 |
| **Type** | OBSERVATION |
| **Location** | `.pi-subagents/artifacts/22d5d96a_*`, roadmap `SESSION.md` |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | MITIGATED |
| **Recommendation** | Mesurer exactitude, contradictions, fallback et coût total sur plusieurs cas comparables. |

**Evidence trace** : OBSERVATION — entrée, sortie, métadonnées et réintégration
existent → SIGNAL — la délégation réduit la charge du contexte parent →
VÉRIFICATION — sortie réintégrée identique hors newline, exit 0, mais 54k tokens
d'entrée et plusieurs contradictions internes ; un audit historique signale
aussi un scout échoué avec fallback manuel → FINDING.

### SYS-SUB-002 — `subagent_eligible` exprime une intention non imposée

| Champ | Valeur |
|---|---|
| **Severity** | P2 |
| **Type** | OBSERVATION |
| **Location** | `skills/*/SKILL.md`, routeurs/outils |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | ACCEPTED |
| **Recommendation** | Le documenter comme advisory jusqu'à un besoin d'enforcement démontré. |

**Evidence trace** : OBSERVATION — 45 skills déclarent `true`, 19 `false` →
SIGNAL — le catalogue encode déjà une intention de délégation → VÉRIFICATION —
aucun consommateur effectif du champ n'a été trouvé dans les outils/tests ; les
orchestrateurs principaux sont `false` → FINDING.

L'absence d'enforcement n'appelle pas immédiatement un nouveau linter. Elle doit
d'abord être rendue explicite pour éviter une fausse garantie.

### SYS-SUB-003 — La réintégration contrôle les fichiers, pas suffisamment le sens

| Champ | Valeur |
|---|---|
| **Severity** | P2 |
| **Type** | OBSERVATION |
| **Location** | `.pi-subagents/artifacts/22d5d96a_scout_0_{input,output,meta}.*` |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | NEEDS_DECISION |
| **Recommendation** | Ajouter quatre contrôles : comptes, citations, contradictions, diff sortie→intégration. |

**Evidence trace** : OBSERVATION — le brief impose sources, format et chemin →
SIGNAL — le cadre borne correctement l'écriture → VÉRIFICATION — le brief dit 6
sources mais en liste 8, attend 38 findings mais les sources en totalisent 37 ;
la sortie annonce 12 quick wins puis en énumère 15 et contient des affirmations
contradictoires sur les outils canoniques → FINDING.

### SYS-POC-005 — Le nom d'artefact décision diverge entre prompt et loop closure

| Champ | Valeur |
|---|---|
| **Severity** | P2 |
| **Type** | VIOLATION |
| **Location** | `prompts/canonical/03-p-vbb-decision.md`, `tools/vbb-loop-closure-check.py` |
| **Evidence Level** | VERIFIED_FINDING |
| **Decision** | MITIGATED |
| **Recommendation** | Choisir un nom canonique et conserver une migration/pointer temporaire. |

**Evidence trace** : OBSERVATION — le prompt demande
`03_DECISION_RECORD.md` → SIGNAL — une décision conforme pourrait échouer au
closeout → VÉRIFICATION — la première exécution stricte de la loop closure a
refusé le run avec `03_DECISION.md: missing` malgré le decision record complet
→ FINDING. Le run ajoute un pointer documentaire de compatibilité, sans dupliquer
la décision.

## Modèle de maturité recommandé — dérivé, pas canonique

Ne pas créer une liste globale `proposé → accepté → expérimenté → validé → ...`.
Ces mots mélangent quatre objets différents. Conserver les artefacts actuels et
en dériver une lecture humaine :

| Axe | Source de vérité | Question |
|---|---|---|
| Décision | `ADR.status` | Une option a-t-elle été choisie ? |
| Hypothèse | `POC.verdict` ou « non requis » explicite | La principale incertitude a-t-elle été testée ? |
| Implémentation | execution + review + closeout + P.R2 | Le changement existe-t-il et respecte-t-il ses critères ? |
| Terrain | lien vers run/projet consommateur | Le comportement a-t-il été observé en usage réel ? |

Lectures dérivées possibles :

- **proposé** : ADR `PROPOSED` ;
- **décidé** : ADR `ACCEPTED` ;
- **éprouvé** : POC requis et `GO`, ou POC explicitement non requis ;
- **implémenté** : preuves d'exécution/review/closeout ;
- **observé terrain** : preuve datée d'un consommateur réel.

`PIVOT` et `NO-GO` restent des résultats, jamais des autorisations d'implémenter
la proposition initiale. Aucun de ces libellés ne devient un nouveau statut à
persister dans ce chantier.

## Place des POC

### Quand un POC est pertinent

Le déclencheur devrait être l'**incertitude coûteuse à découvrir après
implémentation**, et non seulement une famille de mots-clés :

- dépendance externe ou environnement non maîtrisé ;
- architecture/pattern nouveau sans précédent local ;
- changement cross-service avec hypothèse de propagation ;
- convention ou gate susceptible de produire de nombreux faux positifs ;
- mécanisme de gouvernance inédit dont le coût cognitif est inconnu.

Un POC n'est pas requis pour une modification déterministe, locale, réversible et
couverte par des tests existants.

### Zone d'expérimentation

Recommandation : **ne pas créer immédiatement un nouveau top-level canonique**.

- Le record durable reste `docs/runs/<id>/POC.md`.
- Un prototype jetable reste hors des modules stables et son chemin est référencé
  par le POC.
- Si un prototype exécutable doit être versionné, utiliser provisoirement un
  espace explicitement expérimental lié au run, sans import depuis `tools/`,
  skills, runtime ou CI.
- N'introduire un dossier global `experiments/` qu'après au moins trois cas où le
  stockage run-local est réellement insuffisant.

### Gate POC → implémentation

Évolution légère proposée :

1. le POC répond uniquement à l'hypothèse et produit GO/NO-GO/PIVOT ;
2. pour canon, architecture ou cross-service, une décision distincte consomme le
   POC et choisit `IMPLEMENT / DEFER / REJECT / NEW_POC` ;
3. le gate vérifie les liens explicites et autorise le travail seulement après
   `GO + IMPLEMENT` ;
4. l'implémentation reste validée par review/P.R2, jamais par le POC ;
5. la preuve terrain est ajoutée plus tard sans rouvrir artificiellement l'ADR.

Pour les travaux simples, les étapes 1–3 restent non requises.

## POC multi-services prioritaires — ordre d'apprentissage

1. **Contrats → multi-repo → graphe** : fixture de 3 repos/4 services, cycle et contrat manquant. Éprouve ADR-0007/0018/0020 et débloque les suivants.
2. **Breaking change → impact log → tâches consommateurs** : projection idempotente et absence de doublons. Éprouve ADR-0010/0017/0024.
3. **Extension database-per-service** : schéma, dépendances, conflit et copie dans deux projets sans effet canonique. Éprouve ADR-0014/0019.
4. **CI multi-services** : cas vert, cycle, contrat manquant et outil absent sur GitHub/GitLab. Seulement après le POC 1 ; éprouve ADR-0021.
5. **`@include` + `@generated`** : cible absente, cycle, sentinel et fraîcheur. Second rideau P2 ; éprouve ADR-0022/0023.

## Pattern méthodologique subagents recommandé

```text
QUESTION
  Une question décisionnelle, non-objectifs, niveau de preuve et réfutation.
    ↓
EXPLORATIONS SPÉCIALISÉES
  1..N briefs orthogonaux, read-only, sources fermées, citations obligatoires.
  Au moins une exploration contradictoire pour canon/P0/P1.
    ↓
SYNTHÈSE
  Le parent vérifie comptes, citations, contradictions, recouvrements et UNKNOWN.
  OBSERVATION → SIGNAL → HYPOTHESIS → VERIFIED_FINDING.
    ↓
DÉCISION
  Contexte distinct ou humain ; désaccords conservés ; majorité ≠ preuve.
```

### Déléguer lorsque

- le sous-problème est séparable, borné et read-only ;
- les sources et la sortie peuvent être fermées ;
- le contexte source est volumineux mais la synthèse attendue compacte ;
- la sortie est vérifiable indépendamment ;
- des angles orthogonaux ou contradictoires sont possibles.

### Ne pas déléguer lorsque

- le gate est rouge ou le scope instable ;
- le sousagent devrait décider du canon, accepter un risque ou arbitrer le produit ;
- plusieurs agents écriraient les mêmes fichiers ;
- la tâche requiert tout le contexte accumulé du parent ;
- le briefing et la réintégration coûtent plus que la tâche ;
- le reviewer reçoit une conclusion à confirmer plutôt qu'une question ouverte.

### Contrat minimal d'un brief

`question`, `scope`, `sources`, `non_goals`, `output_schema`,
`disconfirming_evidence`, `write_boundary`, `acceptance_checks`.

Conserver le pattern actuel « explorateurs read-only → parent sole writer ». Pour
chaque délégation, journaliser succès/échec, durée, tokens, fallback, anomalies et
corrections de réintégration. Ne pas ajouter d'orchestrateur générique avant
d'avoir mesuré plusieurs cas comparables.

## Modifications documentaires éventuellement pertinentes

Ces modifications sont des recommandations, **non implémentées** :

| Priorité | Modification | Justification |
|---|---|---|
| P1 | Aligner `POC.md.template`, `INTEGRATION_GATE.md.template`, GUIDE et `vbb-gate-check.py` | Corrige faux blocage et faux PASS. |
| P1 | Ajouter tests table-driven du gate | Verrouille GO gras/simple, NO-GO, PIVOT, liens, négations et ADR superseded. |
| P2 | Ajouter au GUIDE la lecture de maturité à quatre axes | Clarifie sans nouveau statut ni source de vérité. |
| P2 | Ajouter un petit template de brief subagent en référence | Rend le pattern reproductible sans orchestration complexe. |
| P2 | Documenter `subagent_eligible` comme advisory | Évite de supposer un enforcement absent. |
| P2 | Aligner `03_DECISION.md` et `03_DECISION_RECORD.md` | Évite qu'un run conforme au prompt échoue à la clôture. |
| P3 | Ajouter un mini journal de délégation dans les runs qui l'utilisent | Permet l'apprentissage empirique avant canonisation. |

Toute modification Core future devra appliquer le check d'impact sur Hermes/Cody
et enregistrer la décision dans `docs/DISTRIBUTIONS.md`. Le présent audit ne
modifie ni Core ni distribution.

## Risques consolidés

| Risque | Severity | Probabilité | Impact | Action recommandée |
|---|---|---|---|---|
| `PIVOT` déverrouille l'implémentation | P1 | High | High | Corriger regex + tests avant prochain POC déclenché. |
| Template POC canonique rejeté | P1 | High | Medium | Aligner parseur/template. |
| ADR acceptée lue comme solution éprouvée | P1 | Medium | High | Lecture dérivée quatre axes. |
| Fausse indépendance de subagents au framing identique | P1 | Medium | High | Exploration contradictoire, question sans conclusion suggérée. |
| Réintégration sémantique insuffisante | P2 | Medium | Medium | Comptes/citations/contradictions/diff. |
| Sur-gouvernance par nouveaux statuts/orchestrateur | P2 | Medium | Medium | Réutiliser artefacts existants et observer avant enforcement. |

## Hors scope et UNKNOWN

- Aucun ADR multi-services restant n'a été implémenté.
- Aucun prototype n'a été promu au canon.
- Aucun benchmark comparatif multi-subagents n'a été exécuté.
- UNKNOWN : gain net de tokens/coût sur plusieurs tâches comparables.
- UNKNOWN : adoption terrain des concepts multi-services hors de ce dépôt.
- UNKNOWN : qualité des providers/modèles listés aujourd'hui ; non testée ici.

## Verdict global

**PARTIAL** — architecture méthodologique saine et réutilisable, mais deux défauts
P1 du gate doivent être corrigés avant de considérer la discipline POC fiable.
La proposition recommandée reste volontairement légère : aligner l'existant,
dériver la maturité de quatre sources de preuve et formaliser un brief subagent
minimal après observation de plusieurs cas.

## Handoff

- **Phase suivante** : `03_DECISION`
- **Nouvelle session/contexte recommandé** : oui, décideur distinct de l'auditeur
- **Décisions attendues** : accepter/rejeter/différer la proposition légère ;
  prioriser la correction du gate séparément de toute méthodologie nouvelle.
- **Vigilance** : ne pas convertir ce rapport directement en canon.

## FINAL_STATUS

```yaml
FINAL_STATUS:
  elapsed_seconds: 900
  budget_initial: 180
  progress_emitted: true
  progress_count: 4
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/audits/systemic-poc-subagents-methodology-20260713-1551.md
    - docs/runs/2026-07-13_1551_poc-subagents-methodology-audit/02_AUDIT_REPORT.md
  tests_run:
    - vbb-gate-check current run
    - POC regex verdict matrix
    - ADR and POC inventory counts
    - historical subagent output reintegration diff
    - git history of P0-4 POC promotion
  tests_missing:
    - comparative multi-run subagent benchmark
    - external consumer field validation
  risks:
    - PIVOT currently passes the POC gate
    - canonical POC template verdict currently fails parsing
  open_points:
    - independent decision required
```
