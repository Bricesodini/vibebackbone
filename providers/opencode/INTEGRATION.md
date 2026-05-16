# OpenCode Integration

## Quick start

```bash
bash init-opencode.sh
```

Then follow the OpenCode standard for skill distribution.

## Configuration

1. **Read** `/README.md` — Catalog of 57 skills
2. **Reference** `/AGENTS.md` — Operational triage
3. **Reference** `CONTRIBUTING.md` — Contribution guidelines
4. **Reference** `LICENSE` — MIT license terms

## OpenCode + vibebackbone

vibebackbone is designed for **distribution as OpenCode**:

- **Skills** are open-source, contribute via GitHub
- **Prompts** are public templates, reusable across projects
- **Governance** is transparent: AGENTS.md, SYSTEM.md, PILOTAGE.md
- **Community** can fork, extend, and contribute back

## Distribution workflow

1. **Fork** vibebackbone repository on GitHub
2. **Create branch** for your skill or feature
3. **Follow convention** : `skills/[phase]-vbb-[name]/SKILL.md` for new skills
4. **Include tests** : Validate skill INPUT CONTRACT and BLOCKING CONDITIONS
5. **Submit PR** with reference to issue and CONTRIBUTING.md guidelines

## Skill contribution standards

Each skill must include:

- `SKILL.md` with YAML frontmatter (name, description, version, phase, token_budget)
- `ROLE & POSTURE` section (what the skill does)
- `INPUT CONTRACT` (preconditions, required artifacts)
- `BLOCKING CONDITIONS` (failure modes)
- `SCOPE` (boundaries, non-objectives)
- `PROCESS` (step-by-step execution)
- `OUTPUT CONTRACT` (deliverables)
- `VERDICT RULES` (how to evaluate success)

Reference: `/skills/0-vbb-guide/SKILL.md` for template.

## Contributing

See `/CONTRIBUTING.md` for:
- Code of conduct
- Contribution process
- Conventional commit format
- Review criteria
- Release process

## Governance

vibebackbone follows **Codex v2.0** governance:

- Phase [0] : scope-freeze, audit-readiness
- Phase [1] : structure (dependency-mapper, conventions, tech-debt)
- Phase [2] : audits (security, integrity, ops)
- Phase [3] : consolidation (risk-register)

Distribution model: **Core skills** (DISTRIBUTION mode) + **Consumer projects** (CONSUMER mode).

## License

MIT License — freely usable, modifiable, and distributable.

See `/LICENSE` for full terms.

## Community

- **Issues** : GitHub issues for bugs and feature requests
- **Discussions** : GitHub discussions for ideas and questions
- **PR** : Contributions via pull requests
- **Version tags** : Semantic versioning (v1.0.0, v1.1.0, v2.0.0)

## Multi-provider interoperability

vibebackbone works seamlessly with:
- **Pi (Pinokio)** — Agent orchestration
- **Claude Code** — IDE integration
- **Codex** — Governance model
- **OpenCode** — Distribution standard (this mode)

Skills written for OpenCode work across all providers.

## Troubleshooting

**"My skill doesn't follow the template"** → Reference `/skills/0-vbb-guide/SKILL.md` and restructure.

**"How do I test my skill?"** → Implement INPUT CONTRACT checks and BLOCKING CONDITIONS. Test on example consumer projects.

**"Should I publish my skill to npm?"** → OpenCode supports npm distribution (future). For now, use git clone.

**"Versioning strategy?"** → Use semantic versioning (MAJOR.MINOR.PATCH). See `CHANGELOG.md` for examples.

## Support

- **Skill development** → See `CONTRIBUTING.md` § Skill standards
- **Governance questions** → See `skills/vibebackbone/docs/PILOTAGE.md`
- **Distribution** → See `docs/INSTALLATION.md`
