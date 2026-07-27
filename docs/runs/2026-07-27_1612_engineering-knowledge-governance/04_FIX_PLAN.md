---
run_id: "2026-07-27_1612_engineering-knowledge-governance"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "BLOCKED"
agent: "codex"
started_at: "2026-07-27T14:31:00Z"
ended_at: "2026-07-27T14:35:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "03_DECISION.md"
  - "CANON_CHANGE_PROPOSAL.md"
  - "POC.md"
artifacts_produced:
  - "04_FIX_PLAN.md"
---

# 04_FIX_PLAN — Engineering knowledge governance

## Objectif

Intégrer, après validation finale, la seconde boucle de gouvernance avec une
autorité unique, un comportement agentique explicite et des contrôles
rétrocompatibles.

## Pré-conditions

- Revue indépendante de la proposition : `GO`.
- Décision humaine finale : `APPROVED`.
- ADR 0049 : `ACCEPTED`.
- POC : `GO`.
- Integration gate : `CAN_CODE_START=true`.
- Contrôle manuel du POC, obligatoire même si le détecteur lexical retourne
  `POC_REQUIRED=false` :

  ```bash
  rg -n "^\\- \\*\\*Verdict\\*\\*: GO$" \
    docs/runs/2026-07-27_1612_engineering-knowledge-governance/POC.md
  ```

  Exit `0` requis avant toute modification du Core.
- Le run non suivi `2026-07-26_1701_i1-i2-normative-remediation` reste intact.

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|---|---|---|---|
| 1 | Créer l'autorité et le template de connaissance | `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`, `docs/templates/KNOWLEDGE_RECORD.md.template` | Frontières et maturité complètes | Retirer les deux fichiers |
| 2 | Intégrer la boucle dans le Core | `AGENTS.md`, `docs/PILOTAGE.md`, `docs/AGENTIC_RUN_PROTOCOL.md`, `docs/CONVENTIONS.md` | Liens et règles cohérents | Revert atomique |
| 3 | Intégrer les rôles dans les prompts | prompts 02, 03, 06, 07 et template closeout | Tests de contrat documentaire | Revert des prompts/templates |
| 4 | Étendre le routeur existant | `skills/vibebackbone/SKILL.md`, son contrat/index si requis | Contract lint | Revert routeur |
| 5 | Ajouter l'enforcement rétrocompatible | outil(s) et tests ciblés | Historique valide, promotions incomplètes refusées | Désactiver le nouveau contrôle |
| 6 | Mettre à jour l'architecture et la navigation | architecture, relations, guide, index, README | Architecture lint + link checks | Régénérer depuis état précédent |
| 7 | Vérifier les quatre distributions | `docs/DISTRIBUTIONS.md`, smoke tests | Pi/OpenCode/Codex/Claude PASS | Stop avant commit |
| 8 | Revue indépendante, P.R2 et closeout | run artefacts | Tous les gates PASS | Aucun commit si échec |

## Critères d'acceptation

- [ ] Les sept phases restent inchangées.
- [ ] Le Knowledge Harvest est obligatoire mais léger.
- [ ] Aucune promotion sans audit, revue indépendante et décision humaine.
- [ ] Deux validations indépendantes sont évaluées dans le périmètre revendiqué.
- [ ] La fiche de connaissance n'est jamais l'autorité.
- [ ] Une seule autorité finale contient la règle promue.
- [ ] Une connaissance canonique évolue uniquement par nouvelle version.
- [ ] Les patterns et anti-patterns partagent le même cycle.
- [ ] Les runs historiques restent valides.
- [ ] Les quatre distributions héritent du même Core.

## Plan de rollback global

Revert atomiquement l'autorité, les prompts/templates, le routeur, l'enforcement
et les projections documentaires. Ne jamais conserver le Knowledge Harvest sans
le cycle de qualification, ni le cycle sans la règle d'autorité unique.

## Risques identifiés

- Gate trop strict pour les runs historiques : isoler l'enforcement à la
  version effective du nouveau protocole.
- Nouvelle compétence prématurée : réutiliser d'abord les phases existantes.
- Fausse indépendance : rendre le profil d'indépendance obligatoire et revu.
- Règle dupliquée : faire du lien `final_authority` un invariant.

## Analyse d'impact

- **Effectuée ?** : OUI via `t-vbb-impact-analyzer`.
- **Périmètre** : Governance Core, Prompt Library, Architecture Source, Audit
  Memory et quatre distributions.
- **Classification** : `CONDITIONAL`.

## Integration Gate

- **ADR** : `docs/adr/0049-engineering-knowledge-governance.md` — `PROPOSED`.
- **POC** : `POC.md` — `GO`.
- **Gate automatique observé** : `POC_REQUIRED=false`,
  `POC_PRESENT_AND_GO=true`, `ADR_PRESENT_AND_ACCEPTED=false`,
  `CAN_CODE_START=false`,
  blocker `ADR_NOT_ACCEPTED`.
- **Gate manuel POC** : `PASS`, mais ne peut pas lever seul le blocage.
- **CAN_CODE_START** : `NO` jusqu'à revue indépendante et décision humaine.

## Handoff

- **Première action concrète après déblocage** : accepter ADR 0049 et relancer
  `vbb-gate-check.py`, puis exécuter le contrôle manuel POC.
- **Points de vigilance** : aucune exécution Core dans ce run de proposition.
