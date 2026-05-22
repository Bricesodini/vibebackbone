---
context_role: memory-rules
phase: transverse
status: active
updated: 2026-05-23
---

# MEMORY_AND_HANDOFF — Mémoire officielle et transitions

La mémoire de vibebackbone n'est pas dans la conversation. Elle est dans des
artefacts stables, versionnés ou explicitement locaux.

## Trois niveaux de mémoire

### 1. Conversationnelle (éphémère)

La fenêtre de contexte LLM en cours.

- Disparaît à la fin de la session ou au compactage.
- Ne peut pas être citée comme source dans un artefact.
- N'est jamais autoritative.

### 2. Locale persistante (gitignored)

Fichiers présents sur le poste, non versionnés.

- `docs/SESSION.md` — mémoire de reprise immédiate.
- Toute note personnelle dans `.vbb/` (si présent).
- Survit à une session, pas à un changement de machine.

### 3. Officielle (versionnée)

Artefacts dans `docs/` versionnés par git. C'est la mémoire autoritative.

- `docs/CONTEXT.md` — état stable du projet (MOC).
- `docs/PROJECT_MODE.md` — mode opérationnel.
- `docs/AUDIT_STATUS.md` — état des audits.
- `docs/runs/{slug}/0X_*.md` — artefacts de phase.
- `docs/audits/*.md` — rapports d'audit horodatés.

## Règles de priorité

En cas de divergence entre niveaux :

| Niveau 1 (conversation) | Niveau 2 (local) | Niveau 3 (versionné) | Source de vérité |
|--------------------------|------------------|----------------------|------------------|
| A | A | A | A |
| A | A | B | **B** (officiel) |
| A | B | B | **B** (officiel) |
| A | B | C | **C** (officiel) |

La conversation ne fait jamais foi seule.

## Handoff entre sessions

### Ce qui doit traverser

| Information | Support |
|-------------|---------|
| Décision majeure | `07_CLOSEOUT.md` + `docs/CONTEXT.md` |
| Action concrète restante | `07_CLOSEOUT.md` § « État pour la prochaine session » |
| Risque identifié non résolu | `docs/AUDIT_STATUS.md` |
| Hypothèse à valider | `07_CLOSEOUT.md` § « Points ouverts » |
| Mode opérationnel actuel | `docs/PROJECT_MODE.md` |
| Reprise immédiate (étape suivante) | `docs/SESSION.md` (local) |

### Ce qui ne traverse pas

- Le raisonnement intermédiaire (compaction du contexte LLM).
- Les explorations abandonnées (sauf si décision documentée).
- Les sorties de commande verbeuses (sauf citation utile).
- L'historique conversationnel détaillé.

## Cycle d'écriture

Toute information qui doit survivre à une session est explicitement persistée.

```
Conversation
   │
   │ (filtrage : utile à la suite ?)
   ▼
07_CLOSEOUT.md du run en cours
   │
   │ (synthèse : change l'état stable du projet ?)
   ▼
CONTEXT.md / AUDIT_STATUS.md
```

Si une information n'est jamais persistée, elle n'existe pas pour la session
suivante.

## Cycle de lecture

À l'ouverture d'une session :

1. `docs/CONTEXT.md` (toujours)
2. `docs/PROJECT_MODE.md` (toujours)
3. `docs/SESSION.md` (si présent localement)
4. `docs/AUDIT_STATUS.md` (si voie AUDIT)
5. Dernier `07_CLOSEOUT.md` sous `docs/runs/` (si présent)
6. Autres `0X_*.md` du run en cours, sur besoin

Ne pas charger l'intégralité de `docs/runs/` en début de session — cibler le
dernier run ou le run explicitement référencé.

## Anti-patterns

- Citer un fait depuis la conversation sans l'avoir écrit dans un artefact.
- Reprendre une session sans relire `07_CLOSEOUT.md` du run précédent.
- Mettre à jour `docs/CONTEXT.md` directement sans passer par un closeout.
- Considérer `docs/SESSION.md` comme une source autoritative (il est local).

## Discipline de contexte

`AGENTS.md` §12 prescrit la compaction proactive avant 75 % de la fenêtre.
Le pipeline de compaction utilise les artefacts officiels comme cible — pas
de compaction qui efface une décision qui n'a pas été écrite ailleurs.

## Liens

- [`AGENTIC_RUN_PROTOCOL.md`](AGENTIC_RUN_PROTOCOL.md) — les 7 phases
- [`SESSION_RULES.md`](SESSION_RULES.md) — quand changer de session
- [`runs/README.md`](runs/README.md) — convention des artefacts de run
