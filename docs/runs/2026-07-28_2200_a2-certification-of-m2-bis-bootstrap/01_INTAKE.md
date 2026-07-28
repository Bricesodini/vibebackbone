---
run_id: "2026-07-28_2200_a2-certification-of-m2-bis-bootstrap"
phase: "01_INTAKE"
voie: "AUDIT"
status: "ACTIVE"
kind: "ADVERSARIAL_REVIEW"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
linked_subject:
  schema: "git-commit-range"
  range: "921a780ccf8299bc37099b377ce4e7d0d8ba2561^..ab21d9a70f03789c623893b200024f9876b7991b"
  commit_1_sha: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
  commit_1_subject: "feat(adversarial): bootstrap assurance governance v1.1"
  commit_2_sha: "ab21d9a70f03789c623893b200024f9876b7991b"
  commit_2_subject: "feat(adversarial): deploy v1.1 operational integration"
  frozen_head: "ab21d9a70f03789c623893b200024f9876b7991b"
agent: "external attacker (A2 distinct agent proxy)"
started_at: "2026-07-28T22:00:00Z"
ended_at: null
next_phase: "02_AUDIT"
artifacts_consumed:
  - "subject: v1.1 evolution (commit range 921a780..ab21d9a)"
  - "source normatives: M1_DECISIONS.md (M1-01..M1-06), R1 03_DECISION.md (REM-01..REM-10)"
  - "canon: docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md, docs/GATE_ASSURANCE_GOVERNANCE.md, ADR 0051"
  - "validators: tools/vbb-loop-closure-check.py, tools/vbb-adversarial-gate.py"
  - "tests: 51 NEW test cases attached to validators/bootstrap"
  - "templates: 5 (2 NEW + 3 extended)"
  - "skills: 4 (2 NEW + 2 extended)"
  - "prompts: 4 (extended)"
  - "distributions: 5 (4 canonical + DISTRIBUTIONS.md)"
  - "run evidence: docs/runs/2026-07-28_{1002,1200,1400,1600,1800,2000}/"
artifacts_produced:
  - "01_INTAKE.md"
  - "attacker_identity disclosed below"
---

# 01_INTAKE — A2 CERTIFICATION CAMPAIGN

## Mission

Attaquer et falsifier le sujet livré (l'intégralité de l'évolution
Vibe Backbone v1.1 figée par les deux commits locaux). Mission
de falsification, **PAS de confirmation**.

## Sujet livré (linked)

```yaml
linked_subject:
  schema: "git-commit-range"
  commit_1_sha: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
  commit_1_subject: "feat(adversarial): bootstrap assurance governance v1.1"
  commit_2_sha: "ab21d9a70f03789c623893b200024f9876b7991b"
  commit_2_subject: "feat(adversarial): deploy v1.1 operational integration"
  frozen_head: "ab21d9a70f03789c623893b200024f9876b7991b"
  parent_of_head: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
```

## Niveau

```yaml
adversarial_level: A2
```

La gouvernance canonique, les prompts, les skills, les templates,
les validateurs et les distributions ne sont pas éligibles à A0.

## Identité publiée de l'attaquant (M1-02)

```yaml
attacker_identity:
  agent: "external attacker (A2 distinct agent proxy via subagent + fresh context)"
  llm: "minimax/MiniMax-M3"
  provider: "minimax"
  system_prompt_version: "attack-falsifier-v1 (independent of M2-BIS producer)"
  session: "fresh-context subagent (no memory of M2-BIS producer session)"
  proxy_mode: "A2_DISTINCT_AGENT_PROXY (per ADR 0051 §1.4 + M1-02)"
  proxy_limitations:
    - "model: same LLM as producer (no provider-level override available in environment)"
    - "system prompt: explicitly distinct (attack-falsifier focus vs M2-BIS implementer focus)"
    - "session: fresh context (no inherited memory)"
    - "quarterly_external_review: required per M1-02 (downshift A2→A1 prohibited)"
  quarterly_external_review_commitment:
    due: "2026-10-28"
    method: "different LLM family or human reviewer"
    consequence_if_breached: "automatic SUSPENDED transition per M1-04 SLA"
```

**Transparence sur la limite proxy** : le LLM utilisé est le même
que le producteur M2-BIS (limitation d'environnement). Le proxy
est augmenté par :

1. **System prompt distinct** — focalisé sur l'attaque, non sur
   l'implémentation.
2. **Context fresh** — aucune mémoire héritée du producteur.
3. **Quarterly external review** — engagement daté.

Conformément à M1-02, l'A2_DISTINCT_AGENT_PROXY est fail-closed
vers la prudence : un défaut de distinction n'autorise **pas** un
downshift A2→A1 ; au contraire, il impose la revue trimestrielle
externe. Cette contrainte est tracée.

## Surface auditée

L'attaquant peut librement explorer :

- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (NEW, 569 lignes)
- `docs/adr/0051-adversarial-assurance-dimension.md` (NEW, 236 lignes)
- `docs/GATE_ASSURANCE_GOVERNANCE.md` (étendu, Schema 1.1)
- `docs/AGENTIC_RUN_PROTOCOL.md`, `docs/CONVENTIONS.md`,
  `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`, `docs/PILOTAGE.md`,
  `docs/REFERENCE/pre-merge-gate.md` (canon étendu)
- `tools/vbb-loop-closure-check.py` (étendu v1.1)
- `tools/vbb-adversarial-gate.py` (NEW, 975 lignes)
- 12 fichiers de tests (51 NEW cases + 1 count adjustment)
- 5 templates (2 NEW + 3 étendus)
- 4 skills (2 NEW + 2 étendus)
- 4 prompts (étendus)
- 5 fichiers distributions
- `docs/DISTRIBUTIONS.md` §Decisions log
- 6 run evidence directories sous `docs/runs/2026-07-28_*`

## Axes d'attaque obligatoires

| # | Axe | Objectif |
|---|---|---|
| 1 | Bootstrap et statuts | PRE_CERTIFICATION permanence, MIGRATION circumvention, statut sans preuves, transitions contradictoires, v1.0 reinterpretation |
| 2 | Validateurs | exit codes, entrées absentes/inconnues/mal typées, combinaisons incohérentes, preuves manquantes, fail-open, sortie humaine vs JSON, v1.0 reader sur v1.1, dates/timezones, fichiers malveillants, erreurs partielles |
| 3 | Certification | 13 conditions (obtenir CERTIFIED sans toutes), SHA linkage, post-audit divergence, corpus incomplet, witnessed_by/test_review, A2 indépendance, owner/cadence invalide, S0/S1 findings non fermés |
| 4 | Compatibilité ascendante | v1.0 valides, v1.0 incomplets, v1.1 valides, v1.1 incomplets, hybrides, inconnus/futurs, dégradation silencieuse vers OTHER interdite |
| 5 | Propagation | règles identiques dans canon/templates/prompts/skills/distributions/validators/tests ; divergences de vocabulaire, énumérations, seuils, statuts, fail-closed |
| 6 | Mirage de tests | branches non testées, tests réimplémentant le code, fixtures trop favorables, assertions superficielles, chemins d'erreur non exercés, validateurs sur exemples canoniques uniquement |

## Posture

Mission de falsification. Le succès de la campagne est mesuré par
le nombre de findings valides découverts, **PAS** par la confirmation
que tout va bien. Si aucun finding bloquant n'est trouvé, le
verdict sera `PASS_ADVERSARIAL` ; si findings bloquants confirmés,
le verdict sera `FAIL_ADVERSARIAL`.

## Phases à exécuter

1. **01_INTAKE.md** ✅ (ce fichier)
2. **02_AUDIT.md** : exécution axe par axe, avec preuves
3. **03_FINDINGS.md** : liste stable des findings (id, sévérité,
   reproduction, preuve, impact, code concerné, classification,
   test fails-before)
4. **06_INDEPENDENT_REVIEW.md** : revue de la campagne par un
   autre acteur
5. **07_CLOSEOUT.md** : verdict, conditions de certification,
   autorisation de push

## Engagement

Aucun commit correctif ne sera effectué pendant la campagne
initiale. Toute correction ultérieure passe par `closure_evaluation`,
sans réécriture de l'agrégation initiale.