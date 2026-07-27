---
run_id: "2026-07-27_2117_design-certification-gates-governance-audit"
phase: "05_IMPACT_ANALYSIS"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-27T19:21:46Z"
ended_at: "2026-07-27T19:35:55Z"
revised_at: "2026-07-27T19:35:55Z"
next_phase: "06_INDEPENDENT_REVIEW"
artifacts_consumed:
  - "02_ANALYSIS.md"
  - "03_OPTIONS.md"
  - "04_RECOMMENDATION.md"
artifacts_produced:
  - "05_IMPACT_ANALYSIS.md"
---

# 05_IMPACT_ANALYSIS — Additive gate taxonomy

## Classification

- **Impact conceptuel**: structural.
- **Impact proposé sur le schéma**: additive et versionnée.
- **Compatibilité visée**: non-breaking.
- **État**: recommandation seulement; aucune surface listée n'est modifiée.

## Bénéfices

- Distingue immédiatement « comportement non spécifié » de « preuve non
  certifiée ».
- Réduit les faux signaux d'instabilité dans dashboards et handoffs.
- Rend les corrections plus ciblées : retour Design ou remédiation
  Certification.
- Améliore la qualité des revues indépendantes et la traçabilité.
- Préserve l'orthogonalité d'ADR 0043 et l'autorisation fail-closed.
- Permet de mesurer séparément progression de conception et dette de preuve.

## Risques et mitigations

| ID | Priorité | Risque consolidé | Décision | Mitigation requise |
|---|---|---|---|---|
| DGCG-01 | P1 | Un défaut substantif découvert dans un document est mal classé Certification et le Design reste faussement PASS. | MITIGATE | Règle obligatoire de reclassification selon l'objet affecté. |
| DGCG-02 | P1 | `implementation_authorized` est inféré de deux PASS et contourne d'autres gates. | MITIGATE | Décision explicite, fail-closed, raisons et liste de préconditions. |
| DGCG-03 | P1 | Remplacement du verdict casse parseurs et historiques. | AVOID | Extension versionnée; verdict legacy conservé; aucun rewrite. |
| DGCG-04 | P2 | Multiplication des champs crée des états contradictoires. | MITIGATE | Schéma, invariants de cohérence et linter contractuel. |
| DGCG-05 | P2 | Deux checklists augmentent le coût de review. | MITIGATE | Profils proportionnels au scope; une session indépendante peut produire deux verdicts séparés. |
| DGCG-06 | P2 | Le Harvest devient un troisième gate pré-implémentation. | AVOID | Maintien dans le closeout; boucle knowledge autonome. |
| DGCG-07 | P2 | Les interfaces continuent d'afficher le verdict legacy seul. | MITIGATE | Adoption progressive et affichage prioritaire des dimensions lorsqu'elles existent. |
| DGCG-08 | P3 | Consommateurs externes inconnus. | DEFER | Fenêtre de dépréciation; fallback; documentation de version. |

## Impact sur les autorités Core

Un futur run positif devrait examiner, sans présumer tous les changements :

| Surface | Impact potentiel |
|---|---|
| `AGENTS.md` | Règle critique de sémantique des gates si retenue comme canon transverse. |
| `docs/PILOTAGE.md` | Taxonomie, escalade et projection vers autorisation. |
| `docs/AGENTIC_RUN_PROTOCOL.md` | États d'assurance orthogonaux dans les sept phases. |
| `docs/ARCHITECTURE.md` | Source structurée des nouvelles relations; régénération de `RELATIONS.md`. |
| `docs/CONVENTIONS.md` | Seulement si une règle qualité canonique change; CCP et validation humaine obligatoires. |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | Clarification de frontière, sans déplacer le Harvest. |
| `docs/DISTRIBUTIONS.md` | Analyse Core→quatre distributions et entrée au journal de décision. |

Cette liste prouve l'étendue potentielle; elle n'autorise aucun patch.

## Impact sur prompts, templates et outils

### Prompts et templates

- Audit : déclarer famille et dimension affectée par finding.
- Decision/Plan : conserver l'autorisation explicite.
- Review : deux profils de checklist et deux verdicts.
- Closeout : synthèse multidimensionnelle, Harvest inchangé.
- Statut d'assurance : bloc frère versionné, runtime `FINAL_STATUS` inchangé.

### Outils candidats à l'inventaire futur

- `vbb-gate-check.py` : producteur d'autorisation, sans déduction implicite.
- `vbb-loop-closure-check.py` : accepter legacy et schéma enrichi.
- dashboard : afficher dimensions avant le verdict agrégé.
- executor/contrats/lints : valider les invariants du bloc.
- tests : corpus historique, nouveau schéma, contradictions et
  non-applicabilité.

## Compatibilité vérifiée

La compatibilité a été vérifiée pour tous les producteurs et consommateurs
supportés présents dans ce dépôt; voir
[`COMPATIBILITY_EVIDENCE.md`](COMPATIBILITY_EVIDENCE.md). Le corpus externe
non publié reste un UNKNOWN borné et ne fait pas partie du support observable.

La stratégie reste non-breaking sous les conditions suivantes :

1. Aucun champ actuel n'est supprimé ou renommé.
2. Le bloc frère `ASSURANCE_STATUS` est absent des runs historiques.
3. Les futurs readers utilisent le bloc enrichi lorsqu'il existe, sinon le verdict
   legacy.
4. Un cutoff de protocole futur rend les champs obligatoires uniquement pour
   les nouveaux artefacts concernés.
5. Les runs terminés restent valides sous leur version d'origine.
6. Aucun ancien `FAIL` n'est rétroactivement reclassé sans preuve.
7. La migration des projets actifs se fait à leur prochain gate, pas par
   réécriture historique.

Les contrôles ont confirmé que le seul reader Core structuré de
`FINAL_STATUS`, `vbb-loop-closure-check.py`, ignore les blocs frères et champs
inconnus; le dashboard ne consomme pas ce bloc; aucun adapter de distribution
ne le parse; le linter conserve l'interdiction de `verdict_mapping`. Le futur
run devra transformer cette compatibilité observée en tests de régression
permanents avant activation.

## Projets existants et terminés

- **Terminés**: aucune action; affichage `legacy aggregate` si nécessaire.
- **Actifs au moment du cutoff**: choix explicite de finir sous l'ancien
  contrat ou d'adopter le nouveau à un checkpoint documenté; jamais de mélange
  silencieux dans le même gate.
- **Nouveaux**: schéma enrichi obligatoire après activation canonique.
- **Backbone Know**: non modifié et non requalifié par ce run.

## Revues indépendantes

Impact positif attendu : le reviewer peut approuver le Design tout en refusant
la Certification, ou rouvrir le Design avec un motif explicite. Risque :
fragmentation des responsabilités. Mitigation : même phase 06, profils
distincts, artefact unique autorisé mais verdicts séparés.

## Closeouts

Le closeout ne doit plus réduire tous les résultats à une seule impression de
stabilité. Il synthétise :

- verdict runtime du worker;
- état Design;
- état Certification;
- autorisation et raisons;
- risques résiduels;
- disposition Knowledge Harvest.

Politique déterministe :

| Gate non satisfait | Effet closeout |
|---|---|
| Certification `PRE_IMPLEMENTATION` | `HANDOFF`, implémentation non autorisée; Design PASS préservé |
| Certification `POST_IMPLEMENTATION` | `HANDOFF`, livraison non certifiée; Design PASS préservé sauf reclassification |
| Knowledge Harvest absent | contrat de closeout incomplet, donc `HANDOFF` |
| Tous gates finaux requis satisfaits | `CLOSEOUT` possible si aucun autre point critique |

## `FINAL_STATUS`

Le champ canonique `FINAL_STATUS.verdict` reste le statut runtime défini par
ADR 0043 et `PILOTAGE.md`. Un bloc frère `ASSURANCE_STATUS`, dont le futur ADR
doit fixer la localisation exacte, porte les conclusions du sujet. Il n'existe
aucune conversion implicite entre les deux et aucun `legacy_verdict` nouveau.

## Propagation aux distributions

La règle est générique et doit donc être promue au Core si elle est acceptée.
Pi, OpenCode, Codex et Claude doivent être examinés dans le futur run :

- consommation des prompts/templates Core;
- parseurs ou renderers de statut;
- tests smoke de setup et de résolution;
- absence de logique provider-specific copiée.

L'analyse actuelle ne trouve aucune raison de créer quatre variantes
normatives.

## Consolidation des risques

Le registre DGCG-01 à DGCG-08 consolide tous les findings de ce run. Aucun P0
n'est identifié. DGCG-01 à DGCG-03 sont les conditions bloquantes d'une future
implémentation; ils ne bloquent pas la présente recommandation.

## Verdict d'impact

**READY sous conditions** — l'option additive est compatible avec les
producteurs, readers, historiques et distributions supportés visibles. Le
futur run doit figer le schéma et convertir les vérifications ponctuelles en
tests de non-régression. Les consommateurs externes non publiés restent
explicitement hors preuve.
