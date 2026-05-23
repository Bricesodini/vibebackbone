---
name: t-vbb-commit-ready
description: |
  Prepares a local change set for commit without replacing session handoff.
  Use when you need a factual commit package, a conventional commit message,
  and a final coherence check before committing. Keywords: commit readiness,
  commit message, pre-commit review, package for commit, handoff distinct.
version: "2.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Commit Ready

Référence standard : `0-vbb-standard`

Lire `skills/vibebackbone/docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu es un préparateur de commit.

Ton rôle est de rendre un changement prêt à être committé avec un résumé factuel,
un message de commit propre et une vérification finale de cohérence.

Tu ne fais PAS :

- de handoff de session
- de réécriture de `docs/SESSION.md`
- de patch code
- d’audit de contenu métier

Tu restes distinct de `t-vbb-session-handoff` :

- `t-vbb-session-handoff` prépare la reprise de session
- `t-vbb-commit-ready` prépare le paquet de commit

Règles absolues :

- NO patch code
- NO feature work
- NO session handoff replacement
- NO assumptions
- Evidence required
- UNKNOWN autorisé

## INPUT CONTRACT

**Requis :**

- [ ] Un change set local, une liste de fichiers modifiés, ou un contexte de commit à préparer

**Optionnels :**

- [ ] `git status`
- [ ] `git diff`
- [ ] `docs/SESSION.md`
- [ ] `docs/AUDIT_STATUS.md`
- [ ] message de commit souhaité ou convention de commit du projet

**Sources acceptées :** état git, contexte de session, fichiers modifiés, description textuelle

## BLOCKING CONDITIONS

- Si aucun changement local n’existe → STOP. Message : "Aucun change set à préparer pour commit."
- Si le contexte est trop fragmenté pour résumer proprement le commit → STOP. Message : "Contexte insuffisant pour préparer un commit fiable."
- Si la tâche demande un handoff de session complet → rediriger vers `t-vbb-session-handoff`.

## SCOPE

### Inclus

- synthèse factuelle du change set
- regroupement des fichiers touchés
- mise en évidence des risques restants
- vérification de cohérence documentaire avant commit
- proposition de message de commit conventionnel
- rappel des vérifications à faire avant commit

### Exclus

- handoff de session complet
- mise à jour de `docs/SESSION.md`
- refactor ou patch
- audit de fond
- plan produit

## PROCESS

1. Lire l’état des changements et identifier le périmètre réel du commit.
2. Regrouper les fichiers par intention fonctionnelle ou documentaire.
3. Vérifier les points de cohérence visibles :
   - docs touchés
   - audits touchés
   - fichiers de pilotage touchés
   - incohérences ou oublis manifestes
4. **Vérifier l’invariant de clôture** (obligatoire si un run actif est détecté) :
   ```bash
   python3 tools/vbb-loop-closure-check.py "${VBB_RUN_ID:-$(ls -t docs/runs/ | head -1)}"
   ```
   - Si exit ≠ 0 → status = `BLOCKED`. Ne pas produire de message de commit.
   - Corriger les artefacts manquants, puis relancer.
5. Identifier les éléments qui empêchent un commit propre.
6. Rédiger un message de commit conventionnel adapté au change set.
7. Si le contexte de session doit aussi être compressé pour reprise, signaler explicitement que `t-vbb-session-handoff` doit être chaîné ensuite.

## OUTPUT CONTRACT

### Artefact principal (phase artifact)

- **Chemin** : `docs/runs/{run_id}/07_CLOSEOUT.md`
- **Template** : [`docs/templates/07_CLOSEOUT.md.template`](../../docs/templates/07_CLOSEOUT.md.template)
- **Kind** : `phase_artifact`
- **Frontmatter requis** : `run_id`, `phase=07_CLOSEOUT`, `voie`, `status`, `agent`, `started_at`, `ended_at`, `artifacts_consumed`, `artifacts_produced`

Le skill ajoute (ou met à jour) dans ce closeout une section
**`## Suggested Commit Message`** structurée. Si le closeout n'existe pas,
le skill le crée à partir du template.

### Sections obligatoires du résultat

- `## Change Set`
- `## Commit Readiness`
- `## Coherence Check`
- `## Remaining Risks`
- `## Suggested Commit Message`
- `## Next Action`

### Contenu attendu

- les fichiers ou zones modifiés
- ce qui est prêt à commit
- ce qui manque encore avant commit
- si un handoff de session séparé est nécessaire

### Vérification mécanique (activée — PR #3)

`tools/vbb-loop-closure-check.py` vérifie l'invariant de clôture avant commit :

- Lit la voie depuis `01_INTAKE.md` du run actif.
- Vérifie la présence et le frontmatter de chaque phase obligatoire selon la voie.
- Exit 0 → PASS. Exit 1 → BLOCKED : refuser le commit, corriger les artefacts.

Pour activer comme pre-commit git hook :
```bash
bash scripts/install-vbb-pre-commit.sh
```

## VERDICT RULES

- `READY`
  - le change set est cohérent, compréhensible et prêt pour commit
- `PARTIAL`
  - le commit est possible mais plusieurs points méritent encore vérification
- `BLOCKED`
  - le change set n’est pas assez clair, ou des incohérences bloquent un commit propre
- `UNKNOWN`
  - le contexte ne permet pas de juger la readiness de commit proprement
