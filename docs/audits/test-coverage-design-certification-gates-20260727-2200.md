---
kind: audit_report
audit_type: test-coverage
status: READY
updated: 2026-07-27
run_id: "2026-07-27_2145_design-certification-gates-core-integration"
---

# Test coverage — Design/Certification gate governance

## Critical paths

| Path | Risk | Visible coverage | Status |
|---|---|---|---|
| Historical run without assurance v1 | Retroactive breakage | `test_historical_run_without_assurance_remains_valid` plus existing audit run strict check | COVERED |
| Valid explicit authorization | False block | `test_assurance_v1_accepts_explicit_authorization` | COVERED |
| Missing authorization record | Implicit authorization | `test_assurance_v1_is_fail_closed_without_authorization_record` | COVERED |
| Executed run with explicit non-authorization | Unauthorized closeout | `test_not_authorized_does_not_allow_executed_closeout` | COVERED |
| Certification FAIL closeout | False final certification | `test_certification_fail_requires_handoff_and_preserves_design_result` | COVERED |
| Reopened Design FAIL closeout | False design stability | `test_design_fail_requires_handoff` | COVERED |
| Blank proof or reasons | Empty strings accepted as evidence | `test_authorized_rejects_blank_reason_and_evidence` | COVERED |
| Certification not assessed | Incomplete proof final-closes | `test_certification_not_assessed_requires_handoff` | COVERED |
| Undeclared non-applicability | Required gate bypass | `test_not_applicable_requires_profile_declaration` | COVERED |
| Declared non-applicability | False rejection of valid profile | `test_not_applicable_accepts_declared_profile` | COVERED |
| Knowledge Harvest | Accidental relocation or omission | Existing Knowledge Governance v1 fixtures | COVERED |

## Priority gaps

No blocking gap remains in the supported Core reader. External unpublished
consumers are not observable and remain outside the demonstrable boundary.

## Top tests recommended first

All ten risk-reducing tests recommended by the audit and Review Runs 01–02 are
implemented:

1. legacy fallback;
2. valid explicit authorization;
3. absent authorization;
4. executed closeout rejected when not authorized;
5. Certification FAIL requiring `HANDOFF`;
6. Design FAIL requiring `HANDOFF`;
7. blank evidence and reasons rejected.
8. Certification `NOT_ASSESSED` requiring `HANDOFF`;
9. undeclared `NOT_APPLICABLE` rejected;
10. declared profile applicability accepted.

## Evidence

- Focused suite after Review Run 02 remediation: `40 passed`.
- Full suite after remediation: `255 passed, 1 skipped`.
- Four-distribution setup smoke: `32 PASS, 0 FAIL`.

## Unknowns and limits

No claim is made about unpublished external parsers. Consumer projects were not
modified or executed, as required by scope.

## Verdict

**READY after remediation** — ASR-R01 through ASR-R06 have dedicated positive
or negative coverage. The remaining UNKNOWN is explicitly outside the
supported observable boundary.
