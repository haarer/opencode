---
name: release-note
description: Generate semantic release notes from git changes
---

# Release Note Skill

## Description
Generates Markdown release notes from git history by analyzing commit messages and categorizing changes into semantic groups: Features, Bug Fixes, Performance, Cleanup, and Cosmetic changes.

Uses the script `generate-release-notes.py` (stdlib Python 3, no dependencies).

## Usage

```bash
# Auto-detect last tag -> HEAD
python3 /root/.config/opencode/skills/release-note/generate-release-notes.py

# Specific ref (v1.0..HEAD)
python3 /root/.config/opencode/skills/release-note/generate-release-notes.py v1.0

# Explicit range
python3 /root/.config/opencode/skills/release-note/generate-release-notes.py v1.0..v2.0

# Pipe to file
python3 /root/.config/opencode/skills/release-note/generate-release-notes.py > notes.md
```

## How Categorization Works

Each commit is classified into one of these groups, checked in priority order:

| Category | Conventional Commit Prefix | Keyword Fallback |
|---|---|---|
| Features | `feat:`, `feature:` | add, new, implement, support, introduce, create, enable |
| Bug Fixes | `fix:`, `bugfix:`, `hotfix:` | fix, bug, crash, incorrect, wrong, error, issue, patch |
| Performance | `perf:` | performance, speed, fast, optimize, latency, slow |
| Cleanup | `refactor:`, `chore:`, `test:`, `ci:`, `build:` | cleanup, refactor, rename, move, remove, delete, simplif, deprecat, extract, restructur |
| Cosmetic | `style:`, `docs:`, `cosmetic:`, `typo:` | typo, cosmetic, format, lint, beautify, prettif, spelling |
| Other | (no match) | (no match) |

If a commit's subject starts with a conventional commit prefix (e.g., `feat(auth): add login`), it's matched immediately. Otherwise the subject + body are scanned for category keywords.

## Features

- **No dependencies** — uses Python stdlib only (`subprocess`, `re`, `argparse`, `datetime`)
- **Auto-range** — detects last git tag if no argument given
- **Issue linking** — `#123` and `GH-123` references are turned into Markdown links (supports GitHub, GitLab, Bitbucket)
- **Diff stats** — files changed, insertions/deletions are included
- **Merge skip** — merge commits (`--no-merges`) are excluded
- **Conventional commit** support with keyword fallback

## Output

Prints Markdown to stdout. Example:

```markdown
## v1.0..v2.0

**2026-05-24** · 12 commits · 5 files changed · +150/−30

### Features
- Add user avatar upload
- Implement dark mode toggle (#89)

### Bug Fixes
- Fix crash on empty search results (#92)

### Cleanup
- Refactor auth middleware to use async/await

### Cosmetic
- Fix typo in login error message

**Full Changelog**: https://github.com/owner/repo/compare/v1.0...v2.0
```
