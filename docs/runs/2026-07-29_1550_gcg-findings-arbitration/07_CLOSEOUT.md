---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "PARTIAL"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
knowledge_harvest: "OBSERVATION_RECORDED"
kind: "HANDOFF"
subject_kind: "GOVERNANCE_FINDINGS_ARBITRATION"
adversarial_level: "A2"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T13:50:00Z"
ended_at: "2026-07-29T14:55:00Z"
next_phase: null
artifacts_consumed:
  - "01_INTAKE.md, 02_FINDINGS_REGISTER.md, 03_DEPENDENCY_AND_ARBITRATION_MAP.md, 04_PLAN.md, 04_INDEPENDENT_ARBITRATION_REVIEW.md, 05_DECISIONS_REQUIRED.md, 05_EXECUTION.md, 06_RESUMPTION_SEQUENCE.md"
artifacts_produced:
  - "07_CLOSEOUT.md (this file)"
---

# 07_CLOSEOUT — GCG-ARB-01

## Résultat

L'espace de décisions est constitué. **36 constats** issus de cinq sources sont
réunis dans un registre unique, classés par nature et par autorité de clôture,
ordonnés par un graphe de dépendances, et convertis en **13 décisions** dont
aucune n'est prise ici. Une séquence de dix runs est proposée, aucun n'est
ouvert.

Un constat **P0 nouveau** est né du run : `GCG-36`, quatrième voie de
blanchiment, trouvée par la revue indépendante de l'arbitrage.

## Verdict global

Verdict du dépôt inchangé : `PARTIAL`. Le verdict mesuré du GCG reste `2/15`,
exit 2. Ce run n'ajoute aucune capacité, ne ferme aucun défaut, et **augmente**
la quantité de non-conformité qualifiée.

Verdict de viabilité du modèle, dérivé en `03` §7 :

```
VERDICT: REQUIRES_REDESIGN
```

conditionnel et réversible, avec la branche de repli
`DUPLICATES_EXISTING_CANON` vers laquelle les mesures actuelles penchent.

---

## 1. Ce qui est factuellement établi

Mesuré dans ce run, reproductible, indépendant de toute décision.

| Fait | Mesure |
|---|---|
| `classify_run` teste `HISTORICAL_VALID` (ligne 176) **avant** `OVERCLAIM` (ligne 197) — un renommage annule la catégorie non migrable | lecture du code + démonstration de la revue sur 3 runs synthétiques |
| le commentaire lignes 195-196 affirme la primauté d'`OVERCLAIM` que l'ordre des branches rend fausse | lecture du code |
| **aucune signature dans l'historique** : 243 commits sur 244 en `%G? = N` | `git log --format='%G?'` |
| **14 closeouts sur 157 suivis** ont plus d'un commit ; `b9084e2` a écrit `verdict: PASS`, `PASS_ADVERSARIAL` et `CERTIFIED` **après** la clôture du run | boucle `git log` + `git log -p` |
| `enforcement_effective_from` n'est déclaré **nulle part** au canon ; la borne n'existe qu'à `vbb-governance-compat.py:105` | `grep -rn` |
| les bornes du code sont des `datetime` **sans fuseau**, alors que le canon déclare `cutoff_timestamp` en UTC | lecture du code |
| **75 runs sur 164** positionnent leur identité à plus d'une minute de leur `started_at`, écart max 22,1 h | sonde Python, 3 résolveurs |
| les **9** closeouts déclarant une disposition de connaissance positive ne portent **aucune** section Knowledge Harvest | `grep -ci harvest` |
| l'obligation de corpus se déclenche sur un bloc adverse de closeout, donc **jamais** sur un constat produit hors run | lecture de `tests/test_corpus_mandatory.py` |
| `LEDGERABLE` inclut `HISTORICAL_VALID` ; `historical_debt` ne le somme pas ; `applicable` l'exclut | lecture du code |
| scan complet : **0,68 à 0,91 s**, contre « plusieurs secondes » affirmé par le modèle §6.2 | `/usr/bin/time` ×3, deux mesureurs |

## 2. Ce qui a été arbitré

**Classification.** 36 constats classés par nature, avec déclaration des quatre
cas où la taxonomie ne discrimine pas, et une scission justifiée (GCG-01 défaut
de modèle / GCG-21 défaut de preuve). L'axe réellement structurant n'est pas la
nature mais **qui peut clore** ; il est ajouté et corrigé après revue.

**Ordonnancement.** Deux règles dérivées : une correction dont la sémantique
dépend d'une décision ouverte est invalide même si elle est correcte ; une
décision qui peut retirer le périmètre passe avant celles qui le supposent.
Neuf relations vérifiées, dont **trois se révèlent différentes de l'attendu** :
GCG-14 n'est pas une correction mécanique (il ouvre GCG-03) ; GCG-27 change la
*nature* du P0 et non seulement sa gravité ; D4 ne peut pas précéder D1/D2.

**Séparation normatif / technique.** 18 constats sur 36 exigent une décision
normative. **8 portent un risque de réparation défensive caractérisé** — leur
correction technique existe et déciderait silencieusement. Neuf sont des
corrections mécaniques, dont cinq exécutables immédiatement.

**Ce qui a été retiré ou inversé après revue**, sans effacement :

- le chiffre « 5 catégories sur 8 dupliquent le canon » — la table sous-jacente
  assimilait des classifications dérivées à des statuts déclarés ;
- mes recommandations pour D1 et D2 — elles détectaient sans attester, dans un
  dépôt sans signature ;
- ma correction de GCG-22 — elle surestimait la couverture, le mode d'échec
  exact que le constat reproche au modèle ;
- la divergence V3 — une erreur de mesure figée en désaccord épistémique ;
- la dérivation du verdict — incohérente, reconstruite sur d'autres motifs ;
- trois conditions d'arrêt sur dix — infalsifiables ou déjà remplies.

## 3. Ce qui nécessite encore une décision de l'utilisateur

Aucune n'est prise. Détail et options en `05_DECISIONS_REQUIRED.md`.

| # | Décision | Bloque |
|---|---|---|
| **D0** | la certification v1.1 publiée est-elle soutenue ? | P0, R-0 |
| **D1** | qu'est-ce que la position d'un artefact ? | tout le temporel |
| **D2** | quelle population, et comment l'immuabilité est-elle établie ? | tout l'historique |
| **D3** | où les deux bornes sont-elles déclarées, avec quelle unité et quelle inclusivité ? | I8, câblage CI |
| **D4** | quelle préséance entre statut déclaré et classification dérivée ? | vérité parallèle |
| **D5** | qu'est-ce qu'une revendication, et sa structure de validation ? | `OVERCLAIM`, GCG-28 |
| **D6** | l'arbitration peut-elle attribuer une disposition non-dette ? | ledger |
| **D7** | que signifie l'absence du porteur de preuve ? | `PENDING_LIFECYCLE` |
| **D8** | comment épingle-t-on un constat produit hors run ? | **ce run en est une instance** |
| **D9–D11** | questions normatives héritées du run `1021` | canon adverse |
| **D12** | le chantier progresse-t-il sans acteur A2 distinct ? | toute certification |

**Cinq abstentions déclarées** : D0 (arbitrage A/B), D4, D6, D8, D12. Sur
chacune, l'agent écarte explicitement l'option « statu quo » et s'arrête là.

## 4. Ce qui reste bloqué

- **Le ledger, le Migration Engine et le câblage CI** — bloqués jusqu'à R-6
  inclus. Enregistrer des dispositions contre des classifications provisoires
  produirait la dette que le modèle prétend gouverner.
- **L'ADR 0052** — non rédigeable avant R-9, et peut-être jamais si D4 conclut à
  l'absorption dans ADR 0051.
- **Six corrections mécaniques identifiées et non appliquées** (contrainte C3),
  dont **GCG-36 qui est P0** et dont dépend la preuve du P0 de D0.
- **GCG-36 n'est épinglé par aucune entrée de corpus** — écart déclaré en
  `05_EXECUTION.md` §4. Le déclarer `CONFIRMED` dans le bloc adverse forcerait à
  écrire du code contre C3 ; le rétrograder serait « rétrograder un niveau pour
  obtenir le vert ». Le registre est son seul porteur. **C'est GCG-25
  s'appliquant à ce run lui-même, et cela rend D8 urgente.**
- **`G7`** — différé par décision explicite de l'utilisateur.
- **R3, R4, R5** du plan de remédiation du run `1021` restent entiers.

## 5. Niveau réel d'indépendance obtenu

| Dimension | Obtenu | Manquant |
|---|---|---|
| contexte | **isolé** — nouveau contexte, aucun accès à la conversation de l'agent principal | — |
| dépôt | **lecture seule** vérifiée ; démonstration en répertoire temporaire | — |
| orientation du mandat | **non orientée** — consigne explicite de ne pas se calibrer sur l'attente de l'agent principal | — |
| famille de LLM | — | **identique** (`claude-opus-5`) |
| prompt système | — | **identique** |
| acteur humain distinct | — | **absent** |

`A2_DISTINCT_AGENT_PROXY` **n'est pas satisfait**. Ce qui a été obtenu est une
**isolation de contexte**, et son rendement est mesurable : la revue a produit
un P0 nouveau, réfuté quatre de mes énoncés et invalidé trois conditions
d'arrêt. C'est un argument en faveur de l'isolation de contexte comme dispositif
utile ; ce n'est pas un substitut à la distinction d'acteur, et il n'est pas
présenté comme tel.

La revue déclare elle-même cette limite, sans y être invitée.

## ASSURANCE_STATUS

```yaml
ASSURANCE_STATUS:
  schema_version: "1.1"
  subject: "GCG findings arbitration, 5d4fe34 -> closeout SHA"
  gate_results:
    - gate_id: "vbb-gate-check-adr-poc-integration"
      gate_family: "DESIGN"
      checkpoint: "PRE_IMPLEMENTATION"
      subject: "ADR + POC + Integration gate before any code (Critical Rule 11)"
      verdict: "FAIL"
      evidence:
        - "CAN_CODE_START: False, blocker MISSING_POC"
        - "no code written: tools/, tests/, scripts/, docs/REFERENCE/ unchanged"
      reasons:
        - "the run carries no POC and wrote no code; the gate is honored by abstention, not by derogation"
        - "this is the difference with deviation G9 of run 1050, where code was touched under the same gate verdict"
    - gate_id: "independent-arbitration-review"
      gate_family: "DESIGN"
      checkpoint: "CLOSEOUT"
      subject: "the classification and arbitration reviewed by a context-isolated agent"
      verdict: "PASS"
      evidence:
        - "11 findings returned, none dismissed on the facts"
        - "6 re-verified by the principal agent: branch order, git signatures, closeout denominator, harvest measurement"
        - "4 statements of the arbitration refuted and corrected, none erased"
        - "3 of 10 stop conditions found unfalsifiable or already met, all rewritten"
      reasons:
        - "the review was mandated to attack the arbitration and did; the gate records that it produced substantive change"
    - gate_id: "vbb-governance-compat"
      gate_family: "CERTIFICATION"
      checkpoint: "CLOSEOUT"
      subject: "post-cutoff run population against adversarial 1.1"
      verdict: "FAIL"
      evidence:
        - "exit 2, current conformance 2/15, unchanged by this run"
      reasons:
        - "expected: the instrument stays red and unwired; C8 forbids laundering it"
        - "GCG-36, once repaired, will increase the number of blocking artifacts"
  implementation_authorization:
    status: "NOT_AUTHORIZED"
    required_gate_ids:
      - "vbb-gate-check-adr-poc-integration"
    reasons:
      - "the gate returned can_code_start=false (MISSING_POC) and no code was written"
      - "six mechanical corrections were identified and deliberately not applied (constraint C3)"
      - "NOT_APPLICABLE was written first and is not a value the schema admits; NOT_AUTHORIZED is both valid and more accurate — implementation was not authorized, and none occurred"
  final_status: "HANDOFF"
```

## Bloc adverse

```yaml
adversarial:
  level: "A2"
  campaign_ref: "docs/runs/2026-07-29_1550_gcg-findings-arbitration/04_INDEPENDENT_ARBITRATION_REVIEW.md"
  corpus_version: "1.2.0"
  exploration_performed: true
  surfaces_declared:
    - "the findings register as a place to bury a finding by regrouping it"
    - "the taxonomy as a way to make a normative decision look technical"
    - "the dependency graph as a way to defer what should be repaired now"
    - "the viability verdict as a self-serving conclusion"
    - "the stop conditions of the proposed runs as unfalsifiable success guarantees"
  surfaces_unexplored:
    - "the 14 findings of 2026-07-28_2200 (deferred to R-7)"
    - "whether a fifth laundering route exists (mandated to R-5)"
    - "the substance of GCG-C1, GCG-C2, GCG-C5, R3/R4/R5"
    - "any rule set outside this repository"
  residual_uncertainty: |
    The review found a fourth laundering route by checking a coverage claim I
    had just corrected in the wrong direction. That is a strong signal that the
    search was not exhaustive on either side: neither review was systematic
    about the classification order of `classify_run`, and the one that found it
    found it incidentally. A fifth route is not excluded, and R-5 is mandated to
    look for one.
  defender_identity:
    agent: "claude-opus-5 (Claude Code)"
    llm: "claude-opus-5"
    system_prompt_version: "claude-code-2026-07"
  attacker_identity:
    agent: "claude-opus-5 (Claude Code, isolated subagent a2f715163e55cc42e)"
    llm: "claude-opus-5"
    system_prompt_version: "claude-code-2026-07"
    session: "7d41772d-7943-4130-8c25-55882072a2b2"
  findings: []
  verdict: "FINDINGS_OPEN"
  non_claim: |
    No PASS_ADVERSARIAL is claimed. Attacker and defender share the LLM family
    and the system prompt, so A2_DISTINCT_AGENT_PROXY is not satisfied. What was
    obtained is context isolation, whose yield is measurable (one new P0, four
    refuted statements, three invalid stop conditions) and which is reported as
    what it is, not as a substitute for a distinct actor.

    `findings: []` is deliberate and is not an omission. This run conducts no
    adversarial campaign: it arbitrates findings produced elsewhere. GCG-36 was
    brought to it by a review, not discovered by an attack of its own. The
    finding is registered in 02_FINDINGS_REGISTER.md, which is its durable
    carrier.
  corpus_obligation_conflict: |
    GCG-36 is CONFIRMED, P0, and born in this run. Declaring it here would
    trigger the corpus obligation (ADVERSARIAL_ASSURANCE §9 destination 6) and
    force writing code, against constraint C3 of the request. Downgrading its
    confidence to disarm the obligation would be "downgrading a level to obtain
    green", forbidden by the standing constraint and by C4. The conflict is
    declared rather than resolved silently: GCG-36 is unpinned, and this is
    finding GCG-25 applying to the run that registered it. Decision D8 is the
    canonical resolution and is now urgent. The obligation is redirected to
    run R-A, which repairs GCG-36 and must carry the pin.
  certification:
    status: "NOT_CERTIFIED"
  certification_blocker: |
    A2 requires an actor distinct by LLM family, system prompt and
    provider-or-human. None was available. Context isolation was obtained and
    was productive; it does not satisfy the proxy contract.
```

## Vérification P.R2

| # | Commande | Résultat |
|---|---|---|
| 1 | `vbb-architecture.py lint` | non exécuté — aucun bloc d'architecture touché |
| 3 | `vbb-contract-lint.py` | PASS — 0 error, 1 warning non bloquant (`F12`) |
| 4 | `vbb-loop-closure-check.py <run_id> --strict --validate-plan` | PASS — après correction de deux erreurs de schéma de mon propre `ASSURANCE_STATUS` (`checkpoint: POST_ANALYSIS` inexistant ; `implementation_authorization: NOT_APPLICABLE` non admis) |
| 5 | `ruff check tools tests` / `ruff format --check tools tests` / `mypy tools` | PASS |
| 5 | `pytest tests/ -q` | PASS — 447 passed, 1 skipped |
| 5b | `vbb-adversarial-gate.py <run_id> --strict` | FAIL attendu — A2 sans acteur distinct |
| 5b | `pytest tests/adversarial_corpus/ -q` | PASS |
| — | `bash scripts/vbb-ci-local.sh` | **16 passed, 0 failed, 0 warnings** |
| — | `vbb-credentials-gate.py` | PASS — 0 finding |
| — | `vbb-governance-compat.py --strict` | **FAIL attendu** — exit 2, `2/16` |

Les deux `FAIL` sont les résultats corrects. Le premier enregistre l'absence
d'acteur distinct ; le second est la mesure que ce run avait interdiction de
blanchir.

**Ce run entre dans la population qu'il mesure et s'y classe
`CURRENT_NONCOMPLIANCE`**, bloquant, faute d'acteur A2 distinct — exactement
comme les quatre runs GCG qui l'ont précédé. La conformité passe de `2/15` à
`2/16` : le dénominateur augmente, le numérateur non. **Elle ne s'améliore pas
et ne devait pas.**

Effet de bord vérifié : `PENDING_LIFECYCLE` retombe de 1 à 0. Ce run en était
l'unique occupant tant qu'il était ouvert — observation de la revue (RA-F-K),
qui notait que la baseline de `01` §5 n'était pas la mesure neutre qu'elle
paraissait. La clôture du run la résout.

## Knowledge Harvest

Trois candidats, tous en `OBSERVATION`. Aucun n'est promu vers `CONVENTIONS.md`
ou `AGENTS.md` — cela exigerait le parcours ADR 0049.

1. **Un arbitrage protège ce qu'il arbitre, et il le fait dans ses remèdes plus
   que dans ses constats.** Mes constats sur le modèle étaient durs et exacts ;
   mes *recommandations* pour les réparer étaient des réparations défensives —
   détecter les contre-exemples connus sans établir la propriété. Le test
   déclaré-vs-établi, que j'appliquais avec force aux constats, ne s'était pas
   retourné vers mes propres options. **Un run d'arbitrage doit appliquer ses
   propres critères à ses recommandations, pas seulement à son objet.**

2. **Une condition d'arrêt qui ne peut pas être atteinte est pire qu'une
   absence de condition.** Trois des dix runs proposés avaient une sortie en
   échec inatteignable par les options que le même document recommandait. Ils
   auraient rapporté un succès avec le défaut intact — et l'auraient rapporté
   *avec preuve*. Une condition d'arrêt doit être testée contre les options
   qu'on recommande, pas seulement contre l'objectif qu'on vise.

3. **Corriger un aveu d'honnêteté est plus risqué que l'écrire.** Le tableau de
   couverture du modèle était faux ; ma correction l'était aussi, et dans le sens
   de la **surestimation** — le mode d'échec exact que le constat reprochait.
   Un document qui déclare ce qu'il ne garantit pas achète de la confiance sur
   cette phrase ; corriger cette phrase demande la même vérification que
   n'importe quelle revendication positive, et non moins.

Portée : observations d'un run sur un dépôt. Pas des règles canoniques.

## Points ouverts

- **13 décisions** en attente d'arbitrage humain, `05_DECISIONS_REQUIRED.md`.
- **`GCG-36`** — P0, quatrième voie de blanchiment, non épinglé par un corpus.
- **`GCG-26` / `GCG-27`** — P0 sur la certification v1.1 publiée, inchangés, et
  dont la **preuve** dépend désormais de la réparation de `GCG-36`.
- **Six corrections mécaniques** identifiées et non appliquées (C3).
- **`A2_DISTINCT_AGENT_PROXY`** jamais satisfait sur les cinq runs du chantier.
- **`G7`**, **R3/R4/R5**, **`AUD-F8`** — portés, non arbitrés.
- **Le modèle reste `PROPOSED`** et en lecture seule. Aucune v3 n'est amorcée.

## FINAL_STATUS

```yaml
FINAL_STATUS: HANDOFF
reason: |
  L'espace de décisions est constitué et opposable : 36 constats, 13 décisions,
  un graphe de dépendances, une séquence de reprise dont les conditions d'arrêt
  sont désormais falsifiables. Ce qui manque n'est pas du travail d'analyse :
  ce sont treize décisions qu'aucun agent n'a autorité pour rendre, et un acteur
  A2 distinct que ce run ne peut pas fournir sans le simuler. COMPLETE serait
  une revendication d'assurance non tenue.
implementation_complete: false
verification_complete: true
adversarial_certification: false
next_action: |
  Arbitrage humain, dans cet ordre : (1) autoriser R-A, qui répare GCG-36 sans
  aucune décision préalable — la preuve du P0 en dépend ; (2) trancher D0 sur la
  certification v1.1 publiée ; (3) trancher D1 et D2, qui décident si le modèle a
  encore un sujet. Puis seulement : D4, D3, les prédicats, et la question de
  l'ADR. Rien dans cette séquence n'autorise le ledger, le Migration Engine ou
  le câblage CI avant R-6.
```
