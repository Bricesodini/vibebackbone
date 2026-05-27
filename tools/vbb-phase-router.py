#!/usr/bin/env python3
"""
VBB Phase Router — Phase 4.1
Routes execution to skill contracts based on triggers and phase_scope.

Supports:
  - Trigger-based routing (keywords)
  - Phase scope filtering
  - Agent capability matching
  - Dry-run mode (no execution)
  - Strict mode (fail on ambiguous routing)
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / "skills"
INDEX_FILE = SKILLS_DIR / "INDEX.yaml"


def load_index() -> Dict:
    with open(INDEX_FILE) as f:
        return yaml.safe_load(f)


def load_contract(skill_id: str) -> Optional[Dict]:
    index = load_index()
    entry = next((e for e in index["skills"] if e["id"] == skill_id), None)
    if not entry:
        return None
    contract_path = SKILLS_DIR / entry["contract"].lstrip("./")
    with open(contract_path) as f:
        return yaml.safe_load(f)


def score_triggers(contract: Dict, query: str) -> float:
    """Score how well a contract matches a query via triggers."""
    triggers = contract.get("routing", {}).get("triggers", [])
    if not triggers:
        return 0.0

    query_lower = query.lower()
    score = 0.0

    for trigger in triggers:
        trigger_lower = trigger.lower()
        if trigger_lower in query_lower:
            # Exact substring match
            score += 1.0
            # Bonus for word boundary
            if query_lower.startswith(trigger_lower) or query_lower.endswith(trigger_lower):
                score += 0.5

    return score


def score_phase_scope(contract: Dict, target_phase: Optional[str] = None) -> float:
    """Score based on phase_scope match."""
    if not target_phase:
        return 0.5  # Neutral if no phase specified

    scopes = contract.get("routing", {}).get("phase_scope", [])
    if target_phase in scopes:
        return 1.0
    return 0.0


def score_agent_compatibility(contract: Dict, agent: str) -> float:
    """Score based on agent compatibility."""
    agents = contract.get("compatibility", {}).get("agents", [])
    if agent in agents:
        return 1.0
    if not agents:
        return 0.5  # Neutral if no agent specified
    return 0.0


def route(query: str, agent: str = "local", phase: Optional[str] = None,
         strict: bool = False, dry_run: bool = False) -> List[Tuple[str, float, Dict]]:
    """
    Route a query to matching contracts.

    Returns sorted list of (skill_id, score, contract) tuples.
    Score is 0.0 to 3.0 (trigger + phase + agent).
    """
    index = load_index()
    candidates = []

    for entry in index["skills"]:
        skill_id = entry["id"]
        contract = load_contract(skill_id)
        if not contract:
            continue

        trigger_score = score_triggers(contract, query)
        phase_score = score_phase_scope(contract, phase)
        agent_score = score_agent_compatibility(contract, agent)

        total_score = trigger_score + phase_score + agent_score

        if total_score > 0:
            candidates.append((skill_id, total_score, contract))

    # Sort by score descending
    candidates.sort(key=lambda x: x[1], reverse=True)

    if strict and len(candidates) > 1:
        # Check for ambiguity: top 2 within 0.5 points
        if len(candidates) >= 2 and (candidates[0][1] - candidates[1][1]) < 0.5:
            raise ValueError(
                f"Ambiguous routing for query '{query}': "
                f"top candidates {candidates[0][0]} ({candidates[0][1]}) "
                f"and {candidates[1][0]} ({candidates[1][1]}) are too close. "
                f"Use a more specific query or disable strict mode."
            )

    if dry_run:
        return candidates

    # Filter out low scores for non-dry-run
    return [(sid, score, c) for sid, score, c in candidates if score >= 0.5]


def route_to_skill(query: str, agent: str = "local", phase: Optional[str] = None,
                   strict: bool = False, dry_run: bool = False) -> Optional[str]:
    """Route and return just the top skill_id, or None."""
    candidates = route(query, agent, phase, strict, dry_run)
    if not candidates:
        return None
    return candidates[0][0]


def print_routing(query: str, agent: str = "local", phase: Optional[str] = None,
                  strict: bool = False) -> None:
    """Print routing decision for a query."""
    print(f"Router: query='{query}' agent='{agent}' phase='{phase}' strict={strict}")
    print()

    try:
        candidates = route(query, agent, phase, strict, dry_run=False)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    if not candidates:
        print("  No matching contracts found.")
        return

    print(f"  Found {len(candidates)} matching contract(s):")
    for skill_id, score, contract in candidates:
        print(f"  [{score:.1f}] {skill_id}")
        print(f"       triggers : {contract.get('routing', {}).get('triggers', [])}")
        print(f"       phase_scope : {contract.get('routing', {}).get('phase_scope', [])}")
        print(f"       agents : {contract.get('compatibility', {}).get('agents', [])}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="VBB Phase Router")
    parser.add_argument("query", nargs="?", default=None,
                        help="Query string to route")
    parser.add_argument("--agent", default="local",
                        help="Target agent (default: local)")
    parser.add_argument("--phase", default=None,
                        help="Target phase scope (e.g. phase_0, closeout)")
    parser.add_argument("--strict", action="store_true",
                        help="Fail on ambiguous routing")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show routing without executing")
    parser.add_argument("--list", action="store_true",
                        help="List all contracts and their triggers")

    args = parser.parse_args()

    if args.list:
        print("=== VBB Skill Contracts ===\n")
        index = load_index()
        for entry in index["skills"]:
            contract = load_contract(entry["id"])
            if contract:
                print(f"{entry['id']}")
                print(f"  triggers  : {contract.get('routing', {}).get('triggers', [])}")
                print(f"  phase_scope: {contract.get('routing', {}).get('phase_scope', [])}")
                print(f"  agents    : {contract.get('compatibility', {}).get('agents', [])}")
                print()
        sys.exit(0)

    if not args.query:
        print("Usage: python vbb-phase-router.py <query> [--agent local] [--phase PHASE] [--strict] [--dry-run]")
        print("       python vbb-phase-router.py --list")
        sys.exit(1)

    print_routing(args.query, args.agent, args.phase, args.strict)