"""C0-C5 read-only validation pilot over experimental PoA fixtures."""

import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/vbb-document-model-validation.py"
FIXTURES_PATH = (
    ROOT
    / "docs/runs/2026-08-02_document-model-validation-pilot/fixtures/poa_fixtures.json"
)
C3_C4_FIXTURES_PATH = (
    ROOT
    / "docs/runs/2026-08-02_document-model-validation-pilot/fixtures/c3_c4_fixtures.json"
)
C5_FIXTURES_PATH = (
    ROOT
    / "docs/runs/2026-08-02_document-model-validation-pilot/fixtures/c5_finding_fixtures.json"
)


spec = importlib.util.spec_from_file_location("document_model_validation", MODULE_PATH)
assert spec and spec.loader
validation = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validation
spec.loader.exec_module(validation)


def records():
    return [validation.ValidationInput.from_mapping(item) for item in json.loads(FIXTURES_PATH.read_text())]


def c3_c4_records():
    return [
        validation.ValidationInput.from_mapping(item)
        for item in json.loads(C3_C4_FIXTURES_PATH.read_text())
    ]


def c5_records():
    return [
        validation.ValidationInput.from_mapping(item)
        for item in json.loads(C5_FIXTURES_PATH.read_text())
    ]


def finding_for(record, source_validator, discrepancy):
    findings = validation.findings_for_record("c5-test-run", record)
    return next(
        finding
        for finding in findings
        if finding.source_validator == source_validator
        and finding.discrepancy == discrepancy
    )


def test_c0_result_contract_uses_only_authorized_verdicts():
    record = records()[0]
    result = validation.validate(record)["DIM"]

    assert set(result.as_dict()) == {
        "artifact",
        "identity",
        "representation",
        "revision",
        "ontology",
        "critical_relations",
        "contract_version",
        "verdict",
        "findings",
        "evidence",
        "confidence",
        "compatibility",
    }
    assert result.verdict in {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}
    assert result.compatibility == "UNKNOWN"


def test_dim_accepts_identity_representation_revision_and_location():
    result = validation.validate_dim(records()[6])

    assert result.verdict == "PASS"
    assert result.identity == "Pi runtime posture"
    assert result.representation == "SYSTEM.md symlink"


def test_dim_keeps_incomplete_generated_revision_unknown():
    result = validation.validate_dim(records()[9])

    assert result.verdict == "UNKNOWN"
    assert "REVISION_UNKNOWN" in result.findings


def test_dim_rejects_orphan_representation():
    record = records()[0]
    orphan = validation.ValidationInput(
        **{**record.__dict__, "identity": None}
    )

    result = validation.validate_dim(orphan)

    assert result.verdict == "FAIL"
    assert "ORPHAN_REPRESENTATION" in result.findings


def test_dim_rejects_location_presented_as_identity():
    record = records()[6]
    abusive = validation.ValidationInput(
        **{**record.__dict__, "identity": record.location}
    )

    result = validation.validate_dim(abusive)

    assert result.verdict == "FAIL"
    assert "LOCATION_PRESENTED_AS_IDENTITY" in result.findings


def test_dim_rejects_revision_inferred_only_from_date_or_path():
    record = records()[0]
    for basis in ("date", "path"):
        invalid = validation.ValidationInput(
            **{**record.__dict__, "revision_basis": basis}
        )
        result = validation.validate_dim(invalid)
        assert result.verdict == "FAIL"
        assert "REVISION_INFERRED_FROM_PATH_OR_DATE" in result.findings


def test_ontology_accepts_multi_period_adversarial_governance():
    result = validation.validate_ontology(records()[3])

    assert result.verdict == "PASS"
    assert result.ontology["temporality"] == "MULTI_PERIOD"


def test_ontology_accepts_old_adr_that_remains_applicable():
    result = validation.validate_ontology(records()[5])

    assert result.verdict == "PASS"
    assert result.ontology["lifecycle"] == "ACTIVE"
    assert result.ontology["temporality"] == "CURRENT"


def test_ontology_rejects_multiple_primary_functions():
    record = records()[8]
    invalid = validation.ValidationInput(
        **{
            **record.__dict__,
            "ontology": {
                **record.ontology,
                "primary_function": ["NORMATIVE", "REFERENCE"],
            },
        }
    )

    result = validation.validate_ontology(invalid)

    assert result.verdict == "FAIL"
    assert "MULTIPLE_PRIMARY_FUNCTIONS" in result.findings


def test_ontology_rejects_secondary_normative_function_hiding_prescription():
    record = records()[7]
    invalid = validation.ValidationInput(
        **{
            **record.__dict__,
            "ontology": {
                **record.ontology,
                "authority": "NON_AUTHORITATIVE",
                "secondary_functions": ["NORMATIVE"],
            },
        }
    )

    result = validation.validate_ontology(invalid)

    assert result.verdict == "FAIL"
    assert "SECONDARY_NORMATIVE_HIDES_PRESCRIPTION" in result.findings


def test_ontology_rejects_retired_always_loaded_artifact():
    record = records()[10]
    invalid = validation.ValidationInput(
        **{
            **record.__dict__,
            "ontology": {**record.ontology, "load_policy": "ALWAYS"},
        }
    )

    result = validation.validate_ontology(invalid)

    assert result.verdict == "FAIL"
    assert "RETIRED_OR_SUPERSEDED_ALWAYS_LOADED" in result.findings


def test_ontology_rejects_invalid_dimension_value():
    record = records()[0]
    invalid = validation.ValidationInput(
        **{
            **record.__dict__,
            "ontology": {**record.ontology, "temporality": "HISTORICAL"},
        }
    )

    result = validation.validate_ontology(invalid)

    assert result.verdict == "FAIL"
    assert "TEMPORALITY_VALUE_INVALID" in result.findings


def test_all_eleven_poa_fixtures_are_covered():
    fixture_records = records()
    assert len(fixture_records) == 11
    assert {record.artifact for record in fixture_records} == {
        "AGENTS.md",
        "docs/ARCHITECTURE.md",
        "docs/REFERENCE/pre-merge-gate.md",
        "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md",
        "docs/adr/0053-a2-a3-assurance-alignment.md",
        "docs/adr/0001-formal-executor-boundary.md",
        "SYSTEM.md",
        "distributions/pi/README.md",
        "prompts/canonical/04-p-vbb-plan.md",
        "docs/RELATIONS.md",
        "docs/runs/2026-07-31_vbb-doc-v1-external-pilot/07_CLOSEOUT.md",
    }


def test_all_poa_fixtures_validate_without_writes():
    before = {path: path.read_bytes() for path in (ROOT / "AGENTS.md", ROOT / "docs/ARCHITECTURE.md")}

    results = [validation.validate(record) for record in records()]

    after = {path: path.read_bytes() for path in before}
    assert all("DIM" in result and "ONTOLOGY" in result for result in results)
    assert results[9]["DIM"].verdict == "UNKNOWN"
    assert results[10]["ONTOLOGY"].verdict == "PASS"
    assert before == after


def test_dts_covers_all_required_compatibility_results():
    results = {record.artifact: validation.validate_dts(record) for record in c3_c4_records()}

    assert results["fixtures/dts-contract-missing"].compatibility == "UNKNOWN"
    assert results["fixtures/dts-artifact-without-tag"].compatibility == "UNKNOWN"
    assert results["fixtures/dts-old-compatible"].compatibility == "COMPATIBLE"
    assert results["fixtures/dts-migration-required"].compatibility == "MIGRATION_REQUIRED"
    assert results["fixtures/dts-unknown-dimension"].compatibility == "UNKNOWN"
    assert results["docs/ARCHITECTURE.md"].compatibility == "COMPATIBLE"
    assert results["docs/RELATIONS.md"].compatibility == "COMPATIBLE"
    assert results["fixtures/dts-projection-orphan"].compatibility == "INCOMPATIBLE"
    assert results["fixtures/dts-runtime-other-state"].compatibility == "MIGRATION_REQUIRED"


def test_dts_unknowns_are_not_silently_compatible():
    for record in c3_c4_records()[:2] + [c3_c4_records()[4]]:
        result = validation.validate_dts(record)
        assert result.compatibility == "UNKNOWN"
        assert result.verdict == "UNKNOWN"


def test_dts_projection_requires_a_traceable_source():
    valid = validation.validate_dts(c3_c4_records()[6])
    orphan = validation.validate_dts(c3_c4_records()[8])

    assert valid.compatibility == "COMPATIBLE"
    assert orphan.compatibility == "INCOMPATIBLE"
    assert "DERIVED_SOURCE_ORPHAN" in orphan.findings


def test_dts_runtime_from_another_documentary_state_requires_migration():
    result = validation.validate_dts(c3_c4_records()[9])

    assert result.compatibility == "MIGRATION_REQUIRED"
    assert "RUNTIME_OR_DISTRIBUTION_REVISION_DIVERGENT" in result.findings


def test_dgm_accepts_architecture_projection_and_system_location_relations():
    records_by_name = {record.artifact: record for record in c3_c4_records()}

    architecture = validation.validate_dgm(records_by_name["docs/ARCHITECTURE.md"])
    projection = validation.validate_dgm(records_by_name["docs/RELATIONS.md"])
    system = validation.validate_dgm(records_by_name["SYSTEM.md"])

    assert architecture.verdict == "PASS"
    assert projection.verdict == "PASS"
    assert system.verdict == "PASS"


def test_dgm_detects_representation_and_revision_misattachments():
    records_by_name = {record.artifact: record for record in c3_c4_records()}

    orphan = validation.validate_dgm(records_by_name["fixtures/dgm-representation-orphan"])
    wrong_revision = validation.validate_dgm(
        records_by_name["fixtures/dgm-revision-wrong-representation"]
    )

    assert orphan.verdict == "FAIL"
    assert "REPRESENTATION_WITHOUT_IDENTITY" in orphan.findings
    assert wrong_revision.verdict == "FAIL"
    assert "REVISION_OF_TARGET_MISMATCH" in wrong_revision.findings


def test_dgm_keeps_missing_source_and_decision_unknown():
    records_by_name = {record.artifact: record for record in c3_c4_records()}

    projection = validation.validate_dgm(records_by_name["fixtures/dgm-projection-no-source"])
    authority = validation.validate_dgm(records_by_name["fixtures/dgm-authority-no-decision"])
    evidence = validation.validate_dgm(records_by_name["fixtures/dgm-evidence-unattached"])
    provenance = validation.validate_dgm(records_by_name["fixtures/dgm-broken-provenance"])

    assert projection.verdict == "UNKNOWN"
    assert authority.verdict == "UNKNOWN"
    assert evidence.verdict == "UNKNOWN"
    assert provenance.verdict == "UNKNOWN"


def test_dgm_detects_conflict_superseded_reference_and_distribution_divergence():
    records_by_name = {record.artifact: record for record in c3_c4_records()}

    conflict = validation.validate_dgm(records_by_name["fixtures/dgm-authority-conflict"])
    superseded = validation.validate_dgm(
        records_by_name["fixtures/dgm-active-reference-superseded"]
    )
    distribution = validation.validate_dgm(
        records_by_name["fixtures/dgm-distribution-divergent"]
    )

    assert conflict.verdict == "FAIL"
    assert "AUTHORITY_CONFLICT_SAME_SCOPE" in conflict.findings
    assert superseded.verdict == "FAIL"
    assert "ACTIVE_REFERENCE_TO_SUPERSEDED_REVISION" in superseded.findings
    assert distribution.verdict == "FAIL"
    assert "DISTRIBUTION_SOURCE_DIVERGENT" in distribution.findings


def test_dgm_allows_only_the_declared_relation_vocabulary():
    record = c3_c4_records()[5]
    invalid = validation.ValidationInput(
        **{**record.__dict__, "relations": ({"type": "INVENTED_RELATION"},)}
    )

    result = validation.validate_dgm(invalid)

    assert result.verdict == "FAIL"
    assert "RELATION_TYPE_INVALID" in result.findings


def test_c5_normalizes_findings_with_stable_identity_and_required_evidence():
    record = c3_c4_records()[8]

    first = finding_for(record, "DTS", "DERIVED_SOURCE_ORPHAN")
    second = finding_for(record, "DTS", "DERIVED_SOURCE_ORPHAN")

    assert first.finding_id == second.finding_id
    assert first.artifact == record.artifact
    assert first.identity == record.identity
    assert first.applicable_authority == "NON_AUTHORITATIVE"
    assert first.source_validator == "DTS"
    assert first.evidence
    assert first.potential_impact
    assert first.confidence == "HIGH"
    assert first.human_decision_status == "AWAITING_HUMAN_DECISION"
    assert first.proposed_route is None


def test_c5_covers_required_finding_cases():
    records_by_name = {record.artifact: record for record in c3_c4_records()}
    invalid_ontology = validation.ValidationInput(
        **{
            **records_by_name["fixtures/dts-unknown-dimension"].__dict__,
            "ontology": {
                **records_by_name["fixtures/dts-unknown-dimension"].ontology,
                "temporality": "HISTORICAL",
            },
        }
    )

    cases = {
        "orphan_projection": finding_for(
            records_by_name["fixtures/dts-projection-orphan"],
            "DTS",
            "DERIVED_SOURCE_ORPHAN",
        ),
        "artifact_without_tag": finding_for(
            records_by_name["fixtures/dts-artifact-without-tag"],
            "DTS",
            "ARTIFACT_TAG_ABSENT",
        ),
        "authority_conflict": finding_for(
            records_by_name["fixtures/dgm-authority-conflict"],
            "DGM",
            "AUTHORITY_CONFLICT_SAME_SCOPE",
        ),
        "historical_authority": finding_for(
            c5_records()[0], "DGM", "ACTIVE_REFERENCE_TO_SUPERSEDED_REVISION"
        ),
        "runtime_divergence": finding_for(
            records_by_name["fixtures/dts-runtime-other-state"],
            "DTS",
            "RUNTIME_OR_DISTRIBUTION_REVISION_DIVERGENT",
        ),
        "invalid_ontology": finding_for(
            invalid_ontology, "ONTOLOGY", "TEMPORALITY_VALUE_INVALID"
        ),
        "unknown": finding_for(
            c5_records()[1], "DIM", "LOCATION_UNKNOWN"
        ),
    }

    assert set(cases) == {
        "orphan_projection",
        "artifact_without_tag",
        "authority_conflict",
        "historical_authority",
        "runtime_divergence",
        "invalid_ontology",
        "unknown",
    }


def test_c5_records_oui_non_plus_tard_without_mutation():
    record = c3_c4_records()[1]
    finding = finding_for(record, "DTS", "ARTIFACT_TAG_ABSENT")
    before = C3_C4_FIXTURES_PATH.read_bytes()

    oui = validation.decide_finding(finding, "OUI")
    non = validation.decide_finding(finding, "NON")
    later = validation.decide_finding(finding, "PLUS_TARD")

    assert oui.human_decision_status == "APPROVED_FOR_ROUTING"
    assert oui.proposed_route == "DOCUMENTARY_CORRECTION"
    assert non.human_decision_status == "DECLINED"
    assert non.proposed_route is None
    assert later.human_decision_status == "DEFERRED"
    assert later.proposed_route is None
    assert finding.human_decision_status == "AWAITING_HUMAN_DECISION"
    assert C3_C4_FIXTURES_PATH.read_bytes() == before


def test_c5_unknown_finding_is_approved_without_unsafe_route():
    finding = finding_for(c5_records()[1], "DIM", "LOCATION_UNKNOWN")

    routed = validation.decide_finding(finding, "OUI")

    assert routed.human_decision_status == "APPROVED_FOR_ROUTING"
    assert routed.proposed_route is None
    assert routed.canon_change_proposal_required is False
    assert routed.route_reason == "INSUFFICIENT_EVIDENCE"


def test_c5_canon_change_is_separate_from_ordinary_correction():
    records_by_name = {record.artifact: record for record in c3_c4_records()}
    conflict = finding_for(
        records_by_name["fixtures/dgm-authority-conflict"],
        "DGM",
        "AUTHORITY_CONFLICT_SAME_SCOPE",
    )
    ordinary = finding_for(
        records_by_name["fixtures/dts-runtime-other-state"],
        "DTS",
        "RUNTIME_OR_DISTRIBUTION_REVISION_DIVERGENT",
    )

    canon_route = validation.decide_finding(conflict, "OUI")
    ordinary_route = validation.decide_finding(ordinary, "OUI")

    assert canon_route.proposed_route == "CANON_CHANGE"
    assert canon_route.canon_change_proposal_required is True
    assert ordinary_route.proposed_route == "DOCUMENTARY_CORRECTION"
    assert ordinary_route.canon_change_proposal_required is False


def test_c5_route_proposals_never_execute_remediation():
    record = c3_c4_records()[8]
    finding = finding_for(record, "DTS", "DERIVED_SOURCE_ORPHAN")
    before = {path: path.read_bytes() for path in (ROOT / "AGENTS.md", ROOT / "SYSTEM.md")}

    routed = validation.decide_finding(finding, "OUI")

    assert routed.proposed_route == "ARCHIVE"
    assert {path: path.read_bytes() for path in before} == before
