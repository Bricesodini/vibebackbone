"""Contract checks for the four skills aligned with the C0-C5 pilot."""

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "harmonizer": ROOT / "skills/1-vbb-doc-harmonizer/SKILL.md",
    "coherence": ROOT / "skills/1-vbb-code-doc-coherence-auditor/SKILL.md",
    "gap": ROOT / "skills/1-vbb-code-doc-gap-integrator/SKILL.md",
    "context_init": ROOT / "skills/t-vbb-project-context-init/SKILL.md",
}


@pytest.fixture(scope="module")
def skill_texts():
    return {name: path.read_text(encoding="utf-8") for name, path in SKILLS.items()}


def test_target_skills_share_the_c0_c5_decision_boundary(skill_texts):
    required = (
        "C0-C5",
        "OUI",
        "NON",
        "PLUS_TARD",
        "UNKNOWN",
        "authority",
        "representation",
        "validator",
    )

    for name, text in skill_texts.items():
        missing = [term for term in required if term not in text]
        assert not missing, f"{name} missing: {missing}"


def test_harmonizer_no_longer_constructs_a_scalar_current_truth(skill_texts):
    text = skill_texts["harmonizer"]

    assert 'Extract the "current truth"' not in text
    assert "Classify each document:" not in text
    assert "concurrent authorities" in text
    assert "propose the DTP procedure" in text
    assert "CANON_CHANGE_PROPOSAL" in text


def test_coherence_findings_include_document_model_fields(skill_texts):
    text = skill_texts["coherence"]

    for field in (
        "identity",
        "applicable authority",
        "code-document relation",
        "ontology",
        "compatibility",
        "confidence",
    ):
        assert field in text
    assert "never write a fix automatically" in text


def test_gap_integrator_requires_decision_before_identity_or_document_creation(
    skill_texts,
):
    text = skill_texts["gap"]

    assert "do not create a document or identity after detection alone" in text
    assert "new representation of an existing identity" in text
    assert "proposal for a new identity" in text
    assert "correction of an incomplete" in text
    assert "can never create a canonical authority alone" in text


def test_context_init_negotiates_contract_without_claiming_conformity(skill_texts):
    text = skill_texts["context_init"]

    assert "missing contract is `UNKNOWN`" in text
    assert "old compatible contract" in text
    assert "migration-required contract" in text
    assert "target contract only" in text
    assert "does not claim" in text
    assert "no finding response writes an" in text


def test_previous_read_only_and_non_destructive_boundaries_remain(skill_texts):
    assert "You work ONLY on Markdown files" in skill_texts["harmonizer"]
    assert "never modify code/config" in skill_texts["coherence"]
    assert "Ground every gap" in skill_texts["gap"]
    assert "Idempotent" in skill_texts["context_init"]
    assert "Non-destructive" in skill_texts["context_init"]


def test_no_parallel_historical_model_is_reintroduced(skill_texts):
    forbidden = ("CC-11", "CR-2", "REVISE-C v3", "ADR-0052")

    for name, text in skill_texts.items():
        assert not any(term in text for term in forbidden), name


def test_routes_are_proposals_and_not_remediation(skill_texts):
    for name, text in skill_texts.items():
        assert "OUI" in text and "NON" in text and "PLUS_TARD" in text
        assert "route" in text.lower()
    assert "A route proposal is not execution." in skill_texts["coherence"]
    assert "route proposal" in skill_texts["gap"]
