# POC — Synthetic staged-blob credentials audit harness

**Statut**: CONCLUDED
**Date**: 2026-07-14
**Liée à ADR**: `docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md`
**Liée à RUN**: `docs/runs/2026-07-14_1040_credentials-enforcement-audit/`

## Hypothèse

Le comportement credentials du hook peut être reproduit dans un dépôt Git
temporaire avec un blob synthétique staged, sans créer de secret réel ni de
fichier de travail.

## Test (concret, exécutable)

```bash
tmp=$(mktemp -d /tmp/vbb-credentials-audit-poc.XXXXXX)
git -C "$tmp" init -q
blob=$(git -C "$tmp" hash-object -w --stdin <<< \
  'credential_fixture = "VBB_SYNTHETIC_NOT_A_SECRET"')
git -C "$tmp" update-index --add --cacheinfo \
  100644,"$blob",tools/credential_fixture.py
(cd "$tmp" && bash "$VBB_ROOT/scripts/hooks/pre-commit-framework-gate")
```

## Critère de réussite

GO si le hook observe le chemin staged, expose son comportement credentials,
retourne un exit code reproductible et le worktree temporaire reste sans
fichier hors `.git`.

## Résultat observé

- Message : `checking credentials ... pattern list deferred`.
- Exit code : `0`.
- Chemin staged : `tools/credential_fixture.py`.
- Fichiers de worktree hors `.git` : `0`.

## Décision

- **Verdict**: GO
- **Justification**: le harness permet l'audit des décisions du hook sur des
  blobs synthétiques, sans exposition de credentials ni mutation du repo cible.

## Bilan

L'audit peut démarrer. Ce POC ne valide pas l'enforcement ; il valide seulement
la méthode sûre de reproduction, et confirme déjà que le comportement courant
est informatif avec exit `0`.

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md
hypothesis_validated: true
metric_observed: "exit 0, staged path visible, 0 worktree files"
metric_threshold: "reproductible without real secret or worktree file"
reproducible: true
verified_at: "2026-07-14T10:44:00+02:00"
verified_by: codex
```
