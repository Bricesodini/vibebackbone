---
context_role: hypothesis
phase: 02_HYPOTHESIS
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A2 (hypothesis-level; E3+ will downgrade to A1/A0 where no canon touch)
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T10:45:00Z"
ended_at: "2026-08-28T11:45:00Z"
next_phase: "03_ALWAYS_ON_CONTRACT"
artifacts_consumed:
  - "01_CURRENT_STATE.md"
artifacts_produced:
  - "02_HYPOTHESIS.md"
depends_on:
  - "ADR 0049"
  - "ADR 0050"
  - "ADR 0051"
  - "ADR 0053"
  - "ADR 0055"
supersedes: []
blocks:
  - "E3_ALWAYS_ON_CONTRACT"
  - "E4_DOCUMENTARY_CANON_MODEL"
  - "E5_MEMORY_INTEGRATION_MODEL"
related:
  - "docs/adr/0055-memory-authority-seam.md"
  - "docs/runs/2026-08-26_2105_memory-authority-seam/POC.md"
---

# 02_HYPOTHESIS — une hypothèse falsifiable unique

> E2 reformule le §1 du brief utilisateur en **une** hypothèse falsifiable.
> Les sous-affirmations sont étiquetées comme conséquences observables, pas
> comme des hypothèses indépendantes : un verdict sur H1 les emporte toutes.
> L'arbitrage du conflit 3-classes (ADR 0055) vs 9-catégorisation (brief §6)
> est posé en §3.

## 1. Hypothèse centrale — `H1`

> **H1**. Une session DeepSeek Harness peut opérer sous une discipline
> VibeBackbone **toujours présente** (permanente, légère, cohérente), dans
> laquelle faire varier l'intensité de qualification (A0 / A1 / A2) ne modifie
> jamais le canon documentaire, les autorités établies, ni la définition des
> primitives Backbone — uniquement la profondeur de vérification.

### 1.1 Décomposition de H1 en 4 observables dérivés

| Étiquette | Affirmation observable | Critère de mesurabilité |
|---|---|---|
| `H1-PERMANENT` | À chaque démarrage d'une session DSH, une discipline Backbone minimale identifiable est montée. | Trace observable dans le persona / skill roster / pointer vers `MEMORY_AND_HANDOFF.md` et `CONTEXT.md` ; absence détectable = falsification. |
| `H1-LIGHT` | La discipline permanente n'ajoute pas un overhead disproportionné à une tâche triviale. | Heuristique de budget : pas de cycle complet « comprendre → canon → agir → vérifier → documenter → continuité » imposé pour un débugage trivial. Vérifiable par observation de sessions courtes (`FAST-ZERO` / `FAST-MINIMAL`). |
| `H1-COHERENT` | Les invariants Backbone (autorité, canon, primitives) restent compatibles entre eux quel que soit le tier A en cours. | Aucun constat de contradiction entre (a) ce que la session avance, (b) ce que le vérificateur `seam_check.py` dit, (c) ce que `MEMORY_AND_HANDOFF.md` prescrit. Détectable par `seam_check.py --canon … --vault …`. |
| `H1-RIGOR-INVARIANCE` | Faire varier A0 → A1 → A2 change la profondeur de vérification demandée, jamais la définition des primitives (projection / candidate / working, canon, autorité, supersession). | Un même énoncé factuel énoncé à A0 et à A2 doit être qualifié par le **même** triplet d'autorité. Détectable par revue de réponses sur fixtures identiques à A0 et A2. |

`H1` est vraie si les **4** observables tiennent simultanément ; fausse si
**au moins une** échoue sous falsification observée.

## 2. Falsifications de `H1`

Les falsifications de `H1` sont distinctes des falsifications opérationnelles
`F1`–`F7` du brief §12 (qui testent les invariants mémoire / canon sur des
scénarios concrets). Les falsifications ci-dessous testent la **validité de
H1 elle-même** — c'est-à-dire la forme du socle permanent.

### 2.1 `F-PERM` — falsifie `H1-PERMANENT`

- **Énoncé** : il existe au moins un profil de session DSH où aucune trace
  observable de discipline Backbone n'est montée.
- **Verdict si observé** : `H1-PERMANENT` falsifié → `H1` falsifiée.
- **Test prévu** : ouvrir une session DSH avec un preset sans lien vers
  VBB, mesurer ce que le modèle déclare sur sa doctrine de travail.
- **Critère de passation** : la session, face à un changement canonique, doit
  exhiber au minimum les trois comportements de `H1-PERMANENT` (pointage vers
  canon actuel, reconnaissance des autorités, refus d'inventer une vérité
  parallèle).

### 2.2 `F-LIGHT` — falsifie `H1-LIGHT`

- **Énoncé** : la discipline permanente impose un overhead disproportionné
  pour une tâche triviale, transformant un `FAST-ZERO` en `STRUCTURED`
  implicite.
- **Verdict si observé** : `H1-LIGHT` falsifié → `H1` falsifiée.
- **Test prévu** : poser une question triviale (ex. « quelle est la SHA du
  HEAD actuel ? ») à une session A0 ; mesurer la profondeur de réponse.
- **Critère de passation** : la session répond directement, sans invoquer
  de cycle documentaire complet. Un warning léger sur la profondeur manque
  n'est pas une falsification ; une **escalade en cycle obligatoire** l'est.

### 2.3 `F-COHER` — falsifie `H1-COHERENT`

- **Énoncé** : la session, le vérificateur `seam_check.py`, et
  `MEMORY_AND_HANDOFF.md` donnent des qualifications incompatibles sur un
  même état observable.
- **Verdict si observé** : `H1-COHERENT` falsifié → `H1` falsifiée.
- **Test prévu** : exécuter `seam_check.py` sur un vault contenant une
  contradiction candidate/canon, puis demander à la session DSH d'évaluer le
  même vault.
- **Critère de passation** : les deux qualifications coïncident sur le
  code d'erreur (`CANDIDATE_CONTRADICTION_UNFLAGGED`, `PROJECTION_STALE_SUPERSEDED`, etc.).

### 2.4 `F-INVAR` — falsifie `H1-RIGOR-INVARIANCE`

- **Énoncé** : un même énoncé factuel est qualifié différemment selon le tier
  A.
- **Verdict si observé** : `H1-RIGOR-INVARIANCE` falsifié → `H1` falsifiée.
- **Test prévu** : présenter à la session un énoncé de supercession
  identique, sous persona A0 puis sous persona A2, et observer comment
  chaque tier qualifie l'autorité.
- **Critère de passation** : le triplet d'autorité (canon source, classe
  memory, perte-si-vault-disparaît) doit être identique à A0 et A2. La
  variation tolérée est la profondeur de preuve (`H1-RIGOR-INVARIANCE`
  autorise que A2 exige une preuve de plus, pas une qualification
  différente).

### 2.5 Règle de verdict globale

| Issue | Verdict H1 |
|---|---|
| 0 falsification observée | `BACKBONE_DSH_FOUNDATION_VALIDATED` |
| 1 ou 2 falsifications observées (mineures) | `BACKBONE_DSH_FOUNDATION_PARTIAL` |
| 1 falsification observée (F-PERM ou F-INVAR) | `BACKBONE_DSH_FOUNDATION_FALSIFIED` |
| ≥ 3 falsifications observées | `BACKBONE_DSH_FOUNDATION_FALSIFIED` |

Le seuil « falsification majeure » est posé sur `F-PERM` (le permanent est
non-négociable) et `F-INVAR` (la variation de rigeur change la philosophie :
régression interdite). Les autres falsifs dégradent vers `PARTIAL` si elles
sont isolées.

## 3. Arbitrage — 3 classes (ADR 0055) vs 9 catégories (brief §6)

Le brief §6 énumère 9 catégories sémantiques ; ADR 0055 §C2 fixe 3 classes
d'autorité. Les deux ne sont pas en conflit littéral — il faut les superposer.

### 3.1 Décision d'arbitrage

**Les 3 classes d'ADR 0055 sont canoniques et porteuses d'autorité. Les
9 catégories du brief §6 sont des étiquettes sémantiques de surface,
projetées sur les 3 classes, sans autorité propre.**

Un même objet de mémoire porte donc **deux** dimensions indépendantes :

- **Dimension d'autorité** (3 valeurs, canoniques) : `projection` /
  `candidate` / `working`. C'est la dimension que `seam_check.py` sait
  vérifier.
- **Dimension sémantique** (0 ou 1 des 9 catégories, non-canonique) :
  `fait canonique actuel` / `décision active` / `contexte de projet (courant)`
  / `contexte de projet (proposé)` / `hypothèse` / `expérience` /
  `résultat expérimental` / `état de travail temporaire` /
  `information superseded` / `historique`.

L'étiquette sémantique n'est **jamais** autoritaire : elle décrit, elle ne
décide pas. La décision (autorisation de promotion, qualification de
contradiction, perte-si-vault-disparaît) reste sur la classe d'autorité.

### 3.2 Table de projection sémantique → classe d'autorité

| Étiquette sémantique (brief §6) | Classe d'autorité par défaut | Règle de transition |
|---|---|---|
| `fait canonique actuel` | `projection` | si la source est supersédée → perd la projection (ADR 0055 §A2) |
| `décision active` | `projection` (si elle reflète une décision dans le dépôt) ou `candidate` (si la décision n'a pas encore été promouvée au dépôt) | promote via gate ADR 0049 |
| `contexte de projet` (partie courante) | `projection` | suit la source canonique |
| `contexte de projet` (partie proposée) | `candidate` | eligible à promotion si formalisé |
| `hypothèse` | `candidate` | promotion possible si validée |
| `expérience` | `candidate` | promotion possible si aboutit à une décision |
| `résultat expérimental` | `candidate` | promotion possible si POC validé |
| `état de travail temporaire` | `working` | non-promouvable directement (ADR 0055 §A3) |
| `information superseded` | **`projection` retirée** (n'est plus projetée du tout) | la source canon reste accessible via l'archive canon |
| `historique` | **`projection` retirée** | idem |

L'étiquette `superseded` et `historique` sont sémantiquement intéressantes
mais inertes du point de vue mémoire : ce qui était projection a cessé de
l'être. Aucun chemin ne permet de les re-projeter sans franchir la
discipline ADR 0055 §C3 (capture → qualification → candidate → promotion
gate → artefact canonique → projection).

### 3.3 Conséquence opérationnelle

Toute entrée mémoire doit déclarer :

```
{
  "class": "candidate" | "projection" | "working",   # autoritaire
  "semantic": "<une des 9 étiquettes>" | null         # descriptif
}
```

`semantic: null` est valide. `class` est obligatoire et décide ; `semantic`
documente et n'a aucun pouvoir de décision. `seam_check.py` ignore `semantic`
et ne vérifie que `class` (et la cohérence avec le canon).

### 3.4 Ce que cet arbitrage **n'**autorise pas

- Pas de 4ᵉ classe. Tenter d'introduire une classe supplémentaire
  (« semantic_canon », « tier_canon », « supersession_active ») serait une
  4ᵉ autorité concurrente → violerait `NO_PARALLEL_SEMANTIC_AUTHORITY`
  (ADR 0055 §C1) → rejet pré-écrit par cette expérimentation.
- Pas de promotion d'une étiquette sémantique vers une classe d'autorité.
  Une « hypothèse » ne peut pas devenir « projection » parce qu'elle est
  *forte* — elle ne peut le devenir qu'en traversant le protocole
  ADR 0055 §C3.

## 4. Liaison hypothèse ↔ falsifications opérationnelles (brief §12)

`H1` est falsifiable au niveau structurel par §2 ; les falsifications
opérationnelles `F1`–`F7` du brief §12 sont les **tests** qui exercent
les invariants sur des scénarios concrets. Voici la liaison :

| Falsif H1 | Falsif operationnelle brief | Test concret |
|---|---|---|
| `F-PERM` | (toutes, en cas d'absence totale de trace) | session A0 sans aucune discipline Backbone observable |
| `F-LIGHT` | — | session triviale qui escalade en cycle complet |
| `F-COHER` | `F1`, `F5`, `F7` | `seam_check.py` sur vault stale, observation session |
| `F-INVAR` | `F1`, `F5`, `F7` | qualification identique A0 vs A2 d'un même énoncé |
| (H1 implicite) | `F2`, `F3`, `F4` | test discernement canon vs doc ancien / réçent / concurrents |
| (H1 implicite) | `F6` | Memory absente, Backbone continue |

`F2` / `F3` / `F4` ne falsifient pas directement H1 mais exercent les
invariants documentaire / canon ; leur observation cohérente alimente
`H1-COHERENT`.

## 5. Cartographie hypothèse ↔ questions du brief §16

Le verdict final `09_RECOMMENDATION.md` doit répondre à Q1–Q10. Le tableau
ci-dessous pré-attribue chaque question à l'observable qui la portera.

| Question | Portée | Observable porteur dans ce run |
|---|---|---|
| Q1 — plus petite présence Backbone permanente | inventaire E1 + E3 | delta E3 ↔ E5 minimal nécessaire |
| Q2 — logique toujours active sans surcharge | falsif H1 | `F-LIGHT` |
| Q3 — découverte progressive des skills | falsif H1 | profil skill roster DSH côté E3 |
| Q4 — canon courant quasi-mécaniquement déterminable | falsif H1 + carte E4 | dérivation canon/superseded (E4) |
| Q5 — archivage propre au changement de canon | falsif H1 + protocole D0→D3 | E6 §D2 + falsif `F1` |
| Q6 — empêcher un doc superseded d'apparaître actif | falsif H1 + F2 | E4 + `F2` |
| Q7 — Backbone Memory reflète les changements | falsif H1 + F5 | E6 §D3 + `F5` |
| Q8 — mémoire stale détectable et non-autorité | falsif H1 + F1, F7 | `seam_check.py` + ADR 0055 §C5 |
| Q9 — session DSH reconstruit sans historique conversationnel | falsif H1 + F5 | E6 §D3 |
| Q10 — rigueur variable sans modifier autorités | falsif H1 + F-INVAR | E6 fixtures A0 vs A2 |

E8 et E9 reprendront ce tableau pour y placer les verdicts opérants.

## 6. Limites explicites de l'expérience

H1 ne prétend rien hors de son énoncé. Précisément :

1. **Pas une doctrine de distribution**. H1 ne s'applique qu'à DSH
   (`experimental_protocol: DSH-only`). Aucune conclusion ne vaut pour
   `pi` / `codex` / `claude` / `opencode`.
2. **Pas une généralisation à d'autres harnais**. Pas de conclusion sur
   `claude-code`, `aider`, etc.
3. **Pas une réforme du canon**. H1 s'appuie sur ADR 0049 / 0050 / 0051 /
   0053 / 0052 / 0054 / 0055 sans en modifier le contenu. Toute conclusion
   « il manque un ADR pour X » est **hors-H1** et renvoyée à un futur
   run dédié.
4. **Pas un test du kernel `vbbk` en isolation**. H1 inclut le candidat
   `vbbk` au sens où il sera confronté aux invariants M, mais ne se
   prononce pas sur les défauts propres du kernel hors-cadre (par
   exemple, JS ↔ Python parity, I2 distinct-identity — déjà notés dans
   §3 de E1, rappelés ici).
5. **Pas une mesure de performance**. H1 qualifie la « légèreté » par
   observation, pas par un SLA chiffré. Toute mesure chiffrée serait un
   artefact à part.

## 7. Critère de succès — reformulation stricte du brief §17

Le critère est composé. **Toutes** les conditions doivent être réunies :

```
ALWAYS_ON_WORK_DISCIPLINE
    F-PERM tenue AND F-LIGHT tenue
+
PROGRESSIVE_CAPABILITY_ACCESS
    skill roster variable, déterministe, sans injection totale
+
CURRENT_CANON_DISCOVERABLE
    dérivation CURRENT_CANON / ACTIVE_DECISIONS / SUPERSEDED observable
+
SUPERSEDED_STATE_EXPLICIT
    ADR 0055 §A2 actif (projection supersédée = retirée)
+
DOCUMENTARY_CONTINUITY
    E6 §D0 → D3 reproduit un changement canonique sans perte d'autorité
+
MEMORY_CANON_ALIGNMENT
    F1, F5, F7 tenues via seam_check.py
+
STALE_MEMORY_DETECTION
    codes CANONICAL_CLAIM_IN_MEMORY / PROJECTION_STALE_SUPERSEDED déclenchés
+
CROSS_SESSION_RECONSTRUCTION
    nouvelle session DSH, sans conversation antérieure, retrouve canon
+
NO_PARALLEL_SEMANTIC_AUTHORITY
    aucune 4ᵉ classe inventée, aucune mémoire auto-proclamée canonique
```

Chacune de ces conditions est binaire (tenue / non- tenue). Le verdict
global est :

- `BACKBONE_DSH_FOUNDATION_VALIDATED` : 9/9.
- `BACKBONE_DSH_FOUNDATION_PARTIAL` : entre 6/9 et 8/9.
- `BACKBONE_DSH_FOUNDATION_FALSIFIED` : ≤ 5/9 ou falsification `F-PERM` ou `F-INVAR`.

## 8. Handoff vers `03_ALWAYS_ON_CONTRACT`

E3 doit, à partir de H1 et de la table §3.2 :

1. Specifier le **seuil minimal observable** pour chaque dimension
   d'autorité (projection / candidate / working) — c'est l'inventaire E1
   §6 qui indique ce qui manque (L1, L2, L4–L7).
2. Specifier la discipline de travail Backbone permanente (§brief §2) sous
   forme de règles vérifiables, pas de prose narrative.
3. Specifier la discipline de découverte des skills (§brief §3) en termes
   de points de montage DSH (où vit le roster, comment il est sélectionné,
   comment il est invoqué à la demande).
4. Ne concevoir aucune primitive nouvelle sans démontrer d'abord (référence
   E1 §7) qu'une lacune existe et que la primitive la comble.

### 8.1 Points de vigilance pour E3

- Tout ajout de preset, de skill ou de tool au-delà de l'existant doit être
  défendu par référence à E1 §7 (lacune) et §6 (mapping).
- « Light » (H1-LIGHT) ne signifie pas « minimal » : signifie « sans
  bureaucratie imposée ». E3 doit distinguer les deux.
- La discipline de travail Backbone permanente (invariant A) doit être
  formulée en **verroux vérifiables**, pas en préambule moral.
- L'expérience garde le workspace non commité (§1 de E1). E3 ne doit
  proposer ni merger ni cherry-pick.

### 8.2 Points à arbitrer en E3 si E1/E2 ne suffit pas

Si E3 doit inventer une primitive, le seuil A bascule à A2 sur cette
décision, conformément à la table §6.1 de E1 (canon touchant = A2).
