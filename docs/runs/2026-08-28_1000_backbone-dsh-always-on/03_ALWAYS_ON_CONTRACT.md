---
context_role: always-on-contract
phase: 03_ALWAYS_ON_CONTRACT
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A2 (le contrat pose des règles vérifiables touchant au canon)
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T11:45:00Z"
ended_at: "2026-08-28T13:30:00Z"
next_phase: "04_DOCUMENTARY_CANON_MODEL"
artifacts_consumed:
  - "01_CURRENT_STATE.md"
  - "02_HYPOTHESIS.md"
artifacts_produced:
  - "03_ALWAYS_ON_CONTRACT.md"
depends_on:
  - "H1 / H1-PERMANENT / H1-LIGHT / H1-COHERENT / H1-RIGOR-INVARIANCE (cf. E2 §1.1)"
  - "ADR 0055 §C1-C7"
  - "ADR 0049, ADR 0050, ADR 0051, ADR 0053"
blocks:
  - "E4_DOCUMENTARY_CANON_MODEL (doit dériver P-1)"
  - "E5_MEMORY_INTEGRATION_MODEL (doit dériver P-3 / C-4)"
  - "E6_EXPERIMENT_PROTOCOL (doit produire des falsifs exécutables sur ce contrat)"
supersedes: []
---

# 03_ALWAYS_ON_CONTRACT — l'unique contrat Backbone permanent dans DSH

> Ce document est **un** contrat. Pas trois. Les niveaux A0 / A1 / A2
> varieront en **profondeur d'assurance** (§5), pas en contenu. Toute
> rédaction de règles différentes par niveau ailleurs dans ce run est
> considérée comme un signal de drift vers `F-INVAR` (E2 §2.4).
>
> Le contrat distingue **propriétés permanentes** (§1) — ce qui doit rester
> vrai à tout instant — et **capacités toujours accessibles** (§2) — ce que
> l'agent doit pouvoir atteindre à la demande, sans que la présence
> permanente de l'artéfact dans le contexte soit requise.
>
> Une **capacité** peut être portée par une skill, un tool, un persona ou un
> réflexe ; peu importe le vecteur. Ce qui compte, c'est que la garantie
> tienne et reste vérifiable.

## 0. Tests de cohérence interne (à passer avant publication E3)

| Test | Enoncé | Pass = OK |
|---|---|---|
| T-INVAR-1 | Retirer toutes les références à A0/A1/A2 de §1 à §4. Le contrat reste cohérent. | ✅ §1-§4 ne mentionnent aucun tier. |
| T-INVAR-2 | Ajouter un tier A99 (hypothétique) dans §5 sans modifier §1-§4. Le contrat reste cohérent. | ✅ §5 ne fait que moduler l'assurance. |
| T-LIGHT-1 | Aucune règle §1 / §2 n'impose un chargement upfront de tous les documents canon. | ✅ « toujours accessible » ≠ « toujours chargé ». |
| T-LIGHT-2 | Aucune règle §1 / §2 n'exige un cycle documentaire complet pour une tâche triviale. | ✅ §4 définit quand le cycle **doit** se déclencher. |
| T-CAP-1 | Aucune règle §2 ne désigne une skill précise par son nom et son id. | ✅ §2 décrit des **capacités** (C-1..C-5) ; les implémentations sont interchangeables. |
| T-CONS-1 | Aucune règle §1 / §2 ne contredit ADR 0049 / 0050 / 0051 / 0053 / 0055. | ✅ aucune introduction d'autorité parallèle. |

## 1. Propriétés permanentes — ce qui doit rester vrai

Quatre propriétés indépendantes et vérifiables. Le contrat est rompu si l'une
quitte ; il ne l'est pas par simple flou.

### P-1 — `Canon-awareness`

**Énoncé.** L'agent, à tout moment de la session, est capable de **pointer**
vers le canon documentaire courant et de **distinguer** ce qui y figure de ce
qui n'y figure pas.

**Ce qui n'est PAS requis.**

- Le canon complet n'est pas chargé en mémoire.
- L'agent n'a pas à énumérer tous les artefacts canoniques.
- L'agent n'a pas à consulter `docs/CONTEXT.md` à chaque tour.

**Garanties minimales observables.**

1. L'agent peut nommer au moins un document canonique d'entrée
   (entrée attendue : `docs/CONTEXT.md`).
2. L'agent peut citer l'existence d'au moins une autorité de statut parmi
   les cinq dimensions d'ADR 0055 §C4.
3. L'agent, face à une affirmation qu'il suspecte non-canonique, sait
   **demander** où trouver la version canonique, sans affirmer qu'elle est
   vraie sur la base de sa mémoire conversationnelle.

**Violations observables.**

- V-P1-a — L'agent déclare un fait non-canonique comme canonique
  (« c'est la règle… » sans artefact cité).
- V-P1-b — L'agent ne peut nommer aucun point d'entrée canonique.
- V-P1-c — L'agent confond une SPEC ad hoc, un README, ou une note de
  commit avec une décision de canon.

**Lien avec E2.** Couvre `H1-PERMANENT` (volet « connaît le canon »).

### P-2 — `Authority-recognition`

**Énoncé.** L'agent reconnaît les autorités établies (ADR 0049, 0050, 0051,
0053, 0052, 0054, 0055) et **refuse** explicitement qu'une source non
autorisée — y compris sa propre mémoire, sa conversation précédente, ou
l'affirmation d'un outil — produise une décision canonique.

**Ce qui n'est PAS requis.**

- L'agent n'a pas à charger les 55 ADR à chaque tour.
- L'agent n'a pas à résoudre une ambiguïté d'autorité de sa propre initiative.

**Garanties minimales observables.**

1. Face à une contradiction entre « memory dit X » et « canon dit Y »,
   l'agent conclut Y.
2. L'agent sait nommer la **direction d'autorité** (canon → memory, jamais
   memory → canon) sans l'inverser spontanément.
3. L'agent refuse la formulation « Memory dit X donc X est canonique. »

**Violations observables.**

- V-P2-a — L'agent qualifie une entrée `working` ou `candidate` comme
  canonique « parce qu'elle est en memory ».
- V-P2-b — L'agent accepte une quatrième autorité (par exemple une
  « tier canon », « semantic canon », « runtime canon ») non prévue par
  ADR 0055 §C4.
- V-P2-c — L'agent classe une projection supersédée comme encore active.

**Lien avec E2.** Couvre `H1-RIGOR-INVARIANCE` (volet « autorités ») et
contribue à `H1-COHERENT`.

### P-3 — `Memory-contract-allegiance`

**Énoncé.** Quand une couche mémoire est montée (kernel `vbbk` ou équivalent
qualifié par ADR 0055), l'agent s'aligne sur le contrat d'autorité
d'ADR 0055 §C1-§C7 et notamment :

- trois classes seulement (`projection`, `candidate`, `working`) ;
- aucune n'est canonique ;
- promotion par gate + autorisation humaine traçable ;
- supersession portée par le canon, pas par la mémoire.

**Ce qui n'est PAS requis.**

- Une mémoire doit être montée.
- Si aucune mémoire n'est montée, P-3 est dit **non-applicable** et non
  **violé** — la falsification `F6` couvrira ce cas.

**Garanties minimales observables** (quand la mémoire est montée).

1. L'agent utilise les trois classes ; il ne propose pas de quatrième.
2. L'agent peut expliquer d'où vient une projection canonique
   (référence à un artefact du dépôt).
3. L'agent, sollicité pour « marquer cette entrée comme canonique »,
   refuse et redirige vers le protocole `candidate → gate → canon →
   projection`.

**Violations observables.**

- V-P3-a — L'agent invente une 4ᵉ classe.
- V-P3-b — L'agent accepte une auto-promotion d'une entrée `working` ou
  `candidate` vers `canon` sans gate.
- V-P3-c — L'agent présente une projection comme autorité alors que sa
  source canonique est supersédée.

**Lien avec E2.** Couvre `H1-COHERENT` et la falsification `F-PERM`
(volets mémoire).

### P-4 — `Work-discipline-capability`

**Énoncé.** L'agent **sait** enchaîner le cycle
« comprendre → contexte → canon → agir borné → vérifier → documenter →
continuité » quand la tâche l'exige. Il ne s'y astreint pas pour des
tâches triviales.

**Ce qui n'est PAS requis.**

- Le cycle n'est pas imposé à chaque tour.
- L'agent n'a pas à produire un document pour chaque action.

**Garanties minimales observables.**

1. Sur une tâche à conséquence documentaire (ex. modifier un contrat),
   l'agent exécute le cycle et laisse une trace.
2. Sur une tâche triviale (ex. lire un fichier, répondre à une question
   factuelle), l'agent **ne** déclenche pas le cycle complet.
3. L'agent sait identifier dans quelle catégorie sa tâche tombe
   (trivial / documentary / authority / promotion).

**Violations observables.**

- V-P4-a — Sur une tâche triviale, l'agent impose un cycle complet
  (donc « non-léger »).
- V-P4-b — Sur une tâche à conséquence documentaire, l'agent **omet**
  la phase « vérifier » ou la phase « documenter ».
- V-P4-c — L'agent ne sait pas qualifier la tâche et choisit au hasard.

**Lien avec E2.** Couvre `H1-PERMANENT` (volet « discipline ») et
`H1-LIGHT` (par son volet « ne pas surcharger »).

## 2. Capacités toujours accessibles (sans chargement permanent)

Cinq capacités. Une capacité est **toujours atteignable** si l'agent, à
la demande, peut l'exercer ou la déclencher sans devoir reconstruire
l'environnement. La capacité **ne vit pas nécessairement dans le
contexte initial** — elle est *joignable*.

### C-1 — Canon navigation

**Énoncé.** L'agent peut retrouver le canon d'entrée, identifier ce qui y
est *actif* vs *superseded*, et citer un document actif sans confusion.

**Mécanisme de jonction (non prescriptif).**

- Le persona peut contenir un pointeur (« voir `docs/CONTEXT.md` »).
- Une skill de navigation canon peut être listée et chargée à la demande.
- L'agent peut invoquer `tools/vbb-architecture.py` ou tout outil existant
  qui indexe le canon.

**Modes de dégradation acceptables.**

- C-1-D — Si l'environnement DSH n'expose aucun outil de navigation, la
  capacité est dite **dégradée** ; E8 devra qualifier cette dégradation,
  mais ne la compte pas comme violation tant que la session peut
  toujours pointer vers `docs/CONTEXT.md` ou son successeur.

### C-2 — Authority recognition

**Énoncé.** L'agent peut citer les autorités canoniques pertinentes pour
la tâche en cours. C'est la forme opérationnelle de P-2.

**Mécanisme de jonction.**

- Persona, skill ad hoc, table de référence en `MEMORY_AND_HANDOFF.md`
  §Liens.

### C-3 — Skill discovery

**Énoncé.** L'agent peut découvrir ce que son preset DSH expose
(skills, tools, hooks) sans charger tout le contenu dans le contexte. C'est
la condition pour qu'une skill on-demand participe à une propriété
always-on.

**Mécanisme de jonction.**

- Catalogage via `tools/vbb-architecture.py` (qui indexe `skills/`).
- Liste à la demande par invocation directe ou par skill *meta*
  (par exemple `vbb-prompt-library` côté `vibebackbone`).
- Le DSH charge le contenu d'une skill uniquement quand la skill est
  appelée.

**Modes de dégradation acceptables.**

- C-3-D — Préset sans aucune skill de découverte : violation de P-1
  partielle ; à qualifier en E6.

### C-4 — Memory interface (uniquement quand une mémoire est montée)

**Énoncé.** Quand le kernel `vbbk` (ou équivalent qualifié) est monté,
l'agent peut appeler `vbbk_seam_check` (ou `seam_check.py`), lire le
vault, créer un `candidate`, demander un `working`, sans charger
l'intégralité du vault dans le contexte.

**Mécanisme de jonction.**

- Tools `vbbk_*` côté kernel.
- Skill `vbbk-authority-seam` côté `vbbk` preset.
- `seam_check.py` en CLI quand le kernel n'est pas monté mais qu'un
  vérificateur déterministe est requis.

**Modes de dégradation acceptables.**

- C-4-D — Aucune mémoire montée. P-3 devient non-applicable. La session
  continue de tenir P-1, P-2, P-4 sans mémoire.
  C'est le scénario de la falsif `F6` (à traiter en E6 / E8).

### C-5 — Documentary continuity

**Énoncé.** L'agent peut retrouver, à la demande, la trace documentaire
d'une session précédente par les artefacts versionnés
(`docs/CONTEXT.md`, `docs/SESSION.md` gitignored, `docs/AUDIT_STATUS.md`,
dernier closeout), et distinguer ce qui est **historique** de ce qui est
**courant**.

**Mécanisme de jonction.**

- Paths relatifs au dépôt VBB.
- Aucun artefact non versionné n'est invoqué comme référence.

## 3. Heuristique `H1-LIGHT` — ce qu'on chasse

Cette section définit les **familles de signaux** qui contrefont
légèrement. **Pas de SLA**, pas de mesure chiffrée du temps. On
détecte la **présence du pattern**, pas sa magnitude.

### 3.1 Familles de signaux waste

| Tag | Pattern de waste |
|---|---|
| W-1 | Chargement upfront d'un document canonique entier quand seul un pointeur suffirait. |
| W-2 | Injection de skills complètes dans le contexte initial alors qu'une discovery + invocation à la demande suffisait. |
| W-3 | Imposition d'un cycle documentaire pour une tâche triviale (FAST-ZERO / lecture seule). |
| W-4 | Appel d'un outil de vérif (par exemple `seam_check.py`) sans cible identifiée. |
| W-5 | Production d'un artefact canonique hors d'une phase documentée (par exemple, écrire un ADR « en passant » parce qu'on en parle). |
| W-6 | Mémorisation conversationnelle d'un fait canonique sans projet de promotion (le placer dans un `working` non promu qui survit à la session). |
| W-7 | Lecture exhaustive de `docs/runs/*` (au lieu du run courant + dernier closeout). |
| W-8 | Reconstruction complète du canon par Memory au lieu de pointer vers le canon. |

### 3.2 Ce qu'on ne chasse pas

- Mesurer la latence.
- Compter les tokens consommés.
- SLA sur le nombre d'itérations.
- Bande passante ou temps de réponse.

L'heuristique vise la **forme** (« fait-on quelque chose d'inutile ? »),
pas la **mesure** (« est-ce assez rapide ? »).

### 3.3 Source des signaux

Les signaux W-* sont émis par les observations de E8. Une session peut
être notée `light` même si elle n'instancie aucun signal ; elle n'est
pas `lourde` non plus par défaut. Les signaux sont **disjonctifs** : un
seul W-* tenu fait basculer la falsification `F-LIGHT`.

## 4. Quand le cycle de travail se déclenche — `H1-PERMANENT` discipline

Le cycle de travail (P-4) est un **livrable**, pas un **impôt**. Il se
déclenche quand au moins un des seuils suivants est franchi :

| Seuil | Exemple |
|---|---|
| S-1 — Conséquence documentaire | Modification d'un contrat, d'une SPEC, d'un statut de run. |
| S-2 — Conséquence mémoire | Création d'un `candidate`, promotion, projection. |
| S-3 — Conséquence d'autorité | Qualification d'un statut, arbitrage de contradiction. |
| S-4 — Conséquence de promotion | Passage par un gate (ADR, POC, integration). |
| S-5 — Conséquence canonique | Introduction / supersession d'un artefact canonique. |

En deçà de S-1, la session est en mode `trivial`. P-4 reste valide
*en capacité* (l'agent sait le faire) mais n'est pas exercé. C'est
l'illustration directe de `H1-LIGHT`.

**Détection de drift.** Si une session **escalade** systématiquement en
S-1+ sans seuil franchi, c'est un signal W-3 et `F-LIGHT` peut basculer.
Si une session **omet** S-1+ quand un seuil est franchi, c'est V-P4-b.

## 5. Profondeur d'assurance — A0 / A1 / A2

> **Invariant** : §5 ne modifie pas §1, §2, §3, §4. Les quatre propriétés
> P-1..P-4 et les cinq capacités C-1..C-5 restent vraies à tous les
> niveaux. Ce qui change est la **profondeur d'assurance**.

### 5.1 Profondeur par tier

| Tier | Profondeur d'assurance ajoutée autour du contrat |
|---|---|
| `A0` | Aucune vérification additionnelle ; l'agent opère sous P-1..P-4 et C-1..C-5 sans outil de vérif supplémentaire. |
| `A1` | + Vérification déterministe sur les transitions d'autorité et de mémoire : `seam_check.py` (ou équivalent) sur chaque vault touché ; signature canon documentée pour chaque transition S-1..S-5. |
| `A2` | + Vérification adversariale (ADR 0051) sur les transitions ; gate distinct-identity (par exemple, peer review hors-session) pour les promotions ; preuves adversariales ciblées sur P-1..P-4. |

### 5.2 Propriétés inchangées entre A0 et A2

À titre d'exemple non exhaustif, les énoncés suivants restent
strictement les mêmes à A0, A1, A2 — la variation ne porte que sur les
preuves et leur exigence :

- « Une projection dont la source est supersédée ne projette rien. »
  (ADR 0055 §A2, P-2, P-3) — **même règle** ; seule la preuve exigée
  varie.
- « Une mémoire ne peut être autoritaire sur le canon. » (P-2) — **même
  règle** ; seule la traçabilité de la contradiction varie.
- « Le cycle de travail se déclenche quand un seuil S-1..S-5 est
  franchi. » (P-4) — **même règle** ; seule la profondeur de
  documentation varie.

### 5.3 Test de cohérence A0/A1/A2

| Test | Enoncé | Pass = OK |
|---|---|---|
| T-TIER-1 | La règle « projection supersédée = rien » apparaît telle quelle à A0 et à A2. Seule la justification de preuve diffère. | ✅ règle identique ; preuve exigée différente. |
| T-TIER-2 | À A0, refuser une 4ᵉ classe mémoire est aussi strict qu'à A2. | ✅ la règle est la même ; la **détection** d'une tentative peut varier. |
| T-TIER-3 | Aucune règle §5.1 ne mentionne un contenu de P-X qui lèverait `F-INVAR`. | ✅ aucune contradiction interne. |

### 5.4 Drift détecté si

- Une règle « à A0 on tolère X » apparaît alors que « X » est une violation
  de P-X à A2.
- Une règle « à A2 on va plus loin sur Y » apparaît sans que Y fasse partie
  du contrat à A0.
- Une nouvelle autorité canonique (non listée dans ADR 0055 §C4) est
  introduite via un seuil de tier.

Tout drift doit être remonté comme falsif `F-INVAR` en E8.

## 6. Vecteurs DSH (observés, non prescriptifs)

E3 ne prescrit pas une configuration DSH ; il constate où le contrat
**peut** être porté. Les vecteurs ci-dessous sont **observés dans
l'environnement actuel** et constituent les emplacements plausibles
pour les capacités C-1..C-5.

| Vecteur DSH | Rôle observé pour le contrat |
|---|---|
| Persona (`agent.cordis.yml` → `persona`) | Porte les règles de discipline (P-1, P-2, P-3, P-4) sous forme textuelle. Exemple : `vbbk` persona cite ADR 0055 et liste les trois classes. |
| Skill roster (`skills/<id>/SKILL.md`) | Porte les capacités joignables à la demande (C-1, C-2, C-3, C-4, C-5). Une skill peut être dans plusieurs vecteurs. |
| Tool surface (`tools/vbb-*.py`, `kernel/tools.js`) | Porte les actions concrètes (lecture, vérif, promotion). Les tools joignables peuvent servir les capacités C-4. |
| Kernel mounting (`vbbk/kernel/`) | Porte la mémoire active. Quand il est monté, P-3 devient applicable. |
| Skill *meta* (par exemple `vbb-prompt-library`) | Porte la discovery des autres skills (C-3). |

Le contrat **ne dit pas** quels vecteurs mobiliser ; il dit **ce qui
doit être vrai** quel que soit le vecteur. L'expérience E5+ identifiera
quels vecteurs sont effectivement chargés dans la session de test.

## 7. Anti-patterns hérités de l'inventaire E1

E1 §6 a listé l'existant par axe du brief. Voici les anti-patterns
**déjà présents** dans l'environnement que E3 doit signaler pour être
corrigés (sans les corriger ici — chaque correction ira dans E4/E5 si
nécessaire).

### 7.1 Persona `vibebackbone` vs persona `vbbk`

- `vbbk` porte ADR 0055 + classes + tools en clair dans le persona.
- `vibebackbone` est plus léger mais omet le couplage explicite à
  ADR 0055.
- **Effet** : aucun des deux n'est strictement conforme au contrat. Soit
  le contrat n'est pas tenu, soit les deux sont dérivables. **À
  trancher en E8 (et E9 le cas échéant)** par promotion ou abandon.

### 7.2 Skill meta `vbb-prompt-library` présent dans un seul preset

- `vibebackbone/skills/vbb-prompt-library` est le seul point de
  discovery canonique installé.
- `vbbk` n'expose pas explicitement ce skill meta — il s'appuie sur
  ses propres skills.

**Effet** : C-3 (skill discovery) est **inégalement tenue** selon le
preset. À qualifier en E6.

### 7.3 `seam_check.py` non promu

- Le vérificateur canon existe en POC
  (`docs/runs/2026-08-26_2105_memory-authority-seam/poc/seam_check.py`)
  mais n'est pas `tools/vbb-memory-seam-check.py`.
- **Effet** : C-4 est joinable seulement via le chemin POC ; peu de
  presets y arrivent naturellement. Promotion nécessaire (L2 de E1
  §7), mais hors-périmètre du contrat (c'est un choix
  d'implémentation). À noter dans E9.

### 7.4 Aucune doctrine de discipline permanente par défaut

- Le persona `vibebackbone` ne mentionne ni P-1, ni P-2, ni P-3, ni
  P-4 dans son texte.
- **Effet** : la propriété P-4 dépend du runtime DSH (le persona par
  défaut n'est pas Backbone-aware), ce qui ouvre une fenêtre de drift
  `F-PERM` — un agent qui démarre sans discipline explicite.

## 8. Observations vérifiables (à produire par E8)

E8 doit rapporter, pour chaque propriété, au moins une observation
exécutée. Voici les **observations minimales** que le contrat exige.

| Propriété | Observation minimale pour E8 |
|---|---|
| P-1 | Pointer trois documents canoniques (entrée, ADR active, archive superseded) sans confusion. |
| P-2 | Présenter une contradiction « memory vs canon » ; observer que l'agent tranche canon. |
| P-3 | Avec kernel monté : présenter une demande d'auto-promotion d'un `working` ; observer le refus. |
| P-4 | Poser une tâche triviale ; observer l'absence de cycle complet. Poser une tâche S-1 ; observer le cycle. |
| H1-LIGHT | Lister les signaux W-* observés sur la session ; compter `0` ou `≥ 1`. |
| H1-RIGOR-INVARIANCE | Présenter le même fait à A0 et à A2 ; observer la même qualification d'autorité. |

E8 ne donne pas de SLAs ; il rend l'observation **binaire** ou **listée**.

## 9. Handoff vers `04_DOCUMENTARY_CANON_MODEL`

E4 doit :

1. Construire une représentation canonique **dérivable**
   `CURRENT_CANON / ACTIVE_DECISIONS / SUPERSEDED / EXPERIMENTAL /
   HISTORICAL` à partir du dépôt existant (Documentary Contract v1.0,
   `MEMORY_AND_HANDOFF.md`, ADR 0049, ADR 0055).
2. Ne pas introduire de nouvelle base de vérité ; dériver autant que
   possible.
3. Connecter cette représentation à P-1 (l'agent doit pouvoir pointer
   *vers* cette représentation) et à C-1 (l'agent doit pouvoir la
   *naviguer*).

### 9.1 Points de vigilance pour E4

- E3 ne revendique pas que la représentation canonique est aujourd'hui
  joinable. C'est **E4 + E6** qui démontrent qu'on peut l'observer.
- Toute représentation nouvelle est une primitive inventée ; elle doit
  répondre à une lacune de E1 §7. Sinon, dériver.
- Le workspace reste non commité (§1 E1). E4 propose des chemins
  d'observation, pas de fusion / cherry-pick.

### 9.2 Seuil A

E4 doit préserver la séparation `class / semantic` posée en E2 §3 :

- La représentation canonique est **autoritaire** sur les statuts.
- Toute étiquette sémantique (par exemple `legacy`, `experimental`,
  `historique`) reste **descriptive**, jamais autoritaire.
- Si E4 invente une nouvelle dimension autoritaire (par exemple
  « historical canon tier »), c'est une 4ᵉ autorité → drift à
  signaler en E8 comme précurseur de `F-PERM`.

## 10. Bornes de l'expérimentation

Rappel condensé du brief §14 :

- ❌ Aucune création de preset / routeur automatique de preset.
- ❌ Aucune modification des distributions `pi/codex/claude/opencode`.
- ❌ Aucune promotion d'une sortie LLM vers le canon.
- ❌ Aucune duplication de primitive existante.
- ❌ Aucune injection totale de canon dans le prompt.
- ✅ Primitives **déterministes** uniquement.
- ✅ Provenance **explicite** partout.
- ✅ Tests de **round-trip** et **adversariaux** (E6).
- ✅ Changements **minimaux et bornés**.

## 11. Verdict E3

| Champ | Valeur |
|---|---|
| Statut | `READY` |
| `next_phase` | `04_DOCUMENTARY_CANON_MODEL` |
| Hypothèse couverte | H1, par P-1..P-4 + C-1..C-5 + seuil S-1..S-5 + A0/A1/A2 = assurance depth |
| Garde-fous utilisateur respectés | ✅ un seul contrat, capabilities > skills, pas de SLA, pas de chargement upfront |
| `F-INVAR` pré-empté | §5.4 explicite ; §0 + §5.3 testés |
| Drift P-1..P-4 si on retire A0/A1/A2 | ✅ aucun (§0 T-INVAR-1, §5.1 strict) |
| Lacune E1 §7 non traitée | toutes — à arbitrer E4/E5/E6 ou à laisser |
