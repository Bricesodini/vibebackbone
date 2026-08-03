# F03-GOVERNANCE-REMEDIATION — Plan

1. Run the repository gate before implementation.
2. Record the exact pre-change passage and its relation to ADR-0053.
3. Replace only the unqualified `distinct actor` wording at lines 347–349
   with explicit v1.2/v1.1/A3 scope.
4. Re-read the complete surrounding clauses and verify no other file changed.
5. Run targeted A2 review, architecture/contract/convention checks, relevant
   tests, and `git diff --check`.
6. Close with only `F03_CLOSED` or `F03_REQUIRES_REVISION`.

No migration, adoption, publication, or Git integration is part of this run.

