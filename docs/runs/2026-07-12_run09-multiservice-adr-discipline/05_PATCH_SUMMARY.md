# 05_PATCH_SUMMARY — Run 09 Multi-service ADR disciplinaire

**Date** : 2026-07-13
**Route** : STRUCTURED
**Fichiers créés** : 3 ADR + index + 3 artefacts run
**Lignes ajoutées** : ~700 (ADR substantiels)

---

## 3 ADR créés

### ADR-0009 — Linter discipline multi-service (Gap-04, P0)

**Fichier** : `docs/adr/0009-multiservice-lint-discipline.md`

**Décision** : créer `tools/vbb-multiservice-lint.py` qui valide 3 familles de règles :
1. **DB isolation** : interdit accès direct DB cross-service pour `db_orientation: shared_external_*`
2. **IMPACT_LOG à jour** : si contrats consommés existent
3. **CONTRACTS_CONSUMED à jour** : `Last updated < 90 jours`

Configuration par projet via `docs/MULTISERVICE_DISCIPLINE.yaml` (allow-list, severity par règle).

**Modes** : par défaut warning + exit 0, `--strict` exit 2, `--json` machine-readable.

**Justification** : la discipline multi-service passe de vigilance humaine à vérification outillée. Séparation claire avec `vbb-contract-lint` (concerns différents).

**Alternatives rejetées** (3) :
- A — statu quo conversationnel (régression silencieuse)
- B — intégrer dans `vbb-contract-lint` (séparation des concerns)
- C — pre-commit framework externe (dépendance réseau)

### ADR-0010 — IMPACT_LOG cumulatif (Gap-06, P0)

**Fichier** : `docs/adr/0010-impact-log-cumulative.md`

**Décision** : créer `docs/IMPACT_LOG.md` (par projet), append-only, avec table à 7 colonnes (Date, Type, Contrat, Avant, Après, Services impactés, Lien run).

Skill `t-vbb-impact-log-update` (à créer Run 10+) facilite l'entrée via formulaire guidé.

**Types d'entrées** : `breaking` / `additive` / `deprecation` / `fix` / `consumed_change`.

**Justification** : sans log cumulatif, l'historique des impacts est perdu. Le log sert de trace vérifiable et permet les métriques de discipline.

**Alternatives rejetées** (3) :
- A — persistance binaire (non versionnable, non lisible)
- B — un fichier par impact (dispersion)
- C — git log (non structuré, non queryable)

### ADR-0011 — Taxonomie contrats cross-service (Gap-10, P0)

**Fichier** : `docs/adr/0011-cross-service-contract-taxonomy.md`

**Décision** : étendre `1-vbb-api-contract-designer` pour ajouter un champ obligatoire `Consumers` dans `CONTRACT.yaml` (sous `outputs.artifact`).

```yaml
consumers:
  - service: <slug>
    type: <internal | external>
    version_pinned: <semver>
    contract_consumed_ref: <path>
    criticality: <critical | medium | low>
```

**Validation croisée** : chaque `consumers[*]` doit avoir une entrée correspondante dans `CONTRACTS_CONSUMED.md` du service cible (vérifié par `vbb-multiservice-lint`, ADR-0009).

**Modifications** : `1-vbb-api-contract-designer` (PROCESS, OUTPUT CONTRACT, VALIDATION LOOP, EXAMPLES) + symétrique `2-vbb-api-auditor`.

**Justification** : la boucle producer↔consumer est fermée au niveau framework. La discipline devient vérifiable des deux côtés.

**Alternatives rejetées** (3) :
- A — inférer depuis `CONTRACTS_CONSUMED.md` (fragile au bootstrapping)
- B — optionnel (jamais rempli)
- C — fichier séparé `CONTRACT_CONSUMERS.yaml` (dispersion)

---

## Index — `docs/adr/README.md`

**Modification** : 3 lignes ajoutées dans la table indexe (ADR-0009, ADR-0010, ADR-0011).

---

## Vérifications P.R2 (pre-merge gate REQUIS, route STRUCTURED)

| # | Vérification | Statut | Preuve |
|---|--------------|--------|--------|
| 1 | **Lint / format** | ✅ | `python tools/vbb-contract-lint.py` → 0 error, 0 warning |
| 2 | **Type / schema** | ✅ N/A | ADR = markdown |
| 3 | **Tests** | ✅ N/A | Aucun test impacté |
| 4 | **Build** | ✅ N/A | Pas de code build |
| 5 | **Documentation coherence** | ✅ | 3 ADR présents, 3 références dans README.md |

**Verdict pre-merge gate** : **PASS**.

### Sanity checks

- ✅ `git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md tools/vbb-contract-lint.py skills/1-vbb-api-contract-designer/SKILL.md` = vide
- ✅ Chaque ADR a ≥ 2 alternatives rejetées (vérifié : 3 alternatives par ADR)

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers créés | 4 (3 ADR + index ADR) |
| Fichiers modifiés | 0 (canon intact) |
| Lignes ajoutées | ~700 |
| Canon touché | 0 |
| Outils créés | 0 (différé à Run 10+) |
| Templates créés | 0 |
| Skills modifiés | 0 |
| ADR créés | 3 (0009, 0010, 0011) |
| ADR status initial | ACCEPTED |
| Risque | Faible (documents de design seulement, pas d'implémentation) |
| Findings P0 résolus (design) | Gap-04, Gap-06, Gap-10 (les 3 derniers P0 du tiercé disciplinaire) |