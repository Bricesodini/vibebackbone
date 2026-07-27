from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_canonical_authority_defines_required_lifecycle():
    governance = _read("docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md")
    for state in ("OBSERVATION", "CANDIDATE", "VALIDATED", "CANONICAL"):
        assert f"### {state}" in governance
    assert "Independent knowledge review" in governance
    assert "Only a human approves" in governance
    assert "Direct semantic edits" in governance


def test_non_authoritative_artifacts_are_explicit():
    governance = _read("docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md")
    for artifact in ("Playbook", "Knowledge record", "Run", "Review", "Closeout"):
        row = next(
            line for line in governance.splitlines() if f"| {artifact} |" in line
        )
        assert row.rstrip().endswith("| No |")


def test_templates_expose_protocol_and_harvest_contract():
    intake = _read("docs/templates/01_INTAKE.md.template")
    closeout = _read("docs/templates/07_CLOSEOUT.md.template")
    record = _read("docs/templates/KNOWLEDGE_RECORD.md.template")
    assert 'knowledge_governance_version: "1.0"' in intake
    assert 'knowledge_governance_version: "1.0"' in closeout
    assert "NONE|OBSERVATION_RECORDED|EVIDENCE_LINKED" in closeout
    assert "never a normative authority" in record


def test_agent_surfaces_require_review_and_human_decision():
    agents = _read("AGENTS.md")
    audit_prompt = _read("prompts/canonical/02-p-vbb-audit.md")
    review_prompt = _read("prompts/canonical/06-p-vbb-review.md")
    decision_prompt = _read("prompts/canonical/03-p-vbb-decision.md")
    assert "Governed capitalization" in agents
    assert "knowledge audit never promotes" in audit_prompt
    assert "reviewer ≠ knowledge auditor" in review_prompt
    assert "must be human" in decision_prompt
