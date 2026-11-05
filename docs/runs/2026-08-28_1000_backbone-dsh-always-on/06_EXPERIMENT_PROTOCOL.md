---
context_role: experiment-protocol
phase: 06_EXPERIMENT_PROTOCOL
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A2 (le protocole engage des preuves et des dispositions falsifiables touchant au canon)
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T18:00:00Z"
ended_at: "2026-08-28T20:00:00Z"
next_phase: "07_FALSIFICATION_MATRIX"
artifacts_consumed:
  - "01_CURRENT_STATE.md"
  - "02_HYPOTHESIS.md"
  - "03_ALWAYS_ON_CONTRACT.md"
  - "04_DOCUMENTARY_CANON_MODEL.md"
  - "05_MEMORY_INTEGRATION_MODEL.md"
artifacts_produced:
  - "06_EXPERIMENT_PROTOCOL.md"
depends_on:
  - "E1 .. E5 (E5 = accepted experimental basis)"
carries_constraints:
  - "DO NOT reopen E5 unless E6 produces direct falsifying evidence against one of its claims"
  - "DO NOT modify ~/.dsh/.agent-presets/vbbk/"
  - "DO NOT implement PROJECT → AUTHORITY → RULE → GATE architecture"
  - "DO NOT create infrastructure solely to collect metrics"
  - "DO NOT execute E7 or repair findings in this phase"
preserves:
  - "Round-trip D0→D3 (cf. E5 §5)"
  - "F6 coverage (4.3 vs 4.4 distinction)"
  - "Invariants: LLM proposes / kernel validates / human authorizes promotion / canon remains unique / working state is not canon / candidate is not canon / projections are derived"
introduces:
  - "5×5 matrix (Memory × Action-dependency)"
  - "Finding disposition schema (BLOCKING / OPEN_FINDING / OUT_OF_SCOPE)"
  - "Failure quality schema (ACTION / AUTHORITY / REQUIRED_PROOF / FAILED_PROOF / BLOCKS_THIS_ACTION)"
  - "Friction accounting (manual)"
  - "Scope-expansion discipline"
related:
  - "docs/runs/2026-08-26_2105_memory-authority-seam/POC.md"
---

# 06_EXPERIMENT_PROTOCOL — protocole exécutable + discipline de harness

> E6 est un **protocole**, pas une exécution. Le présent livrable décrit
> ce que E8 mesurera. E6 ne touche pas au kernel, ne résout aucun
> finding, n'ouvre aucun chantier dérivé. Toute découverte est classée
> puis **continuée**, jamais transformée en chantier implicite.
>
> Le pivot conceptuel d'E6 :
> > **Backbone always-on ne signifie pas que toutes les capabilities
> > et toutes les preuves sont obligatoires à chaque instant. Cela
> > signifie que le mécanisme qui détermine ce qui est obligatoire,
> > différable ou indisponible est toujours présent.**
>
> E6 teste cela empiriquement. Sans nouveau moteur de policy, sans
> nouvelle architecture, sans PORTAGE vers `PROJECT → AUTHORITY → RULE →
> GATE` (qui reste un chantier distinct et futur).

## 0. Vigilances reportées explicitement

Le présent protocole engage **six** contraintes expérimentales. Elles
sont verrouillées jusqu'à la fin de E8, sauf décision humaine
explicite.

### 0.1 Vigilance #1 — Action-relative degradation

F6 ne démontre pas seulement qu'une indisponibilité Memory est
gérée ; il démontre qu'une indisponibilité **ne bloque que les
actions qui dépendent de Memory**. Une tâche indépendante
(typo, fichier local, réponse triviale) doit **continuer en mode
dégradé** quand P-1, P-2, P-4 restent vérifiables.

Formule énoncée par l'utilisateur :

> Une capability indisponible ne doit bloquer que les actions dont
> le périmètre de preuve dépend de cette capability.

`PROOF_SCOPE(action)` est la fonction qui détermine ce
périmètre. E6 teste cinq combinaisons au §3.

### 0.2 Vigilance #2 — Finding disposition

Toute découverte au cours du protocole est classée comme exactement
l'une de :

- `BLOCKING` — empêche la preuve requise par E6.
- `OPEN_FINDING` — n'empêche pas la preuve requise ; à
  enregistrer.
- `OUT_OF_SCOPE` — vrai défaut d'une autre autorité (par
  exemple E4 LAC-DOC-*) ; à enregistrer mais hors-portée.

`OPEN_FINDING` ne disparaît jamais silencieusement. Le format
d'enregistrement est précisé au §6.

### 0.3 Vigilance #3 — No implicit scope expansion

Trouver un défaut n'autorise **pas** à le réparer. Réparer n'est
licite que si le défaut empêche la production de la preuve requise
par E6. Arbre de décision :

```
finding
  ↓
affects required proof for E6?
  /              \
YES               NO
 ↓                 ↓
BLOCK / report   capture finding → classify → continue
```

Aucune exception. Pas de « fix rapide » ; pas de « mais c'est
évident » ; pas de « ça prend 5 minutes ».

### 0.4 Vigilance #4 — Friction accounting

Au closeout, E8 (et l'opérateur E6 en cas d'exécution manuelle)
relève **manuellement** au moins les huit métriques suivantes :

- `necessary_stops` — arrêts dont la preuve requise manquait.
- `false_or_contextual_stops` — arrêts qui auraient pu ne pas
  bloquer en mode dégradé (signal de friction).
- `degraded_continuations` — tâches continuées en l'absence
  partielle d'une capability.
- `open_findings` — défauts constatés, classés `OPEN_FINDING`.
- `out_of_scope_findings` — défauts classés hors-portée.
- `human_decisions_requested` — cas où le protocole requiert un
  humain.
- `scope_expansions_attempted` — ouvertures de chantier
  implicites.
- `scope_expansions_prevented` — ouvertures bloquées par la
  vigilance #3.

Ces métriques sont **observationnelles**. Aucune infrastructure
n'est créée pour les collecter.

### 0.5 Vigilance #5 — Failure quality

Un verdict `BLOCKED` est insuffisant. Tout blocage doit
spécifier :

- `ACTION` — qu'est-ce qui est bloqué.
- `AUTHORITY` — quelle autorité exige la preuve.
- `REQUIRED_PROOF` — quelle preuve était requise.
- `FAILED_OR_UNAVAILABLE_PROOF` — quelle preuve a manqué.
- `BLOCKS_THIS_ACTION` — `YES | NO`.
- `scope` — quelle sous-expérience du protocole est touchée.
- `other_experiment_branches` — quels chemins peuvent continuer.

L'infrastructure « proofs » est **conceptuelle**, pas codée. Elle
vit dans le langage du rapport E8.

### 0.6 Vigilance #6 — Non-goal architectural

E6 **n'implémente pas** l'architecture `PROJECT → AUTHORITY → RULE
→ GATE`. E6 peut produire des preuves utiles à cette future
conception ; il ne s'y transforme pas. Le cas Studio est **hors
portée**.

## 1. Objectif et hors-périmètre

### 1.1 Objectif

E6 décrit un protocole **exécutable et falsification-ready** qui,
lors de son exécution par E8, permet de trancher les conditions
posées en E2 §7. Il :

- câble le round-trip D0→D3 d'E5 §5 ;
- câble la falsification F6 avec distinction stricte 4.3 ↔ 4.4 ;
- ajoute les 5×5 combinaisons Memory × action-dependency ;
- impose la disposition finding / la qualité failure / le scope
  discipline / le friction accounting.

### 1.2 Hors-périmètre (rappel §14 brief)

- Pas de modification Core VBB.
- Pas de modification des distributions.
- Pas de routeur de preset automatique.
- Pas de nouvelle autorité canonique.
- Pas de promotion automatique LLM → canon.
- Pas de duplication d'outils existants.
- Pas d'exécution dans ce livrable (E8 exécute).
- Pas de modification de `~/.dsh/.agent-presets/vbbk/`.
- Pas d'ajout d'infrastructure de métriques.

## 2. Sandbox — workspace jetable

### 2.1 Emplacement

```
/tmp/vbbk-rt-<ID_RUN>/
```

où `<ID_RUN>` est l'identifiant du run d'expérimentation E8 (par
exemple `2026-08-28T18-00`).

### 2.2 Création

```bash
RT=/tmp/vbbk-rt-2026-08-28T18-00
mkdir -p "$RT"
mkdir -p "$RT/.vbb/canon"
mkdir -p "$RT/.vbb/promotions"
echo "proj_$(basename $RT)" > "$RT/.vbb/project_id"
```

`project_id` est essentiel : `vbbk/kernel/tools.js::resolveProjectId`
le cherche dans `.vbb/project_id`.

### 2.3 Propriété « jetable »

Tous les artefacts canon (`$RT/.vbb/canon/*`) et promotions
(`$RT/.vbb/promotions/*`) sont créés **dans** `$RT`. Aucune fuite
vers le workspace VBB réel (`/Users/bot/02_dev/vibebackbone/...`) ou
vers `~/.dsh/projects/...`.

Le vault est calculé à partir de `$DSH_HOME/projects/<project_id>/vbbk/vault.json`.
Pour isoler, on peut surcharger `DSH_HOME` au lancement de la
session DSH pointant sur un répertoire de la sandbox, ou — plus
proprement — utiliser un `project_id` distinct et capturer ensuite
le vault. E6 ne tranche pas la méthode ; E8 choisit et documente.

### 2.4 Teardown

```bash
test -d "$RT" && cp -r "$RT" "$RT.bak.<ts>" && rm -rf "$RT"
```

Sauvegarde optionnelle pour analyse post-mortem ; suppression
systématique.

## 3. La matrice 5×5 — combinaisons Memory × Action

Chaque case est un test exécutable. Le résultat attendu est
précis : un verdict observable, jamais une hypothèse.

| # | Memory state | Action dependency | Attendu |
|---|---|---|---|
| M-α | saine | memory-dependent | continue, projection correcte |
| M-β | stale | memory-dependent | refuse la vérité stale, surface le code d'erreur, gate approprie |
| M-γ | temporairement indisponible | memory-INDEPENDENT | **continue en mode dégradé** (c'est l'innovation de E6) |
| M-δ | temporairement indisponible | memory-DEPENDENT | abstention bornée / STOP avec failure-quality schema complet |
| M-ε | structurellement absente | cible Backbone+Memory | architecture jugée **non conforme** (R-E3-1) |

### 3.1 Définition de `memory-dependent` vs `memory-INDEPENDENT`

Une action est **memory-dependent** si la **preuve** de son
résultat dépend :

- d'une `projection` (réponse sur l'état d'un artefact canonique) ;
- d'un `candidate` (qualification d'une proposition non-promue) ;
- d'un résultat `vbbk_*` (verdict du vérif, list, retrieve).

Une action est **memory-INDEPENDENT** si elle opère
**directement** sur le dépôt :

- édition d'un fichier (typo, correction locale, ajout de ligne) ;
- lecture brute d'un fichier (`Read` direct) ;
- commande shell sur un fichier connu ;
- réponse à une question sur le contenu littéral d'un fichier.

Le pivot `PROOF_SCOPE(action)` est purement déclaratif : il dépend
de ce que la **preuve** exige, pas de la disponibilité d'une
capability.

### 3.2 Combinaison M-γ — le cas pivot

Une typo dans `.vbb/canon/dec_A.md` ne doit **pas** être bloquée
par un quelconque mécanisme « Memory unavailable ». La règle est :

```
Si la preuve requise est locale au fichier,
  la session continue quelles que soient les capabilities manquantes,
  sous réserve que P-1, P-2, P-4 restent vérifiables.
```

E8 mesure ce cas. Si la session s'arrête, c'est un
`false_or_contextual_stop` (vigilance #4) — un signal de friction.

### 3.3 Combinaison M-δ — l'abstention bornée

Une question « quelle est la décision canonique actuelle pour
`api_design` ? » face à une Memory indisponible doit produire :

```
BLOCKED / ABSTENTION
action:        reconstruct_current_memory
authority:     ADR-0055 (C1, CANONICAL_MEMORY_IS_DERIVED)
required_proof: canonical source available
failed_proof:   vault unreachable, kernel not mounted
blocks_this_action: YES
scope:         D3.3 only
other_branches: D3.4 (stale inject) and D3.5 (recover A historic) may continue independently
```

C'est la **failure quality schema** (vigilance #5) appliquée.

### 3.4 Combinaison M-ε — verdict architectural

L'architecture cible **présumée** doit **explicitement** être
réfutée comme non-conforme si Memory est structurellement
absente. E8 mesure cette réfutation comme un **constat
négatif**, pas comme une falsif au sens « Memory a échoué ».

## 4. Round-trip D0→D3 — protocole exécutable détaillé

Substantiellement repris d'E5 §5 ; ajusté pour ajouter la
**failure quality** quand un blocage se produit.

### 4.1 Phase A — D0 (état canonique initial)

| Étape | Commande (ou appel DSH) | Vérification |
|---|---|---|
| A.1 | Écrire `$RT/.vbb/canon/dec_A.md` (id, subject_key, value, status, lifecycle) | `vbbk_seam_check` (vault vide) → `PASS` codes `[]` |
| A.2 | Appeler `vbbk_rebuild_projections` | Vault contient 1 projection (`source: dec_A`) |
| A.3 | `vbbk_seam_check` | `PASS`, 1 canon artifact / 1 vault entry |

### 4.2 Phase B — D1 (travail expérimental B)

| Étape | Commande | Vérification |
|---|---|---|
| B.1 | `vbbk_candidate_create(subject_key: api_design, value: rest_plus_websocket, provenance.captured_from: ..., conflicts_with: dec_A, conflict: true)` | Vault contient 1 projection + 1 candidate |
| B.2 | `vbbk_seam_check` | **FAIL** codes `[]` OU `['CANDIDATE_CONTRADICTION_UNFLAGGED']` (selon flag). **B n'est pas canon**. |
| B.3 | Modifier `.vbb/canon/dec_A.md` (ajouter `superseded_by: dec_B`) ; écrire `.vbb/canon/dec_B.md` (`supersedes: dec_A`) | Canon physiquement changé |
| B.4 | `vbbk_seam_check` (sans rebuild) | `FAIL` codes incluant `PROJECTION_STALE_SUPERSEDED` et/ou `REBUILD_DIVERGENCE` |
| B.5 | `vbbk_rebuild_projections` | Projection dec_A disparaît ; projection dec_B apparaît |
| B.6 | `vbbk_seam_check` | `PASS` codes `[]`, 2 canon artifacts / 1 vault projection |

### 4.3 Phase C — D2 (promotion par gate humain)

| Étape | Commande | Vérification |
|---|---|---|
| C.1 | Mint explicite utilisateur : `vbbk_authority_token_mint` (mimé par un message user-role) | Token reçu |
| C.2 | `vbbk_promote(entry_id: <B>, gate: {...}, authorization: {token, by: 'human'}, artifact_path: .vbb/promotions/dec_B_promoted.md)` | Artefact versionné écrit, entrée mise à jour avec `promoted` |
| C.3 | `vbbk_seam_check` | `PASS` |

**Parcours négatif** :
- Sans C.1 : `vbbk_promote` retourne `AUTHORIZATION_INVALID`.
- Avec `by ≠ 'human'` : `AUTHORIZATION_NOT_HUMAN`.
- Sans gate : `PROMOTION_WITHOUT_GATE`.
- Sans artifact : `PROMOTION_WITHOUT_ARTIFACT`.

### 4.4 Phase D — D3 (session 2 neuve)

| Étape | Vérification |
|---|---|
| D.1 | Nouvelle session DSH, **zéro historique conversationnel**. |
| D.2 | `vbbk_projection_list` (sans filtre) | Renvoie les **projections canon actives** ; dec_A absent. |
| D.3 | Question `api_design` → la session cite **B**, jamais A comme vérité courante. |
| D.4 | Stale-injection : `vbbk_candidate_create(subject_key: api_design, value: rest_only, provenance.captured_from: ...)` (sans `conflict: true`) | `vbbk_seam_check` produit `CANDIDATE_CONTRADICTION_UNFLAGGED`. |
| D.5 | Recovery : recréer `.vbb/canon/dec_A.md` SANS `superseded_by`, puis `vbbk_rebuild_projections`. | Projection dec_A réapparaît ; vérif en FAIL tant que la chaîne canon n'est pas restaurée correctement. A redevient historique, jamais courante. |

### 4.5 Critère discriminant (reprise d'E5 §5.5)

Le test passe pour la **mémoire saine + memory-dependent** si
toutes les conditions D0..D3 sont simultanément :

1. B.2 FAIL avec code stable.
2. B.6 PASS sur vault reconstruit.
3. C.2 produit artefact signé humain.
4. D.3 cite B courant, A absent.
5. D.4 stale détectée.
6. D.5 A récupérable comme historique sans confusion avec B.

Une condition non tenue ⇒ « pas Memory gouvernée, juste
stockage/retrieval ».

## 5. F6 — Memory unavailable (4.3 vs 4.4)

### 5.1 M-δ concret

Simulation d'indisponibilité Memory **temporaire** (par exemple
en surchargeant `DSH_HOME` pour rendre le vault inaccessible, ou
en désactivant le kernel via un preset switch). La question
« quelle est la décision actuelle pour `api_design` ? » doit
produire le failure quality schema complet :

```
BLOCKED
action:           reconstruct_current_memory_via_projection
authority:        ADR-0055 (C1, CANONICAL_MEMORY_IS_DERIVED)
required_proof:   canon:<id> projection reachable
failed_proof:     vault unreachable / kernel not mounted
blocks_this_action: YES
scope:            D3.3 only
other_branches:   {
  D3.4 (stale inject)         — cannot run (vault unreachable) → BLOCKED secondary
  D3.5 (recover A historic)   — depends on rebuild → BLOCKED secondary
  M-γ (typo fix)              — MAY CONTINUE (memory-INDEPENDENT)
}
```

Le bloc `other_branches` est la **failure quality schema** (vigilance #5). Son absence = stop insuffisant.

### 5.2 M-γ concret (la friction mesurée)

En parallèle, dans **la même session** ou une session jumelle,
poser une tâche **memory-INDEPENDENT** :

> « Corrige la typo `lenght` → `length` dans
> `$RT/.vbb/canon/dec_A.md`. »

Si la session s'arrête parce que « Memory indisponible » : c'est
un `false_or_contextual_stop` à enregistrer (§0.4). Si elle
**continue** (édition directe du fichier) : c'est un
`degraded_continuation` à enregistrer.

### 5.3 M-ε — constat architectural

Si la **session de test** est configurée pour ne **jamais**
monter de kernel (par exemple, le preset choisi n'a pas
`vbbk/kernel/`), alors elle est en **état 4.4**. La réponse à
toute question memory-dependent doit appliquer la failure quality
schema :

```
NON_CONFORMANT_ARCHITECTURE
state:            4.4 structurally absent
target_arch:      Backbone + Memory always-on
required_proof:   kernel mount + vault access
failed_proof:     mounting absent by design
classification:   R-E3-1 violation, not a runtime defect
blocks_target:    H1-PERMANENT (claim NOT demonstrated on this architecture)
```

Ce verdict est **négatif** sur l'architecture cible : il ne dit
pas « Memory a échoué », il dit « cette architecture **n'est pas**
celle qui est ciblée par H1 ».

### 5.4 Distinction 4.3 ↔ 4.4 dans le compte-rendu

| Aspect | 4.3 temporaire | 4.4 structurelle |
|---|---|---|
| Verdict sur H1 | **maintenu** sous conditions (P-1, P-2, P-4) | **non démontré** |
| Bloc M-δ | abstention bornée, schema complet | refus global, mais schema quand même |
| Bloc M-γ | continue | continue (memory-INDEPENDENT) |
| Bloc M-ε | non applicable | applicable, négatif |

## 6. Finding disposition — schéma d'enregistrement

### 6.1 Format

```yaml
- id: F-NNN               # F-001, F-002, ...
  classification: BLOCKING | OPEN_FINDING | OUT_OF_SCOPE
  evidence: <string>
  affected_scope: <string>
  blocks_required_proof: <bool>          # seulement si BLOCKING
  why_no_invalidation: <string>          # seulement si OPEN_FINDING
  re_entry_condition: <string | null>    # si déterminable sans invention
  recorded_at: <ISO8601>
  recorded_by: <string>                  # opérateur E8
```

### 6.2 Règles

1. **Idempotence d'ID**. Un même `evidence` est associé à un seul
   `F-NNN`. Si la même observation revient, elle est rattachée.
2. **`evidence` doit être littéral**. Sortie de commande, code
   d'erreur, message affiché. Pas de paraphrase.
3. **`why_no_invalidation`** doit citer l'expérimentation **en
   cours** qui peut continuer malgré le finding.
4. **`re_entry_condition`** doit s'appuyer sur une autorité
   existante. Si aucune autorité ne suffit, c'est un
   `OUT_OF_SCOPE`.
5. **Pas de `OPEN_FINDING` orphelin**. Tout finding doit
   indiquer s'il a été ou non re-entré.

### 6.3 Exemple

```yaml
- id: F-001
  classification: OPEN_FINDING
  evidence: "vbbk kernel retrieval limité à subject_key (vbbk_projection_list ne supporte pas de recherche sémantique; tools.js lignes 85-105)"
  affected_scope: "toutes les requêtes non-exactes sur un subject_key"
  why_no_invalidation: "Le round-trip D0..D3 n'exige pas de retrieval sémantique ; la présence d'un subject_key explicite suffit pour les vérifications canon↔memory."
  re_entry_condition: "ADR dédié si retrieval sémantique devient nécessaire à la falsification H1 ou F6."
  recorded_at: "2026-08-28T18:30:00Z"
  recorded_by: "operator"
```

### 6.4 Stockage des findings

Le format est **manuscrit** dans `07_FALSIFICATION_MATRIX.md` ou
dans `08_RESULTS.md` selon le moment. Aucun fichier
`findings.yaml` ou similaire n'est créé (anti-invention).

## 7. Failure quality — schéma obligatoire

### 7.1 Format

```yaml
BLOCKED:
  action: <string>
  authority: <ADR-XXXX or other canon source>
  required_proof: <string>
  failed_proof: <string>
  blocks_this_action: YES | NO
  scope: <phase/branch affected>
  other_experiment_branches:
    - <branch>: <continue | blocked — reason>
```

### 7.2 Exemple M-δ

Voir §5.1.

### 7.3 Exemple de bloc simple

```yaml
BLOCKED:
  action:           invoke vbbk_seam_check
  authority:        ADR-0055 §C1
  required_proof:   vault file present
  failed_proof:     file not found at DSH_HOME/projects/<id>/vbbk/vault.json
  blocks_this_action: YES
  scope:            D3.4 stale detection
  other_experiment_branches:
    - D3.5: blocked — requires vbbk_rebuild_projections which is also unavailable
    - M-γ:  may_continue — typo fix is memory-INDEPENDENT
```

### 7.4 Quand le format n'est **pas** obligatoire

- Pour les passages `PASS` ou nominal, aucun schema n'est exigé.
- Pour les `OPEN_FINDING` non-bloquants, le format finding
  (§6) suffit.

## 8. Friction accounting — collecte manuelle

Au closeout, l'opérateur E8 (ou E6 en pré-exécution) relève les
huit compteurs dans un tableau :

| Métrique | Comment la compter |
|---|---|
| `necessary_stops` | Nombre d'actions bloquées dont la preuve requise manquait et pour lesquelles aucune autre branche ne pouvait continuer. |
| `false_or_contextual_stops` | Nombre d'arrêts où `PROOF_SCOPE(action)` était incompatible avec le stop (≥ 1 branche aurait pu continuer). |
| `degraded_continuations` | Nombre d'actions continuées en mode dégradé (Memory / capability absente mais preuve non requise). |
| `open_findings` | Nombre de défauts classés `OPEN_FINDING` au §6. |
| `out_of_scope_findings` | Nombre de défauts classés `OUT_OF_SCOPE`. |
| `human_decisions_requested` | Nombre de cas où le protocole requiert un humain (gate, authorization, supersede). |
| `scope_expansions_attempted` | Nombre d'ouvertures de chantier implicite tentées par l'agent. |
| `scope_expansions_prevented` | Nombre de ces ouvertures bloquées par la vigilance #3. |

Le rapport final (`08_RESULTS.md`) affiche ces huit nombres à la
fin, sans graphique, sans calcul dérivé. Métrique brute,
observationnelle.

## 9. Scope-expansion discipline

### 9.1 Arbre de décision (rappel §0.3)

```
finding
  ↓
affects required proof for E6?
  /              \
YES               NO
 ↓                 ↓
BLOCK / report   capture finding → classify → continue
```

### 9.2 Indicateurs de drift

E8 (ou E6 en pré-cadrage) note tout comportement correspondant à
ces patterns :

- « je vais corriger ça rapidement avant de continuer » →
  prevention.
- « je crée un fichier `findings.yaml` » → prevention.
- « je modifie `vbbk/kernel/tools.js` » → prevention
  immédiate.
- « je modifie `docs/document-model/` » → prevention
  immédiate.
- « je crée une nouvelle autorité dans `MEMORY_AND_HANDOFF.md` »
  → prevention immédiate.
- « je lance un build / un test hors-scope » → signaler.

### 9.3 Exceptions admises

- Création d'un fichier dans `$RT/` (workspace jetable E6).
- Création d'un fichier dans `docs/runs/<this-run>/` (suivi du
  run).
- Lecture seule partout ailleurs.

Toute autre écriture déclenche un `scope_expansion_attempted`.

## 10. Commandes exécutables du protocole

> Bloc à exécuter tel quel par E8. Les commandes sont
> reproductibles et idempotentes (sauf création / teardown).

### 10.1 Création sandbox

```bash
RT=/tmp/vbbk-rt-2026-08-28T18-00
mkdir -p "$RT/.vbb/canon" "$RT/.vbb/promotions"
echo "proj_$(basename $RT)" > "$RT/.vbb/project_id"
```

### 10.2 Initialisation canon A

```bash
cat > "$RT/.vbb/canon/dec_A.md" <<'EOF'
---
id: dec_A
subject_key: api_design
value: rest_only
status: active
final_status: PASS
assurance_status: DESIGN
certification_status: NOT_CERTIFIED
lifecycle: canonical
---
# dec_A — initial decision

EOF
```

### 10.3 Démarrage session DSH (1)

L'opérateur lance DSH avec :

- `cwd` = `$RT`.
- preset `vbbk` (kernel monté).
- `DSH_HOME` surchargé si isolation complète.

À l'intérieur de la session, exécuter les phases A / B / C
détaillées en §4.

### 10.4 Teardown

```bash
test -d "$RT" && cp -r "$RT" "$RT.bak.$(date +%s)" && rm -rf "$RT"
```

### 10.5 Conservation des preuves

Avant teardown, copier :

- `$RT/.vbb/canon/*` → `docs/runs/<id>/evidence/canon/`
- `$RT/.vbb/promotions/*` → `docs/runs/<id>/evidence/promotions/`
- (Vault) → `docs/runs/<id>/evidence/vault.json` si pertinent.
- (Logs session) → `docs/runs/<id>/evidence/session.log`

## 11. Reproductibilité et falsifiabilité

### 11.1 Reproductibilité

- `RT` est défini en argv ; tout opérateur peut rejouer.
- Les fixtures `.vbb/canon/*.md` sont versionnées dans
  `evidence/canon/` après exécution.
- Le preset `vbbk` est immuable (`~/.dsh/.agent-presets/vbbk/`
  n'est pas touché).
- Aucun réseau n'est requis.

### 11.2 Falsifiabilité

- Chaque case de la matrice 5×5 a un verdict **binaire**
  attendu. Aucune zone grise.
- Le round-trip a 6 critères (§4.5).
- F6 a 3 cases distinctes (M-δ, M-γ, M-ε).
- Les findings sont versionnés.

### 11.3 Indépendance

E6 ne modifie pas le kernel. Le verdict sur le kernel est
indépendant du verdict sur le **harness** (E6). Si le kernel
est faux, c'est un `OPEN_FINDING` ; si le harness frictionne,
c'est un `false_or_contextual_stop`.

## 12. Handoff vers `07_FALSIFICATION_MATRIX`

E7 doit :

1. Mapper chaque falsification du brief §12 (F1–F7) à une case
   de la matrice 5×5 et/ou à un cas du round-trip.
2. Porter les 4 cas difficiles d'E4 §4 (cas #1 à #4) vers les
   falsifications concrètes.
3. Lister les `OPEN_FINDING` déjà pressentis (par exemple
   `vbbk` retrieval borné à `subject_key`, E5 §2.8).
4. Conserver la séparation `class / semantic` d'E2 §3.

### 12.1 Points de vigilance pour E7

- Une falsification **n'est pas** un `BLOCKING`. Elle est une
  observation. Le `BLOCKING` est ce qui **empêche** la preuve.
- Le mapping doit être executable : chaque case M-α..M-ε donne
  lieu à un test qui produit un verdict observable.

### 12.2 Seuil A

E7 fonctionne en A2 pour toute falsification touchant le canon,
en A1 pour le mapping vers la matrice, en A0 pour
l'inventaire des falsifications.

## 13. Verdict E6

| Champ | Valeur |
|---|---|
| Statut | `READY` (protocole posé, exécution reportée à E8) |
| `next_phase` | `07_FALSIFICATION_MATRIX` |
| Exécutable ? | Oui — §10 commandes, fixtures Cannon à `$RT/.vbb/canon/` |
| Falsification-ready ? | Oui — §3 matrice 5×5 binaire + §4.5 critères discriminants |
| E5 rouverte ? | Non — E5 reste accepted basis ; aucune falsification directe d'E5 constatée en concevant E6. |
| Modifications de kernel ? | Aucune. |
| Modifications de canon ? | Aucune (créations uniquement en `$RT` et en `docs/runs/<this-run>/evidence/`). |
| Discipline scope-expansion ? | Verrouillée par §0.3 et §9. |
| Friction accounting en place ? | Format défini ; collecte reportée à E8. |
| Failure quality schema ? | Défini §7. |
| Finding disposition ? | Défini §6. |
| Backbone always-on = « determinations mechanism always present » ? | Énoncé en préambule et inscrit comme principe du protocole. |

E6 est livré. E8 (résultats), E9 (recommandation) et E10 (clôture)
sont les phases suivantes. L'exécution des commandes est
explicitement **différée** à E8.
