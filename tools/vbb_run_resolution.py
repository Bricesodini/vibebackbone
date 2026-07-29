"""VBB shared run resolution (ADR-0027, TD-101).

Single source of truth for resolving "the current run" from docs/runs/,
shared by vbb-status-dashboard.py, vbb-loop-closure-check.py,
vbb-adversarial-gate.py and the CI path (which invokes those tools).

Two explicit selectors over two distinct populations — never assumed equal:

  * latest_existing_run — newest run, whole population.
    Consumer: loop-closure auto-detection (the run being worked on).
  * latest_closed_run   — newest run that has a closeout.
    Consumers: dashboard "latest runs" listing, adversarial gate --latest.

Ordering is the **run identity**: the ``YYYY-MM-DD_HHMM`` timestamp encoded in
the directory name, which is committed data. Directory mtime is used only as a
tiebreak for names that carry no parsable date.

Why not mtime (audit 2026-07-29, finding F19). The original implementation
sorted purely on ``st_mtime`` to avoid the lexical order, which mishandles mixed
naming schemes (``20260615-usage-audit`` vs ``2026-07-13_1811_slug``, TD-101).
But mtime is not chronology: in a fresh clone every directory carries the
checkout time, so the order is arbitrary. CI runs on fresh clones, so
``latest_closed_run`` there returned ``20260615-usage-audit`` — a June run with
no adversarial block — and the adversarial gate failed on the wrong run. The
defect stayed invisible while the only consumer in local CI was a non-blocking
warning. Parsing the identity fixes both problems: it is chronological *and*
immune to filesystem metadata.
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

__all__ = [
    "list_runs_chronological",
    "list_runs_by_mtime",
    "latest_existing_run",
    "latest_closed_run",
    "find_closeout",
    "run_identity_datetime",
    "resolve_explicit_run",
    "FINDING_STATES",
    "is_active_risk_status",
    "validate_expected_commit",
    "verify_bound_subject",
    "verify_certification_subject",
    "certification_identity",
    "find_duplicate_critical_arguments",
]

# Accepts the three naming schemes present in docs/runs/:
#   2026-07-30_0700_slug      2026-07-30 07:00
#   20260602_0817_slug        2026-06-02 08:17
#   20260615-usage-audit      2026-06-15 00:00
_RUN_ID_RE = re.compile(
    r"^(?P<year>\d{4})-?(?P<month>\d{2})-?(?P<day>\d{2})"
    r"(?:[_-](?P<hour>\d{2})(?P<minute>\d{2}))?"
)


def run_identity_datetime(run_dir: Path) -> Optional[datetime]:
    """Return the timestamp encoded in the run directory name, or None."""
    match = _RUN_ID_RE.match(run_dir.name)
    if not match:
        return None
    try:
        return datetime(
            int(match.group("year")),
            int(match.group("month")),
            int(match.group("day")),
            int(match.group("hour") or 0),
            int(match.group("minute") or 0),
        )
    except ValueError:
        # A name-shaped-but-impossible date (month 13, day 32) is not an identity.
        return None


def _sort_key(run_dir: Path) -> Tuple[int, float]:
    """Newest first: dated runs above undated ones, mtime only as a tiebreak."""
    identity = run_identity_datetime(run_dir)
    if identity is not None:
        return (1, identity.timestamp())
    try:
        return (0, run_dir.stat().st_mtime)
    except OSError:
        return (0, 0.0)


def list_runs_chronological(runs_dir: Path) -> List[Path]:
    """All run directories under ``runs_dir``, newest run identity first.

    Loose files (README.md, stray reports) are excluded: a run is a directory.
    """
    if not runs_dir.exists():
        return []
    run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
    run_dirs.sort(key=_sort_key, reverse=True)
    return run_dirs


def list_runs_by_mtime(runs_dir: Path) -> List[Path]:
    """Deprecated alias kept for callers written against the old name.

    The ordering is no longer mtime-based; see ``list_runs_chronological``.
    """
    return list_runs_chronological(runs_dir)


def find_closeout(run_dir: Path) -> Optional[Path]:
    """Closeout artifact of a run: canonical 07_CLOSEOUT.md first, then any
    *CLOSEOUT*.md fallback (in-progress runs that write CLOSEOUT.md before
    the standard rename). Newest match wins."""
    canonical = run_dir / "07_CLOSEOUT.md"
    if canonical.exists():
        return canonical
    matches = [p for p in run_dir.glob("*CLOSEOUT*.md") if p.is_file()]
    if not matches:
        return None
    return max(matches, key=lambda p: p.stat().st_mtime)


def latest_existing_run(runs_dir: Path) -> Optional[Path]:
    """Selector « dernier run existant » — newest run by identity,
    closed or not. Population: every run directory."""
    runs = list_runs_chronological(runs_dir)
    return runs[0] if runs else None


def latest_closed_run(runs_dir: Path) -> Optional[Path]:
    """Selector « dernier run clôturé » — newest run by identity that has
    a closeout artifact. Population: closed runs only (dashboard's)."""
    for run_dir in list_runs_chronological(runs_dir):
        if find_closeout(run_dir) is not None:
            return run_dir
    return None


def resolve_explicit_run(runs_dir: Path, raw: Path) -> Optional[Path]:
    """Resolve one explicit run argument to an exact child of ``runs_dir``.

    Bare IDs and existing path forms converge on the same canonical directory.
    A path outside ``runs_dir`` or a non-existing path with a matching basename
    is rejected instead of silently falling back to another subject.
    """
    base = runs_dir.resolve()
    if raw.is_absolute() or len(raw.parts) > 1:
        candidate = raw.resolve()
    else:
        candidate = (base / raw.name).resolve()
    if candidate.parent != base or not candidate.is_dir():
        return None
    return candidate


_YAML_FENCE_RE = re.compile(r"```(?:ya?ml)\s*\n(.*?)```", re.DOTALL)
_FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


def find_duplicate_critical_arguments(argv: List[str]) -> Optional[str]:
    """Return the first repeated subject-selecting option in ``argv``.

    ``argparse``'s scalar ``store`` action silently keeps the last occurrence
    of a repeated option.  Release identity must never depend on argument
    order, so both Core gates reject repeated selector options before parsing.
    The ``--name=value`` spelling is counted as an occurrence as well.
    """
    critical = {"--expected-commit", "--candidate-id", "--run-id", "--runs-dir"}
    seen = set()
    for token in argv:
        option = token.split("=", 1)[0] if token.startswith("--") else None
        if option in critical:
            if option in seen:
                return option
            seen.add(option)
    return None


def validate_expected_commit(
    expected_commit: Optional[str],
) -> Tuple[bool, str, Optional[str]]:
    """Validate an explicitly supplied certification SHA.

    ``None`` means the option was omitted and is therefore not a certification
    request.  Any supplied value, including the empty string, must be a full
    hexadecimal commit SHA; callers must not use truthiness for this decision.
    """
    if expected_commit is None:
        return True, "expected commit option absent", None
    normalized = expected_commit.strip().lower()
    if not _FULL_COMMIT_RE.fullmatch(normalized):
        return False, "invalid_or_empty_expected_commit", None
    return True, "valid expected commit", normalized


# Canonical lifecycle from ADVERSARIAL_ASSURANCE_GOVERNANCE.md §2. Consumers
# import it here instead of maintaining partial local state lists.
FINDING_STATES = frozenset(
    {
        "DETECTED",
        "CLASSIFIED",
        "ARBITRATED",
        "REMEDIATION_IN_PROGRESS",
        "REMEDIATED",
        "NON_REGRESSION_LOCKED",
        "GATE_UPDATED",
        "RE_AUDITED",
        "HARVESTED",
        "DEFERRED",
        "CLOSED_REMEDIATED",
        "CLOSED_ACCEPTED",
        "CLOSED_REJECTED",
        "CLOSED_DUPLICATE",
        "REOPENED",
    }
)
_TERMINAL_FINDING_STATES = frozenset(
    {
        "CLOSED_REMEDIATED",
        "CLOSED_ACCEPTED",
        "CLOSED_REJECTED",
        "CLOSED_DUPLICATE",
    }
)
_LEGACY_ACTIVE_RISK_STATUSES = frozenset({"OPEN", "MITIGATING"})


def is_active_risk_status(status: str) -> bool:
    """Return whether a risk-table status represents a non-terminal finding."""
    normalized = re.split(r"[\s—:-]", status.strip().upper(), maxsplit=1)[0]
    return normalized in _LEGACY_ACTIVE_RISK_STATUSES or (
        normalized in FINDING_STATES and normalized not in _TERMINAL_FINDING_STATES
    )


def _bound_to_from_closeout(run_dir: Path) -> Optional[Dict[str, Any]]:
    closeout = find_closeout(run_dir)
    if closeout is None:
        return None
    try:
        text = closeout.read_text(encoding="utf-8")
    except OSError:
        return None
    for match in _YAML_FENCE_RE.finditer(text):
        try:
            parsed = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(parsed, dict):
            continue
        adversarial = parsed.get("adversarial")
        if not isinstance(adversarial, dict):
            continue
        certification = adversarial.get("certification")
        if not isinstance(certification, dict):
            continue
        bound_to = certification.get("bound_to")
        if isinstance(bound_to, dict):
            return bound_to
    return None


def certification_identity(run_dir: Path) -> Optional[Dict[str, Any]]:
    """Return the non-self-referential certification identity metadata.

    A candidate must declare its run and stable candidate identifier.  The
    carrier supplies the commit being tested; the candidate must never embed
    that commit's own SHA in its certification record.
    """
    closeout = find_closeout(run_dir)
    if closeout is None:
        return None
    try:
        text = closeout.read_text(encoding="utf-8")
    except OSError:
        return None
    for match in _YAML_FENCE_RE.finditer(text):
        try:
            parsed = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(parsed, dict):
            continue
        adversarial = parsed.get("adversarial")
        if not isinstance(adversarial, dict):
            continue
        certification = adversarial.get("certification")
        if not isinstance(certification, dict):
            continue
        run_id = str(certification.get("run_id", "")).strip()
        candidate_id = str(certification.get("candidate_id", "")).strip()
        if run_id and candidate_id:
            return {"run_id": run_id, "candidate_id": candidate_id}
    return None


def verify_bound_subject(run_dir: Path, expected_commit: str) -> Tuple[bool, str]:
    """Resolve an existing historical ``certification.bound_to`` run/SHA."""
    valid, _reason, expected = validate_expected_commit(expected_commit)
    if not valid or expected is None:
        return False, "expected commit must be a full 40-character Git SHA"
    bound_to = _bound_to_from_closeout(run_dir)
    if bound_to is None:
        return False, "certification.bound_to is missing"
    bound_run = str(bound_to.get("run_id", "")).strip()
    bound_commit = str(bound_to.get("commit", "")).strip().lower()
    if bound_run != run_dir.name:
        return (
            False,
            f"bound run_id '{bound_run}' does not match explicit run '{run_dir.name}'",
        )
    if not _FULL_COMMIT_RE.fullmatch(bound_commit):
        return False, "certification.bound_to.commit must be a full Git SHA"
    if bound_commit != expected:
        return (
            False,
            f"bound commit '{bound_commit}' does not match expected commit '{expected}'",
        )
    try:
        exists = subprocess.run(
            [
                "git",
                "-C",
                str(run_dir),
                "cat-file",
                "-e",
                f"{expected}^{{commit}}",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False, "Git commit existence could not be verified"
    if exists.returncode != 0:
        return False, f"expected commit '{expected}' is not a Git commit object"
    return True, f"run_id={bound_run}, commit={bound_commit}"


def verify_certification_subject(
    run_dir: Path, expected_commit: str, expected_candidate_id: Optional[str] = None
) -> Tuple[bool, str]:
    """Certify one checkout without requiring a self-referential SHA field."""
    valid, reason, expected = validate_expected_commit(expected_commit)
    if not valid or expected is None:
        return False, reason
    identity = certification_identity(run_dir)
    if identity is None:
        return False, "certification identity metadata is missing"
    if identity["run_id"] != run_dir.name:
        return (
            False,
            f"certification run_id '{identity['run_id']}' does not match explicit run '{run_dir.name}'",
        )
    if expected_candidate_id is not None:
        requested = expected_candidate_id.strip()
        if not requested or requested != identity["candidate_id"]:
            return (
                False,
                f"candidate_id '{identity['candidate_id']}' does not match requested candidate '{requested}'",
            )
    # Legacy records may still carry bound_to. It is checked only as a
    # consistency guard; the carrier SHA and HEAD remain the certification
    # authority for the new non-self-referential contract.
    legacy_bound = _bound_to_from_closeout(run_dir)
    if legacy_bound is not None:
        legacy_commit = str(legacy_bound.get("commit", "")).strip().lower()
        if legacy_commit and legacy_commit != expected:
            return (
                False,
                f"bound commit '{legacy_commit}' does not match expected commit '{expected}'",
            )
    try:
        exists = subprocess.run(
            ["git", "-C", str(run_dir), "cat-file", "-e", f"{expected}^{{commit}}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False, "expected commit could not be verified"
    if exists.returncode != 0:
        return False, f"expected commit '{expected}' is not a Git commit object"
    try:
        head = subprocess.run(
            ["git", "-C", str(run_dir), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False, "checked-out HEAD could not be verified"
    if head.returncode != 0:
        return False, "checked-out HEAD could not be verified"
    evaluated_head = head.stdout.strip().lower()
    if evaluated_head != expected:
        return (
            False,
            f"checked-out HEAD '{evaluated_head}' does not match expected commit "
            f"'{expected}'",
        )
    return True, (
        f"run_id={identity['run_id']}, candidate_id={identity['candidate_id']}, "
        f"expected_commit={expected}, HEAD={evaluated_head}"
    )
