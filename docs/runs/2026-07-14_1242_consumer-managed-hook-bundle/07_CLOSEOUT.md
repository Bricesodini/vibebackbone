---
run_id: "2026-07-14_1242_consumer-managed-hook-bundle"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
kind: "CLOSEOUT"
agent: "codex"
started_at: "2026-07-14T13:12:00+02:00"
ended_at: "2026-07-14T13:15:00+02:00"
next_phase: null
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "04_PLAN.md"
  - "05_EXECUTION.md"
  - "POC.md"
  - "INTEGRATION_GATE.md"
  - "CANON_CHANGE_PROPOSAL.md"
artifacts_produced:
  - "07_CLOSEOUT.md"
---

# 07_CLOSEOUT — Consumer managed hook bundle

## Type de closeout

**Kind**: `CLOSEOUT` — remédiation SEC-CRED-005 et frontière TER-001 terminées.

## Résultat

L'initialiseur dispose d'une frontière d'ownership explicite et d'un bundle de
hooks consommateur complet, préflighté et testable. Un échec d'installation ou
une personnalisation n'est plus masqué comme un succès.

**Evidence**: ADR 0034, POC 6/6, `tools/vbb-project-init.py`, 19 tests project-init
et `docs/audits/test-coverage-20260714-1252.md`.

## Décisions prises

- Documents projet : project-owned, generated-once, jamais rafraîchis par le
  mécanisme runtime.
- Assets hooks : VBB-managed, hashes SHA-256 et preflight global.
- Permissions : document, hook Git et asset géré sont trois consentements
  distincts.
- Propagation : mécanisme Core identique pour Pi, OpenCode, Codex et Claude.

## Change Set

- Initialiseur corrigé, erreurs fail-closed et manifeste atomiquement remplacé.
- Huit scénarios critiques de cycle de vie ajoutés aux tests existants.
- ADR, architecture, skill, checklist consommateur et états actifs réconciliés.
- Aucun dépôt consommateur réel, secret, API, DB ou runtime de production touché.

## Commit Readiness

`READY` — le changement forme un seul lot cohérent : comportement initialiseur,
tests de cycle de vie, contrat d'ownership et propagation documentaire. P.R2
passe sur l'état final ; le scan credentials staged reste le dernier contrôle
mécanique avant commit.

## Coherence Check

- ADR 0034, code, skill et checklist consommateur décrivent les trois mêmes
  permissions séparées.
- ARCHITECTURE est la source ; RELATIONS est régénéré.
- AUDIT_STATUS et CONTEXT retirent les deux gaps consommateurs actifs.
- Les quatre distributions héritent du Core sans fichier adapter modifié.
- Le rapport de couverture expose les limites P2 sans les masquer en succès.

## Remaining Risks

- Les consommateurs historiques sans manifeste exigent une adoption explicite.
- PyYAML reste un prérequis déclaré pour le loop-closure gate.
- Une panne I/O au milieu des copies n'a pas de rollback transactionnel ; les
  conflits logiques sont toutefois détectés avant toute écriture.
- Aucun merge automatique des documents projet n'est fourni ni promis.

## Vérifications finales

- Gate d'entrée : PASS, `can_code_start=true`.
- P.R2 : PASS — architecture 0/0, graph régénéré, contrats 0/0, loop strict
  PASS, 178 tests passés / 1 skipped, CI locale 9/9 sans warning.
- Credentials self-scan staged : à exécuter avant commit.

## Statut dette

- SEC-CRED-005 : fermé par bundle complet, hook réel et erreurs fail-closed.
- TER-001 : fermé dans son acception bornée de frontière d'ownership ; la
  synchronisation documentaire reste volontairement manuelle.
- Gaps P2 de couverture : manifeste corrompu, asset retiré et panne I/O listés
  dans le rapport de test coverage.

## Suggested Commit Message

`fix(init): manage consumer hook bundle safely`

## Next Action

Scanner le diff staged, puis commit et push de la branche.

```yaml
FINAL_STATUS: COMPLETE
decision: GO
evidence:
  - docs/adr/0034-consumer-managed-runtime-assets.md
  - docs/runs/2026-07-14_1242_consumer-managed-hook-bundle/POC.md
  - docs/audits/test-coverage-20260714-1252.md
verification:
  pr2: "PASS — 178 passed, 1 skipped; local CI 9/9"
open_points:
  - historical consumers require explicit managed-asset adoption
```
