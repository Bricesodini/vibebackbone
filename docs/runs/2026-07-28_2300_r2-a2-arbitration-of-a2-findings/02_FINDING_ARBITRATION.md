---
run_id: "2026-07-28_2300_r2-a2-arbitration-of-a2-findings"
phase: "02_FINDING_ARBITRATION"
voie: "AUDIT"
status: "ACTIVE"
kind: "NORMATIVE_ARBITRATION_DECISION"
posture: "qualify without correcting"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
linked_subject:
  audited_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
  baseline_parent: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
  adversarial_verdict: "FAIL_ADVERSARIAL"
  checkpoint_aggregation: "0 S0 + 2 S1 + 6 S2 + 6 S3"
agent: "external arbitrator (distinct session, fresh context, distinct LLM family)"
artifacts_consumed:
  - "01_INTAKE.md (this run)"
  - "docs/runs/2026-07-28_2200_.../{01_INTAKE,02_AUDIT,03_DECISION,07_CLOSEOUT}.md"
  - "docs/runs/2026-07-28_1200/.../M1_DECISIONS.md"
  - "docs/runs/2026-07-28_1800/.../03_DECISION.md"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/adr/0051-adversarial-assurance-dimension.md"
  - "tools/vbb-adversarial-gate.py"
  - "docs/templates/{01_INTAKE,07_CLOSEOUT}.md.template"
  - "tests/test_a2_proxy.py, tests/test_attacker_identity_disclosure.py, tests/test_gate_check_level.py, tests/test_prompt_language.py, tests/test_backward_compat_v1_0.py"
artifacts_produced:
  - "02_FINDING_ARBITRATION.md"
---

# 02_FINDING_ARBITRATION — Qualification formelle des 14 findings A2

> **Posture.** R2 qualifie, M3 corrige. R2 n'applique aucune
> correction. R2 ne dévie pas de M1 (M1-01..M1-06). R2 ne crée
> pas de commit. R2 n'invente pas de nouveau contrat d'A2
> indépendance.

## 0. Méthodologie

Pour chaque finding, R2 documente :

1. **Proposition initiale de l'attaquant** — l'assertion A2 telle
   que publiée dans `02_AUDIT.md` de la campagne A2.
2. **Textes canoniques concernés** — pointeurs vers le canon
   (ADR 0051, ADVERSARIAL_ASSURANCE, GATE_ASSURANCE, M1_DECISIONS).
3. **Comportement observé** — reproduction minimale documentée.
4. **Décision R2** — qualification primaire (et secondaire si
   nécessaire).
5. **Sévérité confirmée ou révisée** — R2 peut réviser au vu
   du canon.
6. **Impact réel** — au-delà de la qualification de l'attaquant.
7. **Bloquant pour la certification** — oui/non selon le brief.
8. **Destination de remédiation** — M3_CODE, M3_TEST, M3_TEMPLATE,
   M3_DOCUMENTATION, M3_NORMATIVE_MINIMAL, FUTURE_RUN, NO_CHANGE.
9. **Test fails-before attendu** — pour chaque finding confirmé.

## 1. ADVR-A2-14 (S1) — Validator self-bug : `read_yaml_block` ne déballe pas la clé `adversarial:`

### Proposition initiale de l'attaquant

> `tools/vbb-adversarial-gate.py` lignes 215-237 : la condition
> `if not isinstance(adv, dict)` est inversée. `read_yaml_block("adversarial")`
> retourne `{"adversarial": {"level": "A2", ...}}` (le bloc YAML
> commence par `adversarial:`) ; `adv` EST un dict, donc la
> condition est False, donc le déballage est ignoré. Les champs
> internes (`level`, `campaign_ref`, etc.) sont inaccessibles.
> **Le validateur est non-fonctionnel pour les v1.1 runs.**

### Textes canoniques concernés

- `tools/vbb-adversarial-gate.py` lignes 215-237 (`check_adversarial_block`).
- `tools/vbb-adversarial-gate.py` lignes 169-183 (`read_yaml_block`).
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.1 (énumérations
  v1.1 ; définit `adversarial:` comme bloc racine).
- `docs/templates/07_CLOSEOUT.md.template` (champ
  `adversarial:` en première ligne — c'est le format canonique).
- ADR 0051 §Schema 1.1.

### Comportement observé

```python
# tools/vbb-adversarial-gate.py:218
adv, adv_err = read_yaml_block(closeout_text, "adversarial")
# adv == {"adversarial": {"level": "A2", ...}}   ← dict

# tools/vbb-adversarial-gate.py:232
if not isinstance(adv, dict):   # ← False (adv IS a dict)
    adv = adv.get("adversarial")  # ← skipped

# tools/vbb-adversarial-gate.py:268
level = str(adv.get("level", "")).strip()  # ← returns ""
# → "level must be in ['A0', 'A1', 'A2']"  →  FAIL
```

Reproduction confirmée :
```bash
$ python tools/vbb-adversarial-gate.py docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap
verdict: FAIL — passes=2 fails=8 (S0=0 S1=4 S2=4)
```

Le bloc `adversarial:` est trouvé (PASS `adv-block-exists`) mais
les champs internes ne sont pas accessibles (FAIL `adv-level-valid`,
`adv-surfaces-declared`, etc.).

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| Le comportement est-il reproductible sur le commit audité ? | **Oui** — `HEAD == ab21d9a` produit le bug à chaque exécution. |
| Le template canonique produit-il une structure imbriquée ? | **Oui** — `docs/templates/07_CLOSEOUT.md.template` ligne 81 commence par `adversarial:` (le format canonique est `nested`). |
| Le validateur échoue fermé, échoue ouvert ou devient inopérant ? | **Inopérant** — il ne retourne pas faux résultat ; il échoue à *lire* le bloc. La quasi-totalité des checks structurels basculent en FAIL même sur un closeout valide. |
| Les tests actuels couvrent-ils la structure produite par les templates ? | **Non** — `tests/test_a2_proxy.py` et `tests/test_attacker_identity_disclosure.py` lisent le canon et les templates comme des fichiers texte ; aucun n'exécute `vbb-adversarial-gate.py` sur un fixture canonique. |
| Le défaut rend-il l'ensemble de `vbb-adversarial-gate.py` non-fonctionnel ou seulement un chemin d'entrée ? | **L'ensemble est non-fonctionnel pour les closesout v1.1** — c'est le seul chemin d'entrée (les checks `adversarial:*` sont au cœur de la certification). |
| Classification : BUG_IMPLEMENTATION, BUG_NORMATIF, ou combinaison avec COUVERTURE_DE_TEST_INSUFFISANTE ? | **BUG_IMPLEMENTATION (primaire) + COUVERTURE_DE_TEST_INSUFFISANTE (secondaire)** — le code ne fait pas ce qu'il prétend faire, et aucun test ne l'aurait détecté. |

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `BUG_IMPLEMENTATION` |
| **Qualification secondaire** | `COUVERTURE_DE_TEST_INSUFFISANTE` |
| **Sévérité** | S1 (confirmée) — le validateur est le mécanisme de certification v1.1 ; un validateur inopérant bloque toute certification. |
| **Impact réel** | `vbb-adversarial-gate.py` retourne FAIL sur tout closeout v1.1 conforme. Sans correctif, le mécanisme de certification A2 ne peut pas être validé mécaniquement. |
| **Bloquant pour la certification** | **OUI** |
| **Destination de remédiation** | `M3_CODE` (fix de la condition inversée) + `M3_TEST` (fails-before tests obligatoires ci-dessous) |
| **Test fails-before attendu** | A. Test sur bloc imbriqué ; B. Test sur bloc déjà déballé (si format autorisé) ; C. Test interdisant une réussite silencieuse ; D. Test de cohérence texte/JSON/exit. Détails §A. |

### Fails-before tests obligatoires (M3)

```python
# A. Test sur bloc imbriqué (format canonique)
def test_adversarial_gate_parses_nested_adversarial_block(tmp_path):
    """vbb-adversarial-gate.py must extract fields from a YAML block
    whose first line is `adversarial:` (the canonical v1.1 structure)."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  attacker_identity:
    agent: "x"
    llm: "different-from-defender"
    system_prompt_version: "v1"
```
```''')
    result = validate_run(tmp_path)
    # FAILS-BEFORE: because validator can't unwrap nested block,
    # passes < 8 expected. FAILS-AFTER: passes >= 8.
    assert result["verdict"] in ("PASS", "FAIL")
    assert any(g.gate_id == "adv-level-valid" and g.verdict == "PASS"
               for g in result["gates"]["passes"])


# B. Test sur bloc déjà déballé (format pré-v1.1 hypothétique)
def test_adversarial_gate_handles_unwrapped_block_format(tmp_path):
    """If a v1.0 block (level/campaign_ref at root, no adversarial: key)
    is encountered, the validator must accept it OR fail loudly — never
    silently pass with missing fields."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
```
```''')
    result = validate_run(tmp_path)
    # The validator must EITHER accept (because nested unwrap works)
    # OR fail with a clear "unwrapped block not supported" message.
    # FAILS-BEFORE: silent FAIL on valid block.
    assert len(result["gates"]["passes"]) >= 7


# C. Test interdisant une réussite silencieuse
def test_adversarial_gate_no_silent_pass_on_missing_fields(tmp_path):
    """If adversarial fields are missing, validator must FAIL, not
    silently pass."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  # campaign_ref missing
  # corpus_version missing
```
```''')
    result = validate_run(tmp_path)
    fails = result["gates"]["fails"]
    assert any("campaign_ref" in g.subject for g in fails)


# D. Test de cohérence texte/JSON/exit
def test_adversarial_gate_consistency_text_json_exit(tmp_path):
    """The validator's exit code, JSON verdict, and human-readable
    summary must be coherent."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
```
```''')
    # FAILS-BEFORE: exit code 1, JSON verdict FAIL, text says FAIL — coherent but wrong.
    # FAILS-AFTER: exit code 1, JSON says CORRECTLY PASS, text says PASS — coherent and right.
    rc, json_result = run_validator_json(tmp_path)
    text = run_validator_text(tmp_path)
    assert rc == 0 if json_result["verdict"] == "PASS" else rc != 0
    assert ("PASS" in text) == (json_result["verdict"] == "PASS")
```

---

## 2. ADVR-A2-01 (S1) — A2_DISTINCT_AGENT_PROXY non mécaniquement validé

### Proposition initiale de l'attaquant

> `tools/vbb-adversarial-gate.py` valide la **présence** des
> champs `attacker_identity.{agent, llm, system_prompt_version}`,
> mais ne vérifie pas que le `llm` est effectivement distinct
> du modèle du défenseur. Un attaquant peut donc prétendre à
> un LLM distinct en écrivant n'importe quelle chaîne.

### Textes canoniques concernés

- `tools/vbb-adversarial-gate.py` lignes 307-340 (validation
  `attacker_identity`).
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §3 (`A2_DISTINCT_AGENT_PROXY`).
- `docs/runs/2026-07-28_1200/.../M1_DECISIONS.md` M1-02 (Option D).
- ADR 0051 §1.4.

### Comportement observé

```python
# tools/vbb-adversarial-gate.py:307-340
identity = adv.get("attacker_identity")
if not isinstance(identity, dict):
    # FAIL
required = ("agent", "llm", "system_prompt_version")
missing = [k for k in required if not non_empty_string(identity.get(k))]
if missing:
    # FAIL
```

Le validateur vérifie les 3 champs comme strings non-vides. Il
**ne vérifie pas** :
1. Que `identity.llm` ≠ `defender.llm`.
2. Que `identity.llm` est une **family** distincte
   (M1-02 §Argumentation 4 : *« different llm family OR
   human »*).
3. Que `identity.provider` est cohérent avec `identity.llm`.
4. Que `identity.system_prompt_version` est distinct du
   system_prompt du producteur.
5. Qu'il existe un `defender_identity` comparable.

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| Quelles propriétés de distinction peuvent être vérifiées mécaniquement ? | (a) `attacker_identity.llm` ≠ `defender_identity.llm` (string equality) ; (b) `attacker_identity.llm` diffère par `family` (regex sur préfixe, ex. `minimax/...` vs `anthropic/...`) ; (c) `attacker_identity.system_prompt_version` ≠ `defender_identity.system_prompt_version` (string) ; (d) `attacker_identity.provider` ≠ `defender_identity.provider` (string) ; (e) `attacker_identity.session` ≠ `defender_session` (string). |
| Quelles propriétés doivent rester déclaratives ? | (a) La qualité de la *falsification* (l'attaquant a-t-il bien essayé de prouver le négatif) ; (b) le caractère distinct de l'**agent** (un même LLM peut être utilisé par deux agents distincts). |
| M1-02 exige-t-il une différence de agent, de llm, de provider, de system_prompt_version, de session, ou d'une combinaison ? | **Combinaison** — M1-02 §Argumentation 4 dit *« different llm family OR human »* mais §Contrat formel exige `distinct_llm: MANDATORY` **et** `distinct_system_prompt: MANDATORY`. La combinaison canonique est : `agent` (distinct par construction via session A2) **+** `llm` (distinct family) **+** `system_prompt_version` (distinct, non dérivé) **+** une des deux options : `provider` distinct ou `human` externe. |
| Comment traiter le cas actuel où le proxy déclare « same LLM as producer » ? | Cas actuel de la campagne A2 : `proxy_limitations: ["same LLM as producer"]`. C'est une **transgression directe** de M1-02 §Contrat (`distinct_llm: MANDATORY`). La campagne actuelle doit être marquée comme **non-conforme à M1-02 stricto sensu** et l'engagement `quarterly_external_review` doit être activé **avant** tout constat PASS. |
| `A2_DISTINCT_AGENT_PROXY` est-il valide avec même LLM mais autre agent, autre prompt, session fraîche ? | **Non** au sens strict M1-02. Pour A2, le contrat exige `distinct_llm + distinct_system_prompt`. La présente campagne a satisfait `distinct_system_prompt` (attack-falsifier-v1 ≠ implementer-v1) et `session` (fresh context) mais **PAS** `distinct_llm` (même provider). Ce cas est explicitement traité par M1-02 comme **engageant le quarterly_external_review** : ce n'est pas une autorisation permanente, c'est une dérogation traçable. |
| Le validateur doit-il comparer l'identité de l'attaquant à une identité explicite du producteur ? | **Oui** — pour les 4 propriétés mécaniques (a)-(d). Un `defender_identity` doit être déclaré ailleurs (par exemple dans `attacker_identity.attacker_vs_defender.compares_to: {llm, provider, system_prompt_version, session}`). |
| L'absence d'identité du producteur doit-elle provoquer un INVALID_EVIDENCE, un FAIL_ADVERSARIAL, ou un autre résultat ? | **FAIL_ADVERSARIAL** au sens canonical M1-02 + R1 §4 : l'absence de comparaison mécanique est une non-conformité au contrat. Le verdict de la campagne A2 actuelle doit explicitement refléter cette non-conformité. |

### Note de limite

R2 n'invente pas de nouveau contrat. R2 observe que M1-02
exige `distinct_llm: MANDATORY` et que le validateur ne l'applique
**pas**. La classification est donc `CONTRAT_INCOMPLET` (le
contrat est complet ; le validateur ne l'applique pas
mécaniquement) — et non `BUG_NORMATIF` (qui impliquerait une
violation du contrat).

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `CONTRAT_INCOMPLET` |
| **Qualification secondaire** | `COUVERTURE_DE_TEST_INSUFFISANTE` (les tests existants `test_a2_proxy.py` et `test_attacker_identity_disclosure.py` ne vérifient que la *présence* des 3 champs) |
| **Sévérité** | S1 (confirmée) — l'exigence M1-02 n'est pas appliquée. |
| **Impact réel** | La présente campagne A2 — qui se déclare elle-même `proxy_limitations: ["same LLM as producer"]` — peut passer `vbb-adversarial-gate.py` sans déclencher le contrat `distinct_llm`. La règle est désamorcée. |
| **Bloquant pour la certification** | **OUI** |
| **Destination de remédiation** | `M3_CODE` (validateur doit comparer `attacker_identity.llm` à une `defender_identity.llm` déclarée) + `M3_TEST` (fails-before : `same LLM` doit FAIL) + `M3_TEMPLATE` (template 07_CLOSEOUT doit exposer un `defender_identity` comparable) |
| **Test fails-before attendu** | Voir §A. |

### Fails-before tests obligatoires (M3)

```python
def test_adversarial_gate_rejects_identical_attacker_and_defender_llm(tmp_path):
    """vbb-adversarial-gate.py must FAIL when attacker_identity.llm
    equals defender_identity.llm (M1-02 + A2_DISTINCT_AGENT_PROXY)."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  attacker_identity:
    agent: "external attacker"
    llm: "minimax/MiniMax-M3"
    provider: "minimax"
    system_prompt_version: "attack-falsifier-v1"
  defender_identity:
    llm: "minimax/MiniMax-M3"   # ← SAME as attacker
    provider: "minimax"
    system_prompt_version: "implementer-v1"
```
```''')
    result = validate_run(tmp_path)
    fails = result["gates"]["fails"]
    # FAILS-BEFORE: cannot detect (no mechanical check).
    # FAILS-AFTER: at least one FAIL with subject mentioning "distinct_llm" or "M1-02".
    assert any("distinct_llm" in g.subject.lower() or "M1-02" in g.subject
               for g in fails)


def test_adversarial_gate_accepts_distinct_llm(tmp_path):
    """vbb-adversarial-gate.py must PASS when attacker_identity.llm
    differs from defender_identity.llm by family."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  attacker_identity:
    agent: "external attacker"
    llm: "anthropic/claude-3-5-sonnet"
    provider: "anthropic"
    system_prompt_version: "attack-falsifier-v1"
  defender_identity:
    llm: "minimax/MiniMax-M3"
    provider: "minimax"
    system_prompt_version: "implementer-v1"
```
```''')
    result = validate_run(tmp_path)
    assert any(g.gate_id == "adv-a2-identity" and g.verdict == "PASS"
               for g in result["gates"]["passes"])
```

---

## 3. ADVR-A2-02 (S2) — `level_reason` documenté dans templates mais absent du canon

### Proposition initiale de l'attaquant

> `docs/templates/01_INTAKE.md.template:71` et
> `docs/templates/07_CLOSEOUT.md.template:88` documentent
> `level_reason` comme requis pour A0. Le canon
> `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` ne contient aucune
> occurrence de ce champ.

### Textes canoniques concernés

- `docs/templates/01_INTAKE.md.template` ligne 71.
- `docs/templates/07_CLOSEOUT.md.template` ligne 88.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (recherche : 0 occurrence).
- `tools/vbb-adversarial-gate.py` lignes 280-300 (validation
  `level == "A0"` requires `level_reason`).

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| Le champ est-il normatif ? | **Oui** au sens du validateur : `vbb-adversarial-gate.py` ligne 285 *« level_reason must be non-empty for A0 »* — gate_id `adv-a0-reason`, sévérité S1. Donc mécaniquement normatif. |
| Est-il seulement documentaire ? | Non — il est validé par le validateur. |
| Doit-il être validé ? | **Oui** — la validation S1 est cohérente avec l'esprit A0 (justifier explicitement l'absence d'audit). |
| Doit-il être supprimé des templates lors de M3 ? | **Non** — il doit au contraire être **ajouté au canon** (§3 ou §A0 du `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`). |

### Comportement observé

```bash
$ grep -n "level_reason" docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md
(no output)

$ grep -n "level_reason" docs/templates/01_INTAKE.md.template
71:  level_reason: "<human-readable reason; required for A0>"

$ grep -n "level_reason" docs/templates/07_CLOSEOUT.md.template
88:  level_reason: "<required when level=A0>"
```

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `CONTRADICTION_DOCUMENTAIRE` |
| **Sévérité** | S2 (confirmée) — divergence entre canon (silence) et templates (requis), couplée à une validation validateur (S1). |
| **Impact réel** | Un lecteur lisant uniquement le canon (`ADVERSARIAL_ASSURANCE_GOVERNANCE.md`) ne saura pas que `level_reason` est un champ requis ; un rédacteur de closeout A0 suivant strictement le canon produira un closeout invalide que le validateur rejettera S1. |
| **Bloquant pour la certification** | **Non** au sens A2 (le cas A0 n'est pas le sujet de cette campagne). **Mais** les futures campagnes A0 seront cassées tant que le canon ne le déclarera pas. |
| **Destination de remédiation** | `M3_DOCUMENTATION` (ajouter `level_reason` au canon §3 ou §A0) + `M3_NORMATIVE_MINIMAL` (déclarer le champ comme obligatoire pour A0 dans `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`). |
| **Test fails-before attendu** | A. Test que le canon contient `level_reason`. |

### Fails-before tests obligatoires (M3)

```python
def test_canon_documents_level_reason_for_a0():
    """The canon ADVERSARIAL_ASSURANCE_GOVERNANCE.md must declare
    the `level_reason` field requirement for A0 (matches templates)."""
    canon = (REPO / "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text()
    assert "level_reason" in canon, \
        "level_reason is documented in templates but absent from canon"
```

---

## 4. ADVR-A2-05 (S2) — `intake_text` lue puis déréférencée (chemin mort)

### Proposition initiale de l'attaquant

> `tools/vbb-adversarial-gate.py:885-887` lit `01_INTAKE.md`
> puis déréfère `intake_text` sans l'utiliser. La lecture
> crée une latence disque inutile et un faux sentiment de
> validation intake-side.

### Textes canoniques concernés

- `tools/vbb-adversarial-gate.py` lignes 882-887 (`validate_run`).
- `docs/AGENTIC_RUN_PROTOCOL.md` §Phases (01_INTAKE obligatoire).

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| Code mort (dette bénigne) ou bug d'implémentation ? | **Bug d'implémentation + indice de validation manquante**. Le code lit intentionnellement `01_INTAKE.md` (sinon il ne le ferait pas) puis déréfère. La présence de la lecture + le fait qu'aucun check ne suive indique qu'une **validation intake-side** était prévue mais non livrée (probablement ADVR-26 ou similaire reportée à M2-BIS). |
| Indice d'une validation attendue mais absente ? | **Oui** — la lecture est faite *avant* les checks `closeout`. Cela suggère un flow `intake → checks intake-side → closeout → checks closeout-side` qui n'est pas implémenté. |

### Comportement observé

```python
# tools/vbb-adversarial-gate.py:885-887
intake_text = intake.read_text(encoding="utf-8")
closeout_text = closeout.read_text(encoding="utf-8")
del intake_text  # currently unused; reserved for future intake-side checks
```

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `BUG_IMPLEMENTATION` |
| **Qualification secondaire** | `COUVERTURE_DE_TEST_INSUFFISANTE` |
| **Sévérité** | S2 (confirmée) — chemin mort mais avec intention sous-jacente. |
| **Impact réel** | Le validateur ne valide **pas** le bloc `adversarial:` éventuel dans `01_INTAKE.md`. Si un attaquant muait `01_INTAKE.md` (par exemple en injectant un `attacker_identity` falsifié), le validateur ne le détecterait pas. |
| **Bloquant pour la certification** | **Non** au sens A2 (l'attacker_identity est aussi dans `07_CLOSEOUT.md`). **Mais** incohérence sémantique : la cohérence entre intake et closeout n'est pas garantie. |
| **Destination de remédiation** | `M3_CODE` (soit supprimer la lecture, soit implémenter les checks intake-side) + `M3_TEST` (test cohérence intake ↔ closeout). |
| **Test fails-before attendu** | A. Test que la mutation de `01_INTAKE.md` est détectée. |

### Fails-before tests obligatoires (M3)

```python
def test_adversarial_gate_validates_intake_adversarial_block(tmp_path):
    """vbb-adversarial-gate.py must validate the intake-side adversarial
    block, not just the closeout-side one. Or remove the dead read."""
    intake = tmp_path / "01_INTAKE.md"
    intake.write_text('''
```yaml
adversarial:
  level: "A2"
  attacker_identity:
    agent: "FAKE_external"
    llm: "minimax/MiniMax-M3"
    system_prompt_version: "attack-falsifier-v1"
```
```''')
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  attacker_identity:
    agent: "external attacker"
    llm: "minimax/MiniMax-M3"
    system_prompt_version: "attack-falsifier-v1"
```
```''')
    result = validate_run(tmp_path)
    # FAILS-BEFORE: validator ignores intake; FAILS-AFTER: validator detects divergence.
    fails = result["gates"]["fails"]
    assert any("intake" in g.subject.lower() and "divergence" in g.subject.lower()
               for g in fails)
```

---

## 5. ADVR-A2-07 (S2) — `attacker_identity.session` sans validation de format

### Proposition initiale de l'attaquant

> Le validateur vérifie que `attacker_identity.{agent, llm, system_prompt_version}`
> sont des strings non-vides, mais ne valide PAS que `session`
> est un identifiant (UUID, timestamp, etc.).

### Textes canoniques concernés

- `tools/vbb-adversarial-gate.py` lignes 307-340.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §3 (mentionne
  `session` comme champ de l'identité A2).
- `docs/templates/07_CLOSEOUT.md.template` (le champ `session`
  est documenté).

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| `session` doit-il être une chaîne opaque, un identifiant structuré, une preuve contrôlable, ou uniquement une divulgation ? | **Chaîne opaque avec contraintes minimales** — non-vide, longueur minimale (≥ 8 chars), pas d'espaces internes. R2 ne prescrit pas un format UUID ; UUID, hash, timestamp + counter, ou session-id provider-specific sont tous acceptables. La présomption est que la **divulgation** suffit pour la traçabilité, pas pour la vérifiabilité cryptographique. |

### Comportement observé

```python
# tools/vbb-adversarial-gate.py:322
required = ("agent", "llm", "system_prompt_version")
missing = [k for k in required if not non_empty_string(identity.get(k))]
# session NOT in required → not validated
```

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `BUG_NORMATIF` (la spec canonique — `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §3 — exige que `session` soit divulgué, ce qui implique qu'il ait *un* format vérifiable ; aucune contrainte n'est appliquée) |
| **Sévérité** | S2 (confirmée) — audibilité du `session` est compromise. |
| **Impact réel** | Un attaquant peut passer `session: "x"` sans contrainte ; impossible de tracer la session d'audit. |
| **Bloquant pour la certification** | **Non** (pas S1). |
| **Destination de remédiation** | `M3_CODE` (validateur : ajouter `session` aux `required` ; appliquer contrainte ≥ 8 chars non-whitespace) + `M3_TEST`. |
| **Test fails-before attendu** | A. Test rejet `session: ""` ou `session: "x"` (trop court). |

### Fails-before tests obligatoires (M3)

```python
def test_adversarial_gate_rejects_empty_session(tmp_path):
    """vbb-adversarial-gate.py must FAIL when attacker_identity.session
    is empty or whitespace-only (M1-02 contractual traceability)."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  attacker_identity:
    agent: "external attacker"
    llm: "minimax/MiniMax-M3"
    provider: "minimax"
    system_prompt_version: "attack-falsifier-v1"
    session: ""   # ← EMPTY
```
```''')
    result = validate_run(tmp_path)
    fails = result["gates"]["fails"]
    assert any("session" in g.subject.lower() for g in fails)
```

---

## 6. ADVR-A2-09 (S2) — Pas de test lecteur v1.0 sur données v1.1

### Proposition initiale de l'attaquant

> `tests/test_backward_compat_v1_0.py` existe mais ne teste
> **pas** ce qui se passe quand un lecteur v1.0 consomme des
> données v1.1. Il teste que le validateur v1.1 accepte des
> données v1.0 valides. La direction inverse (v1.0 reader on
> v1.1 data) n'est pas testée.

### Textes canoniques concernés

- `tests/test_backward_compat_v1_0.py`.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §Schema 1.1
  (compatibilité ascendante).
- `docs/GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1.
- `tools/vbb-loop-closure-check.py` (lecteur v1.0 ; ne
  reconnaît pas `ADVERSARIAL`).

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| Comportement attendu : rejet explicite, statut de migration, lecture partielle clairement signalée, ou interdiction de dégradation silencieuse en OTHER ? | **Rejet explicite** — un lecteur v1.0 face à `gate_family: ADVERSARIAL` ou `checkpoint: COUNTER_PROOF` doit **FAIL** avec un message explicite référençant la version (`UnsupportedSchemaError: reader v1.0 cannot consume v1.1 data`). La compatibilité ascendante (v1.1 consomme v1.0) est préservée ; la lecture inverse (v1.0 consomme v1.1) doit échouer loudly. |
| La compatibilité ascendante ne doit jamais être confondue avec l'acceptation silencieuse de données futures inconnues. | **Confirmé.** Un v1.0 reader qui voit `gate_family: ADVERSARIAL` ne doit pas dégrader silencieusement en `OTHER` ; il doit FAIL. |

### Comportement observé

```bash
$ grep -rn "v1.0_reader\|v10_reader\|downgrade" tests/
(no output)
```

Aucun test ne couvre ce comportement.

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `CONTRAT_INCOMPLET` |
| **Sévérité** | S2 (confirmée) — divergence non testée. |
| **Impact réel** | La garantie « no v1.1 data should be silently degraded to OTHER » n'est pas testée. C'est un risque silencieux. |
| **Bloquant pour la certification** | **Non** (S2). |
| **Destination de remédiation** | `M3_TEST` (ajouter test fails-before) + `M3_DOCUMENTATION` (clarifier dans le canon §Schema 1.1 le comportement fail-closed). |
| **Test fails-before attendu** | A. Test simulant un v1.0 reader sur v1.1 data. |

### Fails-before tests obligatoires (M3)

```python
def test_v10_reader_on_v11_data_does_not_silently_degrade(tmp_path):
    """When a v1.0 reader (closure tool without v1.1 support) consumes
    v1.1 data with gate_family=ADVERSARIAL, it must FAIL loudly, NOT
    silently degrade to OTHER."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  gate_family: "ADVERSARIAL"
  checkpoint: "COUNTER_PROOF"
```
```''')
    # Simulate v1.0 reader by invoking an old closure tool or a v1.0 mock.
    result = simulate_v10_closure_check(tmp_path)
    # FAILS-BEFORE: silently degraded to OTHER (or PASS with no semantic check).
    # FAILS-AFTER: explicit FAIL with "UnsupportedSchemaError" or "v1.0 reader cannot consume v1.1".
    assert result.verdict == "FAIL"
    assert ("UnsupportedSchemaError" in result.errors_text or
            "v1.0 reader" in result.errors_text)
    assert "OTHER" not in result.degraded_to
```

---

## 7. ADVR-A2-10 (S2) — `test_prompt_language.py` modifié seulement pour le count

### Proposition initiale de l'attaquant

> Le test a été modifié uniquement pour passer de `>= 64` à
> `>= 66`. Le test ne valide **PAS** le contenu des skills
> ajoutés.

### Textes canoniques concernés

- `tests/test_prompt_language.py`.
- ADR 0051 §Schema 1.1 (énumérations étendues).
- `skills/2-vbb-adversarial-campaign/SKILL.md` (NEW).
- `skills/t-vbb-adversarial-corpus/SKILL.md` (NEW).

### Comportement observé

```diff
- count_skills = count_skills_in_dir(SKILLS_DIR, language="en")
- assert count_skills >= 64
+ assert count_skills >= 66  # 2 NEW adversarial skills
```

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `COUVERTURE_DE_TEST_INSUFFISANTE` |
| **Sévérité** | S2 (confirmée) — test de superficie. |
| **Impact réel** | Une skill ajoutée avec un frontmatter corrompu ou hors-périmètre passe le test. |
| **Bloquant pour la certification** | **Non** (S2). |
| **Destination de remédiation** | `M3_TEST` (ajouter validation de frontmatter). |
| **Test fails-before attendu** | A. Test validant le frontmatter de chaque skill. |

### Fails-before tests obligatoires (M3)

```python
def test_prompt_language_validates_skill_frontmatter():
    """test_prompt_language.py must validate each skill's frontmatter
    has the required fields (name, description, level if applicable)."""
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = read_frontmatter(skill_md)
        assert "name" in fm, f"{skill_dir.name}: missing 'name'"
        assert "description" in fm, f"{skill_dir.name}: missing 'description'"
        if skill_dir.name.startswith(("2-vbb-", "t-vbb-")):
            # Adversarial and tooling skills must declare their level
            assert "level" in fm or "adversarial_level" in fm, f"{skill_dir.name}: missing level"
```

---

## 8. ADVR-A2-11 (S2) — `test_a2_proxy.py` teste la présence, pas l'indépendance

### Proposition initiale de l'attaquant

> `tests/test_a2_proxy.py` teste la **présence** des champs
> `attacker_identity.{agent, llm, system_prompt_version}`, pas
> leur **différence** réelle.

### Textes canoniques concernés

- `tests/test_a2_proxy.py`.
- `docs/runs/2026-07-28_1200/.../M1_DECISIONS.md` M1-02
  (`distinct_llm: MANDATORY`).
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §3.

### Comportement observé

```python
# tests/test_a2_proxy.py
def test_a2_proxy_contract_in_canon():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "A2_DISTINCT_AGENT_PROXY" in authority
    assert "attacker_identity" in authority
    # Three disclosures
    assert "agent" in authority
    assert "llm" in authority
    assert "system_prompt_version" in authority
    # Quarterly review
    assert "QUARTERLY" in authority
```

Aucun test ne vérifie la *différence* entre l'identité de
l'attaquant et celle d'un défenseur déclaré.

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `COUVERTURE_DE_TEST_INSUFFISANTE` |
| **Sévérité** | S2 (confirmée) — couverture partielle. |
| **Impact réel** | Le test passe si l'attaquant déclare un LLM identique au défenseur. ADVR-A2-01 et ADVR-A2-11 sont liés. |
| **Bloquant pour la certification** | **Non** (S2 — couplé à ADVR-A2-01 S1). |
| **Destination de remédiation** | `M3_TEST` (même set de tests que ADVR-A2-01). |
| **Test fails-before attendu** | Identique à ADVR-A2-01. |

---

## 9. ADVR-A2-03 (S3) — `last_external_review` non mécaniquement validé

### Proposition initiale de l'attaquant

> `docs/templates/07_CLOSEOUT.md.template` documente
> `last_external_review` comme champ obligatoire de la cadence
> (M1-04 SLA). Le validateur `vbb-adversarial-gate.py` ne
> valide pas ce champ.

### Textes canoniques concernés

- `docs/templates/07_CLOSEOUT.md.template` ligne 96.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §7.3 (SLA breach).
- `tools/vbb-adversarial-gate.py` (recherche : 0 occurrence de
  `last_external_review`).

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| Dans quels modes est-il requis ? | **A2 uniquement** (M1-02 §Contrat : `quarterly_external_review` avec `last_external_review` ≤ 90 jours). |
| Format et timezone canoniques ? | **ISO8601 UTC** (cohérent avec `last_reviewed` et `last_external_review` dans `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`). |
| Sa validation relève-t-elle du gate adversarial ou du contrôle de certification owner ? | **Les deux** (séparation assumée) : (a) le gate adversarial valide la **présence** du champ et le **format** ISO8601 ; (b) le contrôle de certification owner valide la **cadence** (≤ 90 jours). |
| Une date future ou trop ancienne doit-elle suspendre la certification ? | **Oui** — date future ⇒ invalide ; date > 90 jours ⇒ `SLA breach` ⇒ `CERTIFIED → SUSPENDED` automatique. |

### Comportement observé

```bash
$ grep -n "last_external_review" tools/vbb-adversarial-gate.py
(no output)
```

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `CONTRAT_INCOMPLET` |
| **Sévérité** | S3 (confirmée) — incomplet mais pas cassant. |
| **Impact réel** | Un run peut prétendre `last_external_review: "2020-01-01"` et passer la validation. |
| **Bloquant pour la certification** | **Non** (S3). |
| **Destination de remédiation** | `M3_CODE` (validateur : valider `last_external_review` ≤ cadence déclarée) + `M3_TEST`. |
| **Test fails-before attendu** | A. Test que `last_external_review > now + 90 days` FAIL. |

### Fails-before tests obligatoires (M3)

```python
def test_adversarial_gate_validates_last_external_review(tmp_path):
    """vbb-adversarial-gate.py must reject a CERTIFIED status when
    last_external_review exceeds cadence (M1-04)."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  attacker_identity:
    agent: "external attacker"
    llm: "anthropic/claude-3-5-sonnet"
    provider: "anthropic"
    system_prompt_version: "v1"
  certification:
    status: "CERTIFIED"
    cadence: "manual:quarterly"
    last_external_review: "2025-01-01"  # > 90 days ago
```
```''')
    result = validate_run(tmp_path)
    fails = result["gates"]["fails"]
    assert any("last_external_review" in g.subject.lower() and
               "cadence" in g.subject.lower() for g in fails)
```

---

## 10. ADVR-A2-04 (S3) — Propagation `gate_family` ADVERSARIAL vérifiée correcte

### Proposition initiale de l'attaquant

> L'énumération canonique `gate_family ∈ {DESIGN, CERTIFICATION,
> ADVERSARIAL, OTHER}` est cohérente entre ADR 0051, GATE_ASSURANCE,
> templates, prompts, skills, distributions, validators, et
> tests. Bonne propagation.

### Textes canoniques concernés

- ADR 0051 §1.
- `docs/GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.1.
- `docs/templates/`, `prompts/`, `skills/`, `distributions/`,
  `tools/`, `tests/`.

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `FAUX_POSITIF` (AXE) — la propagation est correcte. |
| **Sévérité** | S3 (reconfirmée comme nul). |
| **Impact réel** | Aucun. R2 confirme la propagation. |
| **Bloquant pour la certification** | **Non**. |
| **Destination de remédiation** | `NO_CHANGE` — finding nul. |
| **Test fails-before attendu** | **Aucun** (la propagation est correcte ; un test de non-régression est déjà en place via ADVR-FALSIF-03 traité en R1). |

---

## 11. ADVR-A2-06 (S3) — `test_gate_check_level.py` ne couvre que 3 combinaisons

### Proposition initiale de l'attaquant

> `tests/test_gate_check_level.py` n'exécute que 3 tests sur
> les combinaisons de `gate_family × checkpoint`. La matrice
> de couverture est incomplète.

### Textes canoniques concernés

- `tests/test_gate_check_level.py`.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §1.1 (énumérations).
- `tools/vbb-gate-check.py` (validator level fail-closed).

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `COUVERTURE_DE_TEST_INSUFFISANTE` |
| **Sévérité** | S3 (confirmée) — couverture incomplète mais pas cassante. |
| **Impact réel** | Combinaisons invalides (ex. `gate_family: ADVERSARIAL` × `checkpoint: PRE_IMPLEMENTATION`) peuvent passer inaperçues. |
| **Bloquant pour la certification** | **Non** (S3). |
| **Destination de remédiation** | `M3_TEST` (étendre la matrice à au moins 8 combinaisons × 2 verbes = 16 tests). |
| **Test fails-before attendu** | A. Test sur `ADVERSARIAL × PRE_IMPLEMENTATION` doit FAIL. |

### Fails-before tests obligatoires (M3)

```python
def test_gate_family_adversarial_with_pre_implementation_checkpoint():
    """ADVERSARIAL gate family should NOT be paired with
    PRE_IMPLEMENTATION checkpoint (PRE_IMPLEMENTATION is for DESIGN)."""
    result = gate_check_level(family="ADVERSARIAL", checkpoint="PRE_IMPLEMENTATION")
    assert result.verdict == "FAIL"
```

---

## 12. ADVR-A2-08 (S3) — Conditions 6.3.10 et 6.3.11 non mécaniquement validées

### Proposition initiale de l'attaquant

> Le validateur documente `6.3.10 revocation_mechanism declared`
> et `6.3.11 cadence ≤ 90 days` dans la liste des conditions,
> mais le code qui implémente ces validations n'a pas été
> trouvé.

### Textes canoniques concernés

- `tools/vbb-adversarial-gate.py` lignes 116-117 (méta —
  déclaratif, pas implémenté).
- `tools/vbb-adversarial-gate.py` lignes 829-840 (check_certification_status
  pour `CERTIFIED` : passe automatique).
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §5.3 conditions
  6.3.10 + 6.3.11.
- `docs/runs/2026-07-28_1200/.../M1_DECISIONS.md` M1-04.

### Réponse aux questions obligatoires

| Question | Réponse |
|---|---|
| Quelles conditions CERTIFIED doivent être vérifiées par le validateur adversarial ? | 6.3.1, 6.3.2, 6.3.8, 6.3.9, 6.3.13 (champs directement présents dans le closeout). |
| Lesquelles relèvent d'un validateur de certification distinct ? | 6.3.3 (gates agrégées au `CLOSEOUT`), 6.3.4 (résolutions COUNTER_PROOF), 6.3.5 (Harvest disposition), 6.3.6 (ACCEPTED_RISK), 6.3.7 (human decision A2), 6.3.10, 6.3.11, 6.3.12 (état de surveillance owner). |
| L'absence actuelle constitue-t-elle un bug ou une séparation assumée ? | **Séparation assumée** — la conception a placé 6.3.10/11/12 dans le périmètre d'un validateur de state monitoring (potentiellement `vbb-status-dashboard` ou un futur `vbb-certification-monitor`). R2 ne dévie pas. |
| Comment empêcher qu'une certification globale soit émise lorsque la cadence owner dépasse 90 jours ou qu'un trigger de révocation est actif ? | (a) `vbb-status-dashboard` doit produire l'alerte ; (b) `vbb-loop-closure-check` doit produire l'erreur lors d'un passage post-SLA-breach. Aucun de ces deux mechanisms n'est implémenté pour l'instant. |

### Comportement observé

```python
# tools/vbb-adversarial-gate.py:829-840
if status == "CERTIFIED":
    # 13 conditions: we don't validate them mechanically (too
    # context-dependent) but we report them in the evidence.
    passes.append(GateResult(...))
    passes.append(GateResult(...))
```

Le validateur **commente explicitement** qu'il ne valide pas
mécaniquement les 13 conditions. Pour 6.3.10, 6.3.11, 6.3.12,
aucun re-direction vers un autre validateur n'est spécifié.

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `CONTRAT_INCOMPLET` (séparation assumée entre validateurs, mais **non** rédigée) |
| **Sévérité** | S3 (confirmée) — incomplet mais pas cassant. |
| **Impact réel** | Un `CERTIFIED` peut être émis en runtime sans que 6.3.10/11/12 soient surveillées. |
| **Bloquant pour la certification** | **Non** (S3). |
| **Destination de remédiation** | `M3_DOCUMENTATION` (rédiger la séparation des responsabilités entre `vbb-adversarial-gate` et un futur `vbb-certification-monitor`) + `M3_NORMATIVE_MINIMAL` (déclarer 6.3.10/11/12 comme relevant d'un validateur de surveillance distinct). |
| **Test fails-before attendu** | A. Test unitaire mockant 6.3.10/11/12 et vérifiant qu'un CERTIFIED sans `revocation_mechanism` est rejeté. |

### Fails-before tests obligatoires (M3)

```python
def test_certification_monitor_rejects_certified_without_revocation_mechanism(tmp_path):
    """A future vbb-certification-monitor must reject CERTIFIED status
    without revocation_mechanism declared (M1-04)."""
    closeout = tmp_path / "07_CLOSEOUT.md"
    closeout.write_text('''
```yaml
adversarial:
  level: "A2"
  campaign_ref: "test"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared: ["x.py"]
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  certification:
    status: "CERTIFIED"
    # revocation_mechanism missing
    # cadence missing
```
```''')
    result = validate_run(tmp_path)
    fails = result["gates"]["fails"]
    # FAILS-BEFORE: check_certification_status PASSES (no revocation_mechanism check).
    # FAILS-AFTER: at least one FAIL mentions "revocation_mechanism" or "6.3.10".
    assert any("revocation_mechanism" in g.subject.lower() or "6.3.10" in g.subject
               for g in fails)
```

---

## 13. ADVR-A2-12 (S3) — PRE_CERTIFICATION sans expiration mécanique

### Proposition initiale de l'attaquant

> §11.1 du canon définit `PRE_CERTIFICATION` sans imposer de
> durée maximale. Théoriquement, un run peut rester en
> `PRE_CERTIFICATION` indéfiniment.

### Textes canoniques concernés

- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §11.1 (PRE_CERTIFICATION).
- `docs/runs/2026-07-28_1800/.../03_DECISION.md` §3 (Bootstrap
  R1 — R1 a explicitement tranché : la transition
  PRE_CERTIFICATION → CERTIFIED est *pilotée par l'humain*, pas
  par le validateur).

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `CHOIX_ASSUMÉ` (R1 a tranché explicitement : la transition est humaine, pas mécanique) |
| **Sévérité** | S3 (confirmée). |
| **Impact réel** | Aucun pour la certification — la non-expiration est un choix R1. |
| **Bloquant pour la certification** | **Non**. |
| **Destination de remédiation** | `NO_CHANGE` (R1 a tranché). Pour mémoire : un futur run pourra ajouter une alerte owner si PRE_CERTIFICATION demeure > X days, mais c'est une amélioration, pas un correctif. |
| **Test fails-before attendu** | **Aucun** (CHOIX_ASSUMÉ). |

### Note de confirmation

R2 confirme le statut de `ADVR-A2-12` comme `CHOIX_ASSUMÉ` hérité
de R1. **Aucun correctif recommandé**. La mitigation existante
est l'engagement humain + le SLA owner (M1-04 cross-référencé).

---

## 14. ADVR-A2-13 (S3) — `distributions/codex/setup.sh` et `distributions/opencode/setup.sh` non testés

### Proposition initiale de l'attaquant

> Les 4 distributions actives sont censées picker
> automatiquement le Core. Or, le code dans `codex/setup.sh` et
> `opencode/setup.sh` n'a pas été modifié pour intégrer les
> nouveaux champs adversariaux. La propagation automatique
> dépend du mécanisme déjà en place (non vérifié par cette
> campagne).

### Textes canoniques concernés

- `distributions/codex/setup.sh` (non modifié).
- `distributions/opencode/setup.sh` (non modifié).
- `docs/DISTRIBUTIONS.md` §Decisions log.
- `docs/runs/2026-07-28_1200/.../M1_DECISIONS.md` §Critères
  CR#12 (propagation).

### Comportement observé

```bash
$ git diff 75953fc..ab21d9a -- distributions/codex/setup.sh
(no output)

$ git diff 75953fc..ab21d9a -- distributions/opencode/setup.sh
(no output)
```

`distributions/pi/SYSTEM.md` et `distributions/claude/CLAUDE.md`
**ont été** modifiés ; `codex/setup.sh` et `opencode/setup.sh`
**n'ont pas été** modifiés.

### Décision R2

| Dimension | Décision |
|---|---|
| **Qualification primaire** | `CONTRAT_INCOMPLET` |
| **Sévérité** | S3 (confirmée) — la propagation est déclarée CR#12 mais pas mécaniquement testée. |
| **Impact réel** | Si la propagation de `pi/SYSTEM.md` et `claude/CLAUDE.md` vers codex/opencode n'est pas automatique, les distributions codex/opencode ne sauront pas gérer le niveau adversarial. |
| **Bloquant pour la certification** | **Non** (S3). |
| **Destination de remédiation** | `M3_TEST` (test cross-distribution : un test qui vérifie que les 4 distributions réagissent identiquement à un même input adversarial) + `M3_DOCUMENTATION` (clarifier le mécanisme de propagation dans `docs/DISTRIBUTIONS.md`). |
| **Test fails-before attendu** | A. Test hors scope environnement local (skip avec raison). |

### Note de scope

R2 observe que la campagne A2 n'a pas pu exécuter les
distributions codex/opencode (pas d'environnement local). Le
finding reste valide au sens où **la couverture de test est
insuffisante** — c'est un problème de **portabilité**, pas un
défaut de `codex/setup.sh` ou `opencode/setup.sh` *per se*.

---

## 15. Matrice de synthèse

| ID | Sév. A2 | Qual. primaire (A2) | Qual. R2 | Sév. R2 | Bloquant | Destination |
|---|---|---|---|---|---|---|
| ADVR-A2-14 | S1 | BUG_NORMATIF | **BUG_IMPLEMENTATION** + COUVERTURE_DE_TEST_INSUFFISANTE | S1 | OUI | M3_CODE + M3_TEST |
| ADVR-A2-01 | S1 | CONTRAT_INCOMPLET | **CONTRAT_INCOMPLET** + COUVERTURE_DE_TEST_INSUFFISANTE | S1 | OUI | M3_CODE + M3_TEST + M3_TEMPLATE |
| ADVR-A2-02 | S2 | CONTRADICTION_DOCUMENTAIRE | **CONTRADICTION_DOCUMENTAIRE** | S2 | NON | M3_DOCUMENTATION + M3_NORMATIVE_MINIMAL |
| ADVR-A2-05 | S2 | MIRAGE_TEST | **BUG_IMPLEMENTATION** + COUVERTURE_DE_TEST_INSUFFISANTE | S2 | NON | M3_CODE + M3_TEST |
| ADVR-A2-07 | S2 | BUG_NORMATIF | **BUG_NORMATIF** | S2 | NON | M3_CODE + M3_TEST |
| ADVR-A2-09 | S2 | CONTRAT_INCOMPLET | **CONTRAT_INCOMPLET** | S2 | NON | M3_TEST + M3_DOCUMENTATION |
| ADVR-A2-10 | S2 | MIRAGE_TEST | **COUVERTURE_DE_TEST_INSUFFISANTE** | S2 | NON | M3_TEST |
| ADVR-A2-11 | S2 | MIRAGE_TEST | **COUVERTURE_DE_TEST_INSUFFISANTE** | S2 | NON | M3_TEST |
| ADVR-A2-03 | S3 | CONTRAT_INCOMPLET | **CONTRAT_INCOMPLET** | S3 | NON | M3_CODE + M3_TEST |
| ADVR-A2-04 | S3 | CONTRADICTION_DOCUMENTAIRE (nulle) | **FAUX_POSITIF** | S3 | NON | NO_CHANGE |
| ADVR-A2-06 | S3 | MIRAGE_TEST | **COUVERTURE_DE_TEST_INSUFFISANTE** | S3 | NON | M3_TEST |
| ADVR-A2-08 | S3 | CONTRAT_INCOMPLET | **CONTRAT_INCOMPLET** | S3 | NON | M3_DOCUMENTATION + M3_NORMATIVE_MINIMAL |
| ADVR-A2-12 | S3 | CHOIX_ASSUMÉ | **CHOIX_ASSUMÉ** | S3 | NON | NO_CHANGE |
| ADVR-A2-13 | S3 | CONTRAT_INCOMPLET | **CONTRAT_INCOMPLET** | S3 | NON | M3_TEST + M3_DOCUMENTATION |

### Requalifications R2 notables

| ID | A2 a qualifié | R2 qualifie | Raison |
|---|---|---|---|
| ADVR-A2-14 | BUG_NORMATIF | **BUG_IMPLEMENTATION** | C'est un défaut de code (condition inversée), pas une violation normative. |
| ADVR-A2-05 | MIRAGE_TEST | **BUG_IMPLEMENTATION** | Lecture intentionnelle + abandon = code mort qui cache une validation manquante. |
| ADVR-A2-04 | CONTRADICTION_DOCUMENTAIRE (nulle) | **FAUX_POSITIF** | L'attaquant lui-même a reconnu la propagation correcte. |

### Compteurs R2

| Catégorie | Compte |
|---|---|
| BUG_IMPLEMENTATION | 2 (ADVR-A2-14, -05) |
| BUG_NORMATIF | 1 (ADVR-A2-07) |
| CONTRAT_INCOMPLET | 5 (ADVR-A2-01, -03, -08, -09, -13) |
| CONTRADICTION_DOCUMENTAIRE | 1 (ADVR-A2-02) |
| COUVERTURE_DE_TEST_INSUFFISANTE | 4 (ADVR-A2-06, -10, -11, +secondaire) |
| CHOIX_ASSUMÉ | 1 (ADVR-A2-12) |
| FAUX_POSITIF | 1 (ADVR-A2-04) |
| DÉFAUT_DE_MIGRATION | 0 |

### Faux positifs R2

| ID | Détail |
|---|---|
| ADVR-A2-04 | La propagation est correcte ; aucun correctif requis. |

### Bloquants certification

| ID | Bloquant | Justification |
|---|---|---|
| ADVR-A2-14 | **OUI** | Validateur inopérant ⇒ impossible de certifier en v1.1. |
| ADVR-A2-01 | **OUI** | Contrat `distinct_llm` non appliqué ⇒ identité A2 faible. |

### M1 deviations

| ID | M1 dévié ? | Détail |
|---|---|---|
| Aucun | NON | R2 opère strictement à l'intérieur de M1. |
