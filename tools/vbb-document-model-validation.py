#!/usr/bin/env python3
"""Experimental, read-only C0-C5 document model validation pilot.

This module deliberately validates fixture records, not repository files. It
does not write tags, frontmatter, projections, or source artefacts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from typing import Any, Mapping


VERDICTS = {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}
UNKNOWN = "UNKNOWN"
COMPATIBILITY_VERDICTS = {
    "COMPATIBLE",
    "MIGRATION_REQUIRED",
    "INCOMPATIBLE",
    "UNKNOWN",
}
DGM_RELATIONS = {
    "REPRESENTED_BY",
    "REVISION_OF",
    "LOCATED_AT",
    "GENERATED_FROM",
    "PROJECTS",
    "DISTRIBUTED_TO",
    "REFERENCES",
    "GOVERNS",
    "ESTABLISHED_BY",
    "SUPPORTED_BY",
    "SUPERSEDES",
    "CONFLICTS_WITH",
}

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
FINDING_STATUSES = {
    "AWAITING_HUMAN_DECISION",
    "APPROVED_FOR_ROUTING",
    "DECLINED",
    "DEFERRED",
}
HUMAN_DECISIONS = {"OUI", "NON", "PLUS_TARD"}
ROUTES = {
    "DOCUMENTARY_CORRECTION",
    "CANON_CHANGE",
    "HISTORICAL_CLASSIFICATION",
    "ARCHIVE",
    "DELETE",
}


@dataclass(frozen=True)
class ValidationInput:
    """Common experimental input/output boundary for C0-C4."""

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
    tag: Mapping[str, Any] | None = None
    repository_contract: Mapping[str, Any] | None = None
    relations: tuple[Mapping[str, Any], ...] = ()

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
            tag=value.get("tag"),
            repository_contract=value.get("repository_contract"),
            relations=tuple(value.get("relations", ())),
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
    compatibility: str = UNKNOWN

    def __post_init__(self) -> None:
        if self.verdict not in VERDICTS:
            raise ValueError(f"unsupported verdict: {self.verdict}")
        if self.compatibility not in COMPATIBILITY_VERDICTS:
            raise ValueError(f"unsupported compatibility: {self.compatibility}")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentFinding:
    """Normalized C5 finding; routing is a proposal and never a mutation."""

    finding_id: str
    artifact: str
    identity: str
    applicable_authority: str
    source_validator: str
    discrepancy: str
    evidence: tuple[str, ...]
    potential_impact: str
    confidence: str
    human_decision_status: str = "AWAITING_HUMAN_DECISION"
    proposed_route: str | None = None
    canon_change_proposal_required: bool = False
    route_reason: str | None = None

    def __post_init__(self) -> None:
        if self.human_decision_status not in FINDING_STATUSES:
            raise ValueError(
                f"unsupported finding status: {self.human_decision_status}"
            )
        if self.proposed_route not in ROUTES | {None}:
            raise ValueError(f"unsupported route: {self.proposed_route}")
        if self.canon_change_proposal_required and self.proposed_route != "CANON_CHANGE":
            raise ValueError("canon change proposal requires CANON_CHANGE route")

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


def _with_compatibility(result: ValidationResult, compatibility: str) -> ValidationResult:
    return ValidationResult(
        **{**result.as_dict(), "compatibility": compatibility}
    )


def _tag_ontology_record(record: ValidationInput, tag: Mapping[str, Any]) -> ValidationInput:
    return ValidationInput(
        **{
            **record.__dict__,
            "ontology": tag.get("ontology", {}),
        }
    )


def validate_dts(record: ValidationInput) -> ValidationResult:
    """Compare one conceptual tag with the repository documentary contract."""

    contract = record.repository_contract
    tag = record.tag
    findings: list[str] = []

    if not contract or not contract.get("version"):
        findings.append("CONTRACT_VERSION_UNKNOWN")
        return _with_compatibility(
            _base_result(record, "UNKNOWN", findings), "UNKNOWN"
        )
    if not tag:
        findings.append("ARTIFACT_TAG_ABSENT")
        return _with_compatibility(
            _base_result(record, "UNKNOWN", findings), "UNKNOWN"
        )

    if not tag.get("identity") or not tag.get("representation"):
        findings.append("TAG_IDENTITY_OR_REPRESENTATION_UNKNOWN")
    elif tag["identity"] != record.identity or tag["representation"] != record.representation:
        findings.append("TAG_IDENTITY_OR_REPRESENTATION_MISMATCH")

    tag_contract = tag.get("contract_version")
    if not tag_contract:
        findings.append("TAG_CONTRACT_VERSION_UNKNOWN")
    else:
        current = contract["version"]
        compatible = set(contract.get("compatible_versions", ()))
        migration = set(contract.get("migration_required_versions", ()))
        if tag_contract not in {current, *compatible, *migration}:
            findings.append("TAG_CONTRACT_VERSION_INCOMPATIBLE")

    tag_record = _tag_ontology_record(record, tag)
    ontology_result = validate_ontology(tag_record)
    findings.extend(f"TAG_{finding}" for finding in ontology_result.findings)

    kind = tag.get("kind")
    if kind in {"PROJECTION", "DISTRIBUTION", "RUNTIME_ARTIFACT"}:
        if not tag.get("source"):
            findings.append("DERIVED_SOURCE_UNKNOWN")
        elif tag.get("source_exists") is False:
            findings.append("DERIVED_SOURCE_ORPHAN")
        elif tag.get("source_exists") is None:
            findings.append("DERIVED_SOURCE_UNKNOWN")

    inherited_from = tag.get("inherited_from")
    if inherited_from is not None and not isinstance(inherited_from, str):
        findings.append("INHERITANCE_NOT_TRACEABLE")

    source_revision = tag.get("source_revision")
    if source_revision is not None and tag.get("revision") != source_revision:
        findings.append("RUNTIME_OR_DISTRIBUTION_REVISION_DIVERGENT")

    runtime_divergent = "RUNTIME_OR_DISTRIBUTION_REVISION_DIVERGENT" in findings
    hard = [
        finding
        for finding in findings
        if not finding.endswith("UNKNOWN")
        and finding != "TAG_REVISION_UNKNOWN"
        and finding != "RUNTIME_OR_DISTRIBUTION_REVISION_DIVERGENT"
    ]
    unknown = any(finding.endswith("UNKNOWN") for finding in findings)
    if hard:
        compatibility = "INCOMPATIBLE"
    elif runtime_divergent or tag_contract in set(contract.get("migration_required_versions", ())):
        compatibility = "MIGRATION_REQUIRED"
    elif unknown:
        compatibility = "UNKNOWN"
    else:
        compatibility = "COMPATIBLE"

    verdict = "FAIL" if hard else ("UNKNOWN" if unknown else "PASS")
    return _with_compatibility(
        _base_result(record, verdict, findings), compatibility
    )


def _relations_of(record: ValidationInput, relation_type: str) -> list[Mapping[str, Any]]:
    return [relation for relation in record.relations if relation.get("type") == relation_type]


def validate_dgm(record: ValidationInput) -> ValidationResult:
    """Validate the bounded set of DGM relations used by the pilot."""

    findings: list[str] = []
    unknown = False
    relations = record.relations

    for relation in relations:
        if relation.get("type") not in DGM_RELATIONS:
            findings.append("RELATION_TYPE_INVALID")

    if record.representation and not record.identity:
        findings.append("REPRESENTATION_WITHOUT_IDENTITY")

    represented = _relations_of(record, "REPRESENTED_BY")
    if record.identity and record.representation:
        if not represented:
            unknown = True
            findings.append("REPRESENTED_BY_UNKNOWN")
        elif any(relation.get("target") != record.representation for relation in represented):
            findings.append("REPRESENTED_BY_TARGET_MISMATCH")

    revisions = _relations_of(record, "REVISION_OF")
    if record.revision and record.revision != UNKNOWN:
        if not revisions:
            unknown = True
            findings.append("REVISION_OF_UNKNOWN")
        elif any(relation.get("target") != record.representation for relation in revisions):
            findings.append("REVISION_OF_TARGET_MISMATCH")

    locations = _relations_of(record, "LOCATED_AT")
    if record.location:
        if not locations:
            unknown = True
            findings.append("LOCATED_AT_UNKNOWN")
        elif any(relation.get("target") != record.location for relation in locations):
            findings.append("LOCATED_AT_TARGET_MISMATCH")

    kind = (record.tag or {}).get("kind")
    source_relations = _relations_of(record, "GENERATED_FROM") + _relations_of(record, "PROJECTS")
    if kind in {"PROJECTION", "GENERATED"}:
        if not source_relations:
            unknown = True
            findings.append("PROJECTION_SOURCE_UNKNOWN")
        elif any(not relation.get("target") for relation in source_relations):
            findings.append("PROJECTION_SOURCE_ORPHAN")

    if record.ontology.get("authority") in {"CANONICAL", "SCOPED_AUTHORITY"}:
        established = _relations_of(record, "ESTABLISHED_BY")
        if not established:
            unknown = True
            findings.append("AUTHORITY_DECISION_UNKNOWN")
        elif any(not relation.get("target") for relation in established):
            findings.append("AUTHORITY_DECISION_ORPHAN")

    for relation in _relations_of(record, "CONFLICTS_WITH"):
        if relation.get("same_scope") is True:
            findings.append("AUTHORITY_CONFLICT_SAME_SCOPE")

    if record.ontology.get("lifecycle") == "ACTIVE":
        for relation in _relations_of(record, "REFERENCES"):
            if relation.get("target_lifecycle") == "SUPERSEDED":
                findings.append("ACTIVE_REFERENCE_TO_SUPERSEDED_REVISION")

    for relation in _relations_of(record, "DISTRIBUTED_TO"):
        if not relation.get("target_revision"):
            unknown = True
            findings.append("DISTRIBUTION_REVISION_UNKNOWN")
        elif record.revision and relation["target_revision"] != record.revision:
            findings.append("DISTRIBUTION_SOURCE_DIVERGENT")

    if record.ontology.get("primary_function") == "EVIDENCE" or "EVIDENCE" in record.ontology.get("secondary_functions", []):
        supported = _relations_of(record, "SUPPORTED_BY")
        if not supported:
            unknown = True
            findings.append("EVIDENCE_ATTACHMENT_UNKNOWN")
        elif any(not relation.get("target") for relation in supported):
            findings.append("EVIDENCE_ATTACHMENT_ORPHAN")

    if kind in {"DISTRIBUTION", "RUNTIME_ARTIFACT"} and not (
        source_relations or _relations_of(record, "DISTRIBUTED_TO")
    ):
        unknown = True
        findings.append("PROVENANCE_UNKNOWN")

    verdict = _verdict(findings, unknown)
    return _base_result(record, verdict, findings)


def validate(record: ValidationInput) -> dict[str, ValidationResult]:
    """Run the pilot validators without touching the represented artefact."""

    return {
        "DIM": validate_dim(record),
        "ONTOLOGY": validate_ontology(record),
        "DTS": validate_dts(record),
        "DGM": validate_dgm(record),
    }


def _stable_finding_id(
    run_id: str, record: ValidationInput, source_validator: str, discrepancy: str
) -> str:
    seed = "|".join((run_id, source_validator, record.artifact, discrepancy))
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    return f"{run_id}/{source_validator.lower()}/{digest}"


def _finding_impact(source_validator: str, discrepancy: str) -> str:
    if "CONFLICT" in discrepancy:
        return "may create competing authority for one documentary scope"
    if "SUPERSEDED" in discrepancy:
        return "may cause current reasoning to rely on a superseded revision"
    if "ORPHAN" in discrepancy or "PROVENANCE" in discrepancy:
        return "may break provenance between an artefact and its source"
    if discrepancy.endswith("UNKNOWN") or "UNKNOWN" in discrepancy:
        return "current impact cannot be determined from the available evidence"
    if source_validator == "ONTOLOGY":
        return "may make the artefact's governed interpretation ambiguous"
    return "may leave the documentary state inconsistent with its applicable contract"


def normalize_finding(
    run_id: str,
    record: ValidationInput,
    source_validator: str,
    discrepancy: str,
    result: ValidationResult,
) -> DocumentFinding:
    """Convert one validator observation into a decision-ready finding."""

    if source_validator not in {"DIM", "ONTOLOGY", "DTS", "DGM"}:
        raise ValueError(f"unsupported finding source: {source_validator}")
    return DocumentFinding(
        finding_id=_stable_finding_id(run_id, record, source_validator, discrepancy),
        artifact=record.artifact,
        identity=_display(record.identity),
        applicable_authority=_display(record.ontology.get("authority")),
        source_validator=source_validator,
        discrepancy=discrepancy,
        evidence=result.evidence or record.evidence,
        potential_impact=_finding_impact(source_validator, discrepancy),
        confidence=result.confidence,
    )


def findings_for_record(
    run_id: str, record: ValidationInput
) -> tuple[DocumentFinding, ...]:
    """Normalize every C1-C4 observation without deciding or routing it."""

    findings: list[DocumentFinding] = []
    for source_validator, result in validate(record).items():
        findings.extend(
            normalize_finding(run_id, record, source_validator, discrepancy, result)
            for discrepancy in result.findings
        )
    return tuple(findings)


def _proposed_route(finding: DocumentFinding) -> tuple[str | None, bool, str]:
    """Suggest a procedure only when the observation is sufficient to do so."""

    discrepancy = finding.discrepancy
    if discrepancy.endswith("UNKNOWN") or "UNKNOWN" in discrepancy:
        return None, False, "INSUFFICIENT_EVIDENCE"
    if "AUTHORITY_CONFLICT" in discrepancy:
        return "CANON_CHANGE", True, "authority scope conflict requires canon review"
    if "SUPERSEDED" in discrepancy:
        return (
            "HISTORICAL_CLASSIFICATION",
            False,
            "current reasoning references a superseded revision",
        )
    if "ORPHAN" in discrepancy:
        return "ARCHIVE", False, "orphaned artefact has no demonstrated active provenance"
    if discrepancy in {
        "ARTIFACT_TAG_ABSENT",
        "TAG_IDENTITY_OR_REPRESENTATION_UNKNOWN",
        "TAG_IDENTITY_OR_REPRESENTATION_MISMATCH",
        "TAG_CONTRACT_VERSION_INCOMPATIBLE",
        "RUNTIME_OR_DISTRIBUTION_REVISION_DIVERGENT",
        "DISTRIBUTION_SOURCE_DIVERGENT",
    } or finding.source_validator == "ONTOLOGY":
        return "DOCUMENTARY_CORRECTION", False, "alignment can be reviewed without changing canon"
    if finding.source_validator == "DTS" and "INCOMPATIBLE" in discrepancy:
        return "DELETE", False, "incompatible artefact requires explicit removal decision"
    return None, False, "NO_SAFE_PROCEDURE_INFERRED"


def decide_finding(finding: DocumentFinding, response: str) -> DocumentFinding:
    """Record OUI/NON/PLUS_TARD; OUI only creates a route proposal."""

    if response not in HUMAN_DECISIONS:
        raise ValueError(f"unsupported human decision: {response}")
    if response == "NON":
        return DocumentFinding(
            **{
                **finding.as_dict(),
                "human_decision_status": "DECLINED",
                "route_reason": "human decision recorded; artefact remains unchanged",
            }
        )
    if response == "PLUS_TARD":
        return DocumentFinding(
            **{
                **finding.as_dict(),
                "human_decision_status": "DEFERRED",
                "route_reason": "documentary debt recorded for later decision",
            }
        )

    route, requires_canon, reason = _proposed_route(finding)
    return DocumentFinding(
        **{
            **finding.as_dict(),
            "human_decision_status": "APPROVED_FOR_ROUTING",
            "proposed_route": route,
            "canon_change_proposal_required": requires_canon,
            "route_reason": reason,
        }
    )


def finding_json(run_id: str, record: ValidationInput) -> list[dict[str, Any]]:
    """Serialize C5 findings without writing to the represented artefact."""

    return [finding.as_dict() for finding in findings_for_record(run_id, record)]


def result_json(record: ValidationInput) -> dict[str, Any]:
    return {name: result.as_dict() for name, result in validate(record).items()}
