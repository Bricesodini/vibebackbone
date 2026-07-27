---
run_id: "2026-07-27_2117_design-certification-gates-governance-audit"
phase: "04_RECOMMENDATION"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-27T19:21:46Z"
ended_at: "2026-07-27T19:35:55Z"
revised_at: "2026-07-27T19:35:55Z"
next_phase: "05_IMPACT_ANALYSIS"
artifacts_consumed:
  - "02_ANALYSIS.md"
  - "03_OPTIONS.md"
artifacts_produced:
  - "04_RECOMMENDATION.md"
---

# 04_RECOMMENDATION — Additive assurance dimensions

## Recommandation

**Recommander une évolution de gouvernance, mais uniquement selon l'Option C :
qualification additive des gates et états d'assurance orthogonaux.**

Ne pas remplacer `FAIL`, ne pas créer de phase 08 et ne pas faire du Knowledge
Harvest un gate de conception.

## Modèle conceptuel recommandé

Trois questions indépendantes :

1. **Design assurance** — le comportement observable est-il fermé ?
2. **Documentation certification** — la cohérence, la traçabilité et les
   preuves requises sont-elles certifiées pour ce checkpoint ?
3. **Implementation authorization** — toutes les préconditions applicables
   autorisent-elles explicitement l'exécution ?

La troisième question n'est pas la conjonction implicite des deux premières.
Elle inclut les autres gates applicables : décision humaine, MVP readiness,
ADR, POC, sécurité, intégrité ou mode.

## Projection recommandée à côté de `FINAL_STATUS`

Ne pas utiliser trois booléens nus : `false` ne distingue pas échec, absence de
revue et non-applicabilité. Conserver le bloc runtime canonique sans lui donner
autorité sur le domaine. Ajouter un bloc frère versionné et possédé par le
profil de gate :

```yaml
FINAL_STATUS:
  verdict: COMPLETE
  # champs runtime canoniques inchangés

ASSURANCE_STATUS:
  schema_version: "1.0"
  results:
    - gate_id: "design-contract-closure"
      family: "DESIGN"
      checkpoint: "PRE_IMPLEMENTATION"
      subject: "observable-behavior"
      verdict: "PASS"
    - gate_id: "documentary-readiness"
      family: "CERTIFICATION"
      checkpoint: "PRE_IMPLEMENTATION"
      subject: "design-dossier"
      verdict: "PASS"
    - gate_id: "delivery-evidence"
      family: "CERTIFICATION"
      checkpoint: "POST_IMPLEMENTATION"
      subject: "delivery-evidence"
      verdict: "FAIL"
  implementation_authorization:
    state: "NOT_AUTHORIZED"
    reasons:
      - "final-delivery certification incomplete"
```

Pour satisfaire les besoins de lecture humaine, les projections suivantes
peuvent être exposées dans les rapports ou dashboards :

```yaml
design_certified: true
documentation_certified: false
implementation_authorized: false
```

Elles restent des projections dérivées, jamais la source canonique, car elles
perdent `NOT_ASSESSED`, `NOT_APPLICABLE` et `UNKNOWN`.

`FINAL_STATUS` appartient au runtime. `ASSURANCE_STATUS` appartient au profil
de gate. Aucune inférence de `FINAL_STATUS.verdict: COMPLETE` vers un PASS de
domaine n'est autorisée. Aucun `legacy_verdict` ambigu n'est proposé : pendant
la compatibilité, le verdict historique conserve son propriétaire et les
nouvelles projections déclarent leur règle de dérivation dans le futur ADR de
schéma.

## Multiplicité et agrégation

- Les résultats sont identifiés et append-only; un résultat
  `PRE_IMPLEMENTATION` ne peut pas être écrasé par un résultat
  `POST_IMPLEMENTATION`.
- L'agrégat est calculé par `checkpoint` et par liste de gates requis.
- Un checkpoint est `FAIL` si au moins un gate requis échoue,
  `NOT_ASSESSED` si un requis manque, `PASS` si tous passent et
  `NOT_APPLICABLE` uniquement sur déclaration du profil.
- Il n'existe pas d'agrégat de certification universel entre checkpoints.

## Règles normatives candidates pour le futur run

1. Tout résultat de gate déclare son `gate_family`.
2. `FAIL` qualifie le gate local, pas la stabilité globale du produit.
3. Un écart documentaire qui affecte le comportement observable est reclassé
   en Design et rouvre le Design Gate.
4. Un écart de preuve, oracle, référence ou traçabilité reste Certification
   lorsque le comportement demeure non ambigu.
5. `implementation_authorization` est explicite, fail-closed et accompagné de
   raisons.
6. Le verdict historique reste présent pendant la période de compatibilité.
7. Les runs antérieurs au cutoff du futur protocole ne sont ni réécrits ni
   réinterprétés comme non conformes.
8. Le Knowledge Harvest reste un contrôle de closeout; sa boucle de promotion
   reste autonome.

## Politique de closeout

| Situation | Design | Certification concernée | Autorisation | `kind` du run |
|---|---|---|---|---|
| Certification pré-implémentation FAIL | Design PASS préservé | `PRE_IMPLEMENTATION: FAIL` | `NOT_AUTHORIZED` | `HANDOFF` tant que la remédiation est requise |
| Certification finale FAIL après implémentation | Design PASS préservé sauf reclassification substantive | `POST_IMPLEMENTATION: FAIL` | n'annule pas l'exécution passée | `HANDOFF`; livraison non certifiée |
| Knowledge Harvest absent | Design inchangé | closeout contract incomplet | aucune inférence | pas de closeout final; `HANDOFF` jusqu'à disposition |
| Tous gates de closeout requis PASS | état Design courant | checkpoint final PASS | selon gate explicite | `CLOSEOUT` si aucun autre point critique n'est ouvert |

Un FAIL de certification n'est donc jamais masqué par un `CLOSEOUT`, mais il
ne réécrit pas non plus le Design PASS. Si le finding change le comportement
observable, il est d'abord reclassé Design.

## Checklists indépendantes

Créer deux profils de review dans la phase 06, pas deux phases :

- `DESIGN_REVIEW`: fermeture et cohérence du comportement;
- `CERTIFICATION_REVIEW`: qualité et traçabilité de la preuve.

Le reviewer doit rendre deux verdicts si les deux profils sont exécutés. Un
verdict ne peut pas être déduit de l'autre.

## Conditions avant tout changement

Un run distinct devra :

1. produire une proposition de changement canonique;
2. inventorier tous les producteurs et consommateurs de verdicts;
3. décider et accepter un ADR de schéma;
4. réaliser un POC de lecture legacy + lecture enrichie;
5. définir la projection du verdict global;
6. tester les historiques sans réécriture;
7. analyser et vérifier la propagation Pi/OpenCode/Codex/Claude;
8. obtenir une revue indépendante et une décision humaine.

Le futur ADR doit décider la localisation durable exacte de
`ASSURANCE_STATUS`. L'exemple ci-dessus fixe seulement les propriétaires et
l'orthogonalité requis; il n'est pas un schéma canonique implémenté.

## Décision de ce run

Ce document recommande; il n'accepte pas la modification. L'implémentation
reste interdite dans ce run.
