---
run_id: "2026-08-26_local-agents-a2-remediation"
phase: "06_A2_INDEPENDENT_REVIEW"
voie: "STRUCTUREE"
adversarial_level: "A2"
review_profile: "A2 v1.2"
reviewer_role: "isolated adversarial reviewer"
status: "COMPLETE"
verdict: "PASS_ADVERSARIAL"
reviewed_at: "2026-08-26"
---

# A2 independent remediation review

## Verdict

**PASS_ADVERSARIAL** — confidence: **high**. The current uncommitted
remediation meets the A2 v1.2 attack scope assigned to this review: the
external-symlink boundary is decided before content decoding, and Git
provenance is reported for the selected `AGENTS.md` entry rather than its
resolved target. No blocking finding was independently reproduced.

## Operational isolation and inputs

- **Fresh context and role**: this review began from an isolated A2 assignment.
  The reviewer did not read prior review artifacts and did not request an
  implementer conclusion.
- **Runtime identity**: Codex reviewer process, Python `3.11.11`, repository
  `/Users/bricesodini/.codex/worktrees/a753/vibebackbone`, branch
  `codex/local-agents-bootstrap`, inspected base `d38bc3e` with the stated
  remediation still uncommitted.
- **Inputs inspected directly**: `tools/vbb-local-agents.py`,
  `tests/test_local_agents_bootstrap.py`, `docs/LOCAL_AGENT_CONTRACTS.md`, and
  this run's `01_INTAKE.md` and `04_PLAN.md`. The implementation/test/document
  diff was inspected directly with `git diff --` restricted to those three
  changed surfaces.
- **Independent production**: the tests and sentinel probe below were designed
  and executed by this reviewer; their raw outcomes are retained verbatim in
  this artifact. No implementation, test, closeout, or other file was edited.

## Evidence and raw outcomes

### Targeted regression suite

Command:

```text
pytest -q tests/test_local_agents_bootstrap.py
```

Raw outcome:

```text
........                                                                 [100%]
8 passed in 1.08s
```

This covers no contract, tracked/modified/untracked ordinary contracts,
nested-Git isolation, launch-directory precedence/root fallback, ordinary
external symlink refusal, invalid-UTF-8 external target refusal, selected-entry
provenance for an untracked symlink whose in-root target is tracked, and prompt
ordering before `SESSION.md`.

### Boundary-before-content sentinel

The reviewer created a temporary initialized Git repository with an
`AGENTS.md` symlink to an external one-byte invalid-UTF-8 target. In-process,
`Path.read_text` was replaced with a sentinel that raises if invoked. The
verifier completed normally and recorded no sentinel calls.

Command:

```text
python - <<'PY'
import importlib.util, os, subprocess, tempfile
from pathlib import Path
spec = importlib.util.spec_from_file_location('vbb_local_agents', 'tools/vbb-local-agents.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
with tempfile.TemporaryDirectory() as repo_tmp, tempfile.TemporaryDirectory() as outside_tmp:
    repo = Path(repo_tmp)
    subprocess.run(['git', '-C', str(repo), 'init', '-q'], check=True, capture_output=True)
    outside = Path(outside_tmp) / 'AGENTS.md'; outside.write_bytes(b'\\xff')
    os.symlink(outside, repo / 'AGENTS.md')
    original = Path.read_text; calls = []
    def blocked_read(self, *args, **kwargs):
        calls.append(str(self)); raise AssertionError('content read attempted before boundary decision')
    Path.read_text = blocked_read
    try: result = module.discover(repo)
    finally: Path.read_text = original
    print('status=', result['local_agent_contract_status'])
    print('detail=', result['detail']); print('read_text_calls=', calls)
PY
```

Raw outcome:

```text
status= EXTERNAL_SYMLINK
detail= contract target is outside the effective Git root
read_text_calls= []
```

This is direct evidence that the selected external target's content is not
decoded/read before the effective-Git-root boundary verdict.

### Selection, nested Git, and local runtime trace

The following independent temporary-repository probe created a tracked root
contract, an untracked launch-directory contract, and a nested Git repository
without a contract.

Raw outcome:

```text
launch entry precedence:
exit= 0
{
  "agents_md_git_state": "UNTRACKED",
  "detail": null,
  "local_agent_contract_status": "READY",
  "resolved_local_agent_contract": ".../child/AGENTS.md"
}
nested no-contract (must not inherit parent):
exit= 0
{
  "agents_md_git_state": "UNKNOWN",
  "detail": null,
  "local_agent_contract": "NONE",
  "local_agent_contract_status": "NONE",
  "resolved_local_agent_contract": null
}
```

The actual worktree trace was:

```text
{
  "agents_md_git_state": "TRACKED",
  "detail": null,
  "local_agent_contract": "/Users/bricesodini/.codex/worktrees/a753/vibebackbone/AGENTS.md",
  "local_agent_contract_status": "READY",
  "repository_root": "/Users/bricesodini/.codex/worktrees/a753/vibebackbone",
  "resolved_local_agent_contract": "/Users/bricesodini/.codex/worktrees/a753/vibebackbone/AGENTS.md"
}
```

### Static hygiene

Command:

```text
ruff check tools/vbb-local-agents.py tests/test_local_agents_bootstrap.py
ruff format --check tools/vbb-local-agents.py tests/test_local_agents_bootstrap.py
git diff --check
```

Raw outcome:

```text
All checks passed!
2 files already formatted
```

`git diff --check` exited 0 with no output.

## Independent findings

| ID | Finding | Severity | Confidence | Disposition |
|---|---|---:|---:|---|
| None | No finding reproduced within the assigned A2 v1.2 scope. | — | high | PASS |

## Declared and unexplored surfaces

Reviewed attack surfaces were limited to the assigned verifier, regression
tests, protocol, and intake/plan. Specifically exercised: no contract,
ordinary contracts, selected-entry versus resolved-target provenance, internal
selection precedence, nested Git, and invalid-UTF-8 external symlink behavior
with a content-read sentinel. Bootstrap ordering was verified both by the
existing static prompt assertions and the protocol's declared ordering.

Not explored: provider-specific bootstrap implementations outside the assigned
files, concurrent filesystem/symlink replacement (TOCTOU), non-POSIX path
semantics, Git executable failure injection, and a whole-repository or remote-CI
run. These limits do not negate this bounded remediation verdict; they remain
outside the approved A2 review surface.
