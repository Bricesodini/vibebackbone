---
run_id: "2026-07-14_1242_consumer-managed-hook-bundle"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T12:42:00+02:00"
ended_at: "2026-07-14T12:46:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "docs/AUDIT_STATUS.md"
  - "docs/runs/2026-07-14_0721_consumer-refresh-poc/POC.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Consumer managed hook bundle

## Demande

Fermer conjointement `SEC-CRED-005` et la frontière d'ownership de `TER-001` :
`vbb-project-init --install-hook` doit installer un hook consommateur réellement
fonctionnel sans écraser silencieusement la vérité propre au projet.

## Triage

- **Route** : STRUCTURED / STRUCTUREE.
- **Pourquoi** : changement Core structurel, sécurité locale, format de métadonnée
  consommateur et quatre distributions héritières.
- **Décision humaine** : Brice a répondu `Go` après exposition explicite du besoin
  d'un mandat d'ownership commun à SEC-CRED-005 et TER-001.
- **Gate** : ADR + POC + Integration Gate obligatoires avant code.

## Périmètre

- Séparer les documents projet générés une fois des assets runtime gérés par VBB.
- Installer et rafraîchir le bundle de hooks et ses dépendances transitives.
- Refuser un rafraîchissement si un asset géré a été personnalisé depuis le
  dernier état connu, sauf autorisation dédiée et explicite.
- Propager toute erreur d'installation vers un exit non-zéro.
- Tester bootstrap, refresh sûr, conflit, préservation des docs et dry-run.

## Hors périmètre

- Fusion automatique des documents projet personnalisés.
- Mise à niveau générale de tous les templates de gouvernance consommateurs.
- Modification d'un runtime provider ou d'un dépôt consommateur réel.
- Détection de credentials historiques.

## Critères d'acceptation

1. Un dépôt Git temporaire fraîchement initialisé reçoit un hook exécutable.
2. Le hook peut lancer ses outils depuis le dépôt consommateur.
3. Un asset géré inchangé est rafraîchi de façon idempotente.
4. Un asset géré personnalisé est préservé et provoque un exit non-zéro.
5. Les documents projet existants restent inchangés sans `--overwrite`.
6. Un hook étranger n'est remplacé qu'avec une option dédiée.
7. Les quatre distributions héritent du même contrat Core sans glue.

## Liens de décision

- **Liée à ADR** : `docs/adr/0034-consumer-managed-runtime-assets.md`
- **POC requis** : `docs/runs/2026-07-14_1242_consumer-managed-hook-bundle/POC.md`
