---
run_id: "2026-07-29_1130_gcg-genericity-stress-test"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "PARTIAL"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T09:30:00Z"
ended_at: "2026-07-29T10:20:00Z"
artifacts_produced:
  - "02_STRESS_TEST.md"
  - "docs/REFERENCE/governance-compatibility-model.md (v2)"
---

# 05_EXECUTION — GCG-STRESS-01

## 1. Mesures exécutées

Chaque constat de `02_STRESS_TEST.md` est adossé à l'une de ces mesures.

| # | Mesure | Résultat | Sert |
|---|---|---|---|
| 1 | `vbb-governance-compat.py --json` | 162 total, 14 applicables, `2/14`, verdict FAIL | baseline |
| 2 | Balayage de `knowledge_harvest` / `*_governance_version` sur 162 runs | 19 gouvernés par la règle B | §2.1 |
| 3 | `validate_knowledge_harvest()` sur les 162 runs | 2 non-conformités | §2.1 |
| 4 | Lecture de `_knowledge_governance_required()` (`vbb-loop-closure-check.py:216-252`) | **3 sources d'applicabilité**, combinées par `OR` | **S1** |
| 5 | Recherche d'un run pré-cutoff auto-déclarant `adversarial_governance_version` en frontmatter | **aucun** — S1 est latent | **S1** |
| 6 | Recherche d'un run dont `started_at` franchit la borne que l'identité ne franchit pas | **aucun** — S1 est latent | **S1** |
| 7 | Écart identité − `started_at` sur les runs ≥ 2026-07-26 | **deux conventions**, +2.00 h et +0.00 h | **S2** |
| 8 | Constantes `*_CUTOVER_KEY` / `*_CUTOVER_AT` | 3 cutovers, chacun en 2 unités ; paire adverse dupliquée sur 2 fichiers | **S2, S8** |
| 9 | `vbb-contract-lint.py` | 0 erreur / 67 skills — règle C intégralement satisfaite | **S4** |
| 10 | `ls docs/knowledge*` + lecture de `vbb-loop-closure-check.py:310-316` | aucun registre de candidats ; validation par énumération seule | **S6** |
| 11 | Balayage des titres `## …Knowledge Harvest` sur les runs gouvernés | **9 dispositions positives sans section** | **S6** |
| 12 | `find_closeout()` vs chemin en dur `07_CLOSEOUT.md` | divergence réelle sur `2026-07-28_1200_m1` (`02_CLOSEOUT.md`) | **S5** |
| 13 | `git log -S'def validate_knowledge_harvest'` | commit `ae273b5`, même jour et même run que `applies_from` | **S7** |

## 2. Deux hypothèses formulées puis réfutées

Un stress test qui ne réfute rien de ses propres hypothèses n'a pas cherché.

**H1 — « l'énumérateur laisse tomber silencieusement les runs non datables ».**
Formulée en voyant `20260615-usage-audit` et `2026-07-12_runNN`, dont les noms
ne suivent pas le schéma principal. Réfutée par la mesure 1 : 162 répertoires
sur disque, 162 énumérés, 0 perdu. `_RUN_ID_RE` accepte les trois schémas de
nommage. La branche `UNKNOWN` sur identité non parsable est aujourd'hui
inatteignable — c'est un défaut fail-closed correct, pas un défaut actif.

**H2 — « le run `2026-07-28_1002` auto-déclare `adversarial_governance_version`
et GCG le masque ».** Le grep initial trouvait bien la chaîne dans ce run, ce
qui aurait fait de S1 un défaut **actif** avec instance. Vérification au parseur
de frontmatter : l'occurrence est à la ligne 61 de `05_MIGRATION_STRATEGY.md`,
**dans un bloc de code citant le contrat proposé**. C'est le document qui
*spécifie* le champ, pas un artefact qui se déclare gouverné.

S1 est donc **latent, prouvé par construction** — un sous-ensemble d'une
disjonction est au plus aussi inclusif — et non par instance. La distinction est
consignée telle quelle dans `02_STRESS_TEST.md` §5.

## 3. Ce qui a été révisé, et ce qui ne l'a pas été

**Révisé** (v2) : §3.2 (fenêtre vide, métrique), §3.4 (contrat
d'applicabilité), §3.5 (unité de frontière), §3.6 (contrat de population), §3.7
(résolution d'artefact), §4 (tableau annoté), §4.2 (seconde instance
d'`OVERCLAIM`), §5 (I9–I11 + aveu de couverture), §6.1 (acte multi-règles), §7
(portée réelle), §8 (trois questions ouvertes supplémentaires).

**Non révisé, délibérément** : les huit catégories, les invariants I1–I8, la
séparation Scanner / Arbitration / Migration Engine, la règle anti-blanchiment,
la primauté d'`OVERCLAIM`, le refus de dériver la certification. Le test ne les
a pas mis en défaut ; les modifier aurait été de l'embellissement.

## 4. Écart déclaré — l'obligation de corpus a forcé du code

Déclarer `S1`–`S5` comme `CONFIRMED` a déclenché une obligation canonique que
la contrainte C1 ne pouvait pas neutraliser :

```
tests/test_corpus_mandatory.py FAILED
  CONFIRMED finding S1 (severity S1) has no CORPUS-S1.py
  … idem S2, S3, S4, S5
```

ADVERSARIAL_ASSURANCE §9 destination 6 : *mandatory for every `CONFIRMED`
finding, no exception, regardless of severity*. Trois issues, une seule
défendable :

| Issue | Verdict |
|---|---|
| Rétrograder `confidence` en `PLAUSIBLE` | **refusé** — c'est littéralement « rétrograder un niveau pour obtenir le vert », interdit par la contrainte normative du run `1021` §6.3 et par l'invariant I3 |
| Laisser la CI rouge | déclarer une obligation canonique et ne pas l'honorer — la version miroir du défaut que ce chantier combat |
| **Écrire les entrées de corpus** | **retenu** |

Cinq `CORPUS-S<n>.py` écrits, en **BEHAVIOUR_PIN** — le mode déjà utilisé par
`CORPUS-ADVR-RT-01..03` pour des findings non remédiés. Un pin n'encode aucun
verrou `fails_before` / `passes_after` : il fige le comportement **défectueux**
pour qu'il ne puisse pas changer en silence. Vert y signifie *« le défaut connu
est toujours exactement tel que documenté »*, jamais *« corrigé »*.

**C'est une violation de C1, bornée et assumée.** C1 était ma reformulation de
« le but n'est pas d'écrire du code » ; l'interdiction explicite de la demande
portait sur la **poursuite de l'implémentation** — Migration Engine, ledger,
câblage CI. Aucun de ces trois n'a avancé d'une ligne. Le code écrit ne répare
aucun défaut et n'implémente aucun amendement de la v2 : il verrouille les
défauts constatés. Ajout d'une fixture au `conftest.py` du corpus, bump
`VERSION` v1.1.0 → v1.2.0, `INDEX.md` complété.

Ce que cet écart révèle mérite d'être noté : **un run ne peut pas déclarer des
findings confirmés et rester sans code.** L'obligation de corpus est en amont de
toute contrainte de périmètre qu'un run se donne à lui-même.

### Autres écarts

- **`S1` non corrigé** — contrainte C1, et corriger l'instrument pendant qu'on
  le mesure invaliderait la mesure. Reste ouvert, désormais verrouillé par
  `CORPUS-S1.py`.
- **ADR 0052 non écrit** — contrainte C2, et le verdict `NOT_CANONICAL_YET` le
  rendrait de toute façon prématuré.
- **Aucun test pour I9–I11** — les pins verrouillent des défauts, pas des
  invariants. Le ratio de couverture reste 3/11, comme écrit au modèle §5.

## 5. Contraintes d'intake — vérification

| Contrainte | Vérification |
|---|---|
| C1 aucun code écrit ou modifié | ❌ **violée, bornée** — 5 pins de corpus + 2 fixtures ; voir §4 |
| C2 ADR 0052 non rédigé | ✅ `docs/adr/` inchangé |
| C3 implémentation non poursuivie | ✅ ni ledger, ni moteur, ni câblage CI ; `tools/` inchangé |
| C4 verdict justifié, pas affirmé | ✅ 8 constats, chacun rattaché à une mesure du §1 |

## 6. Vérification finale

`bash scripts/vbb-ci-local.sh` → **16 passed, 0 failed, 0 warnings**.

`vbb-governance-compat.py` : `2/15` — le nouveau run entre dans la population
et s'y classe `CURRENT_NONCOMPLIANCE`, comme les précédents, faute d'acteur A2
distinct. La conformité mesurée ne s'améliore pas et ne devait pas.
