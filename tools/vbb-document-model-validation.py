#!/usr/bin/env python3
"""Experimental, read-only C0-C2 document model validation pilot.

This module deliberately validates fixture records, not repository files. It
does not write tags, frontmatter, projections, or source artefacts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


VERDICTS = {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}
UNKNOWN = "UNKNOWN"

AUTHORITIES = {
    "CANONICAL",
    "SCOPED_AUTHORITY",
    "NON_AUTHORITATIVE",
    "UNASSESSED",
}
LIFECYCLES = {"PROPOSED", "ACTIVE", "TRANSITIONAL", "SUPERSEDED", "RETIRED"}
TEMPORALITIES = {"CURRENT", "PAST", "FUTURE", "MULTI_PERIOD", "UNDATED"}
FUNCTIONS = {
    "NORMATIVE",
    "REFERENCE",
    "EVIDENCE",
    "DECISION_RECORD",
    "RUN_ARTIFACT",
    "GENERATED",
    "NAVIGATION",
}
LOAD_POLICIES = {"ALWAYS", "ON_ROUTE", "ON_DEMAND", "NEVER_BY_DEFAULT"}


@dataclass(frozen=True)
class ValidationInput:
    """Common experimental input/output boundary for C0-C2."""

    artifact: str
    identity: str | None
    representation: str | None
    location: str | None
    revision: str | None
    revision_basis: str | None
    ontology: Mapping[str, Any]
    contract_version: str | None
    critical_relations: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    confidence: str = "UNKNOWN"

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ValidationInput":
        return cls(
            artifact=str(value["artifact"]),
            identity=value.get("identity"),
            representation=value.get("representation"),
            location=value.get("location"),
            revision=value.get("revision"),
            revision_basis=value.get("revision_basis"),
            ontology=value.get("ontology", {}),
            contract_version=value.get("contract_version"),
            critical_relations=tuple(value.get("critical_relations", ())),
            evidence=tuple(value.get("evidence", ())),
            confidence=str(value.get("confidence", "UNKNOWN")),
        )


@dataclass(frozen=True)
class ValidationResult:
    artifact: str
    identity: str
    representation: str
    revision: str
    ontology: Mapping[str, Any]
    critical_relations: tuple[str, ...]
    contract_version: str
    verdict: str
    findings: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    confidence: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if self.verdict not in VERDICTS:
            raise ValueError(f"unsupported verdict: {self.verdict}")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _display(value: str | None) -> str:
    return value if value else UNKNOWN


def _verdict(findings: list[str], unknown: bool, *, applicable: bool = True) -> str:
    if not applicable:
        return "NOT_APPLICABLE"
    hard_findings = [finding for finding in findings if not finding.endswith("_UNKNOWN")]
    if hard_findings:
        return "FAIL"
    return "UNKNOWN" if unknown else "PASS"


def _base_result(record: ValidationInput, verdict: str, findings: list[str]) -> ValidationResult:
    return ValidationResult(
        artifact=record.artifact,
        identity=_display(record.identity),
        representation=_display(record.representation),
        revision=_display(record.revision),
        ontology=record.ontology,
        critical_relations=record.critical_relations,
        contract_version=_display(record.contract_version),
        verdict=verdict,
        findings=tuple(findings),
        evidence=record.evidence,
        confidence=record.confidence,
    )


def validate_dim(record: ValidationInput) -> ValidationResult:
    """Validate only DIM identity/representation/revision/location invariants."""

    findings: list[str] = []
    unknown = False

    if not record.representation:
        return _base_result(record, "NOT_APPLICABLE", ["REPRESENTATION_ABSENT"])

    if not record.identity:
        findings.append("ORPHAN_REPRESENTATION")
    elif record.identity == record.location:
        findings.append("LOCATION_PRESENTED_AS_IDENTITY")
    elif not record.location:
        unknown = True
        findings.append("LOCATION_UNKNOWN")

    if not record.revision:
        unknown = True
        findings.append("REVISION_UNKNOWN")
    elif record.revision_basis in {"path", "date"}:
        findings.append("REVISION_INFERRED_FROM_PATH_OR_DATE")
    elif record.revision_basis not in {"explicit", "commit", "source_metadata"}:
        unknown = True
        findings.append("REVISION_BASIS_UNKNOWN")

    verdict = _verdict(findings, unknown)
    return _base_result(record, verdict, findings)


def validate_ontology(record: ValidationInput) -> ValidationResult:
    """Validate the six established ontology dimensions and their invariants."""

    ontology = record.ontology
    findings: list[str] = []
    unknown = False
    required = (
        "authority",
        "lifecycle",
        "temporality",
        "primary_function",
        "secondary_functions",
        "load_policy",
    )

    for key in required:
        if key not in ontology or ontology[key] in (None, "", UNKNOWN):
            unknown = True
            findings.append(f"{key.upper()}_UNKNOWN")

    authority = ontology.get("authority")
    lifecycle = ontology.get("lifecycle")
    temporality = ontology.get("temporality")
    primary = ontology.get("primary_function")
    secondary = ontology.get("secondary_functions")
    load_policy = ontology.get("load_policy")

    if authority not in AUTHORITIES and authority not in (None, UNKNOWN):
        findings.append("AUTHORITY_VALUE_INVALID")
    if lifecycle not in LIFECYCLES and lifecycle not in (None, UNKNOWN):
        findings.append("LIFECYCLE_VALUE_INVALID")
    if temporality not in TEMPORALITIES and temporality not in (None, UNKNOWN):
        findings.append("TEMPORALITY_VALUE_INVALID")
    if load_policy not in LOAD_POLICIES and load_policy not in (None, UNKNOWN):
        findings.append("LOAD_POLICY_VALUE_INVALID")

    if not isinstance(primary, str):
        if primary not in (None, UNKNOWN):
            findings.append("MULTIPLE_PRIMARY_FUNCTIONS")
    elif primary not in FUNCTIONS:
        findings.append("PRIMARY_FUNCTION_VALUE_INVALID")

    if not isinstance(secondary, list):
        if secondary not in (None, UNKNOWN):
            findings.append("SECONDARY_FUNCTIONS_NOT_A_LIST")
    else:
        if len(secondary) != len(set(secondary)):
            findings.append("DUPLICATE_SECONDARY_FUNCTION")
        if primary in secondary:
            findings.append("PRIMARY_FUNCTION_REPEATED_AS_SECONDARY")
        if any(value not in FUNCTIONS for value in secondary):
            findings.append("SECONDARY_FUNCTION_VALUE_INVALID")
        if authority == "NON_AUTHORITATIVE" and "NORMATIVE" in secondary:
            findings.append("SECONDARY_NORMATIVE_HIDES_PRESCRIPTION")

    if lifecycle in {"SUPERSEDED", "RETIRED"} and load_policy == "ALWAYS":
        findings.append("RETIRED_OR_SUPERSEDED_ALWAYS_LOADED")

    verdict = _verdict(findings, unknown)
    return _base_result(record, verdict, findings)


def validate(record: ValidationInput) -> dict[str, ValidationResult]:
    """Run the pilot validators without touching the represented artefact."""

    return {"DIM": validate_dim(record), "ONTOLOGY": validate_ontology(record)}


def result_json(record: ValidationInput) -> dict[str, Any]:
    return {name: result.as_dict() for name, result in validate(record).items()}
