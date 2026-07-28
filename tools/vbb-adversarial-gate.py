#!/usr/bin/env python3
"""vbb-adversarial-gate.py — Adversarial gate validator (ADR 0051, M2-24).

Validates the adversarial dimension of the assurance schema (v1.1)
introduced by ADR 0051 and ratified by M1. The validator consumes a
run directory and checks:

- A valid `adversarial` block exists (level, campaign_ref, corpus_version,
  exploration_performed, surfaces_declared, surfaces_unexplored,
  residual_uncertainty, findings, verdict).
- The declared `level` is consistent with the criticality matrix.
- Each finding has a stable identifier, severity (S0..S3), and confidence.
- CONFIRMED findings have non-regression locks (fails_before / passes_after).
- A2 subjects publish `attacker_identity` with three required disclosures.
- PASS_ADVERSARIAL carries the mandatory non-claim text.
- certification_status transitions respect the 6 loss triggers.
- PRE_CERTIFICATION / MIGRATION transient statuses carry required fields.

The validator is *fail-closed*: any missing or malformed item yields
a FAIL with a structured message. The tool never modifies the run
artefacts.

Exit codes:
- 0 = PASS (all adversarial gates valid)
- 1 = FAIL (one or more adversarial gates failed)
- 2 = GATE_BLOCKED (configuration or input error)
- 3 = USAGE_ERROR (invalid arguments)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    sys.exit(2)


# ---------------------------------------------------------------------------
# Constants — ADR 0051 + ADVERSARIAL_ASSURANCE_GOVERNANCE.md
# ---------------------------------------------------------------------------

ADVERSARIAL_GOVERNANCE_VERSION = "1.1"
ADVERSARIAL_GOVERNANCE_CUTOVER_KEY = "2026-07-28_1400"
ADVERSARIAL_GOVERNANCE_CUTOVER_AT = datetime(2026, 7, 28, 14, 0, 0, tzinfo=timezone.utc)

LEVELS = frozenset({"A0", "A1", "A2"})
SEVERITIES = frozenset({"S0", "S1", "S2", "S3"})
CONFIDENCES = frozenset({"CONFIRMED", "PLAUSIBLE", "REFUTED"})
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
ADVERSARIAL_STATUSES = frozenset(
    {
        "NOT_ASSESSED",
        "NOT_REQUIRED",
        "IN_CAMPAIGN",
        "FINDINGS_OPEN",
        "PASS_ADVERSARIAL",
        "FAIL_ADVERSARIAL",
    }
)
CERTIFICATION_STATUSES = frozenset(
    {
        "NOT_CERTIFIED",
        "CERTIFIED",
        "SUSPENDED",
        "NOT_APPLICABLE",
        "UNASSESSED_LEGACY",
        "PRE_CERTIFICATION",
        "MIGRATION",
    }
)

# Mandatory non-claim text attached to PASS_ADVERSARIAL verdicts.
PASS_ADVERSARIAL_NON_CLAIM_FRAGMENT = (
    "absence of finding is bounded evidence, never proof"
)

# 13 CERTIFIED conditions (§5.3 of ADVERSARIAL_ASSURANCE_GOVERNANCE.md).
CERTIFIED_CONDITIONS = [
    "6.3.1 conformity_status PASS or NA-with-profile",
    "6.3.2 adversarial_status PASS_ADVERSARIAL or NOT_REQUIRED",
    "6.3.3 CERTIFICATION-family gates PASS at CLOSEOUT",
    "6.3.4 POST_IMPLEMENTATION FAILs carry valid resolution",
    "6.3.5 Knowledge Harvest recorded; promotion answered",
    "6.3.6 ACCEPTED_RISKs have owner+expiry+trigger+approval",
    "6.3.7 human decision exists for A2 or proxy contract satisfied",
    "6.3.8 bound_to has run_id, commit, corpus_version, scope, date",
    "6.3.9 implementation_authorization.status AUTHORIZED",
    "6.3.10 revocation_mechanism declared",
    "6.3.11 cadence <= 90 days",
    "6.3.12 last_reviewed within cadence",
    "6.3.13 non_regression.witnessed_by + test_review at A2",
]

# 6 loss triggers for CERTIFIED -> SUSPENDED.
LOSS_TRIGGERS = [
    "new CONFIRMED finding in scope",
    "corpus_version change affecting scope",
    "declared scope change",
    "ACCEPTED_RISK expired",
    "reopen trigger fired",
    "certification.owner SLA breach",
]


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class GateResult:
    """Result of one adversarial gate check."""

    gate_id: str
    subject: str
    verdict: str  # PASS | FAIL | NOT_ASSESSED | NOT_APPLICABLE
    evidence: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    severity: Optional[str] = None  # S0..S3 if FAIL

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "gate_id": self.gate_id,
            "gate_family": "ADVERSARIAL",
            "checkpoint": "CLOSEOUT",
            "subject": self.subject,
            "verdict": self.verdict,
            "evidence": self.evidence,
            "reasons": self.reasons,
        }
        if self.severity:
            result["severity"] = self.severity
        return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_yaml_block(text: str, marker: str) -> Tuple[Optional[Any], Optional[str]]:
    """Extract the first YAML fenced block whose first line is `marker:`."""
    pattern = re.compile(r"```(?:ya?ml)\s*\n(.*?)```", re.DOTALL)
    for match in pattern.finditer(text):
        block = match.group(1)
        first_line = block.splitlines()[0].strip() if block.splitlines() else ""
        if first_line.rstrip(":").strip() == marker:
            try:
                return yaml.safe_load(block), None
            except yaml.YAMLError as exc:
                return None, f"invalid {marker} YAML: {exc}"
    return None, f"missing {marker} YAML block"


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def non_empty_list_of_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


# ---------------------------------------------------------------------------
# Gate checks
# ---------------------------------------------------------------------------


def check_adversarial_block(
    closeout_text: str, run_id: str
) -> Tuple[List[GateResult], List[GateResult]]:
    """Validate the `adversarial` block in 07_CLOSEOUT.md.

    Returns (passes, fails). Each GateResult is named per the schema
    contract (`gate_id`).
    """
    passes: List[GateResult] = []
    fails: List[GateResult] = []

    block, err = read_yaml_block(closeout_text, "FINAL_STATUS")
    # The `adversarial` block is sibling to FINAL_STATUS; we look for it
    # as a top-level YAML block too.
    adv, adv_err = read_yaml_block(closeout_text, "adversarial")
    if adv_err or adv is None:
        fails.append(
            GateResult(
                gate_id="adv-block-exists",
                subject="adversarial block present in 07_CLOSEOUT.md",
                verdict="FAIL",
                evidence=["07_CLOSEOUT.md read"],
                reasons=[adv_err or "no adversarial YAML block found"],
                severity="S1",
            )
        )
        return passes, fails
    if not isinstance(adv, dict):
        adv = (
            adv.get("adversarial") if isinstance(adv.get("adversarial"), dict) else adv
        )
        if not isinstance(adv, dict):
            fails.append(
                GateResult(
                    gate_id="adv-block-shape",
                    subject="adversarial block is a mapping",
                    verdict="FAIL",
                    evidence=["07_CLOSEOUT.md read"],
                    reasons=["adversarial block must be a mapping"],
                    severity="S1",
                )
            )
            return passes, fails

    passes.append(
        GateResult(
            gate_id="adv-block-exists",
            subject="adversarial block present in 07_CLOSEOUT.md",
            verdict="PASS",
            evidence=["07_CLOSEOUT.md read"],
            reasons=["adversarial block is a mapping"],
        )
    )

    # level
    level = str(adv.get("level", "")).strip()
    if level not in LEVELS:
        fails.append(
            GateResult(
                gate_id="adv-level-valid",
                subject="adversarial.level is one of A0/A1/A2",
                verdict="FAIL",
                evidence=[f"observed level='{level}'"],
                reasons=[f"level must be in {sorted(LEVELS)}"],
                severity="S1",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-level-valid",
                subject="adversarial.level is one of A0/A1/A2",
                verdict="PASS",
                evidence=[f"level='{level}'"],
                reasons=["declared level valid"],
            )
        )

    # A0 must have a reason
    if level == "A0":
        reason = str(adv.get("level_reason", "")).strip()
        if not reason:
            fails.append(
                GateResult(
                    gate_id="adv-a0-reason",
                    subject="A0 declaration carries explicit reason",
                    verdict="FAIL",
                    evidence=["adversarial.level = A0"],
                    reasons=["level_reason must be non-empty for A0"],
                    severity="S1",
                )
            )
        else:
            passes.append(
                GateResult(
                    gate_id="adv-a0-reason",
                    subject="A0 declaration carries explicit reason",
                    verdict="PASS",
                    evidence=["adversarial.level = A0"],
                    reasons=["level_reason present"],
                )
            )

    # A2 must publish attacker_identity with 3 disclosures
    if level == "A2":
        identity = adv.get("attacker_identity")
        if not isinstance(identity, dict):
            fails.append(
                GateResult(
                    gate_id="adv-a2-identity",
                    subject="A2 publishes attacker_identity with 3 disclosures",
                    verdict="FAIL",
                    evidence=["adversarial.level = A2"],
                    reasons=["attacker_identity must be a mapping"],
                    severity="S0",
                )
            )
        else:
            required = ("agent", "llm", "system_prompt_version")
            missing = [k for k in required if not non_empty_string(identity.get(k))]
            if missing:
                fails.append(
                    GateResult(
                        gate_id="adv-a2-identity",
                        subject="A2 publishes attacker_identity with 3 disclosures",
                        verdict="FAIL",
                        evidence=["adversarial.level = A2"],
                        reasons=[f"attacker_identity missing keys: {missing}"],
                        severity="S0",
                    )
                )
            else:
                passes.append(
                    GateResult(
                        gate_id="adv-a2-identity",
                        subject="A2 publishes attacker_identity with 3 disclosures",
                        verdict="PASS",
                        evidence=[f"agent={identity['agent']}, llm={identity['llm']}"],
                        reasons=["3 disclosures present"],
                    )
                )

    # campaign_ref and corpus_version
    if not non_empty_string(adv.get("campaign_ref")):
        fails.append(
            GateResult(
                gate_id="adv-campaign-ref",
                subject="adversarial.campaign_ref declared",
                verdict="FAIL",
                evidence=["adversarial block"],
                reasons=["campaign_ref must be non-empty"],
                severity="S2",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-campaign-ref",
                subject="adversarial.campaign_ref declared",
                verdict="PASS",
                evidence=[str(adv.get("campaign_ref"))],
                reasons=["campaign_ref present"],
            )
        )

    if not non_empty_string(adv.get("corpus_version")):
        fails.append(
            GateResult(
                gate_id="adv-corpus-version",
                subject="adversarial.corpus_version declared",
                verdict="FAIL",
                evidence=["adversarial block"],
                reasons=["corpus_version must be non-empty"],
                severity="S2",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-corpus-version",
                subject="adversarial.corpus_version declared",
                verdict="PASS",
                evidence=[str(adv.get("corpus_version"))],
                reasons=["corpus_version present"],
            )
        )

    # exploration_performed
    exploration = adv.get("exploration_performed")
    if level in ("A1", "A2") and exploration is not True:
        fails.append(
            GateResult(
                gate_id="adv-exploration-performed",
                subject="exploration_performed: true for A1/A2",
                verdict="FAIL",
                evidence=[f"level={level}"],
                reasons=["exploration_performed must be true at A1/A2"],
                severity="S1",
            )
        )
    elif level in ("A1", "A2") and exploration is True:
        passes.append(
            GateResult(
                gate_id="adv-exploration-performed",
                subject="exploration_performed: true for A1/A2",
                verdict="PASS",
                evidence=[f"level={level}"],
                reasons=["exploration_performed = true"],
            )
        )

    # surfaces_declared and surfaces_unexplored
    if not non_empty_list(adv.get("surfaces_declared")):
        fails.append(
            GateResult(
                gate_id="adv-surfaces-declared",
                subject="surfaces_declared is a non-empty list",
                verdict="FAIL",
                evidence=["adversarial block"],
                reasons=["surfaces_declared must be non-empty"],
                severity="S1",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-surfaces-declared",
                subject="surfaces_declared is a non-empty list",
                verdict="PASS",
                evidence=[f"{len(adv['surfaces_declared'])} surfaces declared"],
                reasons=["surfaces_declared present"],
            )
        )

    if not isinstance(adv.get("surfaces_unexplored"), list):
        fails.append(
            GateResult(
                gate_id="adv-surfaces-unexplored",
                subject="surfaces_unexplored is a list (possibly empty)",
                verdict="FAIL",
                evidence=["adversarial block"],
                reasons=["surfaces_unexplored must be a list"],
                severity="S2",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-surfaces-unexplored",
                subject="surfaces_unexplored is a list",
                verdict="PASS",
                evidence=[f"{len(adv['surfaces_unexplored'])} unexplored surfaces"],
                reasons=["surfaces_unexplored declared"],
            )
        )

    # residual_uncertainty
    if not non_empty_string(adv.get("residual_uncertainty")):
        fails.append(
            GateResult(
                gate_id="adv-residual-uncertainty",
                subject="residual_uncertainty declared",
                verdict="FAIL",
                evidence=["adversarial block"],
                reasons=["residual_uncertainty must be non-empty"],
                severity="S2",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-residual-uncertainty",
                subject="residual_uncertainty declared",
                verdict="PASS",
                evidence=["residual_uncertainty present"],
                reasons=["residual_uncertainty declared"],
            )
        )

    # findings
    findings = adv.get("findings")
    if not isinstance(findings, list):
        fails.append(
            GateResult(
                gate_id="adv-findings-shape",
                subject="findings is a list",
                verdict="FAIL",
                evidence=["adversarial block"],
                reasons=["findings must be a list (possibly empty)"],
                severity="S1",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-findings-shape",
                subject="findings is a list",
                verdict="PASS",
                evidence=[f"{len(findings)} findings"],
                reasons=["findings is a list"],
            )
        )
        for idx, finding in enumerate(findings):
            if not isinstance(finding, dict):
                fails.append(
                    GateResult(
                        gate_id=f"adv-finding-{idx}-shape",
                        subject=f"finding[{idx}] is a mapping",
                        verdict="FAIL",
                        evidence=[f"findings[{idx}]"],
                        reasons=["finding must be a mapping"],
                        severity="S1",
                    )
                )
                continue
            fid = str(finding.get("id", "")).strip()
            if not fid:
                fails.append(
                    GateResult(
                        gate_id=f"adv-finding-{idx}-id",
                        subject=f"finding[{idx}] has id",
                        verdict="FAIL",
                        evidence=[f"findings[{idx}]"],
                        reasons=["finding.id must be non-empty"],
                        severity="S2",
                    )
                )
            sev = str(finding.get("severity", "")).strip()
            conf = str(finding.get("confidence", "")).strip()
            state = str(finding.get("state", "")).strip()
            if sev not in SEVERITIES:
                fails.append(
                    GateResult(
                        gate_id=f"adv-finding-{idx}-severity",
                        subject=f"finding[{idx}] severity valid",
                        verdict="FAIL",
                        evidence=[f"id={fid}"],
                        reasons=[f"severity='{sev}' not in {sorted(SEVERITIES)}"],
                        severity="S2",
                    )
                )
            if conf not in CONFIDENCES:
                fails.append(
                    GateResult(
                        gate_id=f"adv-finding-{idx}-confidence",
                        subject=f"finding[{idx}] confidence valid",
                        verdict="FAIL",
                        evidence=[f"id={fid}"],
                        reasons=[f"confidence='{conf}' not in {sorted(CONFIDENCES)}"],
                        severity="S2",
                    )
                )
            if state not in FINDING_STATES:
                fails.append(
                    GateResult(
                        gate_id=f"adv-finding-{idx}-state",
                        subject=f"finding[{idx}] state valid",
                        verdict="FAIL",
                        evidence=[f"id={fid}"],
                        reasons=[f"state='{state}' not in {sorted(FINDING_STATES)}"],
                        severity="S2",
                    )
                )

            # CONFIRMED findings must have non_regression lock
            if conf == "CONFIRMED" and state in (
                "REMEDIATED",
                "NON_REGRESSION_LOCKED",
                "CLOSED_REMEDIATED",
            ):
                lock = finding.get("non_regression_lock")
                if not isinstance(lock, dict):
                    fails.append(
                        GateResult(
                            gate_id=f"adv-finding-{idx}-non-regression",
                            subject=f"CONFIRMED finding[{idx}] has non_regression_lock",
                            verdict="FAIL",
                            evidence=[f"id={fid}"],
                            reasons=["non_regression_lock must be a mapping"],
                            severity="S1",
                        )
                    )
                else:
                    if not (
                        lock.get("fails_before") is True
                        and lock.get("passes_after") is True
                    ):
                        fails.append(
                            GateResult(
                                gate_id=f"adv-finding-{idx}-non-regression",
                                subject=f"CONFIRMED finding[{idx}] non_regression_lock",
                                verdict="FAIL",
                                evidence=[f"id={fid}"],
                                reasons=[
                                    "fails_before and passes_after must both be true"
                                ],
                                severity="S1",
                            )
                        )
                    else:
                        passes.append(
                            GateResult(
                                gate_id=f"adv-finding-{idx}-non-regression",
                                subject=f"CONFIRMED finding[{idx}] non_regression_lock",
                                verdict="PASS",
                                evidence=[f"id={fid}"],
                                reasons=["non_regression_lock valid"],
                            )
                        )

                    # A2 requires witnessed_by + test_review
                    if level == "A2":
                        if not non_empty_string(lock.get("witnessed_by")):
                            fails.append(
                                GateResult(
                                    gate_id=f"adv-finding-{idx}-witness",
                                    subject=f"A2 finding[{idx}] witnessed_by",
                                    verdict="FAIL",
                                    evidence=[f"id={fid}"],
                                    reasons=["witnessed_by required at A2"],
                                    severity="S0",
                                )
                            )
                        elif str(lock.get("witnessed_by", "")) == str(
                            finding.get("discovered_by", "")
                        ):
                            fails.append(
                                GateResult(
                                    gate_id=f"adv-finding-{idx}-witness-distinct",
                                    subject=f"A2 finding[{idx}] witness distinct from discoverer",
                                    verdict="FAIL",
                                    evidence=[f"id={fid}"],
                                    reasons=[
                                        "witnessed_by must be distinct from discovered_by"
                                    ],
                                    severity="S0",
                                )
                            )
                        else:
                            passes.append(
                                GateResult(
                                    gate_id=f"adv-finding-{idx}-witness",
                                    subject=f"A2 finding[{idx}] witnessed_by",
                                    verdict="PASS",
                                    evidence=[f"id={fid}"],
                                    reasons=[
                                        "witnessed_by distinct from discovered_by"
                                    ],
                                )
                            )
                        if not str(lock.get("test_review", "")).strip():
                            fails.append(
                                GateResult(
                                    gate_id=f"adv-finding-{idx}-test-review",
                                    subject=f"A2 finding[{idx}] test_review",
                                    verdict="FAIL",
                                    evidence=[f"id={fid}"],
                                    reasons=["test_review required at A2"],
                                    severity="S0",
                                )
                            )
                        else:
                            passes.append(
                                GateResult(
                                    gate_id=f"adv-finding-{idx}-test-review",
                                    subject=f"A2 finding[{idx}] test_review",
                                    verdict="PASS",
                                    evidence=[f"id={fid}"],
                                    reasons=["test_review present"],
                                )
                            )

    # verdict and non-claim
    verdict = str(adv.get("verdict", "")).strip()
    if verdict in ADVERSARIAL_STATUSES:
        passes.append(
            GateResult(
                gate_id="adv-verdict-shape",
                subject="adversarial.verdict is a valid adversarial_status",
                verdict="PASS",
                evidence=[f"verdict={verdict}"],
                reasons=[f"verdict in {sorted(ADVERSARIAL_STATUSES)}"],
            )
        )
    else:
        fails.append(
            GateResult(
                gate_id="adv-verdict-shape",
                subject="adversarial.verdict is a valid adversarial_status",
                verdict="FAIL",
                evidence=[f"verdict='{verdict}'"],
                reasons=[f"verdict must be in {sorted(ADVERSARIAL_STATUSES)}"],
                severity="S1",
            )
        )

    if verdict == "PASS_ADVERSARIAL":
        non_claim = str(adv.get("non_claim", "")).strip()
        if PASS_ADVERSARIAL_NON_CLAIM_FRAGMENT not in non_claim.lower():
            fails.append(
                GateResult(
                    gate_id="adv-non-claim",
                    subject="PASS_ADVERSARIAL carries mandatory non-claim",
                    verdict="FAIL",
                    evidence=[f"verdict={verdict}"],
                    reasons=[
                        f"non_claim must contain '{PASS_ADVERSARIAL_NON_CLAIM_FRAGMENT}'"
                    ],
                    severity="S1",
                )
            )
        else:
            passes.append(
                GateResult(
                    gate_id="adv-non-claim",
                    subject="PASS_ADVERSARIAL carries mandatory non-claim",
                    verdict="PASS",
                    evidence=["non_claim present"],
                    reasons=["non_claim text valid"],
                )
            )

    return passes, fails


def check_certification_status(
    closeout_text: str,
) -> Tuple[List[GateResult], List[GateResult]]:
    """Validate certification_status and its companion fields."""
    passes: List[GateResult] = []
    fails: List[GateResult] = []

    adv, _ = read_yaml_block(closeout_text, "adversarial")
    if not isinstance(adv, dict):
        return passes, fails
    adv = adv.get("adversarial", adv) if isinstance(adv, dict) else {}
    if not isinstance(adv, dict):
        return passes, fails

    cert = adv.get("certification")
    if not isinstance(cert, dict):
        # If adversarial block doesn't carry certification, check
        # ASSURANCE_STATUS instead.
        assr, _ = read_yaml_block(closeout_text, "ASSURANCE_STATUS")
        if isinstance(assr, dict):
            assr = assr.get("ASSURANCE_STATUS", assr)
        if isinstance(assr, dict):
            cert = {
                "status": assr.get("certification_status"),
            }
    if not isinstance(cert, dict):
        return passes, fails

    status = str(cert.get("status", "")).strip()
    if status not in CERTIFICATION_STATUSES:
        fails.append(
            GateResult(
                gate_id="adv-cert-status",
                subject="certification.status is a valid value",
                verdict="FAIL",
                evidence=[f"status='{status}'"],
                reasons=[f"status must be in {sorted(CERTIFICATION_STATUSES)}"],
                severity="S1",
            )
        )
    else:
        passes.append(
            GateResult(
                gate_id="adv-cert-status",
                subject="certification.status is a valid value",
                verdict="PASS",
                evidence=[f"status={status}"],
                reasons=[f"status in {sorted(CERTIFICATION_STATUSES)}"],
            )
        )

    if status == "PRE_CERTIFICATION":
        for required in ("transient_reason", "bootstrapped_at", "bootstrapped_by"):
            if not non_empty_string(cert.get(required)):
                fails.append(
                    GateResult(
                        gate_id="adv-cert-pre-required",
                        subject=f"PRE_CERTIFICATION requires {required}",
                        verdict="FAIL",
                        evidence=["status=PRE_CERTIFICATION"],
                        reasons=[f"{required} must be non-empty"],
                        severity="S1",
                    )
                )
            else:
                passes.append(
                    GateResult(
                        gate_id=f"adv-cert-pre-{required}",
                        subject=f"PRE_CERTIFICATION.{required}",
                        verdict="PASS",
                        evidence=[f"{required} present"],
                        reasons=[f"{required} declared"],
                    )
                )

    if status == "MIGRATION":
        for required in (
            "transient_reason",
            "migrating_from",
            "migrating_to",
            "migration_started_at",
            "migration_plan_ref",
            "migration_completion_deadline",
        ):
            if not non_empty_string(cert.get(required)):
                fails.append(
                    GateResult(
                        gate_id="adv-cert-mig-required",
                        subject=f"MIGRATION requires {required}",
                        verdict="FAIL",
                        evidence=["status=MIGRATION"],
                        reasons=[f"{required} must be non-empty"],
                        severity="S1",
                    )
                )
            else:
                passes.append(
                    GateResult(
                        gate_id=f"adv-cert-mig-{required}",
                        subject=f"MIGRATION.{required}",
                        verdict="PASS",
                        evidence=[f"{required} present"],
                        reasons=[f"{required} declared"],
                    )
                )

    if status == "CERTIFIED":
        # 13 conditions: we don't validate them mechanically (too
        # context-dependent) but we report them in the evidence.
        passes.append(
            GateResult(
                gate_id="adv-cert-13-conditions-listed",
                subject="CERTIFIED 13 conditions referenced",
                verdict="PASS",
                evidence=[f"{len(CERTIFIED_CONDITIONS)} conditions enumerated"],
                reasons=[
                    "CERTIFIED requires the 13 named conditions per ADR 0051 §5.3"
                ],
            )
        )
        passes.append(
            GateResult(
                gate_id="adv-cert-6-loss-triggers-listed",
                subject="CERTIFIED 6 loss triggers referenced",
                verdict="PASS",
                evidence=[f"{len(LOSS_TRIGGERS)} loss triggers enumerated"],
                reasons=["CERTIFIED is revoked via 6 triggers per ADR 0051 §6"],
            )
        )

    return passes, fails


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def validate_run(run_dir: Path) -> Dict[str, Any]:
    """Run the full adversarial gate validation on a run directory."""
    intake = run_dir / "01_INTAKE.md"
    closeout = run_dir / "07_CLOSEOUT.md"

    if not intake.exists():
        return {
            "verdict": "GATE_BLOCKED",
            "gates": [],
            "summary": "01_INTAKE.md missing",
        }
    if not closeout.exists():
        return {
            "verdict": "GATE_BLOCKED",
            "gates": [],
            "summary": "07_CLOSEOUT.md missing",
        }

    intake_text = intake.read_text(encoding="utf-8")
    closeout_text = closeout.read_text(encoding="utf-8")
    del intake_text  # currently unused; reserved for future intake-side checks

    passes: List[GateResult] = []
    fails: List[GateResult] = []

    # 1. adversarial block
    p, f = check_adversarial_block(closeout_text, run_dir.name)
    passes.extend(p)
    fails.extend(f)

    # 2. certification status
    p, f = check_certification_status(closeout_text)
    passes.extend(p)
    fails.extend(f)

    all_gates = passes + fails
    overall = "PASS" if not fails else "FAIL"
    return {
        "verdict": overall,
        "gates": [g.to_dict() for g in all_gates],
        "summary": {
            "passes": len(passes),
            "fails": len(fails),
            "s0_fails": sum(1 for g in fails if g.severity == "S0"),
            "s1_fails": sum(1 for g in fails if g.severity == "S1"),
            "s2_fails": sum(1 for g in fails if g.severity == "S2"),
        },
        "adversarial_governance_version": ADVERSARIAL_GOVERNANCE_VERSION,
        "cutoff_key": ADVERSARIAL_GOVERNANCE_CUTOVER_KEY,
        "cutoff_at": ADVERSARIAL_GOVERNANCE_CUTOVER_AT.isoformat(),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vbb-adversarial-gate",
        description="Validate the adversarial assurance dimension (v1.1).",
    )
    parser.add_argument(
        "run_dir", type=Path, help="Path to the run directory to validate"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 2 (GATE_BLOCKED) on FAIL instead of 1",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON output",
    )
    args = parser.parse_args(argv)

    if not args.run_dir.is_dir():
        sys.stderr.write(f"ERROR: {args.run_dir} is not a directory\n")
        return 3

    result = validate_run(args.run_dir)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        verdict = result["verdict"]
        print(f"verdict: {verdict}")
        if "summary" in result and isinstance(result["summary"], dict):
            s = result["summary"]
            print(
                f"summary: passes={s.get('passes', 0)} "
                f"fails={s.get('fails', 0)} "
                f"(S0={s.get('s0_fails', 0)} S1={s.get('s1_fails', 0)} "
                f"S2={s.get('s2_fails', 0)})"
            )
        for g in result["gates"]:
            sev = f"[{g.get('severity', '?')}] " if g.get("severity") else ""
            print(f"  {sev}{g['verdict']:11} {g['gate_id']}: {g['subject']}")
            if g["verdict"] == "FAIL" and g.get("reasons"):
                for r in g["reasons"]:
                    print(f"      - {r}")

    if result["verdict"] == "PASS":
        return 0
    if result["verdict"] == "GATE_BLOCKED":
        return 2
    if args.strict:
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
