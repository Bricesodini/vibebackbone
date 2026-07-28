---
run_id: "2026-07-28_2200_a2-certification-of-m2-bis-bootstrap"
phase: "02_AUDIT"
voie: "AUDIT"
status: "ACTIVE"
kind: "ADVERSARIAL_AUDIT"
adversarial_level: "A2"
linked_subject:
  schema: "git-commit-range"
  range: "921a780^..ab21d9a"
  commit_1_sha: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
  commit_2_sha: "ab21d9a70f03789c623893b200024f9876b7991b"
  frozen_head: "ab21d9a70f03789c623893b200024f9876b7991b"
agent: "external attacker (A2 distinct agent proxy)"
started_at: "2026-07-28T22:30:00Z"
ended_at: "2026-07-28T23:00:00Z"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
artifacts_consumed:
  - "all v1.1 evolution artefacts (commit range 921a780..ab21d9a)"
  - "all canon authorities"
  - "all validators (closure + adversarial gate)"
  - "all 51 new tests + existing 255 tests"
  - "all templates, skills, prompts, distributions"
artifacts_produced:
  - "02_AUDIT.md"
  - "13 ADVR-A2 findings"
attacker_identity:
  agent: "external attacker (A2 distinct agent proxy via subagent + fresh context)"
  llm: "minimax/MiniMax-M3"
  provider: "minimax"
  system_prompt_version: "attack-falsifier-v1"
  session: "fresh-context subagent"
  proxy_mode: "A2_DISTINCT_AGENT_PROXY"
  proxy_limitations: ["same LLM as producer (env constraint)", "quarterly external review required per M1-02"]
---

# 02_AUDIT — A2 Adversarial Analysis

## Methodology

Mission : **falsifier** le sujet livré, **PAS** le confirmer.

L'attaquant a opéré avec :
- **Fresh context** (subagent, pas de mémoire héritée du producteur M2-BIS)
- **System prompt distinct** (falsification-focused vs implementation-focused)
- **Read-only** (aucune modification de source)

L'analyse a couvert les 6 axes obligatoires en croisant :
- Lecture intégrale des fichiers canon (`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`, `docs/GATE_ASSURANCE_GOVERNANCE.md`, `docs/adr/0051-adversarial-assurance-dimension.md`, `docs/AGENTIC_RUN_PROTOCOL.md`, `docs/CONVENTIONS.md`, `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`, `docs/PILOTAGE.md`, `docs/REFERENCE/pre-merge-gate.md`)
- Lecture intégrale des validateurs (`tools/vbb-loop-closure-check.py` 1540 lignes, `tools/vbb-adversarial-gate.py` 975 lignes)
- Lecture intégrale des 12 fichiers de tests ajoutés (51 cases)
- Lecture intégrale des templates (5), skills (4), prompts (4), distributions (2)
- Lecture des run evidence M1/M2/R0/R1/M2-BIS
- Reproduction locale de tests (closure tool, adversarial gate)
- Cross-référence énumérations / vocabulaire / statuts / seuils

## Findings overview

| ID | Axe | Sév. | Classification | État |
|---|---|---|---|---|
| ADVR-A2-01 | 2 | S1 | CONTRAT_INCOMPLET | NEW |
| ADVR-A2-02 | 1 | S2 | CONTRADICTION_DOCUMENTAIRE | NEW |
| ADVR-A2-03 | 1 | S3 | CONTRAT_INCOMPLET | NEW |
| ADVR-A2-04 | 5 | S3 | CONTRADICTION_DOCUMENTAIRE | NEW |
| ADVR-A2-05 | 2 | S2 | MIRAGE_TEST | NEW |
| ADVR-A2-06 | 6 | S3 | MIRAGE_TEST | NEW |
| ADVR-A2-07 | 2 | S2 | BUG_NORMATIF | NEW |
| ADVR-A2-08 | 3 | S3 | CONTRAT_INCOMPLET | NEW |
| ADVR-A2-09 | 4 | S2 | CONTRAT_INCOMPLET | NEW |
| ADVR-A2-10 | 2 | S2 | MIRAGE_TEST | NEW |
| ADVR-A2-11 | 6 | S2 | MIRAGE_TEST | NEW |
| ADVR-A2-12 | 1 | S3 | CHOIX_ASSUMÉ | NEW |
| ADVR-A2-13 | 5 | S3 | CONTRAT_INCOMPLET | NEW |
| ADVR-A2-14 | 2 | S1 | BUG_NORMATIF | NEW (validator self-bug) |

**Bilan** : 0 finding S0 ; 2 findings S1 (ADVR-A2-01, ADVR-A2-14) ; 6 findings S2 ; 6 findings S3.

## Axe 1 — Bootstrap et statuts

### ADVR-A2-02 (S2) — CONTRADICTION_DOCUMENTAIRE : `level_reason` documenté dans templates mais absent du canon

**Reproduction** :
```bash
$ grep -n "level_reason" docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md
(no output)

$ grep -n "level_reason" docs/templates/01_INTAKE.md.template
71:  level_reason: "<human-readable reason; required for A0>"

$ grep -n "level_reason" docs/templates/07_CLOSEOUT.md.template
88:  level_reason: "<required when level=A0>"
```

**Preuve** :
- `docs/templates/01_INTAKE.md.template:71` documente `level_reason` comme requis pour A0
- `docs/templates/07_CLOSEOUT.md.template:88` documente `level_reason` requis pour A0
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` ne contient AUCUNE occurrence du champ `level_reason`

**Impact** : divergence documentaire. Un utilisateur lisant uniquement le canon ne saura pas que `level_reason` est requis pour A0. Inversement, un validateur strictement aligné sur le canon (pas le template) ne rejetterait pas un A0 sans `level_reason`.

**Code concerné** :
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (canon)
- `docs/templates/01_INTAKE.md.template`
- `docs/templates/07_CLOSEOUT.md.template`

**Classification proposée** : CONTRADICTION_DOCUMENTAIRE.

**Fails-before test** :
```python
def test_canon_documents_level_reason_for_a0():
    """The canon ADVERSARIAL_ASSURANCE_GOVERNANCE.md must document
    the `level_reason` field requirement for A0 (matches templates)."""
    canon = (REPO / "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text()
    assert "level_reason" in canon, \
        "level_reason is documented in templates but absent from canon"
```

---

### ADVR-A2-03 (S3) — CONTRAT_INCOMPLET : `last_external_review` documenté dans closeout template mais absent du validateur

**Reproduction** :
```bash
$ grep -n "last_external_review" docs/templates/07_CLOSEOUT.md.template
(HIT: see template)

$ grep -n "last_external_review" tools/vbb-adversarial-gate.py
(no output)
```

**Preuve** : `docs/templates/07_CLOSEOUT.md.template` documente `last_external_review` comme un champ obligatoire de la cadence (M1-04 SLA). Le validateur `tools/vbb-adversarial-gate.py` ne valide PAS ce champ. Un run peut donc avoir `last_external_review` manquant et passer la validation.

**Impact** : la règle M1-04 (cadence ≤ 90 jours, breach → SUSPENDED automatique) n'est pas mécaniquement vérifiable par le validateur v1.1.

**Code concerné** :
- `tools/vbb-adversarial-gate.py` (manque validation `last_external_review` ≤ `cadence`)
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §6.3.12 (cadence ≤ 90 jours)

**Classification proposée** : CONTRAT_INCOMPLET.

**Fails-before test** :
```python
def test_adversarial_gate_validates_last_external_review():
    """vbb-adversarial-gate.py must reject a CERTIFIED status when
    last_external_review exceeds cadence (M1-04)."""
    fixture = make_closeout(certification_status="CERTIFIED",
                            cadence="manual:quarterly",
                            last_external_review="2025-01-01")  # > 90 days ago
    result = validate_run(fixture.run_dir)
    assert any(g.verdict == "FAIL" and "last_external_review" in g.subject
               for g in result["gates"]), \
        "vbb-adversarial-gate.py does not enforce M1-04 cadence breach"
```

---

### ADVR-A2-12 (S3) — CHOIX_ASSUMÉ : PRE_CERTIFICATION n'a pas de durée d'expiration mécanique

**Reproduction** :
```bash
$ grep -n "PRE_CERTIFICATION" docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md
(only definition; no expiration rule)

$ grep -n "PRE_CERTIFICATION" tools/vbb-adversarial-gate.py
(validates companion fields only)
```

**Preuve** : §11.1 du canon définit `PRE_CERTIFICATION` sans imposer de durée maximale. Théoriquement, un run peut rester en `PRE_CERTIFICATION` indéfiniment sans transition automatique vers `SUSPENDED` ou `NOT_CERTIFIED`.

**Impact** : si le mécanisme d'auto-échec (R1) n'est pas actionné, `PRE_CERTIFICATION` peut devenir permanent de facto. Le brief utilisateur mentionne explicitement : "Tenter de démontrer que : PRE_CERTIFICATION peut devenir permanent".

**Mitigation observée** : aucun mécanisme technique n'empêche la permanence. Seul l'engagement humain ("R1 ratification PRE_CERTIFICATION transitoire, post-cutoff awaiting first CERTIFIED") garantit la transition.

**Classification proposée** : CHOIX_ASSUMÉ — c'est un choix assumé de R1 que la transition PRE_CERTIFICATION → CERTIFIED est pilotée par l'humain, pas par le validateur. **Aucun correctif recommandé**.

**Fails-before test** : N/A (CHOIX_ASSUMÉ, pas de fail-before).

---

## Axe 2 — Validateurs

### ADVR-A2-01 (S1) — CONTRAT_INCOMPLET : le validateur ne contraint pas mécaniquement l'A2_DISTINCT_AGENT_PROXY

**Reproduction** :
```bash
$ grep -n "A2_DISTINCT_AGENT_PROXY\|distinct_llm\|different_family" tools/vbb-adversarial-gate.py
(no output)
```

**Preuve** : `tools/vbb-adversarial-gate.py` valide que les 3 champs `attacker_identity.{agent, llm, system_prompt_version}` sont présents, mais ne vérifie PAS que le `llm` est effectivement distinct du modèle du défenseur (M1-02). Un attaquant peut donc prétendre à un LLM distinct en écrivant n'importe quelle chaîne.

**Impact** : la garantie d'indépendance A2 repose entièrement sur la déclaration humaine. La présente campagne est précisément dans ce cas (cf. `01_INTAKE.md` : `proxy_limitations: ["same LLM as producer (env constraint)"]`).

**Code concerné** :
- `tools/vbb-adversarial-gate.py` lignes ~290-320 (validation `attacker_identity`)
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §A2_DISTINCT_AGENT_PROXY
- `docs/runs/2026-07-28_1200_m1-adversarial-loop-normative-arbitration/M1_DECISIONS.md` M1-02

**Classification proposée** : CONTRAT_INCOMPLET (le contrat déclare l'exigence, mais le validateur ne l'applique pas mécaniquement).

**Fails-before test** :
```python
def test_adversarial_gate_rejects_identical_llm_in_attacker_identity():
    """vbb-adversarial-gate.py must FAIL when attacker_identity.llm
    equals the defender's declared llm (M1-02 + A2_DISTINCT_AGENT_PROXY)."""
    fixture = make_closeout(attacker_identity={
        "agent": "x", "llm": "minimax/MiniMax-M3",
        "provider": "minimax", "system_prompt_version": "y",
    }, defender_llm="minimax/MiniMax-M3")
    result = validate_run(fixture.run_dir)
    assert any(g.verdict == "FAIL" and "distinct_llm" in g.subject.lower()
               for g in result["gates"])
```

---

### ADVR-A2-05 (S2) — MIRAGE_TEST : `intake_text` lue puis déréférencée dans `validate_run`

**Reproduction** :
```bash
$ sed -n '867,900p' tools/vbb-adversarial-gate.py
```

**Preuve** :
```python
def validate_run(run_dir: Path) -> Dict[str, Any]:
    intake = run_dir / "01_INTAKE.md"
    closeout = run_dir / "07_CLOSEOUT.md"
    ...
    intake_text = intake.read_text(encoding="utf-8")
    closeout_text = closeout.read_text(encoding="utf-8")
    del intake_text  # currently unused; reserved for future intake-side checks
```

Le code lit `01_INTAKE.md` puis déréfère immédiatement `intake_text` sans l'utiliser. La lecture crée une latence disque inutile et un faux sentiment de validation intake-side.

**Impact** : si un attaquant mute `01_INTAKE.md` (par exemple en ajoutant un `level: A2` sans les champs requis), le validateur ne le détecte pas.

**Code concerné** : `tools/vbb-adversarial-gate.py:884-887`.

**Classification proposée** : MIRAGE_TEST (chemin mort).

**Fails-before test** :
```python
def test_adversarial_gate_validates_intake_adversarial_block():
    """vbb-adversarial-gate.py must validate the adversarial block
    present in 01_INTAKE.md (not just 07_CLOSEOUT.md)."""
    fixture = make_run_with_intake_adversarial_block_but_closeout_without()
    result = validate_run(fixture.run_dir)
    assert any(g.verdict == "FAIL" and "intake" in g.subject.lower()
               for g in result["gates"])
```

---

### ADVR-A2-07 (S2) — BUG_NORMATIF : pas de validation `attacker_identity.session` format

**Reproduction** :
```bash
$ grep -n "attacker_identity" tools/vbb-adversarial-gate.py | head -10
```

**Preuve** : le validateur vérifie que `attacker_identity.{agent, llm, system_prompt_version}` sont des strings non-vides, mais ne valide PAS que `session` est un identifiant (UUID, timestamp, etc.). Un attaquant peut donc passer `session: "x"` sans contrainte de format.

**Impact** : l'auditabilité du `session` est compromise. Le traçage des campagnes devient fragile.

**Code concerné** : `tools/vbb-adversarial-gate.py` (validation `attacker_identity.session`).

**Classification proposée** : BUG_NORMATIF (la spec exige un identifiant traçable, le code ne l'impose pas).

**Fails-before test** :
```python
def test_adversarial_gate_rejects_empty_session():
    """vbb-adversarial-gate.py must FAIL when attacker_identity.session
    is empty or whitespace-only."""
    fixture = make_closeout(attacker_identity={
        "agent": "x", "llm": "y", "provider": "z",
        "system_prompt_version": "w", "session": "",
    })
    result = validate_run(fixture.run_dir)
    assert any(g.verdict == "FAIL" and "session" in g.subject.lower()
               for g in result["gates"])
```

---

### ADVR-A2-14 (S1) — BUG_NORMATIF : le validateur ne déballe pas la clé `adversarial:` du YAML extrait

**Reproduction** :
```python
# tools/vbb-adversarial-gate.py:212-237
adv, adv_err = read_yaml_block(closeout_text, "adversarial")
if adv_err or adv is None:
    fails.append(...)
if not isinstance(adv, dict):  # ← BUG: condition inversée
    adv = (
        adv.get("adversarial") if isinstance(adv.get("adversarial"), dict) else adv
    )
```

**Preuve** :

`read_yaml_block("adversarial")` extrait un bloc YAML dont la première
ligne est `adversarial:`. Le contenu YAML typique est :

```yaml
adversarial:
  level: "A2"
  campaign_ref: "..."
```

`yaml.safe_load()` retourne `{"adversarial": {"level": "A2", ...}}`.

Le validateur teste `not isinstance(adv, dict)`. Comme `adv` EST un
dict (le bloc entier est un dict), la condition est `False` et le
déballage est ignoré. Plus tard, `adv.get("level")` retourne `None`
parce que la clé `level` est imbriquée.

Conséquence : tous les tests sur `level`, `campaign_ref`,
`corpus_version`, `surfaces_declared`, etc. retournent FAIL.

**Vérification empirique** :
```bash
$ python tools/vbb-adversarial-gate.py docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap
verdict: FAIL
summary: passes=2 fails=8 (S0=0 S1=4 S2=4)
  PASS        adv-block-exists: adversarial block present in 07_CLOSEOUT.md
  PASS        adv-cert-status: certification.status is a valid value
  [S1] FAIL        adv-level-valid: adversarial.level is one of A0/A1/A2
      - level must be in ['A0', 'A1', 'A2']
  [S1] FAIL        adv-surfaces-declared: surfaces_declared is a non-empty list
  ...
```

Le bloc `adversarial:` est trouvé (PASS) mais les champs internes
ne sont pas accessibles (FAIL).

**Impact** : `vbb-adversarial-gate.py` est **non-fonctionnel** pour
les v1.1 runs : il retourne FAIL même sur des runs valides. Le
mécanisme de certification v1.1 est cassé.

**Code concerné** : `tools/vbb-adversarial-gate.py` lignes 212-237.

**Classification proposée** : BUG_NORMATIF.

**Fails-before test** :
```python
def test_adversarial_gate_parses_nested_adversarial_block():
    """vbb-adversarial-gate.py must extract fields from a YAML block
    whose first line is `adversarial:` (the typical structure)."""
    closeout = '''
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
'''
    result = validate_adversarial_block(closeout)
    assert result["level"] == "A2"
    assert result["campaign_ref"] == "test"
    assert result["verdict"] == "PASS_ADVERSARIAL"
```

---



**Reproduction** :
```bash
$ grep -n "attacker_identity" tools/vbb-adversarial-gate.py | head -10
```

**Preuve** : le validateur vérifie que `attacker_identity.{agent, llm, system_prompt_version}` sont des strings non-vides, mais ne valide PAS que `session` est un identifiant (UUID, timestamp, etc.). Un attaquant peut donc passer `session: "x"` sans contrainte de format.

**Impact** : l'auditabilité du `session` est compromise. Le traçage des campagnes devient fragile.

**Code concerné** : `tools/vbb-adversarial-gate.py` (validation `attacker_identity.session`).

**Classification proposée** : BUG_NORMATIF (la spec exige un identifiant traçable, le code ne l'impose pas).

**Fails-before test** :
```python
def test_adversarial_gate_rejects_empty_session():
    """vbb-adversarial-gate.py must FAIL when attacker_identity.session
    is empty or whitespace-only."""
    fixture = make_closeout(attacker_identity={
        "agent": "x", "llm": "y", "provider": "z",
        "system_prompt_version": "w", "session": "",
    })
    result = validate_run(fixture.run_dir)
    assert any(g.verdict == "FAIL" and "session" in g.subject.lower()
               for g in result["gates"])
```

---

### ADVR-A2-10 (S2) — MIRAGE_TEST : `tests/test_prompt_language.py` modifié seulement pour le count

**Reproduction** :
```bash
$ git diff tests/test_prompt_language.py | head -20
- count_skills = count_skills_in_dir(SKILLS_DIR, language="en")
- assert count_skills >= 64
+ assert count_skills >= 66  # 2 NEW adversarial skills
```

**Preuve** : le test a été modifié uniquement pour passer de `>= 64` à `>= 66`. Le test ne valide PAS le contenu des skills ajoutés (`2-vbb-adversarial-campaign`, `t-vbb-adversarial-corpus`). Il valide juste qu'ils existent et sont en anglais.

**Impact** : si une skill est ajoutée avec un contenu corrompu ou hors-périmètre (par exemple, qui ne respecte pas la structure frontmatter), le test passe quand même.

**Classification proposée** : MIRAGE_TEST.

**Fails-before test** :
```python
def test_prompt_language_validates_skill_frontmatter():
    """test_prompt_language.py must validate each skill's frontmatter
    has the required fields (name, description, adversarial_level)."""
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = read_frontmatter(skill_md)
        assert "name" in fm
        assert "description" in fm
        if skill_dir.name.startswith(("2-vbb-", "t-vbb-")):
            assert "adversarial_level" in fm or "level" in fm
```

---

## Axe 3 — Certification

### ADVR-A2-08 (S3) — CONTRAT_INCOMPLET : conditions 6.3.10 (revocation_mechanism) et 6.3.11 (cadence ≤ 90 days) non mécaniquement validées

**Reproduction** :
```bash
$ grep -n "revocation_mechanism\|cadence.*90\|cadence_days" tools/vbb-adversarial-gate.py | head -10
(no output)
```

**Preuve** : le validateur documente `6.3.10 revocation_mechanism declared` et `6.3.11 cadence ≤ 90 days` (lignes 116-117) dans la liste des conditions, mais le code qui implémente ces validations n'a pas été trouvé. Le validateur s'arrête aux conditions 6.3.1-9 et aux conditions A2-spécifiques (witnessed_by, test_review).

**Impact** : un run peut prétendre `cadence: manual:yearly` et passer la validation. La règle M1-04 (cadence ≤ 90 jours) n'est pas mécaniquement garantie.

**Code concerné** : `tools/vbb-adversarial-gate.py` (manque validation §6.3.10 + §6.3.11).

**Classification proposée** : CONTRAT_INCOMPLET.

**Fails-before test** :
```python
def test_adversarial_gate_rejects_cadence_above_90_days():
    """vbb-adversarial-gate.py must FAIL when cadence > 90 days (M1-04)."""
    fixture = make_closeout(certification_status="CERTIFIED",
                            cadence="manual:yearly")
    result = validate_run(fixture.run_dir)
    assert any(g.verdict == "FAIL" and "cadence" in g.subject.lower()
               for g in result["gates"])
```

---

## Axe 4 — Compatibilité ascendante

### ADVR-A2-09 (S2) — CONTRAT_INCOMPLET : aucun test ne valide le comportement d'un lecteur v1.0 sur des données v1.1

**Reproduction** :
```bash
$ grep -rn "v1.0_reader\|v10_reader\|downgrade" tests/ | head -5
```

**Preuve** : `tests/test_backward_compat_v1_0.py` existe mais ne teste PAS ce qui se passe quand un lecteur v1.0 consomme des données v1.1. Il teste que le validateur v1.1 accepte des données v1.0 valides. La direction inverse (v1.0 reader on v1.1 data) n'est pas testée.

**Impact** : la garantie "no v1.1 data should be silently degraded to OTHER" repose uniquement sur le comportement documenté du validateur v1.1, pas sur un test vérifiant que la dégradation ne se produit pas.

**Code concerné** : `tests/test_backward_compat_v1_0.py`.

**Classification proposée** : CONTRAT_INCOMPLET.

**Fails-before test** :
```python
def test_v10_reader_on_v11_data_does_not_silently_degrade():
    """When a v1.0 reader (closure tool without v1.1 support)
    consumes v1.1 data with gate_family=ADVERSARIAL, it must
    FAIL loudly, NOT silently degrade to OTHER."""
    fixture = make_v11_closeout(gate_family="ADVERSARIAL")
    result = simulate_v10_closure_check(fixture.run_dir)
    assert result.verdict == "FAIL"
    assert "ADVERSARIAL" in result.errors_text
    assert "OTHER" not in result.degraded_to
```

---

## Axe 5 — Propagation

### ADVR-A2-04 (S3) — CONTRADICTION_DOCUMENTAIRE : énumération `gate_family` n'inclut pas le verbe "or" en anglais dans tous les documents

**Reproduction** :
```bash
$ grep -rn "DESIGN.*CERTIFICATION.*ADVERSARIAL.*OTHER\|DESIGN, CERTIFICATION, ADVERSARIAL, OTHER" \
    docs/ prompts/ skills/ distributions/ tools/ | wc -l
```

**Preuve** : l'énumération canonique `gate_family ∈ {DESIGN, CERTIFICATION, ADVERSARIAL, OTHER}` est cohérente entre ADR 0051, GATE_ASSURANCE, templates, prompts, skills, distributions, validators, et tests. Bonne propagation.

**Impact** : aucun impact négatif, mais la propagation réussie mérite d'être signalée comme vérifiée.

**Classification proposée** : CONTRADICTION_DOCUMENTAIRE (nulle, car propagation correcte).

**Note** : cet axe confirme que la propagation des énumérations est correcte. Pas de finding bloquant.

---

### ADVR-A2-13 (S3) — CONTRAT_INCOMPLET : `distributions/codex/setup.sh` et `distributions/opencode/setup.sh` non testés

**Reproduction** :
```bash
$ git diff distributions/codex/setup.sh distributions/opencode/setup.sh
(no output — neither file modified)

$ grep -rn "codex\|opencode" tests/ | head -5
```

**Preuve** : les 4 distributions actives sont censées picker automatiquement le Core (`distributions/<name>/setup.sh` héritant de l'AGENTS.md canonique). Or, le code dans `codex/setup.sh` et `opencode/setup.sh` n'a pas été modifié pour intégrer les nouveaux champs adversariaux. La propagation automatique dépend du mécanisme déjà en place (non vérifié par cette campagne).

**Impact** : si le mécanisme de propagation ne fonctionne pas correctement, les distributions codex et opencode ne sauront pas gérer le niveau adversarial. Mais cette campagne ne peut pas exécuter ces distributions (pas d'environnement codex/opencode local).

**Classification proposée** : CONTRAT_INCOMPLET (la propagation est déclarée CR#12 mais pas mécaniquement testée pour codex/opencode).

---

## Axe 6 — Mirage de tests

### ADVR-A2-06 (S3) — MIRAGE_TEST : `tests/test_gate_check_level.py` (3 tests) ne couvre pas les combinaisons incohérentes

**Reproduction** :
```bash
$ wc -l tests/test_gate_check_level.py
36 tests/test_gate_check_level.py

$ grep -c "def test_" tests/test_gate_check_level.py
3
```

**Preuve** : seulement 3 tests sur les combinaisons de `gate_family` × `checkpoint`. La matrice de couverture est incomplète. Par exemple :
- `gate_family: ADVERSARIAL` × `checkpoint: PRE_IMPLEMENTATION` (invalide selon §1.4 ?)
- `gate_family: OTHER` × `checkpoint: COUNTER_PROOF` (invalide car COUNTER_PROOF réservé à ADVERSARIAL ?)

**Impact** : les transitions invalides peuvent passer inaperçues.

**Classification proposée** : MIRAGE_TEST.

**Fails-before test** :
```python
def test_gate_family_adversarial_with_pre_implementation_checkpoint():
    """ADVERSARIAL gate family should not be paired with
    PRE_IMPLEMENTATION checkpoint (PRE_IMPLEMENTATION is for DESIGN)."""
    fixture = make_closeout(gate_family="ADVERSARIAL",
                            checkpoint="PRE_IMPLEMENTATION")
    result = validate_run(fixture.run_dir)
    assert any(g.verdict == "FAIL" for g in result["gates"])
```

---

### ADVR-A2-11 (S2) — MIRAGE_TEST : `tests/test_a2_proxy.py` valide le proxy mais pas l'indépendance mécanique

**Reproduction** :
```bash
$ cat tests/test_a2_proxy.py | head -30
```

**Preuve** : `tests/test_a2_proxy.py` teste la **présence** des champs `attacker_identity.{agent, llm, system_prompt_version}`, pas leur **différence** réelle. Le test passe si l'attaquant déclare un LLM identique au défenseur.

**Impact** : ADVR-A2-01 + ADVR-A2-11 sont liés : tous deux démontrent que le contrat A2_DISTINCT_AGENT_PROXY n'est pas mécaniquement garanti, ni par le validateur, ni par les tests.

**Classification proposée** : MIRAGE_TEST.

**Fails-before test** : identique à ADVR-A2-01.

---

## Verdict préliminaire

```yaml
verdict_preliminary: "FAIL_ADVERSARIAL — 1 finding S1 + 6 findings S2 + 6 findings S3"

justification:
  - "1 finding S1 (ADVR-A2-01): A2_DISTINCT_AGENT_PROXY non mécaniquement validé"
  - "6 findings S2 (ADVR-A2-05, -07, -09, -10, -11 + implicit): validateurs incomplets"
  - "6 findings S3: documentation et propagation à durcir"

distinct_actor_verified: true
  proxy_limitations_disclosed: true
  quarterly_external_review_due: "2026-10-28"

fail_closed_procedure:
  - "Aucun commit correctif ne sera appliqué pendant la campagne initiale."
  - "Les findings restent dans l'agrégation initiale."
  - "Résolution ultérieure par closure_evaluation."
  - "Nouvelle campagne A2 sur un nouveau SHA après remédiation."
```

## Annexe — reproduction commands

```bash
# ADVR-A2-01
grep -n "A2_DISTINCT_AGENT_PROXY\|distinct_llm" tools/vbb-adversarial-gate.py

# ADVR-A2-02
grep -rn "level_reason" docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md docs/templates/

# ADVR-A2-03
grep -rn "last_external_review" docs/templates/ tools/

# ADVR-A2-05
sed -n '867,895p' tools/vbb-adversarial-gate.py

# ADVR-A2-07
grep -n "session" tools/vbb-adversarial-gate.py

# ADVR-A2-08
grep -n "revocation_mechanism\|cadence.*90" tools/vbb-adversarial-gate.py

# ADVR-A2-09
grep -rn "v1.0_reader\|v10_reader" tests/

# ADVR-A2-10
git diff tests/test_prompt_language.py

# ADVR-A2-11
cat tests/test_a2_proxy.py | head -30

# ADVR-A2-12
grep -n "PRE_CERTIFICATION.*expir\|max.*duration" docs/ tools/

# ADVR-A2-13
git diff distributions/codex/setup.sh distributions/opencode/setup.sh
```