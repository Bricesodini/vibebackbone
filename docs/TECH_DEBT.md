---
context_role: tech-debt-register
phase: transverse
status: active
updated: 2026-05-27
---

# TECH_DEBT — registre léger de dette technique

> Index source-based des dettes techniques et documentaires connues.
> Ce fichier évite de rescanner tous les closeouts à chaque session.
> Il ne remplace pas `docs/AUDIT_STATUS.md`, qui reste la source de vérité pour l'état d'audit.

## Règles d'usage

- Chaque entrée doit pointer vers une source vérifiable : closeout, audit, fichier ou finding.
- Ne pas ajouter de dette spéculative sans source.
- Ne pas dupliquer les risques d'audit détaillés : les référencer depuis `docs/AUDIT_STATUS.md` si nécessaire.
- Fermer une entrée uniquement quand la correction et sa validation sont documentées.

## Règles de promotion

- Promouvoir un finding Janitor vers ce registre quand il n'est pas réductible par un diff local sûr.
- Promouvoir une dette quand elle doit être suivie au-delà de la session courante.
- Promouvoir un signal structurel si `1-vbb-code-janitor` recommande `1-vbb-tech-debt`.
- Ne pas promouvoir une préférence de style sans impact opérationnel vérifiable.
- Référencer `docs/AUDIT_STATUS.md` au lieu de dupliquer un risque d'audit déjà suivi.

## Règles de résolution

- Passer à `RESOLVED` uniquement après correction livrée et validation documentée.
- Passer à `MITIGATING` si une réduction partielle existe mais que la dette reste active.
- Passer à `ACCEPTED` seulement avec justification explicite et source vérifiable.
- Conserver `OPEN` si la correction minimale n'a pas été exécutée ou si les checks n'ont pas été relancés.

## Validation attendue

Une réduction de dette doit documenter :

- le diff minimal ou la décision de ne pas patcher
- les checks disponibles lancés, ou la raison de leur absence
- le statut final de l'entrée TECH_DEBT
- le closeout, rapport ou fichier source qui prouve la validation

## Statuts

| Statut | Sens |
|--------|------|
| `OPEN` | Dette connue, non traitée |
| `MITIGATING` | Correction partielle ou mitigation en cours |
| `ACCEPTED` | Dette explicitement acceptée, avec justification |
| `RESOLVED` | Correction livrée et validée |

## Registre

| ID | Statut | Source | Dette | Impact | Correction minimale | Dernière vérification |
|----|--------|--------|-------|--------|---------------------|----------------------|
| TD-001 | `MITIGATING` | [pyyaml-validation-dependency](runs/2026-05-26_2355_pyyaml-validation-dependency/07_CLOSEOUT.md) | Validation loop-closure dépend de PyYAML ; dépendance désormais déclarée mais non installée localement | Les checks mécaniques peuvent échouer dans un environnement Python nu | Installer `requirements.txt`, puis relancer `tools/vbb-loop-closure-check.py` sur les runs récents | 2026-05-26 : dépendance déclarée, validation non relancée |
| TD-002 | `ACCEPTED` | [post-audit-consigne-alignment](runs/2026-05-26_2330_post-audit-consigne-alignment/07_CLOSEOUT.md) | Debt Guard complet non intégré ; seul le pré-check documentaire existe | Le garde-fou reste déclaratif dans les prompts | Planifier un Debt Guard complet dans un run séparé si le besoin est confirmé | 2026-05-26 : explicitement hors scope |
| TD-003 | `OPEN` | [CONTEXT.md § Points ouverts](CONTEXT.md#points-ouverts) | Runs historiques sans closeout formel (`reformat-agentic-protocol`, `run05-test-cases`) | Reprise historique incomplète, rescans possibles | Décider : backfill minimal ou acceptation documentée | 2026-05-27 : toujours listé dans `CONTEXT.md` |
| TD-004 | `RESOLVED` | [SESSION.md § Prochaine session](SESSION.md#prochaine-session) | Couverture `CONTRACT.yaml` incomplète sur les skills restants | Contrats mécaniques partiels, validation inégale selon les skills | Étendre les contrats par phase (`1-vbb-*`, `4-vbb-*`, transverses restants) | 2026-05-27 : 62/62 contrats présents et indexés ; `vbb-contract-lint.py` vert |
| TD-005 | `RESOLVED` | [AUDIT_STATUS.md § REL-001](AUDIT_STATUS.md#risks-identified--status) | Statut release indiquait DEPLOYMENT/RUNBOOK absents alors que les fichiers existent | Reprise trompeuse pour release/readiness | Vérifier présence `docs/DEPLOYMENT.md` et `docs/RUNBOOK.md`, puis corriger `AUDIT_STATUS.md` | 2026-05-27 : fichiers présents et statut REL-001 résolu |

## Dernières mises à jour

| Date | Changement |
|------|------------|
| 2026-05-27 | TD-004 passé à `RESOLVED` après exhaustivité `skills/INDEX.yaml` et linter vert |
| 2026-05-27 | Ajout des règles de promotion, résolution et validation attendue |
| 2026-05-27 | Création du registre léger, initialisé depuis les closeouts et le contexte actif |
