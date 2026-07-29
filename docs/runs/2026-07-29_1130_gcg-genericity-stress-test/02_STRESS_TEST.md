---
run_id: "2026-07-29_1130_gcg-genericity-stress-test"
phase: "02_STRESS_TEST"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_MODEL_VALIDATION"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T09:30:00Z"
ended_at: null
artifacts_produced:
  - "02_STRESS_TEST.md (this file)"
---

# 02_STRESS_TEST — GCG-STRESS-01

Stress test de généricité du *Governance Compatibility Gate*, par application à
trois règles de gouvernance indépendantes de la dimension adverse.

**Verdict en une ligne : le noyau tient, la périphérie ne tient pas, et le
scanner est structurellement plus permissif que le gate qu'il enveloppe.**
Le modèle n'est pas encore canonisable ; une révision v2 est proposée.

---

## 1. Ce qu'un vrai stress test devait éviter

Le piège d'un test de généricité est de choisir une deuxième règle
suffisamment proche de la première pour que le modèle tienne par construction.
Trois précautions ont été prises :

1. **Distance structurelle croissante** — la deuxième règle partage la
   population, la troisième change de population, la quatrième n'en a pas.
2. **Mesure, pas raisonnement** — chaque affirmation ci-dessous est adossée à
   une commande exécutée sur le dépôt à `f7e21a3`. Aucun exemple fabriqué.
3. **Critère de réussite symétrique** — le modèle réussit s'il classe
   correctement la règle proche **et** s'il déclare son inapplicabilité sur les
   règles lointaines. Un modèle qui répond à tout ne discrimine rien.

| Règle | Source | Population | Cardinalité |
|---|---|---|---|
| **A** adversarial-assurance 1.1 | ADR 0051 | runs | 162 (14 applicables) |
| **B** engineering-knowledge 1.0 | ADR 0049 | runs | 162 (19 gouvernés) |
| **C** seven-section skill layout | ADR 0042 | skills | 67 |
| **D** credentials enforcement | ADR 0033 | lignes ajoutées d'un diff | flux |

---

## 2. Règle B — le test proche

`docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`, imposée par
`validate_knowledge_harvest()` dans `tools/vbb-loop-closure-check.py`.
Obligation : tout closeout formel déclare `knowledge_governance_version` et
exactement une disposition `knowledge_harvest ∈ {NONE, OBSERVATION_RECORDED,
EVIDENCE_LINKED}`.

### 2.1 Application du modèle

| Élément du modèle | Valeur pour la règle B | Source |
|---|---|---|
| `applies_from` | `2026-07-27_1712` | `KNOWLEDGE_GOVERNANCE_CUTOVER_KEY` |
| `enforcement_effective_from` | `2026-07-27_1712` | commit `ae273b5`, même run |
| **fenêtre de dette** | **∅** | les deux bornes coïncident |
| population gouvernée | 19 / 162 | mesuré |
| non conformes | 2 | mesuré |

```
2026-07-28_1200_m1  → 07_CLOSEOUT.md: missing Knowledge Harvest for governance v1
2026-07-30_0500     → knowledge_harvest must be one of …; observed 'missing'
```

Les deux échecs sont postérieurs à `enforcement_effective_from`. Le modèle les
classe `CURRENT_NONCOMPLIANCE`, bloquants, non ledgerables. **C'est correct** :
la règle et son vérificateur ont été livrés ensemble, donc aucune dette
historique n'est admissible, et aucune n'est réclamable.

### 2.2 Ce que la règle B a appris au modèle

**La fenêtre vide est l'état cible, pas un cas dégénéré.**

La règle B a une fenêtre de dette nulle parce qu'elle a été outillée dans le
même run que sa publication. La règle A a une fenêtre de six heures parce
qu'elle a été publiée à `1400` et outillée à `2000`. Ces six heures sont
exactement l'intervalle pendant lequel le canon a exigé quelque chose qu'il ne
savait pas vérifier — et c'est exactement là que se trouvent les quatre
`UNKNOWN` en attente d'arbitrage.

La largeur de la fenêtre n'est donc pas un paramètre technique : c'est une
**mesure de la qualité de publication d'une règle**. Un canon discipliné
produit des fenêtres vides. Le modèle gagne un usage qu'il n'avait pas.

### 2.3 `OVERCLAIM` a une seconde instance, trouvée par mesure

`docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md:44` définit :

> `EVIDENCE_LINKED` — evidence was linked to an existing candidate.

Trois constats mesurés :

1. le validateur ne vérifie que l'appartenance à l'énumération — il ne résout
   aucun lien, ne cherche aucun candidat (`vbb-loop-closure-check.py:310-316`) ;
2. **il n'existe aucun registre de candidats** dans le dépôt (`docs/knowledge*`
   n'existe pas) — le « candidat existant » auquel la preuve serait liée n'a
   pas de support ;
3. **9 runs déclarent une disposition positive sans section Knowledge Harvest
   dans le corps du closeout** — 7 `EVIDENCE_LINKED`, 2 `OBSERVATION_RECORDED`.

```
1600 OBSERVATION_RECORDED · 1800 OBSERVATION_RECORDED · 2000 EVIDENCE_LINKED
2200 EVIDENCE_LINKED · 2300 EVIDENCE_LINKED · 07-29_0100 EVIDENCE_LINKED
07-29_0300 EVIDENCE_LINKED · 07-30_0100 EVIDENCE_LINKED · 07-30_0700 EVIDENCE_LINKED
```

C'est la définition généralisée de `OVERCLAIM`, mot pour mot : *un artefact
affirme un verdict positif sans porter la structure qui permettrait de le
valider*. La forme est identique à `PASS_ADVERSARIAL` sans bloc adverse, sur une
règle qui n'a rien à voir.

**C'est le résultat le plus solide de ce test.** `OVERCLAIM` n'a pas été
reconduit par analogie : la seconde instance a été trouvée en mesurant, sur une
règle choisie avant de savoir ce qu'on y trouverait.

*Méthode et réserve.* Les 9 runs sont détectés par balayage des titres de
niveau 2 ; 3 d'entre eux (`2000`, `1600`, `07-30_0100`) ont été vérifiés par
énumération complète des titres. Les 6 autres reposent sur le seul balayage. La
disposition pourrait être justifiée ailleurs qu'en section dédiée — cela reste
à instruire, et ce n'est pas l'objet de ce run.

---

## 3. Règle C — le test lointain : la population change de nature

ADR 0042 : *« Every catalog SKILL.md contains the exact seven mandatory
level-two headings. »* Vérifiée par `check_required_skill_sections()` dans
`vbb-contract-lint.py:375`. État mesuré : **0 erreur sur 67 skills**.

### 3.1 Le modèle ne s'applique pas — et c'est un résultat

Un skill n'a **pas d'identité datée** et n'est **pas immuable**. Il est édité en
continu ; il n'a pas d'instant de production. Conséquences directes :

| Élément du modèle | Statut pour la règle C |
|---|---|
| `applies_from` | déclarable, mais **incomparable** — rien à comparer |
| `enforcement_effective_from` | idem |
| fenêtre de dette | **indéfinie** |
| `HISTORICAL_VALID` | **indéfini** |
| `MIGRATION_AVAILABLE` / `HISTORICAL_NONCOMPLIANCE` | **indéfinis** |
| `CURRENT` / `CURRENT_NONCOMPLIANCE` / `OVERCLAIM` / `PENDING_LIFECYCLE` | applicables |

La moitié temporelle du modèle disparaît. Un scanner GCG naïf appliqué aux
skills classerait les 67 en `UNKNOWN` (identité non parsable) — donc bloquants —
alors que la règle est intégralement satisfaite. **Faux positif total.**

### 3.2 Ce que le canon a réellement fait, et pourquoi c'était juste

Le run `2026-07-14_2045_skill-section-normalization` a migré les 12 skills
divergents **en une passe**, puis le lint a bloqué la dérive. Zéro dette.

Ce n'est pas de la chance : pour une population mutable, **la migration est
toujours disponible**, parce que l'artefact peut être réécrit sans falsifier
quoi que ce soit. Réécrire un skill n'est pas réécrire l'histoire — un skill
n'est pas un enregistrement historique, c'est un objet vivant. La question
« ce document était-il conforme au canon de son époque ? » n'a aucun sens pour
lui.

C'est aussi **le seul précédent réel de Migration Engine** dont dispose le
modèle : déterministe, sourcé dans l'artefact contemporain, sans invention.
L'invariant I1 y est satisfait — par un humain, pas par un moteur.

### 3.3 Le manque : il n'existe aucun contrat de population

Le modèle v1 parle de « l'artefact » sans jamais dire à quelle classe
d'artefacts il s'applique. Or les catégories historiques exigent trois
propriétés que rien ne déclare :

- **daté** — chaque membre porte un instant de production ;
- **immuable** — un membre est un enregistrement, pas un objet vivant ;
- **énumérable** — la population est close et parcourable.

Sans ces trois propriétés, la fenêtre de dette n'a pas de sens. C'est le
manquement structurel principal de la v1.

---

## 4. Règle D — le test de frontière : il n'y a pas de population

ADR 0033, `tools/vbb-credentials-gate.py`. Modes `--staged` (HEAD → index) et
`--range BASE HEAD`. La règle §5 de l'ADR : *« les suppressions, contenus
binaires et lignes inchangées ne sont pas scannés »*.

Il n'y a **aucun ensemble d'artefacts à classer**. L'objet gouverné est un
**flux** : les lignes ajoutées par un changement. On ne peut pas énumérer la
population, on ne peut pas la reclasser, il n'y a rien à migrer.

Le modèle doit se déclarer inapplicable. Il le fera correctement une fois le
contrat de population ajouté (`enumerable: false` → hors périmètre GCG).

Deux remarques toutefois :

- ADR 0033 a réinventé la non-rétroactivité **de son côté** : ne scanner que
  les lignes ajoutées, c'est refuser de juger l'histoire. C'est
  `HISTORICAL_VALID` exprimé pour un flux.
- La comparaison éclaire une limite de vocabulaire : GCG gouverne des
  **états**, pas des **transitions**. Le dire explicitement évite qu'on essaie
  un jour de l'étendre aux gates de flux.

---

## 5. Ce que le test a trouvé

Huit constats. Trois sont des défauts du modèle ou de son implémentation, deux
sont des confirmations fortes, trois sont des corroborations.

### S1 — Le scanner est structurellement plus permissif que l'enforcer *(P1, latent)*

L'enforcer canonique reconnaît **trois** sources d'applicabilité
(`_knowledge_governance_required`, `vbb-loop-closure-check.py:216-252`, et ses
jumeaux assurance et adverse) :

1. identité de run ≥ clé de cutover ;
2. `started_at` ≥ instant de cutover ;
3. **auto-déclaration** de la version dans le frontmatter, quelle que soit la
   date.

Les trois sont combinées par `OR`, donc fail-closed vers l'inclusion. Le scanner
GCG n'implémente que la source 1.

**Un sous-ensemble d'une disjonction est toujours au plus aussi inclusif.** Donc
GCG est, par construction, au plus aussi strict que le gate qu'il enveloppe, et
strictement plus permissif dès que la source 2 ou 3 se déclenche. Un gate de
compatibilité plus permissif que le gate qu'il mesure **masque des échecs** —
exactement la classe de défaut que GCG existe pour rendre visible.

**Statut : latent, pas actif.** Vérifié : aucun run du dépôt ne diverge
aujourd'hui (aucun run pré-cutoff n'auto-déclare, aucun `started_at` ne
franchit la borne que l'identité ne franchit pas). Le défaut est prouvé par
construction, pas par une instance. Il se déclenchera à la première
auto-déclaration rétroactive.

**Non corrigé ici** — contrainte C1 du run. Bloquant pour le câblage CI.

### S2 — La frontière déclare sa valeur, pas son unité *(P1, actif)*

Le modèle v1 §3.3 pose : *« une frontière normative est déclarée par le canon,
jamais dérivée d'un artefact technique »*. Correct, mais incomplet : déclarer
`applies_from: "2026-07-28_1400"` **ne déclare pas un instant**, parce que
l'identité de run n'a pas de fuseau déclaré.

Le canon déclare d'ailleurs la même borne deux fois, dans deux unités :

```python
ADVERSARIAL_GOVERNANCE_CUTOVER_KEY = "2026-07-28_1400"                        # identité
ADVERSARIAL_GOVERNANCE_CUTOVER_AT  = datetime(2026, 7, 28, 14, 0, tzinfo=utc) # instant UTC
```

Mesure de l'écart identité − `started_at` sur les runs récents : **les deux
conventions coexistent dans le corpus**, et la césure tombe précisément sur le
cutover adverse.

```
+2.00h   2026-07-26_1701 … 2026-07-28_1002     identité = heure locale (UTC+2)
+0.00h   2026-07-28_1200 … 2026-07-30_0700     identité = UTC
+2.00h   2026-07-29_0840 … 2026-07-29_1130     identité = heure locale (UTC+2)
-8.00h   20260615-usage-audit                  identité à granularité jour
```

Les runs qui **définissent** le cutover sont en heure locale ; les runs
**gouvernés** par lui sont en UTC. Les deux bornes déclarées sont donc à deux
heures l'une de l'autre, pour une fenêtre de dette large de **six heures** :
l'ambiguïté vaut un tiers de la fenêtre.

Cas pire mesuré : `20260615-usage-audit` et les treize `2026-07-12_runNN` ont
une identité à granularité jour. Leur borne n'est pas un instant mais un
intervalle de 24 h — plus large que bien des fenêtres de dette.

Aucune conséquence de classement aujourd'hui : le `OR` de l'enforcer retient la
borne la plus inclusive. Mais le modèle prétend que la frontière est
non ambiguë, et elle ne l'est pas.

### S3 — L'acte de compatibilité ne sait pas représenter deux règles *(P1, actif)*

`2026-07-30_0500_final-publication-of-v1.1-certification` est simultanément :

- `OVERCLAIM` sous la règle A — `PASS_ADVERSARIAL` sans bloc validable ;
- non conforme sous la règle B — `knowledge_harvest` absent.

Le modèle §4 gère cela correctement : *« une et une seule [catégorie] par couple
(artefact, règle) »*. Mais le schéma de l'acte, §6.1, ne le gère pas :

```yaml
classification: {CURRENT: n, HISTORICAL_VALID: n, ...}   # table plate, sans clé de règle
readings: {current_conformance: "n/m"}                    # un ratio unique
```

Les populations applicables diffèrent — 14 pour A, 19 pour B. Un ratio global
n'a aucun sens, une table de comptage plate ne peut pas distinguer les deux
lectures d'un même artefact.

**La classification est générique ; l'acte est mono-règle.** C'est la deuxième
règle qui casse le schéma, pas le modèle.

### S4 — Les catégories historiques n'ont pas de contrat de population *(P0 structurel)*

Développé en §3.3. Le modèle doit exiger `dated`, `immutable`, `enumerable` et
définir un **mode dégradé** explicite pour les populations qui ne les ont pas.

### S5 — « L'artefact porteur de la preuve » n'est pas défini *(P2, actif)*

Deux résolveurs coexistent et divergent :

| Résolveur | Consommateur | Accepte `02_CLOSEOUT.md` ? |
|---|---|---|
| `find_closeout()` — `07_CLOSEOUT.md` puis repli `*CLOSEOUT*.md` | GCG | **oui** |
| chemin en dur `run_dir / "07_CLOSEOUT.md"` | règle B | **non** |

Instance réelle : `2026-07-28_1200_m1-adversarial-loop-normative-arbitration`
contient `02_CLOSEOUT.md`. Le même run « a un closeout » pour GCG et « n'en a
pas » pour la règle B.

Conséquence sur l'invariant I6. `PENDING_LIFECYCLE` est attribué quand
*l'artefact porteur de la preuve n'existe pas*. Si l'identité de cet artefact
dépend du résolveur, une simple variante de nommage produit un
`PENDING_LIFECYCLE` faux — c'est-à-dire une violation de I6 par une voie que la
limite stricte ne couvre pas. La limite stricte gouverne le **motif** de la
classification ; elle ne gouverne pas la **résolution** de l'artefact.

### S6 — `OVERCLAIM` est générique *(confirmation forte)*

Développé en §2.3. Seconde instance indépendante, trouvée par mesure.

### S7 — La fenêtre de dette tient et gagne un usage *(confirmation)*

Développé en §2.2. Fenêtre vide = état cible ; largeur = métrique de qualité de
publication.

### S8 — GCG factorise une invention que le canon a déjà faite trois fois *(corroboration)*

```python
KNOWLEDGE_GOVERNANCE_CUTOVER_KEY   = "2026-07-27_1712"
ASSURANCE_GOVERNANCE_CUTOVER_KEY   = "2026-07-27_2145"
ADVERSARIAL_GOVERNANCE_CUTOVER_KEY = "2026-07-28_1400"
```

Trois cutovers, même forme, même intention déclarée (*« The cutover is derived
from immutable run identity or `started_at` … Earlier runs remain valid »*),
jamais nommée comme un concept. La paire adverse est en outre **dupliquée**
entre `vbb-loop-closure-check.py` et `vbb-adversarial-gate.py` — valeurs
identiques aujourd'hui, vérité parallèle en attente de dérive
(Critical Rule 5).

C'est l'argument le plus fort **en faveur** du modèle : il ne propose pas un
concept nouveau, il nomme et factorise un mécanisme que le dépôt a réinventé
trois fois de façon ad hoc — quatre avec ADR 0033.

C'est aussi une limite honnête : **aucune des trois instances n'a de seconde
borne**. `applies_from` est corroboré par trois précédents indépendants ;
`enforcement_effective_from` et la fenêtre de dette n'en ont aucun. Ils restent
éprouvés sur la seule règle A.

---

## 6. Verdict

**Le modèle est générique dans son noyau, non générique dans sa périphérie, et
permissif à un endroit qui doit être corrigé avant tout câblage.**

| Composant | Verdict | Fondement |
|---|---|---|
| Classification (§4, 8 catégories) | **tient** | correcte sur B ; correctement inapplicable sur C et D **une fois le contrat de population ajouté** |
| `OVERCLAIM` | **tient, générique** | seconde instance indépendante trouvée par mesure (S6) |
| Deux bornes / fenêtre de dette | **tient, gagne un usage** | S7 — mais unité sous-spécifiée (S2) et sans précédent hors règle A (S8) |
| Séparation Scanner / Arbitration / Engine | **non contredit, non éprouvé** | un seul précédent réel de migration (§3.2), aucune migration exécutée ici |
| Contrat d'applicabilité | **ne tient pas** | S1 — purement temporel là où le canon a trois sources |
| Unité de la frontière | **ne tient pas** | S2 — deux conventions coexistent dans le corpus |
| Schéma de l'acte (§6.1) | **ne tient pas** | S3 — mono-règle par construction |
| Contrat de population | **absent** | S4 |

**Conclusion : `NOT_CANONICAL_YET`.**

La partie du modèle qui décrit *comment penser* la compatibilité — les trois
lectures orthogonales, les catégories, la primauté de `OVERCLAIM`, la règle
anti-blanchiment — a résisté au test et en sort renforcée. La partie qui décrit
*comment l'appliquer* — applicabilité, unité, population, acte — a été écrite en
regardant une seule règle et le montre.

Ce n'est pas un échec du modèle : c'est précisément ce que la §7 de la v1
annonçait — *« un modèle générique appliqué à une seule règle est un modèle non
éprouvé ; la deuxième règle est celle qui dira si l'abstraction tient »*. Elle
l'a dit.

---

## 7. Révision proposée — v2

Six amendements. Aucun ne touche le noyau de classification.

| # | Amendement | Répare |
|---|---|---|
| **A1** | §3.4 **Contrat d'applicabilité** — trois sources, union, fail-closed vers l'inclusion. Nouvel invariant **I9** : *un scanner de compatibilité n'est jamais plus permissif que l'enforcer qu'il enveloppe.* | S1 |
| **A2** | §3.5 **Unité de la frontière** — une borne déclare sa valeur **et** son unité. Granularité jour ⇒ la borne est un intervalle, et la règle fail-closed retient la plus inclusive. Nouvel invariant **I10**. | S2 |
| **A3** | §3.6 **Contrat de population** — `dated`, `immutable`, `enumerable`. Les catégories historiques et la fenêtre de dette exigent les trois ; sinon **mode dégradé** : `CURRENT`, `CURRENT_NONCOMPLIANCE`, `OVERCLAIM`, `PENDING_LIFECYCLE`, **aucune dette admissible**. `enumerable: false` ⇒ hors périmètre GCG. | S4 |
| **A4** | §6.1 **Acte multi-règles** — `rules: [{rule_id, population, classification, readings}]`, verdict global = `OR` des bloquants, **jamais de ratio global**. | S3 |
| **A5** | §3.2 — la fenêtre vide est l'**état cible** ; sa largeur est une **métrique** de qualité de publication. §4 — tableau annoté par prérequis de population. | S7 |
| **A6** | §3.7 **Résolution d'artefact** — déclarée par la règle, pas par le scanner. Nouvel invariant **I11**. | S5 |

### Ce que la v2 ne répare pas

- **La couverture exécutable reste minoritaire.** I2, I4, I6 sont testés. I1,
  I3, I5, I7, I8 ne l'étaient pas ; I9, I10, I11 ne le sont pas davantage.
  Le ratio passe de 3/8 à 3/11. Un invariant sans test est une intention, et
  la v2 en ajoute trois de plus.
- **La séparation Scanner / Engine reste non éprouvée.** Aucune migration n'a
  été exécutée par un moteur. Le seul précédent (§3.2) est un run humain.
- **`enforcement_effective_from` reste sans corroboration externe.** Trois
  précédents pour `applies_from`, zéro pour la seconde borne (S8).
- **S1 reste ouvert dans le code.** La contrainte C1 interdisait de le
  corriger. Il devient un bloquant explicite du câblage CI.
- **Les cinq constats confirmés sont verrouillés, pas réparés.** Déclarer
  `S1`–`S5` en `CONFIRMED` a déclenché l'obligation de corpus et imposé cinq
  entrées `BEHAVIOUR_PIN` (`05_EXECUTION.md` §4). Un pin garantit qu'un défaut
  ne change pas en silence ; il ne garantit rien d'autre.

---

## 8. Ce que ce test n'a pas fait

- Il n'a pas éprouvé le Migration Engine — rien n'a été migré.
- Il n'a pas éprouvé le cache de l'acte ni le déclenchement en session.
- Il n'a testé **aucune règle hors de ce dépôt**. La généricité démontrée est
  celle d'un modèle face à quatre règles d'un même canon, écrites par la même
  équipe, dans le même style. C'est une généricité **interne**.
- Il a été conduit par l'agent qui a écrit le modèle. `A2_DISTINCT_AGENT_PROXY`
  n'est pas satisfait. Trois des huit constats (S1, S3, S4) sont des défauts
  d'une conception que le même agent a produite — ce qui est plutôt bon signe,
  mais ne remplace pas un acteur distinct.
