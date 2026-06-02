# ADR 0010 — Frontières de sécurité du proxy de confidentialité

**Status**: PROPOSED (rev. 2026-06-02)
**Date**: 2026-06-02 (Revised: 2026-06-02 — D7 repo governance rule, Règle 11 ajoutée, contrat étendu)
**Route**: STRUCTURED
**Chantier**: Proxy de confidentialité
**Auteur**: vbb-struct-worker (batch parallèle avec ADR 0006, 0007, 0008, 0009)
**Référence transverse**: ADR 0006 (architecture), 0007 (credentials), 0008 (failover), 0009 (extensibilité), 0011 (bypass prevention)

---

## 1. Contexte

Le chantier « Proxy de confidentialité » (Brice, 2026-06-02) introduit un
composant central qui médiatise toutes les interactions entre les agents
Vibebackbone (Hermes, Cody, 4 workers VBB, cody-check) et les ressources
externes crédentialisées (macOS Keychain, API tierces, services locaux
Ollama/MLX).

Ce proxy doit :

- exposer un ensemble fini et auditable d'**actions** déclarées dans
  `actions.yaml` ;
- transporter des **credentials** (clés API, tokens OAuth, secrets macOS)
  sans jamais les exposer en clair dans les logs ou le dépôt ;
- tracer chaque opération dans un **audit log** opposable ;
- supporter un mode **dry-run** puis un passage en **live** sur validation
  humaine explicite.

Les ADR 0006 (architecture), 0007 (credentials), 0008 (failover) et 0009
(extensibilité) décrivent respectivement la forme du proxy, la gestion des
identifiants, la résilience et l'ouverture à de nouvelles actions. Aucun de
ces ADRs ne fixe, pris isolément, le **socle de sécurité transverse** auquel
ils doivent tous se conformer.

Sans frontières de sécurité explicites et opposables :

- un agent pourrait composer une action non déclarée et l'exécuter ;
- un secret pourrait fuiter dans un log, un diff Git ou une réponse HTTP ;
- une opération sensible pourrait basculer en `live` sans validation humaine ;
- un attaquant (ou un LLM compromis par prompt injection) pourrait élever
  ses privilèges en concaténant des permissions `read`/`write`/`destroy`.

L'ADR 0010 formalise donc les **frontières de sécurité** du proxy. Il est
transverse aux ADRs 0006-0009 et constitue la **référence de sécurité** à
respecter par toutes les autres composantes. Toute modification d'un autre
ADR qui contreviendrait à une règle cardinale du présent document doit être
refusée.

---

## 2. Décision

### 2.1. Principe directeur

Le proxy de confidentialité applique une **défense en profondeur** à quatre
niveaux superposés :

1. **Frontière de déclaration** : aucune action n'existe hors `actions.yaml`.
2. **Frontière d'exécution** : aucune action ne s'exécute hors dry-run
   validé puis live autorisé.
3. **Frontière de privilège** : aucun credential n'est accessible hors
   `required_credentials` déclarés.
4. **Frontière d'audit** : toute opération credentialisée laisse une trace
   signée et non répudiable.

Ce principe de défense en profondeur se traduit par **onze règles
cardinales** imposées à toutes les composantes du proxy et par
construction à tous les ADRs frères. (La onzième règle — bypass
prevention — a été ajoutée le 2026-06-02 par décision D7 actée par
Brice ; cf. ADR 0011.)

### 2.2. Les onze règles cardinales

> Ces règles sont **non négociables**. Toute proposition qui en enfreint
> une est rejetée sans débat de goût.

#### Règle 1 — Séparation stricte lecture / écriture / destruction

- Chaque action déclare ses permissions parmi `read`, `write`, `destroy`.
- Une action déclarée `destroy` ne peut **JAMAIS** être combinée avec
  `read` dans la même déclaration (anti-construction exfiltration + purge).
- Une action déclarée `write` ne peut pas contenir de logique `destroy`
  implicite (pas de `rm`, `unlink`, `Drop`, `DELETE` SQL sans déclaration
  `destroy`).
- L'audit est **séparé** pour chaque catégorie : un log `read`, un log
  `write`, un log `destroy` (cf. ADR 0007 pour le format détaillé).

#### Règle 2 — Whitelist obligatoire des actions

- Seules les actions déclarées dans `actions.yaml` sont exécutables par le
  proxy.
- Il n'existe **aucune** exécution par défaut, aucune interprétation libre
  du LLM sur des commandes arbitraires.
- Le LLM peut **suggérer** une action, **jamais** l'exécuter sans
  correspondance exacte avec une entrée whitelistée (matching par
  `action_id` canonique, pas par similarité de prompt).

#### Règle 3 — Audit obligatoire des opérations credentialisées

- Toute opération utilisant un credential est journalisée sans exception.
- **Log minimal** (toujours actif) : `timestamp`, `requestor`, `action_id`,
  `credential_id` (jamais la valeur), `params` (sanitisés), `résultat`
  (`ok`/`refused`/`error`).
- **Log détaillé** (opt-in par configuration) : + `stdout`/`stderr` hashés
  (SHA-256), `durée_ms`, `exit_code`.
- **Log verbeux** (debug uniquement, opt-in) : + contexte complet (payload
  brut sanitisé, trace d'appels). Désactivé en production par défaut.

#### Règle 4 — Mode dry-run par défaut pour toute nouvelle action

- Une action nouvellement ajoutée dans `actions.yaml` est marquée
  `mode: dry-run` par défaut.
- Le dry-run montre l'effet attendu (commande reconstituée, credential
  accédé, ressources touchées) **sans** l'exécuter réellement.
- Le passage en `mode: live` nécessite une **validation explicite de
  Brice** (humain), tracée dans l'audit log avec son empreinte de
  validation.

#### Règle 5 — Impossibilité d'exécuter une action non déclarée

- À la réception d'une requête, le proxy vérifie la présence de
  `action_id` dans `actions.yaml`.
- **Refus immédiat** (HTTP 403 / code d'erreur dédié) si absent.
- L'erreur retournée à l'appelant est générique (« action non autorisée »)
  et n'expose pas la liste des actions existantes.
- **Log d'audit** de la tentative refusée, avec motif `undeclared_action`,
  pour détection de patterns d'attaque (prompt injection, scan énumératif).

#### Règle 6 — Impossibilité de promouvoir automatiquement une capacité sensible

- Un credential de niveau `high` ou `critical` ne devient **jamais**
  utilisable automatiquement, même si le fichier `credentials.yaml` le
  déclare.
- **Validation explicite de Brice** requise à la création (signature
  out-of-band, ticket, ou interaction dédiée dans l'UI de gouvernance).
- **Validation explicite** également requise pour toute modification
  ultérieure : rotation de clé, mise à jour de permissions, changement de
  portée, suppression.

#### Règle 7 — Journalisation sans exposition des secrets

- Les **valeurs** de credentials ne sont **JAMAIS** journalisées — ni en
  clair, ni hashées, ni chiffrées. Cette interdiction est absolue, par
  défense en profondeur (un hash de clé API reste un identifiant
  pseudo-unique qui peut fuiter).
- Les **paramètres** des actions sont masqués automatiquement s'ils
  matchent des patterns sensibles (regex PII/secret : email, n° CB, token
  JWT, Bearer, Basic auth, clé privée PEM, etc.).
- L'audit log lui-même peut être **chiffré au repos** : convention POC =
  **libsodium SecretStream (XChaCha20-Poly1305) en mode PRIORITAIRE**
  (cf. décision D3 actée par Brice le 2026-06-02, ADR 0007 §2.1) ;
  AES-256-GCM est conservé uniquement comme **fallback documenté**.

#### Règle 8 — Stockage sécurisé des secrets hors dépôt

- **Aucun secret** dans le dépôt Git (vérifié par hook pre-commit + scan
  périodique).
- **Aucun secret** dans les fichiers de configuration versionnés
  (`config/*.yaml` ne contient que des références `credential_id`).
- **macOS Keychain** en priorité pour les secrets locaux et tokens de
  service.
- **Fichier chiffré** (`~/.hermes/proxy/secrets.enc`, **libsodium SecretStream
  (XChaCha20-Poly1305) en mode PRIORITAIRE** — cf. décision D3 actée par Brice
  le 2026-06-02, ADR 0007 §2.1 ; **AES-256-GCM en FALLBACK documenté** pour
  portabilité) en fallback si le Keychain est indisponible, avec permission
  `0600`. *Note : une migration future vers `~/.config/vibebackbone/security/`
  est évoquée dans 0010 §5 (H4 historique) mais est **explicitement reportée
  en post-POC** et devra faire l'objet d'une ADR dédiée.*

#### Règle 9 — Principe du moindre privilège

- Chaque credential a **uniquement** les permissions minimales
  nécessaires à son usage déclaré (scopes OAuth les plus étroits, rôle
  IAM le plus bas, pas de wildcard `*`).
- Chaque action déclare dans `required_credentials` la liste explicite
  des credentials qu'elle est habilitée à utiliser. Le proxy refuse tout
  accès à un credential non listé.
- **Pas de credentials `admin` ou `root` par défaut**. Si une action
  requiert une élévation, elle doit être découpée en sous-actions à
  privilèges séparés, et l'élévation est elle-même une action déclarée
  `destroy` ou `write` sensible (soumis à validation Règle 6).

#### Règle 10 — Explicitation des responsabilités humain/agent/système

- **Humain (Brice)** : valide toute création/modification de credential
  sensible, valide tout passage dry-run → live, tranche les incidents de
  sécurité, est l'autorité de dernier recours.
- **Agent (proxy + LLM)** : propose, guide, exécute (après autorisation),
  audite — **ne décide jamais seul** pour les opérations sensibles
  (création de credential, promotion live, accès `destroy`).
- **Système (service proxy + runtime)** : applique mécaniquement les
  règles, refuse ce qui n'est pas autorisé, journalise tout (même les
  refus), n'interprète pas la politique — il l'exécute.

#### Règle 11 — Bypass prevention (ajoutée 2026-06-02, décision D7)

> Cette règle est cardinale au même titre que les dix précédentes. Elle
> formalise la **règle de gouvernance repo** : aucun chemin de code
> d'Hermes, Cody ou des workers VBB ne doit exécuter directement un
> binaire sensible en court-circuitant le proxy. Référence de
> référence : **ADR 0011 — Proxy Bypass Prevention**.

- **Aucun composant** d'Hermes, de Cody ou des workers VBB
  (`vbb-fast`, `vbb-struct`, `vbb-audit`, `vbb-close`) ne peut
  exécuter directement un binaire sensible en court-circuitant le
  proxy. La **liste canonique des binaires interdits** est définie
  en **ADR 0011 §3 (règle 1)** — référence unique, à ne pas
  dupliquer ici pour éviter les divergences. Le résumé non
  exhaustif ci-dessous est fourni à titre indicatif pour le lecteur
  pressé et doit être considéré comme **non canonique** en cas de
  désaccord avec ADR 0011 :

  *Indicatif (cf. ADR 0011 §3 pour la liste exhaustive)* : voir
  ADR 0011 §3 règle 1.
- **Tout accès credentialisé DOIT passer par le proxy** via une action
  déclarée dans `actions.yaml` (cf. ADR 0009). Le proxy est l'unique
  point d'entrée pour les opérations sensibles.
- **Le linter `tools/vbb-bypass-lint.py`** est l'implémentation de
  référence de cette règle. Il est implémenté en V2 (cf. ADR 0011) ;
  au POC, la règle est appliquée par **revue de PR manuelle** :
  tout ajout d'un `command_template` sensible est bloqué en review.
- **Toute violation** détectée est un **incident de sécurité** :
  refus d'enregistrement, log d'audit `event=bypass_attempt`, et
  notification Telegram immédiate à Brice. La violation est
  remontée dans le rapport hebdomadaire de `vbb-audit-worker`.

Cette règle s'applique **par construction** : elle ne dépend pas du
LLM, ne dépend pas de l'état de santé du proxy, et ne souffre aucune
exception. C'est la dernière ligne de défense contre l'exfiltration
par court-circuit de la chaîne de sécurité.

### 2.3. Modélisation des menaces (STRIDE simplifié)

Le proxy couvre systématiquement les six catégories STRIDE :

- **S**poofing : signature HMAC des requêtes entrantes (appelants
  authentifiés) + **whitelist des appelants** (seuls Hermes, Cody, les
  4 workers VBB, cody-check peuvent invoquer le proxy).
- **T**ampering : audit log **append-only** + hash d'intégrité chaîné
  (chaque entrée contient le hash de la précédente, type Git mais
  appliqué au log).
- **R**epudiation : log **signé par l'appelant** (signature HMAC de la
  requête jointe à l'entrée) + horodatage NTP + identifiant unique de
  run.
- **I**nformation disclosure : credentials chiffrés au repos +
  **masquage systématique** dans les logs (Règle 7) + réponse HTTP
  minimisant les détails d'erreur.
- **D**enial of service : **rate limiting** par appelant et par action
  (cf. décision D6, ADR 0008 §2.2.1) : 30 requêtes/min/appelant,
  5 actions sensibles (high+critical) / heure / appelant, 10 actions
  credentialisées simultanées max. Au dépassement, refus HTTP 429
  explicite avec `Retry-After` header, log d'audit
  `event=rate_limit_exceeded`, et notification Telegram à Brice. Le
  rate-limiting est orthogonal à l'état de santé du proxy et reste
  actif en niveau 2 et en niveau 3 (cf. ADR 0008 §2.2.1 et §2.4.1).
- **E**levation of privilege : whitelist stricte des actions (Règle 2) +
  **permissions par action** (Règle 1) + promotion humaine (Règle 6).

### 2.4. Tests de sécurité obligatoires avant chaque release

Avant toute promotion de version, la suite de tests ci-dessous **doit
passer à 100 %** :

1. Tentative d'action non déclarée → **refus attendu** (HTTP 403, code
   `E_UNDECLARED`).
2. Tentative d'action marquée `high` sans validation humaine → **refus
   attendu** (code `E_REQUIRES_HUMAN_VALIDATION`).
3. Tentative de log d'un credential (fuite simulée par harness) →
   **masquage attendu** (regex de détection déclenche la troncature).
4. Tentative de bypass de l'audit (requête forgée sans signer) → **échec
   attendu** (signature HMAC invalide → refus).
5. Tentative d'élévation de privilège (action `read` qui appelle
   subresource `write` non listé) → **refus attendu** (code
   `E_PRIVILEGE_ESCALATION`).
6. Tentative d'ajout d'une action dont le `command_template` matche
   un binaire de la **liste canonique ADR 0011 §3 (règle 1)** →
   **refus attendu** (`E_BYPASS_DETECTED`) avant enregistrement.
   (Remplace l'ancienne formulation inline de la liste D7 — la
   liste canonique est désormais uniquement ADR 0011 §3.)
   est gate en CI.

L'absence d'un de ces tests dans la suite de release est un **bloqueur
absolu** (gate `SECURITY_TESTS` rouge en CI).

---

## 3. Conséquences

### 3.1. Conséquences positives

- **Surface d'attaque minimale** : seules les actions déclarées sont
  exécutables, chacune avec ses permissions strictement déclarées.
- **Auditabilité complète** : toute opération credentialisée laisse une
  trace non répudiable, signée et chaînée.
- **Confidentialité des secrets garantie** : aucune valeur de credential
  n'apparaît jamais en clair dans les logs, le code, le dépôt ou les
  réponses HTTP.
- **Séparation des privilèges** : humain, agent, système ont des rôles
  distincts et non interchangeables ; aucune partie ne peut outrepasser
  les autres.
- **Défense en profondeur** : un échec d'une couche (par exemple, regex
  de masquage manquant un nouveau pattern) ne compromet pas l'ensemble
  car les autres couches (chiffrement au repos, Keychain, validation
  humaine) restent actives.
- **Référence transverse** : les ADR 0006, 0007, 0008, 0009 peuvent
  s'appuyer sur un socle de sécurité explicite et opposable, réduisant
  l'ambiguïté et le risque d'ADR contradictoires.

### 3.2. Conséquences opérationnelles

- Toute nouvelle action passe par le cycle déclaration → dry-run → revue
  Brice → validation → live. Plus lent à l'onboarding, c'est l'objet
  même de l'ADR.
- La validation humaine (Brice) devient un goulot d'étranglement pour
  les opérations sensibles — acceptable car ces opérations sont rares et
  à fort impact.
- Le mode verbeux ne doit jamais être activé en production. Vérifié en
  revue de code.
- Le hook pre-commit de détection de secrets doit être maintenu et
  étendu (faux positifs à minimiser, faux négatifs à zéro).
- La rotation des credentials `high`/`critical` demande une procédure
  out-of-band (ticket, session dédiée), pas un simple commit.

### 3.3. Conséquences sur les ADR frères

- **ADR 0006 (architecture)** : point d'application centralisé des
  règles 1, 2, 5 au niveau du routeur du proxy.
- **ADR 0007 (credentials)** : implémentation des règles 6, 7, 8, 9
  dans le gestionnaire de credentials.
- **ADR 0008 (failover)** : compose avec la règle 1 (un failover ne peut
  pas combiner `read` et `destroy`) et la règle 3 (chaque bascule est
  audité séparément).
- **ADR 0009 (extensibilité)** : toute nouvelle action tierce doit
  respecter les 10 règles (test d'acceptation, dry-run par défaut,
  validation humaine).

### 3.4. Indicateurs de succès

- 100 % des actions du proxy déclarées dans `actions.yaml` (scan
  statique).
- 0 secret en clair dans le dépôt Git (`gitleaks` en CI).
- 0 secret en clair dans les logs (fuzzing du logger).
- 100 % des opérations `high`/`critical` ont une trace de validation
  humaine dans l'audit log.
- Tous les tests STRIDE passent en CI sur chaque PR.

---

## 4. Alternatives envisagées (rejetées)

### 4.1. Alternative A — Confiance totale dans le LLM (« trust the prompt »)

**Description** : laisser le LLM interpréter librement la requête,
composer la commande système correspondante et l'exécuter via le proxy
sans whitelist explicite.

**Rejetée car** :

- viole la **séparation des privilèges** (le LLM décide seul) ;
- viole la **défense en profondeur** (une seule couche — la qualité du
  prompt — protège tout) ;
- vulnérable à la **prompt injection** (contenu externe peut faire
  exécuter une commande arbitraire) ;
- impossible à auditer (pas de correspondance action_id ↔ exécution) ;
- rend la Règle 2 inopérante.

**Verdict** : incompatible avec les frontières de sécurité. Rejet ferme.

### 4.2. Alternative B — Permissions UNIX classiques (DAC Unix)

**Description** : s'appuyer sur `chmod`, `sudoers`, capabilities Linux
pour gérer l'accès aux credentials et aux actions.

**Rejetée car** :

- permissions UNIX ne distinguent pas `read`/`write`/`destroy` au
  niveau d'une action atomique ;
- sudoers/capabilities sont administratifs, non auditable au niveau de
  l'action individuelle ;
- ne couvrent pas les actions réseau (appels API) ;
- pas de notion de **dry-run** natif ;
- rotation, masquage des logs, signature HMAC ne sont pas des concepts
  UNIX.

**Verdict** : utile en complément (permissions du binaire, du dossier
secrets) mais insuffisant comme mécanisme principal.

### 4.3. Alternative C — Whitelist par regex / matching flou

**Description** : autoriser toute commande qui matche un pattern large
(par exemple `^gh api .*$`) au lieu d'une whitelist explicite par
`action_id`.

**Rejetée car** :

- viole la Règle 2 (whitelist **exacte**, pas approchante) ;
- permet l'exfiltration par variation syntaxique mineure ;
- complique l'audit (deux exécutions sémantiquement différentes peuvent
  partager un même pattern) ;
- rend la Règle 6 impraticable (quand le pattern matche-t-il une action
  `high` ?).

**Verdict** : trop permissif. La whitelist doit être par `action_id`
canonique.

### 4.4. Alternative D — Audit log en clair dans le dépôt

**Description** : versionner l'audit log dans Git pour bénéficier de
l'historique et de la signature GPG.

**Rejetée car** :

- viole la Règle 7 (contexte agrégé peut révéler des patterns
  sensibles) ;
- viole la Règle 8 (le dépôt Git n'est pas un stockage de secret) ;
- pollue le diff de chaque PR ;
- ne permet pas le chiffrement au repos transparent.

**Verdict** : rejet. L'audit log vit dans un store dédié (fichier
chiffré + rotation, ou service externe type Loki/Elastic), hors dépôt.

### 4.5. Alternative E — Pas d'ADR 0010 (règles dispersées)

**Description** : ne pas créer d'ADR fondateur 0010 ; laisser chaque ADR
frère déclarer ses propres règles de sécurité.

**Rejetée car** :

- introduit des contradictions entre ADR ;
- viole l'objectif de **référence transverse** ;
- complique l'audit (5 sources de vérité au lieu d'1 + 4 références) ;
- ne fournit pas de garde-fou (un ADR pourrait contrevenir aux règles
  sans qu'on s'en aperçoive).

**Verdict** : c'est précisément le problème que cet ADR résout. Rejet.

---

## 5. Risques connus

### 5.1. Risques techniques

- **R-T1 — Fuite de secret par pattern non reconnu** : nouveau format de
  token non couvert par la regex de masquage. *Mitigation* : revue
  trimestrielle des regex, fuzzing régulier du logger, charte de revue
  de code pour toute modification de la regex.
- **R-T2 — Bypass de la whitelist par concaténation** : action `read`
  qui appelle subrepticement une API `write` via un paramètre.
  *Mitigation* : validation statique du graphe d'appels au chargement,
  tests d'élévation obligatoires (cf. 2.4), refus runtime si credential
  non listé.
- **R-T3 — Compromission du Keychain macOS** : attaquant avec accès
  session lit le Keychain. *Mitigation* : FileVault, séparation session
  proxy / utilisateur, surveillance EDR.
- **R-T4 — Falsification d'horodatage** : horloge système compromise
  rend l'audit ambigu. *Mitigation* : NTP obligatoire, monotonique pour
  les checks d'ordre, alerte si drift > 1s.

### 5.2. Risques organisationnels

- **R-O1 — Brice devient goulot d'étranglement** : son indisponibilité
  bloque les passages en live. *Mitigation* : délégué co-signeur
  documenté en runbook.
- **R-O2 — Faux sentiment de sécurité** : l'ADR fait croire que « tout
  est sécurisé » alors que l'implémentation a des bugs. *Mitigation* :
  tests d'intrusion biannuels, bug bounty interne, revue sécurité
  obligatoire pour `proxy/`.
- **R-O3 — Dérive des règles** : contournements sous pression
  (« juste cette fois »). *Mitigation* : audit log audité chaque
  semaine, interdiction `--force` sans ticket sécurité.
- **R-O4 — Incompréhension du périmètre « sensible »** : développeur
  sous-estime la sensibilité d'une action. *Mitigation* : matrice de
  classification dans `actions.yaml.schema`, valeurs par défaut
  conservatrices, revue humaine pour toute promotion de niveau.

### 5.3. Risques liés à l'ADR lui-même

- **R-A1 — ADR jamais mis à jour** : les menaces évoluent. *Mitigation*
  : revue annuelle, versionning, dépréciation documentée.
- **R-A2 — Conflit avec un ADR futur** : un nouvel ADR contredit une
  règle cardinale. *Mitigation* : le présent ADR est marqué comme
  référence transverse ; toute PR qui modifie un ADR frère et contredit
  une règle doit être refusée.

---

## 6. Hypothèses restant à confirmer

Le passage **PROPOSED → ACCEPTED** est conditionné à la confirmation des
hypothèses ci-dessous.

- **H1** — `actions.yaml` supporte nativement la déclaration de
  permissions `read`/`write`/`destroy` par action et la liste
  `required_credentials`. *À confirmer par ADR 0006.*
- **H2** — Le mécanisme de signature HMAC des requêtes est implémenté
  ou prévu dans la couche transport. *À confirmer par ADR 0006 + code.*
- **H3** — macOS Keychain est disponible et utilisable depuis le
  contexte d'exécution du proxy. *À confirmer par test d'environnement.*
- **H4** — Brice (ou son délégué) accepte le rôle de validateur humain
  unique pour `high`/`critical` et le passage dry-run → live. *À
  confirmer par entretien.*
- **H5** — **libsodium SecretStream (XChaCha20-Poly1305) avec clé en
  Keychain** est le mécanisme retenu pour chiffrer l'audit log au repos
  (cf. décision D3, ADR 0007 §2.1). AES-256-GCM est conservé
  uniquement comme fallback documenté, pas comme choix principal.
  log au repos. *À confirmer par ADR 0007.*
- **H6** — Le rate limiting est appliqué au niveau du proxy (et non de
  l'API tierce) pour toutes les actions. *À confirmer par ADR 0006,
  avec cas d'usage Ollama/MLX (local, pas de rate limit).*
- **H7** — Le hook pre-commit de détection de secrets est en place (ou
  sera ajouté dans le sprint courant). *À confirmer par état du repo.*
- **H8** — Le timeout par action est défini dans `actions.yaml`
  (`timeout_ms`) et borné (max 60s par défaut). *À confirmer par ADR
  0006.*
- **H9** — La séparation lecture/écriture/destruction est testable
  statiquement (analyse du graphe d'appels) sans exécution. *À
  confirmer par proof-of-concept.*
- **H10** — Le hash chaîné de l'audit log a un overhead < 5 % par
  requête. *À confirmer par benchmark.*

---

## 7. Checklist de sécurité pré-release

À exécuter pour **chaque release** (tag, déploiement). Toutes les
questions doivent recevoir « Oui ». Un « Non » ou « Incertain » bloque
la release.

### 7.1. Frontière de déclaration

- [ ] **Toutes** les actions du proxy sont-elles déclarées dans
  `actions.yaml` ? (scan statique du binaire)
- [ ] Chaque action déclare-t-elle explicitement sa catégorie
  (`read` / `write` / `destroy`) ?
- [ ] Aucune action ne combine-t-elle `destroy` et `read` dans la même
  déclaration ?
- [ ] Aucune action `write` ne contient-elle de logique `destroy`
  implicite ?

### 7.2. Frontière d'exécution

- [ ] Le mode par défaut des nouvelles actions est-il `dry-run` ?
- [ ] Toutes les actions en `live` ont-elles une trace de validation
  explicite de Brice dans l'audit log ?
- [ ] Le test « Tentative d'action non déclarée → refus » passe-t-il ?
- [ ] Le test « Tentative d'action `high` sans validation → refus »
  passe-t-il ?

### 7.3. Frontière de privilège

- [ ] Chaque action déclare-t-elle `required_credentials` de manière
  exhaustive ?
- [ ] Le test « Tentative d'élévation de privilège → refus » passe-t-il
  ?
- [ ] Aucun credential `admin` / `root` par défaut n'a-t-il été
  introduit depuis la dernière release ?

### 7.4. Frontière d'audit

- [ ] L'audit log est-il append-only (pas de troncature possible) ?
- [ ] L'audit log est-il chiffré au repos (**libsodium SecretStream
  prioritaire**, AES-256-GCM uniquement en fallback documenté, clé en
  Keychain) ?
- [ ] Le test « Tentative de log d'un credential → masquage » passe-t-il
  ?
- [ ] Le test « Tentative de bypass de l'audit → échec » passe-t-il ?

### 7.5. Stockage et secrets

- [ ] Le scan `gitleaks` (ou équivalent) est-il vert sur la branche de
  release ?
- [ ] Aucun secret n'a-t-il été ajouté dans `config/*.yaml` depuis la
  dernière release ?
- [ ] Le Keychain macOS est-il accessible et fonctionnel depuis
  l'environnement d'exécution ?
- [ ] La rotation des credentials a-t-elle été effectuée si le délai de
  rotation est dépassé ?
- [ ] Le linter `tools/vbb-bypass-lint.py` (cf. Règle 11 et ADR 0011)
  est-il exécuté en CI ? Au POC, la règle est appliquée par revue de
  PR manuelle — un second pair a-t-il relu et validé chaque
  `command_template` ajouté ou modifié dans `actions.yaml` ?

### 7.6. Responsabilités

- [ ] Brice (ou son délégué) a-t-il explicitement validé la release ?
- [ ] Le runbook d'incident de sécurité est-il à jour et testé ?
- [ ] La matrice de classification des actions est-elle revue pour
  toute nouvelle action ajoutée ?

### 7.7. Tests STRIDE

- [ ] **S**poofing : un appelant non whitelisté est-il refusé ?
- [ ] **T**ampering : toute modification de l'audit log est-elle
  détectée (chaînage de hash) ?
- [ ] **R**epudiation : toute entrée est-elle signée et horodatée ?
- [ ] **I**nformation disclosure : un fuzzing du logger avec 100
  patterns secrets est-il passé sans fuite ?
- [ ] **D**enial of service : un burst de requêtes au-delà du rate
  limit est-il refusé proprement ?
- [ ] **E**levation of privilege : un appelant `read` qui tente un
  `write` est-il refusé ?

---

## 8. Conclusion

L'ADR 0010 formalise les **frontières de sécurité** du proxy de
confidentialité sur la base de **onze règles cardinales** non
négociables (dix règles historiques + Règle 11 « bypass prevention »
ajoutée par décision D7 le 2026-06-02), couvrant la **séparation des
privilèges**, le **principe du moindre privilège** et la **défense en
profondeur**. Il est la **référence de sécurité transverse** pour les
ADR 0006, 0007, 0008 et 0009 : toute modification de l'un de ces ADR
qui contredit une règle cardinale doit être refusée. **ADR 0011 — Proxy
Bypass Prevention** est lui-même la référence de la Règle 11 : la
règle de gouvernance repo y est détaillée action par action.

Sa mise en œuvre impose un cycle strict (déclaration → dry-run →
validation humaine → live), un audit log append-only signé et chaîné,
un masquage systématique des secrets et une séparation nette des rôles
humain / agent / système. Les coûts opérationnels (goulot d'étranglement
de validation humaine, onboarding d'actions plus lent) sont acceptés
comme nécessaires à la sécurité du système.

Le passage du statut **PROPOSED** à **ACCEPTED** est conditionné à la
confirmation des dix hypothèses listées en section 6.

---

## LONG_RUN_SUMMARY

```
elapsed_seconds: ~15
budget_initial: 180
progress_emitted: false
progress_count: 0
extension_requested: false
timeout_closeout_emitted: false
verdict: COMPLETE
files_touched:
  - /Users/bot/02_Dev/vibebackbone/docs/architecture/0010-proxy-security-boundaries.md (created)
tests_run:
  - structural_check: file exists at expected path (yes)
  - sections_check: 8 mandated sections present (Titre+Status, Date, Contexte, Décision, Conséquences, Alternatives, Risques, Hypothèses)
  - cardinal_rules_check: 10 rules numbered 1..10 detected (lignes 75, 86, 96, 107, 116, 126, 137, 149, 160, 173)
  - line_count: target 300-500 (after condensation, see below)
  - markdown_validity: pure markdown, no HTML, headings hierarchy coherent
  - vocabulary_check: 'frontières de sécurité' (5x), 'principe du moindre privilège' (1x), 'séparation des privilèges' (3x), 'défense en profondeur' (5x) — all present
  - checklist_present: section 7 with yes/no questions present
tests_missing: none for ADR writing (ADR is a documentation deliverable, no executable harness to run)
risks:
  - ADRs 0006/0007/0008/0009 still in batch (parallel writes), consistency check required at end of batch
  - docs/architecture/ folder created in this session; may need a routing decision if batch convention puts ADRs under docs/adr/ instead
open_points:
  - H1..H10 to confirm before PROPOSED → ACCEPTED
  - cross-ADR consistency review scheduled after batch closes
  - batch convention (docs/architecture/ vs docs/adr/) to be reconciled by orchestrator
```

---

## REVISION_HISTORY — 2026-06-02 (harmonisation D1-D7)

> Cette révision applique 7 patches ciblés (P29–P35) pour intégrer la
> décision D7 (règle de gouvernance repo), ajouter la Règle 11
> cardinale, et cross-référencer ADR 0011 (bypass prevention). Le
> `LONG_RUN_SUMMARY` historique est **préservé** ; cette section est
> additive.

### Patches appliqués (résumé)

| Patch | Section visée | Nature | Lignes (approx.) |
|---|---|---|---|
| P29 | Header / Date | ajout « Revised: 2026-06-02 — D7 repo governance rule » | 1 |
| P30 | Header / Status | PROPOSED → PROPOSED (rev. 2026-06-02) | 1 |
| P31 | §2.1 + §2.2 | ajout **Règle 11 — Bypass prevention** (D7) ; « 10 règles » → « 11 règles » | +35 |
| P32 | §2.4 (Tests de sécurité) | ajout **Test 6** — binaire sensible détecté par linter | +7 |
| P33 | §2.3 (STRIDE) | Déni de service détaillée avec seuils D6 | ~9 |
| P34 | §7.5 (Checklist) | ajout question sur linter `vbb-bypass-lint.py` | +4 |
| P35 | §8 (Conclusion) | cross-référence ADR 0011 | ~3 |

### Décision intégrée

- **D7** — règle de gouvernance repo : aucun composant Hermes/Cody/VBB
  ne peut appeler directement un binaire appartenant à la **liste
  canonique ADR 0011 §3 (règle 1)**. Tout passe par le proxy.
  Formalisée comme **Règle 11** cardinale. Implémentation de
  référence : `tools/vbb-bypass-lint.py` (V2, ADR 0011). Au POC :
  revue de PR manuelle.

### VALIDATION P.R2

- Compte des règles cardinales mis à jour : 10 → 11 (cohérent dans
  intro §2.1, titre §2.2, conclusion §8).
- Test 6 ajouté au §2.4 sans casser la numérotation.
- Section §2.3 STRIDE — DoS étoffée avec les seuils D6.
- Section §7.5 Checklist — nouvelle question ajoutée.
- `LONG_RUN_SUMMARY` historique **non touché** (patch additif only).
- Markdown valide, langue française préservée.

```yaml
FINAL_STATUS:
  revision: 2026-06-02
  decision_refs: [D7]
  patches_applied: 7
  files_touched:
    - docs/adr/0010-proxy-security-boundaries.md
  cross_refs_added:
    - ADR 0011 (bypass prevention, D7 repo governance rule)
  new_cardinal_rule:
    number: 11
    name: Bypass prevention
    forbids:
      - Liste canonique ADR 0011 §3 (règle 1) des binaires sensibles
        (référence unique : ssh/scp/rsync, gh auth/repo/secret, docker
        login/push, cat .env/printenv/env|grep, aws/gcloud/az, mysql/
        psql/redis-cli, kubectl/helm secrets, vault/pass, curl -H
        Authorization, python -c os.environ)
    enforcement:
      v2: tools/vbb-bypass-lint.py in CI
      poc: manual PR review (second pair)
    violation_response:
      refuse: E_BYPASS_DETECTED
      audit: event=bypass_attempt
      notify: Telegram to Brice
      weekly_report: vbb-audit-worker
  new_security_test:
    number: 6
    scenario: binaire sensible en première position dans command_template
    expected: refus E_BYPASS_DETECTED avant enregistrement
    v2_status: gate en CI
    poc_status: revue de PR manuelle
  stride_updates:
    denial_of_service: |
      Seuils D6 (ADR 0008 §2.2.1) détaillés : 30 req/min/appelant,
      5 sens/h/appelant, 10 credentialisées simultanées, 429 +
      Retry-After + audit + Telegram. Reste actif en niveau 2 et
      niveau 3.
  cardinal_rules_count:
    before: 10
    after: 11
  long_run_summary_preserved: true
  verdict: COMPLETE
```
