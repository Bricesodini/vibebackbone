# Compatibility evidence — Additive assurance result

## Scope

Read-only inventory of supported in-repository producers, readers, fixtures
and distribution adapters. External unpublished consumers are unobservable and
remain `UNKNOWN`.

## Producer and reader inventory

Repository-wide searches, excluding historical runs and audit narratives,
found:

- `FINAL_STATUS` structured reader:
  `tools/vbb-loop-closure-check.py`;
- contract boundary enforcement:
  `tools/vbb-contract-lint.py` rejects root `verdict_mapping`;
- gate authorization producer:
  `tools/vbb-gate-check.py` owns `can_code_start`;
- dashboard: no `FINAL_STATUS` structured consumption;
- Pi/OpenCode/Codex/Claude distribution adapters: no `FINAL_STATUS`,
  `legacy_verdict`, `documentation_certification` or `design_gate` parser;
- historical fixtures: `tests/test_loop_closure.py`;
- contract fixture: `tests/test_contract_lint.py`.

Commands:

```bash
rg -n --glob '!docs/runs/**' --glob '!docs/audits/**' \
  --glob '!docs/archive/**' --glob '!*.md' \
  'FINAL_STATUS|legacy_verdict|documentation_certification|design_gate|verdict_mapping|can_code_start' .

rg -n --glob '!docs/runs/**' --glob '!docs/audits/**' \
  --glob '!docs/archive/**' \
  'FINAL_STATUS|verdict_mapping' \
  tools tests scripts distributions skills prompts docs/templates docs/*.md
```

## Reader behavior

`validate_long_run_contract()` scans YAML blocks and only treats a block as a
runtime summary when it contains `FINAL_STATUS`. Within that mapping, it reads
the canonical timing and runtime-verdict keys and does not reject unknown
siblings. A separate `ASSURANCE_STATUS` block is therefore ignored by the
current reader and cannot change the legacy runtime verdict.

This is safer than nesting an assurance scalar under `FINAL_STATUS`, and it
preserves ADR 0043 ownership.

Direct invocation against the current run:

```bash
python -c 'import importlib.util; from pathlib import Path; p=Path("tools/vbb-loop-closure-check.py"); s=importlib.util.spec_from_file_location("vbb_loop", p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.validate_long_run_contract(Path("docs/runs/2026-07-27_2117_design-certification-gates-governance-audit"), "AUDIT"))'
```

Observed result: `[]` — no runtime-contract error from the sibling assurance
evidence or the existing structured `FINAL_STATUS`.

## Historical compatibility

- Runs without `ASSURANCE_STATUS` keep their current interpretation.
- Current frontmatter and `FINAL_STATUS` keys are unchanged.
- The loop-closure reader already documents legacy acceptance.
- No historical artifact requires rewriting.
- The contract linter's rejection of implicit `verdict_mapping` remains
  unchanged.

## Distribution compatibility

The four active distributions consume shared Core governance and prompts but
contain no parser for the proposed fields. A future Core addition can therefore
be propagated once, with smoke tests in all four distributions, rather than
forked into provider-specific truth.

## Verification conclusion

Focused regression suites:

```text
pytest tests/test_loop_closure.py tests/test_contract_lint.py -q
62 passed in 10.69s
```

```yaml
supported_repository_consumers_verified: true
historical_runs_require_rewrite: false
distribution_parser_conflict_found: false
external_unpublished_consumers: UNKNOWN
compatibility_verified: true
compatibility_boundary: "supported in-repository surfaces"
```

This evidence verifies the compatibility strategy for the supported,
observable repository. It does not approve or implement the future schema.
