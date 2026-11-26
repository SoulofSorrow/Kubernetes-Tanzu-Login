---
date: 2026-11-25
type: docs
scope: docs, agent tooling
files: [AGENTS.md, CLAUDE.md, .claude/settings.json, .claude/skills/add-cluster-config/SKILL.md, .claude/skills/document-change/SKILL.md, docs/README.md, docs/architecture.md, docs/changes/2026-11-25-ai-ready-docs.md, README.md]
breaking: false
---
# Agent-ready documentation and project skills

## Context

- The repository had no `docs/` folder and no instructions for AI coding
  agents. Knowledge lived in the German `README.md` and `start.py`.
- Goal: an agent knows the login flow, the password handling rule and which
  commands have side effects.

## Change

- `docs/README.md`: index of docs and change records, maintenance rules.
- `docs/architecture.md`: files, code map, login flow, `config.yaml` format,
  external requirements.
- `AGENTS.md`: agent instructions (read order, commands, definition of done,
  hard rules, language table, skill list).
- `CLAUDE.md`: imports `AGENTS.md`, Claude Code notes.
- `.claude/settings.json`: allows an `ast.parse` syntax check of `start.py`
  and `make help|check-git|info`; asks before `python3 start.py`,
  `kubectl-vsphere`, `make clean|setup|all|install-*|set-git-local` and
  `git push`; denies reading `.env` and `~/.kube/**`.
- `.claude/skills/`: `add-cluster-config`, `document-change`.
- `README.md`: German "Dokumentation" section linking `docs/` and `AGENTS.md`.

## Decisions

- Syntax check via `ast.parse` instead of `py_compile`: writes no
  `__pycache__/` (the repository has no `.gitignore`).
- No build or release skill: building `start.exe` is not defined in the
  repository.
- `.dockerignore` not changed: the repository builds no Docker image.

## Usage / Verification

```bash
python3 -m json.tool .claude/settings.json
python3 -c "import ast; ast.parse(open('start.py').read())"
```

## Follow-ups

- Missing standard files: `CHANGELOG.md`, `CONTRIBUTING.md`,
  `.pre-commit-config.yaml`, `README.de.md` (`README.md` is German; an
  English `README.md` is missing), `.editorconfig`, `.gitignore`;
  no `requirements.txt`.
- `Makefile` has no build, test or tag targets.
- `generate_login_command()` contains the literal `<domain>` and runs with
  `shell=True`: the shell treats `<domain>` as redirections, so the command
  does not work as written; the username is interpolated unquoted into a
  shell command (injection risk).
- `--insecure-skip-tls-verify` is always set.
- `delete_kubeconfig()` catches `CalledProcessError` without `check=True`, so
  failures are never reported.
- `install.txt` names the pip package `piyaml` (likely `PyYAML`).
- `start.exe` (about 7 MB binary) is committed without a documented build.
