---
run_id: "2026-07-29_1021_adversarial-gate-population"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_ENFORCEMENT_REMEDIATION"
adversarial_level: "A2"  # canon-gating work: redefines what the adversarial gate measures
scope_id: "GATE-POPULATION-01"
agent: "claude-opus-5 (Claude Code)"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
adr_link: "docs/adr/0051-adversarial-assurance-dimension.md"
linked_subject:
  schema: "git-commit"
  baseline_commit: "6b0daf4"
  audited_state: "6b0daf4785d652b23931b80aafba57979e69d9b4"
started_at: "2026-07-29T08:21:00Z"
ended_at: null
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/runs/2026-07-29_0840_audit-remediation/07_CLOSEOUT.md"
artifacts_produced:
  - "01_INTAKE.md (this file)"
  - "POC.md"
  - "02_DISPOSITION_MATRIX.md"
  - "03_CANON_CHANGE_PROPOSAL.md"
  - "04_PLAN.md"
  - "tools/vbb-governance-compat.py"
  - "tests/test_governance_compat_gate.py"
scope_note: >
  Cadrage révisé en cours de run : la cible passe d'un correctif du gate adverse
  à une capacité de gouvernance (Governance Compatibility Gate), sur demande de
  l'architecte produit. Voir 04_PLAN.md §0.
---

# 01_INTAKE — GATE-POPULATION-01

## 1. Demande reçue

> GO pour matérialiser le run et commencer R1 en fail-first. Avant toute
> modification rétroactive des dix runs, produire une matrice de disposition run
> par run et ne modifier aucun bloc tant que cette classification n'est pas
> arrêtée. Une preuve adversariale historique ne peut être reconstruite que
> depuis des artefacts contemporains suffisants ; sinon enregistrer explicitement
> une non-conformité historique non reconstructible. Ne jamais rétrograder un
> niveau pour obtenir le vert. Le gate final doit distinguer conformité actuelle,
> dette historique acceptée et certification réellement obtenue.

## 2. Objectif

Le gate adverse mesure aujourd'hui **un seul run** (`--latest`). Ce run étend sa
population aux runs post-cutoff, mesure la conformité réelle, et remplace le
verdict binaire par une lecture à trois catégories qui ne peut pas être satisfaite
par relabellisation.

Le critère d'acceptance central n'est pas que le gate repasse au vert. C'est que
le vert, quand il arrive, **ne puisse plus être obtenu autrement que par une
conformité réelle ou une dette explicitement enregistrée comme telle**.

## 3. Baseline mesurée (à `6b0daf4`, working tree propre)

```yaml
baseline:
  HEAD: "6b0daf4785d652b23931b80aafba57979e69d9b4"
  working_tree: clean
  documented_verdict: "PARTIAL"
  gate_command: "python3 tools/vbb-adversarial-gate.py --latest --strict"
  gate_exit: 0
  gate_population: 1          # latest_closed_run = 2026-07-30_0700
  post_cutoff_runs: 12
  post_cutoff_passing: 2
  post_cutoff_failing: 10
  runs_without_adversarial_block: 9
```

### Preuve d'invalidation conservée

Mesure par exécution du gate sur chaque run post-cutoff individuellement, à
`6b0daf4` :

```
gate=2 adv_block=0   2026-07-28_1400_m2-adversarial-loop-implementation
gate=2 adv_block=0   2026-07-28_1600_r0-adversarial-audit-of-m2-implementation
gate=2 adv_block=0   2026-07-28_1800_r1-r0-findings-normative-arbitration
gate=2 adv_block=0   2026-07-28_2000_m2-bis-adversarial-loop-bootstrap-deployment
gate=2 adv_block=1   2026-07-28_2200_a2-certification-of-m2-bis-bootstrap
gate=2 adv_block=0   2026-07-28_2300_r2-a2-arbitration-of-a2-findings
gate=2 adv_block=0   2026-07-29_0100_m3-remediation-of-a2-findings
gate=2 adv_block=0   2026-07-29_0300_a2-retry-certification-of-m3-remediation
gate=2 adv_block=1   2026-07-29_0840_audit-remediation
gate=0 adv_block=1   2026-07-30_0100_a2-auth-certification-of-m3-remediation
gate=2 adv_block=0   2026-07-30_0500_final-publication-of-v1.1-certification
gate=0 adv_block=1   2026-07-30_0700_claude-skills-discovery-01
```

Ces exits ne doivent pas être réécrits : ils constituent la mesure d'origine.
Le CI vert de `6b0daf4` s'explique entièrement par le fait que `--latest`
sélectionne `2026-07-30_0700`, l'un des deux seuls runs conformes.

## 4. Findings traités

| ID | Sévérité | Objet |
|---|---|---|
| `G1` | P0 | Le gate adverse a une population de un. 10/12 runs post-cutoff échouent, dont `2026-07-30_0500_final-publication-of-v1.1-certification` — le run qui publie la certification v1.1 |
| `G2` | P1 | Le run `2026-07-29_0840_audit-remediation` échoue réellement le gate (`[S1] adv-a2-distinct`), échec masqué par la sélection `--latest` |
| `G5` | P2 | `2026-07-28_2200` : 14 findings à `confidence`/`state` invalides + `defender_identity` absent, jamais détectés |
| `F8` | P2↑ | Dérive temporelle : 5 runs datés après la date locale. Promu en pré-requis — toute sélection par identité en dépend |

`G3` (classe de contradiction du frontmatter `status:`), `G4` (fausse équivalence
CI locale/distante) et `G6` (portée étroite de `test_governance_coherence`) sont
hors périmètre de ce run — ils forment R3 et R4 du plan.

## 5. Scope

### Dans le périmètre

- Sélecteur `--all` (population post-cutoff) et `--run <id>` (résolution explicite)
  sur `vbb-adversarial-gate.py`.
- Verdict à trois catégories : conformité actuelle / dette historique acceptée /
  certification obtenue.
- Registre de dette historique, borné par un horizon de conformité.
- Matrice de disposition run par run, **arrêtée avant toute écriture** dans un
  bloc adverse.
- Preuve fail-first : le gate étendu doit être démontré rouge à `6b0daf4`.

### Hors périmètre

- Toute modification d'un bloc adverse existant ou création d'un bloc rétroactif.
  Ce run **produit la classification, il ne l'exécute pas**. L'exécution est un
  run distinct, conditionné à l'arrêt de la matrice.
- R3 (vocabulaire `status:`), R4 (parité CI), R5 (revue A2 indépendante).

### Dépendances détectées

- `tools/vbb_run_resolution.py` — `run_identity_datetime()` fournit l'ordre par
  identité dont dépend la borne cutoff.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` — définit le cutoff `2026-07-28_1400`.
- R5 (acteur A2 distinct) reste bloquant pour la certification, pas pour ce run.

## 6. Contraintes normatives imposées à ce run

Ces quatre contraintes sont des conditions d'acceptance, pas des intentions.

1. **Aucune écriture dans un bloc adverse avant arrêt de la matrice.**
   La matrice de disposition est un artefact livrable en soi (`02_DISPOSITION_MATRIX.md`),
   soumis à validation humaine avant tout run d'exécution.

2. **Reconstructibilité conditionnée aux artefacts contemporains.**
   Un bloc adverse rétroactif n'est autorisé que si les artefacts du run lui-même,
   datés du run, contiennent la substance adverse (surfaces explorées, findings,
   identités). Reconstruire un bloc depuis la mémoire, l'inférence ou des artefacts
   postérieurs est interdit. À défaut : `HISTORICAL_NON_RECONSTRUCTIBLE`, enregistré
   comme tel, jamais comme conformité.

3. **Aucune rétrogradation de niveau pour obtenir le vert.**
   `adversarial_level` ne peut être révisé que sur preuve que le niveau initial
   était une erreur de classification au regard de la matrice de criticité §1.2 —
   jamais parce que le niveau déclaré est coûteux à satisfaire. Toute révision
   exige une justification écrite opposable et la trace du niveau d'origine.

4. **Le vert du gate ne vaut pas certification.**
   Les trois lectures sont orthogonales et rapportées séparément :
   conformité actuelle ≠ dette historique acceptée ≠ certification obtenue.
   Aucune ne peut être dérivée d'une autre.

## 7. Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : le run redéfinit ce que mesure un gate bloquant du canon.
  Une erreur de conception ici produit soit un gate contournable (le défaut qu'on
  corrige), soit un gate qui bloque tout travail futur sur une dette historique
  irréparable.

## 8. Voie recommandée

- **Voie** : `STRUCTUREE`
- **Adversarial level** : `A2` — travail canon-gating au sens §1.2. L'agent
  exécutant est `claude-opus-5`, même famille que l'auteur de
  `2026-07-29_0840` : `A2_DISTINCT_AGENT_PROXY` **n'est pas satisfait** par ce
  run. L'audit externe reçu le 2026-07-29 constitue l'acteur distinct candidat
  (cf. R5) ; il n'est pas encore enregistré comme `attacker_identity`.

## 9. Handoff vers `04_PLAN`

Le POC conditionne le plan : si le gate étendu ne peut pas être démontré **rouge**
à `6b0daf4`, l'instrument de mesure n'est pas fiable et le run s'arrête avant R1.
