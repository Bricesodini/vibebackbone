---
run_id: "2026-08-26_local-agents-bootstrap"
phase: "POC"
status: "CONCLUDED"
---

# POC — local-agents-bootstrap

## Hypothèse

Un bootstrap portable peut identifier de façon déterministe le répertoire de
lancement et la racine Git, sans recherche de parent arbitraire.

## Test

```bash
tmpdir=$(mktemp -d)
git -C "$tmpdir" init -q
mkdir -p "$tmpdir/service"
git -C "$tmpdir/service" init -q
git -C "$tmpdir/service" rev-parse --show-toplevel
```

## Critère de réussite

GO si la commande retourne uniquement la racine du dépôt imbriqué `service`.

## Résultat observé

- **Date d'exécution** : 2026-08-26
- **Métrique mesurée** : la racine retournée est le dépôt `service`.

## Décision

- **Verdict**: GO
- **Justification** : Git fournit une frontière déterministe qui respecte les
  submodules et dépôts imbriqués sans explorer les parents.
