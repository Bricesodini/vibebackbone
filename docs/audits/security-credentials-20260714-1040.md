---
audit_type: security
date: 2026-07-14
auditor: codex
scope: credentials_enforcement
verdict: PARTIAL
---

# Security audit — credentials enforcement

## Executive summary

**Verdict: PARTIAL.** L'interdiction canonique est explicite et honnêtement
documentée, mais aucun contrôle automatique ne bloque actuellement un contenu
staged sensible. Un marqueur synthétique staged traverse le hook avec un exit
code `0`, et le workflow CI n'exécute aucun scanner.

## Trust-boundary map

| Frontière | Contrôle courant | Limite vérifiée |
|---|---|---|
| Index Git → commit local | `pre-commit-framework-gate` | message informatif uniquement, contenu non lu |
| Installation → dépôt consommateur | hook local optionnel | hook préexistant non remplacé ; `--no-verify` possible |
| Push/PR → CI | `vbb-contracts.yml` | contrats, architecture, runtime et tests seulement |
| Canon → humain/agent | AGENTS.md §13 | revue manuelle obligatoire mais non automatisée |

## Findings

### SEC-CRED-001 — P1 — VIOLATION — VERIFIED_FINDING — NEEDS_DECISION

- **Observation** : le hook annonce un contrôle credentials.
- **Signal** : le commentaire du script précise que le futur
  `vbb-credentials-gate.py` est différé et que la vérification est informative.
- **Vérification** : un blob synthétique staged sous
  `tools/credential_fixture.py` produit le message puis un exit code `0` ; le
  worktree temporaire reste vide hors `.git`.
- **Finding** : l'invariant canonique « aucun secret commité » n'a aucun
  enforcement automatique sur le chemin de commit actuel.
- **Impact** : un credential peut entrer dans l'historique si la revue manuelle
  échoue, avec rotation et réécriture d'historique potentiellement nécessaires.

### SEC-CRED-002 — P1 — OBSERVATION — VERIFIED_FINDING — NEEDS_DECISION

- **Observation** : le contrôle pré-commit est installé dans `.git/hooks`.
- **Signal** : l'installation est optionnelle, ne remplace pas un hook existant
  sans `--overwrite`, et le hook documente `git commit --no-verify`.
- **Vérification** : le workflow GitHub Actions ne contient aucune étape de
  scan ; il ne compense donc ni l'absence ni le bypass d'un hook local.
- **Finding** : la frontière de confiance repose sur un mécanisme local
  contournable sans filet serveur versionné.

### SEC-CRED-003 — P2 — TREND — VERIFIED_FINDING — NEEDS_DECISION

- **Observation** : aucun outil ou corpus de test credentials n'existe.
- **Signal** : les tests de hooks couvrent installation, loop closure et message
  de commit, pas le contenu staged.
- **Vérification** : `tools/vbb-credentials-gate.py` est absent et aucune suite
  ne définit les suppressions, renommages, binaires, placeholders ou allowlists.
- **Finding** : une implémentation directe par liste de regex serait dépourvue de
  politique testée et exposée aux faux positifs comme aux faux négatifs.

### SEC-CRED-004 — P3 — OBSERVATION — VERIFIED_FINDING — MITIGATED

- **Observation** : AGENTS.md §13 indique explicitement que l'enforcement est
  différé et impose une vérification manuelle.
- **Vérification** : le hook et la documentation ne prétendent pas qu'un scanner
  actif existe.
- **Finding** : il n'y a pas de fausse déclaration de conformité ; la
  transparence réduit le risque de confiance aveugle, sans fermer les P1.

## Recommandation

1. Décider par ADR d'un outil Core unique qui inspecte les blobs staged.
2. Exécuter le même outil dans le hook local et dans la CI ; la CI constitue le
   filet non dépendant de l'installation locale.
3. Valider par POC les ajouts/modifications/renommages, ignorer les suppressions,
   gérer les binaires, et n'utiliser que des fixtures synthétiques.
4. Définir une allowlist explicite, localisée et justifiée avant tout blocage.
5. Ajouter des tests de faux positifs et faux négatifs avant activation stricte.

## UNKNOWN

- Le moteur de détection optimal (outil interne minimal ou dépendance dédiée)
  n'est pas décidé.
- Les politiques spécifiques des dépôts consommateurs restent hors scope.
