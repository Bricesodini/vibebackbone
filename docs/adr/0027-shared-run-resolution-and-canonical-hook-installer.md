# ADR — 0027-shared-run-resolution-and-canonical-hook-installer

**Status**: PROPOSED — à passer ACCEPTED au GO Brice (GO conditionnel du 2026-07-13, cf. 03_PLAN_REDUCTION_V2.md)
**Date**: 2026-07-13
**Route**: STRUCTUREE
**Décideurs**: Brice (GO conditionnel), Claude (formalisation)
**Liée à**: ADR 0026 (audit global avant remédiation — ce run est la première micro-boucle de remédiation)
**Liée à POC**: docs/runs/2026-07-13_1811_v2r1-gates-fiables/POC.md

## Contexte

L'audit tech-debt global (`docs/audits/tech-debt-20260713-1728.md`) a identifié deux
P1 qui fragilisent les gates locaux :

- **TD-101** : `tools/vbb-loop-closure-check.py` auto-sélectionne le mauvais run
  (détection lexicale d'un ancien run `20260615-usage-audit`), alors que
  `tools/vbb-status-dashboard.py` classe correctement les runs récents par mtime.
  Le gate peut donc contrôler le mauvais run — faux blocage ou fausse assurance.
- **TD-102** : deux installateurs de hooks concurrents
  (`scripts/install-framework-gate-hook.sh` installe un fichier que Git n'exécute
  pas par défaut ; `scripts/install-vbb-pre-commit.sh` écrase `.git/hooks/pre-commit`
  avec une implémentation moins complète). L'utilisateur peut croire les gates
  actifs alors qu'une partie seulement s'exécute.

SESSION.md (closeout `2026-07-13_1717`) déclare ce périmètre comme prochaine
priorité : « run STRUCTURED limité à la sélection auto du run et à l'installation
unique des hooks (TD-101 + TD-102) ».

## Décision

1. **Résolution de run unique à deux sélecteurs** : une seule fonction de résolution
   (classement par mtime, gestion des noms mixtes `YYYYMMDD-*` / `YYYY-MM-DD_HHmm_*`)
   est extraite et partagée par `vbb-status-dashboard.py`, `vbb-loop-closure-check.py`
   et le chemin CI. Elle expose **deux sélecteurs distincts** — « dernier run
   existant » (population : tous les répertoires de runs) et « dernier run clôturé »
   (population : runs avec closeout) — et chaque consommateur déclare explicitement
   lequel il utilise ; les deux populations ne sont jamais supposées identiques.
   La détection lexicale propre à loop-closure est supprimée. Des tests couvrent
   les noms mixtes, le cas TD-101 reproduit, et la divergence normale entre les
   deux sélecteurs quand un run actif n'est pas clôturé.
2. **Installateur de hooks canonique** : un installateur unique compose les deux
   hooks locaux déjà testés (`pre-commit-framework-gate`, `commit-msg-framework-gate`)
   dans `.git/hooks/` ; l'autre point d'entrée est déprécié avec message de
   redirection. Aucun nouveau mécanisme de hook n'est introduit.
3. **Liaison ADR stricte dans le gate** : lorsqu'un `01_INTAKE.md` (ou `04_PLAN.md`)
   référence explicitement une ADR, `tools/vbb-gate-check.py` vérifie **cette ADR-là**
   et ne bascule **jamais** vers une autre ADR acceptée présente dans le contexte.
   Défaut observé le 2026-07-13 pendant la préparation de ce run : le gate s'est
   déclaré satisfait via l'ADR-0026 (ACCEPTED, citée en artefact consommé) alors que
   l'ADR explicitement liée (0027) était PROPOSED — un faux PASS de la même famille
   que TD-101. Test de non-régression requis : intake référençant une ADR `PROPOSED`
   avec une ADR `ACCEPTED` tierce citée → `adr_present_and_accepted=false`,
   blocker `ADR_NOT_ACCEPTED`.

## Conséquences

### Positives
- Le gate loop-closure contrôle le bon run — condition préalable à V2-R6
  (autonomie multi-runs avec loop-closure inter-runs).
- Une seule vérité d'installation des hooks ; fin du faux sentiment de couverture.
- Le gate ADR ne peut plus être satisfait par une ADR non liée : fin d'une seconde
  source de faux PASS. Ce run s'applique la règle à lui-même : son propre gate
  exige 0027 = ACCEPTED, sans bascule vers 0026.

### Négatives / coûts
- Refactor d'un outil sans test direct aujourd'hui (fonction `main` 218 lignes,
  TD-106) : le découpage reste limité à l'extraction de la résolution, pas un
  refactor global (consigne ADR-0026).
- Un installateur déprécié à maintenir en redirection pendant une période de grâce.

### Neutres
- Aucun changement de canon (CONVENTIONS/PILOTAGE intacts) ; pas de CCP requis.
- Comportement du dashboard inchangé (il fournit la référence correcte).

## Alternatives rejetées (≥ 2)

### Alternative A — Corriger seulement la regex lexicale de loop-closure
- **Description** : patcher la détection existante sans partager la résolution.
- **Pourquoi rejetée** : maintient deux implémentations divergentes ; la dérive
  se reproduira au prochain format de nom de run (cause racine de TD-101).

### Alternative B — Supprimer l'un des deux installateurs sans composition
- **Description** : garder uniquement `install-vbb-pre-commit.sh`.
- **Pourquoi rejetée** : c'est l'implémentation la moins complète ; on perdrait
  le framework-gate testé (`tests/test_framework_gate_hook.sh`).

## Périmètre POC

POC requise sur TD-101 uniquement (hypothèse d'intégration : la résolution mtime
du dashboard, appliquée au contexte loop-closure, sélectionne le bon run sur les
données réelles du dépôt). TD-102 ne comporte pas d'hypothèse technique non
validée (mécanique git standard, hooks déjà testés individuellement) : design
couvert par la présente ADR.
