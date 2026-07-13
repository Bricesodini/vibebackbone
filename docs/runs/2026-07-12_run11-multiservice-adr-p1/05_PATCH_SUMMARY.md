# 05_PATCH_SUMMARY — Run 11 Multi-service ADR P1

**Date** : 2026-07-13
**Route** : STRUCTURED
**Fichiers créés** : 4 ADR + index + 3 artefacts run
**Lignes ajoutées** : ~700

---

## 4 ADR créés

### ADR-0012 — Codegen AGENTS.md / CLAUDE.md (Gap-03, P1)

**Décision** : étendre `tools/vbb-architecture.py` avec un mode `agents --write` qui génère `AGENTS.md` + `distributions/claude/CLAUDE.md` depuis `CONTEXT.md` + `PILOTAGE.md` + Critical Rules.

**Justification** : aujourd'hui drift silencieux entre source canonique et fichiers distribué. Le mode `--check` détecte le drift.

### ADR-0017 — Discipline outillée de co-évolution (Gap-07, P1)

**Décision** : étendre `t-vbb-impact-analyzer` avec un mode `--co-evolution --write` qui génère une liste de tâches par consumer (code_migration / dependency_bump / config_update / test_update) stockées dans `IMPACT_LOG.md` (cf. ADR-0010).

**Justification** : la co-évolution passe de vigilance humaine à tâches outillées. Le log cumulatif devient machine-actionable.

### ADR-0014 — Mécanisme canon vs extension (Gap-09, P1)

**Décision** : introduire `docs/extensions/<pattern>/` avec `MANIFEST.yaml` (schema_version, pattern, status, canon_implications, conflicts_with). Outil `vbb-extension-register` lit et valide.

**Justification** : les projets peuvent expérimenter localement sans fork. Les extensions sont visibles et les conflits détectés.

### ADR-0015 — vbb-contract-lint archetype-aware (Gap-11, P1)

**Décision** : étendre `vbb-contract-lint.py` avec règles contextuelles par `project_archetype` (lu depuis `CONTEXT.md` frontmatter). `library` : assoupli, `worker` : trigger obligatoire, `read_only_consumer` : pas d'output exposé, etc.

**Justification** : les règles sont adaptées au contexte. Plus de faux warnings pour les `library`.

---

**Note** : Gap-07 → ADR-0017 (et non 0013) car `0013-repo-organization-core-vs-distributions.md` existe déjà (legacy).

---

## Index — `docs/adr/README.md`

4 lignes ajoutées : ADR-0012, ADR-0014, ADR-0015, ADR-0017 (avec renommage du 0013 → 0017 dans le titre de l'ADR Gap-07).

---

## Vérifications P.R2 (pre-merge gate REQUIS)

| # | Vérification | Statut | Preuve |
|---|--------------|--------|--------|
| 1 | **Lint / format** | ✅ | `python tools/vbb-contract-lint.py` → 0 error, 0 warning |
| 2 | **Type / schema** | ✅ N/A | ADR = markdown |
| 3 | **Tests** | ✅ N/A | Aucun test impacté |
| 4 | **Build** | ✅ N/A | Pas de code |
| 5 | **Documentation coherence** | ✅ | 4 ADR présents, 4 références dans README.md |

**Verdict** : **PASS**.

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers créés | 5 (4 ADR + index ADR) |
| Fichiers modifiés | 0 (canon intact) |
| Lignes ajoutées | ~700 |
| Canon touché | 0 |
| Outils créés | 0 |
| ADR créés | 4 (0012, 0014, 0015, 0017) |
| ADR status initial | ACCEPTED |
| Findings P1 résolus (design) | Gap-03, Gap-07, Gap-09, Gap-11 |
| Risque | Faible (documents de design) |