---
run_id: "2026-07-28_1600_r0-adversarial-audit-of-m2-implementation"
phase: "02_AUDIT"
voie: "AUDIT"
status: "ACTIVE"
kind: "ADVERSARIAL_AUDIT"
posture: "seek-to-falsify"
audit_type: "ADVERSARIAL_FALSIFICATION"
started_at: "2026-07-28T16:15:00Z"
ended_at: "2026-07-28T16:30:00Z"
agent: "external adversarial auditor (distinct session, distinct provider, fresh context)"
artifacts_consumed:
  - "01_INTAKE.md (this run)"
  - "M1_DECISIONS.md (normative source)"
  - "ADR 0050 (predecessor schema)"
  - "ADR 0049 (knowledge governance)"
  - "ADR 0043 (orthogonal runtime/assurance)"
  - "ADR 0031 (autonomous runs)"
  - "ADR 0033 (credentials gate)"
  - "08_INDEPENDENT_REVIEW_DISTINCT_ACTOR.md (M0 GENUINE review)"
  - "06_INDEPENDENT_REVIEW.md (M2 PARTIAL self-review)"
  - "07_CLOSEOUT.md (M2 closeout)"
  - "M2_DEFERRED_ITEMS.md (M2 deferrals)"
  - "MIGRATION.md (M2 migration doc)"
artifacts_produced:
  - "02_AUDIT.md (this file)"
---

# 02_AUDIT — Campagne adversariale de l'implémentation M2

> **Posture.** R0 cherche à **falsifier** M2. Toute hypothèse est présumée
> fausse jusqu'à preuve du contraire. L'absence de falsification est
> *documentée*, pas célébrée.

## Synthèse exécutive

| # | Hypothèse | Trouvé ? | Finding ID |
|---|---|---|---|
| H1 | Conflit d'autorité (double vérité sur un concept) | partiel | ADVR-FALSIF-03 |
| H2 | Boucle impossible à satisfaire | non | (documenté §H2) |
| H3 | Fail-open involontaire | **OUI** | ADVR-FALSIF-01 (= H7) |
| H4 | Régression compatibilité ascendante | **OUI** | ADVR-FALSIF-02, 08 |
| H5 | Ambiguïté normative | **OUI** | ADVR-FALSIF-06, 08 |
| H6 | Conflit ancien/nouveau statut | **OUI** | ADVR-FALSIF-09 |
| H7 | Contournement A0/A1/A2 | **OUI** | ADVR-FALSIF-01 |
| H8 | Règles CERTIFIED/SUSPENDED incohérentes | **OUI** | ADVR-FALSIF-07 |
| H9 | Migration impossible | **OUI** | ADVR-FALSIF-04, 09 |
| H10 | Conflit avec ADRs existantes | **OUI** | ADVR-FALSIF-05 |
| H11 | Cas limite dépôt solo | **OUI** | ADVR-FALSIF-04 |
| H12 | Inflation documentaire inutile | non | (documenté §H12) |

**Verdict global.** 9 falsifications confirmées sur 12 hypothèses.
Aucun finding classé bloquant en absolu, mais plusieurs classés S0/S1.

## Trouvaille #1 — Self-contournement A0 par M2 lui-même

**ID.** ADVR-FALSIF-01

**Hypothèse falsifiée.** H7 (contournement A0/A1/A2) + H3 (fail-open).

**Reproduction (lecture du canon M2).**

`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.1 :

> *In an agent-governed repository, governance documents, prompts, skills
> and templates are the runtime for agents. Any change under `AGENTS.md`,
> `SYSTEM.md`, `docs/PILOTAGE.md`, `docs/templates/`, `prompts/`,
> `skills/`, or any `distributions/` path is **never `A0`** — minimum
> `A1`.*

`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.2 :

> *Governance canon that gates other work (`AGENTS.md`, `SYSTEM.md`,
> `PILOTAGE.md`, gate tools, review profiles) → `A2`.*

`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §4.3 (fail-closed rules) :

> | Niveau déclaré `A0` mais déclencheur `A1`/`A2` matche | **escalade obligatoire** vers le niveau du trigger |

**Comportement M2 réel.**

M2 a modifié 8 fichiers canoniques, dont 6 figurent dans la liste
explicite de §1.1 et tous correspondent au moins au critère de
§1.2 « gouvernance canon » :

| Fichier modifié par M2 | §1.1 hit | §1.2 hit | Niveau requis |
|---|---|---|---|
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (NEW) | implicite (gouverne domaine) | oui (gate authority) | **A2** |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` (extended) | implicite (gate tools) | oui (gate tools) | **A2** |
| `docs/PILOTAGE.md` (extended) | **oui (explicite)** | oui (gates other work) | **A2** |
| `docs/CONVENTIONS.md` (extended) | implicite (gouverne) | oui (quality standards) | **A2** |
| `docs/AGENTIC_RUN_PROTOCOL.md` (extended) | implicite (gouverne) | oui (review profiles) | **A2** |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` (extended) | implicite (gouverne) | oui (knowledge canon) | **A2** |
| `docs/REFERENCE/pre-merge-gate.md` (extended) | implicite (gouverne) | oui (gate reference) | **A2** |
| `docs/adr/0051-...` (NEW) | non listé | partiellement (ADR est décision, pas gate) | **A1** minimum |

M2 a déclaré `level: A0` (cf. `07_CLOSEOUT.md` §ASSURANCE_STATUS
narrative v1.1, archivé) avec la justification :

> *« this run does not claim CERTIFIED on any modified canon file »*
> *« M2 changes are doc-only (markdown + ADR), no executable surface »*

**Conflit direct avec §1.1.**

§1.1 ferme explicitement l'échappatoire « pure doc » pour la
gouvernance canon : *« Any change under `AGENTS.md`, `SYSTEM.md`,
`docs/PILOTAGE.md`, `docs/templates/`, `prompts/`, `skills/`, or any
`distributions/` path is **never `A0`** »*. La justification M2
contredit §1.1 *mot pour mot*.

**Gravité.** **S0** — canon-breaking. La règle §1.1 a été créée par
M2 *pour empêcher exactement ce contournement*. Le premier acte de
M2 la viole. Si le producteur de la règle peut s'y soustraire, la
règle est caduque.

**Impact.**

- Tout futur changement de canon peut désormais invoquer le précédent
  M2 (« pure doc, no executable surface ») pour échapper à §1.1.
- La règle §4.3 fail-closed (escalade obligatoire A0 → A1/A2) est
  inopérante : M2 l'a contournée par la simple mention « doc-only ».
- L'autorité `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` perd sa force
  normative au premier jour de son existence.

**Proposition de classification.**

- **Catégorie** : canon-breaking ; nullité partielle de §1.1.
- **Remédiation canon (proposition, hors scope R0)** :
  - Soit durcir §1.1 pour interdire *explicitement* la justification
    « doc-only » sur les fichiers listés.
  - Soit amender M2-09 (PILOTAGE triage) pour que la règle « A0
    interdit sur gouvernance canon » soit *mécaniquement* vérifiée
    par `vbb-gate-check.py` (et non par déclaration).
- **Effet immédiat** : aucun (M2 closeout est HANDOFF PARTIAL, aucun
  certificat n'est demandé).

---

## Trouvaille #2 — Le cutoff est violé par le producteur du cutoff

**ID.** ADVR-FALSIF-02

**Hypothèse falsifiée.** H4 (régression compatibilité) + H6 (conflit statuts).

**Reproduction.**

`docs/ADR 0051` §Compatibility (et `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`
§10) déclare :

```yaml
adversarial_governance_version: "1.1"
cutoff_run_key: "2026-07-28_1400"
cutoff_timestamp: "2026-07-28T14:00:00Z"
```

avec la règle :

> *At or after the cutoff: runs declare
> `adversarial_governance_version: "1.1"` in intake/closeout and
> carry a valid `adversarial` block, or a valid `A0` declaration.*

Le run M2 lui-même (`run_id: 2026-07-28_1400_m2-adversarial-loop-implementation`)
est exactement *au* cutoff. Il est donc soumis à cette règle.

Or `tools/vbb-loop-closure-check.py` (validateur canon) ne reconnaît
que `assurance_governance_version: "1.0"` et `schema_version: "1.0"`
— pas le champ `adversarial_governance_version: "1.1"`.

`07_CLOSEOUT.md` frontmatter déclare effectivement :

```yaml
assurance_governance_version: "1.0"
```

pour passer le validateur, contrevenant au cutoff qu'il vient
d'instaurer. La section `## Assurance` v1.1 (avec `adversarial_status`
et `certification_status` étendus) a été *rétrogradée* en narrative
hors bloc `ASSURANCE_STATUS` v1.0, précisément parce que le validateur
rejetterait un closeout v1.1 — c'est documenté dans la trace de
session.

**Conséquence.** Le premier run post-cutoff est le premier run non
conforme à son propre cutoff.

**Gravité.** **S1** — observable incorrectness ; incompatibilité
schéma/outillage dès le premier run.

**Impact.**

- Le validateur canon ne peut pas valider un closeout v1.1 jusqu'à
  M2-25 (`vbb-loop-closure-check.py` extension).
- Tout run post-cutoff qui suit est de facto non validable.
- L'argument « compatibilité ascendante préservée » (cf.
  `MIGRATION.md` §Compatibilité ascendante) est faux pour les
  *nouveaux* runs, seuls les pré-cutoff sont épargnés.

**Proposition de classification.**

- **Catégorie** : schéma 1.1 non livrable tant que M2-25 absent.
- **Effet immédiat** : P.R2 #4 (loop-closure) ne sait pas tester
  les champs v1.1. M2-BIS obligatoire avant tout `CERTIFIED`.

---

## Trouvaille #3 — Triple déclaration des énumérations schema 1.1

**ID.** ADVR-FALSIF-03

**Hypothèse falsifiée.** H1 (conflit d'autorité — partiel).

**Reproduction.**

M1-01 §Argumentation 4 dit explicitement :

> *« Tout statut, condition de verdict ou règle promotionnelle est
> défini dans `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`. Tout champ du
> schéma v1.1 (incluant les énumérations étendues, cf. ADVR-11)
> est défini dans `GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1. »*

Or les énumérations `gate_family ∈ {DESIGN, CERTIFICATION, ADVERSARIAL,
OTHER}` et `checkpoint ∈ {PRE_IMPLEMENTATION, POST_IMPLEMENTATION,
COUNTER_PROOF, CLOSEOUT}` apparaissent dans **trois** endroits :

1. `docs/adr/0051-...md` §1 (« Fourth gate family » + « Fourth
   declared checkpoint »).
2. `docs/GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 + v1.1 delta.
3. `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.1 (« A0 exclusion
   rule » cite les valeurs par leur nom).

Le split strict était censé prévenir cette duplication.

**Gravité.** **S2** — dette documentaire. Risque de désynchronisation
lors d'une future extension.

**Impact.** Une modification future des valeurs d'enum (ex. ajout d'un
cinquième `gate_family`) doit être propagée en trois endroits, sinon
l'un diverge et la cross-référence devient mensongère.

**Proposition de classification.**

- **Catégorie** : violation soft de CR#5 (« no parallel truth »).
- **Remédiation** : ADR 0051 §1 peut retirer l'énumération et citer
  GATE_ASSURANCE_GOVERNANCE.md §Schema 1.1 comme seule source.

---

## Trouvaille #4 — Dépôt solo mono-provider ne peut pas atteindre A2

**ID.** ADVR-FALSIF-04

**Hypothèse falsifiée.** H11 (cas limite dépôt solo) + H9 (migration
impossible).

**Reproduction.**

`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §3 :

```yaml
A2_DISTINCT_AGENT_PROXY:
  requirements:
    attacker_identity_disclosure: MANDATORY
    distinct_llm: MANDATORY
    distinct_system_prompt: MANDATORY
    cross_validation: REQUIRED
  external_review:
    cadence: QUARTERLY
    operator_constraint: "different llm family OR human"
```

M1-02 §Argumentation 4 dit :

> *« L'option (ii) [agent d'un autre fournisseur LLM avec un system
> prompt publié et non-dérivé] est la fallback viable pour les
> dépôts qui n'ont pas accès à (i) [humain tiers nommé]. »*

Cas limite : un dépôt solo qui n'a accès à *aucune* famille LLM
distincte (par exemple, contrainte de fournisseur unique, pas
d'humain externe disponible). Le contrat §3 ne fournit aucune
troisième option.

Pour ce dépôt : `A2_DISTINCT_AGENT_PROXY` est inutilisable ; aucun
`CERTIFIED` A2 n'est possible ; aucune certification n'est possible
sur les triggers A2 (auth, secrets, canon, etc.).

**Gravité.** **S2** — fragilité opérationnelle ; exclusion
structurelle d'une catégorie de dépôts.

**Impact.**

- Vibebackbone lui-même est solo-maintenu. Si la politique
  organisationnelle ou technique ne permet qu'un fournisseur LLM,
  Vibebackbone peut certifier des sujets A0/A1 mais aucun sujet A2.
- ADR 0051 liste « gouvernance canon » comme trigger A2 — donc
  ADR 0051 lui-même ne peut pas être CERTIFIED par Vibebackbone.

**Proposition de classification.**

- **Catégorie** : trou contractuel.
- **Remédiation** : ajouter un escape hatch au §3 pour le cas mono-
  provider, ou documenter explicitement l'exclusion.

---

## Trouvaille #5 — ADR 0050 non formellement supersedée

**ID.** ADVR-FALSIF-05

**Hypothèse falsifiée.** H10 (conflit ADR).

**Reproduction.**

ADR 0050 (pre-M2) déclare `gate_results[].gate_family ∈ {DESIGN,
CERTIFICATION, OTHER}` et `checkpoint ∈ {PRE_IMPLEMENTATION,
POST_IMPLEMENTATION, CLOSEOUT}`. M2 étend ces énumérations
(addition de `ADVERSARIAL` et `COUNTER_PROOF`) *sans* modifier ADR
0050 ni lui adjoindre un supersession_metadata.

La cross-référence ADR 0051 → ADR 0050 dans `linked_adrs` est de
type liste plate, pas un supersession formel :

```yaml
linked_adrs:
  - "0043-domain-verdict-runtime-status-orthogonality"
  - "0049-engineering-knowledge-governance"
  - "0050-design-certification-assurance-schema"
```

Pas de marque `supersedes: 0050` ou équivalent.

`docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` §Knowledge non-regression
exige pourtant :

> *Any semantic correction, weakening, extension or replacement:
> 1. creates a new OBSERVATION ;
> 2. becomes a new CANDIDATE and version ;
> 3. passes knowledge audit ;
> 4. passes mandatory independent review ;
> 5. receives a human decision ;
> 6. is integrated as the new canonical version ;
> 7. **explicitly supersedes, but never erases, the prior version**.*

L'extension des énumérations est une *extension* au sens de §7. Elle
devrait explicitement superseder ADR 0050 §Schema, ou amender ADR 0050
par une note. Aucune des deux n'a été faite.

**Gravité.** **S2** — déviation soft du cycle de supersession.

**Impact.** Un lecteur d'ADR 0050 qui n'a pas lu ADR 0051 reçoit
une information objectivement fausse (les énumérations étendues ne
sont pas là où ADR 0050 les annonce).

**Proposition de classification.**

- **Catégorie** : manquement procédural à ENGINEERING_KNOWLEDGE_GOVERNANCE §Knowledge non-regression.
- **Remédiation** : ajouter `supersedes: ["0050"]` au frontmatter
  d'ADR 0051, ou amender ADR 0050 par une note datée.

---

## Trouvaille #6 — Ambiguïté : chemin YAML des champs `witnessed_by`/`test_review`

**ID.** ADVR-FALSIF-06

**Hypothèse falsifiée.** H5 (ambiguïté normative).

**Reproduction.**

`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §5.3 condition 6.3.13 :

> *For every `CONFIRMED` finding at level `A2`, the non-regression
> lock has `witnessed_by` (distinct from `discovered_by`) and
> `test_review` (PASS|FAIL verdict by second agent or human) populated.*

Le texte ne précise pas le chemin YAML. `M1_DECISIONS.md` §M1-05
spécifie `non_regression.witnessed_by` et `non_regression.test_review`
— mais ce n'est pas reporté dans le canon M2.

`ENGINEERING_KNOWLEDGE_GOVERNANCE.md` ne le mentionne pas non plus.
`FINDING.md.template` (M2-26) est différé, donc aucun lieu canonique
ne porte le schéma YAML.

**Gravité.** **S3** — latent. Aucun finding ne peut être émis en
A2 aujourd'hui (validator absent), donc l'ambiguïté ne bloque pas
immédiatement.

**Impact.** Quand M2-26 livre `FINDING.md.template`, deux lectures
sont possibles du canon : un ingénieur peut légitimement placer
`witnessed_by` à `finding.witnessed_by` (top-level) ou
`finding.non_regression.witnessed_by` (nested). Sans canon, c'est
l'arbitraire du premier implémenteur.

**Proposition de classification.**

- **Catégorie** : dette de schéma.
- **Remédiation** : ajouter une ligne à §5.3 condition 6.3.13
  mentionnant le chemin YAML canonique.

---

## Trouvaille #7 — Incohérence §7.3 : dashboard read-only qui « triggers » une mutation

**ID.** ADVR-FALSIF-07

**Hypothèse falsifiée.** H8 (règles CERTIFIED/SUSPENDED incohérentes).

**Reproduction.**

`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §7.3 :

> *If `now - last_reviewed > cadence`, OR if a `webhook` target
> has not emitted a signal for 90 days, **the next pass of
> `tools/vbb-status-dashboard.py`** (or `tools/vbb-loop-closure-check.py`)
> **triggers an automatic transition `CERTIFIED → SUSPENDED`**.

Le skill `t-vbb-status-dashboard` (cf. `skills/vibebackbone/t-vbb-status-dashboard/SKILL.md`)
est explicitement « read-only terminal dashboard ». Une mutation
depuis un outil read-only contredit la désignation read-only.

**Gravité.** **S1** — operational incorrectness. La règle ne peut
pas s'exécuter comme écrite.

**Impact.**

- §5.3 condition 6.3.10 exige `certification.revocation_mechanism`
  déclaré. Si ce mécanisme est `cron:<expr>` ou `manual:<cadence>`,
  la transition ne dépend pas du dashboard — le cron la fait
  directement. Mais le texte §7.3 dit le contraire.
- Si le mécanisme est `webhook:<target>`, le webhook n'a pas de
  cadence propre : il émet quand quelque chose se passe. Si rien ne
  se passe pendant 90j, le silence est détecté *par* le dashboard,
  mais la transition reste à faire *par* quelqu'un.

**Proposition de classification.**

- **Catégorie** : mécanisme de §7.3 non exécutable.
- **Remédiation** : §7.3 doit déclarer un mode `mutation: true`
  exceptionnel pour le dashboard, ou désigner `vbb-loop-closure-check.py`
  comme seul effecteur, et le dashboard comme pur alerteur.

---

## Trouvaille #8 — Comportement du lecteur v1.0 face à `ADVERSARIAL` non spécifié

**ID.** ADVR-FALSIF-08

**Hypothèse falsifiée.** H4 (compatibilité ascendante).

**Reproduction.**

`GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 (v1.1 delta) :

> *A v1.0 reader ignores the new top-level blocks and statuses.
> Where it encounters a v1.1 enum value (`gate_family: ADVERSARIAL`
> or `checkpoint: COUNTER_PROOF`), the reader is **non-conformant**
> by explicit declaration.*

`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §0 :

> *`PASS_ADVERSARIAL` is **bounded evidence**, not proof.*

Le texte dit que le lecteur v1.0 est « non-conformant » quand il voit
`ADVERSARIAL`. Mais le **comportement attendu** n'est pas spécifié :

- (a) crash (lève une exception) ?
- (b) ignore silencieux (la gate est traitée comme non classifiée) ?
- (c) re-injection dans `OTHER` — explicitement interdite.
- (d) résultat dépendant de l'implémentation (non déterministe) ?

Trois comportements sont concevables, un seul est interdit, aucun
n'est imposé. C'est précisément le type d'ambiguïté qu'ADR 0050 §Schema
v1.0 avait résolu pour les valeurs pré-M2.

**Gravité.** **S2** — ambiguïté en fail-closed.

**Impact.** Tout projet satellite adoptant v1.0 et recevant un
artefact v1.1 (par exemple via une dépendance qui migre) a un
comportement indéterminé.

**Proposition de classification.**

- **Catégorie** : trou de spécification.
- **Remédiation** : §Schema 1.1 doit déclarer le comportement
  fail-closed exact : « a v1.0 reader MUST raise
  `UnsupportedSchemaError` on `gate_family: ADVERSARIAL` ».

---

## Trouvaille #9 — Migration impossible : canon post-cutoff structurellement incertifiable

**ID.** ADVR-FALSIF-09

**Hypothèse falsifiée.** H9 (migration impossible) + H6 (conflit statuts).

**Reproduction.**

`§5.3 condition 6.3.2` exige pour `CERTIFIED` :

> *`adversarial_status` ∈ {`PASS_ADVERSARIAL`, `NOT_REQUIRED` (A0
> valide + aucun trigger A1/A2)}.*

`§1.1` interdit A0 sur gouvernance canon.

`§1.2` exige A1 minimum sur gouvernance canon (interne contract,
tool, CLI, schema-adjacent change).

`§1.2` exige A2 sur gouvernance canon « qui gate d'autres travaux ».

Conséquence pour le canon M2 lui-même :

| Sujet post-cutoff | Niveau minimum | adversarial_status possible | CERTIFIED ? |
|---|---|---|---|
| `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (gate authority) | A2 | `PASS_ADVERSARIAL` requis | **Impossible** jusqu'au validateur M2-24 |
| `GATE_ASSURANCE_GOVERNANCE.md` (gate tools) | A2 | idem | **Impossible** |
| `PILOTAGE.md` (gates other work) | A2 | idem | **Impossible** |
| `CONVENTIONS.md` (quality standards) | A2 | idem | **Impossible** |
| `ADR 0051` (decision record) | A1 | `PASS_ADVERSARIAL` requis | **Impossible** |

`M2_DEFERRED_ITEMS.md` admet que `tools/vbb-adversarial-gate.py`
n'est pas livré (M2-24, Tier 3). Tant que M2-24 n'existe pas,
*aucun* des sujets A1/A2 post-cutoff ne peut être certifié, parce
que `PASS_ADVERSARIAL` ne peut pas être délivré (pas de validateur).

**Gravité.** **S1** — migration blocked.

**Impact.**

- ADR 0051 §Compatibility dit : *« Consumer projects adopt this
  contract only through their own future governed change »*. Mais
  Vibebackbone lui-même, qui est son propre premier consumer,
  n'a aucun chemin pour certifier son propre canon.
- C'est un **trou logique** : un système qui exige la certification
  de ses propres composants sans livrer l'outil qui la délivre.
- Le bootstrap auto-référentiel ne se ferme pas tant que M2-BIS
  n'est pas exécuté.

**Proposition de classification.**

- **Catégorie** : fail-closed incomplet au niveau méta.
- **Remédiation** : ADR 0051 §Compatibility doit explicitement
  reconnaître que les sujets A1/A2 post-cutoff sont
  `NOT_CERTIFIED` par défaut (non `UNASSESSED_LEGACY`, qui est
  réservé au pré-cutoff), et ce *jusqu'à* la livraison de
  M2-24. Cette reconnaissance est absente.

---

## Hypothèses non-falsifiées (avec bornes)

### §H2 — Boucle impossible

**Attaques lancées :**

1. Conditions §5.3 6.3.13 + §7.4 re-acquisition simultanées (3 triggers #1/#2/#4 firing). Falsification : §7.4 libère la cause de suspension d'abord. Pas de boucle.
2. A2_PROXY + counter-proof distinct (3 agents minimum). Falsification : aucun minimum n'est imposé sur les LLM families (seulement l'attaquant). Faisable.
3. SLA breach (trigger #6) sans opérateur disponible. Falsification : §7.4 suppose remédiable — voir Trouvaille #10 ci-dessous comme zone grise.

**Limites.** L'audit ne peut pas tester le runtime : la boucle n'est
pas encore instanciée (M2-24 absent). Les attaques sont purement
textuelles.

**Conclusion.** Hypothèse **non falsifiée** dans le périmètre
statique ; aucun finding supplémentaire ici (la Trouvaille #10 capture
l'asymétrie).

### §H12 — Inflation documentaire

**Attaques lancées :**

1. Volume total des nouveaux canoniques vs existant : ~47 KB nouveau
   vs ~6 KB pour GATE_ASSURANCE canon existant.
2. Ratio lignes-spécifiées-M1 vs lignes-produites-M2 : M1 spécifiait
   ~830 lignes ; M2 en produit ~960. Sur-spécification ≈ 0.
3. Fragmentation : 3 documents pour comprendre une seule condition
   (ADR 0051 §X → ADVERSARIAL §Y → GATE_ASSURANCE §Z).

**Falsification.** Le volume est requis par M1 (M1 a tranché 6
décisions ; chaque décision porte du texte). La fragmentation est
une dette d'expérience de lecture, pas une inflation.

**Conclusion.** Hypothèse **non falsifiée** — le volume et la
fragmentation sont *structurellement* nécessaires à ce que M1 a
prescrit.

### §H5.b — Terme `coherence_review`

**Attaque.** Cherché dans tous les fichiers M2 lus : non trouvé.
Pas un finding.

---

## Trouvaille #10 — §7.4 suppose que toute cause de suspension est remédiable

**ID.** ADVR-FALSIF-10

**Hypothèse falsifiée.** H8 (asymétrie CERTIFIED ↔ re-acquisition).

**Reproduction.**

`§6` : 6 triggers de perte (nouveau finding, corpus_version change,
scope change, ACCEPTED_RISK expiré, reopen trigger, SLA breach).

`§7.4` :

> *Re-acquisition requires re-execution of all 13 conditions of §5.3
> **and release of the cause of suspension**.*

Cas pathologiques :

- Trigger #1 (nouveau finding CONFIRMED dans le scope). Si le
  finding est un défaut de design fondamental (par exemple, une
  hypothèse de sécurité invalidée), `release the cause` peut
  signifier *redesign complet* — pas une remédiation bornée.
- Trigger #4 (ACCEPTED_RISK expiré). Si la cause de l'acceptation
  est structurelle (par exemple, dépendance dépréciée), le
  renouvellement est impossible.
- Trigger #6 (SLA breach faute d'opérateur). Si aucun opérateur
  ne veut maintenir la certification, aucune remédiation n'est
  possible — la certification est *de facto* terminale.

§7.4 ne distingue pas entre *cause remédiable* et *cause
irreversible*. Le texte suppose implicitement la première.

**Gravité.** **S3** — operational gap, non bloquant pour les cas
typiques mais observable aux limites.

**Proposition de classification.**

- **Catégorie** : edge case documenté.
- **Remédiation** : §7.4 doit prévoir un état terminal
  `CERTIFICATION_TERMINATED` (distinct de `SUSPENDED`) pour les
  causes irreversibles.

---

## Limites de l'audit R0

Déclaré honnêtement, conformément aux contraintes :

| Limite | Raison |
|---|---|
| Pas de validation runtime | `vbb-adversarial-gate.py` (M2-24) absent ; impossible de tester le comportement d'exécution |
| Pas de re-run P.R2 | Audit est lecture seule ; je ne re-déclenche pas `pytest` ni `vbb-loop-closure-check.py` (déjà fait en M2 et documenté PASS) |
| Pas de revue par un second acteur | Auto-revue disclosed PARTIAL ; voir 03_INDEPENDENT_REVIEW.md |
| Périmètre borné aux 8 fichiers M2 | M2_DEFERRED_ITEMS.md et autres différés explicitement hors audit |
| Pas de modification des fichiers | Conformément aux contraintes R0 ; aucun correctif proposé en pratique |
| Pas d'arbitrage | Conformément aux contraintes R0 ; severity assessments sont indicatives |

R0 n'a pas la prétention d'être *exhaustif*. Il démontre que
*plusieurs* falsifications sont possibles ; il n'élimine pas la
possibilité de falsifications supplémentaires qu'un audit de
runtime ou une revue humaine détecteraient.

---

## Résumé

**9 falsifications confirmées** + **1 falsification annexe** sur
**12 hypothèses** :

| Sévérité | Findings |
|---|---|
| S0 | ADVR-FALSIF-01 |
| S1 | ADVR-FALSIF-02, 07, 09 |
| S2 | ADVR-FALSIF-03, 04, 05, 08 |
| S3 | ADVR-FALSIF-06, 10 |
| (none) | §H2, §H12, §H5.b (documentés non-falsifiés) |

**Verdict R0.** L'implémentation M2 contient au moins une violation
canonique de rang S0 (le self-contournement A0) et trois violations
S1 qui rendent `CERTIFIED` inatteignable pour le canon M2 lui-même
tant que M2-BIS n'est pas livré. Ces falsifications sont
*suffisantes* pour bloquer la certification immédiate d'ADR 0051.

**Aucun finding ne nécessite de modification du canon pendant
l'audit** (conformément aux contraintes R0) ; les propositions de
remédiation sont indicatives, à arbitrer hors R0.