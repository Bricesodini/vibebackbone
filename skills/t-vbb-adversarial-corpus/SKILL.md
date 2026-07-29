---
name: t-vbb-adversarial-corpus
description: |
  Manage the adversarial regression corpus — creation, versioning, quarantine, and
  execution of entries. Use when a CONFIRMED adversarial finding must be registered as a
  permanent regression guard (mandatory per `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §9
  destination 6), or when the corpus must be executed against a code state.
  Keywords: corpus, regression guard, fails_before, passes_after, quarantine, adversarial
  corpus, finds-registry, tests/adversarial_corpus/.
context_role: corpus-steward
phase: "transverse"
status: "active"
version: "1.1"
adr: "0051"
adversarial_level: A2
canonical_authority: "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 + §5.2"
related_skills:
  - "2-vbb-adversarial-campaign (corpus source)"
  - "t-vbb-commit-ready (corpus gating)"
  - "0-vbb-standard (frontmatter discipline)"
---

# t-vbb-adversarial-corpus — Adversarial corpus steward

## ROLE & POSTURE

Manage the corpus of adversarial regression guards that prevents confirmed
findings from re-emerging after a fix. The corpus is the mandatory destination 6
of every CONFIRMED finding (per `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §9). The
corpus is *separate* from the regular `tests/` suite to preserve a clear chain of
custody between an attack and a regression guard.

Posture: steward, not judge. Register what the campaign confirmed; never soften a
finding to make registration easier.

## INPUT CONTRACT

| Input | Required | Source |
|---|---|---|
| Finding record | yes | `docs/runs/<slug>/findings/FIND-*.md` |
| Reproduction | yes | finding's `reproduction` block |
| Oracle | yes | finding's `oracle` field |
| Lock state | yes | finding's `non_regression_lock` |

## BLOCKING CONDITIONS

Abort registration and escalate when:

- `confidence` is not `CONFIRMED` — only confirmed findings are registrable;
- `tests/adversarial_corpus/` is absent from the working tree.

**Severity is never an exemption.** `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §9
destination 6 is "mandatory for every `CONFIRMED` finding, no exception", and
states that the matrix "applies regardless of severity". An earlier revision of
this skill listed `severity ∈ {S0, S1, S2}` as a blocking condition, which
silently exempted S3 and contradicted §9 (audit 2026-07-29, finding F18).

### Which entry kind applies

| Finding state | Lock present | Entry kind |
|---|---|---|
| `REMEDIATED`, `NON_REGRESSION_LOCKED`, `CLOSED_REMEDIATED` | `fails_before` and `passes_after` both `true` | `ACTIVE` regression guard |
| `ARBITRATED`, `DEFERRED`, or any open state | none — the defect is not fixed | `BEHAVIOUR_PIN` |

A `BEHAVIOUR_PIN` encodes the current, defective behaviour so it cannot change
silently: it fails the day the defect is fixed or drifts, forcing the finding to
be re-arbitrated and the entry rewritten as a real guard. A green pin means "the
known defect is still exactly as documented" — never "fixed".

Registering an `ACTIVE` guard without a valid lock remains forbidden: a missing
lock is a reason to register a pin, never to claim a remediation.

## SCOPE

Use when:

- A CONFIRMED finding must be registered as a permanent guard.
- The corpus must be executed against a code state (during pre-merge gate or
  campaign validation).
- A corpus entry must be quarantined (false alarm, promoted to canonical test,
  etc.).
- The corpus version must be bumped.

Do **not** use for:

- General unit tests (use `tests/` and standard tools).
- Documentation changes (corpus is regression for *behavior*).

## PROCESS

### 1. Verify the lock

Check every item of `## BLOCKING CONDITIONS` before touching the corpus.

### 2. Generate the corpus entry

Create `tests/adversarial_corpus/CORPUS-<id>.py` with:

```python
"""Corpus entry for <finding-id>.

Origin: <finding record path>
Severity: <severity>
Confidence: <confidence>
Oracle: <oracle>
"""

def test_<id>(<fixtures>):
    """Assert that <finding-id> cannot re-emerge."""
    # reproduction setup
    # assert that <oracle> fails_before
    # assert that <oracle> passes_after (post-remediation)
```

The test must be a *genuine oracle*, not a tautological assertion. It must
execute against the code state and produce a meaningful result. An entry that
asserts on the wording of a governance document rather than on behavior is not a
corpus entry.

### 3. Update the index

Append to `tests/adversarial_corpus/INDEX.md`:

```markdown
## CORPUS-<id>

- **Origin**: <finding-id>
- **Severity**: <severity>
- **Oracle**: <short description>
- **Added**: <ISO8601>
- **State**: ACTIVE | QUARANTINED | PROMOTED
```

### 4. Bump the corpus version

Update `tests/adversarial_corpus/VERSION` (semver: MAJOR for breaking test
surface, MINOR for new entry, PATCH for fixes).

### 5. Validate

Run `python -m pytest tests/adversarial_corpus/ -q` to ensure the new entry
executes and is consistent with the rest of the corpus.

### 6. Quarantine

A corpus entry may be quarantined when:

- The finding is later reclassified (e.g. CONFIRMED → REFUTED by further
  evidence).
- The finding is promoted to a canonical test (`tests/`) and the corpus entry is
  redundant.
- The reproduction is no longer possible (e.g. dependency removed).

Quarantine does not delete the entry; it sets `state: QUARANTINED` in the index
and skips execution during normal `pytest`. The entry remains for forensic
traceability.

### 7. Promotion

If the corpus entry is also useful as a canonical unit test, it can be *promoted*
to `tests/`. The canonical test becomes the primary guard; the corpus entry
becomes a `PROMOTED` historical reference.

## OUTPUT CONTRACT

| Output | Required | Destination |
|---|---|---|
| Corpus entry | yes | `tests/adversarial_corpus/CORPUS-<id>.py` |
| Corpus index update | yes | `tests/adversarial_corpus/INDEX.md` |
| Corpus version bump | conditional | `tests/adversarial_corpus/VERSION` |

## VERDICT RULES

1. **No CONFIRMED finding without a corpus entry.** This is a canonical
   obligation (`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §9, destination 6), carried
   by `tests/test_corpus_mandatory.py`.
2. **No corpus entry without a valid lock.** A `fails_before=true,
   passes_after=true` lock is required.
3. **No silent removal.** Quarantine is the only way to remove an entry from
   active execution.
4. **Corpus execution is distinct from `tests/`.** Per ADR 0051 and
   `docs/REFERENCE/pre-merge-gate.md` §5b, the corpus is a separately reported
   check.

### Enforcement boundary — read before relying on rule 1

`tools/vbb-adversarial-gate.py` does **not** verify rule 1. It checks that
`adversarial.corpus_version` is a non-empty string in the closeout frontmatter;
it never resolves a CONFIRMED finding to a corpus entry. An earlier revision of
this skill claimed the gate enforced the mandatory destination — it did not
(audit 2026-07-29, finding F16).

Do not infer coverage from this document. Verify which check carries the
obligation before treating rule 1 as enforced.

## Non-claim

This skill manages the corpus; it does not decide the severity or confidence of
findings. Those decisions remain with the campaign orchestrator
(`2-vbb-adversarial-campaign`) and the human reviewer.
