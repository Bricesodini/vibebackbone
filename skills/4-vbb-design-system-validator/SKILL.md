---
name: 4-vbb-design-system-validator
description: |
  Pass 4/7 of the Vibebackbone front pipeline. Hard gate before visual identity work.
  Validates design-system structural readiness, token coverage, inline-style risks,
  and component reuse posture. Audits graphic centralization to enable easy modifications.
  In either GREENFIELD or LEGACY mode.
version: "3.2"
phase: 4
token_budget: high
subagent_eligible: false
mode_sensitive: false
---

# Design System Validator

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Use `4-vbb-front-pipeline-reference` as pipeline reference.

## ROLE & POSTURE

You are the hard gate before any visual identity.

You validate:

- structural readiness of the design system
- token coverage
- inline style risk
- component reusability
- **graphic centralization (who is the single source of truth)**

You must NOT:

- apply visual identity
- change flow or action hierarchy
- introduce patterns contrary to upstream passes

**Our graphic modification goal:**
When a user wants to modify a visual element, they must be able to:
1. Identify where the value is defined (SINGLE_SOURCE_OF_TRUTH)
2. Know all places where it is used
3. Know if the change is simple (token propagated) or risky (hardcoded)

## INPUT CONTRACT

**Required from passes 1–3:**

- [ ] `SURFACE_CARTOGRAPHY`
- [ ] `STATE_MATRIX`
- [ ] `CANONICAL_PATTERNS`
- [ ] `APPROVED_CHANGES`
- [ ] `CL_SCORE`

**Required from codebase:**

- [ ] source paths to inspect
- [ ] declared stack/framework
- [ ] design token file(s) (ex: tokens.css, theme.json, variables.scss…)

**If design tokens are missing → implicit LEGACY mode.**

## BLOCKING CONDITIONS

- If `PASS_STATUS: BLOCKED` from pass 3 → HARD STOP
- If `PASS_STATUS: PATCH_REQUIRED` with no human validation → STOP
- If source paths are missing → STOP
- **IF `SURFACE_CARTOGRAPHY` is absent → HARD STOP.** Message: "Surface cartography missing. Pass 1 must produce `SURFACE_CARTOGRAPHY` before pass 4 can execute."
- **IF `STATE_MATRIX` is absent → HARD STOP.** Message: "State matrix missing. Cannot validate token coverage without `STATE_MATRIX` from pass 1."

## SCOPE

### Modes

Declare:

- `GREENFIELD`
- `LEGACY`

### Included

- token coverage (spacing, typography, colors)
- inline styles
- hardcoded values
- overrides and duplications
- component reusability
- token coverage of changes validated in pass 3
- state token coverage
- **TOKEN_DEFINITION_MAP** — where each token is defined vs where it is used
- **PRIMITIVE_REGISTRY_CHECK** — primitive components centralized or redefined locally
- **SHELL_OVERRIDE_PATTERN** — do shells override primitives via tokens or inline
- **CENTRALIZATION_GAPS** — non-centralized values with impact and remediation order
- **CENTRALIZATION_ROADMAP** — action order to centralize progressively

### Excluded

- visual identity itself
- massive refactor
- flow changes

## PROCESS

1. Declare mode `GREENFIELD` or `LEGACY`.
2. **Centralization Audit (step 2 — always before scoring)**
   2a. TOKEN_DEFINITION_MAP:
       For each token identified in the design token file:
       - Where is it DEFINED (file + line)
       - Where is it USED (list of files/surfaces)
       - Report DUPLICATES: same token defined in multiple places
   2b. PRIMITIVE_REGISTRY_CHECK:
       - Primitive components (Button, Input, Card…): centralized in a file?
       - Redefined locally without registry reuse
       - Drift risk if changes not coordinated
   2c. SHELL_OVERRIDE_PATTERN:
       - Each surface from `SURFACE_CARTOGRAPHY` (Level 1):
         - Does it use tokens or hardcoded values?
         - Do shells define inline styles that bypass tokens?
       - Classification: token-based | mixed | hardcoded
   2d. CENTRALIZATION_GAPS:
       - List of NON-centralized surfaces/values
       - Migration impact: easy (< 5 files) | medium (5–15 files) | hard (> 15 files or breakage risk)
       - Priority by level: shells first, then business surfaces, then primitives
   2e. CENTRALIZATION_ROADMAP:
       - Suggested action order (simplest to most complex)
       - Risk if modification made before full centralization
       - Recommendation: start with shells (Level 1) before primitives (Level 3)
3. Check mode checklist (GREENFIELD / LEGACY).
4. Calculate `DS_SCORE` and `CENTRALIZATION_SCORE`.
5. List structural issues (excluding gaps already documented in 2d).
6. Define `TOKEN_COVERAGE` for pass 3 changes.
7. Define `DS_EXCEPTIONS`.
8. Document commands used or recommended.

## OUTPUT CONTRACT

Emit:
`pass-4-output.md`

Document must contain:

## 0. Context Mode

## 1. System Readiness Score

Key: `DS_SCORE`

## 2. Centralization Audit

Key: `CENTRALIZATION_AUDIT`

### 2.1 Token Definition Map

Key: `TOKEN_DEFINITION_MAP`

```
token-name | defined_in | used_in (count) | status
---------|------------|-----------------|-------
$color-primary | tokens/colors/brand.json:23 | 12 files | OK
$font-size-sm | tokens/typography/base.json:7 | 3 files | OK
$border-radius-lg | tokens/spacing/radii.json:12 | 1 file | OK
$bg-surface | tokens/colors/surface.json:3 | hardcoded in 6 components | DUPLICATE
...
```

**If DUPLICATES detected → immediately BLOCKED.**

### 2.2 Primitive Registry Check

Key: `PRIMITIVE_REGISTRY_CHECK`

- Primitive components found in registry: [list]
- Components redefined locally: [list + affected surfaces]
- Drift risk: [low/medium/high]

### 2.3 Shell Override Pattern

Key: `SHELL_OVERRIDE_PATTERN`

For each Level 1 surface:

```
SurfaceName | token-based | mixed | hardcoded | locations
Header | ✓ | — | — | header.module.css:12
SubHeader | — | ✓ | — | subheader.jsx:23,34
CardSurface | — | — | ✓ | card.module.css:8 (inline hardcoded bg)
ModalShell | ✓ | — | — | modal.module.css:15
```

Summary: X surfaces token-based | Y mixed | Z hardcoded

### 2.4 Centralization Gaps

Key: `CENTRALIZATION_GAPS`

```
Surface | Value | Current | Impact | Priority
-------|--------|---------|--------|----------
CardSurface | background | inline: #f0f0f0 | migration easy | P1
Trace | font-weight | inline: 700 | migration medium | P2
...
```

Summary: X gaps found | easy: N | medium: M | hard: K

### 2.5 Centralization Roadmap

Key: `CENTRALIZATION_ROADMAP`

Suggested order:
1. [Action 1] — token-based shells first (low impact, automatic propagation)
2. [Action 2] — business surfaces (medium impact)
3. [Action 3] — primitives (high impact, risky without test coverage)

Warning: Do not modify primitives before shells.

## 3. Refactor Suggestions

(Structural proposals excluding centralization gaps)

## 4. Tokenization Coverage for Pass 3 Changes

Key: `TOKEN_COVERAGE`

## 5. State Token Coverage

## 6. Exceptions

Key: `DS_EXCEPTIONS`

## 7. Commands Run / Recommended

## VERDICT RULES

- `PASS_STATUS: BLOCKED` if `DS_SCORE < 5`
- `PASS_STATUS: BLOCKED` if `TOKEN_DEFINITION_MAP` contains **DUPLICATES**
- `PASS_STATUS: CONDITIONAL` if `5 ≤ DS_SCORE < 7`
- `PASS_STATUS: CONDITIONAL` if `CENTRALIZATION_GAPS` ≥ 5 hardcoded values
- `PASS_STATUS: READY` if `DS_SCORE ≥ 7` and `TOKEN_DEFINITION_MAP` without DUPLICATES
- `CENTRALIZATION_SCORE` = % of token-based surfaces (target ≥ 80%)

`TOKEN_COVERAGE`, `DS_EXCEPTIONS`, `CENTRALIZATION_AUDIT` are frozen for passes 5–7.

To facilitate graphic modifications, `SURFACE_CARTOGRAPHY` + `TOKEN_DEFINITION_MAP`
form the reference point: the user can always answer "where is this value defined?"

## VALIDITY ENFORCEMENT

### HARD BLOCK CONDITIONS

Pass 4 output is INVALID (BLOCKED) if ANY of:
1. `TOKEN_DEFINITION_MAP` is empty or missing
2. `PRIMITIVE_REGISTRY_CHECK` is empty or missing
3. `CENTRALIZATION_GAPS` is empty or missing
4. `CENTRALIZATION_ROADMAP` is empty or missing
5. `DS_SCORE` is undefined or < 5
6. SURFACE_CARTOGRAPHY from pass 1 is not referenced
7. `SHELL_OVERRIDE_PATTERN` is empty or missing (required for traceability)

**Note:** SHELL_OVERRIDE_PATTERN is a sub-artifact of CENTRALIZATION_AUDIT but is mandatory for Pass 4 validity.

### REJECTION PATTERN DETECTION

If output contains ONLY:
  - "create Button", "new Badge", "design Token $color"
  - "migration to design system"
  - "primitive components"
WITHOUT referencing specific surfaces from SURFACE_CARTOGRAPHY
→ This is GENERIC_FRONTEND_RESPONSE
→ Return: PASS_STATUS: BLOCKED
→ Message: "Response lacks surface-specific context. Every token and component must be traced to a named surface from SURFACE_CARTOGRAPHY."

## CANONICAL EXAMPLES

### ✅ GOOD OUTPUT (Pass 4 valid)

```markdown
## 0. Context Mode
LEGACY

## 1. System Readiness Score
DS_SCORE: 6.5

## 2. Centralization Audit

### 2.1 Token Definition Map
TOKEN_DEFINITION_MAP:
| token | defined_in | used_in | status |
|-------|-----------|---------|--------|
| $color-brand | tokens/brand.json:12 | 8 files | OK |
| $bg-surface | tokens/surface.json:3 | 4 files | OK |
| $shadow-card | tokens/shadow.json:7 | hardcoded in 3 components | MISSING |

### 2.2 Primitive Registry Check
PRIMITIVE_REGISTRY_CHECK:
| primitive | registry | local | surfaces |
|-----------|----------|-------|----------|
| Button | components/Button | yes (TraceCard, HeaderShell) | drift risk: HIGH |
| Badge | components/Badge | no | — |

### 2.3 Shell Override Pattern
SHELL_OVERRIDE_PATTERN:
| Surface | token-based | mixed | hardcoded |
|---------|------------|-------|----------|
| HeaderShell | ✓ | — | — |
| TraceCard | — | ✓ | — |
| ModalShell | — | — | ✓ |

### 2.4 Centralization Gaps
CENTRALIZATION_GAPS:
| Surface | Value | Current | Impact | Priority |
|---------|-------|---------|--------|----------|
| TraceCard | bg | inline #f0f0f0 | medium (4 files) | P1 |
| ModalShell | shadow | hardcoded | easy (2 files) | P2 |

### 2.5 Centralization Roadmap
CENTRALIZATION_ROADMAP:
1. HeaderShell → token-based (already clean)
2. ModalShell → extract $shadow-card token (easy)
3. TraceCard → migrate bg to $bg-surface token (medium)
4. Button primitives → deduplicate from TraceCard (high risk)
```

### ❌ BAD OUTPUT (Pass 4 invalid — GENERIC_FRONTEND_RESPONSE)

```markdown
## Design System Audit

Tokens to create:
- $color-primary
- $spacing-md

Primitive components:
- Button
- Badge
- Card

Next step: migration to design system.
```

**Invalidation reason:** No surface referenced from SURFACE_CARTOGRAPHY.
No token → surface traceability.
**Result:** PASS_STATUS: BLOCKED + GENERIC_FRONTEND_RESPONSE