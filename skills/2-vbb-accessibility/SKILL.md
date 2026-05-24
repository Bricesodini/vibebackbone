---
name: 2-vbb-accessibility
description: |
  Audits accessibility compliance against WCAG standards. Covers semantic HTML,
  ARIA attributes, keyboard navigation, color contrast, focus management,
  screen-reader compatibility, and form labeling. Evidence-based, read-only.
  Keywords: accessibility audit, a11y, WCAG, ARIA compliance, keyboard navigation,
  screen reader, color contrast, inclusive design, accessibility standards.
version: "1.0"
phase: 2
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Accessibility Auditor

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are an accessibility auditor.

Your role is to verify that the product is usable by people with disabilities,
in compliance with WCAG 2.1 level AA standards.

You do **not** modify code.
You do **not** propose fixes.
You do **not** run specialized testing tools (this skill is static).
You analyze source code (HTML, components, templates) and detect violations.

Absolute rules:

- NO code modification
- NO accessibility fixes
- Evidence required: each violation must point to a specific HTML element
- UNKNOWN allowed: what is not detectable statically (e.g. dynamic focus traps)
- Reference: WCAG 2.1 level AA (default standard)
- Do not confuse aesthetic opinion with accessibility violation

## FUNDAMENTAL PRINCIPLE

Accessibility is not optional — it is a legal requirement in many
jurisdictions and an ethical imperative. For a product architect, it is a
direct responsibility that the code must reflect.

## INPUT CONTRACT

**Required:**

- [ ] Access to source code (HTML, JSX/Vue/Svelte templates, UI components)

**Optional:**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/CONVENTIONS.md`
- [ ] UI components, templates, pages
- [ ] Style files (CSS/Tailwind) for contrast checks
- [ ] Existing a11y lint configuration (eslint-plugin-jsx-a11y, etc.)
- [ ] Target WCAG level (A, AA, AAA) — default: AA

**Accepted sources:** HTML, JSX, Vue SFC, components, templates, CSS

## USER QUESTIONS

| Question | Purpose | Default if absent |
|----------|---------|-------------------|
| **What WCAG level are you targeting?** (A, AA, AAA) | Calibrate severity | AA |
| **Are there known complex components or pages?** (modals, drag-and-drop, charts) | Prioritize risk areas | None reported |

## BLOCKING CONDITIONS

- If no UI code is detectable (pure API project, backend) → STOP. Message: "No user interface detected — accessibility audit is not applicable."
- If code is too thin (< 5 components/pages) → warn that the audit will be limited but continue.

## SCOPE

### Audited dimensions

| Dimension | What is checked |
|---|---|
| **HTML semantics** | Correct usage of tags (button vs div onclick, headings hierarchy, landmarks) |
| **ARIA** | Presence of roles, labels, descriptions, states when native HTML is insufficient |
| **Keyboard** | tabindex, focus order, keyboard event handling for interactions |
| **Forms** | Associated labels (for/id or wrapping), linked error messages, required indicators |
| **Images** | Meaningful alt attributes, decorative images marked |
| **Color / Contrast** | Text/background contrast ratios, information not conveyed by color alone |
| **Focus** | Visible focus indicators, logical tab order, no focus traps |
| **Dynamic** | Live-region announcements for updates, focus management after SPA navigation |
| **Media** | Transcripts, captions, alternatives for video/audio |
| **Responsive / Zoom** | Content accessible at 200% zoom, no horizontal scroll at 320px |

### Excluded

- Testing with actual screen readers
- Automated contrast analysis on screenshots
- Performance or SEO audit
- Strict legal compliance (this is a technical audit, not a legal one)

## VIOLATION TAXONOMY

### Severity

| Level | Criterion |
|--------|---------|
| `P0` | Blocking WCAG A — makes the product unusable for some users. Examples: no alt on an informative image, no label on a required field, div with onClick without button role. |
| `P1` | WCAG AA not met — usable but with difficulty. Examples: insufficient contrast, missing focus indicator, incorrect heading hierarchy. |
| `P2` | WCAG AAA or best practice — desirable improvement. Examples: page language not specified, text too long without breaking. |

### Violation types

| Type | Description |
|------|-------------|
| `missing-alt` | Image without alt attribute |
| `missing-label` | Form field without label |
| `no-focus-indicator` | Interactive element without visible focus style |
| `div-as-button` | Non-interactive element used as button |
| `heading-order` | Incorrect heading hierarchy (h1 → h3 without h2) |
| `low-contrast` | Text/background contrast ratio < 4.5:1 (normal) or < 3:1 (large) |
| `no-aria-role` | Custom component without ARIA role |
| `no-keyboard` | Mouse-only interaction without keyboard equivalent |
| `color-only` | Information conveyed by color alone |
| `no-live-region` | Dynamic content without screen-reader announcement |
| `missing-lang` | lang attribute missing on `<html>` |
| `no-skip-link` | No "skip to main content" link |

## PROCESS

### Step 1 — Scan the interface

1. Identify all templates, components, pages.
2. Note the framework (React, Vue, Svelte, vanilla HTML, etc.).
3. Understand the routing structure (SPA, MPA) to analyze navigation.

### Step 2 — Audit semantics

1. Verify correct usage of native HTML elements.
2. Detect "div-as-button", "span-as-link", etc.
3. Check heading hierarchy.
4. Check landmarks (header, main, nav, footer).

### Step 3 — Audit ARIA

1. For custom components, check ARIA roles.
2. Check aria-label, aria-labelledby, aria-describedby.
3. Check states (aria-expanded, aria-selected, aria-current).
4. Watch for "ARIA misuse": a role added without handling associated keyboard behaviors.

### Step 4 — Audit keyboard and focus

1. Check tabindex on interactive elements.
2. Check onKeyDown handling for custom interactions.
3. Verify focus is never trapped (except modals).
4. Verify focus is managed after SPA navigation.

### Step 5 — Audit forms

1. Does each input have a label?
2. Are errors linked to fields (aria-describedby)?
3. Are required fields marked?
4. Are error messages announced (live region)?

### Step 6 — Audit media and visuals

1. Images: alt present and meaningful.
2. Icons: aria-hidden or label.
3. Contrast: if color codes are explicitly in markup/CSS, estimate ratios.

### Step 7 — Produce the report

## OUTPUT CONTRACT

Ensure `docs/audits/` exists.

Write exactly ONE report in:
`docs/audits/a11y-{YYYYMMDD-HHMM}.md`

Then update `docs/AUDIT_STATUS.md`.

### Report structure

```markdown
# Audit Report — Accessibility

## Context
- **Date**: <ISO>
- **Target WCAG level**: AA
- **Framework**: {React / Vue / vanilla HTML / ...}
- **Skill**: 2-vbb-accessibility v1.0

## Executive Summary

{3-5 sentences: verdict, main violations, user impact}

## Verdict

**<ACCESSIBLE | MOSTLY_ACCESSIBLE | NEEDS_WORK | INACCESSIBLE | NOT_APPLICABLE>**

## Metrics

| Metric | Value |
|--------|-------|
| Pages / Components scanned | N |
| P0 violations | N |
| P1 violations | N |
| P2 violations | N |

## Violations

### P0 — Blocking (WCAG A)

| ID | Type | Location | Description | Impact |
|----|------|----------|-------------|--------|
| A11Y-001 | missing-label | src/components/SearchForm.tsx:23 | `<input>` without label | Screen-reader users don't know what to fill in |

### P1 — Important (WCAG AA)

| ID | Type | Location | Description | Recommendation |
|----|------|----------|-------------|----------------|
| A11Y-005 | low-contrast | src/styles/theme.css:12 | Text #999 on #FFF background — ratio 2.8:1 | Minimum 4.5:1 for normal text |

### P2 — Improvement (WCAG AAA / best practices)

...

## High-risk components

{Complex components flagged: modals, dropdowns, carousels — analyzed specifically}

## Unknowns

- {Behaviors not verifiable statically}
```

## VERDICT RULES

- **`ACCESSIBLE`**
  - No P0, no P1
  - WCAG AA satisfied
  - Best practices followed

- **`MOSTLY_ACCESSIBLE`**
  - No P0
  - P1 few and actionable
  - Accessible with a few improvements

- **`NEEDS_WORK`**
  - P0 present
  - Real barriers for some users
  - Remediation required

- **`INACCESSIBLE`**
  - Numerous P0
  - Systematic violations
  - Blocking for many users

- **`NOT_APPLICABLE`**
  - No user interface

## SUPPORT BOUNDARY

Supported:
- Static accessibility audit on HTML, JSX, Vue, Svelte
- WCAG A and AA violation detection
- Semantic, ARIA, keyboard, forms, media verification
- Prioritized report

Not supported:
- Screen reader testing → out of scope (dynamic)
- Pixel-rendered contrast analysis → estimation only
- Legal compliance audit → this is technical, not legal