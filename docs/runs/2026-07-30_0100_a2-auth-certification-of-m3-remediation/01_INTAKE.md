---
run_id: "2026-07-30_0100_a2-auth-certification-of-m3-remediation"
phase: "01_INTAKE"
voie: "AUDIT"
status: "READY"
kind: "A2_AUTH_INTAKE"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "minimax/MiniMax-M3 (authentic A2 distinct attacker)"
started_at: "2026-07-30T01:00:00Z"
ended_at: "2026-07-30T01:30:00Z"
next_phase: "02_IDENTITY_PREFLIGHT"
artifacts_produced:
  - "01_INTAKE.md (this file)"
artifacts_consumed:
  - "01_INTAKE.md"
---

# 01_INTAKE — A2-AUTH Authentic Certification Campaign

## 1. Objectif

Déterminer si le commit M3 de remédiation peut recevoir :

- `adversarial_status = PASS_ADVERSARIAL`
- `certification_status = CERTIFIED`

**Sujet de certification** :

```yaml
audited_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
parent_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
grandparent_commit: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
adversarial_level: A2
```

## 2. Indépendance

Cette campagne utilise deux familles LLM **réellement distinctes**.

```yaml
defender_identity:
  agent: "anthropic primary implementer (M3 producer)"
  llm: "anthropic/claude-sonnet-4-5"
  provider: "anthropic"
  system_prompt_version: "defender-M3-producer-v1"
  session: "M3 session 2026-07-29_0100"

attacker_identity:
  agent: "minimax/MiniMax-M3 (authentic distinct attacker)"
  llm: "minimax/MiniMax-M3"
  provider: "minimax"
  system_prompt_version: "a2-auth-attacker-v1"
  session: "A2-AUTH session 2026-07-30_0100 (fresh context)"
```

**Preuves d'indépendance** :

| Critère M1-02 | defender | attacker | Status |
|---|---|---|---|
| llm family | `anthropic` | `minimax` | ✅ DISTINCT |
| system_prompt_version | `defender-M3-producer-v1` | `a2-auth-attacker-v1` | ✅ DISTINCT |
| provider | `anthropic` | `minimax` | ✅ DISTINCT |
| session | M3 producer session | fresh A2-AUTH session | ✅ DISTINCT |
| agent | M3 implementer | authentic A2 attacker | ✅ DISTINCT |

Le validator `vbb-adversarial-gate.py` considère ces deux identités comme
**mécaniquement distinctes** (familles LLM différentes).

## 3. Baseline Git (immuable pendant la campagne)

```yaml
expected_head: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
required_commits_intact:
  - "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
  - "ab21d9a70f03789c623893b200024f9876b7991b"
  - "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
```

**Vérification effectuée** : voir `02_IDENTITY_PREFLIGHT.md` §3.

## 4. Périmètre d'attaque

| Surface | Statut |
|---|---|
| `tools/vbb-adversarial-gate.py` | IN_SCOPE |
| `tools/vbb-loop-closure-check.py` | IN_SCOPE |
| `tools/vbb-credentials-gate.py` | IN_SCOPE |
| `tools/vbb-architecture.py` | IN_SCOPE |
| `tools/vbb-contract-lint.py` | IN_SCOPE |
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | IN_SCOPE |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | IN_SCOPE |
| `docs/adr/0051-adversarial-assurance-dimension.md` | IN_SCOPE |
| `docs/AGENTIC_RUN_PROTOCOL.md` | IN_SCOPE |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | IN_SCOPE |
| `docs/PILOTAGE.md` | IN_SCOPE |
| `docs/CONVENTIONS.md` | IN_SCOPE |
| `docs/REFERENCE/pre-merge-gate.md` | IN_SCOPE |
| 5 tests M3-* ajoutés (test_adversarial_gate_yaml_unwrap, test_a2_distinct_identity, etc.) | IN_SCOPE |
| 12 tests M3-* ajoutés | IN_SCOPE |
| **Exclusions** | |
| `distributions/claude/setup.sh` | OUT_OF_SCOPE |
| `docs/DISTRIBUTIONS.md` | OUT_OF_SCOPE |
| Claude Skills tests | OUT_OF_SCOPE |
| `CLAUDE-SKILLS-DISCOVERY-01` | DEFERRED |

## 5. Méthodologie

L'attaquant authentique va :

1. Examiner personnellement les axes d'attaque (5.1–5.3 du brief)
2. Vérifier que le corpus existant est pertinent
3. Sélectionner ou rejouer les attaques importantes
4. **Ajouter des variantes s'il identifie un angle non couvert**
5. Ne PAS simplement signer le verdict précédent (A2-retry)

La mission est **falsification**, jamais confirmation.

## 6. Engagements

- ✅ Aucune correction pendant la campagne
- ✅ Aucun commit, aucun push
- ✅ Aucune modification des canoniques / contrats / tests
- ✅ Seuls les artefacts du nouveau run peuvent être créés
- ✅ 7 livrables dans ce répertoire
- ✅ Vérifications finales complètes

## 7. Livrables prévus

1. `01_INTAKE.md` (ce fichier)
2. `02_IDENTITY_PREFLIGHT.md` — préflight vbb-adversarial-gate.py
3. `03_ADVERSARIAL_REVIEW.md` — exécution axes 5.1–5.3
4. `04_M3_LOCK_REVIEW.md` — matrice 12 locks
5. `05_FINDING_DISPOSITION.md` — examen 3 S3
6. `06_INDEPENDENT_REVIEW.md` — checklist indépendant
7. `07_CLOSEOUT.md` — FINAL_STATUS + adversarial: block

## 8. Risques acceptés

- Échec d'adv-a2-distinct (improbable : familles distinctes) → arrêt immédiat
- Découverte de fail-open pendant la campagne → FAIL_ADVERSARIAL
- 3 S3 findings requalifiés en S2 → escalade vers R3
- Découverte de régression M3 → escalade M4
