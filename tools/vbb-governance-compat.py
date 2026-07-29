#!/usr/bin/env python3
"""Governance Compatibility Gate (GCG) — canon proposal 2026-07-29_1021.

A canon that evolves must not make its own history automatically false. This
tool answers, for every artifact subject to a dated rule, *why* it is or is not
compliant — and refuses to let the three answers collapse into one boolean:

    current conformance  != accepted historical debt  != obtained certification

Measured state that motivated it (commit 6b0daf4): the adversarial gate ran as
``--latest``, a population of exactly one. Two runs out of thirteen passed. The
green CI was real and worthless: it reported the best sample of a failing
population.

Classification is mechanical. Where it cannot be mechanical — is this missing
evidence reconstructible? — the tool does not guess: it reads an arbitrated
disposition from the ledger, and blocks when none exists.

Anti-laundering rule (the reason the ledger is not a backdoor):
a ledger entry is honored **only** for runs that predate the birth of the tool
enforcing the rule. An artifact produced when the enforcement already existed
can never be reclassified as historical debt. That frontier is anchored on an
immutable fact — which commit introduced the checker — not on today's date.

Stdlib only, per repository convention.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

sys.path.insert(0, str(Path(__file__).parent))

from vbb_run_resolution import (  # noqa: E402
    find_closeout,
    list_runs_chronological,
    run_identity_datetime,
)

REPO_ROOT = Path(__file__).parent.parent.resolve()
RUNS_DIR = REPO_ROOT / "docs" / "runs"
LEDGER_PATH = REPO_ROOT / "docs" / "GOVERNANCE_COMPATIBILITY_LEDGER.md"

# ── Categories ──────────────────────────────────────────────────────────────
# Blocking categories stop the gate. Non-blocking ones are counted and shown:
# debt that is invisible is debt that never gets paid.

CURRENT = "CURRENT"
HISTORICAL_VALID = "HISTORICAL_VALID"
MIGRATION_AVAILABLE = "MIGRATION_AVAILABLE"
HISTORICAL_NONCOMPLIANCE = "HISTORICAL_NONCOMPLIANCE"
CURRENT_NONCOMPLIANCE = "CURRENT_NONCOMPLIANCE"
OVERCLAIM = "OVERCLAIM"
UNKNOWN = "UNKNOWN"
OUT_OF_SCOPE = "OUT_OF_SCOPE"

BLOCKING = {CURRENT_NONCOMPLIANCE, OVERCLAIM, UNKNOWN}
LEDGERABLE = {HISTORICAL_VALID, MIGRATION_AVAILABLE, HISTORICAL_NONCOMPLIANCE}

# ── Rule set: adversarial assurance 1.1 ─────────────────────────────────────
# `cutoff` — when the rule started applying (ADVERSARIAL_ASSURANCE_GOVERNANCE
# §10, cutoff_run_key 2026-07-28_1400).
# `enforcement_birth` — the run whose commit introduced the checker
# (921a780c "feat(adversarial): bootstrap assurance governance v1.1", produced
# by run 2026-07-28_2000_m2-bis). Runs at or before it could not self-apply:
# they wrote the instrument that judges them. Runs after it could.
#
# Both bounds are expressed as run identities on purpose. Mixing a git
# timestamp with a run identity would cross two clocks, and the repo has a
# known drift between them (finding F8) — a comparison across them would be
# arbitrary in exactly the way this tool exists to prevent.

ADVERSARIAL_CUTOFF = datetime(2026, 7, 28, 14, 0)
ADVERSARIAL_ENFORCEMENT_BIRTH = datetime(2026, 7, 28, 20, 0)
ENFORCEMENT_BIRTH_PROVENANCE = (
    "git 921a780ccf8299bc37099b377ce4e7d0d8ba2561 "
    "'feat(adversarial): bootstrap assurance governance v1.1' "
    "-> run 2026-07-28_2000_m2-bis-adversarial-loop-bootstrap-deployment"
)

# A positive claim is what makes an artifact dangerous rather than merely
# incomplete. An omission is inert; an unsupported PASS is read and believed.
_POSITIVE_CLAIM_RE = re.compile(
    r"^\s*(?:adversarial_status|certification_status)\s*:\s*"
    r"['\"]?(PASS_ADVERSARIAL|CERTIFIED)\b",
    re.MULTILINE,
)
_ADVERSARIAL_BLOCK_RE = re.compile(r"^adversarial:\s*$", re.MULTILINE)


class Classification(NamedTuple):
    run_id: str
    category: str
    reason: str
    gate_exit: Optional[int]


def _run_adversarial_gate(run_dir: Path) -> int:
    """Exit code of the existing adversarial gate on one run."""
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "vbb-adversarial-gate.py"),
            str(run_dir),
            "--strict",
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    return result.returncode


def load_ledger(path: Path = LEDGER_PATH) -> Dict[str, str]:
    """Arbitrated dispositions, as ``run_id -> category``.

    The ledger records decisions a human made about evidence the tool cannot
    weigh. It is a table in Markdown, not YAML, because it is meant to be read
    and contested by people: every row must carry a justification, and the
    justification is the point.
    """
    if not path.exists():
        return {}
    ledger: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        run_id, category = cells[0], cells[1]
        if category in LEDGERABLE and re.match(r"^\d{4}-\d{2}-\d{2}", run_id):
            ledger[run_id] = category
    return ledger


def classify_run(run_dir: Path, ledger: Dict[str, str]) -> Classification:
    """Classify one run against the adversarial 1.1 rule set."""
    run_id = run_dir.name
    identity = run_identity_datetime(run_dir)

    if identity is None:
        return Classification(run_id, UNKNOWN, "run identity is not parsable", None)

    if identity < ADVERSARIAL_CUTOFF:
        return Classification(
            run_id,
            HISTORICAL_VALID,
            "predates the adversarial 1.1 cutoff (2026-07-28_1400)",
            None,
        )

    closeout = find_closeout(run_dir)
    if closeout is None:
        return Classification(
            run_id,
            OUT_OF_SCOPE,
            "run is still open (no closeout artifact)",
            None,
        )

    gate_exit = _run_adversarial_gate(run_dir)
    if gate_exit == 0:
        return Classification(run_id, CURRENT, "adversarial gate passes", gate_exit)

    text = closeout.read_text(encoding="utf-8")
    claim = _POSITIVE_CLAIM_RE.search(text)
    has_block = bool(_ADVERSARIAL_BLOCK_RE.search(text))

    # An unsupported positive claim outranks every other reading, including the
    # historical one. Age does not make a false PASS less believed.
    if claim and not has_block:
        return Classification(
            run_id,
            OVERCLAIM,
            f"declares {claim.group(1)} with no validatable adversarial block",
            gate_exit,
        )

    if identity > ADVERSARIAL_ENFORCEMENT_BIRTH:
        # The checker already existed when this run closed. Whatever the reason
        # for the failure, it is a defect of now, repairable now — never debt.
        return Classification(
            run_id,
            CURRENT_NONCOMPLIANCE,
            "postdates enforcement birth: the checker existed when this run closed",
            gate_exit,
        )

    ledgered = ledger.get(run_id)
    if ledgered:
        return Classification(
            run_id,
            ledgered,
            "arbitrated disposition recorded in the ledger",
            gate_exit,
        )

    return Classification(
        run_id,
        UNKNOWN,
        "predates enforcement birth and carries no arbitrated disposition",
        gate_exit,
    )


def classify_all(runs_dir: Path = RUNS_DIR) -> List[Classification]:
    ledger = load_ledger()
    runs = sorted(list_runs_chronological(runs_dir), key=lambda p: p.name)
    return [classify_run(run_dir, ledger) for run_dir in runs]


def build_act(results: List[Classification]) -> dict:
    """The Governance Compatibility Act — three readings, never derived
    from one another."""
    counts: Dict[str, int] = {}
    for item in results:
        counts[item.category] = counts.get(item.category, 0) + 1

    applicable = [
        r for r in results if r.category not in (HISTORICAL_VALID, OUT_OF_SCOPE)
    ]
    blocking = [r for r in results if r.category in BLOCKING]

    return {
        "rule_set": "adversarial-assurance-1.1",
        "cutoff": ADVERSARIAL_CUTOFF.strftime("%Y-%m-%d_%H%M"),
        "enforcement_birth": ADVERSARIAL_ENFORCEMENT_BIRTH.strftime("%Y-%m-%d_%H%M"),
        "enforcement_birth_provenance": ENFORCEMENT_BIRTH_PROVENANCE,
        "population_total": len(results),
        "population_applicable": len(applicable),
        "counts": counts,
        # Reading 1 — current conformance.
        "current_conformance": f"{counts.get(CURRENT, 0)}/{len(applicable)}",
        # Reading 2 — historical debt, registered and counted, never hidden.
        "historical_debt": counts.get(HISTORICAL_NONCOMPLIANCE, 0)
        + counts.get(MIGRATION_AVAILABLE, 0),
        # Reading 3 — certification is NOT computed here. A green gate has never
        # been evidence of certification, and deriving it would be the exact
        # collapse this tool exists to prevent.
        "certification": "NOT_DERIVABLE_FROM_THIS_GATE",
        "blocking": [
            {"run_id": r.run_id, "category": r.category, "reason": r.reason}
            for r in blocking
        ],
        "verdict": "FAIL" if blocking else "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="vbb-governance-compat",
        description="Governance Compatibility Gate — classify artifacts against dated rules.",
    )
    parser.add_argument("--json", action="store_true", help="emit the act as JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 2 when any artifact falls in a blocking category",
    )
    args = parser.parse_args()

    results = classify_all()
    act = build_act(results)

    if args.json:
        print(json.dumps(act, indent=2))
    else:
        print("=== Governance Compatibility Act ===")
        print(f"rule set          : {act['rule_set']}")
        print(f"cutoff            : {act['cutoff']}")
        print(f"enforcement birth : {act['enforcement_birth']}")
        print()
        for item in results:
            if item.category in (HISTORICAL_VALID, OUT_OF_SCOPE):
                continue
            mark = "BLOCK" if item.category in BLOCKING else "  ok "
            print(f"  [{mark}] {item.category:<26} {item.run_id}")
            print(f"           {item.reason}")
        print()
        print(f"current conformance : {act['current_conformance']}")
        print(f"historical debt     : {act['historical_debt']} registered")
        print(f"certification       : {act['certification']}")
        print(f"verdict             : {act['verdict']}")

    if act["verdict"] == "FAIL" and args.strict:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
