---
description: Post-build validation pipeline — verify that what was built matches what was specified
---

Validate the implementation that was just completed for: $@

## Objective

After a build phase (feature, refactoring, or fix), verify that the result
conforms to its specification, meets quality expectations, and is ready for
the next step. This is the product architect's landing checklist.

## Preferred Vibebackbone skills

- `2-vbb-spec-validator`
- `2-vbb-performance`
- `t-vbb-anti-slop-gate`
- `t-vbb-impact-analyzer`
- `1-vbb-code-doc-coherence-auditor`
- `4-vbb-product-changelog`

## Skill routing and chaining rule

### Phase 1 — Surface verification

Run `t-vbb-anti-slop-gate` to verify the immediate code state.

- If BLOCKED → STOP. The code does not compile or tests fail. Repair it.
- If READY_WITH_WARNINGS → record the warnings and continue.
- If READY → continue.

### Phase 2 — Conformance validation

Run `2-vbb-spec-validator` to verify that the implementation matches the
original specification.

Use the specification provided in the request or recovered from context.
If no implementation plan (intent-decomposer) exists, the validator will
reconstruct the mapping.

- If CONFORM or MOSTLY_CONFORM → continue.
- If PARTIAL → report the gaps and continue with a warning.
- If NON_CONFORM → STOP. The implementation does not match the specification.

### Phase 3 — Impact verification

Run `t-vbb-impact-analyzer` on the changes to detect unanticipated side effects.

- If NON_BREAKING → continue.
- If CONDITIONAL → report the conditions.
- If BREAKING → document the breaking changes. If PROD, STOP.

### Phase 4 — Documentation coherence audit

Run `1-vbb-code-doc-coherence-auditor` on the affected modules.

- If COHERENT → continue.
- If PARTIAL → record documentation gaps to resolve.
- If FRAGMENTED → documentation is substantially out of sync; plan remediation.

### Phase 5 — Performance audit

Run `2-vbb-performance` on the affected modules.

- If PERFORMANT or ADEQUATE → continue.
- If AT_RISK → record risks and recommended actions.
- If CRITICAL → STOP in PROD; warn in DEV.

### Phase 6 — Product changelog

Run `4-vbb-product-changelog` to produce a readable change summary.

## Required process

1. **Restate** what was built.
2. **Phase 1** — Anti-slop gate.
3. **Phase 2** — Spec validation.
4. **Phase 3** — Impact analysis.
5. **Phase 4** — Doc coherence audit.
6. **Phase 5** — Performance audit.
7. **Phase 6** — Product changelog.
8. **Final summary**: overall verdict, gaps, and next actions.

## Gate criteria — the implementation is validated when:

- [ ] Surface is clean (anti-slop READY or READY_WITH_WARNINGS)
- [ ] Specification conformance is established (CONFORM or MOSTLY_CONFORM)
- [ ] Impact is controlled (NON_BREAKING or documented CONDITIONAL)
- [ ] Documentation is coherent (COHERENT or PARTIAL with a plan)
- [ ] Performance is acceptable (PERFORMANT or ADEQUATE)
- [ ] Product changelog is generated

## Optional phases

Run these phases only when relevant:

- **Accessibility** (`2-vbb-accessibility`) — if the feature affects the UI
- **Analytics** (`2-vbb-analytics`) — if the feature has measurable user impact
- **Security** (`2-vbb-security`) — if the feature affects auth, data, or public APIs

## Blocking conditions

If a phase produces BLOCKED → do not proceed to the next phase without
resolution. Present the blocker to the architect.

If the architect accepts continuing despite a blocker → document the risk
acceptance in SESSION.md.

## Output format

- **Goal**
- **Phase 1 — Surface**: anti-slop verdict
- **Phase 2 — Conformance**: spec-validator verdict + gaps
- **Phase 3 — Impact**: impact-analyzer verdict
- **Phase 4 — Documentation**: coherence-auditor verdict
- **Phase 5 — Performance**: performance verdict
- **Phase 6 — Changelog**: product summary
- **Optional phases**: verdicts if run
- **Overall verdict**: VALIDATED / VALIDATED_WITH_CAVEATS / NEEDS_REWORK
- **Residual gaps**: remaining work
- **Next action**: release-check, handoff, or return to development

---

## Closeout sequence (mandatory — run after the global verdict)

After the post-build validation verdict:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <any files modified during validation>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> Post-build validation produces a go/no-go signal for release — do not leave artifacts uncommitted. Do not stop after the verdict. The after-building loop is not closed until git push is done.
