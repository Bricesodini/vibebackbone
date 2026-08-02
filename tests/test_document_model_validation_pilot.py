"""C0-C2 read-only validation pilot over the PoA fixtures."""

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


spec = importlib.util.spec_from_file_location("document_model_validation", MODULE_PATH)
assert spec and spec.loader
validation = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validation
spec.loader.exec_module(validation)


def records():
    return [validation.ValidationInput.from_mapping(item) for item in json.loads(FIXTURES_PATH.read_text())]


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
    }
    assert result.verdict in {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}


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
