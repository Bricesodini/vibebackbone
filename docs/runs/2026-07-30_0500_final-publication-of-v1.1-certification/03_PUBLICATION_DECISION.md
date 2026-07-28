---
run_id: "2026-07-30_0500_final-publication-of-v1.1-certification"
phase: "03_PUBLICATION_DECISION"
voie: "STRUCTUREE"
status: "READY"
kind: "FINAL_PUBLICATION_DECISION"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "minimax/MiniMax-M3 (publication operator)"
started_at: "2026-07-30T05:30:00Z"
ended_at: "2026-07-30T05:45:00Z"
next_phase: "PUBLICATION_ACTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_PRE_PUSH_VERIFICATION.md"
artifacts_produced:
  - "03_PUBLICATION_DECISION.md (this file)"
---

# 03_PUBLICATION_DECISION — Final Publication

## Décision

**GO pour publication**.

| Aspect | Décision |
|---|---|
| Commit documentaire | ✅ Autorisé |
| Tag `vbb-v1.1-adversarial-certified` | ✅ Autorisé |
| Push main | ✅ Autorisé |
| Push tag | ✅ Autorisé |
| Force push | ❌ INTERDIT |

## Actions

```bash
# 1. Commit documentaire
git commit -m "<see below>"

# 2. Tag annoté (sur c4bb4b63, PAS sur le commit documentaire)
git tag -a vbb-v1.1-adversarial-certified c4bb4b63 -m "..."

# 3. Push
git push origin main
git push origin vbb-v1.1-adversarial-certified
```

## Garde-fous

```yaml
commit_message_discipline:
  type: "docs(adversarial)"
  subject: "publish certified v1.1 assurance campaign"
  body_must_include:
    - "Reference to certified commit c4bb4b63"
    - "List of historical campaigns (1, 2, 3)"
    - "Statement that this commit is documentary only"
  prohibited:
    - "Functional modifications"
    - "Normative modifications"
    - "Corrective modifications"

tag_discipline:
  name: "vbb-v1.1-adversarial-certified"
  type: annotated
  target: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
  not_target: "<the new documentary commit>"
  reason: "Tag must point to the CERTIFIED commit, not the publication commit"

push_discipline:
  force_push: false
  branch: main
  tag: vbb-v1.1-adversarial-certified
```

## Critères de succès

| Critère | Vérification |
|---|---|
| Commit créé | `git log --oneline -1` |
| Tag pointe sur c4bb4b63 | `git rev-list -n 1 vbb-v1.1-adversarial-certified` |
| Push réussi | `git fetch origin && git rev-parse origin/main` |
| HEAD == origin/main | post-push verification |
| Tag pushed | post-push verification |
| Tree clean | post-push verification |

## Dette post-certification (backlog)

```yaml
post_certification_backlog:
  M4:
    - "ADVR-RT-01 (gate name trompeur)"
    - "ADVR-RT-02 (level whitespace strip)"
    - "ADVR-RT-03 (revocation_mechanism non mécaniquement vérifié)"
  separate_distribution_fix:
    - "CLAUDE-SKILLS-DISCOVERY-01"

priority:
  1: "CLAUDE-SKILLS-DISCOVERY-01 (empêche l'usage effectif des skills dans Claude Code)"
  2: "ADVR-RT-03 (mécanisme de révocation)"
  3: "ADVR-RT-01 + ADVR-RT-02 (cosmétique)"
```

Ces corrections doivent intervenir après publication, dans des
commits et runs séparés.
