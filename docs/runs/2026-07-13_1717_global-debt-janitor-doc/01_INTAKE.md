---
run_id: "2026-07-13_1717_global-debt-janitor-doc"
phase: "01_INTAKE"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-13T17:17:00+02:00"
ended_at: "2026-07-13T17:19:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/PROJECT_MODE.md"
  - "docs/SESSION.md"
  - "docs/AUDIT_STATUS.md"
  - "docs/CONVENTIONS.md"
  - "docs/adr/0026-global-maintainability-audit-before-remediation.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Global debt, Janitor, conventions and documentation audit

## Demande reçue

Effectuer une passe globale de dette technique et Janitor, puis vérifier la
cohérence avec les conventions et la documentation.

## Reformulation

Auditer l'ensemble du dépôt sans modifier son comportement : inventorier la
dette structurelle, qualifier le bruit de maintenance, évaluer la conformité au
canon `docs/CONVENTIONS.md`, puis croiser les surfaces exécutables et la
documentation active. Produire une roadmap bornée pour les corrections futures.

## Scope

### Dans le périmètre

- Core, outils, scripts, tests, distributions supportées, skills et prompts.
- Documentation active, architecture, catalogues, statuts et dette existante.
- Résidus legacy, fichiers orphelins, chemins obsolètes, duplication et drift.
- Rapports des quatre skills demandés et consolidation dans `AUDIT_STATUS.md`.

### Hors périmètre

- Refactor, suppression, renommage ou correction de code dans cette phase.
- Réécriture des runs, audits, ADR et archives historiques.
- Changement de convention canonique ou ajout de linter.
- Changements utilisateur préexistants et fichiers non suivis hors de ce run.

## Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : scan global et conclusions systémiques sur un framework
  distribué ; les skills sélectionnés imposent une posture read-only.

## Voie recommandée

- **Voie** : `AUDIT`
- **Justification** : diagnostic global, rapports horodatés et aucun patch de
  comportement ou de structure.

## Séquence d'audit

1. `1-vbb-tech-debt`
2. `1-vbb-code-janitor`
3. `1-vbb-conventions`
4. `1-vbb-code-doc-coherence-auditor`
5. consolidation, vérifications et closeout

## Integration Gate

- **ADR** : `docs/adr/0026-global-maintainability-audit-before-remediation.md`
- **POC** : non requis, car aucun code ni intégration n'est produit.
- **Frontière** : audit read-only ; toute remédiation ouvre un run séparé.

## Handoff vers `02_AUDIT`

- Conserver une distinction stricte entre documentation active et historique.
- Ne pas intégrer les artefacts non suivis préexistants au périmètre audité sans
  les identifier comme état local non canonique.
- Chaque finding doit citer un chemin ou une commande reproductible.
