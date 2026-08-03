---
run_id: "2026-08-03_f03-provenance-alignment"
phase: "POC"
status: "GO"
---

# POC — F-03 Provenance Alignment

Le POC est borné à une vérification en lecture seule de la chaîne de
provenance. Il ne certifie ni l’adoption canonique ni le runtime Pi déployé.

## Oracle

La représentation est cohérente si et seulement si :

1. ADR-0051 est conservé comme décision fondatrice historique;
2. ADR-0053 est explicitement la décision d’alignement v1.2;
3. la gouvernance active v1.2 pointe vers ADR-0053;
4. la représentation `SYSTEM.md` consomme la même règle que sa source Pi;
5. aucune phrase ne réinterprète rétroactivement les runs v1.1.

## Limite

L’absence de certification du runtime Pi déployé reste hors périmètre et ne
peut pas être convertie en preuve de conformité.
