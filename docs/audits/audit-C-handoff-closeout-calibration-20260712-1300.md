---
run_id: "2026-07-12_1300_audit-C-handoff-closeout"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "claude-code"
started_at: "2026-07-12T13:00:00Z"
ended_at: "2026-07-12T13:25:00Z"
next_phase: null
artifacts_consumed:
  - "docs/SESSION_RULES.md"
  - "docs/MEMORY_AND_HANDOFF.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "docs/PILOTAGE.md"
  - "docs/CONTEXTS.md"  # not actually read
  - "skills/t-vbb-session-handoff/SKILL.md"
  - "skills/t-vbb-commit-ready/SKILL.md"
  - "prompts/canonical/07-p-vbb-closeout.md"
  - "docs/templates/07_CLOSEOUT.md.template"
  - "docs/SESSION.md"
  - "docs/runs/2026-06-13_1700_release-candidate-prep/07_CLOSEOUT.md"
artifacts_produced:
  - "docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md"
---

# Audit C — Calibration handoff vs closeout

**Date** : 2026-07-12
**Périmètre** : les artefacts et prompts qui distinguent (ou confondent) **handoff** (travail non terminé, reprise attendue) de **closeout** (fin claire du processus).
**Question auditée** : la frontière entre handoff et closeout est-elle suffisamment explicite pour qu'un agent ou un humain lisant les artefacts sache immédiatement si le travail continue ou s'arrête ?
**Verdict** : `PARTIAL — distinction réelle mais implicite, à renforcer`. Les concepts sont bien définis dans `MEMORY_AND_HANDOFF.md` et `SESSION_RULES.md`, mais l'artefact `07_CLOSEOUT.md` sert aux deux usages (handoff et end) sans convention de nommage distincte, et un lecteur只看 `07_CLOSEOUT.md` ne sait pas toujours si le run est "paused-pending-resume" ou "definitively-closed".

---

## Résumé

Trois artefacts sont en jeu :
1. **`docs/SESSION.md`** (gitignored, local) — mémoire de reprise. Contient `Actions en cours` / `Décisions prises` / `Points ouverts`. **C'est le marqueur handoff canonique.**
2. **`docs/runs/{id}/07_CLOSEOUT.md`** (versionné, officiel) — mémoire officielle du run. Contient `Statut global` (COMPLET | PARTIEL | BLOQUÉ | ABANDONNÉ) + `Prochaine session recommandée` (Oui | Non).
3. **`t-vbb-session-handoff`** (skill) — écrit SESSION.md. **Cible le handoff.**
4. **`t-vbb-commit-ready`** (skill) — prépare un commit. **Cible le closeout-versionné.**

**Constat** : la distinction existe mais repose sur **deux signaux indirects** :
- Pour SESSION.md : la présence d'`Actions en cours` non vide = handoff en cours.
- Pour 07_CLOSEOUT.md : la valeur du `Statut global` (COMPLET ≠ PARTIEL) + `Prochaine session recommandée` (Non ≠ Oui).

**Aucun signal explicite** (préfixe de nom, header dédié, label "HANDOFF" vs "CLOSEOUT") ne distingue les deux usages dans les artefacts versionnés. Un humain ouvrant `07_CLOSEOUT.md` d'un vieux run ne sait pas si le run est "fini-terminé" ou "fini-en-pause".

**3 findings** (0 P0, 1 P1, 2 P2). Pas de P0 car aucune confusion catastrophique en cours — la distinction est correcte pour les agents qui lisent SESSION.md en premier (ce que `MEMORY_AND_HANDOFF.md` ligne 56 prescrit). Le risque est pour les nouveaux agents ou humains qui lisent les artefacts versionnés sans lire SESSION.md.

---

## Findings

### P1 (1)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-C-001** | Le même artefact `07_CLOSEOUT.md` est utilisé pour deux usages sémantiquement distincts : (a) **handoff** = "travail non terminé, reprise attendue" ; (b) **closeout** = "fin claire du processus". La distinction repose entièrement sur le couple `Statut global` + `Prochaine session recommandée`, ce qui est **implicite** et non visible dans le nom du fichier, son chemin, ou son header. | `docs/templates/07_CLOSEOUT.md.template` (lignes 1-50) ne contient aucun champ `kind: HANDOFF | CLOSEOUT` ou `type: pause | final`. `prompts/canonical/07-p-vbb-closeout.md` (lignes "Statut global") définit COMPLET/PARTIEL/BLOQUÉ/ABANDONNÉ mais pas un discriminant explicite handoff/closeout. | Un humain qui ouvre un vieux `07_CLOSEOUT.md` doit interpréter le statut pour deviner si le run est terminé ou suspendu. Risque de confusion pour les nouveaux venus et pour les outils qui scannent les artefacts (par exemple `vbb-status-dashboard.py`). |

### P2 (2)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-C-002** | La route "CLOSEOUT" dans `docs/PILOTAGE.md` ligne 27 englobe **trois usages distincts** : "End of session, handoff, pause". L'action prescrite est la même (`t-vbb-commit-ready` → git commit → git push → update SESSION.md + CONTEXT.md) sans distinction explicite selon que le run est fini ou en pause. | `docs/PILOTAGE.md` ligne 27 : la table "4 route families" liste une seule route CLOSEOUT couvrant les trois cas. | Un agent qui reçoit la consigne "CLOSEOUT" ne sait pas s'il doit faire un commit-and-stop (closeout) ou un commit-and-pause-with-handoff. La nuance est dans SESSION.md, pas dans la consigne. |
| **AUDIT-C-003** | `docs/SESSION.md` (gitignored) est **la** mémoire de reprise canonique, mais elle n'a pas de convention de nom pour distinguer un handoff "actif" d'un handoff "archivé". Le fichier est écrasé à chaque session. Si SESSION.md est supprimé (machine réinstallée), un humain ne peut pas savoir quels points étaient ouverts à la dernière session. | `docs/SESSION.md` ligne 1-30 contient "Session active / Actions en cours" sans versioning. Aucun historique `SESSION.{date}.md` n'est conservé. | Perte d'historique de reprise. Si plusieurs sessions courtes s'enchaînent, l'historique de handoff est perdu. Risque mineur car SESSION.md est conçu pour être éphémère par design. |

---

## Cartographie actuelle : qui fait quoi

| Acteur | Quand | Produit | Cible sémantique |
|--------|-------|---------|------------------|
| `t-vbb-session-handoff` | Milieu ou fin de session, contexte à préserver | Update de `docs/SESSION.md` | **Handoff** (travail continue) |
| `t-vbb-commit-ready` | Fin de run, commit à préparer | Update ou création de `docs/runs/{id}/07_CLOSEOUT.md` + message de commit | **Closeout** (commit en cours) |
| `07-p-vbb-closeout.md` (prompt canonique) | Phase 07 d'un run | Création de `07_CLOSEOUT.md` + update de SESSION.md, CONTEXT.md, AUDIT_STATUS.md | **Les deux** (selon statut global) |
| Route CLOSEOUT dans PILOTAGE.md | Décision de fin de session | Enchaîne `t-vbb-commit-ready` + git + update SESSION.md | **Les trois** (end, handoff, pause) |

**Observation** : `t-vbb-session-handoff` est **explicitement handoff** (skill isolé). `t-vbb-commit-ready` est **explicitement commit** (skill isolé). Mais **le prompt canonique 07-p-vbb-closeout.md** et **la route CLOSEOUT** mélangent les deux usages sans discriminant explicite.

---

## Marqueurs actuels (implicites)

| Marqueur | Localisation | Sémantique | Force |
|----------|--------------|------------|-------|
| `Statut global: PARTIEL` | `07_CLOSEOUT.md` | Indique que le travail n'est pas fini | **Moyenne** — lisible mais pas explicite |
| `Prochaine session recommandée: Oui` | `07_CLOSEOUT.md` | Indique une reprise attendue | **Moyenne** — lisible mais pas dans le nom |
| `Actions en cours: [...]` non vide | `docs/SESSION.md` | Indique handoff actif | **Forte** — mais SESSION.md est gitignored, pas versionné |
| `Statut: COMPLET` dans SESSION.md | `docs/SESSION.md` ligne 6 | Indique session terminée | **Forte** — mais même limitation gitignored |
| `next_phase: null` (frontmatter) | `07_CLOSEOUT.md` | Indique qu'il n'y a pas de phase suivante dans ce run | **Faible** — convention frontmatter non documentée partout |

---

## Manifestation concrète du risque

Scénario : Brice revient après 3 mois et veut savoir où en est le projet. Il lit `docs/runs/2026-06-13_1700_release-candidate-prep/07_CLOSEOUT.md`.

**Aujourd'hui** : il doit lire tout le fichier, repérer le `Statut global`, croiser avec `Prochaine session recommandée`, et interpréter manuellement. Si le statut est `PARTIEL`, c'est un handoff. Si `COMPLET`, c'est un closeout.

**Avec un discriminant explicite** (par exemple `kind: HANDOFF | CLOSEOUT` dans le frontmatter), il saurait immédiatement sans lire le corps.

**Cas aggravé** : si Brice n'a pas accès à SESSION.md (gitignored, sur une autre machine), il n'a plus accès à `Actions en cours`. La sémantique de handoff repose alors à 100 % sur `07_CLOSEOUT.md`, qui n'a pas de marqueur dédié.

---

## Comparaison : ce qui est bien vs ce qui manque

### Bien calibré ✅

| Aspect | Pourquoi c'est bon | Référence |
|--------|---------------------|-----------|
| Distinction entre **3 niveaux de mémoire** (conversation / local / versionné) | Claire et sans ambiguïté | `docs/MEMORY_AND_HANDOFF.md` lignes 9-19 |
| Distinction entre **statut** (COMPLET/PARTIEL/BLOQUÉ/ABANDONNÉ) et **prochaine session** (Oui/Non) | Donne deux axes orthogonaux | `prompts/canonical/07-p-vbb-closeout.md` étape 1 |
| `t-vbb-session-handoff` est une skill **distincte** de `t-vbb-commit-ready` | Pas de confusion d'usage | `skills/t-vbb-session-handoff/SKILL.md` + `skills/t-vbb-commit-ready/SKILL.md` |
| `SESSION.md` est gitignored par design | Ne pollue pas le repo | `docs/MEMORY_AND_HANDOFF.md` ligne 14 |
| `CONTEXT.md` doit être mis à jour synthétiquement (pas recopié) | Évite la dérive de narration | `prompts/canonical/07-p-vbb-closeout.md` étape 6 |

### À renforcer ⚠️

| Aspect | Pourquoi c'est fragile | Référence |
|--------|------------------------|-----------|
| Pas de marqueur explicite `kind: HANDOFF | CLOSEOUT` dans `07_CLOSEOUT.md` | Discrimination implicite | `docs/templates/07_CLOSEOUT.md.template` |
| Pas de nom de fichier distinct (par exemple `07_HANDOFF.md` vs `07_CLOSEOUT.md`) | Pas de discrimination par nom | `docs/AGENTIC_RUN_PROTOCOL.md` |
| Pas de préfixe dans SESSION.md (par exemple `SESSION.active.md` vs `SESSION.archived.md`) | Pas de versioning de l'historique handoff | `docs/SESSION.md` |
| Route CLOSEOUT dans PILOTAGE.md englobe 3 usages | Consigne ambiguë si le worker ne lit pas SESSION.md d'abord | `docs/PILOTAGE.md` ligne 27 |
| Pas de documentation explicite "ce run est un HANDOFF, pas un CLOSEOUT" dans les artefacts | Discrimination implicite uniquement | (manquant) |

---

## Recommandations (texte seulement)

| ID reco | Description | Effort | Pré-requis |
|---------|-------------|--------|-----------|
| R-C-1 | Ajouter un champ `kind: HANDOFF \| CLOSEOUT` dans le frontmatter de `07_CLOSEOUT.md.template`. Valeur par défaut : `CLOSEOUT`. Surcharge explicite `HANDOFF` si statut ≠ COMPLET ou si `Prochaine session recommandée = Oui`. | S | Aucun |
| R-C-2 | Renommer `07_CLOSEOUT.md` en `07_HANDOFF.md` quand le statut global = PARTIEL/BLOQUÉ et qu'une prochaine session est prévue. Garder `07_CLOSEOUT.md` pour les runs COMPLET/ABANDONNÉ. **Option lourde** car change la convention ; à arbitrer. | L | R-C-1 |
| R-C-3 | Renforcer `prompts/canonical/07-p-vbb-closeout.md` étape 1 : calculer le `kind` automatiquement selon les règles R-C-1 et l'exposer en haut du closeout (« ⚠️ CE CLOSE EST UN HANDOFF — travail non terminé, reprise attendue »). | S | R-C-1 |
| R-C-4 | Documenter dans `docs/SESSION_RULES.md` la distinction explicite : "**handoff** = SESSION.md est non-vide, le run n'est pas terminé ; **closeout** = SESSION.md vidé après CLOSEOUT, le run est terminé". | S | Aucun |
| R-C-5 | Séparer la route CLOSEOUT dans `PILOTAGE.md` en deux : `CLOSE-HANDOFF` (paused, SESSION.md conservé) et `CLOSE-FINAL` (terminated, SESSION.md vidé). Option orthogonale au route actuel. | M | R-C-1 |
| R-C-6 | Versionner l'historique SESSION.md : créer un fichier `docs/SESSION.history/{date}.md` à chaque closeout, garder `docs/SESSION.md` pour la session active uniquement. Évite la perte d'historique en cas de réinstall. | M | Aucun |

---

## Quick wins

1. **QW-C-1** — Modifier le template `07_CLOSEOUT.md.template` pour ajouter un champ `kind: HANDOFF \| CLOSEOUT` en haut. 5 minutes.
2. **QW-C-2** — Mettre à jour `prompts/canonical/07-p-vbb-closeout.md` étape 1 pour calculer le kind automatiquement et l'annoncer en haut du fichier. 5 minutes.
3. **QW-C-3** — Vérifier les 3 derniers `07_CLOSEOUT.md` de `docs/runs/` : leur statut est-il `COMPLET` ? Si oui, ce sont des closeouts finals. Si `PARTIEL`, ce sont des handoffs — SESSION.md devrait contenir `Actions en cours` non vide. 5 minutes.

---

## Unknowns / needs confirmation

| ID | Question | Conséquence |
|----|----------|-------------|
| UN-C-1 | Brice veut-il une **distinction physique** (nom de fichier différent) ou une **distinction logique** (champ frontmatter) ? | Impacte R-C-2 |
| UN-C-2 | Le renommage `07_HANDOFF.md` vs `07_CLOSEOUT.md` est-il acceptable étant donné que le canon `AGENTIC_RUN_PROTOCOL.md` et `docs/runs/README.md` mentionnent uniquement `07_CLOSEOUT.md` ? | Canon change requis ou extension |
| UN-C-3 | SESSION.md doit-il être **versionné** (perte de la propriété gitignored) ou **archivé localement** (`docs/SESSION.history/` non versionné) ? | Choix privacy vs traçabilité |

---

## Verdict

`PARTIAL — distinction correcte dans le canon, à renforcer dans les artefacts versionnés`. Le risque n'est pas une confusion en cours (les agents lisent SESSION.md en premier par convention), mais une ambiguïté pour les lecteurs qui n'ont pas accès à SESSION.md ou pour les outils de dashboard qui scannent les artefacts. Quick wins disponibles sans canon change. R-C-2 (renommage) est la seule recommandation qui toucherait au canon.