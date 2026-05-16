# Contributing to vibebackbone

Thank you for your interest in contributing! vibebackbone is a collaborative project, and contributions are welcome.

## Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to contribute

### Reporting bugs

- Use GitHub Issues to report bugs
- Include a clear title and description
- Provide a minimal example to reproduce the issue
- Specify your environment (OS, node version, etc.)

### Suggesting enhancements

- Use GitHub Issues to suggest enhancements
- Provide clear motivation and examples
- Consider how the enhancement fits with vibebackbone's philosophy

### Contributing skills

vibebackbone accepts contributions of new skills! Each skill must:

1. **Follow the skill template** — See `skills/0-vbb-guide/SKILL.md`
2. **Have a SKILL.md file** with:
   - YAML frontmatter (name, description, version, phase, token_budget)
   - Clear ROLE & POSTURE
   - INPUT CONTRACT (preconditions)
   - BLOCKING CONDITIONS (failure modes)
   - SCOPE (boundaries)
   - PROCESS (step-by-step)
   - OUTPUT CONTRACT (deliverables)
   - VERDICT RULES (success criteria)

3. **Follow naming convention** — `[phase]-vbb-[descripteur-kebab-case]`
   - Phase: 0, 1, 2, 3, 4, or t (transverse)
   - Example: `2-vbb-security-audit`

4. **Test thoroughly** — Validate INPUT CONTRACT and BLOCKING CONDITIONS

### Pull request process

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-skill`
3. Make your changes
4. Follow conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
5. Push to your fork
6. Create a Pull Request with:
   - Clear title and description
   - Link to related issue (if any)
   - Evidence of testing

### Commit message format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

**Example**:
```
feat(skill): Add 2-vbb-api-auditor for API design review

Implements API design audit skill with:
- OpenAPI validation
- REST principles checking
- Performance anti-patterns detection

Closes #42
```

## Development workflow

1. **Clone the repo**
   ```bash
   git clone https://github.com/vibebackbone/vibebackbone.git
   cd vibebackbone
   ```

2. **Read the documentation**
   - AGENTS.md — Operational grammar
   - SYSTEM.md — Runtime behavior
   - skills/vibebackbone/docs/PILOTAGE.md — Full governance

3. **Create your skill**
   ```bash
   mkdir skills/[phase]-vbb-[name]
   touch skills/[phase]-vbb-[name]/SKILL.md
   ```

4. **Follow the template**
   - Copy structure from `skills/0-vbb-guide/SKILL.md`
   - Fill in all sections
   - Test with example inputs

5. **Test your skill**
   - Verify INPUT CONTRACT
   - Test BLOCKING CONDITIONS
   - Validate OUTPUT CONTRACT

6. **Submit PR**
   - Include skill documentation
   - Add test evidence
   - Reference related issues

## Governance

vibebackbone follows **vibecodex v2.0** governance:

- **Phase [0]** — Readiness (scope-freeze, audit-readiness)
- **Phase [1]** — Structure (conventions, tech-debt, dependency-mapper)
- **Phase [2]** — Audits (security, integrity, ops)
- **Phase [3]** — Consolidation (risk-register)
- **Phase [4]** — Enhancement (UX, performance, advanced skills)
- **Phase [t]** — Transverse (utilities, cross-cutting concerns)

New skills should fit within this framework.

## Support

- **Questions** — GitHub Discussions
- **Bugs** — GitHub Issues
- **Ideas** — GitHub Issues (with `enhancement` label)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to vibebackbone! 🙌
