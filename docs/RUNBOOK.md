# RUNBOOK — vibebackbone

Procédures opérationnelles pour maintenir vibebackbone comme catalogue de distribution versionné.

## Daily Tasks (5 min)

1. **Monitor GitHub** : Vérifier issues/PRs
2. **Check AUDIT_STATUS.md** : dernier audit < 30 jours ?
3. **Git commits** : Continuité normale?

## Weekly Tasks (30 min)

1. **Review PRs** : Vérifier CONTRIBUTING.md conformance
2. **Triage issues** : Classer par P0/P1/P2
3. **Update CHANGELOG.md** : Si changes depuis dernière release

## Monthly Tasks (2 hours)

1. **Security scan** : Vérifier absence secrets en git
2. **Documentation review** : Coherence + staleness
3. **Dependency check** : dépendances déclarées dans `requirements.txt`, vérifier les mises à jour

## Quarterly Tasks (4 hours)

1. **Audit auto-référencé** : Relancer séquence [0→1→2→3]
2. **Risk register update** : Consolider findings
3. **Release planning** : vX.Y.Z?

## Pre-execution gate

Pi, OpenCode, Codex and Claude Code must run the same pre-execution gate
against the run directory before any non-trivial code patch:

```bash
python ~/02_Dev/vibebackbone/tools/vbb-gate-check.py <run_dir>
```

This validates the run against ADR/POC/Integration gate rules and refuses
to proceed if the run is non-conformant. See `docs/PILOTAGE.md` for the
Triage Rule that triggers it.

## Emergency Procedures

### If Secret Leaked
1. Identify commit with leak
2. `git revert [commit]` + push
3. Advise users to update
4. Post security advisory GitHub
5. Run audit security

### If Critical Issue Found
1. Patch immediately
2. Create security advisory
3. Release patch version
4. Notify users

## Backup & Recovery

**Backup** : GitHub is the backup (distributed git)  
**Recovery** : `git checkout [commit]` + push

## Version Management

```
v1.0.0 = MAJOR.MINOR.PATCH
  ├─ MAJOR = breaking changes
  ├─ MINOR = new skills / features
  └─ PATCH = bug fixes / docs

Release process:
1. Update CHANGELOG.md
2. Run `python3 -m pip install -r requirements.txt`
3. Run `bash scripts/vbb-ci-local.sh`
4. Create an RC tag first, e.g. `git tag -a v1.0.0-rc.2 -m "Release candidate v1.0.0-rc.2"`
5. Push the RC tag and rerun external review
6. Before final stable, verify no stale local tags point to older commits
7. Recreate stable tag only from the approved stable commit
8. Create GitHub release
9. Publish package metadata if applicable
```

## Stable tag hygiene

A stale local tag must not be pushed if it points to an older commit than
the approved release candidate. Delete and recreate it deliberately only after
stable approval:

```bash
# Check where the tag points
 git rev-parse v1.0.0
# Delete and recreate deliberately
git tag -d v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
```

---

**Last updated** : 2026-06-13
