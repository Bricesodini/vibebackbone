"""Regression checks for the English-only active prompt convention."""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_ROOT = REPO_ROOT / "prompts"

# Machine-facing route and verdict enums are contracts, not prose.
ALLOWED_CONTRACT_TOKENS = (
    "STRUCTURÉE",
    "RAPIDE",
    "RAPIDE-ZERO",
    "RAPIDE-MINIMAL",
    "CLÔTURE",
    "FAIBLE",
    "MODÉRÉ",
    "ÉLEVÉ",
    "APPROUVÉ",
    "APPROUVÉ_AVEC_RÉSERVES",
    "MODIFICATIONS_REQUISES",
    "REJETÉ",
    "COMPLET",
    "PARTIEL",
    "BLOQUÉ",
    "ABANDONNÉ",
)

# Keep this vocabulary conservative: every entry is unambiguous French
# instructional prose in the prompt catalog, not a shared technical term.
FRENCH_INSTRUCTION_RE = re.compile(
    r"\b(?:"
    r"afin|ainsi|aucun|aucune|avant|avec|cela|ceci|cette|dans|doit|doivent|"
    r"être|étape|étapes|fichier|fichiers|lorsque|nécessaire|objectif|pour|"
    r"sans|selon|après|vérifier|prochaine|produire|créer|lancer|utiliser|"
    r"transmettre|demander|réponds|résumé|résultat|risque|risques|sortie"
    r")\b",
    re.IGNORECASE,
)
FENCED_CONTRACT_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CONTRACT_RE = re.compile(r"`[^`]+`")
ACCENTED_TOKEN_RE = re.compile(r"\b\w*[àâçéèêëîïôùûüÿœ]\w*\b", re.IGNORECASE)


def french_instruction_markers(text: str) -> list[str]:
    """Return unambiguous French prose markers after contract-token removal."""
    normalized = FENCED_CONTRACT_RE.sub("", text)
    normalized = INLINE_CONTRACT_RE.sub("", normalized)
    for token in sorted(ALLOWED_CONTRACT_TOKENS, key=len, reverse=True):
        normalized = normalized.replace(token, "")
    return [match.group(0) for match in FRENCH_INSTRUCTION_RE.finditer(normalized)]


def test_detector_rejects_controlled_french_instruction() -> None:
    markers = french_instruction_markers("Créer le fichier puis vérifier le résultat.")

    assert markers == ["Créer", "fichier", "vérifier", "résultat"]


def test_active_prompts_use_english_instructional_prose() -> None:
    failures: dict[str, list[str]] = {}
    prompt_paths = sorted(PROMPTS_ROOT.rglob("*.md"))

    assert len(prompt_paths) == 33
    for path in prompt_paths:
        markers = french_instruction_markers(path.read_text(encoding="utf-8"))
        if markers:
            failures[str(path.relative_to(REPO_ROOT))] = markers[:10]

    assert failures == {}


def test_active_prompts_have_no_unapproved_accented_tokens() -> None:
    failures: dict[str, list[str]] = {}

    for path in sorted(PROMPTS_ROOT.rglob("*.md")):
        normalized = path.read_text(encoding="utf-8")
        for token in sorted(ALLOWED_CONTRACT_TOKENS, key=len, reverse=True):
            normalized = normalized.replace(token, "")
        accented = ACCENTED_TOKEN_RE.findall(normalized)
        if accented:
            failures[str(path.relative_to(REPO_ROOT))] = accented[:10]

    assert failures == {}
