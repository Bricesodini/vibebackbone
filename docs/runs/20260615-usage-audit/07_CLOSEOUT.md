---
run_id: 20260615-usage-audit
phase: 07_CLOSEOUT
voie: STRUCTURED
status: COMPLETE
agent: pi
started_at: 2026-06-15T08:00:00
ended_at: 2026-06-15T10:30:00
artifacts_consumed:
  - docs/runs/20260615-usage-audit/orgabar_scan.md
  - docs/runs/20260615-usage-audit/swiftminuteur_scan.md
  - Données manuelles Secrets/Guard Backbone
artifacts_produced:
  - docs/runs/20260615-usage-audit/01_INTAKE.md
  - docs/runs/20260615-usage-audit/02_AUDIT.md
  - docs/runs/20260615-usage-audit/07_CLOSEOUT.md
---

# Audit d'usage réel de Vibe Backbone — CLOSEOUT

## Résultat

**Audit croisé terminé.** 164 éléments VBB analysés, 3 projets consommateurs inspectés (Orgabar, Secrets/Guard Backbone, SwiftMinuteur), 24 runs audités.

## Verdict

**Vibe Backbone est surdimensionné de ~67% par rapport à son usage réel.**

- **54 éléments (33%)** sont réellement utilisés et doivent être conservés
- **110 éléments (67%)** sont à alléger, fusionner, archiver ou supprimer

## Décisions actées

1. **Le modèle 8 phases est une fiction** — 0/24 runs l'ont utilisé intégralement. Le pattern réel est 2-3 artefacts.
2. **77% des skills sont inutilisés** — 49/64 skills sans trace d'invocation.
3. **Les 4 documents du noyau dur sont le véritable backbone** — CONTEXT, PROJECT_MODE, SESSION, AUDIT_STATUS (100% de présence).
4. **Les phases 03_DECISION et 06_REVIEW sont à supprimer/fusionner** — jamais produites.
5. **ACTIVITY_LOG.md est une pratique émergente prometteuse** — utilisé intensivement par Secrets.

## Livrables produits

| Livrable | Fichier | Taille |
|----------|---------|--------|
| INTAKE | `01_INTAKE.md` | 1.8 KB |
| AUDIT (rapport croisé) | `02_AUDIT.md` | 30.7 KB |
| CLOSEOUT | `07_CLOSEOUT.md` | ce fichier |
| Scan Orgabar | `orgabar_scan.md` | 14.0 KB |
| Scan SwiftMinuteur | `swiftminuteur_scan.md` | 15.7 KB |

## Prochaine étape

Le rapport est autoporteur. Les recommandations peuvent être appliquées directement :
- **Conserver** : 54 éléments — aucun changement nécessaire
- **Simplifier** : 5 éléments — réécriture légère
- **Fusionner** : 10 éléments (6 paires) — consolidation
- **Archiver** : 78 éléments — déplacer vers `docs/archive/` ou `docs/reference/`
- **Supprimer** : 2 éléments — suppression directe

La mise en œuvre de ces recommandations nécessite une validation humaine (le rapport touche à la structure canonique de VBB Core).

## Points de vigilance

- Les prompts sont classés « archiver » sur la base de l'absence de traces dans les projets, pas sur l'absence d'usage par les agents. Une analyse côté agent (Pi, Cody, Claude Code) serait nécessaire pour affiner.
- Les skills « archivés » restent disponibles pour réactivation si un nouveau contexte les rend nécessaires.
- `t-vbb-mode-transition-gate` est référencé mais jamais exécuté — à surveiller si des projets passent en PROD.
