---
template_id: "ADR"
version: "1.0"
lane_eligible:
  - "STRUCTUREE"
  - "AUDIT"
related:
  - "docs/adr/README.md"
  - "docs/CONVENTIONS.md#pr3--gate-before-action"
---

# ADR — 0055-memory-authority-seam

**Status**: ACCEPTED
**Date**: 2026-08-26
**Route**: STRUCTUREE
**Décideurs**: humain (autorité finale, validation explicite du 2026-08-26) — agent de long cours VibeBackbone/Memory (revue) — agent DSH (rédaction)
**Liée à**: ADR 0049
**Liée à POC**: docs/runs/2026-08-26_2105_memory-authority-seam/POC.md

> **Acceptation** — validée par l'humain le 2026-08-26 sous condition de preuve.
> La preuve est fournie par le POC lié (verdict `GO` : vault conforme accepté,
> six cas adversariaux rejetés avec leur code attendu, round-trip de
> reconstruction vert). L'acceptation porte sur la version **amendée** par les
> cinq points `A1`–`A5` que la construction du banc a révélés (§Amendements).

## Contexte

Un travail expérimental de mémoire agentique (Backbone Memory, jalons M5.x à
M7.11b) a été construit comme kernel déterministe sur DeepSeek Harness. Sa
finalité déclarée n'est pas une « mémoire longue » générique : c'est la gestion
du statut des artefacts d'un projet en phase de codage — production, canon,
legacy — avec une couche déterministe où « le LLM propose, le kernel contrôle,
l'utilisateur reste l'autorité ». Son intégration à VibeBackbone est demandée.

Or VibeBackbone détient déjà l'autorité sur cette question, et par plusieurs
mécanismes canoniques distincts : le statut documentaire (Documentary Contract
v1.0, ADR 0052 et 0054, `.vbb/document-convention.yaml`), l'assurance
(`FINAL_STATUS` et `ASSURANCE_STATUS`, ADR 0050), la certification
(`certification_status`, sept valeurs, ADR 0051 et 0053), le lifecycle du savoir
canonique (`ENGINEERING_KNOWLEDGE_GOVERNANCE.md`, ADR 0049 : le canon ne change
que par une nouvelle version gouvernée), et le résultat de gate (`PASS`/`FAIL`
qualifié par famille `DESIGN`/`CERTIFICATION`/`OTHER`). Ces cinq dimensions sont
orthogonales par construction et outillées par des vérificateurs model-free
versionnés dans le dépôt.

Brancher une seconde couche déterministe qui décide, elle aussi, du statut
d'artefacts produirait deux sources de vérité sur la même question — exactement
la faute interdite par la règle critique #5. Cette faute est silencieuse : elle
ne se manifeste qu'à la première contradiction, c'est-à-dire au pire moment.
L'audit du 2026-07-29 a déjà sanctionné dans ce dépôt un verdict documentaire
que la mesure ne soutenait pas ; accorder une autorité canonique à un composant
dont la qualification est encore ouverte rejouerait ce motif.

La décision ci-dessous ne porte donc pas sur Backbone Memory. Elle définit le
**contrat que toute couche mémoire devra respecter pour habiter VibeBackbone**.
Backbone Memory en est le premier implémenteur candidat, pas le sujet.

## Décision

**Le canon reste le dépôt. Une couche mémoire runtime est une couche de
projection et de candidature : elle ne détient jamais l'autorité canonique sur
le statut d'un artefact, et l'accession au canon passe obligatoirement par une
gate qui produit ou modifie un artefact versionné.**

Cette décision se décline en sept clauses normatives.

### C1 — Trois invariants structurants

```
CANONICAL_MEMORY_IS_DERIVED = 1     # tout contenu mémoire reflétant une source
                                    # canonique est dérivé et reconstructible
PROMOTION_IS_A_GATE = 1             # aucune entrée mémoire ne devient canon
                                    # sans franchir une gate existante
NO_PARALLEL_SEMANTIC_AUTHORITY = 1  # une seule autorité par dimension de statut
```

Ces invariants sont vérifiables sans LLM et doivent être capables d'échouer.

### C2 — Modèle d'état minimal de la mémoire : trois classes, aucune ne vaut canon

| Classe | Définition | Autorité | Perte si le vault disparaît |
|---|---|---|---|
| `projection` | reflète une source canonique existante dans le dépôt | **aucune** — le statut est lu, jamais décidé | néant : reconstructible |
| `candidate` | capturé et qualifié, sans autorité canonique | aucune ; éligible à promotion | la file d'attente de promotion, non le canon |
| `working` | état temporaire utile au raisonnement, pas même candidat | aucune | néant par définition |

Aucune de ces trois classes ne peut signifier « canon », « production » ou
« legacy ». Ces qualificatifs n'existent que sur un artefact du dépôt.

**A2** — Un artefact canonique **supersédé ne projette rien** : son autorité a
migré vers la version qui le supersède, et une projection survivante est une
autorité résiduelle illicite (`PROJECTION_STALE_SUPERSEDED`).

**A3** — Une entrée `working` n'est **ni promouvable, ni porteuse de source** :
le passage par `candidate` est obligatoire (`WORKING_PROMOTED`,
`WORKING_WITH_SOURCE`).

### C3 — Protocole de promotion, défini avant tout stockage

```
capture → qualification → candidate → promotion gate → artefact canonique → projection mémoire
```

La promotion doit : produire ou modifier un artefact dans le dépôt ; franchir les
gates existantes applicables ; laisser une provenance exploitable (quelle
capture, quelle autorisation, quel humain, quel run). La mémoire ne s'autopromeut
jamais, et aucun chemin ne permet d'écrire directement une entrée mémoire dont la
classe serait canonique.

**A5** — L'autorisation de promotion est **explicitement humaine et traçable**
(`authorization.by = human` + identifiant du message autorisant). Une promotion
autorisée par le modèle, par un résultat d'outil, par une mémoire rappelée ou par
un sous-agent est rejetée (`PROMOTION_WITHOUT_AUTHORIZATION`).

### C4 — Les cinq dimensions restent distinctes

Le vocabulaire « canon / legacy / production » n'introduit pas un sixième axe. Il
se projette sur les dimensions existantes ; toute case sans correspondance exige
une `CANON_CHANGE_PROPOSAL`, pas une invention locale.

| Dimension | Autorité canonique | Ce que la mémoire peut en faire |
|---|---|---|
| statut documentaire | Documentary Contract v1.0 (`status:`, frontmatter) | projeter |
| assurance | `FINAL_STATUS` / `ASSURANCE_STATUS` (ADR 0050) | projeter |
| certification | `certification_status`, 7 valeurs (ADR 0051 / 0053) | projeter |
| lifecycle du savoir | `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` (ADR 0049) | projeter, proposer une promotion |
| résultat de gate | vérificateurs du dépôt (`vbb-gate-check.py`, …) | projeter |
| « production / canon / legacy » | **dérivé** des dimensions ci-dessus | projeter uniquement |

Corollaire immédiat : un champ de statut propre à une couche mémoire (par
exemple un `status_loc` expérimental) est licite pour la classe `candidate` et
la classe `working`, et illicite pour la classe `projection`, où le statut est
lu à la source.

### C5 — Conflits et supersession

Une contradiction n'est jamais résolue automatiquement. Un `candidate` qui
contredit un artefact canonique reste `candidate` et rend le conflit visible ;
il ne dégrade ni ne supersède la source. La supersession d'un artefact canonique
suit exclusivement le chemin de l'ADR 0049 : une nouvelle version gouvernée.
Une correction explicite d'un humain est une autorité ; une contradiction
détectée par un modèle n'en est pas une.

**A1** — Tout `candidate` déclare un **`subject_key`**. Sans clé de sujet, la
contradiction avec le canon ou avec un autre candidat n'est pas détectable sans
sémantique, donc pas vérifiable model-free : l'absence de clé est elle-même une
violation (`CANDIDATE_WITHOUT_SUBJECT_KEY`). Limite assumée et documentée : deux
formulations du même fait sous deux clés distinctes ne sont pas rapprochées ;
c'est le prix du déterminisme, et il est explicite.

### C6 — Deux audits séparés, dans cet ordre

1. **Audit architectural** — respect des invariants C1, des classes C2, du
   protocole C3, de la provenance, de la non-résolution automatique des conflits,
   et de la reconstructibilité des projections.
2. **Audit distributionnel** — chemins absolus, dépendances locales, résolution
   de paquets, portabilité inter-machines, comportement sur les runtimes cibles.

L'audit distributionnel **ne bloque pas** l'expérimentation locale sur DSH tant
que l'audit architectural reste propre. Il devient bloquant dès que l'intégration
au Core est demandée, puisque le Core diffuse vers toutes les distributions
actives (règle #12, `DISTRIBUTIONS.md` règle A).

### C7 — Critère de succès, mécanique et permanent

À tout instant, pour toute affirmation portée par la mémoire, ces trois questions
doivent recevoir une réponse mécanique :

1. **D'où vient cette affirmation ?** (capture, source, run, autorisation)
2. **Quelle autorité lui donne son statut ?** (laquelle des cinq dimensions, et
   quel artefact du dépôt)
3. **Que perdrait-on si le vault disparaissait ?** (`néant` pour `projection` et
   `working` ; la file de promotion pour `candidate`)

Toute réponse ambiguë signifie que la couture n'est pas assez solide, et bloque
l'intégration.

**A4** — Les réponses admissibles sont **fixées par classe**, sans quoi la
question resterait rhétorique :

| Classe | Origine | Autorité de statut | Perte si le vault disparaît |
|---|---|---|---|
| `projection` | `repo` (source citée) | `canon:<artefact>` | `none (rebuildable)` |
| `candidate` | capture citée (session, message) | `none (candidate)` | `promotion queue only` |
| `working` | capture citée | `none (working)` | `none (ephemeral)` |

Une entrée dont l'une des trois réponses n'est pas dérivable est en violation
(`C7_UNANSWERABLE`).

### Cas adversariaux de falsification (obligatoires avant toute intégration)

| # | Cas | Verdict attendu |
|---|---|---|
| T1 | un `candidate` contredit un artefact canonique | conflit rendu visible ; canon inchangé ; classe inchangée |
| T2 | une `projection` dont la source a été supersédée | la projection suit la source ou est invalidée ; jamais autorité résiduelle |
| T3 | un fait mémorisé sans source | classe `working` ou `candidate` au plus ; jamais `projection` |
| T4 | deux sessions produisent des `candidate` incompatibles | les deux coexistent ; aucune résolution automatique ; conflit surfacé |
| T5 | destruction complète du vault puis reconstruction | `projection` intégralement reconstruite ; perte limitée à la file de promotion |
| T6 | tentative de marquer une entrée mémoire directement « production » | rejet fail-closed, tracé |

Ces six tests valent plus qu'une intégration prématurée : ils sont la condition
d'acceptation de tout implémenteur, Backbone Memory compris.

### Amendements issus du POC (traçabilité)

Le banc de falsification a été construit **avant** l'acceptation, et sa
construction a révélé cinq sous-spécifications du contrat. Chacune est un endroit
où l'implémenteur aurait dû trancher seul — c'est-à-dire une porte d'entrée pour
une vérité parallèle. Toutes sont intégrées ci-dessus et vérifiées par un code
machine.

| # | Amendement | Clause | Code |
|---|---|---|---|
| A1 | `subject_key` obligatoire sur tout `candidate` | C5 | `CANDIDATE_WITHOUT_SUBJECT_KEY` |
| A2 | un artefact supersédé ne projette rien | C2 | `PROJECTION_STALE_SUPERSEDED` |
| A3 | `working` non promouvable et sans source | C2 | `WORKING_PROMOTED`, `WORKING_WITH_SOURCE` |
| A4 | réponses de C7 fixées par classe | C7 | `C7_UNANSWERABLE` |
| A5 | autorisation de promotion humaine et traçable | C3 | `PROMOTION_WITHOUT_AUTHORIZATION` |

Vérificateur de référence :
`docs/runs/2026-08-26_2105_memory-authority-seam/poc/seam_check.py` (stdlib,
model-free, `--selftest`). Sa promotion en `tools/vbb-memory-seam-check.py` avec
tests associés est un pas d'implémentation, soumis à la gate.

### Ce que cette décision ne fait pas

Elle n'intègre pas Backbone Memory, n'approuve aucun code, n'introduit aucune
dépendance, ne crée aucun répertoire de vault, et ne se prononce ni sur la
qualification architecturale ni sur la portabilité de l'implémentation
existante. Elle ne modifie aucune des cinq autorités existantes : elle les
déclare non partageables.

## Conséquences

### Positives

- La règle #5 est protégée par un contrat explicite plutôt que par vigilance.
- VibeBackbone gagne un contrat utile même si aucune mémoire n'est jamais
  intégrée : la couture clarifie l'articulation entre ADR 0049, ADR 0050 et le
  Documentary Contract.
- Backbone Memory obtient enfin une spécification **externe** contre laquelle se
  mesurer, là où sa qualification actuelle est auto-référentielle.
- Les six cas adversariaux fournissent une définition falsifiable du succès,
  conforme à la doctrine « une gate doit être capable d'échouer ».
- La reconstructibilité (C1) rend la couche mémoire jetable, donc peu risquée.

### Négatives / coûts

- Toute couche mémoire devra implémenter un chemin de promotion, plus coûteux
  qu'une écriture directe.
- Les faits utiles n'ayant pas d'artefact dans le dépôt restent `candidate`, donc
  sans force normative : c'est un inconfort assumé.
- La table C4 crée une obligation de correspondance à maintenir quand une des
  cinq dimensions évolue.

### Neutres

- Aucun changement pour les distributions actives tant que l'intégration n'est
  pas demandée : la couture ne modifie ni chemin, ni secret, ni configuration
  runtime.

## Alternatives rejetées (≥ 2)

### Alternative A — Le vault détient le canon pour certaines classes de faits

- **Description** : autoriser la mémoire à être autorité canonique pour les faits
  qui n'ont pas de fichier (décisions prises en conversation, contraintes
  d'environnement), afin d'éviter le coût de la promotion.
- **Pourquoi rejetée** : cela crée deux autorités sur la même dimension, viole
  `NO_PARALLEL_SEMANTIC_AUTHORITY`, rend le canon illisible sans runtime et
  détruit l'auditabilité model-free — la propriété que la mémoire elle-même
  revendique.

### Alternative B — Unifier les statuts en un axe unique « canon / legacy / production »

- **Description** : écraser statut documentaire, assurance, certification,
  lifecycle et résultat de gate dans une seule énumération, plus simple à
  projeter en mémoire.
- **Pourquoi rejetée** : ces dimensions sont orthogonales par décision explicite
  (ADR 0050, ADR 0051, ADR 0053). Les écraser détruirait de l'information de
  gouvernance et invaliderait des gates existantes.

### Alternative C — Intégrer d'abord, contractualiser ensuite

- **Description** : brancher Backbone Memory sur VibeBackbone, puis formaliser la
  frontière à partir du comportement observé.
- **Pourquoi rejetée** : l'intégration ferait entrer dans le canon un composant
  non qualifié (sélectionnabilité et durcissement production ouverts) et non
  portable (chemins absolus machine-spécifiques mesurés), exportant le défaut
  vers toutes les distributions. L'ordre inverse est la seule variante
  fail-closed.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| La couture reste lettre morte faute de vérificateur | moyenne | fort | exiger les six tests T1–T6 et un vérificateur model-free avant toute intégration |
| Dérive de la table C4 quand une des cinq dimensions évolue | moyenne | moyen | la table devient une entrée du contrôle de cohérence documentaire ; toute évolution de dimension cite l'ADR 0055 |
| Contournement par la classe `working` (tout y devient fourre-tout) | moyenne | moyen | `working` interdit à la projection et non promouvable directement : passage obligatoire par `candidate` |
| Coût de promotion jugé trop lourd, écritures directes réintroduites | faible | fort | T6 rend la tentative détectable et tracée |
| Lecture de la décision comme un rejet de Backbone Memory | moyenne | faible | l'ADR ne juge pas l'implémentation ; il fournit sa cible |

## Hypothèses

- Les cinq dimensions de statut restent orthogonales ; si une fusion était
  décidée par ailleurs, C4 doit être reconsidérée.
- Un artefact canonique est toujours représentable comme fichier versionné dans
  le dépôt ; si une classe de faits gouvernés ne l'était pas, la couture devrait
  être rouverte plutôt que contournée.
- La reconstruction d'une `projection` depuis le dépôt est possible sans LLM ; si
  elle exigeait une interprétation sémantique, `CANONICAL_MEMORY_IS_DERIVED`
  deviendrait non vérifiable.
- L'implémenteur candidat accepte d'être audité en deux temps (C6).

## Références

- ADR amont : 0049 (gouvernance du savoir d'ingénierie), 0050 (assurance
  design/certification), 0051 et 0053 (dimension adversariale), 0052 et 0054
  (Documentary Contract v1.0)
- Canon : `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`,
  `docs/GATE_ASSURANCE_GOVERNANCE.md`, `docs/document-model/`,
  `.vbb/document-convention.yaml`, `AGENTS.md` règles #5, #6, #12, #14, #16
- Run : `docs/runs/2026-08-26_2105_memory-authority-seam/01_INTAKE.md`
- Source externe : synthèse d'architecture Backbone Memory (M5.x → M7.11b,
  2026-08-26) — document de projet tiers, cité comme contexte, non comme canon

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: GOUVERNANCE
reversible: true
depends_on:
  - "ADR 0049"
  - "ADR 0050"
  - "ADR 0054"
  - "docs/runs/2026-08-26_2105_memory-authority-seam/POC.md"
blocks:
  - "audit architectural d'un implémenteur candidat (I2)"
  - "toute intégration d'une couche mémoire au Core"
supersedes: []
amended_by:
  - "A1..A5 (POC 2026-08-26, verdict GO)"
verified_at: "2026-08-26T21:40:00Z"
verified_by: "human"
verified_method: "human-review"
```
