# Installation & Distribution — vibebackbone

Guide for distributing vibebackbone and consuming it in target projects.

## For repo owners (vibebackbone itself)

vibebackbone is distributed via:

- **GitHub** (source, OSS)
  ```bash
  git clone https://github.com/vibebackbone/vibebackbone.git
  ```

- **npm** (future: `npm install vibebackbone`)
  ```bash
  npm install vibebackbone
  ```

- **Copy** (self-contained within consumer projects)
  ```bash
  cp -r vibebackbone/ /path/to/my-project/
  ```

**Current approach** : Use git clone or copy to consumer projects.

---

## For consumer projects

A consumer project is a real application (Node.js, Python, Go, etc.) that uses vibebackbone for operational governance.

### Fresh installation

#### Option A: Auto-detect provider (recommended)

```bash
# Clone vibebackbone (if not present)
git clone https://github.com/vibebackbone/vibebackbone.git
cd vibebackbone

# Run universal installer (auto-detects provider)
bash init.sh --auto
```

The installer detects your provider from environment (VBB_PROVIDER env var or provider-specific files).

#### Option B: Explicit provider selection

```bash
bash vibebackbone/init.sh --provider claude
# or
bash vibebackbone/init.sh --provider pi
# or
bash vibebackbone/init.sh --provider opencode
# or
bash vibebackbone/init.sh --provider codex
```

#### Option C: Interactive selection

```bash
bash vibebackbone/init.sh
# Prompts: Which provider? [1-4]
```

### Existing project (add vibebackbone)

If you already have a project and want to add vibebackbone:

```bash
# Clone/link vibebackbone (if not present)
git clone https://github.com/vibebackbone/vibebackbone.git
# or
npm install vibebackbone

# Run installer (detects existing PROJECT_MODE.md, respects it)
bash vibebackbone/init.sh --provider claude
```

The installer will:
- Detect `docs/PROJECT_MODE.md` exists → use **existing** context
- Preserve your existing configuration
- Add missing session templates (SESSION.md, AUDIT_STATUS.md, audits/)

### What the install scripts do

Each provider's `init-[provider].sh` script:

1. **Creates provider-specific config**
   - `.claude/settings.json` (Claude Code)
   - `.pi/taskplane.json` (Pi)
   - `.opencode/config.json` (OpenCode)
   - `.codex/env.sh` (Codex)

2. **Initializes PROJECT_MODE.md (if fresh)**
   - Declares mode: CONSUMER
   - Declares provider: pi|claude|opencode|codex
   - Sets governance version: v1.0

3. **Creates session memory templates**
   - `docs/SESSION.md` — Local resumption context (gitignored)
   - `docs/AUDIT_STATUS.md` — Local audit dashboard (gitignored)
   - `docs/audits/` — Local reports directory (gitignored)

4. **Updates .gitignore**
   - Adds entries to ignore local session artifacts
   - Prevents accidental commit of SESSION.md, audit reports, secrets

---

## Universal installer (init.sh)

The mutualized installer orchestrates the entire process:

```bash
bash init.sh [OPTIONS]

Options:
  --provider [provider]  Explicit provider: pi|claude|opencode|codex
  --auto                 Auto-detect from environment
  --help                 Show help
```

### Detection logic

**Provider detection:**
1. Check `--provider` flag
2. Check `VBB_PROVIDER` environment variable
3. Check for provider-specific files (.pi/, .claude/, .opencode/, .codex/)
4. Prompt user interactively

**Context detection:**
1. Check `VBB_CONTEXT` environment variable
2. Check if `docs/PROJECT_MODE.md` exists
   - Exists → use "existing" context
   - Missing → use "fresh" context

### Example workflows

**Fresh Claude Code project:**
```bash
bash vibebackbone/init.sh --provider claude
# Creates .claude/settings.json, docs/PROJECT_MODE.md, session templates
```

**Existing Pi project:**
```bash
bash vibebackbone/init.sh --provider pi
# Detects docs/PROJECT_MODE.md, preserves it, adds missing templates
```

**Auto-detect from VBB_PROVIDER env:**
```bash
export VBB_PROVIDER=codex
bash vibebackbone/init.sh --auto
# Detects provider from env, initializes as Codex consumer
```

---

## Directory structure post-installation

```
my-project/
├── docs/
│   ├── PROJECT_MODE.md          # Mode: CONSUMER, provider: [your choice]
│   ├── SESSION.md               # (gitignored, local memory)
│   ├── AUDIT_STATUS.md          # (gitignored, local dashboard)
│   ├── audits/                  # (gitignored, session reports)
│   └── ARCHITECTURE.md          # Your app architecture
│
├── vibebackbone/                # Clone of vibebackbone
│   ├── skills/                  # 57 skills (shared)
│   ├── prompts/                 # 24 prompts (shared)
│   ├── providers/               # Provider integration layer
│   ├── AGENTS.md                # Operational grammar (shared)
│   ├── SYSTEM.md                # Pi runtime (shared)
│   ├── CLAUDE.md                # Claude entry point (shared)
│   ├── README.md                # Catalog (shared)
│   └── ...
│
├── .claude/                     # Claude Code config (if using Claude)
│   └── settings.json
│
├── .pi/                         # Pi config (if using Pi)
│   ├── taskplane.json
│   └── agents/
│
├── .opencode/                   # OpenCode config (if using OpenCode)
│   └── config.json
│
├── .codex/                      # Codex config (if using Codex)
│   └── env.sh
│
├── src/                         # Your application code
├── tests/                       # Your tests
├── .gitignore                   # Includes docs/SESSION.md, docs/AUDIT_STATUS.md, etc.
└── [your other files]
```

---

## Shared state across providers

If running multiple providers on the same project:

**Shared files** (all providers read):
- `docs/PROJECT_MODE.md` — Mode declaration (CONSUMER, DISTRIBUTION)
- `docs/SESSION.md` — Active task context (resume point)
- `skills/`, `prompts/`, `AGENTS.md`, `SYSTEM.md` — Core governance

**Provider-specific** (not shared):
- `.claude/`, `.pi/`, `.opencode/`, `.codex/` — Config isolation
- Session memory location (SESSION.md is shared location)

Example: Pi agent and Claude Code developer on same project
- Both read `docs/PROJECT_MODE.md` → Identify CONSUMER mode
- Both read `docs/SESSION.md` → Resume from same point
- Pi uses `.pi/taskplane.json`, Claude uses `.claude/settings.json` → No conflict

---

## Updating vibebackbone

### Git clone method

```bash
cd vibebackbone/
git fetch origin
git checkout main
git pull
```

Verify compatibility:
- Check `CHANGELOG.md` for breaking changes
- Re-run `init.sh` if major version bump (v1.x → v2.x)

### npm method

```bash
npm update vibebackbone
```

or

```bash
npm install vibebackbone@latest
```

---

## Troubleshooting

### "init.sh not found"

Ensure you're in the directory containing `init.sh` or use full path:
```bash
bash /path/to/vibebackbone/init.sh --provider claude
```

### "Provider not detected"

Set explicit provider:
```bash
bash init.sh --provider pi
```

or set environment variable:
```bash
export VBB_PROVIDER=claude
bash init.sh --auto
```

### "docs/PROJECT_MODE.md already exists"

The installer respects existing PROJECT_MODE.md (preserves your configuration). If you want to re-initialize:
```bash
rm docs/PROJECT_MODE.md
bash init.sh --provider [provider]
```

### ".gitignore conflicts"

If `.gitignore` already exists, the installer appends to it. Check for duplicates:
```bash
grep "docs/SESSION.md" .gitignore | wc -l
```

If multiple entries, manually clean up.

### "Multi-provider conflict"

Each provider has isolated config (`.pi/`, `.claude/`, etc.). As long as each provider writes to its own directory, there's no conflict.

If sharing state causes issues, check `docs/PROJECT_MODE.md` to see which mode (CONSUMER, DISTRIBUTION) is declared.

---

## Multi-provider examples

### Pi + Claude Code on same project

```bash
# Install for Pi
bash vibebackbone/init.sh --provider pi

# Later, install for Claude Code
bash vibebackbone/init.sh --provider claude
```

Result:
- Both `.pi/` and `.claude/` exist
- Both read `docs/PROJECT_MODE.md` and `docs/SESSION.md`
- No conflict because config is isolated

### Fresh project with auto-detection

```bash
# Set VBB_PROVIDER in CI/CD or shell
export VBB_PROVIDER=codex

# Run universal installer
bash vibebackbone/init.sh --auto
```

---

## Support & documentation

- **Skills execution** → See `vibebackbone/README.md` (57 skills catalog)
- **Triage rules** → See `vibebackbone/AGENTS.md`
- **Provider setup** → See `vibebackbone/providers/[provider]/INTEGRATION.md`
- **Governance** → See `vibebackbone/skills/vibebackbone/docs/PILOTAGE.md`
- **Session memory** → See `docs/SESSION.md` (local)
- **Audit dashboard** → See `docs/AUDIT_STATUS.md` (local)

---

**Last updated** : 2026-05-16
**vibebackbone version** : v1.0.0
**Installation method** : Universal installer (init.sh) + 4 targeted installers
