---
run_id: "2026-08-03_f03-provenance-alignment"
phase: "02_AUDIT"
status: "PASS_BOUNDED"
agent: "codex"
---

# 02_AUDIT — F-03 Provenance Alignment

## Question auditée

La provenance active distingue-t-elle correctement la fondation historique
ADR-0051 de l’alignement v1.2 porté par ADR-0053, sans réécriture rétroactive,
et la représentation `SYSTEM.md` est-elle cohérente avec sa source Pi ?

## Observations

| Élément | Observation | Verdict |
|---|---|---|
| ADR-0051 | `Status: ACCEPTED`; décision fondatrice de la dimension adversariale | PASS |
| ADR-0053 | `Status: ACCEPTED`; décision d’alignement A2/A3 v1.2 | PASS |
| Gouvernance active | `version: "1.2"`, `adr: "0053"`, mention explicite que 0053 ne réécrit pas 0051 | PASS |
| Runs v1.1 | La gouvernance active indique que leur sens original est conservé | PASS |
| `SYSTEM.md` | Symlink vers `distributions/pi/SYSTEM.md`; contenu identique par `cmp` | PASS |
| Runtime Pi déployé | Non observé dans ce run | UNKNOWN, hors périmètre |

## Limites

Le contrôle ne certifie pas le runtime déployé, ne modifie aucune source et ne
juge pas l’adoption du modèle documentaire.
