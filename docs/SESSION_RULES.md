---
context_role: session-rules
phase: transverse
status: active
updated: 2026-05-23
---

# SESSION_RULES — Quand rester, quand changer

Une session = une fenêtre de contexte LLM cohérente, avec un rôle stable.
Ces règles décident si on continue dans la même session ou si on en démarre
une nouvelle.

## Principe directeur

> 1 session = 1 rôle = 1 intention = 1 sortie exploitable

Si un changement met en péril l'un de ces quatre invariants, ouvrir une
nouvelle session.

## Rester dans la même session

Autorisé tant que **tous** ces critères sont vrais :

- Même rôle agentique (intake reste intake, audit reste audit, …)
- Même voie d'exécution (`RAPIDE`, `STRUCTUREE`, `AUDIT`, `CLOTURE`)
- Scope inchangé ou réduit par rapport à `01_INTAKE.md`
- Niveau de risque inchangé ou abaissé
- Contexte non saturé (cible : <75 % de la fenêtre)
- Durée raisonnable (<30 min pour une voie RAPIDE, <2 h ailleurs)

Exemples typiques :
- `04_PLAN` → `05_EXECUTION` en voie RAPIDE ou STRUCTUREE (même rôle exécutant).
- Itération sur un même fichier après feedback humain immédiat.

## Changer de session

Obligatoire si **au moins un** de ces signaux apparaît :

- Le rôle change (planner → executor → reviewer → handoff).
- Le risque augmente (escalade détectée — voir `PILOTAGE.md` § Règle d'escalade).
- Le scope s'élargit au-delà de ce que `01_INTAKE.md` avait figé.
- Le contexte dépasse 75 % de la fenêtre.
- La session précédente a produit son artefact de clôture (`07_CLOSEOUT.md`).
- Plus de 30 minutes se sont écoulées en voie RAPIDE, ou plus de 2 h ailleurs.
- L'agent change de provider (claude-code → codex, etc.).

## Règle d'escalade et nouvelle session

Une tâche commencée en voie RAPIDE qui révèle un impact sur un contrat de
données, l'auth, la sécurité, l'intégrité ou la production :

1. **Stop immédiat** dans la session en cours.
2. Produire un `07_CLOSEOUT.md` partiel qui acte l'escalade.
3. Ouvrir une nouvelle session en voie `STRUCTUREE` ou `AUDIT` avec un nouvel
   `01_INTAKE.md` qui reprend le scope mis à jour.

## Handoff entre sessions

La continuité est portée par les artefacts versionnés, pas par la conversation.

À la fin d'une session :

- `07_CLOSEOUT.md` consolide ce qui a été livré et la prochaine action.
- `docs/SESSION.md` (local, gitignored) capture l'état immédiat de reprise.
- `docs/CONTEXT.md` est mis à jour si le run a changé l'état stable du projet.

À l'ouverture de la session suivante :

1. Lire `docs/CONTEXT.md` (MOC).
2. Lire `docs/PROJECT_MODE.md`.
3. Lire `docs/SESSION.md` s'il existe.
4. Lire `docs/AUDIT_STATUS.md` si voie AUDIT.
5. Lire le dernier `07_CLOSEOUT.md` sous `docs/runs/`.

## Anti-patterns à refuser

- Continuer en RAPIDE après détection d'un risque élevé.
- Démarrer une `05_EXECUTION` sans `04_PLAN` figé en voie STRUCTUREE.
- Mélanger deux runs dans le même dossier `docs/runs/{slug}/`.
- Reprendre une session sur la base de souvenir conversationnel sans relire
  l'artefact `07_CLOSEOUT.md` du run précédent.

## Liens

- [`AGENTIC_RUN_PROTOCOL.md`](AGENTIC_RUN_PROTOCOL.md) — les 7 phases
- [`PILOTAGE.md`](PILOTAGE.md) — triage et escalade
- [`MEMORY_AND_HANDOFF.md`](MEMORY_AND_HANDOFF.md) — mémoire entre sessions
