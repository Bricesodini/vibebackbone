---
run_id: "2026-07-28_1200_m1-adversarial-loop-normative-arbitration"
phase: "M1_DECISIONS"
voie: "AUDIT"
status: "READY"
kind: "ARBITRATION_RUN"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
agent: "external arbitrator (distinct session, distinct provider)"
decisions_count: 6
decisions_unresolved: 0
artifacts_produced:
  - "M1_DECISIONS.md"
  - "M2_MODIFICATIONS.md (embedded §8)"
---

# M1 — Décisions normatives arbitrées

> **Statut.** Chaque décision est tranchée et applicable au run d'implémentation
> M2. Aucune n'écrit dans le canon : l'écriture des ADR, du schéma 1.1, des
> templates et des validateurs est différée à un run M2 séparé qui consommera
> cette liste de décisions comme contrat d'entrée.

---

## M1-01 — Autorité canonique (COND-05)

### Options comparées

| # | Option | Description | Coût | Risque |
|---|---|---|---|---|
| A | Nouvelle autorité unique | Toutes les règles adversariales dans `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` ; `GATE_ASSURANCE_GOVERNANCE.md` cité mais non modifié. | Croissance du canon (+1 fichier ~600 lignes). | Risque d'inertie : `GATE_ASSURANCE_GOVERNANCE.md` reste muet sur le 4ᵉ gate family. |
| B | Extension de `GATE_ASSURANCE_GOVERNANCE.md` uniquement | Aucune nouvelle autorité. Le canon croît *dans* le fichier existant (~+300 lignes). | Pas de nouveau fichier. | Dilution sémantique : un seul fichier porte 4 gate families + 4 statuts + closure logic + migration policy. |
| C | **Split strict** | Nouvelle autorité `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` pour : statuts, lifecycle, matrice de criticité, verdict conditions, corpus contract, promotion matrix. `GATE_ASSURANCE_GOVERNANCE.md` étendu **uniquement** pour : schéma v1.1, checkpoint `COUNTER_PROOF`, règle `closure_evaluation`. | Croissance +1 fichier modéré (~350 lignes) + extension minimale du gate canon (+~80 lignes). | Deux autorités à maintenir ; risque de désynchronisation. Mitigé par les références croisées explicites. |
| D | Split distribué (rejet de la revue indépendante) | Règles réparties dans `PILOTAGE.md`, `CONVENTIONS.md`, `GATE_ASSURANCE_GOVERNANCE.md`, `pre-merge-gate.md`. | Aucun nouveau fichier. | **CR#5 violation** : canon dupliqué, lectures parallèles possibles. Rejetée. |

### Décision retenue

**Option C — split strict.**

### Argumentation

1. **Préserve la sémantique.** `GATE_ASSURANCE_GOVERNANCE.md` reste canonique
   pour le *schéma et l'agrégation* ; la nouvelle autorité porte le *domaine
   métier* (adversarial assurance). Cette séparation est la même que celle
   déjà en vigueur entre `GATE_ASSURANCE_GOVERNANCE.md` (assurance générique)
   et `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` (knowledge loop) — un précédent
   de canon.
2. **Lève CR#5** (`no parallel truth`) en garantissant une seule autorité
   par concept. Le schéma vit à un endroit, les règles métier à un autre.
3. **Limite la duplication.** Tout statut, condition de verdict ou règle
   promotionnelle est défini dans `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`.
   Tout champ du schéma v1.1 (incluant les énumérations étendues, cf.
   ADVR-11) est défini dans `GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1.
4. **Traçabilité des énumérations étendues** (réponse à ADVR-11). Le
   paragraphe §Schema 1.1 de `GATE_ASSURANCE_GOVERNANCE.md` doit
   *explicitement* déclarer que `gate_family ∈ {DESIGN, CERTIFICATION,
   ADVERSARIAL, OTHER}` et que `checkpoint ∈ {PRE_IMPLEMENTATION,
   POST_IMPLEMENTATION, COUNTER_PROOF, CLOSEOUT}`. Cette déclaration
   ferme la porte à une lecture v1.0 silencieuse par réinjection en
   `OTHER` : un lecteur v1.0 qui voit `ADVERSARIAL` ne peut plus
   l'ignorer sans invalider son contrat de lecture.
5. **Désynchronisation contrôlée.** La référence croisée est explicite :
   `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §0 cite
   `GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 comme l'autorité sur le
   schéma ; `GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 cite
   `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` comme l'autorité sur les
   valeurs et conditions. Toute édition unilatérale sans mise à jour de
   la référence croisée déclenche `vbb-contract-lint` en erreur.

### Impacts

- **+1 fichier canon** : `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`.
- **+~80 lignes** dans `GATE_ASSURANCE_GOVERNANCE.md` (schéma 1.1 +
  COUNTER_PROOF + closure_evaluation).
- **Pas de modification** de `PILOTAGE.md`, `CONVENTIONS.md`,
  `pre-merge-gate.md` au-delà des références croisées déjà planifiées
  par la migration M2.
- **Distribution** : CR#12 — la nouvelle autorité doit être référencée
  dans les boot-sets des 4 distributions (`pi`, `opencode`, `codex`,
  `claude`).

---

## M1-02 — Contrat de repli `A2` pour dépôt solo (COND-04)

### Options comparées

| # | Option | Description | Crédibilité | Applicabilité |
|---|---|---|---|---|
| A | Interdire `A2` en dépôt solo | Force un downshift automatique à `A1` dans tout dépôt mono-mainteneur. | Élevée (le niveau n'est jamais surévalué). | **Élimine la catégorie `A2`** pour ~80 % des dépôts cibles. |
| B | **`A2_DISTINCT_AGENT_PROXY`** | Permet `A2` en solo via un agent attaquant distinct (autre LLM, autre system prompt, identité publiée) + validation croisée par un second agent ou un humain. | Modérée — l'objectivité est procédurale, pas humaine. | Applicable immédiatement ; traçable par publication des identités. |
| C | `A2_HUMAN_VOUCHED` | Permet `A2` avec une attestation humaine de début de campagne. | Élevée mais coûteuse. | Inapplicable en run autonome / non-interactif. |
| D | **Hybride B + C : `A2_DISTINCT_AGENT_PROXY` + revue externe trimestrielle** | B pour les runs courants, C comme audit annuel par un humain externe. | Élevée + scalable. | Applicable immédiatement ; la revue trimestrielle peut être satisfaite par une CI planifiée ou un re-review par agent distinct. |

### Décision retenue

**Option D — Hybride `A2_DISTINCT_AGENT_PROXY` + revue externe trimestrielle.**

### Argumentation

1. **Préserve la catégorie `A2`** tout en la rendant applicable au dépôt
   Vibebackbone lui-même (qui est solo-maintenu et sera probablement la
   première cible de certification post-M2).
2. **Le niveau `A2` ne baisse pas sémantiquement.** Les conditions
   d'obtention de `CERTIFIED` restent identiques ; seul l'opérateur
   d'audit est relâché.
3. **L'identité publiée crée la traçabilité.** Le finding record doit
   déclarer `adversarial.attacker_identity = { agent: <name>, llm:
   <model>, system_prompt_version: <hash> }`. Cette identité est
   vérifiable par tout lecteur ultérieur — la falsification est
   détectable.
4. **La revue trimestrielle externe est le garde-fou structurel.**
   Elle peut être satisfaite par : (i) un humain tiers nommé, (ii) un
   agent d'un autre fournisseur LLM avec un system prompt publié et
   non-dérivé de celui utilisé pour les runs courants, ou (iii) une
   revue par les pairs via le canal de re-review existant
   (`06_REVIEW_RUN_0n`). L'option (ii) est la fallback viable pour
   les dépôts qui n'ont pas accès à (i).
5. **Pas de downshift silencieux.** Le downgrade de `A2` vers `A1` est
   interdit en M1-02 ; seule la substitution d'opérateur est permise.

### Contrat formel

```yaml
A2_DISTINCT_AGENT_PROXY:
  requirements:
    attacker_identity_disclosure: MANDATORY  # {agent, llm, system_prompt_version}
    distinct_llm: MANDATORY                  # différent du défenseur
    distinct_system_prompt: MANDATORY         # non-dérivé du système principal
    cross_validation: REQUIRED                # second agent ou humain sur le verdict
  external_review:
    cadence: QUARTERLY                       # 90 jours max entre deux revues
    operator_constraint: "different llm family OR human"
    failure_mode: "next CERTIFIED claim must wait for external_review pass"
  incompatible_with:
    - "downshift silencieux A2 -> A1"
    - "identity_disclosure absent"
```

### Impacts

- **+1 champ obligatoire** dans le finding record :
  `adversarial.attacker_identity`.
- **+1 sous-statut** : `A2_PROXY` au niveau field, sémantique `A2`
  préservée.
- **+1 obligation processuelle** : la revue trimestrielle externe doit
  être tracée dans `certification.last_external_review`.
- **Coût opérationnel estimé** : faible (3-4 revues/an par dépôt).

---

## M1-03 — Déclencheurs — N et « contestée » (ADVR-14, ADVR-16)

### M1-03a — Valeur de N

**Décision retenue.** `N = 10` (runs).

**Argumentation.**

- Assez large pour couvrir un cycle d'activité représentatif (un dépôt
  actif produit typiquement 3-10 runs/mois).
- Assez étroit pour détecter un historique récent (au-delà de 10 runs,
  la leçon est probablement déjà capitalisée ou oubliée).
- Cohérent avec le format `YYYY-MM-DD_HHMM` des run_id : la fenêtre
  temporelle implicite est `~3 mois` pour un dépôt actif, `~12 mois`
  pour un dépôt sporadique.
- Fixe une valeur **mesurable** plutôt qu'un seuil qualitatif — donc
  applicable par un validateur automatique (cf. M2).

### M1-03b — Définition de « contestée »

**Décision retenue.**

> Une classification est **contestée** lorsqu'un gate expert identifié
> dans le run refuse par écrit, dans `01_INTAKE.md`, le niveau déclaré
> en argumentant qu'un trigger de la matrice §4.2 a été mal classé.
> L'objection doit nommer le trigger et le motif.

**Argumentation.**

- **Opérationnelle.** Un gate expert est un acteur identifiable, pas
  un algorithme opaque. L'identité permet l'arbitrage ultérieur.
- **Vérifiable.** L'objection doit être dans `01_INTAKE.md`, un
  artefact canonique du run, donc mécaniquement contrôlable par
  `vbb-loop-closure-check`.
- **Non-subjective dans ses effets.** L'arbitre final reste la
  décision humaine M2+, mais le contest est désormais détectable
  automatiquement.
- **Cohérent avec ADR 0049** §Roles : « *Only a human approves,
  rejects, narrows or defers* ». Le contest écrit par un gate expert
  est l'expression de cette prérogative.

### M1-03c — Règles fail-closed

| Situation | Niveau effectif |
|---|---|
| Niveau déclaré `A2`, déclencheur `A2` matche, contest absent | `A2` (autorisé) |
| Niveau déclaré `A2`, déclencheur `A1` matche | `A2` (sur-classification autorisée si justifiée) **mais** contest ouvert par défaut |
| Niveau déclaré `A1`, déclencheur `A2` matche | **escalade obligatoire** vers `A2` — le déclarant ne peut pas sous-classer |
| Niveau non déclaré | `A1` (fail-closed) |
| Niveau déclaré `A0` mais déclencheur `A1`/`A2` matche | **escalade obligatoire** vers le niveau du trigger |
| Niveau contesté (objection écrite) | `A1` jusqu'à résolution du contest, peu importe le déclarant |
| Conflit entre déclarant et classifier automatique | `A1` (le plus prudent) |

**Argumentation.**

- La matrice de criticité est *trigger-based*, pas *déclarative*. Le
  déclencheur est l'autorité ; la déclaration est une commodité.
- Le contest est par défaut conservateur (escalade vers `A1`).
- L'escalade est obligatoire dans le sens *plus prudent*, jamais dans
  le sens *plus laxiste* — symétrie avec D7 (l'agent peut
  escalader, jamais réduire).

### Impacts

- **+1 champ obligatoire** dans `01_INTAKE.md` :
  `contest_register: [{objector, trigger, rationale, status}]`.
- **+1 règle dans `vbb-gate-check.py`** : vérification de cohérence
  déclarant/trigger/contest.
- **Documentation** : `PILOTAGE.md` §Triage rule gagne un alinéa
  « fail-closed rules » listant le tableau ci-dessus.
---

## M1-04 — `certification.owner` (ADVR-13)

### Décision retenue

| Dimension | Décision |
|---|---|
| **Responsabilités** | (a) Surveiller les 5 triggers de révocation de §6.3. (b) Tenir à jour `certification.last_reviewed`. (c) Déclencher la transition `CERTIFIED → SUSPENDED` sur détection de divergence. (d) Maintenir `certification.last_external_review` si applicable. |
| **Mécanisme** | Déclaré par certification. Trois modes autorisés : `manual:<cadence>`, `cron:<expr>`, `webhook:<target>`. Le mode par défaut si non déclaré est `manual:quarterly`. |
| **Cadence** | `manual` ≤ 90 jours entre deux `last_reviewed`. `cron` doit exprimer une périodicité ≤ 90 jours. `webhook` n'a pas de cadence fixe mais ne peut pas être silencieux plus de 90 jours. |
| **SLA breach** | Si `now - last_reviewed > cadence` OU si le `webhook` n'a pas renvoyé de signal depuis 90 jours, transition automatique `CERTIFIED → SUSPENDED` au prochain passage de `vbb-status-dashboard` ou `vbb-loop-closure-check`. |
| **Révocation (perte du `CERTIFIED`)** | Les 5 triggers existants + (e) SLA breach ci-dessus + (f) modification du `certification.owner` sans successeur déclaré. |
| **Conditions de re-acquisition** | Re-exécution de toutes les conditions §6.3 + levée de la cause de suspension. La nouvelle certification reçoit un nouveau `bound_to.run_id` ; l'ancien record reste valide pour son `bound_to`. |

### Argumentation

1. **Opérationnalise ADVR-13.** Le owner n'est plus un rôle
   consultatif ; il a une cadence et un mécanisme mesurable.
2. **Fail-closed par SLA breach.** L'oubli n'est plus permis : un
   `CERTIFIED` qui n'est pas re-validé dans sa cadence tombe
   automatiquement en `SUSPENDED`. C'est la seule façon d'éviter
   l'inertie silencieuse qu'ADVR-13 pointait.
3. **Préserve l'historique.** Le bound state antérieur reste valide.
   Seul l'état *présent* non-revalidé tombe. C'est cohérent avec D6
   (« *Certification is a statement about a frozen state, not a
   property of the project* »).
4. **Cohérent avec le format agent-friendly.** `cron:<expr>` et
   `webhook:<target>` sont des formats exécutables ; un validateur
   peut vérifier la présence et la périodicité.
5. **Le mode `manual:quarterly` par défaut** assure que *toute*
   certification non-déclarée a une cadence ; aucune n'est sans
   surveillance.

### Impacts

- **+3 sous-conditions au §6.3** : 6.3.10 mécanisme, 6.3.11 cadence
  et SLA, 6.3.12 transition automatique.
- **+1 champ obligatoire** dans le finding record :
  `certification.revocation_mechanism`.
- **+1 règle dans `vbb-status-dashboard`** : alerte quand
  `now - last_reviewed > cadence`.
- **+1 test obligatoire** dans M2 :
  `tests/test_certification_owner_sla.py`.

---

## M1-05 — Non-regression lock — `witnessed_by` et `test_review` (ADVR-17)

### Options comparées

| # | Option | Description | Anti-biais | Coût |
|---|---|---|---|---|
| A | **`witnessed_by` + `test_review` obligatoires à `A2`** | Au niveau `A2`, le lock doit être témoigné par un acteur distinct de l'attaquant, et le test lui-même doit être revu. | Fort. | Modéré (revue par second agent ou humain). |
| B | Mandatory à tous les niveaux | Idem à `A0`, `A1`, `A2`. | Fort. | Élevé (ralentit les micro-changements). |
| C | Solution équivalente : two-eyes en code review | Le PR qui inclut le fix doit avoir deux reviewers. | Faible — le reviewer voit le diff, pas l'oracle. | Bas. |
| D | Solution équivalente : le corpus entry est validé par un second agent dans les 30 jours | Le test est revu après coup. | Modéré. | Modéré. |

### Décision retenue

**Option A pour `A2`. Option D en complément à `A1`. Pas
d'obligation à `A0` (où aucun finding n'est attendu).**

### Argumentation

1. **Réponse directe à ADVR-17.** Le non-regression lock écrit par
   l'attaquant seul est un biais de confirmation structurel. La
   présence d'un témoin distinct de l'attaquant est la seule
   séparation qui corrige ce biais sans changer le test lui-même.
2. **Proportionnalité.** Le coût d'un témoin à `A2` est faible parce
   que `A2` est rare. L'appliquer à `A0` (où il n'y a pas de
   finding) et `A1` (où il y en a peu) surchargerait sans gain.
3. **À `A1`, la validation *a posteriori* du corpus entry** par un
   second agent sous 30 jours est un compromis acceptable : le
   test est validé par quelqu'un d'autre, sans bloquer le run
   immédiat. C'est l'option D en complément.
4. **Pas de solution C** : le code review voit le diff mais pas
   l'oracle. Confondre les deux serait une régression par rapport à
   la rigueur de l'oracle exigée par §6.2.7.

### Contrat formel

```yaml
non_regression_lock:
  A0: NOT_APPLICABLE        # pas de finding attendu
  A1:
    fields_required: [test_id, test_path, fails_before, passes_after]
    corpus_review:
      reviewer: "second_agent"
      deadline_days: 30
      verdict_required: true
  A2:
    fields_required: [test_id, test_path, fails_before, passes_after,
                      witnessed_by, test_review]
    witnessed_by: REQUIRED       # distinct de discovered_by
    test_review: REQUIRED        # verdict PASS|FAIL explicite
    test_review_reviewer: "second_agent_or_human"
```

### Impacts

- **+2 champs obligatoires** dans le finding record (§5.3) :
  `non_regression.witnessed_by`, `non_regression.test_review`.
- **+1 obligation de timing** à `A1` : revue corpus sous 30 jours.
- **+1 test obligatoire** dans M2 :
  `tests/test_non_regression_witness.py`.

---

## M1-06 — Statut `CERTIFIED` (ADVR-11, ADVR-13, M1-04)

### Conditions d'obtention (13 conditions nommées)

Les 9 conditions de la proposition v0.2 (§6.3) + 3 issues de M1-04
(sous-conditions 6.3.10, 6.3.11, 6.3.12) + 1 issue de M1-05 (6.3.13,
applicable à `A2`).

| # | Condition | Source |
|---|---|---|
| 6.3.1 | `conformity_status` ∈ {`PASS_CONFORMITY`, `NOT_APPLICABLE` avec profil} | v0.2 |
| 6.3.2 | `adversarial_status` ∈ {`PASS_ADVERSARIAL`, `NOT_REQUIRED` (A0 valide + aucun trigger A1/A2)} | v0.2 |
| 6.3.3 | Toutes les gates `CERTIFICATION` au `CLOSEOUT` checkpoint = `PASS` | v0.2 |
| 6.3.4 | Chaque `POST_IMPLEMENTATION` `FAIL` porte une `resolution` valide → `COUNTER_PROOF` PASS | v0.2 (D3) |
| 6.3.5 | Knowledge Harvest disposition enregistré ; chaque finding `CONFIRMED` a son bloc `promotion` répondu | v0.2 |
| 6.3.6 | Chaque `ACCEPTED_RISK` en scope : owner + expiry + reopen trigger + human approval ; aucun expiré | v0.2 |
| 6.3.7 | Décision humaine existe pour les sujets `A2` (M1-02 : `A2_DISTINCT_AGENT_PROXY` ou humain externe) | v0.2 |
| 6.3.8 | Binding : `run_id`, commit, `corpus_version`, scope, date tous enregistrés | v0.2 |
| 6.3.9 | `implementation_authorization.status` = `AUTHORIZED` (si implémentation) | v0.2 |
| 6.3.10 | `certification.revocation_mechanism` déclaré (`manual`, `cron`, `webhook`) | **M1-04** |
| 6.3.11 | Cadence déclarée ≤ 90 jours | **M1-04** |
| 6.3.12 | `certification.last_reviewed` ≥ `now - cadence` | **M1-04** |
| 6.3.13 | Pour tout finding `CONFIRMED` au niveau `A2` : `non_regression.witnessed_by` + `non_regression.test_review` présents | **M1-05** |

**Toutes les conditions sont individuellement evidenceées.** Aucune
n'est agrégée, moyennée ou inférée (D6).

### Conditions de perte (6 triggers)

1. Nouveau finding `CONFIRMED` dans le scope certifié.
2. Changement de `corpus_version` qui affecte la surface certifiée.
3. Changement de scope déclaré.
4. `ACCEPTED_RISK` expirée sans renouvellement.
5. Reopen trigger fired.
6. SLA breach du `certification.owner` (cf. M1-04).

**Conséquence.** `CERTIFIED → SUSPENDED`. Le record historique reste
valide pour son `bound_to` ; seul l'état *présent* non-revalidé tombe.

### Relation avec les audits adversariaux

- `CERTIFIED` exige `adversarial_status = PASS_ADVERSARIAL` (6.3.2).
  Donc un `CERTIFIED` est *toujours* adossé à un audit adversarial
  réussi (ou à un `NOT_REQUIRED` dûment justifié et exempt de tout
  trigger `A1`/`A2`).
- Les audits adversariaux produisent des findings ; les findings
  peuvent suspendre `CERTIFIED` (trigger 1). Donc la boucle
  adversariale *alimente* la boucle de certification, elle ne la
  court-circuite pas.
- La révocation automatique (SLA breach, trigger 6) ne dépend pas
  d'un audit en cours ; elle est purement mécanique.

### Argumentation

1. **Exhaustivité.** Les 13 conditions couvrent les 9 du v0.2 + les
   4 amendements de M1 (M1-04, M1-05). Aucune condition n'est
   redondante.
2. **Réponse à ADVR-11.** Les énumérations `gate_family` et
   `checkpoint` sont déclarées explicitement comme étendues dans
   `GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 (cf. M1-01). Un
   validateur v1.0 qui voit `gate_family: ADVERSARIAL` est invalide
   par construction ; la migration doit vérifier qu'aucun
   validateur v1.0 représentatif ne reste en service sans mise à
   jour (POC COND-02).
3. **Réponse à ADVR-13.** Le mécanisme de surveillance est
   défini ; le SLA breach déclenche la suspension automatique. La
   règle « *certification never expires by time alone* » est
   corrigée : elle expire par *état de surveillance*, pas par
   oubli.
4. **D6 préservée.** La conjonction reste *nommée*, pas agrégée.
5. **Cohérent avec ADR 0050.** La séparation
   `checkpoint_aggregation` / `closure_evaluation` (D3) n'est pas
   touchée.

### Impacts

- **§6.3** du canon étendu de 4 sous-conditions.
- **Schema v1.1** étendu : 4 nouveaux champs sur
  `certification.*`.
- **Tests obligatoires M2** :
  `tests/test_certified_conditions_6_3_1_to_13.py` (13 tests).

---

## §7 — Impacts identifiés (transversaux)

### Fichiers canoniques

| Fichier | Type de modification | Origine |
|---|---|---|
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | NEW (~350 lignes) | M1-01 |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | MODIFY (+~80 lignes : schéma 1.1, COUNTER_PROOF, closure_evaluation) | M1-01, M1-06 |
| `docs/PILOTAGE.md` | MODIFY (+~30 lignes : triage step 6, fail-closed rules) | M1-03 |
| `docs/CONVENTIONS.md` | MODIFY (+~10 lignes : P.R5 renforcé, règle épistémique) | M0 (04 §10) |
| `docs/AGENTIC_RUN_PROTOCOL.md` | MODIFY (+~20 lignes : 3ᵉ profil review phase 06) | M0 (04 §9.3) |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | MODIFY (+~15 lignes : producers anti-pattern) | M0 (04 §8) |
| `docs/REFERENCE/pre-merge-gate.md` | MODIFY (+~10 lignes : corpus execution comme check distinct) | M0 (04 §9.4) |
| `AGENTS.md` | MODIFY (1 nouvelle Critical Rule) | M0 (CANON §Impact) |

### ADR

| Fichier | Type | Origine |
|---|---|---|
| `docs/adr/00XX-adversarial-assurance-dimension.md` | NEW (ADR M1+M2) | M2 (out of M1 scope) |

### Modules / Architecture Blocks

| Block | Impact | Action M2 |
|---|---|---|
| Assurance contract | Additive schema `1.1` | Update `docs/ARCHITECTURE.md`, regen `RELATIONS.md` |
| Gate tooling | New validator, two extended validators | New tests |
| Run artifacts | Two new templates | Additive |

### Skills

| Skill | Change | Priorité M2 |
|---|---|---|
| `2-vbb-adversarial-campaign` (NEW) | Orchestrate existing technique skills into contracted campaign | P1 |
| `t-vbb-adversarial-corpus` (NEW) | Corpus entry creation, quarantine, versioning | P1 |
| `2-vbb-security`, `2-vbb-systemic-risk`, etc. | Referenced as technique providers; no behavior change | P2 |
| `0-vbb-pilotage`, `0-vbb-standard` | Level declaration at triage (M1-03) | P1 |

### Prompts

| Prompt | Change | Priorité M2 |
|---|---|---|
| `0-p-vbb-triage` | Declare the adversarial level; fail-closed rules (M1-03) | P1 |
| `07-p-vbb-closeout` | Statuses, campaign verdict, promotion completeness, contest register (M1-03) | P1 |
| `2-p-vbb-audit-task` | Campaign shape for `A2` + `A2_DISTINCT_AGENT_PROXY` (M1-02) | P2 |
| `1-p-vbb-structured-task` | `A1` inline campaign | P2 |

### Tests (toutes obligatoires)

| Test | Vérifie |
|---|---|
| `tests/test_adversarial_gate.py` (NEW) | Validation du schéma, fail-closed defaults, `resolution` links |
| `tests/test_certification_owner_sla.py` (NEW) | M1-04 — SLA breach → `SUSPENDED` |
| `tests/test_non_regression_witness.py` (NEW) | M1-05 — `witnessed_by` + `test_review` à `A2` |
| `tests/test_certified_conditions_6_3_1_to_13.py` (NEW) | M1-06 — 13 conditions |
| `tests/test_contest_register.py` (NEW) | M1-03 — contest déclenche A1 |
| `tests/test_a2_proxy.py` (NEW) | M1-02 — `A2_DISTINCT_AGENT_PROXY` accepté |
| `tests/test_attacker_identity_disclosure.py` (NEW) | M1-02 — identité publiée |
| `tests/test_gate_check_level.py` (MODIFY) | M1-03 — fail-closed level determination |
| `tests/test_loop_closure_*.py` (MODIFY) | Extended for `A1`/`A2` artifacts |
| `tests/test_engineering_knowledge_governance.py` (no change) | Non-regression on ADR 0049 |
| `tests/test_runtime_conformance.py` (no change) | Four-distribution conformance |

### Distributions (CR#12)

| Distribution | Surface | Action M2 |
|---|---|---|
| `pi` | `SYSTEM.md` posture reference, prompts | Reference new authority |
| `opencode` | Agent profile boot set | Reference new authority |
| `codex` | Agent profile boot set, conformance fixtures | Reference new authority |
| `claude` | `CLAUDE.md` entry point, skills index | Reference new authority |

---

## §8 — Liste des modifications à effectuer lors de M2

> **Statut.** Cette liste est le **contrat d'entrée** du run M2. Chaque
> ligne est l'expression d'une décision M1 ; M2 l'implémente. Aucune
> décision M2 ne peut contredire cette liste sans réouvrir M1.

### 8.1 — Création du canon (ADR + autorité + schémas)

| # | Modification | Décision source |
|---|---|---|
| M2-01 | Rédiger l'ADR `00XX-adversarial-assurance-dimension.md` | M0 |
| M2-02 | Créer `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | M1-01 |
| M2-03 | Étendre `GATE_ASSURANCE_GOVERNANCE.md` : §Schema 1.1, §COUNTER_PROOF, §closure_evaluation | M1-01, M1-06 |

### 8.2 — Statuts et lifecycle

| # | Modification | Décision source |
|---|---|---|
| M2-04 | Implémenter les 4 statuts avec `status_evidence` obligatoire | M0 §3, M0 §9.1 |
| M2-05 | Implémenter le finding lifecycle (17 états ; `history[]` externalisé — ADVR-18) | M0 §5.1 |
| M2-06 | Implémenter le `UNASSESSED_LEGACY` comme 5ᵉ valeur de `certification_status` | M0 §3.4 |

### 8.3 — Critique, déclencheurs, contest

| # | Modification | Décision source |
|---|---|---|
| M2-07 | Implémenter la matrice `A0/A1/A2` avec `N=10` | M1-03a |
| M2-08 | Implémenter le `contest_register` dans `01_INTAKE.md` | M1-03b |
| M2-09 | Implémenter les 7 règles fail-closed dans `PILOTAGE.md` §Triage | M1-03c |
| M2-10 | Implémenter `tools/vbb-gate-check.py` extension : cohérence déclarant/trigger/contest | M1-03c |

### 8.4 — `A2_DISTINCT_AGENT_PROXY` et revue trimestrielle

| # | Modification | Décision source |
|---|---|---|
| M2-11 | Implémenter `A2_DISTINCT_AGENT_PROXY` (sémantique `A2` préservée) | M1-02 |
| M2-12 | Ajouter `adversarial.attacker_identity` obligatoire | M1-02 |
| M2-13 | Ajouter `certification.last_external_review` (≤ 90 jours) | M1-02 |
| M2-14 | Implémenter `tests/test_a2_proxy.py`, `tests/test_attacker_identity_disclosure.py` | M1-02 |

### 8.5 — `certification.owner` et SLA

| # | Modification | Décision source |
|---|---|---|
| M2-15 | Ajouter §6.3.10, §6.3.11, §6.3.12 (mécanisme, cadence, transition auto) | M1-04 |
| M2-16 | Ajouter `certification.revocation_mechanism` obligatoire | M1-04 |
| M2-17 | Implémenter transition `CERTIFIED → SUSPENDED` sur SLA breach dans `vbb-status-dashboard` | M1-04 |
| M2-18 | Implémenter `tests/test_certification_owner_sla.py` | M1-04 |

### 8.6 — Non-regression lock

| # | Modification | Décision source |
|---|---|---|
| M2-19 | Ajouter `non_regression.witnessed_by` + `non_regression.test_review` ; obligatoire à `A2` | M1-05 |
| M2-20 | À `A1` : revue corpus sous 30 jours par un second agent | M1-05 |
| M2-21 | Implémenter `tests/test_non_regression_witness.py` | M1-05 |

### 8.7 — `CERTIFIED` : 13 conditions

| # | Modification | Décision source |
|---|---|---|
| M2-22 | Ajouter §6.3.13 (witnessed_by + test_review pour findings `A2`) | M1-05, M1-06 |
| M2-23 | Implémenter `tests/test_certified_conditions_6_3_1_to_13.py` (13 tests) | M1-06 |

### 8.8 — Outils, templates, skills, prompts

| # | Modification | Décision source |
|---|---|---|
| M2-24 | Créer `tools/vbb-adversarial-gate.py` | M0 §9.4 |
| M2-25 | Étendre `tools/vbb-loop-closure-check.py` | M0 §9.4 |
| M2-26 | Créer `docs/templates/ADVERSARIAL_CAMPAIGN.md.template`, `FINDING.md.template` | M0 §9.4 |
| M2-27 | Étendre `docs/templates/07_CLOSEOUT.md.template`, `06_REVIEW.md.template` | M0 §9.4 |
| M2-28 | Étendre `docs/templates/01_INTAKE.md.template` (contest_register, level declaration) | M1-03 |
| M2-29 | Créer skills `2-vbb-adversarial-campaign`, `t-vbb-adversarial-corpus` | M0 §9.4 |
| M2-30 | Étendre skills `0-vbb-pilotage`, `0-vbb-standard` | M1-03 |
| M2-31 | Étendre prompts `0-p-vbb-triage`, `07-p-vbb-closeout`, `2-p-vbb-audit-task`, `1-p-vbb-structured-task` | M0 CANON §Prompts |

### 8.9 — Distributions

| # | Modification | Décision source |
|---|---|---|
| M2-32 | Propager dans les 4 distributions : référence à la nouvelle autorité + boot-set update | CR#12 |
| M2-33 | Mettre à jour `docs/DISTRIBUTIONS.md` §Decisions log | CR#12 |

### 8.10 — Cutoff, ramp, validation

| # | Modification | Décision source |
|---|---|---|
| M2-34 | Déclarer le cutoff : `cutoff_run_key` + `cutoff_timestamp` | M0 §5.1 |
| M2-35 | Démarrer le ramp en `R0` (advisory) | M0 §5.4 |
| M2-36 | Exécuter `python tools/vbb-gate-check.py <run> --json` pour validation post-canon | M0 §5.2 |
| M2-37 | Exécuter `python -m pytest tests/ -q` (toute la nouvelle suite verte) | M0 §5.4 |

---

## §9 — Revues

### 9.1 Auto-revue (référence)

| Champ | Valeur |
|---|---|
| Source | `2026-07-28_1002/06_INDEPENDENT_REVIEW.md` |
| Independence | PARTIAL (divulguée §1) — même agent, même session, même dépôt |
| Verdict | `PASS_WITH_CONDITIONS` (10 blockers `ADVR-01..10` clos en v0.2) |
| Conditions ouvertes | `COND-01..06` |

**Statut M1.**
- `COND-01` → **levée** par `08_INDEPENDENT_REVIEW_DISTINCT_ACTOR.md`.
- `COND-04` → **tranchée** par M1-02 (Option D).
- `COND-05` → **tranchée** par M1-01 (Option C).
- `COND-02` → **POC listé** dans M2-24, M2-36.
- `COND-03` → **mesure R0** listée dans M2-35.
- `COND-06` → **vérification ADR 0031** notée pour l'ADR M2-01.

### 9.2 Revue indépendante par acteur distinct (référence)

| Champ | Valeur |
|---|---|
| Source | `2026-07-28_1002/08_INDEPENDENT_REVIEW_DISTINCT_ACTOR.md` |
| Independence | GENUINE |
| Verdict | `PASS_WITH_CONDITIONS` |
| Réserves nouvelles (8) | `ADVR-11..18` |

**Statut M1.** Chaque réserve est arbitrée :

| Réserve | Décision M1 | Verdict |
|---|---|---|
| `ADVR-11` (énumérations étendues) | M1-01 §Argumentation 4 : déclaration explicite dans `GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 + POC COND-02 | **Levée** par M1-01 + M2-36 |
| `ADVR-12` (A2 inapplicable en solo) | M1-02 : Option D, `A2_DISTINCT_AGENT_PROXY` + revue trimestrielle | **Levée** par M1-02 |
| `ADVR-13` (certification.owner sans mécanisme) | M1-04 : 3 modes + cadence ≤ 90 jours + SLA breach auto | **Levée** par M1-04 |
| `ADVR-14` (N non défini) | M1-03a : N=10 | **Levée** par M1-03a |
| `ADVR-15` (autorité non tranchée) | M1-01 : Option C split strict | **Levée** par M1-01 |
| `ADVR-16` (« contestée » non défini) | M1-03b : objection écrite par gate expert dans `01_INTAKE.md` | **Levée** par M1-03b |
| `ADVR-17` (non-regression lock biaisé) | M1-05 : `witnessed_by` + `test_review` obligatoires à `A2` | **Levée** par M1-05 |
| `ADVR-18` (finding record trop riche) | Reportée à M2-05 : externaliser `history[]` vers audit log séparé | **Partiellement levée** — décision d'implémentation en M2-05 |

**Réserves toutes arbitrées.** Aucune ne reste ouverte à l'issue de M1.

### 9.3 Évaluation par cette M1

Cette M1 tranche :
- 6 décisions normatives (M1-01 à M1-06) — toutes uniques, argumentées,
  applicables.
- 8 réserves de la revue indépendante — toutes arbitrées.
- 6 conditions du self-review — toutes arbitrées ou escaladées.
- 37 modifications canon/outillage/skills/prompts/tests listées pour M2.

**Cohérence globale.** Chaque décision préserve au moins un des
principes suivants :
- CR#5 (no parallel truth) — M1-01 split strict.
- CR#4 (hiérarchie documentaire) — M1-04 owner dans l'autorité
  nouvelle.
- ADR 0049 (knowledge governance) — M1-05 promotion par ADR 0049.
- ADR 0050 (assurance schema) — M1-06 13 conditions nommées, pas agrégées.
- ADR 0043 (orthogonalité FINAL/ASSURANCE) — non touché.
- ADR 0031 (autonomous runs) — noté dans §9.1, à intégrer dans l'ADR M2-01.

---

## §10 — Points non résolus (pour transparence)

Aucun point normatif n'est laissé ouvert par cette M1.

| ID | Élément | Destination |
|---|---|---|
| U-01 | Détails stylistiques du schéma 1.1 (ordonnancement, indentation, libellés) | M2 — implémentation |
| U-02 | Texte exact de la non-claim canonique `ADVERSARIAL_NON_CLAIM_v1` (ADVR-18) | M2 — implémentation |
| U-03 | Liste détaillée des templates à étendre (M2-26, M2-27, M2-28) | M2 — implémentation |
| U-04 | Vérification formelle de l'interaction avec ADR 0031 | M2-01 — ADR |

**Ces 4 points sont des questions d'implémentation, pas d'arbitrage
normatif.** Ils n'invalident aucune des 6 décisions M1.

---

## §11 — Note de passation vers M2

**Le run M2 peut démarrer sur la base des éléments suivants :**

1. **6 décisions normatives arbitrées** (M1-01 à M1-06).
2. **37 modifications listées** (§8) — base contractuelle de M2.
3. **Conditions du self-review** : `COND-01` levée, `COND-04`/`05` tranchées,
   `COND-02`/`03`/`06` à intégrer dans M2.
4. **8 réserves de la revue indépendante** : toutes arbitrées.
5. **Note U-04** : interaction ADR 0031 à vérifier dans l'ADR M2-01.

**Aucune des 6 décisions M1 ne peut être ré-ouverte en M2 sans run
d'arbitrage séparé.** Toute déviation doit être documentée comme
`M2_DEVIATION_FROM_M1` avec justification et traçabilité.
