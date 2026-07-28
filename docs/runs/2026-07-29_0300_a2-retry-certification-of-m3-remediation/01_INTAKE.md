---
run_id: "2026-07-29_0300_a2-retry-certification-of-m3-remediation"
route: AUDIT
phase: "ADVERSARIAL"
voie: "AUDIT"
status: "READY"
kind: "A2_RETRY_CAMPAIGN"
level: "A2"
adversarial_level: "A2"
agent: "A2-retry hostile-falsifier"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
knowledge_harvest: "EVIDENCE_LINKED"
subject_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
parent_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
grandparent_commit: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
adversarial_governance_cutoff: "2026-07-28_1400"
adversarial_governance_cutoff_at: "2026-07-28T14:00:00Z"
remediation_run: "M3"
initial_adversarial_campaign:
  status: "FAIL_ADVERSARIAL"
  audited_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
  findings_count: 14
  findings_s1: 2
  findings_s2: 6
  findings_s3: 6
certification_status_at_start: "NOT_CERTIFIED"
adversarial_status_at_start: "REMEDIATION_COMPLETE_AWAITING_RETEST"
started_at: "2026-07-29T03:00:00Z"
ended_at: "2026-07-29T05:00:00Z"
next_phase: null
proxy_mode: "A2_DISTINCT_AGENT_PROXY"
proxy_limitations:
  - "same LLM family as M3 producer (anthropic) — distinct_llm NOT satisfied by family"
  - "same provider — provider_or_human boundary symbolic"
  - "session distinct from M3 producer"
  - "system_prompt_version distinct"
quarterly_external_review_due: "2026-10-29"
artifacts_consumed:
  - "c4bb4b6 (M3 remediation commit)"
artifacts_produced:
  - "01_INTAKE.md, 02_ADVERSARIAL_CAMPAIGN.md, 03_FINDINGS.md, 04_NON_REGRESSION_LOCK.md, 05_TEST_REPORT.md, 06_INDEPENDENT_REVIEW.md, 07_CLOSEOUT.md (this directory)"
---

# 01_INTAKE — A2-RETRY Certification après M3

## Mission

Campagne A2 falsification stricte du commit `c4bb4b63` (M3 remédiation
des findings de la première campagne A2 sur `ab21d9a`).

L'attaquant ne doit **pas** simplement vérifier que les 59 tests M3
passent. Il doit tenter de découvrir :

- des corrections incomplètes ;
- des contournements ;
- des régressions introduites par M3 ;
- des contradictions entre contrats, templates, outils et tests ;
- de nouveaux chemins fail-open ;
- des limites non déclarées par M3.

## Identités (M1-02 / M3-02)

### defender_identity (producteur M3)

```yaml
defender_identity:
  agent: "M3 producer (subagent codegen, session id 2026-07-29_0100)"
  llm: "anthropic/claude-sonnet-4"
  provider: "anthropic"
  system_prompt_version: "vibebackbone-m3-remediation-context-2026-07-29-01"
  session: "m3-remediation-session-2026-07-29T0100Z-c4bb4b6"
```

### attacker_identity (A2-retry)

```yaml
attacker_identity:
  agent: "A2-retry campaign — this session"
  llm: "anthropic/claude-sonnet-4"
  provider: "anthropic"
  system_prompt_version: "vibebackbone-a2-retry-hostile-falsifier-2026-07-29-03"
  session: "a2-retry-campaign-2026-07-29T0300Z-c4bb4b6"
```

### proxy_mode

```yaml
proxy_mode: A2_DISTINCT_AGENT_PROXY
proxy_limitations:
  - same LLM family (anthropic) — `distinct_llm` MANDATORY NOT satisfied
    by family comparison; mechanical PASS depends on distinct_system_prompt
    AND declared provider boundary
  - same provider — boundary is symbolic; relies on session/prompt separation
  - quarterly_external_review_due: 2026-10-29 (within 90 days of 2026-07-29)
```

**Justification contractuelle** : M1-02 accepte l'usage du même LLM si
les 3 dimensions mécaniques sont établies (distinct_session +
distinct_system_prompt + declared_provider_or_human boundary).
`check_a2_distinct_identity` du validateur exige
`distinct_llm (family)` ET `distinct_system_prompt` ET
`provider_or_human`. **L'attaquant ne satisfera donc pas**
`distinct_llm` au niveau famille → tout closeout A2-retry qui
déclarerait ce couple d'identités au validateur **échouera
mécaniquement** sur le gate `adv-a2-distinct`.

C'est attendu et conforme au contrat : un PASS A2 authentique exige un
vrai acteur distinct (humain différent ou LLM différent). Ce A2-retry
ne peut donc PAS se décerner PASS_ADVERSARIAL en l'état — il doit
soit (a) déclarer un échec mécanique honnête, soit (b) constater que
le validateur refuse de tels couples (ce qui EST le comportement
recherché).

## Engagements

- Aucune correction.
- Aucun commit.
- Aucun push.
- Modification des fichiers canoniques **interdite**.
- Seuls les artefacts du run A2-retry peuvent être créés.
- Vérifier immutabilité de `c4bb4b63`, `ab21d9a7`, `921a780c` à
  chaque jalon.

## Périmètre

### Dans le périmètre

- Code M3 (`tools/vbb-adversarial-gate.py`)
- Canon M3 (`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`,
  `docs/GATE_ASSURANCE_GOVERNANCE.md` §5.3.0)
- Templates M3 (`docs/templates/07_CLOSEOUT.md.template`)
- Distributions M3 (`distributions/codex/setup.sh`,
  `distributions/opencode/setup.sh`)
- Tests M3 (12 fichiers ajoutés)

### Hors périmètre (rappel)

- `distributions/claude/setup.sh`
- `docs/DISTRIBUTIONS.md`
- Tests de distribution
- `CLAUDE-SKILLS-DISCOVERY-01` (DEFERRED)

### Exclus explicitement

- `docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap/` (campagne historique immuable)
- `docs/runs/2026-07-29_0100_m3-remediation-of-a2-findings/` (M3 clos)
- Modification de `01_INTAKE.md` des runs antérieurs

## Méthodologie d'attaque

1. **Rejeu M3-01..M3-12** : pour chaque item, reproduire l'attaque
   initiale + créer ≥1 variante hostile nouvelle (pas une réplique du
   test M3).
2. **6 axes obligatoires** :
   3.1 Lecteur YAML adversarial — clés dupliquées, ancres, listes,
      plusieurs blocs, contradiction, etc.
   3.2 Identités A2 — toutes les variantes de cosmétique vs fond.
   3.3 Temporalité — dates fixes (90 jours ± 1s, future, leap-year,
      timezone, etc.).
   3.4 Compatibilité v1.0/v1.1 — documents hybrides + version future.
   3.5 Certification globale fail-closed — combinaison de gates.
   3.6 Tests et mirages — analyse statique des tests M3 (réimpl.,
      fixtures simplistes, assertions chaînes seulement, etc.).
3. **Mutations temporaires** : si nécessaire, muter le validateur dans
   un fichier temporaire (hors repo), démontrer que le test M3
   échouerait, restaurer, vérifier.
4. **Limites déclarées par M3** : monitor, finding records, ancien
   closeout.
5. **Propagation** : comparer canon/template/prompt/skill/outils/tests
   sur les champs obligatoires.

## Structure des livrables

1. `01_INTAKE.md` — ce fichier (identité, scope, méthodologie).
2. `02_ADVERSARIAL_CAMPAIGN.md` — plan d'attaque détaillé + matrice
   M3-01..M3-12.
3. `03_FINDINGS.md` — findings découverts.
4. `04_NON_REGRESSION_LOCK.md` — vérifications des locks M3.
5. `05_TEST_REPORT.md` — exécution des tests et preuves.
6. `06_INDEPENDENT_REVIEW.md` — auto-revue par acteur distinct.
7. `07_CLOSEOUT.md` — verdict final + FINAL_STATUS.

## Critères de verdict

- **PASS_ADVERSARIAL** : impossible ici (proxy_mode = même LLM,
  distinct_llm non satisfait au niveau famille) — donc le verdict
  attendu est un constat technique honnête.
- Si le validateur **rejette** correctement le couple déclaré →
  comportement attendu → pas de finding.
- Si le validateur **accepte** un couple indûment → S0 finding.
- Si un nouveau fail-open est découvert → S0/S1 finding.
- Si une régression M3 est confirmée → S1+ finding.

## Vérification pré-campagne

```bash
$ git rev-parse HEAD
c4bb4b63b1e59e67d92acead1371ca6a95cf002a  ✅

$ git status --short
?? docs/runs/2026-07-26_1701_i1-i2-normative-remediation/  (untracked)
?? docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap/  (untracked)
?? docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/  (untracked)
?? docs/runs/2026-07-29_0100_m3-remediation-of-a2-findings/  (untracked)
?? docs/runs/2026-07-29_0300_a2-retry-certification-of-m3-remediation/  (untracked, NEW)

$ git log --oneline -3
c4bb4b6 fix(adversarial): remediate first A2 certification findings
ab21d9a feat(adversarial): deploy v1.1 operational integration
921a780 feat(adversarial): bootstrap assurance governance v1.1
```