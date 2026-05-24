---
context_role: runs-index
phase: transverse
status: active
updated: 2026-05-23
---

# docs/runs/ — Artefacts de run

Chaque run vibebackbone produit un dossier horodaté qui contient les artefacts
de ses phases. Ces artefacts forment la mémoire officielle, versionnée et
machine-vérifiable du travail effectué.

## Convention de nommage

```
docs/runs/YYYY-MM-DD_HHmm_slug/
```

- `YYYY-MM-DD` : date du jour de démarrage du run
- `HHmm` : heure approximative de démarrage (24h, sans séparateur)
- `slug` : kebab-case court qui décrit l'intention (`fix-error-message`,
  `security-audit`, `artifact-infra-lot-a`)

Exemples :
- `docs/runs/2026-05-19_1000_moc-context-strategy/`
- `docs/runs/2026-05-23_1600_artifact-infra-lot-a/`

## Invariant de clôture

**Toute boucle, quelle que soit sa voie, produit au minimum 3 artefacts :**

```
docs/runs/{slug}/
├── 01_INTAKE.md          ← obligatoire (cadrage)
├── 0X_<phase métier>.md  ← ≥1 phase intermédiaire selon la voie
└── 07_CLOSEOUT.md        ← obligatoire (clôture)
```

Phases minimales par voie :

| Voie         | Phases obligatoires       | Phases conditionnelles |
|--------------|---------------------------|------------------------|
| `RAPIDE-ZERO`   | Aucun (`docs/runs/` non requis) | Activity Log uniquement |
| `RAPIDE-MINIMAL`| 05_PATCH_SUMMARY seul | Activity Log requis |
| `RAPIDE`     | 01 + 05 + 07              | 04 si plan non trivial |
| `STRUCTUREE` | 01 + 04 + 05 + 07         | 06 si DoD critique     |
| `AUDIT`      | 01 + 02 + 03 + 07         | 04 + 05 si remédiation |
| `CLOTURE`    | 07 seul (cas spécial)     | 06 si bilan long       |

Cet invariant sera vérifié mécaniquement par `tools/vbb-loop-closure-check.py`
(livré dans PR #3 du plan d'artefacts).

## Format des artefacts

Chaque fichier `0X_*.md` suit le template correspondant dans
[`docs/templates/`](../templates/).

Frontmatter YAML obligatoire :

```yaml
---
run_id: "YYYY-MM-DD_HHmm_slug"
phase: "0X_NAME"
voie: "RAPIDE-ZERO|RAPIDE-MINIMAL|RAPIDE|STRUCTUREE|AUDIT|CLOTURE"
status: "READY|PARTIAL|BLOCKED|UNKNOWN"
agent: "claude-code|codex|pi|opencode"
started_at: "ISO8601 UTC"
ended_at: "ISO8601 UTC"
next_phase: "0X_NAME | null"
artifacts_consumed: [...]
artifacts_produced: [...]
---
```

## Cycle de vie

1. Un run démarre par la production de `01_INTAKE.md` qui fige la voie et le scope.
2. Les phases intermédiaires se succèdent selon la voie identifiée.
3. Le run se termine par `07_CLOSEOUT.md` qui consolide les artefacts produits.
4. À la clôture, `docs/CONTEXT.md` § Runs récents doit être mis à jour.
5. Si la voie était AUDIT, `docs/AUDIT_STATUS.md` est également mis à jour.

## Liens connexes

- [Protocole agentique complet](../AGENTIC_RUN_PROTOCOL.md)
- [Templates d'artefacts](../templates/)
- [Règles de session](../SESSION_RULES.md)
- [Mémoire et handoff](../MEMORY_AND_HANDOFF.md)
