---
run_id: "2026-07-13_1717_global-debt-janitor-doc"
phase: "03_DECISION"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-13T17:36:00+02:00"
ended_at: "2026-07-13T17:37:00+02:00"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "02_AUDIT.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — Maintainability remediation boundary

## Décision

Clore cette passe comme baseline `PARTIAL`, sans patch de code ni changement de
canon. Traiter ensuite les findings par lots ordonnés : vérité des gates,
portabilité/docs, caractérisation executor, puis Janitor et typage.

## Rationale

Les contrôles canoniques sont verts et aucun P0 n'impose une mutation immédiate.
Mélanger un fix de gate, une fusion d'installateurs, 25 autofix Ruff, 26
reformatages et 48 erreurs mypy créerait un diff impossible à attribuer ou
rollbacker proprement.

## Ordre de décision recommandé

1. `TD-101 + TD-102` — run STRUCTURED gate/hooks.
2. `TD-105 + O-01..O-07` — run FAST-STANDARD docs/portabilité.
3. `TD-104` — run STRUCTURED tests executor.
4. `JAN-02..JAN-07` — run Janitor contrôlé.
5. Dette mypy — lots séparés par outil.

## Non-décisions

- Ruff/mypy ne deviennent pas des gates par défaut.
- `docs/CONVENTIONS.md` n'est pas modifié sans proposition canonique.
- Le fichier loose routing n'est ni déplacé ni supprimé sans clarifier son sort.
