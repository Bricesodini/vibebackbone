---
run_id: "2026-08-03_f03-provenance-alignment"
phase: "05_EXECUTION"
status: "PASS_BOUNDED"
agent: "codex"
---

# 05_EXECUTION — F-03 Provenance Alignment

Toutes les actions ci-dessous sont en lecture seule.

## Preuves d’identité

- HEAD observé : `55b3696a5f2b681af73384167717bbb318056152`.
- `SYSTEM.md -> distributions/pi/SYSTEM.md`.
- Hash SHA-1 Git observés :
  - ADR-0051 : `1371501fb2208db199b38d71b4b2a1aae2c5168e`.
  - ADR-0053 : `ca004cfda48f48f9deabd37c346efc61fc32db99`.
  - gouvernance v1.2 : `26170bb09fbc1990df8362eabffeec890f5c411f`.
  - source Pi et représentation `SYSTEM.md` : `f9926431ba0651a20dbbf0f39e26842929e2b074`.

## Validations exécutées

| Commande / contrôle | Résultat |
|---|---|
| `python tools/vbb-gate-check.py docs/runs/2026-08-03_f03-provenance-alignment --json` | PASS; `can_code_start: true`, sans écriture |
| `readlink SYSTEM.md` | PASS; source Pi identifiée |
| `cmp -s SYSTEM.md distributions/pi/SYSTEM.md` | PASS |
| Recherche des références 0051/0053 et v1.2 | PASS; provenance explicite et non rétroactive |
| Statut ADR-0051 / ADR-0053 | PASS; les deux sont ACCEPTED |
| `python tools/vbb-adversarial-gate.py ... --strict` | PASS; forme A2 valide, verdict de campagne FAIL attendu à cause des findings |
| `pytest tests/test_adversarial_gate_yaml_unwrap.py tests/test_governance_coherence.py tests/test_canon_documents_level_reason.py` | PASS; 23 tests |
| `python tools/vbb-architecture.py lint` | PASS; 0 erreur, 0 warning |
| `python tools/vbb-contract-lint.py` | PASS avec 1 warning préexistant non bloquant |
| `git diff --check` et recherche d’espaces finaux du run | PASS |

## Validations non exécutées

- Aucun test de code C0–C5 : F-03 ne modifie ni validateur ni test.
- `tests/test_adversarial_gate.py` : non exécuté, fichier absent; le test ciblé disponible a été exécuté ci-dessus.
- Aucun runtime Pi : état déployé non accessible dans ce run.
- Aucune validation de publication, tag, merge ou adoption : explicitement hors périmètre.

La convention documentaire complète reste bloquée par la précondition de dépôt
`.vbb/document-convention.yaml` absente; ce contrôle n’est pas converti en
PASS et ne modifie pas la qualification des findings F-03.

## Mutation

Aucun fichier candidat, ADR ou distribution n’a été modifié par ce run.
