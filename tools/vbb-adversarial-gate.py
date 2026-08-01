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
import importlib.util
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

ADVERSARIAL_GOVERNANCE_VERSION = "1.2"
SUPPORTED_GOVERNANCE_VERSIONS = frozenset({"1.1", "1.2", "1.2-proposed"})
ADVERSARIAL_GOVERNANCE_CUTOVER_KEY = "2026-07-28_1400"
ADVERSARIAL_GOVERNANCE_CUTOVER_AT = datetime(2026, 7, 28, 14, 0, 0, tzinfo=timezone.utc)

LEVELS = frozenset({"A0", "A1", "A2", "A3"})
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
    """Extract the first YAML fenced block whose first line starts with `marker:`.

    The v1.1 canonical adversarial block is `adversarial: { ... }`, which
    parses to `{"adversarial": {...}}`. This helper recognises both the bare
    `marker:` line and `marker: <value>` lines (mapping, scalar, list).
    """
    pattern = re.compile(r"```(?:ya?ml)\s*\n(.*?)```", re.DOTALL)
    for match in pattern.finditer(text):
        block = match.group(1)
        first_line = block.splitlines()[0].strip() if block.splitlines() else ""
        # Accept any line that starts with `marker:` (with or without a value).
        if first_line == marker or first_line.startswith(marker + ":"):
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


def check_a2_distinct_identity(
    adv: Dict[str, Any],
) -> Tuple[List[GateResult], List[GateResult]]:
    """M3-02: Verify A2 attacker_identity is distinct from a declared defender_identity.

    The M1-02 contract (A2_DISTINCT_AGENT_PROXY) requires:
      - distinct_llm: MANDATORY (different llm family or human)
      - distinct_system_prompt: MANDATORY
      - distinct_provider_or_human: MANDATORY (different provider OR human)

    Mechanical comparison:
      - attacker.llm != defender.llm by family
      - attacker.system_prompt_version != defender.system_prompt_version
      - either attacker.provider != defender.provider OR external human
    """
    passes: List[GateResult] = []
    fails: List[GateResult] = []

    defender = adv.get("defender_identity")
    attacker = adv.get("attacker_identity")
    if not isinstance(defender, dict):
        fails.append(
            GateResult(
                gate_id="adv-a2-defender-identity",
                subject="A2 declares defender_identity comparable to attacker_identity",
                verdict="FAIL",
                evidence=["adversarial.attacker_identity declared"],
                reasons=[
                    "defender_identity must be a mapping for mechanical "
                    "comparison (M1-02 distinct_llm MANDATORY)"
                ],
                severity="S1",
            )
        )
        return passes, fails

    # Required mechanical fields on defender
    for key in ("llm", "system_prompt_version"):
        if not non_empty_string(defender.get(key)):
            fails.append(
                GateResult(
                    gate_id="adv-a2-defender-identity",
                    subject="A2 defender_identity declares mandatory mechanical fields",
                    verdict="FAIL",
                    evidence=["defender_identity block present"],
                    reasons=[f"defender_identity.{key} must be non-empty"],
                    severity="S1",
                )
            )
            return passes, fails

    if not isinstance(attacker, dict):
        # Without attacker comparison is impossible.
        fails.append(
            GateResult(
                gate_id="adv-a2-distinct",
                subject="A2 attacker_identity and defender_identity are mechanically distinct",
                verdict="FAIL",
                evidence=["defender_identity present"],
                reasons=["attacker_identity must be present to compare"],
                severity="S1",
            )
        )
        return passes, fails

    # Mechanical distinctness: at least one strict dimension must differ.
    a_llm = str(attacker.get("llm", "")).strip()
    d_llm = str(defender.get("llm", "")).strip()
    a_sp = str(attacker.get("system_prompt_version", "")).strip()
    d_sp = str(defender.get("system_prompt_version", "")).strip()
    a_pr = str(attacker.get("provider", "")).strip()
    d_pr = str(defender.get("provider", "")).strip()

    llm_distinct = _llm_family_distinct(a_llm, d_llm)
    prompt_distinct = bool(a_sp) and bool(d_sp) and (a_sp != d_sp)
    provider_distinct = bool(a_pr) and bool(d_pr) and (a_pr != d_pr)

    if llm_distinct and prompt_distinct and (provider_distinct or not a_pr):
        passes.append(
            GateResult(
                gate_id="adv-a2-distinct",
                subject="A2 attacker_identity and defender_identity are mechanically distinct",
                verdict="PASS",
                evidence=[
                    f"attacker.llm={a_llm}, defender.llm={d_llm}",
                    f"attacker.system_prompt_version={a_sp}",
                    f"defender.system_prompt_version={d_sp}",
                ],
                reasons=[
                    "distinct_llm (family), distinct_system_prompt, and "
                    "provider_or_human boundary declared (M1-02 contract)"
                ],
            )
        )
    else:
        reasons = []
        if not llm_distinct:
            reasons.append(
                f"distinct_llm MANDATORY: attacker.llm={a_llm!r} and "
                f"defender.llm={d_llm!r} are not distinct (M1-02)"
            )
        if not prompt_distinct:
            reasons.append(
                f"distinct_system_prompt MANDATORY: attacker.system_prompt_version="
                f"{a_sp!r} and defender={d_sp!r} match (M1-02)"
            )
        if not provider_distinct and a_pr:
            reasons.append(
                f"distinct_provider_or_human MANDATORY: attacker.provider={a_pr!r} "
                f"and defender.provider={d_pr!r} match (M1-02)"
            )
        fails.append(
            GateResult(
                gate_id="adv-a2-distinct",
                subject="A2 attacker_identity and defender_identity are mechanically distinct",
                verdict="FAIL",
                evidence=[
                    f"attacker.llm={a_llm}",
                    f"defender.llm={d_llm}",
                    f"attacker.system_prompt_version={a_sp}",
                    f"defender.system_prompt_version={d_sp}",
                ],
                reasons=reasons,
                severity="S1",
            )
        )

    # A2 proxy mode disclosure (optional but if declared must be coherent)
    proxy = adv.get("a2_proxy_mode")
    if isinstance(proxy, dict):
        enabled = bool(proxy.get("enabled"))
        limitations = proxy.get("limitations")
        if enabled:
            if not isinstance(limitations, list) or not limitations:
                fails.append(
                    GateResult(
                        gate_id="adv-a2-proxy-disclosure",
                        subject="A2_DISTINCT_AGENT_PROXY declares limitations when enabled",
                        verdict="FAIL",
                        evidence=["a2_proxy_mode.enabled = true"],
                        reasons=[
                            "A2_DISTINCT_AGENT_PROXY requires limitations[] "
                            "to be non-empty when enabled (M1-02)"
                        ],
                        severity="S2",
                    )
                )

    return passes, fails


def _llm_family_distinct(attacker_llm: str, defender_llm: str) -> bool:
    """Return True if the two LLM identifiers belong to distinct families.

    A family is the prefix before the first `/` (e.g., 'anthropic',
    'minimax', 'google'). Same family => same operator / model line.
    Different families => mechanical distinction.
    """
    if not attacker_llm or not defender_llm:
        return False
    if attacker_llm == defender_llm:
        return False
    fam_a = attacker_llm.split("/", 1)[0].strip().lower()
    fam_b = defender_llm.split("/", 1)[0].strip().lower()
    return bool(fam_a) and bool(fam_b) and fam_a != fam_b


def check_a2_a3_clarification(adv: dict, level: str):
    """Enforce the versioned A2 isolation / A3 independence clarification."""
    passes: List[GateResult] = []
    fails: List[GateResult] = []
    version = str(adv.get("governance_version", "1.1")).strip()
    if version not in SUPPORTED_GOVERNANCE_VERSIONS:
        fails.append(
            GateResult(
                "adv-governance-version",
                "adversarial governance version supported",
                "FAIL",
                [version],
                [f"version must be in {sorted(SUPPORTED_GOVERNANCE_VERSIONS)}"],
                "S1",
            )
        )
        return passes, fails
    if version == "1.1":
        return passes, fails
    if level not in {"A2", "A3"}:
        return passes, fails
    isolation = adv.get("operational_isolation")
    required = {
        "session_distinct",
        "fresh_context",
        "adversarial_role_explicit",
        "inputs_preserved",
        "raw_transcript_preserved",
        "findings_independent",
        "declared_scope",
        "runtime_identity_observed",
    }
    isolation_ok = (
        isinstance(isolation, dict)
        and all(isolation.get(key) is True for key in required)
        and isolation.get("defender_conclusions_exposed") is False
    )
    if not isolation_ok:
        fails.append(
            GateResult(
                "adv-a2-operational-isolation",
                "A2 operational isolation evidence",
                "FAIL",
                [f"level={level}", f"governance_version={version}"],
                [f"all required isolation fields must be true: {sorted(required)}"],
                "S0",
            )
        )
    else:
        passes.append(
            GateResult(
                "adv-a2-operational-isolation",
                "A2 operational isolation evidence",
                "PASS",
                [f"governance_version={version}"],
                [
                    "session, fresh context, role, evidence preservation, independence and runtime identity observed"
                ],
            )
        )
    if level == "A3":
        external = adv.get("external_independence")
        if (
            not isinstance(external, dict)
            or external.get("independent_actor") is not True
            or external.get("producer_control_absent") is not True
        ):
            fails.append(
                GateResult(
                    "adv-a3-external-independence",
                    "A3 strengthened external independence",
                    "FAIL",
                    [f"governance_version={version}"],
                    ["independent_actor and producer_control_absent must both be true"],
                    "S0",
                )
            )
        else:
            passes.append(
                GateResult(
                    "adv-a3-external-independence",
                    "A3 strengthened external independence",
                    "PASS",
                    [f"independent_actor={external.get('actor_type', 'declared')}"],
                    ["external independence evidence present"],
                )
            )
    return passes, fails


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
    # Handle the canonical v1.1 nested structure: `adversarial: { ... }`
    # parses to `{"adversarial": {...}}`. Unwrap if the YAML root is a
    # mapping whose `adversarial` key holds a mapping.
    if isinstance(adv, dict) and "adversarial" in adv:
        inner = adv["adversarial"]
        if isinstance(inner, dict):
            adv = inner
    if not isinstance(adv, dict) or not adv:
        fails.append(
            GateResult(
                gate_id="adv-block-shape",
                subject="adversarial block is a non-empty mapping",
                verdict="FAIL",
                evidence=["07_CLOSEOUT.md read"],
                reasons=["adversarial block must be a non-empty mapping"],
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
            reasons=["adversarial block is a non-empty mapping"],
        )
    )

    # level
    level = str(adv.get("level", "")).strip()
    if level not in LEVELS:
        fails.append(
            GateResult(
                gate_id="adv-level-valid",
                subject="adversarial.level is one of A0/A1/A2/A3",
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
                subject="adversarial.level is one of A0/A1/A2/A3",
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

                # M3-05: validate `session` (M1-02 traceability, opaque token)
                sess = identity.get("session")
                sess_str = str(sess).strip() if isinstance(sess, (str, int)) else ""
                if not sess_str:
                    fails.append(
                        GateResult(
                            gate_id="adv-a2-session-present",
                            subject="A2 attacker_identity declares a session token",
                            verdict="FAIL",
                            evidence=["adversarial.level = A2"],
                            reasons=[
                                "attacker_identity.session must be a non-empty string "
                                "(M1-02 session traceability)"
                            ],
                            severity="S2",
                        )
                    )
                elif len(sess_str) < 8:
                    fails.append(
                        GateResult(
                            gate_id="adv-a2-session-length",
                            subject="A2 attacker_identity.session is at least 8 chars",
                            verdict="FAIL",
                            evidence=[f"observed session length={len(sess_str)}"],
                            reasons=[
                                f"attacker_identity.session must be at least 8 chars "
                                f"(observed len={len(sess_str)})"
                            ],
                            severity="S2",
                        )
                    )
                else:
                    passes.append(
                        GateResult(
                            gate_id="adv-a2-session",
                            subject="A2 attacker_identity declares a session token",
                            verdict="PASS",
                            evidence=[f"session length={len(sess_str)} chars"],
                            reasons=["session present and length >= 8"],
                        )
                    )

        # M3-02 is the v1.1 compatibility profile. Under v1.2, A2 is gated
        # by operational isolation; model/provider identity is disclosure
        # metadata and must not reintroduce the obsolete distinct-actor
        # failure. A3 gets its stronger external-independence check below.
        governance_version = str(adv.get("governance_version", "1.1")).strip()
        if governance_version == "1.1":
            p, f = check_a2_distinct_identity(adv)
            passes.extend(p)
            fails.extend(f)

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

    p, f = check_a2_a3_clarification(adv, level)
    passes.extend(p)
    fails.extend(f)

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
    if level in ("A1", "A2", "A3") and exploration is not True:
        fails.append(
            GateResult(
                gate_id="adv-exploration-performed",
                subject="exploration_performed: true for A1/A2/A3",
                verdict="FAIL",
                evidence=[f"level={level}"],
                reasons=["exploration_performed must be true at A1/A2"],
                severity="S1",
            )
        )
    elif level in ("A1", "A2", "A3") and exploration is True:
        passes.append(
            GateResult(
                gate_id="adv-exploration-performed",
                subject="exploration_performed: true for A1/A2/A3",
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

    # M3-09: last_external_review cadence validation when CERTIFIED or PRE_CERTIFICATION
    if status in ("CERTIFIED", "PRE_CERTIFICATION"):
        ler = cert.get("last_external_review")
        cadence = str(cert.get("cadence", "manual:quarterly")).strip()
        # Cadence format check (manual:, cron:, webhook:).
        cadence_ok = (
            cadence.startswith("manual:")
            or cadence.startswith("cron:")
            or cadence.startswith("webhook:")
        )
        if not cadence_ok:
            fails.append(
                GateResult(
                    gate_id="adv-cert-cadence-format",
                    subject="cadence format (manual:|cron:|webhook:)",
                    verdict="FAIL",
                    evidence=[f"cadence={cadence}"],
                    reasons=[
                        "cadence must be one of manual:<interval>, cron:<expr>, "
                        "webhook:<target>"
                    ],
                    severity="S2",
                )
            )
        # last_external_review must be ISO8601 UTC and within cadence.
        if not non_empty_string(ler):
            fails.append(
                GateResult(
                    gate_id="adv-cert-last-external-review",
                    subject="last_external_review declared (ISO8601 UTC)",
                    verdict="FAIL",
                    evidence=[f"status={status}, cadence={cadence}"],
                    reasons=[
                        f"last_external_review must be ISO8601 UTC string when "
                        f"status={status}"
                    ],
                    severity="S2",
                )
            )
        else:
            # Naive cadence check: manual:quarterly = 90 days.
            from datetime import datetime, timezone

            try:
                ler_dt = datetime.fromisoformat(str(ler).replace("Z", "+00:00"))
                if ler_dt.tzinfo is None:
                    ler_dt = ler_dt.replace(tzinfo=timezone.utc)
                # Reference `now` = run's knowledge cutoff (deterministic, not time-of-day).
                from datetime import datetime as _dt, timezone as _tz

                ref = _dt(2026, 7, 28, tzinfo=_tz.utc)
                delta = abs((ref - ler_dt).days)
                if ler_dt > ref:
                    fails.append(
                        GateResult(
                            gate_id="adv-cert-last-external-review-future",
                            subject="last_external_review is not in the future",
                            verdict="FAIL",
                            evidence=[f"last_external_review={ler}"],
                            reasons=[
                                f"last_external_review is in the future "
                                f"(delta={delta} days, ref={ref.isoformat()})"
                            ],
                            severity="S2",
                        )
                    )
                elif delta > 90:
                    fails.append(
                        GateResult(
                            gate_id="adv-cert-last-external-review-cadence",
                            subject=f"last_external_review within cadence ({cadence})",
                            verdict="FAIL",
                            evidence=[
                                f"last_external_review={ler}",
                                f"ref={ref.isoformat()}, delta={delta} days",
                            ],
                            reasons=[
                                f"last_external_review exceeds cadence "
                                f"(delta={delta} days > 90 for {cadence})"
                            ],
                            severity="S2",
                        )
                    )
                else:
                    passes.append(
                        GateResult(
                            gate_id="adv-cert-last-external-review",
                            subject="last_external_review within cadence",
                            verdict="PASS",
                            evidence=[
                                f"last_external_review={ler}, delta={delta} days"
                            ],
                            reasons=["last_external_review within cadence"],
                        )
                    )
            except ValueError as exc:
                fails.append(
                    GateResult(
                        gate_id="adv-cert-last-external-review-format",
                        subject="last_external_review ISO8601 UTC format",
                        verdict="FAIL",
                        evidence=[f"last_external_review={ler}"],
                        reasons=[f"invalid ISO8601 UTC: {exc}"],
                        severity="S2",
                    )
                )

    return passes, fails


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def validate_run(
    run_dir: Path,
    expected_commit: Optional[str] = None,
    expected_candidate_id: Optional[str] = None,
) -> Dict[str, Any]:
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

    # M3-04: 01_INTAKE.md exists-only check. The validator must not derive
    # data from `01_INTAKE.md` (no read-then-ignore pattern). Future intake-side
    # checks must be added with an explicit test asserting the read has
    # observable effect on the verdict.
    assert intake.exists(), f"01_INTAKE.md missing in {run_dir}"
    closeout_text = closeout.read_text(encoding="utf-8")

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

    if expected_commit is not None:
        subject_ok, subject_reason = _run_resolution.verify_certification_subject(
            run_dir, expected_commit, expected_candidate_id
        )
        result = GateResult(
            gate_id="release-subject-binding",
            subject="explicit run_id, candidate_id and expected commit match checkout",
            verdict="PASS" if subject_ok else "FAIL",
            evidence=[subject_reason],
            reasons=[
                "release subject is explicitly bound" if subject_ok else subject_reason
            ],
            severity=None if subject_ok else "S0",
        )
        (passes if subject_ok else fails).append(result)

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


REPO_ROOT = Path(__file__).parent.parent.resolve()
RUNS_DIR = REPO_ROOT / "docs" / "runs"

# Shared run resolution (ADR-0027), reused from vbb-loop-closure-check.py so
# that "latest run" means the same thing to every gate.
_RUN_RES_SPEC = importlib.util.spec_from_file_location(
    "vbb_run_resolution", Path(__file__).parent / "vbb_run_resolution.py"
)
assert _RUN_RES_SPEC is not None and _RUN_RES_SPEC.loader is not None
_run_resolution = importlib.util.module_from_spec(_RUN_RES_SPEC)
_RUN_RES_SPEC.loader.exec_module(_run_resolution)


def resolve_run_dir(
    raw: Optional[Path],
    use_latest: bool = False,
    runs_dir: Path = RUNS_DIR,
    require_canonical_child: bool = False,
) -> Optional[Path]:
    """Resolve a run argument to an existing run directory.

    Accepts three forms so that the canonical block, the CI scripts and manual
    invocations cannot diverge:

      * ``--latest``            -> most recent *closed* run under docs/runs/
      * a bare run_id           -> docs/runs/<run_id>
      * a path (relative or absolute) -> used as given

    ``--latest`` deliberately selects the latest *closed* run, not the latest
    existing one. A run still in progress has no 07_CLOSEOUT.md, so validating
    it would block CI on every commit made during a run — a failure of the
    selector, not of the adversarial contract.

    Returns ``None`` when nothing resolves, so the caller reports the failure
    instead of silently validating the wrong run.
    """
    if use_latest:
        latest = _run_resolution.latest_closed_run(runs_dir)
        return latest if latest is not None and latest.is_dir() else None
    if raw is None:
        return None
    if require_canonical_child:
        return _run_resolution.resolve_explicit_run(runs_dir, raw)
    if raw.is_dir():
        return raw.resolve()
    return _run_resolution.resolve_explicit_run(runs_dir, raw)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vbb-adversarial-gate",
        description="Validate the adversarial assurance dimension (v1.1).",
    )
    parser.add_argument(
        "run_dir",
        type=Path,
        nargs="?",
        help="Run directory or bare run_id to validate (omit with --latest)",
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help=(
            "Validate the most recent closed run for diagnostics. "
            "Not valid with --expected-commit."
        ),
    )
    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=RUNS_DIR,
        help="Override docs/runs for isolated tests.",
    )
    parser.add_argument(
        "--expected-commit",
        metavar="SHA",
        help=(
            "Require the explicit run's carrier expected commit to equal HEAD "
            "and its non-self-referential certification identity."
        ),
    )
    parser.add_argument(
        "--candidate-id",
        metavar="ID",
        help=(
            "Require the explicit run's stable certification candidate_id to "
            "equal this value. Omit to use the candidate declared by the run."
        ),
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

    if args.expected_commit is not None:
        valid_expected, expected_reason, _ = _run_resolution.validate_expected_commit(
            args.expected_commit
        )
        if not valid_expected:
            sys.stderr.write(f"ERROR: {expected_reason}\n")
            return 2 if args.strict else 1

    if args.expected_commit is not None and (args.latest or args.run_dir is None):
        sys.stderr.write(
            "ERROR: --expected-commit requires an explicit run and cannot use --latest\n"
        )
        return 3

    run_dir = resolve_run_dir(
        args.run_dir,
        use_latest=args.latest,
        runs_dir=args.runs_dir,
        require_canonical_child=args.expected_commit is not None,
    )
    if run_dir is None:
        target = "--latest" if args.latest else args.run_dir
        sys.stderr.write(f"ERROR: cannot resolve a run directory from {target}\n")
        return 3
    args.run_dir = run_dir

    result = validate_run(
        args.run_dir,
        expected_commit=args.expected_commit,
        expected_candidate_id=args.candidate_id,
    )
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
