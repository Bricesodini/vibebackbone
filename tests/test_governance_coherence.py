"""Active governance surfaces must not contradict the durable record.

Audit findings F6 and F7. `docs/AUDIT_STATUS.md` declared `ADV-GOV-001` as
"PROPOSED, not approved and not integrated", blocked on `COND-01`, while
`docs/adr/0051-adversarial-assurance-dimension.md` carried `status: accepted`,
the canonical authority document existed, the validator was named canonical in
AGENTS.md / SYSTEM.md / CLAUDE.md, tests enforced it, and five runs had used it.
`docs/CONTEXT.md` likewise pointed at a human decision that had already been
made.

Correcting those two files repairs the state. It does not repair the mechanism
that produced the drift, which is what these tests are for: the contradiction
becomes detectable by a command instead of by someone noticing.

Scope is deliberately narrow. These tests do not judge whether a decision is
right; they only reject two shapes of statement that cannot both be true.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
ADR_DIR = REPO_ROOT / "docs" / "adr"
AUDIT_STATUS = REPO_ROOT / "docs" / "AUDIT_STATUS.md"
CONTEXT = REPO_ROOT / "docs" / "CONTEXT.md"
RUNS_DIR = REPO_ROOT / "docs" / "runs"

_FRONTMATTER_STATUS = re.compile(r"^status:\s*['\"]?([A-Za-z_-]+)", re.MULTILINE)
_PENDING_HEADING = re.compile(
    r"^#{1,6}\s*Pending governance proposals\s*$", re.MULTILINE | re.IGNORECASE
)
_RUN_REF = re.compile(r"(\d{4}-\d{2}-\d{2}_\d{4}_[a-z0-9-]+)")


def _pending_section(audit_status_text: str) -> str:
    """Text of the 'Pending governance proposals' section, quotes excluded.

    Block quotes are dropped: a `>` paragraph recording what a surface *used to*
    claim is history, not a live claim.
    """
    heading = _PENDING_HEADING.search(audit_status_text)
    if not heading:
        return ""
    rest = audit_status_text[heading.end() :]
    next_heading = re.search(r"^#{1,6}\s+\S", rest, re.MULTILINE)
    section = rest[: next_heading.start()] if next_heading else rest
    return "\n".join(
        line for line in section.splitlines() if not line.lstrip().startswith(">")
    )


def accepted_adr_runs(adr_dir: Path) -> dict:
    """Map run_id -> ADR slug, for every run cited by an accepted ADR.

    The link is taken from the ADR side because that is the one that survives.
    An AUDIT_STATUS bullet describing a proposal does not necessarily name the
    ADR it later produced — the real ADV-GOV-001 bullet named none — but the
    accepted ADR always cites the run it came from, in `related:` and in its
    body. Reading the link backwards is what makes the drift detectable.
    """
    mapping = {}
    for adr in sorted(adr_dir.glob("[0-9]*.md")):
        text = adr.read_text(encoding="utf-8")
        match = _FRONTMATTER_STATUS.search(text)
        if not match or match.group(1).lower() != "accepted":
            continue
        for run_id in set(_RUN_REF.findall(text)):
            mapping.setdefault(run_id, adr.stem)
    return mapping


def find_status_contradictions(audit_status_text: str, adr_dir: Path) -> list:
    """Return proposals still listed as pending although their ADR is accepted.

    Only the 'Pending governance proposals' section is read, and a proposal is
    matched to an ADR through the run it cites. A subject listed there whose
    originating run is cited by an accepted ADR is a parallel truth: the
    decision exists, the surface still says it does not.
    """
    section = _pending_section(audit_status_text)
    if not section.strip():
        return []

    decided_runs = accepted_adr_runs(adr_dir)
    contradictions = []
    for run_id in sorted(set(_RUN_REF.findall(section))):
        if run_id in decided_runs:
            contradictions.append(
                f"'Pending governance proposals' still cites {run_id}, but "
                f"{decided_runs[run_id]} is accepted — the decision was made"
            )
    return contradictions


def _logical_bullets(text: str) -> list:
    """Join each markdown bullet with its indented continuation lines.

    Scanning raw lines is not enough: in the real CONTEXT.md the words
    "Next action: human decision on" and the run identifier they refer to sat
    on two different lines, so a line-based checker saw neither claim whole.
    """
    bullets = []
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")) and not stripped.startswith("> "):
            if current is not None:
                bullets.append(current)
            current = stripped
        elif current is not None and line.startswith((" ", "\t")) and stripped:
            current += " " + stripped
        elif not stripped:
            if current is not None:
                bullets.append(current)
                current = None
    if current is not None:
        bullets.append(current)
    return bullets


def find_stale_pending_decisions(context_text: str, runs_dir: Path) -> list:
    """Return CONTEXT claims of a pending decision on an already-decided run.

    A decision is considered recorded when the referenced run directory holds a
    decision artifact (``03_DECISION*.md`` or ``*DECISIONS*.md``).
    """
    stale = []
    for bullet in _logical_bullets(context_text):
        lowered = bullet.lower()
        if "decision" not in lowered:
            continue
        if not any(
            marker in lowered
            for marker in ("pending", "awaiting", "next action", "blocked on")
        ):
            continue
        for run_name in set(_RUN_REF.findall(bullet)):
            run_dir = runs_dir / run_name
            if not run_dir.is_dir():
                continue
            decided = list(run_dir.glob("03_DECISION*.md")) or list(
                run_dir.glob("*DECISIONS*.md")
            )
            if decided:
                stale.append(
                    f"CONTEXT presents a decision as pending on {run_name}, but "
                    f"{decided[0].name} records it: {bullet[:110]}"
                )
    return stale


# ---------------------------------------------------------------------------
# The invariants, on the real repository
# ---------------------------------------------------------------------------


def test_audit_status_does_not_contradict_accepted_adrs():
    violations = find_status_contradictions(
        AUDIT_STATUS.read_text(encoding="utf-8"), ADR_DIR
    )
    assert violations == [], "\n  ".join(["parallel truth detected:"] + violations)


def test_context_does_not_present_a_decided_matter_as_pending():
    violations = find_stale_pending_decisions(
        CONTEXT.read_text(encoding="utf-8"), RUNS_DIR
    )
    assert violations == [], "\n  ".join(["stale pending decision:"] + violations)


# ---------------------------------------------------------------------------
# Proof that the checkers can fail
# ---------------------------------------------------------------------------


HISTORICAL_PENDING_SECTION = (
    "## Pending governance proposals\n\n"
    "- `ADV-GOV-001` — adversarial assurance dimension is `PROPOSED`, not approved\n"
    "  and not integrated. The design run maps the current cycle, records gaps\n"
    "  `AG-01`…`AG-13`, and proposes an additive assurance schema `1.1`. No\n"
    "  canon file was modified.\n"
    "- Blocking before any decision: `COND-01` — the review of the proposal is a\n"
    "  disclosed adversarial self-review.\n"
    "- Evidence:\n"
    "  [`design dossier`](runs/2026-07-28_1002_adversarial-loop-governance-design/04_DESIGN_DOSSIER.md),\n"
    "  [`closeout`](runs/2026-07-28_1002_adversarial-loop-governance-design/07_CLOSEOUT.md).\n"
    "\n## Active risks\n"
)


def _fixture_adr(adr_dir: Path, status: str, run_id: str) -> None:
    adr_dir.mkdir(exist_ok=True)
    (adr_dir / "0051-fixture.md").write_text(
        f'---\nstatus: {status}\nrelated:\n  - "docs/runs/{run_id}/"\n---\n# fixture\n',
        encoding="utf-8",
    )


def test_status_contradiction_is_detected(tmp_path):
    """The real ADV-GOV-001 text must be caught.

    This fixture is the section as it actually stood on main until 2026-07-29.
    It names no ADR at all, which is why a checker keyed on an inline ADR
    reference would have reported nothing.
    """
    adr_dir = tmp_path / "adr"
    _fixture_adr(
        adr_dir, "accepted", "2026-07-28_1002_adversarial-loop-governance-design"
    )

    violations = find_status_contradictions(HISTORICAL_PENDING_SECTION, adr_dir)
    assert len(violations) == 1, violations
    assert "2026-07-28_1002_adversarial-loop-governance-design" in violations[0]


def test_no_contradiction_when_the_adr_is_still_proposed(tmp_path):
    adr_dir = tmp_path / "adr"
    _fixture_adr(
        adr_dir, "proposed", "2026-07-28_1002_adversarial-loop-governance-design"
    )

    assert find_status_contradictions(HISTORICAL_PENDING_SECTION, adr_dir) == []


def test_historical_note_in_a_blockquote_is_not_a_live_claim(tmp_path):
    """A `>` paragraph recording past wording must not re-trigger the check."""
    adr_dir = tmp_path / "adr"
    _fixture_adr(
        adr_dir, "accepted", "2026-07-28_1002_adversarial-loop-governance-design"
    )

    text = (
        "## Pending governance proposals\n\nNone.\n\n"
        "> It was listed as not integrated until 2026-07-29, citing\n"
        "> runs/2026-07-28_1002_adversarial-loop-governance-design/.\n"
        "\n## Active risks\n"
    )
    assert find_status_contradictions(text, adr_dir) == []


def test_only_the_pending_section_is_read(tmp_path):
    """Citing a decided run elsewhere in the document is legitimate."""
    adr_dir = tmp_path / "adr"
    _fixture_adr(
        adr_dir, "accepted", "2026-07-28_1002_adversarial-loop-governance-design"
    )

    text = (
        "## Pending governance proposals\n\nNone.\n\n"
        "## Latest governance integration\n\n"
        "- Evidence: runs/2026-07-28_1002_adversarial-loop-governance-design/.\n"
    )
    assert find_status_contradictions(text, adr_dir) == []


def test_stale_pending_decision_is_detected(tmp_path):
    runs = tmp_path / "runs"
    run = runs / "2026-07-28_1200_fixture-run"
    run.mkdir(parents=True)
    (run / "M1_DECISIONS.md").write_text("# decided\n", encoding="utf-8")

    text = "- **Next action**: pending human decision on 2026-07-28_1200_fixture-run\n"
    violations = find_stale_pending_decisions(text, runs)
    assert len(violations) == 1 and "fixture-run" in violations[0], violations


def test_stale_pending_decision_is_detected_across_lines(tmp_path):
    """The claim and the run id may sit on different lines.

    This is the shape the real CONTEXT.md had: "Next action: human decision on"
    ended one line and the run reference began the next, so a line-based scan
    saw a claim with no subject and a subject with no claim.
    """
    runs = tmp_path / "runs"
    run = runs / "2026-07-28_1002_fixture-design"
    run.mkdir(parents=True)
    (run / "03_DECISION.md").write_text("# decided\n", encoding="utf-8")

    text = (
        "- **Next action**: human decision on\n"
        "  [`CANON_CHANGE_PROPOSAL.md`](runs/2026-07-28_1002_fixture-design/"
        "CANON_CHANGE_PROPOSAL.md)\n"
        "  after a distinct-actor independent review.\n"
    )
    violations = find_stale_pending_decisions(text, runs)
    assert len(violations) == 1 and "fixture-design" in violations[0], violations


def test_pending_decision_without_a_record_is_not_stale(tmp_path):
    runs = tmp_path / "runs"
    run = runs / "2026-07-28_1200_fixture-run"
    run.mkdir(parents=True)
    (run / "01_INTAKE.md").write_text("# intake\n", encoding="utf-8")

    text = "- **Next action**: pending human decision on 2026-07-28_1200_fixture-run\n"
    assert find_stale_pending_decisions(text, runs) == []
