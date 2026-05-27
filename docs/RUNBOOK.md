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
3. **Dependency check** : dépendances déclarées dans `requirements.txt`, rien à mettre à jour

## Quarterly Tasks (4 hours)

1. **Audit auto-référencé** : Relancer séquence [0→1→2→3]
2. **Risk register update** : Consolider findings
3. **Release planning** : vX.Y.Z?

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
2. `git tag -a v1.0.0 -m "Release 1.0.0"`
3. `git push origin v1.0.0`
4. Create GitHub release
5. Publish to npm (if applicable)
```

---

**Last updated** : 2026-06-13
