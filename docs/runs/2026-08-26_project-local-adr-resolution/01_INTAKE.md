---
run_id: "2026-08-26_project-local-adr-resolution"
phase: "01_INTAKE"
route: "STRUCTURED"
status: "READY_FOR_GATE"
agent: "codex"
adversarial_level: "A2"
---

# Project-local ADR resolution

adr_link: project:docs/adr/0021-ci-gate-enforcement.md

Fix the Core integration gate so local ADR references resolve from the active
project root, VBB references require explicit namespace, ambiguity fails
closed, and canonicalized paths remain within authorized roots. No Scol_FC
product, harness, test, schema, deployment, or OVH mutation is in scope.
