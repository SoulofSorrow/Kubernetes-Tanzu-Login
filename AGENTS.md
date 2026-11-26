# AGENTS.md

Instructions for AI coding agents working in this repository. Tool-agnostic;
`CLAUDE.md` imports this file.

## Project

Kubernetes-Tanzu-Login: small PyQt5 desktop GUI (`start.py`, Python 3,
dependencies `PyQt5`, `PyYAML`) that logs in to VMware Tanzu Kubernetes
clusters via `kubectl-vsphere login`, using namespaces, servers and cluster
names from `config.yaml`. A second button deletes `~/.kube`. UI texts and
`README.md` are German. License GPL-3.0 (`LICENSE.md`).

## Read first

1. `docs/README.md` (index).
2. `docs/architecture.md` for the login flow, `config.yaml` format and
   external commands.

## Commands

```bash
python3 -c "import ast; ast.parse(open('start.py').read())"   # syntax check, writes nothing
python3 start.py                 # start the GUI (needs PyQt5, PyYAML, kubectl-vsphere)
```

Dependency hints are in `install.txt` (`brew reinstall pyqt@5`, a pip
install). No `requirements.txt`, tests, linter config or CI exist. How
`start.exe` is built is not defined in the repository.

## Definition of done

- The `ast.parse` syntax check from "Commands" succeeds.
- `docs/architecture.md` updated when flow, config format or commands change.
- New file `docs/changes/YYYY-MM-DD-<slug>.md` (template in
  `.claude/skills/document-change/SKILL.md`), listed in `docs/README.md`.
- User-visible behaviour changed: update `README.md` (German).

## Hard rules

- The password is passed only through the environment variable
  `KUBECTL_VSPHERE_PASSWORD` and removed after a successful login. Never log,
  display or write the password; never put it on the command line.
- `config.yaml` holds only server addresses and names; never add usernames,
  passwords or tokens.
- `load_cluster_config()` reads `config.yaml` next to `start.py`; keep the
  structure `<namespace>: {server, cluster_names}`.
- `delete_kubeconfig()` removes `~/.kube` recursively; keep the confirmation
  dialog.
- Do not run `python3 start.py` or `kubectl-vsphere` unless the user asks.
- Do not modify or rebuild `start.exe` unless the user asks.
- No emojis in code, logs or docs.

## Language

| Artifact | Language |
| --- | --- |
| UI texts and messages in `start.py`, `README.md` | German (existing convention) |
| Code comments | German in existing code; English for new comments |
| `docs/`, `AGENTS.md`, `CLAUDE.md`, skills, commit messages | English |

Commits: imperative, no tool attribution trailers.

## Project skills

Located in `.claude/skills/<name>/SKILL.md`.

| Skill | Use for |
| --- | --- |
| `add-cluster-config` | New namespace, server or cluster in `config.yaml` |
| `document-change` | Writing the `docs/changes/` record |
