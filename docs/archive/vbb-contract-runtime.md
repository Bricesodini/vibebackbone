# VBB Contract Runtime — Documentation

## Statut

Phase 3 a livré plus que prévu :
- **Plan initial** : Phase 3 = Phase Router (routing reader) + INDEX.yaml
- **Livré** : Runtime minimal avec exécution récursive des blocking gates
- **Decision** : Dérive acceptée, documentée ici, stabilisée avant Phase 4

---

## Comportement

### Principe fondamental

Le runtime est un exécuteur de contrats declaratifs. Il ne modifie aucun fichier métier. Il ne fait pas de suggestions. Il ne modifie pas la logique des prompts.

### Cycle d'exécution

```
1. validate  → Linter doit passer (exit 0)
2. load      → Lit skills/INDEX.yaml, charge les contrats
3. resolve   → Résout les blocking gates récursivement
4. execute   → Simule l'exécution, enregistre le statut
5. trace     → Écrit les traces JSON dans docs/audits/vbb-runtime/
```

### Blocking gates

Un contrat avec un blocking gate vers un autre skill :
1. Appelle récursivement `execute_contract()` sur le skill cible
2. Compare le `status` retourné avec `expected_status`
3. Si différent → statut `BLOCKED`, pas d'exécution further

**Exemple** :
```
0-vbb-audit-readiness
  └── blocking gate: scope_must_be_frozen → 0-vbb-scope-freeze (expected: PASS)
      └── 0-vbb-scope-freeze retourne PARTIAL → 0-vbb-audit-readiness est BLOCKED
```

C'est le comportement attendu. Voir § Comportements documentés.

### Statuts

| Statut | Signification |
|---|---|
| `PASS` | Toutes les gates passent |
| `PARTIAL` | Certaines gates échouent mais le contrat peut continuer |
| `FAIL` | Erreur fatale |
| `BLOCKED` | Un blocking gate a échoué |

### Traces

Chaque exécution produit deux fichiers JSON dans `docs/audits/vbb-runtime/` :
- `{contract_id}_{timestamp}.json` — trace isolée
- `{contract_id}_latest.json` — dernière exécution (overwrite)

Format de trace :
```json
{
  "contract_id": "...",
  "status": "PASS|PARTIAL|BLOCKED|FAIL",
  "started_at": "ISO8601",
  "ended_at": "ISO8601",
  "duration_ms": N,
  "agent": "local",
  "inputs": {...},
  "gates": [...],
  "outputs": {...},
  "warnings": [...],
  "errors": [...],
  "events": {
    "declared": true/false,
    "executed": false,
    "reason": "Events disabled in Phase 3 minimal runtime"
  }
}
```

---

## Commandes

### Validation seule

```bash
python tools/vbb-contract-runtime.py validate
```

### Exécuter un contrat

```bash
python tools/vbb-contract-runtime.py run <contract_id>
```

### Exécuter tous les contrats

```bash
python tools/vbb-contract-runtime.py test-all
```

---

## Comportements documentés

### BLOCKED attendus

| Skill appelant | Gate bloquante | Raison |
|---|---|---|
| `0-vbb-audit-readiness` | `scope_must_be_frozen` | `0-vbb-scope-freeze` retourne PARTIAL (pas PASS) |
| `t-vbb-mode-transition-gate` | `scope_must_be_clear` | Même raison |

Ces BLOCKED ne sont pas des erreurs. Ils reflètent l'état réel du projet (scope pas encore gelé).

### Events désactivés

Les events (`on_success`, `on_partial`, `on_failure`, `on_blocked`) sont **déclarés dans les contrats mais non exécutés**.

Raison : Phase 3 minimal runtime. Les events seront activés dans Phase 4 selon des règles de correlation.

### Phase Router

**Statut** : Non livré en Phase 3.

Le runtime minimal remplace partiellement la fonction de routing :
- Il lit INDEX.yaml pour charger les contrats
- Il ne route pas encore vers des agents spécifiques

Le Phase Router complet (Phase 3 originale) est reporté à Phase 4.

---

## Limites

- Ne modifie aucun fichier métier (docs/, src/, etc.)
- Ne peut pas exécuter un skill sans contrat dans INDEX.yaml
- Ne supporte pas encore les agents distants (claude-code, codex, etc.)
- Profondeur max des gates = 2 (configurable dans chaque contrat)

---

## Phase 4 — Orientation

Phase 4 sera "Optional Runtime Hardening" :
- events activables
- dry-run / strict mode
- traces améliorées
- Phase Router
- tests automatisés
- CI optionnel

Pas : "créer le runtime" — il existe déjà.