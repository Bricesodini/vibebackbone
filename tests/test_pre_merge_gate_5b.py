"""Pre-merge gate 5b must exist in one executable form, in three places.

Audit findings F3 and F5.

F5 — the canonical shell block in docs/REFERENCE/pre-merge-gate.md wrapped both
5b lines in `[ "$(adversarial_governance_cutoff_state)" = "pre-cutoff" ]`. That
function exists nowhere in the repository, so the substitution failed, the
comparison was false and the `&&` chain aborted whatever the state. The block
presented as canonical bash had never been runnable.

F3 — neither scripts/vbb-ci-local.sh nor .github/workflows/vbb-contracts.yml ran
the adversarial gate or the corpus, so the obligation had no carrier at all.

These tests keep the documented block executable and keep the three surfaces
calling the same interface.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
GATE_DOC = REPO_ROOT / "docs" / "REFERENCE" / "pre-merge-gate.md"
CI_LOCAL = REPO_ROOT / "scripts" / "vbb-ci-local.sh"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "vbb-contracts.yml"

ADVERSARIAL_GATE = "tools/vbb-adversarial-gate.py"
CORPUS_TARGET = "tests/adversarial_corpus/"


def _canonical_block() -> str:
    """Return the fenced bash block below the canonical-block heading."""
    text = GATE_DOC.read_text(encoding="utf-8")
    heading = re.search(r"^##\s+Bloc shell canonique\s*$", text, re.MULTILINE)
    assert heading, "canonical block heading not found in pre-merge-gate.md"
    fence = re.search(r"```bash\n(.*?)```", text[heading.end() :], re.DOTALL)
    assert fence, "no bash fence under the canonical block heading"
    return fence.group(1)


def test_canonical_block_has_no_undefined_command_substitution():
    """Every $(...) in the block must resolve to something that exists."""
    block = _canonical_block()
    substitutions = re.findall(r"\$\(([^)]*)\)", block)
    for sub in substitutions:
        command = sub.strip().split()[0] if sub.strip() else ""
        assert command, f"empty command substitution in the canonical block: {sub!r}"
        resolvable = shutil.which(command) is not None or (REPO_ROOT / command).exists()
        assert resolvable, (
            f"canonical block calls {command!r}, which is neither an executable "
            f"nor a repository path — the block is not runnable"
        )


def test_canonical_block_does_not_reference_the_removed_cutoff_helper():
    """Regression for F5: the phantom helper must not come back."""
    assert "adversarial_governance_cutoff_state" not in _canonical_block(), (
        "the canonical block references a helper that does not exist"
    )


def test_canonical_block_scripts_are_syntactically_valid():
    """The block must at least parse as bash with RUN_ID substituted."""
    block = _canonical_block().replace("<run_id>", "dummy-run-id")
    result = subprocess.run(["bash", "-n"], input=block, capture_output=True, text=True)
    assert result.returncode == 0, (
        f"canonical block is not valid bash:\n{result.stderr}"
    )


def test_canonical_block_uses_one_interpreter():
    """No bare `pytest`: every line must run under the same interpreter.

    Regression for F20. The block mixed `python -m pytest` and a bare `pytest`,
    which resolves to the first shim on PATH. Where `python` is 3.11 and the
    `pytest` shim is 3.13, the block died on ModuleNotFoundError for yaml —
    a failure with no relation to the state being gated.
    """
    for line in _canonical_block().splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        assert not re.match(r"^\(?\s*pytest\b", stripped), (
            f"bare pytest invocation in the canonical block: {stripped!r}; "
            "use `python -m pytest` so the interpreter is the same throughout"
        )


def test_canonical_block_invokes_both_halves_of_5b():
    block = _canonical_block()
    assert ADVERSARIAL_GATE in block, "5b adversarial gate missing from the block"
    assert CORPUS_TARGET in block, "5b corpus execution missing from the block"


def test_local_ci_runs_both_halves_of_5b():
    ci = CI_LOCAL.read_text(encoding="utf-8")
    assert ADVERSARIAL_GATE in ci, "local CI does not run the adversarial gate"
    assert CORPUS_TARGET in ci, "local CI does not run the adversarial corpus"


def test_remote_ci_runs_both_halves_of_5b():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert ADVERSARIAL_GATE in workflow, "remote CI does not run the adversarial gate"
    assert CORPUS_TARGET in workflow, "remote CI does not run the adversarial corpus"


def test_local_and_remote_ci_use_the_same_5b_interface():
    """The two CI surfaces must call the gate with the same flags."""
    ci = CI_LOCAL.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(ADVERSARIAL_GATE) + r"([^\n]*)")

    local_flags = {m.group(1).strip() for m in pattern.finditer(ci)}
    remote_flags = {m.group(1).strip() for m in pattern.finditer(workflow)}
    assert local_flags, "no adversarial gate invocation found in local CI"
    assert remote_flags, "no adversarial gate invocation found in remote CI"
    assert local_flags == remote_flags, (
        f"local CI calls the gate with {local_flags}, remote CI with "
        f"{remote_flags} — the two surfaces have drifted"
    )


def test_empty_corpus_exits_zero_for_a_corpus_scoped_run():
    """An empty corpus is legitimate and must not break the `&&` chain."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", CORPUS_TARGET, "-q"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"corpus-scoped run exited {result.returncode}; pre-merge gate 5b would "
        f"abort:\n{result.stdout}\n{result.stderr}"
    )


def test_whole_suite_collecting_nothing_still_fails():
    """The exit-5 override must stay scoped to corpus-only invocations."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "-k", "zzz_no_such_test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 5, (
        "a whole-suite run that collects nothing must still report exit 5, "
        f"got {result.returncode}"
    )
