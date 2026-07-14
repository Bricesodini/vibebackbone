# Security Remediation Plan — 2026-07-14 11:50

## Sources

- `docs/audits/security-credentials-20260714-1040.md`
- `docs/AUDIT_STATUS.md` — SEC-CRED-001 / SEC-CRED-002
- ADR 0033 — explicit human decision for layered Core enforcement

## P0 — Immediate / Blocking

Aucun P0 identifié par la source.

## P1 — Short-term

### SEC02-A — Implement one differential Core scanner

- **Source**: SEC-CRED-001
- **Action**: détecter les lignes ajoutées sensibles depuis l'index ou une plage
  Git avec un moteur Python stdlib unique.
- **Why**: remplacer le contrôle log-only par un verdict reproductible.
- **Effort**: medium
- **Dependencies**: ADR 0033, POC GO, Integration Gate
- **Status**: done

### SEC02-B — Enforce the same scanner locally and in CI

- **Source**: SEC-CRED-002
- **Action**: appeler le même outil depuis le hook, la CI locale et GitHub
  Actions afin que l'absence ou le bypass du hook ait un filet commun.
- **Why**: fermer la frontière de confiance locale contournable.
- **Effort**: medium
- **Dependencies**: SEC02-A
- **Status**: done

## P2 — Improvement

### SEC02-C — Define regression corpus and justified exceptions

- **Source**: SEC-CRED-003
- **Action**: couvrir positifs/négatifs, suppressions, binaires, SHA zéro,
  placeholders et exception avec justification.
- **Why**: maîtriser faux positifs et faux négatifs avant activation stricte.
- **Effort**: medium
- **Dependencies**: SEC02-A
- **Status**: done

## Quick wins

- Aucun quick win isolé : un hook-only fix laisserait SEC-CRED-002 ouvert.

## Structural fixes

- SEC02-A + SEC02-B forment une seule remédiation structurelle.
- SEC02-C est un prérequis d'activation, pas un polish différable.

## Cross-dependencies

| Action | Depends on | Nature |
|---|---|---|
| SEC02-A | ADR 0033 + POC | architecture et faisabilité |
| SEC02-B | SEC02-A | moteur partagé |
| SEC02-C | SEC02-A | contrat testable du moteur |

## Verdict

- **Status**: READY
- **Justification**: sources, décision, dépendances et critères sont bornés ;
  aucun P0 n'empêche la remédiation.
- **Recommended next step**: passer l'Integration Gate, puis implémenter
  SEC02-A/B/C dans le même run.

## Notes

- Aucun nouveau finding n'est créé par ce plan.
- La détection reste une défense en profondeur, pas une garantie exhaustive.
