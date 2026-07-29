"""ADVERSARIAL_ASSURANCE §9 destination 6 — corpus mandatory.

Every CONFIRMED finding must produce a corpus entry, "no exception", the matrix
applying "regardless of severity".

Audit finding F4: the previous version of this file claimed to verify that
invariant and did not. Its four assertions checked that the word "corpus"
appeared in a governance document, that the word "Mandatory" appeared somewhere
in it, that a table had at least six rows, and that a directory existed. All
four passed with a permanently empty corpus and could not fail on the rule they
named.

This version checks the rule: it resolves CONFIRMED findings declared in run
closeouts to corpus entries on disk, and it proves it can fail by running the
same checker against synthetic fixtures.
"""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
RUNS_DIR = REPO_ROOT / "docs" / "runs"
CORPUS_DIR = REPO_ROOT / "tests" / "adversarial_corpus"
GATE = REPO_ROOT / "tools" / "vbb-adversarial-gate.py"

# §10: runs before this key keep their original protocol and are out of scope.
CUTOFF_RUN_KEY = "2026-07-28_1400"
_RUN_KEY_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})_(\d{4})")


def _gate_module():
    spec = importlib.util.spec_from_file_location("vbb_adversarial_gate_check", GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["vbb_adversarial_gate_check"] = module
    spec.loader.exec_module(module)
    return module


def _is_post_cutoff(run_name: str) -> bool:
    match = _RUN_KEY_RE.match(run_name)
    if not match:
        return False
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}_{match.group(4)}" >= (
        CUTOFF_RUN_KEY
    )


def _confirmed_findings(closeout_text: str):
    """Yield (finding_id, severity) for every CONFIRMED finding declared."""
    gate = _gate_module()
    block, error = gate.read_yaml_block(closeout_text, "adversarial")
    if error or not isinstance(block, dict):
        return
    adv = block.get("adversarial")
    if not isinstance(adv, dict):
        return
    findings = adv.get("findings")
    if not isinstance(findings, list):
        return
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        if str(finding.get("confidence", "")).strip().upper() != "CONFIRMED":
            continue
        finding_id = str(finding.get("id", "")).strip()
        if finding_id:
            yield finding_id, str(finding.get("severity", "")).strip()


def find_corpus_violations(runs_dir: Path, corpus_dir: Path):
    """Return CONFIRMED findings that have no corpus entry.

    This is the checker under test. It is exercised below against the real
    repository *and* against synthetic fixtures, so a green result on the
    repository is backed by a demonstration that the checker can go red.
    """
    violations = []
    if not runs_dir.exists():
        return violations
    for run_dir in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        if not _is_post_cutoff(run_dir.name):
            continue
        closeout = run_dir / "07_CLOSEOUT.md"
        if not closeout.exists():
            continue
        text = closeout.read_text(encoding="utf-8")
        for finding_id, severity in _confirmed_findings(text):
            entry = corpus_dir / f"CORPUS-{finding_id}.py"
            if not entry.exists():
                violations.append(
                    f"{run_dir.name}: CONFIRMED finding {finding_id} "
                    f"(severity {severity or 'unspecified'}) has no {entry.name}"
                )
    return violations


# ---------------------------------------------------------------------------
# The invariant, on the real repository
# ---------------------------------------------------------------------------


def test_every_confirmed_finding_has_a_corpus_entry():
    violations = find_corpus_violations(RUNS_DIR, CORPUS_DIR)
    assert violations == [], (
        "ADVERSARIAL_ASSURANCE §9 destination 6 is mandatory for every CONFIRMED "
        "finding, regardless of severity:\n  " + "\n  ".join(violations)
    )


def test_corpus_is_only_legitimately_empty_when_nothing_is_confirmed():
    """Make the current state visible instead of implicit."""
    entries = sorted(p.name for p in CORPUS_DIR.glob("CORPUS-*.py"))
    confirmed = []
    for run_dir in sorted(p for p in RUNS_DIR.iterdir() if p.is_dir()):
        closeout = run_dir / "07_CLOSEOUT.md"
        if _is_post_cutoff(run_dir.name) and closeout.exists():
            confirmed += [
                fid
                for fid, _ in _confirmed_findings(closeout.read_text(encoding="utf-8"))
            ]
    if confirmed:
        assert entries, (
            f"{len(confirmed)} CONFIRMED findings exist ({sorted(set(confirmed))}) "
            "but the corpus is empty"
        )


# ---------------------------------------------------------------------------
# Proof that the checker can fail — the part the previous version lacked
# ---------------------------------------------------------------------------


def _write_run(runs_dir: Path, name: str, findings_yaml: str) -> Path:
    run_dir = runs_dir / name
    run_dir.mkdir(parents=True)
    (run_dir / "07_CLOSEOUT.md").write_text(
        "# closeout\n\n```yaml\nadversarial:\n"
        '  level: "A2"\n'
        '  campaign_ref: "fixture"\n'
        '  corpus_version: "v1.1"\n'
        "  findings:\n" + findings_yaml + "```\n",
        encoding="utf-8",
    )
    return run_dir


CONFIRMED_S1 = (
    '    - id: "FIX-01"\n      severity: "S1"\n      confidence: "CONFIRMED"\n'
)
CONFIRMED_S3 = (
    '    - id: "FIX-03"\n      severity: "S3"\n      confidence: "CONFIRMED"\n'
)
PLAUSIBLE = '    - id: "FIX-99"\n      severity: "S1"\n      confidence: "PLAUSIBLE"\n'


def test_confirmed_without_corpus_entry_is_detected(tmp_path):
    runs = tmp_path / "runs"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    _write_run(runs, "2026-07-29_0900_fixture", CONFIRMED_S1)

    violations = find_corpus_violations(runs, corpus)
    assert len(violations) == 1 and "FIX-01" in violations[0], violations


def test_adding_the_corpus_entry_clears_the_violation(tmp_path):
    runs = tmp_path / "runs"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    _write_run(runs, "2026-07-29_0900_fixture", CONFIRMED_S1)
    assert find_corpus_violations(runs, corpus), "fixture did not reproduce"

    (corpus / "CORPUS-FIX-01.py").write_text("def test_fix_01(): pass\n")
    assert find_corpus_violations(runs, corpus) == []


def test_severity_s3_is_not_exempt(tmp_path):
    """§9: 'the matrix applies regardless of severity'."""
    runs = tmp_path / "runs"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    _write_run(runs, "2026-07-29_0900_fixture", CONFIRMED_S3)

    violations = find_corpus_violations(runs, corpus)
    assert len(violations) == 1 and "FIX-03" in violations[0], (
        f"an S3 CONFIRMED finding must still require an entry: {violations}"
    )


def test_non_confirmed_findings_do_not_require_an_entry(tmp_path):
    runs = tmp_path / "runs"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    _write_run(runs, "2026-07-29_0900_fixture", PLAUSIBLE)

    assert find_corpus_violations(runs, corpus) == []


def test_pre_cutoff_runs_are_out_of_scope(tmp_path):
    """§10: runs before 2026-07-28_1400 keep their original protocol."""
    runs = tmp_path / "runs"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    _write_run(runs, "2026-07-01_0900_legacy", CONFIRMED_S1)

    assert find_corpus_violations(runs, corpus) == []


# ---------------------------------------------------------------------------
# Surrounding contract
# ---------------------------------------------------------------------------


def test_corpus_directory_is_tracked():
    """It must exist in a clone, not only on a developer machine (F14)."""
    assert CORPUS_DIR.is_dir(), "tests/adversarial_corpus must exist"
    assert (CORPUS_DIR / ".gitkeep").exists() or any(CORPUS_DIR.glob("CORPUS-*.py")), (
        "nothing in tests/adversarial_corpus is tracked by git"
    )


def test_corpus_entries_are_actually_collected():
    """A CORPUS-*.py file must be executed, not silently skipped (F3)."""
    entries = sorted(CORPUS_DIR.glob("CORPUS-*.py"))
    if not entries:
        pytest.skip("corpus is empty")
    conftest = (CORPUS_DIR / "conftest.py").read_text(encoding="utf-8")
    assert "pytest_collect_file" in conftest, (
        "CORPUS-<id>.py matches neither test_*.py nor *_test.py; without a "
        "collection hook the corpus reports 'no tests ran' while fully populated"
    )


def test_every_entry_is_declared_in_the_index():
    index = (CORPUS_DIR / "INDEX.md").read_text(encoding="utf-8")
    for entry in sorted(CORPUS_DIR.glob("CORPUS-*.py")):
        assert entry.stem in index, f"{entry.name} is not declared in INDEX.md"
