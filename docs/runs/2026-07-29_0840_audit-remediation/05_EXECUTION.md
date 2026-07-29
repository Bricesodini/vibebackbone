---
run_id: "2026-07-29_0840_audit-remediation"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T06:40:00Z"
ended_at: "2026-07-29T09:30:00Z"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "05_EXECUTION.md"
---

# 05_EXECUTION — AUDIT-REMEDIATION-01

## Commits

| SHA | Objet | Findings |
|---|---|---|
| `f8850ca` | ruff check + format sur le périmètre canonique | F1 |
| `a2a1d0a` | corpus directory tracked | F14 |
| `95516ad` | verdict `NOT_READY` + parser de verdict | F15, ouverture du run |
| `6986c7d` | lint bidirectionnel + contrats adversariaux | F2, F16, F17 |
| `2ec063b` | gate 5b exécutable et exécuté | F3, F5 |
| `10696b0` | tri des runs par identité | F19 |
| `9efb145` | obligation corpus + 3 entrées | F4, F18 |
| `bfd02f5` | réalignement des surfaces + cohérence | F6, F7 |

`f8850ca` et `a2a1d0a` sont hors run (route FAST-MINIMAL) : ils rétablissaient la
CI, prérequis à toute vérification.

## Findings découverts pendant l'exécution

Sept findings non identifiés par l'audit initial, tous confirmés par mesure.

| ID | Objet | Comment il a été trouvé |
|---|---|---|
| F14 | `tests/adversarial_corpus/` non suivi par git — CI rouge sur 8 commits | POC EXP-3, suite exécutée sur un clone frais |
| F15 | Le dashboard lisait le verdict dans la prose sous la déclaration | En écrivant `NOT_READY`, le dashboard affichait `READY` |
| F16 | Le skill corpus affirmait une application par un gate qui ne l'assure pas | Lecture du gate en écrivant son contrat |
| F17 | Entrées de corpus routées vers `docs/adversarial_corpus/`, inexistant | Lecture du skill campagne en écrivant son contrat |
| F18 | Le skill corpus exemptait S3, en contradiction avec §9 | Trois findings CONFIRMED S3 réels sans entrée |
| F19 | Sélecteur « dernier run » trié par `mtime`, arbitraire dans un clone | CI distante rouge juste après le câblage de 5b |
| F20 | Le bloc canonique mélangeait `python -m pytest` et `pytest` nu | Preuve négative n°5, exécution verbatim du bloc |

F19 mérite d'être noté : c'est une régression introduite par ce run. Rendre 5b
bloquant a exposé un défaut de sélecteur que deux consommateurs partageaient
depuis ADR-0027, invisible tant que le seul appelant local était non bloquant et
qu'aucun n'était câblé en CI distante.

## Décisions

- **§9 vs skill corpus (F18)** — escaladé, non tranché seul. Décision humaine :
  appliquer §9 tel qu'il est écrit, créer les trois entrées manquantes, et
  n'amender §9 que par un `CANON_CHANGE_PROPOSAL` distinct si l'obligation sur
  les S3 s'avère injustifiée à l'usage. Le canon n'est pas modifié pour
  correspondre à l'implémentation.
- **Findings ARBITRATED sans lock** — les trois findings sont confirmés mais non
  remédiés, donc sans `fails_before`/`passes_after`. Enregistrés comme
  `BEHAVIOUR_PIN` : l'entrée fige le comportement défectueux actuel et casse le
  jour où il change. Un pin vert signifie « le défaut connu est inchangé »,
  jamais « corrigé ».
- **Renversement de l'assertion RUN 3 (F19)** — `mtime` ne peut pas arbitrer
  l'ordre des runs. La préoccupation protégée par RUN 3 (un dossier future-daté
  ne doit pas dominer) est reportée sur le signal de provenance temporelle, qui
  la porte déjà, et pinnée par un test.
- **Artefacts du run non commités incrémentalement** — le hook de clôture exige
  les quatre phases dès qu'un run est stagé. Les fournir à mi-parcours aurait
  signifié publier un closeout dont les résultats de gate n'existaient pas.

## Matrice de preuve négative

Exécutée le 2026-07-29. Chaque manipulation est annulée immédiatement après
mesure ; l'état restauré est revérifié à chaque ligne.

| # | Manipulation | Attendu | Observé |
|---|---|---|---|
| 1 | Retirer `skills/t-vbb-index/CONTRACT.yaml` | lint non-zéro, dashboard FAIL | `contract-lint exit=1`, 2 erreurs nommant `t-vbb-index`, `Contracts 65/66 FAIL` — restauré exit=0 |
| 2 | Retirer `CORPUS-ADVR-RT-01.py` | test corpus échoue en nommant le finding | `exit=1` : « CONFIRMED finding ADVR-RT-01 (severity S3) has no CORPUS-ADVR-RT-01.py » — restauré exit=0 |
| 3 | Retirer 5b de la CI locale | dérive détectée vs CI distante | `exit=1` : `test_local_ci_runs_both_halves_of_5b` et `test_local_and_remote_ci_use_the_same_5b_interface` — restauré exit=0 |
| 4 | Réintroduire la revendication `PROPOSED` sur un ADR accepté | contrôle de cohérence échoue | `exit=1` : « still cites 2026-07-28_1002_… but 0051-… is accepted » — restauré exit=0 |
| 5 | Exécuter le bloc canonique verbatim | sortie 0 | **d'abord exit=2** → F20 découvert et corrigé → **exit=0**, se termine sur `CI PASSED` |

Preuves négatives complémentaires exécutées au fil des étapes : outil du
dashboard ramené à HEAD (2 tests échouent), les trois surfaces 5b ramenées à HEAD
(5 tests sur 9 échouent), helper de résolution ramené à HEAD (le sélecteur
renvoie `20260602_0817_legacy`), `AUDIT_STATUS.md` et `CONTEXT.md` réels ramenés
à HEAD (les deux contrôles de cohérence échouent sur le texte historique exact).

**Deux checkers ont dû être reconstruits après avoir échoué leur propre preuve
négative** : la première version du contrôle de statut cherchait une référence
ADR dans la puce — la puce réelle n'en contenait aucune ; la première version du
contrôle CONTEXT lisait ligne à ligne — la revendication et son sujet étaient sur
deux lignes. Les deux versions initiales passaient au vert contre le texte
fautif. Consigné plutôt que masqué.

## Critical Rule #12 — impact quatre distributions

Surfaces Core modifiées : `vbb-contract-lint.py`, `vbb-status-dashboard.py`,
`vbb-adversarial-gate.py`, `vbb_run_resolution.py`, `vbb-ci-local.sh`,
`vbb-contracts.yml`, `pre-merge-gate.md`, catalogue `skills/`.

Vérification : aucun fichier de `distributions/**` n'apparaît dans les diffs du
run. Les quatre distributions consomment le catalogue et les gates sans les
redéfinir ; le durcissement est strictement Core. Aucune glue à propager.

## Vérification finale

Boucle P.R2 complète, dans l'ordre canonique, plus la vérification sur clone
frais imposée par F14. Résultats consignés dans `07_CLOSEOUT.md`.
