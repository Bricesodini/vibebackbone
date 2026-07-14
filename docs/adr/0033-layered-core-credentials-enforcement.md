# ADR — 0033-layered-core-credentials-enforcement

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Décideurs**: Brice (`Go`, 2026-07-14), Codex (formalisation)
**Liée à**: ADR 0027 (canonical hook installer), AGENTS.md Critical Rule #13
**Liée à POC**: `docs/runs/2026-07-14_1150_credentials-enforcement/POC.md`

## Contexte

L'audit SEC-01 confirme que le hook pré-commit affiche seulement un message
credentials et retourne `0`, tandis que la CI n'exécute aucun contrôle de
contenu. Le mécanisme local est en outre optionnel et contournable par
`--no-verify`. Deux findings P1, SEC-CRED-001 et SEC-CRED-002, restent donc
ouverts malgré l'interdiction canonique de commiter un secret.

La remédiation doit couvrir la frontière locale et la frontière CI avec une
politique unique, sans dépendance externe, sans vrais credentials de test et
sans scanner inutilement les suppressions ou les contenus historiques.

## Décision

Nous adoptons un **scanner credentials Core unique**, versionné sous
`tools/vbb-credentials-gate.py`, avec deux modes d'entrée partageant exactement
le même moteur de détection :

1. `--staged` analyse les lignes ajoutées entre `HEAD` et l'index Git ;
2. `--range BASE HEAD` analyse les lignes ajoutées dans une plage Git en CI ;
3. le hook pré-commit appelle le mode staged et bloque sur finding ;
4. GitHub Actions appelle le mode range avec un historique complet ;
5. les suppressions, contenus binaires et lignes inchangées ne sont pas scannés ;
6. les exceptions utilisent un marqueur local explicite avec une justification,
   visible dans le diff et signalé par le scanner ;
7. l'outil reste Python stdlib et les fixtures sont synthétiques, assemblées à
   l'exécution afin qu'aucune valeur ressemblant à un credential ne soit suivie.

## Alternatives considérées

### Alternative A — Hook local uniquement

- **Avantages** : faible effort, retour rapide au développeur.
- **Inconvénients** : installation optionnelle et `--no-verify` maintiennent
  SEC-CRED-002 ouvert.

### Alternative B — Scanner tiers en CI uniquement

- **Avantages** : moteur spécialisé et filet centralisé.
- **Inconvénients** : feedback tardif, nouvelle dépendance/supply chain et
  divergence avec le contrôle local.

### Alternative C — Scan complet du dépôt à chaque passage

- **Avantages** : détecte aussi le contenu historique.
- **Inconvénients** : bruit sur les exemples existants, coût croissant et
  blocage de changements sans rapport avec une dette antérieure.

### Statu quo — Revue manuelle

- **Avantages** : aucun coût d'implémentation.
- **Inconvénients** : non reproductible et insuffisant face aux deux P1.

## Rationale

Le modèle local + CI est le seul qui couvre simultanément le feedback rapide et
le bypass des hooks. L'analyse différentielle borne les faux positifs aux
contenus nouvellement introduits. Un moteur Core unique évite que les quatre
distributions développent des politiques divergentes.

## Conséquences

### Positives

- Même décision de sécurité en local et en CI.
- Aucun package supplémentaire à installer.
- Preuves reproductibles sur ajouts, modifications, suppressions et binaires.

### Négatives / coûts

- Les patterns high-confidence ne garantissent pas de détecter tout secret.
- Le marqueur d'exception peut être abusé et doit rester visible/revu.
- La CI doit disposer de l'historique Git nécessaire au calcul de plage.

### Neutres / à surveiller

- Les credentials historiques ne sont pas requalifiés par ce gate différentiel.
- L'enforcement est Core ; aucune glue spécifique aux distributions n'est prévue.

## Références

- `docs/audits/security-credentials-20260714-1040.md`
- `docs/runs/2026-07-14_1040_credentials-enforcement-audit/03_DECISION.md`
- `scripts/hooks/pre-commit-framework-gate`
- `.github/workflows/vbb-contracts.yml`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: SECURITY_ARCHITECTURE
reversible: true
depends_on:
  - docs/runs/2026-07-14_1040_credentials-enforcement-audit/03_DECISION.md
blocks: []
supersedes: []
verified_at: "2026-07-14T11:50:00+02:00"
verified_by: "Brice + Codex"
verified_method: "explicit-human-approval + bounded-poc"
```
