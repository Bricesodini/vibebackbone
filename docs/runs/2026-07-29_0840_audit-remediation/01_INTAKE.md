---
run_id: "2026-07-29_0840_audit-remediation"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
kind: "GOVERNANCE_ENFORCEMENT_REMEDIATION"
adversarial_level: "A2"  # canon-gating work: hardens the gates that authorize READY
scope_id: "AUDIT-REMEDIATION-01"
agent: "claude-opus-5 (Claude Code)"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
adr_link: "docs/adr/0051-adversarial-assurance-dimension.md"
linked_subject:
  schema: "git-commit"
  baseline_commit: "f8850ca"
  invalidated_commit: "218a6fd"
started_at: "2026-07-29T06:40:00Z"
ended_at: "2026-07-29T09:30:00Z"
artifacts_produced:
  - "01_INTAKE.md (this file)"
  - "POC.md"
  - "04_PLAN.md"
  - "05_EXECUTION.md"
  - "07_CLOSEOUT.md"
---

# 01_INTAKE — AUDIT-REMEDIATION-01

## 1. Objectif

Fermer les findings F2 à F7 d'un audit en lecture seule mené le 2026-07-29, qui a
établi que **le verdict `READY` publié n'était pas soutenu par la mesure**.

Ce run ne corrige pas seulement l'état : il corrige les **mécanismes** qui ont
permis de publier un faux verdict. Le critère d'acceptance central n'est pas que
les gates repassent au vert, mais qu'ils soient démontrés **capables d'échouer**.

## 2. Baseline (au démarrage)

```yaml
baseline:
  HEAD: "f8850ca"
  origin/main: "f8850ca"
  working_tree: clean
  documented_verdict: "READY"          # contesté par ce run
  measured_local_ci: "14 passed / 0 failed (après hotfix F1)"
  canonical_skills_count: 66
  contracted_skills_count: 64          # écart F2
  adversarial_corpus_entries: 0
```

### Preuve d'invalidation conservée

Le run CI distant `vbb-contracts` était `failure` sur `218a6fd` **et déjà sur
`3f4d831`** (API GitHub Actions, observée le 2026-07-29). Le rouge distant
précédait donc d'au moins deux commits la publication du verdict `READY`.
Ces SHA ne doivent pas être réécrits : ils constituent la preuve d'échec.

## 3. Findings traités

| ID | Sévérité | Objet |
|---|---|---|
| F2 | P1 | Contract lint fail-open sur `CONTRACT.yaml` absent ; 2 skills adversariaux hors contrat et hors index |
| F3 | P1 | Gate 5b (adversarial + corpus) absent de la CI locale et distante ; corpus vide sortant en code 5 |
| F4 | P1 | `tests/test_corpus_mandatory.py` est un test-mirage : il grep de la prose, il ne peut pas échouer |
| F5 | P1 | Bloc shell « canonique » de `pre-merge-gate.md` inexécutable (`adversarial_governance_cutoff_state` inexistant) |
| F6 | P1 | `AUDIT_STATUS.md` déclare `ADV-GOV-001` PROPOSED alors que ADR 0051 est ACCEPTED — vérité parallèle |
| F7 | P1 | `CONTEXT.md` pointe vers une décision humaine déjà rendue |

F1 (P0) est fermé par le hotfix `f8850ca`, hors de ce run.
F8 à F13 (P2/P3) sont hors scope de ce run et seront inscrits au registre des
risques actifs avec owner et trigger de réouverture.

### Chaîne de vérité visée

```
déclaration d'un invariant
  → enregistrement dans les contrats et l'index      (F2)
  → gate capable de le vérifier                      (F3/F5)
  → test capable d'échouer                           (F4)
  → CI qui exécute le gate                           (F3)
  → surface canonique qui reflète le résultat        (F6/F7)
  → verdict READY autorisé ou interdit
```

Les six findings sont traités ensemble parce qu'ils forment un seul maillage :
corriger l'un sans les autres laisse la chaîne rompue.

## 4. Scope autorisé

| Path | Mutable ? |
|---|---|
| `tools/vbb-contract-lint.py` | ✅ |
| `tools/vbb-status-dashboard.py` | ✅ |
| `skills/2-vbb-adversarial-campaign/` | ✅ |
| `skills/t-vbb-adversarial-corpus/` | ✅ |
| `skills/INDEX.yaml` | ✅ |
| `scripts/vbb-ci-local.sh` | ✅ |
| `.github/workflows/vbb-contracts.yml` | ✅ |
| `docs/REFERENCE/pre-merge-gate.md` | ✅ |
| `tests/test_corpus_mandatory.py` | ✅ |
| `tests/test_contract_lint.py` | ✅ |
| `tests/adversarial_corpus/` | ✅ |
| `docs/{AUDIT_STATUS,CONTEXT,DISTRIBUTIONS}.md` | ✅ |
| `docs/runs/2026-07-29_0840_audit-remediation/**` | ✅ |

### Hors scope strict

| Path | Raison |
|---|---|
| `docs/adr/00*.md` | ADR acceptés, immuables — ce run les **applique**, il n'en crée pas |
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | Canon v1.1 certifié ; le run implémente son §9, il ne le réécrit pas |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | Canon certifié |
| `tools/vbb-adversarial-gate.py` | Validator — lu et appelé, non modifié |
| Runs et audits historiques | Preuve immuable (`TEMPORAL_PROVENANCE.md`) |
| `distributions/**` | Aucune glue de distribution n'est touchée (voir §7) |

## 5. Position ADR — pourquoi aucun nouvel ADR

Ce run **n'introduit aucune décision d'architecture nouvelle**. Il rend
exécutoires trois décisions déjà `ACCEPTED` :

- `ADR 0042` — layout exact à sept sections pour tout skill. Deux skills y
  échappent aujourd'hui parce qu'ils n'ont pas de contrat ; le run les y ramène.
- `ADR 0051` — dimension adversarial, gate family et destination 6 obligatoire du
  corpus. Le run fournit le porteur d'exécution qui manquait.
- `ADR 0046` — intégrité de la readiness. Le run rétablit l'invariant que le
  verdict suit la mesure.

Si l'exécution révélait un arbitrage non couvert par ces trois ADR, le run
s'arrête et produit un `CANON_CHANGE_PROPOSAL.md` au lieu de trancher seul.

## 6. Critères d'acceptance

Aucun critère n'est satisfait par une observation « au vert ». Chaque durcissement
doit être démontré capable de rendre la CI rouge.

| # | Critère | Preuve exigée | Status |
|---|---|---|---|
| 1 | Contract lint bidirectionnel | Skill temporaire sans `CONTRACT.yaml` → exit non-zéro | TODO |
| 2 | Population canonique définie | Définition inscrite dans le code, pas seulement dans ce run | TODO |
| 3 | Couverture contractuelle 66/66 | `vbb-contract-lint.py` 0 erreur, dashboard `PASS` | TODO |
| 4 | Dashboard binaire | Couverture < 100 % rendue `FAIL`, pas un pourcentage | TODO |
| 5 | Sept sections ADR 0042 | Les 2 skills passent `check_required_skill_sections` | TODO |
| 6 | Bloc pre-merge exécutable | Bloc copié-collé tel quel → exit 0 | TODO |
| 7 | 5b câblé identiquement | Commandes identiques dans `vbb-ci-local.sh` et `vbb-contracts.yml` | TODO |
| 8 | Corpus sort proprement à vide | `pytest tests/adversarial_corpus/ -q` → exit 0, pas 5 | TODO |
| 9 | Test corpus comportemental | CONFIRMED sans corpus → échec ; avec corpus → succès ; pré-cutoff → non exigé | TODO |
| 10 | Cohérence vérifiable | ADR ACCEPTED vs AUDIT_STATUS PROPOSED détecté par une commande | TODO |
| 11 | Verdict honnête pendant le run | `AUDIT_STATUS` en `NOT_READY` dès le premier commit | TODO |
| 12 | F8–F13 inscrits | Registre des risques actifs avec owner et trigger | TODO |

## 7. Critical Rule #12 — impact quatre distributions

Surfaces Core touchées : `vbb-contract-lint.py`, `vbb-status-dashboard.py`,
`vbb-ci-local.sh`, `vbb-contracts.yml`, `pre-merge-gate.md`, catalogue `skills/`.

Impact attendu sur `pi`, `opencode`, `codex`, `claude` : **aucun changement de
glue**. Les quatre distributions consomment le catalogue et les gates, elles ne
les redéfinissent pas. Le durcissement est strictement Core.

Vérification obligatoire avant closeout : `grep` des chemins modifiés dans
`distributions/**` et consignation dans `docs/DISTRIBUTIONS.md` §Decisions log.
Si une distribution s'avérait dépendre du comportement fail-open corrigé, le run
s'arrête et escalade (Critical Rule 2).

## 8. Dimension adversarial — A2

Niveau `A2` : le run modifie les gates qui autorisent un verdict de publication.
Une régression ici réintroduit exactement le défaut audité.

`A2_DISTINCT_AGENT_PROXY` requis au closeout. Aucun acteur humain distinct n'est
disponible pour ce run ; la revue sera donc conduite sous proxy avec les trois
disclosures d'identité, ou déclarée absente. **Le run ne prétendra pas à une
indépendance qu'il n'a pas** — c'est précisément la faute `COND-01` qui avait
bloqué le run `2026-07-28_1002`.

Surfaces à explorer en adversarial : les cinq manipulations de preuve négative du
§6, plus la question ouverte « existe-t-il un autre gate fail-open du même type
que F2 ? ».

## 9. Risques identifiés

| Risque | Mitigation |
|---|---|
| Le durcissement du lint casse un skill non anticipé | Lancer le lint sur les 66 avant de rendre l'erreur bloquante |
| La normalisation des 7 sections altère le sens des 2 skills | Remapper le contenu, ne rien réécrire ; diff relu section par section |
| Le nouveau test corpus devient à son tour tautologique | Preuve négative obligatoire (critère 9) |
| Ajouter 5b à la CI distante casse les PR existantes | Vérifier le comportement sur corpus vide avant de rendre bloquant |
| Corriger `AUDIT_STATUS` sans corriger le mécanisme | Le contrôle de cohérence (critère 10) est le livrable, pas l'édition |
| Le run se déclare indépendant sans l'être | Proxy déclaré explicitement, ou absence déclarée |

## 10. Next action

Basculer `docs/AUDIT_STATUS.md` en `NOT_READY — remediation in progress` avant
toute modification de code, puis exécuter `vbb-gate-check.py` sur ce run.
