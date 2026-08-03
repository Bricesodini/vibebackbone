---
run_id: "2026-08-02_documentary-cleanup-living-core-pilot"
phase: "03_DECISION"
voie: "AUDIT"
status: "AUTHORIZED_PARTIAL"
agent: "codex"
started_at: "2026-08-02T00:00:00Z"
ended_at: "2026-08-02T00:00:00Z"
next_phase: "04_REMEDIATION"
artifacts_consumed:
  - "02_AUDIT.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — Human decisions required

Le run s’arrête avant toute remédiation. Les décisions doivent être données
finding par finding, et non comme approbation globale.

## Lot A — gouvernance adversariale et boot

| Finding | Décision attendue | Question |
|---|---|---|
| LDC-001 | `OUI` | Réintégrer la Critical Rule 16 validée, sans CC-11, CR-2 ni REVISE-C v3. |
| LDC-002 | `OUI` | Aligner `SYSTEM.md` et sa source Pi sur la gouvernance v1.2 / ADR 0053. |
| LDC-003 | `OUI` | Corriger la provenance sans réécrire ADR 0051. |
| LDC-004 | `PLUS TARD` | Maintenir la dette sur les références périphériques ADR 0051 / ADR 0053 jusqu’à preuve complémentaire. |

## Lot B — contrat et état courant

| Finding | Décision attendue | Question |
|---|---|---|
| LDC-005 | `PLUS TARD` | Ne pas élargir le scope DTS dans ce lot; conserver `UNKNOWN`. |
| LDC-006 | `OUI` | Mettre à jour `docs/CONTEXT.md` comme routeur d’état et de sources. |
| LDC-007 | `PLUS TARD` | Maintenir `PROMPTS_ARCHITECTURE.md` partiellement `UNKNOWN`. |
| LDC-008 | `PLUS TARD` | Ne pas modifier ni redéployer Pi; préparer un handoff séparé. |

## Règle d’arrêt

Une réponse `OUI` autorise uniquement la détermination de la procédure. Elle
n’autorise aucune écriture. Une réponse `NON` est enregistrée sans modifier
l’artefact. Une réponse `PLUS TARD` devient une dette documentaire différée.

Les décisions humaines autorisent uniquement les remédiations explicitement
décrites dans le lot suivant. Elles n’autorisent aucune écriture hors périmètre,
aucun changement implicite du canon et aucun redéploiement.

## Verdict

`LIVING_DOCUMENTARY_CORE_REMEDIATION_AUTHORIZED_PARTIAL`
