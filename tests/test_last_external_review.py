"""M3-09 — last_external_review cadence validation (M1-04 SLA).

R2 §9 (ADVR-A2-03): templates declare `last_external_review` as required
at A2 with quarterly cadence. The validator does NOT mechanically
validate this field today.

M3-09 mandate: when adversarial.level == A2 and certification.status ==
CERTIFIED, the validator must reject closeouts whose `last_external_review`
exceeds the declared cadence (default `manual:quarterly` = 90 days).

The test uses absolute dates to avoid time-of-day flakiness. Inject the
"now" reference by writing a closeout whose `last_external_review` is
older than 90 days, expect FAIL closed.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _write_run(tmp_path: Path, body: str) -> Path:
    (tmp_path / "01_INTAKE.md").write_text("# stub intake\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(body, encoding="utf-8")
    return tmp_path


def _run_validator(run_dir: Path) -> tuple[int, str]:
    proc = subprocess.run(
        ["python", "tools/vbb-adversarial-gate.py", str(run_dir)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _passes(text: str) -> set[str]:
    return set(
        re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?PASS\s+(\S+):", text, re.MULTILINE)
    )


def _fails(text: str) -> set[str]:
    return set(
        re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?FAIL\s+(\S+):", text, re.MULTILINE)
    )


def _body(
    *,
    level: str = "A2",
    last_review: str = "2025-01-01T00:00:00Z",
    cadence: str = "manual:quarterly",
) -> str:
    """Build a v1.1 closeout body with the given values."""
    return f"""```yaml
adversarial:
  level: "{level}"
  campaign_ref: "test-canon"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared:
    - "x.py"
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  non_claim: "absence of finding is bounded evidence, never proof"
  last_external_review: "{last_review}"
  attacker_identity:
    agent: "external attacker"
    llm: "anthropic/claude-3-5-sonnet"
    provider: "anthropic"
    system_prompt_version: "attack-falsifier-v1"
    session: "sess-abc12345678"
  defender_identity:
    agent: "implementer"
    llm: "minimax/MiniMax-M3"
    provider: "minimax"
    system_prompt_version: "implementer-v1"
    session: "sess-def-12345678"
  certification:
    status: "CERTIFIED"
    cadence: "{cadence}"
```
```"""


def test_adversarial_gate_rejects_expired_external_review(tmp_path: Path):
    """last_external_review > 90 days ago (cadence=quarterly) must FAIL closed.

    2025-01-01 is well past the 90-day cadence window from any plausible
    "now" within the M3 timeframe.
    """
    run = _write_run(tmp_path, _body(last_review="2025-01-01T00:00:00Z"))
    rc, text = _run_validator(run)
    f = _fails(text)
    assert any(
        "external_review" in s.lower()
        or "external-review" in s.lower()
        or "cadence" in s.lower()
        for s in f
    ), f"expected last_external_review-related FAIL, got fails={f}"


def test_adversarial_gate_rejects_future_external_review(tmp_path: Path):
    """A future last_external_review is incoherent (date in the future).

    The validator must reject it (or at minimum flag it as invalid format).
    """
    run = _write_run(tmp_path, _body(last_review="2099-01-01T00:00:00Z"))
    rc, text = _run_validator(run)
    f = _fails(text)
    # It's sufficient to have at least one FAIL; the validator must NOT silently
    # accept a date 70 years in the future.
    assert len(f) >= 1 or rc != 0, "future last_external_review was silently accepted"


def test_adversarial_gate_validates_cadence_format(tmp_path: Path):
    """Cadence must follow the `manual:`, `cron:`, or `webhook:` format.

    An unknown cadence value must FAIL closed.
    """
    run = _write_run(tmp_path, _body(cadence="unknown:format"))
    rc, text = _run_validator(run)
    f = _fails(text)
    assert any("cadence" in s.lower() or "revocation" in s.lower() for s in f), (
        f"expected cadence-related FAIL for unknown cadence, got fails={f}"
    )
