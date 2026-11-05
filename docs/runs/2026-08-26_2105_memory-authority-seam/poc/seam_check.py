#!/usr/bin/env python3
"""VBB Memory Seam Check — falsification bench for ADR 0055.

Model-free verifier of the authority seam between the documentary canon (the
repository) and a runtime memory layer. No LLM, no network, stdlib only, so the
verdict is reproducible and inspectable by a human.

WHAT IT CHECKS (ADR 0055 clauses)

  C1  CANONICAL_MEMORY_IS_DERIVED     projections are rebuildable from canon
      PROMOTION_IS_A_GATE             promotion cites artifact + gate + authority
      NO_PARALLEL_SEMANTIC_AUTHORITY  memory never decides a canonical dimension
  C2  three classes only, none of them canonical
  C3  promotion protocol, no self-promotion, `working` not promotable
  C4  the five dimensions are read from the source, never local to memory
  C5  contradictions surfaced, never auto-resolved; supersession only in canon
  C7  the three questions are mechanically answerable for EVERY entry

INPUTS

  canon/   flat-frontmatter Markdown artifacts = the canonical source of truth
  vault    a JSON array of memory entries = the runtime layer under test

The canon is authoritative by construction: this tool never rewrites it.

EXIT CODES

  0  PASS  — the vault conforms to the seam
  1  FAIL  — at least one violation, each with a stable machine-readable code
  2  usage / fixture error

SELFTEST

  `--selftest` runs the conformant fixture plus the six adversarial fixtures
  T1..T6 and asserts the EXPECTED verdict of each one. A check that cannot fail
  proves nothing, so the bench requires every Tn to actually fail, with the
  exact code it is supposed to raise.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLASSES = ("projection", "candidate", "working")

# Vocabulary a memory entry may never claim: these belong to the canon alone.
CANONICAL_CLAIM_KEYS = ("canon", "is_canon", "production", "legacy", "canonical")
CANONICAL_CLAIM_VALUES = ("canon", "production", "legacy", "canonical")

# The five orthogonal dimensions of ADR 0055 §C4.
DIMENSIONS = (
    "status",
    "final_status",
    "assurance_status",
    "certification_status",
    "lifecycle",
)

# Fields that would make a projection decide instead of read.
LOCAL_STATUS_FIELDS = ("status_loc", "local_status", "memory_status")


# ─────────────────────────────────────────────────────────── canon parsing ──

def parse_frontmatter(text: str) -> dict:
    """Parse a deliberately flat `key: value` frontmatter block.

    Flat on purpose: a stdlib parser with no YAML dependency keeps the verifier
    installable anywhere and its behaviour unambiguous.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict = {}
    for line in text[3:end].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        out[key.strip()] = value if value else None
    return out


def load_canon(canon_dir: Path) -> dict:
    canon = {}
    for path in sorted(canon_dir.glob("*.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        artifact_id = fm.get("id")
        if not artifact_id:
            raise SystemExit(f"fixture error: {path} has no `id`")
        fm["_path"] = str(path.name)
        canon[artifact_id] = fm
    return canon


def load_vault(vault_path: Path) -> list:
    data = json.loads(vault_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"fixture error: {vault_path} must hold a JSON array")
    return data


# ────────────────────────────────────────────────────────────── rebuilding ──

def rebuild_projections(canon: dict) -> dict:
    """Derive the projection set from the canon alone (C1).

    A canonical artifact that has been superseded projects nothing: its
    authority moved to the superseding version.
    """
    expected = {}
    for artifact_id, fm in canon.items():
        if fm.get("superseded_by"):
            continue
        expected[artifact_id] = {
            "projected": {d: fm.get(d) for d in DIMENSIONS},
            "subject_key": fm.get("subject_key"),
            "value": fm.get("value"),
        }
    return expected


# ─────────────────────────────────────────────────────────────── the check ──

class Report:
    def __init__(self) -> None:
        self.violations: list[tuple[str, str, str]] = []  # (code, entry_id, detail)
        self.answers: list[dict] = []                      # C7 answers

    def fail(self, code: str, entry_id: str, detail: str) -> None:
        self.violations.append((code, entry_id, detail))

    @property
    def codes(self) -> list[str]:
        return sorted({code for code, _, _ in self.violations})


def check(canon: dict, vault: list) -> Report:
    report = Report()
    expected = rebuild_projections(canon)
    seen_projections: dict[str, dict] = {}

    # Candidate contradiction is only mechanically detectable on a declared
    # subject key (POC amendment A1): without it, a verifier would need
    # semantics, which would break the model-free property.
    canon_by_subject = {
        fm.get("subject_key"): (artifact_id, fm.get("value"))
        for artifact_id, fm in canon.items()
        if fm.get("subject_key") and not fm.get("superseded_by")
    }
    candidates_by_subject: dict[str, list[tuple[str, str]]] = {}

    for entry in vault:
        entry_id = str(entry.get("id", "<no-id>"))
        klass = entry.get("class")

        # ── C2: three classes, nothing else ──────────────────────────────
        if klass not in CLASSES:
            report.fail("CLASS_UNKNOWN", entry_id, f"class={klass!r}")
            continue

        # ── C2/C6: no entry may claim canonical standing ─────────────────
        for key in CANONICAL_CLAIM_KEYS:
            if key in entry and entry[key] not in (None, False, ""):
                report.fail("CANONICAL_CLAIM_IN_MEMORY", entry_id,
                            f"field {key}={entry[key]!r}")
        for field in ("class", "kind", "tier", "level"):
            if str(entry.get(field, "")).lower() in CANONICAL_CLAIM_VALUES:
                report.fail("CANONICAL_CLAIM_IN_MEMORY", entry_id,
                            f"{field}={entry.get(field)!r}")

        # ── C3: promotion protocol ───────────────────────────────────────
        promoted = entry.get("promoted")
        if promoted:
            if klass == "working":
                report.fail("WORKING_PROMOTED", entry_id,
                            "a working entry is not promotable")
            if not promoted.get("artifact"):
                report.fail("PROMOTION_WITHOUT_ARTIFACT", entry_id, "no artifact")
            elif promoted["artifact"] not in canon:
                report.fail("PROMOTION_WITHOUT_ARTIFACT", entry_id,
                            f"artifact {promoted['artifact']} absent from canon")
            if not promoted.get("gate"):
                report.fail("PROMOTION_WITHOUT_GATE", entry_id, "no gate record")
            authorization = promoted.get("authorization") or {}
            if authorization.get("by") != "human":
                report.fail("PROMOTION_WITHOUT_AUTHORIZATION", entry_id,
                            f"authorized by {authorization.get('by')!r}")

        # ── per-class rules ──────────────────────────────────────────────
        if klass == "projection":
            source = entry.get("source")
            if not source:
                report.fail("PROJECTION_WITHOUT_SOURCE", entry_id, "no source")
            elif source not in canon:
                report.fail("PROJECTION_WITHOUT_SOURCE", entry_id,
                            f"source {source} absent from canon")
            else:
                fm = canon[source]
                if fm.get("superseded_by"):
                    report.fail("PROJECTION_STALE_SUPERSEDED", entry_id,
                                f"source {source} superseded by "
                                f"{fm['superseded_by']}")
                projected = entry.get("projected") or {}
                for dimension in DIMENSIONS:
                    if projected.get(dimension) != fm.get(dimension):
                        report.fail("PROJECTION_STATUS_DIVERGES", entry_id,
                                    f"{dimension}: memory="
                                    f"{projected.get(dimension)!r} "
                                    f"canon={fm.get(dimension)!r}")
                seen_projections[source] = entry
            for field in LOCAL_STATUS_FIELDS:
                if field in entry:
                    report.fail("PROJECTION_LOCAL_STATUS_FIELD", entry_id,
                                f"projection carries {field}")

        elif klass == "candidate":
            if not entry.get("provenance"):
                report.fail("CANDIDATE_WITHOUT_PROVENANCE", entry_id,
                            "no provenance")
            subject = entry.get("subject_key")
            if not subject:
                # Amendment A1: without a subject key, contradiction with the
                # canon cannot be detected mechanically.
                report.fail("CANDIDATE_WITHOUT_SUBJECT_KEY", entry_id,
                            "contradiction would be undetectable model-free")
            else:
                candidates_by_subject.setdefault(subject, []).append(
                    (entry_id, entry.get("value")))
                canon_hit = canon_by_subject.get(subject)
                if canon_hit and canon_hit[1] != entry.get("value"):
                    if not entry.get("conflict"):
                        report.fail("CANDIDATE_CONTRADICTION_UNFLAGGED",
                                    entry_id,
                                    f"subject {subject}: candidate="
                                    f"{entry.get('value')!r} canon="
                                    f"{canon_hit[1]!r}")
                    if entry.get("conflicts_with") not in (None, canon_hit[0]):
                        report.fail("CANDIDATE_CONTRADICTION_UNFLAGGED",
                                    entry_id, "conflicts_with points elsewhere")
            if entry.get("supersedes"):
                report.fail("MEMORY_SUPERSEDES_CANON", entry_id,
                            "supersession belongs to the canon (ADR 0049)")

        else:  # working
            if entry.get("source"):
                report.fail("WORKING_WITH_SOURCE", entry_id,
                            "a working entry projects nothing")

        # ── C7: the three questions, answered mechanically ───────────────
        origin = (entry.get("provenance") or {}).get("captured_from") \
            or (entry.get("source") and "canon")
        authority = {
            "projection": "canon:" + str(entry.get("source")),
            "candidate": "none (candidate)",
            "working": "none (working)",
        }[klass]
        loss = {"projection": "none (rebuildable)",
                "candidate": "promotion queue only",
                "working": "none (ephemeral)"}[klass]
        if not origin:
            report.fail("C7_UNANSWERABLE", entry_id, "origin not derivable")
        report.answers.append({
            "id": entry_id, "class": klass, "origin": origin,
            "authority": authority, "loss_if_vault_deleted": loss,
        })

    # ── C5: two candidates on one subject must not be silently reconciled ──
    for subject, rows in candidates_by_subject.items():
        values = {value for _, value in rows}
        if len(rows) > 1 and len(values) == 1 and len(
                {entry_id for entry_id, _ in rows}) > 1:
            # Same subject, one surviving value, several entries: acceptable
            # only when every entry kept its own record. Collapsing two
            # incompatible candidates into one value is auto-resolution.
            continue
        if len(values) > 1:
            flagged = [
                entry_id for entry_id, _ in rows
                if any(v.get("id") == entry_id and v.get("conflict")
                       for v in vault)
            ]
            if len(flagged) < len(rows):
                report.fail("CONFLICT_AUTO_RESOLVED", subject,
                            f"{len(rows)} incompatible candidates, "
                            f"{len(flagged)} flagged")

    # ── C1: rebuildability ────────────────────────────────────────────────
    for source, shape in expected.items():
        entry = seen_projections.get(source)
        if entry is None:
            report.fail("REBUILD_DIVERGENCE", source,
                        "canon artifact has no projection")
            continue
        if (entry.get("projected") or {}) != shape["projected"]:
            report.fail("REBUILD_DIVERGENCE", source, "projected fields differ")
    for source in seen_projections:
        if source not in expected:
            report.fail("REBUILD_DIVERGENCE", source,
                        "projection has no live canon counterpart")

    return report


# ──────────────────────────────────────────────────────────────── selftest ──

EXPECTED = {
    "conformant": (0, set()),
    "t1_candidate_contradicts_canon": (1, {"CANDIDATE_CONTRADICTION_UNFLAGGED"}),
    "t2_projection_source_superseded": (1, {"PROJECTION_STALE_SUPERSEDED"}),
    "t3_fact_without_source": (1, {"PROJECTION_WITHOUT_SOURCE"}),
    "t4_incompatible_candidates": (1, {"CONFLICT_AUTO_RESOLVED"}),
    "t5_vault_destroyed": (1, {"REBUILD_DIVERGENCE"}),
    "t6_direct_production_marking": (1, {"CANONICAL_CLAIM_IN_MEMORY"}),
}


def run_one(base: Path, name: str) -> tuple[int, Report]:
    canon = load_canon(base / "canon")
    vault = load_vault(base / "vaults" / f"{name}.json")
    report = check(canon, vault)
    return (1 if report.violations else 0), report


def selftest(base: Path) -> int:
    print("VBB Memory Seam Check — selftest (ADR 0055 T1..T6)\n")
    ok = True
    for name, (want_code, want_codes) in EXPECTED.items():
        got_code, report = run_one(base, name)
        got_codes = set(report.codes)
        passed = got_code == want_code and want_codes.issubset(got_codes)
        ok &= passed
        mark = "OK  " if passed else "BAD "
        print(f"  {mark} {name:34s} exit={got_code} "
              f"codes={sorted(got_codes) if got_codes else '[]'}")
        if not passed:
            print(f"       expected exit={want_code} "
                  f"codes⊇{sorted(want_codes)}")
    print()
    if ok:
        print("SELFTEST PASS — the conformant vault passes and each of the six "
              "adversarial cases fails with its expected code.")
        return 0
    print("SELFTEST FAIL — the bench does not discriminate as specified.")
    return 1


# ──────────────────────────────────────────────────────────────────── main ──

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="vbb-memory-seam-check",
        description="Falsification bench for the ADR 0055 authority seam.")
    parser.add_argument("--canon", type=Path, help="canonical artifact dir")
    parser.add_argument("--vault", type=Path, help="vault JSON file")
    parser.add_argument("--answers", action="store_true",
                        help="print the C7 answers for every entry")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    parser.add_argument("--selftest", action="store_true",
                        help="run the T1..T6 fixtures and assert verdicts")
    parser.add_argument("--rebuild", action="store_true",
                        help="derive the projection set from --canon alone "
                             "(T5: destroy the vault, rebuild, re-check)")
    parser.add_argument("--fixtures", type=Path,
                        default=Path(__file__).parent / "fixtures",
                        help="fixture root for --selftest")
    args = parser.parse_args()

    if args.selftest:
        return selftest(args.fixtures)

    if args.rebuild:
        if not args.canon:
            parser.error("--rebuild requires --canon")
        canon = load_canon(args.canon)
        rebuilt = [
            {
                "id": f"p_{source}",
                "class": "projection",
                "source": source,
                "subject_key": shape["subject_key"],
                "value": shape["value"],
                "projected": shape["projected"],
                "provenance": {"captured_from": "repo", "run": "rebuild"},
            }
            for source, shape in sorted(rebuild_projections(canon).items())
        ]
        print(json.dumps(rebuilt, indent=2, ensure_ascii=False))
        return 0

    if not args.canon or not args.vault:
        parser.error("--canon and --vault are required without --selftest")

    canon = load_canon(args.canon)
    vault = load_vault(args.vault)
    report = check(canon, vault)
    payload = {
        "canon_artifacts": len(canon),
        "vault_entries": len(vault),
        "violations": [
            {"code": c, "entry": e, "detail": d} for c, e, d in report.violations
        ],
        "codes": report.codes,
        "verdict": "FAIL" if report.violations else "PASS",
    }
    if args.answers:
        payload["answers"] = report.answers

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"canon: {len(canon)} artifact(s) | vault: {len(vault)} entry(ies)")
        for code, entry, detail in report.violations:
            print(f"  {code:34s} {entry:22s} {detail}")
        if args.answers:
            print("\nC7 — origin / authority / loss if the vault disappears:")
            for a in report.answers:
                print(f"  {a['id']:8s} {a['class']:11s} "
                      f"{str(a['origin']):16s} {a['authority']:26s} "
                      f"{a['loss_if_vault_deleted']}")
        print(f"\nVERDICT: {payload['verdict']}")
    return 1 if report.violations else 0


if __name__ == "__main__":
    sys.exit(main())
