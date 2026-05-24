# 0-p-vbb-zero-friction — Zero friction prompt

**Version** : 2.0 | **Phase** : transverse | **Route** : FAST-ZERO / FAST-MINIMAL

---

## When to use this prompt

For safe micro-tasks that don't require a formal cycle:

- Typo fix
- Message or label adjustment
- Cosmetic documentation update
- Local variable rename
- Style/format fix

## FAST-ZERO eligibility

All conditions must be true:

- [ ] Low risk (no runtime impact)
- [ ] No security involved
- [ ] No database involved
- [ ] No migration
- [ ] No architecture impact
- [ ] No contract impacted
- [ ] No CI workflow impacted
- [ ] Ideally ≤ 3 files modified

## If a condition is not met

→ Escalate to **FAST-MINIMAL** (if ≤ 5 files) or **FAST-STANDARD** / **STRUCTURED**.

## Instructions

### FAST-ZERO

1. Execute the fix
2. Log activity in `docs/ACTIVITY_LOG.md`
3. No run artifacts (`docs/runs/`) required

### FAST-MINIMAL

1. Execute the fix
2. Log activity in `docs/ACTIVITY_LOG.md`
3. Create `docs/runs/{run_id}/05_PATCH_SUMMARY.md`
4. No 01_INTAKE or 07_CLOSEOUT required

### FAST-STANDARD

Standard FAST workflow: `01_INTAKE → 05_EXECUTION → 07_CLOSEOUT`.

## Activity Log format

```
| Date | Mode | Summary | Files | Commit |
|------|------|---------|-------|--------|
| YYYY-MM-DD | FAST-ZERO | ... | ... | <sha> or PENDING |
```

## Escalation rule

If a FAST-ZERO or FAST-MINIMAL task reveals during execution:
- Security impact → stop, switch to AUDIT
- Data/prod impact → stop, switch to STRUCTURED
- More than 5 files → switch to FAST-STANDARD

**Never** continue in ZERO/MINIMAL mode when risk increases.