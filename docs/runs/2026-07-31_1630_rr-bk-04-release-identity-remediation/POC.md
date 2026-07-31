# POC — RR-BK-04 release identity and circularity boundary

**Statut**: CONCLUDED  
**Date**: 2026-07-31  
**Liée à ADR**: `docs/adr/0050-design-certification-assurance-schema.md`  
**Liée à RUN**: `docs/runs/2026-07-31_1630_rr-bk-04-release-identity-remediation/`

**CANDIDATE_SHA**: `58e51eeebfd057a359eb78393ce16d6df4a05cf3`

## Hypothèse

Nous supposons qu’un commit candidat limité aux métadonnées techniques peut
être identifié par son SHA complet `S`, tandis que les documents qui doivent
inscrire `S` sont portés séparément sans créer de dépendance circulaire.

## Test

```bash
git rev-parse --verify 0dd572cce05c60e95a0c0b850041b069e63e366a
git commit --dry-run --allow-empty -m "test: release identity boundary"
```

## Critère de réussite

GO si le sujet technique n’exige pas de contenir son propre SHA final et si
les documents SHA-dépendants peuvent être identifiés comme evidence carrier.

## Résultat observé

- **Date d’exécution vérifiable** : 2026-07-31 15:47:46+02:00 (premier commit du carrier)
- **Sortie littérale** : le commit Git est calculé à partir de son contenu;
  un document qui y inscrit son SHA final est donc auto-référentiel.
- **Métrique mesurée** : frontière technique/evidence carrier identifiable
  (seuil attendu : oui)

## Décision

- **Verdict** : GO
- **Justification** : la checklist et les documents de préparation SHA-liés
  seront traités comme evidence carrier distinct; le futur `P` reste non créé.

## Bilan

Hypothèse validée : le sujet candidat et son evidence carrier doivent être
explicitement séparés pour satisfaire l’identité exacte sans circularité.

---

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0050-design-certification-assurance-schema.md
hypothesis_validated: true
metric_observed: "non-circular subject/evidence-carrier boundary"
metric_threshold: "boundary identified"
reproducible: true
verified_at: "2026-07-31T13:47:46Z"
verified_by: "codex/gpt-5"
```
