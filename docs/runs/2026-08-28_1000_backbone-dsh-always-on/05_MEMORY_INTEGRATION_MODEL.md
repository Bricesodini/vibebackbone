---
context_role: memory-integration-model
phase: 05_MEMORY_INTEGRATION_MODEL
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A2 (les décisions de §6 — vbbk est A/B/C/D — touchent au rang ontologique du candidat)
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T15:30:00Z"
ended_at: "2026-08-28T18:00:00Z"
next_phase: "06_EXPERIMENT_PROTOCOL"
artifacts_consumed:
  - "01_CURRENT_STATE.md"
  - "02_HYPOTHESIS.md"
  - "03_ALWAYS_ON_CONTRACT.md"
  - "04_DOCUMENTARY_CANON_MODEL.md"
  - "$HOME/.dsh/.agent-presets/vbbk/kernel/auth.js"
  - "$HOME/.dsh/.agent-presets/vbbk/kernel/entry.js"
  - "$HOME/.dsh/.agent-presets/vbbk/kernel/extraction.js"
  - "$HOME/.dsh/.agent-presets/vbbk/kernel/tools.js"
  - "$HOME/.dsh/.agent-presets/vbbk/kernel/vault.js"
  - "$HOME/.dsh/.agent-presets/vbbk/kernel/verifier.js"
  - "$HOME/.dsh/.agent-presets/vbbk/skills/vbbk-authority-seam/SKILL.md"
  - "$HOME/.dsh/.agent-presets/vbbk/audit/2026-08-26_vbbk-quality-campaign/SYNTHESIS.md"
artifacts_produced:
  - "05_MEMORY_INTEGRATION_MODEL.md"
depends_on:
  - "ADR 0055 §C1-C7 + A1-A5"
  - "vbbk kernel — observed as-is"
carried_reservations:
  - "R-E3-1 reformulated (cf. §4 : quatre états de Memory)"
  - "R-E4-1 (cf. §7 : aucune nouvelle autorité introduite par E5)"
related:
  - "docs/adr/0055-memory-authority-seam.md"
  - "docs/runs/2026-08-26_2105_memory-authority-seam/POC.md"
---

# 05_MEMORY_INTEGRATION_MODEL — qualifier `vbbk` empiriquement

> E5 ne dit pas « `vbbk` est Backbone Memory ». E5 **lit** le code, **lit**
> le skill, **lit** la campagne d'audit et qualifie chaque responsabilité
> parmi `IMPLEMENTED` / `PARTIAL` / `NOT_IMPLEMENTED` /
> `OUT_OF_SCOPE_BY_DESIGN`. Le code et les comportements observables
> tranchent. La conclusion A/B/C/D est tirée de cette qualification, sans
> projection d'intention.

## 0. Vigilances reportées explicitement

| # | Intitulé | Application |
|---|---|---|
| 1 | Tester `vbbk` tel qu'il est, sans projection d'intention. | E5 ne réécrit **rien** dans `~/.dsh/.agent-presets/vbbk/kernel/`. E5 lit, qualifie, conclut. |
| 2 | Disponibilité ≠ optionalité architecturale. | §4 pose **quatre états** de Memory. P-3=N/A en F6 ne vaut pas pour l'architecture cible. |
| 3 | Déterminer empiriquement ce qu'est `vbbk`. | §1 lecture, §2 grid 12×4, §6 conclusion A/B/C/D. |
| 4 | Ne réparer ni `vbbk` ni le corpus. | §7 attribution corpus / `vbbk` / les deux sans aucune modification opportuniste. |
| — | Round-trip A→B obligatoire. | §5 protocole exécutable E6+. |

R-E3-1 (transférée d'E4) est reformulée en §4. R-E4-1 est honorée par
construction : aucune autorité nouvelle n'est créée ici.

## 1. Lecture du code `vbbk` — ce que le kernel fait

Six fichiers, 1143 lignes au total. Chaque ligne lue a été
mappée à une responsabilité ; rien n'a été pris « pour acquis » à
partir de la documentation seule. Les commentaires inline sont
traités comme du commentaire de design, pas comme une garantie
d'exécution : seule l'exécution du code tranche.

### 1.1 Inventaire des fichiers

| Fichier | Lignes | Rôle observé |
|---|---|---|
| `kernel/auth.js` | 40 | `AuthorityTokenBroker` — jeton SHA-256 single-use, session-scoped, mintable uniquement sur rôle `user`. Secret module-privé (post P2.a) ; `consume` rejette token absent / used / mismatch. |
| `kernel/vault.js` | 58 | Stockage JSON sérialisable à `$DSH_HOME/projects/<project_id>/vbbk/vault.json`. Schéma versionné (`SCHEMA_VERSION=1`). Append + update. |
| `kernel/entry.js` | 122 | Point d'entrée kernel : enregistre 8 tools sur `ctx.tools`, écoute `agent/inbox/inserted` (mint token + extraction auto) et `agent/turn-stopping` (clear tokens). |
| `kernel/tools.js` | 417 | 8 tools : `vbbk_projection_list`, `vbbk_candidate_create`, `vbbk_working_set`, `vbbk_promote`, `vbbk_seam_check`, `vbbk_rebuild_projections`, `vbbk_authority_token_mint`, `vbbk_extract`. Field filter `rejectCanonicalFields` au niveau tool. |
| `kernel/verifier.js` | 285 | Cœur ADR 0055 : `loadCanon`, `detectIntraCanon`, `rebuildProjections`, `check` (exécute tous les codes d'erreur), `c7Answers`. Code stable, model-free. |
| `kernel/extraction.js` | 221 | Pipeline 5 étages heuristique model-free : `passesT1 → splitFacts → deriveSubjectKey → deriveValue → validateCandidate`. Konservatif (« prefer to miss a fact than to write a wrong one »). |

### 1.2 Points d'entrée runtime observés

- `agent/inbox/inserted` (entry.js ligne 68) — déclenche
  `broker.mint(...)` + extraction optionnelle.
- `agent/turn-stopping` (entry.js ligne 110) — vide les tokens
  consommés.
- L'isolation est garantie par le realm `isolate: true` déclaré
  dans `agent.cordis.yml` du preset (cf. E1 §3).

### 1.3 Scope opératoire observé

Le kernel **ne connaît que** :
- `$DSH_HOME/projects/<project_id>/vbbk/vault.json` (stockage),
- `<cwd>/.vbb/canon/` (canon d'entrée pour le vérificateur),
- `<cwd>/.vbb/promotions/` (cible par défaut de `vbbk_promote`).

Le kernel **ne connaît pas** :
- `docs/CONTEXT.md`, `docs/document-convention.yaml`,
- les 5 vues documentaires d'E4,
- `tools/vbb-*.py`, `MEMORY_AND_HANDOFF.md`,
- la structure ADR du dépôt.

Ces **non-connaissances** sont des choix d'isolation
intentionnels ; il ne s'agit pas de défauts mais de **bornes
du kernel**. La conséquence est mesurée en §7.

## 2. Grid d'attribution — 12 responsabilités × 4 verdicts

| # | Responsabilité | Verdict | Évidence (fichier:ligne) |
|---|---|---|---|
| 2.1 | **Capture** | IMPLEMENTED | `extraction.js` pipeline complet ; `entry.js:68-108` déclenche l'extraction auto à chaque message user ; feature-flag `VBBK_EXTRACTION_DISABLED=1` (entry.js:66). Capture aussi possible via `vbbk_candidate_create` explicite. |
| 2.2 | **Classification autoritaire** | IMPLEMENTED | `verifier.js:11` `CLASSES = ['projection', 'candidate', 'working']` ; `verifier.js:144-148` rejette `CLASS_UNKNOWN`. Aucune porte d'entrée ne propose une 4ᵉ classe. |
| 2.3 | **Working state** | IMPLEMENTED (avec nuance) | `workingSetTool` (tools.js:161-186) ; `verifier.js:236-240` rejette `WORKING_WITH_SOURCE`. **Nuance** : `workingSetTool` **persiste** l'entrée dans le vault via `appendEntry` (tools.js:182), donc « working » est en pratique « éphémère mais persisté ». ADR 0055 §C2 dit « néant par définition si le vault disparaît » ; `vbbk` documente working comme « reasoning » (provenance.captured_from = 'reasoning') mais le survit à la session. C'est une **différence de design**, pas une violation. Marqué en §6.5. |
| 2.4 | **Promotion** | IMPLEMENTED | `promoteTool` (tools.js:190-286). Path check **avant I/O** (post P0, tools.js:216-227) ; token consommé à execute (`broker.consume`) ; gate `{name, verdict: 'PASS', run_id}` ; artefact versionné écrit ; entrée vault mise à jour avec bloc `promoted`. `WORKING_NOT_PROMOTABLE` (tools.js:239) bloque la promotion directe de working. |
| 2.5 | **Stockage durable** | IMPLEMENTED | `vault.js` complet : `readVault`, `writeVault`, `appendEntry`, `findEntry`, `updateEntry`. Schema versionné. Survit aux sessions. |
| 2.6 | **Projection** | IMPLEMENTED | `rebuildProjections` (verifier.js:74-85) dérive du canon les 5 dimensions (`status`, `final_status`, `assurance_status`, `certification_status`, `lifecycle`). `projectionListTool` (tools.js:85-106) liste par `subject_key`. Refus de `status_loc`/`local_status`/`memory_status` (`PROJECTION_LOCAL_STATUS_FIELD`). |
| 2.7 | **Reconstruction** | IMPLEMENTED | `rebuildTool` (tools.js:321-352) persiste les projections reconstruites (post P-recipe.3, see SYNTHESIS §Patches). Le round-trip T5 (destruction → reconstruction → vérif) est désormais green. |
| 2.8 | **Retrieval** | PARTIAL | `vbbk_projection_list` (filtre `subject_key`) + lecture vault. **Aucun retrieval sémantique** : pas d'embedding, pas de similarité, pas de LLM-side recall. Les seules requêtes sont par identifiant ou `subject_key`. Tout « retrieval intelligent » est porté par le LLM **au-dessus** du kernel, pas par le kernel. |
| 2.9 | **Invalidation / supersession** | PARTIAL | Le vérificateur **détecte** `PROJECTION_STALE_SUPERSEDED` (verifier.js:197-199) et **`REBUILD_DIVERGENCE`** quand la source canon est absente ou divergente. **Mais le kernel ne déclenche aucune invalidation active** : aucun tool « supprimer cette projection » ou « invalider ce vault entry ». La résolution est « l'utilisateur appelle `vbbk_rebuild_projections` ». C'est explicite par design (le LLM propose, le kernel valide) ; c'est noté en §6.5. |
| 2.10 | **Provenance** | IMPLEMENTED | `provenance.captured_from` exigé à la création (tools.js:137) ; pour `working` : `provenance.captured_from: 'reasoning'` (tools.js:179) ; pour `projection` rebuild : `provenance.captured_from: 'repo'` ou `run: 'rebuild'` (tools.js:339) ; l'extraction ajoute `extractor_version: 'vbbk-t1.0'` et un `source_text: fact.slice(0, 200)` (extraction.js:200-205). Traçabilité chiffrée à la racine. |
| 2.11 | **Stale detection** | IMPLEMENTED | Codes stables produits par le vérifier : `PROJECTION_STALE_SUPERSEDED`, `PROJECTION_STATUS_DIVERGES`, `PROJECTION_WITHOUT_SOURCE`, `REBUILD_DIVERGENCE`, `CANDIDATE_CONTRADICTION_UNFLAGGED`, `CONFLICT_AUTO_RESOLVED`, `C7_UNANSWERABLE`. Round-trip T5 validé. |
| 2.12 | **Synchronisation avec le canon** | PARTIAL | Le vérificateur **détecte** la divergence entre `entry.projected` et `canon[source]` pour chaque `projection` (verifier.js:200-205). **Mais le kernel ne déclenche pas une re-synchronisation automatique** : la divergence reste jusqu'à l'invocation de `vbbk_rebuild_projections`. Si une session oublie d'appeler rebuild après un changement canonique, la projection stale survit. Aucune alarme proactive. |

### 2.1 Bilan quantitatif

| Verdict | Compte |
|---|---|
| `IMPLEMENTED` | 9 |
| `PARTIAL` | 3 (retrieval, invalidation, sync) |
| `NOT_IMPLEMENTED` | 0 |
| `OUT_OF_SCOPE_BY_DESIGN` | 0 (aucune responsabilité explicitement hors-périmètre dans le code) |

Les 3 PARTIAL ne sont pas des bugs — ce sont des choix
d'isolation : le kernel laisse à l'utilisateur / au LLM la
décision de reconstruire ou non, plutôt que d'agir en silence.

## 3. Mapping ADR 0055 §C1–§C7 et A1–§A5

Le vérificateur de `vbbk` est explicitement aligné sur ADR 0055.
Lecture ligne à ligne, vérification d'application effective :

| Règle ADR 0055 | Application vbbk | Évidence | Verdict |
|---|---|---|---|
| `CANONICAL_MEMORY_IS_DERIVED` | projection must have source ; round-trip T5 | verifier.js:190-194 + rebuildTool | ✅ |
| `PROMOTION_IS_A_GATE` | promoteTool exige `gate.{name, verdict: PASS, run_id}` | tools.js:199-203 + verifier.js:180-182 | ✅ |
| `NO_PARALLEL_SEMANTIC_AUTHORITY` | rejet des CANONICAL_CLAIM_KEYS et CANONICAL_CLAIM_VALUES | tools.js:40-66 ; verifier.js:13-14, 91-104, 151-165 | ✅ |
| `CLASSES = {projection, candidate, working}` | refus de classes inconnues | verifier.js:11, 144-148 | ✅ |
| `projection` sans source | rejet `PROJECTION_WITHOUT_SOURCE` | verifier.js:190-194 | ✅ |
| `working` non-promouvable | rejet `WORKING_NOT_PROMOTABLE` + `WORKING_PROMOTED` + `WORKING_WITH_SOURCE` | tools.js:239 ; verifier.js:170-172, 236-240 | ✅ |
| `superseded` n'est pas `projection` | rejet `PROJECTION_STALE_SUPERSEDED` | verifier.js:197-199 | ✅ |
| Promotion artefact versionné | `writeFileSync` avec frontmatter complet | tools.js:240-274 | ✅ |
| Autorisation humaine (A5) | `AUTHORIZATION_INVALID` + `AUTHORIZATION_NOT_HUMAN` | tools.js:230-234 | ✅ |
| 5 dimensions lues du canon (C4) | `DIMENSIONS = ['status', 'final_status', 'assurance_status', 'certification_status', 'lifecycle']` | verifier.js:15 | ✅ |
| Pas de champs locaux de statut | rejet `status_loc`, `local_status`, `memory_status` | verifier.js:208-212 | ✅ |
| `subject_key` obligatoire (A1) | rejet `CANDIDATE_WITHOUT_SUBJECT_KEY` | verifier.js:217-220 | ✅ |
| Contradiction surfaced pas auto-résolue (C5) | `CANDIDATE_CONTRADICTION_UNFLAGGED`, `CONFLICT_AUTO_RESOLVED` | verifier.js:222-231, 248-258 | ✅ |
| Supersession vit dans le canon (C5) | rejet `MEMORY_SUPERSEDES_CANON` | verifier.js:233-235 | ✅ |
| C7 — trois questions | `c7Answers` retourne origin / authority / loss ; `C7_UNANSWERABLE` rejette | verifier.js:106-120, 243 | ✅ |
| Réponses C7 fixées par classe (A4) | tables fixes par `klass` | verifier.js:106-120 | ✅ |

**Résultat** : tous les invariants et amendements d'ADR 0055 sont
**techniquement appliqués** par le vérificateur de `vbbk`. Aucun
manquement au contrat ADR 0055 §C1-§C7 / A1-A5 au niveau
sémantique du kernel.

Ce que cela **ne prouve pas** : que la discipline est tenue dans
une session DSH réelle (E5 qualifie, E6 mesure).

## 4. Quatre états de Memory (reformulation R-E3-1)

La réserve R-E3-1 est reformulée en quatre états explicites. Le
**verdict E5** sur R-E3-1 est : ces quatre états doivent être
distingués dans la falsification `F6`, et dans le verdict
`H1-PERMANENT` final.

| # | État | Description | Verdict attendu sur H1 / sous-propriétés |
|---|---|---|---|
| 4.1 | **Memory disponible + saine** | Vault monté, vérificateur vert. | `H1-PERMANENT` ✅ ; `H1-COHERENT` ✅ ; `P-3` APPLICABLE ✅. |
| 4.2 | **Memory disponible + stale** | Vault monté, vérificateur FAIL sur des codes stables. | `H1-COHERENT` testé par la détection ; canon prioritaire ; `P-3` APPLICABLE. Le **verdict** final dépend du nombre de codes et de leur résolution. |
| 4.3 | **Memory temporairement indisponible** | Kernel non monté, vault inaccessible, vérificateur absent. Falsif `F6` du brief. | `P-3` N/A (dégradation) ; `H1-PERMANENT` maintenu **si** la discipline hors-noyau (`P-1`, `P-2`, `P-4`) reste **vérifiable**. C'est la falsif `F6`. |
| 4.4 | **Memory structurellement absente** | Architecture cible sans kernel et sans substitut équivalent. | `H1-PERMANENT` ne peut **pas** être démontré sur cette architecture. La cible « Backbone + Memory always-on » n'est **pas** satisfaite. P-3 N/A est valide pour la dégradation (état 4.3) mais **invalide** comme proxy d'architecture cible. |

**Conséquence de R-E3-1** :

- L'état 4.3 (dégradation) **est** acceptable pour démontrer la
  résilience du Backbone hors-Memory (falsif `F6`).
- L'état 4.4 (absence structurelle) **n'est pas** acceptable pour
  démontrer que la cible `H1-PERMANENT` est satisfaite. Un
  `P-3 = N/A` rendu permanent serait une **falsification** de
  `H1-PERMANENT`.

L'expérience E6+E8+E9 doit donc distinguer :
- les sessions en état 4.3 (vérifier que Backbone tient sans
  Memory — falsif `F6`) ;
- l'architecture cible présumée (vérifier qu'elle n'est **pas**
  en 4.4 — par exemple, par la présence effective du kernel dans
  la session test).

## 5. Protocole round-trip A→B

Le brief dit que ce test est « probablement le plus discriminant
pour savoir si nous avons réellement une mémoire gouvernée, plutôt
qu'un système de stockage/retrieval ». E5 en pose ici le
**protocole exécutable** ; E6 le câble en commandes ; E8 le
**mesure** ; E9 en tire les verdicts.

### 5.1 Pré-requis

- Un workspace jetable (par exemple `/tmp/vbbk-rt-<id>/`) avec
  `.vbb/canon/` et `.vbb/promotions/` créés en début de run.
- Le preset `vbbk` chargé en session DSH (kernel monté).
- Vault initial vide.
- Aucun fichier ADR/SESSION.md à mentionner : la mémoire de la
  session 2 doit provenir **uniquement** du vault.

### 5.2 Étapes D0 → D2 (session 1)

| Étape | Action | Vérification |
|---|---|---|
| D0.1 | Écrire `.vbb/canon/dec_A.md` (`id: dec_A`, `subject_key: api_design`, `value: rest_only`, `status: active`, `lifecycle: canonical`) | `vbbk_seam_check` (vault vide) : `PASS`, codes `[]`, `answers[]` vide. |
| D0.2 | `vbbk_rebuild_projections` | `vault.json` contient 1 projection (`source: dec_A`). |
| D0.3 | `vbbk_seam_check` | `PASS` ; 1 canon artifact, 1 vault entry. |
| D1.1 | Créer une entrée expérimentale : `vbbk_candidate_create`(`subject_key: api_design`, `value: rest_plus_websocket`, `provenance.captured_from: 'session_1/experiment_websocket.md'`, `conflicts_with: dec_A`) | `vault.json` contient 1 projection + 1 candidate. |
| D1.2 | `vbbk_seam_check` | **FAIL** avec codes `['CANDIDATE_CONTRADICTION_UNFLAGGED']` ; canon prioritaire. B **n'est pas canon** — le vérificateur le dit. |
| D1.3 | Modifier le canon : ajouter `superseded_by: dec_B` à `dec_A.md` et écrire `.vbb/canon/dec_B.md` (`id: dec_B`, `subject_key: api_design`, `value: rest_plus_websocket`, `status: active`, `lifecycle: canonical`, `supersedes: dec_A`) | Le canon est physiquement changé. |
| D1.4 | `vbbk_seam_check` (sans rebuild) | La projection de `dec_A` n'est **pas** re-synchronisée automatiquement. Résultat attendu : `FAIL` avec codes incluant `PROJECTION_STALE_SUPERSEDED` et/ou `REBUILD_DIVERGENCE`. |
| D1.5 | `vbbk_rebuild_projections` | La projection de `dec_A` disparaît du vault ; celle de `dec_B` apparaît. |
| D1.6 | `vbbk_seam_check` | `PASS` avec 2 canon artifacts, 1 vault projection, codes `[]`. |

### 5.3 Phase 2 — promotion par gate humain (D2)

| Étape | Action | Vérification |
|---|---|---|
| D2.1 | L'utilisateur autorise explicitement la promotion de B. Mint : `vbbk_authority_token_mint` (écoute du message utilisateur). | Réception d'un token. |
| D2.2 | Le LLM appelle `vbbk_promote` (`entry_id` = id du candidate B, `gate: {name: 'vbb-gate-check', verdict: 'PASS', run_id: '<id>'}` , `authorization: {token: <token>, by: 'human', message_id: <id>}`, `artifact_path: .vbb/promotions/dec_B_promoted.md`) | Écriture d'un artefact versionné avec frontmatter complet. |
| D2.3 | `vbbk_seam_check` | `PASS`. |

**Sans promotion** (parcours négatif) :
- Si l'étape D2.1 est sautée : `vbbk_promote` retourne
  `AUTHORIZATION_INVALID`. **B n'est pas canon**.
- Si l'utilisateur refuse `by: 'human'`, ou si le LLM essaie sans
  token : refus immédiat.

### 5.4 Étape D3 — session 2 neuve

| Étape | Action | Observation |
|---|---|---|
| D3.1 | Nouvelle session DSH, **aucun** historique conversationnel. | Pas de cache. Vault chargé depuis disque. |
| D3.2 | `vbbk_projection_list` (sans filtre) | Renvoie **2 entrées canoniques actives, dont dec_B** (le canon) et dec_db_choice, etc. dec_A n'apparaît plus. |
| D3.3 | L'agent répond à « quelle est la décision sur `api_design` ? » en interrogeant uniquement `vbbk_projection_list` ou son propre raisonnement. | Doit citer **B**, jamais A comme vérité courante. A peut être cité comme **historique** si on l'interroge explicitement sur la chaîne. |
| D3.4 | Injecter une entrée stale dans le vault (par exemple `vbbk_candidate_create` avec `value: rest_only` et `subject_key: api_design` sans `conflict: true`) | `vbbk_seam_check` doit retourner `CANDIDATE_CONTRADICTION_UNFLAGGED`. L'agent doit conclure que la stale dit le contraire du canon et ne pas la valider. |
| D3.5 | Vérifier qu'on peut **reconstruire A** comme historique : ré-écrire `dec_A.md` (avec `superseded_by: dec_B` supprimé) + `vbbk_rebuild_projections` | Projection de A réapparaît ; vérificateur reste en FAIL tant que `superseded_by` manque. C'est la garantie que A est **retrouvable**, jamais **active**. |

### 5.5 Critère discriminant

Le test est discriminant si **toutes** les conditions suivantes
sont vérifiées :

1. D1.2 produit un code stable et non ignorable.
2. D1.6 produit `PASS` sur le vault reconstruit.
3. D2.2 produit un artefact versionné signé par un humain.
4. D3.3 cite B comme vérité courante, jamais A.
5. D3.4 produit le bon code de stale detection.
6. D3.5 reconstruit A **historique** sans confusion avec B
   actif.

Si une seule échoue, ce n'est pas un système « Memory
gouvernée » — c'est du stockage/retrieval.

### 5.6 Cablage

E6 câble ce protocole en commandes et fixtures reproductibles
(`/tmp/vbbk-rt-<id>/`). Le test est reproductible si tous les
artifacts canon et vault sont versionnés sur disque ; toute
divergence doit être lue comme un échec du **kernel** ou de
l'**environnement**, jamais comme un défaut du test.

## 6. Conclusion A / B / C / D — quelle est la nature de `vbbk` ?

### 6.1 Lecture synthétique

`vbbk` est un kernel **JS DSH-périmètre** qui :

1. **Implémente intégralement** les invariants d'ADR 0055 (§3
   ci-dessus). Couverture technique totale du contrat canonique
   mémoire ↔ canon. Pas de 4ᵉ classe, pas de promotion
   silencieuse, pas de classification locale qui outrepasse
   l'autorité.
2. **Implémente 9 sur 12 responsabilités** au sens strict
   (capture / classification / working / promotion / storage /
   projection / reconstruction / provenance / stale detection).
3. **Implémente partiellement** les 3 restantes (retrieval —
   bornée à `subject_key` ; invalidation / supersession —
   détectée, jamais active ; synchronisation — détectée, jamais
   proactive).
4. **N'opère que** dans le périmètre `.vbb/canon/` ⇄
   `.vbb/promotions/` ↔ `$DSH_HOME/projects/<id>/vbbk/vault.json`.
   **Aucune lecture** des surfaces documentaires plus larges
   (`docs/CONTEXT.md`, `MEMORY_AND_HANDOFF.md`,
   `docs/document-model/`, ADR catalogue, vues E4).
5. **Conserve** des working entries sur disque (différence de
   design observée par rapport à l'esprit ADR 0055 §C2 «
   néant par définition » ; pas une violation au sens §C2 du
   vérificateur, qui regarde `source` et non la persistence).

### 6.2 Réponse à A / B / C / D

`vbbk` n'est **pas** Backbone Memory au sens complet :

- Il ne porte **pas** la continuité documentaire complète du
  canon (les 5 vues d'E4).
- Il ne porte **pas** la discipline permanente P-1..P-4 (la
  discipline est portée par le **persona + skill**, pas par le
  kernel — qui ne fait que Outiller la décision).
- Il ne porte **pas** la falsification `F2` (README historique
  pris pour canonique actif) ni `F3` (récence prise pour
  autorité). Sa fonction de vérif **ne sait pas lire** les
  vues documentaires d'E4.

`vbbk` **est** une composante structurelle de Backbone Memory.
Il porte les invariants d'autorité canon ↔ mémoire qui **sont**
le cœur de la couture ADR 0055 ; sans lui, la couture n'est pas
vérifiable mécaniquement.

### 6.3 Conclusion retenue

> **`vbbk` est la composante C (composante de Backbone Memory) —
> plus précisément : le kernel d'autorité canon ↔ mémoire
> exécutant les invariants ADR 0055.**
>
> Conclusion de réserve : `vbbk` tend vers **B** (kernel
> d'autorité de Backbone Memory) par sa couverture exhaustive des
> invariants ; il n'atteint pas **A** (Backbone Memory complet)
> parce que les vues documentaires E4 ne sont pas dans son
> périmètre.

C'est la qualification **empirique** la plus défensable sur la
base de ce qui est aujourd'hui dans `~/.dsh/.agent-presets/vbbk/`.

### 6.4 Ce que cette qualification **n'est pas**

- **Pas une promotion au rang de canon.** `vbbk` reste un
  **candidat testé**, jamais une autorité canonique. S'il
  devenait autoritaire par décret, ce serait une violation de
  `NO_PARALLEL_SEMANTIC_AUTHORITY` (ADR 0055 §C1). Vigilance #3
  explicitée.
- **Pas une disqualification de `vbbk`.** La qualification C/B
  n'est pas un rejet ; elle constate un périmètre. E6+E8 sont
  chargés de mesurer si ce périmètre **tient** ses promesses
  quand on l'opère.

### 6.5 Limites assumées à reporter en E9

| Limite | Justification |
|---|---|
| `vbbk` ne porte pas la discipline permanente. | Le kernel n'est pas Backbone entier ; la discipline est dans le persona/skill. |
| `vbbk` working entries persistent sur disque. | Design choice : pas une violation du vérificateur, mais une différence avec l'esprit ADR 0055 §C2. À documenter et à arbitrer en E9. |
| `vbbk` ne lit que `.vbb/canon/`. | Isolation intentionnelle ; le reste du canon est joint par voies externes (`docs/CONTEXT.md`). |
| `vbbk` ne déclenche pas la re-sync automatique. | Cohérent avec « LLM propose, kernel valide, humain autorise » : la re-sync est une décision. |
| Retrieval borné à `subject_key`. | Aucun retrieval sémantique embarqué ; la mémorisation sémantique est portée par le LLM, pas par le kernel. |
| I2 distinct-identity (campagne A2 du 2026-08-26) jamais exécutée. | Lacune héritée SYNTHESIS §What is still NOT covered n°1 ; hors-scope de E5. |
| T10.2 (oversized value cap, DoS surface). | Différé SYNTHESIS §Open ; hors-scope. |

## 7. Attribution corpus / `vbbk` / les deux (vigilance #4)

Vigilance #4 demande d'attribuer chaque défaut (ou succès)
correctement, sans réparer opportuniste. E5 ne constate que ce
que les lectures permettent ; E6 mesurera l'exécution.

### 7.1 Lacunes du corpus VS lacunes de `vbbk` (intersection avec E4 §6)

| Lacune E4 §6 | Source | Attribuable à | Action E5 |
|---|---|---|---|
| LAC-DOC-1 — aucune métadonnée ontologique peuplée hors fixtures POC | corpus | **corpus** | aucune — la lacune est dans la pratique documentaire, pas dans `vbbk`. E5 ne fabrique pas de frontmatter. |
| LAC-DOC-2 — aucun `load_policy` canonique observable | corpus | **corpus** | aucune — `vbbk` ne consomme pas ce champ. |
| LAC-DOC-3 — translation style A ↔ style B non déclarée | corpus | **corpus** | aucune — translation est un travail documentaire. |
| LAC-DOC-4 — pas de chaîne A→B→C reconstructible | corpus | **corpus** | aucune — le kernel saurait supporter la chaîne si le canon la portait. |
| LAC-DOC-5 — style A/B d'ADR non résolu | corpus | **corpus** | aucune — hors-scope du run. |
| LAC-DOC-6 — `tools/vbb-architecture.py` ne consomme pas le frontmatter ontologique | corpus | **corpus** | aucune — tool canonique hors-portée du kernel. |
| Working entries persistent sur disque (§6.5) | `vbbk` | **`vbbk` design choice** | aucun repair. À noter dans E9. |
| Retrieval borné à `subject_key` (§6.5) | `vbbk` | **`vbbk` design choice (par isolation)** | aucun repair. Acceptable en l'état. |
| Pas d'invalidation active des projections stale | `vbbk` | **`vbbk` design choice** | aucun repair. Pourrait être un futur tool `vbbk_invalidate_stale`, mais c'est un ajout hors-périmètre. |
| Pas de re-synchronisation automatique | `vbbk` | **`vbbk` design choice** | aucun repair. Acceptable. |
| `vbbk` ne lit pas `docs/CONTEXT.md`, `MEMORY_AND_HANDOFF.md`, etc. | `vbbk` (par isolation) + corpus (par absence d'interface canon ↔ kernel) | **les deux** | aucune réparation opportuniste. C'est un futur **connecteur** canon ↔ `vbbk`, hors-périmètre de ce run. |
| I2 distinct-identity non exécutée | `vbbk` audit | **`vbbk` audit, pas kernel** | hors-scope de ce run. |
| T10.2 oversized value | `vbbk` | **`vbbk`** | déféré par maintainer ; hors-scope. |

### 7.2 Attribution transversale

- **Lacunes du corpus** sont toutes situées dans le **mode dégradé**
  (E3 §2, mode dégradé acceptable) ; elles ne violent pas le
  contrat E3.
- **Lacunes du kernel `vbbk`** sont toutes situées **dans son
  périmètre** ; elles n'élargissent pas le périmètre du contrat
  E3 ; elles sont notées comme choix de design assumés.
- **Lacunes communes** (canon ↔ kernel) sont notées comme **un
  futur connecteur** ; pas de réparation dans ce run.

### 7.3 Test de cohérence

| Test | Énoncé | Pass = OK |
|---|---|---|
| T-ATTR-1 | Aucun ajout de champs/classes/autorités n'est proposé pour fermer LAC-DOC-*. | ✅ aucune proposition. |
| T-ATTR-2 | Aucune modification de `~/.dsh/.agent-presets/vbbk/` n'est entreprise. | ✅ lecture seule. |
| T-ATTR-3 | Aucun fichier `docs/` n'est créé ou touché pour « produire » une vue. | ✅ aucune création. |
| T-ATTR-4 | Aucune clause « faire passer le test en étendant le corpus » n'apparaît. | ✅ toutes les lacunes sont des constats, pas des cibles. |

## 8. Handoff vers `06_EXPERIMENT_PROTOCOL`

E6 doit :

1. **Câbler** le protocole §5 en commandes exécutables. En
   particulier : le `/tmp/vbbk-rt-<id>/` workspace, les fixtures
   `.vbb/canon/`, le script de session 1, le script de session 2.
2. **Couvrir** la falsif `F6` en testant l'état 4.3 (kernel
   temporairement non monté). L'état 4.4 (Memory structurellement
   absente) doit **explicitement être qualifié faux** sur
   l'architecture cible — c'est l'application de R-E3-1 §4.
3. **Boucher** l'exécution de la résolution à 9 conditions
   posées en E2 §7 (critère de succès du brief). Chaque condition
   est binaire pour E8.
4. **Reprendre** LAC-DOC-* sans en faire une dépendance
   bloquante : si LAC-DOC-1 empêche le câblage, c'est un blocage
   à signaler, pas une incitation à inventer.
5. **Limiter** le scope à DSH-only (rappel §14 brief). Aucune
   commande ne sort de DSH.

### 8.1 Points de vigilance pour E6

- Le test D3.4 (stale detection sur Memory) est le plus subtil :
  il faut injecter une candidate contradictoire **avec** le
  bon `subject_key` mais **sans** `conflict: true`, et observer
  que le vérificateur produit `CANDIDATE_CONTRADICTION_UNFLAGGED`.
- Le test D3.5 (reconstruction historique) exige que
  `vbbk_rebuild_projections` soit appelé **après** que le canon
  ré-introduise A comme actif ; ce n'est pas un effacement, c'est
  une reconstruction sur signal explicite.
- L'état 4.3 (F6) doit être testé en désactivant **proprement**
  le kernel (par exemple `VBBK_EXTRACTION_DISABLED=1` est
  insuffisant — il faut tester *kernel absent*). E6 doit trouver
  une bascule qui simule l'absence sans toucher au code.

### 8.2 Seuil A

E6 fonctionne en A2 pour toute décision touchant aux codes du
vérifier, à la falsification, et à l'attribution corpus /
`vbbk`. A1 pour le câblage du protocole. A0 pour l'inventaire
des workspaces jetables. La répartition reste cohérente avec
E3 §0 et E4 §10.

## 9. Bornes

- ❌ Aucune modification de `~/.dsh/.agent-presets/vbbk/`.
- ❌ Aucun ajout de classe autoritaire (vigilance #1 + R-E3-1).
- ❌ Aucune promotion de `vbbk` au rang de canon (vigilance #3).
- ❌ Aucune fermeture opportuniste des lacunes (vigilance #4).
- ❌ Aucune exécution dans ce livrable : E6 câble, E8 exécute.
- ❌ Aucune sortie de DSH-only.

## 10. Verdict E5

| Champ | Valeur |
|---|---|
| Statut | `READY` |
| `next_phase` | `06_EXPERIMENT_PROTOCOL` |
| Conclusion A/B/C/D | **`C` — composante de Backbone Memory, tendant vers `B` (kernel d'autorité)**. Cf. §6. |
| 12 responsabilités attribuées | 9 IMPLEMENTED ; 3 PARTIAL ; 0 NOT_IMPLEMENTED ; 0 OUT_OF_SCOPE_BY_DESIGN |
| Conformité ADR 0055 | totale sur §C1-§C7 et A1-A5 au niveau du vérificateur |
| R-E3-1 reformulée | 4 états (4.1 nominal, 4.2 stale, 4.3 indisponibilité temp., 4.4 absence struct.) — §4 |
| R-E4-1 honorée | aucune autorité inventée — vérifié T-ATTR-1..4 |
| Round-trip A→B | protocole posé (§5) ; E6 câble |
| Lacunes non-réparées | 12 identifiées, attribuées, **toutes laissées ouvertes** |
| Drift préempté | E6 §8.1 signale les 3 points de vigilance de E6 |
